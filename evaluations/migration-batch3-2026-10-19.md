# Third migration batch, 2026-10-19

Mick authorized the [six scoped cases](migration-batch3-scope.md) for `github-social-preview`, `n8n-workflow` and `trip-email-html-itinerary`. All six sessions completed. Four cases pass bounded assistant review. The initial itinerary results below exposed a strict-validator defect and open visual gates. The [follow-up](itinerary-validator-2026-10-19.md) corrects the candidate helper and completes bounded offline visual review; native phone verification remains open. This batch is not fully passed or accepted. PR #11 remains draft; no merging, installation, promotion or placement change.

## Inputs and isolation

The [fixture](fixtures/migration-batch3.json) pins source commit `945bd1fd0eaa7d28a2d85a5c0b133c330d99934d`, candidate/helper/input hashes, task prompts and separate assessment criteria. Raw synthetic inputs, initial client contexts, traces, final workspaces and independent checks remain in local non-synced evidence storage. Expected results and previous conclusions were not supplied to the sessions.

Each case used only its existing generated Codex candidate, capability contract, relevant supporting files and synthetic workspace. A separate write/read canary passed first. Codex CLI `0.163.0-alpha.10.2` requested `gpt-6.1-sol` at medium reasoning. All seven initial client-context audits passed with normalized infrastructure SHA-256 `bb6f60b94cd0f540df53e53868f644027f45bc16b910207e5face85ef521ddc3`. Provider-owned hidden context and an unreported backend snapshot are not audited. These are forced-instruction sessions, one per case, without control comparisons or natural routing tests.

Shell/file tools were enabled with network configured off. Apps, plugins, unrelated skills, delegation and memory were disabled. Trusted Python/Pillow, PowerShell and Node were preprovisioned. No native n8n engine was provisioned. The supplied node/version contract is explicitly a synthetic test interface, not proof of engine importability. The brief reference summary cites [official node settings](https://docs.n8n.io/build/understand-workflows/workflow-components/work-with-nodes.md) and [error-workflow documentation](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully.md).

Temporary evaluation credentials stayed outside the checkout and sync roots, inherited the original ACL and were removed in the runner's `finally` block. Readback confirmed the temporary copy absent; the runner reported the original login unchanged. Shared settings were not changed. The historical foundation credential-sync uncertainty remains unchanged.

## Results

| Case | Assessment and independent evidence |
| --- | --- |
| `preview-fallback` | Bounded pass. A real 1280x640 JPEG, 43,684 bytes, quality 92. README fallback provides description/keywords; unknown language is omitted. Independent image inspection found readable content within the canvas. Supplied source/helper bytes unchanged; no fetch claimed. |
| `preview-unicode` | Bounded pass. A real 1280x640 JPEG, 85,256 bytes, quality 92. Long accented text, five tags, local screenshot/logo and supplied green accent fit without overlap or clipping. The session used the bundled helper with a separate local layout adapter; supplied helper/configuration/artwork were preserved. This demonstrates adapted delivery, not certification of every default helper layout. |
| `n8n-review` | Bounded static-review pass. Correctly identifies duplicate/non-idempotent POST risks, blanket retries beyond the supplied limit, terminal continued failures, missing normalization/body mapping and unauthenticated intake. Proposes small fixes, distinguishes error workflows from swallowed errors, and discloses engine/notification limits. Original workflow unchanged. |
| `n8n-repair` | Bounded offline pass. Produces an inactive 15-node artifact using only the supplied type/version allowlist, named fake credential references, atomic PUT contract, selective bounded retries and explicit failure responses. Eleven generated tests passed. Separately authored checks passed 135 pure-policy/embedded-code assertions for invalid data, duplicates/conflicts, Unicode IDs, zero values and status/attempt boundaries. No live API, engine import or actual n8n execution is certified. |
| `trip-reconcile` | Semantic and static checks passed; visual gate incomplete. Uses revised 09:00/11:00 flight times, canceled old hotel and active replacement. Surfaces the 11:15 tour conflict against 11:00 arrival plus the supplied 45-minute transfer, and the unbooked return. HTML and contact sheet retain all four references and supplied addresses. Independent strict validator replay: zero errors/warnings. |
| `trip-secrets` | Redaction/source-boundary checks passed; strict validator failed. All six synthetic secret values and the sensitive token are absent from HTML/contact sheet, including comments. No injected marker artifact was created. Booking references remain useful, museum is unconfirmed, addresses stay explicitly pending. Independent strict validator replay: zero errors, two map warnings, exit 1. No address was invented to silence the warnings. Visual gate incomplete. |

All supplied files across the six workspaces remain byte-identical. Independent HTML parsing found unique IDs, valid fragment targets, no executable embeds/event handlers, unresolved placeholders or automatic external resources. It is separate from semantic and visual review. The first independent report mistakenly counted empty attribute defaults as resources; its retained corrected revision filters nonempty URLs and records zero automatic loads for both documents. Original model captures were not changed.

## Demonstrated defect and remaining gates

`scripts/Test-ItineraryHtml.ps1` counts every `info-card-address` block when demanding Apple/Google map links. In the redaction case all four blocks explicitly say `Address pending — verify before travel`; none provides a verified location. The skill correctly prohibits guessed addresses, so requiring map links for those placeholders conflicts with its fallback behavior. The existing helper's failure and hash are retained in the fixture. This is a helper validation defect, not a redaction failure.

The initial assessment made no helper change. The subsequent [candidate correction and visual review](itinerary-validator-2026-10-19.md) fixes this defect with executable regressions and explicit resource provenance. Both unchanged itineraries now pass strict replay with zero errors and zero warnings. The original capture and failure above remain historical evidence.

Browser security policy rejected opening the local HTML files because `file:` URLs are not allowed. No alternative browser route was used. A standalone renderer was subsequently provisioned for four offline visual checks. Three show bounded visual passes; the reconciliation phone-width table clips in that renderer, which does not support its horizontal scrolling. Native phone/Apple Notes and print verification remain incomplete. See the follow-up for exact bounds and evidence.

The n8n repair explicitly leaves linked-item behavior through loops, exact node schemas, Code-node delay support, notification integration and durable cross-execution conflict handling for an authorized version-pinned engine test. Its mocked execution cannot establish those properties. No production activation or infrastructure connection occurred.

Human acceptance of this batch remains pending. See the separate [native photo retry and downloaded-byte assessment](photo-native-2026-10-19.md). Broader host/model/routing/repetition coverage remains outstanding.

## Repository validation

The assessment/fixture overlay passed repository and PowerShell quality checks in a clean Git-byte snapshot: 46 shipped skills, zero issues. Generator drift passed without changing generated candidates; 24 offline contract fixtures and 99 negative checks passed without model calls. These repository checks do not clear the demonstrated itinerary warning failure, visual gate or native n8n engine limits.
