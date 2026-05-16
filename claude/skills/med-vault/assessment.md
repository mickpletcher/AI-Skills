# MedVault Assessment

Date: 2026-05-15

## Current state

`med-vault` is a strong concept with substantial draft documentation, but it is not ready to be treated as a finished Claude skill yet.

The folder currently contains `SKILL.md`, `README.md`, upgrade logs, and supporting docs. It does not contain a packaged `.skill` export, helper scripts, templates, schemas as standalone machine readable files, or any runtime that would make the persistence and API behavior in the docs actually happen.

## What is working well

1. The core use case is clear. Medication tracking, interaction review, OCR assisted intake, and schedule generation fit together well.

2. The safety posture is better than average for an early draft. The skill repeats that it is not medical advice and includes emergency escalation guidance.

3. The supporting docs are broad. OCR flow, interaction analysis, scheduling, security, and roadmap material are already mapped out.

4. The user experience is easy to understand. The `mv` command set is simple and memorable.

## Findings

### 1. The skill overstates what is implemented

Severity: High

`SKILL.md` describes behavior as if MedVault can save local JSON files, track audit history, cache interaction results, export files, store image paths, and call external providers. Examples include:

1. Saving and reloading inventory state in local files.
2. Storing image references and audit logs.
3. Querying RxNorm, OpenFDA, and DailyMed.
4. Exporting JSON and card outputs to local folders.

That behavior is described in [`SKILL.md`](./SKILL.md) and the docs, but there are no scripts or packaged helpers in this skill folder to perform those actions. As written, this is a prompt specification, not an implemented local medication vault.

Why this matters:

This is not just a product gap. It is a safety gap. A medical skill cannot imply deterministic storage, OCR confidence scoring, or interaction lookups if those controls do not actually exist.

Recommendation:

Pick one direction and make the docs consistent with it.

1. Prompt only skill: rewrite the skill so it clearly acts as a guided medication organizer inside chat only.
2. Real local vault: add scripts, storage helpers, packaging, and validation that support the documented behavior.

### 2. The skill is not packaged to repo standard

Severity: High

Other Claude skills in this repo are shipped with a `.skill` export and README instructions that point to the packaged artifact. `med-vault` does not include that export. The whole folder is also currently untracked in git.

Why this matters:

Without the packaged export, this skill is not aligned with the current repo pattern and is harder to install, test, and version.

Recommendation:

1. Add `med-vault.skill`.
2. Update the README so it matches the repo standard for source files and packaged import.
3. Track the folder in git once the draft is stable enough to keep.

### 3. The docs conflict with each other

Severity: Medium

There are several mismatches that will confuse the next person who works on this skill.

Examples:

1. `README.md` says to copy only `SKILL.md` into Claude, while other repo skills document both source and packaged install paths.
2. `README.md` says `mv export` supports JSON, Markdown, or Emergency Card. `SKILL.md` says the command exports JSON or PDF summary in the command table, then later describes JSON, Markdown summary, or Emergency Medication Card.
3. `README.md` uses `MedVault/` while `SKILL.md` uses `medvault/`.
4. `docs/roadmap.md` says the release has no external dependencies, but the skill claims online provider lookups and local file persistence.

Recommendation:

Do one consistency pass across `README.md`, `SKILL.md`, and the docs after the product direction is chosen.

### 4. The validation section is aspirational, not verified

Severity: Medium

The checklist in [`SKILL.md`](./SKILL.md) reads like a completed validation matrix, but there is no test evidence, no executable validation harness, and no example outputs tied to actual storage or provider code.

Why this matters:

For a medication skill, validation language should only claim what has been tested. Right now it reads as a release checklist for software that does not exist in the folder.

Recommendation:

Replace the current validation section with one of these:

1. A prompt behavior checklist for a prompt only skill.
2. A real test matrix tied to scripts and example fixtures for an implemented skill.

### 5. The medical safety boundary still needs tightening

Severity: Medium

The disclaimers are present, but the skill still presents interaction severity, symptom guidance, and schedule advice with a level of certainty that is stronger than the current implementation supports, especially in offline mode.

Why this matters:

Medical users may read structured tables and severity labels as verified output, even when the result came from model knowledge rather than a source backed lookup.

Recommendation:

1. Make the source of truth explicit in every result.
2. Downgrade certainty language when no verified source is available.
3. Require a visible verification prompt before any schedule or interaction output is treated as action ready.

## Recommended next steps

1. Decide whether MedVault is a prompt only Claude skill or the design spec for a real local app with helpers.

2. If prompt only, cut the file persistence, export to disk, API integration, cache, and audit log claims from the current docs.

3. If real local vault, add the missing implementation surface first:
   `med-vault.skill`, runtime helpers, storage schema files, example fixtures, and a basic validation path.

4. After that, run one doc normalization pass so README, SKILL, roadmap, and examples all describe the same product.

## Bottom line

MedVault has a solid product idea and a strong documentation draft. It is not release ready in its current state. The biggest issue is the gap between what the docs say the skill does and what the repo actually contains.
