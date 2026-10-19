# Tasks

- [x] Inventory 35 Claude skills and existing canonical foundation.
- [x] Add 32 masters and provenance with dependencies and license notices.
- [x] Generate four-target bundles without changing shipped trees.
- [x] Add migration catalog, ownership checks and regression tests.
- [x] Complete focused static review of generation, capability contracts and the three foundational masters.
- [x] Fix linked-parent/junction, destination type and portable filename collision gaps; add offline regressions and read-only generator workflow permissions.
- [x] Complete final local/CI verification of the review fixes.
- [ ] Complete target-host behavioral evaluation; the authorized foundation pilot is tracked below.
- [ ] Separately authorize promotion after behavior evidence and human review. No promotion is authorized by this pilot.

- [x] Audit three foundational masters against originals, restore portable requirements with provenance, and distinguish pasted-input modes from file operations in seven contracts.

## Review validation, 2026-10-19

- Clean Git snapshot plus the reviewed diff: all 66 Python unit tests passed on Windows with Python 3.12, including real symlink and junction fixtures. The new collision regressions also detected the original generator failures.
- Generator drift check, Python compilation, repository and PowerShell quality validation passed. Repository validation checked 46 shipped skills with zero issues; exact-case folder validation checked 35 Claude skills with zero issues.
- All 22 installer regressions passed under PowerShell 7 and Windows PowerShell 5.1 using temporary libraries.
- Synthetic fixture self-test passed 24 cases and 99 negative checks. Actual model evaluations remain zero.
- All six hosted checks passed for code commit `8b8e0b8349dc140531d15a3b704591bd484d0873`: [Windows/Linux validation](https://github.com/mickpletcher/AI-Skills/actions/runs/39272642478), [installer matrix](https://github.com/mickpletcher/AI-Skills/actions/runs/39272642167), and [generator drift](https://github.com/mickpletcher/AI-Skills/actions/runs/39272642211).
- Original shipped sources, packages, catalogs, checksums and the API runner are unchanged. Ignored local notes and the existing local itinerary-template line endings were preserved; validation used Git source bytes rather than rewriting the working files.
- PR #11 remains draft and unmerged. Host/model comparisons, helper certification, wider-distribution configuration review and promotion remain separate outstanding work.

## Foundation behavioral pilot, 2026-10-19

- [x] Prepare six synthetic cases for the three foundational skills, with comparison conditions, rubrics and hard failures.
- [x] Select the configured Codex CLI model/settings and verify a tool-disabled canary with unrelated skill descriptions removed. This did not establish complete context isolation.
- [x] Capture 36 responses: six scenarios, three instruction conditions and two fresh-session repetitions.
- [x] Record assistant triage, the line-count discrepancy, context contamination and coverage limits without claiming human approval.
- [ ] Establish and audit a clean effective prompt context, then rerun every condition. The first batch is provisional and context-confounded.
- [ ] Complete evidence-backed scoring of every human rubric. Scores remain unscored and no skill has passed acceptance.
- [ ] Complete the full host/tool/routing scenarios and human acceptance review before considering promotion.
