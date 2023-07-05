#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
import plotly.graph_objects as go
import numpy as np
import json


# 获取token名称和hash
def get_token():
  url = "https://api.gmx.io/tokens"
  response = requests.get(url)
  data = response.json()
  data = pd.json_normalize(data)
  data['data.address'] = data['data.address'].str.lower()
  symbol = data.set_index('data.address')
  return symbol

def get_actions():
  url = 'https://api.gmx.io/' + 'actions'
  response = requests.get(url,params={'after':'0x7399c39ff0b393777396b927477373ba8336bb62c57080e4b000bd29e6a0e6e1'})
  data = pd.json_normalize(response.json())
  data['time'] = pd.to_datetime(data['data.timestamp'], unit='s')
  return data



def fetch_stats(query,name):
    url = 'https://subgraph.satsuma-prod.com/3b2ced13c8d9/gmx/gmx-arbitrum-stats/api'
    headers = {'Content-Type': 'application/json'}

    request_json = {'query': query}
    response = requests.post(url, headers=headers, data=json.dumps(request_json))
    data = response.json()

    if 'errors' in data:
        error_message = data['errors'][0]['message']
        raise Exception(f"GraphQL query failed: {error_message}")
    data = data['data'][name]
    data = pd.DataFrame(data)
    data['time'] = pd.to_datetime(data['id'], unit='s') 
    return data


def get_glp(end_day):
  end_day = int(pd.to_datetime(end_day,format = '%Y%m%d%H').timestamp())
  glpquery = f'''
  {{
    hourlyGlpStats(
      first: 10000
      orderBy: id
      orderDirection: desc
      where: {{ id_gte: 0, id_lte: {end_day} }}
      subgraphError: allow
    ) {{
      id
      aumInUsdg
      glpSupply
      __typename
    }}
  }}
  '''
  # 调用函数并打印结果
  glp = fetch_stats(glpquery, 'hourlyGlpStats')
  # 转换为dataframe
  glp = pd.DataFrame(glp)
  glp['time'] = pd.to_datetime(glp['id'], unit='s')
  glp = glp[glp['glpSupply'] != '0']
  glp['price'] = glp['aumInUsdg'].astype(float) / glp['glpSupply'].astype(float)
  return glp

def get_fee(end_day):
  # str to tp int
  end_day = int(pd.to_datetime(end_day,format = '%Y%m%d%H').timestamp())
  feesquery = f'''{{
    hourlyFees(
      first: 10000
      orderBy: id
      orderDirection: desc
      where: {{ id_gte: 0, id_lte: {end_day} }}
      subgraphError: allow
    ) {{
      id
      margin
      marginAndLiquidation
      swap
      mint
      burn
      __typename
    }}
  }}'''
  # 调用函数并打印结果
  fees = fetch_stats(feesquery, 'hourlyFees')
  return fees

def get_fast_price(symbol,end_day,token_list):
  # 获取价格
  # 获取token的address
  # token_list = ['ETH',"WBTC"]
  address_list = [x for x in symbol.index if symbol.loc[x,'data.symbol'] in token_list]
  prc = {}
  end_day = int(pd.to_datetime(end_day,format = '%Y%m%d%H').timestamp())
  for address in address_list:
    query = f'''query {{
  fastPrices(first: 10000, orderBy: id, orderDirection: desc,where: {{token: "{address}", period: "hourly",timestamp_gt: 0, timestamp_lt: {end_day}}}) {{
        id
        token
        value
        period
        timestamp
      }}
    }}
    '''

    url = 'https://subgraph.satsuma-prod.com/3b2ced13c8d9/gmx/gmx-arbitrum-stats/api'
    headers = {'Content-Type': 'application/json'}
    request_json = {'query': query}
    response = requests.post(url, headers=headers, data=json.dumps(request_json))
    price_data = response.json()
    if 'errors' in price_data:
        error_message = price_data['errors'][0]['message']
        raise Exception(f"GraphQL query failed: {error_message}")
    price_data = price_data['data']['fastPrices']
    price_data = pd.DataFrame(price_data)
    price_data['time'] = pd.to_datetime(price_data['timestamp'], unit='s')
    # 生成token对应的名字
    price_data['token'] = price_data['token'].apply(lambda x: symbol.loc[x]['data.symbol'])
    price_data['value'] = price_data['value'].astype(float) / 10**30
    token_name = symbol.loc[address]['data.symbol']
    price_data.rename(columns={'value':'value.' + token_name.lower()}, inplace=True)
    prc[token_name] = price_data

  return prc

def show_case(glp,fees,prc,hedge_ratio = []):
  # 转换精度
  data = pd.merge(glp,fees,on=['id','time'])
  data = pd.merge(data,prc['ETH'][['time','value.eth']],on=['time'])
  data = pd.merge(data,prc['WBTC'][['time','value.wbtc']],on=['time'])
  data.sort_values('time',inplace=True)
  data['margin'] = data['margin'].astype(float) / 10**30
  data['marginAndLiquidation'] = data['marginAndLiquidation'].astype(float) / 10**30
  data['swap'] = data['swap'].astype(float) / 10**30
  data['mint'] = data['mint'].astype(float) / 10**30
  data['burn'] = data['burn'].astype(float) / 10**30
  data['total'] = data['marginAndLiquidation'] + data['swap'] + data['mint'] + data['burn']
  data['aumInUsdg'] = data['aumInUsdg'].astype(float) / 10**18
  data['glpSupply'] = data['glpSupply'].astype(float) / 10**18
  data['liquidation'] = data['marginAndLiquidation'] - data['margin']
  data.reset_index(inplace=True,drop=True)

  # 设置仓位和对冲比率
  v0 = 10000 # usd
  veth = v0 * hedge_ratio[0]
  vwbtc = v0 * hedge_ratio[1]
  
  # 计算买的数量
  result = pd.DataFrame()
  result['Date'] = data['time']
  my_glp = v0 / data['price'][0]
  my_eth = -veth / data['value.eth'][0]
  my_wbtc = -vwbtc / data['value.wbtc'][0] # 取负号方便后面计算hedge_value
  
  # 计算资产池的价值

  result['glp_value'] = data['price'] * my_glp
  result['eth_value'] = data['value.eth'] * my_eth
  result['wbtc_value'] = data['value.wbtc'] * my_wbtc
  result['total_value'] = result['glp_value'] + result['eth_value'] + result['wbtc_value'] 
  result['ratio'] = my_glp / data['glpSupply']
  result['div'] = data['total'] * result['ratio']
  # ret是累计分红 + 资产池相对于初始状态变化
  result['ret'] = result['div'].cumsum() + result['total_value'] - result['total_value'].iloc[0]

  result = result.fillna(0)
  # 计算最大回撤
  result['nav'] = (result['ret'] / (v0 + veth + vwbtc) + 1)
  result['max'] = result['nav'].cummax()
  result['drawdown'] = result['nav'] / result['max'] - 1
  # 最大回撤时间段
  max_drawdown_end = result['Date'].iloc[result['drawdown'].idxmin()]
  # 年化收益率
  apy = result['ret'].iloc[-1] / (v0 + veth + vwbtc) * 365 / (result['Date'].iloc[-1] - result['Date'].iloc[0]).days
  # 夏普比率,按每日收益率计算
  result.set_index('Date',inplace=True)
  sharpe = result['nav'].resample('D').last().pct_change().mean() / result['nav'].resample('D').last().pct_change().std() * np.sqrt(365)
  result.reset_index(inplace=True)
  # print result
  print('apy: ', apy)
  print('sharpe: ', sharpe)
  print('max drawdown: ',result['drawdown'].min(),'end at: ', max_drawdown_end)
  indicators = [apy,sharpe,result['drawdown'].min()]


  # plot
  plot_data = [go.Scatter(x=result['Date'], y=result['ret'] / (v0 + veth + vwbtc), name='ret'),\
          go.Scatter(x=result['Date'], y=result['total_value'] / (v0 - veth - vwbtc) - 1, name='position value'),\
          go.Scatter(x=result['Date'], y=result['div'].cumsum() / (v0 + veth + vwbtc), name='div'),\
          go.Scatter(x=result['Date'], y=result['glp_value'] / v0 - 1, name='glp_value'),\
          go.Scatter(x=result['Date'], y=(result['eth_value'] + result['wbtc_value'] ) / (veth + vwbtc)  + 1, name='hedge_value'),\
          go.Scatter(x=result['Date'], y=result['nav'], name='nav',yaxis='y2'),\
          ]

  layout = go.Layout(
          title='GLP',
          yaxis=dict(
                  title='return',
          ),
          yaxis2=dict(
                  title='price',
                  overlaying='y',
                  side='right')
  )

  fig = go.Figure(data=plot_data, layout=layout)
  return result,fig,data,indicators

