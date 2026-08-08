#!/usr/bin/env python3
"""edge-check.py — arch-diagrams 边几何自检

用法:
    python3 edge-check.py <output.html>

解析主图 <svg id="diagram"> 里的节点与边, 断言 9 条连线纪律:

  端点纪律（终点即边界，起点即出界）
  [1] 每条边的起点落在某节点边界上 (rect 四边 / circle 圆周 / polygon·path 外包框 / lifeline)
  [2] 起点不在节点角部 (距 rect / 外包框任一角 < CORNER_TOL 即报 —— "线从角上出发"是脏观感)
  [3] 每条边的终点(箭头)够到某节点边界 / 圆周 (误差 ≤ TOL —— "箭头悬空"算没画完)
  [4] 不存在"一条边的箭头终点 = 另一条边的起点"的碰撞 (≤ SHARE_TOL 即报
      —— 请求到达点和回执出发点挤在同一个边界点上, 就是这类问题。
      *注意* fan-in(多条箭头同时进同一点) / fan-out(多条边同点出发) 是正常模式, 不报)

  内部纪律（端点之外，线本身与节点/标签的干涉）
  [5] 曲线边 (C/S/Q/T/A) 的内部采样点不得落入任何节点形状内部
      —— 自环/弧线若"凸进节点里"(如椭圆圆心算在节点内、弧向左弯进矩形), 端点检查看不见, 采样才看得见
  [6] composite-bg 组合框内的节点必须完整落在框内
      —— 组框是语义容器, 节点探出框边(几像素都算)说明布局没对齐
  [7] 边标签 (edge-label / t-lbl) 的文字锚点不得落在节点形状内部
      —— 标签压在无关节点身体上 = 视觉事故; 允许贴在边界上但不允许探进内部
      *豁免*: 标签所属的那条边本身穿过该节点 (bus/backbone 线骑在节点上) 时不报
      —— 微服务/架构图的共享总线本来就画在服务卡片之上, 标签骑在线上是正常拓扑样式;
          只有"标签所属边并不经过该节点"仍落入节点内部才算误放
  [8] ER 关系线 (er-edge) 的直线段不得穿过任何表体 (table-frame) 内部
      —— 关系线必须正交绕行(走表间走廊), 横穿/斜穿表体是 ER 布局事故;
          端点本来就落在表边界, 内部采样(t∈(0,1)) + 3px 边界容差自动避开边界点
          (仅对 class 含 er-edge 的边生效, 不影响 bus/spine 等其它图型)
  [9] 时序图激活条: 贴 lifeline 的消息端点必须落在激活条上
      —— 覆盖: 端点 y 必须在某激活条 y 区间内(容差 ACT_TOL, 允许箭头在条顶上方 ~5px 设计间距)
               "激活条没盖住最后一条消息" = 条子画短了;
          贴边: 端点 x 必须贴激活条左/右边缘(EDGE_TOL), 不能在条中心/lifeline 上
               "消息从激活条中心出发/进入" = 线从图形内部进出, 观感脏
      (仅对 class 含 activation 的 rect 生效; 节点-节点连边不适用)

支持 8 种图型的结构差异:
  - 节点可能是 g.node 里的 rect / circle / polygon / path(菱形) / ellipse / g.node 外的 stub 小圆
  - 时序图用竖向 lifeline 做锚线, 消息箭头与 lifeline 有 ~5px 间距, 故 lifeline 容差放宽到 8px
  - 主图 svg 用 id="diagram" 定位 (flowchart 是 class="flow" id="diagram", 其它是 class="diagram")
  - 泳道 lane / 架构 tier-band 是容器 rect, 不是 g.node, 不参与"标签入节点/段穿节点"判定

这是 selftest 的第 8 项。无节点可解析或无可判定边时, 输出 ○ 并跳过(exit 0)。

退出码: 0 通过 / 1 有几何问题。
"""

import math
import re
import sys
import xml.etree.ElementTree as ET

TOL = 1.5        # 边界贴合容差(px): 路径端点应精确落在节点边上
LINE_TOL = 8.0   # lifeline 容差(px): 时序箭头与 lifeline 有 ~5px 设计间距
CORNER_TOL = 5.0 # 距矩形角 < 此值视为"从角部出发"
SHARE_TOL = 2.5  # 终点与起点 < 此距离视为"请求/回执碰撞"
INSIDE_TOL = 3.0 # 曲线采样点/直线段中点"探进节点内部"的容差(px): 探进超过此值才报
BOX_TOL = 1.0    # composite 框包含容差(px): 节点边缘探出框边超过此值才报
LABEL_TOL = 2.0  # 标签锚点"探进节点内部"的容差(px)
CURVE_SAMPLES = 3  # 每条曲线段采样的内部 t 值个数 (t=1/4,2/4,3/4)
ARC_SAMPLES = 5    # 圆弧采样的内部点数
ACT_TOL = 6.0      # 激活条覆盖容差(px): 箭头可在条顶上方 ~5px 设计间距
EDGE_TOL = 2.0     # 消息端点须贴激活条左/右边缘的容差(px)

# 哪些 <path> 是"边"而不是装饰/图标/容器。主图 svg 已过滤掉按钮图标与 legend 内联 svg。
EDGE_CLASS = re.compile(
    r'\b(vflow|seq-flow|flow|edge|msg|spine|arc|fail|req|res|lifeline-edge)\b'
)
LABEL_CLASS = re.compile(r'\b(edge-label|t-lbl)\b')


def parse_path_d(d):
    """把 <path d> 解析成 (绝对坐标点列表, 段列表)。

    点列表含起点(用于边折线与端点判定)。段列表含每个 M/L/H/V/C/S/Q/T/A/Z 产生的
    线段或曲线段, 供"内部纪律"采样:
      - 线段: {'kind':'line', 'a':(x,y), 'b':(x,y)}
      - 三次贝塞尔 (C/S): {'kind':'cubic', 'p0', 'c1', 'c2', 'p1'}
      - 二次贝塞尔 (Q/T): {'kind':'quad',  'p0', 'c1', 'p1'}
      - 圆弧 (A):         {'kind':'arc',   'p0', 'rx','ry','rot','large','sweep','p1'}
    """
    tokens = re.findall(
        r'[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', d)
    arity = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4,
             'Q': 4, 'T': 2, 'A': 7, 'Z': 0}
    points = []
    segs = []
    cur = (0.0, 0.0)
    start = None
    cmd = None
    prev_ctrl = None  # 上一个曲线的控制点, 供 S/T 平滑反射
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if re.match(r'[MmLlHhVvCcSsQqTtAaZz]', t):
            cmd = t
            i += 1
            continue
        if cmd is None:
            return None, []
        n = arity[cmd.upper()]
        if cmd in ('Z', 'z'):
            nxt = start if start else cur
            if nxt != cur:
                segs.append({'kind': 'line', 'a': cur, 'b': nxt})
            cur = nxt
            i += 1
            points.append(cur)
            prev_ctrl = None
            continue
        if i + n > len(tokens):
            return None, []
        nums = [float(x) for x in tokens[i:i + n]]
        i += n
        rel = cmd.islower()
        u = cmd.upper()

        def P(x, y):
            return ((x + cur[0]) if rel else x, (y + cur[1]) if rel else y)

        if u == 'M':
            cur = P(nums[0], nums[1])
            if start is None:
                start = cur
            prev_ctrl = None
        elif u == 'L':
            nxt = P(nums[0], nums[1])
            segs.append({'kind': 'line', 'a': cur, 'b': nxt})
            cur = nxt
            prev_ctrl = None
        elif u == 'H':
            nxt = ((nums[0] + cur[0]) if rel else nums[0], cur[1])
            segs.append({'kind': 'line', 'a': cur, 'b': nxt})
            cur = nxt
            prev_ctrl = None
        elif u == 'V':
            nxt = (cur[0], (nums[0] + cur[1]) if rel else nums[0])
            segs.append({'kind': 'line', 'a': cur, 'b': nxt})
            cur = nxt
            prev_ctrl = None
        elif u == 'C':
            c1 = P(nums[0], nums[1])
            c2 = P(nums[2], nums[3])
            p1 = P(nums[4], nums[5])
            segs.append({'kind': 'cubic', 'p0': cur, 'c1': c1, 'c2': c2, 'p1': p1})
            prev_ctrl = c2
            cur = p1
        elif u == 'S':
            c1 = (2 * cur[0] - prev_ctrl[0], 2 * cur[1] - prev_ctrl[1]) if prev_ctrl else cur
            c2 = P(nums[0], nums[1])
            p1 = P(nums[2], nums[3])
            segs.append({'kind': 'cubic', 'p0': cur, 'c1': c1, 'c2': c2, 'p1': p1})
            prev_ctrl = c2
            cur = p1
        elif u == 'Q':
            c1 = P(nums[0], nums[1])
            p1 = P(nums[2], nums[3])
            segs.append({'kind': 'quad', 'p0': cur, 'c1': c1, 'p1': p1})
            prev_ctrl = c1
            cur = p1
        elif u == 'T':
            c1 = (2 * cur[0] - prev_ctrl[0], 2 * cur[1] - prev_ctrl[1]) if prev_ctrl else cur
            p1 = P(nums[0], nums[1])
            segs.append({'kind': 'quad', 'p0': cur, 'c1': c1, 'p1': p1})
            prev_ctrl = c1
            cur = p1
        elif u == 'A':
            segs.append({'kind': 'arc', 'p0': cur, 'rx': nums[0], 'ry': nums[1],
                         'rot': nums[2], 'large': int(nums[3]), 'sweep': int(nums[4]),
                         'p1': P(nums[5], nums[6])})
            prev_ctrl = None
            cur = segs[-1]['p1']
        points.append(cur)
    return points, segs


# ── 曲线采样 ────────────────────────────────────────────────────────

def _cubic(p0, c1, c2, p1, t):
    mt = 1 - t
    return (
        mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * p1[0],
        mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * p1[1],
    )


def _quad(p0, c1, p1, t):
    mt = 1 - t
    return (
        mt * mt * p0[0] + 2 * mt * t * c1[0] + t * t * p1[0],
        mt * mt * p0[1] + 2 * mt * t * c1[1] + t * t * p1[1],
    )


def _arc(p0, rx, ry, phi_deg, large, sweep, p1, t):
    """SVG 椭圆弧的端点参数化 → 中心参数化采样。"""
    x1, y1 = p0
    x2, y2 = p1
    phi = math.radians(phi_deg)
    dx = (x1 - x2) / 2.0
    dy = (y1 - y2) / 2.0
    cosp, sinp = math.cos(phi), math.sin(phi)
    x1p = cosp * dx + sinp * dy
    y1p = -sinp * dx + cosp * dy
    rx = abs(rx) or 1e-9
    ry = abs(ry) or 1e-9
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1:
        s = math.sqrt(lam)
        rx *= s
        ry *= s
    sign = -1.0 if large == sweep else 1.0
    num = max(rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p, 0.0)
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    coef = sign * math.sqrt(num / den) if den > 1e-12 else 0.0
    cxp = coef * (rx * y1p / ry)
    cyp = coef * (-ry * x1p / rx)
    cx = cosp * cxp - sinp * cyp + (x1 + x2) / 2.0
    cy = sinp * cxp + cosp * cyp + (y1 + y2) / 2.0

    def _ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a + 2 * math.pi if a < 0 else a

    ux = (x1p - cxp) / rx
    uy = (y1p - cyp) / ry
    vx = (-x1p - cxp) / rx
    vy = (-y1p - cyp) / ry
    th1 = _ang(1.0, 0.0, ux, uy)
    dth = _ang(ux, uy, vx, vy)
    if sweep == 0 and dth > 0:
        dth -= 2 * math.pi
    if sweep == 1 and dth < 0:
        dth += 2 * math.pi
    a = th1 + dth * t
    return (
        cx + rx * math.cos(a) * cosp - ry * math.sin(a) * sinp,
        cy + rx * math.cos(a) * sinp + ry * math.sin(a) * cosp,
    )


def segment_samples(seg):
    """取一段的内部采样点(不含端点)。直线段取中点; 曲线段取多个 t 值。"""
    kind = seg['kind']
    if kind == 'line':
        a, b = seg['a'], seg['b']
        return [((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)]
    out = []
    for k in range(1, CURVE_SAMPLES + 1):
        t = k / (CURVE_SAMPLES + 1)
        if kind == 'cubic':
            out.append(_cubic(seg['p0'], seg['c1'], seg['c2'], seg['p1'], t))
        elif kind == 'quad':
            out.append(_quad(seg['p0'], seg['c1'], seg['p1'], t))
        elif kind == 'arc':
            out.append(_arc(seg['p0'], seg['rx'], seg['ry'], seg['rot'],
                            seg['large'], seg['sweep'], seg['p1'], t))
    return out


def is_curve_seg(seg):
    return seg['kind'] in ('cubic', 'quad', 'arc')


def edge_crosses_shape(segs, shape):
    """边是否"穿进"某节点内部(采样点探入 > INSIDE_TOL)。用于 [7] 的 bus 线豁免。"""
    for seg in segs:
        if seg['kind'] == 'line':
            a, b = seg['a'], seg['b']
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(2, int(L / 12))
            for k in range(1, n):
                t = k / n
                if shape.strictly_inside(a[0] + (b[0] - a[0]) * t,
                                         a[1] + (b[1] - a[1]) * t, INSIDE_TOL):
                    return True
        else:
            for (mx, my) in segment_samples(seg):
                if shape.strictly_inside(mx, my, INSIDE_TOL):
                    return True
    return False


# ── 距离 / 包围盒 ───────────────────────────────────────────────────

def dist_point_segment(px, py, a, b):
    """点到线段的距离。"""
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    wx, wy = px - ax, py - ay
    L2 = vx * vx + vy * vy
    if L2 <= 1e-9:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / L2))
    return math.hypot(px - (ax + t * vx), py - (ay + t * vy))


def dist_to_polyline(px, py, pts):
    return min(dist_point_segment(px, py, pts[i], pts[i + 1])
               for i in range(len(pts) - 1))


def path_bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)


class Shape:
    """一个可被边连接的节点形状。"""

    __slots__ = ('kind', 'nid', 'x', 'y', 'w', 'h', 'cx', 'cy', 'r')

    def __init__(self, kind, nid=None, x=None, y=None, w=None, h=None,
                 cx=None, cy=None, r=None):
        self.kind = kind          # rect | circle | poly(外包框) | line
        self.nid = nid            # data-id 或 None(terminal stub)
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cx, self.cy, self.r = cx, cy, r

    def label(self):
        if self.nid:
            return f"{self.kind}:{self.nid}"
        if self.kind == 'circle':
            return f"circle@{self.cx},{self.cy} r{self.r}"
        return f"{self.kind}({self.x},{self.y} {self.w}×{self.h})"

    def bounds(self):
        """外包框 (left, top, right, bottom)。"""
        if self.kind == 'circle' and self.cx is not None:
            return self.cx - self.r, self.cy - self.r, self.cx + self.r, self.cy + self.r
        if self.x is None:
            return None
        return self.x, self.y, self.x + self.w, self.y + self.h

    def center(self):
        b = self.bounds()
        if b is None:
            return None
        return (b[0] + b[2]) / 2, (b[1] + b[3]) / 2

    def on_boundary(self, px, py, tol):
        if self.kind == 'circle':
            if self.cx is None:
                return False
            d = math.hypot(px - self.cx, py - self.cy)
            return abs(d - self.r) <= tol
        if self.kind == 'line':
            # 竖向锚线: 水平贴近 x, 纵向在区间内
            return abs(px - self.x) <= LINE_TOL and self.y - tol <= py <= self.y + self.h + tol
        # rect / poly 按矩形外包框处理
        if self.x is None:
            return False
        on_h = (abs(px - self.x) <= tol and self.y - tol <= py <= self.y + self.h + tol) \
            or (abs(px - (self.x + self.w)) <= tol and self.y - tol <= py <= self.y + self.h + tol)
        on_v = (abs(py - self.y) <= tol and self.x - tol <= px <= self.x + self.w + tol) \
            or (abs(py - (self.y + self.h)) <= tol and self.x - tol <= px <= self.x + self.w + tol)
        return on_h or on_v

    def at_corner(self, px, py, tol):
        """起点距矩形四角之一 < tol(两个轴都算) —— 即从角部出发。"""
        if self.kind == 'circle' or self.x is None:
            return False
        corners = [
            (self.x, self.y),
            (self.x + self.w, self.y),
            (self.x, self.y + self.h),
            (self.x + self.w, self.y + self.h),
        ]
        return any(abs(px - cx) <= tol and abs(py - cy) <= tol for cx, cy in corners)

    def strictly_inside(self, px, py, margin):
        """点是否位于形状内部(距边界 > margin)。边界点不算内部。"""
        if self.kind == 'circle':
            if self.cx is None:
                return False
            return math.hypot(px - self.cx, py - self.cy) <= self.r - margin
        if self.kind == 'line' or self.x is None:
            return False
        return (self.x + margin <= px <= self.x + self.w - margin
                and self.y + margin <= py <= self.y + self.h - margin)


def main():
    if len(sys.argv) != 2:
        print('usage: python3 edge-check.py <output.html>', file=sys.stderr)
        return 2
    path = sys.argv[1]
    try:
        with open(path, encoding='utf-8') as f:
            html = f.read()
    except OSError as e:
        print(f'✗ 无法读取 {path}: {e}', file=sys.stderr)
        return 2

    m = re.search(r'<svg[^>]*id="diagram"[^>]*>(.*?)</svg>', html, re.S)
    if not m:
        print('○ 边几何校验 (跳过 · 未找到主图 <svg id="diagram">)')
        return 0
    try:
        root = ET.fromstring(f'<svg>{m.group(1)}</svg>')
    except ET.ParseError as e:
        print(f'✗ 主图 SVG 解析失败: {e}', file=sys.stderr)
        return 1

    def local(tag):
        return tag.rsplit('}', 1)[-1] if '}' in tag else tag

    parent_map = {c: p for p in root.iter() for c in p}

    def in_defs(el):
        p = parent_map.get(el)
        while p is not None:
            if local(p.tag) in ('defs', 'marker', 'symbol'):
                return True
            p = parent_map.get(p)
        return False

    def f(attr, el, default=0.0):
        try:
            return float(el.get(attr))
        except (TypeError, ValueError):
            return default

    # ── 收集节点形状 ──────────────────────────────────────────────
    shapes = []
    for g in root.iter():
        if local(g.tag) != 'g':
            continue
        if 'node' not in (g.get('class') or '').split():
            continue
        nid = g.get('data-id')
        kids = list(g)
        cands = []  # (area, Shape)
        for c in kids:
            tag = local(c.tag)
            if tag == 'rect':
                w, h = f('width', c), f('height', c)
                cands.append((w * h, Shape('rect', nid, x=f('x', c), y=f('y', c), w=w, h=h)))
            elif tag == 'circle':
                r = f('r', c)
                cands.append((math.pi * r * r, Shape('circle', nid, cx=f('cx', c), cy=f('cy', c), r=r)))
            elif tag == 'ellipse':
                rx, ry = f('rx', c), f('ry', c)
                cx, cy = f('cx', c), f('cy', c)
                cands.append((math.pi * rx * ry, Shape('poly', nid, x=cx - rx, y=cy - ry, w=rx * 2, h=ry * 2)))
            elif tag == 'polygon':
                pts = [float(v) for v in re.findall(r'[-+]?\d*\.?\d+', c.get('points', ''))]
                xs = pts[0::2] or [0.0]
                ys = pts[1::2] or [0.0]
                w = max(xs) - min(xs)
                h = max(ys) - min(ys)
                cands.append((w * h, Shape('poly', nid, x=min(xs), y=min(ys), w=w, h=h)))
            elif tag == 'path':
                pts, _ = parse_path_d(c.get('d', ''))
                if pts and len(pts) >= 3:
                    x, y, w, h = path_bbox(pts)
                    cands.append((w * h, Shape('poly', nid, x=x, y=y, w=w, h=h)))
        if cands:
            # 取最大面积形状: db 节点是"圆柱 path + 顶盖 ellipse", 顶盖更小, 会被正确跳过
            _, best = max(cands, key=lambda t: t[0])
            shapes.append(best)

    # standalone terminal stub(小圆, 不在 g.node 里) —— 也是可被箭头指向的目标
    for c in root.iter():
        if local(c.tag) != 'circle' or in_defs(c):
            continue
        if any('node' in (g.get('class') or '').split() for g in _ancestors(c, parent_map)):
            continue
        if c.get('cx') is None:
            continue
        shapes.append(Shape('circle', None, cx=f('cx', c), cy=f('cy', c), r=f('r', c)))

    # lifeline(时序图) —— 竖直锚线, 消息箭头落在线上的任意 y
    for line in root.iter():
        if local(line.tag) != 'line':
            continue
        if 'lifeline' not in (line.get('class') or '').split():
            continue
        x1, y1, x2, y2 = f('x1', line), f('y1', line), f('x2', line), f('y2', line)
        if abs(x1 - x2) <= 0.5:  # 仅竖向 lifeline
            shapes.append(Shape('line', None, x=x1, y=min(y1, y2), h=abs(y2 - y1), w=0))

    # ── 收集 composite 组合框 ─────────────────────────────────────
    boxes = []  # (x, y, w, h)
    for r in root.iter():
        if local(r.tag) != 'rect' or in_defs(r):
            continue
        if 'composite-bg' not in (r.get('class') or '').split():
            continue
        boxes.append((f('x', r), f('y', r), f('width', r), f('height', r)))

    # ── 收集边 ────────────────────────────────────────────────────
    edges = []  # (idx, class, d, points, segments)
    edge_pos = {}  # id(element) -> edge index, 供标签关联"所属边"
    for p in root.iter():
        if local(p.tag) != 'path' or in_defs(p):
            continue
        cls = (p.get('class') or '').strip()
        if not EDGE_CLASS.search(cls):
            continue
        d = p.get('d')
        if not d:
            continue
        pts, segs = parse_path_d(d)
        if not pts or len(pts) < 2:
            continue
        edge_pos[id(p)] = len(edges)
        edges.append((len(edges), cls, d, pts, segs))

    if not edges:
        print('○ 边几何校验 (跳过 · 未找到 vflow/edge 类边)')
        return 0
    if not shapes:
        print('○ 边几何校验 (跳过 · 未找到可判定节点形状)')
        return 0

    problems = []

    def on_other_edge(px, py, skip_idx):
        """点是否落在其它某条边的折线上 (交汇点/并入点, 合法)。"""
        for oi, _, _, opts, _ in edges:
            if oi == skip_idx:
                continue
            if dist_to_polyline(px, py, opts) <= TOL:
                return True
        return False

    # ── [1][2][3][4] 端点纪律 ─────────────────────────────────────
    for idx, cls, d, pts, segs in edges:
        sx, sy = pts[0]
        ex, ey = pts[-1]
        s_shapes = [s for s in shapes if s.on_boundary(sx, sy, TOL)]
        e_shapes = [s for s in shapes if s.on_boundary(ex, ey, TOL)]
        s_junction = on_other_edge(sx, sy, idx)
        e_junction = on_other_edge(ex, ey, idx)

        if not s_shapes and not s_junction:
            problems.append(f'  边 #{idx} [{cls}] 起点 ({sx:.0f},{sy:.0f}) 不在任何节点/边上\n'
                            f'      d="{d}"')
        elif s_shapes and not s_junction:
            # 起点在节点角部才报; 若同时是交汇点则视为合法并入
            corners = [s.label() for s in s_shapes if s.at_corner(sx, sy, CORNER_TOL)]
            if corners:
                problems.append(f'  边 #{idx} [{cls}] 起点 ({sx:.0f},{sy:.0f}) 从角部出发 '
                                f'(节点 {", ".join(corners)})\n'
                                f'      d="{d}"')

        if not e_shapes and not e_junction:
            problems.append(f'  边 #{idx} [{cls}] 箭头终点 ({ex:.0f},{ey:.0f}) 没够到任何节点/边\n'
                            f'      d="{d}"')

    # 请求/回执碰撞: 一条边的箭头终点恰好落在另一条边的起点上
    starts = [(idx, pts[0]) for idx, _, _, pts, _ in edges]
    for ei, (ex, ey) in [(idx, pts[-1]) for idx, _, _, pts, _ in edges]:
        for si, (sx, sy) in starts:
            if ei == si:
                continue
            if math.hypot(ex - sx, ey - sy) <= SHARE_TOL:
                problems.append(
                    f'  边 #{ei} 箭头终点 ({ex:.0f},{ey:.0f}) 与边 #{si} 起点共享同一连接点 '
                    f'(请求/回执碰撞)\n'
                    f'      #{ei}: d="{edges[ei][2]}"')
                break

    # ── [5] 曲线内部采样: 不得探进任何节点 ─────────────────────────
    for idx, cls, d, pts, segs in edges:
        for seg in segs:
            if not is_curve_seg(seg):
                continue
            for (mx, my) in segment_samples(seg):
                hit = [s for s in shapes
                       if s.strictly_inside(mx, my, INSIDE_TOL)]
                if hit:
                    problems.append(
                        f'  边 #{idx} [{cls}] 曲线段采样点 ({mx:.0f},{my:.0f}) 探进节点 '
                        f'{", ".join(s.label() for s in hit[:3])} 内部 '
                        f'(弧/贝塞尔凸进了节点身体)\n'
                        f'      d="{d}"')
                    break  # 一条边一条曲线报一次, 不刷屏

    # ── [6] composite 框包含: 框内节点必须完整落框内 ───────────────
    for bx, by, bw, bh in boxes:
        for s in shapes:
            if s.kind == 'line':
                continue
            c = s.center()
            if c is None:
                continue
            if not (bx <= c[0] <= bx + bw and by <= c[1] <= by + bh):
                continue
            b = s.bounds()
            if b is None:
                continue
            if (b[0] < bx - BOX_TOL or b[1] < by - BOX_TOL
                    or b[2] > bx + bw + BOX_TOL or b[3] > by + bh + BOX_TOL):
                problems.append(
                    f'  composite 框 ({bx:.0f},{by:.0f} {bw:.0f}×{bh:.0f}) 内节点 {s.label()} '
                    f'探出框边 (bounds {b[0]:.0f},{b[1]:.0f}-{b[2]:.0f},{b[3]:.0f}, '
                    f'框右/下 {bx+bw:.0f},{by+bh:.0f})')

    # ── [7] 边标签锚点: 不得落在节点内部 ───────────────────────────
    # 先按文档顺序收集标签并关联"所属边"(最后一个出现在它前面的边路径)。
    labels = []  # (x, y, cls, text, assoc_edge_idx | None)
    last_edge = None
    for el in root.iter():
        if local(el.tag) == 'path' and id(el) in edge_pos:
            last_edge = edge_pos[id(el)]
        elif local(el.tag) == 'text' and not in_defs(el):
            cls = (el.get('class') or '').strip()
            if LABEL_CLASS.search(cls):
                labels.append((f('x', el), f('y', el), cls,
                               (el.text or '').strip()[:28], last_edge))

    for lx, ly, cls, txt, assoc in labels:
        for s in shapes:
            if not s.strictly_inside(lx, ly, LABEL_TOL):
                continue
            # 豁免: 标签所属边本身穿过该节点 → bus 线骑线标签, 正常拓扑样式
            if assoc is not None and edge_crosses_shape(edges[assoc][4], s):
                continue
            problems.append(
                f'  边标签 "{txt}" 锚点 ({lx:.0f},{ly:.0f}) 落在节点 {s.label()} 内部'
                f' (所属边未经过该节点)')
            break

    # ── [8] ER 关系线 (er-edge) 直线段不得穿表体 ──────────────────────
    er_tables = []
    for g in root.iter():
        if local(g.tag) != 'g' or 'node' not in (g.get('class') or '').split():
            continue
        for c in g:
            if local(c.tag) == 'rect' and 'table-frame' in (c.get('class') or '').split():
                w, h = f('width', c), f('height', c)
                er_tables.append(Shape('rect', g.get('data-id'),
                                       x=f('x', c), y=f('y', c), w=w, h=h))
                break
    if er_tables:
        for idx, cls, d, pts, segs in edges:
            if 'er-edge' not in cls:
                continue
            for seg in segs:
                if seg['kind'] != 'line':
                    continue
                a, b = seg['a'], seg['b']
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                n = max(2, int(L / 12))
                hit = None
                for k in range(1, n):
                    mx = a[0] + (b[0] - a[0]) * (k / n)
                    my = a[1] + (b[1] - a[1]) * (k / n)
                    for s in er_tables:
                        if s.strictly_inside(mx, my, INSIDE_TOL):
                            hit = s
                            break
                    if hit:
                        break
                if hit is not None:
                    problems.append(
                        f'  边 #{idx} [er-edge] 直线段穿过表 {hit.label()} 内部 '
                        f'(关系线必须正交绕行, 不得横穿表体)\n'
                        f'      d="{d}"')
                    break

    # ── [9] 时序图激活条: 贴 lifeline 的消息端点必须落在激活条上 ──────
    activations = []
    for r in root.iter():
        if local(r.tag) != 'rect' or in_defs(r):
            continue
        if 'activation' not in (r.get('class') or '').split():
            continue
        activations.append((f('x', r), f('y', r), f('width', r), f('height', r)))

    if activations:
        lifelines = [s for s in shapes if s.kind == 'line']
        for idx, cls, d, pts, segs in edges:
            for px, py, which in ((pts[0][0], pts[0][1], '起点'),
                                  (pts[-1][0], pts[-1][1], '终点')):
                # 横向贴近某条 lifeline 的消息端点
                lls = [s for s in lifelines
                       if abs(px - s.x) <= LINE_TOL
                       and s.y - TOL <= py <= s.y + s.h + TOL]
                if not lls:
                    continue
                # 落在节点形状上 = 节点-节点连边, 不走激活条规则
                if any(s.on_boundary(px, py, TOL) for s in shapes if s.kind != 'line'):
                    continue
                ll = min(lls, key=lambda s: abs(px - s.x))
                # 该 lifeline 上画了激活条才强制; 完全没画条的 lifeline 不误伤
                bars = [a for a in activations if abs((a[0] + a[2] / 2) - ll.x) <= 3]
                if not bars:
                    continue
                cover = [a for a in bars if a[1] - ACT_TOL <= py <= a[1] + a[3] + ACT_TOL]
                if not cover:
                    problems.append(
                        f'  边 #{idx} [{cls}] {which} ({px:.0f},{py:.0f}) 贴 lifeline '
                        f'x={ll.x:.0f} 但不在任何激活条内 '
                        f'(条 y 区间: {", ".join(f"{a[1]:.0f}~{a[1]+a[3]:.0f}" for a in bars)})'
                        f' — 激活条没盖住消息\n'
                        f'      d="{d}"')
                    continue
                bx, bw = cover[0][0], cover[0][2]
                if not (abs(px - bx) <= EDGE_TOL or abs(px - (bx + bw)) <= EDGE_TOL):
                    problems.append(
                        f'  边 #{idx} [{cls}] {which} ({px:.0f},{py:.0f}) 贴 lifeline '
                        f'x={ll.x:.0f} 但不在激活条 {bx:.0f}..{bx+bw:.0f} 的边沿'
                        f' (应在条边中点, 不在条中心/内部 — 线从图形内部进出)\n'
                        f'      d="{d}"')

    if problems:
        print(f'✗ 边几何校验失败 · {len(problems)} 处:')
        print('\n'.join(problems))
        return 1

    n_curves = sum(1 for _, _, _, _, segs in edges for s in segs if is_curve_seg(s))
    print(f'✓ 边几何校验通过 ({len(edges)} 边 · {len(shapes)} 节点形状'
          + (f' · {n_curves} 曲线段' if n_curves else '') + ')')
    return 0


def _ancestors(el, parent_map):
    p = parent_map.get(el)
    while p is not None:
        yield p
        p = parent_map.get(p)


if __name__ == '__main__':
    sys.exit(main())
