# pihole-csv-analyzer

A Claude skill for analyzing Pi-hole CSV exports and turning them into practical cleanup recommendations.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/pihole-csv-analyzer/SKILL.md) as the canonical source for this skill. The packaged [pihole-csv-analyzer.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/pihole-csv-analyzer/pihole-csv-analyzer.skill) file is the Claude-ready export built from it.

## What It Does

This skill analyzes Pi-hole CSV exports and produces:

- an in-chat summary of the most actionable findings
- candidate blocklist domains to review
- candidate allowlist domains to review

## Trigger Conditions

Use this skill when the user:

- uploads or mentions a Pi-hole CSV file
- types `pihole` or `ph analyze`
- asks to analyze DNS query data
- asks to review blocklist hits
- asks to find domains to block or allowlist

## Supported Export Types

The analyzer should identify the export type from the CSV structure:

1. Query Log
2. Top Domains
3. Top Clients
4. Blocklist or Adlist exports

If detection is unclear, it should inspect the header and early rows before continuing.

## Important Status-Code Note

This skill uses Pi-hole's query-database status definitions when interpreting query-log exports. The blocked-versus-allowed mapping must stay aligned with the current Pi-hole documentation, especially for common values like:

- `1` blocked by gravity
- `2` allowed and forwarded
- `3` allowed and replied from cache
- `17` allowed and replied from stale cache

## File Structure

```text
pihole-csv-analyzer/
|-- README.md
|-- SKILL.md
|-- upgrades.md
`-- pihole-csv-analyzer.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `pihole-csv-analyzer.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
