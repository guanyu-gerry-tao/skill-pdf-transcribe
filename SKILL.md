---
name: skill-pdf-transcribe
description: "Transcribe lecture PDFs (often slide decks) into strict per-page Markdown notes using Ekphrasis, with a 10-pages-per-batch workflow and support for merging PAGE ranges when animations span multiple pages. Use when: lecture notes, transcribe slides, ekphrasis, PAGE_N format."
argument-hint: PDF path + optional page range + batching preference
---

# PDF Transcribe (Lecture Notes)

Turn lecture PDFs (often slide decks) into **strict, per-page Markdown notes** using the required Lecture Notes format and Ekphrasis rules.

## When to use

Use this skill when the user wants:
- lecture notes for a PDF / slide deck
- strict `# PAGE_N:` / `# PAGE_N-M:` blocks
- Ekphrasis transcription (no commentary)
- a batching workflow (read 10 pages, write 10 pages) to control context size

## End-to-end workflow (required)

When the user asks to transcribe a PDF:

1. Create a temporary working directory (temp dir) **in the same folder as the PDF** (i.e., sibling to the PDF).
2. Inside it, create two subfolders: `lr/` and `hr/`.
3. Render PDF pages into both folders:
  - `lr/`: 72 DPI, JPEG (`.jpg`)
  - `hr/`: 300 DPI, JPEG (`.jpg`)
4. Perform transcription using the **low-resolution** images by default (batching 10 pages at a time).
  - If a page is ambiguous, consult the corresponding `hr/` page image for accuracy.
5. Write the transcription output to a Markdown file that:
  - has the **same base name** as the PDF
  - lives in the **same directory** as the PDF
  - example: `/path/to/Lecture 01.pdf` → `/path/to/Lecture 01.md`
6. After finishing, delete the temp dir.

## Safety: deleting the working folder

Deletion MUST be defensive. Never delete anything unless all checks pass.

Required guardrails:

- The working folder must be created **next to the PDF** and must be uniquely named per run.
- The working folder name should include a distinctive suffix (recommended: `__working.<random>`).
- Before deleting, verify:
  - the path is non-empty and is a directory
  - the directory is under the PDF’s directory
  - the directory name matches the expected `__working.*` pattern
  - it contains both `lr/` and `hr/` subdirectories (sentinel check)
- If any check fails: do not delete; stop and surface an error.

### Suggested rendering commands (optional)

Any equivalent rendering is acceptable as long as it produces `.jpg` at the required DPI.

Example using `pdftoppm` (Poppler):

```sh
set -euo pipefail

pdf="/path/to/file.pdf"
pdf_dir="$(dirname "$pdf")"
pdf_base="$(basename "$pdf" .pdf)"

# Create the working folder NEXT TO the PDF, with a unique name.
(
  cd "$pdf_dir"
  tmpdir="$(mktemp -d "${pdf_base}__working.XXXXXXXX")"
  export tmpdir
)

mkdir -p "$tmpdir/lr" "$tmpdir/hr"

# 72 DPI JPGs
pdftoppm -jpeg -r 72 "$pdf" "$tmpdir/lr/page"

# 300 DPI JPGs
pdftoppm -jpeg -r 300 "$pdf" "$tmpdir/hr/page"

# ...transcribe...

# Defensive cleanup: refuse to delete unless all checks pass.
case "$tmpdir" in
  "$pdf_dir"/*__working.*) ;;
  *) echo "Refusing to delete unexpected path: $tmpdir" >&2; exit 1 ;;
esac

if [ ! -d "$tmpdir" ] || [ ! -d "$tmpdir/lr" ] || [ ! -d "$tmpdir/hr" ]; then
  echo "Refusing to delete: missing sentinel subfolders in $tmpdir" >&2
  exit 1
fi

rm -rf -- "$tmpdir"
```

## Required output format

Each page (or merged page range) MUST be emitted as:

```md
# PAGE_N:
## Title
<original slide title or No_Title>
## Content
<Ekphrasis>
## Note

---
```

If multiple pages describe the same continuing sequence (e.g., PPT animations), merge into a single block header like:

```md
# PAGE_4-6:
```

## Output file conventions

- Output is a single Markdown file in the same folder as the PDF.
- File name is the PDF’s base name with extension changed to `.md`.

## Ekphrasis rules (non-negotiable)

### Text content
- Transcribe **all visible text as-is**.
- Do **not** add explanations, summaries, or commentary.
- Code must be in fenced Markdown blocks with a language tag when known.

### Diagrams / images

**If the diagram is traceable** (memory layout, arrow relationships, tables, simple diagrams):
1. First, produce an ASCII art tracing.
2. Immediately after the ASCII block, add one line starting with `[DESCRIPTION]` describing the visual appearance (position, arrows, colors, layout).

**If the diagram is not traceable** (screenshots, photos, abstract images, complex visuals):
- Use `[IMAGE]` lines with a detailed visual description, including:
  - where it appears on the slide (top-left / center / bottom-right, etc.)
  - what it depicts and means
  - visual appearance (shapes, arrows, colors, layout)
  - if multiple images, use multiple `[IMAGE]` lines

## Batch workflow (10 pages at a time)

To avoid oversized context, work in batches:

1. Read low-resolution page images for the current batch from the temp dir (10 pages per batch).
  - Recommended naming: `lr/page-1.jpg`, `lr/page-2.jpg`, ... (whatever the renderer produced)
2. Write/append the corresponding pages into the target Markdown notes file.
3. Repeat until all pages are processed.

### Cross-batch animation continuation

If you detect the same animated sequence continues past the end of a batch:
- In the next batch, after reading the continuation pages, go back and **expand** the earlier header `# PAGE_N:` to `# PAGE_N-M:`
- Append the newly discovered content into that merged block’s `## Content`

## Quality checks

- Every page (or merged range) ends with `---`
- `## Note` is present and left empty
- No missing visible text (spot-check a couple of pages)
- Diagrams follow the ASCII + `[DESCRIPTION]` or `[IMAGE]` rules

## Assets

- [examples/prompts.md](examples/prompts.md)
- [references/lecture-notes-format.md](./references/lecture-notes-format.md)
- [references/quality-checklist.md](./references/quality-checklist.md)
