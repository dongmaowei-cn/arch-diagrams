#!/usr/bin/env bash
# selftest.sh — arch-diagrams skill 输出自检
# usage: bash selftest.sh <output.html>

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: bash selftest.sh <output.html>" >&2
  exit 2
fi

FILE="$1"
if [[ ! -f "$FILE" ]]; then
  echo "✗ file not found: $FILE" >&2
  exit 2
fi

PASS=0
FAIL=0

check() {
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "  ✓ $desc"
    PASS=$((PASS + 1))
  else
    echo "  ✗ $desc"
    FAIL=$((FAIL + 1))
  fi
}

fail() {
  echo "  ✗ $1"
  FAIL=$((FAIL + 1))
}

echo "═══ arch-diagrams selftest: $FILE ═══"

# 1. SVG data-id ↔ nodeData key 双向对齐
SVG_IDS=$(/usr/bin/grep -oE 'data-id="[^${}"]+"' "$FILE" | sed -E 's/data-id="(.*)"/\1/' | sort -u)
DATA_IDS=$(/usr/bin/grep -oE "^ +'[a-zA-Z0-9_-]+': \{" "$FILE" | sed -E "s/^ +'(.*)': \{/\1/" | sort -u)

ORPHAN_SVG=$(comm -23 <(echo "$SVG_IDS") <(echo "$DATA_IDS") || true)
ORPHAN_DATA=$(comm -13 <(echo "$SVG_IDS") <(echo "$DATA_IDS") || true)

if [[ -z "$ORPHAN_SVG" && -z "$ORPHAN_DATA" ]]; then
  N=$(echo "$SVG_IDS" | grep -c . || true)
  echo "  ✓ node-data 对齐 (${N} 个节点)"
  PASS=$((PASS + 1))
else
  echo "  ✗ node-data 不对齐"
  [[ -n "$ORPHAN_SVG" ]]  && echo "      SVG 有但 nodeData 无：$(echo $ORPHAN_SVG)"
  [[ -n "$ORPHAN_DATA" ]] && echo "      nodeData 有但 SVG 无：$(echo $ORPHAN_DATA)"
  FAIL=$((FAIL + 1))
fi

# 2. viewBox 与 svg height 一致
SVG_LINE=$(/usr/bin/grep -m1 -E 'class="(diagram|flow)" id="diagram"' "$FILE" || true)
SVG_H=$(echo "${SVG_LINE:-}" | /usr/bin/grep -oE 'height="[0-9]+"' | /usr/bin/grep -oE '[0-9]+' || true)
VB_H=$(echo "${SVG_LINE:-}" | /usr/bin/grep -oE 'viewBox="0 0 [0-9]+ [0-9]+"' | /usr/bin/grep -oE '[0-9]+' | tail -1 || true)

if [[ -n "${SVG_H:-}" && "${SVG_H:-}" == "${VB_H:-}" ]]; then
  echo "  ✓ viewBox 与 svg height 一致 (${SVG_H})"
  PASS=$((PASS + 1))
else
  fail "viewBox 与 svg height 不一致: height=${SVG_H:-empty}, viewBox-h=${VB_H:-empty}"
fi

# 3. B 区已删（搜不到 B 区注释、且无 SVG 节点使用 gallery-card-node）
if /usr/bin/grep -qE '<!-- B ·|<!-- 区 B' "$FILE" \
   || /usr/bin/grep -qE 'class="node gallery-card-node"|class="gallery-card-node"' "$FILE"; then
  fail "B 区元素图鉴未清理 (搜到 B 区注释或 gallery-card-node 节点)"
else
  echo "  ✓ B 区已删 (无 gallery-card-node 节点)"
  PASS=$((PASS + 1))
fi

# 4. nodeData 中无残留 g-* 伪节点
if /usr/bin/grep -qE "^ +'g-[a-z-]+': \{" "$FILE"; then
  LEFT=$(/usr/bin/grep -oE "'g-[a-z-]+':" "$FILE" | sort -u | tr '\n' ' ')
  fail "nodeData 残留 g- 前缀伪节点：$LEFT"
else
  echo "  ✓ nodeData 无 g- 前缀残留"
  PASS=$((PASS + 1))
fi

# 5. ER 模板特定残留（pk-marker/fk-marker 等）
ER_PSEUDO="pk-marker|fk-marker|crows-foot|one-to-many|many-to-many|self-ref|field-markers"
if /usr/bin/grep -qE "^ +'($ER_PSEUDO)': \{" "$FILE" 2>/dev/null && /usr/bin/grep -q "er-diagram\|crowfoot\|er-edge" "$FILE"; then
  fail "ER nodeData 残留教学伪节点"
else
  echo "  ✓ ER 教学伪节点无残留"
  PASS=$((PASS + 1))
fi

# 6. 外壳文字已替换（不应残留模板原场景的特征词）
#    仅在"产物模式"下生效;模板本身就该带原场景标题,自动跳过。
#    模板判定：文件路径含 templates/ 目录 且 文件名以 0?-*.html 命名。
BASENAME=$(basename "$FILE")
IS_TEMPLATE=0
if [[ "$FILE" == *templates/* && "$BASENAME" =~ ^0[0-9]?-.*\.html$ ]]; then
  IS_TEMPLATE=1
fi

if [[ "$IS_TEMPLATE" -eq 1 ]]; then
  echo "  ○ 外壳文字检查 (跳过 · 模板态)"
else
  ORIG_KEYWORDS="提现审核|UnionPay|订单结算 idempotency|订单业务状态机|电商交易中台|订单业务 ER|电商订单跨部门|API 记录创建|电商微服务全景"
  if /usr/bin/grep -qE "<title>.*($ORIG_KEYWORDS)" "$FILE"; then
    fail "<title> 仍是模板原场景标题，未替换"
  else
    echo "  ✓ 外壳文字已替换"
    PASS=$((PASS + 1))
  fi
fi

# 7. 不可见崩裂检查（基础 HTML/SVG 结构）
SVG_OPEN=$(/usr/bin/grep -c '<svg ' "$FILE" || true)
SVG_CLOSE=$(/usr/bin/grep -c '</svg>' "$FILE" || true)
if [[ "$SVG_OPEN" -eq "$SVG_CLOSE" ]]; then
  echo "  ✓ <svg> 开闭标签对称 (${SVG_OPEN} 对)"
  PASS=$((PASS + 1))
else
  fail "<svg> 开闭不对称：开=$SVG_OPEN 闭=$SVG_CLOSE"
fi

echo "───────────────────────────────────────"
echo "  通过 $PASS · 失败 $FAIL"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
