# Cursor Skill: pr-review

Use this skill when reviewing a pull request, patch, or changed file set for regressions, practical risk, and missing tests. The goal is not to summarize the diff. The goal is to find what could break, what is under-tested, and what should block merge.

## Use When

- You are reviewing a pull request or local diff
- You want findings, not praise
- The change touches behavior, data flow, CI, auth, scripts, or deployment paths
- You need to map changed code to missing or weak validation

## Do Not Use When

- The task is to implement the feature instead of reviewing it
- The request is mainly about formatting or naming
- There is no diff, changed file list, or patch to inspect
- The user wants release notes or a summary instead of review findings

## Review Priorities

1. Behavioral regressions
2. Logic risk
3. Missing validation or error handling
4. Test gaps
5. Deployment, CI, or automation break risk
6. Docs drift when setup or usage changed

## Workflow

1. Read the pull request summary, changed files, and diff first.
2. Identify the risky areas:
   - core logic changes
   - auth or permission paths
   - API shape changes
   - state, storage, or schema changes
   - CI, workflow, or deployment changes
   - refactors that could hide behavior drift
3. Review the diff with a regression mindset.
4. Check whether the changed behavior has matching tests.
5. Prefer a short list of real findings over a long list of low value comments.
6. If no material findings exist, say that plainly and note residual risks or testing gaps.

## Output Format

Start with findings. Order them by severity.

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

- Brief merge risk statement
```

If there are no findings:

```text
Findings

No material bugs or regressions found.

Residual Risks

- ...

Testing Gaps

- ...
```

## Constraints

- Do not lead with compliments
- Do not spend time on trivia
- Tie every finding to a real file and a real risk
- Keep the output focused on merge risk

## Example Prompts

```text
Use pr-review on this diff and focus on regressions, practical risk, and missing tests.
```

```text
Review these changed files like a strict PR reviewer. Ignore style and look for behavior break risk.
```

```text
Check this patch for changed behavior without matching test coverage.
```
