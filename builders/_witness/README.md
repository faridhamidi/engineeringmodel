# Builder-line witness

A small, dependency-free witness for the plain-language blast-radius line in
[`../START_HERE.md`](../START_HERE.md). It is **not** a runtime tool a builder
operates and it is not a reference layout — it demonstrates that the translation is
precise and stays honest.

**Evidence:** implemented, tested. The underlying methodology claim is *proposed*.

## Exact claims demonstrated

1. The blast-radius line is expressible as a deterministic decision over two
   observable signals — *touches shared ground?* and *can you undo it easily?*
2. Both signals are load-bearing: dropping either one misroutes a case (the
   `test_*_is_load_bearing` tests are the minimal falsifiers).
3. Uncertainty fails closed — an unknown signal routes **above** the line.
4. The builder surface links into the engine and every repo-relative link resolves
   (a zero-violation ratchet), and the checker reports a missing reference
   (the known-bad case).

## Run

```bash
python -m unittest discover -s builders/_witness/tests -v
```

This witness does not prescribe a language, project layout, or that a builder run
any of this code. It exists so the translation cannot silently become vague or link
to engine text that no longer exists.
