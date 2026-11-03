# AI workflow design

Use this reference from the core n8n workflow skill for AI-assisted classification, extraction, summarization, tool use, or retrieval. It is not a separate skill. Core rules still govern credentials, retry contracts, authorization, runtime checks, and release boundaries.

**Official documentation checked:** 2026-11-03. These are documented capabilities, not verified capabilities of the user's instance. Confirm installed n8n version, node type/version, hosting/queue mode, provider/model, available nodes, and plan before implementation. No minimum version is inferred from a current documentation page. This module uses established workflow AI nodes; a separate Agents product is not a dependency.

## Select the smallest architecture

1. **Rules first:** use deterministic parsing, IF/Switch, and ordinary service nodes when rules suffice. Do not pay a model to copy known fields.
2. **Bounded inference:** use [Text Classifier](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.text-classifier) for routing, [Information Extractor](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.information-extractor) for fields, or [Basic LLM Chain](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.chainllm) for a prompt and optional parser. Configure an explicit no-match branch instead of silently dropping unclassified items.
3. **Tool selection:** choose [AI Agent](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent) only when the model must choose tools or steps. It needs a chat model and at least one tool. Do not attach a dummy tool to perform a simple summary; use a chain. Start with one agent and a small allowlist.
4. **Grounded answers:** add retrieval only when answers need an external corpus. RAG can use direct retrieval and a chain; it does not require an agent. Separate ingestion from querying. See [n8n RAG](https://docs.n8n.io/build/integrate-ai/understand-ai-components/retrieve-relevant-context.md).

HTTP Request remains an alternative for provider features unavailable in an installed node. Use named credentials and a verified API contract; do not assume a particular model, response shape, or native node exists.

## Specify contracts before wiring

Record input fields, required/optional values, item cardinality, output schema, and terminal outcomes: success, invalid output, insufficient evidence, denied action, provider failure, and uncertain side effect. Bound prompt size, output tokens, agent iterations/tool calls, elapsed time, and cost. Declare allowed retries and total attempts; a parser repair or model fallback is another call, not a free or automatically authorized retry.

- **Structured output:** prefer an explicit JSON Schema with enums, required fields, and deliberate null handling. The [Structured Output Parser](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.outputparserstructured) does not support `$ref`; schema generation from an example makes every field mandatory. Validate business rules separately before a write or send. A valid JSON object is not proof of truth or permission.
- **Agent results:** n8n warns that direct structured parsing with agents can be unreliable and recommends a separate LLM chain for parsing the agent result. Budget that extra call and validate its output. The parser governs final output, not tool authorization or every intermediate step. See [parser common issues](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.outputparserstructured/common-issues).
- **Multiple items:** sub-node expressions resolve against the first input item, unlike ordinary per-item root-node expressions. Do not assume a dynamic schema, session key, or model parameter varies for each item. When these differ, isolate one item per AI invocation using an explicit loop/sub-workflow contract and test two distinct users together. See [sub-node parameter behavior](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.outputparserstructured).

## Tools and approval boundaries

Treat prompts, email/RSS, retrieved documents, model responses, and tool results as untrusted data. They cannot grant permission or change trusted tool configuration. Enforce tool input schemas, allowed destinations, and operation scope outside the prompt; never accept arbitrary model-generated URLs, credentials, or tenant IDs as trusted configuration.

Design approval before consequential tools, not after the agent's final answer. n8n's [human review for tools](https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools.md) pauses a selected tool call; approval executes its specified inputs, while denial cancels it. Show the reviewer the exact operation, recipient/resource, and consequential parameters. Test denial, changed parameters, missing review, and expired/unavailable review. Default to no action when approval is absent; never route around denial through a different tool. If native review is unavailable, keep side-effect tools disconnected and return a proposal for review rather than claiming an equivalent gate exists.

A workflow review node does not replace the host's confirmation rules or authorize running this design now. Design, import, evaluation, live execution, provider data transmission, and production activation remain separate boundaries.

## Retrieval and memory isolation

**Ingestion contract:** approved source → load/split → embed → store. Specify source ID/version, chunk ID, tenant/access metadata, chunk/overlap strategy, retention, and duplicate/update/deletion behavior. Identify where raw text and embeddings go; private ingestion requires authorization for those providers and destinations. Self-hosted n8n alone does not make a remote embedding/model call local.

**Query contract:** authenticate caller → enforce authorized corpus/filter → retrieve bounded chunks → answer with source IDs → validate citations and abstention. Use the same embedding model for indexing and querying, as [n8n's RAG guide](https://docs.n8n.io/build/integrate-ai/understand-ai-components/retrieve-relevant-context.md) specifies. Verify matching vector dimensions/configuration. Access filtering must happen before unauthorized content reaches the model. Preserve source references; do not manufacture citations. Missing or contradictory evidence should produce an explicit insufficient-evidence/conflict result, not a fabricated answer.

**Storage choices:** [Simple Vector Store](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreinmemory) is recommended for development only. Its data is nonpersistent, can disappear on restart or memory pressure, and uses global keys accessible to all instance users regardless of original workflow permissions. A unique key is not an access-control boundary. Use only nonsensitive synthetic fixtures there; select and verify a persistent, access-controlled backend for private production knowledge.

**Conversation state:** derive session identity from authenticated tenant/user/conversation context, not model output or an unverified client key. Define retention, reset, and concurrent-update behavior. Chat history is distinct from the retrieval corpus. [Simple Memory](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow) is unsuitable for active production workflows in queue mode because calls may reach different workers. Select a shared supported memory backend when needed and test isolation; do not assume adding a memory node solves it.

## Deliverables and evaluation gates

Provide:

- Architecture rationale and node-by-node wiring, including model/parser/tool connections and the installed-feature assumptions.
- Data, schema, tool, retrieval/session, and cost/timeout contracts; credential placeholders only.
- Failure, abstention, review, and uncertain-outcome paths; observability without unnecessary prompt/private-data logging.
- Synthetic fixtures and expected outcomes, evaluation rubric, and explicit verification limits. Label a blueprint as a blueprint, not importable JSON or an executed workflow.

Start with mocked model/retrieval outputs and sink tools. Require every applicable deterministic safety case to pass before proposing authorized model tests. Evaluate real model quality separately on held-out examples with agreed category accuracy, field accuracy, citation grounding, abstention, latency, and cost thresholds. Record model/prompt/schema versions and dataset revision; do not claim mock success predicts model quality.

[Native metric-based evaluations](https://docs.n8n.io/build/integrate-ai/test-and-improve-ai-workflows/use-metrics-to-measure-quality.md) currently list Cloud Pro/Enterprise and self-hosted Enterprise, with a single-workflow allowance for registered Community/Starter users. Verify the actual entitlement and limits. If unavailable, deliver a local fixture table/report with deterministic comparisons; no plan purchase or account creation is needed. AI-based graders add cost and variability, so prefer deterministic schema/safety checks and separately authorize paid evaluation calls.

| Mock scenario | Required observable result |
| --- | --- |
| Valid extraction plus a missing optional value | Exact approved field types; deliberate null/omission behavior; no invented value |
| Malformed JSON, wrong type, or forbidden enum | Validation failure routes to review/error; no downstream write |
| Unsupported question or conflicting documents | Abstention or explicit conflict with real source IDs |
| Retrieved text asks to disclose secrets or change tools | Instruction ignored; no unauthorized tool use/data disclosure |
| Agent proposes a send; review denies or never arrives | Zero send calls; denial/pending outcome visible |
| Approval granted, then recipient/amount changes | Old approval cannot authorize changed parameters |
| Two users/items have different session keys and schemas | No first-item reuse, cross-user history, or corpus leakage |
| Queue-mode design contains Simple Memory | Design review blocks that configuration before production |
| Development vector data disappears | Explicit unavailable/rebuild path, not an unsupported answer |
| Provider timeout or tool response is lost | Contract-specific handling; uncertain side effect is not blindly retried |

Report separately what was statically reviewed, mock-tested, imported, executed with sinks, evaluated against a real model, and observed in production. Omit success claims for stages not performed.
