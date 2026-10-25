---
name: github-readme
description: Write or repair an accurate, repository-specific README based on verified project files and requirements.
---
<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->
# Repository README Writer

## Purpose
Create or update README documentation that accurately describes a repository, its installation, configuration, use, testing, and limitations. Prefer verified evidence over plausible-looking instructions.

## Triggers
Use when asked to write, rewrite, repair, or document a repository README. Recognize the shortcuts `readme` and `gr` followed by repository details.

## Do not use
- For designing a new repository from scratch: use a repository architecture workflow.
- For implementing code, reviewing a pull request, or auditing unrelated documentation.
- When the user has provided too little information to identify the repository: ask for a repository link, path, or description.

## Inputs and evidence
Obtain the repository name, purpose, audience, language, files, entry points, dependencies, configuration, license, and existing README when available. Prefer inspected repository files over an old README, and an old README over unsupported guesses. If repository access is unavailable, label any unverifiable commands, paths, and claims explicitly.

## Workflow
1. Classify the repository (single script, CLI, API, MCP server, automation, multi-module toolkit, skills library, website, or template).
2. Inspect available source files and existing documentation. Verify names, paths, command flags, environment variables, dependencies, and license text.
3. Determine whether to repair existing sections or create a new README. Preserve useful existing structure and voice; avoid unnecessary rewrites.
4. Draft only applicable sections: overview, capabilities, component inventory, structure, prerequisites, installation, configuration, usage, tests, troubleshooting, security, related projects, and license.
5. Provide runnable examples only when grounded in inspected files or explicit user input. Mark unverified examples clearly.
6. Cross-check all links, filenames, commands, and configuration names against evidence. Identify unresolved assumptions.
7. Deliver the requested README text or, when repository write access is available and authorized, propose or apply the file change and report what was actually committed.

## Writing requirements
Use plain, direct technical language and short paragraphs. Avoid promotional adjectives, emojis, empty headings, invented testimonials, and generic setup commands. Use tables for modules, environment variables, and parameters when useful. Keep the license section accurate and last. Respect the user's preferred voice without hardcoding an individual author.

## Repair mode
Compare the current README to verified repository contents; identify stale sections, broken paths, and missing features. Prefer targeted updates when the document remains substantially correct. Explain any major omissions or changes.

## Validation
- All documented paths and case-sensitive filenames exist or are marked unverified.
- Setup and usage commands match real entry points or are explicitly hypothetical.
- Dependencies, configuration, and license claims are supported by evidence.
- Security notes appear when credentials or sensitive data are involved.
- The result has no placeholders disguised as finished documentation.
- The README matches the repository's actual scope, not a generic template.

## Examples
- "readme for this Python CLI, using the actual pyproject.toml and commands"
- "gr owner/repository: repair outdated installation and usage instructions"
- "Draft a README for this PowerShell module based on the supplied files"

## Section details
Choose only the blocks supported by the repository evidence:
- Start with a readable H1 matching the repository name and a plain one-sentence description. Keep the overview to two to four sentences about contents and audience; keep setup steps separate.
- For multiple skills, use a `Skill | Trigger | Description` inventory; for modules, `Module | Purpose | Typical User | Main Outputs`; for an MCP server, `Tool | Description`. Document API endpoints, authentication and payload schemas when applicable.
- Use an annotated repository tree when structure matters; annotate folders rather than every file in a large repository.
- List prerequisite software, tools, accounts and versions separately from installation. Use numbered setup steps with exact, verified commands for cloning, environment creation, dependency installation and configuration where applicable. For mixed stacks, cover each stack. Include skill installation paths only when the repository actually requires them.
- For environment configuration use `Variable | Required | Example | What It Controls`. Use safe example values, never real secrets.
- Put the safest, simplest usage command first; use a subsection for each major component when needed. Use code blocks for commands, paths, configuration and examples.
- For non-obvious failure modes use `Problem | Likely Cause | Fix`. Add factual security notes for credentials, keys and sensitive data.
- For static sites cover local preview, deployment and content editing; for starter repositories cover customization points.
- Include related projects only when useful, with `Repo | Description`. A blog reference is optional, useful to the public-facing repository, and limited to one line.
- Keep the license last and match the actual license file, including MIT only when that is the repository's license.
Avoid em dashes and motivational sign-offs in README prose, as well as the promotional language already excluded above.

## Delivery and help
Default to complete README content in the response unless a repository edit is requested or authorized. For repairs, return corrected sections with placement notes or the full file, whichever creates less churn. Recommend a full rewrite only when roughly half or more is stale, and explain why. Briefly confirm the repository name, chosen type, and major included or omitted sections.
If the user needs help, explain the workflow, request a path, pasted repository summary or specific README problem, show a relevant example, and offer a short next prompt. With supplied text only, distinguish a draft from a README verified against current repository files.

## README delivery boundary
For a complete README delivered in chat, put the entire README in one fenced Markdown block. Use an outer fence longer than every fence inside the README so command examples cannot close the artifact. The README body must end with the License section and its supported license content. Do not put change summaries, validation notes, execution claims or sign-offs inside or after the License section of the README.
Put any repository/type confirmation, placement explanation, change summary or validation status outside that block, explicitly labeled `Review notes (not part of README)`. For an authorized file edit, keep those notes in the response only; never append them to README.md. For a partial repair, clearly label the replacement sections and give placement notes outside their fences; preserve targeted repair mode rather than forcing a full rewrite.
Before delivery, inspect the actual README body independently of the surrounding response: its final heading is License, nested example fences remain intact, and all review notes are outside the artifact.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.

## Claude-specific behavior
Preserve the original shortcuts `readme` and `gr`. When Claude has authorized repository access, inspect actual files before documenting them. Do not imply that repository edits, links, or command tests were performed without evidence. Follow the target Claude host's skill packaging requirements.

## Target model and capability overlay

Profile: baseline; provider: unconfigured; model: unconfigured.
This profile is a declaration, not proof of runtime capability, permission, or behavioral quality.

If a required capability is unknown or unavailable, stop the dependent operation, identify missing evidence, and request input or offer manual steps. Do not claim completion.
Capability declarations never grant authorization. Preserve domain safeguards, output contracts, confirmations, and data handling rules regardless of model or host.

Required capabilities:
- text_reasoning: unknown. Verify actual availability before the dependent operation.
- Conditional web_retrieval: unknown. Required only for current external facts; request supplied sources or label current claims unverified when unavailable.
- Conditional file_access: unknown. Required for verifying actual local repository contents or saving README changes. Not required for drafting or repairing from pasted source, file listings and README text. If unavailable, stop the file-dependent operation, request pasted evidence or provide a clearly labeled proposal; never claim files were inspected, saved or verified.

Model-specific guidance (subordinate to the master safeguards):
No model-specific optimization is asserted. Verify capabilities in the selected host before use.

Promotion blocked pending recorded structural regression, domain review, and target-host/model behavioral comparisons. No future model compatibility is inferred.
