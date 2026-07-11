# MedVault Scheduling Engine

## Overview

The scheduling engine takes the active medication inventory and produces a practical daily dosing schedule. Each time slot includes the medication, the dose, and a plain-language explanation of why that timing is optimal. The engine also detects conflicts between medications that should not be taken at the same time or require separation.

---

## Time Blocks

The schedule is organized into six daily blocks:

| Block | Time Range | Typical Medications |
|---|---|---|
| Early Morning | Before 6:00 AM | Fasting labs prep, specialized regimens |
| Morning | 6:00 AM to 10:00 AM | Thyroid medications, corticosteroids, ADHD medications, blood pressure |
| Midday | 10:00 AM to 2:00 PM | Antibiotics (second daily dose), supplements that need food |
| Afternoon | 2:00 PM to 6:00 PM | Antibiotics (third daily dose), pain management |
| Evening | 6:00 PM to 10:00 PM | Statins, metformin (evening dose), blood pressure (second dose) |
| Bedtime | After 10:00 PM | Antihistamines, sleep aids, some antidepressants, anticholinergics |

---

## Timing Rules

### Morning Rules

| Medication / Class | Reason |
|---|---|
| Levothyroxine (thyroid) | Must be taken on an empty stomach, 30-60 minutes before food or other medications. Food and calcium block absorption significantly. |
| Corticosteroids (prednisone) | Mimics the natural morning cortisol surge. Taking at night suppresses the adrenal axis and worsens insomnia. |
| ADHD medications (amphetamines, methylphenidate) | Taken early to avoid insomnia. Effect lasts 4-12 hours depending on formulation. |
| ACE inhibitors and ARBs (blood pressure) | Morning dosing aligns with the natural blood pressure rise after waking. |
| Diuretics (furosemide, HCTZ) | Morning dosing prevents nocturia — frequent nighttime urination. |
| Bisphosphonates (alendronate, risedronate) | Must be taken first thing in the morning with a full glass of water, 30-60 minutes before food. Patient must remain upright to prevent esophageal irritation. |

### With Food Rules

| Medication / Class | Reason |
|---|---|
| Metformin | Food significantly reduces GI side effects (nausea, diarrhea). |
| NSAIDs (ibuprofen, naproxen) | Food reduces stomach irritation and risk of ulceration. |
| Iron supplements (when GI tolerability allows) | Food reduces nausea; however, note that food also reduces absorption by 33-50%. If GI tolerance is not a problem, take on an empty stomach for best absorption. |
| Most antibiotics | Reduces GI upset; check specific antibiotic as some require fasting. |
| Fat-soluble vitamins (A, D, E, K) | Fat in food is required for absorption. |
| Fish oil | Food reduces fishy burping. |
| Potassium | Reduces GI irritation. |

### Empty Stomach Rules

| Medication / Class | Reason |
|---|---|
| Levothyroxine | Food (especially calcium, iron, fiber) blocks absorption dramatically. |
| Bisphosphonates | Food halts absorption entirely. |
| Some antibiotics (azithromycin capsules, rifampin, ciprofloxacin) | Food reduces or delays absorption. |
| Enteric-coated medications | Food slows gastric emptying and can cause premature dissolution in stomach acid. |
| Omeprazole and other PPIs | Take 30-60 minutes before eating. Works best when proton pumps are active during meal-stimulated acid secretion. |

### Bedtime Rules

| Medication / Class | Reason |
|---|---|
| Statins (simvastatin, lovastatin, pravastatin) | Cholesterol synthesis peaks between midnight and 2 AM. Evening dosing maximizes inhibition. Note: atorvastatin and rosuvastatin have longer half-lives and can be taken any time. |
| Antihistamines (diphenhydramine, doxylamine) | Sedation is the primary side effect — make it work for sleep. |
| Alpha-blockers (terazosin, doxazosin) | First-dose hypotension risk makes bedtime dosing safer. |
| Tricyclic antidepressants (amitriptyline, nortriptyline) | Sedating effects are better tolerated at night. |
| Muscle relaxants (cyclobenzaprine) | Sedation is the primary effect; taken at night avoids daytime impairment. |
| Some antihypertensives | Bedtime dosing may better control nocturnal blood pressure in some patients (evidence-based, but physician should guide). |

### Avoid Before Exercise

| Medication / Class | Reason |
|---|---|
| Beta-blockers | Blunt heart rate response, limiting aerobic capacity. Time-to-peak effect is 1-2 hours; take after workouts when possible. |
| Diuretics | Increase dehydration risk during exercise. Take in morning after workouts. |
| Sedating medications | Obvious impairment of coordination and judgment during exercise. |
| Alpha-blockers | Exercise-induced vasodilation combined with alpha-blocker effect increases hypotension risk. |

### Separate by Time

| Pair | Separation Required | Reason |
|---|---|---|
| Levothyroxine + calcium or iron | 4 hours minimum | Calcium and iron both bind levothyroxine and block absorption |
| Fluoroquinolone antibiotics + calcium, iron, or magnesium | 2 hours before or 6 hours after antacid/mineral | Multivalent cations form insoluble chelates with fluoroquinolones |
| Tetracycline antibiotics + dairy or calcium | 2 hours | Same chelation mechanism |
| Bisphosphonates + any food, beverage except water, or other medication | 30-60 minutes | Absorption blocked by virtually everything |
| PPIs + clopidogrel | Separate by hours (omeprazole especially) | CYP2C19 competition reduces clopidogrel activation |

---

## Conflict Detection

The scheduling engine flags the following conflict types:

### Same-Time Conflicts

| Conflict Type | Example | Action |
|---|---|---|
| Absorption competition | Levothyroxine + calcium supplement both in morning | Separate levothyroxine to early morning, push calcium to midday |
| Combined sedation | Antihistamine + muscle relaxant scheduled at same time | Consolidate at bedtime, warn about additive sedation |
| Combined blood pressure lowering | ACE inhibitor + alpha-blocker at same time | Acceptable; note additive hypotension risk to user |
| Combined QT prolongation | Two QT-prolonging drugs at same time | Flag as Major conflict, recommend physician review |

### Timing Optimization Suggestions

When a conflict is detected, the engine provides a specific recommendation:

```
Conflict: Levothyroxine (scheduled: Morning) + Iron supplement (scheduled: Morning)

Problem: Iron chelates levothyroxine and blocks absorption by up to 50%.

Recommended fix:
  - Levothyroxine: move to Early Morning (30-60 min before food, 4+ hours before iron)
  - Iron supplement: keep in Morning slot (with food if GI tolerance requires)
```

---

## Output Format

The schedule output is a table organized by time block:

```
Daily Medication Schedule — 2026-05-15

Early Morning (before 6:00 AM)
  [none]

Morning (6:00 AM – 10:00 AM)
  Levothyroxine 50mcg         30 min before food, no calcium or iron within 4 hrs
  Lisinopril 10mg             With or without food; morning aligns with BP rise
  Metoprolol 25mg             Take after morning workout if exercising in AM

Midday (10:00 AM – 2:00 PM)
  Metformin 500mg             With lunch to reduce GI side effects
  Vitamin D3 2000 IU          With food (fat required for absorption)
  Calcium 500mg               With food; 4+ hours after levothyroxine

Afternoon (2:00 PM – 6:00 PM)
  [none]

Evening (6:00 PM – 10:00 PM)
  Metformin 500mg             With dinner
  Atorvastatin 20mg           Anytime (long half-life; evening is fine)

Bedtime (after 10:00 PM)
  Melatonin 3mg               30 min before target sleep time

Conflicts: 0 detected
Notes:
  - Grapefruit juice should be avoided with atorvastatin
  - Avoid alcohol with metformin (lactic acidosis risk)

---
MedVault is not medical advice. This schedule can be wrong or incomplete. Verify it with both your doctor and pharmacist.
```

---

## Reminder Export

The schedule can be exported in formats compatible with calendar and reminder systems:

| Format | Use |
|---|---|
| Plain text | Copy/paste into any app |
| iCal (.ics) | Import into Google Calendar, Apple Calendar, Outlook |
| JSON | Integration with custom apps or Home Assistant |
| Markdown | View in Obsidian, Notion, or any markdown reader |

Reminder export includes:
- Event title: medication name and dose
- Time: block start time (user can adjust)
- Notes: timing explanation
- Recurrence: daily

---

## Time Zone Handling

The schedule is generated in the user's local time zone. If the user travels across time zones:

- `mv schedule timezone [tz]` regenerates the schedule for the target time zone
- Medications with narrow therapeutic windows (warfarin, insulin, immunosuppressants) include a travel note: "Maintain consistent dosing intervals. If crossing more than 3 time zones, consult your physician about dose timing adjustment."
- Travel mode (planned feature) will automate time zone shift calculations.
