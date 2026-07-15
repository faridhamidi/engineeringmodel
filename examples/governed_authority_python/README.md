# Governed Authority Witness — Python

This specimen demonstrates selected invariants from the seven-power model and [Declared protected actions and derived controls](../../governed-automation/MODELS.md#11-declared-protected-actions-and-derived-controls) with in-memory state and standard-library tests.

It is intentionally incomplete as an application. It contains no cloud SDK, database, queue, HTTP service, credentials, or deployment configuration.

The runtime checks show that logical authority is backed by role enforcement:

- `COMMIT` may write canonical state but cannot mutate the managed resource;
- `RECONCILER` may mutate the managed resource but cannot write canonical state;
- `RECOVERY` owns only an authenticated reconciliation-request capability;
- the recovery object does not import or hold the privileged reconciler type, identity, store, or managed resource;
- stale proposal versions cannot overwrite newer canonical decisions;
- protected actions select controls from one declared registry;
- runtime facts evaluate the selected controls without redefining them;
- unknown protected actions fail closed with a visible canonical reason.

The structural tests additionally restrict protected method call sites, prove that recovery reaches execution only through the request boundary, prevent direct registry reads, and keep static control selection independent of runtime state modules.

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

## Model 11 coverage

| Declared protected-action property | Witness status |
|---|---|
| Complete protected-action registry | Executed for the three-action specimen |
| Static control selection | Executed |
| Separate runtime evaluation | Executed |
| Unknown-action fail-closed behavior | Executed |
| Canonical machine-readable hold reasons | Executed |
| Operator message derived from canonical reason | Executed |
| No direct registry reads outside its owner | Executed |
| Production authorization policy and identity provisioning | Not demonstrated |

## Not demonstrated by this witness

- workload-identity provisioning;
- substrate permission policies;
- credential rotation and revocation;
- independently retained audit storage;
- break-glass authorization and post-use review;
- production action inventory or organization-specific control categories.

These remain production security requirements where the adoption gate and threat model justify them. They are not represented by synthetic in-memory roles.

Run from the repository root:

```bash
python -m unittest discover -s examples/governed_authority_python/tests -v
```