# 01 · 业务流程图 / Flowchart

## 用在哪里
讲**一个流程**从触发到终态：有判断分支、有 YES/NO、可能写库或调外部。
单一主体视角（不区分谁做的），强调**做什么 → 接下来做什么**。

> 涉及多角色协作 → 用 [06 泳道图](./06-swimlane.md)
> 涉及对象状态变化 → 用 [03 状态机](./03-state-machine.md)

## 模板信息

- **模板文件**：`01-flowchart.html`
- **viewBox**：`1080 × 1500`（**这张图无 B 区，不用改 height**）
- **关键行号**
  - SVG 开始：285
  - A 区：294-440
  - `</svg>`：440
  - `window.DIAGRAM_CONFIG`：搜索定位（在最末 script 块）

## 这张图的特殊性

**01 是唯一没有 B 区元素图鉴的模板**。aside 用 `.legend-group` HTML 区域显示节点形状图例。

→ 因此**跳过"删 B 区"步骤**，直接改 A 区即可。

## 节点类型（class）

| class | 形状 | 视觉 | 何时用 |
|---|---|---|---|
| `node term`         | 胶囊矩形 (rx=17) | gray-150 底 | START 起始事件 |
| `node term success` | 胶囊矩形 | olive 浅底 | 成功终态（如 SETTLED） |
| `node term fail`    | 胶囊矩形 | rust 浅底  | 失败终态（如 DECLINED） |
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

## 坐标约定

```
viewBox 1080 × 1500
节点矩形    : 200 × 60
判断菱形    : 180 × 80
起止胶囊    : 180 × 50
水平间距    : 节点之间 ≥ 30
垂直间距    : 行之间 ≥ 80（给边留空间）
中心线 x   : 540（主流程通常居中）
```

边走**直角**：
```
M x1,y1 L x_mid,y1 L x_mid,y2 L x2,y2
```

## 改造步骤（5 步）

### Step 1 · 复制
```bash
cp ~/.claude/skills/arch-diagrams/templates/01-flowchart.html \
   <output-dir>/<scenario>-flowchart.html
```

### Step 2 · 改 A 区主图（行 294-439）
读原 A 区 → 删除所有原节点和边 → 按用户场景画新节点：

1. 顶端一个 START（`node term`）
2. 主流程一系列 `node process`，关键步骤之间用 `node decision`
3. 写库的步骤旁边画 `node db`，连 `edge db`
4. 调外部接口用 `node io`
5. 失败路径走 `edge no` 接 `node term fail`
6. 成功终态 `node term success`

### Step 3 · 同步 nodeData
找到 `window.DIAGRAM_CONFIG = { nodeData: { ... } }`：
- 删除原 nodeData 所有项
- 为每个新 `data-id` 添加项（schema 见 `shared/node-data-schema.md`）

### Step 4 · 改外壳文字
- `<title>`：`<场景> · 业务流程图`
- `.eyebrow`：`Diagram 01 · 业务流程图`
- `<h1>` + `<h1><em>`：场景中文 + 英文副标
- `.lead`：1-2 句业务背景
- `.stat-row` (如有)：节点数 / 判断数 / 分支数

### Step 5 · 自检
- [ ] 主流程从 START 走到至少一个 END
- [ ] 每个判断菱形出两条边（YES + NO）
- [ ] 所有 data-id 在 nodeData 有对应项

## 反例

- ✗ 一个判断有 3 个出口（用嵌套判断或重新设计）
- ✗ 主流程走斜线（必须正交）
- ✗ 同时有两个 START
- ✗ 失败路径用 olive

## 示例片段（参考写法）

```html
<g class="node process" data-id="validate" tabindex="0">
  <rect class="shape" x="440" y="180" width="200" height="60"/>
  <text class="t-cn" x="540" y="208" text-anchor="middle">校验金额</text>
  <text class="t-sub" x="540" y="226" text-anchor="middle">~12ms · FOR UPDATE</text>
</g>

<path class="edge" d="M540,240 L540,290" marker-end="url(#arrow)"/>

<g class="node decision" data-id="kyc-check" tabindex="0">
  <path class="shape" d="M540,290 L630,330 L540,370 L450,330 Z"/>
  <text class="t-cn" x="540" y="328" text-anchor="middle">KYC?</text>
  <text class="t-sub" x="540" y="344" text-anchor="middle">等级 L2</text>
</g>

<path class="edge yes" d="M630,330 L760,330" marker-end="url(#arrow-olive)"/>
<text class="edge-label" x="695" y="324" text-anchor="middle">PASS</text>

<path class="edge no" d="M450,330 L300,330 L300,460" marker-end="url(#arrow-rust)"/>
<text class="edge-label" x="375" y="324" text-anchor="middle">FAIL</text>
```
