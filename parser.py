from __future__ import annotations
"""
parser.py
---------
PDF parsing module for the MAT116 problem extractor.

Responsibilities:
  - Open a PDF file using PyMuPDF (fitz)
  - Extract raw text page by page
  - Locate a target section (e.g., "4.1")
  - Detect and extract numbered exercise problems via regex
  - Clean up broken lines, hyphenation artefacts, and extra whitespace
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ── helper: expand problem-number ranges ──────────────────────────────────────

def expand_ranges(range_strings: list[str]) -> set[int]:
    """
    Convert a list of range strings such as ["37-42", "57-68"] into a
    flat set of integers: {37, 38, 39, 40, 41, 42, 57, …, 68}.
    Also accepts plain numbers like ["99"].
    """
    numbers: set[int] = set()
    for part in range_strings:
        part = part.strip()
        if "-" in part:
            lo, hi = part.split("-", 1)
            numbers.update(range(int(lo.strip()), int(hi.strip()) + 1))
        elif part.isdigit():
            numbers.add(int(part))
    return numbers


# ── main class ─────────────────────────────────────────────────────────────────

class PDFParser:
    """
    Parses a Sullivan Precalculus PDF for exercise problems.

    Usage:
        parser = PDFParser("Precalculus-Sullivan 10th edition.pdf")
        raw    = parser.extract_text()
        probs  = parser.extract_problems(
                     section="4.1",
                     problem_ranges=["37-42", "43-50", "51-56", "57-68", "81-90"])
    """

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self._full_text: Optional[str] = None  # cached full text

    # ── public API ─────────────────────────────────────────────────────────────

    def extract_text(self) -> str:
        """Return the full plain-text of the PDF (cached after first call)."""
        if self._full_text is not None:
            return self._full_text

        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF is not installed. Run: pip install PyMuPDF"
            )

        logger.info(f"Opening PDF: {self.pdf_path}")
        doc = fitz.open(self.pdf_path)

        pages: list[str] = []
        for page_num, page in enumerate(doc):
            text = page.get_text("text")  # plain-text extraction
            pages.append(text)
            logger.debug(f"  Page {page_num + 1}: extracted {len(text)} chars")

        doc.close()
        self._full_text = "\n".join(pages)
        logger.info(f"Total extracted characters: {len(self._full_text)}")
        return self._full_text

    def extract_problems(
        self,
        section: str,
        problem_ranges: list[str],
    ) -> list[dict]:
        """
        Locate *section* in the PDF text and return a list of problem dicts:
            [{"number": 37, "question": "..."}, ...]

        Only problems whose numbers fall within *problem_ranges* are returned.
        The list is sorted by problem number.
        """
        full_text = self.extract_text()
        target_nums = expand_ranges(problem_ranges)

        section_text = self._locate_section(full_text, section)
        if not section_text:
            logger.warning(
                f"Section {section} not found in PDF — returning empty list."
            )
            return []

        problems = self._parse_numbered_problems(section_text)

        # Filter to requested numbers
        filtered = [p for p in problems if p["number"] in target_nums]
        filtered.sort(key=lambda p: p["number"])
        logger.info(
            f"Extracted {len(filtered)} problems from section {section}."
        )
        return filtered

    # ── private helpers ────────────────────────────────────────────────────────

    def _locate_section(self, text: str, section: str) -> str:
        """
        Return the slice of *text* that covers the given *section*.
        Looks for headings like "4.1", "Section 4.1", "SECTION 4.1", etc.
        Stops at the next section heading of the same or higher level.
        """
        # Build a flexible pattern for the section header
        escaped = re.escape(section)
        # Match lines like "4.1  Polynomial Functions" or "Section 4.1"
        header_pat = re.compile(
            rf"(?m)^.*?(?:SECTION\s+|Section\s+)?{escaped}\b.*$"
        )

        match = header_pat.search(text)
        if not match:
            logger.debug(f"Primary header search missed; trying relaxed search for '{section}'.")
            # Fallback: just look for the bare section number
            match = re.search(rf"(?m)\b{escaped}\b", text)
            if not match:
                return ""

        start = match.start()

        # Try to find the NEXT section heading to know where to stop.
        # Sullivan sections are numbered like "4.2", "4.3", …
        parts = section.split(".")
        next_section_candidates: list[str] = []
        if len(parts) == 2:
            major, minor = int(parts[0]), int(parts[1])
            next_section_candidates = [
                f"{major}.{minor + 1}",  # same chapter, next section
                f"{major + 1}.1",        # next chapter
            ]

        end = len(text)
        for ns in next_section_candidates:
            ns_escaped = re.escape(ns)
            ns_match = re.search(
                rf"(?m)^.*?(?:SECTION\s+|Section\s+)?{ns_escaped}\b.*$",
                text[start + len(match.group()):],
            )
            if ns_match:
                end = start + len(match.group()) + ns_match.start()
                break

        section_text = text[start:end]
        logger.debug(
            f"Section {section} text snippet ({len(section_text)} chars): "
            f"{section_text[:200]!r}"
        )
        return section_text

    def _parse_numbered_problems(self, text: str) -> list[dict]:
        """
        Scan *text* for exercise problems of the form:
            37. f(x) = (x + 2)^4 − 3
            38. In Problems 38–40 …

        Returns a list of dicts: [{"number": int, "question": str}, …]

        Strategy:
          1. Collapse the text into a single "flow" (join broken lines that
             don't start with a new problem number).
          2. Use a regex that anchors on '<number>.' at a token boundary.
          3. Grab everything up to the next numbered problem.
        """
        # Step 1: lightweight clean-up — remove soft hyphens and page numbers
        text = self._clean_text(text)

        # Step 2: find all positions of "NN." where NN is a 1-3 digit number
        #         followed by a space or letter (avoids decimal numbers like 4.1)
        token_pat = re.compile(r"(?m)(?:^|\n)(\d{1,3})\.\s+(.+?)(?=(?:\n\d{1,3}\.\s)|\Z)", re.DOTALL)

        problems: list[dict] = []
        for m in token_pat.finditer(text):
            num = int(m.group(1))
            # Exclude very small or very large numbers (problem numbers are typically 1-200)
            if num < 1 or num > 250:
                continue
            raw_q = m.group(2).strip()
            question = self._clean_question(raw_q)
            if question:
                problems.append({"number": num, "question": question})

        return problems

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove artefacts common in PDF text extraction."""
        # Soft hyphen (U+00AD)
        text = text.replace("\u00ad", "")
        # Replace unicode minus with ASCII dash
        text = text.replace("\u2212", "-")
        # Replace curly quotes
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        # Collapse runs of blank lines → single blank line
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    @staticmethod
    def _clean_question(text: str) -> str:
        """Normalise whitespace inside a question string."""
        # Join lines that continue a sentence (no leading number)
        text = re.sub(r"\n(?!\d)", " ", text)
        # Collapse multiple spaces
        text = re.sub(r" {2,}", " ", text)
        return text.strip()
