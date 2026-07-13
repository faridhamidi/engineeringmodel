# Plain-Language Decision Tree

Use the trigger, not the term, to decide what the system needs.

## Boundaries and ownership

**Does decision code directly construct or call databases, provider SDKs, queues, files, clocks, or network clients?**

- No → keep the current structure.
- Yes → add one named seam at the external dependency. The seam may be a function parameter, wrapper, module, or protocol.

**Can two components change the same authoritative field or external resource?**

- No → no sole-writer rule is required.
- Yes, but they own disjoint fields → declare field ownership.
- Yes, and their writes can conflict → designate one logical mutation authority.

## State and commitment

**Can a proposed edit be incomplete, reviewed, rejected, or corrected before it becomes authoritative?**

- No → write directly with validation.
- Yes → separate proposal state from committed state.

**Can requested intent remain valid while policy temporarily blocks execution?**

- No → store the direct state.
- Yes → retain requested intent and derive effective state with a classified reason.

## Execution and repair

**Can the managed system drift from valid committed intent?**

- No → do not add reconciliation.
- Yes → compare desired and observed state, then apply idempotent corrections.

**Could incomplete observation cause an unsafe repair?**

- No → ordinary retry may be enough.
- Yes → observe first, block repair on unknown evidence, and require the normal mutation path.

**Could retry or restoration grant more authority than the original operation?**

- No → ordinary retry semantics are enough.
- Yes → require recovery to re-enter the original validation and mutation boundaries.

## Evidence and explanation

**Can inferred data be confused with an authoritative fact or human judgment?**

- No → store the value normally.
- Yes → store source and conflict status; add confidence only when its meaning is defined.

**Would an operator later need to explain who decided, why, and from which evidence?**

- No → ordinary audit logging may be enough.
- Yes → preserve decision provenance as system state.

**Does work cross a process, queue, event, scheduled job, or remote call?**

- No → local logs are usually sufficient.
- Yes → propagate a stable operation identifier and structured context across every hop. A tracing product is optional.

## Final check

A selected mechanism should remove a specific ambiguity or failure mode. If it only adds terminology, files, or transitions, skip it.
