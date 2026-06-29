# Completed Upgrades

Tracked summary of major completed repo upgrades and additions.

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
