# pihole-blocklist

A Claude skill for evaluating, categorizing, and documenting new Pi-hole blocklist sources.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/pihole-blocklist/SKILL.md) as the canonical source for this skill. The packaged [pihole-blocklist.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/pihole-blocklist/pihole-blocklist.skill) file is the Claude-ready export built from it.

## Overview

This skill covers the curation side of Pi-hole maintenance: deciding whether a new source should be added, skipped, or handled cautiously. It complements [pihole-csv-analyzer](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/pihole-csv-analyzer/README.md), which focuses on analyzing what is already being blocked.

## Trigger

Use this skill when the user:

- pastes a raw blocklist URL for evaluation
- asks whether a list should be added
- wants to review existing sources for overlap
- wants repo documentation updated for a new source or category
- asks about adding or removing a Pi-hole blocklist source

## Evaluation Output

The skill should produce structured output like:

```text
SOURCE: [Name]
URL: [raw URL]
CATEGORY: [from taxonomy]
MAINTAINER: [GitHub user / org / project name]
LAST UPDATED: [date or "active"]
DOMAIN COUNT: [approximate]
FORMAT: [hosts / plain domain list / mixed]
OVERLAP RISK: [low / medium / high]
FALSE POSITIVE RISK: [low / medium / high]
RECOMMENDATION: [Add / Add with caution / Skip / Whitelist candidate]
NOTES: [caveats, known issues, context]
```

## Reference File

Use [pihole-blocklist-sources.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/pihole-blocklist/pihole-blocklist-sources.md) as the local source index for the current curated-source catalog.

## File Structure

```text
pihole-blocklist/
|-- README.md
|-- SKILL.md
|-- pihole-blocklist-sources.md
|-- upgrades.md
`-- pihole-blocklist.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `pihole-blocklist.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
