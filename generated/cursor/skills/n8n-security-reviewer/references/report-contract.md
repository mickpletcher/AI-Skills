# Report contract

Begin with the most consequential supported findings and what the review can establish. Report “No issue identified in the inspected evidence” only when applicable, followed by the limits, never “safe” or “certified.”

## Scope and provenance

- Input hashes or immutable revisions; received artifact types and review date.
- Claimed n8n version, node versions, deployment/edition, and whether independently evidenced or unknown.
- Snapshot/published-state uncertainty; explicit exclusions, missing sub-workflows, omitted credentials/config, and unavailable runtime verification.

## Findings

For each finding include:

- Stable identifier; concise title; classification (observed issue, conditional risk, hardening option, unknown); severity and separate confidence.
- Safe locator: file role/hash, workflow/node index or non-sensitive ID, field/connection/line. Use a redacted snippet only if necessary; no secret values, raw personal payloads, or sensitive names.
- What is actually observed; attacker/control source, relevant route, affected sink, and impact preconditions. Do not upgrade possible access to proven internet reachability.
- Minimal proposed remediation and compatibility/edition constraints.
- Safe validation: what static evidence would support closure. Runtime verification must be clearly marked not run and separately authorized, not silently performed.
- Relevant authoritative URL and checked date for product-specific behavior. Give inference separately from the sourced fact.

Suggested priority meanings: high for a plausible reachable consequential effect or likely credential disclosure; medium for narrower conditional exposure; low for limited impact/hardening. Reserve critical for evidence of critical impact, not merely a dangerous node or hardcoded placeholder. Do not invent a CVSS score without its assumptions.

## Coverage and next evidence

Cover each applicable checklist area as reviewed, partial, not applicable, or unknown. Summarize effective-looking controls without treating them as runtime proof. List the smallest missing non-secret evidence that would change the conclusion, plus not-run checks. Preserve original findings if later evidence changes them; explain the correction.

If artifacts change during review, compare their hashes and re-review affected paths. If unavailable, label the conclusions snapshot-specific and potentially stale. Do not claim the helper verified control flow or that every secret pattern was found.
