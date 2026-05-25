# 坐标系约定 · 所有图共用

## 全局尺寸

```
SVG viewBox 宽度    = 1080（永远不变）
SVG viewBox 高度    = A 区实际占用 + 60 边距
节点最小 padding    = 14px
节点间最小 gap      = 20px
节点圆角            = 8 (常规) / 17 (胶囊) / 10 (gallery card)
节点描边粗细        = 1.5px (常规) / 2.4px (强调) / 2.5px (final state)
```

## A 区起点

各图的"section-label / section-sub"文字一般在 y=20~92。
A 区第一个容器（tier-band / lifeline / lane）从 y=70~100 起。

## 节点尺寸推荐

| 用途 | width × height |
|---|---|
| 流程图常规处理矩形       | 200 × 60   |
| 流程图判断菱形           | 180 × 80   |
| 架构图客户端/边缘节点    | 210 × 88~96 |
| 架构图 BFF/服务节点      | 200~270 × 80~104 |
| 状态机普通态             | 180 × 70 |
| 状态机终态（同心圆）     | r=22 outer, r=16 inner |
| 时序图 actor 头          | 200 × 50 |
| ER 图实体表格            | 240 × 自适应（按字段数） |
| 泳道节点                 | 180 × 60 |

## 容器尺寸推荐

| 容器 | 尺寸 |
|---|---|
| 架构图 tier-band         | x=30, w=1020, h=120~180 |
| 泳道 lane（水平）        | h=120~160，w=1020 |
| 泳道 lane（垂直）        | w=240~260，h=按内容 |
| 时序图 lifeline 间距     | 200~240 px |
| ER 区中心点             | 与 SVG 中心对齐 |

## 文字字号

```
section-label   : 22px serif (区标题，如 "A · 用户登录主路径")
section-sub     : 11px mono  (区副标)
t-cn (节点中文): 13px sans bold
t-en (节点英文): 11px mono lowercase
t-stack (技术栈): 11px mono
t-metric (指标) : 11px mono，可加颜色 class（gold/plum…）
t-title         : 13px sans bold
t-sub           : 10px sans
t-lbl           : 9.5~11px mono（边标签）
```

## 关键约定

1. **节点 x/y 用 10 的倍数**：网格更整齐
2. **同列节点 x 一致**：用 grid 思维布局
3. **同行节点 y 一致**：tier 之间统一节奏
4. **边走直角**（orthogonal routing）：除非时序图，否则别走斜线
   - 直角路径：`M x1,y1 L x_mid,y1 L x_mid,y2 L x2,y2`
   - 起点终点要预留 8-12px 间距，不贴节点边
5. **数据流方向**：架构图一般 **从上到下**；流程图 **从上到下**；时序图 **从左到右**

## 删 B 区后调整 SVG 高度

每张图的 catalog 卡片给了"删除 B 区后推荐 height"。一般规律：

| 图型 | B 区前最末 y | 推荐 svg height |
|---|---|---|
| 02 sequence       | 约 1200 | 1280 |
| 03 state-machine  | 约 1400 | 1480 |
| 04 architecture   | 约 1700 | 1780 |
| 05 ER             | 约 1100 | 1180 |
| 06 swimlane       | 约 1700 | 1780 |
| 06 vertical       | 约 1450 | 1530 |
| 07 microservice   | 约 1800 | 1880 |

> 具体看 catalog 卡片 "A 区结束 y 坐标" 字段。
