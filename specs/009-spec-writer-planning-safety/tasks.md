# Tasks

- [x] T1 (S): Update canonical instructions and source transformation provenance.
- [x] T2 (S): Add synthetic planning fixtures and negative regression checks.
- [x] T3 (S): Regenerate candidates and run deterministic validation.
- [x] T4 (S): Review changed paths and record results/limits.

| Criterion | Validation task | Check | Expected result |
|---|---|---|---|
| AC-1 | T2 | Collision, reuse and incomplete-context fixtures plus negative mutations | Writes to unresolved destinations and duplicate new specs rejected by fixture checks |
| AC-2 | T2, T4 | Preservation/status mutations and scoped diff review | User files preserved; planning does not imply implementation done |
| AC-3 | T2 | Missing/dangling/empty-result mapping mutations | Invalid synthetic mappings rejected |
| AC-4 | T3 | Generator and shared-support regression checks | Four candidates agree with source and retain identical bundled standard |
