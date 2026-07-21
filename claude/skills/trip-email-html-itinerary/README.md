# trip-email-html-itinerary

A Claude skill for turning travel emails and booking confirmations into one polished, shareable HTML itinerary with Apple Notes on iPhone as the primary retrieval workflow.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical instruction source. The sanitized [itinerary-template.html](assets/itinerary-template.html) file is the required output starting point. The packaged [trip-email-html-itinerary.skill](trip-email-html-itinerary.skill) file is the Claude-ready export built from both.

## Trigger

Use this skill when a user wants travel emails, booking confirmations, or reservation notes converted into a complete HTML itinerary.

Primary usage pattern: the generated `.html` file is dropped into Apple Notes for quick access while traveling.

Example prompts:

```text
Turn these trip emails into a shareable offline HTML itinerary.

Create a family travel handoff page from these hotel, flight, and rental car confirmations.

Build a full HTML trip document from these booking emails. Include contacts, day-by-day logistics, booking references, pending items, researched restaurant and activity suggestions for each destination, and redactions.
```

## What It Does

- Extracts flights, lodging, rental cars, events, travel admin, and pending items from email text.
- Researches current restaurant and activity suggestions for each overnight destination.
- Matches suggestions to the trip schedule, location, preferences, budget, and practical booking needs.
- Clearly separates suggestions from confirmed reservations and links to current sources.
- Preserves the established Europe & Morocco HTML format by placing suggestions inside the existing destination grids and reusing the current card and alert-strip components.
- Starts every itinerary from a sanitized reusable HTML template based on that format, with no personal trip data embedded.
- Adds a generation-stamped Today's Critical Details panel for the current or next travel day.
- Calculates practical travel time and buffers between scheduled locations and flags tight transitions.
- Reconciles confirmations, cancellations, updates, conflicts, and missing details.
- Redacts sensitive PINs, access codes, passwords, and payment details.
- Produces one complete HTML document using the established dark-theme itinerary design system.
- Prioritizes Apple Notes mobile readability with larger section and metadata labels for in-transit scanning.
- Renders major section titles at 18px on desktop and 19–20px on phone layouts so they are plainly recognizable.
- Uses the canonical destination timeline, alert strips, flights panel, day-by-day grid, booking references, checklist, admin grid, and footer sections.
- Structures the itinerary for both the traveler and family members who need quick reference information.
- Keeps output self-contained and Apple Notes friendly with static HTML/CSS and no JavaScript dependency.

## Output Structure

The generated HTML includes:

1. Hero with trip title, date range, route, badges, and destination palette
2. Destination timeline cards
3. Action items
4. Today's Critical Details
5. Flights
6. Destination sections with restaurant and activity suggestions
7. Day-by-day itinerary with travel-time lines
8. Booking references
9. Booking checklist
10. Travel admin
11. Footer

## Implement In Claude

1. Update `SKILL.md` first.
2. Keep `assets/itinerary-template.html` synchronized with structural or CSS changes.
3. Rebuild `trip-email-html-itinerary.skill` from the current source files and assets.
4. Import the `.skill` package into Claude using your normal Claude skills workflow.
5. Test with pasted booking emails and confirm the output uses the template, contains no unresolved placeholders, and remains one complete HTML document.

## Upgrade Log

See [upgrades.md](upgrades.md) for implemented upgrades and [future-upgrades.md](future-upgrades.md) for backlog ideas.
