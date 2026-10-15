# Skill modernization and migration standard

## Objective
Convert legacy platform-specific skills into improved platform-neutral master skills without changing existing installed skills until reviewed.

## Per-skill procedure
1. Inventory original instructions, trigger conditions, references, scripts, assets, tools, prerequisites, safety constraints and sample outputs.
2. Record baseline behavior and at least three representative tests, including one negative trigger and one missing-input case.
3. Audit for outdated tool assumptions, unsafe automation, hallucination risks, excessive prompt length, unclear branching, duplicate instructions, missing failure handling, and platform coupling.
4. Draft a platform-neutral master defining intent, inputs, outputs, decision flow, boundaries, error recovery, and verification requirements.
5. Propose improvements explicitly. Preserve essential original behavior unless a documented change is justified.
6. Put platform-specific commands, integration requirements, and supported capabilities in adapters; never imply access to a tool without checking.
7. Generate candidate outputs and test against baseline and improved scenarios. Mark unsupported capabilities and behavior changes.
8. Review changes and promote the migrated skill only after checks pass. Do not overwrite original Claude sources automatically.

## Assessment record
For each skill create a review containing: original path, original version if declared, purpose, dependencies, known risks, improvement proposals, compatibility matrix, baseline tests, regression results, and migration status.

## Migration stages
- inventoried
- assessed
- generalized
- adapted
- tested
- reviewed
- promoted

## Safety
Existing Claude skills remain authoritative until each migration is approved. Generated artifacts must not overwrite hand-authored files. A failure to validate blocks promotion, not existing installations. Avoid copying personal credentials or private data into shared master skills.
