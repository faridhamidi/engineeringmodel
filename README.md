# Engineering Models

Reusable engineering tradecraft extracted from operational software, organized by adoption cost and problem scope.

This repository is a governing seed, not a framework or mandatory starter template. Its central rule is mechanical proportionality: broadly useful hygiene is separated from specialized authority machinery so a team does not have to infer the boundary from prose caveats.

## Two adoption layers

| Layer | Intended scope | Start here |
|---|---|---|
| **Core Hygiene** | Any non-trivial operational codebase | [`core/README.md`](core/README.md) |
| **Governed Automation** | Systems that encode durable authority or make consequential shared-state changes | [`governed-automation/ADOPTION_CHECK.md`](governed-automation/ADOPTION_CHECK.md) |

Always begin with the core layer. Adopt the governed layer only when its gate is satisfied.

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
CONTRIBUTING.md           evidence, extraction, writing, and confidentiality rules
```

## How product repositories use this seed

A product repository should:

1. adopt the core questions and only the checks that protect real seams;
2. complete the governed-automation adoption check;
3. record selected models and explicit rejections;
4. keep product contracts, runbooks, and local decisions in the product repository;
5. contribute a reusable lesson here only after implementation or operational evidence exists.

Do not copy every file mechanically. The objective is to prevent specific ambiguity and failure modes, not to reproduce this repository’s shape.

## Evidence boundary

A deployed system can still be young. Strong tests improve confidence but do not prove correctness. A lesson observed in one system remains a bounded inference until repeated elsewhere.
