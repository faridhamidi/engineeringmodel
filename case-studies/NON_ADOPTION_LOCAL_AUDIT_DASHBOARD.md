# Non-Adoption Case: Local Session-Audit Dashboard

## Purpose of this case

This is not a failed project. It is a boundary case showing where the Core Hygiene Layer is useful and the complete Governed Automation Layer is not justified.

The source was a real public personal repository. Identifying names, paths, session contents, screenshots, and runtime artifacts are intentionally omitted.

## Operating shape

The application:

- reads local session records;
- parses them into typed datasets;
- generates replaceable CSV and JSON reports;
- serves a dashboard on the local loopback interface;
- protects refresh with a process-local lock and short cooldown;
- excludes generated artifacts that may contain local paths, labels, or prompt text from version control.

## Adoption-check result

| Gate | Result |
|---|---|
| Consequential external effect | No — writes local, regenerable reports |
| Durable authority | No — no approval, admission, entitlement, or lifecycle decision |
| Material blast radius | No — one local user and replaceable artifacts |
| Evidence-sensitive privileged action | No — incorrect output is an audit defect, not authorization |
| Governed recovery | No — refresh or rerun is sufficient |

**Adoption:** Core Hygiene Layer only.

## What remains valuable

- parsing, reporting, and HTTP concerns have understandable module boundaries;
- generated schemas and output names are centralized;
- refresh concurrency is explicitly controlled;
- transformations and metrics can be tested independently;
- sensitive runtime output is excluded from the public repository;
- the server defaults to local-only exposure.

## What should not be added

The following would add coordination cost without controlling a meaningful authority risk:

- draft and canonical report stores;
- an approval state for refresh;
- a dedicated commit authority;
- desired-state reconciliation;
- a recovery hierarchy or healer;
- decision provenance for ordinary local regeneration.

## Counterfactual misapplication

Force-applying the seven-power authority split would create at least three unnecessary states—proposal, committed intent, and observed report output—for a task whose authoritative intent is simply “refresh the local reports now.” Contributors would need to understand promotion and recovery terminology before changing a parser, while failure would still be corrected by deleting the output and rerunning generation.

The result would be more latency, more transitions, and more explanation without a corresponding reduction in blast radius or privilege risk.

## Evidence

- **Implemented:** local ingestion, report generation, local HTTP serving, bounded refresh concurrency, and runtime-artifact exclusion.
- **Tested:** transformation and reporting behavior in the source repository.
- **Observed scope:** one personal local application.
- **Inferred:** governed-automation machinery would add state and contributor cost without materially reducing authority risk.

## Lesson

A clean codebase still needs boundaries, semantics, tests, and safe defaults. It does not need a governance model unless it actually governs something.
