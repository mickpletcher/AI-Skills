# Local validation evidence

Scope: review items 2, 4, 5 and 6, developed locally from commit `701a5d616376e58c78a11938a2a76a3388993d52`. These are implementation/structural results, not model-quality certifications.

| Check | Observed result |
| --- | --- |
| Python environment | Python 3.11, PyYAML 6.0.3, macOS |
| Python regression suite | 26 tests passed; validators, failure fixtures, evaluation contracts, moved sections, release gate/reproducibility, workflow structure |
| PowerShell environment | PowerShell 7.5.4, macOS |
| Installer regression suite | 15 tests passed, including temporary installation of all 35 rebuilt packages |
| Folder validator wrapper | 35 Claude skills checked, zero issues |
| Full validator wrapper / Python CLI | 46 skills checked, zero issues |
| Reproducible packages | All 35 archives match deterministic rebuilds, source member sets and canonical payload bytes |
| Catalog/checksums | Generated outputs match current sources/packages; 46 catalog entries |
| Offline evaluation harness | 24 synthetic cases and 99 negative checks passed; zero model evaluations performed |
| Empty response evaluation | All 24 scenarios report `not_run` |
| Selective reference moves | Five complete sections match contiguous baseline text and recorded SHA-256 hashes |
| Release gate | Actual empty LICENSE produces a nonzero refusal before creating output |
| Release test fixture | Two builds from the same temporary fixture produce identical bundles/checksums; existing output is refused |
| Diff whitespace | Passes with `core.whitespace=cr-at-eol` for preserved existing CRLF source lines |

The resume entry point shrank from 786 to 162 lines; the itinerary entry point from 574 to 307 lines. The moved details remain required when the corresponding workflow is selected. The six former astrophotography section failures were resolved using existing boundaries/workflow text plus explicit examples/checks.

## Limits and owner decisions

- The Windows/Linux GitHub matrix passed for commit `7173462f3e491bf274099cb0ee1fd146f62f3423` ([run evidence](https://github.com/mickpletcher/AI-Skills/actions/runs/38459029576)). Windows PowerShell 5.1 is not part of that matrix and remains untested.
- Markdown navigable internal links and anchors are checked. External URLs, arbitrary runtime paths, and template placeholder URLs are not fetched or certified.
- No actual model evaluation, production installation, release, workflow dispatch, or account-setting change was performed.
- Required-check enforcement must be configured separately by the owner; adding a workflow alone does not block merging.
- At the time of this validation, `LICENSE` was empty. The owner has since selected MIT; see [current licensing and release requirements](distribution.md#license). The empty-license regression fixture remains enforced.
- Initial versions remain undeclared for `astrophotography-processing`, `github-readme`, `github-repo-architect`, and `idea-forge`. The catalog preserves null values; the owner must decide versions before describing those as independently versioned releases.
- Package sizes increase because ZIP_STORED avoids compressor-version differences. The largest rebuilt archive is approximately 1.53 MB.
- Installer extraction resource limits from the separate post-merge review are not implemented in this change. The merged installer implementation remains unchanged; the test harness resets expected child-process failures after successful completion so CI receives the correct exit status.
