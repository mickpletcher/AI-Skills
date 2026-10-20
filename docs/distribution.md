# Packaging, versions, and release preparation

## Reproducible packages

Release preparation includes existing shipped ChatGPT sources from `openai/chatgpt/` and the OpenAI directory guide. The existing `openai/codex/` example scaffold and `generated/` review candidates remain outside the release bundle; regrouping folders does not promote skills.

```sh
python tools/skill_repository.py package
python tools/skill_repository.py catalog
python tools/skill_repository.py validate
python tools/skill_repository.py package --check
```

The packager uses sorted relative paths, fixed 1980 timestamps, fixed regular-file permissions, ZIP_STORED (no compressor-version variance), and LF canonicalization for text files. It excludes archives, hidden files/directories, Python bytecode/caches, and `future-upgrades.md` local planning files. It rejects symlinked payloads. Keep unreviewed personal files outside skill source folders: every other visible source file is part of the package. Generated archives are intentionally larger than compressed predecessors.

Validation checks exact package member sets, CRCs, and every payload byte against canonical source content, then compares the whole archive with a deterministic rebuild. Modification times are not used. [SHA256SUMS](../SHA256SUMS) and [catalog.json](../catalog.json) are generated from the resulting archives. Rebuild packages after editing a packaged README, reference, history file, helper, or source—not only `SKILL.md`.

## Versions

A declared skill version must be a string matching the repository's `major.minor.patch` format with optional prerelease/build suffixes. Increment declared versions when changing behavior; use patch increments for compatible documentation/packaging corrections according to owner review. Four existing Claude skills have no declared version, and instruction-only platforms do not currently require frontmatter; the manifest reports null instead of inventing a release history. The owner should choose initial versions before presenting these as independently versioned releases.

For a repository bundle, the owner supplies a separate `vMAJOR.MINOR.PATCH` tag. A catalog entry's version is a source declaration, not evidence of model testing. Reference-only moves preserve source behavior and their original declared versions; the change history identifies the packaging/documentation transition.

## Release template

[The release workflow template](../.github/workflow-templates/release.yml) is deliberately outside `.github/workflows`, so it cannot run. After separate owner approval to activate release publishing, copy it into the workflows directory and review its permissions. It requires an existing version tag, validates the tagged source, creates a local distribution ZIP, and opens a **draft** release. It does not create tags or publish a release automatically. Configure an appropriate release review process before enabling it.

`python tools/prepare_release.py --version v1.2.3 --output /path/to/new-output` prepares a deterministic bundle only; it does not call GitHub. It refuses an empty LICENSE and an existing output directory. The bundle includes source, packages, catalog, checksums, maintenance docs/tools, and evaluation fixtures; Git internals, hidden/local files, and optional planning files are excluded.

Release preparation checks every explicit input and visible validation input for symlinks, Windows junctions, and paths outside the canonical repository root before reading source content. Markdown anchor targets receive the same check at their read boundary, including targets in hidden directories. Archive members are rechecked before packing. Use a reviewed checkout that is not being modified concurrently; these path checks do not provide isolation from concurrent filesystem replacement.

Release ZIP members are ordered by relative POSIX path strings. The checksum sidecar is explicit UTF-8 with LF endings. A fixed synthetic fixture hash is checked on Windows and Linux; the same-host rebuild test also checks the complete repository fixture and its extracted links.

## License

The root [LICENSE](../LICENSE) contains the MIT License, copyright 2026 Mick Pletcher. Existing third-party licenses and attribution notices remain applicable and must be preserved. The repository bundle includes the root license; the existing skill-specific license is retained unchanged.

The license choice satisfies the nonempty-license preparation gate. It does not activate the release workflow, create a tag, or authorize publishing a release. The workflow remains an inactive template requiring separate owner approval.
