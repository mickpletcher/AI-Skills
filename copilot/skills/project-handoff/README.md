# project-handoff

A GitHub Copilot skill for creating durable handoff documents such as `assessment.md`, `project-analysis.md`, or `handoff.md` after substantial repo work.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/project-handoff/instructions.md) as the editable source of truth for this skill.

## What It Does

This skill creates repo-local context files that let a future engineer or AI agent resume quickly:

1. current state
2. source of truth files
3. completed work
4. validation
5. known risks
6. next steps

## How To Implement In Copilot

Copilot skills are instruction files. Paste the contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/project-handoff/instructions.md) into the Copilot instruction surface you use.

## First Test

```text
Use project-handoff to create a handoff.md for this repo.
```

## File Structure

```text
copilot/skills/project-handoff/
|-- README.md
`-- instructions.md
```
