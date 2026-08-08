# 01 · 业务流程图 / Flowchart

## 用在哪里
讲**一个流程**从触发到终态：有判断分支、有 YES/NO、可能写库或调外部。
单一主体视角（不区分谁做的），强调**做什么 → 接下来做什么**。

> 涉及多角色协作 → 用 [06 泳道图](./06-swimlane.md)
> 涉及对象状态变化 → 用 [03 状态机](./03-state-machine.md)

## 模板信息（canonical · 批量代发 Job 领域内流转）

- **模板文件**：`01-flowchart.html`
- **viewBox**：`1080 × 1500`
- **关键行号**
  - SVG 开始：285
  - A 区主图：286–455
  - `</svg>`：456
  - `const NODE_DATA`：578
- **内容**：19 节点 / 18 边 · 主流程轴线 x=480 · 2 个判断（空列表 / 受理成功）· 2 个事务边界（TX1 落库 / TX2 回滚）· 左右双 DB 柱（batch_record · trade_flow · withdraw_bill ｜ wallet）

## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/01-flowchart.html`](../templates/gallery/01-flowchart.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 模板保留内容

- A 区 SVG 主图
- aside.panel.detail（点击节点弹详情）
- aside.legend-group（紧凑图例，保留在模板内）
- 外壳（topbar / footer / canvas-controls）

> 元素图鉴 + 详细画法说明在 `templates/gallery/01-flowchart.html`。

## 节点类型（class）

| class | 形状 | 视觉 | 何时用 |
|---|---|---|---|
| `node term`         | 胶囊矩形 (rx=17) | gray-150 底 | START 起始事件 |
| `node term success` | 胶囊矩形 | olive 浅底 | 成功终态（如 SUCCESS / ONGOING） |
| `node term fail`    | 胶囊矩形 | rust 浅底  | 失败终态（如 FAILURE） |
| `node process`      | 直角矩形 | paper 底  | 处理动作（动词） |
| `node decision`     | 菱形    | paper 底  | 二元判断 |
| `node io`           | 平行四边形 | plum 浅底 | 输入/输出/外部接口 |
| `node db`           | 圆柱   | clay 浅底  | 数据库 |
| `node subprocess`   | 双竖线矩形 | olive 浅底 | 封装的子流程 |
| `node connector`    | 小圆圈 | paper 底 + clay 边 | 长距离跳转 |
| `node document`     | 波浪底矩形 | rust 浅底 | 生成单据 |

## 边类型

| class | 视觉 | 何时用 |
|---|---|---|
| `edge`     | gray 实线  | 默认顺序流 |
| `edge yes` | olive 实线 | 判断 YES 分支 |
| `edge no`  | rust 虚线  | 判断 NO 分支 |
| `edge db`  | clay 虚线  | 数据库读写 |

**直走 or 绕行**：整体不拥挤时，判断的 NO 分支可以直接横走到目标节点（`M550,1080 L690,1080` 直线）；空间紧时再走直角绕行。是否直走看有没有撞到其它节点。

## 坐标约定

```
viewBox 1080 × 1500
主流程轴线 x : 480（中心列）
节点矩形    : 160 × 60（模板）／200 × 60（通用）
判断菱形    : 180 × 80
起止胶囊    : 160 × 44
左侧 DB 柱 x: 250（批量写库：batch_record / trade_flow / withdraw_bill）
右侧 DB 柱 x: 890（补偿写库：wallet）
水平间距    : 节点之间 ≥ 30
垂直间距    : 行之间 ≥ 80（给边留空间）
```

边走**直角**（除直走分支）：
```
M x1,y1 L x_mid,y1 L x_mid,y2 L x2,y2
```

**事务边界**：一个事务用一束 `edge db` 连到同一张/多张表，事务内多步落库共享同一批 DB 边；事务外调外部接口用 `node io` 平行四边形。

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/01-flowchart.html \
   <output-dir>/<scenario>-flowchart.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 顶端一个 START（`node term`）
2. 主流程一系列 `node process`，关键步骤之间用 `node decision`
3. 写库步骤旁画 `node db`（列边成柱）；调外部接口用 `node io`
4. 失败路径走 `edge no` 接 `node term fail`；成功终态 `node term success`
5. 为每个新 `data-id` 添加 nodeData 项（schema 见 `shared/node-data-schema.md`）
6. 若 A 区比模板矮，同步收紧 viewBox

### Step 3 · 改外壳 + 自检
- `<title>` / `.eyebrow` / `<h1>` / `.lead` / `.stat-row`
- 主流程从 START 到至少一个 END；每个判断菱形出 YES + NO 两条边
- 自检：`bash $SKILL_DIR/shared/selftest.sh <output.html>` 8/8

## 反例

- ✗ 一个判断有 3 个出口（用嵌套判断或重新设计）
- ✗ 主流程走斜线（必须正交，除非空间允许的直走 NO 分支）
- ✗ 同时有两个 START
- ✗ 失败路径用 olive
- ✗ 边 `edge db` 横穿节点身体（DB 边也必须走空隙）

## 示例片段（参考写法）

```html
<g class="node process" data-id="validate" tabindex="0">
  <rect class="shape" x="400" y="120" width="160" height="60"/>
  <text class="t-cn" x="480" y="148" text-anchor="middle">查询待代发</text>
  <text class="t-sub" x="480" y="166" text-anchor="middle">status=1 · pcs=0 · way=2</text>
</g>

<g class="node decision" data-id="empty-decision" tabindex="0">
  <path class="shape" d="M480,240 L550,280 L480,320 L410,280 Z"/>
  <text class="t-cn" x="480" y="278" text-anchor="middle">有待代发?</text>
  <text class="t-sub" x="480" y="294" text-anchor="middle">Lists.partition 100/批</text>
</g>

<!-- 空间允许时 NO 直走（不撞节点） -->
<path class="edge no" d="M550,280 L700,280"/>
<text class="edge-label" x="625" y="274" text-anchor="middle">空</text>

<!-- DB 边：正交走空隙，不穿节点 -->
<path class="edge db" d="M400,650 L280,650 L280,585 L250,585"/>
```
