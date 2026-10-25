# Plan

1. Update three source contracts and README provenance.
2. Add focused synthetic fixtures and deterministic regression checks, then regenerate candidates/catalog using repository tooling.
3. Run focused and aggregate checks; inspect all generated changes and record actual results.

Risk: prompt additions may not yield the intended native behavior. Preserve historical passes and label new native behavior not run. Rollback is reverting this focused change; no active host installation is modified.
