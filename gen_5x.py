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

      /* ── Mini Insight Step ── */
      .step.insight {
        background: #fff8e1;
        border-left: 4px solid #ff9800;
      }
      .step.insight .step-title {
        color: #bf360c;
        font-style: italic;
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
        extra_cls = f' {step["class"]}' if step.get('class') else ''
        steps_html += f"""            <div class="step{extra_cls}">
              <div class="step-title">{step['title']}</div>
              <div class="step-body">{step['body']}</div>
            </div>\n"""

    ans_secs = ''
    for step in p['steps']:
        if step.get('class') == 'insight':
            continue  # exclude Mini Insight from Exam Answer box
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


def _insight(body):
    return {'title': '💡 Mini Insight (Exam Shortcut)', 'class': 'insight', 'body': body}


PROBS_5_6 = [
    # ── Log equations 15-30 ───────────────────────────────────────────────────
    {
        'num': 15, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;2\\log_3(x+4) - \\log_3 9 = 2$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': 'Argument of each log must be positive.\n$x + 4 &gt; 0 \\Rightarrow x &gt; -4$'},
            {'title': 'Step 2 — Evaluate the known logarithm',
             'body': '$\\log_3 9 = 2 \\quad$ (since $3^2 = 9$)\nSubstitute: $\\;2\\log_3(x+4) - 2 = 2$'},
            {'title': 'Step 3 — Isolate the log (add 2 to both sides)',
             'body': '$2\\log_3(x+4) = 4$'},
            {'title': 'Step 4 — Remove the coefficient (divide both sides by 2)',
             'body': '$\\log_3(x+4) = 2$'},
            {'title': 'Step 5 — Convert to exponential form',
             'body': 'Recall: $\\log_b A = c \\Longleftrightarrow A = b^c$\n$x + 4 = 3^2 = 9$'},
            {'title': 'Step 6 — Solve for x',
             'body': '$x = 9 - 4 = 5$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = 5 &gt; -4$ ✓\nVerify: $2\\log_3(9) - \\log_3 9 = 2(2) - 2 = 2$ ✓'},
            _insight('Once you arrive at $\\log_3(x+4) = 2$, recall $\\log_3 9 = 2$,\n'
                     'so immediately: $x + 4 = 9 \\Rightarrow x = 5$ — no formal conversion needed!'),
        ],
        'answer': '$x = 5$',
    },
    {
        'num': 16, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;3\\log_2(x-1) + \\log_2 4 = 5$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x - 1 &gt; 0 \\Rightarrow x &gt; 1$'},
            {'title': 'Step 2 — Evaluate the known logarithm',
             'body': '$\\log_2 4 = 2 \\quad$ (since $2^2 = 4$)\nSubstitute: $\\;3\\log_2(x-1) + 2 = 5$'},
            {'title': 'Step 3 — Isolate the log (subtract 2 from both sides)',
             'body': '$3\\log_2(x-1) = 3$'},
            {'title': 'Step 4 — Remove the coefficient (divide both sides by 3)',
             'body': '$\\log_2(x-1) = 1$'},
            {'title': 'Step 5 — Convert to exponential form',
             'body': 'Recall: $\\log_b A = c \\Longleftrightarrow A = b^c$\n$x - 1 = 2^1 = 2$'},
            {'title': 'Step 6 — Solve for x',
             'body': '$x = 2 + 1 = 3$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = 3 &gt; 1$ ✓\nVerify: $3\\log_2(2) + \\log_2 4 = 3(1) + 2 = 5$ ✓'},
            _insight('Once you reach $\\log_2(x-1) = 1$, instantly think: $x - 1 = 2^1 = 2$.\n'
                     'Key fact: $\\log_b(b) = 1$ always — so $\\log_2(2) = 1$.'),
        ],
        'answer': '$x = 3$',
    },
    {
        'num': 17, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log x + \\log(x-21) = 2$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': 'Both arguments must be positive:\n'
                     '$x &gt; 0$ and $x - 21 &gt; 0$\nStricter condition: $x &gt; 21$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': 'Product Rule: $\\log M + \\log N = \\log(MN)$\n$\\log[x(x-21)] = 2$'},
            {'title': 'Step 3 — Convert to exponential form (base 10)',
             'body': 'Recall: $\\log A = c \\Longleftrightarrow A = 10^c$\n$x(x-21) = 10^2 = 100$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 - 21x = 100$\n$x^2 - 21x - 100 = 0$'},
            {'title': 'Step 5 — Factor the quadratic',
             'body': 'Find two numbers that multiply to $-100$ and add to $-21$: $-25$ and $+4$\n'
                     '$(x-25)(x+4) = 0$\n$x = 25 \\quad$ or $\\quad x = -4$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': 'Reject $x = -4$: fails domain ($-4 \\not&gt; 21$).\n'
                     'Check $x = 25$: $\\log 25 + \\log 4 = \\log(100) = 2$ ✓'},
            _insight('When you get two solutions from a quadratic, always test both against the domain.\n'
                     'Here, only $x = 25$ satisfies $x &gt; 21$.'),
        ],
        'answer': '$x = 25$',
    },
    {
        'num': 18, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log x + \\log(x+15) = 2$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x &gt; 0$ and $x+15 &gt; 0$ — stricter condition: $x &gt; 0$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': '$\\log[x(x+15)] = 2$'},
            {'title': 'Step 3 — Convert to exponential form',
             'body': '$x(x+15) = 10^2 = 100$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 + 15x = 100$\n$x^2 + 15x - 100 = 0$'},
            {'title': 'Step 5 — Factor the quadratic',
             'body': 'Find two numbers that multiply to $-100$ and add to $+15$: $+20$ and $-5$\n'
                     '$(x+20)(x-5) = 0$\n$x = -20 \\quad$ or $\\quad x = 5$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': 'Reject $x = -20$: fails domain ($x &gt; 0$ required).\n'
                     'Check $x = 5$: $\\log 5 + \\log 20 = \\log 100 = 2$ ✓'},
            _insight('Pattern: $\\log x + \\log(x+n) = 2$ means $x(x+n) = 100$.\n'
                     'Base-10 log of $100 = 2$ since $10^2 = 100$.'),
        ],
        'answer': '$x = 5$',
    },
    {
        'num': 19, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log(2x) - \\log(x-3) = 1$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$2x &gt; 0$ and $x - 3 &gt; 0$ — stricter condition: $x &gt; 3$'},
            {'title': 'Step 2 — Apply the Quotient Rule',
             'body': 'Quotient Rule: $\\log M - \\log N = \\log\\!\\left(\\dfrac{M}{N}\\right)$\n'
                     '$\\log\\!\\left(\\dfrac{2x}{x-3}\\right) = 1$'},
            {'title': 'Step 3 — Convert to exponential form',
             'body': '$\\dfrac{2x}{x-3} = 10^1 = 10$'},
            {'title': 'Step 4 — Cross-multiply and solve',
             'body': '$2x = 10(x-3)$\n$2x = 10x - 30$\n$-8x = -30$\n$x = \\dfrac{30}{8} = \\dfrac{15}{4}$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = \\dfrac{15}{4} = 3.75 &gt; 3$ ✓\nVerify: $\\log(7.5) - \\log(0.75) = \\log(10) = 1$ ✓'},
            _insight('Quotient rule turns the subtraction of logs into a single fraction $= 10$.\n'
                     'Cross-multiplying then gives a straightforward linear equation.'),
        ],
        'answer': '$x = \\dfrac{15}{4}$',
    },
    {
        'num': 20, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log(2x+1) = 1 + \\log(x-2)$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$2x+1 &gt; 0$ and $x-2 &gt; 0$ — stricter condition: $x &gt; 2$'},
            {'title': 'Step 2 — Move all log terms to the left side',
             'body': '$\\log(2x+1) - \\log(x-2) = 1$'},
            {'title': 'Step 3 — Apply the Quotient Rule',
             'body': '$\\log\\!\\left(\\dfrac{2x+1}{x-2}\\right) = 1$'},
            {'title': 'Step 4 — Convert to exponential form',
             'body': '$\\dfrac{2x+1}{x-2} = 10^1 = 10$'},
            {'title': 'Step 5 — Cross-multiply and solve',
             'body': '$2x+1 = 10(x-2)$\n$2x+1 = 10x - 20$\n$-8x = -21$\n$x = \\dfrac{21}{8}$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = \\dfrac{21}{8} = 2.625 &gt; 2$ ✓'},
            _insight('When a constant (like $+1$) sits on the same side as a log, move it left first.\n'
                     'This lets you combine into a single $\\log = 1$ form before converting.'),
        ],
        'answer': '$x = \\dfrac{21}{8}$',
    },
    {
        'num': 21, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_2(x+7) + \\log_2(x+8) = 1$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 7 &gt; 0$ and $x + 8 &gt; 0$ — stricter condition: $x &gt; -7$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': '$\\log_2[(x+7)(x+8)] = 1$'},
            {'title': 'Step 3 — Convert to exponential form (base 2)',
             'body': '$(x+7)(x+8) = 2^1 = 2$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 + 15x + 56 = 2$\n$x^2 + 15x + 54 = 0$'},
            {'title': 'Step 5 — Factor the quadratic',
             'body': 'Find two numbers that multiply to $54$ and add to $15$: $9$ and $6$\n'
                     '$(x+9)(x+6) = 0$\n$x = -9 \\quad$ or $\\quad x = -6$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': 'Reject $x = -9$: $-9 \\not&gt; -7$ (fails domain).\n'
                     'Check $x = -6$: $\\log_2(1) + \\log_2(2) = 0 + 1 = 1$ ✓'},
            _insight('With base 2 and RHS $= 1$: product $= 2^1 = 2$. The small RHS leads to\n'
                     'small (possibly negative) $x$ — always check domain carefully here.'),
        ],
        'answer': '$x = -6$',
    },
    {
        'num': 22, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_6(x+4) + \\log_6(x+3) = 1$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 4 &gt; 0$ and $x + 3 &gt; 0$ — stricter condition: $x &gt; -3$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': '$\\log_6[(x+4)(x+3)] = 1$'},
            {'title': 'Step 3 — Convert to exponential form (base 6)',
             'body': '$(x+4)(x+3) = 6^1 = 6$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 + 7x + 12 = 6$\n$x^2 + 7x + 6 = 0$'},
            {'title': 'Step 5 — Factor the quadratic',
             'body': '$(x+6)(x+1) = 0$\n$x = -6 \\quad$ or $\\quad x = -1$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': 'Reject $x = -6$: $-6 \\not&gt; -3$ (fails domain).\n'
                     'Check $x = -1$: $\\log_6(3) + \\log_6(2) = \\log_6(6) = 1$ ✓'},
            _insight('Spot the verification shortcut: $\\log_6(3) + \\log_6(2) = \\log_6(3 \\cdot 2) = \\log_6 6 = 1$.\n'
                     'Recognising this product-rule check saves time on the exam.'),
        ],
        'answer': '$x = -1$',
    },
    {
        'num': 23, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_5(x+3) = 1 - \\log_5(x-1)$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 3 &gt; 0$ and $x - 1 &gt; 0$ — stricter condition: $x &gt; 1$'},
            {'title': 'Step 2 — Move all log terms to the left side',
             'body': '$\\log_5(x+3) + \\log_5(x-1) = 1$'},
            {'title': 'Step 3 — Apply the Product Rule',
             'body': '$\\log_5[(x+3)(x-1)] = 1$'},
            {'title': 'Step 4 — Convert to exponential form (base 5)',
             'body': '$(x+3)(x-1) = 5^1 = 5$'},
            {'title': 'Step 5 — Expand and rearrange',
             'body': '$x^2 + 2x - 3 = 5$\n$x^2 + 2x - 8 = 0$'},
            {'title': 'Step 6 — Factor the quadratic',
             'body': '$(x+4)(x-2) = 0$\n$x = -4 \\quad$ or $\\quad x = 2$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': 'Reject $x = -4$: $-4 \\not&gt; 1$ (fails domain).\n'
                     'Check $x = 2$: $\\log_5(5) = 1 - \\log_5(1) = 1 - 0 = 1$ ✓'},
            _insight('Pattern: $\\log_b A = 1 - \\log_b B \\Rightarrow \\log_b(AB) = 1 \\Rightarrow AB = b$.\n'
                     'Move the log right, then apply the product rule.'),
        ],
        'answer': '$x = 2$',
    },
    {
        'num': 24, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_8(x+6) = 1 - \\log_8(x+4)$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 6 &gt; 0$ and $x + 4 &gt; 0$ — stricter condition: $x &gt; -4$'},
            {'title': 'Step 2 — Move all log terms to the left side',
             'body': '$\\log_8(x+6) + \\log_8(x+4) = 1$'},
            {'title': 'Step 3 — Apply the Product Rule',
             'body': '$\\log_8[(x+6)(x+4)] = 1$'},
            {'title': 'Step 4 — Convert to exponential form (base 8)',
             'body': '$(x+6)(x+4) = 8^1 = 8$'},
            {'title': 'Step 5 — Expand and rearrange',
             'body': '$x^2 + 10x + 24 = 8$\n$x^2 + 10x + 16 = 0$'},
            {'title': 'Step 6 — Factor the quadratic',
             'body': '$(x+8)(x+2) = 0$\n$x = -8 \\quad$ or $\\quad x = -2$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': 'Reject $x = -8$: $-8 \\not&gt; -4$ (fails domain).\n'
                     'Check $x = -2$: $\\log_8(4) + \\log_8(2) = \\log_8(8) = 1$ ✓'},
            _insight('Same pattern as Problem 23: $\\log_b A = 1 - \\log_b B \\Rightarrow AB = b$.\n'
                     'Here $(x+6)(x+4) = 8$.'),
        ],
        'answer': '$x = -2$',
    },
    {
        'num': 25, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\ln(x+1) - \\ln x = 2$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 1 &gt; 0$ and $x &gt; 0$ — stricter condition: $x &gt; 0$'},
            {'title': 'Step 2 — Apply the Quotient Rule',
             'body': '$\\ln\\!\\left(\\dfrac{x+1}{x}\\right) = 2$'},
            {'title': 'Step 3 — Convert to exponential form (base $e$)',
             'body': 'Recall: $\\ln A = c \\Longleftrightarrow A = e^c$\n$\\dfrac{x+1}{x} = e^2$'},
            {'title': 'Step 4 — Cross-multiply and solve',
             'body': '$x + 1 = e^2 \\cdot x$\n$1 = e^2 x - x = x(e^2 - 1)$\n$x = \\dfrac{1}{e^2-1}$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = \\dfrac{1}{e^2-1} \\approx 0.156 &gt; 0$ ✓'},
            _insight('$\\ln$ uses base $e$, so $\\ln A = c \\Rightarrow A = e^c$.\n'
                     'Factor $x$ from the right side: $1 = x(e^2-1) \\Rightarrow x = \\dfrac{1}{e^2-1}$.'),
        ],
        'answer': '$x = \\dfrac{1}{e^2-1}$',
    },
    {
        'num': 26, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\ln x + \\ln(x+2) = 4$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x &gt; 0$ and $x+2 &gt; 0$ — stricter condition: $x &gt; 0$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': '$\\ln[x(x+2)] = 4$'},
            {'title': 'Step 3 — Convert to exponential form (base $e$)',
             'body': '$x(x+2) = e^4$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 + 2x = e^4$\n$x^2 + 2x - e^4 = 0$'},
            {'title': 'Step 5 — Apply the quadratic formula',
             'body': '$a=1,\\; b=2,\\; c=-e^4$\n'
                     '$x = \\dfrac{-2 \\pm \\sqrt{4 + 4e^4}}{2} = \\dfrac{-2 \\pm 2\\sqrt{1+e^4}}{2} = -1 \\pm \\sqrt{1+e^4}$'},
            {'title': '✅ Check — reject negative root',
             'body': 'Reject $x = -1-\\sqrt{1+e^4}$ (negative, fails $x &gt; 0$).\n'
                     'Check $x = -1+\\sqrt{1+e^4} \\approx 6.46 &gt; 0$ ✓'},
            _insight('When you cannot factor (because $e^4$ is irrational), use the quadratic formula.\n'
                     'Always simplify: $\\sqrt{4+4e^4} = 2\\sqrt{1+e^4}$.'),
        ],
        'answer': '$x = -1+\\sqrt{1+e^4}$',
    },
    {
        'num': 27, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_2(x+1) + \\log_2(x+7) = 3$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 1 &gt; 0$ and $x + 7 &gt; 0$ — stricter condition: $x &gt; -1$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': '$\\log_2[(x+1)(x+7)] = 3$'},
            {'title': 'Step 3 — Convert to exponential form (base 2)',
             'body': '$(x+1)(x+7) = 2^3 = 8$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 + 8x + 7 = 8$\n$x^2 + 8x - 1 = 0$'},
            {'title': 'Step 5 — Apply the quadratic formula (cannot factor)',
             'body': '$x = \\dfrac{-8 \\pm \\sqrt{64+4}}{2} = \\dfrac{-8 \\pm \\sqrt{68}}{2} = \\dfrac{-8 \\pm 2\\sqrt{17}}{2} = -4 \\pm \\sqrt{17}$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': '$x = -4+\\sqrt{17} \\approx 0.12 &gt; -1$ ✓\n'
                     'Reject $x = -4-\\sqrt{17} \\approx -8.12$ (fails $x &gt; -1$).'},
            _insight('Simplify the discriminant: $\\sqrt{68} = \\sqrt{4 \\cdot 17} = 2\\sqrt{17}$.\n'
                     'Always factor out perfect squares from under the radical.'),
        ],
        'answer': '$x = -4+\\sqrt{17}$',
    },
    {
        'num': 28, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_3(x+1) + \\log_3(x+4) = 2$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x + 1 &gt; 0$ and $x + 4 &gt; 0$ — stricter condition: $x &gt; -1$'},
            {'title': 'Step 2 — Apply the Product Rule',
             'body': '$\\log_3[(x+1)(x+4)] = 2$'},
            {'title': 'Step 3 — Convert to exponential form (base 3)',
             'body': '$(x+1)(x+4) = 3^2 = 9$'},
            {'title': 'Step 4 — Expand and rearrange',
             'body': '$x^2 + 5x + 4 = 9$\n$x^2 + 5x - 5 = 0$'},
            {'title': 'Step 5 — Apply the quadratic formula',
             'body': '$x = \\dfrac{-5 \\pm \\sqrt{25+20}}{2} = \\dfrac{-5 \\pm \\sqrt{45}}{2} = \\dfrac{-5 \\pm 3\\sqrt{5}}{2}$'},
            {'title': '✅ Check — reject extraneous solutions',
             'body': '$x = \\dfrac{-5+3\\sqrt{5}}{2} \\approx 0.854 &gt; -1$ ✓\n'
                     'Reject $x = \\dfrac{-5-3\\sqrt{5}}{2} \\approx -5.854$.'},
            _insight('Simplify the surd: $\\sqrt{45} = \\sqrt{9 \\cdot 5} = 3\\sqrt{5}$.\n'
                     'Always factor perfect squares out of surds for full marks.'),
        ],
        'answer': '$x = \\dfrac{-5+3\\sqrt{5}}{2}$',
    },
    {
        'num': 29, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_4(x^2-9) - \\log_4(x+3) = 3$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x^2-9 &gt; 0 \\Rightarrow (x-3)(x+3) &gt; 0 \\Rightarrow x &gt; 3$ or $x &lt; -3$\n'
                     '$x+3 &gt; 0 \\Rightarrow x &gt; -3$\nIntersection: $x &gt; 3$'},
            {'title': 'Step 2 — Apply the Quotient Rule',
             'body': '$\\log_4\\!\\left(\\dfrac{x^2-9}{x+3}\\right) = 3$'},
            {'title': 'Step 3 — Factor the numerator (difference of squares)',
             'body': '$\\dfrac{(x-3)(x+3)}{x+3} = x-3 \\quad$ (cancel $x+3 \\neq 0$)'},
            {'title': 'Step 4 — Simplified equation; convert to exponential form',
             'body': '$\\log_4(x-3) = 3$\n$x - 3 = 4^3 = 64$'},
            {'title': 'Step 5 — Solve for x',
             'body': '$x = 64 + 3 = 67$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = 67 &gt; 3$ ✓\n'
                     'Verify: $\\log_4(67^2-9) - \\log_4(70) = \\log_4\\!\\left(\\dfrac{4480}{70}\\right) = \\log_4(64) = 3$ ✓'},
            _insight('Always check if the argument factors — $x^2-9 = (x-3)(x+3)$.\n'
                     'The $(x+3)$ cancels, simplifying to $\\log_4(x-3) = 3$.'),
        ],
        'answer': '$x = 67$',
    },
    {
        'num': 30, 'badge': 'Logarithmic Equation',
        'given': 'Solve: $\\;\\log_{1/3}(x^2+x) - \\log_{1/3}(x^2-x) = -1$',
        'steps': [
            {'title': 'Step 1 — State domain restriction',
             'body': '$x^2+x &gt; 0 \\Rightarrow x(x+1) &gt; 0 \\Rightarrow x &lt; -1$ or $x &gt; 0$\n'
                     '$x^2-x &gt; 0 \\Rightarrow x(x-1) &gt; 0 \\Rightarrow x &lt; 0$ or $x &gt; 1$\n'
                     'Intersection: $x &gt; 1$'},
            {'title': 'Step 2 — Apply the Quotient Rule',
             'body': '$\\log_{1/3}\\!\\left(\\dfrac{x^2+x}{x^2-x}\\right) = -1$'},
            {'title': 'Step 3 — Simplify the fraction by factoring',
             'body': '$\\dfrac{x(x+1)}{x(x-1)} = \\dfrac{x+1}{x-1}$\n'
                     'So: $\\log_{1/3}\\!\\left(\\dfrac{x+1}{x-1}\\right) = -1$'},
            {'title': 'Step 4 — Convert to exponential form',
             'body': 'Recall: $\\log_b A = c \\Longleftrightarrow A = b^c$\n'
                     '$\\dfrac{x+1}{x-1} = \\left(\\dfrac{1}{3}\\right)^{-1} = 3$'},
            {'title': 'Step 5 — Cross-multiply and solve',
             'body': '$x+1 = 3(x-1)$\n$x+1 = 3x-3$\n$4 = 2x$\n$x = 2$'},
            {'title': '✅ Check — verify against domain',
             'body': '$x = 2 &gt; 1$ ✓\n'
                     'Verify: $\\log_{1/3}(6) - \\log_{1/3}(2) = \\log_{1/3}(3) = -1$ ✓ (since $(\\tfrac{1}{3})^{-1}=3$)'},
            _insight('Key: $\\left(\\dfrac{1}{3}\\right)^{-1} = 3$, so $\\log_{1/3}(3) = -1$.\n'
                     'A negative exponent with base $&lt; 1$ gives a value $&gt; 1$.'),
        ],
        'answer': '$x = 2$',
    },
    # ── Exponential equations 57-66 ───────────────────────────────────────────
    {
        'num': 57, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;3^{2x} + 3^x - 2 = 0$',
        'steps': [
            {'title': 'Step 1 — Recognize the quadratic structure',
             'body': 'Note: $3^{2x} = (3^x)^2$ — this equation is quadratic in $3^x$.'},
            {'title': 'Step 2 — Let $u = 3^x$ (substitution)',
             'body': 'Important: $u = 3^x &gt; 0$ for all $x$.\nEquation becomes: $u^2 + u - 2 = 0$'},
            {'title': 'Step 3 — Factor the quadratic',
             'body': '$(u+2)(u-1) = 0$\n$u = -2 \\quad$ or $\\quad u = 1$'},
            {'title': 'Step 4 — Reject invalid root',
             'body': 'Reject $u = -2$: impossible since $3^x &gt; 0$ always.\nKeep $u = 1$.'},
            {'title': 'Step 5 — Solve $3^x = 1$ for $x$',
             'body': '$3^x = 1 = 3^0$\nSince bases match: $x = 0$'},
            {'title': '✅ Check — verify',
             'body': '$3^{2(0)} + 3^0 - 2 = 1 + 1 - 2 = 0$ ✓'},
            _insight('When $a^x = 1$ (any base $a \\neq 0$): always $x = 0$, since $a^0 = 1$.'),
        ],
        'answer': '$x = 0$',
    },
    {
        'num': 58, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;2^{2x} + 2^x - 12 = 0$',
        'steps': [
            {'title': 'Step 1 — Recognize the quadratic structure',
             'body': '$2^{2x} = (2^x)^2$ — quadratic in $2^x$.'},
            {'title': 'Step 2 — Let $u = 2^x$ (substitution)',
             'body': '$u &gt; 0$. Equation becomes: $u^2 + u - 12 = 0$'},
            {'title': 'Step 3 — Factor the quadratic',
             'body': '$(u+4)(u-3) = 0$\n$u = -4 \\quad$ or $\\quad u = 3$'},
            {'title': 'Step 4 — Reject invalid root',
             'body': 'Reject $u = -4$ (negative, $2^x &gt; 0$). Keep $u = 3$.'},
            {'title': 'Step 5 — Solve $2^x = 3$ for $x$',
             'body': 'Take $\\ln$ of both sides:\n$x \\ln 2 = \\ln 3$\n$x = \\dfrac{\\ln 3}{\\ln 2} = \\log_2 3$'},
            {'title': '✅ Check — verify (approximate)',
             'body': '$x \\approx 1.585$. Then $2^{2(1.585)} + 2^{1.585} - 12 \\approx 9 + 3 - 12 = 0$ ✓'},
            _insight('When $2^x = 3$ (not a power of 2): $x = \\log_2 3 = \\dfrac{\\ln 3}{\\ln 2}$.\n'
                     'Change-of-base: $\\log_b a = \\dfrac{\\ln a}{\\ln b}$.'),
        ],
        'answer': '$x = \\log_2 3 \\approx 1.585$',
    },
    {
        'num': 59, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;2^{2x} + 2^{x+2} - 12 = 0$',
        'steps': [
            {'title': 'Step 1 — Rewrite $2^{x+2}$ using exponent rules',
             'body': '$2^{x+2} = 2^x \\cdot 2^2 = 4 \\cdot 2^x$\nEquation becomes: $2^{2x} + 4 \\cdot 2^x - 12 = 0$'},
            {'title': 'Step 2 — Let $u = 2^x$ (substitution)',
             'body': '$u &gt; 0$. Equation becomes: $u^2 + 4u - 12 = 0$'},
            {'title': 'Step 3 — Factor the quadratic',
             'body': '$(u+6)(u-2) = 0$\n$u = -6 \\quad$ or $\\quad u = 2$'},
            {'title': 'Step 4 — Reject invalid root',
             'body': 'Reject $u = -6$. Keep $u = 2$.'},
            {'title': 'Step 5 — Solve $2^x = 2$ for $x$',
             'body': '$2^x = 2 = 2^1 \\Rightarrow x = 1$'},
            {'title': '✅ Check — verify',
             'body': '$2^2 + 2^3 - 12 = 4 + 8 - 12 = 0$ ✓'},
            _insight('Key step: $2^{x+2} = 4 \\cdot 2^x$.\n'
                     'Always rewrite $a^{x+k} = a^k \\cdot a^x$ BEFORE substituting.'),
        ],
        'answer': '$x = 1$',
    },
    {
        'num': 60, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;3^{2x} + 3^{x+1} - 4 = 0$',
        'steps': [
            {'title': 'Step 1 — Rewrite $3^{x+1}$ using exponent rules',
             'body': '$3^{x+1} = 3 \\cdot 3^x$\nEquation becomes: $3^{2x} + 3 \\cdot 3^x - 4 = 0$'},
            {'title': 'Step 2 — Let $u = 3^x$ (substitution)',
             'body': '$u &gt; 0$. Equation becomes: $u^2 + 3u - 4 = 0$'},
            {'title': 'Step 3 — Factor the quadratic',
             'body': '$(u+4)(u-1) = 0$\n$u = -4 \\quad$ or $\\quad u = 1$'},
            {'title': 'Step 4 — Reject invalid root',
             'body': 'Reject $u = -4$. Keep $u = 1$.'},
            {'title': 'Step 5 — Solve $3^x = 1$ for $x$',
             'body': '$3^x = 1 = 3^0 \\Rightarrow x = 0$'},
            {'title': '✅ Check — verify',
             'body': '$3^0 + 3^1 - 4 = 1 + 3 - 4 = 0$ ✓'},
            _insight('Same approach as Problem 59: rewrite $3^{x+1} = 3 \\cdot 3^x$ first,\n'
                     'making the coefficient of $u$ equal to $3$ in the quadratic.'),
        ],
        'answer': '$x = 0$',
    },
    {
        'num': 61, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;16^x + 4^{x+1} - 3 = 0$',
        'steps': [
            {'title': 'Step 1 — Rewrite all terms in base 4',
             'body': '$16^x = (4^2)^x = (4^x)^2$\n$4^{x+1} = 4 \\cdot 4^x$\nEquation: $(4^x)^2 + 4 \\cdot 4^x - 3 = 0$'},
            {'title': 'Step 2 — Let $u = 4^x$ (substitution)',
             'body': '$u &gt; 0$. Equation: $u^2 + 4u - 3 = 0$'},
            {'title': 'Step 3 — Quadratic formula (does not factor nicely)',
             'body': '$u = \\dfrac{-4 \\pm \\sqrt{16+12}}{2} = \\dfrac{-4 \\pm \\sqrt{28}}{2} = \\dfrac{-4 \\pm 2\\sqrt{7}}{2} = -2 \\pm \\sqrt{7}$'},
            {'title': 'Step 4 — Reject invalid root',
             'body': '$\\sqrt{7} \\approx 2.646$\n'
                     '$u = -2+\\sqrt{7} \\approx 0.646 &gt; 0$ ✓  Keep.\n'
                     '$u = -2-\\sqrt{7} \\approx -4.646 &lt; 0$ ✗  Reject.'},
            {'title': 'Step 5 — Solve $4^x = \\sqrt{7}-2$ for $x$',
             'body': 'Take $\\ln$ of both sides:\n'
                     '$x \\ln 4 = \\ln(\\sqrt{7}-2)$\n'
                     '$x = \\dfrac{\\ln(\\sqrt{7}-2)}{\\ln 4} = \\dfrac{\\ln(\\sqrt{7}-2)}{2\\ln 2}$'},
            {'title': '✅ Check — verify (approximate)',
             'body': '$x \\approx \\dfrac{\\ln(0.646)}{\\ln 4} \\approx -0.317$\nConfirmed numerically. ✓'},
            _insight('Key simplification: $\\sqrt{28} = 2\\sqrt{7}$ — then cancel the 2 to get $u = -2 \\pm \\sqrt{7}$.'),
        ],
        'answer': '$x = \\dfrac{\\ln(\\sqrt{7}-2)}{2\\ln 2} \\approx -0.317$',
    },
    {
        'num': 62, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;9^x - 3^{x+1} + 1 = 0$',
        'steps': [
            {'title': 'Step 1 — Rewrite all terms in base 3',
             'body': '$9^x = (3^2)^x = (3^x)^2$\n$3^{x+1} = 3 \\cdot 3^x$\nEquation: $(3^x)^2 - 3 \\cdot 3^x + 1 = 0$'},
            {'title': 'Step 2 — Let $u = 3^x$ (substitution)',
             'body': '$u &gt; 0$. Equation: $u^2 - 3u + 1 = 0$'},
            {'title': 'Step 3 — Quadratic formula (does not factor)',
             'body': '$u = \\dfrac{3 \\pm \\sqrt{9-4}}{2} = \\dfrac{3 \\pm \\sqrt{5}}{2}$'},
            {'title': 'Step 4 — Both roots are positive (two valid solutions!)',
             'body': '$u_1 = \\dfrac{3+\\sqrt{5}}{2} \\approx 2.618 &gt; 0$ ✓\n'
                     '$u_2 = \\dfrac{3-\\sqrt{5}}{2} \\approx 0.382 &gt; 0$ ✓'},
            {'title': 'Step 5 — Solve for $x$ in each case',
             'body': 'Case 1: $3^x = \\dfrac{3+\\sqrt{5}}{2} \\Rightarrow x_1 = \\log_3\\!\\left(\\dfrac{3+\\sqrt{5}}{2}\\right)$\n'
                     'Case 2: $3^x = \\dfrac{3-\\sqrt{5}}{2} \\Rightarrow x_2 = \\log_3\\!\\left(\\dfrac{3-\\sqrt{5}}{2}\\right)$'},
            {'title': '✅ Check — verify (approximate)',
             'body': '$x_1 \\approx 0.859$ and $x_2 \\approx -0.859$ — both satisfy the original equation.'},
            _insight('This is rare — both quadratic roots are positive, giving TWO valid solutions.\n'
                     'Notice: $x_1 = -x_2$ (symmetric about $x=0$).'),
        ],
        'answer': '$x = \\log_3\\!\\left(\\dfrac{3 \\pm \\sqrt{5}}{2}\\right)$',
    },
    {
        'num': 63, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;6^x - 6 \\cdot 6^{-x} = -9$',
        'steps': [
            {'title': 'Step 1 — Eliminate the negative exponent',
             'body': 'Multiply every term by $6^x$ (valid since $6^x &gt; 0$):\n$(6^x)^2 - 6 = -9 \\cdot 6^x$'},
            {'title': 'Step 2 — Rearrange into standard form',
             'body': '$(6^x)^2 + 9 \\cdot 6^x - 6 = 0$'},
            {'title': 'Step 3 — Let $u = 6^x$ (substitution)',
             'body': '$u &gt; 0$. Equation: $u^2 + 9u - 6 = 0$'},
            {'title': 'Step 4 — Quadratic formula',
             'body': '$u = \\dfrac{-9 \\pm \\sqrt{81+24}}{2} = \\dfrac{-9 \\pm \\sqrt{105}}{2}$'},
            {'title': 'Step 5 — Reject invalid root',
             'body': '$\\sqrt{105} \\approx 10.247$\n'
                     '$u = \\dfrac{-9+\\sqrt{105}}{2} \\approx 0.624 &gt; 0$ ✓  Keep.\n'
                     '$u = \\dfrac{-9-\\sqrt{105}}{2} \\approx -9.624 &lt; 0$ ✗  Reject.'},
            {'title': 'Step 6 — Solve $6^x = \\dfrac{\\sqrt{105}-9}{2}$ for $x$',
             'body': '$x = \\log_6\\!\\left(\\dfrac{\\sqrt{105}-9}{2}\\right) = \\dfrac{\\ln\\!\\left(\\dfrac{\\sqrt{105}-9}{2}\\right)}{\\ln 6}$'},
            _insight('Trick: when $a^{-x}$ appears, multiply through by $a^x$ to clear the negative exponent.\n'
                     'This converts the equation into a quadratic in $a^x$.'),
        ],
        'answer': '$x = \\log_6\\!\\left(\\dfrac{\\sqrt{105}-9}{2}\\right)$',
    },
    {
        'num': 64, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;5^x - 8 \\cdot 5^{-x} = -16$',
        'steps': [
            {'title': 'Step 1 — Eliminate the negative exponent',
             'body': 'Multiply every term by $5^x$:\n$(5^x)^2 - 8 = -16 \\cdot 5^x$'},
            {'title': 'Step 2 — Rearrange into standard form',
             'body': '$(5^x)^2 + 16 \\cdot 5^x - 8 = 0$'},
            {'title': 'Step 3 — Let $u = 5^x$ (substitution)',
             'body': '$u &gt; 0$. Equation: $u^2 + 16u - 8 = 0$'},
            {'title': 'Step 4 — Quadratic formula with surd simplification',
             'body': '$u = \\dfrac{-16 \\pm \\sqrt{256+32}}{2} = \\dfrac{-16 \\pm \\sqrt{288}}{2}$\n'
                     'Simplify: $\\sqrt{288} = \\sqrt{144 \\cdot 2} = 12\\sqrt{2}$\n'
                     '$u = \\dfrac{-16 \\pm 12\\sqrt{2}}{2} = -8 \\pm 6\\sqrt{2}$'},
            {'title': 'Step 5 — Reject invalid root',
             'body': '$u = -8+6\\sqrt{2} \\approx 0.485 &gt; 0$ ✓  Keep.\n'
                     '$u = -8-6\\sqrt{2} &lt; 0$ ✗  Reject.'},
            {'title': 'Step 6 — Solve $5^x = 6\\sqrt{2}-8$ for $x$',
             'body': '$x = \\log_5(6\\sqrt{2}-8) = \\dfrac{\\ln(6\\sqrt{2}-8)}{\\ln 5}$'},
            _insight('Key simplification: $\\sqrt{288} = 12\\sqrt{2}$ (factor out $144 = 12^2$).\n'
                     'Then $\\dfrac{12\\sqrt{2}}{2} = 6\\sqrt{2}$ — always simplify surds fully.'),
        ],
        'answer': '$x = \\log_5(6\\sqrt{2}-8)$',
    },
    {
        'num': 65, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;2 \\cdot 49^x + 11 \\cdot 7^x + 5 = 0$',
        'steps': [
            {'title': 'Step 1 — Recognize the quadratic structure',
             'body': '$49^x = (7^2)^x = (7^x)^2$ — quadratic in $7^x$.'},
            {'title': 'Step 2 — Let $u = 7^x$ (substitution)',
             'body': '$u &gt; 0$. Equation: $2u^2 + 11u + 5 = 0$'},
            {'title': 'Step 3 — Factor the quadratic',
             'body': '$(2u+1)(u+5) = 0$\n$u = -\\dfrac{1}{2} \\quad$ or $\\quad u = -5$'},
            {'title': 'Step 4 — Reject both roots',
             'body': '$u = 7^x &gt; 0$ for all real $x$.\n'
                     'Both roots ($-\\tfrac{1}{2}$ and $-5$) are negative — neither is valid.'},
            {'title': 'Step 5 — Conclusion',
             'body': 'No real solution exists.'},
            _insight('When ALL quadratic roots are $\\leq 0$ (and base $&gt; 1$), there is NO real solution.\n'
                     'Spotting this quickly saves time on the exam.'),
        ],
        'answer': 'No real solution',
    },
    {
        'num': 66, 'badge': 'Exponential Equation',
        'given': 'Solve: $\\;3 \\cdot 4^x + 4 \\cdot 2^x + 8 = 0$',
        'steps': [
            {'title': 'Step 1 — Rewrite in a common base',
             'body': '$4^x = (2^2)^x = (2^x)^2$ — quadratic in $2^x$.'},
            {'title': 'Step 2 — Let $u = 2^x$ (substitution)',
             'body': '$u &gt; 0$. Equation: $3u^2 + 4u + 8 = 0$'},
            {'title': 'Step 3 — Compute the discriminant',
             'body': '$\\Delta = b^2 - 4ac = (4)^2 - 4(3)(8) = 16 - 96 = -80$'},
            {'title': 'Step 4 — Negative discriminant: no real roots',
             'body': '$\\Delta = -80 &lt; 0 \\Rightarrow$ the quadratic has no real solutions.\n'
                     'Therefore, no real $x$ satisfies the original equation.'},
            _insight('Always compute $\\Delta = b^2 - 4ac$ first.\n'
                     'If $\\Delta &lt; 0$: write "no real solution" immediately — saves exam time!'),
        ],
        'answer': 'No real solution ($\\Delta = -80 &lt; 0$)',
    },
    # ── Application Problems 105-107 ──────────────────────────────────────────
    {
        'num': 105, 'badge': 'Exponential Growth Application',
        'given': 'Population Model: $P(t) = 287(1.010)^{t-1999}$ (millions, year $t$)\n'
                 '(a) When will the population reach 307 million?\n'
                 '(b) When will the population reach 394 million?',
        'steps': [
            {'title': 'Part (a): Solve $287(1.010)^{t-1999} = 307$',
             'body': 'Step 1 — Divide both sides by 287:\n'
                     '$(1.010)^{t-1999} = \\dfrac{307}{287} \\approx 1.0697$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$\\ln\\left[(1.010)^{t-1999}\\right] = \\ln(1.0697)$\n'
                     '$(t-1999) \\ln(1.010) = \\ln(1.0697)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t - 1999 = \\dfrac{\\ln(1.0697)}{\\ln(1.010)} = \\dfrac{0.0674}{0.00995} \\approx 6.78$\n'
                     '$t \\approx 1999 + 6.78 = 2005.78$'},
            {'title': 'Step 4 — Interpret the result',
             'body': 'The population will reach 307 million during the year 2006.\n(More precisely, around October 2005.)'},
            {'title': 'Part (b): Solve $287(1.010)^{t-1999} = 394$',
             'body': 'Step 1 — Divide both sides by 287:\n'
                     '$(1.010)^{t-1999} = \\dfrac{394}{287} \\approx 1.3728$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$(t-1999) \\ln(1.010) = \\ln(1.3728)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t - 1999 = \\dfrac{\\ln(1.3728)}{\\ln(1.010)} = \\dfrac{0.3173}{0.00995} \\approx 31.9$\n'
                     '$t \\approx 1999 + 31.9 = 2030.9$'},
            {'title': 'Step 4 — Interpret the result',
             'body': 'The population will reach 394 million during the year 2031.'},
            _insight('For exponential growth models: divide to isolate the exponential, take $\\ln$,\n'
                     'then solve for time. Always round the year up if the decimal is positive.'),
        ],
        'answer': '(a) ≈ 2006  |  (b) ≈ 2031',
    },
    {
        'num': 106, 'badge': 'Exponential Growth Application',
        'given': 'World Population Model: $P(t) = 7.14(1.011)^{t-2014}$ (billions, year $t$)\n'
                 '(a) When will the population reach 9 billion?\n'
                 '(b) When will the population reach 12.5 billion?',
        'steps': [
            {'title': 'Part (a): Solve $7.14(1.011)^{t-2014} = 9$',
             'body': 'Step 1 — Divide both sides by 7.14:\n'
                     '$(1.011)^{t-2014} = \\dfrac{9}{7.14} \\approx 1.2605$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$(t-2014) \\ln(1.011) = \\ln(1.2605)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t - 2014 = \\dfrac{\\ln(1.2605)}{\\ln(1.011)} = \\dfrac{0.2317}{0.01095} \\approx 21.2$\n'
                     '$t \\approx 2014 + 21.2 = 2035.2$'},
            {'title': 'Step 4 — Interpret',
             'body': 'The world population will reach 9 billion during the year 2035.'},
            {'title': 'Part (b): Solve $7.14(1.011)^{t-2014} = 12.5$',
             'body': 'Step 1 — Divide both sides by 7.14:\n'
                     '$(1.011)^{t-2014} = \\dfrac{12.5}{7.14} \\approx 1.7507$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$(t-2014) \\ln(1.011) = \\ln(1.7507)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t - 2014 = \\dfrac{\\ln(1.7507)}{\\ln(1.011)} = \\dfrac{0.5596}{0.01095} \\approx 51.1$\n'
                     '$t \\approx 2014 + 51.1 = 2065.1$'},
            {'title': 'Step 4 — Interpret',
             'body': 'The world population will reach 12.5 billion during the year 2065.'},
            _insight('Similar pattern to Problem 105: isolate the base, take $\\ln$, solve.\n'
                     'Note: growth rate here (1.1% per year) is slightly faster than Problem 105 (1.0%).'),
        ],
        'answer': '(a) ≈ 2035  |  (b) ≈ 2065',
    },
    {
        'num': 107, 'badge': 'Exponential Decay Application',
        'given': 'Car Depreciation Model: $V(t) = 14,162(0.83)^t$ (dollars, year $t$)\n'
                 '(a) When will the car be worth $8000?\n'
                 '(b) When will the car be worth $3000?\n'
                 '(c) When will the car be worth $1000?',
        'steps': [
            {'title': 'Part (a): Solve $14,162(0.83)^t = 8000$',
             'body': 'Step 1 — Divide both sides by 14,162:\n'
                     '$(0.83)^t = \\dfrac{8000}{14162} \\approx 0.5646$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$t \\ln(0.83) = \\ln(0.5646)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t = \\dfrac{\\ln(0.5646)}{\\ln(0.83)} = \\dfrac{-0.5738}{-0.1863} \\approx 3.08$ years'},
            {'title': 'Part (b): Solve $14,162(0.83)^t = 3000$',
             'body': 'Step 1 — Divide both sides by 14,162:\n'
                     '$(0.83)^t = \\dfrac{3000}{14162} \\approx 0.2119$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$t \\ln(0.83) = \\ln(0.2119)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t = \\dfrac{\\ln(0.2119)}{\\ln(0.83)} = \\dfrac{-1.5507}{-0.1863} \\approx 8.32$ years'},
            {'title': 'Part (c): Solve $14,162(0.83)^t = 1000$',
             'body': 'Step 1 — Divide both sides by 14,162:\n'
                     '$(0.83)^t = \\dfrac{1000}{14162} \\approx 0.0707$'},
            {'title': 'Step 2 — Take $\\ln$ of both sides',
             'body': '$t \\ln(0.83) = \\ln(0.0707)$'},
            {'title': 'Step 3 — Solve for $t$',
             'body': '$t = \\dfrac{\\ln(0.0707)}{\\ln(0.83)} = \\dfrac{-2.6478}{-0.1863} \\approx 14.22$ years'},
            {'title': 'Summary of Results',
             'body': 'At 17% depreciation per year (factor 0.83):\n'
                     '• Car worth $8,000 after ≈ 3.1 years\n'
                     '• Car worth $3,000 after ≈ 8.3 years\n'
                     '• Car worth $1,000 after ≈ 14.2 years'},
            _insight('For decay models with $0 &lt; b &lt; 1$: the $\\ln$ of the base is negative,\n'
                     'so dividing by it flips the sign. The fraction decreases as $t$ increases.'),
        ],
        'answer': '(a) ≈ 3.1 years  |  (b) ≈ 8.3 years  |  (c) ≈ 14.2 years',
    },
]

# ─── old helper stubs (no longer called, kept for safety) ───────────────────
def log_eq_prob(*args): pass
def exp_eq_sub_prob(*args): pass


CFG_5_6 = {
    'section_label': '5.6',
    'section_name': 'Logarithmic and Exponential Equations',
    'folder': '5.6',
    'fname': 'section_5_6.html',
    'groups': [
        {'title': 'Logarithmic Equations', 'probs': list(range(15, 31))},
        {'title': 'Exponential Equations', 'probs': list(range(57, 67))},
        {'title': 'Applications and Extensions', 'probs': [105, 106, 107]},
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
