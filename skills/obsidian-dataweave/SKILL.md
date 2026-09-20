---
name: obsidian-dataweave
description: "Use the user's existing ObsidianDataWeave installation as the memory and knowledge layer for the Brain vault. Use for recalling or searching existing notes/wiki, processing notes or documents, NotebookLM workflows, LLM Wiki operations, and questions about what is already known in the user's vault."
---

# ObsidianDataWeave

Use the existing installation. Do not create a second installation.

## Existing runtime

- Repository: `/Users/sheva/tools/ObsidianDataWeave`
- Vault: `/Users/sheva/Documents/Obsidian/Vault/Brain`

## Canonical contract

Before performing a DataWeave operation:

1. Read `/Users/sheva/tools/ObsidianDataWeave/AGENTS.md`.
2. Treat that file and the repository's current scripts as the canonical behavior.
3. Read `/Users/sheva/tools/ObsidianDataWeave/SKILL.md` when intent mapping or workflow details are needed.

Do not duplicate those instructions here when the repository already defines them.

## Important rules

- Prefer `/Users/sheva/tools/ObsidianDataWeave/.venv/bin/python` for repository scripts.
- Do not overwrite `config.toml`.
- For recall or questions about vault/wiki knowledge, search the FTS5 memory before answering.
- Use the repository's write pipeline for vault mutations; do not bypass its writer or integrity guards.
- Use `--dry-run` before destructive operations when supported.
- Never bypass the LLM Wiki wikilink-preservation guard.
- Do not assume NotebookLM authentication exists. Check it before NotebookLM work and request interactive login only when required.
- Distinguish information recalled from the vault from general model knowledge.

## Current known state

The installation already has a working Brain vault, FTS5 memory index and LLM Wiki.

NotebookLM authentication and rclone are independent optional prerequisites and may need setup before workflows that require them.
