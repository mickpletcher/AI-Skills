# Canonical skills

Skills in this directory are platform-independent sources. Each skill uses a `SKILL.md` with YAML frontmatter containing `name` and `description`. Keep platform-specific instructions in `adapters/<platform>/<skill>/append.md`.

Generate outputs with `python tools/generate_master_skills.py`. Run `python tools/generate_master_skills.py --check` in CI to detect drift. Existing platform-owned skills remain untouched until explicitly migrated.

Supported initial targets: Claude (`SKILL.md`), ChatGPT (`instructions.md`), Cursor (`instructions.md`), and Codex (`SKILL.md`). Generated content does not imply automatic installation or runtime compatibility. Validate actual behavior in each target host.

Generation requires `python -m pip install -r requirements-dev.txt`. Canonical frontmatter is validated against the repository schema before any candidates are written. The generated marker sits after YAML frontmatter. Both generation and `--check` report obsolete managed candidates when a master is removed or renamed; review and remove those files manually. The generator does not delete stale files or overwrite unmanaged content.

## Migration inventory and provenance

The [candidate catalog](CATALOG.md) and [machine-readable inventory](catalog.json) contain 36 masters: all 35 Claude skill names plus the example scaffold. This batch adds 32 masters to the existing three real masters. The shipped catalog and packages are unchanged. All candidates remain unpromoted and behavior evaluation is **not run** on every target.

Each new master keeps the original workflow and supported frontmatter, with narrowly recorded changes to assistant-host wording and a capability fallback section. Product-specific examples such as an Anthropic API integration remain because they describe the task, not a required assistant host. Owner preferences are retained as source context, not verified current facts. Claude's named WebFetch option lives in its adapter; other targets use only the capabilities actually available.

`migration.json` records the source commit, original hash and frontmatter, exact wording substitutions, dependency hashes, and original-only files. Scripts, references, schemas, templates, examples, assets, and skill-specific license notices are copied byte-for-byte. Original README/install guidance, `.skill` packages, and maintenance history stay in the unchanged Claude tree and are linked through pinned source READMEs. New candidate READMEs do not claim those packages install the candidates.

## Complete generated bundles

Generation includes the complete master directory except package archives and Python bytecode caches. ChatGPT/Cursor use `instructions.md` as their entry point and retain a canonical `SKILL.md` companion so internal reference links still resolve. Claude/Codex use the rendered `SKILL.md` entry point. Supporting resource bytes are not rewritten, and `.gitattributes` preserves those bytes on every checkout platform.

`generated/.resource-manifest.json` tracks resource ownership and hashes. Check mode reports missing/drifted files and obsolete tracked resources. Normal generation refuses to overwrite edited or unmanaged resources, validates the whole plan first, and never deletes anything. For an intentional resource removal/rename, review and remove its obsolete generated copies **and their manifest entries** in the same change before regenerating. Resolve local edits manually before regeneration. Symlinked bundles are rejected.

Helper prerequisites remain those of the source: see [repository dependencies](../docs/dependencies.md) and the pinned original README in each candidate. Copying a helper does not execute it, install dependencies, grant filesystem/app access, or schedule anything. Keep runtime outputs and personal data outside these tracked candidate bundles.

## Review gates

Run `python tools/generate_master_skills.py --check`, `python tools/skill_repository.py validate`, and `python -m unittest discover -s tools/tests -v`. Migration regressions cover inventory equality, metadata/provenance, exact source and resource preservation, navigable local links, and generated-resource collision/drift/removal behavior. These are structural checks; the existing synthetic fixture self-test does not certify all 35 migrated skills. Before promotion, review actual behavior with synthetic inputs on each intended host/model and verify helper prerequisites independently.
