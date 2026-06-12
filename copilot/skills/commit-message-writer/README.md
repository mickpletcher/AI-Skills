# commit-message-writer

A GitHub Copilot skill for writing consistent, ready to paste commit messages from a diff, changed file list, or work summary.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/commit-message-writer/instructions.md) as the editable source of truth for this skill.

## What It Does

This skill helps Copilot turn repo work into a clean commit message:

1. short imperative subject
2. concise body bullets when useful
3. accurate validation or packaging notes only when supported
4. no vague filler

## How To Implement In Copilot

Copilot skills are instruction files. Paste the contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/commit-message-writer/instructions.md) into the Copilot instruction surface you use.

## First Test

```text
Use commit-message-writer for these changed files and give me a ready to paste message.
```

## File Structure

```text
copilot/skills/commit-message-writer/
|-- README.md
`-- instructions.md
```
