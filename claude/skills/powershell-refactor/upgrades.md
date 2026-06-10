# Upgrade Log: powershell-refactor

Tracks implemented upgrades to this skill. Future upgrade ideas are in `future-upgrades.md` which stays local only and is not tracked in git.

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-06-10 | Added refactor scope presets | Naming only, deduplication only, and full cleanup control how aggressive the pass is. |
| 2026-06-10 | Added PSScriptAnalyzer alignment pass | Violations are measured before and after, fixed in scope, and never newly introduced. |
| 2026-06-10 | Added change summary output | Every refactor ends with a behavior, line count, and change list summary. |
| 2026-05-14 | Initial skill add | Added Claude source, wrapper README, and packaged export for focused PowerShell refactoring |
