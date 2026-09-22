# sheva-agent-stack

Agent infrastructure: shared Codex skills, lifecycle activation and the weekly updater for external Git sources. Knowledge policy and data are in the separate [sheva-knowledge-stack](https://github.com/rokko1998/sheva-knowledge-stack) repository.

Run `scripts/activate-knowledge-stack` to link that repository's `wrapup` skill, install its Codex lifecycle hooks and verify its pinned ObsidianDataWeave runtime. The installer reconciles its own hook block without changing other hooks. The knowledge repository owns the bounded Jev end-intent check, pending-session recovery, canonical writer, and AI Brain publication; this repository owns activation and external-source update discovery.

The weekly `scripts/update-agent-skills` updates clean upstream skill-source checkouts with fast-forward only. It also checks for newer ObsidianDataWeave commits through the knowledge repository, but leaves its pinned runtime unchanged. Promotion is a separate tested `python3 -m knowledge_stack promote <commit>` operation in the knowledge repository.

## Graphify structural code graph

Graphify is an independent, local code-intelligence layer. The clean upstream checkout is `~/.local/share/agent-skill-sources/github/Graphify-Labs/graphify` on its `v8` branch. `scripts/activate-graphify` installs that exact checkout as an isolated `graphifyy[mcp]` uv tool, enables Codex multi-agent support, registers one global stdio `graphify` MCP server, and links `~/.agents/skills/graphify` to this repository's thin skill adapter. It does not run Graphify's installer or change AGENTS.md, hooks, or a project's application code.

The active CLI and MCP are `~/.local/bin/graphify` and `~/.local/bin/graphify-mcp` from the same uv tool environment. The adapter's `protocol.md` and `references/` symlinks point into that **installed package**, so the active Codex instructions cannot move ahead of the CLI/MCP when the weekly updater fast-forwards the upstream source. `scripts/activate-graphify --status` reports the active and available commits and detects runtime/skill drift. After reviewing an available upstream change, rerun `scripts/activate-graphify` to promote source, uv runtime, and active protocol together. Weekly update reports include the source diff and explicitly mark Graphify as available but unpromoted.

Build a project's local code graph only when requested:

```bash
~/.local/bin/graphify extract /path/to/project --code-only
~/.local/bin/graphify query "How does publication work?" --graph /path/to/project/graphify-out/graph.json
~/.local/bin/graphify update /path/to/project
```

The shared MCP server accepts `project_path` for each project; no default graph or per-project MCP entry is required. Graphify graphs are not canonical memory. This integration does not enable semantic/media extraction, a watch process, AGENTS.md injection, strict or Git hooks, architecture enforcement, or automatic Obsidian/AI Brain writes.
