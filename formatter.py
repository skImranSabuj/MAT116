from __future__ import annotations
"""
formatter.py
------------
Converts solver output (list of solution dicts) into:
  • Markdown (.md) files  – GitHub-renderable, with LaTeX math fences
  • HTML (.html) file     – standalone page with MathJax, ready for GitHub Pages

Public API:
    formatter = Formatter(output_dir="4.1")
    formatter.write_markdown(solutions, filename="section_4_1_part1.md", title="Section 4.1 – Part 1")
    formatter.write_html(solutions, filename="section_4_1.html", section="4.1")
"""

import os
import re
import logging
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)

# ── constants ─────────────────────────────────────────────────────────────────

PROBLEM_TYPE_LABELS = {
    "transformation":   "Graphing with Transformations",
    "form_polynomial":  "Form a Polynomial",
    "analysis":         "Polynomial Analysis",
    "application":      "Application Problem",
    "generic":          "General Problem",
}

# ── helper ────────────────────────────────────────────────────────────────────

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _latex_to_md(text: str) -> str:
    """
    GitHub Markdown doesn't render LaTeX natively, but many renderers (and
    our HTML output) use MathJax / KaTeX.  We keep dollar-sign math as-is
    for the .md files so they render correctly in editors like VS Code with
    the Markdown+Math extension, and in our HTML export.
    """
    return text


# ── Markdown formatter ────────────────────────────────────────────────────────

class Formatter:
    """Handles all output generation."""

    def __init__(self, output_dir: str = "4.1", template_dir: str = "templates"):
        self.output_dir   = output_dir
        self.template_dir = template_dir
        _ensure_dir(output_dir)

    # ── Markdown ──────────────────────────────────────────────────────────────

    def write_markdown(
        self,
        solutions: list[dict],
        filename: str,
        title: str = "Section 4.1 Solutions",
        section: str = "4.1",
    ) -> str:
        """
        Write *solutions* to a Markdown file inside *output_dir*.
        Returns the full path of the written file.
        """
        lines: list[str] = []

        # ── front-matter header ───────────────────────────────────────────
        lines += [
            f"# {title}",
            "",
            f"> **Course:** MAT 116 — Precalculus  ",
            f"> **Textbook:** Sullivan *Precalculus* 10th Edition  ",
            f"> **Section:** {section}  ",
            f"> **Generated:** {date.today().strftime('%B %d, %Y')}",
            "",
            "---",
            "",
        ]

        # ── one block per problem ─────────────────────────────────────────
        for sol in solutions:
            num      = sol["number"]
            question = sol["question"]
            ptype    = sol.get("type", "generic")
            steps    = sol.get("steps", [])
            answer   = sol.get("answer", "")

            type_label = PROBLEM_TYPE_LABELS.get(ptype, ptype.title())

            lines += [
                f"## Problem {num}",
                "",
                f"**Type:** {type_label}  ",
                "",
                "### Given",
                "",
                self._blockquote(question),
                "",
            ]

            for step in steps:
                lines += [
                    f"### {step['title']}",
                    "",
                    step["body"],
                    "",
                ]

            if answer:
                lines += [
                    "### Final Answer",
                    "",
                    f"> {answer}",
                    "",
                ]

            lines += ["---", ""]

        content = "\n".join(lines)
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        logger.info(f"Markdown written → {path}")
        return path

    # ── HTML ─────────────────────────────────────────────────────────────────

    def write_html(
        self,
        solutions: list[dict],
        filename: str = "section_4_1.html",
        section: str = "4.1",
        title: str = "Section 4.1 Solutions",
    ) -> str:
        """
        Write a standalone, MathJax-enabled HTML page.
        Returns the full path of the written file.
        """
        # Load Jinja2 template if available, else use built-in fallback
        try:
            from jinja2 import Environment, FileSystemLoader, select_autoescape

            env = Environment(
                loader=FileSystemLoader(self.template_dir),
                autoescape=select_autoescape(["html"]),
            )
            template = env.get_template("base.html")
            html = template.render(
                title=title,
                section=section,
                solutions=solutions,
                type_labels=PROBLEM_TYPE_LABELS,
                generated=date.today().strftime("%B %d, %Y"),
            )
        except Exception as e:
            logger.warning(f"Jinja2 template failed ({e}); using built-in HTML builder.")
            html = self._build_html(solutions, title, section)

        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        logger.info(f"HTML written → {path}")
        return path

    # ── built-in HTML builder (no Jinja2 required) ────────────────────────────

    def _build_html(self, solutions: list[dict], title: str, section: str) -> str:
        """Pure-Python HTML builder — no external template needed."""
        head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{self._esc(title)}</title>

  <!-- MathJax — renders LaTeX math expressions -->
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath:  [['$','$'], ['\\\\(','\\\\)']],
        displayMath: [['$$','$$'], ['\\\\[','\\\\]']],
        processEscapes: true
      }},
      options: {{ skipHtmlTags: ['script','noscript','style','textarea'] }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

  <style>
    /* ── Reset & base ─────────────────────────────── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ font-size: 16px; }}
    body {{
      font-family: 'Georgia', 'Times New Roman', serif;
      line-height: 1.75;
      color: #1a1a2e;
      background: #f8f9fa;
      padding: 0 1rem 4rem;
    }}

    /* ── Layout ───────────────────────────────────── */
    .container {{
      max-width: 860px;
      margin: 0 auto;
      background: #ffffff;
      padding: 2.5rem 3rem;
      border-radius: 8px;
      box-shadow: 0 2px 16px rgba(0,0,0,.08);
    }}

    /* ── Typography ───────────────────────────────── */
    h1 {{
      font-size: 2rem;
      color: #16213e;
      border-bottom: 3px solid #0f3460;
      padding-bottom: .5rem;
      margin-bottom: .25rem;
    }}
    .subtitle {{
      font-size: .9rem;
      color: #555;
      margin-bottom: 2rem;
    }}
    h2 {{
      font-size: 1.45rem;
      color: #0f3460;
      border-left: 5px solid #e94560;
      padding-left: .75rem;
      margin: 2.5rem 0 .75rem;
    }}
    h3 {{
      font-size: 1.1rem;
      color: #16213e;
      margin: 1.2rem 0 .4rem;
      font-style: italic;
    }}

    /* ── Problem cards ────────────────────────────── */
    .problem {{
      border: 1px solid #e0e0e0;
      border-radius: 6px;
      padding: 1.5rem 2rem;
      margin: 2rem 0;
      background: #fff;
    }}
    .problem-type {{
      display: inline-block;
      background: #0f3460;
      color: #fff;
      font-size: .75rem;
      font-weight: bold;
      letter-spacing: .05em;
      text-transform: uppercase;
      border-radius: 3px;
      padding: .15rem .6rem;
      margin-bottom: 1rem;
    }}
    .given-box {{
      background: #f0f4ff;
      border-left: 4px solid #0f3460;
      border-radius: 4px;
      padding: .75rem 1rem;
      margin: .5rem 0 1.25rem;
      font-family: 'Courier New', monospace;
      font-size: .95rem;
    }}

    /* ── Steps ────────────────────────────────────── */
    .step {{
      margin: 1rem 0;
      padding: .75rem 1rem;
      background: #f9f9f9;
      border-radius: 4px;
      border: 1px solid #eaeaea;
    }}
    .step-title {{
      font-weight: bold;
      color: #0f3460;
      margin-bottom: .4rem;
    }}
    .step-body {{
      white-space: pre-wrap;
    }}

    /* ── Answer box ───────────────────────────────── */
    .answer-box {{
      background: #e8f5e9;
      border: 1px solid #a5d6a7;
      border-radius: 6px;
      padding: .75rem 1.25rem;
      margin-top: 1rem;
    }}
    .answer-box strong {{ color: #2e7d32; }}

    /* ── Navigation / ToC ─────────────────────────── */
    .toc {{
      background: #f0f4ff;
      border: 1px solid #c5cae9;
      border-radius: 6px;
      padding: 1.25rem 1.75rem;
      margin-bottom: 2.5rem;
    }}
    .toc h2 {{ border: none; padding: 0; margin: 0 0 .75rem; font-size: 1.15rem; }}
    .toc ul {{ list-style: disc; padding-left: 1.25rem; columns: 2; }}
    .toc a {{ color: #0f3460; text-decoration: none; }}
    .toc a:hover {{ text-decoration: underline; }}

    /* ── divider ──────────────────────────────────── */
    hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 2rem 0; }}

    /* ── code ─────────────────────────────────────── */
    code {{
      background: #f4f4f4;
      font-family: 'Courier New', monospace;
      padding: .1em .35em;
      border-radius: 3px;
      font-size: .9em;
    }}
  </style>
</head>
<body>
<div class="container">
"""

        gen_date = date.today().strftime("%B %d, %Y")
        body_top = f"""
  <h1>{self._esc(title)}</h1>
  <p class="subtitle">
    MAT 116 — Precalculus &nbsp;|&nbsp;
    Sullivan <em>Precalculus</em> 10th Edition &nbsp;|&nbsp;
    Section {self._esc(section)} &nbsp;|&nbsp;
    Generated: {gen_date}
  </p>

  <!-- Table of Contents -->
  <nav class="toc">
    <h2>Problems in This File</h2>
    <ul>
"""
        toc_items = "".join(
            f'      <li><a href="#prob-{s["number"]}">Problem {s["number"]}</a></li>\n'
            for s in solutions
        )
        body_top += toc_items + """    </ul>
  </nav>
"""

        problem_blocks = []
        for sol in solutions:
            num        = sol["number"]
            question   = sol["question"]
            ptype      = sol.get("type", "generic")
            steps      = sol.get("steps", [])
            answer     = sol.get("answer", "")
            type_label = PROBLEM_TYPE_LABELS.get(ptype, ptype.title())

            # Build step HTML
            steps_html = ""
            for step in steps:
                steps_html += (
                    f'      <div class="step">\n'
                    f'        <div class="step-title">{self._esc(step["title"])}</div>\n'
                    f'        <div class="step-body">{self._md_to_html(step["body"])}</div>\n'
                    f'      </div>\n'
                )

            answer_html = ""
            if answer:
                answer_html = (
                    f'      <div class="answer-box">'
                    f'<strong>Final Answer:</strong> {self._md_to_html(answer)}'
                    f'</div>\n'
                )

            problem_blocks.append(
                f'  <div class="problem" id="prob-{num}">\n'
                f'    <h2>Problem {num}</h2>\n'
                f'    <span class="problem-type">{self._esc(type_label)}</span>\n'
                f'    <h3>Given</h3>\n'
                f'    <div class="given-box">{self._md_to_html(question)}</div>\n'
                + steps_html
                + answer_html
                + f'  </div>\n'
                f'  <hr />\n'
            )

        foot = """</div>
</body>
</html>
"""
        return head + body_top + "\n".join(problem_blocks) + foot

    # ── utilities ─────────────────────────────────────────────────────────────

    @staticmethod
    def _esc(text: str) -> str:
        """Minimal HTML escaping (does NOT escape math — MathJax handles it)."""
        return (
            text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )

    @staticmethod
    def _blockquote(text: str) -> str:
        """Prefix every line of *text* with '> ' for Markdown blockquote."""
        lines = text.strip().splitlines()
        return "\n".join(f"> {line}" if line.strip() else ">" for line in lines)

    @staticmethod
    def _md_to_html(text: str) -> str:
        """
        Lightweight Markdown-to-HTML converter for step bodies.
        Handles: **bold**, *italic*, `code`, numbered lists, bullet lists,
        and raw LaTeX (left alone for MathJax).
        Converts newlines to <br> for pre-wrap display.
        """
        # Bold / italic
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*",     r"<em>\1</em>",         text)
        # Inline code
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        # Preserve \n for CSS pre-wrap
        return text
