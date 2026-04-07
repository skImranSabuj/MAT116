from __future__ import annotations
"""
sample_data.py
--------------
Hand-coded Section 4.1 problems from Sullivan Precalculus 10th Edition.

Used as **fallback** when the PDF parser cannot locate a problem, or when
running the project without a PDF file.  The data reflects the actual problem
types in Section 4.1 ("Polynomial Functions and Models").
"""

# Each entry: {"number": int, "question": str}
# • Transformation problems 37-50   ( graphing using transformations )
# • Form-polynomial problems 51-56  ( build polynomial from zeros     )
# • Analysis problems 57-68         ( analyze / sketch polynomial     )
# • Application problems 81-90      ( real-world polynomial models    )

SECTION_4_1_PROBLEMS: list[dict] = [
    # ── Graphing using transformations ────────────────────────────────────────
    {"number": 37, "question": "Graph f(x) = (x + 1)^3 using transformations."},
    {"number": 38, "question": "Graph f(x) = (x - 2)^3 using transformations."},
    {"number": 39, "question": "Graph f(x) = (x + 1)^4 using transformations."},
    {"number": 40, "question": "Graph f(x) = (x - 2)^4 using transformations."},
    {"number": 41, "question": "Graph f(x) = (x - 1)^4 + 2 using transformations."},
    {"number": 42, "question": "Graph f(x) = (x + 2)^4 - 3 using transformations."},
    {"number": 43, "question": "Graph f(x) = -(x + 2)^3 using transformations."},
    {"number": 44, "question": "Graph f(x) = -(x - 3)^3 + 1 using transformations."},
    {"number": 45, "question": "Graph f(x) = 2(x - 1)^4 using transformations."},
    {"number": 46, "question": "Graph f(x) = (1/2)(x + 1)^4 - 2 using transformations."},
    {"number": 47, "question": "Graph f(x) = (x - 1)^5 using transformations."},
    {"number": 48, "question": "Graph f(x) = (x + 2)^5 - 3 using transformations."},
    {"number": 49, "question": "Graph f(x) = -2(x + 1)^5 + 3 using transformations."},
    {"number": 50, "question": "Graph f(x) = 3(x - 2)^5 - 1 using transformations."},

    # ── Form polynomial with given degree and zeros ───────────────────────────
    {
        "number": 51,
        "question": (
            "Form a polynomial f(x) with real coefficients having degree 3 "
            "and zeros: -3, 0, 4. Use 1 as the leading coefficient."
        ),
    },
    {
        "number": 52,
        "question": (
            "Form a polynomial f(x) with real coefficients having degree 4 "
            "and zeros: -1, 2 (multiplicity 2), 4. Use 1 as the leading coefficient."
        ),
    },
    {
        "number": 53,
        "question": (
            "Form a polynomial f(x) with real coefficients having degree 4 "
            "and zeros: 1, -2 (each multiplicity 1) and 3 (multiplicity 2). "
            "Use 1 as the leading coefficient."
        ),
    },
    {
        "number": 54,
        "question": (
            "Form a polynomial f(x) with real coefficients having degree 5 "
            "and zeros: -2 (multiplicity 2), 0, 1 (multiplicity 2). "
            "Use 1 as the leading coefficient."
        ),
    },
    {
        "number": 55,
        "question": (
            "Form a polynomial f(x) with real coefficients having degree 3 "
            "and zeros: 4 + i, 3. Use 1 as the leading coefficient."
        ),
    },
    {
        "number": 56,
        "question": (
            "Form a polynomial f(x) with real coefficients having degree 4 "
            "and zeros: i, 1 + 2i. Use 1 as the leading coefficient."
        ),
    },

    # ── Analyze polynomial functions ──────────────────────────────────────────
    {
        "number": 57,
        "question": (
            "For f(x) = x^2(x - 3)(x + 4): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 58,
        "question": (
            "For f(x) = x(x + 2)(x - 4): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 59,
        "question": (
            "For f(x) = (x + 4)^2(x - 3): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 60,
        "question": (
            "For f(x) = (x - 2)^2(x + 3): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 61,
        "question": (
            "For f(x) = (x - 1)(x + 3)(x + 5): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 62,
        "question": (
            "For f(x) = (x + 1)(x - 2)(x - 4): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 63,
        "question": (
            "For f(x) = x^2(x - 2)(x^2 + 3): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 64,
        "question": (
            "For f(x) = x^3(x + 2)(x^2 + 1): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 65,
        "question": (
            "For f(x) = (x - 1)^2(x + 2)^2: "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 66,
        "question": (
            "For f(x) = (x + 1)^2(x - 3)^2: "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 67,
        "question": (
            "For f(x) = x^2(x - 3)^3(x + 1): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },
    {
        "number": 68,
        "question": (
            "For f(x) = x^4(x^2 - 1)(x + 1): "
            "(a) Find the degree and the leading term. "
            "(b) Find the x- and y-intercepts. "
            "(c) Determine whether the graph crosses or touches the x-axis at each intercept. "
            "(d) Find the maximum number of turning points. "
            "(e) Determine the end behavior."
        ),
    },

    # ── Application problems ──────────────────────────────────────────────────
    {
        "number": 81,
        "question": (
            "A box with no top is to be made from a 12-inch by 12-inch piece of "
            "cardboard by cutting equal squares of side x from each corner and "
            "folding up the sides. "
            "(a) Express the volume V as a function of x. "
            "(b) What is the domain of V? "
            "(c) Find the maximum volume and the value of x that gives it."
        ),
    },
    {
        "number": 82,
        "question": (
            "A box with no top is to be made from a 10-inch by 16-inch piece of "
            "cardboard by cutting equal squares of side x from each corner and "
            "folding up the sides. "
            "(a) Express the volume V as a function of x. "
            "(b) What is the domain of V? "
            "(c) Find the maximum volume and the value of x that gives it."
        ),
    },
    {
        "number": 83,
        "question": (
            "The revenue R received by a company selling x units of a product "
            "is R(x) = -0.5x^2 + 100x. "
            "(a) Find the revenue at x = 50 and x = 120. "
            "(b) Find the number of units that maximises revenue. "
            "(c) What is the maximum revenue?"
        ),
    },
    {
        "number": 84,
        "question": (
            "A farmer with 200 feet of fencing wants to enclose a rectangular "
            "area and then divide it in half with a fence parallel to one of the "
            "sides. "
            "(a) Express the total area A enclosed as a function of the width w. "
            "(b) What is the maximum area? "
            "(c) What dimensions give the maximum area?"
        ),
    },
    {
        "number": 85,
        "question": (
            "A manufacturer finds that the cost C (in dollars) of producing "
            "x units is C(x) = 0.002x^3 - 3x^2 + 1500x + 4000. "
            "Find the production level x that minimises the marginal cost C'(x)."
        ),
    },
    {
        "number": 86,
        "question": (
            "The profit P (in thousands of dollars) a company earns from selling "
            "x hundred units is P(x) = -x^3 + 6x^2 + 15x - 12. "
            "Find all values of x for which P(x) > 0 (profitable range)."
        ),
    },
    {
        "number": 87,
        "question": (
            "A projectile is launched from the ground. Its height h (in feet) "
            "after t seconds is modelled by h(t) = -16t^2 + 80t. "
            "(a) Find the maximum height. "
            "(b) When does it return to the ground?"
        ),
    },
    {
        "number": 88,
        "question": (
            "The population P (in thousands) of a city t years after 2000 is "
            "modelled by P(t) = -0.01t^3 + 0.3t^2 + 2t + 50. "
            "(a) What was the population in 2000? "
            "(b) Predict the population in 2020."
        ),
    },
    {
        "number": 89,
        "question": (
            "A tank in the shape of an inverted cone has height 10 m and base "
            "radius 4 m. Water is poured in to a depth of x metres. "
            "(a) Express the volume V of water as a polynomial in x. "
            "(b) Find V when x = 5."
        ),
    },
    {
        "number": 90,
        "question": (
            "A wire 36 inches long is cut into two pieces. One piece is bent "
            "into a square and the other into a circle. "
            "(a) Express the total area A as a function of the side s of the square. "
            "(b) Find the value of s that minimises the total area."
        ),
    },
]

# Build a lookup dict for O(1) access by problem number
PROBLEM_LOOKUP: dict[int, dict] = {p["number"]: p for p in SECTION_4_1_PROBLEMS}


def get_problems(problem_ranges: list[str]) -> list[dict]:
    """
    Return sample problems from SECTION_4_1_PROBLEMS that match
    the given *problem_ranges* (e.g. ["37-42", "57-68"]).
    Problems are returned sorted by number.
    """
    from parser import expand_ranges  # local import to avoid circular ref at top
    target = expand_ranges(problem_ranges)
    found = [PROBLEM_LOOKUP[n] for n in sorted(target) if n in PROBLEM_LOOKUP]
    return found
