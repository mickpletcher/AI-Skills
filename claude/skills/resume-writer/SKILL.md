---
name: resume-writer
description: Rewrite and enhance resumes using a persistent library of principles harvested from real recruiters, hiring managers, and HR professionals. Always trigger immediately when the user's message starts with "rw". Also trigger on "resume writer", "rewrite my resume", "enhance my resume", "fix my resume", "review my resume", or any request to improve, audit, or critique a resume. Also trigger when the user pastes a recruiter or hiring manager post (LinkedIn, blog, Reddit) and says "add to my library", "add insight", "rw add", or indicates they want to capture it as a resume principle. Handles paste, .docx, .pdf, and screenshot inputs. Produces a full rewrite plus a condensed audit by default, with full forensic line by line audit only when requested. General-purpose skill that works for any user's resume, not just the skill owner.
---

# Resume Writer

Rewrites resumes using a persistent, user-curated library of principles harvested from recruiters, hiring managers, and HR professionals. Every change made is traceable back to a specific principle in `insights/principles.md` or a pattern in `references/common-patterns.md`.

## Two modes

This skill operates in one of two modes. Detect which one before proceeding.

### Mode 1: Enhance a resume (default)

Triggered when the user provides a resume (pasted, .docx, .pdf, or screenshot) and asks for a rewrite, review, audit, or critique.

Go to the **Enhance Workflow** section.

### Mode 2: Add an insight to the library

Triggered when the user pastes or uploads a recruiter/HR post and says something like "rw add", "add to library", "add this insight", or pastes a post without a resume present.

Go to the **Add Insight Workflow** section.

### Mode detection rules

- If a resume-shaped input is present (text with experience/education sections, or a .docx/.pdf/image file that looks like a resume), default to Enhance mode. Do not ask.
- If only a recruiter/HR post is present with no resume, default to Add Insight mode. Do not ask.
- Only ask "enhance or add to library?" when the input is genuinely ambiguous (e.g., a LinkedIn profile export that could be either).

## Output Mode Handling

Default output mode is `human`.

`json-output-spec.md` is the authoritative contract for machine-readable output.

Switch output mode when user intent indicates automation needs:

- If user asks for automation, API, JSON, machine-readable, structured output, pipeline use, CLI use, n8n use, or parsing, switch to `json` or `both`.

Mode behavior:

- `human`: return the standard readable audit output.
- `json`: return valid JSON only, matching `json-output-spec.md`.
- `both`: return standard readable audit first, followed by a JSON block that matches `json-output-spec.md`.

Hard enforcement rules:

- In `json` mode, return valid JSON only.
- In `json` mode, do not use markdown fences.
- In `json` mode, do not include prose outside the JSON object.
- In `both` mode, the JSON block must still fully conform to the schema.
- Do not omit required fields from `json-output-spec.md`.
- When uncertain between two adjacent values, choose the more conservative lower score.
- When a field cannot be supported by evidence, use `null` or an empty array instead of guessing.

---

## Enhance Workflow

### Step 1: Extract resume text

Match the input type:

- **Pasted text**: Use as-is.
- **.docx**: Use the available document-reading tooling to extract the text while preserving structure as much as possible.
- **.pdf**: Use the available PDF-reading tooling to extract text. If the PDF is image-based (scanned), fall back to image-based reading.
- **Screenshot / image**: Read the image directly.

Apply these deterministic extraction rules:

- **Single column and readable**: proceed.
- **Multi column or table heavy**: proceed with a parsing fidelity warning.
- **Severely scrambled or incomplete extraction**: stop and ask for pasted text.

Extraction confidence model:

- **High confidence**: pasted text or clean DOCX.
- **Medium confidence**: machine readable PDF.
- **Low confidence**: screenshots, scans, or heavily formatted resumes.

If the source is not pasted text, include extraction confidence in the final output.

### Step 2: Load the insights library and common patterns

Read `insights/principles.md` and `references/common-patterns.md` in full. Both are authoritative sources for the audit.

If either file cannot be read, continue in degraded mode and state exactly what is missing and how that limits the audit.

**Precedence rule**: When a violation could map to both a library principle and a common pattern, cite the library principle. Library principles carry named sources and specific framing; patterns are the fallback for hygiene issues no library principle covers.

If a weakness is clearly real but no principle or pattern covers it, capture it in the "Not-in-library observations" section of the output rather than attributing it to something that does not exist.

### Step 3: Ask one clarifying question (if needed)

Before rewriting, ask at most ONE question if it materially affects the rewrite:

- If no target role is specified AND the resume is ambiguous: "What role or type of role is this resume targeting?"
- If the user already gave the target role, do not ask.
- If the user provided a job description, target role, or target company, do not ask a generic target question.
- Do not ask about tone, format, or style preferences — infer them from the resume itself.

Skip this step entirely if the target is obvious.

### Step 4: Targeted rewrite track (when target info exists)

When both a resume and a job description or explicit target role are present, run a targeted rewrite track inside Enhance mode.

- Prioritize alignment to the target role over generic improvements.
- Reorder summary, skills, and bullet emphasis to match the target role.
- Highlight directly relevant evidence first in each recent role.
- Do not fabricate experience, achievements, or keywords not supported by the original resume.

### Step 5: Audit the resume

For every bullet, section, and structural element, check it against each principle in the library and each pattern in common-patterns. Build an internal list of violations in this format:

```
- [Location: Section / bullet N]
- [Source: <library principle name>  OR  common-patterns § <section name>]
- [Current text: "<exact quote>"]
- [Issue: <specific problem>]
- [Recommended fix: "<rewritten text>"]
```

Be specific. "Weak bullet" is not a valid issue. "No outcome specified — says 'improved processes' without saying what improved or by how much" is.

When the same violation maps to both a library principle and a pattern, apply the precedence rule: cite the library principle.

Capture scoring inputs while auditing:

- Principle name
- Score (`0` to `3`)
- Severity (`CRITICAL`, `MAJOR`, `MINOR`, `INFO`)
- Category (from `scoring-model.md`)
- Principle weight (from `scoring-model.md`)
- Missing data flag (if present)

### Step 6: Produce the rewrite

Rewrite the full resume applying all recommended fixes. Preserve:

- Contact info exactly as given
- Employer names, job titles, dates exactly as given
- Education details (school, degree, dates)
- Any certifications (keep all, but reorder per library principles)

Rewrite freely:

- Bullet wording, order, and specificity
- Summary / profile section
- Skills section organization
- Section ordering within the resume

Do not invent facts. If a bullet lacks a number and the user did not provide one, rewrite using the strongest truthful framing available — do not fabricate metrics. Flag in the audit that a number is needed and ask the user to supply it.

### Step 7: Self-validate the rewrite

Before presenting the output, re-audit the rewritten text against the library and patterns. Rewrites frequently introduce new violations — a bullet fixed for specificity can end up too long, a reorganized skills section can drop ATS-relevant keywords.

For each section of the rewrite, check:

- Does every bullet follow action verb / object / outcome?
- Is every quantified claim actually supported by the original, or did a number sneak in that was not there before?
- Did any weak verb ("Responsible for", "Helped with") survive the rewrite?
- Does the final length still fit the target from common-patterns § Length?
- Did any section get longer than its target bullet count?

If the re-audit surfaces issues, fix them silently before presenting. Do not show the user the self-validation pass — it is an internal checkpoint, not part of the deliverable.

### Step 8: Produce the output

Apply Output Mode Handling before final response assembly.

Deliver seven sections, in this order:

1. **Final Score Summary**
   - Final Score
   - Verdict
   - Hire Likelihood Signal
   - Confidence
   - Audit Mode
   - Review Context

2. **Category Breakdown**
   - Positioning and Narrative
   - Evidence and Bullet Strength
   - ATS and Structural Reliability
   - Relevance and Targeting
   - Professionalism and Trust

3. **Issues by Severity**
   - CRITICAL
   - MAJOR
   - MINOR

4. **Missing Data**
   - MISSING METRIC
   - MISSING SCOPE
   - MISSING TARGET ROLE
   - MISSING TOOL SPECIFICITY
   - MISSING OUTCOME
   - MISSING TIMELINE CONTEXT

5. **Audit Findings**
   - Condensed by default.
   - Full forensic only when explicitly requested.
   - Source field must hold either a library principle name or `common-patterns § <section>`.

6. **Rewritten Resume (if requested)**
   - Include this section when the request is in rewrite mode or the user explicitly requests a rewrite.
   - If input was .docx, produce .docx using the available document tooling when the environment supports it, preserving any letterhead or formatting when possible.
   - If input was .pdf, produce .docx by default.
   - If input was paste or image, produce Markdown unless the user asks for .docx.
   - In JSON output, map this content to `rewritten_resume`.

7. **Top Fixes / Next Steps**
   - List highest impact improvements first.
   - Include missing metrics and follow up items.
   - Include any "Not-in-library observations".
   - If any Not-in-library observation recurs, offer to add it as a principle.

If source is not pasted text, always state extraction confidence (High, Medium, or Low) and parsing limitations.

Output mode assembly rules:

- `human`: return only the seven human-readable sections.
- `json`: return only the JSON object defined by `json-output-spec.md`.
- `both`: return the seven human-readable sections first, then append a fully conforming JSON object.

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
   - `notes`

11. Bind rewrite output to scoring records:
   - Every CRITICAL or MAJOR issue MUST include a fix recommendation.
   - Every CRITICAL or MAJOR issue MUST include an example rewrite when possible.
   - In `json` and `both` modes, populate `principle_scores[].fix` whenever possible.
   - If rewrite output is included, place full rewritten resume in `rewritten_resume`.
   - If no rewrite was requested, set `rewritten_resume` to `null`.

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

## Add Insight Workflow

### Step 1: Extract the source

- Paste text: use as-is
- Screenshot: OCR the image, read the text
- URL: fetch the URL if accessible

Capture: who said it (name, title if visible), platform, approximate date, and the raw text.

### Step 2: Extract the principle(s)

A single post may contain multiple principles. Extract each one separately. For each, identify:

- **Principle name** — short, memorable (e.g., "Lead with impact, not credentials")
- **The rule** — 1-2 sentences
- **Rationale** — why the source says it matters
- **Example violation** — quote the bad example if given, otherwise synthesize a realistic one
- **Example fix** — quote the good example if given, otherwise synthesize one
- **Source** — Name, Title, Platform, Date

Skip anything that is opinion without an actionable rule (e.g., "I prefer Helvetica" is too weak to be a principle unless it is part of a broader formatting rule).

### Step 3: Check for duplicates

Read the existing `insights/principles.md`. If a principle is already covered, either:

- **Skip it** and tell the user "already in library as '<existing principle name>'", OR
- **Merge it**: if the new post strengthens or adds nuance, append a new source line to the existing principle using the `(adds: <angle>)` inline format defined in `insights/principles.md`.

Never create near-duplicate entries.

### Step 4: Append to library

Add new principles to `insights/principles.md` using the format defined at the top of that file. Maintain the existing structure. Do not reorder existing entries.

If the environment cannot write to `insights/principles.md`, do not claim the library was updated. Instead return the exact principle text that should be appended manually.

### Step 5: Confirm

Tell the user exactly what was added, merged, or skipped:

```
Added 2 principles to the library:
1. [Name] — [1-sentence summary]
2. [Name] — [1-sentence summary]

Merged into existing: [Name of existing principle] — added source with angle: "<angle>"
Skipped (already covered): [Name]
```

---

## Principles of using this skill

- **Every audit finding must map to a library principle, a pattern in `common-patterns.md`, or be clearly flagged as "Not-in-library observations".** Do not invent principles.
- **Library principles win over patterns** when both apply. Library entries have attribution and specific framing; patterns are the fallback.
- **Never fabricate metrics.** If a bullet needs a number the user did not supply, flag it in the "Missing data" section and rewrite with the strongest truthful framing available.
- **Preserve facts, rewrite framing.** Employers, titles, dates, certifications, and education details are never changed. Everything else is fair game.
- **The library grows over time.** If during a rewrite you notice the user would benefit from a principle not yet captured, mention it in "Next steps": "This weakness maps to a common recruiter complaint I do not have in your library yet. Want to add it?"
- **General-purpose tone.** Do not assume the resume belongs to the skill owner. Match the voice of the existing resume unless the user requests a tone change.

## Operational Constraints

- If `insights/principles.md` or `references/common-patterns.md` cannot be read, continue in degraded mode and clearly state that the audit is limited.
- If resume extraction comes from an image, screenshot, or scanned PDF and quality is poor, label the audit as partial.
- If the resume is multi column, table heavy, or visually complex, proceed but warn that parsing fidelity may be reduced.
- If a job description, target role, or target company is provided, prioritize alignment to that target over generic optimization.
- If the environment cannot write to `insights/principles.md`, return exact append ready principle text and state that manual update is required.
