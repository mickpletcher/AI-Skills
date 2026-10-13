# GitHub README pilot modernization review

Legacy source: `claude/skills/github-readme/SKILL.md` (unchanged).
Neutral master: `master-skills/github-readme/SKILL.md`.

## Improvements
- Removed hardcoded author identity while retaining direct technical style.
- Explicitly separates verified commands and repository facts from assumptions.
- Preserves `readme` and `gr` shorthand triggers.
- Strengthens repair-mode behavior and discourages needless full rewrites.
- Separates actual authorized repository writes from drafting advice.

## Known differences and risk
The original contains detailed example sections and repository-type templates. The neutral master is more compact; compare output completeness before any promotion. No live model behavior has been tested.

## Regression scenarios
1. Existing Python CLI with real pyproject.toml: generate README using verified commands.
2. Outdated PowerShell README: propose targeted corrections rather than a full rewrite.
3. Repository link unavailable: mark commands and paths as unverified.
4. Request to architect a new repository: route away from README writer.
5. Explicit request to edit GitHub without access: draft only; never claim a commit.

Status: generalized; awaiting generation checks and behavioral evaluation.
