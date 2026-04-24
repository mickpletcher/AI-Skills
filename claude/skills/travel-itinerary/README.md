# travel-itinerary

A Claude skill for planning, formatting, and exporting travel itineraries as Obsidian-ready Markdown files.

## Source of Truth

Use [SKILL.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-itinerary/SKILL.md) as the canonical source for this skill. The packaged [travel-itinerary.skill](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/claude/skills/travel-itinerary/travel-itinerary.skill) file is the Claude-ready export built from it.

## Trigger

Start any message with `trip` or `itinerary` to activate this skill immediately.

It also applies to requests like:

```text
trip build me a 7 day Japan itinerary
itinerary format this Europe trip for Obsidian
plan my trip to Costa Rica
format this itinerary for Obsidian
export my trip as markdown
```

## What It Does

This skill builds a usable first draft without unnecessary questions when enough information already exists. It:

- extracts trip logistics, dates, destinations, and anchor events from the conversation
- builds a single Markdown itinerary document
- validates date math, routing, and budget assumptions
- produces an Obsidian-friendly output structure

## Output Structure

Full itinerary requests can include:

1. Trip Summary
2. Logistics Overview
3. Anchor Events
4. Day-by-Day Plan
5. Accommodation Summary
6. Budget Tracker
7. Packing List
8. Key Contacts and Info
9. Open Items / To-Do

## File Structure

```text
travel-itinerary/
|-- README.md
|-- SKILL.md
`-- travel-itinerary.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `travel-itinerary.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
