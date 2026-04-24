# Container Home Claude Skill

Claude-specific skill package for Mick's off-grid shipping container lake home project in Dover, Tennessee.

This skill now uses a checked-in source file instead of the older `skill.md` plus `skill.zip` layout.

## Files

```text
claude/skills/container-home/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- container-home.skill
```

## Source Of Truth

- Claude runtime source: [`SKILL.md`](./SKILL.md)

Update `SKILL.md` when the project context or guidance changes, then rebuild `container-home.skill` so the packaged export stays in sync.

## What This Skill Covers

- Design and expansion questions for the container home project
- Septic, solar, water, and other off-grid systems planning
- Fabrication and welding guidance specific to this build
- Project-aware writing help, including Facebook posts about the build

## Installation

Package `SKILL.md` into `container-home.skill`, then install it with your normal Claude skill workflow.

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `container-home.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
