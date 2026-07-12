# Case Studies

These summaries are sanitized. They preserve engineering observations while excluding organization-specific identifiers, source code, infrastructure values, and proprietary workflows.

## Governance control plane for centralized cloud monitoring

### Context

A centralized observability account could receive metrics, logs, and alarms from many cloud accounts. Each relationship was technically easy to create but represented a governance decision: whether the source account was active, appropriately classified, approved where required, and explicitly requested for monitoring.

The operational risk existed in both directions:

- failing to include an eligible account created a monitoring blind spot;
- including an ineligible or unapproved account violated governance intent.

### Initial framing

The request could have been implemented as account discovery followed by automatic link creation.

That design was rejected because it would allow the discovery mechanism to acquire decision authority.

### Implemented authority chain

```text
organization inventory
    -> discovery and fact refresh
    -> draft proposal
    -> operator or narrow system decision
    -> contract validation
    -> atomic canonical promotion
    -> pure desired-state evaluation
    -> OAM reconciliation
    -> monitoring pipeline
```

A separate healer detects interrupted flows and either re-drives an existing decision through the promoter or restores a known prior generation. It cannot approve monitoring or directly mutate links.

### Important separations

#### Discovery versus admission

Newly found accounts enter staging. Discovery owns account facts and may improve classification provenance under strict confidence rules, but it cannot change approval, requested monitoring state, or decision rationale.

#### Requested versus effective monitoring

Requested monitoring is stored as governance intent. Effective monitoring is derived from lifecycle, environment, approval, requested state, and exclusions. A request can remain recorded while policy correctly prevents its execution.

#### Proposal versus truth

The operator interface edits drafts. A designated promoter is the only authority that commits canonical governance records. Drafts never trigger OAM mutation.

#### Decision versus execution

The reconciler is the only OAM mutator. It reads canonical records, derives desired state, compares real links, and converges them. It cannot approve or classify an account.

#### Observation versus repair

Manual repair begins with a read-only diff. Repair is blocked when sink observation is incomplete or fatal. When permitted, repair requires a reason and invokes the same reconciler used by ordinary execution.

### Testing approach

The project uses a three-axis classification:

- test intent: falsification, regression, or confirmation;
- test target: decision oracle, invariant, contract, architecture boundary, or concurrency safety;
- input generation: examples, matrices, exhaustive products, boundaries, fault injection, or anomaly sequences.

Key protected properties include:

- governance fields survive discovery refresh unchanged;
- externally owned facts survive governance edits unchanged;
- incomplete policy inputs fail closed;
- reconciliation is idempotent;
- stale writers are rejected atomically;
- cloud SDK and raw storage calls cannot leak into the pure decision core;
- only authorized adapters may bypass each port;
- recovery cannot create new authority.

Static architecture tests function as executable fitness rules. They scan source for forbidden bypasses and are themselves tested using seeded bad examples.

### Documentation approach

The project distinguishes:

- forward documents for non-binding direction;
- design documents for scoped implementation plans;
- architecture decision records for durable rules.

Work can move from direction to plan to durable decision, with provenance recorded in both directions. Completed plans are archived; superseded decisions remain visible in the decision history.

### Main lessons

1. The hard problem was not cloud API orchestration. It was constraining automated authority.
2. A control plane can be small and domain-specific while still having real control-plane properties.
3. Human sovereignty must be structural, not a comment in code.
4. Recovery paths deserve the same authority analysis as primary paths.
5. Architecture boundaries can and should be tested when bypass would invalidate the operating model.
6. Uncertainty should remain visible rather than being coerced into a convenient value.

### Deliberate non-claims

The system does not establish equivalence to Crossplane, Kubernetes controllers as an ecosystem, or a general multi-cloud platform. Its decision core is separated from AWS adapters, but the implemented adapters are AWS-specific. Portability of design is not the same as implemented portability.

The testing approach is rigorous for the domain, but it is not a proof of correctness and should not be compared to the scale of testing programs in mature database engines.

## Real-time operational status and reporting

### Context

Multiple operators update a shared status board while viewers observe the same page. The committed board also becomes the source for scheduled and on-demand reports delivered to an external collaboration channel.

### Main model

- full-state synchronization on connect and reconnect;
- delta updates during steady state;
- separation of in-progress drafts from committed board state;
- immutable report snapshots;
- delivery progress and retry accountability;
- explicit operational, security, and observability boundaries.

### Main lesson

A status page used by a 24/7 function is a coordination and accountability system, not merely a dashboard. Its value lies in shared state, synchronization, commitment, and reproducible delivery.

### Deliberate constraint

A single-node application, SQLite in WAL mode, a conventional reverse proxy, and a frontend without a build pipeline were sufficient for the actual workload. Distributed complexity was not imported for appearance.
