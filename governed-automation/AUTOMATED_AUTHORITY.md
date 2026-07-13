# Automated Authority

## Problem

Automation often begins as a convenience: discover resources, update records, and call an API. At organizational scale, the same automation begins exercising authority. A small incorrect decision can then be multiplied across an estate.

The engineering problem becomes:

> How can a machine act repeatedly and quickly without silently acquiring the authority to decide what should be true?

## Model

Split the workflow into seven powers.

### 1. Discover

Read facts from an upstream authority.

Examples include account lifecycle, identity, tags, inventory, or current managed-resource state.

Discovery may refresh fields it owns. It may create a proposal. It may not convert existence into admission.

### 2. Propose

Create mutable draft state representing a possible decision.

The proposal may originate from an operator or from a narrow system policy. It remains non-authoritative until promoted.

### 3. Validate

Evaluate the proposal against a versioned contract:

- required fields;
- allowed values;
- field ownership;
- transition rules;
- evidence freshness;
- concurrency token;
- prohibited combinations.

Reject unknown fields rather than carrying them silently.

### 4. Commit

Use one designated authority to write canonical state atomically.

The commit gate records the decision and its provenance. It does not directly mutate the managed resource.

### 5. Derive

Compute effective desired state from canonical intent and current policy.

For example:

```text
requested enablement
+ active lifecycle
+ appropriate approval
+ resolved classification
+ valid evidence
- explicit exclusions
= effective enablement
```

The result should be derived, not manually maintained as another mutable truth.

### 6. Execute

Use one designated reconciler to compare effective desired state with observed resource state and apply idempotent corrections.

The reconciler does not decide policy. It executes policy already committed elsewhere.

### 7. Recover

Detect interrupted or inconsistent flows and re-drive them through the same gates.

Recovery may restore a known snapshot or retry a committed decision. It must not infer a more permissive decision from failure.

## Authority matrix

| Capability | Discovery | Operator UI | Commit authority | Reconciler | Recovery |
|---|---:|---:|---:|---:|---:|
| Refresh externally owned facts | Yes | No | No | No | No |
| Edit draft proposal | Limited | Yes | No | No | Limited |
| Write canonical decision | No | No | Yes | No | Restore-only, bounded |
| Derive effective state | Advisory only | Advisory only | Validate | Yes | No |
| Mutate managed resource | No | No | No | Yes | No |
| Invent new governance authority | No | No | No | No | No |

The matrix should be enforced in code and tests. A table alone does not create a boundary.

## Core invariants

1. Discovery cannot enable a governed capability merely by finding a resource.
2. Draft state cannot cause downstream mutation.
3. Only the commit authority can create or change canonical governance state.
4. Only the reconciler can mutate the managed resource.
5. Effective state is derived from canonical data and policy.
6. Missing or conflicting evidence produces the safe non-acting state.
7. Human decisions are not silently overwritten by weaker machine inference.
8. Recovery reuses normal authority gates.
9. Every mutation is attributable to a canonical decision.
10. Reapplying an already converged operation is a no-op.

## Why this is not merely a workflow

A workflow describes order. An authority model describes who may exercise each power, which evidence is required, and which bypasses are forbidden.

The distinction matters during failure. A workflow engine may happily resume at the next step. An authority-aware system must establish whether the next step is still permitted.

## When to use this model

Use it when automation:

- affects many resources;
- changes access, monitoring, security, lifecycle, or compliance state;
- acts on behalf of operators or governance bodies;
- must preserve human approval;
- must be auditable and recoverable;
- can cause broad damage through one incorrect default.

## When not to use it

Do not build this machinery for a small, reversible, low-risk task with one owner and no durable governance decision.

A script with explicit input, dry-run output, idempotency, and clear ownership may be enough. The model should reduce risk, not manufacture architecture.
