<p align="center">
  <img src="docs/assets/engineering-model-governance-harness.jpg" alt="Engineering Models — governed automation harness" width="100%">
</p>

# Engineering Models

Reusable engineering tradecraft extracted from operational software, organized by adoption cost and problem scope.

This repository is a governing seed: a source of reusable constraints, questions, and evidence-backed models, not a framework or mandatory starter template. Its central rule is mechanical proportionality: broadly useful hygiene is separated from specialized authority machinery, so a team does not have to infer the boundary from prose caveats.

## Repository map

```text
core/                    normal starting point for application repositories
governed-automation/     gated exception for authority-bearing systems
builders/                plain-language front door and safe-operation guidance
skills/                  reusable Agent Skills package for the methodology
case-studies/            evidence-tagged adoption and non-adoption cases
examples/                dependency-free executable witnesses
.github/workflows/       CI for the executable witnesses
AGENTS.md                concise contributor and agent navigation
CLAUDE.md                Claude-native always-on steering surface
CONTRIBUTING.md          evidence, ownership, writing, and confidentiality rules
```

Examples demonstrate individual constraints, mechanisms, and models in isolation, while case studies record bounded evidence about adoption and non-adoption. Neither constitutes a starter template, architectural prescription, or automatic precedent for another repository.

## Builder access

Start with [`builders/START_HERE.md`](builders/START_HERE.md) when directing work
through an AI agent without needing the methodology's engineering vocabulary. Before
publishing, deploying, applying, granting, deleting, or sending anything outside the
local workspace, follow [`builders/SAFE_OPERATION.md`](builders/SAFE_OPERATION.md).

The reusable [`engineering-model` skill](skills/engineering-model/SKILL.md) carries the
same engine for on-demand agent use. Its always-on steering must also be installed in
the runtime's native instruction surface; this repository exercises both `AGENTS.md`
and `CLAUDE.md` forms.

Git supplies the local save points required by this builder layer. Install and verify
it using [`builders/GIT_SETUP.md`](builders/GIT_SETUP.md), then initialize the project
with `git init` when it is not already a repository. Git can restore authoring changes;
it cannot reverse an effect already applied to an external system.

## Choose your layer

**Default path: Core Hygiene. Stop there unless the gate below says otherwise.**

1. Does the system create, change, disable, delete, admit, expose, or grant access to shared or external resources? A local report, cache, generated file, or easily regenerated personal artifact does not normally satisfy this gate.
   - **No** → stay in [Core Hygiene](core/README.md).
   - **Yes** → continue.
2. Does it also encode durable authority — such as approval, entitlement, admission, or lifecycle state — or involve material blast radius, evidence-sensitive action, or recovery that could bypass the normal authority path?
   - **No** → stay in Core Hygiene. Adopt an isolated low-cost pattern only where it solves a concrete risk.
   - **Yes** → complete the [Governed Automation Adoption Check](governed-automation/ADOPTION_CHECK.md) before selecting governed models.

**When uncertain, remain in Core Hygiene.** The burden of proof belongs to the additional machinery — importance, complexity, distribution, AI-assisted use, and production status do not by themselves justify Governed Automation.

## What each layer provides

**[Core Hygiene](core/README.md)** keeps three properties visible in non-trivial operational codebases:

1. **Boundaries** — decisions and external effects have clear owners and testable seams.
2. **Semantics** — important states, actions, outcomes, and reasons are declared once branching, ambiguity, or repetition makes them load-bearing.
3. **Traceability** — where work crosses remote or asynchronous hops, one operation retains a stable identity.

It adds proportionate testing and documentation guidance without imposing architectural branding, a prescribed directory tree, staged truth, approval machinery, reconciliation, or governance vocabulary. Repositories with several stable, cross-cutting constraints may optionally escalate direct tests into a [Repository Conformance Harness](core/CONFORMANCE_HARNESS.md); that remains a Core Hygiene mechanism, not a third layer.

**[Governed Automation](governed-automation/README.md)** is deliberately exceptional, reserved for systems exercising consequential authority over shared or external state. Its authority, evidence, reconciliation, recovery, and security models are described inside that directory once the gate above has been crossed.

## How product repositories use this seed

1. Adopt the Core Hygiene questions and only the checks that protect real seams, using the smallest direct test, ratchet, or local convention that controls the identified risk.
2. If the authority gate above is crossed, complete the adoption and cost check and select only the governed models whose triggers are present.
3. Keep product contracts, runbooks, decisions, and local rule sets in the product repository; contribute a reusable lesson here only after implementation or operational evidence exists.

**For most repositories, step 1 is the complete adoption.** Do not copy every file mechanically — the objective is to prevent specific ambiguity and failure modes, not to reproduce this repository's shape.

## Evidence boundary

A deployed system can still be young. Strong tests improve confidence but do not prove correctness. A lesson observed in one system remains a bounded inference until repeated elsewhere. Case studies provide evidence, not universal precedent, and do not independently justify crossing the Governed Automation gate.

The documented cases currently come from operational tooling and infrastructure-adjacent systems. The models have not yet been validated here through documented cases in financial transaction processing, regulated data pipelines, ML training or deployment governance, healthcare, identity systems, or non-technical human approval workflows. Those remain open evidence boundaries, not implied coverage.
