# skill-pdf-transcribe

A reusable skill specification for transcribing PDFs into strict, per-page Markdown notes.

Slide decks (lecture materials) are a common use case, but this workflow is designed to work for any PDF.

This repo is intentionally minimal: it defines the workflow, output contract, and safety rules.

## Install

```sh
npx skills add guanyu-gerry-tao/skill-pdf-transcribe
```

## Usage

- In chat, invoke the skill by name: `/pdf-transcribe`
- Provide the PDF path and any page range constraints
- See the workflow in [skills/pdf-transcribe/SKILL.md](skills/pdf-transcribe/SKILL.md)
- Copy/paste ready-to-use prompts from [skills/pdf-transcribe/examples/prompts.md](skills/pdf-transcribe/examples/prompts.md)
- Review output with:
  - [skills/pdf-transcribe/references/format-spec.md](skills/pdf-transcribe/references/format-spec.md)
  - [skills/pdf-transcribe/references/quality-checklist.md](skills/pdf-transcribe/references/quality-checklist.md)

## What it does

- Renders the PDF into page images in a working folder next to the PDF:
	- `lr/` → 72 DPI JPGs (default for batch transcription)
	- `hr/` → 300 DPI JPGs (consult only when needed for accuracy)
- Transcribes in 10-page batches using Ekphrasis (no commentary)
- Writes output to a Markdown file with the same base name as the PDF, in the same folder
- Deletes the working folder at the end, with strict safety checks to avoid accidental deletion

## Output format (contract)

Each page (or merged page range) is emitted as a block:

```md
# PAGE_N:
## Title
<original slide title or No_Title>
## Content
<Ekphrasis>
## Note

---
```

Diagrams:
- Traceable → ASCII art + a single `[DESCRIPTION] ...` line
- Non-traceable → one or more `[IMAGE] ...` lines

## What’s inside

- [skills/pdf-transcribe/SKILL.md](skills/pdf-transcribe/SKILL.md) — the skill definition (workflow + decision points + output formats)
- [skills/pdf-transcribe/examples/prompts.md](skills/pdf-transcribe/examples/prompts.md) — copy/paste prompt examples
- [skills/pdf-transcribe/references/quality-checklist.md](skills/pdf-transcribe/references/quality-checklist.md) — completion/quality checks
- [skills/pdf-transcribe/references/format-spec.md](skills/pdf-transcribe/references/format-spec.md) — the strict PAGE/Ekphrasis spec