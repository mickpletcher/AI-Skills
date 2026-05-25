# MedVault API Abstraction Layer

## Overview

The API layer provides a consistent interface for querying external drug data sources. It abstracts provider-specific response formats into a normalized MedVault schema. Adding a new provider requires implementing the provider interface without touching the interaction engine or UI logic.

---

## Provider Interface

Each API provider implements the following operations:

```
interface MedVaultApiProvider {
  normalizeDrugName(rawName: string): DrugNameResult
  getDrugLabel(identifier: string): DrugLabel
  getInteractions(drugA: string, drugB: string): InteractionResult[]
  searchDrug(query: string): DrugSearchResult[]
  getDrugInfo(identifier: string): DrugInfo
}
```

Providers return normalized types. Provider-specific fields are stored in a `raw` passthrough field for debugging without affecting downstream logic.

---

## Current Providers

### 1. RxNorm (National Library of Medicine)

**Purpose:** Drug name normalization, concept lookup, synonym resolution

**Base URL:** `https://rxnav.nlm.nih.gov/REST/`

**Authentication:** None required (public API)

**Rate limits:** No hard limits; NLM requests reasonable use

**Key Endpoints:**

| Endpoint | Use |
|---|---|
| `GET /drugs?name={name}` | Find drug by name, returns RxCUI |
| `GET /rxcui/{rxcui}/properties` | Get normalized name, synonym, drug class |
| `GET /rxcui/{rxcui}/related?tty=BN+IN` | Get brand and generic name relationship |
| `GET /interaction/list?rxcuis={a+b}` | Get interaction data between two RxCUI identifiers |

**Response normalization:**

Map RxNorm `minConceptGroup.minConcept.name` to `MedVaultApiResult.normalizedName`. Map `interactionTypeGroup.interactionType.interactionPair` to `InteractionResult[]`.

---

### 2. OpenFDA

**Purpose:** Label data, adverse events, recall status, structured drug data

**Base URL:** `https://api.fda.gov/drug/`

**Authentication:** API key optional (higher rate limits with key); anonymous use supported

**Rate limits:** 240 requests/minute with key; 40 requests/minute anonymous

**Key Endpoints:**

| Endpoint | Use |
|---|---|
| `GET /label.json?search=openfda.brand_name:{name}` | Get full prescribing label |
| `GET /event.json?search=patient.drug.medicinalproduct:{name}` | Adverse event reports |
| `GET /enforcement.json?search=product_description:{name}` | Recall history |
| `GET /ndc.json?search=brand_name:{name}` | NDC number lookup |

**Response normalization:**

Map `results[0].warnings` to `DrugLabel.warnings`. Map `results[0].drug_interactions` to `DrugLabel.interactions`. Map `results[0].dosage_and_administration` to `DrugLabel.dosageInstructions`.

**API Key Configuration:**

Set `OPENFDA_API_KEY` in MedVault configuration. If not set, anonymous access is used with lower rate limits.

---

### 3. DailyMed (NLM)

**Purpose:** Full structured prescribing information (SPL format), contraindications, boxed warnings

**Base URL:** `https://dailymed.nlm.nih.gov/dailymed/services/v2/`

**Authentication:** None required (public API)

**Rate limits:** No stated limits; NLM requests reasonable use

**Key Endpoints:**

| Endpoint | Use |
|---|---|
| `GET /drugnames.json?drug_name={name}` | Find SPL records by drug name |
| `GET /spls/{setid}.json` | Get full structured product label |
| `GET /spls/{setid}/sections.json` | Get specific label sections |

**Sections of interest:**

| Section Code | Content |
|---|---|
| `34067-9` | Indications and usage |
| `34071-1` | Warnings |
| `34084-4` | Adverse reactions |
| `34073-7` | Drug interactions |
| `34070-3` | Contraindications |
| `34068-7` | Dosage and administration |

**Response normalization:**

Parse SPL XML structure. Map contraindications section to `DrugLabel.contraindications`. Map drug interactions section to `InteractionResult[]` with confidence `high` (FDA-sourced).

---

### 4. NIH Office of Dietary Supplements (ODS)

**Purpose:** Vitamin and supplement interaction data, recommended daily allowances, safety information

**Base URL:** `https://ods.od.nih.gov/`

**Data access:** Primarily via curated fact sheets (no structured API). Supplement interaction data is built into the MedVault supplement interaction table and updated with each skill release.

**Built-in supplement table:** See `docs/interaction-engine.md` supplement section.

---

### 5. DrugBank (Planned — Commercial License Required)

**Purpose:** Comprehensive drug interaction database, drug target information, pharmacokinetic profiles

**Status:** Planned for v1.2.0. Requires commercial API license.

**Base URL:** `https://go.drugbank.com/api/v1/`

**Authentication:** API key required (paid subscription)

**Value:** More comprehensive interaction coverage than public APIs, especially for newer drugs and complex polypharmacy scenarios.

**Implementation note:** The provider interface is already designed to accommodate DrugBank. Implementing the provider requires: API key configuration, response mapping to `InteractionResult[]`, and confidence scoring calibration against existing provider results.

---

## Provider Priority and Fallback Chain

When multiple providers return interaction data for the same pair, results are merged using this priority:

```
DailyMed (FDA-labeled contraindications) — highest priority
    ▼
OpenFDA (adverse event and label data)
    ▼
RxNorm (NLM interaction pairs)
    ▼
Claude pharmacological knowledge base (offline / gap fill)
    ▼
Built-in supplement interaction table
```

When providers disagree on severity, use the **higher severity** from the most authoritative source. Log the discrepancy in the interaction record under `raw.providerConflicts`.

---

## Offline Fallback

When no network is available:

1. All API provider calls return empty results immediately (no timeout wait)
2. Claude's built-in pharmacological knowledge handles all interaction detection
3. Built-in supplement and food interaction tables remain fully functional
4. All results are labeled `[Offline — Claude knowledge base only]`
5. Confidence is capped at `medium` for all offline results
6. A banner is shown at the top of every interaction report: "Network unavailable. Results are based on Claude's training data and may be wrong or incomplete. Verify with both your doctor and pharmacist."

---

## Adding a New Provider

1. Create a new provider file implementing the `MedVaultApiProvider` interface.
2. Add provider configuration (base URL, auth method, rate limits) to `providers/config.json`.
3. Implement response normalization mapping.
4. Set provider priority level in the fallback chain configuration.
5. Add the provider to the provider registry in `providers/registry.json`.
6. Update `docs/api-layer.md` with the new provider details.

No changes to the interaction engine or SKILL.md are required.

---

## Response Cache

API responses are cached in memory for the duration of a session. Interaction analysis results are persisted to `interactions.json` with a timestamp. Results older than 24 hours are considered stale.

Cache invalidation triggers:

- Any `mv add`, `mv edit`, `mv stop`, or `mv delete` action
- Manual `mv check` command (always forces fresh API queries)
- Cache age exceeding 24 hours

---

## Error Handling

| Error Type | Response |
|---|---|
| Network timeout (>5s) | Skip provider, continue with remaining providers, log timeout |
| HTTP 4xx | Log error with status code, skip provider for this session |
| HTTP 5xx | Retry once after 2 seconds, then skip provider |
| Malformed response | Log parse error, skip provider result |
| Rate limit (429) | Back off 30 seconds, retry once, then skip provider for this session |
| All providers fail | Use offline mode, display offline banner |
