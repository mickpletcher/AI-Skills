# Canonical skills

Skills in this directory are platform-independent sources. Each skill uses a `SKILL.md` with YAML frontmatter containing `name` and `description`. Keep platform-specific instructions in `adapters/<platform>/<skill>/append.md`.

Generate outputs with `python tools/generate_master_skills.py`. Run `python tools/generate_master_skills.py --check` in CI to detect drift. Existing platform-owned skills remain untouched until explicitly migrated.

Supported initial targets: Claude (`SKILL.md`), ChatGPT (`instructions.md`), Cursor (`instructions.md`), and Codex (`SKILL.md`). Generated content does not imply automatic installation or runtime compatibility. Validate actual behavior in each target host.

Generation requires `python -m pip install -r requirements-dev.txt`. Canonical frontmatter is validated against the repository schema before any candidates are written. The generated marker sits after YAML frontmatter. Both generation and `--check` report obsolete managed candidates when a master is removed or renamed; review and remove those files manually. The generator does not delete stale files or overwrite unmanaged content.
