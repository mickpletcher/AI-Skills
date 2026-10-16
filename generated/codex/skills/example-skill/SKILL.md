---
name: example-skill
description: Demonstrate a reusable cross-platform skill without accessing external systems.
---
<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->
# Example skill

## When to use
When a user asks for a concise task plan.

## Workflow
Ask for the objective if missing. Provide three actionable steps and one verification check.

## Constraints
Never claim to have performed an action without evidence.

## Capability Contract

Read `capabilities.json` for required and conditional capabilities, fallback behavior, and safeguards. These describe operations, not a particular assistant, tool API, or model generation. Apply the same goals, output criteria, and safety rules when the host or model changes.

## Target model and capability overlay

Profile: baseline; provider: unconfigured; model: unconfigured.
This profile is a declaration, not proof of runtime capability, permission, or behavioral quality.

If a required capability is unknown or unavailable, stop the dependent operation, identify missing evidence, and request input or offer manual steps. Do not claim completion.
Capability declarations never grant authorization. Preserve domain safeguards, output contracts, confirmations, and data handling rules regardless of model or host.

Required capabilities:
- text_reasoning: unknown. Verify actual availability before the dependent operation.
- Conditional web_retrieval: unknown. Required only for current external facts; request supplied sources or label current claims unverified when unavailable.
- Conditional file_access: unknown. Required for inspecting supplied files; accept pasted content or state extraction limits when unavailable.

Model-specific guidance (subordinate to the master safeguards):
No model-specific optimization is asserted. Verify capabilities in the selected host before use.

Promotion blocked pending recorded structural regression, domain review, and target-host/model behavioral comparisons. No future model compatibility is inferred.
