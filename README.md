<p align="center">
  <img src="docs/assets/engineering-model-governance-harness.jpg" alt="Engineering Models — governed automation harness" width="100%">
</p>

# Engineering Models

Reusable engineering tradecraft extracted from operational software, organized by adoption cost and problem scope.

> **Default path: use Core Hygiene and stop there.**
>
> For most application repositories, Core Hygiene is the complete adoption: clear boundaries, declared semantics, traceable operations, focused tests, and maintainable documentation.
>
> **Governed Automation is deliberately exceptional.** It is for systems that exercise consequential authority over shared or external state. It is not a maturity level, an advanced architecture tier, or the expected destination for an ordinary application.

This repository is a governing seed, not a framework or mandatory starter template. Its central rule is mechanical proportionality: add only the machinery justified by the failure mode and authority involved.

## Choose the layer in 30 seconds

1. **Does the system create, change, disable, delete, admit, expose, or grant access to shared or external resources?**
   - **No:** remain in [`Core Hygiene`](core/README.md).
   - **Yes:** continue.
2. **Does it also carry durable authority, material blast radius, evidence-sensitive action, or recovery that could bypass the normal authority path?**
   - **No:** remain in Core Hygiene. Select an isolated low-cost pattern only where it solves a concrete risk.
   - **Yes:** complete the [`Governed Automation Adoption Check`](governed-automation/ADOPTION_CHECK.md) before selecting governed models.

**When uncertain, remain in Core Hygiene. The burden of proof belongs to the additional machinery.**

## Core Hygiene — the normal path

Start with [`core/README.md`](core/README.md). Core Hygiene keeps three properties visible:

1. **Boundaries** — decisions and external effects have clear owners and testable seams.
2. **Semantics** — important states, actions, outcomes, and reasons are declared when repetition makes them load-bearing.
3. **Traceability** — one operation can be followed across remote or asynchronous hops.

It also provides proportionate testing and documentation guidance. It does not require architectural branding, a prescribed directory tree, staged truth, approval machinery, reconciliation, dedicated recovery components, or a governance vocabulary.

The fact that software is an API, service, worker, CLI, internal tool, data pipeline, AI-assisted workflow, distributed system, or production application does **not** by itself justify Governed Automation.

Repositories with several stable, cross-cutting structural constraints may optionally escalate direct tests into a [`Repository Conformance Harness`](core/CONFORMANCE_HARNESS.md). That remains a Core Hygiene mechanism, not a third adoption layer.

## Governed Automation — the exception path

Consider [`governed-automation/`](governed-automation/README.md) only after the need gate is crossed.

The complete layer is a candidate when:

- the system performs a consequential shared or external effect; **and**
- at least one additional authority risk exists:
  - a durable approval, entitlement, admission, policy, or lifecycle decision;
  - material blast radius;
  - evidence whose absence or corruption could authorize an unsafe action;
  - recovery that could bypass normal authority.

Even then, adoption is not automatic. Technical identities must be able to enforce the separation, and the reduction in consequential risk must exceed the added coordination, operational, and cognitive cost.

Do not adopt the complete layer merely because a system is important, complex, distributed, asynchronous, AI-assisted, or deployed to production.

## Repository map

```text
core/                    normal starting point for application repositories
governed-automation/     gated exception for authority-bearing systems
case-studies/             evidence-tagged adoption and non-adoption cases
examples/                 dependency-free executable witnesses
.github/workflows/        CI for the executable witnesses
AGENTS.md                 concise contributor and agent navigation
CONTRIBUTING.md           evidence, ownership, writing, and confidentiality rules
```

The examples are deliberately small. They prove selected constraints can be enforced; they are not production templates or claims that Python is the preferred implementation language.

## How product repositories use this seed

1. Adopt the Core Hygiene questions and only the checks that protect real seams.
2. Use the smallest direct test, ratchet, or local convention that controls the identified risk.
3. Stop there unless the system crosses the consequential-authority gate.
4. If it does, complete the adoption and cost check and select only the governed models whose triggers are present.
5. Keep product contracts, runbooks, decisions, and local rule sets in the product repository.
6. Contribute a reusable lesson here only after implementation or operational evidence exists.

**For most repositories, steps 1–3 are the complete adoption.** Using less machinery is the correct result when the authority risk is absent.

Do not copy every file mechanically. The objective is to prevent specific ambiguity and failure modes, not to reproduce this repository's shape.

## Governed document ownership

This section matters only after the governed-automation gate has been crossed.

- [`MODELS.md`](governed-automation/MODELS.md) is the canonical source for each model's trigger, mechanism, invariant, cost, security implications, and skip condition.
- [`DECISION_TREE.md`](governed-automation/DECISION_TREE.md) is a trigger-based projection into the model catalog.
- [`VOCABULARY.md`](governed-automation/VOCABULARY.md) provides short definitions and links to canonical entries.
- [`PRINCIPLES.md`](governed-automation/PRINCIPLES.md) contains only cross-cutting positions.
- [`AUTOMATED_AUTHORITY.md`](governed-automation/AUTOMATED_AUTHORITY.md) describes how the seven powers compose.

## Evidence boundary

A deployed system can still be young. Strong tests improve confidence but do not prove correctness. A lesson observed in one system remains a bounded inference until repeated elsewhere.

The documented cases currently come from operational tooling and infrastructure-adjacent systems. The models have not yet been validated here through documented cases in financial transaction processing, regulated data pipelines, ML training or deployment governance, healthcare, identity systems, or non-technical human approval workflows. Those remain open evidence boundaries, not implied coverage.
