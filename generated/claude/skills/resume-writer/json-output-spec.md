# Resume Writer JSON Output Spec

Official machine-readable contract for Resume Writer audit outputs.

## Purpose of JSON Mode

JSON mode provides consistent structured output for automation and integrations.

Use cases include:

- CLI parsing
- n8n pipelines
- local scripts
- dashboards
- batch resume processing

## Supported Output Modes

- `human`: standard readable audit output.
- `json`: pure JSON object only.
- `both`: readable audit first, then JSON object that matches this schema.

## JSON Mode Rules

- Output must be valid JSON.
- No markdown fences inside pure JSON mode.
- No prose outside the JSON object in pure JSON mode.
- The fenced examples below document the schema. Do not copy their fences or language labels into a `json` response. Before sending, parse the entire response as one JSON object without stripping a prefix, suffix or code block. Its first non-whitespace character must be `{` and its last must be `}`.
- Use `null` when a scalar field cannot be confidently populated.
- Use empty arrays when a list has no items.
- Do not invent values.

## Top Level Schema Definition

```json
{
  "output_mode": "human | json | both",
  "review_context": "generic | targeted",
  "rubric_version": "fixed-evidence-v1",
  "scoring_evidence": {},
  "confidence": "high | medium | low",
  "audit_mode": "condensed | forensic",
  "final_score": 0,
  "verdict": "Excellent | Strong | Good but inconsistent | Weak | High risk",
  "hire_likelihood": "string",
  "critical_issue_count": 0,
  "major_issue_count": 0,
  "minor_issue_count": 0,
  "category_scores": {
    "positioning_and_narrative": 0,
    "evidence_and_bullet_strength": 0,
    "ats_and_structural_reliability": 0,
    "relevance_and_targeting": 0,
    "professionalism_and_trust": 0
  },
  "principle_scores": [
    {
      "criterion_id": "positioning | specificity | measurements | structure | chronology | alignment | privacy",
      "principle": "string",
      "source_type": "library_principle | common_pattern",
      "source_name": "string",
      "category": "string",
      "score": 0,
      "weight": 0,
      "severity": "CRITICAL | MAJOR | MINOR | INFO",
      "reason": "string",
      "before": "string or null",
      "after": "string or null",
      "fix": "string or null"
    }
  ],
  "missing_data_flags": [
    "MISSING_METRIC",
    "MISSING_SCOPE",
    "MISSING_TARGET_ROLE",
    "MISSING_TOOL_SPECIFICITY",
    "MISSING_OUTCOME",
    "MISSING_TIMELINE_CONTEXT"
  ],
  "system_flags": [
    "BULLET_QUALITY_LOW",
    "METRICS_ABSENT",
    "ATS_RISK_HIGH",
    "TARGETING_WEAK",
    "TIMELINE_CONFUSING",
    "CONTACT_INFO_UNSAFE"
  ],
  "top_fixes": [
    "string"
  ],
  "rewritten_resume": "string or null",
  "notes": [
    "string"
  ]
}
```

## Field by Field Explanation

- `output_mode`: response mode selected for this run.
- `review_context`: `targeted` when job description or explicit role target exists, otherwise `generic`.
- `confidence`: extraction confidence based on input fidelity.
- `audit_mode`: `condensed` default, `forensic` only when explicitly requested.
- `final_score`: weighted score out of 100.
- `verdict`: final verdict after critical overrides.
- `hire_likelihood`: short practical likelihood signal.
- `critical_issue_count`, `major_issue_count`, `minor_issue_count`: severity totals.
- `category_scores`: weighted category scores, computed from the current ledger.
- `rubric_version` and `scoring_evidence`: required for numeric scoring. Use the complete inventory and fixed mappings in `scoring-model.md`. The calculator generates exactly seven criterion entries; do not add other patterns, select principles or estimate severity. Supporting source citations do not imply a free choice of numeric category.
- Run the score calculator and final `--check` when code execution is available. Severity totals must equal the ledger, and verdict caps must not raise a verdict.
- `principle_scores`: per principle audit records.
- `missing_data_flags`: missing evidence markers, separate from writing quality.
- `system_flags`: cross-principle aggregate warnings.
- `top_fixes`: highest-value next actions.
- `rewritten_resume`: full rewritten resume text when rewrite requested, else `null`.
- `notes`: operational notes, confidence caveats, and degraded mode warnings.

## Required vs Optional Fields

All top-level fields in this schema are required.

Unscored fallback may additionally use null for final_score, verdict and severity counts, with empty category_scores/principle_scores and null scoring_evidence. This fallback is not a completed numeric audit.

Allowed nullable scalars:

- `principle_scores[].before`
- `principle_scores[].after`
- `principle_scores[].fix`
- `rewritten_resume`

Optional content with required key presence:

- `principle_scores` may be `[]` when scoring cannot be safely performed.
- `missing_data_flags` may be `[]`.
- `system_flags` may be `[]`.
- `top_fixes` may be `[]`.
- `notes` may be `[]`.

## System Flags

These are aggregate warnings across multiple findings, not individual principle scores.

- `BULLET_QUALITY_LOW`
- `METRICS_ABSENT`
- `ATS_RISK_HIGH`
- `TARGETING_WEAK`
- `TIMELINE_CONFUSING`
- `CONTACT_INFO_UNSAFE`

## Example JSON Object

```json
{
  "output_mode": "json",
  "review_context": "targeted",
  "confidence": "high",
  "audit_mode": "condensed",
  "missing_data_flags": [],
  "system_flags": [],
  "top_fixes": [],
  "rewritten_resume": null,
  "notes": [
    "Illustrative complete evidence inventory; not evidence for the current applicant."
  ],
  "hire_likelihood": "Document rubric only; not a calibrated interview probability.",
  "category_scores": {
    "positioning_and_narrative": 100.0,
    "evidence_and_bullet_strength": 100.0,
    "ats_and_structural_reliability": 100.0,
    "relevance_and_targeting": 100.0,
    "professionalism_and_trust": 100.0
  },
  "final_score": 100.0,
  "verdict": "Excellent",
  "critical_issue_count": 0,
  "major_issue_count": 0,
  "minor_issue_count": 0,
  "rubric_version": "fixed-evidence-v1",
  "scoring_evidence": {
    "positioning": {
      "state": "role_and_evidence",
      "evidence": "Data Engineer summary names SQL pipeline work."
    },
    "experience_statements": [
      {
        "text": "Built SQL pipelines processing 100 records daily.",
        "names_specific_object": true,
        "has_supplied_measure": true,
        "evidence": "Named SQL pipelines and supplied volume."
      }
    ],
    "structure": {
      "state": "standard",
      "evidence": "Experience and Education headings."
    },
    "chronology": {
      "state": "clear",
      "evidence": "Jan 2021 - Dec 2024 role range."
    },
    "requirements": [
      {
        "text": "SQL",
        "supported": true,
        "evidence": "Built SQL pipelines."
      }
    ],
    "privacy": {
      "state": "safe",
      "evidence": "Supplied plain text contains ordinary contact data only."
    }
  },
  "principle_scores": [
    {
      "criterion_id": "positioning",
      "principle": "Make the target role obvious in the top third",
      "source_type": "library_principle",
      "source_name": "Make the target role obvious in the top third",
      "category": "Positioning and Narrative",
      "score": 3,
      "weight": 1.5,
      "severity": "INFO",
      "reason": "Data Engineer summary names SQL pipeline work.",
      "before": null,
      "after": null,
      "fix": null
    },
    {
      "criterion_id": "specificity",
      "principle": "Every bullet must name the thing",
      "source_type": "library_principle",
      "source_name": "Every bullet must name the thing",
      "category": "Evidence and Bullet Strength",
      "score": 3,
      "weight": 1.5,
      "severity": "INFO",
      "reason": "1/1 experience statements meet specificity; see scoring_evidence.experience_statements",
      "before": null,
      "after": null,
      "fix": null
    },
    {
      "criterion_id": "measurements",
      "principle": "Numbers, everywhere, or you get an interview with nobody",
      "source_type": "library_principle",
      "source_name": "Numbers, everywhere, or you get an interview with nobody",
      "category": "Evidence and Bullet Strength",
      "score": 3,
      "weight": 1.5,
      "severity": "INFO",
      "reason": "1/1 experience statements meet measurements; see scoring_evidence.experience_statements",
      "before": null,
      "after": null,
      "fix": null
    },
    {
      "criterion_id": "structure",
      "principle": "Standard section headings beat clever branding",
      "source_type": "library_principle",
      "source_name": "Standard section headings beat clever branding",
      "category": "ATS and Structural Reliability",
      "score": 3,
      "weight": 1.25,
      "severity": "INFO",
      "reason": "Experience and Education headings.",
      "before": null,
      "after": null,
      "fix": null
    },
    {
      "criterion_id": "chronology",
      "principle": "Chronology should be easy to follow",
      "source_type": "library_principle",
      "source_name": "Chronology should be easy to follow",
      "category": "ATS and Structural Reliability",
      "score": 3,
      "weight": 1.25,
      "severity": "INFO",
      "reason": "Jan 2021 - Dec 2024 role range.",
      "before": null,
      "after": null,
      "fix": null
    },
    {
      "criterion_id": "alignment",
      "principle": "Mirror the job description's language naturally",
      "source_type": "library_principle",
      "source_name": "Mirror the job description's language naturally",
      "category": "Relevance and Targeting",
      "score": 3,
      "weight": 1.5,
      "severity": "INFO",
      "reason": "1/1 supplied requirements supported; see scoring_evidence.requirements",
      "before": null,
      "after": null,
      "fix": null
    },
    {
      "criterion_id": "privacy",
      "principle": "No photos, no headshots, no personal data",
      "source_type": "common_pattern",
      "source_name": "common-patterns \u00a7 No photos, no headshots, no personal data",
      "category": "Professionalism and Trust",
      "score": 3,
      "weight": 1.0,
      "severity": "INFO",
      "reason": "Supplied plain text contains ordinary contact data only.",
      "before": null,
      "after": null,
      "fix": null
    }
  ]
}
```

## Failure Handling Rules

- If extraction is severely scrambled or incomplete, return valid JSON with:
  - no numeric score when the full required evidence inventory cannot be observed,
  - relevant `system_flags`,
  - clear `notes`,
  - `rewritten_resume` set to `null` unless a safe rewrite was still possible.
- If a field cannot be supported by evidence, use `null` or `[]`.
- Never fill unknown fields with guessed values.

## Low Confidence Extraction Behavior

- Set `confidence` to `low`.
- Score only trusted sections.
- If any required criterion cannot be observed, do not omit it or guess a low score. Return an unscored audit: `final_score`, `verdict` and severity counts null, `category_scores` {}, `principle_scores` [], `scoring_evidence` null, and explicit limitation notes. Do not run numeric calculation on that fallback.
- Cap maximum verdict at `Strong` unless user manually confirms extracted text.

## Targeted vs Generic Review Context Behavior

- `review_context = targeted` when job description or explicit role target exists.
- `review_context = generic` otherwise.
- Targeted reviews apply stronger relevance checks and should reflect that in `category_scores.relevance_and_targeting` and `top_fixes`.
