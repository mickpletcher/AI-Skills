# Patent, food and workout delivery repairs

Date: 2026-10-22. Source `985bdbdc42c4d5a7774139f4816b7af55fad44dc`. PR #11 remains draft. No merge, installation or promotion.

## Changes and protocol

Patent now budgets the complete 14-section package, counts headings and all surrounding text, limits section 10 separately, and avoids repeated disclaimer/completion text. A read-only helper checks exact section inventory, populated bodies and whitespace word counts. The five required boundaries remain upfront. This helper does not assess legal or technical sufficiency.

Food returns a minimal request when a visual task has no usable image or sufficient text. It avoids a report template and a separate general disclaimer during intake. Sufficient supplied text remains a supported input.

Workout validates canonical Markdown before serializing one literal `text` fence, starts the response with that block, and puts metadata afterward. `--render-inline` writes the validated bytes without padding or an extra fence. The exact Copy output is tested without trimming or normalization.

Only canonical candidates and their existing Claude/ChatGPT review bundles changed. Shipped sources/packages, versions, original source hashes, capabilities, suitability and placement remain unchanged. No Codex/Cursor expansion.

Original synthetic tasks, sources, external criteria, upload transport, wrappers and visible modes are preserved. Patent/food use Instant; workout uses its original Medium mode and two uploads. Each changed-candidate revision uses a fresh Temporary chat. No feedback, regeneration or same-candidate retry. Original workout duplicate and explicit correction turns run in that case's conversation. External criteria stay outside uploads.

## Results

| Revision | Result | Disposition |
| --- | --- | --- |
| Patent v1 | 1,272 total words; section 10 293 | Total-limit failure retained. |
| Patent v2 | 1,252 total words; section 10 300 | Total-limit failure retained. |
| Patent v3 | **1,114 total words; section 10 289; all 14 sections populated** | Bounded word-limit/package verification passes. |
| Food v1 | 53 words, three sentences | Original concise rubric passes, but new one-to-two-sentence instruction gap retained. |
| Food v2 | Two sentences request actual photo or usable description, ingredients and portions | Bounded concise missing-image verification passes. No invented nutrition or allergen clearance. |
| Workout v1 | Initial and corrected Copy each 332 bytes, with leading newline | Delivery failure retained despite correct source content and duplicate handling. |
| Workout v2 initial | **290 exact bytes, `---` at byte zero**, unchanged validator pass | Bounded initial Copy verification passes. |
| Workout v2 duplicate | Asks overwrite/skip; no silent re-export | Bounded duplicate protection passes. No option submitted. |
| Workout v2 correction | **290 exact bytes, `---` at byte zero**, unchanged validator pass | Full replacement changes row to 60 lbs, four sets, six reps; push-ups preserved. |

The original three-point content rubrics score 2/2/2 for final affected cases. Additional delivery contracts are assessed separately, so content passes never conceal failed word limits or Copy bytes. Patent's final response preserves the opening-release and closed-lid-only reset mechanism, all five upfront disclaimer points, confidentiality flags with suggested replacements, drafting-aid claims and search-only strategy. No invented electronics, numeric CPC classification, reference or filing action is claimed. Unknown engineering details remain review gaps.

Workout's corrected note differs from the initial note only in the row set count. Both exact copies pass the supplied frontmatter/duration validator. No unsupported body stats, duration, effort, PR or progression data are inserted. No Obsidian vault ingestion or write was tested. Provider claims of helper execution are distinct from independently running the validator on captured bytes.

## Controls and open paths

The v1 supplied-label food control passes independent scaling checks: 200 g/800 kcal for the full batch and 50 g/200 kcal per container, with corresponding macros, sodium/fiber daily values and peanut warning. V1 patent interview asks one substantive mechanism question without inventing a package. These are historical passes against v1 instruction bytes.

Final-byte controls were pinned separately. Food's final control Send timed out; subsequent focus and Page.enable readbacks also timed out. Later readback proved the original submission completed, without a resend. Its total/per-container arithmetic, sodium 10.87% and fiber 17.86% daily values, peanut warning and refusal of the unsupported glucose guarantee pass. It correctly uses sufficient text without asking for an image. The final patent interview then completed in a separate fresh Instant Temporary chat: one substantive mechanism question, illustrative alternatives rather than invented facts, all five required boundaries and no full package or external action. **Both final-byte controls pass their original criteria.** Earlier v1 controls remain historical observations.

The workout duplicate had already been sent when an earlier browser read was blocked by automatic approval review due to the account usage limit. After explicit user resume, readback proved completion, so it was not resent. Its original authorized correction then ran once. Navigation timeouts were resolved only by readback proving the new empty context, before test submission. No alternate browser control channel bypassed the block.

Close the three reported defects and two final controls only for these recorded observations. Keep repeatability, other hosts/models/routing, provider execution tracing, live integrations and human acceptance open. Existing bounded acceptances remain historical; none grants acceptance of these new revisions. The four earlier bounded closures from batch 13 remain unchanged. No merge or promotion is authorized.

The [fixture](fixtures/native-batch14.json) pins original inputs, every candidate revision, wrappers, exact native Copy and UI capture hashes. Raw captures remain private outside Git and OneDrive. The [current matrix](native-coverage-2026-10-22.md) and [acceptance recommendations](native-acceptance-review-2026-10-22.md) distinguish defect verification, outstanding controls and human acceptance.

## Validation

The isolated tracked overlay passes repository validation (46 skills, zero issues), generator drift (807 expected files), and all 24 offline cases/99 negative checks with zero model evaluations. All 117 final regressions pass (329.453 seconds). New helper tests cover exact total/section word boundaries, populated section inventory, read-only CLI behavior, exact inline serialization, LF/CRLF preservation and combined-duration handling. Initial sandbox temp-directory errors were environmental; the focused rerun outside that restriction passed all 15 helper tests.

The generic skill-creator validator rejects the preserved `version` field identically for all three baseline/corrected pairs. That pre-existing limitation remains; it is not reported as a generic-validator pass. Repository-target validation is separate. Source CI on `985bdbd` passes all twelve checks; delivery CI must be checked against the new commit.
