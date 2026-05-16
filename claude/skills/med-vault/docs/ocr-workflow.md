# MedVault OCR Workflow

## Overview

The OCR workflow processes uploaded medication label images and extracts structured medication data. It is designed to handle real-world label conditions: partial occlusion, glare, shadows, curved bottle surfaces, and degraded print quality.

---

## Image Input Types

| Input Type | Expected Fields |
|---|---|
| Prescription bottle label | Name, dosage, frequency, doctor, pharmacy, Rx number, refill date, expiration |
| Supplement bottle label | Product name, serving size, ingredients, manufacturer, expiration |
| Blister pack label | Medication name, dosage, lot number, expiration |
| Pharmacy bag label | Medication name, patient name (do not store), instructions, pickup date |
| Medication insert | Ingredient list, dosage table (partial support — table parsing is best-effort) |

---

## Processing Pipeline

```
Image Upload
    │
    ▼
Image Quality Assessment
    │ ── [too dark / too blurry] ──► Notify user, ask for retake
    │
    ▼
Text Region Detection
    │
    ▼
OCR Extraction (field-by-field)
    │
    ▼
Confidence Scoring (per field)
    │
    ├── High confidence ──► Accept, include in confirmation table
    ├── Medium confidence ──► Flag with [?] in confirmation table
    └── Low confidence ──► Flag with [?], annotate with best guess in parentheses
    │
    ▼
Common Error Correction Pass
    │
    ▼
Normalization Pass (dates, units, drug names)
    │
    ▼
Confirmation Table Presented to User
    │
    ├── User confirms ──► Save to medications.json
    └── User corrects ──► Apply corrections, then save
    │
    ▼
Image Reference Stored (path to uploaded file)
    │
    ▼
Interaction Check Triggered
```

---

## Confidence Scoring

Each extracted field receives a confidence score:

| Level | Criteria | Behavior |
|---|---|---|
| High | Clean text, no ambiguous characters, matches known drug name pattern | Accept without flagging |
| Medium | 1-2 ambiguous characters, partial occlusion of field, unusual abbreviation | Flag with `[?]`, ask for confirmation |
| Low | Multiple ambiguous characters, significant blur or shadow, no pattern match | Flag with `[?]`, show best guess, require user input |
| Unreadable | Cannot extract any interpretable text from region | Ask user to type manually |

---

## Common OCR Errors and Corrections

### Character Substitutions

| OCR Output | Corrected To | Rule |
|---|---|---|
| `0` vs `O` | Contextual: in dosage numbers use `0`; in drug names use `O` | Numeric vs alpha context |
| `1` vs `l` vs `I` | Contextual: in dosage numbers use `1`; in drug names use `l` or `I` | Numeric vs alpha context |
| `5` vs `S` | Contextual: numbers in dosage fields, letters in name fields | Numeric vs alpha context |
| `rn` vs `m` | Check against known drug name list: `Warfarin` not `Warfarın` | Known drug name matching |
| `cl` vs `d` | Check against known drug name list: `clonidine` vs `clonidirie` | Known drug name matching |

### Unit Corrections

| OCR Output | Normalized To | Note |
|---|---|---|
| `mcg`, `ug`, `µg` | `mcg` | Micrograms standardized |
| `mEq` | `mEq` | Milliequivalents — verify context |
| `mg/ml`, `mg/mL` | `mg/mL` | Liquid concentration |
| `IU`, `iu` | `IU` | International Units |
| `%` | `%` | Topical concentrations |

### Drug Name Normalization

1. Strip trailing whitespace and OCR artifacts.
2. Check against RxNorm name list when available.
3. Apply Levenshtein distance matching for close matches (distance <= 2 for names > 8 characters, distance <= 1 for shorter names).
4. Flag matches with distance > 0 as medium confidence even if a match is found.

### Date Normalization

All dates are normalized to ISO 8601 format on save:

| Input Format | Normalized Output |
|---|---|
| `EXP 06/27` | `2027-06` |
| `Exp: Jun 2027` | `2027-06` |
| `06-27` | `2027-06` (expiration context) |
| `06/15/2027` | `2027-06-15` |
| `JUN 15 2027` | `2027-06-15` |

---

## Confirmation Table Format

After extraction, present a table before saving:

```
OCR Extraction Results — Please confirm or correct

Field                   Extracted Value         Confidence
──────────────────────────────────────────────────────────
Medication Name         Lisinopril              High
Brand Name              Zestril                 Medium [?]
Dosage                  10mg                    High
Frequency               Once daily              High
Prescribing Doctor      Dr. A. Johnson [?]      Medium
Pharmacy                CVS Pharmacy #4421      High
Rx Number               RX-8834291              High
Refill Date             2026-08-15              High
Expiration              2027-03 [?]             Medium
Instructions            Take by mouth           High

[?] = low or medium confidence — please verify these fields

Type corrections or press Enter to confirm as shown.
Patient name was detected but will NOT be saved unless you request it.
```

---

## Privacy Rules During OCR

- Patient name detected on prescription labels: display as detected, ask user whether to save. Default is NOT to save.
- Date of birth if present: do not extract or display.
- Insurance information: do not extract.
- Address: do not extract.
- Prescriber DEA number: do not extract or display.
- Image files: stored at the local path the user provided. MedVault stores a reference to the path, not the image content in the database.

---

## Failure Modes and Recovery

| Failure | Response |
|---|---|
| Image too dark | "The image is too dark to process. Try in better lighting or increase your phone's flash." |
| Image too blurry | "The image is blurry. Hold your camera steady and tap the label to focus before capturing." |
| Label at extreme angle | "The label appears to be at an angle. Try photographing it flat-on." |
| No text detected | "No readable text was found. This may not be a medication label, or the image quality is too low." |
| Only partial label visible | Extract what is visible. Mark all missing fields as unreadable. Ask user to fill in manually. |
| Multiple labels in one image | "Multiple labels detected. Please photograph one label at a time." |

---

## Supported Image Formats

- JPEG / JPG
- PNG
- HEIC (iPhone native — convert to JPEG before processing if conversion tools are available)
- PDF single-page (pharmacy printouts)

Minimum recommended resolution: 1200 x 900 pixels at the label region.
