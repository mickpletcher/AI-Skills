# Upgrade Log: med-vault

Tracks implemented upgrades to this skill. Future upgrade ideas are in [future-upgrades.md](future-upgrades.md) (local only, not tracked in git).

| Date | Upgrade | Notes |
|------|---------|-------|
| 2026-06-10 | Added refill prediction | mv refill estimates days remaining, projects run-out dates, and flags refills needed now or soon. |
| 2026-06-10 | Added adherence tracking | mv take confirms doses and mv adherence reports rates, streaks, and missed dose patterns. |
| 2026-06-10 | Added side effect journal | mv journal logs timestamped observations and correlates them with medication timeline changes. |
| 2026-05-15 | Initial packaged release | Created the first packaged Claude import file `med-vault.skill`, added `assessment.md` with the current repo assessment, and added the repo standard tracking files. |
| 2026-05-15 | Travel medication mode | Added travel medication mode with country restriction guidance. |
| 2026-05-15 | Emergency card auto print | Added an emergency card auto print workflow. |
| 2026-05-15 | Expanded OCR support | Expanded OCR support for handwritten and faxed prescription material, updated supporting docs, and rebuilt `med-vault.skill`. |
| 2026-05-24 | Stronger medical warning language | Tightened every-response disclaimer language so users are told MedVault can be wrong or incomplete and must verify results with both a doctor and pharmacist. |
