# Upgrade Log: photo-rename

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md) (local only, not tracked in git).

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-05-13 | Added stronger filename ordering rules | Keeps date, location, event, and subject ordering more consistent |
| 2026-05-13 | Added confidence handling | Separates clear identifications from partial or low-confidence guesses |
| 2026-05-13 | Added collision-safe rename behavior | Appends stable suffixes when duplicate names would otherwise collide |
| 2026-05-13 | Added batch review mode | Groups similar photos and applies more consistent naming across a set |
| 2026-05-13 | Added GPS fallback improvements | Handles missing or obviously wrong GPS metadata more safely |
| 2026-05-13 | Added export report guidance | Reports old names, new names, and confidence reasons clearly |
