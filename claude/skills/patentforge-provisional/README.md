# PatentForge Provisional Claude Skill

Structured Claude skill for turning a raw invention idea into an invention disclosure, prior art search strategy, claim candidates, and a provisional draft package for review.

## What This Skill Does

- Captures a rough invention idea
- Asks targeted disclosure questions
- Converts answers into a structured invention disclosure
- Identifies technical components and novelty candidates
- Suggests prior art search terms and possible CPC areas
- Generates claim candidates as drafting aids
- Builds a provisional style draft package
- Produces a figure list, filing checklist, and attorney review notes

## What This Skill Does Not Do

- It does not provide legal advice.
- It does not guarantee patentability, allowance, or protection.
- It does not replace a registered patent attorney.
- It does not submit anything to Patent Center.
- It does not perform exhaustive prior art searching.

## Claude Trigger Metadata

Claude skills are triggered by the `name` and `description` metadata in [`SKILL.md`](./SKILL.md). The description must be specific enough to tell Claude when this skill should be used instead of a more general drafting skill.

## Files

```text
claude/skills/patentforge-provisional/
|-- LICENSE
|-- README.md
|-- SKILL.md
|-- upgrades.md
|-- future-upgrades.md
|-- completedchanges.md
|-- patentforge-provisional.skill
|-- docs/
|   |-- patent-center-upload-guide.md
|   |-- safety-rules.md
|   |-- validation-checklist.md
|   `-- workflow.md
|-- examples/
|   |-- sample-idea.md
|   `-- sample-output.md
|-- schemas/
|   |-- claim-set.schema.json
|   |-- invention-disclosure.schema.json
|   `-- prior-art-report.schema.json
`-- templates/
    |-- attorney-review-notes.md
    |-- claim-candidates.md
    |-- filing-checklist.md
    |-- invention-disclosure.md
    |-- prior-art-report.md
    `-- provisional-application.md
```

## Installation

Use either of these locations depending on how you manage Claude skills:

- Repo source location: `C:\Users\mick0\OneDrive\Documents\Code & Dev\GitHub\AI-Skills\claude\skills\patentforge-provisional`
- Local Claude skills directory example: `C:\Users\mick0\OneDrive\Documents\Codex\Skills\patentforge-provisional`

If you use packaged imports, import [`patentforge-provisional.skill`](./patentforge-provisional.skill). If you manage skills manually, place the folder where your Claude setup reads local skills from.

## Example Prompts

```text
Use patentforge-provisional for this idea: a modular cable routing clip for workshop benches that can be repositioned without tools.
```

```text
Turn this invention concept into an invention disclosure, prior art search strategy, claim candidates, and a provisional draft package. Ask me any missing questions first.
```

```text
Draft claim candidates and a provisional package for a software system that detects machine maintenance drift using sensor data and adaptive thresholds. Keep the output as drafting support only.
```

## Safety Disclaimer

This skill is a drafting and organization aid only. It is not legal advice. Prior art results are not exhaustive. Claim candidates are drafting aids only. A registered patent attorney should review any output before filing. The user is responsible for final Patent Center submission.

## Future Roadmap

- Add optional intake modes for hardware, software, and chemistry heavy inventions
- Add structured figure prompt templates for diagram generation workflows
- Add optional export formats for attorney intake packets
- Add stronger internal validation against the included JSON schemas

## Upgrade Log

See [upgrades.md](upgrades.md) for the structured upgrade log and [completedchanges.md](completedchanges.md) for tracked completed changes.

## Implement In Claude

1. Update the checked in source files for this skill first.
2. Rebuild `patentforge-provisional.skill` from the current source files. Include all supporting templates, schemas, docs, and examples the package depends on.
3. Import the `.skill` package into Claude using your normal Claude skills workflow, or place the folder in your local Claude skills directory if you manage skills manually.
4. Refresh Claude or start a new chat, then test the skill with one of the example prompts in this README.
