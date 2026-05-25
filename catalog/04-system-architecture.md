# 04 · 系统架构图 / System Architecture

## 用在哪里
讲**整个系统的物理拓扑**：分了几层、每层有哪些组件、技术栈是什么、QPS 多大。
强调**层次（tier）+ 节点（技术栈卡片）+ 主路径 spine**。

> 微服务运行时（K8s ns / sidecar）→ 用 [07 微服务架构图](./07-microservice.md)
> 数据模型 → 用 [05 ER 图](./05-er-diagram.md)

## 模板信息

- **模板文件**：`04-system-architecture.html`
- **viewBox**：`1080 × 1500`
- **关键行号**
  - SVG 开始：420
  - A 区主图：434–889
  - `</svg>`：1146
  - `window.DIAGRAM_CONFIG`：1247



## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/04-system-architecture.html`](../templates/gallery/04-system-architecture.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 容器结构

架构图核心是 **tier-band（层带子）**，每层一个：

```
┌───────────────────────────────────────────────────┐
│  01 Client │ [节点1] [节点2] [节点3] [节点4]      │
│  客户端层  │                                       │
└───────────────────────────────────────────────────┘
┌───────────────────────────────────────────────────┐
│  02 Edge   │ [CDN] [WAF] [Gateway] [LB]           │
│  边缘接入  │                                       │
└───────────────────────────────────────────────────┘
...
```

- `<rect class="tier-band" x="30" y="<Y>" width="1020" height="<H>">`
- 标签贴左侧（x=50）：`tier-num`(序号) / `tier-name`(英文) / `tier-cn`(中文) / `tier-sub`(说明)
- 节点从 x=140 开始排，等距
- spine 层（主路径所在层）用 `tier-band spine`（olive 加深背景）

## 节点类型（class）

| class | 颜色 | 何时用 |
|---|---|---|
| `node client`         | gray  | 客户端（Web / iOS / Android / 小程序） |
| `node edge-net`       | gold  | CDN / WAF / API Gateway / LB |
| `node bff`            | plum  | BFF 聚合层 |
| `node svc core`       | olive | 核心服务（主路径） |
| `node svc trade`      | clay  | 交易域服务 |
| `node svc catalog`    | plum  | 商品/库存域服务 |
| `node svc edge-domain`| teal  | 用户/通知/推荐域 |
| `node mw`             | gray  | 中间件（默认） |
| `node mw cache`       | gold  | 缓存（Redis） |
| `node mw search`      | teal  | 搜索（ES） |
| `node data-store`     | clay  | 数据库（MySQL / TiDB / ClickHouse） |
| `node infra`          | teal  | 横切设施（K8s / Prom / Jaeger） |

## 节点内容（4 行文本）

```html
<g class="node svc core" data-id="svc-order" tabindex="0">
  <rect class="shape" x="140" y="540" width="200" height="104"/>
  <text class="t-cn"    x="154" y="562">订单服务</text>
  <text class="t-en"    x="154" y="578">order-service · go</text>
  <text class="t-stack" x="154" y="598">Kratos · gRPC · 24 实例</text>
  <text class="t-metric olive" x="154" y="618">8 万 QPS · P99 80ms</text>
</g>
```

文字 class：
- `t-cn`：中文名（13px sans）
- `t-en`：英文/技术名（11px mono）
- `t-stack`：技术栈（11px mono）
- `t-metric`：关键指标，可加颜色 class（`gold` / `olive` / `plum` / `clay` / `teal`）

## 边类型

| class | 视觉 | 何时用 |
|---|---|---|
| `edge sync-arch`   | slate 实线   | 同步 |
| `edge rpc`         | gray 实线    | RPC 调用 |
| `edge async-event` | plum 虚线    | Kafka / MQ 异步事件 |
| `edge db-edge`     | clay 虚线    | 服务 → DB |
| `edge cache-edge`  | gold 实线    | 服务 → Cache |
| `edge cdc`         | teal 虚线    | CDC 变更数据 |
| `edge scrape`      | teal 虚线    | Prometheus scrape |
| `edge spine`       | olive 粗实线 | 主路径强调 |

## 坐标约定

```
viewBox 1080 × <按内容调整>
节点统一宽 200~270，高 80~104
tier-band: x=30, w=1020, h=120~180（按节点数调）
节点起始 x=140，等距 230 步进（4 个节点）
tier 之间垂直 gap=20
节点 y = tier-band y + 30
```

## 改造步骤（3 步）（5 步）

### Step 1 · 复制
```bash
cp ~/.claude/skills/arch-diagrams/templates/04-system-architecture.html \
   <output-dir>/<scenario>-architecture.html
```


### Step 2 · 改 A 区主图

1. **规划层数**：常见 4-7 层。最少应包含：client / edge / service / data-store
2. **改 section-label**：`A · <场景名> · N 层分层架构`
3. **每层一个 tier-band**：
   - 计算 y 坐标：每层 100~150 高 + 20 gap
   - tier-num / tier-name / tier-cn / tier-sub 写左侧
4. **每层放节点**：按业务挑 class，4 行文字填充
5. **画 spine 主路径**：用 `edge spine` 自上而下串起核心节点
6. **画其它边**：DB 用 `edge db-edge`，cache 用 `edge cache-edge` 等

### Step 2 · 同步 nodeData
每个节点都要有 nodeData 项，meta 三件套：tier 信息 / 技术栈 / 关键指标。

### Step 3 · 改外壳 + 自检
- `<title>` / `.eyebrow` / `<h1>` / `.lead`
- `.stat-row`：层数 / 节点数 / 峰值 QPS
- 自检：tier-band 不重叠；节点不超出 tier-band；spine 连续

## 反例

- ✗ 同一层混用 5 种颜色（每层尽量同一类 class）
- ✗ DB 画在 service 层（数据存储应单独一层）
- ✗ 跨层斜线（必须正交）
- ✗ 横切设施（K8s/Prom）和业务服务混在一层（要么放最底/最右，要么独立横切带）
