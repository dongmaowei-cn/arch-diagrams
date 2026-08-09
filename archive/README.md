# archive/ · 历史迁移脚本，不属于运行时流程

这两个脚本是 v1 → v2 重构（把 B 区元素图鉴从模板正文拆到独立的 `templates/gallery/0X-*.html`）时用过**一次**的一次性迁移工具：

- `split-index-galleries.py` — 把旧的单体 `templates/index.html` 拆成"薄导航页 + 独立 gallery 页"
- `rebuild-index-galleries.py` — 需要一份重构前的模板备份目录才能跑，用于从旧模板重建 gallery 页

迁移已经完成，仓库现在的 `templates/` 和 `templates/gallery/` 就是迁移后的最终形态。这两个脚本：

- **不在** `SKILL.md` 引用的工作流里，正常画图不会用到
- 再次运行大概率会报错或产生错误结果（`rebuild-index-galleries.py` 依赖的备份目录本来就不存在于交付物里；`split-index-galleries.py` 依赖的旧版 `index.html` 结构现在的文件里也没有了）

留档只是为了保留历史记录，不要在正常任务流程中调用。如果需要参考"当初是怎么拆的"，看脚本本身的 docstring。
