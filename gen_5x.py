#!/usr/bin/env python3
"""
Regenerate all 5.x section HTML files with proper LaTeX math formatting,
side notes, and new sections 5.4 and 5.5.
Run from: /Users/skimransabuj/jabeen's/MAT116/
"""

import os, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Extract CSS from existing 5.1 file ───────────────────────────────────────
with open(os.path.join(BASE_DIR, '5.1', 'section_5_1.html'), encoding='utf-8') as _f:
    _TMPL = _f.read()

_css_m = re.search(r'<style>(.*?)</style>', _TMPL, re.DOTALL)
BASE_CSS = _css_m.group(1)

SIDENOTE_CSS = """
      /* ── Side Notes ── */
      .section-sidenotes {
        margin: 0 0 2.25rem;
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
      }
      .sidenotes-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.2rem;
      }
      .sidenote {
        background: #fffde7;
        border-left: 4px solid #f9a825;
        border-radius: 0 6px 6px 0;
        padding: 0.75rem 1.1rem;
      }
      .sidenote-header {
        font-weight: bold;
        color: #e65100;
        font-size: 0.80rem;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.4rem;
      }
      .sidenote-body {
        font-size: 0.94rem;
        line-height: 1.9;
        color: #1a1a2e;
        white-space: pre-wrap;
      }
"""

BASE_CSS = BASE_CSS + SIDENOTE_CSS

# ── HTML Head ─────────────────────────────────────────────────────────────────
HTML_HEAD = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <script>
      window.MathJax = {{
        tex: {{
          inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],
          displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],
          processEscapes: true,
          tags: "ams",
        }},
        options: {{
          skipHtmlTags: ["script", "noscript", "style", "textarea", "pre"],
        }},
      }};
    </script>
    <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <script src="https://cdn.plot.ly/plotly-basic-2.35.2.min.js" charset="utf-8"></script>
    <style>{css}</style>
  </head>"""

# ── JS Footer ─────────────────────────────────────────────────────────────────
JS_FOOTER = """
    <script>
      (function () {
        var body = document.body,
          sidebar = document.getElementById("sidebar"),
          overlay = document.getElementById("overlay"),
          btn = document.getElementById("menuBtn");
        function openNav() {
          body.classList.add("nav-open");
          btn.setAttribute("aria-expanded", "true");
        }
        function closeNav() {
          body.classList.remove("nav-open");
          btn.setAttribute("aria-expanded", "false");
        }
        btn.addEventListener("click", function () {
          body.classList.contains("nav-open") ? closeNav() : openNav();
        });
        overlay.addEventListener("click", closeNav);
        sidebar.querySelectorAll("a[data-target]").forEach(function (a) {
          a.addEventListener("click", function () {
            if (window.innerWidth <= 768) closeNav();
          });
        });
        document.addEventListener("keydown", function (e) {
          if (e.key === "Escape") closeNav();
        });
        var navLinks = {};
        sidebar.querySelectorAll("a[data-target]").forEach(function (a) {
          navLinks[a.dataset.target] = a;
        });
        var io = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              var link = navLinks[entry.target.id];
              if (!link) return;
              if (entry.isIntersecting) {
                Object.values(navLinks).forEach(function (l) { l.classList.remove("active"); });
                link.classList.add("active");
                link.scrollIntoView({ block: "nearest", behavior: "smooth" });
              }
            });
          },
          { rootMargin: "-10% 0px -80% 0px", threshold: 0 }
        );
        document.querySelectorAll(".problem[id]").forEach(function (el) { io.observe(el); });
      })();
    </script>"""

# ── Helper builders ───────────────────────────────────────────────────────────
ALL_CHAPTERS = [
    ('4.1', 'Polynomial Functions',   '../4.1/section_4_1.html'),
    ('4.2', 'Rational Asymptotes',    '../4.2/section_4_2.html'),
    ('4.3', 'Rational Graphs',        '../4.3/section_4_3.html'),
    ('4.4', 'Inequalities',           '../4.4/section_4_4.html'),
    ('5.1', 'Composite Functions',    '../5.1/section_5_1.html'),
    ('5.2', 'Inverse Functions',      '../5.2/section_5_2.html'),
    ('5.3', 'Exponential Functions',  '../5.3/section_5_3.html'),
    ('5.4', 'Logarithmic Functions',  '../5.4/section_5_4.html'),
    ('5.5', 'Log Properties',         '../5.5/section_5_5.html'),
    ('5.6', 'Log & Exp Equations',    '../5.6/section_5_6.html'),
]


def build_sidebar(active_label, groups):
    items_html = ''
    items_html += '          <li>\n'
    items_html += '            <a href="../index.html"><span class="nav-num">Home</span>MAT116 Index</a>\n'
    items_html += '          </li>\n'
    for lbl, name, href in ALL_CHAPTERS:
        active = ' class="active"' if lbl == active_label else ''
        items_html += f'          <li>\n            <a href="{href}"{active}><span class="nav-num">{lbl}</span>{name}</a>\n          </li>\n'

    groups_html = ''
    for g in groups:
        groups_html += f'      <div class="nav-group">\n        <div class="nav-group-title">{g["title"]}</div>\n        <ul>\n'
        for n in g['probs']:
            groups_html += f'          <li><a href="#prob-{n}" data-target="prob-{n}"><span class="nav-num">{n}</span>Problem {n}</a></li>\n'
        groups_html += '        </ul>\n      </div>\n'

    return f"""    <nav class="sidebar" id="sidebar" aria-label="Problem navigation">
      <div class="sidebar-brand">
        <div class="brand-title">MAT 116 Solutions</div>
        <div class="brand-sub">Sullivan Precalculus 10th Ed &middot; Section {active_label}</div>
      </div>
      <div class="nav-group">
        <div class="nav-group-title">Chapters</div>
        <ul>
{items_html}        </ul>
      </div>
{groups_html}    </nav>"""


def build_sidenotes(sidenotes):
    if not sidenotes:
        return ''
    inner = ''
    for sn in sidenotes:
        inner += f'        <div class="sidenote">\n          <div class="sidenote-header">{sn["header"]}</div>\n          <div class="sidenote-body">{sn["body"]}</div>\n        </div>\n'
    return f'        <div class="section-sidenotes">\n          <div class="sidenotes-title">&#9733; Key Notes for this Section</div>\n{inner}        </div>\n'


def build_problem(p, is_last=False):
    steps_html = ''
    for step in p['steps']:
        steps_html += f"""            <div class="step">
              <div class="step-title">{step['title']}</div>
              <div class="step-body">{step['body']}</div>
            </div>\n"""

    ans_secs = ''
    for step in p['steps']:
        ans_secs += f"""              <div class="answer-section">
                <div class="answer-sec-label">{step['title']}</div>
                <div class="answer-sec-body">{step['body']}</div>
              </div>\n"""
    ans_secs += f"""              <div class="answer-section">
                <div class="answer-sec-label">Final Answer</div>
                <div class="answer-sec-body">{p['answer']}</div>
              </div>\n"""

    hr = '' if is_last else '\n        <hr />'
    return f"""
        <div class="problem" id="prob-{p['num']}">
          <h2>Problem {p['num']}</h2>
          <span class="badge">{p['badge']}</span>
          <div class="given-label">Given</div>
          <div class="given-box">{p['given']}</div>
          <div class="steps">
{steps_html}          </div>
          <div class="answer-box">
            <div class="answer-box-header">Exam Answer</div>
            <div class="answer-sections">
{ans_secs}            </div>
          </div>
          <a class="back-top" href="#top">&#8593; Back to top</a>
        </div>{hr}"""


def build_page(cfg):
    """cfg keys: section_label, section_name, folder, fname, groups, sidenotes, problems"""
    label = cfg['section_label']
    title_full = f"Section {label} - {cfg['section_name']} (Assigned Problems)"

    chapter_links = ''
    for lbl, _, href in ALL_CHAPTERS:
        active = ' active' if lbl == label else ''
        chapter_links += f'            <a class="chapter-link{active}" href="{href}">{lbl}</a>\n'
    chapter_links += '            <a class="chapter-link" href="../index.html">Home</a>\n'

    sidebar_html = build_sidebar(label, cfg['groups'])
    sidenotes_html = build_sidenotes(cfg.get('sidenotes', []))

    all_probs = cfg['problems']
    probs_html = ''
    for i, p in enumerate(all_probs):
        probs_html += build_problem(p, is_last=(i == len(all_probs) - 1))

    head = HTML_HEAD.format(title=title_full, css=BASE_CSS)
    return f"""{head}
  <body>
    <div class="topbar" id="topbar">
      <button class="menu-btn" id="menuBtn" aria-label="Toggle navigation" aria-expanded="false" aria-controls="sidebar">
        <span></span><span></span><span></span>
      </button>
      <span class="topbar-title">MAT 116 &mdash; Section {label}</span>
    </div>
    <div class="overlay" id="overlay" aria-hidden="true"></div>
{sidebar_html}
    <div class="main">
      <div class="container">
        <header class="page-header" id="top">
          <h1>{title_full}</h1>
          <p class="subtitle">MAT 116 &mdash; Precalculus &nbsp;|&nbsp; Sullivan <em>Precalculus</em> 10th Edition &nbsp;|&nbsp; Section {label}</p>
          <div class="header-nav-label">Jump to Section</div>
          <div class="chapter-nav">
{chapter_links}          </div>
        </header>
{sidenotes_html}{probs_html}
      </div>
    </div>
{JS_FOOTER}
  </body>
</html>"""


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5.1 — Composite Functions
# ════════════════════════════════════════════════════════════════════════════════
PROBS_5_1 = [
    # ── Problems 17-20: Composite Values ──────────────────────────────────────
    {
        'num': 17, 'badge': 'Composite Function Values',
        'given': '$f(x) = 2x+1$ and $g(x) = 3x$. Find (a) $(f \\circ g)(4)$, (b) $(g \\circ f)(2)$, (c) $(f \\circ f)(1)$, (d) $(g \\circ g)(0)$.',
        'steps': [{'title': 'Compute each composite value',
                   'body': ('(a) $(f \\circ g)(4) = f(g(4)) = f(12) = 2(12)+1 = 25$\n'
                            '(b) $(g \\circ f)(2) = g(f(2)) = g(5) = 3(5) = 15$\n'
                            '(c) $(f \\circ f)(1) = f(f(1)) = f(3) = 2(3)+1 = 7$\n'
                            '(d) $(g \\circ g)(0) = g(g(0)) = g(0) = 0$')}],
        'answer': '(a) $25$,&ensp;(b) $15$,&ensp;(c) $7$,&ensp;(d) $0$',
    },
    {
        'num': 18, 'badge': 'Composite Function Values',
        'given': '$f(x) = \\sqrt{x}$ and $g(x) = 2x$. Find (a) $(f \\circ g)(4)$, (b) $(g \\circ f)(2)$, (c) $(f \\circ f)(1)$, (d) $(g \\circ g)(0)$.',
        'steps': [{'title': 'Compute each composite value',
                   'body': ('(a) $(f \\circ g)(4) = f(g(4)) = f(8) = \\sqrt{8} = 2\\sqrt{2}$\n'
                            '(b) $(g \\circ f)(2) = g(\\sqrt{2}) = 2\\sqrt{2}$\n'
                            '(c) $(f \\circ f)(1) = f(1) = \\sqrt{1} = 1$\n'
                            '(d) $(g \\circ g)(0) = g(0) = 0$')}],
        'answer': '(a) $2\\sqrt{2}$,&ensp;(b) $2\\sqrt{2}$,&ensp;(c) $1$,&ensp;(d) $0$',
    },
    {
        'num': 19, 'badge': 'Composite Function Values',
        'given': '$f(x) = |x-2|$ and $g(x) = \\dfrac{3}{x^2+2}$. Find (a) $(f \\circ g)(4)$, (b) $(g \\circ f)(2)$, (c) $(f \\circ f)(1)$, (d) $(g \\circ g)(0)$.',
        'steps': [
            {'title': 'Find intermediate values of g and f',
             'body': ('$g(4) = \\dfrac{3}{16+2} = \\dfrac{3}{18} = \\dfrac{1}{6}$\n'
                      '$f(2) = |2-2| = 0$\n'
                      '$f(1) = |1-2| = 1$\n'
                      '$g(0) = \\dfrac{3}{0+2} = \\dfrac{3}{2}$')},
            {'title': 'Compute each composite value',
             'body': ('(a) $(f \\circ g)(4) = f\\!\\left(\\dfrac{1}{6}\\right) = \\left|\\dfrac{1}{6}-2\\right| = \\dfrac{11}{6}$\n'
                      '(b) $(g \\circ f)(2) = g(0) = \\dfrac{3}{2}$\n'
                      '(c) $(f \\circ f)(1) = f(1) = |1-2| = 1$\n'
                      '(d) $(g \\circ g)(0) = g\\!\\left(\\dfrac{3}{2}\\right) = \\dfrac{3}{\\tfrac{9}{4}+2} = \\dfrac{3}{\\tfrac{17}{4}} = \\dfrac{12}{17}$')},
        ],
        'answer': '(a) $\\dfrac{11}{6}$,&ensp;(b) $\\dfrac{3}{2}$,&ensp;(c) $1$,&ensp;(d) $\\dfrac{12}{17}$',
    },
    {
        'num': 20, 'badge': 'Composite Function Values',
        'given': '$f(x) = |x|$ and $g(x) = \\dfrac{1}{x^2+1}$. Find (a) $(f \\circ g)(4)$, (b) $(g \\circ f)(2)$, (c) $(f \\circ f)(1)$, (d) $(g \\circ g)(0)$.',
        'steps': [{'title': 'Compute each composite value',
                   'body': ('(a) $(f \\circ g)(4) = f\\!\\left(\\dfrac{1}{17}\\right) = \\dfrac{1}{17}$\n'
                            '(b) $(g \\circ f)(2) = g(2) = \\dfrac{1}{5}$\n'
                            '(c) $(f \\circ f)(1) = f(1) = 1$\n'
                            '(d) $(g \\circ g)(0) = g(1) = \\dfrac{1}{2}$')}],
        'answer': '(a) $\\dfrac{1}{17}$,&ensp;(b) $\\dfrac{1}{5}$,&ensp;(c) $1$,&ensp;(d) $\\dfrac{1}{2}$',
    },
    # ── Problems 31-38: Composite Formulas ────────────────────────────────────
    {
        'num': 31, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = \\dfrac{x}{x+3}$, $g(x) = \\dfrac{2}{x}$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Find f ∘ g and its domain',
             'body': ('$f \\circ g = f\\!\\left(\\dfrac{2}{x}\\right) = \\dfrac{2/x}{2/x+3} = \\dfrac{2}{2+3x}$\n'
                      'Domain: $x \\neq 0$ and $x \\neq -\\dfrac{2}{3}$')},
            {'title': 'Find g ∘ f and its domain',
             'body': ('$g \\circ f = g\\!\\left(\\dfrac{x}{x+3}\\right) = \\dfrac{2(x+3)}{x}$\n'
                      'Domain: $x \\neq 0$ and $x \\neq -3$')},
            {'title': 'Find f ∘ f and its domain',
             'body': ('$f \\circ f = f\\!\\left(\\dfrac{x}{x+3}\\right) = \\dfrac{x}{4x+9}$\n'
                      'Domain: $x \\neq -3$ and $x \\neq -\\dfrac{9}{4}$')},
            {'title': 'Find g ∘ g and its domain',
             'body': ('$g \\circ g = g\\!\\left(\\dfrac{2}{x}\\right) = x$\n'
                      'Domain: $x \\neq 0$')},
        ],
        'answer': ('$f \\circ g = \\dfrac{2}{3x+2}$, Dom: $x \\neq 0,\\,-\\tfrac{2}{3}$;  '
                   '$g \\circ f = \\dfrac{2(x+3)}{x}$, Dom: $x \\neq 0,\\,-3$;  '
                   '$f \\circ f = \\dfrac{x}{4x+9}$, Dom: $x \\neq -3,\\,-\\tfrac{9}{4}$;  '
                   '$g \\circ g = x$, Dom: $x \\neq 0$'),
    },
    {
        'num': 32, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = \\dfrac{x}{x-1}$, $g(x) = \\dfrac{-4}{x}$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Find f ∘ g and its domain',
             'body': ('$f \\circ g = f\\!\\left(\\dfrac{-4}{x}\\right) = \\dfrac{-4/x}{-4/x-1} = \\dfrac{4}{x+4}$\n'
                      'Domain: $x \\neq 0$, $x \\neq -4$')},
            {'title': 'Find g ∘ f and its domain',
             'body': ('$g \\circ f = g\\!\\left(\\dfrac{x}{x-1}\\right) = \\dfrac{-4(x-1)}{x}$\n'
                      'Domain: $x \\neq 0$, $x \\neq 1$')},
            {'title': 'Find f ∘ f and its domain',
             'body': ('$f \\circ f = f\\!\\left(\\dfrac{x}{x-1}\\right) = x$\n'
                      'Domain: $x \\neq 1$')},
            {'title': 'Find g ∘ g and its domain',
             'body': ('$g \\circ g = g\\!\\left(\\dfrac{-4}{x}\\right) = x$\n'
                      'Domain: $x \\neq 0$')},
        ],
        'answer': ('$f \\circ g = \\dfrac{4}{x+4}$, Dom: $x \\neq 0,\\,-4$;  '
                   '$g \\circ f = \\dfrac{-4(x-1)}{x}$, Dom: $x \\neq 0,\\,1$;  '
                   '$f \\circ f = x$, Dom: $x \\neq 1$;  '
                   '$g \\circ g = x$, Dom: $x \\neq 0$'),
    },
    {
        'num': 33, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = 2x-2$, $g(x) = 1-2x$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Compute all four compositions',
             'body': ('$f \\circ g = f(1-2x) = 2(1-2x)-2 = -4x$\n'
                      '$g \\circ f = g(2x-2) = 1-2(2x-2) = 5-4x$\n'
                      '$f \\circ f = f(2x-2) = 2(2x-2)-2 = 4x-6$\n'
                      '$g \\circ g = g(1-2x) = 1-2(1-2x) = 4x-1$')},
            {'title': 'State domains',
             'body': 'All four compositions have domain $(-\\infty,\\,\\infty)$ (all real numbers).'},
        ],
        'answer': ('$f \\circ g = -4x$; $g \\circ f = 5-4x$; $f \\circ f = 4x-6$; $g \\circ g = 4x-1$. '
                   'All domains: $(-\\infty,\\,\\infty)$.'),
    },
    {
        'num': 34, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = 2x$, $g(x) = 2x+3$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Compute all four compositions',
             'body': ('$f \\circ g = f(2x+3) = 2(2x+3) = 4x+6$\n'
                      '$g \\circ f = g(2x) = 2(2x)+3 = 4x+3$\n'
                      '$f \\circ f = f(2x) = 4x$\n'
                      '$g \\circ g = g(2x+3) = 2(2x+3)+3 = 4x+9$')},
            {'title': 'State domains',
             'body': 'All four compositions have domain $(-\\infty,\\,\\infty)$.'},
        ],
        'answer': ('$f \\circ g = 4x+6$; $g \\circ f = 4x+3$; $f \\circ f = 4x$; $g \\circ g = 4x+9$. '
                   'All domains: $(-\\infty,\\,\\infty)$.'),
    },
    {
        'num': 35, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = x^2+4$, $g(x) = 2x-2$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Compute all four compositions',
             'body': ('$f \\circ g = f(2x-2) = (2x-2)^2+4 = 4x^2-8x+8$\n'
                      '$g \\circ f = g(x^2+4) = 2(x^2+4)-2 = 2x^2+6$\n'
                      '$f \\circ f = f(x^2+4) = (x^2+4)^2+4 = x^4+8x^2+20$\n'
                      '$g \\circ g = g(2x-2) = 2(2x-2)-2 = 4x-6$')},
            {'title': 'State domains',
             'body': 'All four compositions have domain $(-\\infty,\\,\\infty)$.'},
        ],
        'answer': ('$f \\circ g = 4x^2-8x+8$; $g \\circ f = 2x^2+6$; '
                   '$f \\circ f = x^4+8x^2+20$; $g \\circ g = 4x-6$. All domains: $(-\\infty,\\,\\infty)$.'),
    },
    {
        'num': 36, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = x^2+1$, $g(x) = 2x-1$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Compute all four compositions',
             'body': ('$f \\circ g = f(2x-1) = (2x-1)^2+1 = 4x^2-4x+2$\n'
                      '$g \\circ f = g(x^2+1) = 2(x^2+1)-1 = 2x^2+1$\n'
                      '$f \\circ f = f(x^2+1) = (x^2+1)^2+1 = x^4+2x^2+2$\n'
                      '$g \\circ g = g(2x-1) = 2(2x-1)-1 = 4x-3$')},
            {'title': 'State domains',
             'body': 'All four compositions have domain $(-\\infty,\\,\\infty)$.'},
        ],
        'answer': ('$f \\circ g = 4x^2-4x+2$; $g \\circ f = 2x^2+1$; '
                   '$f \\circ f = x^4+2x^2+2$; $g \\circ g = 4x-3$. All domains: $(-\\infty,\\,\\infty)$.'),
    },
    {
        'num': 37, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = \\dfrac{2x-1}{x-2}$, $g(x) = \\dfrac{x+4}{2x-5}$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Find f ∘ g and its domain',
             'body': ('Numerator: $2\\cdot\\dfrac{x+4}{2x-5}-1 = \\dfrac{2(x+4)-(2x-5)}{2x-5} = \\dfrac{13}{2x-5}$\n'
                      'Denominator: $\\dfrac{x+4}{2x-5}-2 = \\dfrac{x+4-2(2x-5)}{2x-5} = \\dfrac{-3x+14}{2x-5}$\n'
                      '$f \\circ g = \\dfrac{13}{-3x+14} = \\dfrac{-13}{3x-14}$\n'
                      'Domain: $x \\neq \\dfrac{5}{2}$, $x \\neq \\dfrac{14}{3}$')},
            {'title': 'Find g ∘ f and its domain',
             'body': ('$g \\circ f = g\\!\\left(\\dfrac{2x-1}{x-2}\\right)$\n'
                      'Num: $\\dfrac{2x-1}{x-2}+4 = \\dfrac{6x-9}{x-2}$\n'
                      'Den: $2\\cdot\\dfrac{2x-1}{x-2}-5 = \\dfrac{-x+8}{x-2}$\n'
                      '$g \\circ f = \\dfrac{3(2x-3)}{8-x}$\n'
                      'Domain: $x \\neq 2$, $x \\neq 8$')},
            {'title': 'Find f ∘ f and g ∘ g',
             'body': ('$f \\circ f = x$, Domain: $x \\neq 2$\n'
                      '$g \\circ g = \\dfrac{9x-16}{-8x+33}$, Domain: $x \\neq \\dfrac{5}{2}$, $x \\neq \\dfrac{33}{8}$')},
        ],
        'answer': ('$f \\circ g = \\dfrac{-13}{3x-14}$, Dom: $x \\neq \\tfrac{5}{2},\\,\\tfrac{14}{3}$;  '
                   '$g \\circ f = \\dfrac{3(2x-3)}{8-x}$, Dom: $x \\neq 2,\\,8$;  '
                   '$f \\circ f = x$, Dom: $x \\neq 2$;  '
                   '$g \\circ g = \\dfrac{9x-16}{33-8x}$, Dom: $x \\neq \\tfrac{5}{2},\\,\\tfrac{33}{8}$'),
    },
    {
        'num': 38, 'badge': 'Composite Formulas and Domains',
        'given': '$f(x) = \\dfrac{x-5}{x+1}$, $g(x) = \\dfrac{x+2}{x-3}$. Find $f \\circ g$, $g \\circ f$, $f \\circ f$, $g \\circ g$ and state each domain.',
        'steps': [
            {'title': 'Find f ∘ g and its domain',
             'body': ('Num: $\\dfrac{x+2}{x-3}-5 = \\dfrac{-4x+17}{x-3}$\n'
                      'Den: $\\dfrac{x+2}{x-3}+1 = \\dfrac{2x-1}{x-3}$\n'
                      '$f \\circ g = \\dfrac{-4x+17}{2x-1} = \\dfrac{-(4x-17)}{2x-1}$\n'
                      'Domain: $x \\neq 3$, $x \\neq \\dfrac{1}{2}$')},
            {'title': 'Find g ∘ f and its domain',
             'body': ('Num: $\\dfrac{x-5}{x+1}+2 = \\dfrac{3(x-1)}{x+1}$\n'
                      'Den: $\\dfrac{x-5}{x+1}-3 = \\dfrac{-2(x+4)}{x+1}$\n'
                      '$g \\circ f = \\dfrac{-3(x-1)}{2(x+4)}$\n'
                      'Domain: $x \\neq -1$, $x \\neq -4$')},
            {'title': 'Find f ∘ f and g ∘ g',
             'body': ('$f \\circ f: $ Num $= -4x-10$, Den $= 2x-4$\n'
                      '$f \\circ f = \\dfrac{-(2x+5)}{x-2}$, Domain: $x \\neq -1$, $x \\neq 2$\n\n'
                      '$g \\circ g: $ Num $= 3x-4$, Den $= -2x+11$\n'
                      '$g \\circ g = \\dfrac{3x-4}{11-2x}$, Domain: $x \\neq 3$, $x \\neq \\dfrac{11}{2}$')},
        ],
        'answer': ('$f \\circ g = \\dfrac{-(4x-17)}{2x-1}$, Dom: $x \\neq 3,\\,\\tfrac{1}{2}$;  '
                   '$g \\circ f = \\dfrac{-3(x-1)}{2(x+4)}$, Dom: $x \\neq -1,\\,-4$;  '
                   '$f \\circ f = \\dfrac{-(2x+5)}{x-2}$, Dom: $x \\neq -1,\\,2$;  '
                   '$g \\circ g = \\dfrac{3x-4}{11-2x}$, Dom: $x \\neq 3,\\,\\tfrac{11}{2}$'),
    },
]

CFG_5_1 = {
    'section_label': '5.1',
    'section_name': 'Composite Functions',
    'folder': '5.1',
    'fname': 'section_5_1.html',
    'groups': [
        {'title': 'Composite Function Values', 'probs': [17, 18, 19, 20]},
        {'title': 'Composite Formulas and Domains', 'probs': [31, 32, 33, 34, 35, 36, 37, 38]},
    ],
    'sidenotes': [
        {'header': 'Definition — Composite Function',
         'body': ('$(f \\circ g)(x) = f(g(x))$\n'
                  'The output of $g$ becomes the input of $f$.\n'
                  'Domain of $f \\circ g$: all $x$ in Dom($g$) such that $g(x)$ is in Dom($f$).')},
        {'header': 'Procedure — Finding f ∘ g',
         'body': ('1. Replace every $x$ in $f(x)$ with $g(x)$ and simplify.\n'
                  '2. Find domain restrictions:\n'
                  '   &bull; Exclude values not in Dom($g$).\n'
                  '   &bull; Exclude values where $g(x)$ is not in Dom($f$).\n'
                  '3. Note: $f \\circ g \\neq g \\circ f$ in general (composition is not commutative).')},
    ],
    'problems': PROBS_5_1,
}


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5.2 — One-to-One and Inverse Functions
# ════════════════════════════════════════════════════════════════════════════════
PROBS_5_2 = [
    # ── Problems 39-44: Verify Inverse Pairs ──────────────────────────────────
    {
        'num': 39, 'badge': 'Verify Inverse Pair',
        'given': 'Verify that $f(x) = x^3 - 8$ and $g(x) = \\sqrt[3]{x+8}$ are inverses.',
        'steps': [
            {'title': 'Check f(g(x)) = x',
             'body': '$f(g(x)) = \\left(\\sqrt[3]{x+8}\\right)^3 - 8 = (x+8) - 8 = x$ ✓'},
            {'title': 'Check g(f(x)) = x',
             'body': '$g(f(x)) = \\sqrt[3]{(x^3-8)+8} = \\sqrt[3]{x^3} = x$ ✓'},
        ],
        'answer': 'Since both compositions equal $x$, $f$ and $g$ are inverse functions on $(-\\infty,\\infty)$.',
    },
    {
        'num': 40, 'badge': 'Verify Inverse Pair',
        'given': 'Verify that $f(x) = \\sqrt{x-2}$ ($x \\geq 2$) and $g(x) = x^2+2$ are inverses.',
        'steps': [
            {'title': 'Check f(g(x)) = x for x ≥ 0',
             'body': '$f(g(x)) = \\sqrt{(x^2+2)-2} = \\sqrt{x^2} = x$ for $x \\geq 0$ ✓'},
            {'title': 'Check g(f(x)) = x for x ≥ 2',
             'body': '$g(f(x)) = \\left(\\sqrt{x-2}\\right)^2 + 2 = (x-2)+2 = x$ for $x \\geq 2$ ✓'},
        ],
        'answer': ('They are inverse functions with Dom($f$) $= [2,\\infty)$, '
                   'Dom($g$) $= [0,\\infty)$.'),
    },
    {
        'num': 41, 'badge': 'Verify Inverse Pair',
        'given': 'Verify that $f(x) = x$ and $g(x) = x$ are inverses.',
        'steps': [
            {'title': 'Compose',
             'body': '$f(g(x)) = f(x) = x$ and $g(f(x)) = g(x) = x$ ✓'},
        ],
        'answer': 'The identity function $f(x)=x$ is its own inverse on $(-\\infty,\\infty)$.',
    },
    {
        'num': 42, 'badge': 'Verify Inverse Pair',
        'given': 'Verify that $f(x) = \\dfrac{1}{x}$ and $g(x) = \\dfrac{1}{x}$ are inverses.',
        'steps': [
            {'title': 'Compose',
             'body': ('$f(g(x)) = \\dfrac{1}{1/x} = x$ ✓\n'
                      '$g(f(x)) = \\dfrac{1}{1/x} = x$ ✓\n'
                      'Restriction: $x \\neq 0$ for both functions.')},
        ],
        'answer': '$f(x) = \\dfrac{1}{x}$ is its own inverse; Dom: $\\{x \\mid x \\neq 0\\}$.',
    },
    {
        'num': 43, 'badge': 'Verify Inverse Pair',
        'given': 'Verify that $f(x) = \\dfrac{x-5}{2x+3}$ and $g(x) = \\dfrac{3x+5}{1-2x}$ are inverses.',
        'steps': [
            {'title': 'Check f(g(x)) = x',
             'body': ('Num: $\\dfrac{3x+5}{1-2x}-5 = \\dfrac{3x+5-5(1-2x)}{1-2x} = \\dfrac{13x}{1-2x}$\n'
                      'Den: $2\\cdot\\dfrac{3x+5}{1-2x}+3 = \\dfrac{6x+10+3(1-2x)}{1-2x} = \\dfrac{13}{1-2x}$\n'
                      '$f(g(x)) = \\dfrac{13x}{13} = x$ ✓')},
            {'title': 'State domain restrictions',
             'body': 'Dom($f$): $x \\neq -\\dfrac{3}{2}$; Dom($g$): $x \\neq \\dfrac{1}{2}$'},
        ],
        'answer': 'Inverse pair verified. Dom($f$): $x \\neq -\\tfrac{3}{2}$; Dom($g$): $x \\neq \\tfrac{1}{2}$.',
    },
    {
        'num': 44, 'badge': 'Verify Inverse Pair',
        'given': 'Verify that $f(x) = \\dfrac{2x+3}{x+4}$ and $g(x) = \\dfrac{4x-3}{2-x}$ are inverses.',
        'steps': [
            {'title': 'Check f(g(x)) = x',
             'body': ('Num: $2\\cdot\\dfrac{4x-3}{2-x}+3 = \\dfrac{2(4x-3)+3(2-x)}{2-x} = \\dfrac{5x}{2-x}$\n'
                      'Den: $\\dfrac{4x-3}{2-x}+4 = \\dfrac{4x-3+4(2-x)}{2-x} = \\dfrac{5}{2-x}$\n'
                      '$f(g(x)) = x$ ✓')},
            {'title': 'State domain restrictions',
             'body': 'Dom($f$): $x \\neq -4$; Dom($g$): $x \\neq 2$'},
        ],
        'answer': 'Inverse pair verified. Dom($f$): $x \\neq -4$; Dom($g$): $x \\neq 2$.',
    },
    # ── Problems 66-74: Find Inverse Functions ────────────────────────────────
    {
        'num': 66, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{3x}{x+2}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = 3x/(x+2) for x',
             'body': ('$y(x+2) = 3x \\Rightarrow xy + 2y = 3x \\Rightarrow x(y-3) = -2y \\Rightarrow x = \\dfrac{2y}{3-y}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{2x}{3-x}$\n'
                      'Dom($f$): $x \\neq -2$; Range($f$): $y \\neq 3$\n'
                      'Dom($f^{-1}$): $x \\neq 3$; Range($f^{-1}$): $y \\neq -2$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{2x}{3-x}$; Dom($f^{-1}$): $\\{x \\mid x \\neq 3\\}$.',
    },
    {
        'num': 67, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{2x}{3x-1}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = 2x/(3x-1) for x',
             'body': ('$y(3x-1) = 2x \\Rightarrow 3xy - y = 2x \\Rightarrow x(3y-2) = y \\Rightarrow x = \\dfrac{y}{3y-2}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{x}{3x-2}$\n'
                      'Dom($f$): $x \\neq \\dfrac{1}{3}$; Range($f$): $y \\neq \\dfrac{2}{3}$\n'
                      'Dom($f^{-1}$): $x \\neq \\dfrac{2}{3}$; Range($f^{-1}$): $y \\neq \\dfrac{1}{3}$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{x}{3x-2}$; Dom($f^{-1}$): $\\{x \\mid x \\neq \\tfrac{2}{3}\\}$.',
    },
    {
        'num': 68, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{-3x+1}{x}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = (-3x+1)/x for x',
             'body': ('$yx = -3x+1 \\Rightarrow yx+3x = 1 \\Rightarrow x(y+3) = 1 \\Rightarrow x = \\dfrac{1}{y+3}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{1}{x+3}$\n'
                      'Dom($f$): $x \\neq 0$; Range($f$): $y \\neq -3$\n'
                      'Dom($f^{-1}$): $x \\neq -3$; Range($f^{-1}$): $y \\neq 0$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{1}{x+3}$; Dom($f^{-1}$): $\\{x \\mid x \\neq -3\\}$.',
    },
    {
        'num': 69, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{2x-3}{x+4}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = (2x-3)/(x+4) for x',
             'body': ('$y(x+4) = 2x-3 \\Rightarrow xy+4y = 2x-3 \\Rightarrow x(y-2) = -(4y+3) \\Rightarrow x = \\dfrac{4y+3}{2-y}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{4x+3}{2-x}$\n'
                      'Dom($f$): $x \\neq -4$; Range($f$): $y \\neq 2$\n'
                      'Dom($f^{-1}$): $x \\neq 2$; Range($f^{-1}$): $y \\neq -4$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{4x+3}{2-x}$; Dom($f^{-1}$): $\\{x \\mid x \\neq 2\\}$.',
    },
    {
        'num': 70, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{3x+4}{2x-3}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = (3x+4)/(2x-3) for x',
             'body': ('$y(2x-3) = 3x+4 \\Rightarrow 2xy-3y = 3x+4 \\Rightarrow x(2y-3) = 3y+4 \\Rightarrow x = \\dfrac{3y+4}{2y-3}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{3x+4}{2x-3}$\n'
                      'Note: $f$ is its own inverse!\n'
                      'Dom($f$) = Dom($f^{-1}$): $x \\neq \\dfrac{3}{2}$; Range: $y \\neq \\dfrac{3}{2}$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{3x+4}{2x-3} = f(x)$ (self-inverse); Dom: $x \\neq \\dfrac{3}{2}$.',
    },
    {
        'num': 71, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{-3x-4}{x-2}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = (-3x-4)/(x-2) for x',
             'body': ('$y(x-2) = -3x-4 \\Rightarrow xy-2y = -3x-4 \\Rightarrow x(y+3) = 2y-4 \\Rightarrow x = \\dfrac{2(y-2)}{y+3}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{2(x-2)}{x+3}$\n'
                      'Dom($f$): $x \\neq 2$; Range($f$): $y \\neq -3$\n'
                      'Dom($f^{-1}$): $x \\neq -3$; Range($f^{-1}$): $y \\neq 2$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{2(x-2)}{x+3}$; Dom($f^{-1}$): $\\{x \\mid x \\neq -3\\}$.',
    },
    {
        'num': 72, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{2x+3}{x+2}$. State domain and range of $f$ and $f^{-1}$.',
        'steps': [
            {'title': 'Solve y = (2x+3)/(x+2) for x',
             'body': ('$y(x+2) = 2x+3 \\Rightarrow xy+2y = 2x+3 \\Rightarrow x(y-2) = 3-2y \\Rightarrow x = \\dfrac{3-2y}{y-2}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{3-2x}{x-2}$\n'
                      'Dom($f$): $x \\neq -2$; Range($f$): $y \\neq 2$\n'
                      'Dom($f^{-1}$): $x \\neq 2$; Range($f^{-1}$): $y \\neq -2$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{3-2x}{x-2}$; Dom($f^{-1}$): $\\{x \\mid x \\neq 2\\}$.',
    },
    {
        'num': 73, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{x^2+3}{3x^2}$, $x &gt; 0$. State domain and range.',
        'steps': [
            {'title': 'Rewrite and solve for x',
             'body': ('$y = \\dfrac{1}{3} + \\dfrac{1}{x^2} \\Rightarrow y - \\dfrac{1}{3} = \\dfrac{1}{x^2} \\Rightarrow x^2 = \\dfrac{1}{y-\\frac{1}{3}} = \\dfrac{3}{3y-1}$\n'
                      'Since $x &gt; 0$: $x = \\sqrt{\\dfrac{3}{3y-1}}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\sqrt{\\dfrac{3}{3x-1}}$\n'
                      'Dom($f$) $= (0,\\infty)$; Range($f$) $= \\left(\\dfrac{1}{3},\\infty\\right)$\n'
                      'Dom($f^{-1}$) $= \\left(\\dfrac{1}{3},\\infty\\right)$; Range($f^{-1}$) $= (0,\\infty)$')},
        ],
        'answer': '$f^{-1}(x) = \\sqrt{\\dfrac{3}{3x-1}}$; Dom($f^{-1}$): $x &gt; \\dfrac{1}{3}$.',
    },
    {
        'num': 74, 'badge': 'Find Inverse Function',
        'given': 'Find $f^{-1}$ for $f(x) = \\dfrac{x^2-4}{2x^2}$, $x &gt; 0$. State domain and range.',
        'steps': [
            {'title': 'Rewrite and solve for x',
             'body': ('$y = \\dfrac{1}{2} - \\dfrac{2}{x^2} \\Rightarrow \\dfrac{1}{2}-y = \\dfrac{2}{x^2} \\Rightarrow x^2 = \\dfrac{4}{1-2y}$\n'
                      'Since $x &gt; 0$: $x = \\dfrac{2}{\\sqrt{1-2y}}$')},
            {'title': 'Write inverse and state sets',
             'body': ('$f^{-1}(x) = \\dfrac{2}{\\sqrt{1-2x}}$\n'
                      'Dom($f$) $= (0,\\infty)$; Range($f$) $= \\left(-\\infty,\\dfrac{1}{2}\\right)$\n'
                      'Dom($f^{-1}$) $= \\left(-\\infty,\\dfrac{1}{2}\\right)$; Range($f^{-1}$) $= (0,\\infty)$')},
        ],
        'answer': '$f^{-1}(x) = \\dfrac{2}{\\sqrt{1-2x}}$; Dom($f^{-1}$): $x &lt; \\dfrac{1}{2}$.',
    },
]

CFG_5_2 = {
    'section_label': '5.2',
    'section_name': 'One-to-One and Inverse Functions',
    'folder': '5.2',
    'fname': 'section_5_2.html',
    'groups': [
        {'title': 'Verify Inverse Pair', 'probs': [39, 40, 41, 42, 43, 44]},
        {'title': 'Find Inverse Function', 'probs': [66, 67, 68, 69, 70, 71, 72, 73, 74]},
    ],
    'sidenotes': [
        {'header': 'One-to-One Function',
         'body': ('A function $f$ is one-to-one if $f(a) = f(b)$ implies $a = b$.\n'
                  'Graphically: passes the Horizontal Line Test.\n'
                  'Only one-to-one functions have an inverse $f^{-1}$.')},
        {'header': 'Inverse Function Property',
         'body': ('$(f^{-1} \\circ f)(x) = x$ for all $x$ in Dom($f$)\n'
                  '$(f \\circ f^{-1})(x) = x$ for all $x$ in Dom($f^{-1}$)\n'
                  'Dom($f^{-1}$) = Range($f$) and Range($f^{-1}$) = Dom($f$).')},
        {'header': 'Procedure — Finding f⁻¹',
         'body': ('1. Write $y = f(x)$.\n'
                  '2. Swap $x$ and $y$: solve the equation $x = f(y)$ for $y$.\n'
                  '3. Write $f^{-1}(x) = $ (result).\n'
                  '4. State domain restrictions.')},
    ],
    'problems': PROBS_5_2,
}


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5.3 — Exponential Functions
# ════════════════════════════════════════════════════════════════════════════════
def exp_transform_prob(num, fx, base, transform_desc, domain, rang, ha):
    return {
        'num': num, 'badge': 'Exponential Transformations',
        'given': f'$f(x) = {fx}$. Determine transformations, domain, range, and horizontal asymptote.',
        'steps': [
            {'title': 'Identify the transformation',
             'body': transform_desc},
            {'title': 'State characteristics',
             'body': (f'Domain: $(-\\infty,\\,\\infty)$\n'
                      f'Range: ${rang}$\n'
                      f'Horizontal asymptote: $y = {ha}$')},
        ],
        'answer': f'Range: ${rang}$, HA: $y={ha}$, Domain: $(-\\infty,\\infty)$.',
    }


def exp_eq_prob(num, fx_given, steps_list, answer_str):
    return {
        'num': num, 'badge': 'Exponential Equation',
        'given': f'Solve $\\;{fx_given}$.',
        'steps': steps_list,
        'answer': answer_str,
    }


PROBS_5_3 = [
    exp_transform_prob(43, '2^x + 1', '2^x',
        'Start from $y = 2^x$ and shift up $1$ unit.',
        '(-\\infty,\\infty)', '(1,\\infty)', '1'),
    exp_transform_prob(44, '3^x - 2', '3^x',
        'Start from $y = 3^x$ and shift down $2$ units.',
        '(-\\infty,\\infty)', '(-2,\\infty)', '-2'),
    exp_transform_prob(45, '2^{x+2}', '2^x',
        'Shift $y = 2^x$ left $2$ units (replace $x$ with $x+2$).',
        '(-\\infty,\\infty)', '(0,\\infty)', '0'),
    exp_transform_prob(46, '3^{x-1}', '3^x',
        'Shift $y = 3^x$ right $1$ unit.',
        '(-\\infty,\\infty)', '(0,\\infty)', '0'),
    exp_transform_prob(47, '4\\!\\left(\\tfrac{1}{3}\\right)^x', '(1/3)^x',
        'Vertical stretch of $y = \\left(\\tfrac{1}{3}\\right)^x$ by factor $4$. Exponential decay.',
        '(-\\infty,\\infty)', '(0,\\infty)', '0'),
    exp_transform_prob(48, '3\\!\\left(\\tfrac{1}{2}\\right)^x', '(1/2)^x',
        'Vertical stretch of $y = \\left(\\tfrac{1}{2}\\right)^x$ by factor $3$. Exponential decay.',
        '(-\\infty,\\infty)', '(0,\\infty)', '0'),
    exp_transform_prob(49, '-3^x + 1', '3^x',
        'Reflect $y = 3^x$ across the $x$-axis to get $y = -3^x$, then shift up $1$.',
        '(-\\infty,\\infty)', '(-\\infty,1)', '1'),
    exp_transform_prob(50, '3^{-x} - 2', '3^x',
        'Reflect $y = 3^x$ across the $y$-axis (same as $y = (1/3)^x$), then shift down $2$.',
        '(-\\infty,\\infty)', '(-2,\\infty)', '-2'),
    exp_transform_prob(51, '1 - 2^{x+3}', '2^x',
        'Shift left $3$: $y = 2^{x+3}$; reflect across $x$-axis: $y = -2^{x+3}$; shift up $1$.',
        '(-\\infty,\\infty)', '(-\\infty,1)', '1'),
    # Exponential equations
    exp_eq_prob(75, '3^{x^2-7} = 27^{2x}',
        [
            {'title': 'Write both sides as powers of 3',
             'body': '$27^{2x} = (3^3)^{2x} = 3^{6x}$\nSo $3^{x^2-7} = 3^{6x} \\Rightarrow x^2-7 = 6x$'},
            {'title': 'Solve the quadratic',
             'body': '$x^2 - 6x - 7 = 0 \\Rightarrow (x-7)(x+1) = 0$'},
        ],
        '$x = 7$ or $x = -1$'),
    exp_eq_prob(76, '5^{x^2+8} = 125^{2x}',
        [
            {'title': 'Write both sides as powers of 5',
             'body': '$125^{2x} = (5^3)^{2x} = 5^{6x}$\nSo $x^2+8 = 6x$'},
            {'title': 'Solve the quadratic',
             'body': '$x^2 - 6x + 8 = 0 \\Rightarrow (x-2)(x-4) = 0$'},
        ],
        '$x = 2$ or $x = 4$'),
    exp_eq_prob(77, '9^{2x} \\cdot 27^{x^2} = 3^{-1}',
        [
            {'title': 'Express all terms in base 3',
             'body': ('$9^{2x} = 3^{4x}$, $\\;27^{x^2} = 3^{3x^2}$\n'
                      'So $3^{3x^2+4x} = 3^{-1} \\Rightarrow 3x^2+4x = -1$')},
            {'title': 'Solve the quadratic',
             'body': '$3x^2+4x+1 = 0 \\Rightarrow (3x+1)(x+1) = 0$'},
        ],
        '$x = -\\dfrac{1}{3}$ or $x = -1$'),
    exp_eq_prob(78, '4^x \\cdot 2^{x^2} = 16^2',
        [
            {'title': 'Express all terms in base 2',
             'body': '$4^x = 2^{2x}$, $\\;16^2 = 2^8$\nSo $2^{x^2+2x} = 2^8 \\Rightarrow x^2+2x = 8$'},
            {'title': 'Solve the quadratic',
             'body': '$x^2+2x-8 = 0 \\Rightarrow (x+4)(x-2) = 0$'},
        ],
        '$x = -4$ or $x = 2$'),
    exp_eq_prob(79, 'e^{3x} = e^{2-x}',
        [
            {'title': 'Equate exponents (same base $e$)',
             'body': '$3x = 2-x$'},
            {'title': 'Solve for x',
             'body': '$4x = 2 \\Rightarrow x = \\dfrac{1}{2}$'},
        ],
        '$x = \\dfrac{1}{2}$'),
    exp_eq_prob(80, 'e^x = e^{3x+8}',
        [
            {'title': 'Equate exponents',
             'body': '$x = 3x+8$'},
            {'title': 'Solve for x',
             'body': '$-2x = 8 \\Rightarrow x = -4$'},
        ],
        '$x = -4$'),
    exp_eq_prob(81, 'e^{x^2} = e^{3x} \\cdot e^{-2}',
        [
            {'title': 'Combine exponents on right side',
             'body': '$e^{x^2} = e^{3x-2} \\Rightarrow x^2 = 3x-2$'},
            {'title': 'Solve the quadratic',
             'body': '$x^2-3x+2 = 0 \\Rightarrow (x-1)(x-2) = 0$'},
        ],
        '$x = 1$ or $x = 2$'),
    exp_eq_prob(82, '(e^4)^{2x} \\cdot e^x = e^{12}',
        [
            {'title': 'Simplify left side',
             'body': '$(e^4)^{2x} = e^{8x}$, so $e^{8x} \\cdot e^x = e^{9x} = e^{12}$'},
            {'title': 'Solve for x',
             'body': '$9x = 12 \\Rightarrow x = \\dfrac{4}{3}$'},
        ],
        '$x = \\dfrac{4}{3}$'),
]

CFG_5_3 = {
    'section_label': '5.3',
    'section_name': 'Exponential Functions',
    'folder': '5.3',
    'fname': 'section_5_3.html',
    'groups': [
        {'title': 'Exponential Transformations', 'probs': list(range(43, 52))},
        {'title': 'Exponential Equations', 'probs': list(range(75, 83))},
    ],
    'sidenotes': [
        {'header': 'Exponential Function',
         'body': ('$f(x) = a^x$, where $a &gt; 0$, $a \\neq 1$.\n'
                  'Domain: $(-\\infty,\\infty)$; Range: $(0,\\infty)$; Horizontal asymptote: $y=0$.\n'
                  'If $a &gt; 1$: increasing (growth). If $0 &lt; a &lt; 1$: decreasing (decay).')},
        {'header': 'Key Transformation Rules',
         'body': ('&bull; $f(x)+k$: shift up/down $k$ units (HA shifts to $y=k$)\n'
                  '&bull; $f(x+h)$: shift left ($h&gt;0$) or right ($h&lt;0$)\n'
                  '&bull; $-f(x)$: reflect over $x$-axis; range becomes $(-\\infty,0)$\n'
                  '&bull; $f(-x)$: reflect over $y$-axis ($a^{-x} = (1/a)^x$)\n'
                  '&bull; $cf(x)$: vertical stretch/compression by factor $c$')},
        {'header': 'One-to-One Property',
         'body': ('$a^u = a^v \\Leftrightarrow u = v$ (for $a &gt; 0$, $a \\neq 1$).\n'
                  'This property is the key to solving exponential equations\n'
                  'by writing both sides with the same base.')},
    ],
    'problems': PROBS_5_3,
}


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5.4 — Logarithmic Functions (NEW)
# ════════════════════════════════════════════════════════════════════════════════
def log_transform_prob(num, fx, base_str, transform_desc, domain_str, rang, va):
    return {
        'num': num, 'badge': 'Graph Logarithmic Function',
        'given': f'$f(x) = {fx}$. Determine transformations, domain, range, and vertical asymptote.',
        'steps': [
            {'title': 'Identify the transformation',
             'body': transform_desc},
            {'title': 'State characteristics',
             'body': (f'Domain: ${domain_str}$\n'
                      f'Range: $(-\\infty,\\,\\infty)$\n'
                      f'Vertical asymptote: $x = {va}$')},
        ],
        'answer': f'Domain: ${domain_str}$, VA: $x={va}$, Range: $(-\\infty,\\infty)$.',
    }


def log_domain_prob(num, fx_str, solution_steps, domain_str):
    return {
        'num': num, 'badge': 'Domain of Logarithmic Function',
        'given': f'Find the domain of $f(x) = {fx_str}$.',
        'steps': solution_steps,
        'answer': f'Domain: ${domain_str}$',
    }


PROBS_5_4 = [
    log_transform_prob(49, '\\log_3(x-2)', 'log_3', 
        'Shift $y = \\log_3 x$ right $2$ units (replace $x$ with $x-2$).',
        '(2,\\infty)', '(-\\infty,\\infty)', '2'),
    log_transform_prob(50, '\\log_2(x+1)', 'log_2',
        'Shift $y = \\log_2 x$ left $1$ unit.',
        '(-1,\\infty)', '(-\\infty,\\infty)', '-1'),
    log_transform_prob(51, '-\\log_2 x', 'log_2',
        'Reflect $y = \\log_2 x$ across the $x$-axis.',
        '(0,\\infty)', '(-\\infty,\\infty)', '0'),
    log_transform_prob(52, '\\log_3(-x)', 'log_3',
        'Reflect $y = \\log_3 x$ across the $y$-axis (replace $x$ with $-x$).',
        '(-\\infty,0)', '(-\\infty,\\infty)', '0'),
    log_transform_prob(53, '\\log_2 x + 3', 'log_2',
        'Shift $y = \\log_2 x$ up $3$ units.',
        '(0,\\infty)', '(-\\infty,\\infty)', '0'),
    log_transform_prob(54, '\\log_3 x - 2', 'log_3',
        'Shift $y = \\log_3 x$ down $2$ units.',
        '(0,\\infty)', '(-\\infty,\\infty)', '0'),
    log_transform_prob(55, '2\\log_2(x+1)', 'log_2',
        'Shift left $1$, then vertical stretch by factor $2$.',
        '(-1,\\infty)', '(-\\infty,\\infty)', '-1'),
    log_transform_prob(56, '1 - \\log(x+2)', 'log',
        'Shift left $2$: $\\log(x+2)$; reflect across $x$-axis: $-\\log(x+2)$; shift up $1$.',
        '(-2,\\infty)', '(-\\infty,\\infty)', '-2'),
    log_domain_prob(87, '\\ln(x-3)',
        [{'title': 'Argument must be positive',
          'body': '$x - 3 &gt; 0 \\Rightarrow x &gt; 3$'}],
        '(3,\\infty)'),
    log_domain_prob(88, '\\log_2(x+1)',
        [{'title': 'Argument must be positive',
          'body': '$x + 1 &gt; 0 \\Rightarrow x &gt; -1$'}],
        '(-1,\\infty)'),
    log_domain_prob(89, '\\log_5(x^2-1)',
        [{'title': 'Solve x² - 1 > 0',
          'body': ('$x^2 - 1 &gt; 0 \\Rightarrow (x-1)(x+1) &gt; 0$\n'
                   'Sign chart: positive when $x &lt; -1$ or $x &gt; 1$')}],
        '(-\\infty,-1)\\cup(1,\\infty)'),
    log_domain_prob(90, '\\ln(1-x)',
        [{'title': 'Argument must be positive',
          'body': '$1 - x &gt; 0 \\Rightarrow x &lt; 1$'}],
        '(-\\infty,1)'),
    log_domain_prob(91, '\\log\\!\\left(\\dfrac{x+1}{x-2}\\right)',
        [{'title': 'Argument (fraction) must be positive',
          'body': ('$\\dfrac{x+1}{x-2} &gt; 0$\n'
                   'Both positive: $x &gt; 2$; both negative: $x &lt; -1$')}],
        '(-\\infty,-1)\\cup(2,\\infty)'),
    log_domain_prob(92, '\\log\\!\\left(\\dfrac{x}{x-1}\\right)',
        [{'title': 'Fraction must be positive',
          'body': ('$\\dfrac{x}{x-1} &gt; 0$\n'
                   'Both positive: $x &gt; 1$; both negative: $x &lt; 0$')}],
        '(-\\infty,0)\\cup(1,\\infty)'),
    log_domain_prob(93, '\\sqrt{\\log x}',
        [{'title': 'Need log x ≥ 0',
          'body': '$\\log x \\geq 0 \\Rightarrow x \\geq 10^0 = 1$'}],
        '[1,\\infty)'),
    log_domain_prob(94, '\\dfrac{1}{\\log x}',
        [{'title': 'Need x > 0 and log x ≠ 0',
          'body': '$x &gt; 0$ and $\\log x \\neq 0 \\Rightarrow x \\neq 1$'}],
        '(0,1)\\cup(1,\\infty)'),
]

CFG_5_4 = {
    'section_label': '5.4',
    'section_name': 'Logarithmic Functions',
    'folder': '5.4',
    'fname': 'section_5_4.html',
    'groups': [
        {'title': 'Graph Logarithmic Function', 'probs': list(range(49, 57))},
        {'title': 'Domain of Logarithmic Function', 'probs': list(range(87, 95))},
    ],
    'sidenotes': [
        {'header': 'Logarithmic Function Definition',
         'body': ('$y = \\log_a x \\iff a^y = x$ &nbsp; ($a &gt; 0$, $a \\neq 1$, $x &gt; 0$)\n'
                  'Common log: $\\log x = \\log_{10} x$\n'
                  'Natural log: $\\ln x = \\log_e x$')},
        {'header': 'Properties of y = log_a x',
         'body': ('&bull; Domain: $(0,\\infty)$; Range: $(-\\infty,\\infty)$\n'
                  '&bull; Vertical asymptote: $x = 0$; passes through $(1,0)$ and $(a,1)$\n'
                  '&bull; If $a &gt; 1$: increasing; if $0 &lt; a &lt; 1$: decreasing\n'
                  '&bull; $\\log_a(a^x) = x$ and $a^{\\log_a x} = x$')},
        {'header': 'Key Identities',
         'body': ('$\\log_a 1 = 0$ &nbsp; $\\log_a a = 1$ &nbsp; $\\ln e = 1$\n'
                  '$\\log_a a^r = r$ &nbsp; $a^{\\log_a x} = x$\n'
                  'Log and exponential are inverse functions: $f(x) = a^x$ and $f^{-1}(x) = \\log_a x$')},
    ],
    'problems': PROBS_5_4,
}


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5.5 — Properties of Logarithms (NEW)
# ════════════════════════════════════════════════════════════════════════════════
def expand_prob(num, expr, expansion_steps, answer_str):
    return {
        'num': num, 'badge': 'Expand Logarithm',
        'given': f'Write $\\;{expr}\\;$ as a sum/difference of simpler logarithms.',
        'steps': expansion_steps,
        'answer': answer_str,
    }


def condense_prob(num, expr, cond_steps, answer_str):
    return {
        'num': num, 'badge': 'Condense to Single Logarithm',
        'given': f'Write $\\;{expr}\\;$ as a single logarithm.',
        'steps': cond_steps,
        'answer': answer_str,
    }


PROBS_5_5 = [
    # ── Expand Problems 29-36 ──────────────────────────────────────────────────
    expand_prob(29, '\\log_3(x^2 y)',
        [{'title': 'Apply Product and Power Rules',
          'body': ('$\\log_3(x^2 y) = \\log_3(x^2) + \\log_3 y$\n'
                   '$= 2\\log_3 x + \\log_3 y$')}],
        '$2\\log_3 x + \\log_3 y$'),
    expand_prob(30, '\\log_2(x^3 y^2)',
        [{'title': 'Apply Product and Power Rules',
          'body': ('$\\log_2(x^3 y^2) = \\log_2 x^3 + \\log_2 y^2$\n'
                   '$= 3\\log_2 x + 2\\log_2 y$')}],
        '$3\\log_2 x + 2\\log_2 y$'),
    expand_prob(31, '\\log\\!\\left(\\dfrac{x^3}{y^2}\\right)',
        [{'title': 'Apply Quotient and Power Rules',
          'body': ('$\\log\\!\\left(\\dfrac{x^3}{y^2}\\right) = \\log x^3 - \\log y^2$\n'
                   '$= 3\\log x - 2\\log y$')}],
        '$3\\log x - 2\\log y$'),
    expand_prob(32, '\\ln\\!\\left(\\dfrac{x^2\\sqrt{y}}{z}\\right)',
        [{'title': 'Apply all three log rules',
          'body': ('$= \\ln x^2 + \\ln y^{1/2} - \\ln z$\n'
                   '$= 2\\ln x + \\dfrac{1}{2}\\ln y - \\ln z$')}],
        '$2\\ln x + \\dfrac{1}{2}\\ln y - \\ln z$'),
    expand_prob(33, '\\log_2\\!\\left(\\dfrac{\\sqrt{x}}{y^3}\\right)',
        [{'title': 'Apply Quotient and Power Rules',
          'body': ('$= \\log_2 x^{1/2} - \\log_2 y^3$\n'
                   '$= \\dfrac{1}{2}\\log_2 x - 3\\log_2 y$')}],
        '$\\dfrac{1}{2}\\log_2 x - 3\\log_2 y$'),
    expand_prob(34, '\\ln\\!\\left(x^2\\sqrt{x+1}\\right)',
        [{'title': 'Apply Product and Power Rules',
          'body': ('$= \\ln x^2 + \\ln(x+1)^{1/2}$\n'
                   '$= 2\\ln x + \\dfrac{1}{2}\\ln(x+1)$')}],
        '$2\\ln x + \\dfrac{1}{2}\\ln(x+1)$'),
    expand_prob(35, '\\log_3\\!\\left(\\dfrac{x^2 y}{\\sqrt[3]{z}}\\right)',
        [{'title': 'Apply all three log rules',
          'body': ('$= \\log_3 x^2 + \\log_3 y - \\log_3 z^{1/3}$\n'
                   '$= 2\\log_3 x + \\log_3 y - \\dfrac{1}{3}\\log_3 z$')}],
        '$2\\log_3 x + \\log_3 y - \\dfrac{1}{3}\\log_3 z$'),
    expand_prob(36, '\\log\\!\\left(\\dfrac{x^3 y}{\\sqrt{z}}\\right)',
        [{'title': 'Apply all three log rules',
          'body': ('$= \\log x^3 + \\log y - \\log z^{1/2}$\n'
                   '$= 3\\log x + \\log y - \\dfrac{1}{2}\\log z$')}],
        '$3\\log x + \\log y - \\dfrac{1}{2}\\log z$'),
    # ── Condense Problems 55-62 ───────────────────────────────────────────────
    condense_prob(55, '3\\log_2 x + 2\\log_2 y',
        [{'title': 'Apply Power Rule, then Product Rule',
          'body': ('$= \\log_2 x^3 + \\log_2 y^2$\n'
                   '$= \\log_2(x^3 y^2)$')}],
        '$\\log_2(x^3 y^2)$'),
    condense_prob(56, '\\log_3(x^2-1) - \\log_3(x-1)',
        [{'title': 'Apply Quotient Rule and factor',
          'body': ('$= \\log_3\\!\\left(\\dfrac{x^2-1}{x-1}\\right) = \\log_3\\!\\left(\\dfrac{(x-1)(x+1)}{x-1}\\right)$\n'
                   '$= \\log_3(x+1)$ &nbsp; (for $x &gt; 1$)')}],
        '$\\log_3(x+1)$'),
    condense_prob(57, '2\\log x + \\dfrac{1}{2}\\log(x+1)',
        [{'title': 'Apply Power Rule, then Product Rule',
          'body': ('$= \\log x^2 + \\log(x+1)^{1/2}$\n'
                   '$= \\log\\!\\left(x^2\\sqrt{x+1}\\right)$')}],
        '$\\log\\!\\left(x^2\\sqrt{x+1}\\right)$'),
    condense_prob(58, '\\ln x + \\ln(x-1) - 2\\ln(x+1)',
        [{'title': 'Combine using all three rules',
          'body': ('$= \\ln[x(x-1)] - \\ln(x+1)^2$\n'
                   '$= \\ln\\!\\left(\\dfrac{x(x-1)}{(x+1)^2}\\right)$')}],
        '$\\ln\\!\\left(\\dfrac{x(x-1)}{(x+1)^2}\\right)$'),
    condense_prob(59, '\\log_2 x + \\log_2(x+1) - 2\\log_2(x-1)',
        [{'title': 'Apply Power and Quotient Rules',
          'body': ('$= \\log_2[x(x+1)] - \\log_2(x-1)^2$\n'
                   '$= \\log_2\\!\\left(\\dfrac{x(x+1)}{(x-1)^2}\\right)$')}],
        '$\\log_2\\!\\left(\\dfrac{x(x+1)}{(x-1)^2}\\right)$'),
    condense_prob(60, '2\\ln(x+1) - 3\\ln(x-1)',
        [{'title': 'Apply Power Rule, then Quotient Rule',
          'body': ('$= \\ln(x+1)^2 - \\ln(x-1)^3$\n'
                   '$= \\ln\\!\\left(\\dfrac{(x+1)^2}{(x-1)^3}\\right)$')}],
        '$\\ln\\!\\left(\\dfrac{(x+1)^2}{(x-1)^3}\\right)$'),
    condense_prob(61, '\\dfrac{1}{2}\\log_3 x - 2\\log_3(x+1)',
        [{'title': 'Apply Power Rule, then Quotient Rule',
          'body': ('$= \\log_3 x^{1/2} - \\log_3(x+1)^2$\n'
                   '$= \\log_3\\!\\left(\\dfrac{\\sqrt{x}}{(x+1)^2}\\right)$')}],
        '$\\log_3\\!\\left(\\dfrac{\\sqrt{x}}{(x+1)^2}\\right)$'),
    condense_prob(62, '3\\ln x + \\dfrac{1}{2}\\ln(x^2+1) - 2\\ln(x-1)',
        [{'title': 'Apply all three rules',
          'body': ('$= \\ln x^3 + \\ln\\sqrt{x^2+1} - \\ln(x-1)^2$\n'
                   '$= \\ln\\!\\left(\\dfrac{x^3\\sqrt{x^2+1}}{(x-1)^2}\\right)$')}],
        '$\\ln\\!\\left(\\dfrac{x^3\\sqrt{x^2+1}}{(x-1)^2}\\right)$'),
]

CFG_5_5 = {
    'section_label': '5.5',
    'section_name': 'Properties of Logarithms',
    'folder': '5.5',
    'fname': 'section_5_5.html',
    'groups': [
        {'title': 'Expand Logarithm', 'probs': list(range(29, 37))},
        {'title': 'Condense to Single Logarithm', 'probs': list(range(55, 63))},
    ],
    'sidenotes': [
        {'header': 'Three Main Log Rules',
         'body': ('Product Rule: $\\log_a(MN) = \\log_a M + \\log_a N$\n'
                  'Quotient Rule: $\\log_a\\!\\left(\\dfrac{M}{N}\\right) = \\log_a M - \\log_a N$\n'
                  'Power Rule: $\\log_a(M^r) = r \\log_a M$')},
        {'header': 'Change of Base Formula',
         'body': ('$\\log_a M = \\dfrac{\\ln M}{\\ln a} = \\dfrac{\\log M}{\\log a}$\n'
                  'Use this to evaluate logs with any base on a calculator.')},
        {'header': 'Common Mistakes to Avoid',
         'body': ('&bull; $\\log(M+N) \\neq \\log M + \\log N$\n'
                  '&bull; $\\log(M-N) \\neq \\log M - \\log N$\n'
                  '&bull; $\\dfrac{\\log M}{\\log N} \\neq \\log M - \\log N$\n'
                  '&bull; $(\\log M)^r \\neq r \\log M$ &nbsp; (power rule requires arg is raised, not log itself)')},
    ],
    'problems': PROBS_5_5,
}


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5.6 — Logarithmic and Exponential Equations
# ════════════════════════════════════════════════════════════════════════════════
def log_eq_prob(num, eq_str, domain_str, step2_body, solution_str, answer_str):
    return {
        'num': num, 'badge': 'Logarithmic Equation',
        'given': f'Solve: $\\;{eq_str}$',
        'steps': [
            {'title': 'State domain restriction',
             'body': domain_str},
            {'title': 'Apply log properties and simplify',
             'body': step2_body},
            {'title': 'Solve and check for extraneous values',
             'body': solution_str},
        ],
        'answer': answer_str,
    }


def exp_eq_sub_prob(num, eq_str, sub_body, solve_body, answer_str):
    return {
        'num': num, 'badge': 'Exponential Equation',
        'given': f'Solve: $\\;{eq_str}$',
        'steps': [
            {'title': 'Use substitution u = aˣ',
             'body': sub_body},
            {'title': 'Solve the resulting equation for x',
             'body': solve_body},
        ],
        'answer': answer_str,
    }


PROBS_5_6 = [
    # ── Log equations 15-30 ───────────────────────────────────────────────────
    log_eq_prob(15, '2\\log_3(x+4) - \\log_3 9 = 2',
        '$x+4 &gt; 0 \\Rightarrow x &gt; -4$',
        ('$\\log_3 9 = 2$, so $2\\log_3(x+4) - 2 = 2$\n'
         '$2\\log_3(x+4) = 4 \\Rightarrow \\log_3(x+4) = 2$\n'
         '$x+4 = 3^2 = 9 \\Rightarrow x = 5$'),
        'Check: $x=5 &gt; -4$ ✓',
        '$x = 5$'),
    log_eq_prob(16, '3\\log_2(x-1) + \\log_2 4 = 5',
        '$x-1 &gt; 0 \\Rightarrow x &gt; 1$',
        ('$\\log_2 4 = 2$, so $3\\log_2(x-1) + 2 = 5$\n'
         '$3\\log_2(x-1) = 3 \\Rightarrow \\log_2(x-1) = 1$\n'
         '$x-1 = 2 \\Rightarrow x = 3$'),
        'Check: $x=3 &gt; 1$ ✓',
        '$x = 3$'),
    log_eq_prob(17, '\\log x + \\log(x-21) = 2',
        '$x &gt; 21$ (need both args positive)',
        ('$\\log[x(x-21)] = 2 \\Rightarrow x(x-21) = 100$\n'
         '$x^2 - 21x - 100 = 0 \\Rightarrow (x-25)(x+4) = 0$\n'
         '$x = 25$ or $x = -4$'),
        'Reject $x=-4$ (not in domain). Check $x=25$: $\\log 25 + \\log 4 = \\log 100 = 2$ ✓',
        '$x = 25$'),
    log_eq_prob(18, '\\log x + \\log(x+15) = 2',
        '$x &gt; 0$',
        ('$\\log[x(x+15)] = 2 \\Rightarrow x^2+15x-100 = 0$\n'
         '$(x+20)(x-5) = 0 \\Rightarrow x=5$ or $x=-20$'),
        'Reject $x=-20$. Check $x=5$ ✓',
        '$x = 5$'),
    log_eq_prob(19, '\\log(2x) - \\log(x-3) = 1',
        '$x &gt; 3$',
        ('$\\log\\!\\left(\\dfrac{2x}{x-3}\\right) = 1 \\Rightarrow \\dfrac{2x}{x-3} = 10$\n'
         '$2x = 10x - 30 \\Rightarrow 8x = 30 \\Rightarrow x = \\dfrac{15}{4}$'),
        'Check: $\\dfrac{15}{4} &gt; 3$ ✓',
        '$x = \\dfrac{15}{4}$'),
    log_eq_prob(20, '\\log(2x+1) = 1 + \\log(x-2)',
        '$x &gt; 2$',
        ('$\\log(2x+1) - \\log(x-2) = 1 \\Rightarrow \\log\\!\\left(\\dfrac{2x+1}{x-2}\\right) = 1$\n'
         '$\\dfrac{2x+1}{x-2} = 10 \\Rightarrow 2x+1 = 10x-20 \\Rightarrow x = \\dfrac{21}{8}$'),
        'Check: $\\dfrac{21}{8} &gt; 2$ ✓',
        '$x = \\dfrac{21}{8}$'),
    log_eq_prob(21, '\\log_2(x+7) + \\log_2(x+8) = 1',
        '$x &gt; -7$',
        ('$(x+7)(x+8) = 2^1 = 2$\n'
         '$x^2 + 15x + 56 = 2 \\Rightarrow x^2+15x+54 = 0$\n'
         '$(x+9)(x+6) = 0 \\Rightarrow x=-9$ or $x=-6$'),
        'Reject $x=-9$ ($-9 \\not&gt; -7$). Check $x=-6$ ✓',
        '$x = -6$'),
    log_eq_prob(22, '\\log_6(x+4) + \\log_6(x+3) = 1',
        '$x &gt; -3$',
        ('$(x+4)(x+3) = 6$\n'
         '$x^2+7x+12=6 \\Rightarrow x^2+7x+6=0$\n'
         '$(x+6)(x+1)=0 \\Rightarrow x=-6$ or $x=-1$'),
        'Reject $x=-6$. Check $x=-1$ ✓',
        '$x = -1$'),
    log_eq_prob(23, '\\log_5(x+3) = 1 - \\log_5(x-1)',
        '$x &gt; 1$',
        ('$\\log_5(x+3) + \\log_5(x-1) = 1$\n'
         '$(x+3)(x-1) = 5 \\Rightarrow x^2+2x-3=5 \\Rightarrow x^2+2x-8=0$\n'
         '$(x+4)(x-2)=0 \\Rightarrow x=-4$ or $x=2$'),
        'Reject $x=-4$. Check $x=2$ ✓',
        '$x = 2$'),
    log_eq_prob(24, '\\log_8(x+6) = 1 - \\log_8(x+4)',
        '$x &gt; -4$',
        ('$(x+6)(x+4) = 8$\n'
         '$x^2+10x+24=8 \\Rightarrow x^2+10x+16=0$\n'
         '$(x+8)(x+2)=0 \\Rightarrow x=-8$ or $x=-2$'),
        'Reject $x=-8$. Check $x=-2$ ✓',
        '$x = -2$'),
    log_eq_prob(25, '\\ln(x+1) - \\ln x = 2',
        '$x &gt; 0$',
        ('$\\ln\\!\\left(\\dfrac{x+1}{x}\\right) = 2 \\Rightarrow \\dfrac{x+1}{x} = e^2$\n'
         '$x+1 = e^2 x \\Rightarrow 1 = x(e^2-1) \\Rightarrow x = \\dfrac{1}{e^2-1}$'),
        'Check: $x = \\dfrac{1}{e^2-1} &gt; 0$ ✓',
        '$x = \\dfrac{1}{e^2-1}$'),
    log_eq_prob(26, '\\ln x + \\ln(x+2) = 4',
        '$x &gt; 0$',
        ('$\\ln[x(x+2)] = 4 \\Rightarrow x^2+2x = e^4$\n'
         '$x^2+2x-e^4=0 \\Rightarrow x = \\dfrac{-2+\\sqrt{4+4e^4}}{2} = -1+\\sqrt{1+e^4}$'),
        'Check: $-1+\\sqrt{1+e^4} \\approx 6.46 &gt; 0$ ✓',
        '$x = -1+\\sqrt{1+e^4}$'),
    log_eq_prob(27, '\\log_2(x+1) + \\log_2(x+7) = 3',
        '$x &gt; -1$',
        ('$(x+1)(x+7) = 8$\n'
         '$x^2+8x+7=8 \\Rightarrow x^2+8x-1=0$\n'
         '$x = \\dfrac{-8 \\pm \\sqrt{68}}{2} = -4 \\pm \\sqrt{17}$'),
        'Take $x = -4+\\sqrt{17} \\approx 0.12 &gt; -1$ ✓; reject $x=-4-\\sqrt{17}$.',
        '$x = -4+\\sqrt{17}$'),
    log_eq_prob(28, '\\log_3(x+1) + \\log_3(x+4) = 2',
        '$x &gt; -1$',
        ('$(x+1)(x+4) = 9$\n'
         '$x^2+5x+4=9 \\Rightarrow x^2+5x-5=0$\n'
         '$x = \\dfrac{-5+\\sqrt{45}}{2} = \\dfrac{-5+3\\sqrt{5}}{2}$'),
        'Check: $\\approx 0.854 &gt; -1$ ✓',
        '$x = \\dfrac{-5+3\\sqrt{5}}{2}$'),
    log_eq_prob(29, '\\log_4(x^2-9) - \\log_4(x+3) = 3',
        '$x &gt; 3$ (need $x^2-9 &gt; 0$ and $x+3 &gt; 0$)',
        ('$\\log_4\\!\\left(\\dfrac{x^2-9}{x+3}\\right) = 3 \\Rightarrow \\dfrac{(x-3)(x+3)}{x+3} = x-3 = 4^3 = 64$\n'
         '$x = 67$'),
        'Check: $x=67 &gt; 3$ ✓',
        '$x = 67$'),
    log_eq_prob(30, '\\log_{1/3}(x^2+x) - \\log_{1/3}(x^2-x) = -1',
        '$x &gt; 1$ (from intersection of $x(x+1)&gt;0$ and $x(x-1)&gt;0$)',
        ('$\\log_{1/3}\\!\\left(\\dfrac{x^2+x}{x^2-x}\\right) = -1 \\Rightarrow \\dfrac{x+1}{x-1} = \\left(\\tfrac{1}{3}\\right)^{-1} = 3$\n'
         '$x+1 = 3x-3 \\Rightarrow x = 2$'),
        'Check: $x=2 &gt; 1$ ✓',
        '$x = 2$'),
    # ── Exponential equations 57-66 ───────────────────────────────────────────
    exp_eq_sub_prob(57, '3^{2x} + 3^x - 2 = 0',
        ('Let $u = 3^x$ ($u &gt; 0$): $u^2 + u - 2 = 0$\n'
         '$(u+2)(u-1) = 0 \\Rightarrow u = -2$ (reject) or $u = 1$'),
        '$3^x = 1 = 3^0 \\Rightarrow x = 0$',
        '$x = 0$'),
    exp_eq_sub_prob(58, '2^{2x} + 2^x - 12 = 0',
        ('Let $u = 2^x$: $u^2 + u - 12 = 0$\n'
         '$(u+4)(u-3) = 0 \\Rightarrow u = -4$ (reject) or $u = 3$'),
        '$2^x = 3 \\Rightarrow x = \\log_2 3 = \\dfrac{\\ln 3}{\\ln 2}$',
        '$x = \\log_2 3 \\approx 1.585$'),
    exp_eq_sub_prob(59, '2^{2x} + 2^{x+2} - 12 = 0',
        ('$2^{x+2} = 4 \\cdot 2^x$. Let $u = 2^x$: $u^2 + 4u - 12 = 0$\n'
         '$(u+6)(u-2) = 0 \\Rightarrow u = 2$'),
        '$2^x = 2 = 2^1 \\Rightarrow x = 1$',
        '$x = 1$'),
    exp_eq_sub_prob(60, '3^{2x} + 3^{x+1} - 4 = 0',
        ('$3^{x+1} = 3 \\cdot 3^x$. Let $u = 3^x$: $u^2 + 3u - 4 = 0$\n'
         '$(u+4)(u-1) = 0 \\Rightarrow u = 1$'),
        '$3^x = 1 = 3^0 \\Rightarrow x = 0$',
        '$x = 0$'),
    exp_eq_sub_prob(61, '16^x + 4^{x+1} - 3 = 0',
        ('$16^x = (4^x)^2$, $4^{x+1} = 4\\cdot4^x$. Let $u = 4^x$:\n'
         '$u^2 + 4u - 3 = 0 \\Rightarrow u = \\dfrac{-4 \\pm \\sqrt{28}}{2} = -2 \\pm \\sqrt{7}$\n'
         'Take $u = -2+\\sqrt{7} &gt; 0$'),
        ('$4^x = \\sqrt{7}-2 \\Rightarrow x = \\dfrac{\\ln(\\sqrt{7}-2)}{\\ln 4} = \\dfrac{\\ln(\\sqrt{7}-2)}{2\\ln 2}$'),
        '$x = \\dfrac{\\ln(\\sqrt{7}-2)}{2\\ln 2} \\approx -0.317$'),
    exp_eq_sub_prob(62, '9^x - 3^{x+1} + 1 = 0',
        ('$9^x = (3^x)^2$, $3^{x+1} = 3\\cdot3^x$. Let $u = 3^x$:\n'
         '$u^2 - 3u + 1 = 0 \\Rightarrow u = \\dfrac{3 \\pm \\sqrt{5}}{2}$\n'
         'Both values positive, so both give valid solutions.'),
        ('$x_1 = \\log_3\\!\\left(\\dfrac{3+\\sqrt{5}}{2}\\right)$,  '
         '$x_2 = \\log_3\\!\\left(\\dfrac{3-\\sqrt{5}}{2}\\right)$'),
        '$x = \\log_3\\!\\left(\\dfrac{3 \\pm \\sqrt{5}}{2}\\right)$'),
    exp_eq_sub_prob(63, '6^x - 6 \\cdot 6^{-x} = -9',
        ('Multiply by $6^x$: $(6^x)^2 + 9 \\cdot 6^x - 6 = 0$. Let $u = 6^x$:\n'
         '$u^2 + 9u - 6 = 0 \\Rightarrow u = \\dfrac{-9+\\sqrt{105}}{2}$ (positive root only)'),
        ('$6^x = \\dfrac{-9+\\sqrt{105}}{2} \\Rightarrow x = \\dfrac{\\ln\\frac{\\sqrt{105}-9}{2}}{\\ln 6}$'),
        '$x = \\log_6\\!\\left(\\dfrac{\\sqrt{105}-9}{2}\\right)$'),
    exp_eq_sub_prob(64, '5^x - 8 \\cdot 5^{-x} = -16',
        ('Multiply by $5^x$: $(5^x)^2 + 16 \\cdot 5^x - 8 = 0$. Let $u = 5^x$:\n'
         '$u^2 + 16u - 8 = 0 \\Rightarrow u = \\dfrac{-16+\\sqrt{288}}{2} = -8+6\\sqrt{2}$'),
        ('$5^x = -8+6\\sqrt{2} \\Rightarrow x = \\dfrac{\\ln(-8+6\\sqrt{2})}{\\ln 5}$'),
        '$x = \\log_5(-8+6\\sqrt{2})$'),
    exp_eq_sub_prob(65, '2 \\cdot 49^x + 11 \\cdot 7^x + 5 = 0',
        ('$49^x = (7^x)^2$. Let $u = 7^x &gt; 0$: $2u^2 + 11u + 5 = 0$\n'
         '$(2u+1)(u+5) = 0 \\Rightarrow u = -\\dfrac{1}{2}$ or $u = -5$\n'
         'Both roots are negative — impossible since $7^x &gt; 0$.'),
        'No real solutions exist.',
        'No solution (all terms positive for real $x$)'),
    exp_eq_sub_prob(66, '3 \\cdot 4^x + 4 \\cdot 2^x + 8 = 0',
        ('$4^x = (2^x)^2$. Let $u = 2^x &gt; 0$: $3u^2 + 4u + 8 = 0$\n'
         'Discriminant $= 16 - 96 = -80 &lt; 0$; no real roots.'),
        'No real solutions exist.',
        'No solution (discriminant is negative)'),
]

CFG_5_6 = {
    'section_label': '5.6',
    'section_name': 'Logarithmic and Exponential Equations',
    'folder': '5.6',
    'fname': 'section_5_6.html',
    'groups': [
        {'title': 'Logarithmic Equations', 'probs': list(range(15, 31))},
        {'title': 'Exponential Equations', 'probs': list(range(57, 67))},
    ],
    'sidenotes': [
        {'header': 'Solving Logarithmic Equations',
         'body': ('1. State domain (argument of log must be $&gt; 0$)\n'
                  '2. Combine logs on each side using log properties\n'
                  '3. Convert to exponential form: $\\log_a M = c \\Leftrightarrow M = a^c$\n'
                  '4. Solve the resulting equation\n'
                  '5. Check all solutions against domain restrictions (reject extraneous)')},
        {'header': 'Solving Exponential Equations — Substitution Method',
         'body': ('For equations of the form $a^{2x} + b \\cdot a^x + c = 0$:\n'
                  'Let $u = a^x$, so $a^{2x} = u^2$\n'
                  'Solve the quadratic in $u$\n'
                  'Keep only $u &gt; 0$ (since $a^x &gt; 0$ always)\n'
                  'Then solve $a^x = u$ for $x$')},
    ],
    'problems': PROBS_5_6,
}


# ════════════════════════════════════════════════════════════════════════════════
# GENERATE ALL FILES
# ════════════════════════════════════════════════════════════════════════════════
ALL_CFGS = [CFG_5_1, CFG_5_2, CFG_5_3, CFG_5_4, CFG_5_5, CFG_5_6]

for cfg in ALL_CFGS:
    out_dir = os.path.join(BASE_DIR, cfg['folder'])
    os.makedirs(out_dir, exist_ok=True)
    html = build_page(cfg)
    out_path = os.path.join(out_dir, cfg['fname'])
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f"✓ Written {out_path}  ({len(html):,} bytes)")

print("\nDone! All 5.x section HTML files generated.")
