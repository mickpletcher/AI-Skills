# Model-aware candidate builds

The master describes the task, domain invariants, output criteria and capabilities. An ecosystem adapter describes host conventions. A model profile identifies an exact provider/model and declared capabilities, plus optional model-specific guidance. Neither adapter nor profile can grant permissions or relax master safeguards. Treat claims as hypotheses until verified in the actual deployment.

`baseline.json` is deliberately unconfigured: every capability is unknown, with no provider/model identity and no evidence. It generates the committed candidates under `generated/`. It is not a recommended model or a compatibility promise.

For an explicitly selected new model, copy the baseline into `<profile-id>.json`, set a distinct lowercase hyphenated `id`, exact `provider` and `model_id`, and keep unsupported/unknown capabilities honest. `overlay` is plain guidance subordinate to master rules; evidence contains reviewed artifact references, not credentials or personal inputs. Leave evidence empty until measured. Unknown capabilities require a runtime check or the master fallback; a supported declaration still requires host availability and authorization.

```sh
python tools/generate_master_skills.py --model-profile your-reviewed-profile
python tools/generate_master_skills.py --check --model-profile your-reviewed-profile
```

Non-baseline builds go to `generated-models/<profile-id>/<ecosystem>/skills/`, isolated from the committed baseline. The profile name must match an existing validated file; future model names are never guessed. These commands perform deterministic local generation only, with no API client, network, installation, or evaluation. Do not add secrets or personal outputs to profiles or generated bundles.

Each `build-provenance.json` records the content-addressed master bundle revision, ecosystem adapter path/hash (or explicit absence), model profile ID/hash, provider/model identity, generator/helper and ecosystem-path-map hashes, and unverified promotion/evaluation state. All generated files have hash ownership checks; manual edits block regeneration rather than being silently discarded. Preserve a reviewed prior build before changing its profile if it is an evaluation baseline.

OpenAI target IDs remain `chatgpt` and `codex`. Named-profile outputs use `generated-models/<profile>/openai/<target>/skills/`, matching the baseline grouping. This directory change does not widen suitability or establish model capabilities.

## Reassessment before promotion

A new model or profile change starts a new candidate, never an automatic promotion. First pass structural/source-preservation regressions. Then, with separate authorization for any model calls, compare identical synthetic tasks and settings in three conditions: prior approved model with its skill baseline; new model without the skill; new model with the generated candidate. Include triggers, near misses, missing inputs, unsupported capabilities, adversarial source content, high-stakes safeguards and output contracts. Compare domain correctness and safety first, then usefulness, latency/cost if measured, and unnecessary instruction overhead. Repeat enough to expose variability; keep failures and uncertainty visible.

Record exact provider/model/settings, master/adapter/profile provenance, input fixtures, outputs, rubric judgments, and reviewer. Propose revisions only where the comparison supports them; rerun the same cases after revisions. A stronger model may need less instruction, but removing safeguards or useful domain detail requires evidence. Promotion requires human review of regressions and behavior evidence; current tooling always labels builds unreviewed/not-run and never performs promotion. No automated assessment runner or paid calls are added here.

Ecosystem suitability is evaluated first from each master’s `ecosystems.json`. Even a model profile declaring every capability supported cannot generate an excluded target. `target-decisions.json` records the included/skipped decisions for each build.
