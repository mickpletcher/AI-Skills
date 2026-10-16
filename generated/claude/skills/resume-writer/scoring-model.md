# Resume Writer Scoring Model

This file defines the deterministic scoring framework used by Resume Writer audits.

## Purpose

The scoring model makes audits consistent across reviewers and input formats.

- Translate qualitative findings into a repeatable score out of 100
- Keep issue severity separate from numeric score
- Preserve missing data flags as their own signal
- Support generic and targeted review contexts without changing core principles

## Core Scales

### Principle score scale (0 to 3)

- `0`: Fails the principle. Clear weakness or missing requirement.
- `1`: Weak. Some signal exists but not enough to be competitive.
- `2`: Solid. Meets expectation with only minor improvement needed.
- `3`: Strong. Clear, specific, and competitive execution.

### Severity scale

Severity is assigned independently from the 0 to 3 score.

- `CRITICAL`: High risk issue that can block interviews or damage trust.
- `MAJOR`: Meaningful weakness that reduces competitiveness.
- `MINOR`: Improvement opportunity with lower immediate risk.
- `INFO`: Context note that does not count as a failure.

## Category Model and Weights

Use one of these category weight profiles based on review context.

### Generic resume review weights

- Positioning and Narrative: `25%`
- Evidence and Bullet Strength: `35%`
- ATS and Structural Reliability: `20%`
- Relevance and Targeting: `10%`
- Professionalism and Trust: `10%`

### Targeted resume review weights

- Positioning and Narrative: `25%`
- Evidence and Bullet Strength: `30%`
- ATS and Structural Reliability: `20%`
- Relevance and Targeting: `15%`
- Professionalism and Trust: `10%`

## Principle Weight Model

Each principle has an internal weight inside its category.

- `1.5`: Core competitive signal. Usually interview deciding.
- `1.25`: High value signal.
- `1.0`: Standard signal.
- `0.75`: Supporting signal.

Principle weights are normalized only within their own category.

## Scoring Formulas

### Per principle normalized score

$$
principleNormalized = \frac{principleScore}{3}
$$

### Weighted category score

$$
categoryScore = \frac{\sum(principleNormalized \times principleWeight)}{\sum(principleWeight)} \times 100
$$

Round category scores to one decimal place.

### Final score out of 100

$$
finalScore = \sum(categoryScore \times categoryWeight)
$$

Category weights are decimal fractions of 1.0. Round the final score to one decimal place.

## Verdict Bands

- `90 to 100`: Excellent
- `80 to 89`: Strong
- `70 to 79`: Good but inconsistent
- `60 to 69`: Weak
- `Below 60`: High risk

## Hire Likelihood Signal Guidance

Use a short practical signal tied to verdict.

- Excellent: High likelihood of interview traction
- Strong: Good likelihood of interview traction
- Good but inconsistent: Possible interview traction if top issues are fixed
- Weak: Low likelihood without major revision
- High risk: Very low likelihood in current state

## Critical Failure Overrides

Critical overrides cap verdict regardless of numeric score.

Critical conditions include:

- Unreadable or badly parsed resume
- Missing or unsafe contact information
- Unclear target role
- Mostly vague bullets
- ATS hostile layout
- Confusing or misleading timeline

Override caps:

- `1 CRITICAL` issue: maximum verdict `Strong`
- `2 CRITICAL` issues: maximum verdict `Good but inconsistent`
- `3 or more CRITICAL` issues: maximum verdict `Weak`

## Missing Data Flags

Track missing data separately from writing quality.

- `MISSING METRIC`
- `MISSING SCOPE`
- `MISSING TARGET ROLE`
- `MISSING TOOL SPECIFICITY`
- `MISSING OUTCOME`
- `MISSING TIMELINE CONTEXT`

These flags do not automatically become writing failures. They are used for follow up action and can explain why an otherwise clean bullet cannot reach a higher score.

## System Flags

System flags are cross-principle aggregate warnings, not individual principle scores.

- `BULLET_QUALITY_LOW`
- `METRICS_ABSENT`
- `ATS_RISK_HIGH`
- `TARGETING_WEAK`
- `TIMELINE_CONFUSING`
- `CONTACT_INFO_UNSAFE`

Use these to summarize higher-level risk patterns that appear across multiple findings.

## Conservative Scoring Guardrails

- When uncertain between two adjacent scores, choose the lower score unless strong evidence supports the higher score.
- Do not inflate scores because wording sounds polished if evidence quality is still weak.
- Weak extraction confidence must reduce certainty and must not be ignored.
- Missing data must never be fabricated to improve scoring outcomes.

## Context Modes

### Generic resume review

- Use Generic category weights
- Judge against broad competitiveness

### Targeted resume review

- Use Targeted category weights
- Increase emphasis on target role alignment and keyword relevance

### Low confidence extraction

- Score only sections that can be trusted from extraction
- Mark uncertain sections as unscorable, not failed
- Attach extraction confidence label
- Cap maximum verdict at `Strong` unless user manually confirms extracted text

## User Facing Output Model

The final audit output should always appear in this order:

1. Final Score Summary
2. Category Breakdown
3. Issues by Severity
4. Missing Data
5. Audit Findings (condensed by default, forensic on request)
6. Rewritten Resume
7. Top Fixes / Next Steps

## Internal JSON Output Example

Official JSON contract and field naming live in `json-output-spec.md`.

```json
{
  "reviewContext": "targeted",
  "confidence": "Medium",
  "scoringModelVersion": "1.0",
  "finalScore": 78.4,
  "rawVerdict": "Strong",
  "finalVerdict": "Good but inconsistent",
  "hireLikelihoodSignal": "Possible interview traction if top issues are fixed",
  "overrideApplied": {
    "applied": true,
    "criticalCount": 2,
    "capVerdict": "Good but inconsistent",
    "reasons": [
      "Mostly vague bullets",
      "Unclear target role"
    ]
  },
  "categoryScores": {
    "Positioning and Narrative": 74.0,
    "Evidence and Bullet Strength": 70.8,
    "ATS and Structural Reliability": 86.5,
    "Relevance and Targeting": 72.2,
    "Professionalism and Trust": 83.0
  },
  "severityCounts": {
    "CRITICAL": 2,
    "MAJOR": 4,
    "MINOR": 5,
    "INFO": 2
  },
  "missingDataFlags": [
    "MISSING METRIC",
    "MISSING OUTCOME"
  ]
}
```

## Starter Principle to Category Mapping

Use this starter table for current principles in `insights/principles.md`.

| Principle | Category | Weight | Default Severity If Weak |
| --- | --- | ---: | --- |
| Lead with project impact, not credentials | Positioning and Narrative | 1.25 | MAJOR |
| Every bullet must name the thing | Evidence and Bullet Strength | 1.5 | MAJOR |
| Numbers, everywhere, or you get an interview with nobody | Evidence and Bullet Strength | 1.5 | MAJOR |
| Two pages is the ceiling | ATS and Structural Reliability | 1.0 | MINOR |
| A resume is a sales document, not a job history | Positioning and Narrative | 1.25 | MAJOR |
| Make the target role obvious in the top third | Positioning and Narrative | 1.5 | CRITICAL |
| The summary must be targeted, not decorative | Positioning and Narrative | 1.0 | MAJOR |
| Mirror the job description's language naturally | Relevance and Targeting | 1.5 | MAJOR |
| Standard section headings beat clever branding | ATS and Structural Reliability | 1.25 | MAJOR |
| Keep critical data out of headers, footers, and text boxes | ATS and Structural Reliability | 1.5 | CRITICAL |
| Single column wins over pretty layouts | ATS and Structural Reliability | 1.25 | MAJOR |
| Your technical resume needs a clear narrative | Positioning and Narrative | 1.0 | MAJOR |
| Chronology should be easy to follow | ATS and Structural Reliability | 1.25 | CRITICAL |
| Use hybrid structure only when the timeline needs help | ATS and Structural Reliability | 1.0 | MAJOR |
| The bullet formula is verb, work, outcome | Evidence and Bullet Strength | 1.5 | MAJOR |
| Put the strongest proof first under each role | Evidence and Bullet Strength | 1.25 | MAJOR |
| Skills lists need proof, not just nouns | Evidence and Bullet Strength | 1.0 | MAJOR |
| When hard metrics are missing, show scope instead of fluff | Evidence and Bullet Strength | 1.0 | MAJOR |
| Explain career direction, do not make the recruiter guess | Positioning and Narrative | 1.25 | MAJOR |
| Simplicity signals judgment | Professionalism and Trust | 1.0 | MINOR |
| The file name is part of the first impression | Professionalism and Trust | 0.75 | MINOR |
| Early career candidates should emphasize proof of readiness, not apologize for lack of years | Positioning and Narrative | 1.0 | MAJOR |
| Senior candidates must show scope, not just tenure | Positioning and Narrative | 1.0 | MAJOR |
| Proofread like a hiring manager is looking for a reason to say no | Professionalism and Trust | 1.25 | MAJOR |

This starter map can be extended as the principle library grows.
