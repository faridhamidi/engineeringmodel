# Governed Automation Adoption Check

Use this check before introducing staged truth, commit authorities, policy-derived activation, reconciliation, or governed recovery.

## Gate 1 — consequential external effect

Does the system create, change, disable, delete, admit, expose, or grant access to shared or external resources?

- **No:** remain in the Core Hygiene Layer.
- **Yes:** continue.

A local report, cache, generated file, or easily regenerated personal artifact does not normally satisfy this gate.

## Gate 2 — durable authority

Does the system encode a decision such as approval, entitlement, admission, lifecycle state, policy applicability, or another judgment that must remain attributable?

## Gate 3 — material blast radius

Can one incorrect, stale, or overly permissive default affect multiple resources, accounts, users, services, or compliance obligations?

## Gate 4 — evidence-sensitive action

Could missing, stale, malformed, conflicting, or unreadable evidence accidentally authorize a privileged or destructive action?

## Gate 5 — governed recovery

Could retry, repair, restoration, or offboarding bypass the authority or evidence required by the normal path?

## Decision

Adopt the **complete governed-automation layer** when Gate 1 is **Yes** and at least one of Gates 2–5 is also **Yes**.

Adopt **selected models only** when Gate 1 is Yes but the effect is narrow, reversible, and has no durable governance meaning. Examples include idempotency, a single mutation owner, or observe-before-repair without a staging system.

Use **core hygiene only** when the system transforms local data, generates replaceable artifacts, or performs a direct low-risk operation whose failure can be corrected by rerunning it.

## Stop signals

Do not add the full authority model when most of these are true:

- one operator owns the task;
- the operation affects one local or replaceable artifact;
- there is no approval or admission decision;
- the direct action is already the authoritative intent;
- failure is visible and a rerun is sufficient;
- a staging layer would duplicate state without creating a review boundary;
- recovery requires no privilege beyond the original operation.

## Record the result

A product repository adopting this layer should record:

```text
External effect:
Durable decision:
Blast radius:
Evidence failure risk:
Recovery bypass risk:
Adoption: core only | selected models | complete governed layer
Models selected:
Models explicitly rejected:
```

Revisit the result when the system gains new actors, broader mutation scope, approvals, asynchronous recovery, or shared-state ownership.
