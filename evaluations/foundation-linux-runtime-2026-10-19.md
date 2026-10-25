# Foundation Linux runtime continuation

Status: **bounded artifact replay passed; skill acceptance pending**. The architect master now requires formatter application, formatting/lint/test checks and delivery of the exact final file contents. All allowed review candidates were regenerated. Historical restoration provenance and raw captures remain intact. PR #11 stays draft, with no merge or promotion.

## Execution and results

The [Linux runtime run](https://github.com/mickpletcher/AI-Skills/actions/runs/39346195941) passed all five jobs at commit `d511376b139c51fdb13db3118b4c3e4593084edf`. Execution used Ubuntu, Linux kernel `6.17.0-1022-azure`, PowerShell 7.6.7 and Python 3.11.17, 3.12.15, 3.13.16 and 3.14.8. Each Python job replayed all six reviewed projects from the earlier captures. This covers the Python versions explicitly named across both proposed scaffold workflows, plus Python 3.12.

| Skill or case | Result |
| --- | --- |
| powershell-refactor | Nine Pester tests passed across all 12 prior proposals. Zero before/after PSScriptAnalyzer findings and zero new findings. |
| github-readme | Both prior candidate command sets passed installation, text/JSON output, help and unittest discovery on all four Python versions. One supplied unittest passed per draft per version. |
| github-repo-architect, scaffold 1 | 21 generated pytest cases and all independent input/error checks passed per Python version. Original formatting already passed. |
| github-repo-architect, scaffold 2 | Original formatting failed as expected on all four versions. Formatter changed only `tests/test_cli.py`, with an unchanged AST. Final format/lint checks, ten pytest cases and independent input/error checks passed per version. |
| Both focused whitespace modules | 17 generated pytest cases per module and all six independent whitespace oracles passed per Python version. |

Each Python ledger contains **78 successful check assertions**, or **312 across four versions**. This includes asserting that the original second scaffold fails formatting with exit code 1; it does not reclassify the original proposal as passing. The four pytest suites passed **65 cases per Python version**, or 260 executions of those same cases. README unittest counts are separate. Both full scaffolds also passed six independent inputs through file, implicit stdin and explicit `-`, plus invalid UTF-8, missing-file and invalid-argument checks.

All four jobs copied the final validated architect/module files into retained delivery artifacts. The uploaded Python source hashes match the final ledger hashes for every file. The original fixture bytes remain unchanged. CI continues to check formatting without rewriting files; formatter application belongs to delivery preparation.

## Method and provenance

The [reviewed runtime fixture](fixtures/foundation-runtime/projects.json) contains hash-pinned executable source excerpts, packaging configuration and proposed CI text. Full model responses and personal context remain private. README prose is replaced by synthetic packaging/input text; command arguments and supplied implementation are retained. This tests those commands and installed entry points, not an exact reconstruction of either full README draft.

Trusted dependencies were provisioned before execution. Python used separate temporary virtual environments and projects, offline/no-dependency/no-build-isolation project installs, reviewed setuptools backends, a minimal child environment and disabled pytest plugin autoload. PowerShell used Pester 5.7.1 and PSScriptAnalyzer 1.25.0 with the same default settings as the Windows phase. Generated execution ran in a separate Linux network namespace as the runner user. Checkout credential persistence was disabled. No model calls, personal inputs, live-service operations, installation of skills or promotion occurred.

Python tools were pinned to pytest 8.4.2, Ruff 0.16.6, pip 26.2.1, setuptools 84.0.0 and wheel 0.48.0. The fixture SHA-256 is `654069e92e4a1df660246b09fe204a5a1853c883c7be5a52988ef7e149bc0729`. Downloaded ledgers and delivered files were inspected after the jobs completed. Ledger SHA-256 values:

| Artifact | SHA-256 |
| --- | --- |
| Python 3.11 | `e7911d8825222fa93cc2a419a22fe40f8524fefa5084052e03501f24d9fff2eb` |
| Python 3.12 | `714598be7f0eae0832657b353d18d081dc393596eef612c423eb8d512f841fb6` |
| Python 3.13 | `347a910b5b871cd6065e622ff8d7525f09ebf3845744bc1abe0a751b86f1bfe0` |
| Python 3.14 | `0264cd59a2400eeec5d0758844151cd98091935929f5ef26c2891b8ac1a25f39` |
| PowerShell | `c505cc99df0a1f269b75aa2070825952aa13085e101c588ea87f48f0df255f33` |

## Assessment and remaining work

The earlier formatting defect is reproducible on Linux and is corrected by the delivery feedback loop without a semantic code change. The validated delivery bytes are retained, which addresses the stale-code delivery risk in this replay. Counting semantics, CLI errors, documented README commands and bounded PowerShell contracts behaved consistently across the tested Windows and Linux environments.

This is a deterministic replay of historical artifacts. It does not prove that a fresh model follows the updated instructions, uses tools correctly or generates a passing scaffold independently. The proposed workflow checks were executed by the replay harness; the generated workflow files themselves were not installed as separate repositories' workflows. Remaining work includes an independent agent/tool evaluation, other PowerShell scenarios, broader README/repository and host/routing coverage, the full revised comparison matrix and human acceptance. Keep promotion blocked.

The initial local Git-byte snapshot passed all 72 repository regressions, generator drift, the architect skill validator, 46-skill quality checks, 35 Claude-folder checks and the 24-case/99-negative-check offline self-test. Hosted regression testing subsequently caught a newly added relative workflow link missing from release bundles. That documentation link was changed to an immutable hosted source URL; final validation is tracked in the PR and migration checklist.
