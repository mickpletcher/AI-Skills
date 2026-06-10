# Upgrade Log: alpaca-trading

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md) (local only, not tracked in git).

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-06-10 | Added Alpaca capability profile | Repo advice now accounts for paper fill optimism, fractional limits, bracket amend limits, crypto rules, IEX data, and PDT. |
| 2026-06-10 | Added order lifecycle checklist | Entry, open orders, partial fills, exits, cancel replace, and failure paths are validated before order changes ship. |
| 2026-06-10 | Added regression test matrix | Common trading changes map to the exact Python and PowerShell test passes to run. |
