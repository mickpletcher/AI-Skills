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
- applies an itinerary template for city trips, road trips, active travel, or mixed work plus leisure trips
- checks daily structure so transit time, meals, and pacing are more realistic
- adds visa and border crossing checkpoints for multi-country trips
- compares lodging location, price, and transit convenience in accommodation notes
- uses arrival and departure day templates for red-eye flights, late check-ins, early departures, and overnight transit
- rolls up packing and reservation summaries for faster trip review
- adds route notes, daily budget visibility, and contingency planning where useful
- validates date math, routing, and budget assumptions
- produces an Obsidian-friendly output structure

## Output Structure

Full itinerary requests can include:

1. Trip Summary
2. Logistics Overview
3. Anchor Events
4. Day-by-Day Plan
5. Accommodation Summary
6. Visa and Border Checkpoints
7. Budget Tracker
8. Packing List
9. Key Contacts and Info
10. Open Items / To-Do
11. Reservation Summary
12. Daily Budget View
13. Map and Route Notes
14. Packing Summary

## Supported Templates

- `city trip`
- `road trip`
- `active travel`
- `mixed work and leisure`

## Example Prompts

```text
trip build a road trip itinerary from Nashville to Colorado with nightly stop planning

itinerary format this mixed work and leisure Tokyo trip for Obsidian

trip build an active travel itinerary around a triathlon weekend

itinerary add route notes, daily budgets, and backup plans to this Europe trip

trip build a Spain, Morocco, and Portugal itinerary with border checkpoints and lodging tradeoffs

itinerary tighten this red-eye arrival and late check-in day so it is realistic
```

## File Structure

```text
travel-itinerary/
|-- README.md
|-- SKILL.md
`-- travel-itinerary.skill
|-- upgrades.md
```

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `travel-itinerary.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.

