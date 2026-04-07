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

PROBLEM_LOOKUP: dict[int, dict] = {p["number"]: p for p in SECTION_4_1_PROBLEMS}


def get_problems(problem_ranges: list[str]) -> list[dict]:
    from parser import expand_ranges
    target = expand_ranges(problem_ranges)
    return [PROBLEM_LOOKUP[n] for n in sorted(target) if n in PROBLEM_LOOKUP]
