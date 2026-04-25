# resume-writer

A Claude skill for rewriting, auditing, and scoring resumes using a persistent library of recruiter and hiring-manager principles.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [resume-writer.skill](resume-writer.skill) file is the Claude-ready export built from it.

## Overview

This skill has three main modes:

1. `Enhance` mode for rewriting, auditing, and scoring a resume. When a job description is provided, it also auto-generates a matching cover letter.
2. `Add Insight` mode for extracting new principles from recruiter or hiring guidance and adding them to the local library
3. `Refresh Tips` mode for maintaining a weekly staging area of fresh recruiter, HR, and hiring-manager advice before promoting anything into the durable library

It supports human-readable audit output plus structured JSON output for automation.

## How To Use

Use this skill by starting your message with `rw` or by asking for resume rewrite, audit, or scoring directly.

### 1. Enhance Mode (default)

Use when you want your resume reviewed, scored, and rewritten.

Example prompts:

```text
rw review and rewrite this resume for a senior automation engineer role
rw score this resume and show major issues only
rw generate json output for this resume audit
```

If you include a job description, the skill also generates a targeted cover letter automatically.

Example:

```text
rw rewrite this resume for this job description: [paste JD]
```

### 2. Two Page Mode

Use when you need a strict trim to two pages while preserving high-value content.

Trigger phrases include:

```text
rw two page audit
rw trim to two pages
rw fit on two pages
```

This mode returns a trimming report showing what was removed and what can be restored.

### 3. Add Insight Mode

Use when you want to add recruiter guidance into the local principles library.

Example prompts:

```text
rw add this recruiter post to my library: [paste text]
rw add insight from this hiring manager thread
```

### 4. Output Modes

Use these based on your workflow:

1. `human` for standard readable output
2. `json` for machine-readable output only
3. `both` for readable output plus JSON

Example:

```text
rw audit this resume in json mode
```

### 5. Refresh Tips Mode

Use when you want to keep a `tips/` subdirectory current with new post suggestions from recruiters, HR influencers, and hiring managers.

Example prompts:

```text
rw refresh my resume tips library
rw review the latest items in tips/inbox
rw promote the best reviewed tips into the principles library
```

### 6. What You Get Back

Depending on prompt and mode, output can include:

1. Final score summary and verdict
2. Category score breakdown
3. Issues by severity
4. Missing data flags
5. Rewritten resume
6. Cover letter (when JD is present or requested)
7. Two page trimming report (when two page mode is active)

## Core Files

- [SKILL.md](SKILL.md): triggers, workflows, scoring flow, and output rules
- [scoring-model.md](scoring-model.md): deterministic scoring rules
- [json-output-spec.md](json-output-spec.md): machine-readable output contract
- [insights/principles.md](insights/principles.md): persistent recruiter-principle library
- [references/common-patterns.md](references/common-patterns.md): fallback structural patterns and red flags
- [tips/README.md](tips/README.md): staging workflow for fresh recruiter and hiring guidance
- [tips/sources.json](tips/sources.json): curated weekly source roster
- [scripts/Invoke-ResumeTipsRefresh.ps1](scripts/Invoke-ResumeTipsRefresh.ps1): local helper for weekly refresh packets and candidate tip imports
- [scripts/Register-ResumeTipsRefreshTask.ps1](scripts/Register-ResumeTipsRefreshTask.ps1): helper to register the weekly Windows scheduled task

## File Structure

```text
resume-writer/
|-- README.md
|-- SKILL.md
|-- scoring-model.md
|-- json-output-spec.md
|-- scripts/
|   |-- Invoke-ResumeTipsRefresh.ps1
|   |-- Register-ResumeTipsRefreshTask.ps1
|   `-- resume-tip-submissions-template.csv
|-- tips/
|   |-- README.md
|   |-- sources.json
|   |-- inbox/
|   |-- reviewed/
|   `-- archive/
|-- upgrades.md
|-- future-upgrades.md
|-- insights/
|   `-- principles.md
|-- references/
|   `-- common-patterns.md
`-- resume-writer.skill
```

## Upgrade Log

See [upgrades.md](upgrades.md) for a record of implemented upgrades.

## Weekly Tips Workflow

This skill now supports a two-layer knowledge model:

- `insights/principles.md` is the authoritative source used for normal audits
- `tips/` is a staging area for fresh post suggestions that still need review

That separation matters. Social posts can be useful, but they are often anecdotal, trend-driven, or contradictory. The weekly process keeps the skill current without polluting the main principles library.

### What the weekly task does

`[scripts/Invoke-ResumeTipsRefresh.ps1](scripts/Invoke-ResumeTipsRefresh.ps1)` creates a dated weekly review packet and can optionally import post candidates from a CSV into `tips/inbox/`.

It does not try to do brittle authenticated scraping of social feeds. Instead, it gives you a repeatable workflow:

1. Review the curated sources in [tips/sources.json](tips/sources.json)
2. Capture promising posts or articles
3. Drop them into `tips/inbox/`
4. Review and promote only the strongest patterns

### Option 1: Run it manually

From the `resume-writer` folder:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-ResumeTipsRefresh.ps1
```

That creates a file like `tips/weekly-review-2026-04-24.md`.

If you have already collected candidate posts into CSV form, use the included template and import them in the same run:

```powershell
Copy-Item .\scripts\resume-tip-submissions-template.csv .\tips\my-weekly-submissions.csv
powershell -ExecutionPolicy Bypass -File .\scripts\Invoke-ResumeTipsRefresh.ps1 -SubmissionCsvPath .\tips\my-weekly-submissions.csv
```

### Option 2: Register a local weekly Windows task

You can create the scheduled task automatically with the included helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Register-ResumeTipsRefreshTask.ps1
```

That creates a task named `Resume Writer Weekly Tips Refresh` for Mondays at `09:00`.

To customize the schedule:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Register-ResumeTipsRefreshTask.ps1 -DayOfWeek Friday -StartTime 07:30
```

If you prefer to create the task manually, use Windows Task Scheduler:

1. Open `Task Scheduler`
2. Choose `Create Task...`
3. Name it something like `Resume Writer Weekly Tips Refresh`
4. On `Triggers`, add a weekly trigger for the day and time you want
5. On `Actions`, add:
   Program/script:
   `powershell.exe`
   Add arguments:
   `-ExecutionPolicy Bypass -File "C:\Users\mick0\OneDrive\Documents\Code & Dev\GitHub\AI-Skills\claude\skills\resume-writer\scripts\Invoke-ResumeTipsRefresh.ps1"`
   Start in:
   `C:\Users\mick0\OneDrive\Documents\Code & Dev\GitHub\AI-Skills\claude\skills\resume-writer`
6. Save the task and run it once manually to confirm it creates the weekly review file

### Option 3: Use the repo-driven GitHub Action

The repo now includes [resume-writer-tips-refresh.yml](../../../.github/workflows/resume-writer-tips-refresh.yml), which runs on:

1. a weekly schedule
2. manual `workflow_dispatch`

What it does:

1. checks out the repo on `windows-latest`
2. runs `scripts/Invoke-ResumeTipsRefresh.ps1`
3. uploads the generated `weekly-review-*.md` file as a workflow artifact

How to use it:

1. Push this repo to GitHub
2. Open `Actions` in GitHub
3. Run `Resume Writer Tips Refresh` manually, or let the Monday schedule run automatically
4. Download the `resume-writer-weekly-review` artifact from the workflow run

This GitHub Action does not attempt authenticated social scraping. It is meant to keep the weekly review cadence repo-driven and reproducible, while you still decide which sources and posts deserve promotion.

### After any option runs

1. Open the new `tips/weekly-review-<date>.md` packet
2. Visit the listed discovery URLs
3. Capture strong posts into `tips/inbox/`
4. Move good keepers into `tips/reviewed/`
5. Promote only durable ideas into `insights/principles.md`

### Recommended promotion rule

Promote a tip into `insights/principles.md` only when it is:

1. Specific enough to change a resume audit
2. Actionable beyond one niche situation
3. Consistent with other trusted recruiter or hiring-manager guidance
4. Worth citing repeatedly in future resume reviews

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `resume-writer.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
