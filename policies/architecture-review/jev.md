# Architecture Review Jev Choice Policy v1

Use only the structured graph delta and explicit rules in state. Graphify reports what exists and changed; you decide only whether bounded structural and policy conditions apply. Do not invent project rules or infer a source-level violation from generic SOLID/Clean Architecture advice. A new import cycle may be a structural concern without a policy violation. A god node or cross-community edge alone is not failure. However, a new cross-community edge cannot be called CLEAN unless the state also supplies reliable context showing that boundary crossing is expected; without such context choose UNCERTAIN. Existing conditions before the baseline are not new changes. `reliable_policy_evidence` is the authoritative list where both the explicit policy rule and its matching EXTRACTED new edge were verified against cited project source. Never choose VIOLATED when that list is empty. INFERRED or AMBIGUOUS evidence never appears in that list and cannot establish VIOLATED. Confidence and probabilities are telemetry, never custom thresholds. Incomplete evidence means UNCERTAIN.

## structural_assessment

Instructions: Classify the material structural delta relative to the supplied baseline, not the absolute state of the project.

### CLEAN
The structural delta is consistent with the existing architecture and contains no material new architectural concern in the supplied evidence. No change is CLEAN.

### CONCERN
The delta introduces a material structural change deserving explicit review, such as a new import cycle, unexpected boundary crossing, significant coupling increase, new architectural hub, unexpectedly large blast radius, or disproportionate growth. A new cycle is a concern even without a policy.

### UNCERTAIN
The graph evidence is incomplete, ambiguous, inferred, or insufficient to classify reliably. This includes a new cross-community edge when no reliable context says whether that boundary crossing is expected.

## policy_compliance

Instructions: Apply only explicit project architecture rules supplied in state and relevant to this delta. Do not turn structural smells into policy violations.

### COMPLIANT
Explicit project architecture rules are applicable and reliable structural evidence shows that this delta conforms to them.

### VIOLATED
An explicit project architecture rule is applicable and `reliable_policy_evidence` contains a matching source-verified EXTRACTED edge showing the delta violates it. This choice is forbidden when `reliable_policy_evidence` is empty.

### NOT_APPLICABLE
No explicit project architecture rule applies to this delta, or the project has no explicit architecture policy.

### UNCERTAIN
A relevant explicit policy may apply, but `reliable_policy_evidence` is empty or the supplied evidence is otherwise insufficient to decide reliably.
