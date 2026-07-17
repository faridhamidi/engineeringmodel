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
| [`FD-001-builder-accessible-layer.md`](FD-001-builder-accessible-layer.md) | Forward document | realized, historical |
| [`DD-001-builder-accessible-layer.md`](DD-001-builder-accessible-layer.md) | Design document | completed, historical |
| [`ADR-001-builder-accessible-layer.md`](ADR-001-builder-accessible-layer.md) | ADR | accepted |
| [`DD-002-share-ready-seed.md`](DD-002-share-ready-seed.md) | Design document | completed, historical |
| [`ADR-002-share-ready-seed.md`](ADR-002-share-ready-seed.md) | ADR | accepted |
| [`ADR-003-proportionate-quality-steering.md`](ADR-003-proportionate-quality-steering.md) | ADR | accepted |
| [`REP-001-seed-cleanroom-observation.md`](REP-001-seed-cleanroom-observation.md) | Observation report (evidence) | complete (n=5, single runtime) |
| [`REP-002-seed-codex-cleanroom.md`](REP-002-seed-codex-cleanroom.md) | Observation report (Codex + Claude, real runtimes) | complete (gpt-5.5 + sonnet-4.6, n=2+2 each) |
| [`REP-003-claude-new-steering-behavioral-tests.md`](REP-003-claude-new-steering-behavioral-tests.md) | Observation report (new-steering Claude runs) | complete but partly confounded; superseded for the quality-floor question |
| [`DD-003-claude-quality-steering-cleanroom.md`](DD-003-claude-quality-steering-cleanroom.md) | Design document | ready to execute (invocation validated) |
| [`DD-005-cleanroom-task-design-methodology.md`](DD-005-cleanroom-task-design-methodology.md) | Design document | living — consolidated task-authoring/coverage-gate/firewall methodology for rounds 3-5+ |
| [`REP-004-claude-quality-steering-cleanroom-result.md`](REP-004-claude-quality-steering-cleanroom-result.md) | Observation report (falsification program) | living — R1–2 invocation confirmed; R3 hard-task A/B disconfirms correctness lift |
| [`REP-005-falsification-program-narrative.md`](REP-005-falsification-program-narrative.md) | Narrative report (program history) | living — Kiro sessions → Codex → Claude R1–3 → R4/4b → R5 (in progress) |
| [`REP-006-prior-art-related-work.md`](REP-006-prior-art-related-work.md) | Related-work / prior-art note | living — 2026 studies converge (process↑, outcome flat); controls to borrow |
| [`DD-004-structure-vs-content.md`](DD-004-structure-vs-content.md) | Experiment design (terminal round) | proposed — 4-arm (bare/placebo/labels-only/full) pass-rate A/B; stopping rule |

## Reading order for a newcomer

1. Read the top-level [`README.md`](../README.md) to understand what the seed is.
2. Read ADR-001 for the durable builder-layer decision, ADR-002 for its share-ready
   distribution projection, and ADR-003 for the evidence-backed quality floor.
3. Read the forward and design documents only when the direction or implementation
   history is relevant.
4. Follow their links into `core/` and `governed-automation/` for canonical mechanisms.
