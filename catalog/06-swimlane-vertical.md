# 06V · 泳道图 · 垂直 / Swimlane Vertical

## 用在哪里
讲**跨阶段流程**，**纵向**展开阶段。
强调**阶段（phase）从上到下** × **角色（lane）从左到右** 的矩阵。

> 跨角色横向时间 → 用 [06H 水平泳道](./06-swimlane.md)
> 单一角色 → 用 [01 流程图](./01-flowchart.md)

## 模板信息

- **模板文件**：`06-swimlane-vertical.html`
- **viewBox**：`1080 × 2680`（删 B 区后改为 **1080 × 1340**）
- **关键行号**
  - SVG 开始：442
  - A 区主图：460–695
  - **B 区元素图鉴：696–934（删除）**
  - `</svg>`：935
  - `window.DIAGRAM_CONFIG`：1021

## 删除 B 区步骤

1. Edit 删除 696–934 整段
2. 改 svg height/viewBox 高度为 1340
3. 改 nodeData 顶部 `viewBox: { w: 1080, h: 1340 }`

## 容器结构

垂直泳道 = **顶端横向 lane header + 左侧纵向 phase header**：

```
        Lane 1      Lane 2      Lane 3      Lane 4
        用户        前端        网关        服务
       ┌──────────┬──────────┬──────────┬──────────┐
Phase 1│  [任务]  │          │  [任务]  │          │
设计   │          │  [任务]  │          │          │
       ├──────────┼──────────┼──────────┼──────────┤
Phase 2│          │  [任务]  │  [任务]  │  [任务]  │
开发   │          │          │          │          │
       ├──────────┼──────────┼──────────┼──────────┤
Phase 3│          │          │          │  [任务]  │
测试   │          │          │          │          │
       └──────────┴──────────┴──────────┴──────────┘
```

- `<rect class="phase-band">`：每个 phase 一条横向带
- `<rect class="lane-header-top">`：顶端角色名
- `<text class="lane-label">` + `<text class="lane-en">`：角色中文/英文
- `<text class="t-phase">`：phase 名
- `<line class="lane-divider-vert">`：lane 之间的竖线

## 节点与边

节点和 06H 一致：默认 `node` + `gateway` 菱形 + `event` 圆。
边类型：`seq-flow` / `seq-flow spine` / `seq-flow yes` / `seq-flow fail` + `edge-label yes` / `edge-label fail`。

## 坐标约定

```
viewBox 1080 × 1340 (删 B 区后)
顶端 lane-header 高 60
4 lane 时每 lane 宽 240
phase 高 250~300
节点矩形 180 × 50
任务 cx = lane 中心
```

## 改造步骤

1. **复制**：`cp ~/.claude/skills/arch-diagrams/templates/06-swimlane-vertical.html <场景>-swimlane-vertical.html`
2. **删 B 区**：696-934 + 改 svg height = 1340
3. **改 A 区**：
   - 决定 lane 数（横向角色，3-5）和 phase 数（纵向阶段，3-5）
   - 改 lane-header 与 phase-band 容器
   - 每个 phase × lane 格子里放任务
   - 跨格子边走直角，主路径 spine 加粗
4. **同步 nodeData**
5. **改外壳**

## 反例

- ✗ 一个 phase 全部 lane 都空（删掉这个 phase）
- ✗ 任务跨 lane 边界（应贴住所在 lane 中心）

## 示例片段

```html
<!-- Pool 外框 -->
<rect class="pool-frame" x="40" y="150" width="1000" height="1240"/>

<!-- Lane header row 底边线 -->
<line class="lane-header-rule" x1="40" y1="210" x2="1040" y2="210"/>
<!-- Phase 列右边线 -->
<line class="phase-col-rule" x1="120" y1="210" x2="120" y2="1390"/>

<!-- 4 lane 竖向分隔线 -->
<line class="lane-divider" x1="350" y1="210" x2="350" y2="1390"/>
<line class="lane-divider" x1="580" y1="210" x2="580" y2="1390"/>
<line class="lane-divider" x1="810" y1="210" x2="810" y2="1390"/>

<!-- Lane header 文字（cx 居 lane 中心：235/465/695/925） -->
<text class="lane-kicker" x="80" y="185" text-anchor="middle">Phase</text>
<text class="lane-label"  x="235" y="183" text-anchor="middle">Customer</text>
<text class="lane-sub"    x="235" y="200" text-anchor="middle">external actor</text>

<!-- Phase 编号（左侧列，单字符竖排） -->
<text class="phase-num"  x="80" y="240" text-anchor="middle">01</text>
<text class="phase-name" x="80" y="285" text-anchor="middle">
  <tspan x="80" dy="0">I</tspan><tspan x="80" dy="14">n</tspan>
  <tspan x="80" dy="14">i</tspan><tspan x="80" dy="14">t</tspan>
</text>

<!-- Phase 之间水平分隔 -->
<line class="phase-divider-rule" x1="120" y1="480" x2="1040" y2="480"/>

<!-- 任务节点 -->
<g class="node" data-id="submit" tabindex="0">
  <rect class="task-rect shape" x="180" y="310" width="130" height="50"/>
  <text class="task-name" x="245" y="332" text-anchor="middle">填写表单</text>
  <text class="task-sub"  x="245" y="346" text-anchor="middle">User Task</text>
</g>

<!-- 起始事件 + 主路径边 -->
<circle class="event-start" cx="235" cy="245" r="10"/>
<path class="vflow spine" d="M235,255 L235,290" marker-end="url(#arrow-olive)"/>

<!-- 跨 lane 边（带标签） -->
<path class="vflow spine" d="M310,335 L390,335"/>
<rect class="edge-label-bg" x="318" y="319" width="64" height="13"/>
<text class="edge-label" x="350" y="329" text-anchor="middle">submit</text>

<!-- 空格子占位（某 phase × lane 没任务） -->
<text class="cell-empty" x="695" y="350" text-anchor="middle">—</text>
```

## 类型速查

| class | 用途 |
|---|---|
| `pool-frame`        | 外层圆角白底卡片 |
| `lane-header-rule`  | 顶端 lane 行底边线 |
| `phase-col-rule`    | 左侧 phase 列右边线 |
| `lane-divider`      | lane 间竖分隔 |
| `phase-divider-rule`| phase 间横分隔 |
| `phase-num`         | phase 编号（serif） |
| `phase-name`        | phase 名（竖排，单字符 tspan） |
| `lane-label`        | lane 主名 |
| `lane-sub`          | lane 副标 |
| `vflow`             | 默认顺序流（竖向） |
| `vflow spine`       | 主路径加粗 |
| `cell-empty`        | 空格子占位（"—"） |
