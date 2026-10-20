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

## Calculation and source evidence

Use `json-output-spec.md` as the single output schema. Its example is illustrative, not evidence for the current audit. Compute numeric fields from the current `principle_scores` ledger with `scripts/score_audit.py`. The calculator validates source headings, mapped weights/categories, rounding, severity totals and verdict caps.

Every CRITICAL, MAJOR or MINOR finding counted in a summary must be represented in that ledger. Score each source once, grouping its related findings. Score categories from supported text; do not invent document layout or missing history. Include a supported ledger entry for each category before giving an overall score.

Common patterns use source type `common_pattern`, an exact `common-patterns § <heading>` from the supplied file and weight 1.0. Choose the relevant category and explain the observed evidence. Unattributed observations remain explicitly not-in-library and outside numerical scoring.

## Starter Principle to Category Mapping

Only the following names are current headings in `insights/principles.md`. A weight-map row does not create a principle or establish attribution. Cite the actual library heading and source, or a real common-pattern heading. Do not label a scoring example as a library entry.

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

Extend the map only after the corresponding attributed principle is actually present in the library. Common patterns retain their own source type.
