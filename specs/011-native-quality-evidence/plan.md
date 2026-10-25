# Plan

Sanitize completed evidence, link metadata, regenerate with existing tooling, run artifact/schema/provenance/aggregate checks, and review the diff. Publish a draft PR only after validation. No inference reruns or behavior fixes are needed. Reverting these evidence/metadata commits rolls back the index without changing behavior.
