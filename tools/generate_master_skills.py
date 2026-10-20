#!/usr/bin/env python3
"""Generate isolated review candidates; never overwrite existing platform skills."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from skill_repository import frontmatter
from ecosystem_paths import PLATFORM_PATHS
from model_profiles import digest, load_profile, load_contract, model_guidance, load_ecosystems, local_tree

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
    appendix = ROOT / "adapters" / PLATFORM_PATHS[platform] / name / "append.md"
    suffix = appendix.read_text(encoding="utf-8").strip() if appendix.exists() else ""
    return body.rstrip() + ("\n\n" + suffix if suffix else "") + "\n"


def generate(check: bool = False, model_profile: str = "baseline"):
    for directory in ('master-skills', 'adapters', 'model-profiles', 'schemas'):
        local_tree(ROOT, ROOT / directory)
    profile, profile_hash = load_profile(ROOT, model_profile)
    output_root = ROOT / "generated" if model_profile == "baseline" else ROOT / "generated-models" / model_profile
    output_paths = local_tree(ROOT, output_root)
    # Plan and validate the complete bundle before writing anything.
    expected = {}
    resources = {}
    decisions = {}
    for source in sorted((ROOT / "master-skills").glob("*/SKILL.md")):
        files = sorted(source.parent.rglob("*"))
        frontmatter(source, ROOT)
        contract = load_contract(source)
        placement = load_ecosystems(source, TARGETS)
        decisions[source.parent.name] = placement
        bundle_hash = digest(json.dumps({p.relative_to(source.parent).as_posix(): digest(p.read_bytes()) for p in files if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}, sort_keys=True).encode())
        for platform, filename in TARGETS.items():
            if platform not in placement["allowed"]:
                continue
            folder = output_root / PLATFORM_PATHS[platform] / "skills" / source.parent.name
            expected[folder / filename] = (render(source, platform) + "\n" + model_guidance(profile, contract) + "\n").encode("utf-8")
            appendix = ROOT / "adapters" / PLATFORM_PATHS[platform] / source.parent.name / "append.md"
            provenance = {"master_revision": bundle_hash, "master_revision_kind": "sha256-bundle", "adapter": str(appendix.relative_to(ROOT)).replace("\\", "/") if appendix.exists() else None, "adapter_sha256": digest(appendix.read_bytes()) if appendix.exists() else None, "model_profile": profile["id"], "model_profile_sha256": profile_hash, "provider": profile["provider"], "model_id": profile["model_id"], "ecosystem": platform, "generator_sha256": digest(Path(__file__).read_bytes()), "profile_loader_sha256": digest(Path(__file__).with_name("model_profiles.py").read_bytes()), "promotion": "blocked_pending_review", "behavior_evaluation": "not_run"}
            provenance["ecosystem_paths_sha256"] = digest(Path(__file__).with_name("ecosystem_paths.py").read_bytes())
            expected[folder / "build-provenance.json"] = (json.dumps(provenance, sort_keys=True, indent=2) + "\n").encode()
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

    expected[output_root / "target-decisions.json"] = (json.dumps(decisions, indent=2, sort_keys=True) + "\n").encode()
    resources = {path.relative_to(output_root).as_posix(): digest(content) for path, content in expected.items()}
    manifest = output_root / ".resource-manifest.json"
    planned = {}
    for destination in [*expected, manifest]:
        for path in [destination, *destination.parents]:
            if path == output_root:
                break
            relative = path.relative_to(output_root).as_posix()
            entry = (relative, path == destination)
            if planned.setdefault(relative.casefold(), entry) != entry:
                raise ValueError(f'Case or file/directory collision in generated bundle: {relative}')
            if path.exists() and (not path.is_file() if path == destination else not path.is_dir()):
                raise ValueError(f'Generated destination has wrong file type: {path.relative_to(ROOT)}')
    previous = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
    if not isinstance(previous, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        or not re.fullmatch(r"[a-f0-9]{64}", value)
        or key.startswith("/") or "\\" in key or ".." in key.split("/")
        or (key != "target-decisions.json" and not any(
            key.startswith(PLATFORM_PATHS[target] + "/skills/")
            and len(key.split("/")) >= len(PLATFORM_PATHS[target].split("/")) + 3
            for target in TARGETS))
        for key, value in previous.items()
    ):
        raise ValueError("Invalid generated resource manifest")
    stale = {output_root / path for path in previous.keys() - resources.keys()}
    for path in output_paths:
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
            key = destination.relative_to(output_root).as_posix()
            existing = destination.read_bytes()
            owned = key in previous and hashlib.sha256(existing).hexdigest() == previous[key]
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
    parser.add_argument("--model-profile", default="baseline")
    args = parser.parse_args()
    generate(args.check, args.model_profile)
