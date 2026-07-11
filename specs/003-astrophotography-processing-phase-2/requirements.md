<!-- markdownlint-disable MD013 -->

# 003 Astrophotography Processing Phase 2 Requirements

## Change Summary

Define and implement a read-only dataset audit for the Claude `astrophotography-processing` skill. Phase 2 must turn folders of astronomical files into trustworthy, machine-readable evidence about frame inventory, metadata consistency, integration time, and calibration compatibility.

## User Outcome

Given a file or folder of astrophotography data, Claude must be able to run one deterministic audit and answer:

- What files and frame types are present?
- Which sessions, filters, exposures, camera settings, and geometries occur?
- How much light-frame integration time exists per comparable group?
- Which calibration groups appear compatible, incompatible, missing, or impossible to assess?
- Which metadata conflicts, unreadable files, or structural problems require attention?
- What evidence supports each conclusion?

## Phase Boundary

Phase 2 is a metadata and structural audit. It must not:

- calibrate, debayer, register, stack, stretch, denoise, sharpen, or alter images;
- score stars, FWHM, eccentricity, gradients, or image noise;
- load full pixel arrays unless a user explicitly requests checksum verification or another operation that requires data access;
- reject, move, rename, delete, or overwrite files;
- download dependencies, tools, models, or reference data automatically.

Pixel-level diagnostics and linear previews belong to Phase 3. Subframe scoring belongs to Phase 4.

## Functional Requirements

### FR-1 Input Discovery

The audit must accept one file or one directory. Directory scans must be recursive by default and must not follow symbolic-link directories unless explicitly requested.

The core must recognize:

- `.fit`
- `.fits`
- `.fts`
- `.fit.gz`
- `.fits.gz`
- `.fts.gz`
- tiled-compressed FITS commonly named `.fz`

Generated and administrative folders must be excluded by default, including `process`, `exports`, `.git`, `__pycache__`, and `.pytest_cache`.

### FR-2 FITS-First Core

FITS support must be the required core capability and use `astropy.io.fits` in read-only mode. The implementation must handle primary images, image extensions, and `CompImageHDU` without assuming that image data lives in the primary HDU.

### FR-3 Optional Format Adapters

XISF and camera RAW must be optional capabilities:

- XISF metadata may use a separately installed `xisf` package, but the project must not vendor that GPL-licensed implementation or make it a core dependency.
- Camera RAW metadata should prefer a separately installed ExifTool subprocess adapter. `rawpy` may be detected for limited structural metadata but must not be used to convert or post-process RAW data in Phase 2.
- Missing optional adapters must be reported as capability limitations, not as a failed FITS audit.

### FR-4 HDU Inventory and Selection

For each FITS file, the audit must inventory every HDU and select one primary science/image HDU for normalized metadata. Selection must be deterministic and recorded.

Selection priority:

1. the primary HDU when it contains a supported 2D or 3D image;
2. a supported image HDU named `SCI`;
3. the first supported image-bearing `ImageHDU` or `CompImageHDU`;
4. no selection when no supported image exists.

The report must retain the full HDU inventory so HST, JWST, and other multi-extension files are not misrepresented as simple amateur frames.

### FR-5 Metadata Normalization with Provenance

Normalize common metadata fields without discarding source information. Every normalized value must retain:

- source format;
- HDU index/name or XISF/EXIF source;
- source keyword/tag;
- raw value;
- normalized value;
- normalized unit where applicable;
- confidence;
- conflicts or parse warnings.

Selected-extension values take precedence for structural metadata. For observational metadata, use the selected extension first and the primary header only when the selected extension lacks a usable value. Never silently overwrite conflicting values.

### FR-6 Normalized Fields

Capture at least:

- relative path and file size;
- file format and compression form;
- HDU inventory and selected HDU;
- dimensions, axes, sample/data type, `BITPIX`, `BSCALE`, `BZERO`, and `BUNIT`;
- frame type;
- master/processed-state indicators when present;
- exposure duration in seconds;
- filter;
- instrument/camera and telescope;
- camera gain setting;
- conversion/electronic gain in electrons per ADU as a separate field;
- ISO;
- offset;
- measured sensor temperature and set temperature in degrees Celsius as separate fields;
- X and Y binning;
- pixel size when present;
- Bayer pattern, X/Y Bayer offsets, and row order;
- readout/camera mode when present;
- object name;
- observation start time and time scale/assumption;
- session/date grouping value;
- WCS presence, celestial-WCS validity, and distortion presence;
- FITS checksum presence and optional verification result;
- FITS structural-verification warnings.

### FR-7 Frame Classification

Classify probable `light`, `dark`, `flat`, `bias`, `dark-flat`, `master`, `processed`, or `unknown` frames.

Classification evidence priority:

1. explicit header/property value;
2. combination of multiple header properties;
3. filename/folder inference;
4. unknown.

Each classification must include a confidence category and evidence list. A filename-based classification must never be presented as header-confirmed.

### FR-8 Grouping

Create comparable file groups using normalized frame type, session, filter, exposure family, gain/ISO, offset, temperature family, X/Y binning, dimensions, instrument, readout mode, Bayer pattern, row order, and pixel type as applicable.

Unknown values must remain explicit. They must not be coerced to zero, an empty string, or an assumed default.

### FR-9 Integration Summary

Calculate file count and total light-frame integration seconds per comparable light group. Exclude unknown or invalid exposure values from the total and report the excluded count.

### FR-10 Calibration Compatibility

Compare groups rather than every individual file pair. Findings must use these states:

- `compatible`
- `compatible_within_tolerance`
- `incompatible`
- `missing`
- `unknown`
- `not_applicable`

Compatibility must be evidence-based:

- darks: exposure, gain/ISO, offset, temperature, binning, geometry, instrument, readout mode;
- flats: filter, gain/ISO, binning, geometry, instrument, Bayer/row-order compatibility, and optical-path metadata when available;
- dark-flats: flat exposure, gain/ISO, offset, temperature, binning, geometry, instrument, readout mode;
- bias: gain/ISO, offset, temperature when relevant, binning, geometry, instrument, readout mode.

Do not infer focus position, camera rotation, dust movement, or optical-path sameness when metadata is absent.

### FR-11 Tolerances

Expose tolerances as CLI/configuration values and include effective values in the output. Initial defaults may be conservative starting points, but documentation must state that they are audit tolerances, not universal calibration laws.

At minimum expose:

- exposure absolute tolerance in seconds;
- exposure relative tolerance;
- temperature tolerance in degrees Celsius;
- date/session gap threshold;
- optional numeric gain/offset tolerance, defaulting to exact matching.

### FR-12 Integrity Checks

Provide optional, off-by-default checks for:

- FITS standard verification in warning-only mode;
- `CHECKSUM` and `DATASUM` verification when cards exist;
- full-file SHA-256 duplicate detection.

Do not use approximate hashes to declare files identical. Do not call Astropy verification modes that fix or rewrite input headers.

### FR-13 Outputs

Provide:

- a concise human-readable text summary;
- a canonical JSON report;
- a CSV bundle containing separate file, group, and finding tables.

The canonical JSON report must include:

- `schema_version`
- `tool_version`
- `generated_at`
- `input_root`
- `options`
- `capabilities`
- `files`
- `groups`
- `integration_summary`
- `calibration_findings`
- `warnings`
- `errors`

Use relative paths by default. Do not leak absolute user paths into portable reports.

### FR-14 CLI Behavior

Support at least:

```text
audit_dataset.py INPUT
audit_dataset.py INPUT --format text
audit_dataset.py INPUT --format json --output process/audit.json
audit_dataset.py INPUT --format csv --output-dir process/audit-csv
audit_dataset.py INPUT --verify-fits --verify-checksum
audit_dataset.py INPUT --hash sha256
```

Machine-readable stdout must not contain progress messages. Send diagnostics to stderr.

### FR-15 Exit Codes

Use:

- `0`: audit completed, including completed audits with warnings or per-file errors;
- `1`: required dependency or explicitly requested adapter unavailable;
- `2`: invalid arguments or invalid input path;
- `3`: no supported files discovered;
- `4`: fatal audit/output failure.

### FR-16 Backward Compatibility

Retain `fits_audit.py` as a compatibility wrapper for one release unless repository search confirms that it has no callers. The wrapper must point to `audit_dataset.py` and must not maintain a second implementation.

## Non-Functional Requirements

### NFR-1 Read-Only Safety

Open source files read-only. All output must go to a user-selected location or a new `process/` location. Existing output must not be overwritten unless an explicit `--overwrite` flag is supplied.

### NFR-2 Performance

The default path must be header-first and sequential to behave safely with local disks, network volumes, and cloud-synchronized folders. Avoid full-array reads and full hashing by default.

### NFR-3 Determinism

For the same inputs and options, normalized records, groups, findings, and sort order must be deterministic. `generated_at` is allowed to vary and must be excluded from deterministic comparisons in tests.

### NFR-4 Fault Isolation

One unreadable or malformed file must not abort the entire dataset audit. Record the file error and continue.

### NFR-5 Scientific Caution

Distinguish camera gain settings from conversion gain. Distinguish measured temperature from setpoint. Distinguish absent WCS from invalid WCS. Distinguish unknown metadata from incompatibility.

### NFR-6 Dependency Discipline

Require Astropy for FITS. Keep optional adapters lazy-loaded. Never install dependencies automatically.

## Non-Goals

- pixel statistics or image-quality scoring;
- automatic calibration-frame creation;
- cosmetic correction or bad-pixel mapping;
- plate solving;
- modifying FITS headers;
- interpreting all observatory-specific metadata dialects in the first release;
- automatic session organization or file movement.

## Acceptance Signals

1. A synthetic mixed FITS dataset produces valid text, JSON, and CSV reports.
2. A primary-empty, `SCI`-extension FITS file is audited correctly.
3. Header conflicts are visible with provenance.
4. Duplicate basenames remain distinguishable by relative path.
5. Calibration compatibility never treats missing metadata as a confirmed match or mismatch.
6. The default run does not load full image arrays, hash entire files, follow symlink directories, or modify inputs.
7. The audit continues after a malformed file and exits `0` with recorded per-file errors.
8. Missing Astropy exits `1` with an actionable message.
9. Output schemas and exit codes are tested.
10. No XISF or RAW library is bundled into the skill package.

<!-- markdownlint-enable MD013 -->
