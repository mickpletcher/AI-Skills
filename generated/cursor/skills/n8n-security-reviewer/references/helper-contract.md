# Offline helper contract

`scripts/review_export.py` accepts one local workflow JSON plus optional `--config` JSON. Inputs remain untouched. Output is JSON on stdout; invalid inputs return a value-free error on stderr and exit 2. Exit 0 means triage completed, not a security pass. Standard library only; no network, n8n executable, workflow code evaluation, dependency installation, file writes, or secret validation.

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
- `NSR-AUTH`, `NSR-AUTH-UNKNOWN`, `NSR-AUTH-REVIEW`: explicit Webhook auth `none`, absent auth, or a selection requiring contextual verification. None of these proves internet reachability or effective authentication.
- `NSR-URL`, `NSR-HTTP`, `NSR-URL-SECRET`, `NSR-TLS`: HTTP Request expressions in URLs, plain HTTP, URL auth-like fields, and explicit `options.allowUnauthorizedCerts=true`. Different node schemas require manual inspection.
- `NSR-CODE`: known code/command/file node types as manual review points, not findings of exploitation.
- `NSR-PIN`, `NSR-LOG`: nonempty pinned data and explicit workflow success/error save-all settings. Sensitivity and actual storage are unverified.
- `NSR-CONFIG`, `NSR-WILDCARD`: a narrow set of explicit protection-disabling flags and whole-value wildcards. Names appear in the script; absent settings, inherited values, `_FILE` settings, defaults and pattern combinations are not resolved.

Locations use zero-based normalized workflow and node ordinals. They are not literal JSON pointers: a single input object is workflow 0; list/wrapper entries retain order. No user-provided node names, IDs, field names, URLs, code, credential names, or values appear in reports. Secret scanning gives a parameter-scope locator and count; inspect that node locally for exact attribution. Disabled-node flags are reported; reachability is never inferred.

## Deliberate limits

10 MiB per file, depth 80, 100,000 JSON values, 5,000 nodes. Duplicate keys, nonfinite numbers, malformed formats and linked/device input paths are rejected. These bounds reduce accidental resource use; they are not a hardened parser sandbox or a guarantee against a concurrently modified filesystem. Review authorized files in a trusted workspace. Hashes identify the bytes read, not the current on-disk file after review.

The scanner is intentionally incomplete: it does not inspect secrets in all notes/settings/pinned data, decode embedded JSON/header strings, evaluate expressions, trace branches, inspect SQL semantics, verify AI authorization, review every custom/community node, or identify every secret format. Expressions and clear placeholders are not treated as literal secrets, so a secret concatenated into an expression can evade this heuristic. Even a “clean” helper report requires the full manual checklist. Do not add a pass/fail gate based on the candidate count.
