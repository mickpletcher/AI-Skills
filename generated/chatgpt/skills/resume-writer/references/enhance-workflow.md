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

Apply a role family preset when the target clearly fits one of these:

- infrastructure
- endpoint engineering
- cloud
- support escalation
- leadership

Role family presets should shift emphasis, skills ordering, and proof selection without changing facts.

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

**Recruiter skim view** (run as part of every audit):

Build a first-30-seconds summary that surfaces the top proof points a recruiter should notice immediately. Prefer:

- target headline or likely role fit
- 3 to 5 strongest quantified achievements
- the most relevant tools, domains, or platform depth
- any unusual credibility signal such as leadership scope, rare certification, or major migration or transformation outcome

Keep this view tight and evidence based.

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

**LinkedIn and artifact alignment check** (run as part of every audit when enough data is present):

When the user provides LinkedIn profile text, a LinkedIn export, or references profile wording, check whether the resume and LinkedIn drift on:

- current title or headline
- date ranges
- core platform or technology claims
- seniority framing
- major achievement emphasis

If a cover letter is generated, also check that the role story, dates, and seniority framing stay consistent across resume, LinkedIn, and cover letter artifacts.

Flag:

- `LINKEDIN_ALIGNMENT_GAP` when the profile and resume tell materially different stories
- `ARTIFACT_TIMELINE_MISMATCH` when dates or sequence conflict across resume, LinkedIn, and cover letter context

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

When bullets are too vague, push harder on quantified framing:

- scope: team size, endpoint count, user base, region, budget, or system count
- action: what was actually changed, automated, stabilized, deployed, migrated, or reduced
- outcome: time saved, risk reduced, incidents prevented, SLA improved, cost avoided, or adoption increased

If numbers are unavailable, prefer stronger concrete nouns and outcome language over filler.

### Step 7: Self-validate the rewrite

Before presenting the output, re-audit the rewritten text against the library and patterns. Rewrites frequently introduce new violations — a bullet fixed for specificity can end up too long, a reorganized skills section can drop ATS-relevant keywords.

For each section of the rewrite, check:

- Does every bullet follow action verb / object / outcome?
- Is every quantified claim actually supported by the original, or did a number sneak in that was not there before?
- Did any weak verb ("Responsible for", "Helped with") survive the rewrite?
- Does the final length still fit the target from common-patterns § Length?
- Did any section get longer than its target bullet count?

If the re-audit surfaces issues, fix them silently before presenting. Do not show the user the self-validation pass — it is an internal checkpoint, not part of the deliverable.

**ATS keyword balance check** (when a job description or target role is present): extract the 8 to 12 highest-signal terms from the job description — named tools, certifications, methodologies, and role-specific nouns — and verify each appears in the rewrite where the resume genuinely supports it. Two failure directions, both checked:

- **Missing**: a term the candidate's history supports but the rewrite never uses; work it into the relevant bullet or skills entry naturally
- **Stuffed**: a term appearing more than two or three times, in bullets that do not evidence it, or in an unsupported skills-section pile; cut to the supported instances

Terms the history does not support get listed in Top Fixes as honest gaps, never inserted. The resume should read the same to a human after this check as before it; only placement and coverage change.

**Reference project mapping** (when the user has repos, a portfolio, or public work): for each major bullet, note when a concrete artifact backs it — a GitHub repo, blog writeup, or portfolio piece. Include a short mapping in Top Fixes, such as which repo to link from LinkedIn or mention in an interview for which claim. Do not put raw URLs in the resume body unless the user asks; the map is for the user's preparation, not the page.

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

**Company-type variants**: when the job description or user context signals the company type, tune the letter accordingly; when it is ambiguous, default to the enterprise register:

- **Enterprise**: slightly more formal register, emphasize scale, compliance, process maturity, and cross-team coordination; certifications and platform names carry weight
- **Startup or fast-moving team**: tighter and more direct, emphasize shipping speed, breadth, ownership, and tolerance for ambiguity; one concrete built-it-myself proof point beats a process narrative

If the user asks for both, produce both variants with the same facts and clearly labeled.

**When no job description is present but a cover letter is explicitly requested**, generate a generic version targeting the most likely role based on resume content. Prepend this label to the output: `Generic version — personalize the hook and company-specific references before sending.`

**Self-validate the cover letter**: Before presenting, confirm the hook references something specific from the JD (or resume target role), both proof paragraphs cite real resume evidence, and the close names a concrete next step.

### Step 8b: Interview prep handoff

When the user asks for interview prep, or when a targeted rewrite has enough target-role context to justify it, generate a short interview prep handoff:

- likely questions based on the rewritten resume
- proof points the user should be ready to explain
- talking points for ambiguous or weak areas
- one short story angle for each major target-role requirement when possible

Keep it tied to the actual rewritten resume and target role. Do not fabricate scenarios.

### Step 9: Produce the output

Apply Output Mode Handling before final response assembly.

Deliver the sections below in the standard order, plus the two-page report when two-page mode ran:

1. **Final Score Summary**
   - Final Score
   - Verdict
   - Hire Likelihood Signal
   - Confidence
   - Audit Mode
   - Review Context
   - Job Fit Before Rewrite
   - Job Fit After Rewrite (when a rewrite was requested)

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

6. **Recruiter Skim View**
   - Top proof points for the first 30 seconds
   - Short target-role fit framing when enough context exists

7. **Rewritten Resume (if requested)**
   - Include this section when the request is in rewrite mode or the user explicitly requests a rewrite.
   - If input was .docx, produce .docx using the available document tooling when the environment supports it, preserving any letterhead or formatting when possible.
   - If input was .pdf, produce .docx by default.
   - If input was paste or image, produce Markdown unless the user asks for .docx.
   - In JSON output, map this content to `rewritten_resume`.

8. **Top Fixes / Next Steps**
   - List highest impact improvements first.
   - Include missing metrics and follow up items.
   - Include any "Not-in-library observations".
   - If any Not-in-library observation recurs, offer to add it as a principle.

9. **Cover Letter** (when generated per Step 8)
   - Include the full cover letter text.
   - If generated from a job description, no label is needed.
   - If generated without a job description, prepend the generic-version label.
   - In JSON output, map this content to `cover_letter`. Set to `null` if no cover letter was generated.

10. **Interview Prep Handoff** (when generated per Step 8b)
   - Include likely questions and talking points.
   - In JSON output, map this content to `interview_prep_handoff`. Set to `null` if not generated.

11. **Two-Page Trimming Report** (when two-page mode ran)
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
