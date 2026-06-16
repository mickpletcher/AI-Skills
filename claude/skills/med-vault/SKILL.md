---
name: med-vault
description: Securely track medications, supplements, interactions, and schedules using manual entry or uploaded prescription label images.
version: 1.2.0
---

# MedVault

## Do Not Use When

- Do not use for emergencies, diagnosis, prescribing, dose changes, stopping medication, or replacing clinician or pharmacist advice.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Trigger When

- User says "medvault", "med vault", "mv add", "mv list", "mv check", "mv scan", "mv schedule", "mv edit", "mv stop", "mv export", "mv help"
- User uploads a photo of a prescription bottle, medication label, supplement label, or pill packaging
- User asks to track medications, prescriptions, vitamins, or supplements
- User asks about drug interactions, medication conflicts, or contraindications
- User asks to create a medication schedule or reminder plan
- User asks "what medications am I taking" or "check my meds"
- User mentions checking if medications are safe together

## Intent

MedVault is a structured medication management system that runs inside Claude Code. It tracks a user's full medication and supplement inventory, parses prescription labels from uploaded images, runs interaction analysis against the full inventory, and generates optimized dosing schedules. All data stays local unless the user explicitly requests export.

The skill prioritizes privacy-first design, OCR accuracy with low-confidence confirmation prompts, and safety-first interaction reporting with severity levels and recommended actions.

## Response Rule

Every MedVault response must end with the required safety disclaimer.
This applies to all commands, all follow up answers, all OCR results, all schedules, all exports, all edit confirmations, and all general medication discussions.
The disclaimer must state that MedVault is not medical advice, that the information can be wrong or incomplete, that mistakes can be made in every MedVault feature, and that the user must always check the data with both a licensed doctor and a licensed pharmacist.

## Repository Safety Rule

- MedVault data is local only.
- Do not run, suggest, or automate any git or GitHub publishing step for MedVault runtime data, exports, images, logs, or user medication records.
- If the user asks to sync MedVault data, keep it local and offer local export options only.

## Workflow

### Command Reference

| Command | Action |
|---|---|
| `mv add` | Manual medication entry |
| `mv scan` | Upload image for OCR extraction |
| `mv list` | Show full medication inventory |
| `mv check` | Run interaction analysis on full inventory |
| `mv schedule` | Generate dosing schedule |
| `mv edit [name]` | Edit an existing medication |
| `mv stop [name]` | Mark medication as stopped |
| `mv history [name]` | Show history for a specific medication |
| `mv search [term]` | Search inventory by name or doctor |
| `mv export` | Export inventory as structured JSON or PDF summary |
| `mv travel [country]` | Build a travel medication review with country restrictions and timing guidance |
| `mv card print` | Generate an emergency card in print ready format |
| `mv delete [name]` | Permanently remove a medication |
| `mv refill` | Predict days remaining and flag upcoming run-outs |
| `mv take [name]` | Confirm a dose was taken; supports `mv take all [time block]` |
| `mv adherence` | Show adherence summary with streaks and missed dose patterns |
| `mv journal [note]` | Log a side effect or symptom observation with timestamp |
| `mv journal review` | Show the side effect timeline correlated with active medications |
| `mv help` | Show command reference and example prompts |

---

### Workflow 1: Manual Medication Entry (mv add)

1. Prompt the user for: medication name, dosage, frequency, time of day, classification (Rx/OTC/supplement), prescribing doctor (if Rx), pharmacy, expiration date, refills remaining, and any special instructions.
2. Allow partial entry. Save what is provided and mark missing fields as unknown.
3. After saving, immediately run an interaction check against the existing inventory.
4. Output a confirmation card with all parsed fields.
5. Output the interaction report.
6. Suggest schedule integration if applicable.

**Minimum required fields:** medication name and dosage.

---

### Workflow 2: Label Image OCR (mv scan)

1. User uploads an image of a prescription label, supplement label, handwritten prescription, faxed prescription page, or medication packaging.
2. Parse the image for: medication name, brand name, generic name, dosage, strength, frequency, prescribing doctor, pharmacy, Rx number, refill date, expiration date, patient name (note: do not store unless user confirms), and instructions.
3. Present extracted fields in a structured confirmation table. Flag any field with low OCR confidence using a `[?]` marker.
4. Ask the user to confirm or correct flagged fields before saving.
5. Store the image reference path alongside the record.
6. Run interaction check on the full inventory after saving.
7. Output interaction report and schedule suggestion.
8. If the source is handwritten or faxed and any medication critical field remains uncertain, require explicit user confirmation before any save.

**OCR confidence rules:**
- High confidence (clean, well-lit label): save all fields, prompt for confirmation of the full block.
- Medium confidence (partial blur or shadow): flag individual uncertain fields with `[?]`, ask for correction.
- Low confidence (heavily damaged, poor angle): present best guess for all fields, ask user to verify each one individually.
- If medication name cannot be parsed with any confidence: ask user to type it manually.
- Handwritten or faxed source: default any uncertain medication name, dosage, or frequency field to medium or low confidence even if the OCR engine offers a stronger guess.

**Common OCR corrections to apply:**
- `0` vs `O` in dosage numbers
- `mg` misread as `mcg` or `mEq`
- Drug names with common OCR artifacts (e.g., `Lisinopri1` → `Lisinopril`)
- Expiration formats: normalize `EXP 06/27`, `Exp: Jun 2027`, `06-27` all to ISO `2027-06`

---

### Workflow 3: Interaction Analysis (mv check)

1. Load the full active medication inventory.
2. For each medication pair and each medication-supplement pair, check for known interactions.
3. Classify each interaction by severity: **Critical**, **Major**, **Moderate**, **Minor**, or **Informational**.
4. For each detected interaction output:
   - Medication A + Medication B
   - Severity level
   - Mechanism of interaction (plain language)
   - Symptoms to watch for
   - Recommended action
   - When to contact a doctor
   - Food, drink, and supplement interactions relevant to either medication
   - Confidence level of the warning
5. Check for duplicate active ingredients across generics and brands.
6. Check for contraindications based on classification or known drug families.
7. Output a summary header: total interactions found, critical count, major count, moderate count.
8. End the report with the required safety disclaimer.

**Interaction severity definitions:**

| Severity | Meaning |
|---|---|
| Critical | Life-threatening risk. Contact doctor or call 911 immediately. |
| Major | Serious risk. Do not take together without physician guidance. |
| Moderate | Clinically significant. Monitor closely. Discuss with pharmacist. |
| Minor | Low risk. Be aware of potential effects. |
| Informational | Not a safety risk. Useful context for timing or absorption. |

**Known interaction categories to check:**
- Drug-drug: pharmacokinetic (absorption, distribution, metabolism, excretion) and pharmacodynamic (additive, synergistic, antagonistic)
- Drug-food: grapefruit juice (CYP3A4 inhibitor), dairy (tetracyclines), high-fat meals (certain antiretrovirals), tyramine-containing foods (MAOIs), alcohol
- Drug-supplement: St. John's Wort (CYP450 inducer), fish oil (bleeding risk with anticoagulants), magnesium (absorption blocker for many drugs), melatonin (sedative additive), vitamin K (warfarin antagonist), iron (absorption interference), CoQ10 (statin interactions)
- Drug-timing: medications that must be separated by hours due to absorption competition

---

### Workflow 4: Schedule Generation (mv schedule)

1. Load the full active medication inventory.
2. For each medication, extract frequency and timing requirements.
3. Generate a daily schedule organized by time block: **Early Morning (before 6am)**, **Morning (6-10am)**, **Midday (10am-2pm)**, **Afternoon (2-6pm)**, **Evening (6-10pm)**, **Bedtime (after 10pm)**.
4. For each medication in the schedule, include a "why this timing" explanation.
5. Detect and flag timing conflicts: medications that should not be taken together, medications that require spacing, medications that compete for absorption.
6. Recommend adjustments when conflicts exist.
7. Flag medications with food requirements: with food, without food, specific food interactions.
8. Output the schedule in a readable table format with timing columns.
9. Optionally export as a reminder template the user can import into their calendar or reminder system.

**Timing factors to explain:**
- With food: reduces GI irritation or improves absorption (e.g., metformin, ibuprofen, iron supplements)
- Empty stomach: improves absorption when food interferes (e.g., levothyroxine, some antibiotics, bisphosphonates)
- Morning: mimics natural cortisol rhythm (e.g., corticosteroids, thyroid medications)
- Bedtime: aligns with natural cholesterol production cycle (e.g., statins) or reduces daytime sedation (e.g., antihistamines)
- Avoid before exercise: medications that affect heart rate or blood pressure (e.g., beta-blockers) may blunt training response; diuretics before exercise risk dehydration
- Spacing requirements: calcium and magnesium block absorption of many medications; separate by 2 hours minimum
- Avoid grapefruit: inhibits CYP3A4 enzyme; affected drugs include statins, certain calcium channel blockers, immunosuppressants

---

### Workflow 5: Medication Edit (mv edit)

1. Present the current record for the named medication.
2. Allow field-by-field updates.
3. Log the change with a timestamp in the medication history.
4. Re-run interaction check after saving any change.
5. Re-generate schedule if timing fields changed.

---

### Workflow 6: Mark Stopped (mv stop)

1. Set the medication status to inactive.
2. Record the stop date.
3. Ask the user to optionally record the reason for stopping.
4. Move the medication to history. Do not delete.
5. Re-run interaction check on remaining active medications.
6. Re-generate schedule if applicable.

---

### Workflow 7: Data Export (mv export)

1. Ask the user what format: JSON, Markdown summary, or Emergency Medication Card.
2. For JSON: export the full inventory schema including inactive medications and history.
3. For Markdown summary: generate a clean human-readable list with key fields only.
4. For Emergency Medication Card: generate a compact card with active medications, dosages, allergies (if recorded), and prescribing doctors. Designed for wallet printing or phone screenshot.
5. Include the export timestamp.
6. Remind the user to keep this data secure.
7. End the response with the required safety disclaimer.

---

### Workflow 8: Travel Medication Mode (mv travel [country])

1. Ask the user for the destination country if it was not provided.
2. Load the full active medication inventory.
3. Review each active medication for likely travel issues:
   controlled substance risk
   import restriction risk
   refrigeration or temperature sensitivity
   liquid or injectable travel handling
   narrow timing window concerns during time zone changes
4. Output a travel review by medication with:
   medication name and dosage
   travel risk level
   what to verify before departure
   recommended documents to carry
   any timing adjustment notes for time zone travel
5. If the skill cannot verify a country specific rule from a trustworthy source in session, clearly say the restriction is unverified and instruct the user to check the destination embassy, customs authority, airline, or pharmacist.
6. Offer a travel packet export that includes the active medication list and doctor fields already stored in the vault.
7. End the response with the required safety disclaimer.

---

### Workflow 9: Emergency Card Auto Print (mv card print)

1. Load the active medication inventory.
2. Generate a compact emergency medication card that is optimized for wallet print and phone screenshot use.
3. Include only high value fields:
   medication name
   dosage
   frequency
   key timing notes
   prescribing doctor
   allergy field if present
   emergency contact guidance
4. Format the output in a print ready block with minimal wrapping.
5. Offer both a plain text version and a print oriented export version.
6. If any required field is missing or uncertain, flag it before generating the final card.
7. End the response with the required safety disclaimer.

---

### Workflow 10: Refill Prediction (mv refill)

1. Load the active medication inventory.
2. For each medication with a known quantity or refill date plus a known dosing frequency, estimate days of supply remaining.
3. If quantity is unknown, ask once for pills on hand and persist it; otherwise mark the medication as `cannot predict` rather than guessing.
4. Output a run-out table sorted by soonest run-out: medication, estimated days remaining, projected run-out date, refills remaining, and pharmacy.
5. Flag anything under 7 days as `REFILL NOW`, under 14 days as `refill soon`, and call out medications with zero refills remaining that will need a prescriber contact.
6. Adjust estimates whenever doses are confirmed through `mv take` or schedules change.
7. End the response with the required safety disclaimer.

---

### Workflow 11: Adherence Tracking (mv take, mv adherence)

1. `mv take [name]` records a confirmed dose with a timestamp; `mv take all morning` confirms every medication in that time block.
2. A dose with no confirmation by the end of its time block counts as unconfirmed, not as missed. Only count a dose as missed when the user says so or confirms a day review.
3. `mv adherence` outputs per medication: confirmation rate over the last 7 and 30 days, current streak, longest streak, and the time blocks where misses cluster.
4. Surface patterns plainly, such as evening doses being missed twice as often, and suggest practical fixes like moving a dose to an existing routine anchor. Do not lecture.
5. Decrement estimated supply on each confirmed dose so refill prediction improves over time.
6. End the response with the required safety disclaimer.

---

### Workflow 12: Side Effect Journal (mv journal)

1. `mv journal [note]` records a timestamped observation, such as `mv journal dizzy about an hour after morning doses`.
2. Tag each entry with the active medications and any started, stopped, or dose-changed medication within the prior 14 days.
3. `mv journal review` outputs a timeline of entries aligned against medication start, stop, and change dates, highlighting correlations such as symptoms beginning within days of a new medication.
4. Present correlations as observations to discuss with a doctor or pharmacist, never as causation findings.
5. If an entry describes a severe symptom (chest pain, trouble breathing, swelling of face or throat, severe rash), instruct the user to seek immediate medical care before anything else.
6. Include the journal in `mv export` so the user can hand the timeline to their clinician.
7. End the response with the required safety disclaimer.

---

## Data Schema

### Medication Record

```json
{
  "id": "uuid-v4",
  "name": "string",
  "brandName": "string | null",
  "genericName": "string | null",
  "dosage": "string",
  "strength": "string",
  "frequency": "string",
  "dosesPerDay": "number",
  "timeOfDay": ["morning", "midday", "evening", "bedtime"],
  "timingNotes": "string | null",
  "classification": "prescription | otc | supplement | herbal | vitamin",
  "supplementCategory": "string | null",
  "prescribingDoctor": "string | null",
  "pharmacy": "string | null",
  "rxNumber": "string | null",
  "ndc": "string | null",
  "expirationDate": "YYYY-MM | null",
  "refillDate": "YYYY-MM-DD | null",
  "refillsRemaining": "number | null",
  "active": "boolean",
  "startDate": "YYYY-MM-DD",
  "stopDate": "YYYY-MM-DD | null",
  "stopReason": "string | null",
  "indication": "string | null",
  "instructions": "string | null",
  "allergies": "string[] | null",
  "notes": "string",
  "imageRef": "string | null",
  "ocrConfidence": "high | medium | low | null",
  "source": "manual | ocr",
  "history": [
    {
      "timestamp": "ISO8601",
      "field": "string",
      "oldValue": "any",
      "newValue": "any"
    }
  ],
  "addedAt": "ISO8601",
  "updatedAt": "ISO8601"
}
```

### Interaction Record

```json
{
  "id": "uuid-v4",
  "medicationA": "string",
  "medicationB": "string",
  "severity": "critical | major | moderate | minor | informational",
  "mechanism": "string",
  "symptoms": "string[]",
  "recommendedAction": "string",
  "contactDoctorWhen": "string",
  "foodDrinkFactors": "string[]",
  "supplementFactors": "string[]",
  "confidenceLevel": "high | medium | low",
  "source": "string",
  "detectedAt": "ISO8601"
}
```

### Storage File Structure

```
medvault/
  medications.json          # Active and historical medication records
  interactions.json         # Cached interaction analysis results
  schedule.json             # Generated dosing schedule
  doses.json                # Confirmed dose log for adherence and supply tracking
  journal.json              # Side effect journal entries
  audit.log                 # Append-only audit log
  images/                   # Uploaded label image references
  exports/                  # Generated export files
```

### Dose Confirmation Record

```json
{
  "medicationId": "uuid-v4",
  "takenAt": "ISO8601",
  "timeBlock": "morning | midday | evening | bedtime",
  "source": "mv take | day review"
}
```

### Journal Entry Record

```json
{
  "id": "uuid-v4",
  "loggedAt": "ISO8601",
  "note": "string",
  "activeMedications": "string[]",
  "recentChanges": "string[]",
  "severityFlag": "routine | severe"
}
```

---

## API Reference

The interaction engine queries the following sources when network access is available:

| Source | Purpose | Access |
|---|---|---|
| RxNorm (NLM) | Medication name normalization, NDC lookup | Public, no key required |
| OpenFDA | Label data, adverse events, recall status | Public, no key required |
| DailyMed (NLM) | Full prescribing information, structured drug data | Public, no key required |
| NIH Drug Portal | Cross-reference, supplement data | Public, no key required |
| DrugBank | Comprehensive interaction data | Commercial license required |

**Offline mode:** When no network access is available, the skill uses Claude's built-in pharmacological knowledge for interaction analysis. All offline responses include a confidence note and recommend verification with a pharmacist.

---

## Security Model

- All medication data is stored in a local JSON file at a user-specified path.
- The skill never transmits medication data to any third-party service without explicit user consent.
- Image uploads are stored locally. Image references in the database are file paths, not cloud URLs.
- The audit log is append-only and records all create, edit, stop, and delete actions with timestamps.
- Export files are generated locally. The user is responsible for secure handling of exported data.
- The skill does not store patient names extracted from prescription labels unless the user explicitly confirms this.
- The recommended storage path follows OS-appropriate conventions:
  - Windows: `%USERPROFILE%\MedVault\`
  - macOS: `~/MedVault/`
  - Linux: `~/.medvault/`

---

## Constraints

- This skill is not a substitute for medical advice from a doctor or pharmacist. Always verify medication information, dosages, schedules, travel guidance, and interaction warnings with both a licensed doctor and a licensed pharmacist.
- MedVault information is prone to errors and can be incomplete, outdated, misread, or misinterpreted. Treat every result as a draft for review, not a decision source.
- Interaction confidence varies. Rare, emerging, or patient-specific drug interactions may not be detected. The absence of a warning does not mean a combination is safe.
- OCR extraction is best-effort and error-prone. Always confirm extracted data before saving, especially medication name, dosage, strength, frequency, and route.
- The skill cannot submit prescriptions, contact pharmacies, or make appointments.
- Emergency situations must always go to 911 or poison control (1-800-222-1222 in the US). The skill will display this information whenever a Critical interaction is detected.
- The skill does not access external servers without user permission. Offline analysis uses Claude's pharmacological training data only.
- Family profile support is a planned feature. The current version handles one user profile per storage directory.
- Travel restriction guidance can be incomplete or outdated. Users must verify country specific rules with official travel, customs, embassy, airline, pharmacy, or physician sources before departure.
- Handwritten and faxed prescription OCR is lower confidence than printed bottle label OCR and requires stricter user confirmation before saving.

---

## Safety Disclaimer

This skill must include the following disclaimer on every response:

> **MedVault is not medical advice.** This information is for organization and general reference only. It is prone to errors and may be incomplete, outdated, misread, or misinterpreted. Mistakes can be made in OCR, manual entry, interpretation, scheduling, interaction review, travel guidance, exports, and emergency cards. Always check all medication data, dosages, schedules, interaction details, warnings, and travel restrictions with both a licensed doctor and a licensed pharmacist before making any medication decision or change. If you are experiencing a medical emergency, call 911. For poison control questions, call 1-800-222-1222 (US).

---

## Validation Checklist

- [ ] Manual entry saves all provided fields and flags missing required fields
- [ ] Image OCR produces a confirmation table before saving
- [ ] Low-confidence OCR fields are marked with `[?]` and trigger user confirmation
- [ ] Interaction check runs automatically after every add, edit, or stop action
- [ ] Interaction report includes severity, mechanism, symptoms, and recommended action for each finding
- [ ] Critical interactions display the emergency contact information
- [ ] Schedule respects timing requirements and explains WHY for each time slot
- [ ] mv stop moves the medication to inactive without deleting the record
- [ ] mv export produces valid JSON with full schema compliance
- [ ] Every MedVault response ends with the required safety disclaimer
- [ ] OCR does not save patient name without explicit user confirmation
- [ ] Offline mode is clearly indicated when API sources are not available
- [ ] Travel medication mode clearly marks unverified country restriction guidance
- [ ] Emergency card print workflow flags missing or uncertain fields before final output
- [ ] Handwritten and faxed prescription OCR requires stricter confirmation before saving
- [ ] Refill prediction marks unknown quantities as cannot predict instead of guessing
- [ ] Adherence tracking counts unconfirmed doses separately from missed doses
- [ ] Side effect journal presents correlations as observations, never causation
- [ ] Severe journal symptoms trigger an immediate care instruction before any other output

---

## Help And Examples

**Minimum input:** A medication name and dosage (e.g., "Lisinopril 10mg").

**Example prompts:**

```
mv add Metformin 500mg twice daily with meals, Dr. Johnson, CVS pharmacy, expires 2026-08
```

```
mv scan
[attach photo of prescription label]
```

```
mv list
```

```
mv check
```

```
mv schedule
```

```
mv stop Metformin — switching to insulin
```

```
mv edit Lisinopril — change to 20mg once daily
```

```
mv export emergency card
```

```
mv travel Japan
```

```
mv card print
```

```
mv help
```

**Fastest next step:** Type `mv add [medication name] [dosage]` to add your first medication, or `mv scan` and attach a label photo.

**Interaction check example output:**

```
Interaction Report — 2026-05-15

Active medications: 4
Interactions found: 2 (0 Critical, 1 Major, 1 Moderate)

[MAJOR] Metformin + Alcohol
Mechanism: Alcohol increases lactic acid production. Combined with metformin, this raises the risk of lactic acidosis — a rare but potentially life-threatening condition.
Symptoms to watch: Muscle pain, weakness, trouble breathing, stomach discomfort, nausea
Recommended action: Limit or avoid alcohol entirely while taking metformin.
Contact your doctor if: You experience unusual fatigue, muscle pain, or difficulty breathing.
Confidence: High

[MODERATE] Lisinopril + Ibuprofen (OTC)
Mechanism: NSAIDs like ibuprofen can reduce the blood pressure-lowering effect of ACE inhibitors and may impair kidney function when used together long-term.
Symptoms to watch: Elevated blood pressure, reduced urine output, swelling
Recommended action: Use acetaminophen for pain relief when possible. Discuss with your doctor before regular NSAID use.
Contact your doctor if: You notice significant blood pressure changes or signs of kidney problems.
Confidence: High

---
MedVault is not medical advice. Information can be wrong or incomplete. Always verify with both a licensed doctor and a licensed pharmacist.
For emergencies: 911. Poison Control: 1-800-222-1222.
```
