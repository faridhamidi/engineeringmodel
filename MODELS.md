# Models

## 1. Fact, decision, and effect are separate state axes

### Problem

A single record often mixes externally observed facts, human decisions, machine recommendations, and real-world effects. Broad updates then overwrite information outside the caller's authority.

### Model

Separate at least four axes:

- **observed facts** — identity, lifecycle, tags, timestamps;
- **governance intent** — approval, requested enablement, operator rationale;
- **derived effective state** — policy result;
- **observed effect** — what exists in the managed system.

Assign write ownership per field group.

### Invariants

- fact refresh does not change governance intent;
- governance edits do not rewrite externally owned facts;
- derived state is reproducible from source inputs;
- observed effect is not mistaken for desired state.

### Boundary

This separation creates more states to reason about. It is justified only where those states can legitimately diverge.

## 2. Draft-to-canonical promotion

### Problem

Direct writes from an interface combine editing, validation, commitment, and side effects. Partial or invalid work can become authoritative too early.

### Model

- write proposed records to staging;
- expose validation and readiness state;
- promote through one atomic commit authority;
- remove staging data only after successful commitment;
- trigger downstream execution from canonical changes, not draft edits.

### Invariants

- staging is never an execution source;
- canonical records satisfy the complete contract;
- promotion preserves fields outside the proposal's ownership;
- concurrent stale proposals cannot silently overwrite newer truth.

### Boundary

For low-risk single-user configuration, a full staging layer may be excessive. A transactional preview-and-commit operation can provide similar protection.

## 3. Derived effective state

### Problem

Raw intent may be disallowed by current policy. Storing only one boolean loses either the request or the reason it is inactive.

### Model

Retain requested intent and derive effective state through a pure policy function.

```text
effective_state = policy(canonical_intent, lifecycle, classification, approval, exclusions)
```

Return a classified reason, not only a boolean.

### Invariants

- the same inputs produce the same result;
- missing required input yields a safe classified outcome;
- policy does not mutate the canonical record;
- presentation labels do not become policy inputs.

### Boundary

Do not introduce a policy layer where direct state is already authoritative and unconstrained.

## 4. Sole-writer authority

### Problem

When multiple components can write the same authoritative state or mutate the same external resource, safety rules drift and incidents become difficult to attribute.

### Model

Designate:

- one canonical governance writer;
- one managed-resource mutator;
- explicit ports through which all callers must pass.

Use static architecture tests to reject raw adapter calls outside authorized modules.

### Invariants

- no production path bypasses the writer or reconciler;
- interfaces remain narrow;
- adapters contain substrate-specific operations;
- policy code remains independent of infrastructure clients.

### Boundary

A sole writer can become a bottleneck or single failure domain. The model governs authority, not deployment topology; the writer can be replicated behind concurrency control.

## 5. Policy-driven reconciliation

### Problem

The managed system drifts from valid organizational state as resources appear, close, change classification, or fail midway through mutation.

### Model

1. read canonical state;
2. derive effective desired state;
3. observe actual managed-resource state;
4. classify missing, stale, matching, and unknown conditions;
5. block mutation if observation is incomplete;
6. apply idempotent create or delete operations;
7. record results and unresolved errors.

### Invariants

- reconciliation never originates policy;
- repeated execution converges rather than duplicates;
- one failing resource does not corrupt unrelated decisions;
- deletion requires the same level of evidence as creation;
- ambiguous observation does not authorize repair.

### Boundary

This is a domain-specific reconciliation model. It is not a replacement for a general infrastructure orchestration ecosystem.

## 6. Observe-then-repair

### Problem

A repair button can become a privileged bypass that hides the state on which mutation is based.

### Model

Split manual remediation into two explicit operations:

- **diff** — read-only comparison of desired and observed state;
- **repair** — reconciler invocation after explicit confirmation and operator reason.

Block repair when the observation path reports fatal or incomplete reads.

### Invariant

The operator can see what will change and why before mutation begins, and the mutation still occurs through the normal execution authority.

### Boundary

This does not eliminate the need for automated reconciliation. It is an operator safety path for exceptional or supervised action.

## 7. Recovery without privilege escalation

### Problem

Retries and healers are often granted broad access so they can "fix anything." They then become less governed than the primary workflow.

### Model

Define bounded recovery levels:

- re-drive an existing ready proposal;
- restore a previously committed generation or snapshot;
- escalate to an operator when proof is insufficient.

Recovery must preserve the original decision metadata and use the normal commit or reconcile ports.

### Invariants

- recovery cannot create a new approval;
- recovery cannot turn unknown state into enabled state;
- restored state is attributable to a known version;
- repeated recovery is safe;
- failed recovery becomes visible rather than recursive.

### Boundary

Some destructive incidents require break-glass procedures. Those should be separately authorized and audited rather than disguised as normal healing.

## 8. Confidence-bearing knowledge

### Problem

Inferred values are often stored as though they were authoritative. Later automation cannot distinguish observation, inference, and human judgment.

### Model

Store value, source, confidence, and conflict flags separately. Permit automatic "ripening" only toward stronger evidence and only where it cannot overwrite a sovereign human or authoritative external value.

### Invariants

- weaker evidence cannot silently replace stronger evidence;
- conflicting authoritative signals remain unresolved and visible;
- uncertainty is a valid state;
- confidence metadata does not itself authorize a governed action.

### Boundary

Confidence fields are useful only when their semantics are defined. Decorative percentages create false precision.

## 9. Committed snapshot delivery

### Problem

Reports generated from live mutable state can combine different moments and become impossible to reproduce.

### Model

Commit state, create an immutable snapshot, render all outputs from that snapshot, persist delivery progress, and retry from the accountable record.

### Invariant

Every delivered artifact is attributable to one committed state even if live state changes afterward.

### Boundary

Consistency does not guarantee correctness; incorrect input can be captured consistently.
