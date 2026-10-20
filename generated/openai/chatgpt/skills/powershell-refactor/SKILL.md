---
name: powershell-refactor
description: Refactor existing PowerShell scripts and modules while preserving observable behavior, interfaces, and safety controls.
---
# PowerShell Refactor

## Purpose
Modernize an existing PowerShell script or module with minimal, reviewable changes. Preserve its externally observable contract unless the user explicitly authorizes a change.

## Use when
A user asks to simplify, deduplicate, standardize, or improve maintainability of existing PowerShell code.

## Do not use when
The user requests a new script, an unrelated architecture redesign, or documentation only. Clarify when expected behavior is unknown and the changes could be risky.

## Inputs and baseline
Inspect the actual source, tests, manifest, CI configuration, PSScriptAnalyzer settings, supported PowerShell versions, platform constraints, and dependent callers when accessible. Record parameters, pipeline behavior, object types, stdout/stderr streams, exit codes, error behavior, file/network effects, and WhatIf/Confirm semantics. Distinguish verified facts from assumptions. Never claim tests ran without execution evidence.

## Scope presets
- **naming only:** change naming and casing without unrelated cleanup.
- **deduplication only:** consolidate repeated logic without changing public names.
- **full cleanup (default):** apply behavior-preserving structural improvements with minimal abstractions.
Respect the selected scope and report other findings separately.

## Workflow
1. Establish a baseline: inspect the code and available tests; record observed behavior and current diagnostics.
2. Identify dead code, duplication, unclear control flow, inconsistent naming, error handling, and security concerns. Avoid deleting code solely because static inspection cannot find a caller.
3. Plan the smallest safe patch. Treat exported functions, positional parameters, aliases, pipeline contracts, output object shapes, and serialization as compatibility surfaces.
4. Refactor with idiomatic PowerShell: approved verbs where safe, advanced functions when justified, structured objects, Write-Verbose/Warning, and appropriate terminating versus nonterminating errors.
5. Preserve safety boundaries: ShouldProcess, WhatIf, Confirm, credential handling, least privilege, quoting, encoding, and external command exit codes. Do not introduce Invoke-Expression or unsafe interpolation.
6. Run existing tests and Invoke-ScriptAnalyzer before and after when tools are available; honor repository settings. Prefer Pester and relevant PowerShell editions/platforms. When execution is unavailable, give reproducible commands and mark checks **not run**.
7. Review diffs for behavior drift, regressions, unintentional dependency changes, and changes outside the requested scope.
8. Present a concise change summary, evidence of tests, unresolved risks, and any recommended follow-up.

## Constraints
- Do not invent files, test results, APIs, or repository permissions.
- Preserve observable behavior by default; request approval for breaking changes.
- Never remove safeguards from destructive operations.
- Avoid gratuitous rewrites, compatibility shims, dependencies, and comments.
- Do not expose secrets in output or logs.

## Output contract
Report files changed, changes made, behavior preserved or exceptions, line counts when measured, analyzer findings, test commands and results (pass/fail/not run), and out-of-scope observations. State whether changes were committed or merely proposed.

## Examples
- Refactor a PowerShell reporting script without changing its parameters or output object properties.
- Deduplicate retry logic while preserving timeout and error behavior.
- Standardize a module's internal functions without changing its exported API.

## Validation checklist
- No unintended changes to exported functions, parameters, output types, or side effects.
- Existing tests pass or their unavailability is explicitly reported.
- Analyzer results are verified rather than inferred.
- Security controls and chosen scope are preserved.

## Analyzer acceptance gate
Run `Invoke-ScriptAnalyzer` before and after with the same repository settings, including `PSScriptAnalyzerSettings.psd1` when present. Fix violations within the selected scope and list each remaining violation with a one-line reason, including deliberate interactive `Write-Host` use when justified. Never introduce new analyzer violations. If comparison cannot be executed, mark this gate not verified and supply the commands; do not infer a pass from reading the code.

## Refactoring discipline
Prefer editing existing files. Remove confirmed obsolete code instead of adding compatibility shims, while preserving public contracts and checking callers before deletion. Do not introduce helper classes, extra modules or layers without a demonstrated need. Use clear parameter blocks, pipeline-aware logic when useful, and `try`/`catch` only when it improves control or diagnostics. Add comments only where the logic would otherwise be unclear. Preserve or improve validation and confirmation controls for high-risk actions.
Follow the target project's authoring and naming conventions when available, including its shared skill standard and naming-conventions documents if present. Do not assume those repository-specific files exist in every host.

## Refactor Summary
End with these fields:
- Behavior preserved: yes, or explicitly listed exceptions.
- Lines: measured before -> after, or not measured.
- Changes: one line per behavior-preserving change.
- Analyzer: violations fixed and count remaining, with reasons listed; or not run with the limitation.
- Tests: commands and pass/fail/not run evidence.
- Out of scope findings: observations left untouched.
- Delivery: files edited, committed, or proposed only, as verified.

## Help response
Request the script or module (pasted source is sufficient for a proposed refactor), behavior to preserve, and style constraints such as keeping a single file. Explain the scope presets, show an example below, and offer a short next prompt. In deduplication-only mode preserve names and structure except the consolidation needed to remove duplication.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.
