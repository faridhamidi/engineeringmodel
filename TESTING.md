# Testing

## Purpose

The testing model extracted here is not "write many tests." It is a method for making safety claims explicit and trying to disprove them.

A test is classified on three independent axes.

## Axis A — Intent

### Falsification

State a belief that must not hold, then construct inputs that would expose it.

Examples:

- discovery can accidentally change approval;
- a missing policy input can still enable a resource;
- a stale writer can overwrite a newer generation;
- an unauthorized module can call the storage adapter directly.

This is the default for safety-sensitive logic.

### Regression

Pin a specific defect so the old behavior cannot return.

A regression test is a falsification test with a known historical hypothesis: "the previous bug is back."

### Confirmation

Demonstrate an intended happy path. This is valid for wiring, presentation, and ordinary flows, but it should not be the only evidence for a critical decision rule.

## Axis B — Target

### Decision-table oracle

Encode the authoritative input-to-outcome mapping independently of the implementation. Test the implementation against the table.

Use this for finite policy decisions with classified results.

### Invariant

Assert a property that must survive many operations:

- **conservation** — one authority cannot alter another authority's fields;
- **determinism** — equal inputs produce equal outputs;
- **idempotency** — reapplying converged work is a no-op;
- **fail-closed behavior** — missing or ambiguous evidence produces no privileged action.

Test the invariant helper itself with known-bad data. An assertion that cannot fail creates false confidence.

### Contract and schema

Test both sides:

- valid records are accepted;
- missing, malformed, and unknown fields are rejected.

Pair every allowlist acceptance test with a falsifier proving the boundary did not become permissive.

### Architecture boundary

Parse source or inspect imports and calls to prove that required seams are not bypassed.

Examples:

- only the repository adapter may use the raw database client;
- only the reconciler adapter may call the managed-resource API;
- pure policy modules may not import cloud SDKs, filesystem, subprocess, network, or environment access;
- presentation projections may be displayed but may not drive mutation decisions.

Architecture tests are executable constraints, not style preferences.

### Concurrency safety

Use a stateful model of the backing store to drive stale tokens and racing writers. Prove that optimistic concurrency rejects lost updates and preserves atomicity.

## Axis C — Input generation

Choose how the test obtains cases:

- single example;
- parametrized matrix;
- exhaustive finite cross-product;
- boundary values;
- fault injection;
- anomaly sequencing, such as failure at step N followed by retry.

Every external seam should have a fault-injection case. Every retry or recovery path should have at least one anomaly sequence.

## A complete test description

A useful review sentence names all three axes:

> A falsification test of the field-conservation invariant using an exhaustive cross-product of lifecycle, approval, and requested-state inputs.

This is more informative than calling something a unit test or integration test.

## Testing priorities for governed automation

1. Policy decisions and classified refusal reasons.
2. Field ownership and conservation.
3. Unknown-field and malformed-contract rejection.
4. Stale-write and concurrent-update behavior.
5. Idempotent reconciliation.
6. Partial observation and dependency failure.
7. Recovery that must not escalate authority.
8. Static bypass detection for protected adapters.
9. Regression tests for every escaped semantic defect.
10. Seeded bad examples proving that test oracles actually detect failure.

## What not to copy

Do not copy test counts, naming ceremonies, or coverage thresholds from a larger system without identifying the risk they control.

High branch coverage is especially useful for small pure decision modules. It is less meaningful as a universal repository score. Mutation testing, property-based testing, fuzzing, and load testing should be introduced when a specific blind spot warrants them, not as badges.

## Minimal template

```text
Intent:
Target:
Generation strategy:
Belief being challenged:
Invariant or oracle:
Known-bad case proving the oracle:
External seams and injected faults:
Evidence boundary:
```
