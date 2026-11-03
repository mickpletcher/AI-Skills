# Expressions and code

Use expressions for field mapping and small calculations; use native transform nodes for common operations; use Code only for logic that benefits from it. Examples below are illustrative JavaScript, not verified runtime exports. Documentation checked 2026-11-03.

## Data shape and item identity

n8n passes items containing a `json` object and optional `binary` data. Distinguish one item containing an array from multiple items. Record cardinality before/after split, filter, aggregate and join operations. Handle missing, null, empty string, zero and false deliberately; `value || default` incorrectly replaces zero/false when those are legitimate values. Validate types before arithmetic or date comparison. Do not coerce an invalid identifier or amount into a plausible value. [Data structure](https://docs.n8n.io/build/work-with-data/understand-n8ns-data-structure.md)

`$json` means current-item JSON in the appropriate expression context. `.first()` deliberately selects one item; it is not a fix for ambiguous item linking. If you create/reorder/filter items in a Code node, preserve pairing to the actual source indices so downstream linked-item expressions still refer to the correct input. Multiple inputs/outputs can need richer pairing. Test at least two distinguishable records and an empty input. [Item linking](https://docs.n8n.io/build/work-with-data/reference-data/link-data-items.md)

Illustrative Code node, JavaScript, **Run Once for All Items**, preserving source indices through a filter:

```javascript
return $input.all().flatMap((item, index) => {
  const title = item.json.title;
  if (typeof title !== 'string' || title.trim() === '') return [];
  return [{
    json: { ...item.json, title: title.trim() },
    ...(item.binary ? { binary: item.binary } : {}),
    pairedItem: { item: index },
  }];
});
```

Expected: missing/blank titles are excluded by this example's contract, valid titles are trimmed, other fields/binary references survive, and paired indices refer to original inputs, not filtered positions. For a contract requiring rejection rather than exclusion, add a separate validation/error path. Do not paste this all-items snippet into per-item mode unchanged.

## Joins and dates

Specify whether Merge appends, joins by key, matches positions, or combines products. Test no match, duplicate keys, uneven lengths and a missing branch. Joining by position can silently attach one person's data to another. Check the actual node version and legacy workflow execution-order settings before diagnosing branches from a screenshot. [Merge](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.merge)

Keep timestamps with explicit offsets or a declared IANA zone. Define inclusive/exclusive boundaries and invalid-date behavior. Do not compare display-formatted dates lexically or assume a cron schedule's intended timezone. Test DST transitions where the zone observes them.

## Runtime boundaries

Code-node JavaScript/Python capabilities, built-ins and allowed imports depend on hosting/version. Current docs distinguish all-items and per-item modes; native Python has a different helper surface from legacy Pyodide. Do not present standalone Python scripts as drop-in Code-node programs. Prefer HTTP Request and dedicated file nodes rather than assuming Code has network/filesystem access. [Code node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code)

Do not install dependencies or change runner/module allowlists to make an example work without the required authorization. Production/sensitive execution needs an appropriately isolated runner configuration; designing an expression does not authorize operations changes. See [runtime gates](runtime-and-release.md).

Binary data is not ordinary JSON text. Preserve binary metadata and use supported nodes/helpers for content access on the target; do not assume an in-memory base64 field or local filesystem path. Limit size and avoid logging, serializing or embedding private file contents into prompts unintentionally.
