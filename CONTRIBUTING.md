# Contributing

This repository should preserve engineering reasoning, not advertise the author.

## Required structure

A new model or case study should state:

- the concrete operating context;
- the decision or state being governed;
- the actors and authority boundaries;
- the invariant;
- the mechanism;
- failure and recovery behavior;
- tests or operational evidence;
- limitations;
- what was deliberately not built.

## Claim classification

Mark important claims mentally or explicitly as one of:

- **implemented** — visible in production code;
- **tested** — protected by a named test or executable check;
- **deployed** — running in a real environment;
- **operationally used** — consumed by real operators or workflows;
- **proposed** — documented direction, not current behavior;
- **inferred** — a conclusion drawn from evidence but not directly measured.

Do not let a proposed design inherit the language of deployed behavior.

## Writing rules

Use plain technical language. Prefer "sole canonical writer" to "enterprise governance engine" and "exhaustive finite cross-product" to "advanced testing methodology."

Avoid:

- revolutionary;
- next-generation;
- enterprise-grade without defined evidence;
- production-ready without an operating record;
- best practice without context;
- zero-error or zero-downtime as unqualified objectives;
- cloud-agnostic when only one provider is implemented;
- AI-powered when a model is incidental to the value;
- comparisons to large frameworks without a strict statement of which property is shared.

## Evidence rule

Every broad conclusion should identify its basis:

- source behavior;
- test or invariant;
- deployment state;
- operational use;
- measured result;
- documented incident or defect.

Absence of incidents is evidence of stable operation, not proof that every risk was prevented.

## Architecture terminology rule

Use **control plane** only when the system contains authority, canonical desired state, policy derivation, observation, and a reconciliation or enforcement path.

Use **hexagonal architecture** only when ports isolate core decisions from adapters and bypasses are prevented or at least detectable.

Use **SRE** only for practices actually implemented, such as service objectives, error budgets, incident learning, or toil-reduction mechanisms. Reading SRE literature is not implementation.

## Confidentiality

Do not include employer names, account identifiers, internal domains, credentials, proprietary source, unapproved adoption metrics, or incident details that identify affected parties.

Sanitize the example while preserving the state model and decision.

## Revision rule

Corrections are more valuable than consistency with an earlier claim. When code or evidence changes, revise the model and retain the boundary. Do not defend wording that the implementation no longer supports.
