# Offline helper contract

`scripts/review_export.py` accepts one local workflow JSON plus optional `--config` JSON. Inputs remain untouched. Schema-v2 output is JSON on stdout; invalid outer inputs return a value-free error on stderr and exit 2. Exit 0 means triage completed, possibly with partial embedded coverage, not a security pass. Standard library only; no network, n8n executable, workflow code evaluation, dependency installation, file writes, or secret validation. Unsupported inner JSON yields coverage unknowns without discarding unrelated findings.

## Input formats

Workflow: a single object with a `nodes` array, an array of those objects, or an object whose `data` is that array. Nodes require a string `type` and, if supplied, object `parameters`. It accepts incomplete exports for partial review, not as proof of importability. JSON cannot represent all n8n schemas across versions. YAML, `.env`, SQLite, archives, URLs, credential exports and package files are not accepted. Do not convert credential dumps just to use this helper.

Optional configuration is deliberately narrow:

```json
{
  "n8n_version": "unknown",
  "edition": "unknown",
  "hosting": "self-hosted",
  "environment": {
    "N8N_RUNNERS_INSECURE_MODE": false,
    "N8N_BLOCK_ENV_ACCESS_IN_NODE": true,
    "N8N_SSRF_PROTECTION_ENABLED": true,
    "EXECUTIONS_DATA_PRUNE": true
  }
}
```

These are supplied observations, not installed-version or runtime claims. Provide only relevant non-secret flags or redacted metadata; never a whole environment dump. Metadata is intentionally not echoed or used to guess defaults. The helper checks explicit values only and cannot verify that any flag is supported or loaded.

## Implemented triage

- `NSR-SECRET`: selected secret-named literal fields or header name/value pairs, and a small known-token/private-key marker set in node parameters. Credential references are counted separately, never classified as plaintext secrets merely because they exist.
- `NSR-EMBEDDED-SECRET`: one strict JSON layer in `parameters.jsonHeaders` / `parameters.jsonBody` on HTTP Request / HTTP Request Tool nodes only. Parsed secret-named literal values and known token markers yield conditional candidates. Generic body-name matches are low priority because tokens, passwords or cookies can be examples or non-secret business data; header/signature matches are medium. Values are never validated. Authorization/Proxy-Authorization values consisting of Bearer/Basic plus a supported redaction placeholder are suppressed in this decoded scan. This does not change the original raw-field heuristic.
- `NSR-AUTH`, `NSR-AUTH-UNKNOWN`, `NSR-AUTH-REVIEW`: explicit Webhook auth `none`, absent auth, or a selection requiring contextual verification. None of these proves internet reachability or effective authentication.
- `NSR-URL`, `NSR-HTTP`, `NSR-URL-SECRET`, `NSR-TLS`: HTTP Request expressions in URLs, plain HTTP, URL auth-like fields, and explicit `options.allowUnauthorizedCerts=true`. Different node schemas require manual inspection.
- `NSR-CODE`: known code/command/file node types as manual review points, not findings of exploitation.
- `NSR-PIN`, `NSR-LOG`: nonempty pinned data and explicit workflow success/error save-all settings. Sensitivity and actual storage are unverified.
- `NSR-CONFIG`, `NSR-WILDCARD`: a narrow set of explicit protection-disabling flags and whole-value wildcards. Names appear in the script; absent settings, inherited values, `_FILE` settings, defaults and pattern combinations are not resolved.

Locations use zero-based normalized workflow and node ordinals. They are not literal JSON pointers: a single input object is workflow 0; list/wrapper entries retain order. No user-provided node names, IDs, arbitrary field names, URLs, code, credential names, or values appear in reports. Original secret scanning gives a parameter-scope locator; embedded scanning may append only the fixed allowlisted `jsonHeaders` or `jsonBody` field. No paths containing decoded keys, snippets, exception messages or individual-secret hashes are emitted. Marker counts are heuristic observations and may overlap raw and decoded scans; they are not distinct credentials. Disabled-node flags are reported; reachability is never inferred. Present stored fields are inspected regardless of send/mode flags, whose compatibility and runtime use are unverified.

## Schema-v2 coverage and consumers

Existing top-level fields remain, with `schema_version` now 2. `candidates` includes the additional embedded rule. `coverage` is separate: each record has a fixed `location`, `status: unknown`, `reason`, and value-free message. A coverage record is not a finding that a credential exists or an expression executes. Consumers must support version 2 and inspect coverage rather than deriving a security result from candidate count or exit code.

Coverage reasons:

- `expression_like_secret_value`: an ordinary secret-named field or header name/value pair contains expression markers. At most one notice per node parameter scope; reference-only expressions are not hardcoded-secret findings.
- `unevaluated_expression`: a selected JSON field is expression-like rather than supported strict JSON. No JavaScript parsing, coercion or evaluation occurs.
- `dynamic_embedded_value`: parsed JSON has expression-like keys or values. Literal siblings are still scanned. Markers can also occur in ordinary text, so runtime evaluation is not asserted.
- `not_strict_json`: malformed/unsupported inner JSON, duplicate keys, nonfinite constants or parser recursion rejection. `nonfinite_number` covers numeric overflow discovered after decoding.
- `unsupported_unicode`: invalid UTF-8 representation, including decoded unpaired surrogates in keys or values. `unsupported_field_shape` and `unsupported_header_shape` preserve unknowns for non-string selected fields and non-object header JSON.
- `field_size_limit`, `structure_limit`, `total_parse_budget`, `total_value_budget`, `total_field_budget`: the specified per-field or shared budget prevented complete inspection.

`embedded_review.status` is `partial` when this scan has coverage gaps or truncation, otherwise `completed_within_scope`. The latter means only the declared narrow scan finished; custom fields, arbitrary code/notes, absent settings, double encoding and runtime behavior remain outside scope. Empty or absent selected fields require no parse attempt. It does not mean a workflow is safe.

`embedded_review.counts` records decoded fields, named-literal and token markers, dynamic/unreviewed scopes, and separately suppressed finding/coverage records. A scope can be a whole node's parameters or a selected field; these are not counts of unique secrets. `budgets` reports consumed embedded bytes, values and parse attempts. `output_truncated` applies to this added embedded/coverage output; original rules retain their existing outer-input bounds.

Embedded findings and coverage each have separate caps of 100 records. Early coverage notices cannot consume finding capacity. Any omitted records have explicit suppressed counts and partial/truncated status. Never treat a truncated report as complete.

## Embedded decoding bounds

Decode only one serialization layer, with no recursive deserialization of descendant strings and no conversion of JavaScript object syntax into JSON. Strict JSON is attempted before expression-marker classification except prefixes that cannot start JSON. The resulting tree reuses the narrow secret-name/signature checks and does not establish n8n schema validity.

Per field: 64 KiB UTF-8 text, depth 32, and 4,096 decoded values. Across every workflow in one review: 256 KiB of attempted decoding, 16,384 decoded values, and 128 parse attempts. Failed parse attempts also consume the byte/attempt budgets. Byte caps apply before parsing; structural/value checks apply after the standard JSON parser creates the bounded tree. Separate output caps keep reporting bounded. These are resource safeguards, not a hardened parser sandbox or a guarantee against every resource attack.

## Deliberate limits

10 MiB per file, depth 80, 100,000 JSON values, 5,000 nodes. Duplicate keys, nonfinite numbers, malformed formats and linked/device input paths are rejected. These bounds reduce accidental resource use; they are not a hardened parser sandbox or a guarantee against a concurrently modified filesystem. Review authorized files in a trusted workspace. Hashes identify the bytes read, not the current on-disk file after review.

The scanner is intentionally incomplete: it does not inspect secrets in all notes/settings/pinned data, decode arbitrary strings or multiple layers, evaluate expressions, trace branches, inspect SQL semantics, verify AI authorization, review every custom/community node, or identify every secret format. A secret concatenated into an expression can still evade secret detection; relevant expression scopes are marked unknown rather than interpreted. Known raw token signatures can already trigger inside expressions. Clear placeholders are not proof that all content was sanitized. Even a report with no candidates requires the full manual checklist. Do not add a pass/fail gate based on the candidate count.
