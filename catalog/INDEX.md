# Catalog · 8 张图速查表

模板源（**只读**）：`~/.claude/skills/arch-diagrams/templates/`

## 选型矩阵

| 用户表达模式 | 关键词 | 图型 |
|---|---|---|
| "A 做完做 B，B 失败就回 C" | 流程 / 分支 / 判断 / YES NO | **01 flowchart** |
| "client 调网关，网关调 auth，auth 查 redis" | 调用链 / 顺序 / 谁先谁后 | **02 sequence** |
| "订单从待支付到已完成中间有多个态" | 状态 / 转移 / guard / 生命周期 | **03 state-machine** |
| "整个系统长什么样" | 分层 / 架构 / 技术栈 / 拓扑 | **04 system-architecture** |
| "用户表 → 订单表 → 商品表" | 实体 / 关系 / PK FK / 表结构 | **05 ER** |
| "运营审单后财务打款" | 跨部门 / 跨角色 / 谁负责 | **06 swimlane**（水平） |
| "需求 → 设计 → 开发 → 测试" | 阶段 / 里程碑 / phase | **06 swimlane-vertical** |
| "K8s ns / sidecar / istio / prom" | 微服务 / namespace / 运行时 | **07 microservice** |

## 每图速查

| ID | 文件 | viewBox | A 区行 | B 区行（删除） | nodeData 起点 | `</svg>` |
|---|---|---|---|---|---|---|
| 01 | `01-flowchart.html`           | 1080×1500 | 285-440 | 无 B 区          | (单独 script，搜索 `window.DIAGRAM_CONFIG`) | 440 |
| 02 | `02-sequence.html`            | 1080×2680 | 365-608 | **609-846** 删   | 927  | 847 |
| 03 | `03-state-machine.html`       | 1080×2660 | 419-692 | **693-988** 删   | 1081 | 989 |
| 04 | `04-system-architecture.html` | 1080×2680 | 420-889 | **890-1145** 删  | 1247 | 1146 |
| 05 | `05-er-diagram.html`          | 1080×2680 | 400-610 | **611-909** 删   | 993  | 910 |
| 06H | `06-swimlane.html`           | 1080×2660 | 446-805 | **806-1163** 删  | 1255 | 1164 |
| 06V | `06-swimlane-vertical.html`  | 1080×2680 | 442-695 | **696-934** 删   | 1021 | 935 |
| 07 | `07-microservice.html`        | 1080×2660 | 467-930 | **931-1249** 删  | 1339 | 1250 |

> **行号是模板原文行号**。删除 B 区后，需把 `<svg width="1080" height="2680">` 和 `viewBox="0 0 1080 2680"` 中的高度改为 A 区实际占用高度 + 60px 边距。各图推荐目标高度在自己的卡片里。

## 节点 class 清单（每图独有的类型）

各图独有的节点 class（去掉所有图都有的 `.gallery-card-node`）：

```
01 flowchart       : term / term success / term fail / process / decision /
                     io / db / subprocess / connector / document
02 sequence        : actor / actor-system / actor-external
03 state-machine   : state / state-initial / state-final /
                     state success / state fail /
                     state-final success / state-final fail / decision
04 architecture    : client / edge-net / bff /
                     svc core / svc trade / svc catalog / svc edge-domain /
                     mw / mw cache / mw search / data-store / infra
05 ER              : node（统一类，靠 entity-weak / attribute-key 等子样式区分）
06H swimlane       : node（统一类，靠所在 lane 区分语义）
06V swimlane-v     : node（同上）
07 microservice    : 同 04 + svc（无业务域子类）
```

## 边 class 清单

```
01 flowchart       : edge / edge yes / edge no / edge db
02 sequence        : edge sync / edge async msg / edge return
                     + edge-label / edge-label plum / edge-label-bg
03 state-machine   : edge / edge yes / edge no / edge spine
                     + edge-label trigger / edge-label guard / edge-label action
04 architecture    : edge sync-arch / edge rpc / edge async-event /
                     edge db-edge / edge cache-edge / edge cdc /
                     edge scrape / edge spine
                     + edge-label clay/gold/olive/plum/teal
05 ER              : 自定义关系连线（搜索 .er-rel-line / .er-rel-marker）
06H swimlane       : edge（默认即可）
06V swimlane-v     : edge / edge-label yes / edge-label fail
07 microservice    : 同 04
```

## 进入下一步

针对用户指定的图型，**只读对应一张 catalog 卡片**：

- `catalog/01-flowchart.md`
- `catalog/02-sequence.md`
- `catalog/03-state-machine.md`
- `catalog/04-system-architecture.md`
- `catalog/05-er-diagram.md`
- `catalog/06-swimlane.md`
- `catalog/06-swimlane-vertical.md`
- `catalog/07-microservice.md`
