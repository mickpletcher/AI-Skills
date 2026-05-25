# AI Skills Changelog

Compiled from repo history and the current working tree.

## 2026-05-24

- Strengthened `claude/skills/med-vault` warnings and disclaimers so every response states that MedVault is not medical advice, can be wrong or incomplete, and must be checked with both a doctor and pharmacist
- Rebuilt `claude/skills/med-vault/med-vault.skill` so the packaged Claude import matches the updated safety language
- Upgraded `claude/skills/travel-itinerary` with visa and border crossing checkpoints, lodging decision notes, and smarter arrival and departure day templates
- Upgraded `claude/skills/travel-research` with live data checks for flight pricing, weather normals, and crowd levels plus travel friction scoring
- Upgraded `claude/skills/facebook-post` with cross-platform output bundles for Facebook, X, and LinkedIn versions from one source draft

## 2026-05-22

- Added `skill-improvement-assessment.md` with a skill-by-skill improvement review across Claude, ChatGPT, Copilot, and Cursor skills
- Linked the assessment from `README.md`
- Added `claude/scripts/Validate-SkillQuality.ps1` for standard section coverage and stale Claude package checks
- Normalized missing standard sections across Claude, ChatGPT, Copilot, and Cursor skills
- Converted ChatGPT `food-analyzer` from wrapper format into a standalone instruction skill
- Rebuilt Claude `.skill` packages after source updates

## 2026-05-21

- Moved the repository social preview asset to `.github/github-social-preview.jpg` for stable future reference inside the repo
- Refreshed `.github/github-social-preview.jpg` so the repository social preview now reflects the expanded platform set including Gemini, Perplexity, and Cursor
- Added the first Cursor skill set with `cursor/skills/pr-review/`, `cursor/skills/workflow-debugger/`, `cursor/skills/repo-assessment/`, and `cursor/skills/spec-writer/`, each with source instructions and beginner friendly setup READMEs
- Updated the root `README.md`, Cursor platform docs, and completed projects tracking so Cursor now has live skill examples instead of a placeholder section
- Moved the shipped Cursor skills out of the Cursor future backlog
- Added first class platform docs for `gemini/`, `perplexity/`, and `cursor/` with root folder READMEs and beginner notes for future skills
- Updated the root `README.md`, shared platform guidance, and local future backlog so Gemini, Perplexity, and Cursor are treated as real platform areas in the repo
- Added the first GitHub Copilot skill `copilot/skills/pr-review/` with a source `instructions.md` file and beginner friendly setup README for risk focused pull request review
- Updated the root `README.md` so the GitHub skills catalog includes `pr-review` and the Copilot setup guide now points to a live example
- Moved `copilot/skills/pr-review` out of the GitHub future backlog and into `completed-projects.md`
- Expanded the root `README.md` with beginner friendly instructions for implementing skills in Claude, ChatGPT, and GitHub Copilot style workflows
- Updated shared repo standards so each skill README is expected to include plain language implementation steps for novice users
- Expanded `future-projects.md` with a few additional ChatGPT and Claude skill ideas and fixed the affected numbering
- Added the new Claude skill `claude/skills/travel-research/` with a source `SKILL.md`, wrapper `README.md`, tracked change history, and packaged `.skill` export for deeper destination comparison before full trip planning
- Updated the root `README.md` so the Claude skill catalog includes `travel-research`
- Moved `claude/skills/travel-research` out of the Claude future backlog and into `completed-projects.md`
- Added the new Claude skill `claude/skills/spec-writer/` with a source `SKILL.md`, wrapper `README.md`, tracked change history, and packaged `.skill` export for generating numbered repo spec folders with requirements, plan, and tasks
- Updated the root `README.md` so the Claude skill catalog includes `spec-writer`
- Moved `claude/skills/spec-writer` out of the Claude future backlog and into `completed-projects.md`

## 2026-05-14

- Added explicit `Help And Examples` sections to every Claude skill `SKILL.md` so Claude can explain usage, state minimum input, and show example prompts when the user is unsure how to use a skill
- Updated the shared skill standard and Claude skill templates so future skills keep the same help and examples behavior by default
- Rebuilt the packaged Claude `.skill` exports so installed skills match the updated source files
- Expanded the root local planning backlog in `future-projects.md` with a broader set of ChatGPT, Claude, GitHub, shared-platform, and repo-wide ideas
- Added the root `completed-projects.md` file and moved completed additions out of `future-projects.md` so future work and completed work are tracked separately
- Updated the root `README.md` so the Claude skill catalog matches the actual skill folders, including `fitness-programming`, `github-social-preview`, and `patentforge-provisional-skill`
- Updated the root `README.md` to link to `completed-projects.md` and restored the root changelog link for repo discoverability
- Added the new Claude skill `claude/skills/powershell-refactor/` with a focused source `SKILL.md`, wrapper `README.md`, upgrade log, and packaged `.skill` export for simplifying and standardizing existing PowerShell scripts
- Upgraded `claude/skills/fitness-programming` with goal presets, fatigue adjustment prompts, safer substitutions, phased nutrition guidance, benchmark reviews, annual season planning, fitness-log handoff, and event countdown planning
- Added `claude/skills/fitness-programming` with source files, tracked change history, and a packaged `.skill` export for structured training plans and season programming

## 2026-05-13

- Upgraded `claude/skills/photo-rename` with stronger filename ordering, confidence handling, collision-safe rename output, batch review, GPS fallback logic, and export-style rename reports
- Added `specs/002-completed-changes-rollup` for the repo-wide completed history migration
- Moved Claude skill completed history into tracked `completed-changes.md` files and updated skill READMEs to link them
- Updated the future-upgrades maintenance workflow so local planning files point to tracked completed history instead of regenerating shipped changes
- Added `specs/001-skill-repo-workflow` as the baseline GitHub spec workflow for non-trivial repo changes
- Updated the root `README.md` to point contributors to the new `specs/` workflow
- Upgraded `claude/skills/travel-planning` with destination comparison scoring, trip style presets, booking triage, seasonal guidance, risk notes, packing suggestions, and itinerary handoff
- Upgraded `claude/skills/travel-itinerary` with itinerary templates, daily pacing checks, packing and reservation summaries, route notes, budget visibility, and contingency planning
- Upgraded `claude/skills/resume-writer` with job fit before and after scoring, recruiter skim views, stronger bullet quantification guidance, and role family presets
- Upgraded `claude/skills/resume-writer` with LinkedIn alignment checks, interview prep handoff, career timeline consistency checks, and longitudinal revision tracking
- Upgraded `claude/skills/linkedin-post` with post modes, LinkedIn tuned hook styles, and stronger credibility checks
- Upgraded `claude/skills/linkedin-post` with CTA styles, tone controls, and audience testing variants
- Upgraded `claude/skills/github-social-preview` with theme presets, smarter text fitting, preview QA checks, and optional logo or screenshot or background assets
- Upgraded `claude/skills/food-analyzer` with confidence labeled analysis, goal aware modes, and quick summary output
- Upgraded `claude/skills/food-analyzer` with comparison mode, timing specific guidance, and cleaner ingredient risk grouping
- Upgraded `claude/skills/food-analyzer` with meal history review and user preference memory within the conversation
- Upgraded `claude/skills/fitness-log` with trend summaries for strength, endurance, consistency, and recovery across logged workouts
- Upgraded `claude/skills/fitness-log` with goal based program checks for pull ups, cycling, triathlon, and similar training targets
- Upgraded `claude/skills/fitness-log` with weekly review output, nutrition timing prompts, and cleaner exercise normalization
- Upgraded `claude/skills/fitness-log` with long horizon progression planning and export friendly structured output for dashboards or Obsidian
- Upgraded `claude/skills/facebook-reply` with tone modes for appreciative, clarifying, humorous, and boundary setting responses
- Upgraded `claude/skills/facebook-reply` with original post context handling and commenter aware replies
- Upgraded `claude/skills/facebook-reply` with concise versus fuller reply depth control
- Upgraded `claude/skills/facebook-reply` with difficult comment handling for skepticism, criticism, hostility, and off-topic comments
- Upgraded `claude/skills/facebook-reply` with batch reply mode and thread summarization for repeated questions
- Upgraded `claude/skills/facebook-reply` with sentiment tagging so supportive, neutral, skeptical, critical, off-topic, and hostile comments get different treatment
- Upgraded `claude/skills/facebook-post` with feedback guided mode so new drafts can borrow patterns from prior high interaction posts
- Upgraded `claude/skills/facebook-post` with repurpose mode to turn a Facebook post into a matching X post
- Upgraded `claude/skills/facebook-post` with audience mode switching for friends and family, technical peers, and mixed audience drafts
- Upgraded `claude/skills/facebook-post` with caption guidance for build photos, screenshots, and workout images
- Upgraded `claude/skills/facebook-post` with engagement guardrails so questions stay natural instead of turning into comment bait
- Upgraded `claude/skills/facebook-post` with inferred post modes for personal updates, technical lessons, project progress, and opinion posts
- Upgraded `claude/skills/facebook-post` with inferred length presets for short update, standard, and story driven drafts
- Upgraded `claude/skills/facebook-post` with stronger hook selection so the first sentence lands without sounding promotional
- Updated the `facebook-post` skill README and root `README.md` to document the new behavior
- Added `claude/skills/patentforge-provisional-skill` with source files, templates, schemas, docs, examples, and a packaged `.skill` export for provisional drafting support with legal safety boundaries
- Updated every skill `future-upgrades.md` file across `claude/skills` and `chatgpt/skills`
- Created the missing `chatgpt/skills/food-analyzer/future-upgrades.md`
- Improved `claude/scripts/Update-FutureUpgrades.ps1` so it can populate skill specific tier ideas, preserve existing tier content, and handle single skill roots
- Updated `claude/skills/idea-forge` to support Apple Notes output delivery on macOS and iOS handoff flows
- Updated `claude/skills/idea-forge` to support Obsidian `Ideas` folder output delivery on macOS and iOS handoff flows
- Added this root `changelog.md`
- Added root `README.md` link to the changelog
- Added `claude/scripts/Update-FutureUpgrades.ps1` to create and refresh skill `future-upgrades.md` files from `upgrades.md`
- Updated `claude/scripts/README.md` with the new maintenance script

## 2026-05-12

- Added the `idea-forge` Claude skill
- Added the packaged `idea-forge.skill` export
- Changed the `idea-forge` trigger word from `forge` to `idea`

## 2026-05-02

- Added `github-social-preview`

## 2026-04-27

- Added follow up tool selection maintenance work recorded in git history

## 2026-04-24

- Added `resume-writer` tips refresh automation
- Improved `resume-writer` README usage guidance and GitHub links
- Added Claude skill packs and reference libraries
- Updated `alpaca-trading` skill docs and template metadata
- Removed obsolete shared Alpaca skill source
- Reorganized skills as platform specific sources
- Added the Claude Alpaca Trading skill
- Defined the portable skill standard and starter templates
- Completed the initial folder setup
