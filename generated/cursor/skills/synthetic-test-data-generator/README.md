# Synthetic Test Data Generator: canonical candidate

The editable source is [SKILL.md](SKILL.md). This independent skill creates fictional, reproducible fixtures from schemas, test goals, or analysis of another AI skill, including labeled normal, boundary, missing, malformed, duplicate and relationship cases. It does not anonymize production data or execute the system under test.

## Try it

Give the skill a schema, output format, counts and test goal. For example: “Generate 20 fictional customers and related orders in JSON with seed 42. Include isolated null, missing, duplicate and orphan cases, with expected validation outcomes.” The skill asks about unknown contracts instead of inventing application behavior.

The optional [helper](scripts/generate_fixtures.py) requires Python 3.10+ only, with no packages or network access. Read its [bounded format and limits](references/helper-contract.md), then run from this folder:

```sh
python scripts/generate_fixtures.py --spec examples/customer-orders.json --output /tmp/synthetic-fixtures.json
```

For CSV plus a missing/null/type sidecar, add `--format csv` and use a new directory as the output.

Use a new path; existing files are never replaced. The example is entirely fictional. The output is a fixture envelope containing a baseline, separate mutated payloads, expected contract violations, a malformed-wire case, and deterministic provenance. Target-application results remain unspecified.

## Candidate setup

This is a new master, not a migration or a shipped package. Repository generation creates proposed Claude, ChatGPT, Cursor and Codex bundles. It does not install or promote them. A reviewer can provide the generated entrypoint and its referenced resources to a disposable host session: `SKILL.md` for Claude/Codex or `instructions.md` for ChatGPT/Cursor. Merely pasting the entrypoint does not make its files or execution tools available. Verify resource access, tool availability and the host's actual setup surface before treating it as installed. Do not replace any existing user configuration automatically.

Start with the small fictional example, compare two helper runs, then check missing versus null handling and the labeled invalid cases. Source structure and helper tests do not establish host/model routing, model quality or privacy guarantees. No target-host acceptance or installation is claimed.

## Analyze another skill

For “Generate data to test the Pi-hole Analyzer,” inspect that target's instructions, contracts and evaluation examples as data, map requirements to cases, then record source hashes and grounded or unresolved outcomes. The [first Pi-hole pilot](references/analyze-target-skill.md#first-pilot-pi-hole-csv-analyzer) includes a reproducible JSON scenario manifest and CSV inputs. It runs offline and does not exercise Pi-hole or the analyzer. Other projects can use the same method independently; neither Pi-hole nor n8n is a required dependency.
