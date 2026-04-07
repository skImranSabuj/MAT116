from __future__ import annotations
"""
solver.py
---------
Solution-generation engine for MAT116 / Precalculus Section 4.1.

Classifies each problem into one of four types and generates a
step-by-step, "topper student" solution dict:

    {
        "number":   int,
        "question": str,
        "type":     str,          # transformation | form_polynomial | analysis | application
        "steps":    [             # ordered list of solution steps
            {"title": "Step 1: ...", "body": "..."},
            ...
        ],
        "answer":   str           # concise final answer
    }

Math is formatted in LaTeX (dollar-sign delimiters) so MathJax can
render it in the HTML output.
"""

import re
import logging
from fractions import Fraction
from typing import Union

logger = logging.getLogger(__name__)

# ── small helpers ──────────────────────────────────────────────────────────────

def _frac_str(numerator: Union[int, float], denominator: Union[int, float]) -> str:
    """Return a LaTeX fraction or integer string."""
    if denominator == 1:
        return str(int(numerator))
    return rf"\dfrac{{{int(numerator)}}}{{{int(denominator)}}}"


def _sign(n: float) -> str:
    return "+" if n >= 0 else "-"


def _end_behavior(degree: int, leading_coeff: float) -> str:
    """Human-readable end-behaviour sentence for a polynomial."""
    pos_lc = leading_coeff > 0
    if degree % 2 == 0:           # even degree
        if pos_lc:
            return (r"As $x \to +\infty$, $f(x) \to +\infty$ and "
                    r"as $x \to -\infty$, $f(x) \to +\infty$ "
                    r"(both ends rise — $\cup$ shape).")
        else:
            return (r"As $x \to +\infty$, $f(x) \to -\infty$ and "
                    r"as $x \to -\infty$, $f(x) \to -\infty$ "
                    r"(both ends fall — $\cap$ shape).")
    else:                          # odd degree
        if pos_lc:
            return (r"As $x \to -\infty$, $f(x) \to -\infty$ and "
                    r"as $x \to +\infty$, $f(x) \to +\infty$ "
                    r"(falls left, rises right).")
        else:
            return (r"As $x \to -\infty$, $f(x) \to +\infty$ and "
                    r"as $x \to +\infty$, $f(x) \to -\infty$ "
                    r"(rises left, falls right).")


# ── classifier ────────────────────────────────────────────────────────────────

_TRANSFORM_RE = re.compile(
    r"""
    f\s*\(\s*x\s*\)\s*=\s*           # f(x) =
    (?P<a>-?\s*\d*\.?\d*\s*)?        # optional coefficient a (may be -1 etc.)
    \(\s*x\s*                        # opening (x
    (?P<sign>[+-])\s*                # shift sign
    (?P<h>\d+\.?\d*)\s*              # shift amount |h|
    \)\s*\^\s*(?P<n>\d+)             # )^n
    (?:\s*(?P<vshift>[+-]\s*\d+\.?\d*))?  # optional vertical shift
    """,
    re.VERBOSE | re.IGNORECASE,
)

_SIMPLE_POWER_RE = re.compile(
    r"f\s*\(\s*x\s*\)\s*=\s*(-?\s*\d*\.?\d*\s*)?\(\s*x\s*\)\s*\^\s*(\d+)",
    re.IGNORECASE,
)

_FORM_POLY_RE = re.compile(
    r"form\s+a\s+polynomial|real\s+coefficients|zeros?:",
    re.IGNORECASE,
)

_ANALYSIS_RE = re.compile(
    r"for\s+f\s*\(|x-.*intercept|leading\s+term|turning\s+point|end\s+behavior|multiplicity",
    re.IGNORECASE,
)

_APPLICATION_RE = re.compile(
    r"box|revenue|area|volume|profit|population|projectile|wire|tank|farmer|manufacturer|cost",
    re.IGNORECASE,
)


def _classify(question: str) -> str:
    if _TRANSFORM_RE.search(question):
        return "transformation"
    # Check for transformation without explicit h shift, e.g. f(x)=(x)^4
    if re.search(r"f\s*\(x\)\s*=.*\(x.*\)\^\d+", question, re.IGNORECASE):
        return "transformation"
    if _FORM_POLY_RE.search(question):
        return "form_polynomial"
    if _ANALYSIS_RE.search(question):
        return "analysis"
    if _APPLICATION_RE.search(question):
        return "application"
    return "generic"


# ── main solver class ──────────────────────────────────────────────────────────

class Solver:
    """Top-level dispatcher."""

    def solve(self, problem: dict) -> dict:
        q = problem.get("question", "")
        ptype = _classify(q)
        logger.debug(f"Problem {problem['number']}: type = {ptype}")

        if ptype == "transformation":
            steps, answer = self._solve_transformation(q)
        elif ptype == "form_polynomial":
            steps, answer = self._solve_form_polynomial(q)
        elif ptype == "analysis":
            steps, answer = self._solve_analysis(q)
        elif ptype == "application":
            steps, answer = self._solve_application(problem["number"], q)
        else:
            steps, answer = self._solve_generic(q)

        return {
            "number":   problem["number"],
            "question": q,
            "type":     ptype,
            "steps":    steps,
            "answer":   answer,
        }

    # ── TRANSFORMATION SOLVER ─────────────────────────────────────────────────

    def _solve_transformation(self, question: str) -> tuple[list[dict], str]:
        """
        Handle problems of the form: f(x) = a(x ± h)^n + k
        """
        steps: list[dict] = []

        # ── Parse the function ──────────────────────────────────────────────
        m = _TRANSFORM_RE.search(question)
        if not m:
            # Try simpler patterns like f(x) = (x-2)^3
            m2 = re.search(
                r"f\(x\)\s*=\s*(-?\d*\.?\d*)?\s*\(\s*x\s*([+-])\s*(\d+\.?\d*)\s*\)\^(\d+)"
                r"(?:\s*([+-]\s*\d+\.?\d*))?",
                question, re.IGNORECASE,
            )
            if m2:
                raw_a   = m2.group(1) or "1"
                sign_h  = m2.group(2)
                raw_h   = m2.group(3)
                raw_n   = m2.group(4)
                raw_k   = m2.group(5) or "0"
            else:
                return self._solve_generic(question)
        else:
            raw_a   = (m.group("a") or "1").strip()
            sign_h  = m.group("sign")
            raw_h   = m.group("h")
            raw_n   = m.group("n")
            raw_k   = (m.group("vshift") or "0").strip()

        # Clean coefficient
        raw_a = raw_a.replace(" ", "")
        if raw_a in ("", "+"):
            a = 1.0
        elif raw_a == "-":
            a = -1.0
        else:
            try:
                a = float(raw_a)
            except ValueError:
                a = 1.0

        # Standard form: f(x) = a(x - h)^n + k
        # (x + c) means h = -c  → shift LEFT  by c
        # (x - c) means h = +c  → shift RIGHT by c
        h = float(raw_h) * (-1 if sign_h == "+" else 1)
        n = int(raw_n)
        try:
            raw_k = raw_k.replace(" ", "")
            k = float(raw_k)
        except ValueError:
            k = 0.0

        # ── Step 1: Identify parent function ───────────────────────────────
        parent = rf"y = x^{{{n}}}"
        steps.append({
            "title": "Step 1: Identify the Parent Function",
            "body": (
                rf"The expression inside the parentheses is raised to the power $n = {n}$, "
                rf"so the **parent function** is $${parent}$$"
                + (
                    "\nThis is an **even-degree** power function (U-shaped with both ends going up)."
                    if n % 2 == 0
                    else "\nThis is an **odd-degree** power function (S-shaped, falls left / rises right)."
                )
            ),
        })

        # ── Step 2: Identify each transformation ───────────────────────────
        transform_list: list[str] = []

        if a < 0:
            transform_list.append(f"**Reflection** over the $x$-axis (because $a = {a} < 0$).")
        if abs(a) != 1:
            if abs(a) > 1:
                transform_list.append(
                    rf"**Vertical stretch** by a factor of $|a| = {abs(a)}$."
                )
            else:
                transform_list.append(
                    rf"**Vertical compression** by a factor of $|a| = {abs(a)}$."
                )

        if h != 0:
            direction = "right" if h > 0 else "left"
            transform_list.append(
                rf"**Horizontal shift** $|h| = {abs(h)}$ unit(s) to the **{direction}** "
                rf"(because the factor is $(x {'+' if h < 0 else '-'} {abs(h)})$)."
            )

        if k != 0:
            direction = "up" if k > 0 else "down"
            transform_list.append(
                rf"**Vertical shift** $|k| = {abs(k)}$ unit(s) **{direction}**."
            )

        if not transform_list:
            transform_list.append("No transformations — the graph is the parent itself.")

        steps.append({
            "title": "Step 2: Identify All Transformations",
            "body": "Apply the following transformations **in order**:\n\n"
                    + "\n".join(f"- {t}" for t in transform_list),
        })

        # ── Step 3: Identify key point ─────────────────────────────────────
        key_point_name = "vertex" if n % 2 == 0 else "inflection point"
        px, py = h, k
        # If a ≠ ±1 and n even, apply a to y-coordinate of vertex
        if n % 2 == 0:
            py = a * (0) + k  # vertex y = a*(0)^n + k = k (minimum/maximum)
        steps.append({
            "title": f"Step 3: Find the Key Point ({key_point_name.title()})",
            "body": (
                rf"Start from the parent's key point at $(0, 0)$. "
                rf"After shifting, the {key_point_name} moves to:"
                rf"$$({px:.4g},\ {py:.4g})$$"
                + (
                    rf" — this is the **minimum** of the graph."
                    if (n % 2 == 0 and a > 0)
                    else (
                        rf" — this is the **maximum** of the graph."
                        if n % 2 == 0
                        else rf" — this is the inflection point of the graph."
                    )
                )
            ),
        })

        # ── Step 4: Axis of symmetry (even degree only) ────────────────────
        if n % 2 == 0:
            steps.append({
                "title": "Step 4: Axis of Symmetry",
                "body": (
                    rf"For even-degree power functions the graph is symmetric about the "
                    rf"vertical line through the vertex:$$x = {px:.4g}$$"
                ),
            })
        else:
            steps.append({
                "title": "Step 4: Symmetry",
                "body": (
                    "Odd-degree power functions have **point symmetry** (rotational symmetry "
                    rf"of 180°) about the inflection point $({px:.4g},\ {py:.4g})$. "
                    "They are **not** symmetric about a vertical axis."
                ),
            })

        # ── Step 5: End behaviour ──────────────────────────────────────────
        steps.append({
            "title": "Step 5: End Behavior",
            "body": _end_behavior(n, a),
        })

        # ── Step 6: Sketch instructions ────────────────────────────────────
        steps.append({
            "title": "Step 6: How to Sketch the Graph",
            "body": (
                f"1. Plot the key point / {key_point_name} at $({px:.4g},\ {py:.4g})$.\n"
                "2. Apply end-behavior arrows.\n"
                "3. Use the symmetry noted above to mirror the curve.\n"
                "4. Note that the graph passes **through** $y$-axis at "
                + rf"$x = 0$:  $f(0) = {a:.4g}(0 {'+' if -h>=0 else '-'} {abs(-h):.4g})^{{{n}}} "
                + (rf"+ {k:.4g}" if k >= 0 else rf"- {abs(k):.4g}") + "$."
            ),
        })

        # ── Concise answer ─────────────────────────────────────────────────
        answer_parts = []
        answer_parts.append(f"Parent function: $y = x^{{{n}}}$.")
        if transform_list:
            answer_parts.append("Transformations: " + "; ".join(
                t.replace("**", "") for t in transform_list
            ))
        answer_parts.append(
            f"{key_point_name.title()}: $({px:.4g},\\ {py:.4g})$."
        )
        answer_parts.append(_end_behavior(n, a))

        return steps, " ".join(answer_parts)

    # ── FORM-POLYNOMIAL SOLVER ────────────────────────────────────────────────

    def _solve_form_polynomial(self, question: str) -> tuple[list[dict], str]:
        steps: list[dict] = []

        # ── Parse degree ────────────────────────────────────────────────────
        deg_m = re.search(r"degree\s+(\d+)", question, re.IGNORECASE)
        degree = int(deg_m.group(1)) if deg_m else None

        # ── Parse zeros & multiplicities ────────────────────────────────────
        # Examples:  "zeros: -3, 0, 4"
        #            "zeros: -1, 2 (multiplicity 2), 4"
        #            "zeros: 4 + i, 3"
        zeros_raw = re.search(
            r"zeros?\s*:?\s*(.*?)(?:\.|$|use\s+1)",
            question, re.IGNORECASE | re.DOTALL,
        )
        zero_entries: list[tuple[str, int]] = []   # (zero_string, multiplicity)

        if zeros_raw:
            raw = zeros_raw.group(1)
            # Split on commas, but be careful with complex zeros like "4 + i"
            # Strategy: split on comma-not-followed-by-space-digit (heuristic)
            parts = re.split(r",\s*", raw.strip())
            i = 0
            while i < len(parts):
                part = parts[i].strip()
                if not part:
                    i += 1
                    continue
                # Check for explicit multiplicity annotation
                mult_m = re.search(r"\(multiplicity\s+(\d+)\)", part, re.I)
                mult = int(mult_m.group(1)) if mult_m else 1
                # Strip the multiplicity annotation
                z_str = re.sub(r"\s*\(multiplicity\s+\d+\)", "", part).strip()
                # Handle complex conjugate pairs like "4 + i"
                if re.search(r"[+-]\s*\d*\s*i", z_str):
                    zero_entries.append((z_str, mult))
                    # Add its conjugate automatically
                    conj = re.sub(r"\+\s*(\d*)\s*i", r"- \1i", z_str)
                    if conj == z_str:
                        conj = re.sub(r"-\s*(\d*)\s*i", r"+ \1i", z_str)
                    if conj != z_str:
                        zero_entries.append((conj, mult))
                elif re.search(r"^\s*i\s*$", z_str):
                    zero_entries.append(("i", mult))
                    zero_entries.append(("-i", mult))
                else:
                    zero_entries.append((z_str, mult))
                i += 1

        # ── Step 1: Recall the zero-factor theorem ──────────────────────────
        steps.append({
            "title": "Step 1: Apply the Zero-Factor Theorem",
            "body": (
                "If $r$ is a zero of polynomial $f(x)$ with multiplicity $m$, then "
                "$(x - r)^m$ is a factor of $f(x)$.  "
                "We build the polynomial by writing one factor for **each** zero."
            ),
        })

        # ── Step 2: Write the factors ───────────────────────────────────────
        factor_strs: list[str] = []
        for z_str, mult in zero_entries:
            z_clean = z_str.strip()
            # Build factor string  (x - z)^m
            if z_clean.startswith("-"):
                num_part = z_clean[1:].strip()
                factor = rf"(x + {num_part})"
            elif z_clean == "0":
                factor = "x"
            else:
                factor = rf"(x - {z_clean})"
            if mult > 1:
                factor += rf"^{{{mult}}}"
            factor_strs.append(factor)

        factors_product = r" \cdot ".join(factor_strs)
        steps.append({
            "title": "Step 2: Write the Factored Form",
            "body": (
                "Write $f(x)$ as a product of its linear (and complex) factors:\n\n"
                rf"$$f(x) = {factors_product}$$"
            ),
        })

        # ── Step 3: Expand / verify degree ─────────────────────────────────
        try:
            from sympy import symbols, expand, factor, I, Rational
            from sympy.parsing.sympy_parser import parse_expr

            x_sym = symbols("x")

            def parse_zero(z_str: str):
                """Convert zero string to sympy number."""
                z_str = z_str.strip()
                # Handle complex like "4 + i", "4 - 2i", "i", "-i"
                z_str = re.sub(r"\bi\b", "*I", z_str)
                z_str = z_str.replace(" ", "")
                return parse_expr(z_str, local_dict={"I": I})

            poly_sym = 1
            for z_str, mult in zero_entries:
                z_val = parse_zero(z_str)
                poly_sym *= (x_sym - z_val) ** mult

            expanded = expand(poly_sym)
            expanded_str = str(expanded).replace("**", "^").replace("*", r"\,")
            # Replace I with i for display
            expanded_str = expanded_str.replace("I", "i")

            steps.append({
                "title": "Step 3: Expand the Polynomial",
                "body": (
                    "Multiply out all the factors (use FOIL / distributive property):\n\n"
                    rf"$$f(x) = {expanded_str}$$"
                    + (
                        f"\n\nCheck: the degree of the polynomial is "
                        rf"$\deg f = {int(expanded.as_poly(x_sym).degree())}$"
                        + (f", matching the required degree ${degree}$." if degree else ".")
                    )
                ),
            })
            answer_poly = rf"f(x) = {expanded_str}"
        except Exception as e:
            logger.debug(f"sympy expansion failed: {e}")
            steps.append({
                "title": "Step 3: Expand the Polynomial",
                "body": (
                    "Multiply out all the factors using the distributive property / FOIL.\n"
                    "The factored form is:\n\n"
                    rf"$$f(x) = {factors_product}$$"
                ),
            })
            answer_poly = rf"f(x) = {factors_product}"

        # ── Step 4: Verify zeros ────────────────────────────────────────────
        steps.append({
            "title": "Step 4: Verify the Zeros",
            "body": (
                "To confirm, substitute each zero back into $f(x)$ — the result must be $0$.\n"
                "By construction, evaluating at any zero $r$ causes the factor $(x - r) = 0$, "
                "so $f(r) = 0$. ✓"
            ),
        })

        return steps, answer_poly

    # ── ANALYSIS SOLVER ───────────────────────────────────────────────────────

    def _solve_analysis(self, question: str) -> tuple[list[dict], str]:
        """
        For polynomials already in factored form like
          f(x) = x^2(x-3)(x+4)
        produce full analysis.
        """
        steps: list[dict] = []

        # Extract the polynomial expression from "For f(x) = ..."
        expr_m = re.search(
            r"[Ff]\s*\(\s*x\s*\)\s*=\s*(.+?)(?:\s*[:(]|\s*$|\s*find|\s*For\s)",
            question,
        )
        raw_expr = expr_m.group(1).strip() if expr_m else question

        # ── Try to analyse with sympy ───────────────────────────────────────
        try:
            from sympy import symbols, expand, factor, degree as sym_degree
            from sympy import Poly, roots, LC, Integer
            from sympy.parsing.sympy_parser import parse_expr

            x_sym = symbols("x")

            # Normalise for sympy: ^ → **, remove extra characters
            sympy_expr = raw_expr
            sympy_expr = re.sub(r"\^", "**", sympy_expr)
            sympy_expr = re.sub(r"(\d)\s*\(", r"\1*(", sympy_expr)

            f_sym = parse_expr(sympy_expr, local_dict={"x": x_sym})
            poly  = Poly(expand(f_sym), x_sym)

            deg   = poly.degree()
            lc    = float(poly.LC())
            expanded_str = str(expand(f_sym)).replace("**", "^").replace("*x", "x").replace("* x", "x")

            # ── Step (a): degree & leading term ────────────────────────────
            leading_term = (
                rf"{int(lc) if lc == int(lc) else lc}x^{{{deg}}}"
                if lc != 1
                else rf"x^{{{deg}}}"
            )
            steps.append({
                "title": "Step (a): Degree and Leading Term",
                "body": (
                    f"Expand $f(x)$ and inspect the highest-power term.\n\n"
                    f"**Degree:** ${deg}$\n\n"
                    f"**Leading coefficient:** ${lc:.4g}$\n\n"
                    f"**Leading term:** ${leading_term}$"
                ),
            })

            # ── Step (b): Zeros & y-intercept ──────────────────────────────
            poly_roots = roots(f_sym, x_sym)
            zero_list: list[str] = []
            for root_val, mult in sorted(poly_roots.items(), key=lambda kv: float(kv[0].evalf())):
                r_str = str(root_val)
                zero_list.append(
                    rf"$x = {r_str}$ (multiplicity ${mult}$)"
                )

            y_int = float(f_sym.subs(x_sym, 0).evalf())
            y_int_str = f"{int(y_int)}" if y_int == int(y_int) else f"{y_int:.4g}"

            steps.append({
                "title": "Step (b): x-Intercepts (Zeros) and y-Intercept",
                "body": (
                    "Set $f(x) = 0$ and solve — the zeros come from setting each factor to zero.\n\n"
                    "**Zeros (x-intercepts):**\n"
                    + "\n".join(f"- {z}" for z in zero_list)
                    + f"\n\n**y-intercept:** set $x = 0$: $f(0) = {y_int_str}$, "
                    + rf"so the $y$-intercept is $(0, {y_int_str})$."
                ),
            })

            # ── Step (c): Crossing vs. touching ────────────────────────────
            cross_touch: list[str] = []
            for root_val, mult in poly_roots.items():
                r_str = str(root_val)
                behavior = (
                    "**crosses** (odd multiplicity — the graph passes through the axis)"
                    if mult % 2 == 1
                    else "**touches** (even multiplicity — the graph bounces off the axis)"
                )
                cross_touch.append(rf"At $x = {r_str}$ (mult ${mult}$): graph {behavior}.")

            steps.append({
                "title": "Step (c): Crossing vs. Touching the x-axis",
                "body": (
                    "Check the **multiplicity** of each zero:\n"
                    "- **Odd** multiplicity → graph **crosses** the x-axis.\n"
                    "- **Even** multiplicity → graph **touches** (bounces off) the x-axis.\n\n"
                    + "\n".join(f"- {ct}" for ct in cross_touch)
                ),
            })

            # ── Step (d): Maximum turning points ───────────────────────────
            max_tp = deg - 1
            steps.append({
                "title": "Step (d): Maximum Number of Turning Points",
                "body": (
                    rf"A polynomial of degree $n$ has **at most $n - 1$** turning points. "
                    rf"Here $n = {deg}$, so the maximum is $\mathbf{{{max_tp}}}$ turning point(s)."
                ),
            })

            # ── Step (e): End behavior ─────────────────────────────────────
            steps.append({
                "title": "Step (e): End Behavior",
                "body": (
                    rf"The end behavior is determined by the **leading term** ${leading_term}$:\n\n"
                    + _end_behavior(deg, lc)
                ),
            })

            # Build answer summary
            answer = (
                f"Degree: {deg}. Leading term: ${leading_term}$. "
                f"Zeros: {', '.join(zero_list)}. "
                f"y-intercept: $(0, {y_int_str})$. "
                f"Max turning points: {max_tp}. "
                + _end_behavior(deg, lc)
            )

        except Exception as e:
            logger.warning(f"sympy analysis failed: {e} — using text-only solution.")
            steps, answer = self._solve_generic(question)

        return steps, answer

    # ── APPLICATION SOLVER ───────────────────────────────────────────────────

    def _solve_application(self, num: int, question: str) -> tuple[list[dict], str]:
        """Route to specific application solutions by problem number."""
        routes = {
            81: self._app_box_volume,
            82: self._app_box_volume,
            83: self._app_revenue,
            84: self._app_farmer_fence,
            85: self._app_cost_function,
            86: self._app_profit_function,
            87: self._app_projectile,
            88: self._app_population,
            89: self._app_cone_volume,
            90: self._app_wire_area,
        }
        fn = routes.get(num)
        if fn:
            return fn(question)
        return self._solve_generic(question)

    # ── individual application solutions ─────────────────────────────────────

    def _app_box_volume(self, question: str) -> tuple[list[dict], str]:
        # Detect dimensions from the question
        dim_m = re.search(r"(\d+)-inch by (\d+)-inch", question)
        L = int(dim_m.group(1)) if dim_m else 12
        W = int(dim_m.group(2)) if dim_m else 12

        steps = [
            {
                "title": "Step 1: Define Variables and Diagram",
                "body": (
                    rf"Let $x$ = the side length (in inches) of each square cut from the corners. "
                    rf"After cutting and folding:\n"
                    rf"- Length of box $= {L} - 2x$\n"
                    rf"- Width of box $= {W} - 2x$\n"
                    rf"- Height of box $= x$"
                ),
            },
            {
                "title": "Step 2: Write the Volume Function",
                "body": (
                    rf"$$V(x) = \text{{length}} \times \text{{width}} \times \text{{height}}$$"
                    rf"$$V(x) = ({L} - 2x)({W} - 2x)(x)$$"
                ),
            },
            {
                "title": "Step 3: State the Domain",
                "body": (
                    rf"We need each dimension to be **positive**:\n"
                    rf"- $x > 0$\n"
                    rf"- ${L} - 2x > 0 \Rightarrow x < {L//2}$"
                    + (
                        rf" and ${W} - 2x > 0 \Rightarrow x < {W//2}$"
                        if L != W else ""
                    )
                    + rf"\n\nTherefore the domain is $0 < x < {min(L, W)//2}$."
                ),
            },
            {
                "title": "Step 4: Expand V(x)",
                "body": (
                    rf"First multiply the two binomials:"
                    rf"$$({L} - 2x)({W} - 2x) = {L*W} - {2*L}x - {2*W}x + 4x^2 = 4x^2 - {2*(L+W)}x + {L*W}$$"
                    rf"Now multiply by $x$:"
                    rf"$$V(x) = 4x^3 - {2*(L+W)}x^2 + {L*W}x$$"
                ),
            },
            {
                "title": "Step 5: Maximize Volume",
                "body": (
                    rf"Take the derivative and set it to zero (Calculus approach), or use a graphing utility:\n"
                    rf"$$V'(x) = 12x^2 - {4*(L+W)}x + {L*W}$$"
                    rf"Setting $V'(x) = 0$ and solving gives the $x$-value that maximises $V$."
                    rf"\n\nUsing the quadratic formula or a graph, find $x = x_{{max}}$ in the domain $\left(0, {min(L,W)//2}\right)$."
                ),
            },
        ]
        answer = (
            rf"$V(x) = ({L} - 2x)({W} - 2x)(x) = 4x^3 - {2*(L+W)}x^2 + {L*W}x$, "
            rf"domain: $0 < x < {min(L,W)//2}$."
        )
        return steps, answer

    def _app_revenue(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Identify the Revenue Function",
                "body": (
                    r"From the problem: $R(x) = -0.5x^2 + 100x$. "
                    r"This is a **downward-opening parabola** (leading coefficient $< 0$), "
                    r"so it has a maximum."
                ),
            },
            {
                "title": "Step 2: Find Revenue at Given Points",
                "body": (
                    r"$R(50) = -0.5(50)^2 + 100(50) = -1250 + 5000 = \$3750$"
                    "\n\n"
                    r"$R(120) = -0.5(120)^2 + 100(120) = -7200 + 12000 = \$4800$"
                ),
            },
            {
                "title": "Step 3: Maximize Revenue",
                "body": (
                    r"For a quadratic $R(x) = ax^2 + bx + c$, maximum is at $x = -\dfrac{b}{2a}$."
                    "\n\n"
                    r"$$x = -\frac{100}{2(-0.5)} = -\frac{100}{-1} = 100 \text{ units}$$"
                ),
            },
            {
                "title": "Step 4: Maximum Revenue",
                "body": (
                    r"$$R(100) = -0.5(100)^2 + 100(100) = -5000 + 10000 = \$5000$$"
                    "\n\nThe **maximum revenue** is **$5000** at $x = 100$ units."
                ),
            },
        ]
        answer = r"Max revenue = $\$5000$ at $x = 100$ units."
        return steps, answer

    def _app_farmer_fence(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Set Up Variables",
                "body": (
                    r"Let $w$ = width of the rectangle (feet). "
                    r"The fence creates 3 widths and 2 lengths."
                    "\n\n"
                    r"Constraint: $3w + 2\ell = 200 \Rightarrow \ell = \dfrac{200 - 3w}{2}$"
                ),
            },
            {
                "title": "Step 2: Express Area as Function of w",
                "body": (
                    r"$$A(w) = w \cdot \ell = w \cdot \frac{200 - 3w}{2} = \frac{200w - 3w^2}{2}$$"
                    "\n\n"
                    r"$$A(w) = -\frac{3}{2}w^2 + 100w$$"
                ),
            },
            {
                "title": "Step 3: Find the Maximum",
                "body": (
                    r"Vertex at $w = -\dfrac{100}{2 \cdot (-3/2)} = -\dfrac{100}{-3} = \dfrac{100}{3} \approx 33.33$ ft"
                ),
            },
            {
                "title": "Step 4: Compute Maximum Area",
                "body": (
                    r"$$A\!\left(\tfrac{100}{3}\right)"
                    r"= -\tfrac{3}{2}\!\left(\tfrac{100}{3}\right)^{\!2} + 100\cdot\tfrac{100}{3}"
                    r"= -\tfrac{3}{2}\cdot\tfrac{10000}{9} + \tfrac{10000}{3}"
                    r"= -\tfrac{5000}{3} + \tfrac{10000}{3} = \tfrac{5000}{3} \approx 1666.67 \text{ ft}^2$$"
                ),
            },
        ]
        answer = r"Max area $\approx 1666.67$ ft² at $w = \tfrac{100}{3}$ ft."
        return steps, answer

    def _app_cost_function(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Identify the Marginal Cost",
                "body": (
                    r"The cost function is $C(x) = 0.002x^3 - 3x^2 + 1500x + 4000$."
                    "\n\nMarginal cost = $C'(x)$ (the derivative):\n\n"
                    r"$$C'(x) = 0.006x^2 - 6x + 1500$$"
                ),
            },
            {
                "title": "Step 2: Minimise Marginal Cost",
                "body": (
                    r"$C'(x)$ is itself a quadratic in $x$, opening upward ($a = 0.006 > 0$). "
                    r"Its minimum occurs at its vertex:"
                    "\n\n"
                    r"$$x = -\frac{b}{2a} = -\frac{-6}{2(0.006)} = \frac{6}{0.012} = 500 \text{ units}$$"
                ),
            },
            {
                "title": "Step 3: Verify",
                "body": (
                    r"$$C'(500) = 0.006(500)^2 - 6(500) + 1500 = 1500 - 3000 + 1500 = 0$$"
                    "\n\nThis confirms $x = 500$ is indeed the minimum of the marginal cost."
                ),
            },
        ]
        answer = r"Marginal cost is minimised at $x = 500$ units."
        return steps, answer

    def _app_profit_function(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Write the Profit Function",
                "body": (
                    r"$P(x) = -x^3 + 6x^2 + 15x - 12$ (in thousands of dollars, "
                    r"$x$ = hundreds of units)."
                ),
            },
            {
                "title": "Step 2: Find Zeros",
                "body": (
                    r"Use the Rational Root Theorem — test $x = \frac{p}{q}$ for factors of 12."
                    "\n\n"
                    r"Try $x = -3$: $P(-3) = -(-27) + 6(9) + 15(-3) - 12 = 27 + 54 - 45 - 12 = 24 \ne 0$"
                    "\n\n"
                    r"Try $x = \frac{1}{1} = 1$: $P(1) = -1 + 6 + 15 - 12 = 8 \ne 0$"
                    "\n\nUse numerical methods or a graphing utility to find the roots approximately, "
                    r"then determine the interval where $P(x) > 0$."
                ),
            },
            {
                "title": "Step 3: Sign Analysis",
                "body": (
                    r"Find all real zeros $x_1 < x_2 < x_3$ using a graphing tool. "
                    r"$P(x) > 0$ on the intervals between zeros where the cubic is positive. "
                    r"Because the leading coefficient is $-1 < 0$, the cubic rises on the left "
                    r"and falls on the right."
                ),
            },
        ]
        answer = r"Use sign analysis on $P(x) = -x^3 + 6x^2 + 15x - 12$ to find the profitable range."
        return steps, answer

    def _app_projectile(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Write the Height Function",
                "body": (
                    r"$h(t) = -16t^2 + 80t$ (height in feet, $t$ in seconds)."
                    "\nThis is a downward-opening parabola (maximum height exists)."
                ),
            },
            {
                "title": "Step 2: Maximum Height (vertex)",
                "body": (
                    r"Vertex at $t = -\dfrac{80}{2(-16)} = -\dfrac{80}{-32} = 2.5$ seconds."
                    "\n\n"
                    r"$$h(2.5) = -16(2.5)^2 + 80(2.5) = -100 + 200 = 100 \text{ feet}$$"
                ),
            },
            {
                "title": "Step 3: When Does It Return to the Ground?",
                "body": (
                    r"Set $h(t) = 0$: $-16t^2 + 80t = 0 \Rightarrow t(-16t + 80) = 0$"
                    "\n\n"
                    r"$t = 0$ (launch) or $t = \dfrac{80}{16} = 5$ seconds."
                    "\n\nThe projectile returns to the ground at $t = 5$ seconds."
                ),
            },
        ]
        answer = r"Max height: 100 ft at $t = 2.5$ s; returns to ground at $t = 5$ s."
        return steps, answer

    def _app_population(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Identify the Model",
                "body": r"$P(t) = -0.01t^3 + 0.3t^2 + 2t + 50$ (thousands), $t$ = years after 2000.",
            },
            {
                "title": "Step 2: Population in 2000 (t = 0)",
                "body": (
                    r"$$P(0) = -0.01(0)^3 + 0.3(0)^2 + 2(0) + 50 = 50 \text{ thousand}$$"
                ),
            },
            {
                "title": "Step 3: Population in 2020 (t = 20)",
                "body": (
                    r"$$P(20) = -0.01(8000) + 0.3(400) + 2(20) + 50$$"
                    "\n\n"
                    r"$$= -80 + 120 + 40 + 50 = 130 \text{ thousand}$$"
                ),
            },
        ]
        answer = r"Year 2000: 50,000; Year 2020: 130,000."
        return steps, answer

    def _app_cone_volume(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Set Up Similar Triangles",
                "body": (
                    r"The full cone has height 10 m and base radius 4 m. "
                    r"At depth $x$, the water radius $r$ satisfies:"
                    "\n\n"
                    r"$$\frac{r}{x} = \frac{4}{10} = \frac{2}{5} \implies r = \frac{2x}{5}$$"
                ),
            },
            {
                "title": "Step 2: Write Volume as a Polynomial",
                "body": (
                    r"$$V(x) = \frac{1}{3}\pi r^2 x = \frac{1}{3}\pi \left(\frac{2x}{5}\right)^2 x "
                    r"= \frac{1}{3}\pi \cdot \frac{4x^2}{25} \cdot x = \frac{4\pi}{75}x^3$$"
                ),
            },
            {
                "title": "Step 3: Evaluate at x = 5",
                "body": (
                    r"$$V(5) = \frac{4\pi}{75}(125) = \frac{500\pi}{75} = \frac{20\pi}{3}"
                    r"\approx 20.94 \text{ m}^3$$"
                ),
            },
        ]
        answer = r"$V(x) = \dfrac{4\pi}{75}x^3$; $V(5) = \dfrac{20\pi}{3} \approx 20.94$ m³."
        return steps, answer

    def _app_wire_area(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Define Variables",
                "body": (
                    r"Total wire = 36 inches. Let $s$ = side of the square (inches). "
                    r"Wire for square = $4s$. "
                    r"Wire for circle = $36 - 4s$ = circumference $ = 2\pi r$, so $r = \dfrac{36-4s}{2\pi}$."
                ),
            },
            {
                "title": "Step 2: Express Total Area",
                "body": (
                    r"$$A(s) = s^2 + \pi r^2 = s^2 + \pi\left(\frac{36 - 4s}{2\pi}\right)^2"
                    r"= s^2 + \frac{(36 - 4s)^2}{4\pi}$$"
                ),
            },
            {
                "title": "Step 3: Find Minimum",
                "body": (
                    r"Differentiate and set $A'(s) = 0$:"
                    "\n\n"
                    r"$$A'(s) = 2s + \frac{2(36 - 4s)(-4)}{4\pi} = 2s - \frac{2(36 - 4s)}{\pi}$$"
                    "\n\n"
                    r"Setting $A'(s) = 0$: $2s\pi = 2(36 - 4s) \Rightarrow \pi s = 36 - 4s$"
                    "\n\n"
                    r"$$s(\pi + 4) = 36 \implies s = \frac{36}{\pi + 4} \approx 5.04 \text{ inches}$$"
                ),
            },
        ]
        answer = (
            r"$A(s) = s^2 + \dfrac{(36-4s)^2}{4\pi}$; minimised at $s = \dfrac{36}{\pi+4} \approx 5.04$ in."
        )
        return steps, answer

    # ── generic fallback ──────────────────────────────────────────────────────

    def _solve_generic(self, question: str) -> tuple[list[dict], str]:
        steps = [
            {
                "title": "Step 1: Read and Understand the Problem",
                "body": "Carefully read the given information and identify what is being asked.",
            },
            {
                "title": "Step 2: Identify Relevant Techniques",
                "body": (
                    "This problem may involve:\n"
                    "- Polynomial arithmetic (expanding, factoring)\n"
                    "- Transformation of graphs\n"
                    "- Zero/root analysis\n"
                    "- End behaviour of polynomials"
                ),
            },
            {
                "title": "Step 3: Solve Step by Step",
                "body": "Apply the relevant technique systematically, showing all intermediate work.",
            },
            {
                "title": "Step 4: Verify",
                "body": "Check your answer by substituting back or using a graphing utility.",
            },
        ]
        return steps, "See work above."
