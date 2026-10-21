# n8n retry and container-home context corrections

Date: 2026-10-21. Source commit: `d32d857e4d0334d9922b6afff217015c0eb0f449`. PR #11 stays draft. Blog verification and workout initial delivery remain open. No merging, installation or promotion.

The corrected n8n design and fictional home sequencing cases pass bounded native review. Verification of the corrected n8n existing-workflow review remains open: its two Instant attempts and one separately labelled Medium attempt returned host response-load failures. Static validation and the design-case pass do not establish a pass for that missing response.

## Candidate changes

n8n now derives retry decisions and test expectations from the same supplied contract: allowed statuses/error classes, total-attempt limits, terminal outcomes and uncertainty. Idempotency does not authorize an excluded retry. Lost responses or transport errors are not silently converted into eligible HTTP statuses. If the contract does not permit retrying them, stop automatic retries and report uncertainty; reconciliation requires separate permission. Review mode explicitly checks every example/test row against that policy.

Container-home now establishes the project in scope before applying historical background. Current supplied facts take precedence. Fictional, synthetic and alternate projects use their own supplied facts without inheriting historical location, ownership, retirement purpose, construction history or additional planned structures. Constraints and quality checks agree with that boundary. General phase/safety principles remain usable; requests about Mick's real project can still use relevant historical context without treating it as verified current status.

Seven exact original-source transformations are recorded: two for n8n and five for container-home. Regeneration updates existing allowed review targets only: n8n's Claude/ChatGPT/Codex/Cursor bundles and container-home's Claude/ChatGPT bundles. No placement expansion. Original shipped instruction/package bytes, versions, source hashes, capabilities, suitability and promotion metadata remain unchanged. No helper or wording-matching regression is added for these instruction-only corrections; existing provenance regressions and actual native responses provide verification.

## Controlled native execution

The three original tasks, synthetic sources, capability contracts, wrapper and external criteria remain unchanged. Packet reversal proves that only candidate instruction bytes changed. Criteria stay outside uploads. Each attempt uses a fresh Temporary chat without corrective answer feedback. Five attempts use Instant; the final existing-workflow review is a separate GPT-6 Medium attempt with identical bytes. Exact backend identity and full effective context are unavailable.

| Attempt | Outcome |
| --- | --- |
| n8n design, Instant | Bounded pass. Auth, noncoercive validation, atomic dedupe, distinct response branches, explicit attempt initialization/increment and three-total-attempt ceiling remain intact. Both routing and T12 now stop after one lost-response attempt with uncertainty/no retry. Unexpected HTTP 500 is also not retried under the supplied contract. |
| n8n existing-workflow review, Instant primary | Unassessed host response-load failure. No review available. |
| Home sequencing, Instant primary | Unassessed host response-load failure. No checklist available. |
| n8n existing-workflow review, fresh unchanged Instant retry | Unassessed host response-load failure. No review available. |
| Home sequencing, fresh unchanged Instant retry | Bounded pass. Explicit fictional baseline, no historical location/retirement/owner-solo narrative or added gym/storage structures. Supplied 640/1,280 area, two current/two future containers, unknown layout, 15 kW target and 12 − 2 = 10 trim arithmetic remain correct. Moisture/structural/septic/load and procurement gates remain conditional. |
| n8n existing-workflow review, separate unchanged Medium attempt | Unassessed host response-load failure. This is a separate mode observation, not Instant recovery. |

Six attempts yield two completed domain responses and four unassessed host failures. Retries stop at this bounded sequence. Instant was restored and its UI state retained. A tab-navigation timeout recovered an already-created tab before any submission; later design readback timeouts recovered the existing response without resubmission. Those control interruptions add no model attempts.

The home reply retains general off-grid phase terminology, without asserting an existing off-grid installation. It does not establish building suitability or regulatory approval. The design reply leaves unknown HTTP handling for uncertain outcomes as an implementation prerequisite, rather than inventing a vendor contract. Neither pass certifies actual engine execution, real construction or repeated reliability.

## Evidence and validation

The [repair fixture](fixtures/native-batch7-repairs.json) pins resources, original/current packet hashes, exact native Copy bytes, UI captures, modes, restoration proof, schema comparisons and independent checks. The [original seventh-batch fixture](fixtures/native-batch7.json) and its failed responses remain unchanged. No response is normalized or rewritten to obtain a pass. Raw evidence stays private outside Git and OneDrive. Provider-side tool/network history, input-byte preservation and complete context isolation remain unaudited.

All 108 regressions pass on a clean tracked snapshot with the candidate patch. Generator drift passes for 805 files. Repository/PowerShell quality checks pass for 46 skills with zero issues; exact-case folders pass for 35 Claude skills. All 24 offline contract cases and 99 negative checks pass; these are not model evaluations. The existing Codex n8n entrypoint passes generic skill validation in both baseline/corrected forms. Four master/ChatGPT baseline/corrected pairs retain identical pre-existing `version` frontmatter rejection. No metadata removal conceals that limitation. Hosted checks are tracked on the delivery commit.

## Remaining work

Obtain an assessable native response for the corrected n8n existing-workflow review, keeping its task/source and candidate pins unchanged. Its original policy/test inconsistency remains failed until a new response can be assessed. Separate bounded human acceptance remains pending. Blog verification, workout initial delivery, broader hosts/models/routing, real n8n compatibility and construction suitability remain open. PR stays draft; no merge, installation or promotion.

## Unchanged-candidate review rerun

At commit `e4cbe182af6eb74c603a9c114a1c550bf43df1a3`, one new Instant Temporary chat received the exact existing n8n review packet (`722abfa3…fdef3de7`). Candidate resources, task, synthetic source, wrapper and external criteria remain unchanged. Upload completion and Instant mode were verified before the single submission. The response ended with “This response couldn’t load.” No review or test matrix is available; this is another unassessed host failure, not a candidate pass or a new behavioral failure. No regeneration or mode change followed.

The fixture retains this continuation separately from the original six repair attempts. Cumulative repair evidence now has seven attempts, two assessable responses, two bounded passes and five unassessed host failures. The existing-workflow review verification gate and separate bounded human acceptance remain open. Private packet, staged/ready/submitted/final UI states, conversation and screenshot hashes are recorded without publishing raw evidence.

CI on the unchanged candidate commit passed all five workflows and twelve individual checks. Generator drift also passed locally. Earlier regression results remain attached to their original revision. Blog verification and workout initial delivery remain open. PR #11 stays draft; nothing is merged, installed or promoted.

The evidence overlay passes repository validation on a clean tracked snapshot (46 skills, zero issues) and all 24 offline contract cases/99 negative checks. A direct working-folder check included unrelated ignored legacy files and reported nine issues; those files were preserved and excluded from the tracked-snapshot result. No new candidate code requires another regression run beyond the passing candidate CI.
