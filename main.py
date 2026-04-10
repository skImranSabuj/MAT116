#!/usr/bin/env python3
from __future__ import annotations
"""
main.py
-------
Entry point for the MAT116 problem-solution generator.

Usage
-----
  # Use the bundled PDF and default problem ranges
  python main.py

  # Specify custom ranges
  python main.py --section 4.1 --problems "37-42,43-50"

  # Point to a different PDF
  python main.py --pdf /path/to/textbook.pdf --section 4.1 --problems "57-68"

  # Skip PDF parsing entirely (use sample data)
  python main.py --no-pdf
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# ── Logging setup ──────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── defaults ───────────────────────────────────────────────────────────────────

WORKSPACE   = Path(__file__).parent
DEFAULT_PDF = WORKSPACE / "Precalculus-Sullivan 10th edition.pdf"
DEFAULT_OUT = WORKSPACE / "4.1"

DEFAULT_SECTION  = "4.1"
DEFAULT_PROBLEMS = "37-42,43-50,51-56,57-68,81-90"

PART1_RANGES = ["37-42", "43-50"]          # transformation + simple graphing
PART2_RANGES = ["51-56"]                   # form polynomial
PART3_RANGES = ["57-68"]                   # analysis
PART4_RANGES = ["81-90"]                   # applications


# ── helpers ────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate step-by-step Precalculus solutions from a Sullivan PDF.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--pdf",
        default=str(DEFAULT_PDF),
        help="Path to the PDF textbook. Default: %(default)s",
    )
    parser.add_argument(
        "--section",
        default=DEFAULT_SECTION,
        help="Section to process, e.g. '4.1'. Default: %(default)s",
    )
    parser.add_argument(
        "--problems",
        default=DEFAULT_PROBLEMS,
        help=(
            "Comma-separated list of problem ranges, e.g. '37-42,57-68'.\n"
            "Default: %(default)s"
        ),
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF parsing and use built-in sample data only.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUT),
        help="Directory for output files. Default: %(default)s",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )
    return parser.parse_args()


def split_ranges(raw: str) -> list[str]:
    """Convert '37-42,43-50' → ['37-42', '43-50']."""
    return [r.strip() for r in raw.split(",") if r.strip()]


def load_problems(
    pdf_path: str,
    section: str,
    ranges: list[str],
    no_pdf: bool,
) -> list[dict]:
    """
    Try to extract problems from the PDF.
    Falls back to sample_data if the PDF cannot be read or the
    extracted list is empty.
    """
    problems: list[dict] = []

    if not no_pdf and os.path.isfile(pdf_path):
        try:
            from parser import PDFParser
            logger.info(f"Parsing PDF: {pdf_path}")
            pdf_parser = PDFParser(pdf_path)
            problems   = pdf_parser.extract_problems(section, ranges)
            logger.info(f"  → {len(problems)} problems extracted from PDF.")
        except Exception as exc:
            logger.warning(f"PDF parsing failed ({exc}). Falling back to sample data.")

    if not problems:
        logger.info("Using built-in sample data for section %s.", section)
        from sample_data import get_problems
        problems = get_problems(ranges, section=section)
        logger.info(f"  → {len(problems)} sample problems loaded.")

    return problems


def merge_with_sample(
    pdf_problems: list[dict],
    ranges: list[str],
    section: str,
) -> list[dict]:
    """
    For any problem number in *ranges* that is MISSING from *pdf_problems*,
    look it up in sample_data and fill in the gap.
    """
    from parser import expand_ranges
    from sample_data import get_problem_lookup

    target_nums = expand_ranges(ranges)
    found_nums  = {p["number"] for p in pdf_problems}
    missing     = target_nums - found_nums
    lookup      = get_problem_lookup(section)

    if missing:
        logger.info(
            "Filling %d missing problem(s) from sample data: %s",
            len(missing),
            sorted(missing),
        )
        extra = [lookup[n] for n in sorted(missing) if n in lookup]
        pdf_problems = sorted(pdf_problems + extra, key=lambda p: p["number"])

    return pdf_problems


def generate_solutions(problems: list[dict]) -> list[dict]:
    from solver import Solver
    solver    = Solver()
    solutions = []
    for prob in problems:
        logger.info(f"  Solving problem {prob['number']} …")
        sol = solver.solve(prob)
        solutions.append(sol)
    return solutions


def write_outputs(
    solutions: list[dict],
    output_dir: str,
    section: str,
) -> None:
    from formatter import Formatter

    fmt = Formatter(output_dir=output_dir)

    # ── split into groups ─────────────────────────────────────────────────────
    def by_range(sols: list[dict], lo: int, hi: int) -> list[dict]:
        return [s for s in sols if lo <= s["number"] <= hi]

    def by_type(sols: list[dict], ptype: str) -> list[dict]:
        return [s for s in sols if s.get("type") == ptype]

    written: list[str] = []

    if section == "4.1":
        part1 = by_range(solutions, 37, 50)   # transformations
        part2 = by_range(solutions, 51, 56)   # form polynomial
        part3 = by_range(solutions, 57, 68)   # analysis
        part4 = by_range(solutions, 69, 999)  # applications & rest

        if part1:
            p = fmt.write_markdown(
                part1,
                filename=f"section_{section.replace('.','_')}_transformations.md",
                title=f"Section {section} – Graphing with Transformations (Problems 37–50)",
                section=section,
            )
            written.append(p)

        if part2:
            p = fmt.write_markdown(
                part2,
                filename=f"section_{section.replace('.','_')}_form_polynomial.md",
                title=f"Section {section} – Form a Polynomial (Problems 51–56)",
                section=section,
            )
            written.append(p)

        if part3:
            p = fmt.write_markdown(
                part3,
                filename=f"section_{section.replace('.','_')}_analysis.md",
                title=f"Section {section} – Polynomial Analysis (Problems 57–68)",
                section=section,
            )
            written.append(p)

        if part4:
            p = fmt.write_markdown(
                part4,
                filename=f"section_{section.replace('.','_')}_applications.md",
                title=f"Section {section} – Application Problems (Problems 81–90)",
                section=section,
            )
            written.append(p)
    elif section in ("4.2", "4.5"):
        part_asym = by_type(solutions, "rational_asymptotes")
        part_app  = by_type(solutions, "rational_application")

        if part_asym:
            p = fmt.write_markdown(
                part_asym,
                filename=f"section_{section.replace('.','_')}_rational_asymptotes.md",
                title=f"Section {section} – Rational Asymptotes (Problems 47–56)",
                section=section,
            )
            written.append(p)

        if part_app:
            p = fmt.write_markdown(
                part_app,
                filename=f"section_{section.replace('.','_')}_applications.md",
                title=f"Section {section} – Application Problem (Problem 58)",
                section=section,
            )
            written.append(p)

    # ── full combined HTML ────────────────────────────────────────────────────
    html_path = fmt.write_html(
        solutions,
        filename=f"section_{section.replace('.','_')}.html",
        section=section,
        title=f"Section {section} – Complete Solutions",
    )
    written.append(html_path)

    # ── also write a single combined Markdown ─────────────────────────────────
    combined_md = fmt.write_markdown(
        solutions,
        filename=f"section_{section.replace('.','_')}_all.md",
        title=f"Section {section} – All Solutions",
        section=section,
    )
    written.append(combined_md)

    print("\n✔ Output files written:")
    for path in written:
        print(f"   {path}")


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    section = args.section
    ranges  = split_ranges(args.problems)

    logger.info("=" * 60)
    logger.info("MAT116 Solution Generator")
    logger.info(f"  Section  : {section}")
    logger.info(f"  Ranges   : {ranges}")
    logger.info(f"  PDF      : {args.pdf if not args.no_pdf else '(skipped)'}")
    logger.info(f"  Output   : {args.output_dir}")
    logger.info("=" * 60)

    # 1) Load problems (PDF → sample fallback)
    problems = load_problems(args.pdf, section, ranges, args.no_pdf)

    # 2) Fill any missing problems from sample data
    problems = merge_with_sample(problems, ranges, section)

    if not problems:
        logger.error("No problems found. Exiting.")
        return 1

    logger.info(f"Processing {len(problems)} problems …")

    # 3) Generate solutions
    solutions = generate_solutions(problems)

    # 4) Write output files
    write_outputs(solutions, args.output_dir, section)

    logger.info("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
