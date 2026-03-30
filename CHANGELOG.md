# Changelog

## [Unreleased] — 2026-03-30

### Added

#### pdf-transcribe skill

- **页码标注功能**：新增给 PDF 右下角加页码的工作流（格式 `N/Total`，如 `3/24`）。
  - 样式低调：9pt、深灰色，不遮挡正文内容。
  - 文件命名策略：原始文件重命名为 `_unnumbered.pdf` 备份，加完页码的新文件接管原始文件名，保持引用稳定。
  - 主方案使用 PyMuPDF（矢量叠加，不损失画质）；备选 ImageMagick。

- **依赖自动检测与安装引导**：执行前检查 `pymupdf` 是否可用，缺失时自动尝试 `pip3 install pymupdf`；若连 `pip3` 都不存在，输出分平台安装指引（macOS / Debian / Fedora）。

- **完整工作流总结**：在 SKILL.md 末尾新增流程总览章节，包含：
  - 强烈建议先进入 **Plan Mode**，避免多步操作出错。
  - Task A（转录）和 Task B（加页码）各自的有序检查清单。
  - 合并执行顺序说明：先转录，再加页码，两步互不干扰。
