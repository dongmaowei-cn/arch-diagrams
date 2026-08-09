# Changelog · 2026-08 审计与修复

对 arch-diagrams skill 做的一次系统性审计（读完 SKILL.md / 全部 8 张 catalog 卡片 / 全部 shared 文档 / 8 个模板 / 8 个 gallery 页 / 示例文件，并实际跑 `selftest.sh` + `edge-check.py` 逐一验证，而不是只读文档），目标：让能力更弱的模型也能稳定按 skill 产出高质量图，并新增 PlantUML 输入支持。所有改动均已通过完整回归（8 模板 7/7 + 示例文件 8/8，`shared/selftest.sh` 全绿）。

## 产物级真实 bug（不只是文档描述有误）

- **`examples/online-order-flowchart.example.html`**：修复一条悬空边——"自动取消子流程"节点下沿在 y=780，引出边却从 y=790 起笔，差 10px。此文件是 `examples/dry-run.md` 引用的"真实参照"，此前**没有通过自己的 selftest**。
- **`templates/06-swimlane.html`**：
  - 补上文档一直声称存在、但 CSS 从未定义的 `.seq-flow.yes` / `.seq-flow.no` 分支边样式（此前水平泳道图完全没法给网关分支上色）。
  - 修复模板自带示例里一条"复核不通过"边：用 `stroke=`/`marker-end=` 属性硬覆盖颜色，但被 `.seq-flow` 的 CSS class 规则（更高优先级）打败，实际渲染成灰色而非预期的 rust 色；改成正确的 `class="seq-flow no"` 写法。
  - 同步修了 `templates/gallery/06-swimlane.html` 的镜像内容。
  - 清理了两条从未生效过的死 CSS（`.seq-flow.default-flow` / `.seq-flow.cond`，和 base class 完全同值）。

## 文档漂移（catalog 行号 / viewBox 与实际文件不符 —— 本次审计发现的最大一类问题）

v1→v2 重构（把 B 区元素图鉴从模板正文拆到独立 gallery 页）时，`04-system-architecture.md` / `06-swimlane.md` / `07-microservice.md` 三张卡片的行号引用没有跟着更新，出现几百行的偏差：

| 文件 | 字段 | 旧值（错） | 新值（对） |
|---|---|---|---|
| `catalog/04-system-architecture.md` | `</svg>` | 1146 | 891 |
| | `DIAGRAM_CONFIG` | 1247 | 978 |
| `catalog/06-swimlane.md` | viewBox | 1080×1300 | 1080×1000 |
| | `</svg>` | 1164 | 596 |
| | `DIAGRAM_CONFIG` | 1255 | 656 |
| `catalog/06-swimlane-vertical.md` | viewBox（INDEX.md 里的，卡片本身是对的） | 1080×1500 | 1080×1540 |
| `catalog/07-microservice.md` | `</svg>` | 1250 | 936 |
| | `DIAGRAM_CONFIG` | 1339 | 1010 |
| `catalog/INDEX.md` | 总表 04/06H/06V/07 四行 | 同上 | 同上 |

`catalog/INDEX.md` 总表下新增了一条**现场核实**提示（`grep -n '<svg class=\|DIAGRAM_CONFIG\|NODE_DATA\|</svg>'`），因为这类偏差已经真实发生过三次——文档只做粗定位，模板还会继续迭代，光改一次数字治标不治本。

## 会导致边/节点静默不显示预期样式的 class 名错误

这类问题最隐蔽：class 名字看着合理，SVG 不报错，但因为没有匹配的 CSS 规则，边/节点直接不显色，肉眼和自动化自检都不一定能立刻发现：

- **`catalog/06-swimlane-vertical.md`**：文档写的边 class 是 `seq-flow` 系列，但该模板实际用的是 `vflow` 系列——两个泳道模板边基类名不一样，照抄会导致边不着色。同时修正了不存在的 `vflow yes` 变体声称、`gateway`/`event-end` 等节点 class 的精确写法（06V 和 06H 看着像，内部实现细节不少地方不同）。
- **`catalog/06-swimlane.md`**：`event-end` → `event-end-bpmn`（两处，含底部"任务类型速查"表）；`gateway shape`/`event shape` 等描述改成精确 class 名 `gateway-shape shape`/`event-start shape`。
- **`catalog/INDEX.md`**："边 class 清单"和"节点 class 清单"里 06H/06V 两行原来写的是通用的 `edge`，实际两个模板的边基类分别是 `seq-flow`（06H）和 `vflow`（06V），三者互不相同，已订正。
- **`catalog/02-sequence.md`** / **`shared/edge-types.md`**：`edge sync` 的 marker id 在不同模板里不一样——02/04/07 用 `arrow-sync`，03/05/06H/06V 用 `arrow-slate`，文档之前统一写成 `arrow-slate` 是错的（02-sequence.md 已修正）。`edge-types.md` 补充了完整的对照表和"marker id 不是全模板通用，用前先 grep 目标模板 `<defs>`"的操作提示。

## 与当前 v2 架构矛盾的过期内容

- `shared/coordinate-system.md`：删掉整段"删 B 区后调整 SVG 高度"（v2 模板没有 B 区可删，这段和 SKILL.md 主流程直接矛盾；里面的高度数值也和当前任何模板都对不上），换成准确的"内容变多变少时怎么调整高度"指引。
- `shared/node-data-schema.md`：清理同类过期注释。
- `examples/dry-run.md`："7 项检查"改成"8 项"（第 8 项 edge-check 是后加的）。

## 其它订正

- `shared/design-system.md`：两个颜色 hex（danger `#B04A4A`、warning `#C78E3F`）在全部 8 个模板里出现次数为 0，已改成实际使用的 `#B04A3F`/`#C4994E`（和 `color-semantics.md` 一致）。
- `catalog/04-system-architecture.md`：标题重复文字"（3 步）（5 步）"、Step 2 编号重复、Step 1 里写死的 `~/.claude/skills/...` 路径（改回 `$SKILL_DIR`，这个路径在很多运行环境里根本不存在）。
- `catalog/02-sequence.md`：同样的 Step 2 编号重复问题。
- `catalog/05-er-diagram.md`："purple" 统一成和其它文档一致的 "plum"。

## 新增：PlantUML 输入支持

原来整个 skill 里没有任何 PlantUML 相关内容（全文搜索零匹配），但实际使用场景的输入常常是 PlantUML 源码。新增：

- **`shared/plantuml-mapping.md`**：图型判定表（PlantUML 语法特征 → 8 种图型之一）+ 每种图型的详细元素映射表（participant/actor/entity/state/`\|Lane\|`/`\|\|--o{` 等语法元素 → 本 skill 的 node/edge class），含一个完整的转换实例。写之前专门核实过几个容易搞反的细节（比如 PlantUML 的 `\|Lane\|` swimlane 原生渲染是**纵向**的，对应本 skill 的 06V 而非 06H；`-->` 在时序图里到底是"返回"还是"异步"要看上下文，不能只看虚线本身）。
- `SKILL.md`：frontmatter description 里加了 PlantUML 触发信号；§1 选型矩阵加了 PlantUML 判型的入口说明；§5 共享词汇表加了新文档的引用。
- `catalog/INDEX.md`：选型矩阵加了第 4 列"PlantUML 特征"，同一张表可以同时服务口头描述和 PlantUML 源码两种输入。

## 结构性清理

- `shared/rebuild-index-galleries.py`、`shared/split-index-galleries.py`（v1→v2 迁移时用过一次的一次性脚本，不在 SKILL.md 引用的工作流里，再次运行大概率报错）移到新建的 `archive/` 目录，附 README 说明；避免和 `selftest.sh`/`edge-check.py` 这些真正的常规工具混在一起。
- `shared/selftest.sh`：硬编码的 `/usr/bin/grep` 改成优先取 PATH 里的 `grep`、找不到才兜底用绝对路径，避免在没有该确切路径的沙盒/容器环境里整个脚本直接报错退出。

## 验证方法

每一处修改后都重新跑过 `bash shared/selftest.sh <file>`；全部 8 个模板（模板态 7/7）+ 示例文件（产物态 8/8）在最终交付前做了一次完整回归，全绿。另外写了几轮一次性 Python 脚本，把 catalog 文档里所有反引号标注的 class 名、marker id、viewBox 数值分别和对应模板的真实 CSS/SVG 内容做了逐条自动交叉核对（而非只抽查），本清单里的 class/marker 类问题都是这样系统性找出来的。
