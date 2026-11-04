# Security Policy

## Scope and supported versions

AI Skills contains instructions, reusable skill packages, examples, and maintenance or automation helpers. Report vulnerabilities in repository-owned code, packaging, workflows, or instructions that could expose private data or enable unauthorized actions. Review the relevant skill's permissions and prerequisites before running it.

Security fixes target the current `main` branch. Historical commits, old downloads, local modifications, and unpromoted review candidates do not have a separate backport or support commitment. Identify the exact commit or package version in a report. Generated candidates are not certified secure or production-ready, and a successful static check is not a security guarantee.

## Report a vulnerability privately

**Do not put vulnerability details, exploit steps, credentials, private prompts, or personal data in public issues or pull requests.**

1. Open this repository's [Security page](https://github.com/mickpletcher/AI-Skills/security). If **Report a vulnerability** is available, use that private form.
2. If that option is unavailable, open a [new issue](https://github.com/mickpletcher/AI-Skills/issues/new?title=Request%20for%20private%20security%20contact) titled **Request for private security contact**. Ask @mickpletcher for the preferred private reporting route. Include no vulnerability details, affected private systems, or secrets.
3. Wait for a private route before sending the report. GitHub's private-reporting feature is a separate repository setting; the presence of this policy does not mean it is enabled. See [GitHub's private reporting guidance](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately).

If a credential has already been exposed, revoke or rotate it with its issuing service. Removing a public message or file alone does not invalidate the credential.

## What to include in the private report

- The affected repository path, commit, skill/package version, and relevant runtime or host version.
- A clear description of the security impact and the permissions or conditions needed.
- Minimal reproduction steps using synthetic data or redacted examples.
- Expected and observed behavior, plus a possible fix if known.
- Any disclosure constraints and whether the issue is already public.

Never include live credentials, unnecessary personal data, or another person's private files. Test only systems and data you own or have explicit permission to assess. Do not use a report as permission to scan third-party services, access accounts, or run destructive tests.

## Handling and disclosure

The repository owner reviews reports, requests clarification where needed, and coordinates fixes and disclosure according to impact and available capacity. Please coordinate publication of exploit details through the private reporting route while a report is being assessed. There is no guaranteed response or fix deadline, paid support commitment, or bug-bounty program established by this policy.

For a vulnerability solely in an upstream host, dependency, or service, follow that provider's security policy. Report the repository's affected integration privately here if it also needs a change. Ordinary bugs and usage questions can use [public issue templates](https://github.com/mickpletcher/AI-Skills/issues/new/choose) after sensitive details have been removed.
