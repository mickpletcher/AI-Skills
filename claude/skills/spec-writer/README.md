# spec-writer

A Claude skill for generating numbered repo spec folders with clear requirements, implementation plans, and task lists for non-trivial work.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/spec-writer/SKILL.md) as the canonical source for this skill. The packaged [spec-writer.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/spec-writer/spec-writer.skill) file is the Claude-ready export built from it.

## What It Does

This skill helps create repo specs that are structured enough to drive real implementation work:

1. picks or confirms the next numbered spec folder
2. writes practical `requirements.md`, `plan.md`, and `tasks.md`
3. keeps scope, assumptions, risks, and validation explicit
4. aligns the spec with the live repo instead of generic templates

It is meant for planning non-trivial work, not for tiny changes that should just be implemented directly.

## Use When

- A repo change needs a formal spec package
- The work spans multiple files, phases, or decisions
- The repo already uses numbered specs and needs another one
- The user wants an execution ready breakdown before coding starts

## File Structure

```text
spec-writer/
|-- README.md
|-- SKILL.md
|-- completedchanges.md
|-- upgrades.md
`-- spec-writer.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for implemented changes to this skill.

## Completed Changes

See [completedchanges.md](completedchanges.md) for the tracked shipped history of this skill.

## Implement In Claude

1. Update the checked in source files for this skill first.
2. Rebuild `spec-writer.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Test it against a real repo change that needs a numbered spec folder.
