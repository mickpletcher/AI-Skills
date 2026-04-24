# resume-writer

A Claude skill for rewriting, auditing, and scoring resumes using a persistent library of recruiter and hiring-manager principles.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/SKILL.md) as the canonical source for this skill. The packaged [resume-writer.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/resume-writer.skill) file is the Claude-ready export built from it.

## Overview

This skill has two main modes:

1. `Enhance` mode for rewriting, auditing, and scoring a resume
2. `Add Insight` mode for extracting new principles from recruiter or hiring guidance and adding them to the local library

It supports human-readable audit output plus structured JSON output for automation.

## Core Files

- [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/SKILL.md): triggers, workflows, scoring flow, and output rules
- [scoring-model.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/scoring-model.md): deterministic scoring rules
- [json-output-spec.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/json-output-spec.md): machine-readable output contract
- [insights/principles.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/insights/principles.md): persistent recruiter-principle library
- [references/common-patterns.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/resume-writer/references/common-patterns.md): fallback structural patterns and red flags

## File Structure

```text
resume-writer/
|-- README.md
|-- SKILL.md
|-- scoring-model.md
|-- json-output-spec.md
|-- insights/
|   `-- principles.md
|-- references/
|   `-- common-patterns.md
`-- resume-writer.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `resume-writer.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
