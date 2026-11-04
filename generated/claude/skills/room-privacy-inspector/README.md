# Room Privacy Inspector: review candidate

Editable source: [SKILL.md](SKILL.md). This standalone skill guides hotel/Airbnb guests through a non-invasive walkthrough, reviews supplied photos/video when the host can actually view them, and interprets already supplied Wi-Fi/Bluetooth results. It separates observations, possible explanations and unknowns. Optional [equipment guidance](references/equipment.md) covers iPhone/Android compatibility checks and limitations of optical, RF and external imaging methods. It never certifies a room or accesses suspect devices.

## Try it safely

Start with: “Guide a short visual privacy check of my hotel room without touching fixtures.” Or supply a fictional description: “A clock facing the bed has a shiny dark circle. What can I reasonably conclude?” No app, specialist equipment, account, code runner or other skill is required. No helper runs during this workflow.

## Proposed host setup

Only Claude and ChatGPT conversational candidates are generated. Cursor/Codex placement is deliberately skipped because this is a guest observation workflow, not repository development. This is a review candidate, not an installed or shipped package, and has no native-host acceptance claim.

For a disposable review session, provide `generated/claude/skills/room-privacy-inspector/SKILL.md` or `generated/openai/chatgpt/skills/room-privacy-inspector/instructions.md` with its `references/` directory and capability declaration. Use the host's supported instruction/file attachment surface; do not overwrite existing user configuration. Confirm referenced files and actual image/video capability are available. If they are not, use text guidance and label media unreviewed. Installation and promotion require separate review.

## Verification

[Evaluation protocol](references/evaluation.md) and [synthetic cases](fixtures/scenarios.json) cover ordinary objects, substantial concerns, ambiguous inputs and false positives. The cases are text-only synthetic inputs, not photographs or video and not proof of visual detection accuracy. Offline tests validate the fixture structure and declared coverage, not model compliance. No personal evidence belongs in this bundle.

Run from the repository root:

```sh
python -m unittest discover -s tools/tests -p 'test_room_privacy.py' -v
python tools/generate_master_skills.py --check
python tools/skill_compatibility.py --check
```

Primary capability sources and limits: [iPhone reference](references/phone-capabilities.md). Future host evaluation should include real synthetic media, inaccessible uploads, sampled video and repeated false-positive cases before any stronger claim.
