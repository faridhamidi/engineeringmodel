<!--
Type: Architecture decision record
Status: accepted
Origin: seed-cleanroom-observation.md and seed-codex-cleanroom.md
Owner: repository maintainer (assign on adoption)
Last verified against: local implementation dated 2026-07-16
Supersedes / superseded by: extends ADR-001-builder-accessible-layer.md and ADR-002-share-ready-seed.md
-->

# ADR-003: Put A Proportionate Quality Floor In Always-On Steering

## Decision

Put the minimum code-quality behavior that must reliably occur in the marked always-on
steering block, then use the `engineering-model` skill for its checkable execution
criteria and progressively disclosed testing depth.

- Every non-trivial implementation loads the installed skill before editing. This is a
  direct always-on instruction, not a hoped-for result of model invocation metadata.
- Changed load-bearing behavior gets the lightest executable test that would fail on a
  realistic defect. A test is claimed as enforcement only when its artifact exists and
  it ran successfully for the increment.
- External, asynchronous, and persistence seams get diagnostic context only when an
  important failure would otherwise be silent or difficult to recover. Logging every
  function is explicitly rejected.
- Data mutation must not silently discard or corrupt accepted data. Validation,
  atomicity, and recovery mechanisms remain risk-selected rather than universally
  prescribed.
- When no test or diagnostic is proportionate, the result records why. Test counts,
  coverage thresholds, and universal seam logging are not part of the floor.
- Before treating git as the recovery substrate, the agent verifies that the project
  can create a checkpoint. A constrained runtime reports the missing recovery mechanism
  instead of creating a shadow repository or claiming a checkpoint that does not exist.

The canonical steering remains
[`skills/engineering-model/assets/steering.md`](../skills/engineering-model/assets/steering.md).
The detailed completion criteria remain in the
[`engineering-model` skill](../skills/engineering-model/SKILL.md). Native instruction
files and packaged templates continue to carry byte-identical copies of the marked
block.

## Rationale

The Kiro observation produced tests, seam logging, validation, and atomic writes in all
ten runs, but both arms inherited the operator's always-on quality rules. That round
therefore demonstrates the strength of an always-on quality channel, not a quality lift
from this seed.

The follow-up removed that confound across Codex and Claude. Bare and seeded runs wrote
no tests and no seam logging in all eight executions. The on-demand skill was also
inconsistently consulted, and one Codex run claimed `Enforcement: direct test` without a
test artifact. By contrast, the short always-on commit-scope rule changed concrete
behavior across both runtimes.

The reliable channel should therefore carry the minimum behavior, while the skill
carries branches, reference material, and exhaustive completion criteria. This follows
the skill information hierarchy: immediate actions stay in the always-on front and
branch-specific testing mechanics remain behind context pointers. The shared leading
phrases—`revertible envelope`, `load-bearing behavior`, and `lightest test`—keep the
front and the skill aligned without duplicating the full testing model.

## Consequences

- The always-on block is longer because quality, skill loading, and recovery
  availability are now load-bearing instructions.
- Small edits and throwaway artifacts remain light: the quality mechanism is gated by
  non-trivial implementation and by changed load-bearing behavior.
- A direct-test claim now requires an artifact and observed execution result. Prose-only
  confidence is reported as no enforcement.
- The seed does not mandate the Kiro operator's house standard. It preserves the useful
  outcomes while rejecting universal tests, universal logging, and implementation
  prescriptions that ignore cost of error.
- Structural witnesses can prove block parity and required wording, but cannot prove
  runtime obedience or quality improvement. A new matched clean-room run is required
  before claiming behavioral efficacy for this revision.

## Evidence

**Implemented, tested:** canonical always-on block, native-surface parity, skill
completion criteria, impact-record evidence fields, constrained-git reporting, and
minimal falsifiers that detect removal of each new load-bearing norm.

**Observed:** the pre-change Kiro condition produced tests and logging in 10/10 runs
under ambient always-on quality steering; the pre-change bare Codex and Claude
conditions produced neither in 0/8 runs; skill consultation and its impact ritual were
inconsistent.

**Not demonstrated:** post-change runtime adherence, a measured quality lift, effects
beyond the tested models and task, or operational defect reduction.
