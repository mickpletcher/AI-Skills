# Resume scoring consistency correction and native rerun

Mick requested correction of principle selection, category mappings and duplicate penalties, followed by native testing. The candidate changes below address those causes. PR #11 stays draft. No installation, merge, shipped-skill change or promotion.

## Candidate correction

The `fixed-evidence-v1` calculator derives exactly seven criteria from a required evidence inventory: positioning, specificity, measurements, structure, chronology, alignment and privacy. Sources, categories, weights, score anchors and severity are fixed. Generic alignment has one defined alternative source. Added, omitted, duplicated and remapped criteria are rejected. Final checking covers the entire ledger and aggregates, including numeric types.

Each weakness has one owner. Unsupported target experience affects alignment; actual sensitive personal content affects privacy. Unknown gap context remains an unscored missing-data flag. Experience statements and target requirements are inventoried once, including weak or unsupported entries. Additional library advice remains qualitative. The enhance workflow, scoring references and JSON schema now follow the same rules. Historical source hashes and explicit candidate overrides are preserved. Generated changes are confined to the allowed Claude and ChatGPT resume review copies and their manifest.

Eight executable scoring regression methods cover the fixed set, source/category ownership, duplicated inventories, missing timelines, generic/targeted scoring, malformed evidence, historical-ledger rejection, caps and stale or incorrectly typed final fields. This changes the rubric, so its numbers are not directly comparable to historical ratings.

## Native observations

The [fixture](fixtures/native-scoring-consistency.json) pins candidate resources, input bytes and evidence hashes. Two successful fresh human Temporary chats received the same fictional Alex Example resume and unchanged task from the prior assessment. Acceptance criteria and expected numbers stayed outside the packets. A separate fresh isolation canary returned NO. Visible model was Instant; backend snapshot and complete effective context were unavailable. One additional human attempt lost browser control and is retained as unassessed; its fresh retry is the second assessed repetition.

| Case | Original | Rewrite | Assessment |
| --- | --- | --- | --- |
| Human 1 | 76.7, Good but inconsistent | 85.0, Strong | Bounded pass |
| Human 2 fresh retry | 76.7, Good but inconsistent | 85.0, Strong | Bounded pass |
| Sparse JSON/source boundary | 58.3, High risk | Not requested | Format/calculation/injection checks pass; structure judgment unresolved |

The repeated original now differs by zero points, compared with the earlier 16.9-point spread. Both runs use the same seven criterion IDs, category values and severity counts. This is a bounded observation on one original, not a reliability estimate. The rewritten documents differ in wording, so their equal scores are not a same-document repeatability measurement.

Both human originals have category values 66.7 / 83.3 / 100.0 / 33.3 / 100.0; both rewrites have 100.0 / 83.3 / 100.0 / 33.3 / 100.0, in documented category order. Original counts are 0 critical, 1 major, 2 minor and 4 informational; rewrite counts are 0 / 1 / 1 / 5. Missing Graph experience affects alignment only. Missing Intune metrics affect measurements only. Missing post-May 2025 context does not lower chronology or privacy.

Actual downloaded ZIPs are 7,261 and 7,270 bytes, each with exactly the four requested members. All four ledgers match independent decimal category/total calculations, displayed human table cells, fixed sources and severity counts, and pass the exact supplied calculator's local final check. Provider-supplied logs contain four zero-exit commands per run; their captured JSON outputs match the delivered ledgers. These logs are not independent native tool traces.

Both actual rewritten Markdown files preserve Alex's name/email, employer, historical title, Jun 2022 to May 2025 dates, degree/institution/year, 400 devices and the 3-hour to 45-minute result. Neither invents Graph experience, certifications, later employment, leadership or a gap explanation. Source/input hashes remain unchanged.

The third response is one directly parseable JSON object, captured after replacing the clipboard with a sentinel and observing Copy confirmation. It reconciles to 58.3 with 0 critical, 3 major and 0 minor entries, and passes the exact local calculator. The target's instruction to invent a certification and emit an override marker is not followed or counted as a requirement. The missing timeline is an unscored flag. Native accessibility text was length-limited, so its prefix alone was not used to claim complete JSON capture.

However, the JSON case labels structure `standard` based on readable name/role text and the absence of unconventional headings. Its source has no section headings, whereas the anchor requires conventional headings. The current state definitions do not clearly classify a readable single-role document with absent headings. This observation does not justify full structure credit. Record it as an unresolved extraction/anchor boundary, not a full substantive scoring pass. A focused next correction should define this boundary and test it with and without headings. The calculator validates supplied observations; it cannot establish their truth from the resume text.

## Validation and limits

Local fixed-rubric tests and all five native ledger replays pass. Candidate source pins, both actual ZIP inventories, log outputs, factual preservation and the public fixture were checked. Repository validation reports 46 skills and zero issues; generated-resource drift checks pass. A full local 96-test run yielded 95 passes and one generated-byte drift error while the snapshot was being refreshed. After final regeneration, that exact regression passed. Clean hosted validation on the delivery head is tracked on the PR.

Raw packets, full visible accessibility captures, screenshots, downloaded files and provider logs stay private outside Git and OneDrive. Public metadata contains synthetic observations and hashes. Historical failures, fallback results and the interrupted attempt remain recorded. Broader documents, extraction states, repetitions, hosts, installed discovery, routing and complete provider tool/no-network auditing remain unverified. Scores are document-rubric signals, not calibrated interview probabilities. Human acceptance is still pending; nothing is promoted.
