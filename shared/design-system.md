# Design System · A 区视觉基线

> 采纳自 `html-effectiveness/05-design-system.html`。所有模板的 A 区节点边框、线条颜色、圆角按此基线统一。
> 配套：`color-semantics.md`（语义色）、`coordinate-system.md`（尺寸）。

## 边框（Borders）

| 元素 | 规范 | 说明 |
|---|---|---|
| 节点边框 | `1.5px solid var(--gray-300)` | 中性节点统一浅灰细边，不再用 gray-500 |
| 容器边框（tier/lane/namespace/phase） | `1.5px solid var(--gray-300)` | 12px 圆角 |
| 强调边框（主路径核心/聚焦） | `var(--clay)` #D97757 | 可加 `0 0 0 3px rgba(217,119,87,0.15)` 光晕 |
| 次级分隔线 | `1px solid var(--gray-100)` #F0EEE6 | 行内分隔 |

## 圆角（Radius）

| token | 值 | 用途 |
|---|---|---|
| `--r-sm` | 8px | 普通节点 |
| `--r-md` | 12px | 容器 / 面板 / tier-band |
| `--r-lg` | 20px | 胶囊起止 / 终态 |

## 线条（Lines）

| 用途 | 颜色 |
|---|---|
| 默认边 / 箭头 | `gray-500` #87867F（1.5px）|
| 主路径 / 成功 | `olive` #788C5D |
| 失败 / 拒绝 | `danger` #B04A4A |
| 消息 / 异步 | `plum` #6B5B95（本图谱扩展）|

## 颜色 token（与 design system 对齐）

| 语义 | 值 | 备注 |
|---|---|---|
| ivory（画布底）| `#FAF9F5` | 一致 |
| paper / white（卡底）| `#FFFFFF` | 一致 |
| slate（文字）| `#141413` | 一致 |
| clay（主色/强调）| `#D97757` | 一致 |
| oat（暖灰底）| `#E3DACC` | 一致 |
| gray-100（终端填充）| `#F0EEE6` | 原 gray-150 |
| gray-300（节点边框）| `#D1CFC5` | **节点边框用此** |
| gray-500（线条）| `#87867F` | 边线 |
| gray-700（次级文字）| `#3D3D3A` | 一致 |
| success（成功）| `#788C5D` | = olive |
| danger（失败）| `#B04A4A` | ≈ 原 rust #B04A3F |
| warning（警告）| `#C78E3F` | ≈ 原 gold #C4994E |

## 语义扩展（design system 之外，本图谱保留）

design system 只有 4 个语义色（success/warning/danger/info），本图谱的图形语义需要更多，保留以下扩展：

| 语义 | 值 | 用途 |
|---|---|---|
| plum | `#6B5B95` | 异步 / 消息 / 外部 / BFF |
| teal | `#4A8585` | 横切设施 / 监控 / 链路 |
| gold | `#C4994E` | 网关 / CDN / 边缘接入 / 注释 |

> 若需完全对齐 design system 的 `info` #5C7CA3（蓝）替代 plum，是全局语义变更，另行决定。
