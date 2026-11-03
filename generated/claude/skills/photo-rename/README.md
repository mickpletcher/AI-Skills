# photo-rename: canonical candidate

Read `SKILL.md` for the portable workflow. This is a review candidate, not a shipped or behavior-evaluated replacement.

The [original README](https://github.com/mickpletcher/AI-Skills/blob/1deaab97ec585b6451a7ed80bc2a4398a8428ecc/claude/skills/photo-rename/README.md) retains the source installation instructions, prerequisites, examples, and author context. Original packages and maintenance history remain in the Claude tree. `migration.json` records exact source provenance, metadata, transformations, and dependency hashes. Existing personal preferences and domain examples are preserved, not newly verified.

Supporting files retain their original relative paths and bytes, including any skill-specific license. The repository MIT license applies where no separate notice says otherwise. Generated candidates include these resources; a host must actually support their required tools and file access. Do not execute helpers or install integrations merely by generating a candidate.

## Safe file operations

Read [the file-operation safety workflow](references/file-operation-safety.md) before running [the optional copy helper](scripts/safe_photo_copy.py). Requires Python 3.10+ standard library and a trusted, quiescent local filesystem. It preserves originals and uses reviewed, no-overwrite copies; it does not rename in place or install anything. Synthetic regression tests: `python -m unittest discover -s tools/tests -p test_photo_copy_safety.py -v` from the repository root.
