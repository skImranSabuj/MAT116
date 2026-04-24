from __future__ import annotations
"""
sample_data.py
--------------
EXACT problems from Sullivan Precalculus 10th Edition, Section 4.1
transcribed directly from the scanned textbook pages.

Problem groups:
  37-42  – Graph using transformations
  43-50  – Form polynomial from zeros (degree given)
  51-56  – Find polynomial through a specific point
  57-68  – Analyze polynomial (zeros, behavior, turning points)
  81-90  – Full analysis following Steps 1-5 (p.215)
"""

SECTION_4_1_PROBLEMS: list[dict] = [

    # ── PROBLEMS 37-42: Graph using transformations ───────────────────────────
    {"number": 37, "question": "f(x) = (x + 2)^4 - 3", "type": "transformation", "meta": {"a": 1,    "h": -2, "n": 4, "k": -3}},
    {"number": 38, "question": "f(x) = (x - 1)^5 + 2", "type": "transformation", "meta": {"a": 1,    "h":  1, "n": 5, "k":  2}},
    {"number": 39, "question": "f(x) = (1/2)(x - 1)^5 - 2", "type": "transformation", "meta": {"a": 0.5,  "h":  1, "n": 5, "k": -2}},
    {"number": 40, "question": "f(x) = 2(x + 1)^4 + 1", "type": "transformation", "meta": {"a": 2,    "h": -1, "n": 4, "k":  1}},
    {"number": 41, "question": "f(x) = 3 - (x + 2)^4",  "type": "transformation", "meta": {"a": -1,   "h": -2, "n": 4, "k":  3}},
    {"number": 42, "question": "f(x) = 4 - (x - 2)^5",  "type": "transformation", "meta": {"a": -1,   "h":  2, "n": 5, "k":  4}},

    # ── PROBLEMS 43-50: Form polynomial (degree and zeros given) ──────────────
    {"number": 43, "question": "Zeros: -1, 1, 3; degree 3",                                     "type": "form_polynomial", "meta": {"zeros": [(-1,1),(1,1),(3,1)],                    "degree": 3}},
    {"number": 44, "question": "Zeros: -2, 2, 3; degree 3",                                     "type": "form_polynomial", "meta": {"zeros": [(-2,1),(2,1),(3,1)],                    "degree": 3}},
    {"number": 45, "question": "Zeros: -4, 0, 2; degree 3",                                     "type": "form_polynomial", "meta": {"zeros": [(-4,1),(0,1),(2,1)],                    "degree": 3}},
    {"number": 46, "question": "Zeros: -3, 0, 4; degree 3",                                     "type": "form_polynomial", "meta": {"zeros": [(-3,1),(0,1),(4,1)],                    "degree": 3}},
    {"number": 47, "question": "Zeros: -3, -1, 2, 5; degree 4",                                 "type": "form_polynomial", "meta": {"zeros": [(-3,1),(-1,1),(2,1),(5,1)],             "degree": 4}},
    {"number": 48, "question": "Zeros: -4, -1, 2, 3; degree 4",                                 "type": "form_polynomial", "meta": {"zeros": [(-4,1),(-1,1),(2,1),(3,1)],             "degree": 4}},
    {"number": 49, "question": "Zeros: -2 (multiplicity 2), 4 (multiplicity 1); degree 3",      "type": "form_polynomial", "meta": {"zeros": [(-2,2),(4,1)],                          "degree": 3}},
    {"number": 50, "question": "Zeros: -1 (multiplicity 1), 3 (multiplicity 2); degree 3",      "type": "form_polynomial", "meta": {"zeros": [(-1,1),(3,2)],                          "degree": 3}},

    # ── PROBLEMS 51-56: Find polynomial passing through a given point ─────────
    {"number": 51, "question": "Zeros: -2, 0, 2  |  Point: (-4, 16)",   "type": "form_polynomial_point", "meta": {"zeros": [(-2,1),(0,1),(2,1)],        "point": (-4, 16)}},
    {"number": 52, "question": "Zeros: -3, 1, 4  |  Point: (6, 180)",   "type": "form_polynomial_point", "meta": {"zeros": [(-3,1),(1,1),(4,1)],        "point": (6, 180)}},
    {"number": 53, "question": "Zeros: -5, -1, 2, 6  |  Point: (5/2, 15)", "type": "form_polynomial_point", "meta": {"zeros": [(-5,1),(-1,1),(2,1),(6,1)], "point": (2.5, 15)}},
    {"number": 54, "question": "Zeros: -1, 0, 2, 4  |  Point: (1/2, 63)", "type": "form_polynomial_point", "meta": {"zeros": [(-1,1),(0,1),(2,1),(4,1)], "point": (0.5, 63)}},
    {"number": 55, "question": "Zeros: -1 (multiplicity 2), 0 (multiplicity 2), 3 (multiplicity 2)  |  Point: (1, -48)", "type": "form_polynomial_point", "meta": {"zeros": [(-1,2),(0,2),(3,2)], "point": (1, -48)}},
    {"number": 56, "question": "Zeros: -1 (multiplicity 2), 1 (multiplicity 2)  |  Point: (-2, 45)",  "type": "form_polynomial_point", "meta": {"zeros": [(-1,2),(1,2)], "point": (-2, 45)}},

    # ── PROBLEMS 57-68: Analyze polynomial (zeros, cross/touch, turning pts, end behavior) ──
    {"number": 57, "question": "f(x) = 3(x - 7)(x + 3)^2",           "type": "analysis"},
    {"number": 58, "question": "f(x) = 4(x + 4)(x + 3)^3",           "type": "analysis"},
    {"number": 59, "question": "f(x) = 2(x - 3)(x^2 + 4)^3",         "type": "analysis"},
    {"number": 60, "question": "f(x) = 4(x^2 + 1)(x - 2)^3",         "type": "analysis"},
    {"number": 61, "question": "f(x) = (x - 1/3)^2 (x - 1)^3",       "type": "analysis"},
    {"number": 62, "question": "f(x) = -2(x + 1/2)^2 (x + 4)^3",     "type": "analysis"},
    {"number": 63, "question": "f(x) = (x + sqrt(3))^2 (x - 2)^4",   "type": "analysis"},
    {"number": 64, "question": "f(x) = (x - 5)^3 (x + 4)^2",         "type": "analysis"},
    {"number": 65, "question": "f(x) = -2(x^2 + 3)^3",               "type": "analysis"},
    {"number": 66, "question": "f(x) = 3(x^2 + 8)(x^2 + 9)^2",       "type": "analysis"},
    {"number": 67, "question": "f(x) = 4x(x^2 - 3)",                  "type": "analysis"},
    {"number": 68, "question": "f(x) = -2x^2(x^2 - 2)",               "type": "analysis"},

    # ── PROBLEMS 81-90: Full sketch analysis (Steps 1-5) ─────────────────────
    {"number": 81, "question": "f(x) = x^2(x - 3)",                    "type": "analysis_full"},
    {"number": 82, "question": "f(x) = x(x + 2)^2",                    "type": "analysis_full"},
    {"number": 83, "question": "f(x) = (x - 1)(x + 3)^2",              "type": "analysis_full"},
    {"number": 84, "question": "f(x) = (x + 4)^2 (1 - x)",             "type": "analysis_full"},
    {"number": 85, "question": "f(x) = -(1/2)(x + 4)(x - 1)^3",        "type": "analysis_full"},
    {"number": 86, "question": "f(x) = -2(x + 2)(x - 2)^3",            "type": "analysis_full"},
    {"number": 87, "question": "f(x) = (x - 1)(x + 4)(x - 3)",         "type": "analysis_full"},
    {"number": 88, "question": "f(x) = (x + 1)(x - 2)(x + 4)",         "type": "analysis_full"},
    {"number": 89, "question": "f(x) = x^2(x - 3)(x + 4)",             "type": "analysis_full"},
    {"number": 90, "question": "f(x) = x^2(x - 2)(x + 2)",             "type": "analysis_full"},
]

SECTION_4_5_PROBLEMS: list[dict] = [
  # ── PROBLEMS 47-56: Rational asymptotes ─────────────────────────────────
  {
    "number": 47,
    "question": "H(x) = (x^3 - 8)/(x^2 - 5x + 6)",
    "type": "rational_asymptotes",
    "meta": {"name": "H", "numerator": "x^3 - 8", "denominator": "x^2 - 5x + 6"},
  },
  {
    "number": 48,
    "question": "G(x) = (x^3 + 1)/(x^2 - 5x - 14)",
    "type": "rational_asymptotes",
    "meta": {"name": "G", "numerator": "x^3 + 1", "denominator": "x^2 - 5x - 14"},
  },
  {
    "number": 49,
    "question": "T(x) = x^3/(x^4 - 1)",
    "type": "rational_asymptotes",
    "meta": {"name": "T", "numerator": "x^3", "denominator": "x^4 - 1"},
  },
  {
    "number": 50,
    "question": "P(x) = 4x^2/(x^3 - 1)",
    "type": "rational_asymptotes",
    "meta": {"name": "P", "numerator": "4x^2", "denominator": "x^3 - 1"},
  },
  {
    "number": 51,
    "question": "F(x) = (x^2 + 6x + 5)/(2x^2 + 7x + 5)",
    "type": "rational_asymptotes",
    "meta": {"name": "F", "numerator": "x^2 + 6x + 5", "denominator": "2x^2 + 7x + 5"},
  },
  {
    "number": 52,
    "question": "Q(x) = (2x^2 - 5x - 12)/(3x^2 - 11x - 4)",
    "type": "rational_asymptotes",
    "meta": {"name": "Q", "numerator": "2x^2 - 5x - 12", "denominator": "3x^2 - 11x - 4"},
  },
  {
    "number": 53,
    "question": "R(x) = (8x^2 + 26x - 7)/(4x - 1)",
    "type": "rational_asymptotes",
    "meta": {"name": "R", "numerator": "8x^2 + 26x - 7", "denominator": "4x - 1"},
  },
  {
    "number": 54,
    "question": "R(x) = (6x^2 + 7x - 5)/(3x + 5)",
    "type": "rational_asymptotes",
    "meta": {"name": "R", "numerator": "6x^2 + 7x - 5", "denominator": "3x + 5"},
  },
  {
    "number": 55,
    "question": "F(x) = (x^4 - 16)/(x^2 - 2x)",
    "type": "rational_asymptotes",
    "meta": {"name": "F", "numerator": "x^4 - 16", "denominator": "x^2 - 2x"},
  },
  {
    "number": 56,
    "question": "G(x) = (x^4 - 1)/(x^2 - x)",
    "type": "rational_asymptotes",
    "meta": {"name": "G", "numerator": "x^4 - 1", "denominator": "x^2 - x"},
  },

  # ── PROBLEM 58: Population model application ────────────────────────────
  {
    "number": 58,
    "question": "P(t) = 50(1 + 0.5t)/(2 + 0.01t)",
    "type": "rational_application",
    "meta": {
      "name": "P",
      "numerator": "50*(1 + t/2)",
      "denominator": "2 + t/100",
      "variable": "t",
      "parts": [
        "(a) Population at t = 0",
        "(b) Population at t = 5",
        "(c) Horizontal asymptote and sustainable largest population",
      ],
    },
  },
]


SECTION_4_3_PROBLEMS: list[dict] = [
  {
    "number": 15,
    "question": "H(x) = (x^3 - 1)/(x^2 - 9)",
    "type": "rational_graph_analysis",
    "meta": {"name": "H", "numerator": "x^3 - 1", "denominator": "x^2 - 9"},
  },
  {
    "number": 16,
    "question": "G(x) = (x^3 + 1)/(x^2 + 2x)",
    "type": "rational_graph_analysis",
    "meta": {"name": "G", "numerator": "x^3 + 1", "denominator": "x^2 + 2x"},
  },
  {
    "number": 17,
    "question": "R(x) = (x^2 + x - 12)/(x^2 - 4)",
    "type": "rational_graph_analysis",
    "meta": {"name": "R", "numerator": "x^2 + x - 12", "denominator": "x^2 - 4"},
  },
  {
    "number": 18,
    "question": "R(x) = x^2/(x^2 + x - 6)",
    "type": "rational_graph_analysis",
    "meta": {"name": "R", "numerator": "x^2", "denominator": "x^2 + x - 6"},
  },
  {
    "number": 19,
    "question": "G(x) = 3x/(x^2 - 1)",
    "type": "rational_graph_analysis",
    "meta": {"name": "G", "numerator": "3x", "denominator": "x^2 - 1"},
  },
  {
    "number": 20,
    "question": "G(x) = x/(x^2 - 4)",
    "type": "rational_graph_analysis",
    "meta": {"name": "G", "numerator": "x", "denominator": "x^2 - 4"},
  },
]


SECTION_4_4_PROBLEMS: list[dict] = [
  {
    "number": 20,
    "question": "(x - 5)^2 (x + 2) < 0",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "(x - 5)^2 (x + 2)",
      "relation": "<",
      "right": "0",
    },
  },
  {
    "number": 22,
    "question": "x^3 + 8x^2 < 0",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "x^3 + 8x^2",
      "relation": "<",
      "right": "0",
    },
  },
  {
    "number": 28,
    "question": "x^3 - 2x^2 - 3x > 0",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "x^3 - 2x^2 - 3x",
      "relation": ">",
      "right": "0",
    },
  },
  {
    "number": 35,
    "question": "((x - 3)(x + 2))/(x - 1) <= 0",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "((x - 3)(x + 2))/(x - 1)",
      "relation": "<=",
      "right": "0",
    },
  },
  {
    "number": 37,
    "question": "((x + 5)^2)/(x^2 - 4) >= 0",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "((x + 5)^2)/(x^2 - 4)",
      "relation": ">=",
      "right": "0",
    },
  },
  {
    "number": 40,
    "question": "(x + 2)/(x - 4) >= 1",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "(x + 2)/(x - 4)",
      "relation": ">=",
      "right": "1",
    },
  },
  {
    "number": 43,
    "question": "5/(x - 3) > 3/(x + 1)",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "5/(x - 3)",
      "relation": ">",
      "right": "3/(x + 1)",
    },
  },
  {
    "number": 44,
    "question": "1/(x - 2) < 2/(3x - 9)",
    "type": "inequality_sign_chart",
    "meta": {
      "left": "1/(x - 2)",
      "relation": "<",
      "right": "2/(3x - 9)",
    },
  },
]


SECTION_5_6_PROBLEMS: list[dict] = [
  # Problems 15-30: logarithmic equations
  {"number": 15, "question": "Solve: 2 log_3(x + 4) - log_3 9 = 2", "type": "log_equation", "meta": {"equation": "2*log(x+4,3)-log(9,3)=2"}},
  {"number": 16, "question": "Solve: 3 log_2(x - 1) + log_2 4 = 5", "type": "log_equation", "meta": {"equation": "3*log(x-1,2)+log(4,2)=5"}},
  {"number": 17, "question": "Solve: log x + log(x - 21) = 2", "type": "log_equation", "meta": {"equation": "log(x,10)+log(x-21,10)=2"}},
  {"number": 18, "question": "Solve: log x + log(x + 15) = 2", "type": "log_equation", "meta": {"equation": "log(x,10)+log(x+15,10)=2"}},
  {"number": 19, "question": "Solve: log(2x) - log(x - 3) = 1", "type": "log_equation", "meta": {"equation": "log(2*x,10)-log(x-3,10)=1"}},
  {"number": 20, "question": "Solve: log(2x + 1) = 1 + log(x - 2)", "type": "log_equation", "meta": {"equation": "log(2*x+1,10)=1+log(x-2,10)"}},
  {"number": 21, "question": "Solve: log_2(x + 7) + log_2(x + 8) = 1", "type": "log_equation", "meta": {"equation": "log(x+7,2)+log(x+8,2)=1"}},
  {"number": 22, "question": "Solve: log_6(x + 4) + log_6(x + 3) = 1", "type": "log_equation", "meta": {"equation": "log(x+4,6)+log(x+3,6)=1"}},
  {"number": 23, "question": "Solve: log_5(x + 3) = 1 - log_5(x - 1)", "type": "log_equation", "meta": {"equation": "log(x+3,5)=1-log(x-1,5)"}},
  {"number": 24, "question": "Solve: log_8(x + 6) = 1 - log_8(x + 4)", "type": "log_equation", "meta": {"equation": "log(x+6,8)=1-log(x+4,8)"}},
  {"number": 25, "question": "Solve: ln(x + 1) - ln x = 2", "type": "log_equation", "meta": {"equation": "log(x+1)-log(x)=2"}},
  {"number": 26, "question": "Solve: ln x + ln(x + 2) = 4", "type": "log_equation", "meta": {"equation": "log(x)+log(x+2)=4"}},
  {"number": 27, "question": "Solve: log_2(x + 1) + log_2(x + 7) = 3", "type": "log_equation", "meta": {"equation": "log(x+1,2)+log(x+7,2)=3"}},
  {"number": 28, "question": "Solve: log_3(x + 1) + log_3(x + 4) = 2", "type": "log_equation", "meta": {"equation": "log(x+1,3)+log(x+4,3)=2"}},
  {"number": 29, "question": "Solve: log_4(x^2 - 9) - log_4(x + 3) = 3", "type": "log_equation", "meta": {"equation": "log(x**2-9,4)-log(x+3,4)=3"}},
  {"number": 30, "question": "Solve: log_(1/3)(x^2 + x) - log_(1/3)(x^2 - x) = -1", "type": "log_equation", "meta": {"equation": "log(x**2+x,Rational(1,3))-log(x**2-x,Rational(1,3))=-1"}},

  # Problems 57-68: exponential equations
  {"number": 57, "question": "Solve: 3^(2x) + 3^x - 2 = 0", "type": "exp_equation", "meta": {"equation": "3**(2*x)+3**x-2=0"}},
  {"number": 58, "question": "Solve: 2^(2x) + 2^x - 12 = 0", "type": "exp_equation", "meta": {"equation": "2**(2*x)+2**x-12=0"}},
  {"number": 59, "question": "Solve: 2^(2x) + 2^(x+2) - 12 = 0", "type": "exp_equation", "meta": {"equation": "2**(2*x)+2**(x+2)-12=0"}},
  {"number": 60, "question": "Solve: 3^(2x) + 3^(x+1) - 4 = 0", "type": "exp_equation", "meta": {"equation": "3**(2*x)+3**(x+1)-4=0"}},
  {"number": 61, "question": "Solve: 16^x + 4^(x+1) - 3 = 0", "type": "exp_equation", "meta": {"equation": "16**x+4**(x+1)-3=0"}},
  {"number": 62, "question": "Solve: 9^x - 3^(x+1) + 1 = 0", "type": "exp_equation", "meta": {"equation": "9**x-3**(x+1)+1=0"}},
  {"number": 63, "question": "Solve: 6^x - 6*6^(-x) = -9", "type": "exp_equation", "meta": {"equation": "6**x-6*6**(-x)=-9"}},
  {"number": 64, "question": "Solve: 5^x - 8*5^(-x) = -16", "type": "exp_equation", "meta": {"equation": "5**x-8*5**(-x)=-16"}},
  {"number": 65, "question": "Solve: 2*49^x + 11*7^x + 5 = 0", "type": "exp_equation", "meta": {"equation": "2*49**x+11*7**x+5=0"}},
  {"number": 66, "question": "Solve: 3*4^x + 4*2^x + 8 = 0", "type": "exp_equation", "meta": {"equation": "3*4**x+4*2**x+8=0"}},
  {"number": 67, "question": "Solve: 3^x - 14*3^(-x) = 5", "type": "exp_equation", "meta": {"equation": "3**x-14*3**(-x)=5"}},
  {"number": 68, "question": "Solve: 4^x - 10*4^(-x) = 3", "type": "exp_equation", "meta": {"equation": "4**x-10*4**(-x)=3"}},

  # Problems 105-107: modeling
  {
    "number": 105,
    "question": "Population model: P(t)=287(1.010)^(t-1999). Find when population reaches 307 million and 394 million.",
    "type": "exp_growth_decay_model",
    "meta": {
      "model": "287*(1.010)**(t-1999)",
      "variable": "t",
      "targets": [307, 394],
      "units": "million people",
      "context": "population"
    },
  },
  {
    "number": 106,
    "question": "Population model: P(t)=7.14(1.011)^(t-2014). Find when population reaches 9 and 12.5 billion.",
    "type": "exp_growth_decay_model",
    "meta": {
      "model": "7.14*(1.011)**(t-2014)",
      "variable": "t",
      "targets": [9, 12.5],
      "units": "billion people",
      "context": "population"
    },
  },
  {
    "number": 107,
    "question": "Depreciation model: V(t)=14162(0.832)^t. Find when value is $8000, $3000, and $1000.",
    "type": "exp_growth_decay_model",
    "meta": {
      "model": "14162*(0.832)**t",
      "variable": "t",
      "targets": [8000, 3000, 1000],
      "units": "dollars",
      "context": "depreciation"
    },
  },
]


SECTION_PROBLEMS: dict[str, list[dict]] = {
  "4.1": SECTION_4_1_PROBLEMS,
  "4.3": SECTION_4_3_PROBLEMS,
  "4.4": SECTION_4_4_PROBLEMS,
  "4.2": SECTION_4_5_PROBLEMS,
  "4.5": SECTION_4_5_PROBLEMS,
  "5.6": SECTION_5_6_PROBLEMS,
}


SECTION_LOOKUPS: dict[str, dict[int, dict]] = {
  sec: {p["number"]: p for p in probs}
  for sec, probs in SECTION_PROBLEMS.items()
}

# Backward compatibility for existing imports in 4.1 flow.
PROBLEM_LOOKUP: dict[int, dict] = SECTION_LOOKUPS["4.1"]


def get_problem_lookup(section: str = "4.1") -> dict[int, dict]:
  return SECTION_LOOKUPS.get(section, {})


def get_problems(problem_ranges: list[str], section: str = "4.1") -> list[dict]:
  from parser import expand_ranges

  lookup = get_problem_lookup(section)
  target = expand_ranges(problem_ranges)
  return [lookup[n] for n in sorted(target) if n in lookup]
