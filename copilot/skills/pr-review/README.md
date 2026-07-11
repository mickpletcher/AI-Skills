# pr-review

A GitHub Copilot skill for reviewing pull requests with a focus on regressions, practical risk, and missing tests.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/pr-review/instructions.md) as the editable source of truth for this skill.

## What It Does

This skill helps Copilot review pull requests by focusing on the highest value review work:

1. regressions
2. risky logic changes
3. weak validation or error handling
4. missing or weak tests
5. workflow or deployment break risk

It is meant for review quality, not code generation.

## How To Implement In Copilot

This repo does not package Copilot skills like Claude `.skill` files. Copilot skills are instruction files that you place into the Copilot workflow you use.

### Option 1: Repo level Copilot instructions

Use this when you want the review behavior available in a specific repository.

1. Open the target repository where you use Copilot.
2. Check whether the repo already has a `.github/copilot-instructions.md` file.
3. If it does not exist, create it.
4. Copy the full contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/pr-review/instructions.md).
5. Paste the content into `.github/copilot-instructions.md`.
6. If that file already contains other useful instructions, merge this skill carefully instead of deleting the existing rules.
7. Save the file.
8. Open Copilot Chat in that repo and test the skill with a sample pull request or diff.

### Option 2: Prompt file or note for manual reuse

Use this when you do not want repo wide instructions.

1. Keep [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/pr-review/instructions.md) open in your editor.
2. Start a Copilot Chat session.
3. Paste the instruction content into the chat before the pull request diff or changed files.
4. Add your review request.
5. Reuse the same instruction block whenever you want a strict PR review pass.

## First Test

After setup, test it with a small real diff and ask:

```text
Review this pull request for regressions, risk, and missing tests. Lead with findings only.
```

Then check whether the response:

- starts with findings instead of praise
- points to real files
- explains why the issue matters
- calls out missing tests only when they match changed behavior

## File Structure

```text
copilot/skills/pr-review/
|-- README.md
`-- instructions.md
```
