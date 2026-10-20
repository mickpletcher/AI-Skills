## Scoring Workflow

Use `scoring-model.md` as the source of truth.

Every resume audit in Enhance mode MUST run this scoring workflow.

1. Determine review context:
   - Generic resume review
   - Targeted resume review (job description or explicit target role provided)
   - Low confidence extraction review

2. For each relevant principle:
   - Assign score from `0` to `3`.
   - Assign severity independently (`CRITICAL`, `MAJOR`, `MINOR`, `INFO`).
   - Apply principle weight from the mapping table.
   - When uncertain between adjacent scores, choose the lower score unless strong evidence supports the higher score.
   - Do not inflate scores due to polished wording alone.
   - Weak evidence should score lower even if formatting quality is strong.

3. Calculate category scores:
   - Use weighted average per category from `scoring-model.md`.

4. Calculate final score:
   - Combine category scores using context specific category weights.
   - Output final score out of 100.

5. Apply verdict bands:
   - `90 to 100`: Excellent
   - `80 to 89`: Strong
   - `70 to 79`: Good but inconsistent
   - `60 to 69`: Weak
   - `Below 60`: High risk

6. Apply critical failure overrides:
   - 1 CRITICAL issue caps verdict at Strong.
   - 2 CRITICAL issues cap verdict at Good but inconsistent.
   - 3 or more CRITICAL issues cap verdict at Weak.

7. Handle missing data separately from writing quality:
   - Track required flags under Missing Data.
   - Do not treat missing data flags as identical to writing failures.

8. Confidence and mode labeling:
   - Always label extraction confidence.
   - Always state whether audit ran in Generic or Targeted mode.
   - In Low confidence extraction mode, score only trusted text and cap maximum verdict at Strong unless user manually confirms text.
   - Weak extraction confidence must reduce certainty and must not be silently ignored.

9. Mandatory output sections for scored audits:
   - Final Score Summary
   - Category Breakdown
   - Issues by Severity
   - Missing Data
   - Audit Findings (condensed by default; forensic only when requested)
   - Rewritten Resume (if requested)
   - Top Fixes

10. Populate JSON structure consistently (for `json` and `both` modes):
   - `output_mode`
   - `review_context`
   - `confidence`
   - `audit_mode`
   - `final_score`
   - `verdict`
   - `hire_likelihood`
   - `critical_issue_count`
   - `major_issue_count`
   - `minor_issue_count`
   - `category_scores`
   - `principle_scores`
   - `missing_data_flags`
   - `system_flags`
   - `top_fixes`
   - `rewritten_resume`
   - `cover_letter`
   - `interview_prep_handoff`
   - `two_page_trim_report`
   - `notes`

10a. Longitudinal tracking:
   - When the user provides an earlier resume version, prior score, or prior audit output, compare the current revision against that baseline.
   - Summarize improvement or regression in fit, evidence quality, targeting, and clarity.
   - In `json` and `both` modes, include this under `notes` when no dedicated schema field exists.

11. Bind rewrite output to scoring records:
   - Every CRITICAL or MAJOR issue MUST include a fix recommendation.
   - Every CRITICAL or MAJOR issue MUST include an example rewrite when possible.
   - In `json` and `both` modes, populate `principle_scores[].fix` whenever possible.
   - If rewrite output is included, place full rewritten resume in `rewritten_resume`.
   - If no rewrite was requested, set `rewritten_resume` to `null`.
   - If a cover letter was generated, place it in `cover_letter`.
   - If no cover letter was generated, set `cover_letter` to `null`.

12. System flags:
   - `BULLET_QUALITY_LOW`
   - `METRICS_ABSENT`
   - `ATS_RISK_HIGH`
   - `TARGETING_WEAK`
   - `TIMELINE_CONFUSING`
   - `CONTACT_INFO_UNSAFE`
   - These are cross-principle aggregate signals, not individual issue scores.

13. Preserve existing core rules:
   - Library principles take precedence over common patterns when both apply.
   - Never fabricate metrics.
   - Missing data must not be fabricated to improve scores.
   - Preserve factual resume details.
   - Keep condensed audit default and forensic audit opt in.

---
