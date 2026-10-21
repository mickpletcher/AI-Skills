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
- Unsafe personal data actually present; missing contact details are a follow-up flag
- Unclear target role
- Mostly vague bullets
- ATS hostile layout
- Contradictory recorded dates; an unexplained interval alone is missing context, not a scored failure

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

## Fixed evidence rubric

Numeric audits use `rubric_version: fixed-evidence-v1`. The calculator owns selection, sources, categories, weights, scores and severity. Provide observations in `scoring_evidence`; do not select principles or assign scores yourself. It emits exactly seven entries in canonical order. All other library principles and common patterns may support qualitative advice, but cannot be added to the numeric ledger or severity counts. Historical scores from other rubric versions are not directly comparable.

| Criterion | Source | Category | Weight |
| --- | --- | --- | ---: |
| positioning | Make the target role obvious in the top third | Positioning and Narrative | 1.5 |
| specificity | Every bullet must name the thing | Evidence and Bullet Strength | 1.5 |
| measurements | Numbers, everywhere, or you get an interview with nobody | Evidence and Bullet Strength | 1.5 |
| structure | Standard section headings beat clever branding | ATS and Structural Reliability | 1.25 |
| chronology | Chronology should be easy to follow | ATS and Structural Reliability | 1.25 |
| alignment | Mirror the job description's language naturally | Relevance and Targeting | 1.5 |
| privacy | No photos, no headshots, no personal data | Professionalism and Trust | 1.0 |

Privacy uses `common_pattern` and exact source `common-patterns § No photos, no headshots, no personal data`. The other targeted criteria use actual library headings. Generic alignment instead uses `common-patterns § Skills keyword dumps`, Relevance and Targeting, weight 1.0. No other common-pattern/category assignment is scored. The calculator verifies the authoritative headings exist.

### Observation inventory

`scoring_evidence` contains the following required fields. Preserve this inventory for both original and rewrite. Extract it again from each version, and explain changed observations. Do not carry an original observation into a rewrite without checking it. Exact quoted text and a short evidence explanation make judgments reviewable.

- `positioning`: `{ "state": "...", "evidence": "quoted support or explicit absence" }`. `role_and_evidence` means a headline or summary explicitly names the role AND a concrete work object/outcome (3/INFO). `role_only` means an explicit target/headline without that supported summary (2/MINOR). `inferred` means direction can only be inferred (1/MAJOR). `absent` means no discernible role direction (0/CRITICAL). Historical experience titles alone are not a target summary.
- `experience_statements`: a nonempty list of `{ "text": "exact experience statement", "names_specific_object": true, "has_supplied_measure": false, "evidence": "explanation" }`. Inventory every distinct activity/outcome in the EXPERIENCE section once. Exclude summary repetitions, skills, education and fixture/missing-data notes. Do not split a statement into its scope and result, omit weak statements or add invented work. For specificity, a named system, process, artifact or environment qualifies; no unsupported implementation detail is needed. For measurement, a supplied count, scope, time or outcome qualifies. Presence of a date alone does not. These two booleans concern separate aspects of the same statements.
- `structure`: state/evidence object. `standard` means conventional section headings and readable role entries (3/INFO); `mixed` means some conventional sections, with mixed labels (2/MINOR); `unclear` means sections cannot be identified reliably (1/MAJOR); `unreadable` means parsing is unusable (0/CRITICAL). Do not infer page count, columns or typography from plain text. Use qualitative review if required observations cannot be made.
- `chronology`: state/evidence object. `clear` means supplied role date ranges are explicit, ordered and noncontradictory (3/INFO), including an explicit Present end date. `coarse` means year-only ranges (2/MINOR). `missing_dates` means a supplied role lacks a start/end date (1/MAJOR). `contradictory` requires an actual contradictory range, such as end before start (0/CRITICAL). Concurrent roles or gaps are not automatically contradictions. An unexplained period after a clearly dated role is `MISSING_TIMELINE_CONTEXT`, not a lower chronology state.
- `requirements`: a nonempty list of `{ "text": "one supplied requirement", "supported": true, "evidence": "resume quote or explicit absence" }`. Targeted reviews inventory ALL explicitly supplied requirements once, including unsupported requirements. Generic reviews inventory each claimed skill once and check its experience support; do not invent a target. Preserve the same target inventory for original/rewrite. No inventory means no overall numeric score.
- `privacy`: state/evidence object. `safe` means no photos or unnecessary sensitive personal information in the supplied material (3/INFO). `unsafe` requires actual such content (0/CRITICAL). A supplied name/email is ordinary contact data. Missing contact details or timeline context do not change privacy. If the supplied representation prevents observation, give a qualitative review instead of a numeric total.

### Derived scores and single ownership

Specificity: all statements name a concrete object = 3/INFO; some = 1/MAJOR; none = 0/CRITICAL. Measurements: all statements have a supplied measure = 3/INFO; some = 2/MINOR; none = 0/MAJOR. Alignment: all inventoried requirements supported = 3/INFO; some = 1/MAJOR; none = 0/MAJOR. Unsupported target experience belongs ONLY to alignment; it is not also a trust or evidence-writing penalty.

Each scored weakness has one owner: role framing -> positioning; unnamed work object -> specificity; missing measures -> measurements; unclear sections -> structure; missing/contradictory recorded dates -> chronology; unsupported requirements -> alignment; actual sensitive personal content -> privacy. No extra severity entries or cross-category copies. Unknown gap context, missing certifications and requests for more detail remain unscored follow-up flags. Do not use a second principle/pattern to count the same weakness again. The helper rejects added, omitted, duplicated or remapped numeric criteria.

Run `python scripts/score_audit.py audit-input.json` on the evidence inventory, copy its derived fields and full ledger, then run `python scripts/score_audit.py final-audit.json --check`. The final check covers criterion entries as well as category totals, verdict and counts. Severity follows the anchors; do not edit it independently. Better prose does not turn absent experience or a missing metric into evidence.

These are document-rubric scores, not calibrated interview probabilities or hiring decisions. Stable extraction remains necessary even with deterministic aggregation. If evidence is uncertain, report the uncertainty and use qualitative review rather than choosing arbitrary state/score values.
