# 06H · 泳道图 · 水平 / Swimlane Horizontal

## 用在哪里
讲**跨角色/部门的协作流程**，**横向**展开时间。
强调**谁负责什么**（每个 lane 是一个角色）+ **时间从左到右**。

> 跨阶段而非跨角色 → 用 [06V 垂直泳道](./06-swimlane-vertical.md)
> 单角色流程 → 用 [01 流程图](./01-flowchart.md)

## 模板信息

- **模板文件**：`06-swimlane.html`
- **viewBox**：`1080 × 1000`（对应模板默认的 6 条 lane；lane 数变化时需重算，见「坐标约定」）
- **关键行号**（如与实际文件不符，以 `grep -n 'DIAGRAM_CONFIG\|</svg>' 06-swimlane.html` 现场核实为准，行号会随模板迭代漂移）
  - SVG 开始：446
  - A 区主图：465–595
  - `</svg>`：596
  - `window.DIAGRAM_CONFIG`：656



## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/06-swimlane.html`](../templates/gallery/06-swimlane.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 容器结构

水平泳道 = **pool（外框）+ N 个横向 lane**：

```
┌───┬─────────────────────────────────────────────┐
│ P │ Lane 1 · 用户       [start]→[submit]        │
│ O ├─────────────────────────────────────────────┤
│ O │ Lane 2 · 订单服务         [validate]→...    │
│ L ├─────────────────────────────────────────────┤
│   │ Lane 3 · 支付网关              [...]        │
│   ├─────────────────────────────────────────────┤
│   │ Lane 4 · 仓库                  ...          │
└───┴─────────────────────────────────────────────┘
```

- `<rect class="pool-header">`：左侧竖条（pool 名 + 旋转 -90°）
- `<rect class="pool">`：外框
- `<rect class="lane-header">`：每个 lane 左侧 120×lane高 的"角色名" header
- `<line class="lane-divider">`：lane 分隔线
- `<text class="lane-label">`：lane 中文名
- `<text class="task-sub">`：lane 英文副标

## 节点（任务/事件）

外层 `<g class="node" data-id="...">` 统一，内层 shape 元素的 class 决定形状/颜色（精确 class 名，别按感觉拼写——拼错一个字都会静默不生效）：

| class（写在内层 shape 元素上） | 何时用 |
|---|---|
| `task-rect shape`（+ user/service/send/receive，见下方「任务类型速查」） | 任务（圆角矩形） |
| `gateway-shape shape` | XOR/AND 网关（菱形） |
| `event-start shape` | 触发/起始事件（圆） |
| `event-end-bpmn shape` | 结束事件（粗圆，注意不是 `event-end`） |

`event-msg` 是例外——它不是内层 shape class，是**外层 `<g class="node event-msg">` 上的修饰类**，靠 `.node.event-msg .shape` 后代选择器给里面不管哪种 shape 上色（用于"这个节点代表一条消息"的场景，如收款回执），写的时候加在 `<g>` 上而不是内层 shape 元素上，和上面几个正好相反。

## 边

| class | 视觉 | 何时用 |
|---|---|---|
| `seq-flow`        | gray 实线     | 默认顺序流 |
| `seq-flow spine`  | olive 加粗   | 主路径（happy path） |
| `seq-flow yes`    | olive        | 网关 YES / 通过分支 |
| `seq-flow no`     | rust 虚线    | 网关 NO / 拒绝分支 |
| `msg-flow`        | plum 虚线 + 空心圆起点 | 跨 lane 异步消息（如"打款指令"“到账回执”） |

## 坐标约定

```
viewBox 1080 × 1000（模板默认 6 lane；lane 数变化按下式重算）
pool-header x=40, w=40
lane 区域 x=80, w=960
每个 lane 高 120 (默认)，pool 总高 = 140 + 120 × lane 数
viewBox 高 = pool 总高 + ~140 留白（放跨 lane message flow 和标签）
节点矩形 90 × 50（横向密排）
任务节点 cy = lane 中心 y（lane_y + 60）
```

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/06-swimlane.html \
   <output-dir>/<scenario>-swimlane.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 决定 lane 数量（角色数）和顺序
2. 计算 pool 总高 = 140 起点 + 120 × N
3. 改每个 lane-header 的 y 和 label；重画 lane-divider
4. 节点按时间从左到右排，跨 lane 用直角路径
5. 同步 nodeData；若 lane 数变化，按「坐标约定」公式重算并同步 viewBox（模板默认 h=1000）

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row`
- 自检：每个 task 落在正确 lane；跨 lane 边用 message flow 虚线

## 反例

- ✗ 节点画到 lane 外（"用户"做"打款"是逻辑错误）
- ✗ 主路径不用 spine（看不出 happy path）
- ✗ 时间方向反了（必须左 → 右）

## 示例片段

```html
<!-- Lane 容器 -->
<rect class="lane-header" x="80" y="260" width="120" height="120"/>
<text class="lane-label" x="140" y="316" text-anchor="middle">订单服务</text>
<text class="task-sub"   x="140" y="334" text-anchor="middle">Order Service</text>
<line class="lane-divider" x1="80" y1="380" x2="1040" y2="380"/>

<!-- 起始事件（圆） -->
<g class="node" data-id="start" tabindex="0">
  <circle class="event-start shape" cx="235" cy="200" r="18"/>
</g>

<!-- 用户任务（task-rect user） -->
<g class="node" data-id="submit-order" tabindex="0">
  <rect class="task-rect user shape" x="295" y="172" width="92" height="56"/>
  <text class="task-name" x="341" y="194" text-anchor="middle">提交订单</text>
  <text class="task-sub" x="341" y="208" text-anchor="middle">User Task</text>
  <text class="task-icon-mini" x="304" y="186">👤</text>
</g>

<!-- 服务任务（task-rect service） -->
<g class="node" data-id="validate" tabindex="0">
  <rect class="task-rect service shape" x="385" y="282" width="92" height="56"/>
  <text class="task-name" x="431" y="304" text-anchor="middle">校验库存</text>
  <text class="task-sub" x="431" y="318" text-anchor="middle">Service Task</text>
  <text class="task-icon-mini" x="394" y="296">⚙</text>
</g>

<!-- XOR 网关（菱形） -->
<g class="node" data-id="gw-stock" tabindex="0">
  <path class="gateway-shape shape" d="M505,310 L523,288 L541,310 L523,332 Z"/>
  <text class="gateway-mark"  x="523" y="316" text-anchor="middle">×</text>
  <text class="gateway-label" x="523" y="276" text-anchor="middle">stock?</text>
</g>

<!-- 主路径 spine 边 + 标签 -->
<path class="seq-flow spine" d="M255,200 L295,200" marker-end="url(#arrow-olive)"/>
<rect class="flow-label-bg" x="220" y="190" width="60" height="14"/>
<text class="flow-label" x="250" y="201" text-anchor="middle">submit</text>
```

## 任务类型速查

| class | 视觉 | 用途 |
|---|---|---|
| `task-rect user`     | gold 边 + 👤 | 用户任务（需人工操作） |
| `task-rect service`  | gray 边 + ⚙ | 服务任务（系统自动） |
| `task-rect send`     | plum 边 + ✉ | 发送消息任务 |
| `task-rect receive`  | plum 虚边     | 接收消息任务 |
| `event-start`        | olive 实心圆  | 起始事件 |
| `event-intermediate` | 双圈          | 中间事件（timer / message） |
| `event-end-bpmn`     | rust 粗圆     | 结束事件 |
| `gateway-shape`      | 菱形 + × 或 + | XOR / AND 网关 |
