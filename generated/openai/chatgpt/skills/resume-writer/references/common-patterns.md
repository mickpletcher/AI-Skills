# Common Resume Patterns

Universal structural and formatting patterns that apply regardless of library content. This file is the canonical source for length, section order, bullet mechanics, typography, file format, and red flags. Attributed insights with named sources live in `insights/principles.md` instead.

## How to cite patterns in an audit

When a rewrite is driven by a pattern in this file rather than a library principle, cite it as:

```text
common-patterns § <section name>
```

For example: `common-patterns § Bullet length`, `common-patterns § Content patterns to cut`, `common-patterns § Red flags recruiters look for`.

When both a library principle and a pattern cover the same violation, cite the library principle (see the precedence rule in `insights/principles.md`).

## Audit wording conventions

Use these terms consistently across outputs:

- **Condensed audit**: default grouped findings by section, focused on highest value fixes.
- **Full forensic audit**: line by line detail only when explicitly requested.
- **Missing data**: concrete details the user must supply to improve evidence quality.
- **Not-in-library observations**: real weaknesses not covered by current library principles.

---

## Structural patterns

### Section order (for most mid-to-senior roles)

1. **Contact block** — name, phone, email, city/state, LinkedIn, GitHub if relevant
2. **Summary or profile** — 2-4 lines. Not objective statements. Not "seeking opportunity to leverage..."
3. **Experience** — reverse chronological, most detail on most recent roles
4. **Skills** — grouped, not a wall of keywords
5. **Education** — degree, school, year. No GPA after 5+ years of experience
6. **Certifications** — grouped and ordered by relevance, not alphabetically
7. **Optional** — publications, speaking, open source, patents

Deviations are allowed for specific contexts (academic CV, federal resume, creative portfolio), but the default is this order.

### Reverse chronology

Within experience, always reverse chronological. Functional resumes (skills-first, then a list of employers) signal gaps or career changes and trigger recruiter suspicion. If there is a real gap, address it directly with a one-line "Career break: [dates] - [reason]" rather than obscuring it.

### Collapse old roles

Roles older than 10-12 years should be collapsed into a single "Earlier Experience" line listing employers, titles, and dates, with no bullets. Exception: if a very old role is uniquely relevant to the target position.

---

## Bullet structure

### Action verb, object, outcome

The strongest bullet pattern is `<strong verb> <specific object> <quantified outcome>`.

- Weak: "Worked on improving system reliability"
- Medium: "Improved system reliability through monitoring changes"
- Strong: "Rebuilt Prometheus alerting across 40 services, cutting false-positive pages from 120/week to 8/week"

### Avoid weak verbs

Cut these from the start of bullets: "Responsible for", "Helped with", "Assisted in", "Worked on", "Participated in", "Involved in". They describe presence, not contribution.

Prefer: Led, Built, Shipped, Migrated, Designed, Reduced, Increased, Automated, Replaced, Consolidated, Launched, Scaled, Negotiated, Recovered, Eliminated.

### Bullet length

Target 1-2 lines per bullet. A 3-line bullet is acceptable only if it is the single strongest achievement in the section. Bullets longer than 3 lines are always wrong.

### Bullets per role

Most recent role: 4-6 bullets. Prior role: 3-5 bullets. Older roles: 2-3 bullets. Collapsed roles: 0 bullets.

---

## Formatting patterns

### Length

- Under 5 years experience: 1 page, hard limit
- 5-15 years: 2 pages maximum
- 15+ years, executive/architect: 2 pages, 3 only if truly required (rare)

Length is a filter, not a target. Recruiters spend under a minute on the first pass. Inability to cut signals inability to prioritize.

### Typography

- One font family, one accent color maximum
- 10-11pt body, 11-14pt headers
- Adequate white space. Dense walls of text signal poor judgment.

### File format

- PDF for applications unless the ATS specifically asks for .docx
- Filename: `FirstName_LastName_Role.pdf` — not `resume_final_v7_REAL.pdf`

### No photos, no headshots, no personal data

In the US resume context, never include a photo, date of birth, marital status, or national origin. Exception: countries where it is standard practice (Germany, some Asian markets).

### ATS-safe layout

- Single-column layout parses reliably. Two-column layouts often get scrambled by ATS parsers.
- Do not put contact info, dates, or section headers in headers/footers — many ATS tools skip those regions.
- Avoid tables, text boxes, and graphics for content the ATS must read.
- Use standard section headers ("Experience", "Education", "Skills") rather than creative alternatives ("Where I have Been", "What I Know").

---

## Content patterns to cut

### Objective statements

"Seeking a challenging position where I can leverage my skills to contribute to organizational success." Cut. Replace with a 2-3 line summary of who you are and what you deliver.

### References available upon request

Cut. This is assumed. It wastes a line.

### Soft skill walls

"Detail-oriented, team player, excellent communicator, self-starter, fast learner, passionate about innovation." Cut. These are unverifiable claims everyone makes. Demonstrate them through bullets instead.

### Skills keyword dumps

A comma-separated list of 60 technologies signals no depth in any of them. Group by category (Languages, Cloud, Tooling, Data) and cap at 4-6 items per category. If you know more than that in a category, pick the ones most relevant to the target role.

### Dates in month-year vs year format

Use month-year (Jan 2022 - Mar 2024) for roles under 2 years. Year-only (2022 - 2024) is acceptable for longer roles but month-year is always safer.

---

## Red flags recruiters look for

- **Unexplained gaps over 6 months** — address them directly with a one-line explanation
- **Job hopping under 18 months with no upward trajectory** — group short roles or explain
- **Title inflation** — "CEO" of a 2-person LLC with no revenue will be scrutinized
- **Generic headline** — "Experienced IT Professional" tells the recruiter nothing
- **AI-generated tells** — em dashes used inconsistently, "leverage" and "synergy" and "passionate about" appearing more than once, overly polished language that does not match the rest of the document
- **Inconsistent tense** — past roles should be past tense; current role can be present tense, but stay consistent within each role
