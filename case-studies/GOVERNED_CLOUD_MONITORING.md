# Governed Cloud-Monitoring Relationships

## Context

A central observability environment receives telemetry from many cloud accounts. Creating each technical relationship is easy, but permitting it represents a durable decision: whether the source is active, appropriately classified, approved where required, and explicitly requested for monitoring.

The risk exists in both directions:

- omitting an eligible source creates a monitoring blind spot;
- including an ineligible or unapproved source violates governance intent.

## Adoption-check result

| Gate | Result |
|---|---|
| Consequential external effect | Yes — creates and removes shared monitoring relationships |
| Durable authority | Yes — admission, approval, classification, and requested state |
| Material blast radius | Yes — fleet-wide defaults can affect many accounts |
| Evidence-sensitive action | Yes — stale or incomplete facts must not authorize monitoring changes |
| Governed recovery | Yes — repair and restoration must not invent approval |

**Adoption:** complete governed-automation layer.

## Implemented operating shape

```text
inventory facts
    -> fact refresh and draft proposal
    -> operator or bounded system decision
    -> contract validation
    -> canonical commitment
    -> effective-state derivation
    -> relationship reconciliation
    -> observation and bounded recovery
```

Discovery cannot approve monitoring. Drafts cannot trigger external mutation. One logical authority commits canonical governance state, and one mutation path changes monitoring relationships. Recovery re-drives or restores known decisions through the same gates.

## Lessons

### Discovery must not acquire admission authority

**Evidence:** implemented, tested, deployed, operationally used  
**Scope:** one cross-account monitoring system  
**Conclusion:** fact refresh and governance intent require separate ownership when discovery at fleet scale could silently enable resources.

### Requested intent and effective state may need to coexist

**Evidence:** implemented, tested, deployed  
**Scope:** lifecycle, classification, approval, and monitoring policy  
**Conclusion:** retaining the request while deriving the currently permitted result explains both what was wanted and why it is inactive.

### Recovery deserves the same authority analysis as the primary path

**Evidence:** implemented, tested, deployed  
**Scope:** interrupted promotion, reconciliation, and known-state restoration  
**Conclusion:** a repair component becomes a bypass if it can create approval or mutate shared state outside the normal gates.

### Structural boundaries can be tested

**Evidence:** tested  
**Scope:** protected storage and provider-call seams  
**Conclusion:** static checks are justified where one bypass would invalidate the operating model.

### External generality is bounded

**Evidence:** inferred  
**Scope:** one deployed internal system  
**Conclusion:** the model is credible for similar authority-bearing automation, but it is not proof that all infrastructure tooling needs a control-plane shape.

## Deliberate non-claims

The implementation does not establish equivalence to a general orchestration platform. Separation from provider clients does not prove multi-provider portability. Strong domain tests do not prove correctness under every failure mode.
