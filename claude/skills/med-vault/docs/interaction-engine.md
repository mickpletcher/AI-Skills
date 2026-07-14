# MedVault Interaction Engine

## Overview

The interaction engine compares every medication and supplement in the active inventory against every other entry to detect drug-drug, drug-supplement, drug-food, and drug-drink interactions. It runs automatically after every add, edit, or stop action, and is also available on demand via `mv check`.

---

## Interaction Categories

### Drug-Drug Interactions

Comparisons between any two prescription or OTC medications.

**Pharmacokinetic interactions** (how the body processes a drug):

| Mechanism | Description | Example |
|---|---|---|
| CYP450 inhibition | Drug A slows the metabolism of Drug B, raising Drug B's blood level | Fluconazole + warfarin |
| CYP450 induction | Drug A speeds up Drug B's metabolism, lowering Drug B's effectiveness | Rifampin + birth control pills |
| P-glycoprotein effects | Transporter protein affects drug absorption or elimination | Amiodarone + digoxin |
| Protein binding displacement | Drug A displaces Drug B from plasma proteins, increasing Drug B's free concentration | Aspirin + warfarin (high doses) |
| Renal clearance | Drug A reduces kidney excretion of Drug B | NSAIDs + lithium |

**Pharmacodynamic interactions** (how the drugs affect the body):

| Mechanism | Description | Example |
|---|---|---|
| Additive | Both drugs produce the same effect; combined effect is sum of individual effects | Two sedatives |
| Synergistic | Combined effect exceeds the sum of individual effects | Alcohol + benzodiazepine |
| Antagonistic | Drug A reduces the effect of Drug B | Beta-blockers + epinephrine |
| QT prolongation | Both drugs extend the cardiac QT interval, raising risk of arrhythmia | Azithromycin + haloperidol |
| Serotonin syndrome | Both drugs raise serotonin levels, potentially causing toxic serotonin accumulation | SSRIs + tramadol |
| Additive bleeding risk | Both drugs inhibit clotting or platelet function | Warfarin + aspirin |
| Additive hypotension | Both drugs lower blood pressure | ACE inhibitor + diuretic (moderate) |
| Additive sedation | Both drugs cause CNS depression | Opioids + benzodiazepines |
| Additive nephrotoxicity | Both drugs stress kidney function | NSAIDs + aminoglycosides |

---

### Drug-Supplement Interactions

Comparisons between any medication and any vitamin, mineral, herbal, or supplement.

| Supplement | Interaction Mechanism | Affected Drug Classes |
|---|---|---|
| St. John's Wort | CYP3A4 and P-glycoprotein inducer — reduces blood levels of many drugs | SSRIs, birth control, antiretrovirals, cyclosporine, warfarin, statins |
| Fish oil / Omega-3 | Antiplatelet effect at high doses | Anticoagulants, antiplatelet agents |
| Vitamin K | Antagonizes warfarin effect; sudden changes in dietary K alter INR | Warfarin, acenocoumarol |
| Iron | Chelates tetracyclines, fluoroquinolones, levothyroxine — reduces absorption | Antibiotics, thyroid medications |
| Calcium | Chelates tetracyclines, fluoroquinolones, bisphosphonates, levothyroxine | Antibiotics, osteoporosis drugs, thyroid |
| Magnesium | Reduces absorption of fluoroquinolones, tetracyclines | Antibiotics |
| Melatonin | Additive sedation | Benzodiazepines, opioids, antidepressants, antihistamines |
| Ginkgo biloba | Antiplatelet, potential CYP interactions | Anticoagulants, antiplatelet agents, anticonvulsants |
| Ginseng | May alter blood glucose and blood pressure | Antidiabetics, antihypertensives, anticoagulants |
| Valerian | Additive CNS depression | Sedatives, benzodiazepines, opioids |
| CoQ10 | May reduce warfarin effectiveness; may lower blood pressure | Warfarin, antihypertensives |
| Garlic (high dose) | Antiplatelet; CYP2E1 interactions | Anticoagulants, HIV protease inhibitors |
| Echinacea | CYP3A4 and CYP1A2 interactions | Immunosuppressants, some hepatic drugs |
| Kava | Additive hepatotoxicity; additive CNS depression | Hepatotoxic drugs, sedatives, alcohol |
| Black cohosh | Possible estrogenic effects, CYP2D6 interactions | Hormone therapy, tamoxifen |

---

### Drug-Food and Drug-Drink Interactions

| Food / Drink | Mechanism | Affected Drug Classes |
|---|---|---|
| Grapefruit juice | CYP3A4 inhibitor — raises blood levels of many drugs | Statins (simvastatin, lovastatin, atorvastatin), calcium channel blockers, immunosuppressants, some benzodiazepines, some antiretrovirals, some antiarrhythmics |
| Alcohol | CNS depressant; hepatotoxic; lowers blood sugar; interacts with anticoagulants | Sedatives, opioids, metronidazole (disulfiram reaction), metformin (lactic acidosis risk), warfarin, acetaminophen (hepatotoxicity) |
| Dairy | Chelates tetracyclines and fluoroquinolones — reduces antibiotic absorption | Tetracyclines, fluoroquinolones |
| High-fat meals | Increases absorption of some drugs, decreases others | Certain antiretrovirals (increase), some antibiotics (decrease) |
| Tyramine-containing foods | MAO-A inhibition allows tyramine accumulation — hypertensive crisis | MAO inhibitors (phenelzine, tranylcypromine, selegiline) |
| Vitamin K-rich foods | Antagonizes warfarin | Warfarin |
| Caffeine | Additive stimulant effects; alters theophylline levels | Stimulants, theophylline, some antibiotics that inhibit caffeine metabolism (fluoroquinolones) |
| High-sodium foods | Reduces lithium excretion — raises lithium blood level | Lithium |
| Licorice (real) | Contains glycyrrhizin — raises blood pressure, lowers potassium | Antihypertensives, digoxin, corticosteroids, diuretics |

---

## Severity Levels

| Level | Definition | Required Action |
|---|---|---|
| Critical | Risk of death or permanent harm if combination is taken | Display emergency contacts. Do not proceed without physician clearance. |
| Major | Serious adverse outcome likely without medical supervision | Recommend immediate physician contact before continuing both medications. |
| Moderate | Clinically meaningful effect; requires monitoring or adjustment | Recommend pharmacist consultation. Flag for next doctor visit. |
| Minor | Low-level effect; rarely causes clinical problems | Inform user. No action required unless symptomatic. |
| Informational | No safety risk; useful context for timing, absorption, or efficacy | Display in schedule notes. No alert needed. |

---

## Interaction Report Structure

Each detected interaction must include:

```
[SEVERITY] Drug A + Drug B (or Drug A + Food/Supplement)

Mechanism:
  Plain-language explanation of how the interaction occurs.

Symptoms to watch for:
  Comma-separated list of symptoms the user should recognize.

Recommended action:
  Specific steps the user should take.

Contact your doctor if:
  Specific trigger condition that warrants immediate medical contact.

Food/drink factors:
  Any food or drink that worsens or triggers this interaction.

Supplement factors:
  Any supplements that worsen or trigger this interaction.

Confidence: High / Medium / Low
Source: [API source or Claude pharmacological knowledge — offline]
```

---

## Duplicate Ingredient Detection

The engine checks for duplicate active ingredients across:

- Brand name vs. generic name equivalents (e.g., Tylenol and acetaminophen taken simultaneously)
- Multi-ingredient OTC products that contain an active ingredient already prescribed (e.g., NyQuil containing acetaminophen while the user is on prescription acetaminophen)
- Supplements that contain pharmaceutical-grade equivalents (e.g., melatonin supplement while taking a melatonin-containing prescription)

When duplicates are detected, flag as **Major** with the message: "You may be taking [ingredient] from two separate sources. Exceeding recommended daily dosage increases risk of [organ-specific toxicity]."

---

## Contraindication Detection

The engine flags contraindicated combinations regardless of interaction mechanism:

- MAOIs + serotonergic drugs (serotonin syndrome)
- Fluoroquinolones + QT-prolonging agents (arrhythmia)
- Sildenafil/tadalafil + nitrates (severe hypotension)
- Warfarin + aspirin at full anti-inflammatory doses (major bleeding)
- ACE inhibitors + ARBs in combination (renal failure risk)
- Methotrexate + NSAIDs (methotrexate toxicity)
- Linezolid + SSRIs or tramadol (serotonin syndrome)
- Clonidine + beta-blockers in abrupt withdrawal context (rebound hypertension)

---

## Confidence Levels

| Level | Basis |
|---|---|
| High | Well-established interaction with multiple clinical studies or FDA labeling; sourced from RxNorm/OpenFDA/DailyMed when available |
| Medium | Interaction reported in case studies or pharmacological reasoning supports plausibility; clinical significance may vary by individual |
| Low | Theoretical interaction based on pharmacological mechanism; limited clinical evidence; or Claude knowledge base only without API confirmation |

All Low and Medium confidence reports include: "Verify this with your pharmacist. The absence of a high-confidence warning does not mean a combination is safe."

---

## API Query Flow

```
Interaction check triggered
    │
    ▼
Build medication pairs list
    │
    ▼
For each pair:
    │
    ├── Query OpenFDA drug interaction endpoint (if network available)
    ├── Query RxNorm for drug family classification
    ├── Query DailyMed for contraindications section
    │
    └── Merge results
    │
    ▼
Apply Claude pharmacological knowledge overlay
(catches interactions not covered by public APIs)
    │
    ▼
Check supplement interaction table (built-in)
    │
    ▼
Check food/drink interaction table (built-in)
    │
    ▼
Run duplicate ingredient detection
    │
    ▼
Run contraindication detection
    │
    ▼
Sort by severity (Critical → Informational)
    │
    ▼
Output interaction report
    │
    ▼
Cache results in interactions.json with timestamp
```

---

## Re-run Policy

The interaction engine runs automatically on:

- Every `mv add` (after save)
- Every `mv edit` (after save)
- Every `mv stop` (after status change)
- Every `mv delete` (after removal)
- Every `mv check` (on demand)

Cached results older than 24 hours are marked stale. The engine prompts to re-run on next `mv list` or `mv check` if the cache is stale.
