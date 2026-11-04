# n8n security reviewer: candidate

`SKILL.md` is the editable, platform-neutral source. This is a new read-only review candidate, not a shipped skill, certified scanner, or replacement for `n8n-workflow`. No installation, publication, or live n8n access is part of creating it.

For a local preview, give your assistant `SKILL.md` and the linked reference files as context, then provide a synthetic workflow export. Generated candidates use `SKILL.md` for Claude/Codex and `instructions.md` for ChatGPT/Cursor. Keep the whole generated folder together so linked files resolve. Using a candidate in a host requires that host's supported instruction/file surface and authorization; generation does not install it.

Try: “Review this exported n8n workflow without running it. Separate findings from unknowns and redact any token values.” Start with a small synthetic workflow, then check that the response cites fields, does not contact endpoints, and does not declare the instance secure.

Optional helper: Python 3.10+, standard library only. Run `python scripts/review_export.py /local/workflow.json` from this folder. It reads existing local JSON and prints a value-free triage report; no files are changed. See [helper limits and config format](references/helper-contract.md). Human/contextual review is still required. No helper prerequisites need installation when Python is already available.

The schema-v2 report adds bounded, one-layer JSON header/body scanning and separate coverage unknowns. Inspect `coverage` and `embedded_review`, not just the candidate list: expressions are not evaluated, unsupported fields stay unreviewed, and truncated output is explicit. A successful exit or no candidates does not mean secure. Existing consumers should explicitly support schema version 2 before using the revised report.

The [source notes](references/version-and-sources.md) identify current official documentation and known version/default disagreements. Offline tests check helper behavior and safety invariants, not native host/model quality or a live n8n installation. New candidate acceptance is separate from any prior builder acceptance.
