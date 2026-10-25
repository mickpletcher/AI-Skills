# Copilot Skill: project-handoff

## Intent

Create durable handoff documents such as `assessment.md`, `project-analysis.md`, or `handoff.md` after substantial repo work.

Use this skill when a future engineer or AI agent needs enough context to resume without rescanning the whole repository.

## Use When

- The user asks for an assessment, analysis, handoff, or resume context file
- Substantial repo work has been completed
- The repo needs a source of truth summary for future sessions
- The user wants next steps, risks, validation, and file ownership captured

## Do Not Use When

- The user only wants a chat summary
- The task is a small one-line change
- The user wants a commit message or PR description

## Workflow

1. Inspect the repo tree and changed files.
2. Read the README, changelog, tracking docs, workflows, and main source files relevant to the work.
3. Identify what is current source of truth.
4. Summarize completed work, current state, validation, risks, and next steps.
5. Choose the handoff filename based on repo convention:
   - `assessment.md` for broad repo assessment
   - `project-analysis.md` for project state and recommendations
   - `handoff.md` for session continuation
6. Keep the file practical and repo-specific.

## Output Format

Use this structure:

```markdown
# [Project] Handoff

## Current State

- [What is true now]

## Source Of Truth

| Area | File or Folder | Notes |
|---|---|---|
| [Area] | `[path]` | [why it matters] |

## Completed Work

- [Change]

## Validation

- [Command or check]

## Known Risks

- [Risk]

## Next Steps

1. [Action]
2. [Action]

## Notes For Future Agents

- [Repo convention or warning]
```

## Constraints

- Do not write generic handoff text.
- Do not claim validation that was not run.
- Do not hide unresolved risks.
- Do not replace tracked docs with a handoff file. Link or summarize them.
- Prefer existing repo naming conventions over inventing a new file.

## Help And Examples

Example prompts:

```text
Use project-handoff to create a handoff.md for this repo.
```

```text
Create project-analysis.md so the next agent can resume quickly.
```

```text
Write an assessment.md with current state, risks, and next steps.
```

## Validation Checklist

- The handoff identifies source of truth files.
- Completed work is specific.
- Validation is accurate.
- Risks and next steps are actionable.
- Future agents can resume without a full rediscovery pass.
