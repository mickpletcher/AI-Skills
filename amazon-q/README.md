# Amazon Q Developer

This directory is reserved for Amazon Q Developer-specific skill adaptations generated from the canonical `master-skills/` library.

Amazon Q Developer is distinct from Amazon Bedrock Agents. Its supported instruction and customization surfaces depend on the host and version; do not assume Claude-style `SKILL.md` packages can be imported directly.

Platform-specific instructions belong in `adapters/amazon-q/<skill-name>/`. Generated candidates should be isolated under `generated/amazon-q/` until installation requirements and behavior are verified.

The generator does not yet support Amazon Q Developer. Adding this directory does not install or deploy skills. Existing Claude skills remain unchanged.
