# Governed Authority Witness — Python

This specimen demonstrates selected invariants from the seven-power model with in-memory state and standard-library tests.

It is intentionally incomplete as an application. It contains no cloud SDK, database, queue, HTTP service, credentials, or deployment configuration.

The runtime checks show that logical authority is backed by role enforcement:

- `COMMIT` may write canonical state but cannot mutate the managed resource;
- `RECONCILER` may mutate the managed resource but cannot write canonical state;
- `RECOVERY` owns only an authenticated reconciliation-request capability;
- the recovery object does not import or hold the privileged reconciler type, identity, store, or managed resource;
- stale proposal versions cannot overwrite newer canonical decisions.

The structural tests additionally restrict protected method call sites and prove that recovery reaches execution only through the request boundary.

## Model 10 coverage

| Authority-component security property | Witness status |
|---|---|
| Distinct logical identities | Executed |
| Role-restricted protected effects | Executed |
| Authenticated recovery request | Executed |
| Fail-closed validation | Executed |
| Version and replay protection | Partially executed — stale expected-version rejection is tested; transport replay controls are not |
| Credential rotation and revocation | Not demonstrated |
| Independently retained audit evidence | Not demonstrated |
| Break-glass authorization and post-use review | Not demonstrated |

## Not demonstrated by this witness

- workload-identity provisioning;
- substrate permission policies;
- credential rotation and revocation;
- independently retained audit storage;
- break-glass authorization and post-use review.

These remain production security requirements where the adoption gate and threat model justify them. They are not represented by synthetic in-memory roles.

Run from the repository root:

```bash
python -m unittest discover -s examples/governed_authority_python/tests -v
```
