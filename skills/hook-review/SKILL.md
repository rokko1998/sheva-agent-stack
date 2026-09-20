---
name: hook-review
description: "Review a new or modified Codex lifecycle hook before the user trusts it. Analyze the exact hook definition, source, command, referenced scripts and relevant imports, then explain what it does, why it exists, what data it can access, what side effects it can have, and whether anything materially changed. Use when the user shows a hook that needs Review, asks whether a hook is safe to trust, or asks what an installed hook does."
---

# Hook Review

Review Codex lifecycle hooks before the user marks them as trusted.

The goal is not merely to describe the command line.

Trace the hook far enough to understand its actual behavior.

## Inputs

Use any hook information the user provides, including:

- event;
- source;
- matcher;
- command;
- timeout;
- async/sync mode;
- status message;
- context limit;
- hook definition shown by `/hooks`;
- referenced script or executable.

If the hook definition is incomplete, inspect its source files before drawing conclusions.

## Workflow

1. Identify the hook event and when it runs.

2. Identify the source:
   - user config;
   - project config;
   - plugin;
   - CanvasTTY/runtime;
   - managed/system source;
   - other source.

3. Read the exact command that Codex will execute.

4. If the command references a script, executable or module:
   - inspect that file;
   - inspect directly relevant imports or helper modules;
   - stop once the actual side effects and data flow are understood.

5. Determine what input the hook receives:
   - stdin payload;
   - environment variables;
   - arguments;
   - filesystem state;
   - network access.

6. Determine what the hook can do:
   - read files;
   - write files;
   - launch processes;
   - modify configuration;
   - access credentials;
   - use the network;
   - alter agent/tool behavior;
   - add context to the model;
   - approve, deny or influence actions.

7. Distinguish:
   - observed behavior from code;
   - documented intent;
   - inference.

8. If this appears to be an updated version of a previously trusted hook, compare the relevant implementation when possible and explain the meaningful difference.

9. Do not treat a familiar path, publisher or plugin name as sufficient evidence by itself.

10. Prefer primary sources:
    - installed source code;
    - upstream repository;
    - official documentation.

## Output

Explain the hook in this format:

### Что это

Short explanation of the hook's role.

### Когда срабатывает

Event and matcher behavior.

### Что реально выполняется

Trace from hook definition to the relevant implementation.

### Какие данные получает

Inputs and environment available to it.

### Что может изменить

Filesystem, processes, network, permissions, model context or other side effects.

### Зачем нужен

Documented or clearly inferred purpose.

### Что важно заметить

Security-sensitive behavior, unusual design, or meaningful changes.

### Перед Trust

State what the user should specifically verify before trusting it.

Do not make the trust decision for the user.
Provide enough concrete information for the user to make that decision.
