# Upgrade Log: pihole-csv-analyzer

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md) (local only, not tracked in git).

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-06-10 | Added finding prioritization | High leverage items and likely false positives surface before harmless noise and the long tail. |
| 2026-06-10 | Added client grouping | Problem traffic traces to device types with per-client fixes when they beat global blocks. |
| 2026-06-10 | Added explicit action paths | Every recommendation is block, allow, investigate, or ignore with reasons. |
