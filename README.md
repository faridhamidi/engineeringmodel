<p align="center">
  <img src="docs/assets/engineering-model-governance-harness.avif" alt="Engineering Models — governed automation harness" width="100%">
</p>

# Engineering Models

Reusable engineering tradecraft extracted from operational software, organized by adoption cost and problem scope.

This repository is a governing seed, not a framework or mandatory starter template. Its central rule is mechanical proportionality: broadly useful hygiene is separated from specialized authority machinery so a team does not have to infer the boundary from prose caveats.

## Two adoption layers

| Layer | Intended scope | Start here |
|---|---|---|
| **Core Hygiene** | Any non-trivial operational codebase | [`core/README.md`](core/README.md) |
| **Governed Automation** | Systems that encode durable authority or make consequential shared-state changes | [`governed-automation/ADOPTION_CHECK.md`](governed-automation/ADOPTION_CHECK.md) |

Always begin with the core layer. Adopt the governed layer only when its gate is satisfied and its operating cost is justified.

## Core idea

Build the smallest foundation that keeps three properties visible:

1. **Boundaries** — decisions and external effects have clear owners and testable seams.
2. **Semantics** — important states, actions, outcomes, and reasons are declared when repetition makes them load-bearing.
3. **Traceability** — one operation can be followed across remote or asynchronous hops.

These properties do not require architectural branding or a prescribed directory tree.

## Repository map

```text
core/                    broadly adoptable hygiene
governed-automation/     gated authority and shared-state models
case-studies/             evidence-tagged adoption and non-adoption cases
examples/                 dependency-free executable witnesses
.github/workflows/        CI for the executable witnesses
AGENTS.md                 concise contributor and agent navigation
CONTRIBUTING.md           evidence, ownership, writing, and confidentiality rules
```

The examples are deliberately small. They prove selected constraints can be enforced; they are not production templates or claims that Python is the preferred implementation language.

Repositories with several stable, cross-cutting constraints may optionally escalate direct structural tests into a [manifest-backed conformance harness](core/CONFORMANCE_HARNESS.md). This is an optional Core Hygiene mechanism, not a third adoption layer.

## Canonical document ownership

The governed layer avoids explaining the same concept fully in several places:

- [`MODELS.md`](governed-automation/MODELS.md) is the canonical source for each model's trigger, mechanism, invariant, cost, security implications, and skip condition.
- [`DECISION_TREE.md`](governed-automation/DECISION_TREE.md) is a trigger-based projection into the model catalog.
- [`VOCABULARY.md`](governed-automation/VOCABULARY.md) provides short definitions and links to canonical entries.
- [`PRINCIPLES.md`](governed-automation/PRINCIPLES.md) contains only cross-cutting positions.
- [`AUTOMATED_AUTHORITY.md`](governed-automation/AUTOMATED_AUTHORITY.md) describes how the seven powers compose.

## How product repositories use this seed

A product repository should:

1. adopt the core questions and only the checks that protect real seams;
2. complete the governed-automation adoption and cost check;
3. record selected models and explicit rejections;
4. keep product contracts, runbooks, and local decisions in the product repository;
5. contribute a reusable lesson here only after implementation or operational evidence exists.

Do not copy every file mechanically. The objective is to prevent specific ambiguity and failure modes, not to reproduce this repository's shape.

## Evidence boundary

A deployed system can still be young. Strong tests improve confidence but do not prove correctness. A lesson observed in one system remains a bounded inference until repeated elsewhere.

The documented cases currently come from operational tooling and infrastructure-adjacent systems. The models have not yet been validated here through documented cases in financial transaction processing, regulated data pipelines, ML training or deployment governance, healthcare, identity systems, or non-technical human approval workflows. Those remain open evidence boundaries, not implied coverage.