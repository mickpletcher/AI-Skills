# Design

Extract the existing traceability assertions into a shared test helper. Require nonempty referenced IDs for each parsed criterion, then check ID membership and expected-result text. Mutate only an in-memory copy of the recorded AC-1 row to a blank Validation cell; keep committed evidence unchanged.
