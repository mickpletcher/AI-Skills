# Workout export delivery correction review

Date: 2026-10-21. Scope: existing obsidian-workout-export review candidates. PR #11 stays draft. No installation, merging or promotion.

The combined-duration correction passes two native downloaded exports. Duplicate protection and complete corrected content also pass. Native inline Copy remains unreliable: one of four exact copies starts correctly, while three begin with a blank line before YAML. The final delivery revision requires a validated canonical Markdown download on every permitted file-capable export and correction, alongside any requested inline body. Its native rerun is pending because new ChatGPT test tabs are signed out. This review does not mark that revision, inline Copy or real Obsidian ingestion passed.

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
| Final canonical-file delivery revision | Native pending | Candidate/resource/input hashes are pinned. New temporary chats are signed out; sign-in was requested before uploads. No final-revision native pass is claimed. |

Both actual combined notes use `WorkoutData/2026-10-17.md` from the source chat date and retain actual workout date 2026-10-16. They preserve strength before cycling, 180 lbs bodyweight, goblet squat 40 lbs/3 sets/5-8 rep range, bodyweight pull-ups 2 sets/4 reps, Riverside loop 12 miles/50 minutes/200 ft and skipped calf raises. `ride_duration_minutes: 50` is explicitly scoped; unknown whole-session duration, effort, speed, power, heart rate and progression are not invented.

Both duplicate workflows preserve the October 18 Upper A session. A second `owd` asks before re-exporting. Explicit authorization changes only seated row from 3 to 4 sets of 6 reps at 60 lbs; push-ups remain bodyweight, 2 sets of 8. Missing body stats, duration, effort and PRs remain unlogged. Diagnostic removal of a leading newline establishes content equivalence only. The original copied bytes remain failed deliveries.

## Evidence and limits

The [synthetic fixture](fixtures/native-workout-repairs.json) pins each revision, input hashes, unchanged tasks/source/follow-ups, actual ZIP/member hashes, captures, original Copy bytes and independent checks. Four primary cases produce eight completed domain responses across two revisions. Two first-round primary attempts returned response load failures and were retried once with identical packets. A separate plain text format probe failed to load once, then copied correctly on an identical retry. The availability control returned NO. These host/probe events do not count as domain passes. The final revision has no native execution yet.

The visible model is Instant. Exact backend identity and full effective context are unavailable. Each primary case uses a fresh Temporary chat; duplicate/correction turns intentionally share their test conversation. Criteria are kept outside uploads. Only fabricated workout data and candidate resources are uploaded. Raw chats, screenshots and actual artifacts stay private outside Git and OneDrive. No real vault, Obsidian app, other host/model, installed discovery or complete network trace is certified. Provider execution logs were not requested; independent helper replay verifies delivered bytes, not the provider's claimed command history.

Six focused regression methods and the 108-test repository suite pass. Final instruction/provenance regressions and generator drift checks are rerun after adding file delivery. Repository/PowerShell quality checks find 46 tracked skills and zero issues; 24 offline contract cases and 99 negative checks pass. These are deterministic validations, not native model evaluations. The first isolated snapshot omitted the two untracked generated helpers; its drift failure was corrected in the snapshot, then the full suite passed. Cached interpreter and PowerShell invocation issues were resolved without repository changes. Hosted checks are tracked on the draft PR delivery commit.

Acceptance remains pending. The next gate is to rerun the combined and duplicate/correction cases against the final pinned file-delivery revision after sign-in, verify all actual downloads, and continue recording native Copy separately. Earlier batch failures remain intact in the [original review](native-batch3-2026-10-21.md).
