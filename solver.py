from __future__ import annotations
"""
solver.py  -  Beginner-friendly step-by-step solution engine for Section 4.1
Language is plain and conversational so any student can follow along.
"""
import re, logging
logger = logging.getLogger(__name__)


def _end_plain(degree: int, lc: float) -> str:
    even, pos = (degree % 2 == 0), (lc > 0)
    if even and pos:     return "The graph rises on BOTH sides (like a U-shape)."
    if even and not pos: return "The graph falls on BOTH sides (like an upside-down U)."
    if not even and pos: return "The graph falls to the LEFT and rises to the RIGHT."
    return "The graph rises to the LEFT and falls to the RIGHT."


def _end_math(degree: int, lc: float) -> str:
    even, pos = (degree % 2 == 0), (lc > 0)
    if even and pos:
        return r"As $x \to -\infty,\ f(x) \to +\infty$ and as $x \to +\infty,\ f(x) \to +\infty$"
    if even and not pos:
        return r"As $x \to -\infty,\ f(x) \to -\infty$ and as $x \to +\infty,\ f(x) \to -\infty$"
    if not even and pos:
        return r"As $x \to -\infty,\ f(x) \to -\infty$ and as $x \to +\infty,\ f(x) \to +\infty$"
    return r"As $x \to -\infty,\ f(x) \to +\infty$ and as $x \to +\infty,\ f(x) \to -\infty$"


def _fmt_zero(z) -> str:
    return str(z)


class Solver:
    def solve(self, problem: dict) -> dict:
        ptype = problem.get("type", "generic")
        meta  = problem.get("meta", {})
        num   = problem["number"]
        q     = problem["question"]
        dispatch = {
            "transformation":        self._transformation,
            "form_polynomial":       self._form_polynomial,
            "form_polynomial_point": self._form_polynomial_point,
            "analysis":              self._analysis,
            "analysis_full":         self._analysis_full,
        }
        fn = dispatch.get(ptype, self._generic)
        result = fn(num, q, meta)
        steps, answer, graph = result if len(result) == 3 else (*result, None)
        return {"number": num, "question": q, "type": ptype,
                "steps": steps, "answer": answer, "graph": graph}

    # -----------------------------------------------------------------------
    # GRAPH HELPER
    # -----------------------------------------------------------------------
    def _make_graph(self, f_fn, x_lo: float, x_hi: float,
                    key_points: list = None, n_pts: int = 300) -> dict:
        """Evaluate f_fn over [x_lo, x_hi] and return Plotly-ready data."""
        span = x_hi - x_lo
        xs, ys = [], []
        for i in range(n_pts):
            xv = x_lo + i * span / (n_pts - 1)
            try:
                yv = float(f_fn(xv))
                yv = None if abs(yv) > 1e7 else round(yv, 4)
            except Exception:
                yv = None
            xs.append(round(xv, 5))
            ys.append(yv)
        kp = key_points or []
        kp_ys = [p["y"] for p in kp if p.get("y") is not None]
        valid_ys = [y for y in ys if y is not None]
        if kp_ys:
            yc = sum(kp_ys) / len(kp_ys)
            yspan = max((abs(y - yc) for y in kp_ys), default=0)
            yspan = max(yspan, abs(yc) * 0.25, 2.0)
        elif valid_ys:
            yc = (max(valid_ys) + min(valid_ys)) / 2
            yspan = (max(valid_ys) - min(valid_ys)) / 2 or 2.0
        else:
            yc, yspan = 0.0, 5.0
        return {
            "x": xs, "y": ys, "key_points": kp,
            "x_range": [round(x_lo, 4), round(x_hi, 4)],
            "y_range": [round(yc - max(yspan * 2.6, 4), 2),
                        round(yc + max(yspan * 2.6, 4), 2)],
        }

    # -----------------------------------------------------------------------
    # 1. TRANSFORMATION  (37-42)
    # -----------------------------------------------------------------------
    def _transformation(self, num: int, q: str, meta: dict) -> tuple:
        a = meta.get("a", 1)
        h = meta.get("h", 0)
        n = meta.get("n", 4)
        k = meta.get("k", 0)
        even     = (n % 2 == 0)
        key_name = "Vertex" if even else "Inflection Point"
        a_str = f"{int(a)}" if a == int(a) else str(a)

        if even:
            parent_desc = (
                "  Shape    : U-shaped (like a bowl)\n"
                "  Opens    : upward\n"
                "  Key Pt   : Vertex at (0, 0)\n"
                "  Symmetry : symmetric about the y-axis"
            )
        else:
            parent_desc = (
                "  Shape    : S-shaped (like a cubic curve)\n"
                "  Direction: goes from bottom-left to top-right\n"
                "  Key Pt   : Inflection point at (0, 0)"
            )

        trans_lines = []
        if a < 0 and abs(a) == 1:
            trans_lines.append(
                "FLIP (Reflection over x-axis)\n"
                "     The graph turns upside down.\n"
                "     Reason: the minus sign in front of the function."
            )
        elif a < 0:
            trans_lines.append(
                f"FLIP + VERTICAL STRETCH by {abs(a)}\n"
                f"     The graph flips upside down AND stretches vertically by {abs(a)}."
            )
        elif abs(a) > 1:
            trans_lines.append(
                f"VERTICAL STRETCH by {abs(a)}\n"
                f"     The graph gets taller and narrower."
            )
        elif 0 < abs(a) < 1:
            trans_lines.append(
                f"VERTICAL COMPRESSION by {abs(a)}\n"
                f"     The graph gets shorter and wider."
            )

        if h < 0:
            trans_lines.append(
                f"SHIFT LEFT by {abs(h)} units\n"
                f"     You see (x + {abs(h)}) inside the bracket.\n"
                f"     Trick: PLUS inside = move LEFT. (Feels backwards - but it is correct!)"
            )
        elif h > 0:
            trans_lines.append(
                f"SHIFT RIGHT by {h} units\n"
                f"     You see (x - {h}) inside the bracket.\n"
                f"     Trick: MINUS inside = move RIGHT."
            )

        if k > 0:
            trans_lines.append(
                f"SHIFT UP by {k} units\n"
                f"     The +{k} is OUTSIDE the bracket, so the whole graph moves up."
            )
        elif k < 0:
            trans_lines.append(
                f"SHIFT DOWN by {abs(k)} units\n"
                f"     The {k} is OUTSIDE the bracket, so the whole graph moves down."
            )

        if not trans_lines:
            trans_lines.append("No changes - this IS the parent function.")

        trans_block = "\n\n".join(
            f"  Change {i+1}: {t}" for i, t in enumerate(trans_lines)
        )

        kp_x, kp_y = h, k
        hdir = (f"left {abs(h)} unit(s)" if h < 0
                else (f"right {h} unit(s)" if h > 0 else "stays at 0 (no horizontal shift)"))
        kdir = (f"down {abs(k)} unit(s)" if k < 0
                else (f"up {k} unit(s)"   if k > 0 else "stays at 0 (no vertical shift)"))

        y_int     = a * (0 - h)**n + k
        y_int_str = f"{int(y_int)}" if y_int == int(y_int) else f"{y_int:.4g}"

        # Build a clean y-intercept computation string
        inner_val  = int((0 - h)**n)
        scaled_val = a * inner_val
        scaled_str = f"{int(scaled_val)}" if scaled_val == int(scaled_val) else f"{scaled_val:.4g}"

        steps = [
            {
                "title": "Step 1 - Start with the Parent Function (Ignore the numbers)",
                "body": (
                    "Just look at the POWER for a moment - ignore everything else.\n\n"
                    f"Parent function:  y = x^{n}\n\n"
                    f"What does y = x^{n} look like?\n"
                    + parent_desc
                ),
            },
            {
                "title": "Step 2 - Understand the Changes (Transformations)",
                "body": (
                    f"Now compare y = x^{n} with the given function:\n\n"
                    f"$$f(x) = {a_str}\\left(x - ({h})\\right)^{{{n}}} {'+ ' + str(k) if k >= 0 else '- ' + str(abs(k))}$$\n\n"
                    f"There {'are' if len(trans_lines) > 1 else 'is'} {len(trans_lines)} change(s) from the parent:\n\n"
                    + trans_block
                ),
            },
            {
                "title": f"Step 3 - Find the New {key_name}",
                "body": (
                    f"The parent's key point starts at (0, 0).\n\n"
                    f"Apply the shifts one at a time:\n"
                    f"  Horizontal shift: move {hdir}  ->  x becomes {kp_x}\n"
                    f"  Vertical shift  : move {kdir}  ->  y becomes {kp_y}\n\n"
                    f"New {key_name} = ({kp_x}, {kp_y})\n\n"
                    + (f"This is the {'LOWEST' if a > 0 else 'HIGHEST'} point on the graph."
                       if even else
                       "This is where the S-curve changes its bend (inflection point).")
                ),
            },
            {
                "title": "Step 4 - Shape of the Graph",
                "body": (
                    f"The power is {n}, which is {'EVEN' if even else 'ODD'}.\n\n"
                    + (
                        f"Even power (+ a = {a_str}):\n"
                        + (f"  -> Graph opens UPWARD (U-shape)\n" if a > 0
                           else f"  -> Graph opens DOWNWARD (upside-down U)\n")
                        + f"  -> Symmetric about the vertical line x = {kp_x}"
                        if even else
                        f"Odd power (a = {a_str}):\n"
                        + (f"  -> Bottom-left to top-right (rises on the right)\n" if a > 0
                           else f"  -> Top-left to bottom-right (falls on the right)\n")
                        + f"  -> 180-degree rotational symmetry about ({kp_x}, {kp_y})"
                    )
                ),
            },
            {
                "title": "Step 5 - y-intercept (where does the graph cross the y-axis?)",
                "body": (
                    f"Plug in x = 0:\n\n"
                    f"$$f(0) = {a_str}(0 - ({h}))^{{{n}}} {'+ ' + str(k) if k >= 0 else '- ' + str(abs(k))}$$\n"
                    f"$$f(0) = {a_str} \\times {inner_val} {'+ ' + str(k) if k >= 0 else '- ' + str(abs(k))}$$\n"
                    f"$$f(0) = {scaled_str} {'+ ' + str(k) if k >= 0 else '- ' + str(abs(k))} = {y_int_str}$$\n\n"
                    f"y-intercept = (0, {y_int_str})"
                ),
            },
            {
                "title": "Step 6 - End Behavior (what happens at the far left and right?)",
                "body": (
                    f"Look at the leading term to decide:\n\n"
                    f"{_end_math(n, a)}\n\n"
                    f"In plain words: {_end_plain(n, a)}"
                ),
            },
            {
                "title": "Step 7 - Final Summary (copy this into your exam answer!)",
                "body": (
                    f"  Parent Function : y = x^{n}\n"
                    f"  Transformation  : {', '.join(t.split(chr(10))[0].strip() for t in trans_lines)}\n"
                    f"  {key_name:16s}: ({kp_x}, {kp_y})\n"
                    f"  y-intercept     : (0, {y_int_str})\n"
                    f"  Shape           : {'U-shape, opens ' + ('UP' if a > 0 else 'DOWN') if even else 'S-shape'}\n"
                    f"  End Behavior    : {_end_plain(n, a)}"
                ),
            },
        ]

        answer = (
            f"Parent: $y = x^{{{n}}}$ | "
            f"{key_name}: ({kp_x}, {kp_y}) | "
            f"y-intercept: (0, {y_int_str}) | "
            f"{_end_plain(n, a)}"
        )
        graph = None
        try:
            _a, _h, _n, _k = float(a), float(h), int(n), float(k)
            f_fn = lambda xv, __a=_a, __h=_h, __n=_n, __k=_k: __a * (xv - __h)**__n + __k
            x_span = max(4.0, abs(_h) + 2.5)
            graphkp = [
                {"x": _h, "y": _k, "label": f"{key_name} ({kp_x}, {kp_y})", "color": "#e94560"},
                {"x": 0.0, "y": float(y_int), "label": f"y-int (0, {y_int_str})", "color": "#0f3460"},
            ]
            graph = self._make_graph(f_fn, _h - x_span, _h + x_span, graphkp)
        except Exception:
            graph = None
        return steps, answer, graph

    # -----------------------------------------------------------------------
    # 2. FORM POLYNOMIAL FROM ZEROS  (43-50)
    # -----------------------------------------------------------------------
    def _form_polynomial(self, num: int, q: str, meta: dict) -> tuple:
        zeros  = meta.get("zeros", [])
        degree = meta.get("degree", None)

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

        try:
            from sympy import symbols, expand, Rational
            x = symbols("x")
            expr = 1
            for z, m in zeros:
                zv = (Rational(z).limit_denominator(100)
                      if (isinstance(z, float) and z != int(z)) else int(z))
                expr *= (x - zv)**m
            expanded_str = str(expand(expr)).replace("**","^").replace("*x","x")
            expanded_str = re.sub(r"(\d)\*\*", r"\1^", expanded_str)
        except Exception:
            expanded_str = "(expand manually)"

        factor_lines = "\n".join(
            f"  Zero x = {z}  ->  factor: {p}"
            for p, z, m in factor_parts
        )
        mult_note = "".join(
            f"\n  Note: x = {z} has multiplicity {m}, so {p} is used {m} times as a factor."
            for p, z, m in factor_parts if m > 1
        )

        steps = [
            {
                "title": "Step 1 - What Does a 'Zero' Mean?",
                "body": (
                    "A zero (or root) is an x-value that makes f(x) = 0.\n"
                    "Visually: the graph CROSSES or TOUCHES the x-axis at each zero.\n\n"
                    "The Factor Theorem says:\n\n"
                    "  If x = r is a zero, then (x - r) is a FACTOR of f(x).\n\n"
                    "  Quick examples:\n"
                    "    Zero at x =  3  ->  factor is (x - 3)\n"
                    "    Zero at x = -2  ->  factor is (x - (-2)) = (x + 2)\n"
                    "    Zero at x =  0  ->  factor is (x - 0) = x"
                ),
            },
            {
                "title": "Step 2 - Convert Each Zero to a Factor",
                "body": (
                    "Apply the Factor Theorem to every zero:\n\n"
                    + factor_lines
                    + mult_note
                ),
            },
            {
                "title": "Step 3 - Write the Factored Form",
                "body": (
                    "Multiply all factors together. Use leading coefficient a = 1:\n\n"
                    f"$$f(x) = {factored}$$\n\n"
                    "Note: We use a = 1 because the problem does not specify a value.\n"
                    "Any non-zero multiple of this polynomial has the same zeros."
                ),
            },
            {
                "title": "Step 4 - Expand to Standard Form",
                "body": (
                    "Multiply out all the brackets (FOIL or distributive property):\n\n"
                    f"$$f(x) = {expanded_str}$$"
                ),
            },
            {
                "title": "Step 5 - Verify the Degree",
                "body": (
                    "Add up all the multiplicities - this must equal the stated degree:\n"
                    + "".join(f"\n  x = {z},  multiplicity {m}" for _, z, m in factor_parts)
                    + f"\n  Total = {sum(m for _, _, m in factor_parts)}"
                    + (f"\n\nDegree = {degree}  (matches!)" if degree else "")
                ),
            },
        ]
        answer = f"$f(x) = {factored} = {expanded_str}$"
        graph = None
        try:
            from sympy import symbols as _sym, Rational as _Rat, lambdify
            _x = _sym("x")
            _expr = 1
            for z, m in zeros:
                _zv = _Rat(z).limit_denominator(100) if isinstance(z, float) and z != int(z) else int(z)
                _expr *= (_x - _zv)**m
            _f = lambdify(_x, _expr, "math")
            _zf = [float(z) for z, _ in zeros]
            _margin = max(2.0, (max(_zf) - min(_zf)) * 0.35 + 1) if len(_zf) > 1 else 3.0
            _yint_g = float(_expr.subs(_x, 0))
            _gkp = [{"x": float(z), "y": 0.0, "label": f"x={z}", "color": "#e94560"} for z, _ in zeros]
            _gkp.append({"x": 0.0, "y": round(_yint_g, 4), "label": "y-int", "color": "#0f3460"})
            graph = self._make_graph(_f, min(_zf) - _margin, max(_zf) + _margin, _gkp)
        except Exception:
            graph = None
        return steps, answer, graph

    # -----------------------------------------------------------------------
    # 3. FORM POLYNOMIAL THROUGH A POINT  (51-56)
    # -----------------------------------------------------------------------
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

        try:
            from sympy import symbols, Rational, expand
            x = symbols("x")
            expr_unit = 1
            for z, m in zeros:
                zv = Rational(z).limit_denominator(100) if isinstance(z, float) else int(z)
                expr_unit *= (x - zv)**m
            pxv = Rational(px).limit_denominator(100) if isinstance(px, float) else int(px)
            pyv = Rational(py).limit_denominator(100) if isinstance(py, float) else int(py)
            base_at_px_sym = expr_unit.subs(x, pxv)
            base_at_px     = float(base_at_px_sym.evalf())
            if base_at_px_sym != 0:
                a_val_sym = pyv / base_at_px_sym
            else:
                a_val_sym = None
            expanded_final = (
                str(expand(a_val_sym * expr_unit))
                .replace("**","^").replace("*x","x")
                if a_val_sym else "undefined"
            )
            expanded_final = re.sub(r"(\d)\*\*", r"\1^", expanded_final)
        except Exception:
            base_at_px = None
            a_val_sym  = None
            expanded_final = "(compute manually)"

        px_str = f"{int(px)}" if px == int(px) else f"{px}"
        py_str = f"{int(py)}" if py == int(py) else f"{py}"
        base_str = (
            f"{int(base_at_px)}"
            if base_at_px is not None and base_at_px == int(base_at_px)
            else f"{base_at_px:.4g}" if base_at_px is not None else "?"
        )
        a_str = str(a_val_sym) if a_val_sym is not None else "?"

        factor_list = "\n".join(f"  - {p}" for p, _, _ in factor_parts)

        steps = [
            {
                "title": "Step 1 - Why Do We Need the Extra Point?",
                "body": (
                    "From the zeros alone, the best we can write is:\n\n"
                    f"$$f(x) = a \\cdot {factored_base}$$\n\n"
                    "The 'a' (leading coefficient) is still unknown.\n\n"
                    "Key idea: every value of 'a' produces a polynomial with the SAME zeros\n"
                    "but a different vertical scale.\n\n"
                    f"The point ({px_str}, {py_str}) is like a clue that pins down the exact value of 'a'."
                ),
            },
            {
                "title": "Step 2 - Write the General Form",
                "body": (
                    "Convert each zero to a factor:\n"
                    + factor_list
                    + f"\n\nGeneral form (a is unknown):\n\n"
                    + f"$$f(x) = a \\cdot {factored_base}$$"
                ),
            },
            {
                "title": "Step 3 - Plug In the Known Point to Solve for 'a'",
                "body": (
                    f"We know f({px_str}) = {py_str}  (the graph passes through this point).\n\n"
                    f"Step 3a - Evaluate the base at x = {px_str} (leave 'a' out for now):\n\n"
                    f"$$\\text{{Base at }} x = {px_str}: \\quad {factored_base}\\big|_{{x={px_str}}} = {base_str}$$\n\n"
                    f"Step 3b - Set up the equation and solve:\n\n"
                    f"$$a \\times {base_str} = {py_str}$$\n\n"
                    f"$$a = \\frac{{{py_str}}}{{{base_str}}} = {a_str}$$"
                ),
            },
            {
                "title": "Step 4 - Write the Final Polynomial",
                "body": (
                    f"Substitute a = {a_str}:\n\n"
                    f"Factored form:\n$$f(x) = {a_str} \\cdot {factored_base}$$\n\n"
                    f"Standard form (expanded):\n$$f(x) = {expanded_final}$$"
                ),
            },
            {
                "title": "Step 5 - Verify Your Answer",
                "body": (
                    f"Plug x = {px_str} back in to double-check:\n\n"
                    f"$$f({px_str}) = {a_str} \\times {base_str} = {py_str} \\checkmark$$\n\n"
                    f"The point ({px_str}, {py_str}) lies on our polynomial. Correct!"
                ),
            },
        ]
        answer = f"a = {a_str}  =>  $f(x) = {a_str}({factored_base}) = {expanded_final}$"
        graph = None
        try:
            if a_val_sym is not None:
                from sympy import lambdify, symbols as _sym
                _x2 = _sym("x")
                _full = a_val_sym * expr_unit
                _f2 = lambdify(_x2, _full, "math")
                _zf2 = [float(z) for z, _ in zeros]
                _margin2 = max(2.0, (max(_zf2) - min(_zf2)) * 0.35 + 1) if len(_zf2) > 1 else 3.0
                _yint2 = float(_full.subs(_x2, 0).evalf())
                _gkp2 = [{"x": float(z), "y": 0.0, "label": f"x={z}", "color": "#e94560"} for z, _ in zeros]
                _gkp2.append({"x": 0.0, "y": round(_yint2, 4), "label": "y-int", "color": "#0f3460"})
                _gkp2.append({"x": float(px), "y": float(py), "label": f"({px_str}, {py_str})", "color": "#2e7d32"})
                graph = self._make_graph(_f2, min(_zf2) - _margin2, max(_zf2) + _margin2, _gkp2)
        except Exception:
            graph = None
        return steps, answer, graph

    # -----------------------------------------------------------------------
    # 4. ANALYSIS  (57-68)
    # -----------------------------------------------------------------------
    def _analysis(self, num: int, q: str, meta: dict) -> tuple:
        return self._run_sympy_analysis(q, full=False)

    # -----------------------------------------------------------------------
    # 5. FULL ANALYSIS  (81-90)
    # -----------------------------------------------------------------------
    def _analysis_full(self, num: int, q: str, meta: dict) -> tuple:
        return self._run_sympy_analysis(q, full=True)

    def _run_sympy_analysis(self, q: str, full: bool) -> tuple:
        expr_m = re.search(r"f\s*\(\s*x\s*\)\s*=\s*(.+?)$", q.strip())
        if not expr_m:
            return self._generic(0, q, {})
        raw = expr_m.group(1).strip()

        try:
            from sympy import symbols, expand, Poly, roots, sqrt, Rational
            from sympy.parsing.sympy_parser import (
                parse_expr, standard_transformations,
                implicit_multiplication_application)

            x   = symbols("x")
            raw_s = raw.replace("^", "**")
            tf  = standard_transformations + (implicit_multiplication_application,)
            f_sym = parse_expr(raw_s, local_dict={"x": x, "sqrt": sqrt},
                               transformations=tf)

            poly_expr = expand(f_sym)
            p   = Poly(poly_expr, x)
            deg = int(p.degree())
            lc  = float(p.LC())
            lc_str = f"{int(lc)}" if lc == int(lc) else f"{lc:.4g}"
            lt_str = (f"x^{{{deg}}}"       if lc ==  1 else
                      f"-x^{{{deg}}}"      if lc == -1 else
                      f"{lc_str}x^{{{deg}}}")

            zero_dict  = roots(f_sym, x)
            real_zeros = {z: m for z, m in zero_dict.items() if z.is_real}

            y_int     = float(f_sym.subs(x, 0).evalf())
            y_int_str = f"{int(y_int)}" if y_int == int(y_int) else f"{y_int:.4g}"

            expanded_str = str(poly_expr).replace("**","^").replace("*x","x")
            expanded_str = re.sub(r"(\d)\*\*", r"\1^", expanded_str)

            steps = []

            # (a) degree and leading term
            steps.append({
                "title": "(a) Degree and Leading Term",
                "body": (
                    "Expand the polynomial so the highest power is clear:\n\n"
                    f"$$f(x) = {expanded_str}$$\n\n"
                    f"  Degree (highest power of x) = {deg}\n"
                    f"  Leading coefficient         = {lc_str}\n"
                    f"  Leading term                = {lt_str}\n\n"
                    "The leading term determines the overall behavior of the graph at the extremes."
                ),
            })

            # (b) zeros + y-intercept
            if real_zeros:
                zero_lines = []
                for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                    m = real_zeros[z]
                    z_str = _fmt_zero(z)
                    zero_lines.append(f"  x = {z_str}  (multiplicity {m})")
                zero_body = (
                    "Set each factor equal to zero and solve:\n\n"
                    + "\n".join(zero_lines)
                )
            else:
                zero_body = (
                    "Set each factor equal to zero...\n\n"
                    "  No REAL zeros exist - all roots are complex numbers.\n"
                    "  The graph never crosses or touches the x-axis."
                )

            steps.append({
                "title": "(b) x-Intercepts and y-Intercept",
                "body": (
                    zero_body
                    + f"\n\ny-intercept: substitute x = 0:\n\n"
                    + f"$$f(0) = {y_int_str}$$\n\n"
                    + f"y-intercept = (0, {y_int_str})"
                ),
            })

            # (c) crosses vs touches
            if real_zeros:
                rule = (
                    "Simple Rule:\n"
                    "  ODD multiplicity  ->  graph CROSSES through the x-axis\n"
                    "                        (goes straight through, like x = 0 in y = x)\n"
                    "  EVEN multiplicity ->  graph TOUCHES and BOUNCES BACK\n"
                    "                        (like a ball hitting the floor, x = 0 in y = x^2)\n\n"
                )
                ct_lines = []
                for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                    m = real_zeros[z]
                    z_str = _fmt_zero(z)
                    if m % 2 == 1:
                        ct_lines.append(f"  x = {z_str}  mult {m} (ODD)   ->  CROSSES the x-axis")
                    else:
                        ct_lines.append(f"  x = {z_str}  mult {m} (EVEN)  ->  TOUCHES (bounces back)")
                steps.append({
                    "title": "(c) Does the Graph Cross or Touch the x-axis?",
                    "body": rule + "\n".join(ct_lines),
                })
            else:
                steps.append({
                    "title": "(c) Does the Graph Cross or Touch the x-axis?",
                    "body": "No real zeros -> the graph never reaches the x-axis.",
                })

            # (d) max turning points
            max_tp = deg - 1
            steps.append({
                "title": "(d) Maximum Number of Turning Points",
                "body": (
                    "A turning point is where the graph switches between going up and going down\n"
                    "(a hill becomes a valley, or a valley becomes a hill).\n\n"
                    "Formula:  Maximum turning points = degree - 1\n\n"
                    f"  {deg} - 1 = {max_tp}\n\n"
                    f"This graph can have AT MOST {max_tp} turning point(s)."
                ),
            })

            # (e) end behavior
            steps.append({
                "title": "(e) End Behavior",
                "body": (
                    f"Focus only on the leading term: {lt_str}\n\n"
                    f"  Degree = {deg}  ({'EVEN' if deg % 2 == 0 else 'ODD'})\n"
                    f"  Leading coefficient = {lc_str}  ({'POSITIVE' if lc > 0 else 'NEGATIVE'})\n\n"
                    f"In math notation:\n{_end_math(deg, lc)}\n\n"
                    f"In plain words: {_end_plain(deg, lc)}"
                ),
            })

            if full:
                sketch_lines = [f"  1. Plot the y-intercept at (0, {y_int_str})."]
                if real_zeros:
                    for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                        m = real_zeros[z]
                        z_str = _fmt_zero(z)
                        verb  = "cross straight through" if m % 2 == 1 else "touch and bounce back"
                        sketch_lines.append(f"  2. At x = {z_str}: {verb}.")
                else:
                    sketch_lines.append("  2. No x-intercepts to plot.")
                sketch_lines.append(f"  3. Draw end-behavior arrows: {_end_plain(deg, lc)}")
                sketch_lines.append(f"  4. The graph turns at most {max_tp} time(s).")
                sketch_lines.append("  5. Connect all points with a smooth, continuous curve.")

                steps.append({
                    "title": "Step 5 - How to Sketch the Graph",
                    "body": "Combine everything above:\n\n" + "\n".join(sketch_lines),
                })

            if real_zeros:
                zeros_summary = "; ".join(
                    f"x = {_fmt_zero(z)} (mult {real_zeros[z]})"
                    for z in sorted(real_zeros, key=lambda r: float(r.evalf()))
                )
            else:
                zeros_summary = "no real zeros"

            answer = (
                f"Degree: {deg} | Leading term: ${lt_str}$ | "
                f"Zeros: {zeros_summary} | "
                f"y-intercept: (0, {y_int_str}) | "
                f"Max turning pts: {max_tp} | "
                f"{_end_plain(deg, lc)}"
            )
            graph = None
            try:
                from sympy import lambdify
                _fn = lambdify(x, f_sym, "math")
                _zf3 = [float(z.evalf()) for z in real_zeros] if real_zeros else []
                if _zf3:
                    _m3 = max(2.0, (max(_zf3) - min(_zf3)) * 0.35 + 1)
                    _gxlo, _gxhi = min(_zf3) - _m3, max(_zf3) + _m3
                else:
                    _gxlo, _gxhi = -4.0, 4.0
                _gkp3 = [{"x": float(z.evalf()), "y": 0.0,
                          "label": f"x={_fmt_zero(z)}", "color": "#e94560"}
                         for z in sorted(real_zeros, key=lambda r: float(r.evalf()))]
                _gkp3.append({"x": 0.0, "y": round(y_int, 4),
                              "label": f"y-int (0, {y_int_str})", "color": "#0f3460"})
                graph = self._make_graph(_fn, _gxlo, _gxhi, _gkp3)
            except Exception:
                graph = None
            return steps, answer, graph

        except Exception as e:
            logger.warning(f"sympy analysis failed for '{q}': {e}")
            return self._generic(0, q, {})

    def _generic(self, num: int, q: str, meta: dict) -> tuple:
        steps = [
            {"title": "Step 1 - Read the Problem",  "body": "Identify what is given and what is asked."},
            {"title": "Step 2 - Choose the Method", "body": "Select the appropriate algebraic technique."},
            {"title": "Step 3 - Work Step by Step", "body": "Show every algebraic step clearly."},
            {"title": "Step 4 - Verify",            "body": "Substitute back to check."},
        ]
        return steps, "See steps above.", None
