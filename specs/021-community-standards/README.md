# Community standards

## Requirements

Fill the missing code of conduct, security policy, issue templates, pull request template, and accessibility file identified in GitHub's Community Standards checklist. Preserve the existing description, README, contribution guidance, MIT license, skill sources, generated artifacts, and unrelated work. Do not invent reporting contacts, response deadlines, accessibility conformance, or enabled GitHub settings.

## Design

Place discoverable policies at the repository root, issue forms and their configuration in `.github/ISSUE_TEMPLATE/`, and the pull request template in `.github/PULL_REQUEST_TEMPLATE.md`. Add support routing and cross-links from the README and contributing guide. Use public issue forms for ordinary reports, conditionally available GitHub private vulnerability reporting for security reports, and an explicitly detail-free contact request as its documented fallback. Keep blank issues available as an alternative to forms.

Include the new community files in the explicit local-release allowlist so downloaded bundles keep their linked policies and template checks. Preserve deterministic packaging and source-path protections; update the fixture checksum only for these deliberate additional entries.

Funding and discussion templates are not applicable: no sponsorship destination is authorized and repository discussions are disabled. A custom vulnerability form is not needed to establish a security policy, and private vulnerability reporting has not been verified enabled. No repository settings, release workflows, or permissions are changed.

## Plan and tasks

- [x] Compare the screenshot checklist with the current default branch and inspect existing contribution rules.
- [x] Add policies, support guidance, issue forms, a PR template, and navigation links.
- [x] Add offline regression checks for form structure, discoverable paths, local targets, and reporting safeguards.
- [x] Run repository validation, tests, generator freshness, and offline evaluation checks; record platform limits in the PR.

Publication and hosted checks are recorded in the pull request: verify the exact remote tree and CI results before the authorized merge, then recheck the default-branch checklist.

## Local validation

The final suite ran 319 tests: 312 passed and seven skipped (five require PowerShell, two require Windows junction semantics). Repository validation checked 46 shipped skills with zero issues. Package/catalog rebuilds left generated outputs unchanged; generator freshness and whitespace checks passed. The offline evaluation self-test passed 24 synthetic contracts and 99 negative checks, with no model evaluations. Six new checks cover community files and forms.

The initial aggregate run exposed that the release allowlist omitted the new policies. The fix adds only the eleven community files, uses an external link for the deliberately excluded canonical-candidate documentation, and retains archive byte-equality and path-protection checks. The deterministic fixture hash was updated for the added entries. The complete suite then passed. Independent static review found no blocking defects in the policies, forms, or release changes.

## Sources and verification limits

- [GitHub community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
- [Issue form syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [Private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately)
- [Accessibility page guidance](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-an-accessibility-page-to-your-repository)

Offline tests check committed content and YAML shape, not GitHub's live rendering, enabled private-reporting settings, human response, or assistive-technology compatibility. A draft PR alone does not satisfy the default branch's Community Standards checklist.
