from __future__ import annotations
"""
solver.py  –  Step-by-step solution engine for Section 4.1
Each solution is written exactly as a top student would write it
in an exam: clear numbered steps, every algebra move shown.
"""

import re
import logging
from typing import Union

logger = logging.getLogger(__name__)

# ── tiny helpers ───────────────────────────────────────────────────────────────

def _end_behavior_text(degree: int, lc: float) -> str:
    even = (degree % 2 == 0)
    pos  = (lc > 0)
    if even and pos:
        return (r"As $x \to -\infty,\ f(x) \to +\infty$ "
                r"and as $x \to +\infty,\ f(x) \to +\infty$  "
                r"(graph rises on both sides, like $\cup$).")
    if even and not pos:
        return (r"As $x \to -\infty,\ f(x) \to -\infty$ "
                r"and as $x \to +\infty,\ f(x) \to -\infty$  "
                r"(graph falls on both sides, like $\cap$).")
    if not even and pos:
        return (r"As $x \to -\infty,\ f(x) \to -\infty$ "
                r"and as $x \to +\infty,\ f(x) \to +\infty$  "
                r"(falls to the left, rises to the right).")
    return (r"As $x \to -\infty,\ f(x) \to +\infty$ "
            r"and as $x \to +\infty,\ f(x) \to -\infty$  "
            r"(rises to the left, falls to the right).")


def _cross_touch(mult: int) -> str:
    if mult % 2 == 1:
        return "**crosses** the x-axis (odd multiplicity)"
    return "**touches** the x-axis and turns back (even multiplicity)"


def _fmt_zero(z) -> str:
    """Pretty-print a sympy Rational / Integer / float zero."""
    s = str(z)
    # replace Rational display like "1/3" → already fine
    return s


# ══════════════════════════════════════════════════════════════════════════════
class Solver:

    def solve(self, problem: dict) -> dict:
        ptype = problem.get("type", "generic")
        meta  = problem.get("meta", {})
        num   = problem["number"]
        q     = problem["question"]

        dispatch = {
            "transformation":         self._transformation,
            "form_polynomial":         self._form_polynomial,
            "form_polynomial_point":   self._form_polynomial_point,
            "analysis":                self._analysis,
            "analysis_full":           self._analysis_full,
        }
        fn = dispatch.get(ptype, self._generic)
        steps, answer = fn(num, q, meta)

        return {"number": num, "question": q, "type": ptype,
                "steps": steps, "answer": answer}

    # ══════════════════════════════════════════════════════════════════════════
    # 1. TRANSFORMATION PROBLEMS (37-42)
    # ══════════════════════════════════════════════════════════════════════════

    def _transformation(self, num: int, q: str, meta: dict) -> tuple:
        a = meta.get("a", 1)
        h = meta.get("h", 0)   # actual horizontal shift (right = +, left = -)
        n = meta.get("n", 4)
        k = meta.get("k", 0)

        even = (n % 2 == 0)
        key_name = "vertex" if even else "inflection point"

        # ── describe each transformation ──────────────────────────────────
        transforms = []
        if a < 0:
            transforms.append(f"Reflect over the x-axis (multiply by $-1$).")
        if abs(a) != 1:
            if abs(a) > 1:
                transforms.append(f"Vertically **stretch** by factor $|a| = {abs(a)}$.")
            else:
                transforms.append(f"Vertically **compress** by factor $|a| = {abs(a)}$.")
        if h != 0:
            direction = "right" if h > 0 else "left"
            inside_sign = "-" if h > 0 else "+"
            transforms.append(
                f"Shift **{abs(h)} unit(s) to the {direction}** "
                f"(factor is $(x {inside_sign} {abs(h)})$)."
            )
        if k != 0:
            direction = "up" if k > 0 else "down"
            transforms.append(f"Shift **{abs(k)} unit(s) {direction}**.")
        if not transforms:
            transforms.append("No transformation — this is the parent function itself.")

        # ── y-intercept ───────────────────────────────────────────────────
        y_int = a * (0 - h)**n + k
        y_int_str = (f"{int(y_int)}" if y_int == int(y_int) else f"{y_int:.4g}")

        steps = [
            {
                "title": "Step 1 — Write Down the Standard Form",
                "body": (
                    r"Any polynomial of the form $f(x) = a(x-h)^n + k$ is a "
                    r"**transformation** of the parent $y = x^n$." "\n\n"
                    f"For the given function, identify:\n"
                    f"- $a = {a}$ (vertical scaling / reflection)\n"
                    f"- $h = {h}$ (horizontal shift)\n"
                    f"- $n = {n}$ (degree / shape)\n"
                    f"- $k = {k}$ (vertical shift)"
                ),
            },
            {
                "title": "Step 2 — Identify the Parent Function",
                "body": (
                    f"Remove $a$, $h$, and $k$ and look at the bare power:\n\n"
                    f"$$y = x^{{{n}}}$$\n\n"
                    + (
                        f"This is an **even-degree** power function.  "
                        f"Its graph is U-shaped, symmetric about the y-axis, "
                        f"with a minimum at the origin."
                        if even else
                        f"This is an **odd-degree** power function.  "
                        f"Its graph is S-shaped (like a cubic), "
                        f"with an inflection point at the origin."
                    )
                ),
            },
            {
                "title": "Step 3 — List Every Transformation (Apply in Order)",
                "body": (
                    "Apply each transformation **one at a time**, in this order: "
                    "reflect → stretch/compress → horizontal shift → vertical shift.\n\n"
                    + "\n".join(f"{i+1}. {t}" for i, t in enumerate(transforms))
                ),
            },
            {
                "title": f"Step 4 — Locate the Key Point ({key_name.title()})",
                "body": (
                    f"The parent's key point is at $(0,\\ 0)$.\n\n"
                    f"After the horizontal shift by $h = {h}$ and vertical shift by $k = {k}$:\n\n"
                    f"$$\\text{{{key_name.title()}}} = ({h},\\ {k})$$\n\n"
                    + (
                        f"This is the **{'minimum' if a > 0 else 'maximum'}** of the graph."
                        if even else
                        f"This is the **inflection point** of the graph "
                        f"(where the graph changes concavity)."
                    )
                ),
            },
            {
                "title": "Step 5 — End Behavior",
                "body": _end_behavior_text(n, a),
            },
            {
                "title": "Step 6 — y-intercept",
                "body": (
                    r"Substitute $x = 0$ into $f(x)$:" "\n\n"
                    f"$$f(0) = {a}(0 - ({h}))^{{{n}}} + {k} = {y_int_str}$$\n\n"
                    f"So the y-intercept is $(0,\\ {y_int_str})$."
                ),
            },
            {
                "title": "Step 7 — Sketch Notes",
                "body": (
                    f"1. Plot the {key_name} at $({h},\\ {k})$.\n"
                    f"2. Plot the y-intercept at $(0,\\ {y_int_str})$.\n"
                    "3. Use the end-behavior arrows from Step 5.\n"
                    + (
                        f"4. The graph is symmetric about the vertical line $x = {h}$."
                        if even else
                        f"4. The graph has 180° rotational symmetry about $({h},\\ {k})$."
                    )
                ),
            },
        ]

        answer = (
            f"Parent: $y = x^{{{n}}}$.  "
            f"{key_name.title()}: $({h},\\ {k})$.  "
            f"y-intercept: $(0,\\ {y_int_str})$.  "
            + _end_behavior_text(n, a)
        )
        return steps, answer

    # ══════════════════════════════════════════════════════════════════════════
    # 2. FORM POLYNOMIAL FROM ZEROS (43-50)
    # ══════════════════════════════════════════════════════════════════════════

    def _form_polynomial(self, num: int, q: str, meta: dict) -> tuple:
        zeros  = meta.get("zeros", [])   # list of (value, multiplicity)
        degree = meta.get("degree", None)

        # Build factor strings for display
        factor_parts = []
        for z, m in zeros:
            if z == 0:
                f_str = "x"
            elif z < 0:
                f_str = f"(x + {abs(z)})"
            else:
                f_str = f"(x - {z})"
            if m > 1:
                f_str += f"^{{{m}}}"
            factor_parts.append((f_str, z, m))

        factored = r" \cdot ".join(p[0] for p in factor_parts)

        # Expand using sympy
        expanded_str = ""
        try:
            from sympy import symbols, expand, Rational
            x = symbols("x")
            expr = 1
            for z, m in zeros:
                if isinstance(z, float) and z != int(z):
                    zv = Rational(z).limit_denominator(100)
                else:
                    zv = int(z)
                expr *= (x - zv)**m
            expanded_str = str(expand(expr)).replace("**","^").replace("*","")
        except Exception:
            expanded_str = "(expand manually)"

        steps = [
            {
                "title": "Step 1 — Recall the Factor Theorem",
                "body": (
                    "The **Factor Theorem** states:\n\n"
                    r"> If $r$ is a zero of polynomial $f(x)$, then $(x - r)$ is a factor." "\n\n"
                    r"If $r$ has **multiplicity $m$**, then $(x - r)^m$ is a factor."
                ),
            },
            {
                "title": "Step 2 — Write One Factor for Each Zero",
                "body": (
                    "From the given zeros, build the factors:\n\n"
                    + "\n".join(
                        f"- Zero $x = {z}$ with multiplicity ${m}$ "
                        f"$\\Rightarrow$ factor $({p})$"
                        for p, z, m in factor_parts
                    )
                ),
            },
            {
                "title": "Step 3 — Write in Factored Form (use $a = 1$)",
                "body": (
                    r"With leading coefficient $a = 1$:" "\n\n"
                    f"$$f(x) = {factored}$$"
                ),
            },
            {
                "title": "Step 4 — Expand to Standard Form",
                "body": (
                    "Multiply out all factors (use FOIL / distributive property):\n\n"
                    f"$$f(x) = {expanded_str}$$"
                ),
            },
            {
                "title": "Step 5 — Verify Degree",
                "body": (
                    f"The highest power of $x$ in the expanded form gives the degree.\n\n"
                    + (f"**Degree = {degree}** ✓" if degree else "Check that degree matches.")
                ),
            },
        ]

        answer = f"$f(x) = {factored} = {expanded_str}$"
        return steps, answer

    # ══════════════════════════════════════════════════════════════════════════
    # 3. FORM POLYNOMIAL PASSING THROUGH A POINT (51-56)
    # ══════════════════════════════════════════════════════════════════════════

    def _form_polynomial_point(self, num: int, q: str, meta: dict) -> tuple:
        zeros = meta.get("zeros", [])
        point = meta.get("point", (1, 1))
        px, py = point

        factor_parts = []
        for z, m in zeros:
            if z == 0:
                f_str = "x"
            elif z < 0:
                f_str = f"(x + {abs(z)})"
            else:
                f_str = f"(x - {z})"
            if m > 1:
                f_str += f"^{{{m}}}"
            factor_parts.append((f_str, z, m))
        factored_base = r" \cdot ".join(p[0] for p in factor_parts)

        # Evaluate the base polynomial at px
        try:
            from sympy import symbols, Rational, expand, nsimplify
            x = symbols("x")
            expr_unit = 1
            for z, m in zeros:
                zv = Rational(z).limit_denominator(100) if isinstance(z, float) else int(z)
                expr_unit *= (x - zv)**m
            pxv = Rational(px).limit_denominator(100) if isinstance(px, float) else int(px)
            base_at_px_sym = expr_unit.subs(x, pxv)
            base_at_px = float(base_at_px_sym.evalf())
            if base_at_px_sym != 0:
                pyv = Rational(py).limit_denominator(100) if isinstance(py, float) else int(py)
                a_val_sym = pyv / base_at_px_sym
                a_val = float(a_val_sym.evalf())
            else:
                a_val_sym = None
                a_val = None
            expanded_final = (
                str(expand(a_val_sym * expr_unit))
                .replace("**","^").replace("*x","x")
                if a_val_sym else "undefined"
            )
        except Exception:
            base_at_px = None
            a_val = None
            a_val_sym = None
            expanded_final = "(compute manually)"

        px_str = f"{int(px)}" if px == int(px) else f"{px}"
        py_str = f"{int(py)}" if py == int(py) else f"{py}"
        base_str = (f"{int(base_at_px)}" if base_at_px is not None and base_at_px == int(base_at_px)
                    else f"{base_at_px:.4g}" if base_at_px is not None else "?")

        if a_val_sym is not None:
            a_str = str(a_val_sym)  # sympy rational displays as -1/3, 2, etc.
        else:
            a_str = "?"

        steps = [
            {
                "title": "Step 1 — Write the General Form with Unknown Leading Coefficient",
                "body": (
                    r"Since the zeros are fixed but the leading coefficient $a$ is unknown, write:" "\n\n"
                    f"$$f(x) = a \\cdot {factored_base}$$"
                ),
            },
            {
                "title": "Step 2 — Substitute the Given Point to Solve for $a$",
                "body": (
                    f"The graph passes through $({px_str},\\ {py_str})$, so $f({px_str}) = {py_str}$.\n\n"
                    f"Substitute $x = {px_str}$ into the base (without $a$):\n\n"
                    f"$$\\text{{Base at }} x={px_str}: \\quad {factored_base}\\Big|_{{x={px_str}}} = {base_str}$$\n\n"
                    f"Therefore:\n$$a \\cdot {base_str} = {py_str}$$\n$$a = \\frac{{{py_str}}}{{{base_str}}} = {a_str}$$"
                ),
            },
            {
                "title": "Step 3 — Write the Final Factored Form",
                "body": (
                    f"$$f(x) = {a_str}({factored_base})$$"
                ),
            },
            {
                "title": "Step 4 — Expand to Standard Form",
                "body": (
                    f"$$f(x) = {expanded_final}$$"
                ),
            },
            {
                "title": "Step 5 — Verify",
                "body": (
                    f"Check: substitute the given point $({px_str},\\ {py_str})$:\n\n"
                    f"$$f({px_str}) = {a_str} \\cdot {base_str} = {py_str} \\checkmark$$"
                ),
            },
        ]

        answer = f"$f(x) = {a_str}({factored_base}) = {expanded_final}$"
        return steps, answer

    # ══════════════════════════════════════════════════════════════════════════
    # 4. ANALYSIS – 57-68 (zeros, cross/touch, turning pts, end behavior)
    # ══════════════════════════════════════════════════════════════════════════

    def _analysis(self, num: int, q: str, meta: dict) -> tuple:
        """
        Parse the factored polynomial from the question string and produce
        a full pencil-and-paper analysis.
        """
        steps, answer = self._run_sympy_analysis(q, full=False)
        return steps, answer

    # ══════════════════════════════════════════════════════════════════════════
    # 5. FULL ANALYSIS – 81-90 (Steps 1-5 from p.215)
    # ══════════════════════════════════════════════════════════════════════════

    def _analysis_full(self, num: int, q: str, meta: dict) -> tuple:
        steps, answer = self._run_sympy_analysis(q, full=True)
        return steps, answer

    # ── shared sympy analysis engine ──────────────────────────────────────────

    def _run_sympy_analysis(self, q: str, full: bool) -> tuple:
        """
        Core polynomial analysis used by both _analysis and _analysis_full.
        Parses f(x) from the question string, then produces step-by-step work.
        """
        # Extract "f(x) = <expr>" from the question
        expr_m = re.search(r"f\s*\(\s*x\s*\)\s*=\s*(.+?)$", q.strip())
        if not expr_m:
            return self._generic(0, q, {})
        raw = expr_m.group(1).strip()

        try:
            from sympy import (symbols, expand, Poly, roots, factor,
                               sqrt, Rational, LC, Integer, nsimplify)
            from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

            x = symbols("x")
            # Normalise: ^ -> **, implicit multiplication for coefficients
            raw_s = raw.replace("^", "**")
            raw_s = re.sub(r"sqrt\(([^)]+)\)", r"sqrt(\1)", raw_s)
            # Handle "1/2" literal fractions embedded in the expression
            transformations = standard_transformations + (implicit_multiplication_application,)
            f_sym = parse_expr(raw_s, local_dict={"x": x, "sqrt": sqrt},
                               transformations=transformations)

            poly_expr = expand(f_sym)
            p = Poly(poly_expr, x)
            deg = int(p.degree())
            lc  = float(p.LC())

            # ── leading term ────────────────────────────────────────────
            lc_str = (f"{int(lc)}" if lc == int(lc) else f"{lc:.4g}")
            if lc == 1:
                lt_str = f"x^{{{deg}}}"
            elif lc == -1:
                lt_str = f"-x^{{{deg}}}"
            else:
                lt_str = f"{lc_str}x^{{{deg}}}"

            # ── zeros ────────────────────────────────────────────────────
            zero_dict = roots(f_sym, x)
            real_zeros = {z: m for z, m in zero_dict.items()
                          if z.is_real}

            # y-intercept
            y_int = float(f_sym.subs(x, 0).evalf())
            y_int_str = f"{int(y_int)}" if y_int == int(y_int) else f"{y_int:.4g}"

            # ── build expanded display ───────────────────────────────────
            expanded_str = str(poly_expr).replace("**","^").replace("*x","x")
            expanded_str = re.sub(r"(\d)\*\*", r"\1^", expanded_str)

            # ── assemble steps ────────────────────────────────────────────
            steps = []

            # STEP (a) – degree and leading term
            steps.append({
                "title": "(a) Degree and Leading Term",
                "body": (
                    f"Expand $f(x)$ — the highest-power term tells us the degree and leading coefficient.\n\n"
                    f"$$f(x) = {expanded_str}$$\n\n"
                    f"**Degree:** $n = {deg}$\n\n"
                    f"**Leading coefficient:** $a_n = {lc_str}$\n\n"
                    f"**Leading term:** ${lt_str}$"
                ),
            })

            # STEP (b) – zeros and y-intercept
            if real_zeros:
                zero_lines = []
                for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                    m = real_zeros[z]
                    z_str = _fmt_zero(z)
                    zero_lines.append(
                        f"$x = {z_str}$ — multiplicity $\\mathbf{{{m}}}$ — {_cross_touch(m)}"
                    )
                zero_body = (
                    "Set $f(x) = 0$.  The zeros come from setting each factor equal to zero:\n\n"
                    + "\n\n".join(f"- {zl}" for zl in zero_lines)
                )
            else:
                zero_body = (
                    "Setting each factor to zero:\n\n"
                    "- No **real** zeros exist (all factors give complex roots).\n\n"
                    "The graph does not cross or touch the x-axis."
                )

            steps.append({
                "title": "(b) x-Intercepts (Zeros) and y-Intercept",
                "body": (
                    zero_body
                    + f"\n\n**y-intercept:** Set $x = 0$:  $f(0) = {y_int_str}$, "
                    + f"so the y-intercept is $(0,\\ {y_int_str})$."
                ),
            })

            # STEP (c) – cross vs touch  (already embedded above; add explicit summary)
            if real_zeros:
                ct_lines = []
                for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                    m = real_zeros[z]
                    z_str = _fmt_zero(z)
                    verb = "**crosses**" if m % 2 == 1 else "**touches** (bounces)"
                    reason = "odd multiplicity" if m % 2 == 1 else "even multiplicity"
                    ct_lines.append(f"At $x = {z_str}$: graph {verb} the x-axis ({reason}).")
                steps.append({
                    "title": "(c) Crosses or Touches the x-axis?",
                    "body": (
                        "**Rule:**\n"
                        "- **Odd** multiplicity → graph **crosses** the x-axis.\n"
                        "- **Even** multiplicity → graph **touches** (bounces off) the x-axis.\n\n"
                        + "\n".join(ct_lines)
                    ),
                })
            else:
                steps.append({
                    "title": "(c) Crosses or Touches the x-axis?",
                    "body": "No real zeros → the graph never crosses or touches the x-axis.",
                })

            # STEP (d) – max turning points
            max_tp = deg - 1
            steps.append({
                "title": "(d) Maximum Number of Turning Points",
                "body": (
                    rf"A degree-$n$ polynomial has **at most $n - 1$ turning points**." "\n\n"
                    rf"$$n - 1 = {deg} - 1 = \mathbf{{{max_tp}}}$$"
                ),
            })

            # STEP (e) – end behavior
            steps.append({
                "title": "(e) End Behavior",
                "body": (
                    f"Determined by the **leading term** ${lt_str}$:\n\n"
                    + _end_behavior_text(deg, lc)
                ),
            })

            # For FULL analysis (81-90) add a sketch guide
            if full:
                steps.append({
                    "title": "Step 5 — Rough Sketch Guide",
                    "body": (
                        "Combine all information to sketch the graph:\n\n"
                        f"1. **y-intercept:** $(0,\\ {y_int_str})$\n"
                        + (
                            "2. **x-intercepts (zeros):**\n"
                            + "\n".join(
                                f"   - $x = {_fmt_zero(z)}$ "
                                + ("(crosses)" if real_zeros[z] % 2 == 1 else "(touches/bounces)")
                                for z in sorted(real_zeros, key=lambda r: float(r.evalf()))
                            )
                            if real_zeros else
                            "2. No real x-intercepts."
                        )
                        + f"\n3. **End behavior:** {_end_behavior_text(deg, lc)}\n"
                        f"4. **At most {max_tp} turning point(s).**\n"
                        "5. Connect the intercepts with a smooth curve obeying the end-behavior arrows."
                    ),
                })

            # Build answer summary
            if real_zeros:
                zeros_summary = "; ".join(
                    f"$x={_fmt_zero(z)}$ (mult {real_zeros[z]})"
                    for z in sorted(real_zeros, key=lambda r: float(r.evalf()))
                )
            else:
                zeros_summary = "no real zeros"
            answer = (
                f"Degree: {deg}.  Leading term: ${lt_str}$.  "
                f"Zeros: {zeros_summary}.  "
                f"y-intercept: $(0,\\ {y_int_str})$.  "
                f"Max turning pts: {max_tp}.  "
                + _end_behavior_text(deg, lc)
            )
            return steps, answer

        except Exception as e:
            logger.warning(f"sympy analysis failed for '{q}': {e}")
            return self._generic(0, q, {})

    # ══════════════════════════════════════════════════════════════════════════
    # GENERIC fallback
    # ══════════════════════════════════════════════════════════════════════════

    def _generic(self, num: int, q: str, meta: dict) -> tuple:
        steps = [
            {"title": "Step 1 — Read the Problem", "body": "Identify what is given and what is asked."},
            {"title": "Step 2 — Choose the Right Method", "body": "Select the appropriate algebraic technique."},
            {"title": "Step 3 — Work Step by Step", "body": "Show every algebraic step clearly."},
            {"title": "Step 4 — Verify Your Answer", "body": "Check by substituting back or graphing."},
        ]
        return steps, "See steps above."
