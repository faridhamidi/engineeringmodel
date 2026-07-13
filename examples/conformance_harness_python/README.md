# Repository Conformance Harness Witness

This dependency-free Python witness demonstrates one possible repository conformance harness.

## Demonstrated

- typed, fail-closed manifest parsing;
- stable namespaced rule identifiers and lifecycle validation;
- zero-violation and exact-ratchet enforcement;
- rationale and approval-policy references;
- exact public owner principals and CODEOWNERS correspondence;
- Python-specific checker adapters;
- positive per-rule tests and minimal falsifiers;
- isolated generic ratchet and lifecycle fixtures;
- active, ratchet, ownership, and historical audit sections.

## Not demonstrated

- required code-owner review enforcement;
- branch protection or administrator-bypass prevention;
- record-level ownership inside one manifest file;
- conceptual-role-to-principal resolution;
- cross-language checker portability;
- productivity or defect-rate improvement;
- deployment or production mutation authority.

## Run

From the repository root:

```bash
python -m unittest discover -s examples/conformance_harness_python/tests -v
```

From this directory:

```bash
python check_manifest.py
python check_contracts.py
python run_audit.py --report-path artifacts/conformance-audit.md
```

This is an executable witness, not a prescribed manifest schema, language, directory layout, or organizational ownership model.
