# Microsoft Copilot Studio

This directory is reserved for Microsoft Copilot Studio-specific skill and agent adaptations generated from the canonical `master-skills/` library.

Copilot Studio is distinct from GitHub Copilot and from consumer Microsoft Copilot. It uses agent instructions, topics, actions, connectors, and platform-managed configuration rather than assuming direct import of Claude-style `SKILL.md` archives.

Platform adapters belong in `adapters/microsoft/copilot-studio/<skill-name>/`. Before publishing a skill, verify the actual supported Copilot Studio import/deployment surface and permissions. Generated instructions alone do not create an agent, configure connectors, or grant access.

Existing platform directories and Claude originals remain unchanged. This directory establishes the integration target; generator and deployment support are pending.
