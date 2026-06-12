# Upgrade Log: github-social-preview

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md) (local only, not tracked in git).

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-06-10 | Added language-based accent selection | Previews derive their accent from the repo language unless a theme or brand color is given. |
| 2026-06-10 | Added layout variants | Docs repos, apps, and libraries get different visual emphasis. |
| 2026-06-10 | Added batch mode | Multiple repo URLs produce a themed family of previews with per-repo filenames and a summary table. |
| 2026-05-13 | Added theme preset support | The generator now supports theme presets beyond GitHub dark so previews can better match repo brand and project style. |
| 2026-05-13 | Added smarter text fitting | The generator now fits and truncates long repo names, descriptions, and topic tags more cleanly. |
| 2026-05-13 | Added local preview checklist | The generator now reports contrast, crop safety, and file size checks before final export. |
| 2026-05-13 | Added dynamic asset support | The generator now supports optional logo, screenshot, and custom background art assets when available. |
