#!/usr/bin/env python3
"""Rebuild index.html B-zone galleries (02-07) from backup templates."""

from __future__ import annotations

import re
from pathlib import Path

BACKUP_DIR = Path("/Users/dongmaowei/workspace/arch-diagrams 2/templates")
INDEX_PATH = Path(__file__).resolve().parent.parent / "templates" / "index.html"

SECTIONS = [
    ("02-sequence.html", "sequence", "seq"),
    ("03-state-machine.html", "state", "st"),
    ("04-system-architecture.html", "architecture", "arch"),
    ("05-er-diagram.html", "er", "er"),
    ("06-swimlane.html", "swimlane", "slh"),
    ("06-swimlane-vertical.html", "swimlane-v", "slv"),
    ("07-microservice.html", "microservice", "ms"),
]

# Shared gallery chrome + cross-template text styles (from backup templates style block 1)
SHARED_GALLERY_CSS = """
/* ── Shared gallery chrome (all diagram sections) ── */
.gallery-svg .gallery-card-node { cursor: pointer; }
.gallery-svg .gallery-card-node:hover .gallery-card { stroke: var(--clay); stroke-width: 1.8; }
.gallery-svg .gallery-card-node.active { filter: drop-shadow(0 4px 14px rgba(217,119,87,0.30)); }
.gallery-svg .gallery-card-node.active .gallery-card { stroke: var(--clay); stroke-width: 2; }
.gallery-svg text.gallery-title { font-family: var(--serif); font-weight: 500; font-size: 14px; fill: var(--slate); }
.gallery-svg text.gallery-desc  { font-family: var(--mono); font-size: 10px; fill: var(--gray-700); }
.gallery-svg .gallery-tag-uml-bg { fill: color-mix(in oklab, var(--plum), transparent 80%); stroke: var(--plum); stroke-width: 0.8; rx: 8; ry: 8; }
.gallery-svg text.gallery-tag-uml-text { font-family: var(--mono); font-size: 9px; fill: var(--plum); letter-spacing: 0.06em; font-weight: 600; }
.gallery-svg .gallery-tag-ex-bg { fill: color-mix(in oklab, var(--gold), transparent 75%); stroke: var(--gold); stroke-width: 0.8; rx: 8; ry: 8; }
.gallery-svg text.gallery-tag-ex-text { font-family: var(--mono); font-size: 9px; fill: var(--gold); letter-spacing: 0.06em; font-weight: 600; }
.gallery-svg .gallery-tag-ie-bg { fill: color-mix(in oklab, var(--plum), transparent 80%); stroke: var(--plum); stroke-width: 0.8; rx: 8; ry: 8; }
.gallery-svg text.gallery-tag-ie-text { font-family: var(--mono); font-size: 9px; fill: var(--plum); letter-spacing: 0.06em; font-weight: 600; }
.gallery-svg .ribbon-shown-bg { fill: color-mix(in oklab, var(--olive), transparent 80%); stroke: var(--olive); stroke-width: 0.7; rx: 2; ry: 2; }
.gallery-svg text.ribbon-shown-text { font-family: var(--mono); font-size: 8.5px; fill: var(--olive); font-weight: 600; letter-spacing: 0.04em; }
.gallery-svg .ribbon-ref-bg { fill: var(--paper); stroke: var(--gray-300); stroke-width: 0.7; rx: 2; ry: 2; }
.gallery-svg text.ribbon-ref-text { font-family: var(--mono); font-size: 8.5px; fill: var(--gray-500); letter-spacing: 0.04em; }
.gallery-svg text.state-body { font-family: var(--mono); font-size: 10.5px; fill: var(--gray-700); }
.gallery-svg text.state-body.do { fill: var(--olive); }
.gallery-svg text.state-body.defer { fill: var(--plum); }
.gallery-svg text.state-body.internal { fill: var(--teal); }
.gallery-svg .edge-label-bg { fill: var(--paper); stroke: var(--gray-300); stroke-width: 0.6; rx: 3; ry: 3; }
.gallery-svg text.edge-label { font-family: var(--mono); font-size: 10px; fill: var(--gray-700); }
.gallery-svg text.edge-label.plum { fill: var(--plum); }
.gallery-svg text.edge-label.trigger { fill: var(--slate); }
.gallery-svg text.edge-label.guard { fill: var(--olive); font-style: italic; }
.gallery-svg text.edge-label.action { fill: var(--clay); }
.gallery-svg text.t-ann { font-size: 10.5px; fill: var(--gray-700); font-family: var(--mono); }
.gallery-svg text.t-big { font-family: var(--serif); font-size: 18px; fill: var(--slate); font-weight: 500; }
.gallery-svg text.t-stage { font-family: var(--mono); font-size: 10px; letter-spacing: 0.1em; fill: var(--gray-500); text-transform: uppercase; }
.gallery-svg text.t-lane { font-family: var(--serif); font-size: 16px; fill: var(--slate); font-weight: 500; }
.gallery-svg text.attr-name { font-family: var(--mono); font-size: 12px; fill: var(--slate); }
""".strip()

# Shared defs missing from some templates but referenced by edge.return / edge.bidir CSS
EXTRA_MARKERS = """
<marker id="arrow-open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,0 L10,5 L0,10" fill="none" stroke="#87867F" stroke-width="1.4"/></marker>
<marker id="arrow-rev" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="#87867F"/></marker>
""".strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_style_blocks(html: str) -> list[str]:
    return re.findall(r"<style>(.*?)</style>", html, re.DOTALL)


def extract_shared_edge_css(style1: str) -> str:
    rules = []
    for line in style1.splitlines():
        stripped = line.strip()
        if not stripped.startswith(".edge") and not stripped.startswith(".annotation"):
            continue
        if ".edge-label" in stripped:
            continue
        rules.append(line.replace(".edge", ".gallery-svg .edge").replace(".annotation", ".gallery-svg .annotation"))
    return "\n".join(rules)


def extract_diagram_specific_css(style2: str) -> str:
    out = []
    for line in style2.splitlines():
        if ".diagram" not in line:
            continue
        out.append(line.replace(".diagram", ".gallery-svg"))
    return "\n".join(out)


def extract_b_zone_svg(html: str) -> str:
    svg_match = re.search(r'<svg class="diagram"[\s\S]*?</svg>', html)
    if not svg_match:
        raise ValueError("diagram svg not found")
    svg = svg_match.group(0)
    groups = re.findall(r'<g class="node gallery-card-node"[\s\S]*?</g>\s*', svg)
    b_groups: list[str] = []
    for group in groups:
        m = re.search(r'class="gallery-card"[^>]*\by="(\d+)"', group)
        if m and int(m.group(1)) >= 1400:
            b_groups.append(group)
    if not b_groups:
        raise ValueError("No B-zone gallery cards found (y >= 1400)")
    return "".join(b_groups)


def y_offset(body: str) -> int:
    ys = [int(m.group(1)) for m in re.finditer(r'class="gallery-card"[^>]*\by="(\d+)"', body)]
    return min(ys) - 20


def normalized_height(body: str, offset: int) -> int:
    max_y = 0
    for pat in (r'\by="(\d+)"', r'\bcy="(\d+)"', r'\by1="(\d+)"', r'\by2="(\d+)"'):
        for m in re.finditer(pat, body):
            max_y = max(max_y, int(m.group(1)) - offset)
    for m in re.finditer(r'class="gallery-card"[^>]*\by="(\d+)"[^>]*\bheight="(\d+)"', body):
        max_y = max(max_y, int(m.group(1)) - offset + int(m.group(2)))
    return max_y + 40


def wrap_normalized(body: str, offset: int) -> str:
    indented = "\n".join(f"          {line}" if line.strip() else line for line in body.splitlines())
    return f'        <g transform="translate(0 {-offset})">\n{indented}\n        </g>'


def prefix_defs(defs_html: str, prefix: str) -> str:
    return re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', defs_html)


def prefix_marker_urls(css: str, prefix: str) -> str:
    return re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{prefix}-{m.group(1)})", css)


def prefix_inline_markers(svg_body: str, prefix: str) -> str:
    return re.sub(r'url\(#([^)]+)\)', lambda m: f"url(#{prefix}-{m.group(1)})", svg_body)


def extract_defs(html: str) -> str:
    m = re.search(r"<defs>([\s\S]*?)</defs>", html)
    return m.group(1).strip() if m else ""


def fix_svg_u_tags(svg: str) -> str:
    """HTML inline tags inside SVG <text> break rendering; convert to tspan."""
    svg = re.sub(
        r"<u>(.*?)</u>",
        r'<tspan text-decoration="underline">\1</tspan>',
        svg,
        flags=re.DOTALL,
    )
    svg = re.sub(
        r"<b>(.*?)</b>",
        r'<tspan font-weight="600">\1</tspan>',
        svg,
        flags=re.DOTALL,
    )
    svg = re.sub(
        r"<i>(.*?)</i>",
        r'<tspan font-style="italic">\1</tspan>',
        svg,
        flags=re.DOTALL,
    )
    return svg


def ensure_extra_markers(defs_inner: str) -> str:
    if 'id="arrow-open"' in defs_inner and 'id="arrow-rev"' in defs_inner:
        return defs_inner
    if defs_inner:
        return defs_inner + "\n" + EXTRA_MARKERS
    return EXTRA_MARKERS


def inject_row_zebra_var(index_html: str) -> str:
    if re.search(r":root\s*\{[^}]*--row-zebra\s*:", index_html):
        return index_html
    index_html = index_html.replace(
        "  --shadow:   0 1px 2px rgba(42,42,40,0.03), 0 4px 16px rgba(42,42,40,0.04);\n}",
        "  --shadow:   0 1px 2px rgba(42,42,40,0.03), 0 4px 16px rgba(42,42,40,0.04);\n  --row-zebra:#F7F5EE;\n}",
        1,
    )
    return index_html.replace(
        "  --shadow:   0 1px 2px rgba(0,0,0,0.3), 0 4px 16px rgba(0,0,0,0.4);\n}",
        "  --shadow:   0 1px 2px rgba(0,0,0,0.3), 0 4px 16px rgba(0,0,0,0.4);\n  --row-zebra:#1E1D1B;\n}",
        1,
    )


def build_gallery_svg(section_id: str, prefix: str, body: str, offset: int, height: int, defs_inner: str) -> str:
    defs_block = ""
    if defs_inner:
        defs_block = f"        <defs>\n          {prefix_defs(defs_inner, prefix)}\n        </defs>\n"
    wrapped = wrap_normalized(body, offset)
    return (
        f'      <svg class="gallery-svg" id="{section_id}-gallery" '
        f'viewBox="0 0 1080 {height}" xmlns="http://www.w3.org/2000/svg">\n'
        f"{defs_block}"
        f"{wrapped}\n"
        f"      </svg>"
    )


def build_section_css(section_id: str, prefix: str, html: str) -> str:
    styles = extract_style_blocks(html)
    if len(styles) < 2:
        return ""
    shared = extract_shared_edge_css(styles[0])
    specific = extract_diagram_specific_css(styles[1])
    merged = shared + "\n" + specific
    merged = prefix_marker_urls(merged, prefix)
    scoped_lines = []
    for line in merged.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("/*"):
            scoped_lines.append(line)
            continue
        if stripped.startswith(".gallery-svg"):
            scoped_lines.append(f"#{section_id} {line}")
        else:
            scoped_lines.append(line)
    return "\n".join(scoped_lines)


def replace_gallery_frame(index_html: str, section_id: str, new_svg: str) -> str:
    pattern = (
        rf'(<section id="{re.escape(section_id)}"[\s\S]*?<div class="gallery-frame">\s*)'
        rf'<svg class="gallery-svg"[\s\S]*?</svg>'
        rf'(\s*</div>)'
    )
    updated, n = re.subn(pattern, rf"\1{new_svg}\2", index_html, count=1)
    if n != 1:
        raise ValueError(f"Failed to replace gallery for section {section_id}")
    return updated


def replace_overlay_css(index_html: str, css_block: str) -> str:
    start = index_html.find("/* ── Per-template gallery")
    end = index_html.find("/* ── How to draw block")
    if start == -1 or end == -1:
        raise ValueError("Could not locate CSS overlay region")
    return index_html[:start] + css_block + "\n\n" + index_html[end:]


def inject_shared_gallery_css(index_html: str) -> str:
    marker = ".gallery-svg .t-lbl-no { fill: var(--rust); }"
    if marker not in index_html:
        raise ValueError("Could not locate gallery base CSS")
    if "gallery-tag-uml-bg" in index_html.split(marker)[0][-2000:]:
        return index_html
    return index_html.replace(marker, marker + "\n" + SHARED_GALLERY_CSS, 1)


def main() -> None:
    index_html = read_text(INDEX_PATH)
    index_html = inject_row_zebra_var(index_html)
    index_html = inject_shared_gallery_css(index_html)

    css_parts = [
        "/* ── Per-template gallery shape CSS (from backup templates) ── */",
        SHARED_GALLERY_CSS,
        "",
        "/* Edge + shape rules scoped per section (marker ids prefixed) */",
    ]
    gallery_css = []

    for filename, section_id, prefix in SECTIONS:
        html = read_text(BACKUP_DIR / filename)
        body = fix_svg_u_tags(extract_b_zone_svg(html))
        body = prefix_inline_markers(body, prefix)
        offset = y_offset(body)
        height = normalized_height(body, offset)
        defs_inner = ensure_extra_markers(extract_defs(html))
        svg = build_gallery_svg(section_id, prefix, body, offset, height, defs_inner)
        index_html = replace_gallery_frame(index_html, section_id, svg)
        section_css = build_section_css(section_id, prefix, html)
        gallery_css.append(f"/* ── {section_id} ({filename}) ── */\n{section_css}")
        print(f"  ✓ {section_id}: offset={offset} viewBox=0 0 1080 {height}")

    css_parts.extend(gallery_css)
    css_block = "\n\n".join(css_parts)
    index_html = replace_overlay_css(index_html, css_block)
    INDEX_PATH.write_text(index_html, encoding="utf-8")
    print(f"Updated {INDEX_PATH}")


if __name__ == "__main__":
    main()
