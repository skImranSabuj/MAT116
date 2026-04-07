# MAT116 — Precalculus Solutions Generator

> **Course:** MAT 116 — Precalculus  
> **Textbook:** Sullivan _Precalculus_ 10th Edition  
> **Focus:** Section 4.1 — Polynomial Functions and Models

Automatically extracts exercise problems from a Sullivan Precalculus PDF, classifies each problem type, and generates detailed **step-by-step solutions** written in a "top student" exam style — complete with LaTeX math, transformation analysis, polynomial construction, and end-behavior explanations.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [CLI Usage](#cli-usage)
- [Output files](#output-files)
- [How to Upload to GitHub](#how-to-upload-to-github)
- [How to Enable GitHub Pages](#how-to-enable-github-pages)
- [Extending the Project](#extending-the-project)

---

## Features

| Capability                 | Detail                                                                                       |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **PDF parsing**            | Reads any Sullivan Precalculus PDF (PyMuPDF); falls back to built-in sample data             |
| **Problem classification** | Detects 4 types: Transformation · Form Polynomial · Analysis · Application                   |
| **Transformation solver**  | Parses `a(x ± h)ⁿ + k`; explains every shift, stretch, reflection, key point & end behavior  |
| **Polynomial builder**     | Converts zeros + multiplicity → factored form → fully expanded polynomial (via SymPy)        |
| **Polynomial analysis**    | Finds zeros, multiplicities, y-intercept, end behavior, max turning points                   |
| **Application problems**   | Detailed setups for box-volume, revenue, fence, projectile, population, cone & wire problems |
| **Markdown output**        | GitHub-renderable `.md` with LaTeX math (renders in VS Code + GitHub)                        |
| **HTML output**            | Standalone page with **MathJax** — ready for GitHub Pages                                    |

---

## Project Structure

```
MAT116/
├── main.py              ← entry point / CLI
├── parser.py            ← PDF text extraction & problem detection
├── solver.py            ← step-by-step solution generator
├── formatter.py         ← Markdown & HTML writer
├── sample_data.py       ← hand-coded Section 4.1 problems (fallback)
├── requirements.txt     ← Python dependencies
├── templates/
│   └── base.html        ← Jinja2 HTML template with MathJax
└── 4.1/                 ← generated output files
    ├── section_4_1_transformations.md
    ├── section_4_1_form_polynomial.md
    ├── section_4_1_analysis.md
    ├── section_4_1_applications.md
    ├── section_4_1_all.md
    └── section_4_1.html  ← GitHub Pages entry point
```

---

## Quick Start

### 1. Install dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### 2. Run with the included PDF

```bash
python main.py
```

This reads `Precalculus-Sullivan 10th edition.pdf`, extracts Section 4.1 problems **37-42, 43-50, 51-56, 57-68, 81-90**, generates solutions, and writes all output files to the `4.1/` folder.

### 3. Skip the PDF (use built-in sample data)

```bash
python main.py --no-pdf
```

---

## CLI Usage

```
python main.py [OPTIONS]

Options:
  --pdf PATH          Path to the PDF textbook
                      Default: Precalculus-Sullivan 10th edition.pdf

  --section SECTION   Section to process (e.g. 4.1)
                      Default: 4.1

  --problems RANGES   Comma-separated problem ranges
                      Default: 37-42,43-50,51-56,57-68,81-90

  --no-pdf            Skip PDF parsing, use built-in sample data only

  --output-dir DIR    Output directory
                      Default: 4.1/

  -v, --verbose       Enable debug logging
```

### Examples

```bash
# Just transformation problems (37-42)
python main.py --section 4.1 --problems "37-42"

# All ranges, verbose output
python main.py -v

# Different PDF location
python main.py --pdf ~/Downloads/sullivan_precalc.pdf --section 4.1
```

---

## Output Files

After running, the `4.1/` directory contains:

| File                             | Contents                                            |
| -------------------------------- | --------------------------------------------------- |
| `section_4_1_transformations.md` | Problems 37–50 (graphing with transformations)      |
| `section_4_1_form_polynomial.md` | Problems 51–56 (form polynomial from zeros)         |
| `section_4_1_analysis.md`        | Problems 57–68 (analyze polynomial functions)       |
| `section_4_1_applications.md`    | Problems 81–90 (application / word problems)        |
| `section_4_1_all.md`             | All problems combined in one Markdown file          |
| `section_4_1.html`               | **All problems** in a single HTML page with MathJax |

### Markdown preview

Open any `.md` file in VS Code — install the
[Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
extension for full LaTeX rendering.

### HTML preview

Open `4.1/section_4_1.html` in any web browser. MathJax loads from a CDN so  
you need an internet connection on first open.

---

## How to Upload to GitHub

```bash
# 1. Initialise a Git repository (once)
cd /path/to/MAT116
git init
git add .
git commit -m "Initial commit: MAT116 Section 4.1 solutions"

# 2. Create a repo on GitHub (github.com → New repository → MAT116)
#    Then link and push:
git remote add origin https://github.com/<your-username>/MAT116.git
git branch -M main
git push -u origin main
```

---

## How to Enable GitHub Pages

1. Go to your repository on **github.com**
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source** select **Deploy from a branch**
4. Choose **Branch: `main`**, folder: **`/ (root)`**
5. Click **Save**

GitHub will give you a URL like:

```
https://<your-username>.github.io/MAT116/4.1/section_4_1.html
```

That URL is your live, shareable solution page. 🎉

> **Tip:** Add a `docs/` folder and copy `section_4_1.html` there if you  
> prefer the cleaner `https://<user>.github.io/MAT116/` root URL.

---

## Extending the Project

### Add another section

```bash
python main.py --section 4.2 --problems "1-20,45-60"
```

### Add new problem types

Edit `solver.py`:

1. Add a new classifier pattern (e.g., `_RATIONAL_RE`)
2. Add a `_solve_rational()` method with step-by-step logic
3. Route it in `Solver.solve()`

### Add more sample data

Edit `sample_data.py` and append to `SECTION_4_1_PROBLEMS`.  
Keep the same `{"number": int, "question": str}` structure.

---

## Dependencies

| Package  | Version | Purpose                                      |
| -------- | ------- | -------------------------------------------- |
| PyMuPDF  | ≥ 1.23  | PDF text extraction                          |
| SymPy    | ≥ 1.12  | Symbolic polynomial expansion & root finding |
| Jinja2   | ≥ 3.1   | HTML templating                              |
| markdown | ≥ 3.5   | Markdown utilities (optional)                |

---

_Generated for MAT116 · April 2026_
