# 06H · 泳道图 · 水平 / Swimlane Horizontal

## 用在哪里
讲**跨角色/部门的协作流程**，**横向**展开时间。
强调**谁负责什么**（每个 lane 是一个角色）+ **时间从左到右**。

> 跨阶段而非跨角色 → 用 [06V 垂直泳道](./06-swimlane-vertical.md)
> 单角色流程 → 用 [01 流程图](./01-flowchart.md)

## 模板信息

- **模板文件**：`06-swimlane.html`
- **viewBox**：`1080 × 2660`（删 B 区后改为 **1080 × 1280**）
- **关键行号**
  - SVG 开始：446
  - A 区主图：465–805
  - **B 区元素图鉴：806–1163（删除）**
  - `</svg>`：1164
  - `window.DIAGRAM_CONFIG`：1255

## 删除 B 区步骤

1. Edit 删除 806–1163 整段
2. 改 svg height/viewBox 高度为 1280
3. 改 nodeData 顶部 `viewBox: { w: 1080, h: 1280 }`

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

| class | 何时用 |
|---|---|
| `node` 默认           | 任务（rect 圆角） |
| `gateway` shape       | XOR 网关（菱形） |
| `event` shape         | 触发事件（圆） |
| `event-end` shape     | 结束事件（粗圆） |
| `event-msg` shape     | 消息事件 |

## 边

| class | 视觉 | 何时用 |
|---|---|---|
| `seq-flow`        | gray 实线     | 默认顺序流 |
| `seq-flow spine`  | olive 加粗   | 主路径（happy path） |
| `seq-flow yes`    | olive        | YES 分支 |
| `seq-flow no`     | rust         | NO 分支 |

## 坐标约定

```
viewBox 1080 × 1280 (删 B 区后)
pool-header x=40, w=40
lane 区域 x=80, w=960
每个 lane 高 120 (默认)，pool 总高 = 140 + 120 × lane 数
节点矩形 90 × 50（横向密排）
任务节点 cy = lane 中心 y（lane_y + 60）
```

## 改造步骤

1. **复制**：`cp ~/.claude/skills/arch-diagrams/templates/06-swimlane.html <场景>-swimlane.html`
2. **删 B 区**：806-1163 + 改 svg height = 1280
3. **改 A 区**：
   - 决定 lane 数量（角色数）和顺序
   - 计算 pool 总高 = 140 起点 + 120 × N
   - 改每个 lane-header 的 y 和 label
   - 重画 lane-divider
   - 节点按时间从左到右排，跨 lane 用直角路径
4. **同步 nodeData**
5. **改外壳**

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
| `event-end`          | rust 粗圆     | 结束事件 |
| `gateway-shape`      | 菱形 + × 或 + | XOR / AND 网关 |
