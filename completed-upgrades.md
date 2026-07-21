# Completed Upgrades

Tracked summary of major completed repo upgrades and additions.

## 2026-07-21

- Added safe fictional public-demo generation and a validated ten-image social JPG carousel to `trip-email-html-itinerary`.
- Added accessibility enforcement, automated HTML validation, emergency replacement guidance, and a real offline emergency contacts output to `trip-email-html-itinerary`.
- Added verified plain-text offline addresses plus Apple Maps and Google Maps links throughout `trip-email-html-itinerary` so critical locations work both offline and online.
- Added static quick-navigation links below the `trip-email-html-itinerary` hero for rapid section access without JavaScript.
- Added categorized restaurant and activity recommendations, booking urgency labels, and daily pacing classifications to `trip-email-html-itinerary`.
- Added a current/next travel-day briefing panel and travel-time feasibility checks to `trip-email-html-itinerary`.
- Added a sanitized reusable HTML reference template to `trip-email-html-itinerary` and made it the required source layout for future generated itineraries.
- Increased major `trip-email-html-itinerary` section titles to 18–20px for clearer desktop and iPhone readability.
- Added current restaurant and activity research to `claude/skills/trip-email-html-itinerary`, with itinerary-fit rules, source links, clear separation between suggestions and confirmed reservations, and preservation of the established Europe & Morocco HTML format.

## 2026-06-29

- Replaced `claude/skills/trip-email-html-itinerary` with the v2.0.0 source skill and rebuilt the Claude import package.

## 2026-06-10

- Completed a Tier 1 backlog pass across all 34 Claude skills, shipping the high value items from each skill's local `future-upgrades.md` into `SKILL.md` and logging them in each skill's `upgrades.md` and `completedchanges.md`.
- Normalized `completedchanges.md` naming across the four skills that used `completed-changes.md`.
- Restored shortcut trigger phrases to skill descriptions and added missing version fields.
- Rebuilt all Claude `.skill` packages and passed `Validate-SkillQuality.ps1` and `Validate-SkillFolders.ps1`.

## 2026-05-22

- Normalized skill control sections across Claude, ChatGPT, Copilot, and Cursor skills using `skill-improvement-assessment.md` as the work queue.
- Added `claude/scripts/Validate-SkillQuality.ps1` to catch missing standard sections and stale Claude `.skill` packages.
- Converted ChatGPT `food-analyzer` from wrapper format into a standalone instruction skill.
- Rebuilt Claude `.skill` packages so exports match current source files.

## 2026-05-14

- Added `claude/skills/fitness-programming` to extend the repo fitness area beyond logging into structured planning.
