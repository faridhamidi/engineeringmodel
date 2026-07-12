# Engineering Models

Reusable engineering tradecraft extracted from operational software: how to preserve decision boundaries, constrain automated authority, recover from partial failure, and keep systems understandable after launch.

This repository is a governing seed for future product repositories. It is not a framework, a mandatory directory structure, a maturity model, or a claim of novelty.

## Governing idea

Build the smallest foundation that keeps three things visible from the beginning:

1. **Boundaries** — decision logic and external effects have named owners and testable seams.
2. **Semantics** — important states, actions, outcomes, and reasons are declared rather than scattered through conditionals.
3. **Traceability** — one operation can be followed across every remote or asynchronous hop.

These are steering constraints, not architectural branding. A repository does not need to call itself hexagonal, clean, layered, or a control plane. It only needs enough structure that authority, behavior, and execution remain legible.

See [`FOUNDATION.md`](FOUNDATION.md) for the starting constraint.

## Main operational model

For automation that makes governed changes, the central flow is:

```text
discover facts
    -> stage a proposal
    -> validate against a contract
    -> commit through one authority
    -> derive effective desired state
    -> execute through one mutation path
    -> observe outcomes and drift
    -> recover through the same gates
```

Each arrow may represent an authority boundary, not merely a function call.

## How future repositories use this seed

A product repository should adopt only the parts its problem requires:

- begin with the foundation questions;
- record the boundaries and vocabulary that matter locally;
- add tests that prevent important seams from being bypassed;
- keep product-specific contracts, runbooks, and decisions in the product repository;
- contribute validated, reusable lessons back here after they have survived implementation and operation.

Do not copy every file mechanically. Reference the canonical material and document local adoption or deviation.

## Files

- [`FOUNDATION.md`](FOUNDATION.md) — low-cost starting constraints for boundaries, semantics, and traceability.
- [`PRINCIPLES.md`](PRINCIPLES.md) — positions governing the material.
- [`AUTOMATED_AUTHORITY.md`](AUTOMATED_AUTHORITY.md) — how to constrain automation that acts at scale.
- [`MODELS.md`](MODELS.md) — reusable state, policy, reconciliation, recovery, and codebase-legibility models.
- [`TESTING.md`](TESTING.md) — falsification-first testing and structural conformance.
- [`DOCUMENTATION.md`](DOCUMENTATION.md) — lifecycle for direction, implementation plans, and durable decisions.
- [`VOCABULARY.md`](VOCABULARY.md) — narrow terminology.
- [`CASE_STUDIES.md`](CASE_STUDIES.md) — sanitized observations from source systems.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — evidence, writing, extraction, and confidentiality rules.

## Evidence rule

Treat every statement as bounded by its evidence.

A useful internal system is not automatically a general platform. Interfaces do not prove portability. Strong tests improve confidence but do not prove correctness. Architectural vocabulary is useful only when it describes properties that the implementation actually has.