# GitHub settings workflow

Use for settings advice as well as configure GitHub mode. This is guidance, not a settings executor or authorization grant. Do not run real settings mutations merely to test this skill.

## 1. Inspect current state

Confirm owner/repository, intended default branch, visibility, repository type, user role and available tool permissions. Read current repository settings, matching rulesets (including inherited organization rules), branch protection, review requirements, observed CI check names and sources, allowed merge methods, Actions policy/token defaults and available security features. Record evidence source and inspection time; do not expose tokens or sensitive settings payloads.

A missing field, 403, 404 or unsupported endpoint means **unknown or inaccessible**, not disabled or absent. Read access, file write access and settings administration are different capabilities. Inspect plan/visibility restrictions and organization/enterprise policy where accessible; otherwise mark these constraints unknown. Do not infer effective protection from a workflow file or a local configuration proposal.

## 2. Recommend a minimal, capability-aware change set

For a new project's configure-mode proposal, use this baseline only after checking current state and team needs: an accurate About description and topics; verified social preview; default-branch pull requests and actual passing required checks; no force pushes or branch deletion on the protected branch; independent review for teams with an explicit viable solo-maintainer policy; squash merging and deletion of merged working branches (not the protected default branch); least-privilege Actions; and available dependency alerts/scanning within the existing plan. This is a recommendation profile, not blanket authorization or proof of application. Do not configure nonexistent checks or lock out a solo owner.

Choose a clear, descriptive, searchable project/repository name based on the actual purpose. Automatically review even an explicit user-chosen name for clarity, descriptiveness, relevant terms, brevity, spelling and misleading claims; recommend a better alternative with rationale when useful. Respect the user's explicit final choice: reviewing a name is not permission to replace it. Check name availability in the intended owner namespace when access permits; otherwise label availability unverified. Do not promise search ranking. An existing repository rename requires explicit approval and review of integrations, clone URLs, links and automation impact; never rename silently.

Derive the About description automatically from the verified project purpose in an authorized configure task. Preserve an intentional existing description unless its update is in scope. Recommend relevant factual GitHub topics based on actual purpose, language and technology, not invented features. Topics are not Git release tags and do not authorize tag or release creation. Inspect and authorize About/topic/preview changes like other settings. Keep public versus private an explicit user choice; never infer public intent from a request for a preview.

Use a table: `Setting | Current state/evidence | Recommendation | Impact | Authorization | Result`.

- **Visibility**: retain current visibility unless a change is requested and approved. Explain exposure of code, history, Actions logs and fork consequences before approval; making a repository private does not retract existing public copies.
- **Rulesets or branch protection**: inspect existing and inherited enforcement before proposing changes. Check feature availability for this account, plan and visibility; do not promise an unavailable feature. Specify target branches, enforcement state and bypass actors, and protection against force pushes and branch deletion. Do not weaken protections, expand bypass access or replace unrelated rules implicitly.
- **Required reviews**: tailor count, code-owner review, stale-approval dismissal and last-push approval to actual maintainers. Explain solo-maintainer blocking risk instead of silently weakening the policy.
- **Required checks**: use exact names and sources observed in real CI runs. Confirm triggering paths and events so required checks can report. Unknown names remain pending; do not invent them or require a never-emitted check. A green run alone does not make its checks required.
- **Merge options**: recommend merge, squash or rebase based on history needs and active rules; include whether merged working branches should be deleted automatically, preserving the default/protected branch. Distinguish repository-level availability from merging a PR or enabling auto-merge on one; neither is authorized by settings advice.
- **Actions permissions**: inspect allowed actions/reusable workflows, default `GITHUB_TOKEN` permissions, PR creation/approval and fork workflow policy. Prefer least privilege; explain trust implications before changes. Workflow `permissions` and repository defaults are separate, and organization policy may constrain both. Never grant write tokens or secret access to untrusted fork code as a convenience.
- **Available security features**: inspect dependency graph, Dependabot alerts/updates, code scanning, secret scanning and push protection as applicable. Availability and costs vary by plan, visibility, license and organization policy. Propose only supported features, distinguish scanning from actual remediation, and flag missing licenses or access for an owner. Do not purchase, upgrade, grant access or disable security controls implicitly.

## 3. Authorize and apply narrowly

Present each proposed action with exact repository/branch scope, current and desired value, security/access/visibility or billing implications, and rollback limitations. Obtain action-specific authorization required by the host confirmation policy. Broad phrases such as “set it up” or a configure-mode choice are not blanket approval for sensitive changes. Record which actions were actually approved; a skill cannot waive confirmations.

Re-read relevant state immediately before a mutation. If it drifted, reconcile the changed proposal and obtain any newly required authorization. Use only available, permitted tooling and a minimal update that preserves unrelated fields. Never substitute a broader permission grant, organization-wide change or paid feature for an unavailable operation. Apply only the requested permitted subset; retain independent safe work when another action is blocked.

After denial, stop the denied action and report exact target, reason and known outcome. Do not bypass the restriction through another interface. If a write times out or its outcome is uncertain, inspect state before any retry; do not duplicate potentially completed changes. After partial failure, report each outcome separately; rollback is another mutation requiring appropriate authorization.

## 4. Verify and hand off

Read back each setting from GitHub and compare the actual value with the approved desired state. For protections, verify target matching, active enforcement, bypasses and applicable inherited constraints, not merely the presence of a rule. A successful API response or a generated command is not verification. If read-back fails, report attempted-but-unverified; if state mismatches, report the discrepancy without a completion claim.

Separate recommendations from applied-and-verified settings, blocked actions, unverified attempts and unchanged settings. Supply precise manual UI steps or commands only as **unexecuted proposals**, with permission prerequisites and a verification step. Do not claim tests passed, protections enabled or settings applied without evidence. Finish with artifacts, actual check results and unresolved/manual follow-ups, even for a blueprint-only response.

## Official mechanics references

Reviewed 2026-11-02; recheck current GitHub documentation when executing because availability and policy can change. These sources inform guidance, not proof of any repository's current settings.

- [Repository visibility and consequences](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)
- [Rulesets and availability](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Creating repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- [Protected branches and required checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/configuring-commit-merging-for-pull-requests)
- [Actions permissions and inherited policy](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [Security and analysis settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository)
