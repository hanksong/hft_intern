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





















