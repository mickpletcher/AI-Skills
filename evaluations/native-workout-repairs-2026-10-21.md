# Workout export delivery correction review

Date: 2026-10-21. Scope: existing obsidian-workout-export review candidates. PR #11 stays draft. No installation, merging or promotion.

Latest bounded review: the corrected candidate passes a new 895-byte combined ZIP, a 324-byte corrected strength download and a separately requested 324-byte recovery of the original strength data. Both re-exported notes exactly equal their entire native Copy-code output, with frontmatter at byte zero and no unlogged program. Duplicate protection asks Skip/Overwrite before a second export. Initial delivery remains unassessed after host response load failures; the recovery is not an initial-delivery pass. Mick subsequently accepted these bounded observations on 2026-10-21; the initial-delivery issue remains open. Earlier failures and mode differences remain explicit below.

## Changes

Top-level duration now means the entire note's session. Combined notes omit it unless a whole-session total is explicitly supplied. Partial activity times remain scoped to that activity. A read-only standard-library validator rejects leading whitespace, BOMs, fences, missing note boundaries and unsupported/nonfinite durations. Combined duration additionally requires the explicit source total. It does not establish source truth or parse full YAML; independent YAML parsing remains separate.

Delivery instructions build one canonical UTF-8 note, validate and read it back for each correction, and put the delimiter immediately after the opening plain text fence. Two native rounds demonstrate that this instruction alone cannot certify the host's Copy control. The final revision therefore requires the validated file whenever downloadable output is available and permitted, even when the user also asks for the body in chat. Hosts without file delivery must disclose the unverified inline boundary. File validation must never be presented as native Copy or Obsidian ingestion verification.

Only this master, its existing allowed Claude/ChatGPT candidates, provenance, capability declaration, new helper, regressions and review records change. Original shipped skills, packages, catalog IDs, suitability and promotion metadata remain unchanged.

## Native results

| Round and path | Result | Evidence |
| --- | --- | --- |
| First repair, combined download | Bounded pass | Actual 744-byte ZIP contains only the intended note and folder. Frontmatter starts at byte zero; full YAML parses. No whole-session duration is invented. |
| First repair, original strength Copy | Boundary passes | Actual 323-byte Copy begins with `---` at byte zero and matches visible code. |
| First repair, corrected strength Copy | Delivery failure | Actual 325-byte Copy begins with LF before `---`, despite plain text delivery. Content correction and duplicate protection pass separately. |
| Tighter correction instructions, combined download | Bounded pass | Actual 737-byte ZIP independently passes the same date, duration and source checks. |
| Tighter correction instructions, both strength copies | Delivery failures | Both exact 325-byte copies start with LF. Visible code and clipboard agree. Repeated export asks Skip/Re-export; explicit correction returns one complete replacement. |
| Final canonical-file delivery, combined download | Bounded pass | Actual 743-byte ZIP has the intended folder/note, byte-zero frontmatter, valid YAML and preserved/scoped source data. Candidate/resource/input hashes match the final pinned revision. |
| Final canonical-file delivery, duplicate/correction | Unassessed host failures | Sign-in was confirmed, but the original task, one fresh-chat retry and one unchanged Instant regeneration each returned a response load failure. No initial output, duplicate follow-up or corrected delivery was assessed in this revision. |

All three actual combined notes use `WorkoutData/2026-10-17.md` from the source chat date and retain actual workout date 2026-10-16. They preserve strength before cycling, 180 lbs bodyweight, goblet squat 40 lbs/3 sets/5-8 rep range, bodyweight pull-ups 2 sets/4 reps, Riverside loop 12 miles/50 minutes/200 ft and skipped calf raises. `ride_duration_minutes: 50` is explicitly scoped; unknown whole-session duration, effort, speed, power, heart rate and progression are not invented.

Both duplicate workflows preserve the October 18 Upper A session. A second `owd` asks before re-exporting. Explicit authorization changes only seated row from 3 to 4 sets of 6 reps at 60 lbs; push-ups remain bodyweight, 2 sets of 8. Missing body stats, duration, effort and PRs remain unlogged. Diagnostic removal of a leading newline establishes content equivalence only. The original copied bytes remain failed deliveries.

## Evidence and limits

The [synthetic fixture](fixtures/native-workout-repairs.json) pins each revision, input hashes, unchanged tasks/source/follow-ups, actual ZIP/member hashes, captures, original Copy bytes and independent checks. Four primary cases produce eight completed domain responses across two revisions. Two first-round primary attempts returned response load failures and were retried once with identical packets. A separate plain text format probe failed to load once, then copied correctly on an identical retry. The availability control returned NO. These host/probe events do not count as domain passes. The final revision adds one completed combined response and three unassessed duplicate primary/regeneration attempts. Its follow-up turns were not sent because no initial export was available. Two failure DOMs/screenshots are retained; the third failure was observed in the live DOM before browser control reset and then reported an unattached debugger. No third screenshot is claimed. Sign-in is no longer the blocker.

The visible model is Instant. Exact backend identity and full effective context are unavailable. Each primary case uses a fresh Temporary chat; duplicate/correction turns intentionally share their test conversation. Criteria are kept outside uploads. Only fabricated workout data and candidate resources are uploaded. Raw chats, screenshots and actual artifacts stay private outside Git and OneDrive. No real vault, Obsidian app, other host/model, installed discovery or complete network trace is certified. Provider execution logs were not requested; independent helper replay verifies delivered bytes, not the provider's claimed command history.

Six focused regression methods and the 108-test repository suite pass. Final instruction/provenance regressions and generator drift checks are rerun after adding file delivery. Repository/PowerShell quality checks find 46 tracked skills and zero issues; 24 offline contract cases and 99 negative checks pass. These are deterministic validations, not native model evaluations. The first isolated snapshot omitted the two untracked generated helpers; its drift failure was corrected in the snapshot, then the full suite passed. Cached interpreter and PowerShell invocation issues were resolved without repository changes. Hosted checks are tracked on the draft PR delivery commit.

## Program-template repair and bounded delivery review

A new Instant attempt again failed to load and remains unassessed. A separate fresh GPT-6 Medium run produced an actual initial file despite a response load failure. Its two 365-byte downloads and corrected Copy preserved exercises and correction behavior, but included `15 Percent Body Fat Project`, matching the candidate's hardcoded example program and absent from the session. Boundary/YAML validation passed while source fidelity failed. Both files and the exact Copy remain failed source-fidelity evidence.

The master now uses `[program name, only if explicitly logged]` and omits that line when the source does not name a program. Two exact transformations are recorded in migration provenance; allowed candidates are regenerated. No helper, capability, source/shipped resource, placement or promotion change is involved. This narrow instruction repair is supported by the captured failure; the existing helper still does not verify source truth.

Both cases were rerun with unchanged original tasks, source bytes and two original duplicate/correction follow-ups. Fresh temporary chats used the picker label GPT-6 Medium; its regeneration menu says 6 Thinking. This is distinct from the earlier Instant runs, not proof of Instant recovery or exact backend identity.

| Latest path | Result | Exact evidence |
| --- | --- | --- |
| Combined download | Bounded pass | Actual 895-byte ZIP contains only the requested folder/note. Full YAML preserves both dates, ordered activity metadata and all source values. Ride duration stays 50 minutes; no combined total or program is invented. |
| Initial strength delivery | Unassessed | Two host response load failures, including one unchanged regeneration. No initial file or code body was available. The whole-response Copy returns only the load-error message. |
| Duplicate follow-up | Bounded behavior pass | The exact `owd` follow-up asks Skip/Overwrite without producing another output. The inaccessible initial file's state is not independently verified. |
| Authorized 4-set correction | Bounded delivery/source pass | Actual 324-byte original download equals the entire 324-byte native Copy and visible note. Byte-zero frontmatter and full YAML pass. All supplied facts remain; the unlogged program is omitted. |
| Original 3-set recovery | Bounded recovery pass | One additional explicitly authorized original-source re-export yields an actual 324-byte original download exactly equal to its 324-byte native Copy and visible note. It is a recovery control, not a replacement for the failed initial delivery. |

The additional recovery prompt and source values are recorded verbatim in the fixture. It changes no expected facts and does not give the model the discovered program defect or assessment criteria. Corrected and recovered notes differ only in row set count, 4 versus 3. Push-ups remain bodyweight/2 sets/8 reps. Body stats, duration, effort, program, PRs and progression remain absent or unlogged. No whitespace was stripped from any download or Copy to obtain a boundary pass. A baseline download click timed out, but the actual new file arrived and its original bytes were verified without resending the click.

All 108 repository regressions, generator drift (805 files), intended-target repository/PowerShell quality (46 tracked skills, zero issues) and 24 offline cases/99 negative checks pass. The generic skill-creator validator still rejects the pre-existing `version` key in canonical/ChatGPT frontmatter; that schema limitation is retained, with target/provenance checks passing. No metadata removal or Codex placement expansion was used to conceal it. Hosted checks are tracked on the draft PR delivery commit.

Independent review supports bounded acceptance of source-faithful combined downloads, duplicate confirmation, corrected/recovered file delivery and their observed exact Copy bytes in this Medium run. Mick accepted these bounded observations on 2026-10-21 and authorized the next untested native batch. Cold-start initial delivery, repeatability, Instant recovery, broader hosts/models/routing and real Obsidian ingestion remain open. Earlier batch failures remain intact in the [original review](native-batch3-2026-10-21.md).
