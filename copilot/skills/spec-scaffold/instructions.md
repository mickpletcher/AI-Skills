# Copilot Skill: spec-scaffold

## Intent

Generate numbered spec folders with `requirements.md`, `plan.md`, and `tasks.md` for repo work that needs a clear implementation path before coding.

Use this skill when the user wants to turn a rough feature, fix, migration, or repo maintenance idea into a concrete spec package.

## Use When

- The user asks to create a spec
- The work has enough complexity to benefit from requirements, plan, and tasks
- The repo uses numbered spec folders
- The user wants an implementation checklist before code changes

## Do Not Use When

- The request is a tiny one-file change
- The user wants implementation immediately and no spec
- The task is only a commit message, PR review, or README audit

## Workflow

1. Read the user's request and any repo context.
2. Propose a kebab-case spec slug.
3. Use the next numbered folder if the repo already has a `specs/` directory.
4. Create or draft these files:
   - `requirements.md`
   - `plan.md`
   - `tasks.md`
5. Keep requirements testable and implementation-neutral.
6. Keep the plan practical and repo-aware.
7. Keep tasks ordered and checkable.

## Folder Format

Use this shape:

```text
specs/
  001-short-slug/
    requirements.md
    plan.md
    tasks.md
```

If existing specs use a different numbering or file convention, follow the repo convention.

## Requirements Format

```markdown
# Requirements: [Title]

## Goal

[One paragraph.]

## Functional Requirements

- [Requirement]

## Nonfunctional Requirements

- [Requirement]

## Acceptance Criteria

- [ ] [Observable result]
```

## Plan Format

```markdown
# Plan: [Title]

## Approach

[Short implementation approach.]

## Files Likely Touched

- `[path]`: [why]

## Validation

- [Command or manual check]
```

## Tasks Format

```markdown
# Tasks: [Title]

- [ ] Confirm current behavior and repo conventions
- [ ] Implement [specific change]
- [ ] Update docs or tracking files
- [ ] Run validation
```

## Constraints

- Do not invent repo conventions. Inspect existing `specs/` folders first.
- Do not create broad, vague requirements.
- Do not put implementation details into requirements unless they are true constraints.
- Do not skip validation tasks.

## Help And Examples

Example prompts:

```text
Use spec-scaffold to create a spec package for this feature.
```

```text
Turn this repo cleanup idea into requirements, plan, and tasks.
```

## Validation Checklist

- The spec folder name is numbered and kebab-case.
- Requirements are testable.
- Plan is repo-aware.
- Tasks are ordered and actionable.
- Validation is explicit.
