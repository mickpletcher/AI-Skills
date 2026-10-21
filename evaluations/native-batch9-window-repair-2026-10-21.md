# Crypto-listings UTC-window fallback correction

Date: 2026-10-21. Source commit: `6b2973f7baf63d81544e0a267923169bce8110d4`. PR #11 remains draft. No merging, installation or promotion.

The candidate now leaves the anchor and both UTC windows unestablished when an exact timestamp is unavailable. The original failed native case was rerun twice in fresh Instant Temporary chats; both returned host response-load failures. There is no assessable domain response and native verification remains open. Static checks do not close that gate.

## Candidate correction

Two exact original-source transformations update the workflow and its quality checklist. An exact timestamp with timezone must establish the anchor before windows, filtering or window-based counts are derived. Supplied or authorized clock evidence can establish it; offset timestamps are converted to UTC. A report date does not justify assumed midnight. Without an anchor, the candidate must label the anchor and both windows `Not established`, leave dependent counts unavailable, and request a timestamp with timezone instead of emitting inferred date ranges. Current listing-source verification remains independently required.

The master and migration provenance are updated, then only the existing allowed Claude/ChatGPT review bundles and resource manifest change. Original shipped sources/packages, versions, original source hashes, capability contracts, ecosystem suitability/placement and promotion metadata remain unchanged. No Codex/Cursor placement is added. This focused instruction change uses existing structural/provenance regressions and actual native attempts rather than a wording-matching test.

## Controlled native rerun

The [repair fixture](fixtures/native-batch9-window-repair.json) retains the exact task, synthetic source, wrapper and external rubric from the [ninth-batch fixture](fixtures/native-batch9.json). Only candidate instruction bytes change. Reversing that substitution restores the original packet byte for byte. Capability bytes are unchanged. Criteria remain outside uploads; neither attempt receives prior output, intended answers or corrective feedback.

| Attempt | Observation |
| --- | --- |
| Corrected candidate, fresh Instant primary | Initially blank completed UI, then “This response couldn’t load.” Native Copy returns the same error. Unassessed. |
| Fresh unchanged Instant retry | Same host response-load failure in UI/native Copy. Unassessed. No regeneration or mode switch. |

Two attempts yield zero assessable domain responses and two unassessed host failures. The bounded retry sequence stops here. The original failed response remains failed and unchanged; neither retry demonstrates corrected fallback behavior. Exact native Copy bytes, screenshots, packet/staging/submission hashes and generic-schema comparisons remain private outside Git and OneDrive with hashes in the fixture. Backend identity, full context, provider-side tool history and input preservation are unavailable.

## Validation

All 108 regressions pass on a clean tracked snapshot with the candidate patch (179.253 seconds). Generator drift passes for 805 files. Repository and PowerShell quality checks pass for 46 skills with zero issues; exact-case Claude folder checks pass for 35 skills with zero issues. All 24 offline contract cases and 99 negative checks pass; these perform zero model evaluations.

Generic skill validation retains identical pre-existing `version` frontmatter rejection in both master and ChatGPT baseline/corrected pairs. The metadata is preserved rather than removed to conceal that limitation. Intended-target repository checks remain separate. CI on source commit `6b2973f` passes all five workflows and twelve individual checks; delivery CI is tracked separately.

## Remaining work

Obtain an assessable response for the unchanged corrected-candidate packet before closing crypto-listings native fallback verification. Keep the original failed output and criteria intact. This change does not verify actual live retrieval, current listings, financial accuracy, trading suitability or repeated reliability.

Food-analyzer missing-image verification, n8n workflow-review verification, blog final verification and workout initial delivery remain open. Separate bounded human review and all promotion gates remain open. PR stays draft; nothing is merged, installed or promoted.
