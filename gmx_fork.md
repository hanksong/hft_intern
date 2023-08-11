---
theme: unicorn
---
# HMX

https://kjwez9gefn.feishu.cn/docx/WYAmdQdgiorL9BxdAwTcPzNYnBh

<div grid="~ cols-2 gap-4">
<div>
<img border="rounded" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*Pyt3KKYDuWGCiMs5.png" width="600" height="500">
</div>
<div>
1. 用户将资产存入 GMX 的 GLP 并接收 GLP 代币。

2. 用户在 HMX 上质押 GLP 代币，并收到 HLP 代币作为回报。然后，HMX 代表用户质押 GLP 代币，以继续从 GMX 获得 100% 的收益。
3. GLP 金库中的流动性用于为 GMX 的交易者做市，从而以 ETH 的形式从柜台交易和费用中产生利润/损失。
4. 与此同时，HMX 将质押 GLP 的流动性重新抵押给 HMX 交易者的做市商，通过对销交易和费用（借款、开仓/平仓等）累积利润/损失。
5. 然后，HMX 向其交易者收取费用，并从 GMX 收取 ETH 收益，并将其与 esHMX 发行奖励一起重新分配给用户。

</div>
</div>



---

# global debt pool

![1691375107283](image/gmx_fork/1691375107283.png)

---

# Trader

## Profit：

1. 合约盈亏，以sUSD结算，来源是mint/burn
2. 对手funding，每秒计算
3. 奖励计划(为鼓励trader来交易，根据手续费分得，非长期，不重要)

## Loss：

1. 执行费，支付给keeper，动态费用，2\$左右
2. maker/taker手续费 （2bp / 6bp），100%进入debt pool
3. funding，给对手。

---

# staker

## profit：

1. 债务池缩水(sToken总体下跌)
2. trader Loss（2）的手续费(不再发放，而是通过每周burn的形式减少债务, 即在赎回抵押时减少susd得burn量)
3. SNX（抵押物）升值
4. 通胀奖励

## loss：

1. 债务池膨胀（sToken总体上涨）
2. SNX（抵押物）贬值 ：需要使质押价值维持在c-ratio才能分到fees

---

# Kwenta（integrators）

1. 通过[SIP2002](https://sips.synthetix.io/sips/sip-2002/)提案从synthetix获得SNX奖励。

---

# 基本数据对比

https://dune.com/maverick_cap/perp-dex

|        | TVL                                   | fees(annualized) | volume24h |
| ------ | ------------------------------------- | ---------------- | --------- |
| GMX    | 540m                                  | 63.38m           | 15.23m    |
| Kwenta | https://defillama.com/protocol/kwenta |                  |           |
| SNX    | 481m                                  | 40.04m           | 40.91m    |
| HMX    | 7.74m                                 | 1.73m            | 4.31m     |

---

TODO：

1. price feed hmx喂价机制

   > 1. [hmx使用pyth oracle作为原始价格](https://medium.com/hmx-org/how-hmx-utilizes-pyths-low-latency-price-feed-to-create-the-best-trading-experience-for-users-83fe9e86ab73)
   > 3. Uniswap V3 TickMath ： 用tick压缩价格数据
   > 2. ![Adaptive price](https://miro.medium.com/v2/resize:fit:1400/0*kHp4yGVImgk84WDc)
   > 4. [perp88的防攻击价格](https://medium.com/perp88/mev-aegis-perp88s-newest-mev-resistant-price-feeder-api-ca4d1ddd3071)
2. kwenta奖励计划

   > [kwenta奖励](https://mirror.xyz/kwenta.eth/8KyrISnjOcuAX_VW-GxVqxpcbWukB_RlP5XWWMz-UGk)
   >
3. snx价值

   1. 手续费预期的折现值
   2. 治理价值，持有snx可以调整资金池分配比例（像无形资产）
4. hmx费率大小

   > borrowing rate 每小时最大0.8bp（基于保证金*固定倍率）



# dydx

## 建立在 StarkWare 提供的 StarkEX L2 解决方案的链上交易所

- 相比建立在 L1 上的早期版本，建立在 L2 提供了更低的交易费用、更好的交易性能、更高的杠杆率（4x-25x）、支持更多的交易对。
- 交易过程中每一笔订单的成交都会上链，但是下单、挂单并不上链，在 dYdX 服务器上进行，去中心化程度有限。
- 只在存入资金和赎回资金时需要交 gas ，此后的交易过程不需要。
- 目前正在准备 Cosmos 上的 V4 版本，旨在大幅提升去中心化程度；并将协议产生的交易佣金分配给 dYdX 的持有者。

## dYdX 目前只在在 Layer 2 上提供永续合约交易

- dYdX 支持 8 种不同的订单类型 — — 市价订单、限价订单、止损市价订单、止损限价订单、追踪止损订单、止盈市价订单、止盈限价订单和一篮子订单。
 -提供最高 20 倍的多空双方交易功能，最小杠杆变动倍率为 0.01。
- 交易模式。采用订单簿形式，由专业做市商 Wintermute、Altonomy 等提供流动性。
- 资金费率。资金费率由交易量以及 dYdX 代币持有数量决定。交易量或 dYdX 代币持有量越大，资金费率越低。

## players

将 dYdX 平台上交易的角色分为以下三类：

a. 交易者：在 dYdX 上进行永续合约交易。交易挖矿：每个 epoch 最后，dYdX 协议会空投 3835616 枚 dYdX，根据交易者交易产生的手续费与未平仓量来确定每个交易者在每个 epoch 能分到多少奖励。
dYdX 交易产生的费用对交易者无分成。
b. 专业做市商：专业做市商 Wintermute、Altonomy 等

流动性提供者挖矿：每个 epoch 最后，dYdX 协议会空投 115 万枚 dYdX。
c. dYdX：收取交易佣金（该部分对交易者无分成）。

d. 质押者：通过质押 USDC 进入流动性池 / 安全性池进行流动性质押挖矿。目前两个池子已经关闭，剩余奖励将不会分配，而是累积在奖励金库中，而奖励金库又可以由社区指挥。






# Pyth

数据提供商在 Pythnet 上发布其价格，Pythnet 是专用于 Pyth 的特定应用程序区块链。然后，链上聚合程序聚合 feed 的价格以获得总价格和置信度。接下来，证明程序定期证明最近观察到的 Pyth 价格，并创建一条虫洞消息发送到 Pythnet 上的虫洞合约。然后，虫洞守护者观察证明消息并为该消息创建签名的 VAA。整个过程的结果是经过签名的 Pyth 价格更新流，可以在任何区块链上进行验证。

价格服务是一种实用程序，可帮助用户使用此价格更新流。该服务持续监听Wormhole的 Pyth 价格更新消息。它将最近的更新消息缓存在内存中，并公开 HTTP 和 WebSocket API 以检索最新更新。（任何人都可以运行此 Web 服务的实例，但为了方便起见，Pyth 数据协会运行公共实例。）当用户想要在交易中使用 Pyth 价格时，他们会从价格中检索最新的更新消息（签名的 VAA）服务并在其交易中提交。目标链Pyth合约将验证价格更新消息的有效性，如果有效，则将新价格存储在其链上存储中。

最后，链上协议通过一个简单的 API 与 Pyth 合约集成，该 API 从链上存储中检索当前的 Pyth 价格。只要最近有足够的更新，该 API 就会返回当前价格；这种方法之所以有效，是因为用户将在同一交易中较早地更新 Pyth 价格。协议可以配置新近度阈值以满足其需求，例如，对延迟敏感的应用程序可以设置比默认值更低的阈值。

Pyth 价格可以通过不同的方式纳入协议逻辑，具体取决于相关协议的用例和约束。对于对延迟极其敏感的应用程序，建议以不同于对延迟不敏感的协议的方式使用 Pyth。有关这方面的更多详细信息，请参阅我们的文档。