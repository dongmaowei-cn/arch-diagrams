# 02 · 时序图 / Sequence Diagram

## 用在哪里
讲**多个角色按时间顺序怎么调用**。重点是"谁调谁、什么时候调、同步/异步/返回"。
强调**时间维度（自上而下）+ 跨参与者的消息**。

> 单主体的流程 → 用 [01 流程图](./01-flowchart.md)
> 整个系统物理结构 → 用 [04 架构图](./04-system-architecture.md)

## 模板信息

- **模板文件**：`02-sequence.html`
- **viewBox**：`1080 × 1500`
- **关键行号**
  - SVG 开始：365
  - A 区主图：377–608
  - `</svg>`：847
  - `window.DIAGRAM_CONFIG`：927



## 画法参考

- **元素图鉴 + 怎么画**：[`templates/index.html#sequence`](../templates/index.html#sequence)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 容器结构

时序图核心是 **lifeline 列 + phase frame**：

```
┌─────────────────────────────────────────────────┐
│  [Actor1]  [Actor2]  [Actor3]  [Actor4]   y=80  │
│     │         │         │         │             │
│  ┌──┴─── Phase 1 ──────────────┐    y=160-450  │
│  │  Activation rects + msgs    │               │
│  └─────────────────────────────┘               │
│  ┌──── Phase 2 ────────────────┐    y=486-762  │
│  ...                                            │
```

- **Actor 头部**：`y=80–130`，rect `120×50` + 可选 stick figure
- **Lifeline 间距**：建议 `200~240px`，每个 actor x 居中
- **Phase frame**：`<rect class="phase-frame">` 包住一段消息，左上挂 `<rect class="phase-tab">` + `<text class="t-phase">`
- **Activation**：`<rect class="activation">`，width=10，居 lifeline 中心 (cx-5 → cx+5)
  - 调用方的 activation 必须包含被调方（UML 规则）
- **Lifeline 末尾**：`<line class="lifeline" x1="cx" y1="130" x2="cx" y2="A区底">`

## 节点类型（actor 头）

| class | 视觉 | 何时用 |
|---|---|---|
| `node actor`          | gray 描边 + 头像火柴人 | 用户 / 客户端 |
| `node actor-system`   | plum 浅底 + plum 边    | 系统内部服务 |
| `node actor-external` | gold 浅底 + gold 边    | 外部系统（银行、第三方） |

## 边类型（消息）

| class | 视觉 | 何时用 |
|---|---|---|
| `edge sync`      | slate 实线 + arrow-slate | 同步调用 |
| `edge async msg` | plum 虚线 + arrow-plum   | 异步消息 |
| `edge return`    | gray 虚线 + arrow-open   | 返回值 |

消息标签：
```html
<g>
  <rect class="edge-label-bg" x="..." y="..." width="..." height="18" rx="3"/>
  <text class="edge-label" x="..." y="..." text-anchor="middle">POST /pay</text>
</g>
```

## 坐标约定

```
viewBox 1080 × 1500
Actor 数量    : 推荐 3-5 个，超过 6 个考虑拆分
Lifeline x   : 等距分布，例 120 / 300 / 520 / 740 / 960
Actor 头 y   : 80-130
Lifeline y   : 130 起，延伸到最后一条消息 + 20
Phase frame  : 把同一阶段的消息圈起来，左上贴 tab
Message y 间距: 30-40 px / 条
```

## 改造步骤（3 步）（5 步）

### Step 1 · 复制
```bash
cp ~/.claude/skills/arch-diagrams/templates/02-sequence.html \
   <output-dir>/<scenario>-sequence.html
```


### Step 2 · 改 A 区主图
1. 定 actor 列表与列位置（lifeline 间距 200~240）
2. 画 actor 头（顶端 y=80-130）
3. 画 lifeline 虚线
4. 用 phase frame 把消息分阶段
5. 画 activation rect（要嵌套正确）
6. 画消息边 + 标签

### Step 2 · 同步 nodeData
为每个 actor 添加 nodeData：
```js
'gateway': {
  type: 'actor-system', tagClass: 't-actor',
  title: 'API Gateway — 网关',
  meta: ['edge tier', 'Kong + JWT 插件', '30 万 QPS'],
  body: '<p>统一鉴权入口...</p>',
  tags: ['gateway', 'edge', 'jwt']
}
```

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row`
- 自检：每个 actor 有 nodeData；activation 嵌套对；lifeline 长度 ≥ 最后消息 y

## 反例

- ✗ 消息线斜着穿过其它 lifeline（必须正交，要么直接横到目标 lifeline，要么走 self-message 弧）
- ✗ 异步消息用 sync 样式（视觉欺骗）
- ✗ Activation 不嵌套（caller 比 callee 短）
- ✗ 用 actor-external 表达内部服务（应用 actor-system）

## 示例片段

```html
<!-- 同步消息 + 标签 -->
<g>
  <path class="edge sync" d="M125,205 L295,205" marker-end="url(#arrow-slate)"/>
  <rect class="edge-label-bg" x="160" y="194" width="100" height="18" rx="3"/>
  <text class="edge-label" x="210" y="207" text-anchor="middle">M1 · POST /pay</text>
</g>

<!-- 异步消息（plum 虚线） -->
<g>
  <path class="edge async msg" d="M525,580 L735,580" marker-end="url(#arrow-plum)"/>
  <text class="edge-label plum" x="630" y="574" text-anchor="middle">async · publish</text>
</g>

<!-- 返回 -->
<g>
  <path class="edge return" d="M735,640 L525,640" marker-end="url(#arrow-open)"/>
  <text class="edge-label" x="630" y="634" text-anchor="middle">return ok</text>
</g>
```
