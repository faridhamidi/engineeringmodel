# Agent and Contributor Map

This file is a navigation map, not a second methodology document.

<!-- engineering-model-steering:start -->
## Revertible Envelope

Classify each intended action before performing it:

- If it is local and reversible in one step, continue autonomously.
- If it touches shared ground, is hard to undo, or is uncertain, fail closed and load
  the installed `engineering-model` skill for the depth the decision earns.
- Keep agent-authored work recoverable. At coherent, verified task boundaries, commit
  only task-owned changes with a focused message. Never commit secrets, generated junk,
  unrelated changes, or pre-existing user work. If the task cannot be isolated safely,
  leave the work uncommitted and report why.
- Before relying on git as recovery, verify that the project can create a checkpoint.
  If it cannot, keep the changes local and report the missing recovery mechanism.
- Before any external-substrate effect, stop and obtain explicit human approval for the
  exact target, consequence, and action. Do not treat approval for one effect as
  approval for a broader effect.
- Git can undo authoring; it cannot undo an external effect.

## Implementation Quality

This applies to any code change, regardless of how it is classified above. Load the
installed `engineering-model` skill before editing whenever the change will alter
executable behavior, add or change branching or validation logic, parse external or
untrusted input, or touch a persistence, external, or asynchronous seam. Decide by these
concrete triggers, not by a subjective sense of how large or important the change is; skip
the skill only for pure formatting, comments, or a single-line reversible edit. If the skill
is unavailable, install the packaged skill before continuing; use only the depth the work earns.

- Reuse the repository's existing patterns for the same concern, then self-audit changed code
  for dead or fragile constructs and divergence before completion, and fix findings in the same pass.
  Safety and data integrity override existing conventions: if a pattern would let a failure
  corrupt or lose accepted data, do not preserve it — protect the data and note the intentional
  departure.
- Protect changed load-bearing behavior with the lightest test that would fail on a
  realistic defect. Run the tests and checks you cite. Add diagnostic context at external,
  asynchronous, or persistence seams only when failure would otherwise be silent; never
  silently discard or corrupt data.
<!-- engineering-model-steering:end -->

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
- [`builders/_witness/`](builders/_witness/) — builder-line, steering, native-surface,
  and installable-skill checks.

## Required checks

```bash
python -m unittest discover -s examples/core_boundaries_python/tests -v
python -m unittest discover -s builders/_witness/tests -v
python -m unittest discover -s examples/conformance_harness_python/tests -v
python -m unittest discover -s examples/governed_authority_python/tests -v
python builders/_witness/sync_skill_references.py --check
python -m compileall -q examples builders seed
```

## Change discipline

- Generated output is a proposal, not canonical truth.
- Do not weaken a rule, checker, and falsifier together without documenting the changed architectural decision.
- Do not delete or obscure retired or superseded rule history.
- Do not couple generic harness-engine tests to active rule identifiers.
- Do not copy witness layouts mechanically into product repositories.
- Keep full explanations in their canonical documents.
