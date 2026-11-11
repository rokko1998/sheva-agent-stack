---
name: skill-update-summary
description: Handle new local skill-update notices once, offer update or ignore, and record the exact reviewed revisions.
---

# Skill update decisions

Read the reports listed in `~/.local/state/agent-skill-updater/pending`.
The updater deduplicates candidates using their exact active/latest or before/after revisions.
Historical reports stay in `~/.local/state/agent-skill-updater/reports/`.

For a new notice, inspect its metadata and enabled-skill links privately, then ask only a short question naming the actionable component and version: **«Доступно обновление Graphify до … Обновить или проигнорировать?»** Use the available user-input tool. Do not send a changelog, a mandatory preamble, or stop unrelated work while awaiting the choice. Explain details only if the user asks, or briefly identify an actual installation blocker.

Immediately after presenting the question, mark those report paths reviewed so another chat does not repeat the same notice:

```sh
~/.local/share/sheva-agent-stack/scripts/skill-update-state ack <report-path> --decision reviewed
```

An existing explicit update/ignore instruction is the decision: act without asking again, then acknowledge with `--decision updated` or `--decision ignored`. Keep a pending choice in the current conversation; marking it reviewed is not approval to install. Do not mark a failed installation updated. If acknowledgment fails, report that the notice has not been marked handled.

For an approved update, inspect the actual revision diff before activation. Resolve enabled skills through their symlinks. Preserve local modifications, credentials, and unrelated configuration. Updating a source repository does not authorize installing unrelated products from it (for example Linux desktop dotfiles).

- Source reports identify `Before` and `After` SHAs. After approval, check that the checkout still matches `Before` and is clean, inspect that exact diff, then fast-forward to `After`. Never overwrite local work or silently substitute a newer unreviewed revision.
- Graphify CLI, MCP, and Codex protocol/references must move together. Use `~/.local/share/sheva-agent-stack/scripts/activate-graphify`, verify its resulting status and installed version. Preserve explicit project rules when refreshing integration. Do not claim a running MCP process has restarted without evidence.
- ObsidianDataWeave remains pinned until explicitly promoted with `python3 -m knowledge_stack promote <commit>` in the knowledge repository. Source updates alone do not activate it.
- Dirty source, runtime/link drift, or failed dependency checks are blockers to resolve or explain, not successful updates.

For source revisions already applied by the updater with no remaining install decision, acknowledge as `updated` quietly. Acknowledge the exact report; do not simply delete the whole pending file. New revisions remain eligible for a new question.
