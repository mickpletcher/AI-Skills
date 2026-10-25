---
name: spec-writer
description: Generate numbered repo spec folders with clear requirements, implementation plans, and task lists for non-trivial project work.
version: 1.1.0
---

# Spec Writer Skill

## Intent

Use this skill to turn a rough repo change, feature idea, cleanup effort, or migration into a numbered spec folder with practical planning documents. The goal is to create a working spec package that another engineer can pick up and execute without guessing what the work means.

## Use When

- The user wants a new spec for a repo change, feature, refactor, migration, or workflow
- A project needs structured `requirements.md`, `plan.md`, and `tasks.md` documents
- The repo already uses numbered spec folders and new work should follow that pattern
- The request is large enough that ad hoc notes would be too loose

## Do Not Use When

- The change is tiny and does not need formal planning
- The repo has no spec workflow and the user only wants direct implementation
- The user wants a README, assessment, or changelog instead of an execution spec
- The available context is too thin to produce honest requirements and next steps

## Workflow

1. Read the repo context and Git status first; identify existing planning files and user edits.
2. Inspect existing specs for work matching the user's goal before assigning a number. Compare scope and acceptance criteria, not just folder names. Reuse a matching stale spec when the requested update is authorized; do not create a duplicate merely because its status is old. If multiple specs match or reuse conflicts with the user's requested destination, ask which to use before writing.
3. Confirm the spec root, numbering convention and complete relevant directory listing. With incomplete or inaccessible numbering evidence, request the missing context or provide an unnumbered proposal; do not claim the next number is verified.
4. Only when no matching spec should be reused, use an available user-requested number or otherwise select the next unused number, then choose a short kebab case name. Check both the number across existing folders and the exact destination, including untracked files. If a requested number or destination is occupied by other work, report the conflict and ask for a destination choice; do not overwrite or silently renumber. Recheck immediately before writing; if the destination changed since inspection, stop the write and report the conflict.
5. Write or update only the authorized planning documents:
   - `requirements.md`
   - `plan.md`
   - `tasks.md`
6. Keep each file practical:
   - requirements explain the problem, scope, constraints, and success criteria
   - plan explains the implementation approach, touched areas, risks, and validation path
   - tasks break the work into ordered, checkable execution steps
7. Make assumptions explicit. Do not pretend unknown details are settled facts.
8. Recheck that the spec matches the live repo, existing conventions, and the user's real goal. Verify acceptance-to-validation traceability and preservation of files outside the authorized planning scope.

## Spec Status

Give every spec a visible state so a folder listing tells the truth about the work. Put a status line at the top of `requirements.md`:

```text
Status: draft | in progress | done | abandoned
Last updated: YYYY-MM-DD
```

A new execution spec starts as `draft` with unchecked implementation tasks. Writing or reviewing a plan does not implement the feature or establish that checks passed. Change status only to reflect supported evidence and an authorized update; never mark implementation `done` because planning is complete. For a review-only request, recommend status corrections in the response instead of editing files. When reusing a stale spec, preserve completed-work evidence and explain any proposed status correction; do not reset its history automatically.

## Template Variants

Shape the documents to the work type instead of using one generic skeleton:

- `feature`: requirements emphasize user-facing behavior and acceptance criteria; plan covers integration points and new surface area
- `refactor`: requirements define behavior that must not change and how that is verified; plan emphasizes sequencing and safe checkpoints; tasks alternate change and verify steps
- `migration`: requirements define the end state and cutover criteria; plan covers dual-running, rollback, and data integrity; tasks include a rehearsal step before the real cutover

Name the variant in `requirements.md` so the reader knows which lens the spec uses.

## Requirements Guidance

- State the problem in plain language
- Define in scope and out of scope
- List constraints from the repo, tooling, platform, or user instructions
- Include acceptance criteria that can actually be verified
- Keep wording concrete enough that implementation decisions can be judged against it

## Plan Guidance

- Name the files, modules, folders, scripts, or systems likely to change
- Explain the intended implementation shape without drifting into code
- Call out dependencies, sequencing, migration concerns, and rollback or safety issues where relevant
- Include a validation section with realistic checks such as tests, linting, manual flows, or document review

## Task Guidance

- Break work into an execution order that another engineer can follow
- Prefer tasks that map to real deliverables, not vague activity labels
- Separate implementation, validation, and documentation work when that helps execution
- Keep tasks small enough to complete and review, but not so small that the list becomes noise
- Give each task a rough size of `S` (under an hour), `M` (half a day), or `L` (a day or more) so the spec communicates effort, not just steps; an `L` task is usually a sign it should be split

## Constraints

- Match the repo's existing spec layout if one already exists
- Prefer editing existing planning structure over inventing a new one
- Use direct language and skip filler
- Do not pad specs with generic boilerplate
- Do not hide major assumptions or risks
- If numbering, matching scope or destination intent is ambiguous, ask for the minimum decision before writing; do not silently choose between conflicting user intentions.
- Preserve staged, unstaged and untracked user edits. Read the current planning files before a targeted update; do not replace whole documents or alter unrelated files merely to fit a template. If proposed changes conflict with user work, present the conflict and wait for direction.
- File access is not write authorization. Return a proposal when writing is not requested or authorized; do not create folders for a review-only task.

## Acceptance-to-validation traceability

Use stable acceptance-criterion identifiers (for example `AC-1`) in `requirements.md`, retaining existing identifiers when updating a spec. In `tasks.md`, map every criterion to at least one concrete validation task with the check or procedure and expected observable result. A table such as `Criterion | Validation task | Check | Expected result` is sufficient; follow an equivalent existing repository convention instead of duplicating it. Shared validation tasks may cover several criteria if each mapping is explicit.

Before delivery, check for unmapped criteria, references to nonexistent criteria/tasks, and vague checks without an expected result. Mark unavailable validation as planned or blocked with its prerequisite; do not claim it ran or check it off. Keep implementation tasks separate from proof of acceptance. Summarize the chosen reuse/new-spec decision, destination, changed files, open decisions and checks actually performed.

## References

- `shared/skill-standard.md`
- Existing `specs/` folders in the target repo
- Any repo handoff docs such as `assessment.md`, `project-analysis.md`, or roadmap files if they exist

## Help And Examples

Use this skill when the user wants a real execution spec instead of loose notes.

Minimum useful input:

- the repo or project context
- what needs to be built, changed, or cleaned up
- any scope limits or constraints

Example prompts:

```text
Use spec-writer to create the next numbered spec for moving this repo from ad hoc scripts to a module layout with tests and CI.
```

```text
Create a spec folder for adding OAuth refresh handling and export retry logic to this CLI project.
```

```text
Write a numbered repo spec with requirements, plan, and tasks for a README audit plus stale doc cleanup.
```

## Validation Checklist

- The spec folder name and number fit the repo's existing pattern
- `requirements.md`, `plan.md`, and `tasks.md` are all present
- The requirements are specific enough to judge success
- The plan matches the actual repo context
- The tasks are ordered, practical, and executable
- Matching specs were inspected before numbering; occupied or uncertain destinations remain untouched until resolved
- Existing user edits and files outside the authorized planning scope are preserved
- Every acceptance criterion maps to a validation task with an observable expected result; no dangling mappings remain
- Planning status and task checkboxes distinguish proposed work from verified implementation

## Host Capabilities

Use only tools, files, conversation history, and connected services actually available and authorized in the current host. If browsing, image/document inspection, code execution, persistent storage, or a related skill is unavailable, state the limitation and request the needed input or provide manual steps. Never claim a lookup, save, execution, publication, or installation occurred without evidence. Preserve the domain safety and confirmation rules above.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.
