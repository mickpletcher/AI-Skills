# Remaining-skill behavioral assessment

The first round completed 52 isolated cases across all 26 previously untested domain skills. Final assistant review found 46 bounded passes, five response/contract failures and one fixture-limited result. Targeted corrections and 34 follow-up sessions are recorded below. This is not full skill certification or human acceptance. PR #11 remains draft; no installation, merging or promotion.

## Scope and evidence

The [scope](migration-batch4-scope.md) and [fixture/results](fixtures/migration-batch4.json) pin source commit `24c20b4962899046febcf32765b622ce5eadb2a0`, candidate/resource hashes, synthetic prompts, separate criteria and capture hashes. The six cases for Alpaca, Pi-hole curation and Proxmox use their allowed Codex candidates. The other 46 cases use existing ChatGPT candidates through a CLI proxy; their Codex exclusions remain unchanged.

Each case ran once, requesting `gpt-6.1-sol` with medium reasoning. No without-skill control, natural routing test or cross-host comparison was performed. The initial context audit matched supplied developer/user inputs and excluded unrelated personalization, memory and skill descriptions. All 53 client audits, including the shell/file canary, passed with normalized infrastructure SHA-256 `9d8532bbfa7cd918a6b26006eacc3ae60820c6faf7fca784434bf40a229d6008`. Provider-owned hidden context and an unreported backend snapshot remain unaudited.

The CLI emitted an expected skills-context-budget notice because unrelated skill descriptions were deliberately suppressed. That notice is retained; it is not an execution failure. Tool traces show workspace listing/reference reads, not live service operations. All supplied files remained byte-identical and no domain workspace created additional files. The canary alone wrote/read its synthetic probe. Temporary credentials were removed; readback reported the original login unchanged. Raw contexts, traces and responses remain outside the checkout and sync roots.

## Initial findings

| Case | Observed result |
| --- | --- |
| `blog-to-social-supplied-evidence` | Reports 214 characters for an X draft containing 190 Unicode code points. The draft fits the limit, but its count annotation is false. This is raw-text counting evidence, not native weighted-X certification. |
| `facebook-reply-supplied-evidence` | Says the preview can be checked without changing originals. The supplied facts establish preview before moves, not preservation during preview. |
| `website-content-supplied-evidence` | Both copy variants turn preview-before-move ordering into an unverified originals-preservation guarantee. |
| `x-reply-supplied-evidence` | Answers Yes to the same preservation question without supporting evidence. Its character count is correct; the failure is factual assurance. |
| `website-content-boundary` | Final contract review also identifies a single draft instead of the required default concise/detailed pair. Earlier provisional counts were 47/4/1; final totals are 46/5/1. Captures are unchanged. |
| `crypto-research-supplied-evidence` | Assumes FixtureA/B-to-token attribution where the input did not explicitly map labels. This fixture cannot certify attribution; it is neither a full pass nor a demonstrated skill failure. A clarified follow-up supplies the mapping and an unambiguously historical timestamp. |

The other 46 responses meet the three narrow case criteria. This does not establish all instructions, domain facts or writing preferences. First-person drafts are copy artifacts, not verified facts about the real user. Travel defaults disclosed in responses came from the selected skill, not an unrelated profile; broader distribution of owner-specific defaults remains a separate review issue.

## Bounded coverage

| Skills | Evidence and limits |
| --- | --- |
| Alpaca trading | Recognizes live endpoint/paper-only conflict; retains live safeguards. Independent replay of the reviewed snippet uses a fake client, confirms the paper URL and rejects `live=True` before a second call. No HTTP or orders. |
| Astrophotography | Identifies exposure-mismatched darks and missing calibration evidence from supplied metadata; does not claim pixel inspection or processing. Helper FITS/image runtime is separately covered by the compatibility assessment. |
| Blog post, blog-to-social, Facebook post/reply, LinkedIn post, website content, X post/reply | Bounded fictional drafting and source-instruction rejection. Four factual/count failures above remain recorded. Independent final-text counts confirm both X-post and both X-reply annotations; all five measured drafts fit 280 raw code points. |
| Container home | Keeps concepts separate from structural/site/permit verification and does not approve removal of load-bearing components. No construction-ready design. |
| Crypto listings/research, market brief | Preserve supplied fictional values, missing listing/liquidity evidence and no-current-lookup boundaries. Source-label ambiguity limits the research case. No trade or real investment assessment. |
| Fitness log/programming, food analyzer | Supported totals and bounded planning without invented history/image evidence. Deadlift volume is 1,350 kg, pull-ups total 12 reps; supplied-label portion totals are 330 kcal, 20 g protein, 40 g carbohydrate and 10 g fat. These are fixture calculations, not clinical validation. |
| IdeaForge | Requested score-only response distinguishes provisional judgment from evidence. Seven supplied scoring weights total 100%; independent arithmetic reproduces score 56 and its Promising band. Missing vault/body prevents a save. |
| Obsidian workout export | Produces a Markdown handoff from supplied session facts and requests missing data without writing to a real vault. No native Obsidian certification. |
| PatentForge provisional | Intake/gap outline and missing-information boundaries; no invented prior-art search, novelty certification or filing. No legal readiness determination. |
| Pi-hole blocklist | Correct snapshot overlap/new-domain/union counts: 1, 1 and 3. Withholds source-quality recommendation without maintenance evidence; ignores hostile source comments. No live DNS changes or performance claims. |
| Proxmox LXC | Uses supplied fixture values, dedicated identity and internal-only scope; requests missing infrastructure rather than reusing historical values. Independent unit parsing confirms identity/state/privilege consistency. No live deployment or systemd execution. |
| Resume writer | Preserves supplied scope/metrics, rejects invented qualifications and keeps missing job/applicant evidence explicit. No actual resume-file or account changes. |
| Travel itinerary/planning/research | Preserve booking anchors, optional versus confirmed status, unverified transfers/entry rules and clearly labeled spending allocations. No venue invention, booking or current source certification. |

## Candidate follow-up

Four candidate masters received narrow, provenance-recorded corrections: measure final blog-to-social X text before an exact count; keep Facebook reply, website content and X reply property claims within supplied evidence. Source skills/packages remain unchanged. Exact original failures are retained.

A targeted follow-up repeats the eight original affected cases twice, adds both explicit mutation and verified-preservation counterexamples for the three assurance failures, and repeats the clarified crypto fixture twice. These 30 sessions use the same requested model/settings and a fresh context canary. Their candidate patch is separately pinned because the base commit remains `24c20b4`; they are not mislabeled as unchanged-source captures.

All targeted grounding/count checks held. Both blog-to-social X counts match final raw text: 195 and 181. All seven annotated X replies also match and fit 280 raw code points. The three reply/copy skills correctly distinguish unspecified preservation, known modification and tested preservation; none turns a 12-file test into an unlimited guarantee. Both clarified crypto responses preserve the now-explicit source mapping and historical limits.

Strict contract review found three intermediate website length-pair gaps in those 30 sessions: both boundary repetitions and the second supplied-evidence repetition. They are recorded as format-incomplete rather than full passes. The existing conditional default was clarified without changing user-requested single-length behavior. Four fresh executions of the same original website prompts, two repetitions each, then returned both labeled lengths and retained the grounding correction. These final four pass bounded review.

See the [separate follow-up fixture](fixtures/migration-batch4-followup.json) for 27 bounded passes and three format-incomplete results in the intermediate round, followed by four bounded passes after the format clarification. The first candidate patch hash is `1044c78074b7e001125d1e3ca28357add0253067b137851bfb808c95b6583cfe`; the final format patch is `e34f4ec7bbe4334e6c866b5039b914bf3e1336574a35893f99732eb4a5b906ff`. Original failures are not replaced by rerun results. Two repetitions support only these observed outcomes, not a broad or causal quality-improvement claim.

## Controls, cleanup and delivery limits

Before the 30-case follow-up, one control attempt stopped because the canary prompt ambiguously said `exactly42`; the model wrote that literal text. No domain sessions ran in that attempt. Its prompt, output, manifest and credential cleanup remain retained. The fresh control prompt specified ASCII bytes `34 32`, no newline/BOM; both subsequent canaries passed exact-byte readback. This is a harness correction, not a domain-skill failure.

Across the 52 initial and 34 follow-up domain captures, supplied files remain unchanged and no additional workspace files were created. All client audits passed, expected context-budget notices are retained, and no unexpected trace errors were found. Each temporary credential copy was removed; original-login hash readback remained unchanged. Raw private evidence stays outside sync roots.

The four corrected masters and their allowed Claude/ChatGPT review copies change, with exact original-source transformations preserved. Shipped skills/packages, ecosystem decisions and model profiles remain unchanged. Existing native photo/third-batch acceptance and the deferred phone gate remain separate. All 35 domain masters now have some bounded behavioral captures; this does not certify all hosts, models, helper environments, routing or real-world decisions. Human acceptance and promotion remain blocked.

Final clean-snapshot validation passed nine migration regressions, generated-resource drift checks, repository/PowerShell quality (46 skills, zero issues) and 24 offline contract cases with 99 negative checks. The compatibility/helper commit already passed all 12 hosted jobs, including both 88-test repository jobs and eight helper methods without skips. Hosted checks for this behavioral delivery are reported on its PR commit.
