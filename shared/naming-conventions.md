# Naming Conventions

Use these rules to keep portable skills and platform variants easy to find.

## Skill Names

- Prefer capability names over brand names.
- Use short noun phrases or verb-noun pairs.
- Avoid version numbers in file names.
- Avoid platform names in the canonical portable skill name unless the skill is intentionally platform-specific.

Good examples:

- `repo-readme-audit`
- `azure-resource-visualizer`
- `idea-review`

Avoid:

- `chatgpt-readme-skill-v2`
- `claude_best_prompt_final`
- `copilot-helper-new`

## File Names

- Use lowercase kebab-case.
- Keep names stable even if the implementation improves.
- Use `*-template.md` only for starter files.

## Directory Intent

- `shared/` is for standards and cross-platform guidance.
- `templates/` is for reusable starting points.
- platform folders should contain only platform-owned files or wrappers.

## Variant Naming

When one portable skill has platform variants, keep the base name identical and let the directory communicate the platform.

Example:

- `claude/skills/repo-readme-audit.md`
- `chatgpt/skills/repo-readme-audit.md`
- `copilot/instructions/repo-readme-audit.md`

## Display Titles

The visible title inside a file can be human-friendly, but the file name should remain stable and machine-friendly.
