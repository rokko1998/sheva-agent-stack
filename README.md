# sheva-agent-stack

Agent infrastructure: shared Codex skills, lifecycle activation and the weekly updater for external Git sources. Knowledge policy and data are in the separate [sheva-knowledge-stack](https://github.com/rokko1998/sheva-knowledge-stack) repository.

Run `scripts/activate-knowledge-stack` to link that repository's `wrapup` skill, install its fast Codex hooks and verify its pinned ObsidianDataWeave runtime. The installer is idempotent. Changes to the knowledge pipeline belong in the knowledge repository; this repository owns only activation and external-source update discovery.

The weekly `scripts/update-agent-skills` updates clean upstream skill-source checkouts with fast-forward only. It also checks for newer ObsidianDataWeave commits through the knowledge repository, but leaves its pinned runtime unchanged. Promotion is a separate tested `python3 -m knowledge_stack promote <commit>` operation in the knowledge repository.
