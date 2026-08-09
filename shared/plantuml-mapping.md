# PlantUML 输入映射 · 语法元素 → 本 skill 的 node/edge class

## 这份文档解决什么问题

如果输入是一段 PlantUML 源码（而不是一句业务描述），流程不变——还是「判定图型 → 读对应 catalog 卡片 → 复制模板 → 改」——但多一步：**先把 PlantUML 的语法元素翻译成本 skill 的节点/边清单**，再按正常流程往模板里填。这一步之所以必要，是因为 PlantUML 和本 skill 不是同构的：

- **PlantUML 是纯逻辑骨架**：谁连谁、什么顺序、什么条件。它不携带分层分组的视觉语言（tier-band）、技术栈/QPS 这类 meta 信息、点击弹出的详情面板、也没有网关/事件/K8s namespace 这些更细的图形语义。
- **本 skill 的模板是骨架 + 血肉**：同样的"A 调 B"，在本 skill 里还要决定用什么形状（process/decision/db/io…）、什么颜色语义（成功/失败/异步）、要不要配 nodeData 详情、算不算主路径 spine。

所以翻译 PlantUML 不是"标签替换"，是"提取结构，再按目标图型的正常建造流程重新长肉"。下面的映射表告诉你 PlantUML 的每个语法元素**大概率**对应哪个 class，但最终形状/颜色判断仍然要回到对应 catalog 卡片的语义规则（比如"这一步是不是要写库" → `node db`，不是看 PlantUML 里怎么写的，是看这一步业务上是不是真的在写库）。

## Step 0 · 判定图型

先看 `catalog/INDEX.md` 选型矩阵的「PlantUML 特征」列。简版判定顺序（找到第一个匹配的就停）：

1. 有 `participant` / `actor` / `boundary` / `control` / `entity`（作为参与者声明，不是 ER 的 entity 块）+ 消息箭头 `->`/`-->`/`->>` → **02 sequence**
2. 有 `entity X { ... }` 字段块 + 关系符号里出现 `||`/`o{`/`|{`/`}o` 等 crow's foot 组合 → **05 ER**
3. 有 `[*] -->` 或顶层出现 `state X { ... }` 复合块 → **03 state-machine**
4. 有 `start`/`:action;`/`stop`/`if ... then ... else ... endif` 且**同时**出现 `|LaneName|` → 泳道场景，见下方 §5 判断 06H / 06V
5. 有 `start`/`:action;`/`stop` 但**没有** `|LaneName|` → **01 flowchart**
6. 都是 `package`/`node`/`cloud`/`component`/`database`/`queue`/`folder` 分组 + 箭头，没有 1-5 的特征 → 架构类，见下方 §6 判断 04 / 07

拿不准就用 §6/§5 的细则再判一次；两种都像时，优先选信息量更大的那个（比如同时有分层描述又有 K8s namespace，选 07，因为 07 能表达的细节包含 04 能表达的）。

---

## §1 Activity Diagram（无泳道）→ 01 flowchart

| PlantUML | 说明 | 本 skill class |
|---|---|---|
| `start` | 开始 | `node term`（起始态，不是 success/fail） |
| `stop` / `end` | 结束 | `node term`；如果业务上这是"成功终态"用 `node term success`，"失败终态"用 `node term fail`——**PlantUML 不区分这两种 stop，要按上下文语义判断**，不能无脑都用中性 `term` |
| `:action;` | 动作 | `node process`（动词开头） |
| `if (cond) then (yes)` ... `else (no)` ... `endif` | 二元判断 | `node decision`，两条出边分别是 `edge yes` / `edge no` |
| `while (cond)` ... `endwhile` | 循环 | 通常退化成一个 `node decision` 回指自己上游节点的循环边；简单场景可以直接画成"判断 + NO 分支绕回上一个节点" |
| `fork` / `fork again` / `end fork` | 并行分支 | 本 skill 流程图模板**没有**并行 fork/join 的专用图形；两种处理方式：(a) 场景其实是"同时触发几个独立动作"，就用多条 `edge` 从同一个节点引出；(b) 并行度是重点信息，改用 **04/07 架构图**表达（真正的并行运行时用架构图更合适） |
| `:action|` （分区/partition，不是 `|Lane|`） | 用 `partition` 关键字包一段动作 | 如果只是逻辑分组、不代表"谁执行"，可以忽略分组只保留内部动作序列；如果代表不同角色/系统，改判定为泳道场景，见 §5 |
| 注释 `' comment` | 注释 | 通常丢弃，除非明显是要放进节点详情面板 nodeData 的 body |
| 一条无分支的动作链 | 顺序流 | `edge`（默认灰线），除非这条链是全图唯一主路径，此时可以整体识别为 spine 来加粗强调（01 flowchart 本身没有独立的 `edge spine` class，主路径靠纵向轴线布局体现，不是靠边的样式） |

判断分支的 YES/NO 具体走哪条：PlantUML 的 `if (cond) then (yes-label)` 里 `(yes-label)` 只是箭头旁边的文字，不代表这条一定是"成功/通过"语义——要看 `yes-label` 的实际文字内容（比如 `then (库存充足)` 才是 yes 分支该配的路径，`then (库存不足)` 反而应该走 `edge no` 接失败终态）。**不要机械地把 if 的第一个分支都当 yes**。

---

## §2 Sequence Diagram → 02 sequence

### 参与者

| PlantUML | 本 skill class |
|---|---|
| `actor X` | `node actor`（人 / 客户端 / 触发器） |
| `participant X` / `boundary X` / `control X` | 按业务角色判断用 `node actor-system`（内部服务，多数情况）还是 `node actor-external`（外部系统） |
| `database X` | 时序图里数据库一般作为一个参与者出现，用 `node actor-system`，在消息标签里写清楚"查 X 表"即可，不必强行找一个数据库图标 class |
| `entity X` | 同 participant，按角色判断 actor-system / actor-external |

### 消息箭头（关键：`->` / `-->` / `->>` 语义不同，别混用）

| PlantUML | UML 语义 | 本 skill class |
|---|---|---|
| `A -> B: msg`（实线 + 实心箭头） | 同步调用 | `edge sync` |
| `B --> A: msg`（虚线），且紧跟在一条 `A -> B` 之后、方向相反 | 该次调用的返回值 | `edge return` |
| `A ->> B: msg`（空心箭头，不管实线虚线） | 异步消息，不等待 | `edge async msg` |
| `A -> A: msg` | 自调用 | 模板里的 U 形自调用边（`edge`，折角画法，见 catalog/02-sequence.md「边类型」表最后一行） |

**判断 `-->` 是"返回"还是"异步"的启发式**：看它是不是紧跟着一条方向相反的 `->`，且是同一对参与者——是，就是 return；如果是独立出现、没有配对的前置调用（比如 MQ 事件、webhook 回调通知），才是异步消息 `edge async msg`。PlantUML 本身的图形约定（`plantuml.com` 原话：solid=sync call, dashed=async return）把这两种情况都画成虚线，靠画虚线本身分不出来，必须读上下文语义。

### 控制块

| PlantUML | 本 skill 对应 |
|---|---|
| `alt ... else ... end` | `fragment` 虚线框 + `fragment-tab`（"alt"字样）+ 每个分支前用 `t-cond` 写守卫条件 + `fragment-divider` 分隔线，见 catalog/02-sequence.md「示例片段」 |
| `opt ... end` | 同上，但只有一个分支，`t-frag` 写"opt" |
| `loop ... end` | 同上结构，`t-frag` 写"loop"，守卫写循环条件 |
| `par ... end` | 本 skill 时序图模板没有并行 fragment 的专用画法；如果并行度不是重点，拆成两个独立 fragment 或直接顺序画（加注释说明"并行执行"）；如果并行度是重点信息，考虑改用架构图 |
| `activate X` / `deactivate X` | `<rect class="activation">`，激活区间必须覆盖区间内所有消息端点——这不是可选装饰，是 edge-check [9] 强制项，见 catalog/02-sequence.md「Activation 纪律」 |
| `note left of X` / `note right of X` / `note over X,Y` | 底部折角 `note-box`，或就近放在相关消息旁；具体位置规则见 catalog/02-sequence.md「折角注释纪律」 |

阶段（phase）：PlantUML 没有"阶段"概念，但真实场景的消息通常能按业务动作自然分成 2-4 段（比如"发起请求""校验受理""回调通知"）——转换时主动划出 `phase-frame`，不要把十几条消息平铺在一个 phase 里，可读性会很差。

---

## §3 State Diagram → 03 state-machine

| PlantUML | 本 skill class |
|---|---|
| `[*] --> StateX`（初始伪状态指向的第一个真实状态） | 起始态用 `node state-initial`（实心圆），`StateX` 用 `node state` |
| `StateX --> [*]` | `StateX` 如果是绝大多数实例都会落到的主终态 → `node state-final success`；低频/补偿/异常终态 → `node state-final fail`；如果一个状态机只有一个 `--> [*]`，通常就是 success |
| `StateA --> StateB : event [guard] / action` | `edge`（默认）；如果这是主路径上的转移，考虑升级成 `edge spine`（加粗）；转移标签拆成三段：`edge-label trigger`（event）/ `edge-label guard`（`[guard]`）/ `edge-label action`（`/ action`），见 catalog/03-state-machine.md |
| `state Composite { [*] --> Sub1 ... }` | 复合/子状态机，对应模板里的 `composite-bg` 框（B/C 区），框内节点整体居中排列，距框边 ≥10px；框本身也要有一个在主状态机里可见的父节点 |
| `<<choice>>` 状态 | `node decision`（菱形），本质是守卫分支的可视化，不是一个真正的态 |
| `-->` 无 event 只有纯转移 | 仍然是 `edge`，标签留空即可，不必编造一个 trigger 文案 |
| `note ... end note` | 挂在最相关的状态或转移旁，或收进该节点的 nodeData body，不必强行画一个独立 note 图形（本模板节点详情走点击弹出的 aside 面板，不是画在图上的 note-box） |

**成功/失败态怎么判断**（PlantUML 语法本身不带这个信息，必须读语义）：看这个状态在业务上是不是"绝大多数正常流程会走到的终点"——是→`state-final success`（主终态，用 ⊙ 强调）；只有少数异常/退款/超时路径才会走到→`state-final fail`。普通中间态一律 `node state`，不要因为名字里带"失败""异常"字样就升级成 `state fail`——`state fail` 这个 class 是给"处于失败路径上、但还不是终点"的中间态用的，终点态要用 `state-final fail`，两者不是一回事。

---

## §4 Entity/IE Diagram → 05 ER

| PlantUML | 本 skill class |
|---|---|
| `entity "table_name" as t { ... }` | 一张 `g.node`（table-frame + table-header + table-title） |
| `*field : type`（`*` 前缀，主键/必填标记） | `.cell.pk` + `.tag-pk`（加粗），如果字段名语义上明显是主键（如 `xxx_id`）才归为 PK，`*` 在 PlantUML 里有时只表示"必填"不一定是主键，两者别混淆 |
| `field : type <<FK>>` | `.cell.fk` + `.tag-fk`（斜体） |
| 普通 `field : type` | `.cell`（不加 pk/fk 标记） |
| `<<generated>>` / `<<unique>>` / `<<not null>>` 等 stereotype | 对应 `.tag-idx` / `.tag-uq` / `.tag-nn`，贴在该字段行 |
| `EntityA \|\|--o{ EntityB` | 一条 `.er-edge`（正交走表间走廊，不能斜穿表体）+ 两端 `.crowfoot` 标记：`\|\|` 端画"两条短横"（恰好一个），`o{` 端画"圆圈+三叉"（零或多个） |
| 连接符是 `--`（实线） | identifying，子依赖父 |
| 连接符是 `..`（虚线） | non-identifying，弱关系/自引用 |
| `EntityA }o--o{ EntityB`（多对多） | 本 skill ER 模板按两张表间一条关系线设计，多对多场景建议还原出中间关联表（大多数真实数据库也是这么落地的），画成两条 1:N 关系而不是一条 M:N 线 |

crow's foot 端点对照速查（PlantUML 符号 → 视觉）：`||`=必有一个 / `o|`=零或一个 / `o{`=零或多个 / `|{`=一或多个。两端符号独立读，比如 `||--o{` 是"左边恰好一个，右边零或多个"，标准的 1:N。

---

## §5 Activity + `|Lane|`（泳道）→ 06 swimlane

**关键认知，容易判断反：PlantUML 的 `|Lane|` swimlane 原生渲染是纵向排列的（lane 是并排的列，从上到下走时间）**——这个结构对应本 skill 的 **06V（垂直泳道：lane 左右并排，phase 从上到下）**，不是 06H。判断顺序：

1. 默认选 **06V**：`|LaneA|` → `:action;` → `|LaneB|` → `:action;` … 这种"跳来跳去但整体往下走"的结构，直接对应 06V 的 lane 列 + phase 行。
2. 只有当用户的表达明确要"部门横向排布、时间左到右"（比如"画一条横向时间轴，各部门的泳道从上到下摆"），才改用 **06H**——这是 PlantUML 画不出来但用户明确想要的效果，此时 PlantUML 源码只提供逻辑顺序（谁在哪个 lane、先后顺序），布局方向按用户要求来，不是照抄 PlantUML 的默认渲染方向。

| PlantUML | 本 skill class（06V，默认） |
|---|---|
| `\|LaneName\|` | 一个 `lane`（lane-label 文字用这个名字），lane 中心 x 坐标见 catalog/06-swimlane-vertical.md「坐标约定」 |
| `start` / `:action;` | `node`，内部 shape 按语义选 `task-rect`（默认，user/service/send/receive 四种再细分）/ `gateway-shape`（判断）/ `event-start`（起） |
| `if () then () else () endif` 出现在某个 lane 内 | `gateway-shape` 菱形 + 分支边；分支语义/文字判断参考 §1 的判断分支规则 |
| `stop` | `event-end-bpmn` 或对应的终态 task |
| lane 间的顺序动作 | `vflow`（默认灰）；主路径 `vflow spine`；失败/驳回分支 `vflow fail`；跨 lane 的异步通知 `vflow msg`；很弱的旁路数据流 `vflow data`。**注意这四个 class 的基类是 `vflow`，不是 `edge`，也不是 06H 用的 `seq-flow`——三个模板边基类名互不相同，照抄错模板会导致边没有颜色（class 对不上 CSS 选择器）** |

06H（水平）时把上表的 `vflow` 系列换成 `seq-flow` / `seq-flow spine` / `seq-flow yes` / `seq-flow no` / `msg-flow`，其余节点映射逻辑相同，坐标约定见 catalog/06-swimlane.md。

---

## §6 Component / Deployment Diagram → 04 architecture 或 07 microservice

PlantUML 的 `package`/`node`/`cloud`/`component`/`database`/`queue`/`folder` 这套关键字本身不区分"抽象分层"还是"运行时部署"，要看内容判断落在 04 还是 07：

**判 04（抽象分层）**：源码里的分组是按"客户端 / 网关 / 服务 / 数据"这种逻辑层级组织的，`package`/`node` 的名字类似 `"Client Layer"`、`"Service Layer"`，看不到具体的 K8s/容器编排细节。

**判 07（运行时拓扑）**：源码里出现 namespace 边界（比如 `node "K8s Namespace: trade" { ... }`）、sidecar、服务网格（istio/envoy）、消息总线、服务注册中心，或者用了 C4-PlantUML 的 `Deployment_Node()`/`Container()` 宏——这些都是"这套系统实际怎么部署运行"的信息，04 的 tier-band 分层画法表达不出来。

两种情况的元素映射：

| PlantUML | 04 architecture | 07 microservice |
|---|---|---|
| `package "分层名" { ... }` | 一个 `tier-band`，`tier-name`/`tier-cn` 取分组名 | 一个 `row`（见 catalog/07-microservice.md「容器结构」，07 用 row 不用 tier-band） |
| 组内的 `component`/`rectangle`/`node` | 按业务角色选 `node client` / `node svc core` / `node svc trade` / `node mw` / `node data-store` 等，见 catalog/04-system-architecture.md「节点类型」 | 同 04 的选择逻辑，class 表一致，见 catalog/07-microservice.md「节点类型」 |
| `cloud "CDN"` / `database "MySQL"` / `queue "Kafka"` | `node edge-net`（CDN/网关类）/ `node data-store`（数据库）/ `node mw`（消息队列，中间件类） | 同左 |
| `node "K8s Namespace: xxx" { ... }`（有明确命名空间边界） | 无对应画法（04 本来就不表达运行时边界，出现这个特征本身就是该判 07 的信号） | 虚线方框包裹多个服务节点 + 一个 namespace 标签，见 catalog/07-microservice.md |
| 组间箭头 `-->` | 按语义选 `edge sync-arch`（同步调用）/ `edge rpc`（RPC）/ `edge async-event`（异步事件）/ `edge db-edge`（读写库）/ `edge cache-edge`（读写缓存）/ `edge cdc`（数据同步）/ `edge scrape`（监控抓取），主路径升级 `edge spine` | 同 04，class 表一致 |

C4-PlantUML（`!include C4_Container.puml` 之类）本质是一层宏封装，`Container(alias, "name", "tech", "desc")` 展开后就是一个带 4 行信息的节点（name/tech/desc 正好对应本 skill 节点卡片的"技术栈"行），`Rel(a, b, "desc")` 就是一条边——按上表同样的逻辑映射，多出来的"tech"字段正好可以填进 04/07 节点卡片本来就要求的技术栈那一行，不用丢弃。

---

## 一个小例子（走一遍提取过程）

输入：

```
@startuml
start
:接收提现申请;
if (余额充足?) then (是)
  :扣减余额;
  :写入 withdraw_bill 表;
  :调用银行代发接口;
  if (银行返回成功?) then (是)
    :标记已完成;
    stop
  else (否)
    :标记失败并退款;
    stop
  endif
else (否)
  :拒绝申请;
  stop
endif
@enduml
```

判定：`start`/`:action;`/`if then else`，无 `|Lane|` → **01 flowchart**（§0 规则 5）。

提取结果（给 Step 2 用的节点/边清单，不是最终坐标，坐标按 catalog/01-flowchart.md 正常排布）：

| 节点 | class | 备注 |
|---|---|---|
| 接收提现申请 | `node term` | 起点 |
| 余额充足? | `node decision` | |
| 扣减余额 | `node process` | |
| 写入 withdraw_bill 表 | `node db` | "写入…表"是本 skill 里识别数据库写操作的强信号，即使 PlantUML 里只是一个普通 `:action;` |
| 调用银行代发接口 | `node io` | 调外部系统，用平行四边形而不是普通 process |
| 银行返回成功? | `node decision` | |
| 标记已完成 | `node term success` | 主终态；"标记失败并退款"和"拒绝申请"都是失败终态 |
| 标记失败并退款 | `node term fail` | |
| 拒绝申请 | `node term fail` | |

边：接收→余额判断（`edge`）；余额判断 是→扣减余额（`edge yes`）/ 否→拒绝申请（`edge no`）；扣减余额→写库→调银行接口（`edge` 顺序流，写库前后那两条如果是同一事务，按 catalog/01-flowchart.md「事务边界」规则处理）；银行结果判断 是→已完成（`edge yes`）/ 否→标记失败（`edge no`）。

这一步做完之后，就是正常的 01 flowchart 建造流程：复制模板、按 catalog/01-flowchart.md 的坐标约定把上面这张表画出来、配 nodeData、改外壳、自检。PlantUML 只负责把"要画哪些节点、怎么连"想清楚，剩下的和不给 PlantUML、直接口头描述这个场景，是完全一样的流程。
