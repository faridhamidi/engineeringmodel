# Case Studies

These case studies are sanitized and evidence-tagged. They show both adoption and non-adoption of the governed-automation layer.

## Cases

- [`GOVERNED_CLOUD_MONITORING.md`](GOVERNED_CLOUD_MONITORING.md) — a system where durable authority, broad mutation scope, and recovery risk justify the complete layer.
- [`COMMITTED_STATUS_REPORTING.md`](COMMITTED_STATUS_REPORTING.md) — a system that uses selected models without adopting the complete authority chain.
- [`NON_ADOPTION_LOCAL_AUDIT_DASHBOARD.md`](NON_ADOPTION_LOCAL_AUDIT_DASHBOARD.md) — a local application where core hygiene is sufficient and the governed layer would add state without controlling meaningful authority risk.

## Evidence format

Each case separates:

- **implemented** — visible in code;
- **tested** — protected by executable checks;
- **deployed** — running in a real environment;
- **operationally used** — used by real workflows or operators;
- **inferred** — a bounded conclusion drawn from the observed system.

A lesson inferred from one system is not presented as universal proof.

## Current evidence boundary

All documented cases are operational-tooling or infrastructure-adjacent systems. The repository does not yet contain evidence-tagged cases from financial transaction processing, regulated data pipelines, ML governance, healthcare, identity platforms, or non-technical human approval workflows.

Those domains should be added only when a real implementation or operational record can support the same evidence discipline. Hypothetical portability is not a case study.
