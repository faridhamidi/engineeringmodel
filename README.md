# Engineering Models

Reusable engineering models extracted from operational software that had to make decisions, preserve authority boundaries, recover from partial failure, and remain understandable after launch.

This repository is not a framework, a maturity model, or a claim of novelty. It records what was built, what properties made it trustworthy, what evidence exists, and where the conclusions stop.

## Current synthesis

The current edition is grounded primarily in two deployed internal systems:

- a governance control plane for centralized cloud monitoring;
- a real-time operational status and reporting platform.

The first contributes the strongest material in this edition. Its core problem was not creating cloud links. It was deciding when automation may exercise organizational authority, preserving who decided what, and ensuring that recovery cannot bypass the original safety gates.

The central model is:

```text
discover facts
    -> stage a proposal
    -> validate against a contract
    -> commit through one authority
    -> derive effective desired state
    -> reconcile the managed system
    -> observe outcomes and drift
    -> recover through the same gates
```

Each arrow is an authority boundary, not merely a function call.

## Files

- [`PRINCIPLES.md`](PRINCIPLES.md) — positions that govern the material.
- [`AUTOMATED_AUTHORITY.md`](AUTOMATED_AUTHORITY.md) — the main synthesis: how to constrain automation that acts at scale.
- [`MODELS.md`](MODELS.md) — reusable state, policy, reconciliation, and recovery models.
- [`TESTING.md`](TESTING.md) — a falsification-first testing taxonomy and architecture-conformance approach.
- [`DOCUMENTATION.md`](DOCUMENTATION.md) — a lifecycle for forward direction, implementation plans, and durable decisions.
- [`VOCABULARY.md`](VOCABULARY.md) — intentionally narrow terminology.
- [`CASE_STUDIES.md`](CASE_STUDIES.md) — sanitized observations from the source systems.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — evidence, writing, and confidentiality rules.

## Reading rule

Treat every statement as bounded by its evidence.

A deployed system can still be young. A clean production history does not prove that all failure modes were exercised. A useful domain-specific control plane is not automatically a general orchestration framework. A comprehensive test suite does not create mathematical proof. Good terminology describes implemented properties; it does not upgrade them.

## What this repository deliberately avoids

- renaming ordinary automation to make it sound strategic;
- copying Kubernetes, Crossplane, SRE, or platform-engineering ceremony without the corresponding need;
- claiming multi-cloud portability because interfaces exist;
- presenting vendor independence as an objective in itself;
- measuring engineering quality by tool count;
- treating documentation volume as evidence of correctness.

The useful question is always narrower: **what decision is being made, what invariant is protected, what authority is exercised, and what evidence shows the design holds?**
