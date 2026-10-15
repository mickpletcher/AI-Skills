#!/usr/bin/env python3
"""Generate isolated review candidates; never overwrite existing platform skills."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {"claude": "SKILL.md", "chatgpt": "instructions.md", "cursor": "instructions.md", "codex": "SKILL.md"}
MARKER = "<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->"

def render(source: Path, platform: str) -> str:
    name = source.parent.name
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"Invalid skill directory name: {name}")
    body = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not body.startswith("---\n") or "\n---\n" not in body[4:]:
        raise ValueError(f"Missing YAML frontmatter: {source}")
    appendix = ROOT / "adapters" / platform / name / "append.md"
    suffix = appendix.read_text(encoding="utf-8").strip() if appendix.exists() else ""
    # Append outside frontmatter so metadata stays intact.
    return MARKER + "\n" + body.rstrip() + ("\n\n" + suffix if suffix else "") + "\n"

def generate(check: bool = False):
    failures = []
    for source in sorted((ROOT / "master-skills").glob("*/SKILL.md")):
        for platform, filename in TARGETS.items():
            destination = ROOT / "generated" / platform / "skills" / source.parent.name / filename
            expected = render(source, platform)
            if check:
                if not destination.exists() or destination.read_text(encoding="utf-8") != expected:
                    failures.append(str(destination.relative_to(ROOT)))
            else:
                if destination.exists() and not destination.read_text(encoding="utf-8").startswith(MARKER):
                    raise RuntimeError(f"Refusing to overwrite unmanaged file: {destination}")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(expected, encoding="utf-8")
                print("GENERATED", destination.relative_to(ROOT))
    if failures:
        for path in failures:
            print("MISSING OR DRIFTED", path)
        raise SystemExit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generate(args.check)
