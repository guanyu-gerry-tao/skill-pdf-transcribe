# Example prompts

These prompts target the strict per-page format (`# PAGE_N:` blocks + Ekphrasis + empty `## Note`).

## Single batch (10 pages)

- "Transcribe `/path/to/Document.pdf` into `/path/to/Document.md`.
  Create a temp dir (working folder) next to the PDF with `lr/` (72 DPI JPG) and `hr/` (300 DPI JPG), render all pages into both, then process 10 pages at a time from `lr/`.
  If anything is unclear in `lr/`, consult the matching `hr/` page.
  Output MUST follow the per-page block format:
  `# PAGE_N:` + `## Title` + `## Content` (Ekphrasis) + `## Note` (empty) + `---`.
  Delete the temp dir after finishing."

## Continue next batch

- "Continue with the next 10 pages from the temp dir `lr/` folder and append in the same format. Keep numbering consistent."

## Sequence spans multiple pages

- "If pages 4–6 are the same continuing sequence, merge them into a single block header `# PAGE_4-6:` and combine their Content in order."

## Diagrams rules

- "For diagrams that can be traced, output ASCII art first, then a single `[DESCRIPTION] ...` line describing layout/arrows/colors/position.
  For screenshots/photos, use `[IMAGE] ...` lines with position + meaning + visual appearance."

## Mixed language

- "Keep the document's original language exactly; do not translate. Transcribe all visible text as-is."
