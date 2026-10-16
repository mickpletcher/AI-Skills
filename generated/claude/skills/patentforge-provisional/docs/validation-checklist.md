# Validation Checklist

## Metadata

- YAML frontmatter exists in `SKILL.md`
- `name` exists in the YAML frontmatter
- `description` exists in the YAML frontmatter

## Safety

- `SKILL.md` states that this is not legal advice
- `SKILL.md` states that prior art results are not exhaustive
- `SKILL.md` states that claim candidates are drafting aids only
- `SKILL.md` states that a registered patent attorney should review before filing
- `SKILL.md` states that the user is responsible for final Patent Center submission
- No file introduces forbidden certainty language

## File Completeness

- All requested templates exist
- All requested schemas exist
- All requested docs exist
- Example input and example output files exist
- `LICENSE` exists
- `README.md` explains installation and trigger metadata behavior

## Schema Validation

- `schemas/invention-disclosure.schema.json` is valid JSON
- `schemas/claim-set.schema.json` is valid JSON
- `schemas/prior-art-report.schema.json` is valid JSON

## Output Shape

- The expected final output contains all 14 required sections
- The final section includes the required disclaimer
- The workflow includes intake, prior art, claim drafting, provisional drafting, figure list, filing checklist, and attorney review notes
