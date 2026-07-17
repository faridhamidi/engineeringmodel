# .meta — records about evolving this repository

This folder holds **meta-operation records**: documents about how this repository
itself should change. It is deliberately separate from the methodology content in
`core/`, `governed-automation/`, `examples/`, and `case-studies/`, which describe
engineering tradecraft for *other* systems.

A record here is about *this seed*, not about a product built with it.

## Record types

These follow the repository's own three-record discipline in
[`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md):

| Type | Question it answers | Binding status |
|---|---|---|
| **Forward document** | Where might this repo go, and in what order? | Non-binding direction |
| **Design document** | How will one scoped change be built and verified? | Binding while active |
| **Architecture decision record (ADR)** | What durable rule was decided, and why? | Binding until superseded |

Each record carries the minimal header from `DOCUMENTATION.md` so its type,
status, provenance, and freshness are greppable.

## Current records

| File | Type | Status |
|---|---|---|
| [`builder-accessible-layer.md`](builder-accessible-layer.md) | Forward document | realized, historical |
| [`builder-accessible-layer.design.md`](builder-accessible-layer.design.md) | Design document | completed, historical |
| [`ADR-001-builder-accessible-layer.md`](ADR-001-builder-accessible-layer.md) | ADR | accepted |
| [`share-ready-seed.design.md`](share-ready-seed.design.md) | Design document | completed, historical |
| [`ADR-002-share-ready-seed.md`](ADR-002-share-ready-seed.md) | ADR | accepted |
| [`ADR-003-proportionate-quality-steering.md`](ADR-003-proportionate-quality-steering.md) | ADR | accepted |
| [`rep-001-seed-cleanroom-observation.md`](rep-001-seed-cleanroom-observation.md) | Observation report (evidence) | complete (n=5, single runtime) |
| [`rep-002-seed-codex-cleanroom.md`](rep-002-seed-codex-cleanroom.md) | Observation report (Codex + Claude, real runtimes) | complete (gpt-5.5 + sonnet-4.6, n=2+2 each) |
| [`rep-003-claude-new-steering-behavioral-tests.md`](rep-003-claude-new-steering-behavioral-tests.md) | Observation report (new-steering Claude runs) | complete but partly confounded; superseded for the quality-floor question |
| [`dd-001-claude-quality-steering-cleanroom.md`](dd-001-claude-quality-steering-cleanroom.md) | Design document | ready to execute (invocation validated) |
| [`rep-004-claude-quality-steering-cleanroom-result.md`](rep-004-claude-quality-steering-cleanroom-result.md) | Observation report (falsification program) | living — R1–2 invocation confirmed; R3 hard-task A/B disconfirms correctness lift |
| [`rep-005-falsification-program-narrative.md`](rep-005-falsification-program-narrative.md) | Narrative report (program history) | living — Kiro sessions → Codex → Claude R1–3 → R4/4b → R5 (in progress) |
| [`rep-006-prior-art-related-work.md`](rep-006-prior-art-related-work.md) | Related-work / prior-art note | living — 2026 studies converge (process↑, outcome flat); controls to borrow |
| [`dd-002-structure-vs-content.md`](dd-002-structure-vs-content.md) | Experiment design (terminal round) | proposed — 4-arm (bare/placebo/labels-only/full) pass-rate A/B; stopping rule |

## Reading order for a newcomer

1. Read the top-level [`README.md`](../README.md) to understand what the seed is.
2. Read ADR-001 for the durable builder-layer decision, ADR-002 for its share-ready
   distribution projection, and ADR-003 for the evidence-backed quality floor.
3. Read the forward and design documents only when the direction or implementation
   history is relevant.
4. Follow their links into `core/` and `governed-automation/` for canonical mechanisms.
