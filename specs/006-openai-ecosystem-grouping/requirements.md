Status: done
Last updated: 2026-10-19
Variant: refactor

# OpenAI ecosystem grouping

Group the existing ChatGPT and Codex directories under `openai/`. Mirror the grouping under `generated/` and in future model-specific builds and adapters. Keep `chatgpt` and `codex` as distinct target IDs, with their existing entrypoint formats and suitability maps.

Acceptance criteria:

- Existing source and support bytes survive relocation, apart from explicit documentation path updates.
- Generated counts remain 36 Claude, 36 ChatGPT, 12 Cursor and 12 Codex; no candidate is promoted or installed.
- The generator, ownership manifest, validation and catalog resolve nested paths without supporting obsolete root aliases.
- Nested output/adapter parents retain symlink, junction, collision and drift protections before writes.
- Release preparation includes the relocated shipped ChatGPT files and excludes Codex's existing example scaffold and generated candidates, preserving the release boundary.
- Catalog IDs, ecosystem decisions, behavioral fixtures and historical source pins remain stable. Catalog paths and live navigation follow the new layout.
- Local regressions and hosted checks pass. PR #11 remains draft and unmerged.
