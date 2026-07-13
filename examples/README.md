# Executable Witnesses

These examples prove selected repository claims can be enforced with code and tests.

They are deliberately not reference applications:

- no credentials or network access;
- no external dependencies;
- no organization-specific schema;
- no deployment recommendation;
- no claim that Python or this directory layout is preferred.

## Core boundaries

[`core_boundaries_python/`](core_boundaries_python/) demonstrates:

- pure decision logic separated from an external client;
- external-client construction confined to one module;
- operation-context propagation;
- a structural ratchet that fails when a new bypass appears.

Run:

```bash
python -m unittest discover -s examples/core_boundaries_python/tests -v
```

## Governed authority

[`governed_authority_python/`](governed_authority_python/) demonstrates:

- proposal state cannot cause external mutation;
- invalid or stale evidence fails closed;
- one identity can write canonical state;
- another identity can mutate the managed resource;
- runtime role enforcement backs the logical authority split;
- repeated reconciliation is idempotent;
- recovery re-enters through an authenticated request boundary instead of receiving a privileged reconciler object or identity;
- stale proposal versions cannot overwrite newer canonical decisions;
- structural checks reject new protected call sites.

Run:

```bash
python -m unittest discover -s examples/governed_authority_python/tests -v
```
