# powershell-refactor

A Claude skill for simplifying, tightening, and standardizing existing PowerShell scripts without changing what they are supposed to do.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/powershell-refactor/SKILL.md) as the canonical source for this skill. The packaged [powershell-refactor.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/powershell-refactor/powershell-refactor.skill) file is the Claude ready export built from it.

## What It Does

This skill improves existing PowerShell scripts by focusing on:

1. smaller and clearer control flow
2. less duplication
3. more consistent naming
4. practical PowerShell conventions
5. safer handling for scripts that make changes

It is meant for focused cleanup work, not full rewrites or greenfield scaffolding.

## Use When

- A script works but is messy
- Function names or parameter blocks are inconsistent
- The user wants a script tightened up without changing its job
- The code needs a more idiomatic PowerShell structure

## File Structure

```text
powershell-refactor/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- powershell-refactor.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for implemented changes to this skill.

## Implement In Claude

1. Update the checked in source files for this skill first.
2. Rebuild `powershell-refactor.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Refresh Claude and test with a real PowerShell cleanup request.
