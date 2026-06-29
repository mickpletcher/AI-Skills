# trip-email-html-itinerary

A Claude skill for turning travel emails and booking confirmations into one polished, shareable HTML itinerary.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [trip-email-html-itinerary.skill](trip-email-html-itinerary.skill) file is the Claude-ready export built from it.

## Trigger

Use this skill when a user wants travel emails, booking confirmations, or reservation notes converted into a complete HTML itinerary.

Example prompts:

```text
Turn these trip emails into a shareable offline HTML itinerary.

Create a family travel handoff page from these hotel, flight, and rental car confirmations.

Build a full HTML trip document from these booking emails. Include contacts, day-by-day logistics, booking references, pending items, and redactions.
```

## What It Does

- Extracts flights, lodging, rental cars, events, travel admin, and pending items from email text.
- Reconciles confirmations, cancellations, updates, conflicts, and missing details.
- Redacts sensitive PINs, access codes, passwords, and payment details.
- Produces one complete HTML document using the established dark-theme itinerary design system.
- Uses the canonical destination timeline, alert strips, flights panel, day-by-day grid, booking references, checklist, admin grid, and footer sections.
- Structures the itinerary for both the traveler and family members who need quick reference information.

## Output Structure

The generated HTML includes:

1. Hero with trip title, date range, route, badges, and destination palette
2. Destination timeline cards
3. Action items
4. Flights
5. Destination sections
6. Day-by-day itinerary
7. Booking references
8. Booking checklist
9. Travel admin
10. Footer

## Implement In Claude

1. Update `SKILL.md` first.
2. Rebuild `trip-email-html-itinerary.skill` from the current source files.
3. Import the `.skill` package into Claude using your normal Claude skills workflow.
4. Test with pasted booking emails and confirm the output is a single complete HTML document using the canonical design system.

## Upgrade Log

See [upgrades.md](upgrades.md) for implemented upgrades and [future-upgrades.md](future-upgrades.md) for backlog ideas.
