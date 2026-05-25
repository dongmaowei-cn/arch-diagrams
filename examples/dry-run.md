# Dry-run · 端到端示例

> 用户一句话 → 最终交付 HTML 的完整动作链路。
> 此示例展示了 skill 怎么在不打断用户的情况下，从需求到产物全自动跑完。

---

## 场景

```
用户输入：
> 画一个用户在线下单的流程图，包含库存校验、支付分支、超时取消
```

## skill 的内部动作

### Phase 1 · 识别（无 tool 调用）

- 关键词扫描："流程图" → 命中 **01 flowchart**
- 场景抽取："用户在线下单" → kebab-case → `online-order`
- 节点抽取：库存校验、支付分支、超时取消 → 至少要含：
  - START / 提交订单 / 校验库存 / 库存判断 / 创建订单 / 等待支付 /
    支付判断 / 自动取消 / 发货 / SETTLED / CANCELED / OUT-OF-STOCK
- 输出路径：`<pwd>/online-order-flowchart.html`

### Phase 2 · 读取 catalog

```
Read ~/.claude/skills/arch-diagrams/catalog/01-flowchart.md
Read ~/.claude/skills/arch-diagrams/shared/node-data-schema.md  (按需)
```

### Phase 3 · 复制模板

```bash
cp ~/.claude/skills/arch-diagrams/templates/01-flowchart.html \
   ./online-order-flowchart.html
```

### Phase 4 · 改造（按 catalog/01 步骤）

```
Edit  <title>          : 业务流程图 · 用户在线下单
Edit  .eyebrow         : Diagram type 01 · 业务流程图 · 在线下单
Edit  <h1> + <em>      : 用户在线下单流程 — online order placement
Edit  .lead            : 1-2 句业务背景
Edit  .stat-row        : 12 节点 / 2 失败终态 / 3s P95

Edit  <svg> height     : 1500 → 1020（去掉空白）

Edit  A 区主图（行 293-438）替换为新节点 + 边
  - 12 个 <g class="node ..."> 块
  - 边路径走正交折线（YES olive / NO rust / DB clay-dashed）

Edit  NODE_DATA = { ... }
  - 删原 17 个 key
  - 新增 12 个 key（每个 data-id 一个）
```

（01 模板无 B 区，跳过 Step 2 + 2.5）

### Phase 5 · 自检

```bash
# 自检 1：所有 data-id 都有 nodeData
diff <(/usr/bin/grep -oE 'data-id="[^"]+"' online-order-flowchart.html | sort -u) \
     <(/usr/bin/grep -oE "^  '[a-z-]+':" online-order-flowchart.html | sort -u)

# 自检 2：viewBox 高度与 svg height 一致
/usr/bin/grep "viewBox=\"0 0 1080" online-order-flowchart.html | head -1

# 自检 3：搜不到原模板特有的 "提现" "UnionPay" 字样
/usr/bin/grep -c "提现\|UnionPay" online-order-flowchart.html   # 应为 0
```

### Phase 6 · 报告（一行）

```
✓ 已生成 ./online-order-flowchart.html（14 节点 · 11 条边 · viewBox 1080×1020）
```

---

## 时间复杂度参考

| 阶段 | 工具调用 | 累计 |
|---|---|---|
| 识别 + 读 catalog | 1 Read | ~3s |
| 复制 | 1 Bash | ~1s |
| 改外壳（4 处 Edit） | 4 Edit | ~6s |
| 改 SVG 主图 | 1 大块 Edit | ~10s |
| 改 nodeData | 1 大块 Edit | ~10s |
| 自检 | 1 Bash | ~2s |
| **合计** | ~9 工具调用 | ~30s |

---

## 失败场景的兜底

| 情况 | 处理 |
|---|---|
| `pwd` 不可写 | 退到 `~/Desktop/` 并提示用户 |
| 同名文件存在 | AskUserQuestion：覆盖 / 加后缀 / 取消 |
| 用户说"画个图"但无场景 | AskUserQuestion：你想画什么场景？ |
| 同场景多张图都合理 | AskUserQuestion：流程图 or 时序图？（带 preview） |
| 自检失败（节点 / data 不对齐） | 主动修复后再报告，不要把错误产物交付 |

---

## 真实参照

`~/Desktop/arch-diagrams-demo/online-order-flowchart.html`
就是按这个 dry-run 流程跑出来的产物，可作为回归参考。
