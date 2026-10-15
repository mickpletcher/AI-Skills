# GitHub Repo Architect: pilot migration review

Source: `claude/skills/github-repo-architect/SKILL.md` (unchanged).
Master: `master-skills/github-repo-architect/SKILL.md`.

## Changes
- Removed person-specific style instructions and host-specific assumptions from core.
- Preserved `repo`, `gra`, and `architect repo` triggers.
- Added explicit authorization and evidence checks for repository writes.
- Added a concise output contract and security requirements.
- Moved Claude host instructions into an adapter.

## Known risks
- The original is substantially longer and includes detailed formatting presets; compare behavior before replacing it.
- No live model execution or regression tests have yet been performed.
- Generated variants are candidates only and must not replace installed Claude skills.

## Baseline tests to run
1. `repo Python CLI to monitor local DNS with pytest`: returns coherent tree, README, CI, three tests.
2. `gra private credential management tool`: asks for missing security context before producing sensitive implementation.
3. `Audit my existing GitHub repository`: does not invoke new-repo scaffolding.
4. `Build this repo in GitHub` without write access: supplies a proposal, never claims a commit.

Status: generalized; awaiting automated and live behavioral validation.
