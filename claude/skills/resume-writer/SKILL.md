---
name: resume-writer
description: Rewrite and enhance resumes using a persistent library of principles harvested from real recruiters, hiring managers, and HR professionals. Always trigger immediately when the user's message starts with "rw". Also trigger on "resume writer", "rewrite my resume", "enhance my resume", "fix my resume", "review my resume", or any request to improve, audit, or critique a resume. Also trigger when the user pastes a recruiter or hiring manager post (LinkedIn, blog, Reddit) and says "add to my library", "add insight", "rw add", or indicates they want to capture it as a resume principle. Also trigger on "two page", "two-page", "trim to two pages", "fit on two pages", "two page audit", or "page trim" to run the two-page audit mode. Handles paste, .docx, .pdf, and screenshot inputs. Produces a full rewrite plus a condensed audit by default, with full forensic line by line audit only when requested. General-purpose skill that works for any user's resume, not just the skill owner.
---

# Resume Writer

Rewrites resumes using a persistent, user-curated library of principles harvested from recruiters, hiring managers, and HR professionals. Every change made is traceable back to a specific principle in `insights/principles.md` or a pattern in `references/common-patterns.md`.

`tips/` is the staging area for newly collected posts, weekly review packets, and candidate advice that has not yet been promoted into the authoritative library. Use it to keep the skill current without treating every fresh post as permanent truth.

## Three modes

This skill operates in one of three modes. Detect which one before proceeding.

### Mode 1: Enhance a resume (default)

Triggered when the user provides a resume (pasted, .docx, .pdf, or screenshot) and asks for a rewrite, review, audit, or critique.

Go to the **Enhance Workflow** section.

### Mode 2: Add an insight to the library

Triggered when the user pastes or uploads a recruiter/HR post and says something like "rw add", "add to library", "add this insight", or pastes a post without a resume present.

Go to the **Add Insight Workflow** section.

### Mode 3: Refresh tips staging area

Triggered when the user asks to refresh, review, triage, summarize, or organize recruiter/HR posts for future resume guidance, or refers to the weekly `tips/` update.

Go to the **Refresh Tips Workflow** section.

### Mode detection rules

- If a resume-shaped input is present (text with experience/education sections, or a .docx/.pdf/image file that looks like a resume), default to Enhance mode. Do not ask.
- If only a recruiter/HR post is present with no resume, default to Add Insight mode. Do not ask.
- If the user is asking to maintain the source pipeline, weekly refresh process, source roster, or `tips/` contents, use Refresh Tips mode.
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

Treat `tips/` as optional context only. Never cite a raw `tips/inbox/` item as an authoritative principle unless the user explicitly asks for emerging or experimental guidance. Prefer `tips/reviewed/` over `tips/inbox/` when both exist.

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

### Step 4b: Two-page audit mode (when explicitly requested)

Activate when the user says "two page", "two-page", "trim to two pages", "fit on two pages", "two page audit", or "page trim". Two-page mode runs inside Enhance mode — the full audit and rewrite still execute, but a strict trimming phase is added after the rewrite.

**Estimate current length** before trimming. Use these proxies:

- Pasted text or Markdown: 55 lines per page, ~650 words per page
- DOCX: use word count if available; otherwise estimate from line count
- If the resume is already two pages or under, state that and skip trimming. Still run the full audit.

**Section priority rules** — apply in order until the resume fits two pages:

Pass 1 — trim without removing content:
- Cap the summary at 3 sentences. Cut the rest.
- Collapse the skills section: remove any skill already demonstrated in a bullet point elsewhere. Merge overlapping categories into fewer lines.
- Remove soft-skill filler ("results-driven", "team player", "passionate about") from all sections.

Pass 2 — reduce bullet counts per role:
- Roles held more than 5 years ago: reduce to 3 bullets maximum. Keep only bullets with unique evidence not covered by more recent roles.
- Roles held more than 10 years ago: reduce to 1-2 bullets or collapse to a single line (Title, Company, Date range). Remove the section entirely only if all content is redundant.
- Roles held more than 15 years ago: remove unless they contain a credential or achievement not available anywhere else in the resume (e.g., founding a company, a marquee client, a rare certification).

Pass 3 — cut low-value sections:
- Objective statements: remove entirely.
- Interests or hobbies sections: remove unless directly relevant to the target role.
- References available on request lines: remove.
- GPA: remove unless the user is early-career and GPA is 3.7 or higher.
- High school education: remove if any post-secondary credential exists.

**After each pass**, re-estimate length. Stop as soon as the resume fits. Do not over-trim.

**Trimming report**: After trimming, output a brief itemized list of what was cut and which pass removed it. The user may override any individual cut — flag this explicitly.

**Two-page mode must not**:
- Remove the two most recent roles or any of their primary bullets
- Remove education, degrees, or active certifications
- Remove contact information or target headline
- Fabricate condensed content — if a bullet is cut, it is gone, not reworded into a shorter version that implies something different

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

**Gap analysis** (run as part of every audit):

Parse all employment dates. Flag any gap greater than 2 months between consecutive roles, and any gap between the most recent role's end date and today greater than 3 months.

For each gap found, record:

- Gap period (start and end date)
- Duration in months
- The roles immediately before and after the gap
- Whether any context clue exists in the resume (parenthetical, "Career Break" entry, freelance role, overlapping dates)

Classify each gap:

- **Explained**: The resume already addresses it. No action needed beyond noting it.
- **Unexplained**: No context exists in the resume. Flag as MAJOR, cite `common-patterns § Red flags` (unexplained gaps), and set `MISSING_TIMELINE_CONTEXT`.
- **Overlap**: Two roles share overlapping dates. Flag for the user to verify — may indicate concurrent employment or a title inflation risk.

For each unexplained gap, generate 2-3 framing options based on duration and surrounding context. Present these as options for the user to select and adapt — never insert them into the rewrite without user confirmation.

Framing by duration:

- 2-4 months: "Career transition period", "Targeted job search following [prior role]", "Short-term contract or consulting work"
- 4-9 months: "Career break for personal development", "Caregiver leave", "Relocation and resettlement", "Freelance or contract period"
- 9+ months: "Extended career break (caregiving, health, or relocation)", "Entrepreneurial venture", "Full-time certification or academic study"
- Gaps in early 2020: Note pandemic context — "Career pause during COVID-19 industry disruption"
- Post-layoff context: If the preceding role ended at a known mass-layoff event, note "Consider adding: position eliminated in reduction-in-force, if applicable"

Surface gap findings in the output:

- Unexplained gaps appear as MAJOR issues in Issues by Severity
- `MISSING_TIMELINE_CONTEXT` appears in Missing Data
- Framing options appear in Top Fixes, labeled clearly as options not insertions

**Skills taxonomy validation** (run as part of every audit):

Scan the entire resume — skills sections, bullet points, summaries, and certifications — for tool names, product names, and technology terms that are outdated, deprecated, or renamed. Flag each one with the current preferred name and the reason for the change.

Known substitutions to check (non-exhaustive — apply judgment for any tool that has been renamed, rebranded, or superseded):

- SCCM → Microsoft Configuration Manager (or ConfigMgr)
- SCOM → Microsoft System Center Operations Manager (abbreviated SCOM is still acceptable; flag if the long form is used inconsistently)
- Azure Active Directory / Azure AD → Microsoft Entra ID
- AAD → Microsoft Entra ID
- Office 365 → Microsoft 365
- Exchange Online / EXO → acceptable; flag if "Exchange Server" is listed when the org clearly uses cloud
- Skype for Business → Microsoft Teams (flag if still listed as a current skill)
- Windows 10 Management → flag if listed without also noting Windows 11 readiness for roles dated 2022 or later
- Intune → Microsoft Intune (acceptable abbreviation, but flag if listed as "MDM" generically when Intune is the actual platform)
- PowerBI → Power BI (two words is the current brand style)
- PowerApps → Power Apps (two words)
- PowerAutomate → Power Automate (two words)
- SharePoint Online vs SharePoint Server → flag if version context is ambiguous for a cloud-focused role
- Kubernetes → acceptable; flag if "K8s" is used without spelling it out at least once
- Docker Swarm → flag if listed as a primary orchestration skill without noting Kubernetes, for roles dated 2021 or later where Swarm is largely superseded

For each flagged term:

- Record the outdated term, the preferred term, and the location in the resume
- Classify severity: MINOR if cosmetic, MAJOR if the outdated name signals a skills gap or misalignment with a modern job description
- When a job description is present and uses the current name, escalate to MAJOR if the resume uses the old name

Do not flag abbreviations that are still widely used and unambiguous in context (e.g., "SQL", "VM", "SaaS"). Only flag when the full renamed brand or deprecated product name is the actual issue.

Surface taxonomy findings in the output:

- Each flagged term appears in Audit Findings with current preferred name and severity
- MAJOR taxonomy issues appear in Issues by Severity
- Corrections are applied in the rewritten resume — use the current preferred name everywhere

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

### Step 8: Generate cover letter

Generate a cover letter when either condition is true:

- A job description is present (auto-generate alongside the rewrite — do not ask)
- The user explicitly requests a cover letter, even without a job description

**When a job description is present**, the cover letter must:

- Address the specific role and company named in the job description
- Open without a generic opener — "I am writing to apply for..." is prohibited
- Select 2-3 achievements from the rewritten resume that most directly answer the job's stated requirements
- Mirror language from the job description naturally — same words, not keyword stuffing
- Stay under 400 words and 4 paragraphs
- Close with a direct call to action, not filler phrases ("I look forward to hearing from you" is prohibited)

Cover letter structure:

- **Paragraph 1 (Hook)**: Why this role at this company, stated specifically. Reference something concrete from the job description or the company.
- **Paragraph 2 (Proof 1)**: The single strongest achievement from the rewritten resume that maps directly to the role's top stated need.
- **Paragraph 3 (Proof 2)**: A second achievement or area of fit, with a brief connecting sentence explaining relevance to the role.
- **Paragraph 4 (Close)**: Restate fit in one sentence. Name a specific next step — request for interview, offer to share examples, or similar.

Hard rules:

- Do not repeat resume bullets verbatim. Reframe them as narrative.
- Do not fabricate company details, role details, or achievements not present in the resume.
- Do not add soft skill walls ("I am a passionate, results-driven professional...").

**When no job description is present but a cover letter is explicitly requested**, generate a generic version targeting the most likely role based on resume content. Prepend this label to the output: `Generic version — personalize the hook and company-specific references before sending.`

**Self-validate the cover letter**: Before presenting, confirm the hook references something specific from the JD (or resume target role), both proof paragraphs cite real resume evidence, and the close names a concrete next step.

### Step 9: Produce the output

Apply Output Mode Handling before final response assembly.

Deliver eight sections in the standard order, plus a ninth when two-page mode ran:

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

8. **Cover Letter** (when generated per Step 8)
   - Include the full cover letter text.
   - If generated from a job description, no label is needed.
   - If generated without a job description, prepend the generic-version label.
   - In JSON output, map this content to `cover_letter`. Set to `null` if no cover letter was generated.

9. **Two-Page Trimming Report** (when two-page mode ran)
   - State the estimated pre-trim length and post-trim length.
   - List every item cut, which pass removed it, and the reason.
   - Explicitly note that any cut can be overridden — the user should reply with the item to restore.
   - If no trimming was needed, state "Resume already fits two pages — no content removed."
   - In JSON output, map this content to `two_page_trim_report`. Set to `null` if two-page mode was not active.

If source is not pasted text, always state extraction confidence (High, Medium, or Low) and parsing limitations.

Output mode assembly rules:

- `human`: return only the applicable human-readable sections.
- `json`: return only the JSON object defined by `json-output-spec.md`.
- `both`: return the human-readable sections first, then append a fully conforming JSON object.

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
   - `two_page_trim_report`
   - `notes`

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

## Refresh Tips Workflow

### Step 1: Load the tips workspace

Read these files when present:

- `tips/README.md`
- `tips/sources.json`
- `tips/inbox/`
- `tips/reviewed/`
- `tips/archive/`

Treat this workspace as a staging system:

- `tips/inbox/`: newly captured posts and candidate suggestions
- `tips/reviewed/`: reviewed notes worth keeping as reusable context
- `tips/archive/`: stale, duplicate, or superseded items

### Step 2: Classify the request

Choose the smallest matching action:

- **Refresh run**: create or update a dated weekly review packet, summarize new material, and prepare candidate tip files
- **Review run**: dedupe inbox items, score confidence, and move clear keepers to `reviewed/`
- **Promotion run**: convert reviewed tips into durable principles in `insights/principles.md`

### Step 3: Normalize each candidate tip

Each tip file should capture:

- source name
- source role or source type
- source URL
- published date when known
- fetched or reviewed date
- topic tags
- why it matters
- extracted resume advice
- promotion recommendation

Do not store a long verbatim copy of the full post when a concise summary is enough. Keep enough detail to recover the idea and source.

### Step 4: Evaluate trust level

For each candidate item, label it conceptually as one of:

- **Promote candidate**: specific, actionable, resume-relevant, and consistent with known recruiter behavior
- **Review later**: plausible but needs comparison against other sources
- **Archive**: weak, generic, contradictory, or not resume-focused

Fresh social posts are not automatically principles. If the advice is anecdotal, trendy, or overly specific to one recruiter's workflow, keep it in `tips/` instead of promoting it.

### Step 5: Produce the weekly result

For refresh and review runs, return:

- how many new candidates were added
- how many were moved to `reviewed/`
- how many were archived
- which items look strongest for promotion into `insights/principles.md`

If no new high-value advice was found, say so plainly and keep the workspace unchanged except for the dated review packet if one was requested.

---

## Principles of using this skill

- **Every audit finding must map to a library principle, a pattern in `common-patterns.md`, or be clearly flagged as "Not-in-library observations".** Do not invent principles.
- **Library principles win over patterns** when both apply. Library entries have attribution and specific framing; patterns are the fallback.
- **`tips/` is a staging layer, not the source of truth.** Raw or newly reviewed tips can inform future library growth, but only `insights/principles.md` and `references/common-patterns.md` are authoritative for normal audits.
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
- If `tips/` files cannot be read, continue without them. Do not pretend fresh-source review was performed when the staging files were unavailable.
