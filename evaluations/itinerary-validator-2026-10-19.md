# Itinerary validator correction and visual review, 2026-10-19

The candidate helper now exempts explicitly pending addresses from map-link counts. Supported addresses still require Apple and Google links. Both unchanged batch-3 itineraries pass strict replay with zero errors and zero warnings. Human acceptance remains pending; PR #11 stays draft, with no merging, installation or promotion.

## Candidate correction and provenance

Only the master candidate helper and its four generated review copies change. Leading labels and HTML entities are handled before matching the prescribed `Address pending — verify before travel` fallback. A pending note later in a supported address does not exempt it. Existing global link-count validation is retained; this does not prove each link points to its associated address.

The original source helper SHA-256 remains `78b12232db200a31d268c5575b2b5af64431fde2fd65ab1ad1a599331a71955d` in migration provenance. The explicit candidate override is `23ad3c3c8483887d569908db61643b350758276d6b8b4bd0d62058301ec78353`. Regression checks verify both the original shipped bytes and corrected candidate bytes. Shipped skills, packages, placement and entrypoint instructions are unchanged.

Five executable regression methods cover ten PowerShell invocations: pending variants, supported addresses missing one or both services, both services present, mixed blocks, a later pending note and absent address blocks. All pass. The full suite passes 79 tests in a clean Git-byte snapshot.

## Strict replay

| Case | Original HTML SHA-256 | Corrected strict replay |
| --- | --- | --- |
| `trip-reconcile` | `38cdf527597aabb7bb9e6f4846e8a51bcd80c4df51eb158a4b81dbdd26d2251a` | Exit 0; zero errors, zero warnings |
| `trip-secrets` | `ca51bf1d73332d3d3366b50ee1ff1f415db891b5c93fa0fcf81aedf53515907e` | Exit 0; zero errors, zero warnings |

Original HTML, contact sheets and model captures remain byte-identical. The [initial assessment](migration-batch3-2026-10-19.md) and [fixture](fixtures/migration-batch3.json) retain the original two-warning failure. This is helper replay, not a new model evaluation or comparative quality claim.

## Offline visual review

The [official WeasyPrint 70.0 standalone release](https://github.com/Kozea/WeasyPrint/releases/tag/v70.0) rendered separate copies at 1280 and 390 pixels. The downloaded archive matched its published SHA-256 `ab1151f210b4e6bb7aa7a79e91a67e8ddb760094c107bfda55241b6aaefe7d53`. No machine installation or browser action occurred. Resource fetching allowed only `data`, with HTTP redirects disabled; static inspection found no automatic external resources.

Renderer copies resolve supplied max-width media rules explicitly at each selected width, enable reduced motion and use a tall screen-media page canvas. Original content and layout rules were not repaired. PDFs were rasterized with pypdfium2, inspected as full-document contact sheets and selected full-size tiles, and checked for text beyond horizontal page bounds. Synthetic artifacts, manifests and logs remain local; public hashes are in the fixture.

| Case / width | Observed result |
| --- | --- |
| Reconciliation / 1280 | Bounded visual pass. Readable cards, conflict warning, references and checklist; no observed overlap or horizontal text overflow. |
| Redaction / 1280 | Bounded visual pass. Pending-address warnings, navigation, references and cards remain readable; no observed overlap or horizontal text overflow. |
| Redaction / 390 | Bounded visual pass. Cards stack and the narrow reference table wraps within the canvas. No horizontal text overflow detected. |
| Reconciliation / 390 | Unresolved. Booking-table status cells clip at the right edge. Text extraction detects 46 characters outside the horizontal page bounds, extending about 29 pixels beyond the page. |

WeasyPrint reports unsupported `overflow-x` and `clip-path` declarations. The reconciliation table uses horizontal scrolling, which this renderer cannot demonstrate. The clipping is a real result in this renderer, but does not establish a native browser defect. A permitted native phone check must verify access to every table column before closing that gate. No source layout was changed merely to accommodate the renderer.

This review does not certify Chrome/WebKit, iPhone, Apple Notes, interactive scrolling, focus behavior or print layout. The earlier local-file browser policy rejection remains in effect; no HTTP or alternative browser route was used. The four offline visual checks are complete with the stated unresolved result. Native phone verification and human acceptance remain open.

## Delivery validation

Clean Git-byte snapshot validation passed: all 79 unit tests, repository and PowerShell quality (46 shipped skills, zero issues), exact-case folders (35 Claude skills, zero issues), generator drift and 24 offline cases with 99 negative checks. No shipped source, package, catalog or checksum file changed. These checks do not resolve native phone behavior, native n8n execution, broader host/model coverage or acceptance of this batch and the native photo result.
