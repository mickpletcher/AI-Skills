# travel-planning

A Claude skill for planning solo travel with Mick's travel preferences, constraints, and active-trip context built in.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-planning/SKILL.md) as the canonical source for this skill. The packaged `travel-planning.skill` file should be treated as the Claude-ready export built from it.

## Overview

This skill handles broader trip research and planning, not just itinerary formatting. It is designed to:

- build personalized trip plans
- estimate budgets
- surface logistics flags
- compare destinations and travel options
- use active-trip research files when relevant

All planning defaults to solo travel unless a specific trip is noted otherwise.

## Hard Constraints

| Constraint | Rule |
| --- | --- |
| Accommodation | Private rooms only |
| Home airport | BNA unless explicitly overridden |
| Travel default | Solo |
| Budget mindset | Value-optimized, not backpacker-cheap and not luxury |
| Activity anchor | Prefer endurance or adventure anchors when available |

## Reference Files

Use the local reference files when the trip matches them:

- [references/europe-2026.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-planning/references/europe-2026.md)
- [references/colorado-2026.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-planning/references/colorado-2026.md)

## File Structure

```text
travel-planning/
|-- README.md
|-- SKILL.md
`-- references/
    |-- europe-2026.md
    `-- colorado-2026.md
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `travel-planning.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
