# Copilot Skill: pr-review

## Intent

Review pull requests and diffs for behavioral regressions, merge risk, and missing test coverage.

Use this skill when reviewing a pull request for regressions, practical risk, and missing test coverage. The goal is not to praise the change or restate the diff. The goal is to find what could break, what is weakly validated, and what should be checked before merge.

## Use When

- You are reviewing a pull request
- You want a risk focused review instead of a style pass
- The change touches behavior, data flow, security, automation, or deployment paths
- You need help spotting test gaps tied to the actual files changed

## Do Not Use When

- The task is to write the code instead of reviewing it
- The request is only for formatting or naming feedback
- There is no diff, changed file list, or pull request context
- The user wants release notes, not review findings

## Review Priorities

Focus on the highest value review work first:

1. Behavioral regressions
2. Risky logic changes
3. Missing validation or error handling
4. Weak or missing test coverage
5. Deployment or workflow break risk
6. Documentation mismatch when setup or usage changed

## Workflow

1. Read the pull request summary, changed files, and diff first.
2. Identify the main risk areas:
   - core logic changes
   - auth or permission changes
   - API contract changes
   - data model or persistence changes
   - CI, deployment, or automation changes
   - refactors that could hide behavior drift
3. Review the code with a regression mindset.
4. Look for missing or weak tests that should have changed with the code.
5. Prefer a small set of real findings over a long list of low value comments.
6. If no material findings exist, say that plainly and call out any residual testing gaps.

## What To Check

- Does the new logic still handle the old success path
- Are edge cases still covered
- Did the change alter input or output shape
- Could this break callers, scripts, workflows, or saved data
- Are null, empty, timeout, retry, or permission failure paths handled
- Did any config, secrets, environment assumptions, or file paths change
- Should tests have been added or updated
- Did docs need an update because setup or usage changed

## Output Format

Start with findings. Order them by severity.

Use this structure:

```text
Findings

1. [Severity] Short title
   File: path/to/file
   Why it matters: ...
   Suggested fix: ...

2. [Severity] Short title
   File: path/to/file
   Why it matters: ...
   Suggested fix: ...

Open Questions

- ...

Summary

- Brief overall merge risk statement
```

If there are no findings, use this structure:

```text
Findings

No material bugs or regressions found.

Residual Risks

- ...

Testing Gaps

- ...
```

## Constraints

- Do not lead with compliments or generic summary
- Do not flood the review with style trivia
- Do not invent findings without evidence in the diff
- Tie every finding to a concrete file and behavior
- Keep the review focused on merge risk

## Help And Examples

If the user asks how to use this skill, explain that it reviews a pull request for regressions, risk, and missing tests.

Minimum useful input:

- pull request diff, changed files, or patch
- enough context to understand what the change is supposed to do

Example prompts:

```text
Use pr-review on this pull request and focus on regressions, risk, and missing tests.
```

```text
Review these changed files like a strict PR reviewer. Ignore style and look for behavior break risk.
```

```text
Check this PR for test gaps. Call out any path that changed without matching coverage.
```

## Validation Checklist

- Findings point to real changed files
- Each finding explains the actual break risk
- Test coverage comments are tied to the changed behavior
- The output stays focused on review, not implementation
