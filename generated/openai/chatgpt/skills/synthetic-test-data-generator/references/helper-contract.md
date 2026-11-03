# Deterministic helper contract

Use `scripts/generate_fixtures.py` for small local JSON fixtures. Python 3.10+ and its standard library are the only runtime prerequisites. The helper does not install anything, call a model, access the network, read production data, or execute supplied strings. Input literals are still copied into output: use only approved fictional enums and mutations.

From this skill folder, after reviewing the example:

```sh
python scripts/generate_fixtures.py --spec examples/customer-orders.json --output /tmp/synthetic-fixtures.json
```

Choose a new output path. Existing files are refused, including symlinks; failed input validation creates no output. The helper has fixed limits of 1 MiB input, 1,000 total rows, 50 fields per table, 100 mutation cases, and 20 MiB serialized output. This is for functional fixtures, not load testing. Larger workloads need a separately reviewed streaming generator.

## Input format

The top-level object has exactly `schema_version` (1), `seed` (integer), `tables` (ordered array), and optional `cases`, `source_evidence` and `malformed_json` (boolean, default false). This is a helper-specific format, **not JSON Schema**. Unknown keys and unsupported rule combinations fail rather than being ignored.

Each table has `name` (lowercase identifier), `rows` (1–1,000), and `fields` (object). A field has `type`, optional `required` (default true) and `nullable` (default false), plus type-specific keys:

| Type | Extra keys | Generated values and checks |
| --- | --- | --- |
| `id` | none | Unique synthetic identifiers; duplicate values are errors within that field/table. |
| `text` | `min_length`, `max_length` | Synthetic text; defaults 0–80; lengths count Python Unicode code points. |
| `email` | none | Synthetic mailbox at `example.invalid`; checks the helper's simple email syntax, not deliverability. |
| `integer` | `min`, `max` | Inclusive integer bounds, defaults 0–100; booleans are not integers. |
| `boolean` | none | JSON true/false. |
| `enum` | `values` | Nonempty unique list of JSON scalar strings, integers, or booleans; exact types matter. No null enum members: use `nullable`. |
| `date` | `min`, `max` | Inclusive ISO `YYYY-MM-DD` dates, defaults 2000-01-01–2030-12-31; no clock or time zone dependence. |
| `ref` | `table`, `field` | Reference an `id` field in an earlier table; self/cyclic references are unsupported. |

Table/field identifiers must match `[a-z][a-z0-9_]{0,47}`. Integer bounds are limited to ±10^12. Text length bounds are 0–1,000. Enums have at most 100 values, strings at most 1,000 characters. Generation emits all fields as non-null; optional omissions and explicit nulls are deliberate cases, not random accidents.

The generator hashes the seed, table, row index, and field using SHA-256 and derives bounded values from the digest. It does not use time, locale, Python hash randomization, or mutable RNG state. The bundle records the generator hash, normalized configuration hash, seed, and full configuration. Identical script bytes and configuration produce identical bundle bytes; changing the script intentionally changes provenance even if payloads do not change.

## Case definitions and oracle

A case has `id`, `category`, `description`, `mutations`, and `expected_violations`. Categories are `normal`, `boundary`, `missing`, `malformed`, `duplicate`, or `relationship`; a category alone never implies validity. Case IDs are unique lowercase/hyphen identifiers, excluding reserved `baseline` and `malformed-json`.

Each mutation has `table`, zero-based `row`, `field`, and `operation`: `omit` removes a key; `set` also requires `value` (a JSON value). Each case starts from its own copy of the baseline. Mutations never change the schema or another case. An expected violation is `{ "table": "customers", "row": 0, "field": "email", "rule": "required" }`. Rule IDs are `required`, `null`, `type`, `range`, `length`, `format`, `enum`, `unique`, and `reference`. Duplicate IDs report `unique` on **each** implicated row. Missing keys produce only `required`; nulls produce only `null`; wrong types produce only `type` before other checks.

The helper independently evaluates the final payload under its data contract and refuses to produce output if the exact sorted violation set differs from the declared expectations. An empty expectation means the case must be valid. This catches accidental extra defects, though it is not an independent implementation of the target application's validator.

Optional `source_evidence` records objects with `path`, `sha256`, `revision` (string or null), and `requirements` (requirement IDs). Compute these from the inspected target skill and relevant resources. The helper carries them as supplied metadata and **does not read or verify target files**. Follow the [target analysis procedure](analyze-target-skill.md) to check hashes and derive expectations; metadata alone is not proof of source inspection.

The output is a valid JSON **fixture envelope**, not an application request. Each record case contains `payload` (a mapping of table names to row arrays), `expected_contract_result` (`valid`/`invalid`), and the checked violation list. Application behavior is explicitly unspecified. Extract the payload for an authorized test harness; do not submit the envelope to a strict endpoint.

With `malformed_json: true`, a separate `wire_cases` entry contains a raw, syntactically invalid JSON string and expected JSON parse failure, verified with Python's parser. The outer bundle remains parseable. Write that string verbatim to a separate test input only when needed. Do not “repair” intentional malformed data or silently mix it with valid records.

## CSV output

Use `--format csv --output /tmp/synthetic-csv-new` to create a new directory with per-case/per-table CSV files and `manifest.json`. Existing directories are refused. All payloads and validation finish before the directory is created. An I/O failure during writing can leave partial output; report the failure, do not treat that directory as complete, and retry into a new directory after checking what exists.

The writer uses UTF-8, comma delimiters, standard quoting, LF line endings and canonical sorted field-name order, and verifies a parser round trip. The sidecar maps every cell to its original JSON type or to `missing`/`null`. Missing, null and empty strings all use empty CSV cells, so a CSV file **alone** does not preserve those distinctions. An importer without this sidecar needs its own explicit convention; do not call this an application-ready import without one. Booleans use `true`/`false`; integers use base-10 text. Finite float mutation cells are retained as numeric text with a `float` sidecar type; they remain invalid under an integer-only field contract. Nested wrong-type values are refused for CSV; JSON supports those mutation fixtures.

Formula-like string cells (after whitespace, beginning `=`, `+`, `-` or `@`) are refused rather than quietly rewritten. Keep adversarial spreadsheet strings in a labeled JSON raw fixture and write a task-specific safe preview if needed. Plain negative integer cells remain numbers. The manifest retains the malformed JSON raw string separately and never places it in a CSV row.

## Limits

No SQL execution, application-specific CSV import semantics, standard JSON Schema support, regex synthesis, decimal arithmetic, weighted distributions, nested schema generation, cross-field business rules, or performance claims. Use task-specific code and an appropriate independent validator for those needs. Exact error wording and application rejection status are not inferred. Safe-looking values do not prove anonymity, privacy, correctness of a real application, or complete coverage.
