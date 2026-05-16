# MedVault Data Schemas

## Medication Record

Full schema for a single medication entry in `medications.json`.

```json
{
  "id": "uuid-v4",
  "name": "string",
  "brandName": "string | null",
  "genericName": "string | null",
  "rxcui": "string | null",
  "ndc": "string | null",
  "dosage": "string",
  "strength": "string",
  "unit": "mg | mcg | mEq | IU | % | mg/mL | other",
  "form": "tablet | capsule | liquid | patch | injection | inhaler | cream | drops | other",
  "frequency": "string",
  "dosesPerDay": "integer",
  "timeOfDay": ["early-morning | morning | midday | afternoon | evening | bedtime"],
  "timingNotes": "string | null",
  "foodRequirement": "with-food | empty-stomach | either | null",
  "classification": "prescription | otc | supplement | herbal | vitamin | mineral",
  "supplementCategory": "string | null",
  "prescribingDoctor": "string | null",
  "prescribingDoctorPhone": "string | null",
  "pharmacy": "string | null",
  "pharmacyPhone": "string | null",
  "rxNumber": "string | null",
  "quantity": "integer | null",
  "daysSupply": "integer | null",
  "refillsRemaining": "integer | null",
  "refillDate": "YYYY-MM-DD | null",
  "expirationDate": "YYYY-MM | null",
  "indication": "string | null",
  "instructions": "string | null",
  "active": "boolean",
  "startDate": "YYYY-MM-DD",
  "stopDate": "YYYY-MM-DD | null",
  "stopReason": "string | null",
  "allergies": ["string"],
  "notes": "string",
  "imageRef": "string | null",
  "ocrConfidence": "high | medium | low | null",
  "source": "manual | ocr",
  "history": [
    {
      "timestamp": "ISO8601",
      "action": "create | edit | stop | restart",
      "field": "string | null",
      "oldValue": "any | null",
      "newValue": "any | null",
      "changedBy": "user | system"
    }
  ],
  "addedAt": "ISO8601",
  "updatedAt": "ISO8601"
}
```

### Field Notes

| Field | Notes |
|---|---|
| `id` | UUID v4, generated on creation, never changed |
| `name` | Primary display name (may be brand or generic depending on what was entered or scanned) |
| `brandName` | Optional; populated from OCR or RxNorm lookup |
| `genericName` | Optional; populated from RxNorm lookup |
| `rxcui` | RxNorm concept ID; used for API interaction queries |
| `ndc` | National Drug Code; 10 or 11 digits; used for OpenFDA queries |
| `strength` | Numeric strength value only (e.g., `10`); `dosage` includes the unit (e.g., `10mg`) |
| `dosesPerDay` | Derived from frequency; used by scheduling engine |
| `timeOfDay` | Array to support multiple daily doses at different times |
| `foodRequirement` | Used by scheduling engine for slot assignment |
| `classification` | Determines which interaction categories apply |
| `supplementCategory` | For supplements: vitamin, mineral, herbal, probiotic, amino acid, enzyme, other |
| `refillDate` | Next scheduled refill date; used for refill prediction (planned) |
| `indication` | What condition the medication is treating; user-provided |
| `imageRef` | Relative path to uploaded label image in `images/` directory |
| `ocrConfidence` | Confidence level of the OCR extraction that created this record |
| `source` | How the record was created |
| `history` | Array of all changes to this record with timestamps |

---

## Interaction Record

Schema for an interaction finding in `interactions.json`.

```json
{
  "id": "uuid-v4",
  "medicationAId": "uuid-v4",
  "medicationAName": "string",
  "medicationBId": "uuid-v4 | null",
  "medicationBName": "string",
  "interactionType": "drug-drug | drug-supplement | drug-food | drug-drink | duplicate-ingredient | contraindication",
  "severity": "critical | major | moderate | minor | informational",
  "mechanism": "string",
  "symptoms": ["string"],
  "recommendedAction": "string",
  "contactDoctorWhen": "string",
  "foodDrinkFactors": ["string"],
  "supplementFactors": ["string"],
  "emergencyContacts": {
    "emergency": "911",
    "poisonControl": "1-800-222-1222"
  },
  "confidenceLevel": "high | medium | low",
  "sources": ["string"],
  "offlineOnly": "boolean",
  "detectedAt": "ISO8601",
  "acknowledgedAt": "ISO8601 | null",
  "acknowledged": "boolean"
}
```

---

## Schedule Record

Schema for the generated daily schedule in `schedule.json`.

```json
{
  "generatedAt": "ISO8601",
  "timezone": "string",
  "slots": [
    {
      "block": "early-morning | morning | midday | afternoon | evening | bedtime",
      "timeRange": "string",
      "medications": [
        {
          "medicationId": "uuid-v4",
          "name": "string",
          "dosage": "string",
          "instructions": "string",
          "timingReason": "string",
          "foodRequirement": "with-food | empty-stomach | either | null",
          "separationNotes": "string | null"
        }
      ]
    }
  ],
  "conflicts": [
    {
      "conflictType": "string",
      "medicationIds": ["uuid-v4"],
      "description": "string",
      "recommendation": "string"
    }
  ],
  "globalNotes": ["string"]
}
```

---

## Audit Log Entry

Each line in `audit.log` follows this format (newline-delimited, not JSON):

```
[ISO8601] ACTION medication_id field_name "old_value" -> "new_value" [source]
```

For actions without a specific field:

```
[ISO8601] ACTION medication_id [source]
```

For interaction check runs:

```
[ISO8601] INTERACTION_CHECK total:{n} critical:{n} major:{n} moderate:{n} minor:{n} informational:{n} offline:{bool}
```

---

## Storage File: medications.json

The full storage file is a JSON array of medication records:

```json
{
  "version": "1.0.0",
  "lastUpdated": "ISO8601",
  "medications": [
    { ...medication record... },
    { ...medication record... }
  ]
}
```

---

## Storage File: interactions.json

```json
{
  "version": "1.0.0",
  "lastChecked": "ISO8601",
  "stale": "boolean",
  "interactions": [
    { ...interaction record... },
    { ...interaction record... }
  ]
}
```

---

## Storage File: schedule.json

```json
{ ...schedule record... }
```

---

## Export: Emergency Card

Plain text format for wallet card or phone screenshot:

```
MEDICATION EMERGENCY CARD
Generated: YYYY-MM-DD
Name: [if user chose to store]

ACTIVE MEDICATIONS
─────────────────────────────────────────────
Metformin (Glucophage)       500mg twice daily
Lisinopril                   10mg once daily
Atorvastatin                 20mg once daily
Vitamin D3                   2000 IU daily

PRESCRIBING PHYSICIANS
─────────────────────────────────────────────
Dr. A. Johnson               555-123-4567

PHARMACY
─────────────────────────────────────────────
CVS Pharmacy #4421           555-987-6543

KNOWN ALLERGIES
─────────────────────────────────────────────
Penicillin, Sulfa drugs

EMERGENCY
─────────────────────────────────────────────
911  |  Poison Control: 1-800-222-1222

This card is for informational use only.
Verify with prescribing physician.
```

---

## Export: Full JSON

The full JSON export wraps all storage files into a single export document:

```json
{
  "exportVersion": "1.0.0",
  "exportedAt": "ISO8601",
  "medications": { ...medications.json content... },
  "interactions": { ...interactions.json content... },
  "schedule": { ...schedule.json content... },
  "disclaimer": "This export contains personal health information. Keep it secure. This is not medical advice."
}
```
