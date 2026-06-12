# Copilot Skill: repo-cleanup-audit

## Intent

Audit a repository before cleanup by classifying files into current source of truth, stale artifacts, generated outputs, historical records, dependency or cache folders, and files that need owner review.

Use this skill when the user wants to clean a repo but needs a safe inventory first. The goal is to prevent accidental deletion of important source, docs, test fixtures, workflow files, or historical context.

## Use When

- The user asks what files can be deleted, archived, or ignored
- The repo has old scripts, duplicate docs, generated artifacts, package leftovers, or unclear source files
- The user wants a cleanup plan before running delete commands
- The user needs to separate active files from historical or stale files
- The user asks for a source of truth review across README, scripts, tests, configs, and packaged artifacts

## Do Not Use When

- The user already gave a precise delete list and only wants the command
- The request is a normal pull request review
- The task is to rewrite code instead of classify repository files
- There is not enough file tree, git status, or repo context to classify safely

## Audit Priorities

Classify files conservatively. When in doubt, mark a file as `Needs owner review` instead of recommending deletion.

Use these categories:

1. `Keep`: active source, tests, docs, workflows, config, examples, schemas, templates, or install artifacts still referenced by the repo.
2. `Archive`: historical context worth preserving but not needed in the active path.
3. `Delete candidate`: stale duplicate, broken leftover, obsolete generated file, or unused artifact with clear evidence.
4. `Generated`: build output, coverage, package artifact, compiled asset, logs, or reports that should be recreated from source.
5. `Dependency or cache`: vendored dependency, package cache, virtual environment, node modules, tool cache, or local runtime folder.
6. `Needs owner review`: ambiguous file, unclear ownership, possible user notes, local planning, or something that may be intentionally private.

## Workflow

1. Read the repo tree, README, major docs, package or project files, scripts, tests, workflows, and `.gitignore`.
2. Check git status before recommending cleanup.
3. Identify source of truth files:
   - package manifests
   - main scripts or application entrypoints
   - tests
   - workflows
   - schemas or templates
   - README and tracked docs
   - generated package source versus packaged export
4. Find obvious stale or duplicate files:
   - old package artifacts
   - backup files
   - duplicate docs with older naming
   - obsolete generated outputs
   - checked in local logs or reports
   - orphaned files not referenced by docs, scripts, tests, or manifests
5. Check whether ignored files are intentionally local planning or accidental clutter.
6. Produce a classification table before suggesting any cleanup command.
7. Recommend safe next steps:
   - keep unchanged
   - archive to a named folder
   - add or refine `.gitignore`
   - delete only after owner confirmation
   - update docs to point to the source of truth

## What To Check

- Does README mention a file that no longer exists
- Does a packaged artifact match its source file
- Are there old names and new names for the same tracking document
- Are generated files committed when they should be ignored
- Are local planning files ignored precisely
- Are scripts, tests, or workflows still referencing the file
- Is the file a fixture or example that looks stale but is actually required
- Is the file user-owned context that should not be deleted by an automated cleanup

## Output Format

Use this structure:

```text
Repo Cleanup Audit

Source Of Truth
| Area | Source file or folder | Notes |
|---|---|---|
| [Area] | [Path] | [Why it is current] |

Classification
| Path | Category | Evidence | Recommendation |
|---|---|---|---|
| [path] | Keep / Archive / Delete candidate / Generated / Dependency or cache / Needs owner review | [specific evidence] | [specific action] |

Cleanup Plan
1. [Safe first step]
2. [Next step]
3. [Owner confirmation needed]

Do Not Delete Yet
- [Ambiguous path and why]

Suggested .gitignore Changes
- [Precise ignore rule or none]
```

If no cleanup candidates are found, say that plainly:

```text
Repo Cleanup Audit

No clear delete candidates found.

Residual Risk
- [What still needs owner review or better repo context]
```

## Constraints

- Do not recommend destructive commands as the first response.
- Do not classify a file as safe to delete without evidence.
- Do not assume ignored files are junk. Some local planning files are intentional.
- Do not recommend broad ignore rules that hide real source files.
- Do not delete or move files unless the user explicitly asks for implementation after the audit.
- Keep recommendations tied to concrete paths.
- Prefer precise `.gitignore` rules over broad folder ignores.

## Help And Examples

If the user asks how to use this skill, explain that it audits a repo before cleanup and classifies files by risk.

Minimum useful input:

- repo tree
- git status
- README or project docs
- any cleanup concern from the user

Example prompts:

```text
Use repo-cleanup-audit to classify stale files before I clean this repo.
```

```text
Audit this repo tree and tell me what is source of truth, generated, stale, or owner review.
```

```text
Check whether these old package artifacts can be deleted or should be archived.
```

## Validation Checklist

- The audit identifies source of truth files before cleanup candidates.
- Every delete candidate has concrete evidence.
- Ambiguous files are marked `Needs owner review`.
- `.gitignore` recommendations are precise.
- The output does not suggest destructive commands before user confirmation.
