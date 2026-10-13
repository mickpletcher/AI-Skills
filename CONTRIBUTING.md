# Contributing

Read [shared conventions](shared/skill-standard.md), [platform organization](shared/platform-organization.md), and [installation guidance](docs/installation.md). For cross-skill or shared tooling work, add a numbered spec under `specs/` with requirements, design, plan, and tasks.

1. Work on a focused branch. Keep credentials, local runtime data, and personal inputs outside this repository.
2. Keep the exact `README.md` and platform source filenames. Claude requires `SKILL.md`, `<folder-name>.skill`, and `completedchanges.md`. Use that history spelling consistently. Add supported YAML frontmatter to Claude sources; see [schema](schemas/skill-frontmatter.schema.json).
3. Put lengthy conditional workflows in references. Keep triggers, constraints, routing, and explicit loading instructions in the main source. Verify moved text is preserved; when intentionally editing an existing moved reference, update its snapshot hash with reviewer-visible rationale.
4. Declare helper prerequisites in the skill README. Do not claim a last-tested model/date without an actual recorded evaluation. Add representative scenarios to the [evaluation framework](evaluations/README.md).
5. Install [maintenance dependencies](docs/dependencies.md), rebuild packages and catalog, then run the commands below.
6. Review every changed package payload and generated catalog entry. Add a concise change-history note; do not rewrite past entries. Include test results and platform limits in the PR.

```sh
python tools/skill_repository.py package
python tools/skill_repository.py catalog
python tools/skill_repository.py validate
python -m unittest discover -s tools/tests -v
python tools/evaluate.py self-test
```

```powershell
./claude/scripts/Validate-SkillFolders.ps1 -Root ./claude/skills -FailOnIssues
./claude/scripts/Validate-SkillQuality.ps1 -FailOnIssues
./claude/scripts/tests/Initialize-ClaudeSkills.Tests.ps1
```

The PR workflow runs validation on Windows and Linux with read-only repository permissions and no model calls. A failing step fails the job. This workflow alone **does not enforce merge protection**. An owner must separately require `Validate (ubuntu-latest)` and `Validate (windows-latest)` in the appropriate ruleset/branch protection after those jobs have run and their exact check names are confirmed. No settings are changed here.

External URL availability, arbitrary runtime-generated paths, and actual model quality are not certified by static link/structure checks. The checker validates navigable Markdown inline/reference links and fragments, excluding code examples; review plain-text paths and HTML resources as part of domain changes.

See [distribution and the license decision](docs/distribution.md) before any release. Do not add a license identifier or claim that the project is open source until the owner has supplied the intended terms.

See [local validation evidence](docs/validation-results.md) for the current implementation checks and untested-platform limits.
