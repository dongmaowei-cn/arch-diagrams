# 边类型清单 · 7 种语义边 + 9 个 markers

所有模板共享同一套箭头 markers（在 SVG `<defs>` 里），**不要新增**。

## marker 列表（颜色对应）

| marker id | 颜色 | 用途 |
|---|---|---|
| `arrow`             | gray-500 (#87867F) | 默认 |
| `arrow-clay`        | clay (#D97757)     | DB 读写、动作 |
| `arrow-olive`       | olive (#788C5D)    | 成功路径 / 主路径 spine |
| `arrow-olive-bold`  | olive 加粗         | 主路径强调（架构图 spine） |
| `arrow-rust`        | rust (#B04A3F)     | 失败路径 / NO 分支 |
| `arrow-plum`        | plum (#6B5B95)     | 外部接口 / 消息 |
| `arrow-gold`        | gold (#C4994E)     | 网关 / 边缘 |
| `arrow-teal`        | teal (#4A8585)     | 横切设施 / 监控 |
| `arrow-slate`       | slate (#141413)    | 同步调用（深色） |
| `arrow-open`        | gray, 空心         | return 返回 |

## 边样式（CSS class）

### 通用
| class | 视觉 | 用途 |
|---|---|---|
| `edge`           | gray 实线 + arrow            | 默认顺序流 |
| `edge yes`       | olive 实线 + arrow-olive     | 判断 YES 分支 |
| `edge no`        | rust 虚线 + arrow-rust       | 判断 NO 分支 |
| `edge db`        | clay 虚线 + arrow-clay       | 数据库读写（流程图） |
| `edge async`     | gray 虚线                    | 异步 |
| `edge return`    | gray 虚线 + arrow-open       | 时序图 return |
| `edge sync`      | slate 实线 + arrow-slate     | 时序图同步调用 |
| `edge msg`       | plum 实线 + arrow-plum       | 消息 |
| `edge thick`     | 加粗                         | 主路径强调 |
| `edge bidir`     | 两端箭头                     | 双向 |
| `edge no-arrow`  | 无箭头                       | 仅连接 |
| `edge spine`     | olive 加粗 + arrow-olive-bold | 架构图/状态机 主路径 |

### 架构图专用
| class | 用途 |
|---|---|
| `edge sync-arch`   | 同步 RPC |
| `edge rpc`         | RPC 调用 |
| `edge async-event` | Kafka/MQ 异步事件 |
| `edge db-edge`     | 服务 → DB（clay 虚线） |
| `edge cache-edge`  | 服务 → Cache（gold） |
| `edge cdc`         | CDC 变更数据 |
| `edge scrape`      | Prometheus scrape |

### 时序图专用
| class | 用途 |
|---|---|
| `edge sync`       | 同步调用（实线） |
| `edge async msg`  | 异步消息（plum 虚线） |
| `edge return`     | 返回（空心箭头） |

### 状态机专用
| class | 用途 |
|---|---|
| `edge yes` / `edge no` | 条件转移 |
| `edge spine`           | 主路径 |

## 边标签（小标签贴在线上）

| class | 颜色 | 用途 |
|---|---|---|
| `edge-label`         | gray  | 默认 |
| `edge-label-bg`      | paper | 标签底（消除线穿过） |
| `edge-label yes`     | olive | YES |
| `edge-label fail`    | rust  | 失败 |
| `edge-label trigger` | slate | 状态机触发 |
| `edge-label guard`   | clay  | 状态机守卫条件 |
| `edge-label action`  | olive | 状态机动作 |
| `edge-label clay`    | clay  | 强调 |
| `edge-label gold`    | gold  | 网关相关 |
| `edge-label olive`   | olive | 成功相关 |
| `edge-label plum`    | plum  | 外部相关 |
| `edge-label teal`    | teal  | 横切相关 |

## 标签写法

```svg
<g class="edge-group">
  <path class="edge sync" d="M100,200 L400,200" marker-end="url(#arrow-slate)"/>
  <rect class="edge-label-bg" x="220" y="190" width="60" height="20" rx="3"/>
  <text class="edge-label" x="250" y="204" text-anchor="middle">POST /pay</text>
</g>
```

`edge-label-bg` 必须比 `edge-label` 先画（保证文字在白底之上）。

## 反例（不要做）

- ✗ 在判断节点的 NO 出边用 `edge yes`
- ✗ 自己新建一个 marker
- ✗ 用 `stroke` 直接覆盖 class 样式
- ✗ 一条边贴 3 个以上 label
