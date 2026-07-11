<!-- markdownlint-disable MD013 -->

# 001 Skill Repo Workflow Tasks

## Completed Tasks

- [x] T001 Inspect the current repo layout and confirm there is no existing root `specs/` workflow.
  - Files: root repo, `.github/`, `shared/`, `templates/`
  - Verification: manual repo inspection

- [x] T002 Create the baseline numbered spec package.
  - Files: `specs/001-skill-repo-workflow/requirements.md`, `spec.md`, `plan.md`, `tasks.md`
  - Verification: all four files present

- [x] T003 Define when the `AI-Skills` repo should use spec workflow versus direct edits.
  - Files: `specs/001-skill-repo-workflow/requirements.md`, `spec.md`
  - Verification: usage boundaries are explicit

- [x] T004 Update the root README so the workflow is discoverable.
  - Files: `README.md`
  - Verification: README references `specs/`

- [x] T005 Record the baseline in the root changelog.
  - Files: `changelog.md`
  - Verification: changelog entry added

## Follow-Up Backlog

- [ ] T006 Decide whether repo-level `.github/copilot-instructions.md` should be added for cross-skill agent guidance.
  - Files: likely `.github/` plus root docs
  - Verification: repo-specific instructions exist if the team wants them

- [ ] T007 Decide whether reusable spec prompts belong in `.github/prompts/`.
  - Files: likely `.github/prompts/`
  - Verification: prompts match this repo instead of generic software scaffolding

- [ ] T008 Add the next numbered spec when a shared script, packaging rule, or cross-skill convention changes.
  - Files: future `specs/00N-*/`
  - Verification: non-trivial repo changes stop relying on ad hoc notes

## Verification Notes

- This baseline adds process documentation only.
- No runtime skill logic or packaging scripts were changed.

<!-- markdownlint-enable MD013 -->
