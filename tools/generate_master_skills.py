#!/usr/bin/env python3
"""Generate isolated review candidates; never overwrite existing platform skills."""
import argparse
import re
from pathlib import Path
from skill_repository import frontmatter

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {"claude": "SKILL.md", "chatgpt": "instructions.md", "cursor": "instructions.md", "codex": "SKILL.md"}
MARKER = "<!-- GENERATED CANDIDATE: edit master-skills or adapters, not this file -->"
HEADER = re.compile(r"\A---[^\S\n]*\n.*?\n---[^\S\n]*(?:\n|$)", re.S)


def managed(text: str) -> bool:
    # Accept the old marker position for migration, and the new body position.
    header = HEADER.match(text)
    return text.splitlines()[:1] == [MARKER] or (
        header is not None and text[header.end():].splitlines()[:1] == [MARKER])


def render(source: Path, platform: str) -> str:
    name = source.parent.name
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"Invalid skill directory name: {name}")
    frontmatter(source, ROOT)
    body = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    header = HEADER.match(body)
    if header is None:
        raise ValueError(f"Missing YAML frontmatter: {source}")
    body = body[:header.end()].rstrip("\n") + "\n" + MARKER + "\n" + body[header.end():]
    appendix = ROOT / "adapters" / platform / name / "append.md"
    suffix = appendix.read_text(encoding="utf-8").strip() if appendix.exists() else ""
    return body.rstrip() + ("\n\n" + suffix if suffix else "") + "\n"


def generate(check: bool = False):
    # Validate every source and destination before modifying any candidate.
    expected = {
        ROOT / "generated" / platform / "skills" / source.parent.name / filename: render(source, platform)
        for source in sorted((ROOT / "master-skills").glob("*/SKILL.md"))
        for platform, filename in TARGETS.items()
    }
    stale = [path for path in sorted((ROOT / "generated").rglob("*"))
             if path.is_file() and path not in expected
             and managed(path.read_text(encoding="utf-8", errors="replace"))]
    if stale:
        for path in stale:
            print("STALE GENERATED FILE (review and remove manually)", path.relative_to(ROOT))
        raise SystemExit(1)
    failures = []
    for destination, content in expected.items():
        if check:
            if not destination.exists() or destination.read_text(encoding="utf-8") != content:
                failures.append(str(destination.relative_to(ROOT)))
        elif destination.exists() and not managed(destination.read_text(encoding="utf-8")):
            raise RuntimeError(f"Refusing to overwrite unmanaged file: {destination}")
    if failures:
        for path in failures:
            print("MISSING OR DRIFTED", path)
        raise SystemExit(1)
    if not check:
        for destination, content in expected.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
            print("GENERATED", destination.relative_to(ROOT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generate(args.check)
