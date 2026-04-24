# AI Skills

A shared home for AI skills organized by platform. Skills live under the platform they are written for. Shared docs cover conventions and repo guidance only.

## Claude Skills

| Skill | Description |
| ----- | ----------- |
| [alpaca-trading](./claude/skills/alpaca-trading/) | Safe workflows for the `Trading` repo and Alpaca-related automation |
| [blog-post](./claude/skills/blog-post/) | Write blog posts in Mick's voice for mickitblog.blogspot.com |
| [blog-to-social](./claude/skills/blog-to-social/) | Convert a finished blog post into Facebook, X, and LinkedIn posts in one pass |
| [container-home](./claude/skills/container-home/) | Off-grid shipping container lake home project in Dover, Tennessee |
| [crypto-listings](./claude/skills/crypto-listings/) | Track recent and upcoming cryptocurrency listings across major exchanges |
| [crypto-research](./claude/skills/crypto-research/) | Structured due diligence on a specific cryptocurrency |
| [facebook-post](./claude/skills/facebook-post/) | Write and polish Facebook posts in Mick's voice |
| [facebook-reply](./claude/skills/facebook-reply/) | Write replies to Facebook comments in Mick's voice |
| [fitness-log](./claude/skills/fitness-log/) | Track workouts, log progress, adjust training, and generate fitness Facebook posts |
| [food-analyzer](./claude/skills/food-analyzer/) | Analyze food photos and nutrition labels with glycemic, processing, and timing context |
| [github-readme](./claude/skills/github-readme/) | Write polished README.md files in a direct, technical, practitioner-focused voice |
| [linkedin-post](./claude/skills/linkedin-post/) | Write LinkedIn posts in Mick's professional voice |
| [n8n-workflow](./claude/skills/n8n-workflow/) | Design, build, and troubleshoot n8n workflows on a self-hosted Proxmox stack |
| [obsidian-workout-export](./claude/skills/obsidian-workout-export/) | Export logged workout sessions into Obsidian-ready Markdown files |
| [photo-rename](./claude/skills/photo-rename/) | Rename photos to descriptive names using image understanding and GPS metadata |
| [pihole-blocklist](./claude/skills/pihole-blocklist/) | Evaluate, categorize, and document new Pi-hole blocklist sources |
| [pihole-csv-analyzer](./claude/skills/pihole-csv-analyzer/) | Analyze Pi-hole CSV exports and generate practical cleanup recommendations |
| [proxmox-lxc](./claude/skills/proxmox-lxc/) | Deploy and configure Proxmox LXC containers on a self-hosted homelab stack |
| [resume-writer](./claude/skills/resume-writer/) | Rewrite, audit, and score resumes using recruiter and hiring-manager principles |
| [travel-itinerary](./claude/skills/travel-itinerary/) | Plan, format, and export travel itineraries as Obsidian-ready Markdown files |
| [travel-planning](./claude/skills/travel-planning/) | Plan solo travel with personal preferences, constraints, and active-trip context |
| [website-content](./claude/skills/website-content/) | Write and update content for mickpletcher.com |
| [x-post](./claude/skills/x-post/) | Write X posts on tech, PowerShell, IT automation, and fitness topics |
| [x-reply](./claude/skills/x-reply/) | Write replies to replies on X |

## ChatGPT Skills

| Skill | Description |
| ----- | ----------- |
| [food-analyzer](./chatgpt/skills/food-analyzer/) | Analyze food photos and nutrition labels |

## Repository Structure

- `shared/`: repo-wide guidance, standards, and naming rules
- `templates/`: starter templates for new skills
- `claude/`: Claude-specific skills, scripts, and metadata
- `chatgpt/`: ChatGPT-specific instructions, prompts, and schemas
- `copilot/`: GitHub Copilot instructions and prompts

## Working Model

1. Pick the target platform first.
2. Write the skill in that platform's folder as the source of truth.
3. Use `shared/` for naming, structure, and repo-level guidance only.
4. Record checks with [templates/test-template.md](./templates/test-template.md).

## Start Here

- [shared/skill-standard.md](./shared/skill-standard.md) before creating a new skill
- [shared/platform-organization.md](./shared/platform-organization.md) for folder intent
- [templates/skill-template.md](./templates/skill-template.md) as the base template
