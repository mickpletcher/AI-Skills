# Workflow patterns

Blueprints below are conceptual, not importable JSON. Verify target node versions/settings before turning them into an export. Official documentation checked 2026-11-03; recheck changed or unavailable features against the actual target.

## Webhook intake

Webhook → authenticate → validate/normalize payload → durable deduplication → bounded work → explicit response/error route. Prefer the Webhook node's available built-in authentication; payload validation is a separate check. Use a stable event ID plus payload digest to distinguish repeat delivery from the same ID carrying conflicting data. Authentication does not make a supplied URL safe.

Test and production URLs differ. Registering a test listener or executing an unpublished workflow can still perform real work. Define response status/body and when acknowledgement occurs; an immediate acceptance response is not downstream completion. Avoid multiple Respond to Webhook paths firing for one request. Verify timeout and failure behavior in an authorized sink environment. [Webhook](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook)

## Schedules and briefing/RSS

Schedule Trigger → feed/API nodes → normalize each branch → explicit combine rule → optional bounded summary → approved notification sink/destination. The historical morning briefing and trading-alert examples are use cases, not permission to contact a recipient or place an order.

Set the intended timezone explicitly and test daylight-saving boundaries and missed/overlapping runs; do not assume machine local time. Workflow timezone takes precedence over instance timezone. Weekday 06:00 and every-15-minutes schedules are alternatives, not defaults. [Schedule Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger)

Use RSS Read where it fits the feed; use HTTP Request plus parsing when headers or format require it. Validate actual response shape and timestamps, filter with a clear window, deduplicate stable links/IDs and bound article count/text length. For parallel sources define missing-source tolerance, staleness and whether the briefing stops or explicitly reports partial results. A Merge label alone does not define a join. See [item handling](expressions-and-code.md).

## HTTP requests and provider calls

Prefer a suitable native integration; otherwise configure HTTP Request with its supported predefined or generic credential type. Keep headers/body/response contracts tied to current provider documentation. Do not extract the first text field until the actual response's status, body and content types are validated. Provider models and versions are configuration values to verify, not permanent defaults. [HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest)

A provider request body is not a workflow export: it lacks node type/version, connections, credential binding and workflow settings. Use placeholders for unresolved values. Show response normalization and validation separately from the request configuration.

## Pagination, batches and concurrency

Use a node's built-in pagination where supported; otherwise define cursor/page state, terminal condition, maximum pages/items/duration, duplicate-page detection and allowed request destinations. A repeated cursor or page must terminate with a visible error, not spin indefinitely. Empty results can be legitimate completion; do not send an empty placeholder item into an external effect.

Most nodes already process each input item. Add Loop Over Items only for a concrete batch/rate-limit/sequential requirement and wire its loop and done outputs explicitly. Check exceptions such as execute-once settings and nodes/sub-nodes that use only one item. Combine concurrency limits, batching and retry budgets so they do not amplify calls. [Looping](https://docs.n8n.io/build/flow-logic/looping.md), [HTTP pagination](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest)

Durable idempotency requires a unique key/atomic claim or equivalent server-side guarantee; a read-then-write check and process memory do not prevent concurrent duplicates. Specify claimed/succeeded/failed/uncertain states, ownership/expiry and conflict behavior. Do not mark an uncertain operation complete or replay a whole partially successful batch blindly.

## Native sub-workflows

Use Execute Sub-workflow and its corresponding trigger when the target supports them. Record input field/type/cardinality, output contract, run-per-item versus run-with-all-items, wait-for-completion and error propagation. The caller must not assume a result exists when it does not wait. Resolve workflow IDs locally; sanitized placeholder IDs are not ready bindings. Use webhooks only for a justified cross-instance/external boundary, with authentication and URL trust checks. [Execute Sub-workflow](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow)

## Error routes and notifications

Choose intentionally: stop/fail the workflow and use its configured error workflow, or continue through a verified node-specific error branch and handle it explicitly. Do not expect both automatically. For business-rule failures use an explicit failure path, such as Stop And Error when appropriate. An Error Trigger cannot establish manual-run coverage. Inspect trigger failures separately because their payload may omit normal execution details. [Error Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.errortrigger)

Notifications need an approved recipient, redacted context, correlation ID and a bounded failure path of their own. Avoid recursive alert storms and repeated external side effects. A notification failure must remain visible through an independent permitted channel or execution record, not disappear in a continued branch. Test using a sink.
