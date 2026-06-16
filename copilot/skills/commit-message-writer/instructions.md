# Copilot Skill: commit-message-writer

## Intent

Write consistent, ready to paste commit messages from a repo diff, changed file list, or work summary.

Use this skill when the user wants a concise commit subject and practical body bullets that describe what changed and why.

## Use When

- The user asks for a commit message
- The user provides `git diff`, `git status`, changed files, or a work summary
- The repo has several related changes that need one coherent commit message
- The user wants a ready to paste subject and body

## Do Not Use When

- The user wants release notes, a pull request description, or a changelog entry
- The user has not provided enough context to describe the change safely
- The request is to stage, commit, or push files

## Workflow

1. Read the changed files, diff, or work summary.
2. Identify the main user-visible or repo-visible change.
3. Separate implementation changes from validation and documentation updates.
4. Write a short imperative subject line.
5. Add body bullets only when they add useful context.
6. Avoid mentioning files that were not part of the change.

## Output Format

Use this format:

```text
Short imperative subject

- Body bullet for the main behavior or artifact change
- Body bullet for docs, tests, validation, or packaging updates
- Body bullet for any important cleanup or tracking update
```

For very small changes, use only the subject:

```text
Short imperative subject
```

## Rules

- Keep the subject under 72 characters when practical.
- Use imperative mood: `Add`, `Update`, `Fix`, `Rename`, `Remove`.
- Do not add prefixes like `feat:` unless the user asks for Conventional Commits.
- Do not overstate the change.
- Do not include vague filler like `misc updates`.
- Do not include testing claims unless tests or validation actually ran.
- Prefer one coherent commit over a long laundry list.

## Help And Examples

Minimum useful input:

- `git status`
- changed file list
- diff summary
- or a short description of what changed

Example prompts:

```text
Use commit-message-writer for these changes.
```

```text
Create a commit message from this git diff.
```

```text
Write a concise commit message for the files I just changed.
```

## Validation Checklist

- The subject describes the real change.
- The body bullets are specific and accurate.
- The message is ready to paste.
- The message does not claim unverified tests.
