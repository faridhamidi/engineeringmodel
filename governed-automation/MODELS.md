# Governed Automation Models

Select models by trigger. Do not copy the complete set as a starter template.

| Symptom | Consider |
|---|---|
| Observed facts, human intent, and real effects can diverge | Fact, decision, and effect separation |
| An edit must be reviewed before becoming authoritative | Draft-to-canonical promotion |
| Requested intent can be blocked by current policy | Derived effective state |
| Multiple components can perform the same consequential write | Sole-writer authority |
| Shared resources can drift from valid policy | Policy-driven reconciliation |
| Operators need a safe exceptional repair path | Observe-then-repair |
| Retry or restoration could bypass normal controls | Recovery without privilege escalation |
| Inference must not be confused with authoritative fact | Confidence-bearing knowledge |
| Delivered output must be reproducible from one committed state | Committed snapshot delivery |

## 1. Fact, decision, and effect separation

**Trigger:** one record mixes externally observed facts, human decisions, machine recommendations, and real-world effects.

**Mechanism:** separate observed facts, governance intent, derived effective state, and observed external effect. Assign write ownership to each group.

**Invariant:** refreshing facts cannot change intent; governance edits cannot rewrite externally owned facts; observed effect is not mistaken for desired state.

**Skip when:** the states cannot legitimately diverge.

## 2. Draft-to-canonical promotion

**Trigger:** a proposal may be incomplete, reviewed, rejected, or corrected before it becomes authoritative.

**Mechanism:** write proposals to a reversible workspace, validate them, and promote through one atomic commitment path. Downstream execution reads committed state only.

**Invariant:** draft changes cause no external side effect; stale proposals cannot overwrite newer truth; commitment preserves fields outside the proposal’s ownership.

**Skip when:** one low-risk direct write with validation is already the authoritative intent.

## 3. Derived effective state

**Trigger:** requested intent may remain valid while lifecycle, approval, evidence, or policy prevents current execution.

**Mechanism:** retain requested intent and derive the effective result through a deterministic policy function that returns a classified reason.

**Invariant:** equal inputs produce equal results; missing required evidence produces a safe outcome; presentation labels are not policy inputs.

**Skip when:** stored state is already direct, authoritative, and unconstrained.

## 4. Sole-writer authority

**Trigger:** multiple components can write the same authoritative state or perform the same consequential external mutation.

**Mechanism:** designate one logical writer per state or resource class and require all callers to cross the same narrow seam. Multiple runtime instances may sit behind concurrency control.

**Invariant:** no production path bypasses the writer; policy remains independent of provider clients; conflicting writers cannot silently win.

**Skip when:** components own disjoint fields or effects and cannot conflict.

## 5. Policy-driven reconciliation

**Trigger:** a managed system can drift from valid committed intent as resources appear, close, change, or fail midway through mutation.

**Mechanism:** read committed state, derive desired state, observe the managed resource, classify the difference, and apply bounded idempotent corrections.

**Invariant:** reconciliation executes policy but does not originate it; repeated execution converges; unknown observation does not authorize mutation.

**Skip when:** there is no durable desired state or no meaningful drift.

## 6. Observe-then-repair

**Trigger:** a manual repair action could become a privileged bypass or act on incomplete evidence.

**Mechanism:** separate a read-only difference operation from mutation. Block repair when observation is incomplete and route approved repair through the normal mutation owner.

**Invariant:** the operator can see what will change and why; exceptional repair does not create a second execution authority.

**Skip when:** the operation is local, reversible, and ordinary retry is sufficient.

## 7. Recovery without privilege escalation

**Trigger:** retry, restoration, offboarding, or healing might bypass the controls required by the primary path.

**Mechanism:** re-drive an existing committed decision, restore a known version, or escalate when proof is insufficient. Reuse the normal validation and mutation boundaries.

**Invariant:** recovery cannot create approval, turn unknown state into enabled state, or hide recursive failure.

**Skip when:** recovery has exactly the same narrow effect as an ordinary rerun and carries no additional privilege.

## 8. Confidence-bearing knowledge

**Trigger:** inferred data can be confused with authoritative observation or human judgment.

**Mechanism:** store value, source, and conflict status separately. Add confidence only when its semantics are defined and testable.

**Invariant:** weaker evidence cannot silently replace stronger evidence; uncertainty remains visible; confidence does not authorize a governed action.

**Skip when:** every value has one unambiguous authoritative source.

## 9. Committed snapshot delivery

**Trigger:** reports or artifacts generated from mutable live state must remain reproducible across delivery retries.

**Mechanism:** commit source state, create an immutable snapshot, render outputs from that snapshot, and persist delivery progress against it.

**Invariant:** every delivered artifact is attributable to one committed state even if live state changes later.

**Skip when:** output is disposable, local, and cheap to regenerate without accountability requirements.
