# 07 · 微服务架构图 / Microservices

## 用在哪里
讲**微服务运行时拓扑**：K8s namespace、sidecar、服务注册中心、消息总线、横切设施。
和 04 架构图的区别：**强调"运行时部署形态"**（namespace 边界、sidecar 注入），而不是抽象分层。

> 抽象分层视角 → 用 [04 系统架构图](./04-system-architecture.md)

## 模板信息

- **模板文件**：`07-microservice.html`
- **viewBox**：`1080 × 1500`
- **关键行号**
  - SVG 开始：467
  - A 区主图：484–930
  - `</svg>`：1250
  - `window.DIAGRAM_CONFIG`：1339



## 画法参考

- **元素图鉴 + 怎么画**：[`templates/gallery/07-microservice.html`](../templates/gallery/07-microservice.html)
- 模板内保留 aside.legend-group 作快速查阅；完整教学在 index 对应 section。

## 容器结构（行块布局）

跟 04 用 tier-band 不同，07 用 **row 分组**（`<g id="row-xxx">`）：

```
row 1 · clients      [iOS]  [Web]  [Admin]
row 2 · edge         [CDN]
row 3 · gateway      [API GW ──────────] [Registry]
row 4 · bff          [Mobile BFF] [Web BFF] [Admin BFF]
row 5 · k8s-ns       ┌─ Namespace: trade ────┐
                     │ [order] [pay] [refund]│
                     └───────────────────────┘
row 6 · data         [MySQL] [Redis] [Kafka]
row 7 · infra        [k8s] [Istio] [Prom] [Jaeger]
```

K8s namespace 是个**虚线方框**包裹多个服务节点 + 一个 namespace 标签。

## 节点类型

与 04 几乎一致：
- `node client` / `node edge-net` / `node bff`
- `node svc` / `node svc core` / `node svc trade` / `node svc catalog`
- `node mw` / `node mw cache` / `node mw search`
- `node data-store` / `node infra`

**核心服务**可挂 `<rect class="core-badge">` + CORE 字样徽章。

## 边类型

同 04 架构图：`edge sync-arch` / `edge rpc` / `edge async-event` / `edge db-edge` / `edge cache-edge` / `edge cdc` / `edge scrape` / `edge spine`。

## 改造步骤（3 步）

### Step 1 · 复制
```bash
cp $SKILL_DIR/templates/07-microservice.html \
   <output-dir>/<scenario>-microservice.html
```

### Step 2 · 改 A 区主图 + 同步 nodeData
1. 定 row 列表（clients / edge / gateway / bff / namespaces / data / infra）
2. 改每个 `<g id="row-X">` 内容
3. K8s namespace 用虚线 rect 包裹同 namespace 的服务
4. 画主路径 spine（client → gateway → bff → core svc）
5. 同步 nodeData（默认 h=1500）

### Step 3 · 改外壳 + 自检
- `<title>` / `<h1>` / `.lead` / `.stat-row`
- 自检：sidecar 紧贴服务底部；观测面 scrape 边完整

## 反例

- ✗ 不画 namespace 边界（这是 07 区别于 04 的关键）
- ✗ 把横切设施（Prom / Jaeger）放业务 row（应独立横切行）
- ✗ sidecar 不标注（istio-proxy 是 07 的特色）

## 示例片段

```html
<!-- K8s namespace 虚线方框（包裹同一 namespace 的服务） -->
<g id="k8s-namespace">
  <rect x="30" y="560" width="720" height="580" rx="10"
        fill="none" stroke="#6B5B95" stroke-width="1.4"
        stroke-dasharray="8 4" opacity="0.6"/>
  <rect x="46" y="568" width="262" height="20" rx="3"
        fill="#FAF9F5" stroke="#6B5B95" stroke-width="0.8"/>
  <text x="58" y="583" font-family="ui-monospace, monospace" font-size="9.5"
        fill="#6B5B95" font-weight="700" letter-spacing="0.08em">K8S NAMESPACE: production</text>
  <text x="46" y="606" font-family="ui-monospace, monospace" font-size="9"
        fill="#87867F" letter-spacing="0.06em">istio mesh · sidecar 自动注入 · mTLS</text>
</g>

<!-- 核心服务节点（带 CORE 徽章 + sidecar） -->
<g class="node svc core" data-id="svc-order" tabindex="0">
  <rect class="shape" x="60" y="625" width="200" height="135"/>
  <rect class="core-badge" x="75" y="635" width="38" height="14"/>
  <text class="core-badge-text" x="94" y="646" text-anchor="middle">CORE</text>
  <text class="t-cn"    x="160" y="667" text-anchor="middle">order-service</text>
  <text class="t-en"    x="160" y="681" text-anchor="middle">订单服务</text>
  <text class="t-stack" x="160" y="700" text-anchor="middle">Java 17 · Spring Boot 3</text>
  <text class="t-stack" x="160" y="716" text-anchor="middle">:8002 · gRPC + REST</text>
  <text class="t-metric olive" x="160" y="734" text-anchor="middle">QPS 8K · 12 pods</text>
  <text class="t-metric olive" x="160" y="750" text-anchor="middle">Saga TCC</text>
</g>

<!-- Envoy sidecar 标签（紧贴服务节点底部） -->
<rect class="sidecar-box" x="60" y="765" width="200" height="32"/>
<text class="sidecar-label" x="160" y="780" text-anchor="middle">▣ ENVOY SIDECAR</text>
<text class="t-en"          x="160" y="792" text-anchor="middle">mTLS · trace · retry · timeout</text>

<!-- 普通服务节点（无徽章） -->
<g class="node svc catalog" data-id="svc-product" tabindex="0">
  <rect class="shape" x="280" y="625" width="200" height="135"/>
  <text class="t-cn"    x="380" y="650" text-anchor="middle">product-service</text>
  <text class="t-en"    x="380" y="666" text-anchor="middle">商品服务</text>
  <text class="t-stack" x="380" y="686" text-anchor="middle">Java 17 · Spring Boot</text>
  <text class="t-metric plum" x="380" y="722" text-anchor="middle">QPS 12K · 8 pods</text>
</g>

<!-- 主路径 spine 边 -->
<path class="edge spine" d="M160,420 L160,560" marker-end="url(#arrow-olive-bold)"/>
```

## 关键 class 速查

| class | 用途 |
|---|---|
| `core-badge` + `core-badge-text` | 服务节点左上的 "CORE" 徽章 |
| `sidecar-box` + `sidecar-label`  | Envoy sidecar 紧贴服务底部的横条 |
| `node svc core`                  | 主路径核心服务（olive 加粗边） |
| `node svc trade`                 | 交易域服务（clay） |
| `node svc catalog`               | 商品域服务（plum） |
| `node svc`                       | 默认业务服务（无业务域） |
| `edge spine`                     | 主路径强调（olive 加粗） |
