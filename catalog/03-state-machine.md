# 03 · 状态机 / State Machine

## 用在哪里
讲**一个对象在不同状态间怎么转移**：状态、转移条件（trigger / guard / action）。
强调**有限状态 + 守卫条件**，不强调时间或多角色。

> 多角色流程 → 用 [02 时序图](./02-sequence.md) / [06 泳道图](./06-swimlane.md)
> 一次性流程 → 用 [01 流程图](./01-flowchart.md)
> 同一主状态机有**伴生子状态机**（如批次状态、账务流水状态）→ 也用本模板，底部 A 区迁移派生视图

## 模板信息

- **模板文件**：`03-state-machine.html`
- **viewBox**：`1080 × 1660`
- **结构**：A 区主状态机 + B/C 两个 `composite-bg` 子状态机（A 区迁移派生的联动视图）
- **关键行号**
  - SVG 开始：419
  - A 区主图（Edges + States）：432–590
  - B 子状态机（composite-bg）：592–631
  - C 子状态机（composite-bg）：634–687
  - `</svg>`：688
  - `window.DIAGRAM_CONFIG`：756（`nodeData` 22 项，`exportName` 758）

## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/03-state-machine.html`](../templates/gallery/03-state-machine.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 节点类型（state）

| class | 视觉 | 何时用 |
|---|---|---|
| `node state-initial`        | slate 实心圆        | 起始态（一个） |
| `node state`                | paper + gray 边     | 普通态 |
| `node state success`        | olive 浅底          | 成功路径态 |
| `node state fail`           | rust 浅底           | 失败路径态 |
| `node state-final`          | 同心圆（外圈实+内圈空） | 终态 |
| `node state-final success`  | 同上 + olive        | **主终态**（绝大多数单子止于此，如「已提现」） |
| `node state-final fail`     | 同上 + rust         | 失败/补偿终态 |
| `node decision`             | 菱形                | choice 伪状态 / 守卫分支 |

> **终态建模**：业务上「绝大多数单子止于」的状态应标成 `state-final success`（主终态 ⊙），
> 而不是普通矩形 —— 矩形暗示"还能继续走"。低频补偿路径（如退票）用 `state-final fail` 另起一个 ⊙，
> 中间用 rust 虚线连低频 Job 触发边。

## 边类型

| class | 视觉 | 何时用 |
|---|---|---|
| `edge`        | gray 实线    | 默认转移 |
| `edge yes`    | olive 实线   | 通过守卫 |
| `edge no`     | rust 虚线    | 拒绝/异常/低频补偿 |
| `edge spine`  | olive 加粗   | 主路径转移 |

**边标签**（UML 标准三段式 `trigger [guard] / action`）：
```html
<text class="edge-label trigger" x="..." y="...">submit</text>
<text class="edge-label guard"   x="..." y="...">[amount &gt; 0]</text>
<text class="edge-label action"  x="..." y="...">/ lock funds</text>
```

## 坐标约定

```
主列中心 x       = 400（主路径垂直串行）
状态节点矩形     : x=300, width=200, height=60~80 (rx=10)
判断菱形         : 顶/底 y 差 80, 左/右 x 差 70（外包框 140×80）
终态同心圆       : r=22 外圈, r=16 内圈
起始态实心圆     : r=9，只能一个
B/C 子状态机     : composite-bg 框内节点居中排, 距框边 ≥ 10px
```

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/03-state-machine.html \
   <output-dir>/<scenario>-state-machine.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 起始 initial dot（圆）— 只能一个；**留给它的出边 ≥ 30px**（别让箭头贴着第一个状态）
2. 主路径状态从上到下，spine 串起
3. 终态用同心圆（主终态 success ⊙ / 失败补偿 fail ⊙ 分列两侧）
4. 守卫分支用 decision 菱形 + yes/no 出边
5. 若有伴生子状态机（批次/账务等），复制模板 B/C 的 `composite-bg` 结构 —— 框内节点**必须完整落在框内**（探出框边 = 布局没对齐）
6. 每个 state 在 nodeData 添加一项，`tagClass: 't-state'` / `'t-success'` / `'t-fail'`
7. 若 A 区比模板矮，同步收紧 `<svg height>` / `viewBox` / `viewBox: { h }`

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row`
- 自检：每个 state 有 nodeData；只有一个 initial；每条 transition 有 trigger
- 跑 `shared/selftest.sh`（含 edge-check 7 项子检查）

## 反例

- ✗ 同一状态有 5 个以上出边（拆分子状态机）
- ✗ 起始态有多个（只能一个）
- ✗ 边标签写在线上没有 edge-label-bg 衬底（线穿过文字）
- ✗ 自环/弧线**弯进节点身体**（自环必须凸出节点外侧；edge-check [5] 会拦）
- ✗ 子状态机节点**探出 composite 框**（edge-check [6] 会拦）
- ✗ 边标签**压在无关节点身上**（edge-check [7] 会拦；bus 线骑线标签豁免）
- ✗ 把所有终态都画成普通矩形（主终态应标 success ⊙）

## 示例片段

```html
<!-- 起始态（实心圆）+ 出边 ≥30px -->
<g class="node state-initial" data-id="start" tabindex="0">
  <circle class="shape" cx="400" cy="104" r="9"/>
</g>
<path class="edge spine" d="M400,113 L400,150" marker-end="url(#arrow-olive)"/>

<!-- 普通态（带 entry/do/exit UML 内部行为） -->
<g class="node state" data-id="awaiting" tabindex="0">
  <rect class="shape state-rect" x="300" y="290" width="200" height="60"/>
  <text class="t-title" x="400" y="315" text-anchor="middle">待处理</text>
  <line class="state-divider" x1="310" y1="325" x2="490" y2="325"/>
  <text class="state-body"    x="400" y="341" text-anchor="middle">entry / startTimer</text>
</g>

<!-- choice 判断（菱形） -->
<g class="node decision" data-id="judge" tabindex="0">
  <path class="shape" d="M400,150 L470,190 L400,230 L330,190 Z"/>
  <text class="t-title" x="400" y="186" text-anchor="middle">分账判定</text>
  <text class="t-sub" x="400" y="202" text-anchor="middle">transferAmount &gt; 0?</text>
</g>

<!-- 主终态（橄榄同心圆） -->
<g class="node state-final success" data-id="withdrawn" tabindex="0">
  <circle class="shape" cx="400" cy="1130" r="22"/>
  <circle class="shape-inner" cx="400" cy="1130" r="16"/>
  <text class="t-title" x="400" y="1162" text-anchor="middle">已提现</text>
  <text class="t-sub" x="400" y="1178" text-anchor="middle">balance- · freeze-</text>
</g>

<!-- 伴生子状态机（composite 框 + 节点居中、不外探） -->
<rect class="composite-bg" x="40" y="1350" width="480" height="290"/>
<path class="composite-tag" d="M40,1372 L40,1366 Q40,1350 56,1350 L340,1350 L340,1372 Z"/>
<text class="composite-title-tag" x="50" y="1367">B · 批次状态 batch.status</text>
<!-- 框内节点必须满足: 左/右/上/下 距框边 ≥ 10px -->

<!-- 主路径转移（spine）+ UML trigger + action 标签 -->
<path class="edge spine" d="M400,350 L400,420" marker-end="url(#arrow-olive)"/>
<rect class="edge-label-bg" x="408" y="372" width="96" height="13"/>
<text class="edge-label trigger" x="412" y="382">分账Job 发起</text>

<!-- 自环（自环必须凸出节点外侧；edge-check [5] 采样验证） -->
<path class="edge" d="M500,864 C544,864 544,898 500,898" marker-end="url(#arrow)"/>
<rect class="edge-label-bg" x="552" y="866" width="88" height="13"/>
<text class="edge-label trigger" x="556" y="876">P 处理中</text>
```

## 关键 class 速查

| class | 用途 |
|---|---|
| `composite-bg`              | 子状态机外框（圆角矩形 + olive 浅底虚线框） |
| `composite-tag` + `composite-title-tag` | 子状态机左上角标签 |
| `state-rect` + `state-divider`           | 状态的矩形 + 分隔线 |
| `state-body`                | UML entry/exit/internal action |
| `state-body do`             | UML do 行为（高亮） |
| `edge-label trigger`        | 转移触发条件（如 `submit()`） |
| `edge-label guard`          | 守卫条件（如 `[amount > 0]`，clay 色） |
| `edge-label action`         | 转移动作（如 `/ lockInventory()`） |
