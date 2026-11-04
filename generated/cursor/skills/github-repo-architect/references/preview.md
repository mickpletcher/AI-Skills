# Project preview workflow

Automatically plan a project preview when turning a project description into repository structure. This is a project artifact, not proof the application works.

## Mode and artifact boundaries

- **blueprint-only**: include a root `preview.png` in the proposed tree and a proposed relative README embed; do not create, capture or upload files. PNG is the default social card; JPEG is an allowed photographic alternative and GIF an optional README motion demo. State planned/not created.
- **scaffold/generate files**: create the preview in the generated project's root, not in a nested docs/assets folder, when suitable authorized tools exist. Use PNG for the default social card, JPEG as a photographic alternative, and optionally GIF for a useful README motion demo; do not require animation. Preserve existing user artwork and respect an explicit opt-out. If tools are unavailable, list the missing artifact and exact follow-up rather than creating a placeholder with a fake image extension.
- **configure GitHub**: for a public repository, include setting the verified preview in Settings > Social preview in the proposed action list. Upload only within the specifically authorized scope and host confirmation policy, with a supported interface. Do not assume a REST endpoint exists or treat file-write permission as settings access. Configuring an existing image does not authorize generating new files or publishing a private repository. When the interface or permissions are unavailable, leave upload pending with manual steps.

## Make an honest, safe visual

For a working project, use a sanitized actual demo when capture and execution are authorized. Do not run unsafe code just to obtain a screenshot. For an idea or incomplete scaffold, create a clearly labeled **concept/mockup**, or an informational project card; never show invented successful output as a working demo. Capture no secrets, private data, personal notifications, browser tabs or unrelated desktop content. Use synthetic sample data and inspect every animation frame for leakage.

Provide meaningful README alt text and a nearby plain-text description. Animation must not carry the only explanation; provide a static fallback if motion is essential, avoid flashing, and keep duration/frame count modest. Do not promise that GIF animation survives GitHub or third-party social sharing.

## Validate actual bytes and links

Target **1280 × 640 pixels**, with **640 × 320 pixels** as the minimum quality target, and keep the actual file **under 1 MB** (use less than 1,000,000 bytes conservatively). Decode the file to verify format, dimensions and byte size; a renamed extension is not a conversion. Match `.gif`, `.jpg` or `.png` to the actual encoding. For GIF, check all frames and canvas dimensions. Resize/compress and recheck when needed; if validation cannot run, label it unverified rather than claiming compliance. Inspect the rendered visual for readability and truthful labels.

Verify the image exists in the project's root. Embed that actual filename with a relative link, for example `![Project preview: concept mockup](preview.png)`, and verify the README link resolves. Do not assert an uploaded settings image merely because the image is committed or README renders it.

## Social preview upload and verification

Confirm repository identity, public visibility, existing preview and permissions before proposing replacement. Explain the public-sharing implication and preserve any existing user preview unless replacement is authorized. Never make a repository public to enable this step. GitHub documents limited upload eligibility for private repositories with a previously uploaded image; do not assume a new private repository is eligible. For private/unknown visibility, report the setting deferred unless a supported, specifically authorized case is verified.

When permitted, use Settings > Social preview > Edit > Upload an image with the validated file. Reopen/read the resulting setting to verify that the intended image was selected and saved. Record this independently of root-file and README verification. If verification fails, report attempted-but-unverified; do not guarantee external platform caches have refreshed. If upload is blocked, give these steps as unexecuted manual follow-up and identify the required repository administrator.

Official source reviewed 2026-11-02: [GitHub social media preview documentation](https://github.com/github/docs/blob/main/content/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview.md). Recheck current supported formats, limits and UI before execution.
