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


def _expr_str(e) -> str:
    return str(e).replace("**", "^").replace("*x", "x").replace("*", "·")


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
            "rational_graph_analysis": self._rational_graph_analysis,
            "rational_asymptotes":   self._rational_asymptotes,
            "rational_application":  self._rational_application,
            "inequality_sign_chart": self._inequality_sign_chart,
        }
        fn = dispatch.get(ptype, self._generic)
        result = fn(num, q, meta)
        if len(result) == 4:
            steps, answer, answer_sections, graph = result
        elif len(result) == 3:
            steps, answer, graph = result
            answer_sections = None
        else:
            steps, answer = result
            answer_sections, graph = None, None
        return {"number": num, "question": q, "type": ptype,
                "steps": steps, "answer": answer,
                "answer_sections": answer_sections, "graph": graph}

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

        # ── exam answer sections ──────────────────────────────────────────
        if even:
            parent_line = (f"y = x^{n}\n"
                           f"  Shape    : U-shaped, opens upward\n"
                           f"  Vertex   : (0, 0)\n"
                           f"  Symmetry : symmetric about the y-axis")
        else:
            parent_line = (f"y = x^{n}\n"
                           f"  Shape    : S-shaped curve\n"
                           f"  Key point: inflection point at (0, 0)")

        trans_bullets = []
        for t in trans_lines:
            first_line = t.split("\n")[0].strip()
            trans_bullets.append(f"  • {first_line}")
        if not trans_bullets:
            trans_bullets = ["  • No transformation — this IS the parent function"]
        trans_exam = "\n".join(trans_bullets)

        k_sign = f"+ {abs(k)}" if k >= 0 else f"- {abs(k)}"
        yint_exam = (
            f"  Substitute x = 0 into f(x):\n"
            f"    f(0) = {a_str}(0 − ({h}))^{n} {k_sign}\n"
            f"         = {a_str} × {inner_val} {k_sign}\n"
            f"         = {scaled_str} {k_sign}\n"
            f"         = {y_int_str}\n\n"
            f"  ∴  y-intercept: (0, {y_int_str})"
        )

        if even:
            shape_exam = (
                f"  n = {n}  (EVEN power),  a = {a_str}  ({'> 0' if a > 0 else '< 0'})\n"
                f"  → Graph opens {'UPWARD (U-shape)' if a > 0 else 'DOWNWARD (inverted U)'}\n"
                f"  → Axis of symmetry: x = {kp_x}"
            )
        else:
            shape_exam = (
                f"  n = {n}  (ODD power),  a = {a_str}  ({'> 0' if a > 0 else '< 0'})\n"
                f"  → {'Rises left-to-right' if a > 0 else 'Falls left-to-right'}\n"
                f"  → Point symmetry about ({kp_x}, {kp_y})"
            )

        kp_exam = (
            f"  Start at parent key point (0, 0), apply shifts:\n"
            f"    Horizontal shift: {hdir}  →  x = {kp_x}\n"
            f"    Vertical shift  : {kdir}  →  y = {kp_y}\n\n"
            f"  ∴  {key_name} = ({kp_x}, {kp_y})"
            + (f"\n     (This is the {'lowest' if a > 0 else 'highest'} point on the graph.)"
               if even else "\n     (This is where the curve changes its bend.)")
        )

        end_exam = (
            f"  Leading term: {a_str}·x^{n}  —  "
            f"degree {n} ({'even' if even else 'odd'}), "
            f"a = {a_str} ({'positive' if a > 0 else 'negative'})\n\n"
            f"  {_end_math(n, a)}\n"
            f"  → {_end_plain(n, a)}"
        )

        answer_sections = [
            {"label": "① Parent Function",
             "body": parent_line},
            {"label": "② Transformations Applied",
             "body": trans_exam},
            {"label": f"③ New {key_name}  (apply shifts to key point)",
             "body": kp_exam},
            {"label": "④ Shape & Symmetry",
             "body": shape_exam},
            {"label": "⑤ y-intercept  (substitute x = 0)",
             "body": yint_exam},
            {"label": "⑥ End Behavior",
             "body": end_exam},
        ]
        return steps, answer, answer_sections, graph

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

        # ── exam answer sections ──────────────────────────────────────────
        ft_lines = ["  Factor Theorem:  if x = r is a zero, then (x − r) is a factor.\n"]
        for f_str, z, m in factor_parts:
            mult_tag = f"   ← multiplicity {m} (use this factor {m} times)" if m > 1 else ""
            ft_lines.append(f"  x = {str(z):<6}  →  {f_str}{mult_tag}")
        ft_body = "\n".join(ft_lines)

        factored_body = f"  f(x) = {factored}"
        if any(m > 1 for _, _, m in factor_parts):
            factored_body += ("\n\n  Note: a factor with even multiplicity → graph TOUCHES the x-axis\n"
                              "        a factor with odd  multiplicity → graph CROSSES the x-axis")

        yint_poly = None
        try:
            from sympy import symbols as _s2, Rational as _R2
            _xx = _s2("x")
            _ep = 1
            for z, m in zeros:
                _zv2 = _R2(z).limit_denominator(100) if isinstance(z, float) and z != int(z) else int(z)
                _ep *= (_xx - _zv2)**m
            yint_poly = float(_ep.subs(_xx, 0))
        except Exception:
            yint_poly = None
        yint_poly_str = (f"{int(yint_poly)}" if yint_poly is not None and yint_poly == int(yint_poly)
                         else f"{yint_poly:.4g}" if yint_poly is not None else "—")

        verify_lines = ["  Degree check — sum of multiplicities must equal the stated degree:"]
        for _, z, m in factor_parts:
            verify_lines.append(f"    zero x = {z},  multiplicity {m}")
        total_m = sum(m for _, _, m in factor_parts)
        verify_lines.append(f"    Total = {total_m}" + (f"  =  {degree}  ✓" if degree else ""))
        verify_lines.append(f"\n  y-intercept check:  f(0) = {yint_poly_str}")

        answer_sections = [
            {"label": "① Factor Theorem  (zeros → factors)",
             "body": ft_body},
            {"label": "② Factored Form  (a = 1)",
             "body": factored_body},
            {"label": "③ Standard Form  (expand / multiply out)",
             "body": f"  f(x) = {expanded_str}"},
            {"label": "④ Verify",
             "body": "\n".join(verify_lines)},
        ]
        return steps, answer, answer_sections, graph

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

        # ── exam answer sections ──────────────────────────────────────────
        ft3_lines = ["  Factor Theorem:  zero x = r  →  factor (x − r)\n"]
        for f_str, z, m in factor_parts:
            ft3_lines.append(f"  x = {str(z):<6}  →  {f_str}")
        ft3_body = "\n".join(ft3_lines)

        general_body = (
            f"  Write f(x) with unknown leading coefficient 'a':\n\n"
            f"    f(x) = a · {factored_base}\n\n"
            f"  (Any value of 'a' gives the same zeros — we need the given point to fix it.)"
        )

        solve_a_body = (
            f"  Given point: f({px_str}) = {py_str}\n\n"
            f"  Step 1 — Substitute x = {px_str} into the base (without 'a'):\n"
            f"    {factored_base} at x = {px_str}  =  {base_str}\n\n"
            f"  Step 2 — Set up equation and solve:\n"
            f"    a × {base_str} = {py_str}\n"
            f"    a = {py_str} ÷ ({base_str}) = {a_str}"
        )

        final_poly_body = (
            f"  Factored form:  f(x) = {a_str} · {factored_base}\n\n"
            f"  Standard form:  f(x) = {expanded_final}\n\n"
            f"  Verify: f({px_str}) = {a_str} × {base_str} = {py_str}  ✓"
        )

        answer_sections = [
            {"label": "① Factor Theorem  (zeros → factors)",
             "body": ft3_body},
            {"label": "② General Form  (a is unknown)",
             "body": general_body},
            {"label": "③ Find 'a'  (substitute given point)",
             "body": solve_a_body},
            {"label": "④ Final Polynomial",
             "body": final_poly_body},
        ]
        return steps, answer, answer_sections, graph

    # -----------------------------------------------------------------------
    # 4.3 - Rational Graph Analysis (15-20)
    # -----------------------------------------------------------------------
    def _rational_graph_analysis(self, num: int, q: str, meta: dict) -> tuple:
        try:
            from sympy import (
                symbols, factor, simplify, Poly, Eq, solveset, S,
                cancel, limit
            )
            from sympy.parsing.sympy_parser import (
                parse_expr, standard_transformations,
                implicit_multiplication_application
            )

            x = symbols("x")
            tf = standard_transformations + (implicit_multiplication_application,)

            name = meta.get("name", "R")
            num_raw = meta.get("numerator", "")
            den_raw = meta.get("denominator", "")

            n_expr = parse_expr(str(num_raw).replace("^", "**"), local_dict={"x": x}, transformations=tf)
            d_expr = parse_expr(str(den_raw).replace("^", "**"), local_dict={"x": x}, transformations=tf)
            f_expr = n_expr / d_expr

            n_fact = factor(n_expr)
            d_fact = factor(d_expr)
            simp = cancel(f_expr)
            simp_n, simp_d = simp.as_numer_denom()

            # Step 1/2 foundations: domain, reduced form, holes
            dom_restrict = sorted(solveset(Eq(d_expr, 0), x, domain=S.Reals), key=lambda v: float(v.evalf()))
            va = sorted(solveset(Eq(simp_d, 0), x, domain=S.Reals), key=lambda v: float(v.evalf()))
            holes = [r for r in dom_restrict if r not in va]

            # Step 3: intercepts
            xints_all = sorted(solveset(Eq(simp_n, 0), x, domain=S.Reals), key=lambda v: float(v.evalf()))
            xints = [z for z in xints_all if z not in va and z not in holes]

            yint = None
            if simplify(d_expr.subs(x, 0)) != 0:
                yint = simplify(f_expr.subs(x, 0))

            # Step 4/5: asymptotes
            pn = Poly(simplify(simp_n), x)
            pd = Poly(simplify(simp_d), x)
            dn, dd = pn.degree(), pd.degree()

            h_asym = None
            o_asym = None
            if dn < dd:
                h_asym = simplify(0)
            elif dn == dd:
                h_asym = simplify(pn.LC() / pd.LC())
            elif dn == dd + 1:
                q_poly, _ = pn.div(pd)
                o_asym = simplify(q_poly.as_expr())

            asym_intersections = []
            try:
                if h_asym is not None:
                    sols = sorted(solveset(Eq(simp, h_asym), x, domain=S.Reals), key=lambda v: float(v.evalf()))
                    asym_intersections = [s for s in sols if s not in dom_restrict]
                elif o_asym is not None:
                    sols = sorted(solveset(Eq(simp, o_asym), x, domain=S.Reals), key=lambda v: float(v.evalf()))
                    asym_intersections = [s for s in sols if s not in dom_restrict]
            except Exception:
                asym_intersections = []

            # Step 6: intervals and sign
            critical = sorted(set([*xints, *va]), key=lambda v: float(v.evalf()))
            intervals = []
            if critical:
                intervals.append((-S.Infinity, critical[0]))
                for i in range(len(critical) - 1):
                    intervals.append((critical[i], critical[i + 1]))
                intervals.append((critical[-1], S.Infinity))
            else:
                intervals.append((-S.Infinity, S.Infinity))

            def _sample(a, b):
                if a is S.NegativeInfinity and b is S.Infinity:
                    return simplify(0)
                if a is S.NegativeInfinity:
                    return simplify(b - 1)
                if b is S.Infinity:
                    return simplify(a + 1)
                return simplify((a + b) / 2)

            interval_rows = []
            for a, b in intervals:
                t = _sample(a, b)
                try:
                    val = simplify(simp.subs(x, t))
                    pos = (val.evalf() > 0)
                    loc = "Above x-axis" if pos else "Below x-axis"
                except Exception:
                    val = "undefined"
                    loc = "undefined"
                interval_rows.append((a, b, t, val, loc))

            # Vertical asymptote one-sided behavior
            va_beh = []
            for v in va:
                try:
                    l = limit(simp, x, v, dir='-')
                    r = limit(simp, x, v, dir='+')
                    va_beh.append((v, l, r))
                except Exception:
                    va_beh.append((v, "?", "?"))

            holes_text = []
            hole_points = []
            for h in holes:
                y_h = simplify(simp.subs(x, h))
                holes_text.append(f"({_expr_str(h)}, {_expr_str(y_h)})")
                hole_points.append({"x": float(h.evalf()), "y": float(y_h.evalf()), "label": f"hole ({_expr_str(h)}, {_expr_str(y_h)})", "color": "#ff9800"})

            step6_lines = []
            for a, b, t, val, loc in interval_rows:
                ia = "-∞" if a is S.NegativeInfinity else _expr_str(a)
                ib = "+∞" if b is S.Infinity else _expr_str(b)
                step6_lines.append(
                    f"  ({ia}, {ib})  choose x = {_expr_str(t)}:  R(x) = {_expr_str(val)}  -> {loc}"
                )

            va_lines = []
            for v, l, r in va_beh:
                va_lines.append(
                    f"  x = {_expr_str(v)}:  lim_(x→{_expr_str(v)}-) R(x) = {_expr_str(l)},  lim_(x→{_expr_str(v)}+) R(x) = {_expr_str(r)}"
                )

            asym_line = (
                f"Horizontal asymptote: y = {_expr_str(h_asym)}" if h_asym is not None
                else f"Oblique asymptote: y = {_expr_str(o_asym)}" if o_asym is not None
                else "No horizontal or oblique asymptote"
            )

            inter_line = (
                ", ".join([f"({_expr_str(s)}, {_expr_str(h_asym if h_asym is not None else o_asym)})" for s in asym_intersections])
                if asym_intersections else "none"
            )

            steps = [
                {
                    "title": "Step 1 - Factor Numerator/Denominator and Domain",
                    "body": (
                        f"$$ {name}(x)=\\frac{{{_expr_str(n_expr)}}}{{{_expr_str(d_expr)}}} $$\n"
                        f"Numerator factorization: {_expr_str(n_fact)}\n"
                        f"Denominator factorization: {_expr_str(d_fact)}\n\n"
                        "Domain restriction(s): "
                        + (", ".join([f"x ≠ {_expr_str(r)}" for r in dom_restrict]) if dom_restrict else "none")
                    ),
                },
                {
                    "title": "Step 2 - Write in Lowest Terms",
                    "body": (
                        f"Simplified function:\n$$ {name}(x) = {_expr_str(simp)} $$\n\n"
                        + ("Hole(s): " + ", ".join(holes_text) if holes_text else "No holes")
                    ),
                },
                {
                    "title": "Step 3 - Intercepts",
                    "body": (
                        "x-intercepts (set numerator = 0): "
                        + (", ".join([f"({_expr_str(z)}, 0)" for z in xints]) if xints else "none")
                        + "\n"
                        + (f"y-intercept (x=0): (0, {_expr_str(yint)})" if yint is not None else "y-intercept: none (x=0 not in domain)")
                    ),
                },
                {
                    "title": "Step 4 - Vertical Asymptotes and Side Behavior",
                    "body": (
                        "Vertical asymptote(s): "
                        + (", ".join([f"x = {_expr_str(v)}" for v in va]) if va else "none")
                        + ("\n" + "\n".join(va_lines) if va_lines else "")
                    ),
                },
                {
                    "title": "Step 5 - Horizontal/Oblique Asymptote and Intersections",
                    "body": (
                        f"Degree(numerator)={dn}, Degree(denominator)={dd}\n"
                        f"{asym_line}\n"
                        f"Graph intersects this asymptote at: {inter_line}"
                    ),
                },
                {
                    "title": "Step 6 - Interval Sign Check",
                    "body": "Use zeros and vertical asymptotes to split intervals:\n" + "\n".join(step6_lines),
                },
                {
                    "title": "Step 7 - Graph Summary",
                    "body": (
                        "Plot intercepts and sample points from Step 6. Draw vertical asymptotes as dashed lines.\n"
                        f"Approach {asym_line.lower()} on far left/right.\n"
                        "Sketch branches in each interval based on sign and asymptote behavior."
                    ),
                },
            ]

            answer = (
                f"Domain: "
                + (", ".join([f"x ≠ {_expr_str(r)}" for r in dom_restrict]) if dom_restrict else "all real x")
                + f" | VAs: {', '.join([f'x={_expr_str(v)}' for v in va]) if va else 'None'}"
                + f" | {asym_line}"
                + f" | x-int: {', '.join([f'({_expr_str(z)},0)' for z in xints]) if xints else 'None'}"
                + f" | y-int: {(f'(0,{_expr_str(yint)})' if yint is not None else 'None')}"
            )

            answer_sections = [
                {
                    "label": "① Domain and Reduced Form",
                    "body": (
                        f"Domain restrictions: " + (", ".join([f"x ≠ {_expr_str(r)}" for r in dom_restrict]) if dom_restrict else "none")
                        + f"\nReduced form: {_expr_str(simp)}"
                        + (f"\nHole(s): {', '.join(holes_text)}" if holes_text else "")
                    ),
                },
                {
                    "label": "② Intercepts",
                    "body": (
                        f"x-intercepts: {', '.join([f'({_expr_str(z)},0)' for z in xints]) if xints else 'none'}\n"
                        f"y-intercept: {(f'(0,{_expr_str(yint)})' if yint is not None else 'none')}"
                    ),
                },
                {
                    "label": "③ Asymptotes",
                    "body": (
                        f"Vertical asymptotes: {', '.join([f'x={_expr_str(v)}' for v in va]) if va else 'none'}\n"
                        f"{asym_line}\n"
                        f"Asymptote intersections: {inter_line}"
                    ),
                },
                {
                    "label": "④ Interval Sign/Point Table",
                    "body": "\n".join(step6_lines),
                },
            ]

            graph = None
            try:
                from sympy import lambdify
                f_fn = lambdify(x, simp, "math")
                crit = [float(v.evalf()) for v in set(dom_restrict) | set(xints)]
                if crit:
                    x_lo, x_hi = min(crit) - 3.0, max(crit) + 3.0
                else:
                    x_lo, x_hi = -6.0, 6.0
                kp = [{"x": float(z.evalf()), "y": 0.0, "label": f"x-int ({_expr_str(z)}, 0)", "color": "#2e7d32"} for z in xints]
                if yint is not None:
                    kp.append({"x": 0.0, "y": float(yint.evalf()), "label": f"y-int (0, {_expr_str(yint)})", "color": "#0f3460"})
                kp.extend(hole_points)
                graph = self._make_graph(f_fn, x_lo, x_hi, kp)
            except Exception:
                graph = None

            return steps, answer, answer_sections, graph
        except Exception as e:
            logger.warning(f"rational graph solver failed for '{q}': {e}")
            return self._generic(num, q, meta)

    # -----------------------------------------------------------------------
    # 4.2 - Rational Function Asymptotes (47-56)
    # -----------------------------------------------------------------------
    def _rational_asymptotes(self, num: int, q: str, meta: dict) -> tuple:
        try:
            from sympy import (
                symbols, factor, simplify, Poly, Eq, solveset,
                S, cancel
            )
            from sympy.parsing.sympy_parser import (
                parse_expr, standard_transformations,
                implicit_multiplication_application
            )

            x = symbols("x")
            tf = standard_transformations + (implicit_multiplication_application,)

            name = meta.get("name", "f")
            num_raw = meta.get("numerator", "")
            den_raw = meta.get("denominator", "")
            if not num_raw or not den_raw:
                m = re.search(r"=\s*\((.+)\)/\((.+)\)", q.replace(" ", ""))
                if m:
                    num_raw, den_raw = m.group(1), m.group(2)

            n_expr = parse_expr(str(num_raw).replace("^", "**"), local_dict={"x": x}, transformations=tf)
            d_expr = parse_expr(str(den_raw).replace("^", "**"), local_dict={"x": x}, transformations=tf)

            f_expr = n_expr / d_expr
            n_fact = factor(n_expr)
            d_fact = factor(d_expr)
            simp = cancel(f_expr)

            dom_restrict = sorted(solveset(Eq(d_expr, 0), x, domain=S.Reals), key=lambda v: float(v.evalf()))
            simp_den = simplify(simp.as_numer_denom()[1])
            va = sorted(solveset(Eq(simp_den, 0), x, domain=S.Reals), key=lambda v: float(v.evalf()))
            holes = [r for r in dom_restrict if r not in va]

            n_poly = Poly(simplify(simp.as_numer_denom()[0]), x)
            d_poly = Poly(simplify(simp.as_numer_denom()[1]), x)
            dn, dd = n_poly.degree(), d_poly.degree()

            h_asym = None
            s_asym = None
            asym_explain = ""
            if dn < dd:
                h_asym = "y = 0"
                asym_explain = "degree(numerator) < degree(denominator), so horizontal asymptote is y = 0."
            elif dn == dd:
                ratio = simplify(n_poly.LC() / d_poly.LC())
                h_asym = f"y = {_expr_str(ratio)}"
                asym_explain = "same degree on top and bottom, so horizontal asymptote is ratio of leading coefficients."
            elif dn == dd + 1:
                q_poly, _ = n_poly.div(d_poly)
                s_asym = simplify(q_poly.as_expr())
                asym_explain = "numerator degree is exactly 1 more, so there is a slant (oblique) asymptote from polynomial division."
            else:
                asym_explain = "numerator degree is more than 1 higher than denominator, so there is no horizontal or oblique asymptote."

            va_lines = [f"x = {v}" for v in va] if va else ["None"]
            hole_lines = []
            hole_points = []
            for h in holes:
                y_h = simplify(simp.subs(x, h))
                hole_lines.append(f"x = {_expr_str(h)} (hole at ({_expr_str(h)}, {_expr_str(y_h)}))")
                hole_points.append({"x": float(h.evalf()), "y": float(y_h.evalf()), "label": f"hole ({h}, {y_h})", "color": "#ff9800"})
            if not hole_lines:
                hole_lines = ["None"]

            steps = [
                {
                    "title": "Step 1 - Write the Rational Function and Factor",
                    "body": (
                        f"Given:\n$$ {name}(x)=\\frac{{{n_expr}}}{{{d_expr}}} $$\n\n"
                        f"Factor numerator and denominator:\n"
                        f"$$\\text{{Numerator}} = {_expr_str(n_fact)}$$\n"
                        f"$$\\text{{Denominator}} = {_expr_str(d_fact)}$$"
                    ),
                },
                {
                    "title": "Step 2 - Domain Restrictions and Simplified Form",
                    "body": (
                        "Set denominator = 0 to find forbidden x-values:\n"
                        + "\n".join([f"  x = {_expr_str(r)}" for r in dom_restrict] if dom_restrict else ["  (none)"])
                        + f"\n\nSimplified function (after canceling common factors):\n$$ {name}(x) = {_expr_str(simp)} $$"
                    ),
                },
                {
                    "title": "Step 3 - Vertical Asymptotes and Holes",
                    "body": (
                        "Vertical asymptotes come from the simplified denominator = 0:\n"
                        + "\n".join([f"  {v}" for v in va_lines])
                        + "\n\nAny canceled restriction gives a hole:\n"
                        + "\n".join([f"  {h}" for h in hole_lines])
                    ),
                },
                {
                    "title": "Step 4 - Horizontal or Oblique Asymptote",
                    "body": (
                        f"For the simplified function: degree(top) = {dn}, degree(bottom) = {dd}.\n"
                        f"Rule used: {asym_explain}\n\n"
                        + (f"Horizontal asymptote: {h_asym}" if h_asym else "No horizontal asymptote.")
                        + (f"\nOblique asymptote: y = {_expr_str(s_asym)}" if s_asym is not None else "\nOblique asymptote: None")
                    ),
                },
            ]

            y_int = None
            try:
                y_int = simplify(f_expr.subs(x, 0))
            except Exception:
                y_int = None

            answer_parts = [
                f"Vertical asymptotes: {', '.join([f'x = {_expr_str(v)}' for v in va]) if va else 'None'}",
                f"Horizontal asymptote: {h_asym if h_asym else 'None'}",
                f"Oblique asymptote: {('y = ' + _expr_str(s_asym)) if s_asym is not None else 'None'}",
            ]
            if holes:
                answer_parts.append(
                    "Holes: " + ", ".join([f"({_expr_str(h)}, {_expr_str(simplify(simp.subs(x, h)))})" for h in holes])
                )

            answer = " | ".join(answer_parts)

            answer_sections = [
                {
                    "label": "① Factor and Domain Restrictions",
                    "body": (
                        f"Numerator factorization  : {_expr_str(n_fact)}\n"
                        f"Denominator factorization: {_expr_str(d_fact)}\n\n"
                        + "Domain restrictions (from original denominator):\n"
                        + "\n".join([f"  x = {_expr_str(r)}" for r in dom_restrict] if dom_restrict else ["  none"]) 
                    ),
                },
                {
                    "label": "② Vertical Asymptote Test",
                    "body": (
                        f"Simplified function: {_expr_str(simp)}\n\n"
                        f"Set simplified denominator = 0:\n"
                        + "\n".join([f"  x = {_expr_str(v)}  -> vertical asymptote" for v in va] if va else ["  none"]) 
                    ),
                },
                {
                    "label": "③ Hole Check (canceled factors)",
                    "body": (
                        "Cancellations create removable discontinuities (holes):\n"
                        + "\n".join([f"  {h}" for h in hole_lines])
                    ),
                },
                {
                    "label": "④ Horizontal / Oblique Asymptote",
                    "body": (
                        f"Degree(top) = {dn}, Degree(bottom) = {dd}\n"
                        f"Rule: {asym_explain}\n\n"
                        f"Horizontal asymptote: {h_asym if h_asym else 'None'}\n"
                        f"Oblique asymptote: {('y = ' + _expr_str(s_asym)) if s_asym is not None else 'None'}"
                    ),
                },
            ]

            graph = None
            try:
                from sympy import lambdify
                f_num, f_den = simp.as_numer_denom()
                f_fn = lambdify(x, f_num / f_den, "math")
                xs = [float(v.evalf()) for v in dom_restrict] if dom_restrict else []
                if xs:
                    x_lo, x_hi = min(xs) - 4.0, max(xs) + 4.0
                else:
                    x_lo, x_hi = -6.0, 6.0
                kp = [{"x": float(v.evalf()), "y": None, "label": f"VA x={v}", "color": "#e94560"} for v in va]
                kp.extend(hole_points)
                if y_int is not None and y_int.is_real:
                    kp.append({"x": 0.0, "y": float(y_int.evalf()), "label": f"y-int (0, {y_int})", "color": "#0f3460"})
                graph = self._make_graph(f_fn, x_lo, x_hi, kp)
            except Exception:
                graph = None

            return steps, answer, answer_sections, graph
        except Exception as e:
            logger.warning(f"rational asymptote solver failed for '{q}': {e}")
            return self._generic(num, q, meta)

    # -----------------------------------------------------------------------
    # 4.2 - Rational Application (58)
    # -----------------------------------------------------------------------
    def _rational_application(self, num: int, q: str, meta: dict) -> tuple:
        try:
            from sympy import symbols, simplify, Rational
            from sympy.parsing.sympy_parser import (
                parse_expr, standard_transformations,
                implicit_multiplication_application
            )

            var = meta.get("variable", "t")
            t = symbols(var)
            tf = standard_transformations + (implicit_multiplication_application,)

            name = meta.get("name", "P")
            num_raw = meta.get("numerator", "50*(1 + 0.5*t)")
            den_raw = meta.get("denominator", "2 + 0.01*t")

            n_expr = parse_expr(str(num_raw).replace("^", "**"), local_dict={var: t}, transformations=tf)
            d_expr = parse_expr(str(den_raw).replace("^", "**"), local_dict={var: t}, transformations=tf)
            p_expr = simplify(n_expr / d_expr)

            p0 = simplify(p_expr.subs(t, 0))
            p5 = simplify(p_expr.subs(t, 5))

            # Horizontal asymptote from leading coefficients of linear-over-linear form.
            # Use expansion so coefficients are explicit.
            n_lin = simplify(n_expr.expand())
            d_lin = simplify(d_expr.expand())
            n_a = n_lin.coeff(t, 1)
            d_a = d_lin.coeff(t, 1)
            h_asym = simplify(n_a / d_a) if d_a != 0 else None

            steps = [
                {
                    "title": "Step 1 - Write the Model",
                    "body": (
                        f"Population model:\n$$ {name}({var}) = {p_expr} $$\n"
                        f"where {var} is measured in months."
                    ),
                },
                {
                    "title": "Step 2 - Part (a): Population at t = 0",
                    "body": (
                        f"Substitute {var} = 0:\n"
                        f"$$ {name}(0) = {p0} $$\n"
                        f"So the initial population is {p0}."
                    ),
                },
                {
                    "title": "Step 3 - Part (b): Population after 5 months",
                    "body": (
                        f"Substitute {var} = 5:\n"
                        f"$$ {name}(5) = {p5} $$\n"
                        f"So after 5 months, population is {p5}."
                    ),
                },
                {
                    "title": "Step 4 - Part (c): Horizontal Asymptote and Meaning",
                    "body": (
                        "Because numerator and denominator are both degree 1,\n"
                        "the horizontal asymptote is ratio of leading coefficients:\n"
                        f"$$ y = {h_asym} $$\n"
                        f"Interpretation: the population approaches {h_asym} insects as time becomes very large."
                    ),
                },
            ]

            answer = (
                f"(a) {name}(0) = {p0} | "
                f"(b) {name}(5) = {p5} | "
                f"(c) Horizontal asymptote y = {h_asym}; sustainable largest population ≈ {h_asym}"
            )

            answer_sections = [
                {
                    "label": "(a) Initial Population",
                    "body": (
                        f"Substitute {var}=0:\n"
                        f"  {name}(0) = {p0}\n"
                        f"  Therefore initial population = {p0} insects."
                    ),
                },
                {
                    "label": "(b) Population after 5 months",
                    "body": (
                        f"Substitute {var}=5:\n"
                        f"  {name}(5) = {p5}\n"
                        f"  Therefore population after 5 months = {p5} insects."
                    ),
                },
                {
                    "label": "(c) Horizontal Asymptote and Practical Meaning",
                    "body": (
                        "Degree(top)=Degree(bottom)=1, so use ratio of leading coefficients.\n"
                        f"  Horizontal asymptote: y = {h_asym}\n"
                        f"  Interpretation: maximum sustainable population is about {h_asym} insects."
                    ),
                },
            ]

            graph = None
            try:
                from sympy import lambdify
                f_fn = lambdify(t, p_expr, "math")
                kp = [
                    {"x": 0.0, "y": float(p0.evalf()), "label": f"(0, {p0})", "color": "#0f3460"},
                    {"x": 5.0, "y": float(p5.evalf()), "label": f"(5, {p5})", "color": "#2e7d32"},
                ]
                graph = self._make_graph(f_fn, 0.0, 60.0, kp)
            except Exception:
                graph = None

            return steps, answer, answer_sections, graph
        except Exception as e:
            logger.warning(f"rational application solver failed for '{q}': {e}")
            return self._generic(num, q, meta)

    # -----------------------------------------------------------------------
    # 4.4 - Solving Inequalities Algebraically (selected problems)
    # -----------------------------------------------------------------------
    def _inequality_sign_chart(self, num: int, q: str, meta: dict) -> tuple:
        try:
            from sympy import (
                Eq, FiniteSet, Gt, Ge, Interval, Le, Lt, S, Union,
                cancel, factor, simplify, solveset, symbols, together, roots
            )
            from sympy.parsing.sympy_parser import (
                parse_expr, standard_transformations,
                implicit_multiplication_application
            )
            from sympy.sets.sets import EmptySet
            from sympy.solvers.inequalities import solve_univariate_inequality

            x = symbols("x")
            tf = standard_transformations + (implicit_multiplication_application,)

            left_raw = meta.get("left", "0")
            right_raw = meta.get("right", "0")
            relation = meta.get("relation", ">")

            left_expr = parse_expr(str(left_raw).replace("^", "**"), local_dict={"x": x}, transformations=tf)
            right_expr = parse_expr(str(right_raw).replace("^", "**"), local_dict={"x": x}, transformations=tf)

            work_expr = simplify(left_expr - right_expr)
            combined = together(work_expr)
            num_expr, den_expr = combined.as_numer_denom()
            red_expr = cancel(combined)
            red_num, red_den = red_expr.as_numer_denom()

            left_den = simplify(left_expr.as_numer_denom()[1])
            right_den = simplify(right_expr.as_numer_denom()[1])
            dom_restrict = sorted(
                set(solveset(Eq(left_den, 0), x, domain=S.Reals))
                | set(solveset(Eq(right_den, 0), x, domain=S.Reals)),
                key=lambda v: float(v.evalf()),
            )
            reduced_undefined = sorted(
                solveset(Eq(simplify(red_den), 0), x, domain=S.Reals),
                key=lambda v: float(v.evalf()),
            )
            holes = [r for r in dom_restrict if r not in reduced_undefined]

            zeros_all = sorted(
                solveset(Eq(simplify(red_num), 0), x, domain=S.Reals),
                key=lambda v: float(v.evalf()),
            )
            zeros = [z for z in zeros_all if z not in dom_restrict]
            critical = sorted(set(dom_restrict + zeros), key=lambda v: float(v.evalf()))

            zero_mult = roots(simplify(red_num), x)
            pole_mult = roots(simplify(red_den), x)

            def _sample_point(left, right):
                if left is S.NegativeInfinity and right is S.Infinity:
                    return S.Zero
                if left is S.NegativeInfinity:
                    return simplify(right - 1)
                if right is S.Infinity:
                    return simplify(left + 1)
                return simplify((left + right) / 2)

            def _make_interval(left, right):
                if left is S.NegativeInfinity and right is S.Infinity:
                    return S.Reals
                return Interval(left, right, True, True)

            def _fmt_bound(v):
                if v is S.NegativeInfinity:
                    return "-∞"
                if v is S.Infinity:
                    return "+∞"
                return _expr_str(v)

            def _fmt_set(sol):
                if sol == EmptySet:
                    return "No real solution"
                if sol == S.Reals:
                    return "(-∞, ∞)"
                if isinstance(sol, Interval):
                    lb = "(" if sol.left_open else "["
                    rb = ")" if sol.right_open else "]"
                    return f"{lb}{_fmt_bound(sol.start)}, {_fmt_bound(sol.end)}{rb}"
                if isinstance(sol, FiniteSet):
                    vals = sorted(sol, key=lambda t: float(t.evalf()))
                    return "{" + ", ".join(_expr_str(v) for v in vals) + "}"
                if isinstance(sol, Union):
                    return " ∪ ".join(_fmt_set(part) for part in sol.args)
                return str(sol)

            intervals = []
            if critical:
                intervals.append((S.NegativeInfinity, critical[0]))
                for i in range(len(critical) - 1):
                    intervals.append((critical[i], critical[i + 1]))
                intervals.append((critical[-1], S.Infinity))
            else:
                intervals.append((S.NegativeInfinity, S.Infinity))

            want_positive = relation in (">", ">=")
            include_equal = relation in (">=", "<=")

            sign_rows = []
            selected_pieces = []
            for left, right in intervals:
                test_x = _sample_point(left, right)
                test_val = simplify(red_expr.subs(x, test_x))
                is_positive = bool(test_val.evalf() > 0)
                sign_symbol = "+" if is_positive else "−"
                keep_interval = is_positive if want_positive else not is_positive
                sign_rows.append({
                    "left": left,
                    "right": right,
                    "test_x": test_x,
                    "test_val": test_val,
                    "sign": sign_symbol,
                    "keep": keep_interval,
                })
                if keep_interval:
                    selected_pieces.append(_make_interval(left, right))

            if include_equal:
                for z in zeros:
                    selected_pieces.append(FiniteSet(z))

            manual_solution = EmptySet if not selected_pieces else Union(*selected_pieces)

            relation_obj = {
                ">": Gt(work_expr, 0),
                ">=": Ge(work_expr, 0),
                "<": Lt(work_expr, 0),
                "<=": Le(work_expr, 0),
            }[relation]
            exact_solution = solve_univariate_inequality(relation_obj, x, relational=False)
            final_solution = exact_solution if exact_solution is not None else manual_solution

            critical_lines = []
            for c in critical:
                if c in zeros:
                    mult = zero_mult.get(c)
                    if mult is not None:
                        critical_lines.append(f"  x = {_expr_str(c)}  makes the numerator zero (multiplicity {mult})")
                    else:
                        critical_lines.append(f"  x = {_expr_str(c)}  makes the numerator zero")
                else:
                    mult = pole_mult.get(c)
                    if mult is not None:
                        critical_lines.append(f"  x = {_expr_str(c)}  makes the denominator zero, so it is excluded from the domain (multiplicity {mult})")
                    else:
                        critical_lines.append(f"  x = {_expr_str(c)}  makes the denominator zero, so it is excluded from the domain")

            sign_lines = []
            for row in sign_rows:
                sign_lines.append(
                    f"  ({_fmt_bound(row['left'])}, {_fmt_bound(row['right'])})  test x = {_expr_str(row['test_x'])}:  value = {_expr_str(row['test_val'])}  -> sign {row['sign']}"
                    + ("  KEEP" if row["keep"] else "  REJECT")
                )

            zero_line = ", ".join(_expr_str(z) for z in zeros) if zeros else "none"
            domain_line = ", ".join(f"x ≠ {_expr_str(r)}" for r in dom_restrict) if dom_restrict else "none"
            holes_line = ", ".join(_expr_str(h) for h in holes) if holes else "none"

            steps = [
                {
                    "title": "Step 1 - Move Everything to One Side",
                    "body": (
                        f"Start with the inequality:\n$$ {_expr_str(left_expr)} {relation} {_expr_str(right_expr)} $$\n\n"
                        f"Move everything to the left so the right side is 0:\n$$ {_expr_str(combined)} {relation} 0 $$"
                    ),
                },
                {
                    "title": "Step 2 - Factor and State the Domain Restrictions",
                    "body": (
                        f"Numerator factorization: {_expr_str(factor(num_expr))}\n"
                        f"Denominator factorization: {_expr_str(factor(den_expr))}\n"
                        f"Reduced expression for sign testing: {_expr_str(red_expr)}\n"
                        f"Domain restriction(s): {domain_line}"
                        + (f"\nHole(s) after cancellation: {holes_line}" if holes else "")
                    ),
                },
                {
                    "title": "Step 3 - Find the Critical Numbers",
                    "body": (
                        "Critical numbers come from zeros of the numerator and denominator.\n"
                        + "\n".join(critical_lines)
                        + (f"\n\nPlace these on a number line in increasing order: {', '.join(_expr_str(c) for c in critical)}" if critical else "\n\nThere are no critical numbers.")
                    ),
                },
                {
                    "title": "Step 4 - Test the Sign on Each Interval",
                    "body": "Use one test value in each interval:\n" + "\n".join(sign_lines),
                },
                {
                    "title": "Step 5 - Write the Solution Set",
                    "body": (
                        f"We need the expression to be {'positive' if want_positive else 'negative'}"
                        + (" or zero" if include_equal else "")
                        + f".\nTherefore the solution is:\n{_fmt_set(final_solution)}"
                        + (f"\nInclude zero(s) of the numerator because the inequality is {relation}." if include_equal and zeros else "")
                        + (f"\nExclude x = {', '.join(_expr_str(r) for r in dom_restrict)} because the original expression is undefined there." if dom_restrict else "")
                    ),
                },
            ]

            answer = f"Solution: {_fmt_set(final_solution)}"

            answer_sections = [
                {
                    "label": "① Rewrite in Standard Form",
                    "body": (
                        f"  {_expr_str(left_expr)} {relation} {_expr_str(right_expr)}\n"
                        f"  ⇔ {_expr_str(combined)} {relation} 0"
                    ),
                },
                {
                    "label": "② Critical Numbers",
                    "body": (
                        f"  Zeros of numerator: {zero_line}\n"
                        f"  Excluded values: {domain_line}\n"
                        + (f"  Holes after cancellation: {holes_line}\n" if holes else "")
                        + ("\n".join(critical_lines) if critical_lines else "  None")
                    ),
                },
                {
                    "label": "③ Sign Chart Decision",
                    "body": "\n".join(sign_lines),
                },
                {
                    "label": "④ Final Answer",
                    "body": (
                        f"  Solution set: {_fmt_set(final_solution)}\n"
                        + (f"  Include zero(s) of the numerator because {relation} allows equality.\n" if include_equal and zeros else "")
                        + (f"  Exclude x = {', '.join(_expr_str(r) for r in dom_restrict)} because the expression is undefined there." if dom_restrict else "")
                    ),
                },
            ]

            graph = None
            try:
                from sympy import lambdify
                f_fn = lambdify(x, red_expr, "math")
                finite_pts = [float(v.evalf()) for v in critical] if critical else []
                x_lo = (min(finite_pts) - 3.0) if finite_pts else -6.0
                x_hi = (max(finite_pts) + 3.0) if finite_pts else 6.0
                kp = [
                    {"x": float(z.evalf()), "y": 0.0, "label": f"zero x={_expr_str(z)}", "color": "#2e7d32"}
                    for z in zeros
                ]
                graph = self._make_graph(f_fn, x_lo, x_hi, kp)
            except Exception:
                graph = None

            return steps, answer, answer_sections, graph
        except Exception as e:
            logger.warning(f"inequality sign-chart solver failed for '{q}': {e}")
            return self._generic(num, q, meta)

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

            # ── exam answer sections ──────────────────────────────────────
            a_sec = (
                f"  f(x) = {expanded_str}\n\n"
                f"  Degree              = {deg}   (highest power of x)\n"
                f"  Leading coefficient = {lc_str}\n"
                f"  Leading term        = ${lt_str}$"
            )

            if real_zeros:
                b_lines = ["  Set factors equal to zero:\n"]
                for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                    m = real_zeros[z]
                    z_str = _fmt_zero(z)
                    b_lines.append(f"    x = {z_str}   (multiplicity {m})")
                b_lines.append(f"\n  y-intercept: f(0) = {y_int_str}  →  point (0, {y_int_str})")
            else:
                b_lines = [
                    "  No real zeros — graph never crosses or touches the x-axis.",
                    f"\n  y-intercept: f(0) = {y_int_str}  →  point (0, {y_int_str})"
                ]
            b_sec = "\n".join(b_lines)

            if real_zeros:
                c_lines = [
                    "  Rule: ODD multiplicity  → graph CROSSES (passes through) x-axis",
                    "        EVEN multiplicity → graph TOUCHES x-axis and bounces back\n"
                ]
                for z in sorted(real_zeros, key=lambda r: float(r.evalf())):
                    m = real_zeros[z]
                    z_str = _fmt_zero(z)
                    behavior = "CROSSES" if m % 2 == 1 else "TOUCHES (bounces back)"
                    c_lines.append(f"  x = {z_str}  (mult {m}, {'odd' if m%2==1 else 'even'})  →  {behavior}")
                c_sec = "\n".join(c_lines)
            else:
                c_sec = "  No real zeros — no x-intercepts to cross or touch."

            d_sec = (
                f"  Formula: maximum turning points = degree − 1\n\n"
                f"  = {deg} − 1 = {max_tp}\n\n"
                f"  ∴  This graph has at most {max_tp} turning point(s)."
            )

            e_sec = (
                f"  Leading term: ${lt_str}$\n"
                f"  Degree = {deg} ({'EVEN' if deg % 2 == 0 else 'ODD'}),  "
                f"a = {lc_str} ({'positive' if lc > 0 else 'negative'})\n\n"
                f"  {_end_math(deg, lc)}\n"
                f"  → {_end_plain(deg, lc)}"
            )

            answer_sections = [
                {"label": "(a) Degree & Leading Term", "body": a_sec},
                {"label": "(b) Zeros (x-intercepts) & y-intercept", "body": b_sec},
                {"label": "(c) Cross or Touch the x-axis?", "body": c_sec},
                {"label": "(d) Maximum Number of Turning Points", "body": d_sec},
                {"label": "(e) End Behavior", "body": e_sec},
            ]
            return steps, answer, answer_sections, graph

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
