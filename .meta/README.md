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
| [`builder-accessible-layer.md`](builder-accessible-layer.md) | Forward document | draft |
| [`synthesis.md`](synthesis.md) | Synthesis note (conclusions + candidate ADRs) | draft |

## Reading order for a newcomer

1. Read the top-level [`README.md`](../README.md) to understand what the seed is.
2. Read the forward document here to understand where it is proposed to go.
3. Follow its links into `core/` and `governed-automation/` for the mechanisms
   it references. This folder does not restate them; it points to them.
