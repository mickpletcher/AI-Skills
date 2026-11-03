# Canonical skills

Skills in this directory are platform-independent sources. Each skill uses a `SKILL.md` with YAML frontmatter containing `name` and `description`. Keep platform-specific instructions in `adapters/<target-directory>/<skill>/append.md`; OpenAI target directories are `openai/chatgpt` and `openai/codex`.

Generate outputs with `python tools/generate_master_skills.py`. Run `python tools/generate_master_skills.py --check` in CI to detect drift. Existing platform-owned skills remain untouched until explicitly migrated.

Supported initial targets: Claude (`SKILL.md`), ChatGPT (`instructions.md`), Cursor (`instructions.md`), and Codex (`SKILL.md`). Generated content does not imply automatic installation or runtime compatibility. Validate actual behavior in each target host.

Codex entrypoints render only `name` and `description` in YAML. Repository-specific fields remain in the unchanged canonical header and in Codex `build-provenance.json` as `source_frontmatter`; policy `codex-name-description-v1` applies to baseline and named-model builds. Other targets retain canonical headers. See the [compatibility and helper assessment](../evaluations/candidate-compatibility-2026-10-19.md).

Generation requires `python -m pip install -r requirements-dev.txt`. Canonical frontmatter is validated against the repository schema before any candidates are written. The generated marker sits after YAML frontmatter. Both generation and `--check` report obsolete managed candidates when a master is removed or renamed; review and remove those files manually. The generator does not delete stale files or overwrite unmanaged content.

## Migration inventory and provenance

The [candidate catalog](CATALOG.md) and [machine-readable inventory](catalog.json) contain 38 masters: all 35 Claude skill names, the example scaffold, and the independent n8n security-review and Synthetic Test Data Generator candidates. The original migration batch added 32 masters to the existing three real masters. The shipped catalog and packages are unchanged. All candidates remain unpromoted. All 36 original recorded bounded skill scopes have acceptance: 13 historical scopes plus 23 accepted through Mick-authorized delegated review on 2026-10-25. The repaired workout revision is separately accepted. Personal human inspection, broader host/model coverage and promotion remain separate. See the [current coverage and acceptance matrix](../evaluations/native-coverage-2026-10-22.md). See the [evaluation records](../evaluations/README.md) for the corrected isolated foundation runs, subsequent runtime/tool evidence and exact coverage limits. Creation-time catalog/build labels intentionally remain unreviewed/not-run; they are not a current evaluation log or a claim of broad host/model support.

Each new master keeps the original workflow and supported frontmatter, with narrowly recorded changes to assistant-host wording and a capability fallback section. Product-specific examples such as an Anthropic API integration remain because they describe the task, not a required assistant host. Owner preferences are retained as source context, not verified current facts. Claude's named WebFetch option lives in its adapter; other targets use only the capabilities actually available.

`migration.json` records the source commit, original hash and frontmatter, exact instruction transformations, dependency hashes, and original-only files. Supporting resources retain original source hashes. Reviewed candidate-only corrections are recorded separately in `supporting_file_overrides` with the corrected hash and reason; unchanged resources remain byte-identical. Regression checks verify original shipped hashes, candidate override hashes and every generated copy. Original README/install guidance, `.skill` packages, and maintenance history stay in the unchanged Claude tree and are linked through pinned source READMEs. New candidate READMEs do not claim those packages install the candidates.

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


## Per-skill compatibility and update maps

Every master includes `COMPATIBILITY.md` with intended ecosystem decisions, exact existing candidate/platform sources, adapters, bounded historical evidence and capability limits. ChatGPT and Codex are separate, as are GitHub Copilot and Microsoft Copilot. Existing files do not prove native compatibility; shipped copies remain independently maintained.

Refresh with `python tools/skill_compatibility.py`, then `python tools/generate_master_skills.py`. Check with `python tools/skill_compatibility.py --check`; the standard Python suite also checks map freshness, valid paths, copied bytes and support boundaries. Generate newly allowed candidates before refreshing the map, then regenerate again. Edit declarations/evidence rather than generated prose. This adds no native testing, installation, review pipeline or ecosystem support.

The opening status table lists twelve consistently distinguished ecosystems with `Compatibility` (`Yes`, `No`, `Unknown`) and `Implementation status` (`Implemented`, `Planned`, `Not targeted`). Yes is restricted to the evidence-backed scope printed immediately below the table, with matching instruction hashes; No requires a demonstrated blocker, not skipped placement. Existing variants are Implemented only in the repository, not necessarily installed or natively verified. Reserved product guides alone do not establish per-master plans. Detailed paths, capability contracts and historical limits remain below the summary.
Generation has no blanket target default: every master must classify every ecosystem in `ecosystems.json` with an allowed or skipped reason. `generated/target-decisions.json` exposes all decisions. Food Analyzer explicitly excludes Cursor; model profiles never widen these allowlists. Current proposed coverage is 38 Claude, 38 ChatGPT, 14 Cursor and 14 Codex candidates, including the example and both standalone additions. Manually review ambiguous mode-specific placements in GENERIC-AUDIT.md before promotion.

## New n8n security-review candidate

The original migration and acceptance history covers 36 skills. The additional [n8n-security-reviewer](n8n-security-reviewer/README.md) is a new standalone canonical candidate. It is separate from the n8n builder and has not inherited prior acceptance, installation or promotion.

## New canonical-only synthetic data master

[Synthetic Test Data Generator](synthetic-test-data-generator/SKILL.md) is a new independent master, not a migrated Claude source. It generates fictional JSON/CSV fixtures from schemas or analysis of other skills, with traceability, explicit oracles and source-hash staleness checks. Its offline Pi-hole example does not execute Pi-hole or the analyzed skill. See the [bounded validation record](../evaluations/synthetic-test-data-generator-2026-11-03.md); native host/model acceptance remains open. No shipped catalog or package is added.

The n8n-workflow expansion, n8n security reviewer and Synthetic Test Data Generator remain local review candidates. Prior acceptance applies only to the exact historical revisions and bounded scopes recorded in the linked evidence; it does not transfer to these additions or revisions.
