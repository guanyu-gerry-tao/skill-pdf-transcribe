---
name: pdf-transcribe
description: "Transcribe PDFs into strict, per-page Markdown notes using Ekphrasis, with a 10-pages-per-batch workflow and support for merging PAGE ranges when sequences span multiple pages. Slide decks are a common use case. Use when: transcribe PDF, PDF to Markdown, ekphrasis, PAGE_N format."
argument-hint: PDF path + optional page range + batching preference
---

# PDF Transcribe

Turn PDFs into **strict, per-page Markdown notes** using the required format and Ekphrasis rules.

## When to use

Use this skill when the user wants:
- page-by-page transcription for a PDF (slide decks are a common case)
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
  - example: `/path/to/Document.pdf` → `/path/to/Document.md`
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

If multiple pages describe the same continuing sequence (common in slide exports), merge into a single block header like:

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
  - where it appears on the page (top-left / center / bottom-right, etc.)
  - what it depicts and means
  - visual appearance (shapes, arrows, colors, layout)
  - if multiple images, use multiple `[IMAGE]` lines

## Batch workflow (10 pages at a time)

To avoid oversized context, work in batches:

1. Read low-resolution page images for the current batch from the temp dir (10 pages per batch).
  - Recommended naming: `lr/page-1.jpg`, `lr/page-2.jpg`, ... (whatever the renderer produced)
2. Write/append the corresponding pages into the target Markdown notes file.
3. Repeat until all pages are processed.

### Cross-batch continuation

If you detect the same continuing sequence spans batches:
- In the next batch, after reading the continuation pages, go back and **expand** the earlier header `# PAGE_N:` to `# PAGE_N-M:`
- Append the newly discovered content into that merged block’s `## Content`

## Quality checks

- Every page (or merged range) ends with `---`
- `## Note` is present and left empty
- No missing visible text (spot-check a couple of pages)
- Diagrams follow the ASCII + `[DESCRIPTION]` or `[IMAGE]` rules

## Page numbering (optional feature)

When the user asks to **add page numbers** to a PDF (e.g. "给 PDF 加页码", "stamp page numbers"), stamp `N/Total` in the bottom-right corner and **replace** the original filename with the numbered version.

### Output convention

- Rename the original: `Lecture.pdf` → `Lecture_unnumbered.pdf`
- Save the numbered PDF as: `Lecture.pdf` (the original name)
- This way the file the user references by name always has page numbers.

### Dependency check and installation

Before running, verify `pymupdf` is available. If not, install it (or guide the user):

```sh
# Check
python3 -c "import fitz" 2>/dev/null && echo "pymupdf OK" || echo "pymupdf MISSING"
```

If missing, **attempt to install automatically**:

```sh
pip3 install pymupdf
```

If `pip3` itself is unavailable, inform the user and suggest:

```
pip3 not found. Please install Python 3 first:
  macOS:  brew install python   (then retry)
  Linux:  sudo apt install python3-pip  (Debian/Ubuntu)
          sudo dnf install python3-pip  (Fedora)
```

After installing, re-run the check before proceeding.

### Style

- Format: `N/Total` (e.g. `3/24`)
- Position: bottom-left corner, ~15 pt from the left edge, ~15 pt from the bottom
- Font size: 9 pt
- Color: dark gray `(0.4, 0.4, 0.4)` — visible but not distracting
- No background box, no border

### Implementation (PyMuPDF)

Write the snippet below to a temp file and execute it:

```python
import sys, os, fitz  # pip install pymupdf

pdf   = sys.argv[1]                          # e.g. /path/to/Lecture.pdf
base  = os.path.splitext(pdf)[0]
tmp   = base + "__numbered_tmp.pdf"
unnumbered = base + "_unnumbered.pdf"

doc   = fitz.open(pdf)
total = len(doc)

for i, page in enumerate(doc, start=1):
    label = f"{i}/{total}"
    r     = page.rect
    pt    = fitz.Point(15, r.height - 15)
    page.insert_text(
        pt,
        label,
        fontsize = 9,
        color    = (0.4, 0.4, 0.4),
        align    = fitz.TEXT_ALIGN_LEFT,
    )

doc.save(tmp, garbage=4, deflate=True)
doc.close()

# Atomic rename: original → _unnumbered, numbered → original name
os.rename(pdf, unnumbered)
os.rename(tmp, pdf)
print(f"Done: {pdf} (numbered), {unnumbered} (original backup)")
```

Run as:

```sh
python3 /tmp/add_page_numbers.py "/path/to/Lecture.pdf"
```

Result:
- `/path/to/Lecture.pdf` — numbered (replaces original)
- `/path/to/Lecture_unnumbered.pdf` — original backup

### Fallback: ImageMagick (if PyMuPDF unavailable after install attempt)

```sh
pdf="/path/to/Lecture.pdf"
base="${pdf%.pdf}"
tmp="${base}__numbered_tmp.pdf"
unnumbered="${base}_unnumbered.pdf"

total=$(python3 -c "import fitz; print(len(fitz.open('$pdf')))" 2>/dev/null \
        || identify -format "%n\n" "$pdf" | head -1)

convert \
  -density 150 "$pdf" \
  -gravity SouthWest \
  -pointsize 11 \
  -fill "gray50" \
  -annotate +15+12 "%[fx:page+1]/${total}" \
  "$tmp"

mv "$pdf" "$unnumbered"
mv "$tmp" "$pdf"
```

> Note: ImageMagick re-rasterises the PDF; prefer PyMuPDF for vector-clean output.

### Checklist before finishing

- [ ] `pymupdf` was confirmed installed (or user was guided to install it)
- [ ] Original PDF renamed to `_unnumbered.pdf`
- [ ] Numbered PDF saved under the original filename
- [ ] Every page carries the correct `N/Total` label in the bottom-right corner
- [ ] No temp files left behind

## Complete workflow summary

> **Strongly recommended: enter Plan Mode before starting any task.**
> Both transcription and page numbering involve file renames, temp directories, and multi-step shell commands. Planning first surfaces ambiguities and prevents hard-to-reverse mistakes (e.g. overwriting the original PDF, leaving temp dirs behind, writing to the wrong output path).

### How to use Plan Mode

Before executing any step, use the `EnterPlanMode` tool (or `/plan`) to draft and review the full sequence of actions. Only proceed once the plan is confirmed.

---

### Task A — Transcribe PDF to Markdown

```
1. [ ] Confirm PDF path and target .md output path
2. [ ] Create temp dir next to PDF: <base>__working.<random>/lr/ and hr/
3. [ ] Render pages: 72 DPI → lr/, 300 DPI → hr/
4. [ ] Transcribe in batches of 10 pages → write/append to .md file
5. [ ] Verify quality checklist (every PAGE_N block, ## Note, ---)
6. [ ] Defensive cleanup: verify tmpdir pattern + sentinel dirs, then rm -rf
```

### Task B — Add page numbers to PDF

```
1. [ ] Confirm PDF path
2. [ ] Check pymupdf: python3 -c "import fitz"
       → if missing: pip3 install pymupdf (or guide user to install Python)
3. [ ] Write stamp script to /tmp/add_page_numbers.py
4. [ ] Dry-run: confirm page count and label format looks correct
5. [ ] Execute script → produces <base>__numbered_tmp.pdf
6. [ ] Rename original → <base>_unnumbered.pdf
7. [ ] Rename tmp → <base>.pdf (original name)
8. [ ] Verify: open numbered PDF, spot-check first/last page labels
9. [ ] Confirm no temp files remain
```

### Combined (transcribe + number in one session)

Run Task A first (transcription does not touch the PDF file itself), then Task B. The `_unnumbered.pdf` backup remains available if the user needs the original.

---

## Assets

- [examples/prompts.md](examples/prompts.md)
- [references/format-spec.md](references/format-spec.md)
- [references/quality-checklist.md](references/quality-checklist.md)
