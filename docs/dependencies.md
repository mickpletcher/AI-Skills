# Dependencies and prerequisites

## Repository maintenance

- Python 3.11+ and `PyYAML==6.0.3` from [requirements-dev.txt](../requirements-dev.txt) for validation, catalogs, and packaging.
- PowerShell 7+ for the Windows/Linux CI matrix and installer regression suite. The installer also targets Windows PowerShell 5.1, but that runtime is not included in this matrix.
- Git for version control; no token is needed by local validators, catalog generation, packaging, or the offline evaluation runner.
- YAML is parsed with a safe loader that rejects duplicate mapping keys. The frontmatter schema validator supports only the keywords in [the schema](../schemas/skill-frontmatter.schema.json) and rejects unsupported extensions.

Install maintenance dependencies in an isolated environment:

```sh
python -m venv .venv
# Activate with the command appropriate for your shell, then:
python -m pip install -r requirements-dev.txt
```

## Skill-specific helpers

Most skill instructions require the relevant host and user-provided context rather than local packages. The catalog extracts declared README prerequisites and explicitly marks undeclared prerequisites; absence of a declaration is not proof that no dependency exists.

| Helper | Prerequisites and scope |
| --- | --- |
| `astrophotography-processing/scripts/fits_audit.py` | Python and Astropy; reads FITS headers. |
| `astrophotography-processing/scripts/image_stats_preview.py` | Python and Pillow; previews write only when requested. |
| `github-social-preview/scripts/generate_preview.py` | Python and Pillow; internet access for requested GitHub metadata. |
| `idea-forge/scripts/save_to_apple_notes.py` | Python, macOS, Apple Notes, and user-granted automation access. |
| `idea-forge/scripts/save_to_obsidian.py` | Python and an explicitly chosen writable local vault. |
| `trip-email-html-itinerary/scripts/Export-PublicDemoJpegs.ps1` | Windows-oriented PowerShell helper (`npx.cmd`, System.Drawing), Node/npx, Playwright CLI, and installed Edge/browser channel. Its existing `npx --yes --package playwright` can download dependencies; it is not run by repository validation. |
| Resume tips refresh helpers | PowerShell and the source/workspace access described in the skill README; the scheduled refresh workflow is separate from PR validation. |

Optional helper dependencies are not installed or executed by the new validation workflow. Review those helpers and their own instructions before use; compatible versions have not been newly certified here.
