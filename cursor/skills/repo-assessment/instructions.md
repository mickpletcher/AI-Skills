# Cursor Skill: repo-assessment

## Intent

Assess an active repository and produce a durable handoff document with current state, risks, and the next real work item.

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

Use this skill to assess an active repository and produce a durable handoff document that explains the current state, main risks, and the real next implementation step. The goal is to leave behind something another engineer can pick up without rescanning the whole repo.

## Use When

- A repo needs a current state assessment
- The user wants a durable `assessment.md` or `project-analysis.md` style document
- You need to identify risks, stale areas, and the best next work item
- A coding session should end with a reusable handoff

## Do Not Use When

- The task is just a quick README update
- The user already knows the exact file to change and wants direct implementation
- The repo is too small to justify a structured assessment

## Workflow

1. Read the repo layout, root docs, and active scripts first.
2. Identify the real source of truth files.
3. Summarize what the project currently does.
4. Call out the biggest risks:
   - stale docs
   - broken setup
   - missing tests
   - half finished migrations
   - CI or packaging drift
5. Identify the highest value next step.
6. Write the assessment in a reusable, actionable form.

## Evidence and authorization boundaries

- Check git status before assessing the current tree. Distinguish committed content from staged, unstaged and untracked work; preserve user edits and do not reset, clean, move or delete files during an assessment.
- If the repository is inaccessible or the supplied tree/status is incomplete, request the minimum missing path, files or Git evidence. Offer only a provisional assessment of supplied material; do not imply a complete scan or invent findings.
- Cite concrete paths and line numbers or inspected configuration entries for material findings. Separate confirmed findings, hypotheses and open questions, and explain the evidence behind the single highest-value next step.
- Report checks as passed or failed only when actually executed with a recorded result. Label proposed, unavailable and unrun checks explicitly; reading a test or workflow does not mean it passed.
- Return the assessment in the conversation by default. Save or update a handoff file only when writing that file is authorized by the user's request; tool access or a request to assess alone does not grant write authorization. Report the actual destination and changes if saved. Do not implement recommendations as part of the assessment.

## Audit commands and snapshot provenance

- Inspect proposed audit commands and their invoked scripts/configuration before running them. A command named `check` or `test` may rewrite files, install dependencies or contact services. An assessment or cleanup-audit request alone does not authorize those side effects. Use existing explicit authorization when it covers the effects; otherwise leave the command unrun, explain the effects and request only the needed authorization. Continue independent read-only inspection. If effects cannot be established, report that uncertainty rather than execute to discover them.
- Record the assessed repository revision (commit SHA when available), relevant staged, unstaged and untracked changes, and inspected scope. If revision or status evidence is missing, label it unknown and keep conclusions provisional; do not invent a clean snapshot.
- Tie each reported check result to its command/workflow, result and tested revision/local state when available. Distinguish supplied historical results from checks actually executed during this assessment. Passing CI for an older revision does not validate the current tree; unknown provenance is not a current pass.
- Before finalizing, compare the available revision/status with the initial snapshot. If relevant files changed during inspection, mark affected findings stale and re-inspect them when possible; otherwise withhold the affected conclusion and state the missing evidence. Do not overwrite, reset or discard concurrent user changes.

## Output Format

```text
Project Summary

- ...

Current State

- ...

Evidence and Limitations

- Inspected paths, Git state, missing context, and checks actually run versus proposed or unrun.

Risks

1. ...
2. ...

Next Step

- ...

Recommended Follow Up

- ...
```

## Constraints

- Be actionable, not descriptive only
- Prefer the real next engineering step over a long wish list
- Use repo specific evidence

## Example Prompts

```text
Use repo-assessment on this repo and produce a durable handoff with risks and the best next step.
```

```text
Assess this project like you are writing the source of truth brief for the next engineer.
```
