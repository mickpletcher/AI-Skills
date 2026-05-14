# Future Projects

This file is a local planning note for useful repo level skill work. It is intended to stay out of git.

## ChatGPT Skills

### Tier 1

1. `chatgpt/skills/facebook-post`
Create a ChatGPT version of the existing Claude skill so short form social writing is not limited to one platform.

2. `chatgpt/skills/linkedin-post`
Add a professional writing path on ChatGPT since that maps well to reusable prompt driven output.

3. `chatgpt/skills/x-post`
Port the current Claude skill so the main social writing set exists on both platforms.

4. `chatgpt/skills/github-readme`
This repo already has a strong Claude README writer. A ChatGPT version would be broadly useful across other repos.

5. `chatgpt/skills/idea-forge`
This is one of the highest value Claude skills in the repo. A ChatGPT version would make the R and D workflow available in both ecosystems.

6. `chatgpt/skills/facebook-reply`
This should follow `facebook-post` closely so the full Facebook writing loop exists on both platforms.

7. `chatgpt/skills/x-reply`
Useful companion to `x-post` so short form publishing and reply handling stay paired.

8. `chatgpt/skills/fitness-programming`
High reuse value and a strong candidate for a guided prompt driven ChatGPT workflow.

9. `chatgpt/skills/github-social-preview`
Good fit for a visual output workflow on ChatGPT once the repo metadata pattern is ported.

10. `chatgpt/skills/github-repo-architect`
High value planning skill that would pair well with `github-readme` and `idea-forge`.

### Tier 2

1. `chatgpt/skills/resume-writer`
High practical value. The source material and audit patterns already exist on the Claude side.

2. `chatgpt/skills/travel-planning`
Useful for repeat personal use and can reuse much of the current planning logic.

3. `chatgpt/skills/travel-itinerary`
Pairs well with travel planning and gives a clean export focused workflow.

4. `chatgpt/skills/fitness-log`
Would give a second platform path for workout tracking, progress summaries, and post generation.

5. `chatgpt/skills/website-content`
Useful for personal site updates, landing page copy, and iterative content work.

6. `chatgpt/skills/blog-post`
Longer form writing is a good fit for ChatGPT once the core short form ports are finished.

7. `chatgpt/skills/blog-to-social`
Useful after `blog-post`, `facebook-post`, `linkedin-post`, and `x-post` all exist on the ChatGPT side.

8. `chatgpt/skills/obsidian-workout-export`
Good follow on once both `fitness-log` and `fitness-programming` are available in ChatGPT.

9. `chatgpt/skills/travel-research`
Could sit between planning and itinerary output with stronger destination comparison and trip prep support.

10. `chatgpt/skills/website-audit`
Useful for reviewing page clarity, structure, missing CTAs, and content gaps for personal sites.

### Tier 3

1. `chatgpt/skills/photo-rename`
Useful, but it depends more on strong file handling and image workflow conventions.

2. `chatgpt/skills/n8n-workflow`
Likely valuable on ChatGPT, but it probably needs more platform specific design than the writing and planning ports.

3. `chatgpt/skills/proxmox-lxc`
Solid infrastructure skill after the broader writing and planning surface is built out.

4. `chatgpt/skills/powershell-script-review`
Could be a high value ChatGPT skill for code cleanup, readability, and script hardening.

5. `chatgpt/skills/repo-assessment`
Would help create durable `assessment.md` or `project-analysis.md` style outputs across repos.

6. `chatgpt/skills/spec-writer`
Good fit for generating requirements, plans, and tasks for repo level work.

7. `chatgpt/skills/meeting-note-to-action-plan`
General productivity skill that could convert unstructured notes into a clear execution checklist.

8. `chatgpt/skills/automation-idea-screen`
Could provide a fast lightweight version of `idea-forge` for smaller ideas that do not need the full pipeline.

### Tier 4

1. `chatgpt/skills/pihole-blocklist`
Specialized homelab value. Lower priority than writing and planning skills.

2. `chatgpt/skills/pihole-csv-analyzer`
Useful follow on skill once the blocklist workflow is mirrored.

3. `chatgpt/skills/container-home`
Worth building, but this is a specialized personal project skill rather than a broadly reusable first pick.

4. `chatgpt/skills/container-home-budget`
Useful once the main build planning skill exists so costs and decision tradeoffs can be broken out cleanly.

5. `chatgpt/skills/solar-system-planning`
Strong personal value, but it is a specialized planning surface that can wait.

6. `chatgpt/skills/property-project-planner`
Could help with land, shop, utility, and phased build decisions for personal projects.

7. `chatgpt/skills/training-camp-planner`
Useful companion to travel and fitness skills for event driven trips.

8. `chatgpt/skills/content-calendar`
Could unify blog and social planning into a repeatable publishing workflow.

### Tier 5

1. `chatgpt/skills/crypto-research`
Potentially useful, but less urgent than the general productivity and writing skills.

2. `chatgpt/skills/crypto-listings`
Would pair with crypto research, but should follow it.

3. `chatgpt/skills/alpaca-trading`
Worth doing only after the repo has a stronger shared pattern for higher complexity, higher risk finance skills.

4. `chatgpt/skills/crypto-list-watchlist`
Would pair well with `crypto-listings` and give a more persistent tracking workflow.

5. `chatgpt/skills/patentforge-provisional-skill`
Worth porting only after the ChatGPT side has a stronger pattern for complex multi file guided workflows.

6. `chatgpt/skills/market-research-brief`
Could support small business or product idea validation work outside the crypto specific path.

7. `chatgpt/skills/cover-letter-writer`
Useful, but lower priority than `resume-writer` and broader repo planning skills.

8. `chatgpt/skills/tool-comparison`
Could help compare AI tooling, app stacks, or automation choices in a structured way.

## Claude Skills

### Tier 1

1. `claude/skills/azure-ad-automation`
Strong fit for tenant automation, group workflows, and identity cleanup tasks.

2. `claude/skills/m365-admin-automation`
Useful for broader Microsoft 365 tenant automation that is not tied to Intune device management.

3. `claude/skills/intune-policy-writer`
High fit for practical compliance, configuration, and deployment planning inside the Windows endpoint stack.

4. `claude/skills/configmgr-task-sequence`
Strong match for task sequence design, cleanup, and troubleshooting in ConfigMgr.

5. `claude/skills/powershell-script-review`
Useful for audit, simplification, naming cleanup, and maintainability checks in real scripts.

6. `claude/skills/repo-assessment`
High value meta skill for creating durable repo handoff and source of truth documents.

7. `claude/skills/spec-writer`
Strong repo utility for generating numbered spec folders with requirements, plan, and tasks.

### Tier 2

1. `claude/skills/graph-query-builder`
Would help with Microsoft Graph discovery, shaping requests, and translating admin needs into usable calls.

2. `claude/skills/azure-runbook`
Good fit for Azure automation account work and scheduled admin tasks.

3. `claude/skills/script-troubleshooter`
A general debugging skill for PowerShell and automation failures with a practical investigation checklist.

4. `claude/skills/intune-reporting`
Useful for building report logic, CSV exports, device compliance summaries, and admin facing rollups.

5. `claude/skills/azure-automation-runbook`
Good fit for runbook design, module use, identity decisions, and schedule handling.

6. `claude/skills/endpoint-remediation`
Could focus on detection and remediation logic for device issues at enterprise scale.

7. `claude/skills/graph-permission-advisor`
High value for matching Graph tasks to least privilege permission sets.

8. `claude/skills/module-bootstrap`
Useful for creating a clean PowerShell module layout with tests, docs, and CI.

9. `claude/skills/workflow-debugger`
A repo focused skill for CI failure triage, local repro, and fast fix guidance.

10. `claude/skills/docs-audit`
Would fit the repeated pattern of validating README accuracy against the live repo state.

### Tier 3

1. `claude/skills/solar-system-planning`
Strong fit for the container home project and off grid decision work.

2. `claude/skills/container-home-budget`
Useful for scope, purchase, and build phase cost planning.

3. `claude/skills/travel-research`
Could complement the current travel planning skills with deeper destination comparison workflows.

4. `claude/skills/property-project-planner`
A practical planning skill for land, shop, utility, and build sequencing decisions.

5. `claude/skills/off-grid-water-planning`
Useful for water storage, filtration, pumping, and freeze protection decisions.

6. `claude/skills/battery-bank-planning`
Could cover sizing, chemistry tradeoffs, inverter pairing, and phased expansion.

7. `claude/skills/shop-buildout`
Good fit for tool, layout, wiring, and phased workspace planning on the property.

8. `claude/skills/triathlon-season-planner`
Useful personal planning skill that complements fitness programming with race sequencing.

9. `claude/skills/event-trip-planner`
Could join travel planning and athletic event logistics into one workflow.

10. `claude/skills/homelab-service-planner`
Good fit for self hosted service choices, container placement, backup, and maintenance planning.

### Tier 4

1. `claude/skills/security-policy-writer`
Useful for turning practical admin needs into readable baseline security guidance.

2. `claude/skills/license-audit`
Could help map Microsoft licensing questions to likely admin impact areas and decision points.

3. `claude/skills/change-plan-writer`
Good fit for producing implementation plans, rollback steps, validation checks, and communication notes.

4. `claude/skills/training-plan-review`
Would review an existing workout block and call out pacing, overload, and recovery risks.

5. `claude/skills/contractor-scope-review`
Helpful for reviewing quotes, scopes, and missing work items on property or build projects.

6. `claude/skills/notes-to-project-plan`
Could convert raw notes into a clean sequence of work, dependencies, and next actions.

## GitHub Skills

This section is GitHub focused work that should likely live under `copilot/` based on the repo platform rules.

### Tier 1

1. `copilot/skills/pr-review`
A focused review skill for finding regressions, risk, and missing tests in pull requests.

2. `copilot/skills/workflow-debugger`
High value for GitHub Actions failures, local repro steps, and targeted fix guidance.

3. `copilot/skills/issue-to-spec`
Useful for turning a GitHub issue into requirements, plan, tasks, and implementation scaffolding.

4. `copilot/skills/release-notes`
Good fit for changelog generation, release summaries, and version cut checklists.

5. `copilot/skills/repo-bootstrap`
A GitHub centered starter skill for initializing standards, labels, templates, and automation on a new repo.

6. `copilot/skills/pr-checklist`
Useful for generating a concise pre merge review checklist based on the files changed.

7. `copilot/skills/test-failure-triage`
Strong fit for turning failing test output into probable causes and next fixes.

8. `copilot/skills/changelog-writer`
Useful for producing repo rooted change summaries in the style already used across your repos.

### Tier 2

1. `copilot/skills/dependency-upgrade-review`
Useful for evaluating dependency update pull requests and calling out real break risk.

2. `copilot/skills/docs-audit`
Good fit for stale README detection, broken link review, and missing setup coverage.

3. `copilot/skills/test-gap-review`
A focused skill for checking changed files against missing or weak test coverage.

4. `copilot/skills/commit-message-writer`
Useful for repo work where you want consistent, ready to paste commit messages.

5. `copilot/skills/spec-scaffold`
A skill for generating numbered spec folders and the supporting requirements, plan, and task files.

6. `copilot/skills/repo-cleanup-audit`
Would help classify stale files, historical artifacts, and current source of truth files before cleanup.

7. `copilot/skills/readme-sync`
Focused on reconciling README claims with actual code, scripts, commands, and outputs.

8. `copilot/skills/project-handoff`
Useful for creating `assessment.md`, `project-analysis.md`, or similar handoff docs after substantial work.

### Tier 3

1. `copilot/skills/security-review`
Useful, but should follow after the more general PR and workflow skills are in place.

2. `copilot/skills/label-triage`
Could help normalize issue routing and repo hygiene for larger projects.

3. `copilot/skills/discussion-summary`
Useful for summarizing long issue or discussion threads into clear next actions.

4. `copilot/skills/migration-checklist`
A practical repo migration skill for renames, structure changes, and CI transitions.

5. `copilot/skills/release-cutover`
Could guide tagging, packaging, branch checks, changelog review, and release verification.

6. `copilot/skills/action-hardening`
Useful for GitHub Actions permission review, secret handling, and runner choice checks.

7. `copilot/skills/issue-triage-summary`
Could group open issues by risk, effort, and likely next milestone.

8. `copilot/skills/docs-to-tests`
Interesting longer term skill for turning documented examples into test case candidates.

## Shared Platform Ideas

This section is for capabilities that probably need a Claude, ChatGPT, and Copilot flavor rather than living on one platform only.

### Tier 1

1. `repo-assessment`
Create a shared pattern for repo scan, source of truth docs, risks, and next steps across platforms.

2. `spec-writer`
Unify the numbered spec workflow so each platform has a clear path for requirements, plan, and task generation.

3. `docs-audit`
High reuse value because README drift and setup accuracy keep coming up across repos.

4. `commit-message-writer`
Small but consistently useful. Easy win if the prompt patterns are made consistent.

5. `workflow-debugger`
Would be valuable across local coding, GitHub Actions, and repo maintenance tasks.

### Tier 2

1. `readme-sync`
Cross platform version of checking docs against the live repo state and fixing drift.

2. `project-handoff`
Useful for creating durable reuse docs after a complex repo session.

3. `notes-to-plan`
Could turn rough bullets into a structured execution plan with dependencies and next steps.

4. `automation-idea-screen`
Shared lightweight triage skill for deciding whether an automation idea deserves a full build.

5. `content-calendar`
Could unify blog, social, and site publishing plans across tools.

### Tier 3

1. `tool-comparison`
Useful for comparing platforms, services, or implementation paths with a standard decision format.

2. `beginner-readme-writer`
Would specialize in first run onboarding and plain language setup docs.

3. `review-finding-writer`
Could normalize how issues, severity, assumptions, and test gaps are reported.

4. `cleanup-audit`
Useful for classifying stale files before archive or deletion work.

5. `change-summary`
A smaller cross platform skill for turning a patch set into a practical summary and changelog entry.

## Repo Wide Ideas

These are broader repo improvements rather than individual skill folders.

### Tier 1

1. Add a shared packaging script for Claude skills
Right now package rebuilds are manual. A standard script would reduce drift and missed exports.

2. Add a validation script that checks every Claude `.skill` archive for required files
This would catch broken packaging before the repo drifts.

3. Add a root inventory doc for all skills by platform, maturity, and packaging state
Useful for seeing what exists, what is missing, and what needs rebuild work.

4. Add a reusable example prompt convention across every skill README
This would keep usage guidance easier to scan across the repo.

5. Add a status field or maturity marker for each skill
Useful labels would be draft, active, needs refresh, and packaged.

### Tier 2

1. Add a script to compare Claude skill folder contents against packaged archive contents
This would make it easy to spot stale `.skill` files.

2. Add a repo level dashboard markdown file for planned, active, and completed skills
Could become the single planning hub instead of spreading state across several files.

3. Add a standard README section template for implementation steps by platform
This would reduce manual copy edits when new skills are added.

4. Add lightweight test prompts for every skill
Could live beside each skill as a quick regression set.

5. Add a porting checklist for moving a skill from Claude to ChatGPT
Useful because cross platform ports are a recurring pattern in this repo.

### Tier 3

1. Add a shared naming review checklist for new skill folders and exported files
Would help avoid odd package names and stale leftovers.

2. Add a contribution workflow doc for creating a new skill end to end
Could cover source files, package rebuild, README updates, changelog, and validation.

3. Add an examples folder convention for skills that need larger worked samples
Good fit for the more complex planning and drafting skills.

4. Add metadata linting for `SKILL.md` headers
Would catch missing names, versions, or descriptions before packages are rebuilt.

5. Add a cross skill dependency map
Useful for skills like travel planning to itinerary, or blog post to blog to social, where one skill naturally hands off to another.
