# Catalog · 8 张图速查表

模板源（**只读**）：`$SKILL_DIR/templates/`
教学参考：`$SKILL_DIR/templates/index.html` — 8 个锚点 section,每张图含元素图鉴 + 画法说明

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

## 每图速查（v2 · B 区已迁移到 index.html）

| ID | 文件 | viewBox | A 区行 | `</svg>` |
|---|---|---|---|---|
| 01 | `01-flowchart.html`           | 1080×1500 | 285-440 | 440 |
| 02 | `02-sequence.html`            | 1080×1500 | 365-608 | 609 |
| 03 | `03-state-machine.html`       | 1080×1400 | 419-692 | 693 |
| 04 | `04-system-architecture.html` | 1080×1500 | 420-889 | 890 |
| 05 | `05-er-diagram.html`          | 1080×840  | 400-610 | 611 |
| 06H | `06-swimlane.html`           | 1080×1300 | 446-805 | 806 |
| 06V | `06-swimlane-vertical.html`  | 1080×1500 | 442-695 | 696 |
| 07 | `07-microservice.html`        | 1080×1500 | 467-930 | 931 |

> **B 区不再在模板里**。元素图鉴 + 画法说明在 `templates/index.html` 的 8 个锚点 section,见各图 catalog 卡片"画法参考"段。
> 如果新场景的 A 区显著矮于上表 viewBox h,改造时同步收紧 `<svg height>` + `viewBox` + `viewBox: { w, h }`。

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
