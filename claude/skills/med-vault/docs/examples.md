# MedVault Example Prompts and Workflows

## Manual Entry Examples

### Simple entry

```
mv add Metformin 500mg twice daily
```

Claude response: Saves the record with dosage and frequency. Prompts for optional fields: prescribing doctor, pharmacy, expiration date, indication.

---

### Full entry in one line

```
mv add Lisinopril 10mg once daily, Dr. Sarah Johnson, CVS Pharmacy, expires 2027-06, blood pressure management
```

Claude response: Parses all fields from the single line. Presents a confirmation card. Runs interaction check against existing inventory. Reports any findings.

---

### Supplement entry

```
mv add Vitamin D3 2000 IU daily supplement, Nature Made
```

Claude response: Classifies as supplement. Saves manufacturer as pharmacy equivalent. Notes fat-soluble, take with food. Runs interaction check.

---

### OTC medication

```
mv add Ibuprofen 400mg as needed, OTC, for headaches
```

Claude response: Classifies as OTC. Notes indication. Immediately flags interaction if user is on NSAIDs or anticoagulants. Adds to inventory in inactive-on-demand state with note.

---

## OCR Scan Workflows

### Clean label

**User:** `mv scan` [attaches clear photo of prescription bottle]

**Claude:**
```
OCR Extraction Results — Please confirm or correct

Field                   Extracted Value                 Confidence
──────────────────────────────────────────────────────────────────
Medication Name         Atorvastatin                    High
Brand Name              Lipitor                         High
Dosage                  20mg                            High
Frequency               Once daily                      High
Prescribing Doctor      Dr. Michael Chen                High
Pharmacy                Walgreens #2218                 High
Rx Number               RX-7741209                      High
Refill Date             2026-07-22                      High
Expiration              2027-04                         High
Instructions            Take by mouth at bedtime        High

All fields extracted with high confidence.
Patient name was detected but will NOT be saved unless you request it.

Type any corrections, or press Enter to save as shown.
```

---

### Partially obscured label

**User:** `mv scan` [attaches photo where expiration date is partially covered by a sticker]

**Claude:**
```
OCR Extraction Results — Please confirm or correct

Field                   Extracted Value                 Confidence
──────────────────────────────────────────────────────────────────
Medication Name         Metoprolol Succinate            High
Brand Name              Toprol-XL                       High
Dosage                  25mg                            High
Frequency               Once daily                      High
Prescribing Doctor      Dr. A. Johnson [?]              Medium
Pharmacy                CVS Pharmacy                    High
Rx Number               RX-5589021                      High
Refill Date             2026-09 [?]                     Medium
Expiration              [unreadable — please type]      Low
Instructions            Take with or without food        High

Fields marked [?] need confirmation. Expiration date could not be read.

Please type: 1) corrected doctor name (or Enter to keep), 2) refill date (or Enter to keep), 3) expiration date.
```

---

### Low quality image

**User:** `mv scan` [attaches blurry, low-light photo]

**Claude:**
```
Image quality is too low for reliable extraction. Several fields are unreadable.

Best guesses (verify all of these):

Field                   Best Guess                      Confidence
──────────────────────────────────────────────────────────────────
Medication Name         Warfarin [?]                    Low
Dosage                  5mg [?]                         Low
Frequency               Once daily [?]                  Low
All other fields        [unreadable]                    Unreadable

This medication appears to be a blood thinner. Accurate information is especially important here.

Options:
1. Type the correct values manually for the low-confidence fields
2. Retake the photo with better lighting (tap the label to focus)
3. Start a manual entry instead: mv add [name] [dosage]
```

---

## Interaction Check Examples

### No interactions found

```
mv check
```

```
Interaction Report — 2026-05-15
Active medications: 3 (Vitamin D3, Fish Oil, Magnesium)

No drug-drug interactions detected.
No drug-supplement interactions detected.

Food and drink notes:
  - Vitamin D3: take with food (fat improves absorption)
  - Fish oil: take with food (reduces fishy burping)
  - Magnesium glycinate: take with food or without food; evening timing may support sleep

---
MedVault is not medical advice. Information can be wrong or incomplete. Verify with both your doctor and pharmacist.
For emergencies: 911. Poison Control: 1-800-222-1222.
```

---

### Critical interaction detected

```
mv check
```

```
Interaction Report — 2026-05-15
Active medications: 5
Interactions found: 3 (1 Critical, 1 Major, 1 Informational)

[CRITICAL] Phenelzine + Tramadol
Mechanism: Both drugs raise serotonin levels. MAO inhibitors prevent serotonin breakdown while
tramadol is a weak serotonin reuptake inhibitor. Combined, this can cause serotonin syndrome —
a potentially life-threatening condition.
Symptoms to watch for: Agitation, confusion, rapid heart rate, high blood pressure, dilated pupils,
muscle twitching, muscle rigidity, diarrhea, fever
Recommended action: Do NOT take these medications together. Contact your prescribing physician
immediately. This combination is contraindicated.
Contact your doctor if: You have already taken both — seek emergency care now.
Confidence: High | Source: FDA prescribing label (DailyMed)

EMERGENCY: If you are experiencing symptoms — call 911 immediately.
Poison Control: 1-800-222-1222

...
```

---

## Schedule Examples

### Basic schedule request

```
mv schedule
```

Output: Full daily schedule with time blocks, timing reasons, food requirements, conflict flags, and global notes. See `docs/scheduling.md` for full output format.

---

### Time zone adjusted schedule

```
mv schedule timezone America/Chicago
```

Output: Schedule regenerated with Central time labels. All time blocks adjusted. Narrow-window medications flagged with travel note if timezone differs from saved default.

---

## Edit and Stop Examples

### Edit a dosage

```
mv edit Lisinopril — dosage changed to 20mg, Dr. Johnson increased it at my last visit
```

Claude response: Updates dosage field. Logs the change in history with timestamp. Re-runs interaction check. Re-generates schedule if timing was affected.

---

### Stop a medication

```
mv stop Metformin — switching to Ozempic as of today
```

Claude response: Sets active to false. Records stop date as today. Records stop reason. Removes from active interaction check. Re-runs interaction check on remaining active medications. Confirms Metformin is now in history only.

---

## Search and List Examples

### List all active medications

```
mv list
```

Output: Table of all active medications with name, dosage, frequency, prescribing doctor, and expiration date. Count of inactive medications shown with link to view history.

---

### List including stopped medications

```
mv list all
```

Output: Active medications, then inactive medications, each with stop date and reason.

---

### Search by doctor

```
mv search Dr. Johnson
```

Output: All medications prescribed by Dr. Johnson, active and inactive.

---

### Search by medication name

```
mv search statin
```

Output: All medications whose name or drug class matches the search term.

---

## Export Examples

### Emergency card

```
mv export emergency card
```

Output: Compact plain text card with active medications, dosages, doctors, pharmacy, and emergency contacts. Saved to `MedVault/exports/`. User is reminded to keep it secure.

---

### Full JSON export

```
mv export json
```

Output: Full export to `MedVault/exports/[timestamp]-full.json`. Includes all records, history, interaction cache, and schedule.

---

### Markdown summary

```
mv export markdown
```

Output: Human-readable medication list in Markdown format. Suitable for pasting into a medical intake form or Obsidian note.

---

## Help

```
mv help
```

Output: Full command reference table, example prompts, fastest-start guidance, and a link to the skill documentation files.
