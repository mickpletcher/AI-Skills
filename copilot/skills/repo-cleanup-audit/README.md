# repo-cleanup-audit

A GitHub Copilot skill for classifying stale files, historical artifacts, generated outputs, and current source of truth files before repository cleanup.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/repo-cleanup-audit/instructions.md) as the editable source of truth for this skill.

## What It Does

This skill helps Copilot audit a repo before cleanup. It classifies files into:

1. keep
2. archive
3. delete candidate
4. generated
5. dependency or cache
6. needs owner review

It is meant to prevent accidental deletion by separating active source of truth files from stale or generated artifacts.

## How To Implement In Copilot

This repo does not package Copilot skills like Claude `.skill` files. Copilot skills are instruction files that you place into the Copilot workflow you use.

### Option 1: Repo level Copilot instructions

Use this when you want cleanup audit behavior available in a specific repository.

1. Open the target repository where you use Copilot.
2. Check whether the repo already has a `.github/copilot-instructions.md` file.
3. If it does not exist, create it.
4. Copy the full contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/repo-cleanup-audit/instructions.md).
5. Paste the content into `.github/copilot-instructions.md`.
6. If that file already contains other useful instructions, merge this skill carefully instead of deleting the existing rules.
7. Save the file.
8. Open Copilot Chat in that repo and test the skill against a real repo tree and `git status`.

### Option 2: Prompt file or note for manual reuse

Use this when you do not want repo wide instructions.

1. Keep [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/repo-cleanup-audit/instructions.md) open in your editor.
2. Start a Copilot Chat session.
3. Paste the instruction content into the chat before the repo tree, git status, or cleanup concern.
4. Add your audit request.
5. Reuse the same instruction block whenever you want a cleanup classification pass.

## First Test

After setup, test it with a real repo and ask:

```text
Use repo-cleanup-audit to classify stale files before I clean this repo.
```

Then check whether the response:

- identifies source of truth files first
- avoids destructive commands
- classifies ambiguous files as owner review
- ties every cleanup recommendation to concrete evidence
- recommends precise `.gitignore` rules when needed

## File Structure

```text
copilot/skills/repo-cleanup-audit/
|-- README.md
`-- instructions.md
```
