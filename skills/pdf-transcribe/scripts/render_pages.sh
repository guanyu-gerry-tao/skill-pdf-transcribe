#!/usr/bin/env bash
# render_pages.sh — Render a PDF into lr/ (72 DPI) and hr/ (300 DPI) JPEG images.
#
# Usage:
#   ./render_pages.sh <pdf_path>
#
# Output:
#   <pdf_dir>/<pdf_base>__working.<random>/lr/page-*.jpg   (72 DPI)
#   <pdf_dir>/<pdf_base>__working.<random>/hr/page-*.jpg   (300 DPI)
#
# The working directory path is printed to stdout on success so callers can
# capture it:
#   tmpdir=$(./render_pages.sh Lecture.pdf)
#
# Requires: pdftoppm (Poppler)

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <pdf_path>" >&2
  exit 1
fi

pdf="$(realpath "$1")"

if [[ ! -f "$pdf" ]]; then
  echo "Error: file not found: $pdf" >&2
  exit 1
fi

if ! command -v pdftoppm &>/dev/null; then
  echo "Error: pdftoppm not found. Install Poppler:" >&2
  echo "  macOS:  brew install poppler" >&2
  echo "  Linux:  sudo apt install poppler-utils  (Debian/Ubuntu)" >&2
  echo "          sudo dnf install poppler-utils  (Fedora)" >&2
  exit 1
fi

pdf_dir="$(dirname "$pdf")"
pdf_base="$(basename "$pdf" .pdf)"

# Create the working folder next to the PDF with a unique name.
tmpdir="$(cd "$pdf_dir" && mktemp -d "${pdf_base}__working.XXXXXXXX")"
tmpdir="$(realpath "$tmpdir")"

mkdir -p "$tmpdir/lr" "$tmpdir/hr"

# Render 72 DPI → lr/
pdftoppm -jpeg -r 72  "$pdf" "$tmpdir/lr/page"

# Render 300 DPI → hr/
pdftoppm -jpeg -r 300 "$pdf" "$tmpdir/hr/page"

# Print the working directory path for the caller to capture.
echo "$tmpdir"
