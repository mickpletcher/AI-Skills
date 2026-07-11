<!-- markdownlint-disable MD013 -->

# 003 Astrophotography Processing Phase 2 Technical Specification

## Purpose

Phase 2 introduces a deterministic evidence layer between an astrophotography dataset and Claude's recommendations. It replaces the current basename-only FITS header table with a normalized inventory, group analysis, and cautious calibration-compatibility report.

## Research Conclusions

### FITS is the required first-class format

The FITS Standard defines structural keywords but amateur acquisition metadata includes widely used non-standard dialects. Astropy intentionally tolerates many non-standard inputs and does not verify checksums by default. Therefore the audit must preserve raw keyword provenance, normalize known aliases, and make verification optional rather than silently repairing files.

### Multi-extension FITS must be represented explicitly

Professional HST/JWST files and tiled-compressed FITS can store image data outside the primary HDU. The audit must inventory HDUs and record its selection rather than reading only `hdul[0].header`.

### Pixel access is unnecessary for Phase 2

Dimensions, `BITPIX`, scaling, metadata, and HDU structure can normally be inspected from headers/HDU descriptors. Full pixel statistics would make the audit slower and blur the boundary with Phase 3.

### XISF is optional

The maintained Python `xisf` implementation can read XISF metadata and FITS keyword elements but is GPL-3.0 and is not an official PixInsight implementation. It may be used as a separately installed optional adapter but must not become a vendored core dependency without a separate licensing decision.

### RAW metadata should not require RAW conversion

Phase 2 needs metadata, not demosaicing or color rendering. A separately installed ExifTool process is preferable to invoking RAW post-processing. `rawpy` may expose structural data, but its LibRaw-backed conversion behavior is outside this phase.

## Architecture

Keep the implementation testable even if delivered initially as one script:

```text
CLI parsing
    ↓
capability detection
    ↓
file discovery
    ↓
format adapter
    ↓
raw metadata record
    ↓
normalization + provenance
    ↓
classification
    ↓
grouping
    ↓
compatibility evaluation
    ↓
text / JSON / CSV renderer
```

Recommended internal modules or logical components:

- `discovery`: paths, exclusions, supported suffixes, symlink policy;
- `fits_reader`: HDU inventory, selection, headers, optional verification;
- `optional_adapters`: XISF and ExifTool capability boundaries;
- `metadata`: aliases, parsing, units, provenance, conflicts;
- `classification`: frame/master/processed classification and confidence;
- `grouping`: stable comparable-group keys;
- `compatibility`: group-level calibration findings;
- `renderers`: text, canonical JSON, and CSV bundle;
- `cli`: arguments, logging, exit-code mapping.

Do not over-split the first implementation. Separate code when a component has independent tests or format-specific dependencies.

## Data Model

### Provenanced value

Each normalized field should follow this conceptual shape:

```json
{
  "value": 120.0,
  "unit": "s",
  "source": {
    "format": "fits",
    "hdu_index": 0,
    "hdu_name": "PRIMARY",
    "keyword": "EXPTIME",
    "raw_value": 120.0
  },
  "confidence": "explicit",
  "conflicts": []
}
```

Allow compact serialization for fields where provenance is not useful, but never compact observational values that participate in compatibility findings.

### File record

Each file record contains:

- stable relative path;
- format and compression;
- filesystem size and optional SHA-256;
- read status and errors;
- HDU inventory;
- selected-HDU rule/result;
- normalized metadata;
- classification and evidence;
- structural/FITS/WCS/checksum findings.

### Group record

Each group has a deterministic ID derived from a canonical serialization of its grouping key, not from Python's randomized hash. Include group members by relative path and a readable summary of key fields.

### Finding record

Each finding contains:

- stable finding code;
- state/severity;
- subject light/flat group;
- candidate calibration group when applicable;
- compared fields;
- observed values;
- tolerance used;
- evidence;
- smallest next confirmation step.

## FITS Reading Design

### Opening

Use `fits.open(path, mode="readonly", memmap=True, lazy_load_hdus=True)` where supported. Capture warnings rather than suppressing them. Do not call any `fix` verification mode.

For externally compressed FITS, document that memory mapping may not provide the same benefit and avoid touching pixel arrays.

### HDU inventory

Record for each HDU:

- index;
- name and version;
- class/type;
- image/table status;
- dimensions/shape from structural metadata;
- `BITPIX`/data-format information;
- compression indicator;
- `EXTNAME`;
- presence of `SCI`, `ERR`, `DQ`, or other commonly meaningful names.

Treat unsupported cubes and heterogeneous mission structures as inventory findings, not fatal errors.

### Header precedence

Keep primary and selected-extension headers separate. Normalize fields using:

1. selected extension;
2. primary header fallback;
3. other image extension only when a field-specific rule explicitly permits it.

Record every differing non-empty candidate as a conflict. Structural keywords always describe their own HDU and must not be merged across HDUs.

### Verification

- `--verify-fits`: run warning/exception-style verification without mutation and serialize findings.
- `--verify-checksum`: request or invoke checksum/datasum verification only when cards are present; distinguish absent, valid, invalid, and not checked.
- Never write a repaired copy in Phase 2.

## Metadata Alias Registry

Implement aliases as data, not nested `if` statements. Initial aliases should be based on FITS/Siril/N.I.N.A. conventions and expanded through fixtures.

Examples:

| Normalized field | Initial aliases |
| --- | --- |
| exposure seconds | `EXPTIME`, `EXPOSURE` |
| frame type | `IMAGETYP`, `FRAME`, `OBSTYPE` |
| filter | `FILTER`, `FILTNAM`, `INSFLNAM` |
| instrument | `INSTRUME`, camera-specific documented aliases |
| gain setting | `GAIN` |
| conversion gain | `CVF`, `EGAIN` only when units/meaning support electrons per ADU |
| offset | `OFFSET`, `BLACKLVL` |
| sensor temperature | `CCD-TEMP`, `CCD_TEMP`, `CCDTEMP`, `TEMPERAT`, `SENSOR_TEMP` |
| set temperature | `SET-TEMP`, documented aliases |
| binning X/Y | `XBINNING`/`YBINNING`, `CCDBINX`/`CCDBINY` |
| Bayer pattern | `BAYERPAT`, `BAYERPATN`, `COLORTYP` with value validation |
| row order | `ROWORDER` |
| observation time | `DATE-OBS`, then documented alternatives with explicit semantics |

Do not equate `GAIN` with `EGAIN`. Do not equate `SET-TEMP` with measured sensor temperature. Preserve original units and only convert when the unit is known or the convention is documented.

## WCS Design

Report separately:

- WCS keyword presence;
- whether `astropy.wcs.WCS` can parse the selected header;
- `has_celestial`;
- `has_distortion`;
- validation warnings.

Do not plate solve or modify WCS. An absent WCS is informational for raw subs and may be expected.

## Classification Design

Normalize common explicit values case-insensitively, including variants of light, dark, flat, bias, flat-dark/dark-flat, master, and processed/integrated. Preserve the raw value.

Confidence values:

- `explicit`: direct header/property value;
- `derived`: multiple metadata fields support the class;
- `filename`: inferred only from path tokens;
- `unknown`.

Filename inference must tokenize path components and avoid substring accidents such as matching `flat` inside an unrelated object name.

## Grouping Design

Normalize strings with trimmed whitespace and case-insensitive comparison while retaining display values. Normalize numeric values with Decimal or explicit tolerances rather than binary-float equality.

Create group keys appropriate to frame type. Do not force filter into dark groups or exposure into bias groups when not applicable.

Sessions should initially derive from observation dates and a configurable maximum gap. Folder names may supplement but not override timestamps. Files without usable timestamps belong to an `unknown-session` group.

## Compatibility Engine

Evaluate calibration candidates at group level and return all plausible candidates, not only a single winner.

Comparison results per field:

- exact;
- within tolerance;
- mismatch;
- unknown;
- not applicable.

Overall state rules:

- any hard mismatch makes a candidate `incompatible`;
- no hard mismatch plus one or more unknown required fields makes it `unknown`;
- all required fields exact makes it `compatible`;
- all required fields exact/within tolerance with at least one tolerance match makes it `compatible_within_tolerance`;
- no candidate group makes the requirement `missing`;
- calibration type irrelevant to the selected strategy is `not_applicable`.

The output is an audit, not a guarantee that dust, focus, optical rotation, light leaks, sensor behavior, or calibration mathematics are correct.

## CLI and Output Decisions

### JSON is canonical

Text and CSV render from the same in-memory report used for JSON. Never implement separate analysis paths per format.

### CSV is a bundle

Nested findings do not fit one CSV. `--format csv --output-dir DIR` writes:

- `files.csv`
- `groups.csv`
- `integration-summary.csv`
- `calibration-findings.csv`
- `warnings.csv`
- `errors.csv`

### Overwrite behavior

Refuse to overwrite any output unless `--overwrite` is present. Create output directories when their parent exists and creation is safe.

### Logging

Use stderr for progress/warnings. Use stdout only for the requested text/JSON payload when no output path is specified.

## Dependency Decision

Runtime core:

```text
astropy>=6.1
```

Do not set an upper bound without a demonstrated incompatibility. Python standard-library CSV/JSON/hash/path functionality is sufficient for Phase 2.

Optional:

- `xisf`: separately installed GPL-3.0 XISF adapter;
- ExifTool executable: separately installed RAW metadata adapter.

Development/test dependencies may include `pytest`, but must not be required for normal use.

## Test Strategy

Generate all FITS fixtures during tests in temporary directories. Do not commit large binary fixtures.

### Unit tests

- suffix and exclusion matching;
- alias registry and unit conversion;
- provenance and conflict resolution;
- classification confidence;
- tolerance comparisons;
- group-key determinism;
- compatibility overall-state rules;
- JSON serialization and CSV flattening;
- exit-code mapping.

### Integration tests

- simple primary-image FITS;
- primary-empty plus `SCI` image extension;
- `SCI`/`ERR`/`DQ` multi-extension file;
- `CompImageHDU` and `.fz`-style input where Astropy supports the fixture;
- externally gzip-compressed FITS;
- 3D image cube inventory;
- missing and conflicting metadata;
- duplicate basenames;
- malformed/unreadable file mixed with valid files;
- valid/invalid/absent checksum states;
- WCS absent, valid celestial WCS, and malformed WCS;
- JSON and CSV output collision behavior;
- symlink directory not followed by default;
- generated output directories excluded.

### Dependency tests

Use dependency injection or subprocess isolation to verify the missing-Astropy error path without uninstalling the developer's environment.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Non-standard metadata dialects | Alias registry with raw provenance and unknown states |
| Large/cloud-hosted files | Header-first sequential reads; no hashing/checksums by default |
| False calibration certainty | Group-level evidence, explicit unknowns, configurable tolerances |
| HST/JWST misinterpretation | Full HDU inventory and deterministic selected-HDU disclosure |
| GPL dependency leakage | Optional external XISF adapter; no vendoring |
| RAW conversion side effects | Metadata-only ExifTool adapter; no post-processing |
| Duplicate filename ambiguity | Relative paths and deterministic group IDs |
| Malformed file aborts audit | Per-file fault isolation |

## Authoritative References

- [FITS Standard 4.0](https://fits.gsfc.nasa.gov/fits_standard.html)
- [Astropy FITS file handling](https://docs.astropy.org/en/stable/io/fits/index.html)
- [Astropy FITS verification and checksums](https://docs.astropy.org/en/stable/io/fits/usage/verification.html)
- [Astropy compressed image HDUs](https://docs.astropy.org/en/stable/io/fits/usage/unfamiliar.html)
- [Astropy CCDData and WCS metadata](https://docs.astropy.org/en/stable/nddata/ccddata.html)
- [Astropy WCS validation](https://docs.astropy.org/en/stable/wcs/validation.html)
- [Siril FITS format and row-order guidance](https://siril.readthedocs.io/en/stable/file-formats/FITS.html)
- [Siril FITS keyword registry](https://siril.readthedocs.io/en/latest/file-formats/FITS.html)
- [N.I.N.A. FITS metadata documentation](https://nighttime-imaging.eu/docs/master/site/advanced/file_formats/fits/)
- [PixInsight XISF specification site](https://pixinsight.com/xisf/)
- [Python XISF decoder and license](https://github.com/sergio-dr/xisf)
- [rawpy/LibRaw wrapper and licenses](https://github.com/letmaik/rawpy)
- [ExifTool tag reference](https://exiftool.org/TagNames.pdf)

<!-- markdownlint-enable MD013 -->
