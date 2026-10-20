# Native photo follow-up, 2026-10-19

Status: native ChatGPT submission attempted; host response loading failed. Preview assessment and copy/download verification remain incomplete. No native pass or skill failure is claimed.

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

## Execution record

Mick signed into the dedicated Chrome tab and confirmed the browser extension's file-URL access setting. The evaluator did not enter credentials or alter global account settings. Temporary chat was visibly enabled, with the sidebar collapsed. The visible model control said Instant; the retry menu identified `6 Instant`. No exact backend model identifier or effective system/account context was exposed.

Initial uploads using the app-local paths failed with `File is empty`, including after Mick enabled the extension setting. All four inputs had nonzero lengths. Staging the same synthetic bytes under the ignored checkout directory resolved the upload failure: the UI showed all three JPEG attachments and `originals.zip` ready to send.

The exact prepared task and candidate instructions were pasted, then expanded from the UI's pasted-text attachment into the message field before submission. The UI displayed the full instructions in the composer. The first Instant attempt and one unchanged Instant regeneration each ended with `This response couldn’t load`. A separate regeneration using the menu's `Use Thinking` option also showed that failure. These are retained as three failed delivery attempts, not three scored responses. A page reload returned an empty Temporary chat; it did not recover a response. No further retries were submitted.

No readable preview, metadata extraction output or downloadable archive was produced. The copy follow-up depends on a preview mapping and was therefore not sent. No browser download or native runtime copy verification occurred. The fixture's independent local JPEG, EXIF/GPS, ZIP membership, candidate/source-pin and SHA-256 checks passed; those checks validate the supplied inputs only.

## Assessment and next step

Native host delivery is blocked at response loading. This does not demonstrate a defect in the skill instructions, so no master or adapter change is justified by these attempts. Vision, native EXIF extraction and native copy behavior remain unassessed. Claude was not tested. Preserve the prior bounded CLI/proxy acceptance separately.

Retry the same pinned packet in a working native host, capture an actual preview, then send the separately authorized copy request and independently verify its downloaded ZIP. The [next three skills are selected and scoped](migration-batch3-scope.md), but their model sessions have not run. PR #11 remains draft; no merging, installation, placement expansion or promotion.

## Repository validation

A clean Git-byte snapshot with only the intended documentation/fixture overlay passed repository and PowerShell quality validation (46 shipped skills, zero issues), generator drift checks, and all 24 offline contract fixtures with 99 negative checks. Independent Pillow readback verified all original image hashes, exact ZIP membership, both capture timestamps/GPS values and the third image's missing EXIF. Candidate and contract hashes match the pinned commit. These local checks make no native-model or download-success claim.
