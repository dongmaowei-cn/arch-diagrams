# 02 · 时序图 / Sequence Diagram

## 用在哪里
讲**多个角色按时间顺序怎么调用**。重点是"谁调谁、什么时候调、同步/异步/返回"。
强调**时间维度（自上而下）+ 跨参与者的消息**。

> 单主体的流程 → 用 [01 流程图](./01-flowchart.md)
> 整个系统物理结构 → 用 [04 架构图](./04-system-architecture.md)

## 模板信息（canonical · 批量代发 Job 跨域交互）

- **模板文件**：`02-sequence.html`
- **viewBox**：`1080 × 1240`
- **关键行号**
  - SVG 开始：365
  - A 区主图：366–530
  - `</svg>`：531
  - `window.DIAGRAM_CONFIG`：597
- **内容**：5 参与者（XxlJob actor / clearing_server · cldb · bac actor-system / 招行薪福通 actor-external）· 3 阶段 · 15 条消息（①-⑮）· Phase 3 内嵌 `alt` 双分支 · 底部折角注释（维度对齐）

## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/02-sequence.html`](../templates/gallery/02-sequence.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 容器结构

```
┌─────────────────────────────────────────────────┐
│  [Actor1]  [Actor2]  [Actor3]  [Actor4]   y=80  │
│     │         │         │         │             │
│  ┌──┴─── Phase 1 ──────────────┐    y=160-350  │
│  │  Activation rects + msgs    │               │
│  └─────────────────────────────┘               │
│  ┌──── Phase 2 ────────────────┐    y=370-610  │
│  ┌──── Phase 3 ────────────────┐    y=630-1002 │
│  │   … 内嵌 alt fragment        │    y=770-994  │
│  └─────────────────────────────┘               │
│  ┌─ 折角注释 note-box（右缘对齐 phase-frame）─┐   y=1050-1220 │
```

- **Actor 头部**：`y=80–130`，rect `200×50`（XxlJob 用 actor 火柴人，内部系统 actor-system，外部 actor-external）
- **Lifeline 间距**：模板用 `170px`（x = 120 / 290 / 460 / 630 / 800）
- **Phase frame**：`<rect class="phase-frame">` 包住一段消息，左上挂 `<rect class="phase-tab">` + `<text class="t-phase">`
- **Activation**：`<rect class="activation">`，width=10，居 lifeline 中心 (cx-5 → cx+5)
- **fragment（alt/loop/opt）**：`<rect class="fragment">` 虚线框 + `<rect class="fragment-tab">` + `<text class="t-frag">` + `<text class="t-cond">` 守卫 + `<line class="fragment-divider">` 分隔
  - **alt 必须内嵌在它所属的 phase 内部**，不要独立成一个 phase
- **Lifeline 末尾**：`<line class="lifeline" x1="cx" y1="130" x2="cx" y2="A区底">`

## 节点类型（actor 头）

| class | 视觉 | 何时用 |
|---|---|---|
| `node actor`          | gray 描边 + 头像火柴人 | 用户 / 客户端 / Job 触发器 |
| `node actor-system`   | plum 浅底 + plum 边    | 系统内部服务 |
| `node actor-external` | gold 浅底 + gold 边    | 外部系统（银行、第三方） |

## 边类型（消息）

| class | 视觉 | 何时用 |
|---|---|---|
| `edge sync`      | slate 实线 + arrow-sync  | 同步调用 |
| `edge async msg` | plum 虚线 + arrow-plum   | 异步消息 |
| `edge return`    | gray 虚线 + arrow-open   | 返回值 |
| `edge`（U 形 self-message） | slate 实线折角 | 自调用 / 内部处理 |

消息序号：`<text class="t-ord">①…⑮</text>` 放在消息线起点侧；消息标签 `<text class="t-msg">` + 副标 `<text class="t-msg-ret">`。

## Activation 纪律（edge-check [9] 强制）

时序图的激活条是**语义容器**，不是装饰。三条规则：

1. **覆盖**：每条贴 lifeline 的消息端点（起/终）y 必须落在该 lifeline 某激活条的 y 区间内（容差 ±6px，允许箭头在条顶上方 ~5px 设计间距）。
   - 反例：最后一条自环回程 y=982，激活条只画到 972 → "激活条没盖住消息"，edge-check [9] 拦
2. **贴边**：端点 x 必须贴激活条左/右边缘（±2px），不能落在条中心/lifeline 上。
   - 反例：消息从激活条中心 x=cx 出发/进入 → "线从图形内部进出"，edge-check [9] 拦
3. **嵌套**：调用方激活条必须覆盖被调方（caller ≥ callee，UML 规则）。

## 折角注释纪律

底部 `note-box`（折角注释）用于放字段对齐/幂等键等横切信息：

- 框**右缘对齐 phase-frame 右缘**（模板 860），不向右突出
- 文本从 x=+12 起排，**不能溢出框右缘**（改字段链文案时先估宽：mono 10.5px ≈ 6.3px/字符，CJK ≈ 10.5px/字）

## 坐标约定

```
viewBox 1080 × 1240
Actor 数量    : 推荐 3-5 个，超过 6 个考虑拆分
Lifeline x   : 模板 120 / 290 / 460 / 630 / 800（间距 170）
Actor 头 y   : 80-130
Lifeline y   : 130 起，延伸到最后一条消息 + 20
Phase frame  : 把同一阶段的消息圈起来，左上贴 tab
Message y 间距: 30-40 px / 条
fragment     : 右缘比所属 phase-frame 内缩 ~16px 形成嵌套层次
```

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/02-sequence.html \
   <output-dir>/<scenario>-sequence.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 定 actor 列表与列位置（lifeline 间距 200~240，模板 170 起步）
2. 画 actor 头（顶端 y=80-130）
3. 画 lifeline 虚线
4. 用 phase frame 把消息分阶段；有分支时在**所属 phase 内**嵌 alt fragment
5. 画 activation rect：**覆盖所有消息 + 端点贴条边 + 嵌套正确**
6. 画消息边 + 序号 ①-⑮ + 标签
7. 需要时加底部折角注释（右缘对齐 frame）
8. 为每个 actor 添加 nodeData：
```js
'clearing': {
  type: 'actor-system', tagClass: 't-actor',
  title: 'clearing_server — 清结算',
  meta: ['TX 边界', '唯一写库者', 'XxlJob 驱动'],
  body: '<p>清结算核心服务...</p>',
  tags: ['clearing', 'tx', 'job']
}
```

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row` / `.section-sub`（阶段数 · 消息数 · 参与者数）
- 自检：`bash $SKILL_DIR/shared/selftest.sh <output.html>` 8/8；edge-check 含 [9] 激活条

## 反例

- ✗ 消息线斜着穿过其它 lifeline（必须正交，要么直接横到目标 lifeline，要么走 self-message 弧）
- ✗ 异步消息用 sync 样式（视觉欺骗）
- ✗ Activation 不嵌套（caller 比 callee 短）
- ✗ 激活条没盖住最后一条消息 / 消息从激活条中心进出（edge-check [9] 拦）
- ✗ alt fragment 独立成 phase（必须内嵌在所属 phase 内）
- ✗ 折角注释右缘超出 phase-frame 右缘 / 文本溢出框（对不齐、文字探出）
- ✗ 用 actor-external 表达内部服务（应用 actor-system）

## 示例片段

```html
<!-- Phase 3 内嵌 alt 双分支（成功/失败并列） -->
<rect class="fragment" x="52" y="770" width="792" height="224" rx="4"/>
<rect class="fragment-tab" x="52" y="756" width="46" height="22" rx="3" ry="3"/>
<text class="t-frag" x="64" y="771">alt</text>

<text class="t-cond" x="64" y="796">[ 受理成功 · code=200 ]</text>
<path class="edge return" d="M625,806 L295,806"/>

<line class="fragment-divider" x1="52" y1="836" x2="844" y2="836"/>

<text class="t-cond" x="64" y="858">[ 受理失败 · code≠200 / 抛异常 ]</text>
<path class="edge sync" d="M295,868 L455,868"/>

<!-- 同步消息 + 序号 + 标签 -->
<text class="t-ord" x="305" y="656">⑨</text>
<path class="edge sync" d="M295,666 L625,666"/>
<text class="t-msg" x="305" y="661">payrollUpdateExecute(request)</text>
<text class="t-msg-ret" x="305" y="678">SM4+SM3withSM2 签名</text>
```
