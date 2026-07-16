# Builder-layer witnesses

Small, dependency-free witnesses for the builder-accessible layer. They are **not**
runtime tools a builder operates and do not claim that an agent will always obey prose
steering.

**Evidence:** implemented, tested. Runtime agent adherence, native-client installation
behavior, and substrate enforcement are not demonstrated.

## Exact claims demonstrated

1. The blast-radius line is expressible as a deterministic decision over two
   observable signals — *touches shared ground?* and *can you undo it easily?*
2. Both signals are load-bearing: dropping either one misroutes a case (the
   `test_*_is_load_bearing` tests are the minimal falsifiers).
3. Uncertainty fails closed — an unknown signal routes **above** the line.
4. The builder surface links into the engine and every repo-relative link resolves
   (a zero-violation ratchet), and the checker reports a missing reference
   (the known-bad case).
5. A clearly local and reversible action continues, an above-line local action pauses
   for review, and an external effect requires explicit human approval.
6. The canonical steering block and its `AGENTS.md` and `CLAUDE.md` forms contain every
   load-bearing norm and remain byte-for-byte equivalent.
7. The `engineering-model` skill meets the local Agent Skills package contract, keeps
   references one level deep, and carries exact generated copies of every canonical
   engine document. Missing, stale, and extra references are rejected.

## Run

```bash
python -m unittest discover -s builders/_witness/tests -v
python builders/_witness/sync_skill_references.py --check
```

To refresh the carried engine references after an approved canonical engine change,
run `python builders/_witness/sync_skill_references.py`, review the generated diff, and
rerun the checks. Generated copies are projections; `core/` and
`governed-automation/` remain canonical.
