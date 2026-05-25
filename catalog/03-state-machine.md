# 03 · 状态机 / State Machine

## 用在哪里
讲**一个对象在不同状态间怎么转移**：状态、转移条件（trigger / guard / action）。
强调**有限状态 + 守卫条件**，不强调时间或多角色。

> 多角色流程 → 用 [02 时序图](./02-sequence.md) / [06 泳道图](./06-swimlane.md)
> 一次性流程 → 用 [01 流程图](./01-flowchart.md)

## 模板信息

- **模板文件**：`03-state-machine.html`
- **viewBox**：`1080 × 1400`
- **关键行号**
  - SVG 开始：419
  - A 区主图：435–692
  - `</svg>`：989
  - `window.DIAGRAM_CONFIG`：1081



## 画法参考

- **元素图鉴 + 怎么画**：[`templates/index.html#state`](../templates/index.html#state)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 节点类型（state）

| class | 视觉 | 何时用 |
|---|---|---|
| `node state-initial`        | slate 实心圆        | 起始态（一个） |
| `node state`                | paper + gray 边     | 普通态 |
| `node state success`        | olive 浅底          | 成功路径态 |
| `node state fail`           | rust 浅底           | 失败路径态 |
| `node state-final`          | 同心圆（外圈实+内圈空） | 终态 |
| `node state-final success`  | 同上 + olive        | 成功终态 |
| `node state-final fail`     | 同上 + rust         | 失败终态 |
| `node decision`             | 菱形                | 守卫分支判断 |

## 边类型

| class | 视觉 | 何时用 |
|---|---|---|
| `edge`        | gray 实线    | 默认转移 |
| `edge yes`    | olive 实线   | 通过守卫 |
| `edge no`     | rust 虚线    | 拒绝/异常 |
| `edge spine`  | olive 加粗   | 主路径转移 |

**边标签**（UML 标准三段式 `trigger [guard] / action`）：
```html
<text class="edge-label trigger" x="..." y="...">submit</text>
<text class="edge-label guard"   x="..." y="...">[amount &gt; 0]</text>
<text class="edge-label action"  x="..." y="...">/ lock funds</text>
```

## 坐标约定

```
状态节点矩形       : 180 × 70 (rx=10)
终态外圈半径       : 22
普通态间距         : 200~240 px
主路径居中走 y 轴   : x=540
```

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/03-state-machine.html \
   <output-dir>/<scenario>-state-machine.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 起始 initial dot（圆）— 只能一个
2. 主路径状态从上到下，spine 串起
3. 终态用同心圆（success/fail 各占一边）
4. 守卫分支用 decision 菱形 + yes/no 出边
5. 每个 state 在 nodeData 添加一项，`tagClass: 't-state'` / `'t-success'` / `'t-fail'`
6. 若 A 区比模板矮，同步收紧 `<svg height>` / `viewBox` / `viewBox: { h }`

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row`
- 自检：每个 state 有 nodeData；只有一个 initial；每条 transition 有 trigger

## 反例

- ✗ 同一状态有 5 个以上出边（拆分子状态机）
- ✗ 起始态有多个（只能一个）
- ✗ 边标签写在线上没有 edge-label-bg 衬底（线穿过文字）

## 示例片段

```html
<!-- 起始态（实心圆） -->
<g class="node state-initial" data-id="start" tabindex="0">
  <circle class="shape" cx="520" cy="120" r="8"/>
</g>

<!-- 普通态（带 entry/do/exit UML 内部行为） -->
<g class="node state" data-id="awaiting" tabindex="0">
  <rect class="shape state-rect" x="340" y="380" width="120" height="90"/>
  <text class="t-title" x="400" y="402" text-anchor="middle">Awaiting</text>
  <line class="state-divider" x1="350" y1="410" x2="450" y2="410"/>
  <text class="state-body"    x="400" y="425" text-anchor="middle">entry / startTimer</text>
  <text class="state-body do" x="400" y="440" text-anchor="middle">do / pollStatus</text>
  <text class="state-body"    x="400" y="455" text-anchor="middle">exit / cancelTimer</text>
</g>

<!-- 成功子态 -->
<g class="node state success" data-id="sub-paid" tabindex="0">
  <rect class="shape state-rect" x="580" y="380" width="120" height="60"/>
  <text class="t-title" x="640" y="405" text-anchor="middle">Paid</text>
  <line class="state-divider" x1="590" y1="414" x2="690" y2="414"/>
  <text class="state-body" x="640" y="428" text-anchor="middle">exit / stopTimer</text>
</g>

<!-- 终态（同心圆） -->
<g class="node state-final success" data-id="settled" tabindex="0">
  <circle class="shape" cx="800" cy="980" r="20"/>
  <circle class="shape-inner" cx="800" cy="980" r="14"/>
</g>

<!-- 组合态外框（composite-bg + composite-tag） -->
<rect class="composite-bg" x="320" y="290" width="420" height="320"/>
<path class="composite-tag" d="M320,312 L320,306 Q320,290 336,290 L552,290 L552,312 Z"/>
<text class="composite-title-tag" x="330" y="307">composite · pending_payment</text>

<!-- 主路径转移（spine） + UML trigger + action 标签 -->
<path class="edge spine" d="M520,230 L520,290" marker-end="url(#arrow-olive)"/>
<rect class="edge-label-bg" x="528" y="248" width="56" height="13"/>
<text class="edge-label trigger" x="532" y="258">submit()</text>
<rect class="edge-label-bg" x="528" y="266" width="100" height="13"/>
<text class="edge-label action" x="532" y="276">/ lockInventory()</text>

<!-- 失败转移（rust + guard） -->
<path class="edge no" d="M400,470 L400,520" marker-end="url(#arrow-rust)"/>
<rect class="edge-label-bg" x="408" y="487" width="64" height="13"/>
<text class="edge-label trigger" x="412" y="497">after(15min)</text>

<!-- 自转移（self-loop，弧线） -->
<path class="edge" d="M 420,380 A 22,18 0 0 0 380,380" marker-end="url(#arrow)"/>
<rect class="edge-label-bg" x="377" y="343" width="46" height="13"/>
<text class="edge-label trigger" x="400" y="353" text-anchor="middle">retry [n&lt;3]</text>
```

## 关键 class 速查

| class | 用途 |
|---|---|
| `composite-bg`              | 组合态外框（圆角矩形 + olive 浅底） |
| `composite-tag` + `composite-title-tag` | 组合态左上角标签 |
| `state-rect` + `state-divider`           | 状态的矩形 + 分隔线 |
| `state-body`                | UML entry/exit/internal action |
| `state-body do`             | UML do 行为（高亮） |
| `edge-label trigger`        | 转移触发条件（如 `submit()`） |
| `edge-label guard`          | 守卫条件（如 `[amount > 0]`，clay 色） |
| `edge-label action`         | 转移动作（如 `/ lockInventory()`） |
