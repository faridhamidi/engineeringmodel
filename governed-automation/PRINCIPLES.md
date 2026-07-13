# Principles

## Begin with the governed decision

Do not begin with labels such as control plane, SRE, platform, or agent. Begin with the decision that must be made repeatedly and the consequence of making it incorrectly.

Creating a cloud relationship may be technically simple. Deciding whether that relationship is permitted, attributable, reversible, and still valid is a different problem.

## Discovery is not admission

Finding a resource proves that it exists. It does not prove that the resource should be governed, monitored, exposed, deleted, or modified.

Discovery should update facts or create a proposal. It should not silently become permission.

## Separate proposal, commitment, and execution

A human interface may propose a change. A policy engine may evaluate it. A designated authority may commit it. A reconciler may execute it.

Collapsing these powers into one component makes bypasses easy and failures difficult to attribute.

## Make field ownership explicit

Every mutable field should have a named owner. Prefer write allowlists over broad object replacement followed by filtering.

Facts discovered from an external authority, human governance decisions, derived state, recovery metadata, and presentation fields should not share an undifferentiated mutation path.

## Stage before making truth

Draft state is cheap and reversible. Canonical state is deliberate and guarded.

A proposal workspace permits review, correction, and classification without causing downstream side effects. Downstream systems must not treat staging as authoritative.

## Derive effective state

Requested intent is not necessarily valid operating state.

Effective state should be derived from intent plus policy, lifecycle, approvals, evidence freshness, and exclusions. Do not overwrite intent merely because policy currently prevents execution; retaining both explains what was requested and why it is not active.

## Give each irreversible effect one authority

One component should own canonical governance commits. One component should own mutation of the managed system.

A sole-writer rule is useful only when it is enforced structurally and tested against bypass, not merely described in documentation.

## Fail closed under uncertainty

Incomplete, stale, malformed, conflicting, or unreadable evidence must not authorize a privileged action.

Fail-closed behavior must produce an observable reason and a recovery path. Silent refusal is not sufficient operational design.

## Observe before repair

A repair workflow should first present the difference between desired and observed state. Mutation should be blocked when observation is incomplete or unreliable.

Manual repair should still pass through the normal reconciler and should carry an operator reason.

## Recovery must not gain authority

A healer or retry mechanism may re-drive an interrupted operation or restore a known prior state. It must not invent a new governance decision or bypass validation because the primary path failed.

Recovery should re-enter the same commit and execution gates as normal work.

## Preserve provenance as operational data

Who decided, why, when, under which rule, and from which evidence are part of the system state.

A decision whose rationale is lost will eventually be repeated incorrectly.

## Test beliefs, invariants, and boundaries

A test suite should attempt to falsify safety claims, protect previously broken behavior, and lock architectural seams that must not be bypassed.

Testing rigor is not ceremony. It is the ability to state what must never happen and provide evidence that the implementation rejects it.

## Establish legibility early

A small codebase is the cheapest place to preserve boundaries, declare shared vocabulary, and propagate operation context.

Use the lightest mechanism that works. The objective is not to impose a named architecture; it is to prevent external effects, system decisions, and cross-hop execution from becoming indistinguishable as the code grows.

## Earn abstraction from repetition

Declare an interface, registry, state machine, or tracing layer when a concrete dependency, repeated rule, or diagnostic gap justifies it.

Do not pre-build a complete architecture. Create a narrow seam early, enforce it, and deepen it only after the system demonstrates the need.

## Keep claims smaller than the system

A domain-specific control plane can be serious without being equivalent to Kubernetes or Crossplane. Interfaces can reduce coupling without proving actual multi-cloud support. Strong tests can improve confidence without proving correctness.

Precise limits make the achievement more credible, not less.