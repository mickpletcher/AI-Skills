# Behavioral model-runner setup

PowerShell Refactor evaluation requires eight model comparisons from `evaluations/fixtures/powershell-refactor.json`.

Execution is gated on configured provider access and explicit selection of exact model IDs. No credentials belong in this repository.

For each case, run the original Claude skill and the generated candidate in isolated sessions with identical prompts and model settings. Capture the responses, review `must_preserve` and `forbidden_claims`, and record model IDs, timestamps, commit SHAs, and pass/fail evidence. Do not execute generated scripts.

This file records setup requirements only; it does not claim model tests have run.
