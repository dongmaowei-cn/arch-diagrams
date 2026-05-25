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
  For embedded mini-diagrams inside reports/decks, use the host agent's
  report/deck mini-diagram workflow instead.
license: MIT
---

# arch-diagrams · 复制 + 改造工作流

基于 skill 自带的 8 张高质量参考模板（**只读**），
通过 **复制 → 替换主图 → 同步 nodeData → 改外壳文字** 三步产出。
每次画图都生成一个**新文件**，禁止改 templates/ 里的源文件。

> **v2 重构**：模板已经不再内嵌 B 区元素图鉴 / panel.howto 教学内容。
> 教学拆分为 `templates/index.html`（薄导航）+ `templates/gallery/0X-*.html`（每张图一个「元素图鉴 + 画法」页，单文件内联 CSS/JS，无外链）。
> 模板本身只保留：A 区主图 + aside.panel.detail + aside.legend-group + 外壳。

## 0 · 模板源（skill 内部、只读）

```
SKILL_DIR = directory containing this SKILL.md
TEMPLATES_DIR = $SKILL_DIR/templates
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

判断不了时，用当前 agent 的提问机制给 2 个最接近的图型 + 一句话说明。**绝对不要**自己猜后给一张错的图。

### 给用户 index · 自助看模版、快速选型

用户**想画图**（尤其还没说清要哪种图）时，先把总览页给他，比口头描述 8 种图型更高效：

```
路径：$SKILL_DIR/templates/index.html
打开：用浏览器直接打开该文件（file:// 或本地静态服务均可）
```

index 上 **10 张 catalog 卡片**，每张提供两条入口：

| 链接 | 作用 |
|---|---|
| **图鉴 · 画法** → `gallery/0X-*.html` | 看这种图有哪些节点/边、六步怎么画 |
| **范本 →** → `0X-*.html` | 看完整可交互范本长什么样 |

**推荐话术**（图型未定时先发 index，再简短补一句）：

> 可以先打开 `templates/index.html` 浏览 10 种图型和范本样式；点「图鉴 · 画法」看元素说明，点「范本 →」看完整示例。选定图型后告诉我场景，我按对应模板给你出图。

- **图型未明确**：先给 index，等用户选定或从对话里推断，再进入复制改造流程。
- **图型已明确**（如「画订单结算流程图」）：可直接开干；若用户还想对比其他图型，再补发 index。
- **不要**把 index / gallery 当交付物复制进用户场景图 — 它们只是选型与教学参考。

## 2 · 工作流（3 步，全自动执行）

每张图详细改造步骤见对应 `catalog/0X-*.md`。整体框架：

### Step 1 · 复制
```bash
cp $TEMPLATES_DIR/0X-<type>.html <output-dir>/<scenario>-<type>.html
```
- `<output-dir>`：用户当前工作目录（`pwd`），除非用户指定
- `<scenario>`：从用户描述抽取的短语，kebab-case，如 `user-login` / `order-settlement`
- 文件名样例：`user-login-sequence.html`、`order-state-machine.html`

> **不需要再删 B 区**。模板已不内嵌教学图鉴。
> 如果想看元素清单和画法说明,引导用户打开 `templates/gallery/0X-<type>.html`（或从 `templates/index.html` 总览进入）。

### Step 2 · 替换 A 区主图 + 同步 nodeData
按对应 catalog 卡片的"节点种类清单"和"坐标系约定"，重写 A 区 SVG 内容。
**只动 A 区 SVG 节点和边**，不动 `<defs>`、CSS、外壳。

同时在 `<script>window.DIAGRAM_CONFIG = { ... nodeData: { ... } }` 里：
- **删掉**原模板的所有 nodeData 项
- 为每个新 `data-id` 添加对应项，schema 见 `shared/node-data-schema.md`
- **铁律**：SVG 中每个 `data-id` 必须在 nodeData 有同名 key，多一个少一个都报错

如果新 A 区比原模板的"原场景 A 区"矮 (常见),同步收紧 `<svg height>` 和 `viewBox="0 0 1080 H"` 末尾的 H,以及 `viewBox: { w: 1080, h: H }` 里的 h。

### Step 3 · 改外壳文字
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
5. **不要从 `templates/gallery/` 拷元素图鉴的卡片到模板主图** — gallery 页的图鉴是教学示例,颜色比例与主图错位,不可复用
6. **不改节点的标准尺寸** — 模板的节点宽高已经定调，**不要为了"填满 canvas"或"让画面更饱满"私自加大节点**。文字装不下就**精简文字**（缩写、分行、把详情挪到 aside `body`），不要拉宽节点。各图节点标准尺寸见对应 catalog 卡片"坐标约定"段。

## 4 · 自检清单（输出前必须过）

**首选**：跑 `shared/selftest.sh`，7 项检查一次全过：

```bash
bash $SKILL_DIR/shared/selftest.sh <output.html>
```

7 项内容：
1. **节点-数据对齐**：SVG `data-id` ↔ nodeData key 双向 1:1（支持 `[a-zA-Z0-9_-]+`）
2. **viewBox 高度一致**：`<svg height>` 与 `viewBox` 末尾数字相等
3. **B 区已删**：无 `<!-- B ·` 注释、无 SVG `gallery-card-node` 节点（v2 模板天然无 B 区,该项常态 PASS）
4. **nodeData 无 `g-` 残留**：v2 模板天然无 `g-*`,该项常态 PASS
5. **ER 教学伪节点无残留**：`pk-marker / fk-marker / crows-foot …`,v2 模板天然无,该项常态 PASS
6. **外壳文字已替换**：`<title>` 不再是模板原场景特征词。**对模板本身自动跳过**（标识为 `○` 模板态）
7. **SVG 结构对称**：`<svg>` 开闭标签数量一致

任一不通过就修复后再跑，直到全过才报告产物。

> 3/4/5 项作为防御性检查保留:防止用户从 gallery 页误粘 B 区图鉴内容进产物。

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

### 图型未定时

```
0) 给用户 templates/index.html 路径 + 浏览器打开方式（见 §1「给用户 index」）
1) 等用户选定图型，或从描述推断最接近的一种
2) 进入下方「图型已定时」流程
```

### 图型已定时

不啰嗦。用户给"图型 + 场景"后直接执行：

```
1) cp 模板 → 新文件
2) Read 新文件相关行 + 对应 catalog/0X-*.md
3) Edit 改 A 区 + 改 nodeData + 改外壳（必要时收紧 viewBox）
4) 自检
5) 报一行：✓ 已生成 <文件路径>（节点 N / 边 M）
```

只在以下情况向用户确认（**仍可先给 index 辅助选型**）：
- 用户没说图型也没描述清楚场景（"画个图"）→ **先发 index**，再问 1 句场景
- 同一场景有 2 张图都合理（如"用户登录" → 流程图 or 时序图？）→ **给 index** 让用户点两张范本对比
- 已有同名输出文件，问是否覆盖

否则**全自动**，结果直接交付。

## 8 · 何时不该用本 skill

| 场景 | 推荐方案 |
|---|---|
| 报告 / deck 里嵌一张小图 | 用 `html-kit` 的 mini-diagram 骨架,不要复用本 skill 模板 |
| 暗色 / dark-mode 架构图 | 用 `html-effectiveness/cocoon-source` 或 `architecture-diagram` skill |
| markdown 里画轻量 ASCII / mermaid | 直接写 mermaid 代码块 |
| 业务流程 + 数据流混在一起 | 拆成 2 张图:01 业务流程图 + 04 系统架构图 |
| 想画"运行时序 + 物理拓扑" | 拆成 2 张:02 时序图 + 07 微服务架构图 |

本 skill 的定位:**独立交付的工程图**(单文件 HTML,可直接发给非技术同事)。
