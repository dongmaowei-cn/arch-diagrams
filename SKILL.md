---
name: arch-diagrams
description: >
  Generate single-file engineering diagrams (架构图/流程图/时序图/状态机/泳道图/ER 图/微服务图)
  by copying one of 8 curated reference templates and rewriting only the
  in-canvas content. Trigger when the user asks for any of:
  业务流程图 · flowchart · 时序图 · sequence diagram · 状态机 · state machine ·
  系统架构图 · architecture · ER 图 · entity relationship · 泳道图 · swimlane ·
  微服务架构图 · microservices topology.
  Workflow is fully automatic once the user has named the diagram type and
  scenario — do NOT ask follow-up questions unless the request is truly
  ambiguous (e.g. "画个图" with no scenario).
  For embedded mini-diagrams inside reports/decks, use html-kit instead.
license: MIT
---

# arch-diagrams · 复制 + 改造工作流

基于 skill 自带的 8 张高质量参考模板（**只读**），
通过 **复制 → 替换主图 → 同步 nodeData → 删 B 区元素图鉴 → 改外壳文字** 五步产出。
每次画图都生成一个**新文件**，禁止改 templates/ 里的源文件。

## 0 · 模板源（skill 内部、只读）

```
TEMPLATES_DIR = ~/.claude/skills/arch-diagrams/templates
```

所有 8 张模板文件在此目录下（skill 自包含，无外部依赖）。

## 1 · 选型矩阵（先判断图型）

| 用户在讲… | 图型 | 模板文件 |
|---|---|---|
| 一个流程从触发到终态、有判断分支 | **业务流程图** | `01-flowchart.html` |
| 多个角色之间按时间先后调用 | **时序图** | `02-sequence.html` |
| 单个对象在不同状态间转移 | **状态机** | `03-state-machine.html` |
| 系统物理拓扑、分层、技术栈 | **系统架构图** | `04-system-architecture.html` |
| 数据模型、实体关系、表结构 | **ER 图** | `05-er-diagram.html` |
| 跨部门/角色协作（横向时间轴） | **泳道图 · 水平** | `06-swimlane.html` |
| 跨阶段流程（纵向时间轴） | **泳道图 · 垂直** | `06-swimlane-vertical.html` |
| 微服务运行时拓扑、K8s ns、sidecar | **微服务架构图** | `07-microservice.html` |

判断不了时，AskUserQuestion 给 2 个最接近的图型 + 一句话说明。**绝对不要**自己猜后给一张错的图。

## 2 · 工作流（5 步，全自动执行）

每张图详细改造步骤见对应 `catalog/0X-*.md`。整体框架：

### Step 1 · 复制
```bash
cp $TEMPLATES_DIR/0X-<type>.html <output-dir>/<scenario>-<type>.html
```
- `<output-dir>`：用户当前工作目录（`pwd`），除非用户指定
- `<scenario>`：从用户描述抽取的短语，kebab-case，如 `user-login` / `order-settlement`
- 文件名样例：`user-login-sequence.html`、`order-state-machine.html`

### Step 2 · 删除 B 区元素图鉴
用户不需要教学语法。删除以下范围（**整段连同注释**）：

| 文件 | 删除行号范围 | 同时调整 |
|---|---|---|
| 01-flowchart.html | 无 B 区 | — |
| 02-sequence.html | 609–846 | `<svg height>` 由 2680 改为 A 区实际高度 |
| 03-state-machine.html | 693–988 | 同上：2660 → A 区高度 |
| 04-system-architecture.html | 890–1145 | 2680 → A 区高度 |
| 05-er-diagram.html | 611–909 | 2680 → A 区高度 |
| 06-swimlane.html | 806–1163 | 2660 → A 区高度 |
| 06-swimlane-vertical.html | 696–934 | 2680 → A 区高度 |
| 07-microservice.html | 931–1249 | 2660 → A 区高度 |

> "A 区实际高度" 在每张 catalog 卡片里给出推荐值。

### Step 2.5 · 同步清理 nodeData 中的 B 区伪节点

删完 B 区 SVG **必须**同步清理 `window.DIAGRAM_CONFIG.nodeData`（或顶层 `NODE_DATA`）：

- 02 / 03 / 04 / 06H / 06V / 07：删掉所有以 `g-` 开头的 key
  （如 `'g-tier-bands'` `'g-edge-types'` `'g-lifeline'` `'g-history'` …）
- 05 ER：删掉这 7 个 key —
  `'pk-marker'` `'fk-marker'` `'crows-foot'` `'one-to-many'`
  `'many-to-many'` `'self-ref'` `'field-markers'`

**自检命令**（清理完跑一遍，应该没有输出）：
```bash
/usr/bin/grep -nE "'g-[a-z-]+':|'pk-marker'|'fk-marker'|'crows-foot'|'one-to-many'|'many-to-many'|'self-ref'|'field-markers'" <output.html>
```

### Step 3 · 替换 A 区主图
按对应 catalog 卡片的"节点种类清单"和"坐标系约定"，重写 A 区 SVG 内容。
**只动 A 区 SVG 节点和边**，不动 `<defs>`、CSS、外壳。

### Step 4 · 同步 nodeData
在 `<script>window.DIAGRAM_CONFIG = { ... nodeData: { ... } }` 里：
- **删掉**原模板的所有 nodeData 项
- 为每个新 `data-id` 添加对应项，schema 见 `shared/node-data-schema.md`
- **铁律**：SVG 中每个 `data-id` 必须在 nodeData 有同名 key，多一个少一个都报错

### Step 5 · 改外壳文字
| 位置 | 改什么 |
|---|---|
| `<title>` | 场景名 |
| `.eyebrow` | 一行短语标签（如 "Diagram 04 · 用户登录主路径"） |
| `<h1>` | 场景标题 + `<em>` 英文副标 |
| `.lead` | 1-2 句描述：业务背景 + 看图重点 |
| `.stat-row` | 3 个关键数字（节点数 / 层数 / QPS 等） |
| `.footer-note` | 版本信息（保留"返回总览"链接可选删） |

## 3 · 改造红线（绝对不能碰）

1. **不改 CSS tokens / `.node.*` / `.edge.*` / marker `<defs>`** — 视觉系统已调好
2. **不改 viewBox 宽度** — 永远是 1080
3. **不改 chrome**（topbar / aside / canvas-controls / theme toggle / export buttons）
4. **不改 `<script>` 末尾的渲染逻辑**（只改 `nodeData` 内容）
5. **不复制元素图鉴中的卡片**到主图（B 区是教学示例，颜色比例错位）
6. **不改节点的标准尺寸** — 模板的节点宽高已经定调，**不要为了"填满 canvas"或"让画面更饱满"私自加大节点**。文字装不下就**精简文字**（缩写、分行、把详情挪到 aside `body`），不要拉宽节点。各图节点标准尺寸见对应 catalog 卡片"坐标约定"段。

## 4 · 自检清单（输出前必须过）

**首选**：跑 `shared/selftest.sh`，7 项检查一次全过：

```bash
bash ~/.claude/skills/arch-diagrams/shared/selftest.sh <output.html>
```

7 项内容：
1. **节点-数据对齐**：SVG `data-id` ↔ nodeData key 双向 1:1
2. **viewBox 高度一致**：`<svg height>` 与 `viewBox` 末尾数字相等
3. **B 区已删**：无 `<!-- B ·` 注释、无 SVG `gallery-card-node` 节点
4. **nodeData 无 `g-` 残留**：删 B 区后 nodeData 同步清理
5. **ER 教学伪节点无残留**：`pk-marker / fk-marker / crows-foot …` 已清
6. **外壳文字已替换**：`<title>` 不再是模板原场景特征词
7. **SVG 结构对称**：`<svg>` 开闭标签数量一致

任一不通过就修复后再跑，直到全过才报告产物。

## 5 · 共享词汇表

- `shared/node-data-schema.md` — aside 详情面板的 JSON 协议
- `shared/edge-types.md` — 8 种边 + 9 个 markers 的语义清单
- `shared/color-semantics.md` — 颜色语义（clay 动作 / olive 成功 / rust 失败 …）
- `shared/coordinate-system.md` — viewBox / 节点尺寸 / 间距 通用约定

## 6 · 每图卡片（读对应一张就能改）

- `catalog/INDEX.md` — 8 图选型矩阵 + 模板路径 + A 区行号速查
- `catalog/01-flowchart.md`
- `catalog/02-sequence.md`
- `catalog/03-state-machine.md`
- `catalog/04-system-architecture.md`
- `catalog/05-er-diagram.md`
- `catalog/06-swimlane.md`
- `catalog/06-swimlane-vertical.md`
- `catalog/07-microservice.md`

## 7 · 触发后的最小响应

不啰嗦。用户给"图型 + 场景"后直接执行：

```
1) cp 模板 → 新文件
2) Read 新文件相关行
3) Edit 删 B 区、改 A 区、改 nodeData、改外壳
4) 自检
5) 报一行：✓ 已生成 <文件路径>（节点 N / 边 M）
```

只在以下情况 AskUserQuestion：
- 用户没说图型也没描述清楚场景（"画个图"）
- 同一场景有 2 张图都合理（如"用户登录" → 流程图 or 时序图？）
- 已有同名输出文件，问是否覆盖

否则**全自动**，结果直接交付。
