# Vocabulary

These definitions are intentionally narrow. They describe how terms are used in this repository.

## Admission

A governed decision that a discovered resource may participate in a managed capability.

Existence does not imply admission.

## Authority boundary

A structural restriction defining which component or actor may make a class of decision or perform a mutation.

A boundary should be enforceable through interfaces, permissions, contracts, or automated conformance tests.

## Canonical state

The committed source of truth from which downstream policy and execution are derived.

Canonical does not mean infallible. It means authoritative within the system's operating model.

## Commit authority

The sole component permitted to convert a valid proposal into canonical governance state.

## Confidence-bearing knowledge

A value stored with its source, confidence, and conflict status so inferred information is not confused with authoritative fact.

## Control plane

Software that governs desired state and causes another system to converge toward it through explicit policy, authority, observation, and reconciliation.

An administration page or collection of scripts is not automatically a control plane.

## Decision metadata

The attributable context of a governance action: actor, reason, time, route or policy, and relevant evidence.

## Desired state

The state the managed system should converge toward after canonical intent has been evaluated by policy.

## Discovery

Observation of resources or facts from an upstream authority. Discovery may update owned facts or create proposals; it does not grant admission by itself.

## Draft state

Mutable proposal state that has not passed the canonical commit gate and must not cause managed-resource side effects.

## Drift

A meaningful difference between effective desired state and observed managed-resource state.

Unknown or unreadable observation is not ordinary drift; it is an evidence failure.

## Effective state

The valid operating result derived from requested intent plus policy constraints, lifecycle, approval, exclusions, and evidence quality.

## Fail closed

Refuse a privileged action when required evidence is missing, malformed, stale, conflicting, or unreadable.

The refusal should be classified, visible, and recoverable.

## Field ownership

The rule assigning each mutable field or field group to the component permitted to write it.

## Healer

A bounded recovery component that re-drives an interrupted committed flow or restores known prior state without acquiring new decision authority.

## Idempotency

The property that reapplying an operation after convergence produces no additional side effect.

## Observed state

The state currently reported by the managed system or external source. It may be stale, incomplete, or unavailable.

## Promotion

The validated, attributable transition from draft proposal to canonical state.

## Proposal

A candidate governance change that remains reversible and non-authoritative until committed.

## Provenance

The recorded origin and rationale of a fact, proposal, decision, restoration, or mutation.

## Reconciliation

Comparison of effective desired state with observed state, followed by bounded idempotent actions that move the managed system toward convergence.

## Recovery re-entry

The rule that retry and healing paths must pass through the same validation, commit, and execution authorities as ordinary work.

## Sole writer

The one logical authority permitted to mutate a particular canonical state or external resource class. It may be implemented by multiple runtime instances behind concurrency control.

## Staging

The storage area for proposals, classifications, and readiness metadata that are not yet canonical.
