# Formats and expected outcomes

Read the applicable section when the requested output goes beyond the bundled JSON helper.

## JSON and API bodies

Keep case metadata outside strict request objects. Preserve missing keys versus explicit null. Do not use NaN or Infinity in interoperable JSON. Place syntactically broken JSON in a separate raw-text fixture; a JSON array containing broken text is still syntactically valid unless the test extracts that text. Distinguish parser rejection, schema rejection, and business-rule rejection.

## CSV and spreadsheets

Declare encoding, header order, delimiter, quoting, newline style, date representation, and null/missing conventions. CSV fields are text; ordinary CSV cannot preserve every distinction between absent, empty, null, boolean, and numeric values without a documented importer convention. Do not assert that it does. Use a proper writer and round-trip through the intended parser when available.

Spreadsheet applications may interpret cells beginning with `=`, `+`, `-`, or `@` as formulas. Default demo/export values should be inert. If formula-injection handling is the actual test goal, keep exact test strings in a labeled raw fixture and warn against opening them in a spreadsheet; also provide a safely escaped preview, without changing the test bytes. Do not trigger external callbacks, local command execution, or live exfiltration for fixture generation.

## SQL and relational fixtures

Separate schema/DDL from data. Match the chosen dialect, quoting and type rules; use parameterized insert data where possible. State transaction, reset and foreign-key assumptions, but do not execute destructive setup or imports without authorization. Generate parents first and verify foreign keys and uniqueness. An intentionally orphaned row belongs in an isolated negative fixture, not the valid baseline. Cycles require an explicit strategy rather than silently dropping constraints.

## Numbers, dates and distributions

Use decimal types for exact money rules when needed. Define precision, rounding, units and whether bounds are inclusive. Define time zone/reference clock for timestamps and distinguish leap days, daylight-saving transitions and date-only fields. Derive boundaries from stated contracts rather than assuming every domain accepts negative, zero, or empty values.

For probabilistic datasets, record the generator algorithm/version and seed, describe weights and correlations as design choices, and verify observed distributions with tolerances. Do not infer production prevalence, fairness, clinical validity, fraud patterns, or representativeness from invented distributions. Cover rare cases deliberately rather than assuming randomness will select them.

## Oracle ledger

For each case, record the input, intended coverage, exact violated rules if any, expected outcome, source of that expectation, and whether it was observed. A type/range contract can justify validity, not an HTTP status or database error string. Mark unavailable business decisions or target behavior as unspecified, or ask for their source. A mocked successful response is fixture data, never proof the real operation succeeded.
