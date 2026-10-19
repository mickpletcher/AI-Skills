# Foundation runtime pilot, 2026-10-19

Status: **bounded Windows runtime testing started; acceptance pending**. PowerShell and README checks passed. Architect counting/tests passed, but one original proposal failed its configured formatting gate. A separate format-only repair passed; the original failure remains recorded. PR #11 stays draft. No skill, model profile, package or catalog is promoted.

## Fixture repair

[Foundation fixture revision 2](fixtures/foundation-pilot.json) defines a nonempty line exactly as `bool(line.strip())`. Empty lines and ASCII/Unicode whitespace-only lines, including spaces, tabs, U+2003 and U+00A0, do not count. A final non-whitespace line counts without a trailing newline. File reading recognizes LF, CRLF and CR.

The scaffold prompt, rubric and hard failures now state this contract. A seventh scenario, `architect-whitespace-regression`, requests a complete counting module and pytest tests. Its six independent runtime cases cover empty input, ASCII whitespace, Unicode whitespace, mixed content, universal newlines and an unterminated final line. Three repository regressions pin the contract and reject three incorrect counters: counting whitespace as content, trimming ASCII only, and dropping unterminated lines.

The previous six-case text-only assessment remains historical under its recorded fixture hash. Its scores have not been reassigned using a later contract. The complete revision-2 comparison matrix would require 42 responses; this phase captured only four targeted candidate responses, not that full matrix.

## Runtime scope and method

- PowerShell: execute the 12 hash-verified proposals from the prior isolated capture, covering all three instruction conditions and both repetitions for pipeline/injection cases.
- README: execute documented installation, text/JSON examples, help and unittest discovery for the two prior candidate drafts, using the supplied synthetic Python repository.
- Architect: capture two fresh full scaffolds and two focused regression proposals with the revised prompts, then execute their reviewed code and tests.
- Model capture retains the separate profile, fixed base instructions, disabled tools/memory and per-call context audits. All four captures and five rendered contexts passed integrity checks, with constant host/base context and no observed contamination or tool events. Temporary evaluation credentials were removed after capture.
- Runtime execution is a separate, explicitly authorized phase. It uses temporary projects, per-project virtual environments, restricted network access, a minimal environment for Python children, disabled pytest plugin autoload and offline pip installs with a reviewed setuptools backend. Trusted test dependencies were prepared separately from cache. No personal inputs, credentials, live services or credential-vault implementation are exercised.
- Captured responses and extracted source blocks are hash-checked and retained. Formatting is checked before repair. No failing original artifact is overwritten to manufacture a pass.

This tests supplied artifacts on Windows. It does not establish automatic routing, live repository inspection/editing, autonomous tool use by the evaluated model, Linux behavior or broad host/model portability.

## Results

| Area | Evidence | Result |
| --- | --- | --- |
| PowerShell 7.6.7 | Nine Pester tests across all 12 proposals; default PSScriptAnalyzer before/after | 9 passed, 0 failed; 0 analyzer findings before/after |
| Windows PowerShell 5.1.26100.9711 | Same nine tests and analyzer comparison | 9 passed, 0 failed; 0 analyzer findings before/after |
| README repetition 1 | Offline install, documented text/JSON examples, help, unittest discovery | All five commands passed; one supplied import test passed |
| README repetition 2 | Same checks using its documented README input example | All five commands passed; one supplied import test passed |
| Architect scaffold repetition 1 | Editable install, generated tests, lint, formatting, console entry point, independent input/error cases | All 26 command checks passed; 21 pytest cases passed |
| Architect scaffold repetition 2 | Same checks | 25 of 26 command checks passed; 10 pytest cases passed; formatting failed |
| Whitespace regression repetition 1 | Generated tests, lint, formatting and six independent oracles | All four command checks passed; 17 pytest cases passed |
| Whitespace regression repetition 2 | Same checks | All four command checks passed; 17 pytest cases passed |

The accepted Python execution ledger contains 70 command checks: 69 passed and one formatting check failed. The four generated pytest suites passed **65 cases** in total. Each full scaffold also passed all six independent whitespace inputs through file input, implicit stdin and explicit `-` stdin, plus invalid UTF-8, missing-file and invalid-argument checks. Both focused modules passed the six independent oracles. The two fresh scaffold repetitions agree on whitespace semantics.

PowerShell probes compare named, pipeline, empty-string, null, omitted and empty-pipeline behavior against the original function, including output type/property/order and parameter binding. Injection-case functions still return the literal string `ok`. Both editions used Pester 5.7.1 and PSScriptAnalyzer 1.25.0, with identical default analyzer settings before/after. This does not cover the remaining full PowerShell scenarios or repository-specific analyzer settings.

README installs used offline/no-build-isolation/no-dependency flags with preprovisioned build tools. The commands exercised the installed console entry point and actual expected output, rather than the README's illustrative numbers. Online bootstrap, arbitrary repository documentation and licensing review are outside these command checks.

## Architect formatting failure and repair

The second scaffold's `tests/test_cli.py` used a multiline `ending.join(...)` expression that Ruff 0.16.6 formats onto one line. Its proposed CI runs `ruff format --check .`, so this original proposal does not meet its configured local CI gate despite passing pytest and lint. Hosted execution of that generated workflow has not been performed.

A separate copy received only `ruff format tests/test_cli.py`. The source-file hash comparison confirmed that only that test file changed, and its Python AST remained identical. That copy was reinstalled into the second scaffold's isolated environment; offline installation, lint, format checking and all ten pytest cases passed. Those ten repeated cases are not added to the original total of 65. The original response, extracted files and failing result remain unchanged. A repaired local example is not an independent generation pass or skill acceptance.

## Harness corrections and evidence limits

The initial Python extraction skipped test blocks when prose appeared between a file heading and its fence. Those incomplete-project attempts are invalid harness runs, not model failures. The corrected extractor preserves intervening prose, handles nested Markdown fences, rejects traversal/duplicates/unclosed blocks and requires all expected project files before execution. Five offline extraction regressions passed. Accepted results above come from fresh projects and virtual environments after that correction.

Pester's optional TestRegistry helper attempted sandbox-blocked registry access. TestRegistry and unused TestDrive support were disabled; no registry permission was granted. Windows PowerShell needed explicit paths to the already installed trusted modules. Both accepted edition runs used `-NoProfile -NonInteractive`. An initial repair-scope assertion also needed Windows path normalization; the accepted repair was repeated from a fresh copy with an explicit one-file/unchanged-AST check. Earlier attempts remain local and are excluded from pass counts.

## Repository validation

All 69 Python repository regressions passed on Windows/Python 3.12, including the three new fixture regressions. Generator drift, repository/PowerShell quality and exact-case folder checks passed: 46 shipped skills and 35 Claude folders, zero issues. The separate offline contract self-test passed 24 cases and 99 negative checks without model calls. Validation used Git source bytes plus the reviewed changes and preserved ignored notes and existing checkout line-ending differences. These repository checks are separate from the captured runtime results above.

## Tooling and provenance

Python execution used Windows/Python 3.12.13, pytest 8.4.2, Ruff 0.16.6, setuptools 84.0.0, pip 26.2.1 and wheel 0.48.0. Full resolved dependencies, command output, extracted file hashes and timestamps remain outside Git. The requested model was `gpt-6.1-sol`, medium reasoning, Codex CLI 0.163.0-alpha.10.2; a backend snapshot and temperature were not reported.

Instruction sources are pinned to `a4c3c2ae789e515b38f55718fed5a4ab21748cc7` and unchanged from the prior captures. The revised fixture was captured from the reviewed working tree and snapshotted before calls. Source/fixture/response hashes cover bytes; input/context hashes cover normalized UTF-8 text.

- Revision-2 fixture SHA-256: `7c778dd26bdf6a5fb9a3934f90694601ef0602a6d881141529dc319150efcb9f`.
- Four-response capture manifest SHA-256: `fa9e5ca2902ba3abb75380f739a8e61c185fab8bbf1503b3edc85f2e7553b477`.
- Accepted Python execution ledger SHA-256: `e5cc5880c798f65bf0c802befa15fbb124d2883dddd40cd3cb780c3a7d99a316`.
- Separate format-repair ledger SHA-256: `4bac378bd92716ada4dafb64ac13f9bdb8088d9683ab194fe0f6f7a5e1547ec8`.
- PowerShell 7 ledger SHA-256: `e1cb9b0b096a6d178fd5dd0b605cef4d6efa76468375ac30b8b7070e383840cf`.
- Windows PowerShell ledger SHA-256: `639ed23c0c36c6e6936e266aa420222c4116042c2bf29f427bbad3e853cff111`.

## Remaining acceptance work

Exercise actual agent file/tool workflows with formatter/test feedback, complete the other PowerShell cases, test README workflows against additional synthetic repositories, and run the generated scaffold checks on Linux and supported Python versions. Extend host/routing/model coverage and obtain human acceptance. Keep the raw formatting failure visible until the delivery workflow demonstrates it handles the configured gate. Do not merge or promote from this pilot.
