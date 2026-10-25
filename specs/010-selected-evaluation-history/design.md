# Design

Use the existing model-history schema without changing it. Native historical evaluations use its result enum; current not-run behavior and deterministic evidence live separately under review. Additional entry fields identify tested instruction hashes, pre-repair basis commits, host/version limits and bounded scope. Keep development_history empty because original authoring provenance is unknown.

Add spec-writer's metadata as a supporting resource in its migration record with its exact digest. Regenerate only through the established generator. Evidence URLs pin the already-committed main snapshot; fixture pointers identify the relevant cases. Private artifacts remain outside this index. A focused test-only validator supports precisely the existing schema keywords and rejects unsupported extensions without adding runtime dependencies.
