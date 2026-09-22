---
name: architecture-review
description: "Review substantial code implementations and refactors against an existing Graphify structural baseline and explicit project architecture rules. Use for meaningful architecture changes, not documentation, typos, simple questions, or trivial edits."
---

# Architecture review

Use [Graphify](../graphify/SKILL.md) and its active upstream protocol for structural facts. This skill adds preflight, delta review, and bounded official Jev decisions. It does not impose a global constitution or write to Obsidian/AI Brain.

Before a substantial change, inspect the existing graph with `graphify query`, `affected`, relevant neighbors/community, and `path` where applicable. Identify target components, dependency and data flow, blast radius, current abstraction, community boundary, and expected structural change. Then run `scripts/run-architecture-review baseline <project>` and keep its private snapshot path. If the graph is absent and the task explicitly requires one, run `graphify extract <project> --code-only` first.

After editing code, run `scripts/run-architecture-review review <project> --before <snapshot> --update` to perform a Graphify AST update, native graph diff/analysis, and two official Jev Choice decisions. Add `--changed-file` for each changed file. Project rules may be supplied with `--rules-file <json>` only when they are explicitly documented with a source citation; set `matched: true` only for rules applicable to this delta. Inspect source and Graphify further if Jev says UNCERTAIN, then retry with additional bounded evidence if available. Do not seek a second LLM approval for ordinary Jev decisions.

`scripts/graphify-project enable-project <project>` installs the active upstream `## graphify` section and native post-commit/post-checkout hooks, preserving other AGENTS sections and hook logic. `status-project` detects stale rules and pinned-runtime hook blocks. `refresh-project` updates only Graphify-owned sections after runtime promotion. The Codex Graphify `hook-check` PreToolUse command is intentionally a no-op in this installed runtime and is not part of this workflow.

Graphify says what exists and changed; Jev classifies the bounded delta; the coding agent explains and implements; explicit project policy defines allowed architecture. See [review contract](references/review-contract.md) for state, outcome, and provenance rules. Never invent project architecture rules from generic design advice. A graph delta reports structural evidence, not a verdict on application correctness.
