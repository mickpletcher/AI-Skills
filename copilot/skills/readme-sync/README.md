# readme-sync

A GitHub Copilot skill for reconciling README claims with actual code, scripts, commands, tests, configuration, and outputs.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/readme-sync/instructions.md) as the editable source of truth for this skill.

## What It Does

This skill checks README drift by comparing docs against live repo state:

1. paths and links
2. setup commands
3. scripts and parameters
4. validation steps
5. feature claims
6. tracking docs and packaged artifacts

## How To Implement In Copilot

Copilot skills are instruction files. Paste the contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/readme-sync/instructions.md) into the Copilot instruction surface you use.

## First Test

```text
Use readme-sync to check whether README.md matches the current repo.
```

## File Structure

```text
copilot/skills/readme-sync/
|-- README.md
`-- instructions.md
```
