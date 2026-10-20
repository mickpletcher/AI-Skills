# Canonical skills

Skills in this directory are platform-independent sources. Each skill uses a `SKILL.md` with YAML frontmatter containing `name` and `description`. Keep platform-specific instructions in `adapters/<target-directory>/<skill>/append.md`; OpenAI target directories are `openai/chatgpt` and `openai/codex`.

Generate outputs with `python tools/generate_master_skills.py`. Run `python tools/generate_master_skills.py --check` in CI to detect drift. Existing platform-owned skills remain untouched until explicitly migrated.

Supported initial targets: Claude (`SKILL.md`), ChatGPT (`instructions.md`), Cursor (`instructions.md`), and Codex (`SKILL.md`). Generated content does not imply automatic installation or runtime compatibility. Validate actual behavior in each target host.

Generation requires `python -m pip install -r requirements-dev.txt`. Canonical frontmatter is validated against the repository schema before any candidates are written. The generated marker sits after YAML frontmatter. Both generation and `--check` report obsolete managed candidates when a master is removed or renamed; review and remove those files manually. The generator does not delete stale files or overwrite unmanaged content.

## Migration inventory and provenance

The [candidate catalog](CATALOG.md) and [machine-readable inventory](catalog.json) contain 36 masters: all 35 Claude skill names plus the example scaffold. This batch adds 32 masters to the existing three real masters. The shipped catalog and packages are unchanged. All candidates remain unpromoted, with no completed behavioral acceptance evaluation. Creation-time catalog/build labels are not a current run log; see the [foundation pilot evidence](../evaluations/README.md#foundation-instruction-pilot) for partial, context-confounded model captures. The pilot does not update verified support or promotion state.

Each new master keeps the original workflow and supported frontmatter, with narrowly recorded changes to assistant-host wording and a capability fallback section. Product-specific examples such as an Anthropic API integration remain because they describe the task, not a required assistant host. Owner preferences are retained as source context, not verified current facts. Claude's named WebFetch option lives in its adapter; other targets use only the capabilities actually available.

`migration.json` records the source commit, original hash and frontmatter, exact wording substitutions, dependency hashes, and original-only files. Scripts, references, schemas, templates, examples, assets, and skill-specific license notices are copied byte-for-byte. Original README/install guidance, `.skill` packages, and maintenance history stay in the unchanged Claude tree and are linked through pinned source READMEs. New candidate READMEs do not claim those packages install the candidates.

## Complete generated bundles

OpenAI outputs are grouped under `generated/openai/chatgpt/skills/` and `generated/openai/codex/skills/`, mirroring the source layout. Named model builds use the same nested grouping below `generated-models/<profile>/`. Logical IDs remain `chatgpt` and `codex`; all existing suitability and promotion gates remain unchanged.

Generation includes the complete master directory except package archives and Python bytecode caches. ChatGPT/Cursor use `instructions.md` as their entry point and retain a canonical `SKILL.md` companion so internal reference links still resolve. Claude/Codex use the rendered `SKILL.md` entry point. Supporting resource bytes are not rewritten, and `.gitattributes` preserves those bytes on every checkout platform.

`generated/.resource-manifest.json` tracks hashes for every generated file, including instruction entry points, and refuses manual edits before replacement. Check mode reports missing/drifted files and obsolete tracked resources. Normal generation refuses to overwrite edited or unmanaged resources, validates the whole plan first, and never deletes anything. For an intentional resource removal/rename, review and remove its obsolete generated copies **and their manifest entries** in the same change before regenerating. Resolve local edits manually before regeneration. Symlinked bundles are rejected.

Helper prerequisites remain those of the source: see [repository dependencies](../docs/dependencies.md) and the pinned original README in each candidate. Copying a helper does not execute it, install dependencies, grant filesystem/app access, or schedule anything. Keep runtime outputs and personal data outside these tracked candidate bundles.

Generation preflights the master, adapter, profile, schema and selected output trees before reading linked content or writing candidates. Symlinks and Windows junctions in parent directories or bundle members are rejected. Planned files and directories must have distinct names even on case-insensitive filesystems. Existing file/directory type conflicts fail before any candidate is written. These checks do not make filesystem writes transactional against concurrent edits or disk failures.

## Review gates

Run `python tools/generate_master_skills.py --check`, `python tools/skill_repository.py validate`, and `python -m unittest discover -s tools/tests -v`. Migration regressions cover inventory equality, metadata/provenance, exact source and resource preservation, navigable local links, and generated-resource collision/drift/removal behavior. These are structural checks; the existing synthetic fixture self-test does not certify all 35 migrated skills. Before promotion, review actual behavior with synthetic inputs on each intended host/model and verify helper prerequisites independently.

## Ecosystem and model separation

Every master includes a host-neutral `capabilities.json` contract and retains task goals, domain workflows, output criteria and safeguards. Ecosystem names/tool mappings live in adapters; per-model declarations and guidance live in [model profiles](../model-profiles/README.md). The committed baseline has no configured model and no verified capabilities. Every generated bundle includes `build-provenance.json`; deterministic regeneration proves input consistency, not portability or model quality. See the [generic-master audit](GENERIC-AUDIT.md) for retained domain specifics and unresolved adaptations.

Generation has no blanket target default: every master must classify every ecosystem in `ecosystems.json` with an allowed or skipped reason. `generated/target-decisions.json` exposes all decisions. Food Analyzer explicitly excludes Cursor; model profiles never widen these allowlists. Current proposed coverage is 36 Claude, 36 ChatGPT, 12 Cursor and 12 Codex candidates, including the example. Manually review ambiguous mode-specific placements in GENERIC-AUDIT.md before promotion.
