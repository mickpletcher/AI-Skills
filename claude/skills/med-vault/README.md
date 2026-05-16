# MedVault

Track medications, supplements, interactions, and dosing schedules. Supports manual entry and photo uploads of prescription and supplement labels.

---

## What It Does

- Adds medications manually or by scanning prescription/supplement label photos via OCR
- Maintains a local structured medication inventory with full edit history
- Runs drug-drug, drug-supplement, drug-food, and drug-drink interaction analysis
- Generates optimized daily dosing schedules with timing explanations
- Exports data as JSON, Markdown summaries, or Emergency Medication Cards
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
| `mv delete [name]` | Permanently delete a medication record |
| `mv help` | Show command reference |

---

## OCR Label Scanning

Supports prescription bottles, supplement labels, blister packs, and pharmacy bag labels.

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

---

## Safety Notice

MedVault is not medical advice. Mistakes can be made in OCR, interpretation, scheduling, and interaction review. Always check medications, dosages, schedules, and interaction details with a licensed pharmacist or physician.

For emergencies: **911**
Poison Control: **1-800-222-1222**

Every MedVault response should display this safety notice.

---

## Documentation

| File | Contents |
|---|---|
| `SKILL.md` | Full skill definition, workflows, schemas, validation |
| `med-vault.skill` | Packaged Claude import artifact |
| `changelog.md` | Dated log of changes made to this skill |
| `completed-upgrades.md` | Upgrades that have been completed and shipped |
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

1.0.0 — 2026-05-15
