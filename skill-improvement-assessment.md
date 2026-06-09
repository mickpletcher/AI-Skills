# Skill Improvement Assessment

Assessment date: 2026-05-22
Remediation status: completed 2026-05-22

## Scope

Reviewed every current skill folder under:

- `claude/skills/`
- `chatgpt/skills/`
- `copilot/skills/`
- `cursor/skills/`

`gemini/` and `perplexity/` have platform README files only. They do not have live skill folders yet.

## Method

Checks used:

- Confirmed required skill files exist.
- Compared source files against `shared/skill-standard.md`.
- Checked for clear trigger rules, out-of-scope handling, workflow steps, constraints, help behavior, examples, and validation checks.
- Checked Claude `.skill` package timestamps against `SKILL.md`.

## Executive Findings

No skill folder was structurally broken.

The remediation pass is complete. Standard skill control sections were added where missing, ChatGPT `food-analyzer` was converted from wrapper format into a standalone instruction skill, and Claude `.skill` packages were rebuilt after source updates.

Completed fixes:

1. Added `claude/scripts/Validate-SkillQuality.ps1` to check source section coverage and stale Claude packages.
2. Added missing standard sections across Claude, ChatGPT, Copilot, and Cursor skills.
3. Converted `chatgpt/skills/food-analyzer/instructions.md` into a standalone ChatGPT skill.
4. Rebuilt Claude `.skill` packages so packaged exports match current source files.
5. Updated script documentation so both folder validation and quality validation are discoverable.

## Repo-Level Recommendations

Completed:

1. Added a second validator that checks source section coverage, not just file presence.
2. Added package freshness checks for Claude `.skill` files.
3. Ran one standard modernization pass for all skills:
   - `Intent`
   - `Use When`
   - `Do Not Use When`
   - `Workflow`
   - `Constraints`
   - `Help And Examples`
   - `Validation Checklist`
4. Preserved existing source content and added concise control sections instead of rewriting working skills.
5. Kept platform-specific wording for Claude, ChatGPT, Copilot, and Cursor.

## Claude Skills

The table below records the original findings that drove the remediation pass. These items have been addressed by the completed fixes above unless a future refinement is explicitly noted.

| Skill | Status | Improvements Needed |
| --- | --- | --- |
| `alpaca-trading` | Minor | Add explicit `Intent` and `Do Not Use When`. Add example prompts. Current workflow and safety rules are solid. |
| `blog-post` | Minor | Add `Do Not Use When` and a clearer `Workflow` heading. Add example prompts. |
| `blog-to-social` | Minor | Add `Do Not Use When`. Add example prompts for blog input, short excerpt input, and repurpose-only requests. |
| `container-home` | Moderate | Add a true `Workflow` section. Add `Do Not Use When` for engineering, permit, and structural signoff limits. Add example prompts. |
| `crypto-listings` | Moderate | Add explicit `Intent` and `Do Not Use When`. Add examples. Add freshness rules because listing data is time sensitive. |
| `crypto-research` | Moderate | Add explicit `Intent` and `Do Not Use When`. Add examples. Add stronger source freshness and risk disclosure checks. |
| `facebook-post` | Minor | Add explicit `Intent` and `Do Not Use When`. Add examples for photo caption, long post, short post, and X repurpose mode. |
| `facebook-reply` | Good | Mostly complete. Add `Intent` if strict standard alignment matters. Keep existing examples. |
| `fitness-log` | Moderate | Rename or add a clear `Workflow` section. Add explicit `Intent`, `Do Not Use When`, and examples. |
| `fitness-programming` | Moderate | Add explicit `Intent`, `Do Not Use When`, and a top-level `Workflow`. Existing workflow content is strong but buried under custom headings. |
| `food-analyzer` | Moderate | Add explicit `Intent`, `Do Not Use When`, and `Constraints`. It has strong nutrition rules, but the safety boundary should be easier to find. Add examples. |
| `github-readme` | High | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Constraints`, and `Validation Checklist`. This is a core repo-writing skill and should match the standard tightly. |
| `github-repo-architect` | Moderate | Add explicit `Intent`, `Workflow`, and `Constraints` headings. Existing architecture guidance is useful but section naming is inconsistent. |
| `github-social-preview` | High | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Constraints`, and `Validation Checklist`. Keep the script-specific workflow. |
| `idea-forge` | Moderate | Add explicit `Intent`, `Workflow`, `Constraints`, and `Validation Checklist`. It already has a mature staged process. |
| `linkedin-post` | Moderate | Add explicit `Intent`, `Do Not Use When`, `Workflow`, `Constraints`, and `Validation Checklist`. Add examples by mode. |
| `med-vault` | Good | Keep as is structurally. Add `Do Not Use When` for emergency, diagnosis, medication changes, and clinician-only cases. Add examples if not already obvious from command references. |
| `n8n-workflow` | High | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Constraints`, and `Validation Checklist`. Current content reads more like reference notes than a complete skill. |
| `obsidian-workout-export` | Moderate | Add explicit `Intent`, `Do Not Use When`, examples, and validation checks. Current workflow is clear. |
| `patentforge-provisional` | High | Rebuild stale `.skill` package. Add a standard `Workflow` heading if strict conformity is desired. Keep safety and non-legal-advice language prominent. |
| `photo-rename` | Moderate | Add explicit `Intent`, `Do Not Use When`, `Constraints`, and `Validation Checklist`. Existing workflow is practical. |
| `pihole-blocklist` | High | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Workflow`, `Constraints`, and `Validation Checklist`. Current content is useful but reference-heavy. |
| `pihole-csv-analyzer` | High | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Constraints`, and `Validation Checklist`. Add examples for common CSV exports. |
| `powershell-refactor` | Good | No major improvement needed. Add examples if you want every skill to meet the same usage standard. |
| `proxmox-lxc` | High | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Workflow`, `Constraints`, and `Validation Checklist`. Current content is operational reference material, not fully framed as a skill. |
| `resume-writer` | High | Add a short standard wrapper at the top with `Intent`, `Use When`, `Do Not Use When`, `Workflow`, `Constraints`, and `Validation Checklist`. Do not rewrite the detailed body unless needed. |
| `spec-writer` | Good | No major improvement needed. Add concrete examples if enforcing the examples requirement strictly. |
| `travel-itinerary` | Moderate | Add explicit `Intent`, `Use When`, `Do Not Use When`, and `Validation Checklist`. Current step-by-step workflow is useful. |
| `travel-planning` | Moderate | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Workflow`, and `Constraints` headings. It has the content, but not in standard form. |
| `travel-research` | Good | No major improvement needed. Add examples if enforcing the examples requirement strictly. |
| `website-content` | Moderate | Add explicit `Intent`, `Use When`, `Do Not Use When`, `Workflow`, and `Constraints`. Existing quality checklist is useful. |
| `x-post` | Moderate | Add explicit `Intent`, `Do Not Use When`, `Workflow`, `Constraints`, and `Validation Checklist`. Existing examples are useful. |
| `x-reply` | Moderate | Add explicit `Intent`, `Do Not Use When`, `Workflow`, `Constraints`, `Help And Examples`, and `Validation Checklist`. |

## ChatGPT Skills

| Skill | Status | Improvements Needed |
| --- | --- | --- |
| `food-analyzer` | High | Convert from a wrapper-style instruction file into a complete standalone ChatGPT skill. Add explicit `Intent`, `Use When`, `Do Not Use When`, `Workflow`, `Constraints`, `Help And Examples`, and `Validation Checklist`. Keep ChatGPT-specific photo and nutrition behavior. |

## Copilot Skills

| Skill | Status | Improvements Needed |
| --- | --- | --- |
| `pr-review` | Minor | Add explicit `Intent`. Add example prompts. Existing review workflow, constraints, and validation checks are strong. |

## Cursor Skills

| Skill | Status | Improvements Needed |
| --- | --- | --- |
| `pr-review` | Minor | Add explicit `Intent`, `Help And Examples`, and `Validation Checklist`. Current review behavior is clear. |
| `repo-assessment` | Minor | Add explicit `Intent`, `Help And Examples`, and `Validation Checklist`. Current workflow matches the repo preference for durable assessment docs. |
| `spec-writer` | Minor | Add explicit `Intent`, `Help And Examples`, and `Validation Checklist`. Current workflow is practical. |
| `workflow-debugger` | Minor | Add explicit `Intent`, `Help And Examples`, and `Validation Checklist`. Existing workflow is practical. |

## Recommended Work Order

Completed in this order:

1. Rebuild `patentforge-provisional.skill`.
2. Add automated checks for section coverage and package freshness.
3. Modernize the high-value technical skills:
   - `github-readme`
   - `github-social-preview`
   - `n8n-workflow`
   - `pihole-blocklist`
   - `pihole-csv-analyzer`
   - `proxmox-lxc`
   - `resume-writer`
4. Modernize time-sensitive and safety-sensitive skills:
   - `crypto-listings`
   - `crypto-research`
   - `food-analyzer`
   - `med-vault`
   - `patentforge-provisional`
5. Normalize social and travel skills after the core technical skills.

## Validation Result

Command run:

```powershell
& .\claude\scripts\Validate-SkillQuality.ps1 -FailOnIssues
& .\claude\scripts\Validate-SkillFolders.ps1 -Root .\claude\skills -RepairHints
```

Result:

```text
Skill quality validation passed.
Checked skills: 39
Skill folder validation passed.
Checked folders: 33
```

This means current skill source files include the standard sections checked by the repo validator, Claude packages are not stale, and required Claude files exist.
