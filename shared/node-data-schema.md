# nodeData Schema · aside 详情面板协议

aside 详情面板（点击 SVG 节点弹出的右侧详情）由
`window.DIAGRAM_CONFIG.nodeData` 驱动。**每个 SVG `<g class="node" data-id="X">`
都必须对应一个 `nodeData['X']`。**

## 顶层结构

```js
window.DIAGRAM_CONFIG = {
  viewBox: { w: 1080, h: 1500 },           // SVG 自然尺寸；删 B 区后改 h
  exportName: 'user-login-sequence',       // 导出的 SVG/PNG 文件名（不含扩展名）
  svgStyle: '',                            // 可选；通常留空
  nodeData: {
    'node-id-1': { /* see below */ },
    'node-id-2': { ... },
    ...
  }
};
```

## 单个节点对象

```js
'svc-payment': {
  type: 'svc',                      // 节点 type（影响 aside 显示风格，与 SVG class 对齐）
  tagClass: 't-svc',                // 底部 tag 的 CSS class（见下表）
  title: 'Payment Service — 支付服务',
  meta: [                           // 顶部小标签列表，用 · 自动连接
    'tier 04 · core',
    'Go · Kratos · 32 实例',
    '8000 QPS'
  ],
  body: `<p>核心支付服务，承载……</p>
<pre>tech:
· Go 1.22 + Kratos v2
· MySQL 8 · TiDB 6
· Kafka 3 · Redis 7</pre>`,
  tags: ['payment', 'main-path', 'tier-4']
}
```

## tagClass 速查（底部标签着色）

| tagClass | 颜色 | 适用 |
|---|---|---|
| `t-term`        | gray   | 起止、中性节点 |
| `t-process`     | slate  | 处理节点（流程图） |
| `t-decision`    | clay   | 判断节点 |
| `t-io`          | plum   | 输入输出（流程图） |
| `t-db`          | clay   | 数据库节点 |
| `t-subprocess`  | olive  | 子流程节点 |
| `t-document`    | rust   | 文档节点 |
| `t-connector`   | clay   | 连接符 |
| `t-success`     | olive  | 成功终态 |
| `t-fail`        | rust   | 失败终态 |
| `t-actor`       | slate  | 时序图参与者、架构图客户端 |
| `t-state`       | slate  | 状态机的态 |
| `t-entity`      | slate  | ER 图实体 |
| `t-rel`         | clay   | ER 关系 |
| `t-gate`        | gold   | 网关、CDN、WAF |
| `t-event`       | olive  | 事件 / 消息 |
| `t-zone`        | olive  | 安全区 |
| `t-firewall`    | rust   | 防火墙 |

## body 允许的 HTML

```
<p>段落，支持 <b>加粗</b> <code>行内代码</code> <u>下划线</u></p>
<pre>多行代码块
保留缩进
不要超过 80 列</pre>
```

不要用 `<br>`、`<ul>`、`<table>` — 设计样式没适配。

## 字段填写建议

- **title**：中文名 + 英文/技术名，用 `—` 连接
- **meta**：恰好 3 项最佳；少则 1，多则 4
  - 第 1 项：所在层/泳道/阶段（如 `tier 04 · core`）
  - 第 2 项：技术栈（如 `Go · MySQL`）
  - 第 3 项：关键指标（如 `8000 QPS` / `P99 80ms`）
- **body**：1 段说明 + 1 段 `<pre>` 技术细节；总 ≤ 200 汉字
- **tags**：3-5 个，全小写英文短词

## 自检规则（必查）

1. SVG 中所有 `<g class="node" data-id="X">` 的 X，**都**在 nodeData 有键
2. nodeData 里的所有键，**都**在 SVG 能找到对应节点
3. `viewBox.h` 与 `<svg viewBox>` 实际高度一致
4. `exportName` 已改为本次场景的 kebab-case 名称
