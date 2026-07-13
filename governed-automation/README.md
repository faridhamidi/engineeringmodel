# Governed Automation Layer

This layer is intentionally narrow. It applies when software does more than transform local data: it encodes a durable decision, exercises authority, or changes shared external state where an incorrect default can cause material harm.

## Prerequisite

Complete [`ADOPTION_CHECK.md`](ADOPTION_CHECK.md) before adopting this layer.

Core hygiene is always useful. Governed-automation machinery is conditional.

## Contents

- [`ADOPTION_CHECK.md`](ADOPTION_CHECK.md) — an answerable gate for deciding whether this layer applies.
- [`PRINCIPLES.md`](PRINCIPLES.md) — governing positions for authority-bearing systems.
- [`AUTOMATED_AUTHORITY.md`](AUTOMATED_AUTHORITY.md) — separation of discovery, proposal, validation, commitment, derivation, execution, and recovery.
- [`MODELS.md`](MODELS.md) — selectable state, policy, reconciliation, provenance, and recovery models.
- [`DECISION_TREE.md`](DECISION_TREE.md) — plain trigger conditions for the vocabulary and models.
- [`VOCABULARY.md`](VOCABULARY.md) — narrow definitions used by this layer.

## Non-goals

This layer is not a default application architecture. It should not be used merely because a system:

- has a database;
- runs scheduled jobs;
- calls a cloud API;
- has more than one module;
- needs retries;
- benefits from clean code.

Those are core-hygiene concerns unless they also carry consequential authority, shared-state risk, or durable governance decisions.
