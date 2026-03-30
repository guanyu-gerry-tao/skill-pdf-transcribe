# Changelog

## [Unreleased] — 2026-03-30

### Added

#### pdf-transcribe skill

- **Page numbering**: new workflow to stamp `N/Total` (e.g. `3/24`) in the bottom-left corner of every PDF page.
  - Subtle style: 9 pt, dark gray — readable but unobtrusive.
  - File naming: the original PDF is renamed to `_unnumbered.pdf` as a backup; the numbered output takes over the original filename so existing references stay valid.
  - Primary implementation uses PyMuPDF (vector overlay, lossless); ImageMagick provided as fallback.

- **Dependency detection and install guidance**: checks for `pymupdf` before running; automatically attempts `pip3 install pymupdf` if missing; falls back to platform-specific install instructions (macOS / Debian / Fedora) if `pip3` is not found.

- **Workflow summary**: new section at the end of SKILL.md with:
  - A strong recommendation to enter **Plan Mode** before starting, to avoid hard-to-reverse mistakes in multi-step operations.
  - Ordered checklists for Task A (transcription) and Task B (page numbering).
  - Combined execution order: run transcription first, then page numbering — the two tasks are independent and safe to chain.
