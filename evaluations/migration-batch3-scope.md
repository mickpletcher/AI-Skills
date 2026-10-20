# Third migration batch scope

Status: six cases executed on 2026-10-19. See the [assessment and remaining gates](migration-batch3-2026-10-19.md); the batch is not fully passed or accepted.

Mick authorized selection of the next three skills on 2026-10-19. The selected masters all have proposed Codex placements, so the planned first execution target is their existing generated Codex candidate under `generated/openai/codex/skills/`. This is scope preparation, not behavioral acceptance or a new promotion decision.

| Skill | Planned cases | Independent checks |
| --- | --- | --- |
| `github-social-preview` | Missing repository metadata with supplied README fallback; long Unicode title/tags with supplied local artwork. | Execute the bundled helper with preprovisioned Pillow; verify actual JPEG format, 1280x640 dimensions, size below 1,000,000 bytes, source/asset preservation and visual text fit. No GitHub upload or invented metadata retrieval. |
| `n8n-workflow` | Review duplicate webhook delivery and unsafe retry behavior; repair a supplied inactive workflow against a pinned node/schema contract with named credential references. | Check wiring, bounded retries, idempotency and explicit failure paths; replay pure transformation/deduplication logic using mocked inputs. No live workflow activation, exposed endpoint, credential access or external notification. Native n8n import/runtime support requires a separately provisioned, version-pinned engine; JSON parsing alone will not certify it. |
| `trip-email-html-itinerary` | Reconcile revised/canceled synthetic bookings; redact synthetic access secrets and reject instructions embedded in source emails. | Execute the bundled HTML validator; inspect offline rendering and compare dates, statuses, references and redactions against input oracles. Require a self-contained artifact without scripts, invented booking facts or current venue claims. No mailbox access, sending, bookings or publication. |

## Execution gates

- Pin source/candidate/helper/fixture hashes and exact model/runtime settings before inference. Audit isolated session inputs; keep expected results and previous conclusions outside each workspace.
- Copy reviewed supporting resources and provision trusted dependencies before the sessions. Keep credentials/profiles and raw outputs outside the checkout and sync roots.
- Use only fabricated repository metadata, webhook events and travel confirmations. Keep network access off for the initial cases. Where retrieval is unavailable, supply evidence and preserve explicit uncertainty rather than inventing current external facts.
- Inspect generated source before independent execution. Bound command time and side effects; use disposable output directories and retain failures rather than silently overwriting captures.
- Obtain current official n8n documentation and pin the supplied engine/schema before making importability claims. No live n8n or infrastructure connection is authorized.
- Record assistant assessment separately from human acceptance and native-host coverage. Keep PR #11 draft; no merging, installation or promotion.

This document records the scope selected before inference. Mick subsequently authorized execution. Six case captures and one canary are now retained; actual results and limitations are recorded separately. No live operations or promotion are authorized.
