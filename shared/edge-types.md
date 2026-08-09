# 边类型清单 · 语义边与 markers

## ⚠️ marker id 不是所有模板通用的——用之前先看目标模板自己的 `<defs>`

下表是**并集参考**（帮你知道"大概有哪些颜色可用"），但每个模板的 `<defs>` 里只定义了它自己用得到的 markers，**不是这张表列出的都能在任意模板里直接引用**。引用一个当前模板没定义的 marker id 不会报错，只会**静默画不出箭头**（SVG 规范如此），selftest/edge-check 也检查不出来，只能靠肉眼或者提前 grep 确认。

已知最容易踩的坑：**"同步调用"这一个语义在不同模板里 marker id 不一样**——
`02-sequence` / `04-system-architecture` / `07-microservice` 用的是 `arrow-sync`；
`03-state-machine` / `05-er-diagram` / `06-swimlane` / `06-swimlane-vertical` 用的是 `arrow-slate`。
用错模板会导致同步调用边没有箭头。用之前跑一下：
```bash
grep -oE '<marker id="[^"]+"' <output-dir>/<file>.html
```
拿到当前文件真正可用的 marker id 列表，而不是死记这张表。

## marker 列表（并集参考，颜色对应）

| marker id | 颜色 | 用途 | 已知使用的模板 |
|---|---|---|---|
| `arrow`             | gray-500 (#87867F) | 默认 | 全部 |
| `arrow-clay`        | clay (#D97757)     | DB 读写、动作 | 多数 |
| `arrow-olive`       | olive (#788C5D)    | 成功路径 / 主路径 spine | 全部 |
| `arrow-olive-bold`  | olive 加粗         | 主路径强调（架构图 spine） | 多数 |
| `arrow-rust`        | rust (#B04A3F)     | 失败路径 / NO 分支 | 全部 |
| `arrow-plum`        | plum (#6B5B95)     | 外部接口 / 消息 | 多数 |
| `arrow-gold`        | gold (#C4994E)     | 网关 / 边缘 | 多数 |
| `arrow-teal`        | teal (#4A8585)     | 横切设施 / 监控 | 多数 |
| `arrow-sync`        | slate/gray-700 (深色) | 同步调用 | 02 / 04 / 07 |
| `arrow-slate`       | slate (#141413)    | 同步调用（深色） | 03 / 05 / 06H / 06V |
| `arrow-open`        | gray, 空心         | return 返回 | 多数 |

不要凭空新增 marker——但如果目标模板本身没有你要的颜色/语义，先 `grep` 确认真的没有，再决定是复用最接近的已有 marker，还是照抄同 `<defs>` 里已有 marker 的写法新增一个（同色系、同 viewBox 尺寸），而不是引用一个不存在的 id。

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
  <!-- 02/04/07 里同步调用箭头是 arrow-sync，不是 arrow-slate，见上面 marker 表 -->
  <rect class="edge-label-bg" x="220" y="190" width="60" height="20" rx="3"/>
  <text class="edge-label" x="250" y="204" text-anchor="middle">POST /pay</text>
</g>
```

`edge-label-bg` 必须比 `edge-label` 先画（保证文字在白底之上）。

## 反例（不要做）

- ✗ 在判断节点的 NO 出边用 `edge yes`
- ✗ 引用当前模板 `<defs>` 里没有的 marker id（不报错，箭头静默画不出——用前先 grep 确认存在）
- ✗ 凭空发明本表之外的新颜色/新样式（如果确实缺一个语义，就照抄同 `<defs>` 里已有 marker 的写法新增，保持同色系同尺寸，而不是自创视觉风格）
- ✗ 用 `stroke` 直接覆盖 class 样式（会被 CSS 类选择器的优先级打败，看起来像生效了实际没生效；要覆盖就加/改一个 class，别指望 `stroke=` 属性能赢 CSS 规则）
- ✗ 一条边贴 3 个以上 label
