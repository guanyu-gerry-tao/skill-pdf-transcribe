# skill-pdf-transcribe

A starter repository for a reusable **lecture PDF → Markdown notes** transcription skill.

## What’s inside

- [SKILL.md](SKILL.md) — the skill definition (workflow + decision points + output formats)
- [examples/prompts.md](examples/prompts.md) — copy/paste prompt examples
- [references/quality-checklist.md](references/quality-checklist.md) — completion/quality checks
- [references/lecture-notes-format.md](references/lecture-notes-format.md) — the strict PAGE/Ekphrasis spec

This repo is intentionally minimal and focuses on **format + workflow**:
- Strict `# PAGE_N:` blocks with Ekphrasis-only content
- 10-pages-per-batch transcription
- A temp dir rendering step (`lr/` 72 DPI JPG + `hr/` 300 DPI JPG) with cleanup at the end