#!/usr/bin/env python3
"""Generate isolated review candidates; never overwrite existing platform skills."""
import argparse
import hashlib
import json
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
    # Plan and validate the complete bundle before writing anything.
    if (ROOT / "generated").is_symlink():
        raise ValueError("Refusing generated symlink root")
    expected = {}
    resources = {}
    for source in sorted((ROOT / "master-skills").glob("*/SKILL.md")):
        files = sorted(source.parent.rglob("*"))
        if any(path.is_symlink() for path in [source.parent, *files]):
            raise ValueError(f"Symlinks are not supported in master bundles: {source.parent}")
        for platform, filename in TARGETS.items():
            folder = ROOT / "generated" / platform / "skills" / source.parent.name
            expected[folder / filename] = render(source, platform).encode("utf-8")
            for path in files:
                if not path.is_file() or (path == source and filename == "SKILL.md"):
                    continue
                relative = path.relative_to(source.parent)
                if path.suffix in (".skill", ".pyc") or "__pycache__" in relative.parts:
                    continue
                destination = folder / relative
                if destination in expected:
                    raise ValueError(f"Resource collides with generated instructions: {destination}")
                expected[destination] = path.read_bytes()
                resources[destination.relative_to(ROOT / "generated").as_posix()] = hashlib.sha256(expected[destination]).hexdigest()

    manifest = ROOT / "generated/.resource-manifest.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else {}
    if not isinstance(previous, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        or not re.fullmatch(r"[a-f0-9]{64}", value)
        or key.startswith("/") or "\\" in key or ".." in key.split("/")
        or len(key.split("/")) < 4 or key.split("/")[0] not in TARGETS
        or key.split("/")[1] != "skills"
        for key, value in previous.items()
    ):
        raise ValueError("Invalid generated resource manifest")
    stale = {ROOT / "generated" / path for path in previous.keys() - resources.keys()}
    for path in sorted((ROOT / "generated").rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Refusing generated symlink: {path}")
        if path.is_file() and path not in expected and path != manifest and managed(path.read_text(encoding="utf-8", errors="replace")):
            stale.add(path)
    if stale:
        for path in sorted(stale):
            print("STALE GENERATED FILE (review and remove manually)", path.relative_to(ROOT))
        raise SystemExit(1)

    failures = []
    for destination, content in expected.items():
        if check:
            if not destination.exists() or destination.read_bytes() != content:
                failures.append(str(destination.relative_to(ROOT)))
        elif destination.exists():
            key = destination.relative_to(ROOT / "generated").as_posix()
            existing = destination.read_bytes()
            if key in resources:
                owned = key in previous and hashlib.sha256(existing).hexdigest() == previous[key]
            else:
                owned = managed(existing.decode("utf-8"))
            if not owned:
                raise RuntimeError(f"Refusing to overwrite unmanaged or edited file: {destination}")
    manifest_content = (json.dumps(resources, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if check and (not manifest.exists() or manifest.read_bytes() != manifest_content):
        failures.append(str(manifest.relative_to(ROOT)))
    if failures:
        for path in failures:
            print("MISSING OR DRIFTED", path)
        raise SystemExit(1)
    if not check:
        for destination, content in expected.items():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_bytes(manifest_content)
        print(f"GENERATED {len(expected)} files across {len(TARGETS)} target platforms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generate(args.check)
