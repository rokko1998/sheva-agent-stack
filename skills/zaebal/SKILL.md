---
name: zaebal
description: "Manage Z.A.E.B.A.L. settings or explicitly run its self-audit protocol. Automatic complaint detection is handled by the installed lifecycle hook; ordinary mentions of Z.A.E.B.A.L. do not require loading this skill."
---

# Z.A.E.B.A.L.

This is a thin Codex adapter for the upstream installation.

For an explicit `$zaebal` invocation or a direct request to manage Z.A.E.B.A.L.:

1. Read and follow:
   `~/.local/share/agent-skill-sources/github/howdeploy/Z.A.E.B.A.L/skills/zaebal/SKILL.md`
2. Resolve any relative references from that upstream skill directory.
3. Use the installed runtime at:
   `~/.zaebal/core/zaebal.py`

Do not duplicate the upstream protocol here.

The automatic profanity/complaint flow is implemented by the lifecycle hook and does not require implicit invocation of this skill.
