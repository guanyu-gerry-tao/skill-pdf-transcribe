# Output format (spec)

This skill outputs a strict, per-page Markdown structure suitable for transcribing any PDF (slide decks are a common case).

## File naming + location

- Output is saved as a Markdown file next to the PDF.
- The output `.md` file name matches the PDF base name (only the extension changes).

Example:
- `/path/to/Document.pdf` → `/path/to/Document.md`

## Temporary rendering directory

For each transcription run:

1. Create a temp dir **in the same folder as the PDF** (sibling to the PDF).
2. Inside it, create:
   - `lr/` (72 DPI, `.jpg`)
   - `hr/` (300 DPI, `.jpg`)
3. Render all PDF pages into both folders.
4. After transcription completes, delete the temp dir.

### Safe deletion guardrails (required)

Never delete anything unless all checks pass:

- The working folder path is non-empty and is a directory
- The working folder is under the PDF directory
- The working folder name matches an expected distinctive pattern (recommended: `__working.<random>`)
- Both `lr/` and `hr/` sentinel subfolders exist inside it

If any check fails: refuse to delete and stop.

## Per-page block structure

Each page (or merged range) is a block:

```md
# PAGE_N:
## Title
<original title or No_Title>
## Content
<Ekphrasis>
## Note

---
```

If a continuing sequence spans multiple pages (common in slide exports), merge them:

```md
# PAGE_4-6:
```

## Ekphrasis rules

### Text

- Transcribe all visible text as-is.
- Do not add commentary or explanations.
- Code uses fenced Markdown code blocks (add a language tag when possible).

### Images / diagrams

- **Traceable diagrams** (memory layouts, arrows, simple relationship diagrams, tables):
  1) produce ASCII art first
  2) immediately follow with one `[DESCRIPTION] ...` line describing the visual appearance (layout, arrows, colors, positioning)

- **Non-traceable images** (photos/screenshots/complex visuals):
  - use one or more `[IMAGE] ...` lines describing:
    - position on page
    - content and meaning
    - visual appearance (shapes/arrows/colors/layout)

## Batch processing rule

To control context size, use a repeating 10-page batch:

1. Read the current batch low-res images from the temp dir `lr/` folder (10 pages).
2. Write/append those 10 pages into the notes file.
3. Repeat.

### Cross-batch continuation

If a continuing sequence spans batches:
- after reading the next batch, go back and widen the earlier header (`# PAGE_N:` → `# PAGE_N-M:`)
- append the new content to the merged block’s `## Content`
