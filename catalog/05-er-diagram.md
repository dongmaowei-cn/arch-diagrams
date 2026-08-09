# 05 · ER 图 / Entity-Relationship

## 用在哪里
讲**数据模型**：表/实体、主外键、表之间关系（1:1 / 1:N）。
强调**结构 + 基数**（crow's foot 标记）。

## 模板信息

- **模板文件**：`05-er-diagram.html`
- **viewBox**：`1080 × 700`
- **关键行号**
  - SVG 开始：400
  - A 区主图：420–604（`</svg>`：604）
  - 6 张表节点：479–586
  - `window.DIAGRAM_CONFIG`：671
- **exportName**：`xft-withdraw-payroll-er`（复制后改成你的场景 slug）

## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/05-er-diagram.html`](../templates/gallery/05-er-diagram.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 实体表格结构

A 区主图包在 `<g transform="translate(60 140)">`，内部是 **960×560** 子坐标系
（最底表 `detail_result` 底部 y=534，绝对底 = 140 + 534 = 674）。

**推荐 3×2 网格**（6 张表以内）：3 列 `x = 20 / 370 / 720`，2 行 `y = 30 / 330`。

| 参数 | 值 |
|---|---|
| 表宽 | 220（右列独立表可收窄到 200） |
| 表高 | 204（= 表头 ~30 + 8 行 × 22px） |
| 行距 | 22px；`row-zebra` 隔行浅底 |
| 列间走廊 | x 间隙 ~130（关系线竖穿处） |
| 行间走廊 | y 间隙 ~96（关系线横穿处） |

每张表是一组 `g.node`：
```
┌─────────────────────┐
│ withdraw_bill       │  ← table-header + table-title
├─────────────────────┤
│ bill_id     bigint PK│ ← cell pk + tag-pk + typ
│ withdraw_way tinyint │
│ payroll_credit_status│
│ arrival_amount decimal│
└─────────────────────┘
```

关键 class：
- `.table-frame` / `.table-header` / `.table-title`：表格容器
- `.row-zebra` / `.row-divider`：隔行浅底 / 分隔线
- `.cell` / `.cell pk` / `.cell fk`：字段名（PK 加粗、FK 斜体）
- `.tag-pk` / `.tag-fk` / `.tag-uq` / `.tag-idx` / `.tag-nn`：字段标记
- `.typ`：类型（右对齐 mono）
- `.er-edge`：关系线（正交）
- `.crowfoot`：crow's foot 标记（双短横 / 三叉）
- `.edge-label-bg` / `.edge-label`：关系标签（写「FK 列 · 基数」，如 `bill_id · 1—*`）

## 关系基数（crow's foot）

| 标记 | 意义 |
|---|---|
| 两条短横（=）        | 必有一个（1） |
| 三叉（>）            | 多个（many） |
| 短横 + 三叉          | 1 端 + 多端 |
| 圆圈                | 0..1 可选 |
| 实线                | identifying（子依赖父） |
| 虚线                | non-identifying（弱关系 / 自引用） |

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/05-er-diagram.html \
   <output-dir>/<scenario>-er-diagram.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 删 `<g transform>` 内部所有原表与关系
2. 按实体数量布局（≤6 张用 **3×2 网格**，更多再扩行/列，同步调 viewBox h）
3. 每张表 6–10 行；主键挂 `cell pk`+`tag-pk`，外键挂 `cell fk`+`tag-fk`，唯一键挂 `tag-uq`
4. 画关系线 + crow's foot，**遵守连线纪律**（edge-check 会拦，见下）
5. 每张表 nodeData 一项，`tagClass: 't-entity'`，body 写完整字段 / 索引 / 幂等键
6. 若 A 区比模板矮，同步收紧 `viewBox` h（默认 700；含 translate(60 140) 时绝对底 = 140 + 内部底）

**关系线纪律**（`shared/edge-check.py` [1–4][8] 自动拦截）：
- 端点落在表边界**中点**，绝不离角部
- 一条边的入箭头与另一条边的出线**不共用同一连接点**（请求/回执碰撞）
- 关系线**正交绕行，走表间走廊**，不斜穿/横穿任何表体（[8] 专门查 er-edge 穿表）
- 1 端双短横 / N 端三叉标在表边界上，不要悬空

**独立表**（如账务中枢 `wallet`）：不画 FK 字段、不连任何关系线、在 section-sub / nodeData 里注明「独立表 · 无外键」。

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row` / `exportName`（导出名改成场景 slug）
- 自检：`bash $SKILL_DIR/shared/selftest.sh <output.html>` —— 8 项含 node-data 对齐 + 边几何

## 反例

- ✗ 表格内字段超过 ~10 行（拆实体，或收窄列宽）
- ✗ 关系线斜穿/横穿表体 —— 必须正交走表间走廊（edge-check [8] 会拦）
- ✗ 端点从表角部出发 / 箭头悬空 / 请求回执共用连接点（edge-check [1–4] 会拦）
- ✗ 没标 crow's foot 直接画线（看不出基数）

## 示例片段

```html
<!-- 实体表格 -->
<g class="node" data-id="withdraw_bill" tabindex="0">
  <rect class="table-frame" x="20" y="30" width="220" height="204"/>
  <path class="table-header" d="M 20 40 a10 10 0 0 1 10 -10 H 230 a10 10 0 0 1 10 10 V 58 H 20 Z"/>
  <text class="table-title" x="130" y="49" text-anchor="middle">withdraw_bill</text>
  <line class="row-divider" x1="20" y1="58" x2="240" y2="58"/>
  <rect class="row-zebra" x="20" y="58" width="220" height="22"/>
  <text class="cell pk" x="32" y="73">bill_id</text><text class="tag-pk" x="86" y="73">PK</text>
  <text class="typ" x="228" y="73" text-anchor="end">bigint</text>
  <text class="cell" x="32" y="95">arrival_amount</text>
  <text class="typ" x="228" y="95" text-anchor="end">decimal</text>
</g>

<!-- 关系线 + crow's foot（withdraw_bill 1 —* wallet_flow） -->
<path class="er-edge" d="M 130 234 V 330"/>
<!-- 1 端：两条短横 -->
<line class="crowfoot" x1="122" y1="240" x2="138" y2="240"/>
<line class="crowfoot" x1="122" y1="244" x2="138" y2="244"/>
<!-- N 端：三叉 -->
<line class="crowfoot" x1="122" y1="322" x2="130" y2="330"/>
<line class="crowfoot" x1="130" y1="322" x2="130" y2="330"/>
<line class="crowfoot" x1="138" y1="322" x2="130" y2="330"/>

<!-- 关系标签 -->
<g><rect class="edge-label-bg" x="90" y="274" width="80" height="16"/>
   <text class="edge-label" x="130" y="286" text-anchor="middle">bill_id · 1—*</text></g>
```

## 字段标记速查

| class | 视觉 | 用途 |
|---|---|---|
| `cell pk` / `tag-pk` | gold #C4994E · 加粗 | 主键 |
| `cell fk` / `tag-fk` | plum #6B5B95 · 斜体 | 外键 |
| `tag-uq`            | olive #788C5D | UNIQUE 唯一 |
| `tag-idx`           | teal #4A8585  | 索引 |
| `tag-nn`            | clay #D97757  | NOT NULL |
| `typ`               | gray-500 mono 右对齐 | 类型 |
| `row-zebra`         | gray-150 浅底 | 隔行底色 |
| `row-divider`       | gray-300 横线 | 行分隔 |

> `[ex]` 是本图谱自定义约定（独立表/扩展语义），非 IE 标准，用在图例里标注即可。
