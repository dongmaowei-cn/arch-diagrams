# Catalog · 8 张图速查表

**给用户选型**：打开 [`templates/index.html`](../templates/index.html) — 10 张卡片，每张可进 **图鉴 · 画法**（`gallery/`）或 **范本**（`0X-*.html`），比文字列表更直观。

模板源（**只读**）：`$SKILL_DIR/templates/`
教学参考：`$SKILL_DIR/templates/index.html` 导航总览；每张图的**元素图鉴 + 画法**在 `$SKILL_DIR/templates/gallery/0X-*.html`（单文件内联 CSS/JS）

## 选型矩阵

> **输入是 PlantUML 源码时**：先用「PlantUML 特征」列判定图型，图型确定后跳到对应图型的正常流程（读 catalog 卡片）。转换细节（语法元素 → 本 skill 的 node/edge class）看 `shared/plantuml-mapping.md`，不要凭经验直译——PlantUML 是纯逻辑骨架，节点/边样式、分层分组、详情面板这些视觉信息它并不携带，需要按目标图型的正常建造流程补上。

| 用户表达模式 | 关键词 | PlantUML 特征 | 图型 |
|---|---|---|---|
| "A 做完做 B，B 失败就回 C" | 流程 / 分支 / 判断 / YES NO | `@startuml` + `start`/`:action;`/`if()then()`/`stop`，**没有** `\|Lane\|` | **01 flowchart** |
| "client 调网关，网关调 auth，auth 查 redis" | 调用链 / 顺序 / 谁先谁后 | `participant`/`actor`/`database` + `->`/`-->`/`->>` | **02 sequence** |
| "订单从待支付到已完成中间有多个态" | 状态 / 转移 / guard / 生命周期 | `[*] -->` 或 `state X { ... }` | **03 state-machine** |
| "整个系统长什么样" | 分层 / 架构 / 技术栈 / 拓扑 | `package`/`node`/`cloud`/`component` 按**抽象层**分组（client/service/data），无 K8s/sidecar 细节 | **04 system-architecture** |
| "用户表 → 订单表 → 商品表" | 实体 / 关系 / PK FK / 表结构 | `entity X { *pk : type }` + `\|\|--o{` 等 crow's foot 关系符 | **05 ER** |
| "运营审单后财务打款" | 跨部门 / 跨角色 / 谁负责 | activity 图 + `\|Lane\|`，且用户明确要"横向时间轴/按部门分行" | **06 swimlane**（水平，少数场景） |
| "需求 → 设计 → 开发 → 测试" | 阶段 / 里程碑 / phase | activity 图 + `\|Lane\|`（**PlantUML 原生渲染就是纵向 lane**，这是默认目标） | **06 swimlane-vertical**（默认） |
| "K8s ns / sidecar / istio / prom" | 微服务 / namespace / 运行时 | `node`/`cloud` 分组里出现 namespace 边界、sidecar、服务网格、消息总线等**运行时部署**细节 | **07 microservice** |

## 每图速查（v2 · B 区在 gallery/）

| ID | 文件 | viewBox | A 区行 | `</svg>` |
|---|---|---|---|---|
| 01 | `01-flowchart.html`           | 1080×1500 | 286-455 | 456 |
| 02 | `02-sequence.html`            | 1080×1240 | 366-530 | 531 |
| 03 | `03-state-machine.html`       | 1080×1660 | 432-687 | 688 |
| 04 | `04-system-architecture.html` | 1080×1500 | 434-889 | 891 |
| 05 | `05-er-diagram.html`          | 1080×700  | 420-604 | 604 |
| 06H | `06-swimlane.html`           | 1080×1000 | 465-595 | 596 |
| 06V | `06-swimlane-vertical.html`  | 1080×1540 | 460-732 | 732 |
| 07 | `07-microservice.html`        | 1080×1500 | 484-930 | 936 |

> **B 区不再在模板里**。元素图鉴 + 画法说明在 `templates/gallery/0X-*.html`，总览入口见 `templates/index.html`。

> **⚠️ 行号/viewBox 会随模板迭代漂移，此表只做粗定位，不要盲信。** 复制模板后，正式编辑前用一条命令现场核实：
> `grep -n '<svg class=\|DIAGRAM_CONFIG\|NODE_DATA\|</svg>' <output-dir>/<file>.html`
> 之前就发生过表格与实际文件差几百行的情况（04 / 06H / 07 曾经如此）——现场核实成本只有一次 grep，远低于对着错误行号瞎编或者编辑到 script 区域的返工成本。
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
05 ER              : table-frame / table-header / table-title / row-zebra /
                     cell pk / cell fk / tag-pk / tag-fk / tag-uq / tag-idx / tag-nn
06H swimlane       : node 外层统一，内部 shape 用 task-rect（+ user/service/send/receive）/
                     gateway-shape / event-start / event-end-bpmn / event-msg
06V swimlane-v     : node 外层统一，内部 shape 用 task-rect / gateway-shape / event-start（同 06H 体系）
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
05 ER              : er-edge + crowfoot（双短横=1 / 三叉=N）+ edge-label 关系标签
06H swimlane       : seq-flow / seq-flow spine / seq-flow yes / seq-flow no / msg-flow
                     （注意基类是 seq-flow 不是 edge）
06V swimlane-v     : vflow / vflow spine / vflow fail / vflow msg / vflow data
                     + edge-label / edge-label yes / edge-label fail
                     （注意基类是 vflow 不是 edge，也不是 06H 的 seq-flow——两个泳道模板边基类名三者互不相同）
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
