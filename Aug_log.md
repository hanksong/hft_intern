# Aug 1st

1. 总结了kwenta的运营逻辑，明确了各个players的盈利亏损。
   1. 特点：债务池模式，0滑点。kwenta只是前端，synthetix是内核。比gmx更低的手续费。
   2. 多个对手方：long的对手方首先是空头，其次是staker。
2. todo：
   1. 完善kwenta的报告，和binance的费率值做对比
   2. hmx报告

# Aug 2

1. 通过和kwenta开发者的交流明确了金融模型和部分细节。kwenta交易的都是sToken，是可以随时mint和burn的。
2. 理清kwenta和synthetix的关系，在生态系统中，kwenta是synthetix期货的dapp，kwenta通过给synthetix带去交易量获得的后者的激励（SNX）。

TODO

1. HMX研究
2. 一个简明清晰的示意图，展现kwenta的金融模型。

AUG 3

1. 整理HMX的交易逻辑，杠杆做市提高glp利用率，同时采用6种机制保证HLP holder（特别的是价格调整、基于速率的资金费率和利率储备buffer）
2. trader则拥有全局抵押的模式，可用多种币做保证金。
3. 在HMX上进行交易尝试。

Profit reserve是什么含义

文档需要整合到一起，快速切换，保持会议流畅。

# Aug 7

1. 整理两个文档，绘制示意图
2. kwenta + hmx 协议串讲

TODO：

1. price feed hmx喂价机制
2. kwenta奖励计划
3. snx价值


# Aug 8

1. 解答串讲提出的几个问题
2. 构建横向对比的表格，填充已知信息
Todo ： 
   1. dydx数据填充


排期
1. 对比交易所: dydx、gmx、level、 gains.network、kwenta
2. hmx1表格字段:[价格: 喂价机制、实际交易价格]、[交易机制: trader交易的机制、LP0提供流动性的机制、各个角色的风险和收益来源][费用: 开仓平仓费、swap费、funding fee、borrow fee 及其他手续费]
3. 数据对比: 交易量、TVL、累计手续费...


# Aug 9

1. dydx doc整理
2. 补充hmx预言机机制



# Aug 10

1. 联系hmx 看他们的MEV resistant还有没有用: 使用 [pyth VAA](https://pyth.network/blog/pyth-a-new-model-to-the-price-oracle)直接获得价格
2. 阅读期权小白书，重点关注了calendar spread的部分。
3. 在deribit testnet构建calendar spread组合

# Aug 11

1. 在看deribit的期权课程
3. 整理资金费率套利的基本信息


# Aug 15

![Alt text](image-1.png)

[okx资金费率研究报告](https://zhuanlan.zhihu.com/p/75109894)
1. 了解资金费率套利，以及他人的实践结果
1. coinglass拉取资金费率历史数据

todo：

1. 和老a理下策略的schedule



# Aug 16

  - 原理和机制
  - 交易所机制对比
  - 案例




# Aug 17

risk：
1. 仓位安全 , 合约杠杆
   - [实盘八十万资金五倍杠杆](https://www.youtube.com/watch?v=tAzH2LBInK8) 
   - 即将爆仓则增加仓位或平仓
   - 爆仓亏手续费和清算费用
   > 1. 优化手续费，现货手续费为零(BUSD交易对)
   > 2. 算法自动下单，降低滑点，能容纳更大的资金
   > 3. 可以设置价差开仓，赚资金费率，也赚价差,
   > 4. 防止爆仓功能，爆仓前平仓
   > 5. 交易所发生减仓，会自动对冲，防止仓位敞口的出现
   > 6. 高频实时对冲on tick 
2. 开仓时机，不考虑价差
   > 必须得考虑价差，亏损也是价差带来的
   > 可以通过过去一段时间的价差中值指定maker的价格。
3. 开关仓执行，关注成交进度
   
4. 关仓时机，价差，预期盈利比较
   > 同样是关注价差


问题：
1. 合约方向，如果看绝对值，一般是负费率大，这种币的借贷利率会特别高，以明星所为例，LPT借贷利率是年化365%，但其实也还好毕竟和资金费率还有利差，关键我去借时已经被借空了。还有一个就是现货和合约之间有价差，时间一到基本是下跌的，但由于价差的存在现货的下跌幅度是小于合约的，所以现货卖出低价买回赚的抵不上合约做多下跌亏的。

需要觀察一下費率結算時候的價格數據，尤其是期限價差
1. 像前兩天的LPT，套利多頭在收掉資金費后馬上平倉了, spread（期-现）迅速增大，即期货上升，现货减小。所以确实是要是进晚了就容易亏。(blz价差更离谱)
2. 价差未回归则无法平仓。

*费率套利数据coinglass——api缺失*


# Aug 18

- 确认币安的资金费率是浮动的，且只有ok是固定的，对此币安给出的建议是：
> 实际资金费用收益将受市场波动影响，并不保证收益。资金费率正负变化可能导致您在套利策略内付出资金费用。只要长期资金费率趋势符合您的套利策略，您仍可从套利策略中获利。过往收益并不代表未来回报。

- 用s3数据寻找价差和资金费率的关系


# Aug 21

1. 写了一些拉数据的函数；
1. 资金费率详细计算公式，每个交易所都要看；回测先不着急做

todo：
列出的四个交易所的详细计算公式，公式能得到的结论。


# Aug 22

1. 已经弄清楚各个交易所资金费率的具体计算公式
   - 利率是基准线
   - 溢价保证更宽泛的判定期货=现货的范围
   - 费率驱动价格回归
2. 资金费率向利差看齐，结论是保证期货和现货收益无差异；利率的设置和外汇期货的定价公式完全吻合。


# Sept 4

(主要的) ：资金费率静态策略串讲
   - binance的订单识别问题：如何判断一笔资金费率是哪个仓位带来的？
   - 静态策略的整体流程。
   - 遗留计算问题。

(次要的) ：所有的研究结论整理成文档

