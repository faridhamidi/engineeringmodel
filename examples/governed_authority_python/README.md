# Governed Authority Witness — Python

This specimen demonstrates selected invariants from the seven-power model with in-memory state and standard-library tests.

It is intentionally incomplete as an application. It contains no cloud SDK, database, queue, HTTP service, credentials, or deployment configuration.

The runtime checks show that logical authority is backed by role enforcement:

- `COMMIT` may write canonical state but cannot mutate the managed resource;
- `RECONCILER` may mutate the managed resource but cannot write canonical state;
- `RECOVERY` requests reconciliation and receives neither stronger credential.

The structural tests additionally restrict protected method call sites.

Run from the repository root:

```bash
python -m unittest discover -s examples/governed_authority_python/tests -v
```
