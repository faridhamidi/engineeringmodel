---
name: engineering-model
description: Revertible-envelope guidance for classifying engineering changes, preserving Core boundaries, and selecting governed controls. Use when planning or changing a non-trivial system, when work touches shared or external state, or when authority, evidence, blast radius, or recovery affects what may safely happen.
---

# Engineering Model

Keep work inside a **revertible envelope**: act autonomously while authoring remains
local and recoverable, and require explicit human approval before an external-substrate
effect. Use the lightest engineering control that protects the actual risk.

## 1. Classify The Work

Identify each intended action and answer:

- Does it change or reach shared or external state?
- Can the authoring change be undone locally in one step?
- Does the next action itself affect an external substrate?

Treat uncertainty as above the blast-radius line. Do not treat git as an undo mechanism
for an external effect.

**Complete when:** every intended action is classified as local and reversible, above
the line for further judgment, or an external effect requiring approval.

## 2. Select The Layer

For every non-trivial codebase, read [Core Hygiene](references/core-readme.md) and use
[Starting Foundation](references/core-foundation.md) to identify decision owners,
external-effect boundaries, shared language, operation context, and the smallest useful
checks.

Read only the additional branch the work earns:

- When shared states, actions, transitions, reasons, outcomes, or recovery terms have
  become load-bearing, read
  [Semantic Consistency](references/core-semantic-consistency.md).
- When selecting test intent or structural checks, read
  [Testing](references/core-testing.md).
- When recording direction, an implementation plan, or a durable decision, read
  [Documentation](references/core-documentation.md).
- When several stable cross-cutting rules need shared lifecycle, ownership, ratchets,
  or audit output, read
  [Conformance Harness](references/core-conformance-harness.md).
- When the system performs a consequential shared or external effect, orient with the
  [Governed Automation overview](references/governed-readme.md), then read the
  [Governed Automation Adoption Check](references/governed-adoption-check.md) before
  selecting any governed model. If the gate is crossed, continue through the
  [Decision Tree](references/governed-decision-tree.md) and the canonical
  [Models](references/governed-models.md).
- When the complete authority chain is justified, read
  [Automated Authority](references/governed-automated-authority.md) and
  [Principles](references/governed-principles.md). Use
  [Vocabulary](references/governed-vocabulary.md) only to resolve local terms.

**Complete when:** the adoption is recorded as Core only, selected governed models, or
the complete governed layer, with every added mechanism tied to a concrete trigger and
every rejected mechanism left out.

## 3. Protect The Load-Bearing Seams

Implement the selected controls in the product repository. Prefer a direct test before
a ratchet, a ratchet before a manifest-backed harness, and repository-host or substrate
controls when actual admission or authority must be enforced.

Do not claim an authority boundary unless distinct identities and permissions prevent
weaker components from exercising stronger powers. Do not let missing, stale,
conflicting, or unreadable evidence authorize a consequential action. Route recovery
through the normal authority path.

**Complete when:** every consequential decision and external effect has a named owner,
the current implementation satisfies its declared enforcement level, and a known-bad
case proves each new checker detects the prohibited behavior.

## 4. Operate Inside The Envelope

Use git for local authoring checkpoints. Never commit secrets, generated junk, or
unrelated user changes. Before any external-substrate effect, stop, state the target,
consequence, reversibility, and proposed action, then obtain explicit human approval.
Approval for one described effect does not authorize a broader or materially different
effect.

**Complete when:** local changes are recoverable, verification results are recorded,
and no external effect occurred without approval for that exact effect.

## 5. Report The Result

Include this impact record in the final change summary:

```text
Layer: core only | selected governed models | complete governed layer
Semantic impact: none | local | shared
Enforcement: none | direct test | ratchet | harness rule | protected control
Authority impact: none | governed review required
External effects: none | approved and performed | approval required
Residual risk:
```

**Complete when:** each field reflects the implemented behavior and evidence without
promoting structural checks into claims of runtime enforcement.

## Install The Steering

When installing this skill, place [the steering block](assets/steering.md) in the
runtime's always-on instruction surface. Use the packaged
[AGENTS.md template](assets/AGENTS.md) for Codex-compatible runtimes and the packaged
[CLAUDE.md template](assets/CLAUDE.md) for Claude. Preserve the marked block verbatim so
package validation can detect drift. If the runtime has no always-on instruction
surface, tell the user that the skill remains on-demand and the external-effect pause
is not continuously steered.

**Complete when:** every native instruction file used by the runtime loads the steering
on every turn, the skill can be invoked as `$engineering-model`, and each installed
block is identical to the packaged canonical block.
