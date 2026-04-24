# resume-writer

A Claude skill for rewriting, auditing, and scoring resumes using a persistent library of recruiter and hiring-manager principles.

## Source of Truth

Use [SKILL.md](SKILL.md) as the canonical source for this skill. The packaged [resume-writer.skill](resume-writer.skill) file is the Claude-ready export built from it.

## Overview

This skill has two main modes:

1. `Enhance` mode for rewriting, auditing, and scoring a resume. When a job description is provided, it also auto-generates a matching cover letter.
2. `Add Insight` mode for extracting new principles from recruiter or hiring guidance and adding them to the local library

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

### 5. What You Get Back

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

## File Structure

```text
resume-writer/
|-- README.md
|-- SKILL.md
|-- scoring-model.md
|-- json-output-spec.md
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

## Implement In Claude

1. Update the checked-in source files for this skill first.
2. Rebuild `resume-writer.skill` from the current source files. Include any supporting runtime files the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place it in your local Claude skills directory if you manage skills manually.
4. Start a new Claude chat or refresh available skills, then test with one of the trigger phrases or example requests from this README.
