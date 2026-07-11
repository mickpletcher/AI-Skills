---
agent: agent
description: Upgrade the Claude astrophotography-processing skill into an evidence-driven, non-destructive processing copilot with tested diagnostic tools and optional AI-model adapters.
---

# Upgrade the astrophotography-processing skill

Act as the implementation agent for the existing Claude skill at
`claude/skills/astrophotography-processing/`.

Read this entire prompt before editing. Inspect the repository and current files first. Do not
assume that the working tree is clean or that the skill still matches the baseline described here.

## How to invoke this prompt

Run this prompt from GitHub Copilot Chat in agent mode with:

```text
/upgrade-astrophotography-processing phase=1
```

Replace `phase=1` with the phase to implement. If no phase is supplied, inspect the repository,
report current status, and recommend the next incomplete phase without changing files.

Implement one phase at a time unless the user explicitly requests multiple phases. At the end of
each phase, run the relevant tests and report changed files, validation results, assumptions, and
remaining work.

## Primary objective

Turn the skill from a broad advisory router into an evidence-driven astrophotography copilot that
can safely inspect datasets, produce diagnostic artifacts, recommend processing workflows, invoke
approved external tools, and validate before-and-after results.

Keep Claude as the reasoning, workflow-selection, diagnosis, and quality-control layer. Reuse
established astronomical processing engines rather than attempting to recreate PixInsight, Siril,
Astro Pixel Processor, or DeepSkyStacker.

## Required repository context

Read these files before making changes:

- `shared/skill-standard.md`
- `shared/platform-organization.md`
- `shared/naming-conventions.md`
- `claude/skills/astrophotography-processing/SKILL.md`
- every file under `claude/skills/astrophotography-processing/references/`
- every file under `claude/skills/astrophotography-processing/scripts/`
- `claude/skills/astrophotography-processing/README.md`
- `claude/skills/astrophotography-processing/templates/processing-log.md`
- `claude/scripts/README.md`
- `claude/scripts/Validate-SkillFolders.ps1`
- `claude/scripts/Validate-SkillQuality.ps1`

Also inspect:

```bash
git status --short
git diff -- claude/skills/astrophotography-processing
find claude/skills/astrophotography-processing -maxdepth 3 -type f -print | sort
```

Preserve unrelated modifications. Do not reformat, stage, revert, or overwrite files outside this
skill unless the user explicitly expands the scope.

## Product principles

Apply these principles throughout the implementation:

1. Never overwrite original RAW, FITS, XISF, SER, AVI, MOV, or source TIFF files.
2. Default to read-only inspection and dry-run behavior.
3. Separate observations from hypotheses and recommendations.
4. Preserve linear masters, FITS headers, WCS, acquisition metadata, and processing provenance.
5. Treat scientific and aesthetic outputs as separate products.
6. Never insert pixels from Hubble, JWST, a generative model, or another reference image into the
   user's data without an explicit, separately labeled compositing workflow.
7. Never describe generative super-resolution as recovered detail.
8. Use AI models only at processing stages for which they were designed.
9. Make every destructive or nonlinear action explicit and reversible through separate outputs.
10. Prefer deterministic scripts for audits and measurements; use Claude for interpretation and
    workflow selection.
11. Do not automatically delete or reject subframes. Score and flag them with reasons.
12. Avoid universal numeric recipes. Provide starting ranges and measurable acceptance checks.

## Scope boundaries

### In scope

- Claude skill metadata and routing improvements.
- FITS/XISF/TIFF/PNG/JPEG dataset inspection where supported by installed dependencies.
- Calibration-set compatibility reports.
- Robust linear preview generation.
- Subframe-quality measurement and ranking.
- Processing-plan generation.
- Before-and-after image comparisons.
- Provenance and processing logs.
- Optional adapters for separately installed AI or astronomy tools.
- Tests, fixtures generated at test time, documentation, and package regeneration.

### Out of scope

- Building a desktop or web application.
- Implementing a full calibration, registration, or stacking engine from scratch.
- Downloading or bundling neural-network weights without explicit authorization and verified terms.
- Circumventing commercial licenses.
- Training a new foundation model.
- Hubble-guided pixel synthesis.
- Automatically publishing packages or pushing changes.
- Deleting existing user planning files or unrelated repository content.

## Target runtime structure

Move toward this structure only as each file becomes necessary:

```text
claude/skills/astrophotography-processing/
├── SKILL.md
├── README.md
├── assets/
│   └── processing-log.md
├── references/
│   ├── ai-processing-and-validation.md
│   ├── artifact-decision-trees.md
│   ├── broadband-osc.md
│   ├── calibration-validation.md
│   ├── comets-and-mosaics.md
│   ├── integration-and-rejection.md
│   ├── milky-way-landscape.md
│   ├── mono-lrgb.md
│   ├── narrowband-sho-hoo.md
│   ├── planetary-lunar-solar.md
│   ├── scientific-photometry.md
│   └── tool-integrations.md
├── scripts/
│   ├── audit_dataset.py
│   ├── compare_stages.py
│   ├── generate_processing_plan.py
│   ├── make_linear_preview.py
│   ├── score_subframes.py
│   ├── requirements.txt
│   └── model_adapters/
└── tests/
```

Do not create placeholder files. Retain useful existing references until their content has been
merged into a replacement. Avoid duplicating the same guidance across `SKILL.md` and references.

## Phase 1: Correct metadata, routing, and package hygiene

### Goals

- Make the skill reliably discoverable.
- Keep the main instructions concise.
- Correct inconsistent workflow ordering.
- Establish accurate promises about what scripts can do.

### Required changes

1. Update `SKILL.md` frontmatter so the `description` contains both capability and trigger terms.
2. Prefer portable `name` and `description` metadata. Retain extra Claude-specific fields only if
   the repository's current target and validator explicitly require them.
3. Include triggers for deep-sky, broadband, narrowband, OSC, mono LRGB, planetary, lunar, solar,
   Milky Way, comet, mosaic, FITS, XISF, RAW, calibration frames, stacking, diagnostics, and the
   supported software ecosystem.
4. Keep `SKILL.md` under 500 lines and make it a router, not an encyclopedia.
5. Add an explicit execution policy:
   - inspect first;
   - summarize evidence;
   - propose the smallest confirming test;
   - execute only safe authorized operations;
   - validate output;
   - preserve provenance.
6. Correct the Siril ordering inconsistency. Explain that crop and background correction normally
   precede photometric or spectrophotometric color calibration, while allowing tool- and
   data-specific exceptions.
7. Make scientific, aesthetic, and diagnostic branches explicit.
8. Move the processing-log template from `templates/` to `assets/` if doing so matches the current
   repository packaging convention. Update every reference to it.
9. Remove `.DS_Store` from the skill source and package if it is tracked or packaged. Do not touch
   global ignore rules without separate authorization.
10. Ensure every resource named by `SKILL.md` exists.

### Acceptance checks

- The description alone is sufficient to trigger the skill for realistic astrophotography prompts.
- No runtime behavior is promised without an existing script or clearly labeled future phase.
- Scientific mode forbids generative enhancement and preserves an analysis master.
- The package contains no `.DS_Store` or stale duplicate resource.
- Existing repository validators pass for this skill, or every pre-existing validator conflict is
  reported precisely.

## Phase 2: Dataset audit and calibration compatibility

Detailed implementation specification: `specs/003-astrophotography-processing-phase-2/`. Treat that
specification as authoritative if this shorter phase summary differs from it.

### Goal

Replace the basic `fits_audit.py` table with an evidence-producing dataset audit.

### Implement `scripts/audit_dataset.py`

Required behavior:

- Accept a file or directory.
- Recursively discover supported files while excluding generated output directories by default.
- Support `.fit`, `.fits`, `.fts`, and gzip-compressed FITS.
- Add optional XISF and camera-RAW metadata support only when a reliable installed library is
  available; otherwise report the missing optional capability without failing the FITS audit.
- Inspect the first image-bearing FITS extension and merge relevant primary/extension metadata
  without silently hiding conflicts.
- Print relative paths, not only basenames.
- Classify probable light, dark, flat, bias, dark-flat, master, and unknown frames using headers
  first and filenames only as a labeled fallback.
- Capture at least:
  - image type;
  - dimensions and data type/bit depth;
  - exposure;
  - filter;
  - camera/instrument;
  - gain setting and electronic gain as distinct concepts;
  - offset;
  - sensor/set temperature;
  - X and Y binning;
  - Bayer pattern;
  - object;
  - observation time;
  - session/date;
  - WCS presence;
  - relevant calibration/master flags.
- Group comparable frames by session, frame type, filter, exposure, gain, offset, temperature,
  binning, dimensions, camera mode, and Bayer pattern.
- Calculate exposure counts and total integration time by light-frame group.
- Produce calibration-compatibility findings, including missing groups and mismatches.
- Detect unreadable files, duplicate paths/content when practical, conflicting headers, and mixed
  geometry.
- Never claim a mismatch when metadata is absent. Report `unknown` and the evidence needed.

### Command-line interface

Provide at least:

```text
audit_dataset.py INPUT
audit_dataset.py INPUT --format text
audit_dataset.py INPUT --format json --output process/audit.json
audit_dataset.py INPUT --format csv --output process/audit.csv
audit_dataset.py INPUT --output-dir process/
```

Use stable exit codes:

- `0`: audit completed, including completed audits with warnings;
- `1`: missing dependency or partial capability that prevents the requested format/type;
- `2`: invalid input or arguments;
- `3`: no supported files;
- `4`: fatal read/audit failure.

Send warnings and errors to stderr. Keep machine-readable stdout clean.

### Output schema

Version the JSON schema in the output. Include:

- `schema_version`;
- `generated_at`;
- `input_root`;
- `capabilities`;
- `files`;
- `groups`;
- `integration_summary`;
- `calibration_findings`;
- `warnings`;
- `errors`.

Do not put absolute user paths into reports unless the user requests them.

### Compatibility rules

- Darks: compare exposure, gain/ISO, offset, temperature, binning, sensor/readout mode, and geometry.
- Flats: compare filter, optical path assumptions when known, focus/rotation only when metadata or
  user notes support it, gain/ISO, binning, and geometry.
- Dark-flats: compare flat exposure, gain/ISO, offset, temperature, binning, and mode.
- Bias: do not recommend combining bias and dark-flats blindly.
- Warn that dark optimization/scaling can be inappropriate for some CMOS sensors; do not encode a
  universal prohibition.

### Tests

Generate synthetic FITS fixtures in temporary directories. Test:

- primary-header metadata;
- metadata in an image extension;
- conflicting headers;
- duplicate basenames in different directories;
- missing metadata;
- mixed dimensions and binning;
- calibration grouping;
- compressed FITS when supported;
- JSON and CSV validity;
- stable exit codes;
- output-directory exclusion.

Retain `fits_audit.py` temporarily as a compatibility wrapper with a deprecation message, or update
all callers and remove it only after confirming nothing depends on it.

## Phase 3: Linear previews and measurable image diagnostics

### Implement `scripts/make_linear_preview.py`

Required behavior:

- Read FITS and high-bit TIFF; add XISF only through a reliable optional dependency.
- Preserve source files and write only under an explicit output directory, defaulting to
  `process/` beside the selected input root.
- Exclude `process/`, `exports/`, caches, and generated previews during recursive scans.
- Produce unique collision-resistant filenames based on relative paths or short hashes.
- Use robust statistics rather than raw extrema and mean alone.
- Calculate per-channel median, MAD or robust sigma, selected percentiles, finite-pixel count,
  low/high clipping fractions, and dynamic range.
- Provide linked and unlinked channel stretch modes.
- Implement a documented, deterministic STF-like or percentile/MAD autostretch for preview only.
- Never write the preview stretch back into the scientific master.
- Produce a PNG preview and JSON sidecar containing exact statistics and stretch parameters.
- Optionally produce histogram and clipping visualizations.
- Handle NaN, infinity, negative floating-point values, mono images, RGB images, and unsupported
  channel layouts explicitly.

### Keep or replace `image_stats_preview.py`

Do not leave two competing implementations. Either:

- turn it into a compatibility wrapper; or
- migrate all references and remove it after tests confirm the replacement.

### Tests

Test mono/RGB, uint16/float32, negative values, NaN/Inf, dark linear data, duplicate basenames,
output exclusion, deterministic sidecars, and graceful unsupported formats.

## Phase 4: Subframe scoring and processing plans

### Implement `scripts/score_subframes.py`

Measure, where dependencies and data permit:

- star count;
- FWHM or HFR;
- eccentricity;
- background median;
- robust noise;
- SNR proxy;
- saturation fraction;
- gradient strength;
- registration shift for registered inputs.

Rank only within comparable groups, normally the same filter, binning, exposure family, and
session. Use robust statistics and explain every flag. Never automatically delete, move, or reject
a subframe.

Outputs must include CSV and JSON plus an optional contact sheet or plots. Clearly distinguish
measured values, derived scores, and heuristic flags.

### Implement `scripts/generate_processing_plan.py`

Consume an audit JSON file and generate:

- a human-readable Markdown plan;
- a machine-readable JSON plan;
- explicit assumptions and unresolved questions;
- proposed inputs and outputs;
- software-specific route selection;
- checkpoints after calibration, registration, integration, linear correction, AI processing,
  stretch, and export;
- a dry-run command list where supported.

The generator must not process images. It creates a plan for Claude and the user to review.

## Phase 5: AI-model and external-tool adapters

### Architecture

Create a small adapter interface rather than hard-coding each tool throughout the skill. Each
adapter must declare:

```yaml
name: tool-or-model-name
task: denoise | sharpen | remove-stars | remove-gradient | cosmic-rays
expected_stage: calibrated-sub | linear-integration | nonlinear-image
input_types: []
input_range: documented-or-unknown
supports_linear: true
supports_color: true
scientific_safe: false
license_mode: open | external-user-install | commercial-user-license
version: detected-at-runtime
```

### Initial providers

Support only through documented and legally appropriate mechanisms:

- GraXpert: external CLI for background extraction and denoising; save the background model when
  possible.
- Cosmic Clarity: external executable initially. Embed ONNX weights only after the user explicitly
  authorizes it and the model-weight license is verified separately from source-code licensing.
- StarNet2 and DeepSNR: user-installed external command-line tools; do not redistribute.
- RC Astro tools: optional user-installed, user-licensed CLI; never bypass licensing.
- deepCR or Cosmic-CoNN: optional scientific cosmic-ray detection on supported calibrated data;
  require instrument/domain checks and return masks/probabilities before inpainting.

### Safety requirements

- Default every adapter to dry-run.
- Detect executable and version before building a command.
- Validate expected input stage, sample type, bit depth, channels, and supported file types.
- Refuse silent conversion from 32-bit linear data to 16-bit unless the user approves a separate
  intermediate and the conversion is logged.
- Record executable version, model version, parameters, input/output hashes, timestamps, and
  command line in provenance.
- Never download models automatically.
- Never treat output from a generative or super-resolution model as scientific ground truth.

## Phase 6: Before-and-after validation

### Implement `scripts/compare_stages.py`

Required outputs:

- identically normalized before/after previews;
- an absolute and signed difference visualization;
- per-channel histogram/statistics comparison;
- changes in clipping;
- background noise comparison;
- star-count, star-profile, saturation, and FWHM changes when measurable;
- optional tiled HTML or PNG contact sheet;
- JSON findings for Claude to interpret.

The script must not declare that AI output is better. It reports measurable changes and flags
possible failure modes such as:

- erased faint structures;
- halos or ringing;
- tile seams;
- invented high-frequency texture;
- altered star cores or color;
- excessive background flattening;
- new clipping.

## Phase 7: Deepen references and decision trees

Rewrite generic checklist references into concise decision guidance. Cover at least:

- calibration validation, pedestal/clipping, CMOS dark-scaling cautions, flats and light leaks;
- rejection selection based on stack size and contamination;
- local normalization and multi-night processing;
- drizzle eligibility based on sampling, dithering, registration quality, and SNR;
- broadband OSC processing;
- mono LRGB combination and channel weighting;
- SHO, HOO, dual-band extraction, continuum/star handling, and restrained palette guidance;
- HDR targets and bright-core protection;
- star separation/recombination validation;
- Milky Way tracked-sky/static-foreground blending;
- planetary/lunar/solar frame selection, alignment, sharpening, and solar safety;
- comet star-aligned/comet-aligned integrations and mosaics;
- scientific photometry, WCS, linearity, uncertainty, masks, and provenance;
- AI model selection and validation.

For common artifacts, create branching decision trees that identify the first stage where the
problem appears and specify the smallest confirming test. Include dust motes, flat over/under
correction, walking noise, banding, gradients, halos, magenta stars, registration doubles,
clipping, ringing, tilt/backfocus, and color blotching.

## Phase 8: Documentation, validation, and packaging

### README

Update the source README to explain:

- which file is the editable source of truth;
- how to install or import the `.skill` package;
- optional Python dependencies;
- external-tool integrations and licensing boundaries;
- a minimal validation prompt;
- where diagnostic outputs are written;
- that originals are never modified.

Keep implementation planning and changelog prose out of the runtime package unless repository
conventions require them.

### Dependencies

Use a minimal pinned-compatible dependency declaration. Prefer broadly compatible lower bounds
over exact pins unless reproducibility requires exact versions. Imports for optional capabilities
must be lazy and must provide actionable errors.

Do not install dependencies globally or modify the user's Python environment without permission.

### Tests and validation

Run the commands that exist on the current platform. At minimum:

```bash
python3 -m py_compile claude/skills/astrophotography-processing/scripts/*.py
python3 -m pytest claude/skills/astrophotography-processing/tests -q
python3 claude/skills/astrophotography-processing/scripts/audit_dataset.py --help
python3 claude/skills/astrophotography-processing/scripts/make_linear_preview.py --help
python3 claude/skills/astrophotography-processing/scripts/score_subframes.py --help
python3 claude/skills/astrophotography-processing/scripts/compare_stages.py --help
```

If PowerShell is available, inspect script help first and run the repository validators scoped as
narrowly as possible. Do not repair unrelated repository findings.

Also verify:

- every Markdown link in `SKILL.md` resolves;
- no script writes outside its requested output directory;
- recursive scans exclude generated output;
- machine-readable outputs contain no progress text;
- all scripts return documented exit codes;
- tests use temporary directories;
- no neural-network weights or large binary fixtures were added unintentionally.

### Package regeneration

Rebuild `astrophotography-processing.skill` only after all source validation passes. Inspect the
existing archive layout before replacing it. The archive must open with a standard ZIP reader and
place `SKILL.md` at the expected package root.

Exclude at least:

- `.DS_Store`;
- `__pycache__/` and bytecode;
- `.pytest_cache/`;
- test output and temporary fixtures;
- the `.skill` archive itself;
- local-only future planning files;
- unrelated repository documentation.

After rebuilding, list archive contents and confirm that the packaged runtime matches source files.

## Coding standards

- Target Python 3.10 or newer unless repository constraints require otherwise.
- Use `pathlib` and type hints.
- Keep core computation separate from CLI formatting.
- Use dataclasses or typed dictionaries for stable records where useful.
- Use the `logging` module for human diagnostics and stderr for CLI warnings/errors.
- Avoid mutable global configuration.
- Make algorithms deterministic unless an explicit seed is exposed and recorded.
- Document units for every numerical field.
- Do not silently normalize, clip, debayer, stretch, or change color spaces.
- Keep output schemas versioned.
- Write concise docstrings that state inputs, outputs, side effects, and scientific limitations.

## Completion report

At the end of each requested phase, report:

1. Outcome first.
2. Files changed.
3. Tests and commands run, with pass/fail status.
4. Assumptions and limitations.
5. Any licensing or dependency issue requiring user action.
6. The recommended next phase.

Do not claim completion if tests were skipped because dependencies were unavailable. Distinguish
code validation from full functional validation on real astronomical data.

## Final definition of done

The overall upgrade is complete only when:

- Claude can inspect a dataset and cite concrete evidence from generated reports;
- calibration groups and mismatches are reported cautiously;
- useful stretched previews can be generated from linear data without modifying it;
- subframes can be scored without automatic deletion;
- a reviewable processing plan can be generated;
- optional AI tools are invoked through license-respecting adapters;
- before-and-after outputs are measured and compared;
- scientific and presentation workflows remain separated;
- all scripts have automated tests and documented exit behavior;
- the `.skill` package is current, clean, and installable;
- no original astronomical data is ever overwritten.
