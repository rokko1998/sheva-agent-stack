---
name: graphify
description: "Inspect codebase architecture and file relationships with Graphify, especially when graphify-out/graph.json already exists. Build a new graph only when the user asks for one or the task explicitly requires it."
---

# Graphify

Graphify is this harness's structural code graph. It is separate from canonical knowledge and memory.

For architecture, dependency, call path, or blast-radius questions in a project with `graphify-out/graph.json`, query the existing graph with `/Users/sheva/.local/bin/graphify` or the shared Graphify MCP server. Use `query`, `explain`, `path`, `affected`, god nodes, and communities as relevant. Check source files for details that the graph cannot establish.

Do not build a graph merely because the user asks an ordinary code question. Build or update only when explicitly requested or necessary for a task that calls for a Graphify graph. Initial local code indexing uses `graphify extract <project> --code-only`; incremental refresh uses `graphify update <project>`. Do not run semantic extraction, a watch daemon, a Graphify installer, strict hooks, or knowledge/AI Brain publication from this skill. For requested project onboarding with upstream rules and native Git hooks, use the separate architecture-review project helper; it only changes Graphify-owned sections.

For Graphify's detailed Codex workflows, read [the installed upstream protocol](protocol.md) and only the relevant files in [references](references/). These links are installed from the same `graphifyy[mcp]` uv tool environment as the CLI and MCP. This harness's scope and installation boundaries above take precedence over the upstream protocol's general installer instructions.
