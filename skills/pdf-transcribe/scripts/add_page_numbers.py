#!/usr/bin/env python3
"""
add_page_numbers.py — Stamp "N/Total" in the bottom-left corner of every page.

Usage:
    python3 add_page_numbers.py <pdf_path>

Behaviour:
    - Original PDF is renamed to <base>_unnumbered.pdf (backup).
    - Numbered PDF is saved under the original filename.

Requires: pymupdf
    pip3 install pymupdf
"""

import sys
import os


def check_pymupdf() -> None:
    try:
        import fitz  # noqa: F401
    except ImportError:
        print("Error: pymupdf is not installed.", file=sys.stderr)
        print("Install it with:", file=sys.stderr)
        print("  pip3 install pymupdf", file=sys.stderr)
        print("", file=sys.stderr)
        print("If pip3 is not found, install Python 3 first:", file=sys.stderr)
        print("  macOS:  brew install python", file=sys.stderr)
        print("  Linux:  sudo apt install python3-pip  (Debian/Ubuntu)", file=sys.stderr)
        print("          sudo dnf install python3-pip  (Fedora)", file=sys.stderr)
        sys.exit(1)


def stamp_page_numbers(pdf: str) -> None:
    import fitz

    if not os.path.isfile(pdf):
        print(f"Error: file not found: {pdf}", file=sys.stderr)
        sys.exit(1)

    base = os.path.splitext(pdf)[0]
    tmp = base + "__numbered_tmp.pdf"
    unnumbered = base + "_unnumbered.pdf"

    doc = fitz.open(pdf)
    total = len(doc)

    for i, page in enumerate(doc, start=1):
        label = f"{i}/{total}"
        r = page.rect
        # Bottom-left: 15 pt from left edge, 15 pt from bottom
        pt = fitz.Point(15, r.height - 15)
        page.insert_text(
            pt,
            label,
            fontsize=9,
            color=(0.4, 0.4, 0.4),
            align=fitz.TEXT_ALIGN_LEFT,
        )

    doc.save(tmp, garbage=4, deflate=True)
    doc.close()

    # Atomic swap: original → _unnumbered, numbered → original name
    os.rename(pdf, unnumbered)
    os.rename(tmp, pdf)

    print(f"Done.")
    print(f"  Numbered : {pdf}")
    print(f"  Backup   : {unnumbered}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pdf_path>", file=sys.stderr)
        sys.exit(1)

    check_pymupdf()
    stamp_page_numbers(sys.argv[1])
