# Room Privacy Inspector: bounded candidate validation

## Scope

New canonical master at `master-skills/room-privacy-inspector`, based on main `9c190e632c37588ae0ec73594c6714cf4d1ede86`. Proposed Claude and ChatGPT bundles only; no installed, promoted or native-host compatibility claim. Existing shipped skill sources/packages remain unchanged. Creation-time catalog and fixture labels remain `not_run`; separate internal text review does not silently upgrade them.

The skill covers a non-invasive hotel/rental walkthrough, supplied photo/video review with actual-access requirements, supplied Wi-Fi/Bluetooth interpretation, observations versus possible explanations versus unknowns, evidence minimization, safe escalation and optional iPhone/Android equipment guidance. No direct sensors, active network scans, unknown-device access, fixture interference, purchases or clean-room certification.

Primary Apple sources and manufacturer equipment references were checked 2026-11-04 and are linked in the skill's references. No exact phone/accessory combination was recommended, connected or tested. Compatibility checks are required at recommendation time, not assumed from shared connector shape.

## Verification boundaries

Sixteen synthetic text cases cover benign, suspicious, ambiguous and false-positive inputs, plus incomplete video, inaccessible media, prompt injection, phone indicators, tracker alerts and equipment limitations. These are text scenarios, not real photo/video files. Eight focused offline tests check fixture structure, negative cases and generated resource parity; they do not measure model behavior or detection performance.

Full repository and independent review results are recorded below after execution. No Windows PowerShell or native Claude/ChatGPT installation, routing, multimodal or field evaluation is claimed. The environment has no `pwsh` executable, so PowerShell validation is not run here. A new master does not inherit the repository's prior acceptance history.

## Executed offline checks

- Focused Room Privacy fixture contract/parity tests: 8 passed.
- Full Python repository suite: 321 tests, passed with 7 skips (five PowerShell-dependent itinerary tests and two Windows junction tests).
- Canonical generation and compatibility freshness checks: passed; 39 maps, 106 proposed target entrypoints across the repository. Room Privacy adds two entrypoints only.
- Repository validation: 46 shipped skills checked, zero issues. The new canonical-only candidate is additionally covered by migration, resource parity and generator tests.
- Packaging/catalog rebuild: passed and left shipped packages/catalog/checksums unchanged.
- Existing evaluation framework self-test: 24 synthetic contract cases and 99 negative checks passed; zero actual model evaluations in that command. These are framework checks, not 24 Room Privacy evaluations.
- `git diff --check`: passed.

Initial full run failed because the newly linked evaluation report had not yet been created: one release-test error and one link-validation failure. The report was added, validation rerun, and the full suite then passed as above. No domain safety behavior was changed to bypass tests.

## Independent internal text review

A fresh evaluator read the skill and operational references without fixture oracles and answered five adversarial prompts. Review found no concrete defect: no room clearance, thermal/USB-C overclaim, fixture removal, full-video inference or obedience to an injected Bluetooth label. This is bounded supplied-instruction behavior, not automatic routing or a native Claude/ChatGPT test. Expanded case evidence is recorded separately below when complete.

Expanded review: the same evaluator then received only IDs/prompts for all 16 synthetic manifest cases, not their oracles. Its actual responses were separately compared by the parent assistant against each required/forbidden behavior and observation/unknown boundary. All 16 passed that bounded manual text review; no harmful actions occurred. [Captured responses, individual rubric decisions and source hashes](fixtures/room-privacy-text-review-2026-11-04.json) retain the exact evidence. The evaluator's model snapshot was not reported. This is not an external model benchmark, native-host test, actual photo/video inspection, field detection test or personal human acceptance. Case fixture status fields and compatibility declarations remain conservative and unpromoted.
