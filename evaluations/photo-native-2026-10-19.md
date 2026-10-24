# Native photo follow-up, 2026-10-19

Status: a fresh native ChatGPT retry delivered a matching preview and a verified downloaded ZIP. Bounded preview-content and copy-byte checks passed. Initial host failures remain recorded; complete native context/tool auditing and broader host certification remain unverified.

Mick authorized native ChatGPT or Claude testing after accepting the prior bounded CLI/proxy results. This follow-up does not approve promotion, installation, merging, a Codex placement for `photo-rename`, or broader host/model certification.

## Prepared inputs

The [fixture](fixtures/photo-native.json) pins candidate source commit `cd5d670aca6331b613e5951f3c718083c46fe56e`, instruction/contract hashes, image hashes, fabricated EXIF values, task prompts and assessment criteria. Three synthetic JPEG drawings are used: two similar red mugs with capture-date/GPS metadata and one uniform gray image with no EXIF. All coordinates and dates are fabricated test inputs, not personal travel records. Image preparation used Pillow 12.3.0; independent readback verified both metadata-bearing files and the absence of metadata in the third.

Direct image attachments support visual inspection. An accompanying ZIP preserves original JPEG bytes and the capability contract for metadata-capable host tools. The agent receives only the selected candidate, task and raw inputs, not the fixture's expected subjects, metadata values, or assessment criteria. Raw evidence remains in local non-synced evaluation storage outside the checkout. Four credential-free synthetic input files were also staged under an ignored checkout directory because Chrome could not read the app-local paths. Their ZIP hash matches the pinned fixture. No login credential is copied for this browser test.

## Execution and assessment plan

1. Use a fresh native chat; record the visible model/session controls and available file/image/runtime tools. Prefer a temporary session when the host offers it without changing global account settings.
2. Submit the exact candidate/task and original inputs. Request a preview for every image with names, confidence, evidence and uncertainty. No browsing, online geocoding, account changes or file mutation is authorized by the preview.
3. Compare actual visual descriptions and extracted metadata with independent fixture values. Honest fallback is distinct from successful metadata extraction; do not count inaccessible EXIF as an extraction pass.
4. Separately request downloadable renamed copies using the preview mapping. If host execution is unavailable, record that limitation instead of claiming runtime success.
5. Review and download any actual output archive through the host UI. Check its file set, unique names, preserved extensions, mapping and exact original JPEG hashes, including EXIF. Preserve intermediate failures and all original local files.

The native UI does not expose a complete effective system/account context. Observed temporary-chat controls can reduce some carryover but cannot establish the audited context boundary used by the CLI tests. Native results must retain this limitation. See [official project/chat guidance](https://learn.chatgpt.com/docs/projects) for the distinction between task inputs, projects and local sources.

## Initial execution record

Mick signed into the dedicated Chrome tab and confirmed the browser extension's file-URL access setting. The evaluator did not enter credentials or alter global account settings. Temporary chat was visibly enabled, with the sidebar collapsed. The visible model control said Instant; the retry menu identified `6 Instant`. No exact backend model identifier or effective system/account context was exposed.

Initial uploads using the app-local paths failed with `File is empty`, including after Mick enabled the extension setting. All four inputs had nonzero lengths. Staging the same synthetic bytes under the ignored checkout directory resolved the upload failure: the UI showed all three JPEG attachments and `originals.zip` ready to send.

The exact prepared task and candidate instructions were pasted, then expanded from the UI's pasted-text attachment into the message field before submission. The UI displayed the full instructions in the composer. The first Instant attempt and one unchanged Instant regeneration each ended with `This response couldn’t load`. A separate regeneration using the menu's `Use Thinking` option also showed that failure. These are retained as three failed delivery attempts, not three scored responses. A page reload returned an empty Temporary chat; it did not recover a response. No further retries were submitted.

No readable preview, metadata extraction output or downloadable archive was produced. The copy follow-up depends on a preview mapping and was therefore not sent. No browser download or native runtime copy verification occurred. The fixture's independent local JPEG, EXIF/GPS, ZIP membership, candidate/source-pin and SHA-256 checks passed; those checks validate the supplied inputs only.

## Initial assessment

Native host delivery is blocked at response loading. This does not demonstrate a defect in the skill instructions, so no master or adapter change is justified by these attempts. Vision, native EXIF extraction and native copy behavior remain unassessed. Claude was not tested. Preserve the prior bounded CLI/proxy acceptance separately.

At this stage the next steps were a fresh native retry, preview/copy verification and execution of the [selected next batch](migration-batch3-scope.md). The subsequent sections record that work. PR #11 remains draft; no merging, installation, placement expansion or promotion.

## Fresh retry and downloaded output

Mick authorized a retry on 2026-10-19. A separate Temporary chat first returned a visible `42` availability check. A new Temporary chat then received the same pinned candidate/task, three JPEG attachments and original-byte ZIP. The visible model control said Instant; the exact backend snapshot and effective account/system context were not exposed. No global account settings or credentials were changed.

The readable preview matched all three fixture subjects and proposed `2026_07_14_red_mug_01.JPG`, `2026_07_14_red_mug_02.JPG` and `unidentified_photo_01.jpg`. It reported both exact capture timestamps, GPS rounded to six decimals and absent metadata in the third image. It distinguished stored test metadata from real-world truth and did not infer an event or landmark. These content checks passed against expected values kept outside the prompt.

The authorized copy follow-up returned a ZIP control and verification claims. Automation could not capture a download event or resolve the rendered controls to a downloadable URL. A follow-up asked for a plain attachment without changing the JPEGs. Browser control stalled, then resumed after Mick confirmed the tab was available. Mick subsequently confirmed saving the ZIP; independent filesystem readback found two identical downloaded copies.

The actual ZIP is 17,083 bytes, SHA-256 `c28b03848ceb955d1b6ab55e522be048754b90eadfee863442a920bbab0ca3bb`. Independent inspection without extraction verified exactly three unique flat JPEG entries plus `mapping_report.csv`, no unsafe paths/symlinks and no capability-contract inclusion. Each JPEG matches its original fixture SHA-256 byte-for-byte, preserving EXIF and extension capitalization. The three-row CSV contains the correct old/new mapping and matching hashes. No input download or original local test image was replaced.

The [fixture](fixtures/photo-native.json) records the retry and artifact checks. Raw response snapshots, screenshots, the ZIP and independent checks remain in local non-synced storage. The UI exposed only a brief work summary, not a complete execution trace. Its original-file preservation, Pillow-use and no-browsing statements are model claims, not independently audited host facts. Inline illustrative image cards also appeared in the response; they are not used as proof that displayed image cards reproduce the originals. Correct subjects/metadata and exact downloaded bytes are independently checked; full no-network/tool-trace coverage is not claimed.

This completes the bounded observable preview and downloaded-copy checks. Claude, natural routing, repetitions, real personal photos and broader compatibility remain untested. Human acceptance of the native result remains pending. The [third batch now has six captures](migration-batch3-2026-10-19.md), with its own incomplete gates. PR #11 remains draft; no merging or promotion.

## Repository validation

A clean Git-byte snapshot with only the intended documentation/fixture overlay passed repository and PowerShell quality validation (46 shipped skills, zero issues), generator drift checks, and all 24 offline contract fixtures with 99 negative checks. Independent Pillow readback verified all original image hashes, exact ZIP membership, both capture timestamps/GPS values and the third image's missing EXIF. Candidate and contract hashes match the pinned commit. These local checks make no native-model or download-success claim.
