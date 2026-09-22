---
name: skill-update-summary
description: "Analyze pending updates of GitHub-sourced agent skills and available pinned DataWeave or Graphify revisions. Use when SessionStart reports source changes or the user asks what changed in installed skills."
---

# Skill Update Summary

Analyze updates recorded by the local agent-skill updater.

Pending report list:

`~/.local/state/agent-skill-updater/pending`

GitHub source repositories:

`~/.local/share/agent-skill-sources/github/`

Enabled Codex skills:

`~/.agents/skills/`

## Goal

Do not merely repeat commit messages.

Explain the update as if teaching the owner of this agent environment:

- what actually changed;
- what problem the change solves;
- why the author implemented it this way when that can be established from the code or documentation;
- whether agent behavior or automatic skill activation changed;
- whether usage changed;
- whether installation, dependencies, permissions, scripts, hooks, network behavior, or security boundaries changed;
- whether new skills or capabilities appeared;
- whether the user needs to do anything.

Distinguish clearly between:
- facts established by the diff or repository documentation;
- reasonable inference;
- external research.

## Workflow

1. Read every report path listed in `~/.local/state/agent-skill-updater/pending`.
2. For every `UPDATED` repository, read its recorded `Before` and `After` SHAs. For an `AVAILABLE: ObsidianDataWeave` entry, read `Active` and `Latest`; this is an unpromoted candidate.
3. Inspect the actual Git diff between those revisions. For DataWeave, use its clean upstream checkout and compare active to latest without changing the pinned runtime.
4. Read changed `SKILL.md`, `agents/openai.yaml`, README/docs, hooks and scripts when relevant.
5. Resolve symlinks under `~/.agents/skills/` to determine which changed skills are currently enabled.
6. Prioritize changes affecting enabled skills.
7. Separately mention interesting newly added skills or capabilities that are not enabled.
8. Treat metadata changes as behavioral changes when they affect:
   - `name`;
   - `description`;
   - OpenAI metadata;
   - implicit invocation behavior;
   - trigger wording.
9. Treat changes to scripts, hooks, network access, dependencies, credentials, permissions or filesystem behavior as security-sensitive and explain them explicitly.
10. If commit messages and actual code disagree, trust the actual diff.
11. Use the researcher skill when understanding an update genuinely requires current external information.
12. Do not inflate cosmetic changes into meaningful updates.
13. For an available DataWeave revision, explain the candidate and any compatibility concerns. State explicitly that it has **not** been activated. Promotion is `python3 -m knowledge_stack promote <commit>` in the knowledge repository after review; never imply that the weekly updater performed this step.
14. For `AVAILABLE: Graphify`, compare source commits and changed skill, CLI, MCP, or dependency files. The updater may fast-forward the clean upstream source, but it does not promote the installed uv tool. The active Codex protocol/references are linked to that tool, so they stay aligned with CLI/MCP. State the active and available commits and version; activation is `~/.local/share/sheva-agent-stack/scripts/activate-graphify` after review. For `ATTENTION: Graphify`, explain dirty source or runtime/link drift and do not imply promotion succeeded.

## Output

Start with a short plain-language overview.

For every meaningful change use:

### <skill or component>

**Что изменилось:** concrete behavioral or structural change.

**Зачем:** what problem it solves.

**Что это меняет для меня:** practical effect in this Codex / CanvasTTY setup.

**Как пользоваться:** only when usage changed or a new capability appeared.

**Нужно ли что-то сделать:** exact action, or explicitly say that no action is required.

If nothing affecting enabled skills changed, say so explicitly.

## Completion

Only after all pending update reports have been successfully analyzed and explained:

remove:

`~/.local/state/agent-skill-updater/pending`

Do not delete historical reports from:

`~/.local/state/agent-skill-updater/reports/`
