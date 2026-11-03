# resume-writer: canonical candidate

Read `SKILL.md` for the portable workflow. This is a review candidate, not a shipped or behavior-evaluated replacement.

The [original README](https://github.com/mickpletcher/AI-Skills/blob/1deaab97ec585b6451a7ed80bc2a4398a8428ecc/claude/skills/resume-writer/README.md) retains the source installation instructions, prerequisites, examples, and author context. Original packages and maintenance history remain in the Claude tree. `migration.json` records exact source provenance, metadata, transformations, and dependency hashes. Existing personal preferences and domain examples are preserved, not newly verified.

Supporting files retain their original relative paths and bytes, including any skill-specific license. The repository MIT license applies where no separate notice says otherwise. Generated candidates include these resources; a host must actually support their required tools and file access. Do not execute helpers or install integrations merely by generating a candidate.

## Pagination verification (candidate-only)

Two-page claims require the intended final artifact, not a word-count proxy. The workflow distinguishes estimates from rendered evidence and reports missing tools/fonts without claiming a confirmed fit. The JSON audit retains its existing schema; pagination evidence goes in `notes`.

Optional helper prerequisites: Python 3 and Poppler `pdfinfo` + `pdftoppm` on PATH. Run `python scripts/verify_pagination.py final-resume.pdf` only on an authorized PDF. It snapshots the bytes, renders all pages at low resolution in a temporary directory, reports the SHA-256 and actual page count, and removes temporary images. It never alters the input. Exit 0 means the PDF rendered and counted; exit 2 means unverified (including missing tools, invalid inputs or warnings). This is not a DOCX converter or a font/layout/visual-quality checker. Use a document renderer with the intended fonts to export DOCX first; record that conversion and inspect final pages separately at readable resolution.

Synthetic regression checks cover one-, two- and three-page PDFs, unavailable renderer tools, invalid PDF and unsupported DOCX. Native model use and cross-platform DOCX rendering remain separate verification tasks.
