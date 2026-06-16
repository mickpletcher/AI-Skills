# spec-scaffold

A GitHub Copilot skill for generating numbered spec folders with requirements, plan, and task files.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/spec-scaffold/instructions.md) as the editable source of truth for this skill.

## What It Does

This skill turns a rough repo idea into:

1. `requirements.md`
2. `plan.md`
3. `tasks.md`

It follows existing repo spec conventions when they exist.

## How To Implement In Copilot

Copilot skills are instruction files. Paste the contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/copilot/skills/spec-scaffold/instructions.md) into the Copilot instruction surface you use.

## First Test

```text
Use spec-scaffold to create a numbered spec folder for this repo feature.
```

## File Structure

```text
copilot/skills/spec-scaffold/
|-- README.md
`-- instructions.md
```
