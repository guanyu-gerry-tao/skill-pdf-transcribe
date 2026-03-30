# Quality checklist

Use this checklist before considering the transcription "done".

- Every block starts with `# PAGE_N:` or `# PAGE_N-M:`
- Every block contains `## Title`, `## Content`, `## Note`, and ends with `---`
- `## Note` is present and intentionally left empty
- Page numbering is monotonic; merged ranges don't overlap or skip unexpectedly
- Random spot-check: at least 2–3 pages match the source page images visually
- Diagrams:
  - traceable → ASCII art + a single `[DESCRIPTION] ...` line
  - non-traceable → one or more `[IMAGE] ...` lines
- No commentary or interpretation is introduced (Ekphrasis only)
- Temp dir lifecycle: `lr/` and `hr/` were created for rendering and removed at the end
- Cleanup safety: deletion was performed only after path/pattern/sentinel checks passed
- Ambiguous pages were verified against the `hr/` (300 DPI) images
