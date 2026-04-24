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
- Use `null` when a scalar field cannot be confidently populated.
- Use empty arrays when a list has no items.
- Do not invent values.

## Top Level Schema Definition

```json
{
  "output_mode": "human | json | both",
  "review_context": "generic | targeted",
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
- `category_scores`: weighted category scores.
- `principle_scores`: per principle audit records.
- `missing_data_flags`: missing evidence markers, separate from writing quality.
- `system_flags`: cross-principle aggregate warnings.
- `top_fixes`: highest-value next actions.
- `rewritten_resume`: full rewritten resume text when rewrite requested, else `null`.
- `notes`: operational notes, confidence caveats, and degraded mode warnings.

## Required vs Optional Fields

All top-level fields in this schema are required.

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
  "confidence": "medium",
  "audit_mode": "condensed",
  "final_score": 73.8,
  "verdict": "Good but inconsistent",
  "hire_likelihood": "Possible interview traction if top issues are fixed",
  "critical_issue_count": 1,
  "major_issue_count": 3,
  "minor_issue_count": 4,
  "category_scores": {
    "positioning_and_narrative": 72.0,
    "evidence_and_bullet_strength": 68.5,
    "ats_and_structural_reliability": 82.0,
    "relevance_and_targeting": 70.0,
    "professionalism_and_trust": 80.0
  },
  "principle_scores": [
    {
      "principle": "Make the target role obvious in the top third",
      "source_type": "library_principle",
      "source_name": "Make the target role obvious in the top third",
      "category": "Positioning and Narrative",
      "score": 1,
      "weight": 1.5,
      "severity": "CRITICAL",
      "reason": "Summary does not state a clear target role.",
      "before": "Experienced professional with a diverse background.",
      "after": "Platform automation engineer focused on endpoint and cloud operations.",
      "fix": "State target role and strongest aligned evidence in the top third."
    },
    {
      "principle": "The bullet formula is verb, work, outcome",
      "source_type": "library_principle",
      "source_name": "The bullet formula is verb, work, outcome",
      "category": "Evidence and Bullet Strength",
      "score": 1,
      "weight": 1.5,
      "severity": "MAJOR",
      "reason": "Bullets describe tasks without outcomes.",
      "before": "Worked on release checks.",
      "after": "Automated release checks for 12 services and reduced failed deployments.",
      "fix": "Add outcome framing and measurable impact when available."
    }
  ],
  "missing_data_flags": [
    "MISSING_METRIC"
  ],
  "system_flags": [
    "BULLET_QUALITY_LOW"
  ],
  "top_fixes": [
    "Declare a clear target role in the top third and align first bullets to that target."
  ],
  "rewritten_resume": null,
  "notes": [
    "Rewrite not requested in this run."
  ]
}
```

## Failure Handling Rules

- If extraction is severely scrambled or incomplete, return valid JSON with:
  - conservative low scoring,
  - relevant `system_flags`,
  - clear `notes`,
  - `rewritten_resume` set to `null` unless a safe rewrite was still possible.
- If a field cannot be supported by evidence, use `null` or `[]`.
- Never fill unknown fields with guessed values.

## Low Confidence Extraction Behavior

- Set `confidence` to `low`.
- Score only trusted sections.
- Keep uncertain sections out of `principle_scores` or use conservative low scores with explanatory `notes`.
- Cap maximum verdict at `Strong` unless user manually confirms extracted text.

## Targeted vs Generic Review Context Behavior

- `review_context = targeted` when job description or explicit role target exists.
- `review_context = generic` otherwise.
- Targeted reviews apply stronger relevance checks and should reflect that in `category_scores.relevance_and_targeting` and `top_fixes`.
