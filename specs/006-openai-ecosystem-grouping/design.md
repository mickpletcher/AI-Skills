# Design

`openai/` is an organizational parent. The routing map in `tools/ecosystem_paths.py` maps stable target IDs to physical directories. Generation, catalog discovery and offline evaluation share it without adding dependencies to the standard-library evaluation runner. Catalog discovery still covers only already shipped platforms. Codex's existing scaffold remains outside shipped validation and release inventory.

The directory layout is `openai/{chatgpt,codex}/skills/` and `generated/openai/{chatgpt,codex}/skills/`. Existing non-OpenAI paths are unchanged. Generated ownership keys use physical paths while provenance and suitability retain logical target IDs. Manifest validation accepts only the current target directory prefixes.

Relocate existing generated files and rewrite only their ownership keys before regeneration. Verify every managed input against its recorded hash before moving. Regeneration updates generator provenance while preserving instructions and resource bytes. No compatibility links or duplicate trees remain.
