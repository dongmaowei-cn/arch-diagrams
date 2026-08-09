#!/usr/bin/env python3
"""Split monolithic templates/index.html into thin index + per-type gallery pages."""

from __future__ import annotations

import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
INDEX_PATH = TEMPLATES_DIR / "index.html"
GALLERY_DIR = TEMPLATES_DIR / "gallery"

SECTIONS = [
    {
        "id": "flowchart",
        "file": "01-flowchart.html",
        "gallery": "01-flowchart.html",
        "num": "01",
        "title": "业务流程图",
        "en": "Flowchart · ISO 5807",
        "template": "01-flowchart.html",
    },
    {
        "id": "sequence",
        "file": "02-sequence.html",
        "gallery": "02-sequence.html",
        "num": "02",
        "title": "时序图",
        "en": "Sequence Diagram · UML 2.5",
        "template": "02-sequence.html",
    },
    {
        "id": "state",
        "file": "03-state-machine.html",
        "gallery": "03-state-machine.html",
        "num": "03",
        "title": "状态机",
        "en": "State Machine · UML 2.5",
        "template": "03-state-machine.html",
    },
    {
        "id": "architecture",
        "file": "04-system-architecture.html",
        "gallery": "04-system-architecture.html",
        "num": "04",
        "title": "系统架构图",
        "en": "System Architecture · C4 derived",
        "template": "04-system-architecture.html",
    },
    {
        "id": "er",
        "file": "05-er-diagram.html",
        "gallery": "05-er-diagram.html",
        "num": "05",
        "title": "ER 图",
        "en": "Entity-Relationship · IE 1.1",
        "template": "05-er-diagram.html",
    },
    {
        "id": "swimlane",
        "file": "06-swimlane.html",
        "gallery": "06-swimlane.html",
        "num": "06H",
        "title": "泳道图 · 水平",
        "en": "Swimlane (Horizontal) · BPMN",
        "template": "06-swimlane.html",
    },
    {
        "id": "swimlane-v",
        "file": "06-swimlane-vertical.html",
        "gallery": "06-swimlane-vertical.html",
        "num": "06V",
        "title": "泳道图 · 垂直",
        "en": "Swimlane (Vertical) · BPMN",
        "template": "06-swimlane-vertical.html",
    },
    {
        "id": "microservice",
        "file": "07-microservice.html",
        "gallery": "07-microservice.html",
        "num": "07",
        "title": "微服务架构图",
        "en": "Microservices · Cloud Native",
        "template": "07-microservice.html",
    },
]

INLINE_SCRIPT = """
// ── Theme toggle ─────────────────────────────────────────────
const themeToggle = document.getElementById('themeToggle');
const themeIconSun = document.getElementById('themeIconSun');
const themeIconMoon = document.getElementById('themeIconMoon');
function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  themeIconSun.style.display  = theme === 'dark' ? 'none' : '';
  themeIconMoon.style.display = theme === 'dark' ? '' : 'none';
  try { localStorage.setItem('edl-theme', theme); } catch(e) {}
}
applyTheme((function(){
  try { return localStorage.getItem('edl-theme') || 'light'; } catch(e) { return 'light'; }
})());
themeToggle.addEventListener('click', () => {
  applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
});

// ── Copy HTML ────────────────────────────────────────────────
const copyHtml = document.getElementById('copyHtml');
copyHtml.addEventListener('click', async () => {
  const original = copyHtml.innerHTML;
  try {
    await navigator.clipboard.writeText('<!doctype html>\\n' + document.documentElement.outerHTML);
    copyHtml.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 8l3.5 3.5L13 5"/></svg>已复制';
    copyHtml.style.color = 'var(--olive)';
    copyHtml.style.borderColor = 'var(--olive)';
    setTimeout(() => {
      copyHtml.innerHTML = original;
      copyHtml.style.color = '';
      copyHtml.style.borderColor = '';
    }, 1800);
  } catch (e) {
    copyHtml.textContent = '复制失败';
    setTimeout(() => { copyHtml.innerHTML = original; }, 1800);
  }
});
""".strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_style(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    if not m:
        raise ValueError("style block not found")
    return m.group(1)


def extract_section(html: str, section_id: str) -> str:
    m = re.search(rf'<section id="{re.escape(section_id)}"[\s\S]*?</section>', html)
    if not m:
        raise ValueError(f"section {section_id} not found")
    return m.group(0)


def unscope_css(css: str, section_id: str) -> str:
    prefix = f"#{section_id} "
    out = []
    for line in css.splitlines():
        if line.startswith(prefix):
            out.append(line[len(prefix) :])
        else:
            out.append(line)
    return "\n".join(out)


def extract_section_css(full_css: str, section_id: str) -> str:
    marker = f"/* ── {section_id} ("
    start = full_css.find(marker)
    if start == -1:
        return ""
    next_markers = [
        full_css.find("/* ── ", start + len(marker)),
        full_css.find("/* ── How to draw block", start),
    ]
    next_markers = [i for i in next_markers if i != -1]
    end = min(next_markers) if next_markers else len(full_css)
    return unscope_css(full_css[start:end].strip(), section_id)


def gallery_base_css(full_css: str) -> str:
    per_start = full_css.find("/* ── Per-template gallery")
    howto_start = full_css.find("/* ── How to draw block")
    if per_start == -1 or howto_start == -1:
        raise ValueError("could not locate CSS regions")
    return (full_css[:per_start].rstrip() + "\n\n" + full_css[howto_start:]).strip()


def index_nav_css(full_css: str) -> str:
    per_start = full_css.find("/* ── Per-template gallery")
    howto_start = full_css.find("/* ── How to draw block")
    if per_start == -1 or howto_start == -1:
        raise ValueError("could not locate CSS regions")
    head = full_css[:per_start]
    tail = full_css[howto_start:]
    # Drop diagram/gallery-specific rules from index shell.
    drop_prefixes = (
        ".diagram-section",
        ".section-header",
        ".section-intro",
        ".template-link",
        ".gallery-block",
        ".gallery-frame",
        ".gallery-svg",
        ".block-label",
        ".block-sub",
        ".howto-block",
        ".howto-steps",
        ".section-footer",
        ".template-link-large",
        ".placeholder-section",
    )
    filtered = []
    for line in head.splitlines():
        stripped = line.strip()
        if stripped.startswith(drop_prefixes):
            continue
        filtered.append(line)
    nav_tail = []
    for line in tail.splitlines():
        if line.strip().startswith((".howto-", ".section-footer", ".template-link-large", ".placeholder-section")):
            continue
        nav_tail.append(line)
    extra = """
.catalog-card-wrap { display: flex; flex-direction: column; background: var(--paper); min-height: 196px; }
.catalog-card-wrap:hover { background: var(--ivory); }
.catalog-card-wrap:hover .card-num { color: var(--clay); }
.catalog-card-wrap .catalog-card { flex: 1; border: none; }
.catalog-card-links { display: flex; gap: 10px; padding: 0 24px 18px; font-family: var(--mono); font-size: 10px; letter-spacing: 0.04em; }
.catalog-card-links a { color: var(--gray-700); text-decoration: none; border-bottom: 1px dotted var(--gray-500); }
.catalog-card-links a:hover { color: var(--clay); border-color: var(--clay); }
.catalog-card-links .sep { color: var(--gray-300); }
""".strip()
    return "\n".join(filtered).rstrip() + "\n\n" + extra + "\n\n" + "\n".join(nav_tail).strip()


def fix_relative_links(section_html: str) -> str:
    section_html = re.sub(
        r'href="(0[1-7][^"]*\.html)"',
        r'href="../\1"',
        section_html,
    )
    return section_html


def build_gallery_page(meta: dict, section_html: str, css: str) -> str:
    section_html = fix_relative_links(section_html)
    section_css = extract_section_css(css, meta["id"])
    page_css = gallery_base_css(css)
    if section_css:
        page_css += f"\n\n/* ── {meta['id']} specific ── */\n{section_css}"
    crumb = f"{meta['num']} · {meta['title']}"
    return f"""<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta['title']} · 元素图鉴与画法 · Engineering Diagram Library</title>
<style>
{page_css}
</style>
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <div class="crumb">
      <a href="../index.html">Engineering Diagram Library</a>
      <span class="sep">/</span>
      <span style="color:var(--slate)">{crumb}</span>
    </div>
    <div class="toolbar">
      <button class="pill-btn" id="copyHtml" title="复制本页 HTML 源码">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="5" width="9" height="9" rx="1"/><path d="M3 11V3a1 1 0 011-1h7"/></svg>HTML
      </button>
      <button class="icon-btn" id="themeToggle" title="切换主题">
        <svg id="themeIconSun" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14"><circle cx="8" cy="8" r="3"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.5 3.5l1.4 1.4M11.1 11.1l1.4 1.4M3.5 12.5l1.4-1.4M11.1 4.9l1.4-1.4"/></svg>
        <svg id="themeIconMoon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14" style="display:none"><path d="M13 9.5A6 6 0 116.5 3a5 5 0 006.5 6.5z"/></svg>
      </button>
    </div>
  </div>
</header>

{section_html}

<footer class="site-footer">
  <span>Engineering Diagram Library · {meta['num']} · {meta['title']}</span>
  <span><a href="../index.html">← 返回总览</a> · <a href="../{meta['template']}">→ 看完整范本</a></span>
</footer>

<script>
{INLINE_SCRIPT}
</script>
</body>
</html>
"""


def build_index_shell(html: str, css: str) -> str:
    hero_match = re.search(r"<section class=\"hero\">[\s\S]*?</section>", html)
    catalog_match = re.search(r"<section class=\"catalog\">[\s\S]*?</section>", html)
    if not hero_match or not catalog_match:
        raise ValueError("hero/catalog not found")

    cards = []
    for meta in SECTIONS:
        old_href = f'href="#{meta["id"]}"'
        card_pattern = rf'<a {re.escape(old_href)} class="catalog-card">([\s\S]*?)</a>'
        m = re.search(card_pattern, catalog_match.group(0))
        if not m:
            raise ValueError(f"catalog card for {meta['id']} not found")
        card_body = m.group(1)
        cards.append(
            f"""    <div class="catalog-card-wrap">
      <a href="gallery/{meta['gallery']}" class="catalog-card">{card_body}</a>
      <p class="catalog-card-links">
        <a href="gallery/{meta['gallery']}">图鉴 · 画法</a>
        <span class="sep">·</span>
        <a href="{meta['template']}">范本 →</a>
      </p>
    </div>"""
        )

    catalog = (
        '  <p class="catalog-title">图谱总览 · Catalog</p>\n'
        '  <div class="catalog-grid">\n    '
        + "\n    ".join(cards)
        + "\n  </div>"
    )

    return f"""<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Engineering Diagram Library · 10 张图,讲清后端工程的画法</title>
<style>
{index_nav_css(css)}
</style>
</head>
<body>

<header class="topbar">
  <div class="topbar-inner">
    <div class="crumb">
      <span>Engineering Diagram Library</span>
      <span class="sep">/</span>
      <span style="color:var(--slate)">总览</span>
    </div>
    <div class="toolbar">
      <button class="pill-btn" id="copyHtml" title="复制本页 HTML 源码">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5" y="5" width="9" height="9" rx="1"/><path d="M3 11V3a1 1 0 011-1h7"/></svg>HTML
      </button>
      <button class="icon-btn" id="themeToggle" title="切换主题">
        <svg id="themeIconSun" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14"><circle cx="8" cy="8" r="3"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.5 3.5l1.4 1.4M11.1 11.1l1.4 1.4M3.5 12.5l1.4-1.4M11.1 4.9l1.4-1.4"/></svg>
        <svg id="themeIconMoon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" width="14" height="14" style="display:none"><path d="M13 9.5A6 6 0 116.5 3a5 5 0 006.5 6.5z"/></svg>
      </button>
    </div>
  </div>
</header>

{hero_match.group(0)}

<section class="catalog">
{catalog}
</section>

<footer class="site-footer">
  <span>Engineering Diagram Library · v2.0 · 10 张图 · 真实业务场景</span>
  <span><a href="01-flowchart.html">↗ 01 范本</a> · <a href="gallery/01-flowchart.html">↗ 01 图鉴</a></span>
</footer>

<script>
{INLINE_SCRIPT}
</script>
</body>
</html>
"""


def main() -> None:
    html = read_text(INDEX_PATH)
    css = extract_style(html)
    GALLERY_DIR.mkdir(exist_ok=True)

    for meta in SECTIONS:
        section_html = extract_section(html, meta["id"])
        page = build_gallery_page(meta, section_html, css)
        out = GALLERY_DIR / meta["gallery"]
        out.write_text(page, encoding="utf-8")
        print(f"  ✓ gallery/{meta['gallery']}")

    INDEX_PATH.write_text(build_index_shell(html, css), encoding="utf-8")
    print(f"Updated {INDEX_PATH}")


if __name__ == "__main__":
    main()
