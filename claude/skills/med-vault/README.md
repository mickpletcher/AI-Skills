# MedVault

Track medications, supplements, interactions, and dosing schedules. Supports manual entry and photo uploads of prescription and supplement labels.

---

## What It Does

- Adds medications manually or by scanning prescription/supplement label photos via OCR
- Supports expanded OCR review for handwritten and faxed prescription material
- Maintains a local structured medication inventory with full edit history
- Runs drug-drug, drug-supplement, drug-food, and drug-drink interaction analysis
- Generates optimized daily dosing schedules with timing explanations
- Exports data as JSON, Markdown summaries, or Emergency Medication Cards
- Adds travel medication reviews with country restriction guidance
- Generates a print ready emergency card workflow
- Keeps all data local by default — no cloud transmission without explicit consent

---

## Installation

1. Use the packaged skill file if you want the Claude import artifact:

`med-vault.skill`

2. If you manage skills manually, use this folder as the source of truth and keep `SKILL.md` with the supporting docs.

**Windows:**
```
%USERPROFILE%\OneDrive\Documents\Claude\Skills\
```

**macOS / Linux:**
```
~/Documents/Claude/Skills/
```

3. Restart Claude Code or reload skills.

4. Create the MedVault data directory if you are implementing the local vault workflow described by the skill:

**Windows:** `%USERPROFILE%\MedVault\`
**macOS / Linux:** `~/MedVault/`

---

## Quick Start

```
mv add Lisinopril 10mg once daily, Dr. Smith, Walgreens, expires 2027-03
```

```
mv scan
[attach a photo of a prescription bottle label]
```

```
mv check
```

```
mv schedule
```

```
mv help
```

```
mv travel Canada
```

```
mv card print
```

---

## Commands

| Command | Description |
|---|---|
| `mv add` | Manually add a medication or supplement |
| `mv scan` | Upload a label photo for OCR extraction |
| `mv list` | Show all medications in your inventory |
| `mv check` | Run full interaction analysis |
| `mv schedule` | Generate a daily dosing schedule |
| `mv edit [name]` | Edit an existing medication record |
| `mv stop [name]` | Mark a medication as stopped (keeps history) |
| `mv history [name]` | View change history for one medication |
| `mv search [term]` | Search by name, doctor, or pharmacy |
| `mv export` | Export as JSON, Markdown, or Emergency Card |
| `mv travel [country]` | Review travel issues, country restrictions, and time zone notes |
| `mv card print` | Generate a print ready emergency card |
| `mv delete [name]` | Permanently delete a medication record |
| `mv help` | Show command reference |

---

## OCR Label Scanning

Supports prescription bottles, supplement labels, blister packs, pharmacy bag labels, handwritten prescriptions, and faxed prescription pages.

Low-confidence fields are marked `[?]` and require user confirmation before saving. Patient name is detected but never saved without explicit user request.

---

## Interaction Analysis

Checks drug-drug, drug-supplement, drug-food, and drug-drink interactions. Severity levels: Critical, Major, Moderate, Minor, Informational. Every report includes mechanism, symptoms, recommended action, and when to contact a doctor.

API sources when online: RxNorm, OpenFDA, DailyMed. Offline mode uses Claude's pharmacological training data (labeled and lower confidence).

---

## Data Storage

```
MedVault/
  medications.json
  interactions.json
  schedule.json
  audit.log
  images/
  exports/
```

All data is local. Audit log is append-only. Images are renamed to UUIDs on import.
Do not push MedVault runtime data or exports to any GitHub repository.

---

## Travel Medication Mode

`mv travel [country]` reviews the active medication list for likely travel issues such as controlled substance concerns, import restrictions, refrigeration needs, injectable handling, and time zone timing changes.

If a country specific rule cannot be verified in session, the skill should say that clearly and tell the user to verify it with official sources before travel.

---

## Emergency Card Print

`mv card print` generates a compact emergency medication card for wallet print and phone screenshot use. Missing or uncertain fields should be flagged before the final card is produced.

---

## Safety Notice

MedVault is not medical advice. This information is for organization and general reference only. It is prone to errors and may be incomplete, outdated, misread, or misinterpreted. Mistakes can be made in OCR, manual entry, interpretation, scheduling, interaction review, travel guidance, exports, and emergency cards. Always check medications, dosages, schedules, interaction details, warnings, and travel restrictions with both a licensed doctor and a licensed pharmacist before making any medication decision or change.

For emergencies: **911**
Poison Control: **1-800-222-1222**

Every MedVault response must display this safety notice.

---

## Documentation

| File | Contents |
|---|---|
| `SKILL.md` | Full skill definition, workflows, schemas, validation |
| `med-vault.skill` | Packaged Claude import artifact |
| `upgrades.md` | Upgrade log of changes made to this skill |
| `completedchanges.md` | Changes that have been completed and shipped |
| `future-upgrades.md` | Local only list of planned upgrades |
| `docs/ocr-workflow.md` | OCR pipeline, confidence scoring, error correction |
| `docs/interaction-engine.md` | Interaction categories, severity, report structure |
| `docs/security-model.md` | Privacy rules, audit log, encryption roadmap |
| `docs/api-layer.md` | API provider interface, sources, fallback chain |
| `docs/scheduling.md` | Timing rules, conflict detection, schedule format |
| `docs/schemas.md` | Full JSON schemas for all data types |
| `docs/examples.md` | Example prompts and workflow walkthroughs |
| `docs/roadmap.md` | Planned upgrades through v3.0 |

`future-upgrades.md` is local only and should not be pushed to the repo.

---

## Version

1.1.1 - 2026-05-24
