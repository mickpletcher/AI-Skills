# Behavioral model-runner setup

PowerShell Refactor evaluation requires eight model comparisons from `evaluations/fixtures/powershell-refactor.json`.

Execution is gated on configured provider access and explicit selection of exact model IDs. No credentials belong in this repository.

For each case, run the original Claude skill and the generated candidate in isolated sessions with identical prompts and model settings. Capture the responses, review `must_preserve` and `forbidden_claims`, and record model IDs, timestamps, commit SHAs, and pass/fail evidence. Do not execute generated scripts.

This file records setup requirements only; it does not claim model tests have run.

The optional `tools/run_powershell_behavior.py` runner requires a direct HTTPS endpoint: all redirects are rejected so authentication cannot be forwarded to another endpoint. It does not retry failed requests. An existing output path is refused to preserve prior results. Each completed response is saved through an atomic checkpoint before the next request. Output retains `mode` and `cases` and adds `status` (`running`, `completed`, `partial`, or `error`); failures include the case ID and exception type, without provider error text or credentials. A failed run exits nonzero; keep its partial file and use a different output path for any subsequent run. An abrupt interruption may leave `status: running`, with all previously checkpointed cases intact.
