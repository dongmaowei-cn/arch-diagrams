# 05 · ER 图 / Entity-Relationship

## 用在哪里
讲**数据模型**：表/实体、主外键、表之间关系（1:1 / 1:N / N:N）。
强调**结构 + 基数**（crow's foot 标记）。

## 模板信息

- **模板文件**：`05-er-diagram.html`
- **viewBox**：`1080 × 2680`（删 B 区后改为 **1080 × 800**）
- **关键行号**
  - SVG 开始：400
  - A 区主图：417–610
  - **B 区元素图鉴：611–909（删除）**
  - `</svg>`：910
  - `window.DIAGRAM_CONFIG`：993

## 删除 B 区步骤

1. Edit 删除 611–909 整段
2. 改 svg height/viewBox 高度为 800
3. 改 nodeData 顶部 `viewBox: { w: 1080, h: 800 }`

## 实体表格结构

A 区主图被包在 `<g transform="translate(60 140)">` 里，内部坐标是 960×700 的子坐标系。

每个实体是一张"表格"：
```
┌─────────────────────────┐
│ users                   │  ← 表名 header
├─────────────────────────┤
│ id            int PK    │
│ name          varchar   │
│ email         varchar UQ│
│ created_at    timestamp │
└─────────────────────────┘
```

关键 class：
- `.er-table` / `.er-table-header`：表格容器
- `.er-row` / `.er-row-key`：单行/主键行
- `.er-col-name` / `.er-col-type` / `.er-col-flag`：列名/类型/PK/FK 标记
- `.er-edge`：关系线
- `.crowfoot`：crow's foot 三叉线
- `.endpoint-circle`：0..1 端点圆

## 关系基数（crow's foot）

| 标记 | 意义 |
|---|---|
| 两条短横（=）        | 必有一个（1） |
| 三叉（>）            | 多个（many） |
| 短横 + 三叉          | 1 端 + 多端 |
| 圆圈                | 0..1 可选 |
| 两条短横在远端       | 强制 1 |

## 改造步骤

1. **复制**：`cp ~/.claude/skills/arch-diagrams/templates/05-er-diagram.html <场景>-er-diagram.html`
2. **删 B 区**：611-909；svg height = 800
3. **改 A 区**：
   - 删 `<g transform>` 内部所有原表格和关系
   - 按用户实体数量在 960×700 内布局（推荐 3×3 网格，单表 200×180）
   - 每张表 6-8 行；主键挂 PK，外键挂 FK
   - 画关系线 + crow's foot
4. **同步 nodeData**：每张表一项，`tagClass: 't-entity'`，body 详细字段表
5. **改外壳**

## 反例

- ✗ 表格内字段超过 12 行（拆分实体）
- ✗ 关系线斜穿表格（必须正交绕行）
- ✗ 没标 crow's foot 直接画线（看不出基数）

## 示例片段

```html
<!-- 实体表格 -->
<g class="node" data-id="users" tabindex="0">
  <rect class="table-frame" x="20" y="70" width="200" height="120"/>
  <path class="table-header" d="M 20 80 a10 10 0 0 1 10 -10 H 210 a10 10 0 0 1 10 10 V 98 H 20 Z"/>
  <text class="table-title" x="120" y="89" text-anchor="middle">users</text>
  <line class="row-divider" x1="20" y1="98" x2="220" y2="98"/>

  <rect class="row-zebra" x="20" y="98" width="200" height="22"/>
  <text class="cell pk"  x="32" y="113">id</text>
  <text class="tag-pk"   x="52" y="113">PK</text>
  <text class="typ" x="208" y="113" text-anchor="end">bigint</text>

  <text class="cell" x="32" y="135">email</text>
  <text class="tag-uq" x="62" y="135">UQ</text>
  <text class="typ" x="208" y="135" text-anchor="end">citext</text>

  <text class="cell fk" x="32" y="157">role_id</text>
  <text class="tag-fk" x="68" y="157">FK</text>
  <text class="typ" x="208" y="157" text-anchor="end">bigint</text>
</g>

<!-- 关系线 + crow's foot（1 — *） -->
<path class="er-edge" d="M 120 190 V 270"/>
<!-- 1 端：两条短横 -->
<line class="crowfoot" x1="110" y1="194" x2="130" y2="194"/>
<line class="crowfoot" x1="110" y1="198" x2="130" y2="198"/>
<!-- N 端：三叉 -->
<line class="crowfoot" x1="112" y1="262" x2="120" y2="270"/>
<line class="crowfoot" x1="120" y1="262" x2="120" y2="270"/>
<line class="crowfoot" x1="128" y1="262" x2="120" y2="270"/>

<!-- 关系标签 -->
<g><rect class="edge-label-bg" x="84" y="221" width="72" height="16"/>
   <text class="edge-label" x="120" y="233" text-anchor="middle">places · 1—*</text></g>
```

## 字段标记速查

| class | 视觉 | 用途 |
|---|---|---|
| `cell pk`     | clay 色 | 主键字段 |
| `cell fk`     | gray 色 | 外键字段 |
| `cell`        | slate 色 | 普通字段 |
| `tag-pk`      | clay 标签 | PK 角标 |
| `tag-fk`      | gray 标签 | FK 角标 |
| `tag-uq`      | olive 标签 | UNIQUE 角标 |
| `typ`         | gray-500 mono | 类型（右对齐） |
| `row-zebra`   | gray-150 浅底 | 隔行底色 |
| `row-divider` | gray-300 横线 | 行分隔 |
