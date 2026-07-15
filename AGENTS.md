# Agent and Contributor Map

This file is a navigation map, not a second methodology document.

## Read first

1. Read [`README.md`](README.md) for repository scope and adoption layers.
2. Read [`core/README.md`](core/README.md) before adopting any specialized mechanism.
3. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) for evidence, ownership, writing, and confidentiality rules.
4. Read the canonical document for the concept being changed.

## Optional semantic consistency

Read [`core/SEMANTIC_CONSISTENCY.md`](core/SEMANTIC_CONSISTENCY.md) when a change introduces or modifies shared states, actions, transitions, reasons, outcomes, or recovery semantics.

## Optional conformance harness

Read [`core/CONFORMANCE_HARNESS.md`](core/CONFORMANCE_HARNESS.md) only when changing the harness, its rules, or a product repository that has adopted this escalation.

## Executable witnesses

- [`examples/core_boundaries_python/`](examples/core_boundaries_python/) — direct structural checks and a boundary ratchet.
- [`examples/conformance_harness_python/`](examples/conformance_harness_python/) — manifest-backed conformance, ratchets, lineage, ownership binding, and audit output.
- [`examples/governed_authority_python/`](examples/governed_authority_python/) — bounded authority, execution, and recovery.

## Required checks

```bash
python -m unittest discover -s examples/core_boundaries_python/tests -v
python -m unittest discover -s examples/conformance_harness_python/tests -v
python -m unittest discover -s examples/governed_authority_python/tests -v
python -m compileall -q examples
```

## Change discipline

- Generated output is a proposal, not canonical truth.
- Do not weaken a rule, checker, and falsifier together without documenting the changed architectural decision.
- Do not delete or obscure retired or superseded rule history.
- Do not couple generic harness-engine tests to active rule identifiers.
- Do not copy witness layouts mechanically into product repositories.
- Keep full explanations in their canonical documents.