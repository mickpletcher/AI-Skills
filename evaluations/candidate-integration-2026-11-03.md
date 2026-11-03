# Combined local candidate integration: 2026-11-03

This integrates three approved local candidates on the shared baseline `ab0d902903b2b13eb582c88ca5ba6b5e66d6957c`. It is a candidate integration, not publication, installation, promotion or acceptance of runtime compatibility.

## Pinned inputs and preserved separation

| Candidate | Input commit | Preserved scope |
| --- | --- | --- |
| n8n workflow expansion | `d4bb192942288bdbf72ef4c22ebb8337898ef81f` | Core workflow skill with AI/testing modules |
| n8n security reviewer | `bac82ebf3535152636ef1b80611f528ad21bec60` | Separate read-only review skill |
| Synthetic Test Data Generator | `8076b3a527af5bade658c208c861d95936f05cfb` | Independent schema/target-skill fixture generation, including offline Pi-hole pilot |

Every canonical skill file and each of its four generated bundles remains byte-identical to its pinned input. Existing tests for those helpers are unchanged. The integrated inventory is 38 masters and 104 proposed target entrypoints: 38 Claude, 38 ChatGPT, 14 Cursor and 14 Codex.

The original 36 bounded historical acceptance records remain historical. They do not certify these two new skills or the revised n8n-workflow candidate. The individual [core](n8n-workflow-modules-2026-11-03.md), [security](n8n-security-reviewer-2026-11-03.md) and [synthetic data](synthetic-test-data-generator-2026-11-03.md) reports retain their original standalone test counts and evidence limits.

## Reconciliation

- Combined the shared canonical JSON and Markdown catalogs, README counts, evaluation index, generated target decisions and generated resource manifest without dropping either standalone addition.
- Kept exact migration inventory equality with both new skills explicitly listed, retained new-candidate origin/provenance checks, and used exact allowed-master identities for the Codex frontmatter test instead of a hard-coded count.
- Added one regression requiring every Markdown catalog row to match the canonical inventory exactly once, including its source path and ordered target list.
- The security and synthetic branches both selected spec number 016 independently. The synthetic spec moved to 017 with all five files byte-identical; integration requirements/design/plan/tasks use 018.
- Retained all earlier changelog bytes and added current entries. Shipped sources, packages, catalog, checksums, adapters, model profiles and generator implementation remain unchanged.

## Observed offline validation

Environment: Linux, Python 3.12.14, PyYAML 6.0.3, Node.js v24.22.1. Existing tools only; no dependencies installed.

| Check | Result | Limit |
| --- | --- | --- |
| Full `python -m unittest discover -s tools/tests -v` | 225 tests: 218 passed, 7 skipped | Five PowerShell-dependent checks and two Windows-junction checks skipped |
| Focused optimized Python n8n tests | 32 passed (15 core, 17 security) | Local synthetic helper behavior only |
| Focused optimized Python synthetic-data tests | 28 passed | Local fixture generation/materialization only |
| Candidate regeneration and `--check` | 941 files generated; freshness passed | Generated candidates are not installed |
| Generator Python compilation | Passed | Syntax check only |
| Package and shipped catalog rebuild | 35 packages; outputs byte-unchanged | Local reproducibility, no release |
| Repository validation | 46 shipped skill records, zero issues | Structural checks, not candidate runtime quality |
| Evaluation harness self-test | 24 cases and 99 negative checks passed; zero actual model evaluations | Existing contract harness only |
| Independent preservation/integration review | No blocking finding in the reviewed integration content | Read-only bounded review, not native-host acceptance |
| `git diff --check` and source preservation comparisons | Passed | Local content checks |

The first integrated suite passed 224 tests with seven skips before the additional Markdown-catalog regression was added. The 225-test total includes that added test; no behavioral assertion was removed to obtain the pass. Independent review separately verified all three full master trees and all 12 generated bundle trees against the pinned inputs, JSON inventory unions, all 941 manifest hashes, shipped-tree preservation and test reconciliation. Exact final integration commit and committed-head logs are retained in the local review deliverable rather than requiring this report to embed its own future commit hash.

## Remaining verification limits

PowerShell is unavailable, so PowerShell folder/quality/installer entrypoints and the five dependent Python checks were not executed here. Windows junction behavior needs a Windows host. No new software was installed to remove those limits.

No n8n/Pi-hole service access, credential use, workflow import/execution, provider/model call, DNS change, external notification, installation, publication, shared-branch merge or promotion occurred. Native host discovery/routing, qualitative target-skill behavior and version-specific live compatibility remain unverified. Generation and offline testing are not evidence of those behaviors.
