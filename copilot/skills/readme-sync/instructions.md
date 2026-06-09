# Copilot Skill: readme-sync

## Intent

Reconcile README claims with the actual repo files, scripts, commands, tests, configuration, and outputs.

Use this skill when the user wants to know whether documentation matches the current repository behavior.

## Use When

- The user asks whether the README is current
- The repo has scripts, commands, workflows, or setup docs that may have drifted
- The user wants stale claims, missing setup steps, or broken links identified
- A feature changed and docs need to be checked against reality

## Do Not Use When

- The user wants a full rewrite without an audit
- The task is a PR review focused on code risk
- The request is only a commit message

## Workflow

1. Read the README first.
2. Inspect the live repo tree.
3. Check scripts, package files, workflows, config, tests, examples, and docs referenced by the README.
4. Compare README commands to real file paths and available scripts.
5. Check whether setup steps mention required prerequisites and outputs.
6. Identify drift as concrete findings.
7. Recommend exact README edits or apply them if the user asked for implementation.

## What To Check

- Broken relative links
- Files or folders mentioned but missing
- Existing files or commands omitted from the README
- Setup commands that no longer work
- Script names, parameters, or paths that changed
- CI or validation commands missing from docs
- Claims about features that are not implemented
- Packaged artifacts that are stale versus source files
- Tracking docs not linked from the README

## Output Format

Use this structure for audits:

```text
README Sync Audit

Findings
| README Claim | Actual Repo State | Fix |
|---|---|---|
| [claim or path] | [evidence] | [edit] |

Missing From README
- [Useful repo feature, command, or doc]

Suggested Edits
1. [Specific edit]
2. [Specific edit]
```

If no drift is found:

```text
README Sync Audit

No README drift found in the checked areas.

Checked
- [Area]
```

## Constraints

- Do not trust README claims without checking files.
- Do not make vague confidence statements.
- Tie every finding to a path, command, or observed repo state.
- Do not remove useful beginner setup detail just to shorten the README.
- Prefer accurate docs over polished wording.

## Help And Examples

Example prompts:

```text
Use readme-sync to check whether this README matches the repo.
```

```text
Audit the setup commands in README.md against the actual scripts.
```

```text
Find README drift after these repo changes.
```

## Validation Checklist

- README claims were compared to live files.
- Findings cite concrete paths or commands.
- Missing docs are called out separately from wrong docs.
- Suggested edits are specific enough to apply.
