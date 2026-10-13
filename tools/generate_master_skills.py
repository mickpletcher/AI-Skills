#!/usr/bin/env python3
"""Deterministic, standard-library-only cross-platform skill generator."""
import argparse
import difflib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {"claude": "SKILL.md", "chatgpt": "instructions.md", "cursor": "instructions.md", "codex": "SKILL.md"}

def generate(check=False):
    failed = []
    for source in sorted((ROOT / "master-skills").glob("*/SKILL.md")):
        name = source.parent.name
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill directory name: {name}")
        body = source.read_text(encoding="utf-8")
        if not body.startswith("---\n") or "\n---\n" not in body[4:]:
            raise ValueError(f"Missing YAML frontmatter: {source}")
        for platform, filename in TARGETS.items():
            appendix = ROOT / "adapters" / platform / name / "append.md"
            suffix = appendix.read_text(encoding="utf-8") if appendix.exists() else ""
            output = body.rstrip() + ("\n\n" + suffix.strip() if suffix.strip() else "") + "\n"
            destination = ROOT / platform / "skills" / name / filename
            if check:
                actual = destination.read_text(encoding="utf-8") if destination.exists() else ""
                if actual != output:
                    failed.append(str(destination.relative_to(ROOT)))
                    print("DRIFT:", failed[-1])
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(output, encoding="utf-8")
                print("GENERATED:", destination.relative_to(ROOT))
    if failed:
        raise SystemExit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generate(args.check)
