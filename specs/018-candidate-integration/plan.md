# Candidate integration plan

1. Verify clean input branches and pinned commits, then create a local isolated branch from the common baseline (R1, R5).
2. Apply the candidate commits; resolve additive catalogs, ownership manifests, evaluation indexes and tests without modifying standalone skill content (R2, R3).
3. Remove the spec-number collision and add a complete-catalog regression (R3).
4. Regenerate candidate artifacts; rebuild shipped packages/catalog and verify they are unchanged (R3, R4).
5. Run the full offline suite, optimized focused suites, repository validation and harness self-test; retain skips and exact counts (R4).
6. Obtain independent read-only preservation/integration review, rerun checks at the committed head, and deliver local patch/bundle with no external publication or runtime claim (R4, R5).
