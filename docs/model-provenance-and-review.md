# Model provenance and skill review

The repository's existing `changelog.md` records changes to the repository. Individual skill model provenance belongs in a machine-readable `model-history.json` alongside each canonical `master-skills/<skill>/SKILL.md`.

Record separately:
- **Development history:** actual model/provider used to author or revise a skill, date, description, and optional commit.
- **Evaluation history:** actual model/provider used to execute tests, date, test suite, result, and evidence.
- **Review status:** whether a review is needed, with a documented reason.

Do not infer historical model names from Git commits, file dates, or assumptions. Use `unknown` if provenance cannot be verified, and never claim a test occurred without test evidence.

When a new model becomes available, compare its capabilities, tool interfaces, and instruction handling against the skill's requirements. Flag affected skills for review; a new version alone is not proof of incompatibility. Prioritize failures, deprecated integrations, high-risk actions, and skills with old or missing evaluations. Log meaningful changes in the existing changelog.

Validate metadata against `schemas/skill-model-history.schema.json`. CI can later generate a review queue from this data and a maintained model compatibility registry. Model release detection and automated retesting require a separately configured source and actual test harness; neither is implemented by this document.
