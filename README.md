# sheva-agent-stack

Agent infrastructure: shared Codex skills, lifecycle activation and the weekly updater for external Git sources. Knowledge policy and data are in the separate [sheva-knowledge-stack](https://github.com/rokko1998/sheva-knowledge-stack) repository.

Run `scripts/activate-knowledge-stack` to link that repository's `wrapup` skill, install its Codex lifecycle hooks and verify its pinned ObsidianDataWeave runtime. The installer reconciles its own hook block without changing other hooks. The knowledge repository owns the bounded Jev end-intent check, pending-session recovery, canonical writer, and AI Brain publication; this repository owns activation and external-source update discovery.

The weekly `scripts/update-agent-skills` updates clean upstream skill-source checkouts with fast-forward only. It also checks for newer ObsidianDataWeave commits through the knowledge repository, but leaves its pinned runtime unchanged. Promotion is a separate tested `python3 -m knowledge_stack promote <commit>` operation in the knowledge repository.

## Graphify structural code graph

Graphify is an independent, local code-intelligence layer. The clean upstream checkout is `~/.local/share/agent-skill-sources/github/Graphify-Labs/graphify` on its `v8` branch. `scripts/activate-graphify` installs that exact checkout as an isolated `graphifyy[mcp]` uv tool, enables Codex multi-agent support, registers one global stdio `graphify` MCP server, and links `~/.agents/skills/graphify` to this repository's thin skill adapter. It also activates the separate user-owned `architecture-review` skill. It does not run Graphify's broad Codex installer or change a project's application code.

The active CLI and MCP are `~/.local/bin/graphify` and `~/.local/bin/graphify-mcp` from the same uv tool environment. The adapter's `protocol.md` and `references/` symlinks point into that **installed package**, so the active Codex instructions cannot move ahead of the CLI/MCP when the weekly updater fast-forwards the upstream source. `scripts/activate-graphify --status` reports the active and available commits and detects runtime/skill drift. After reviewing an available upstream change, rerun `scripts/activate-graphify` to promote source, uv runtime, and active protocol together. Weekly update reports include the source diff and explicitly mark Graphify as available but unpromoted.

Build a project's local code graph only when requested:

```bash
~/.local/bin/graphify extract /path/to/project --code-only
~/.local/bin/graphify query "How does publication work?" --graph /path/to/project/graphify-out/graph.json
~/.local/bin/graphify update /path/to/project
```

The shared MCP server accepts `project_path` for each project; no default graph or per-project MCP entry is required. Graphify graphs are not canonical memory.

For explicit project onboarding, `scripts/graphify-project enable-project /path/to/project` adds or refreshes only the official `## graphify` section in `AGENTS.md`, and calls native `graphify hook install` for additive `post-commit` and `post-checkout` hooks. This also registers Graphify's merge driver in local Git config and adds `graphify-out/graph.json merge=graphify` to `.gitattributes`. `status-project` compares rules and hook blocks with the **active installed runtime**; `refresh-project` updates only those owned sections. Registered projects are refreshed by manual `activate-graphify` promotion, and the weekly update summary reports stale project integration. The installed Codex `graphify hook-check` PreToolUse command is a no-op, so no such hook is installed.

For a substantial implementation/refactor, the `architecture-review` skill uses Graphify `query`/`path`/`affected` for preflight, then a private baseline and native Graphify delta analysis. The official TypeSafe/SystemOne Jev classifies bounded structural and explicit-policy questions using [`policies/architecture-review/jev.md`](policies/architecture-review/jev.md); the adapter reuses the existing Keychain credential (`sheva-knowledge-stack/typesafe`) without depending on that repository at runtime. No project rule is invented. Example:

```bash
scripts/architecture-review baseline /path/to/project
scripts/architecture-review review /path/to/project --before /private/baseline.json --update --changed-file src/example.py
```

The graph, rules, Git hooks, skill, and Jev review are advisory. This integration does not enable a watch daemon, semantic/media extraction, CI blocking, global constitution, Graphify memory, or automatic Obsidian/AI Brain writes.
