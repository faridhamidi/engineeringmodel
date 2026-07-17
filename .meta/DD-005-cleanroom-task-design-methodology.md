<!--
Type: Design document
Status: living — consolidates the clean-room task-design methodology used across rounds 3-5
Origin: extracted from the out-of-repo harness briefs (CODEX-TASK-DESIGN-BRIEF.md, -v2.md) and
        the practice recorded in REP-005-falsification-program-narrative.md and
        REP-006-prior-art-related-work.md
Owner: repository maintainer (assign on adoption)
Last verified against: Round 5 (2026-07-17); Claude Code 2.1.212; us.anthropic.claude-sonnet-4-6
Supersedes / superseded by: extends DD-003-claude-quality-steering-cleanroom.md (which covers only
the fixed-task, round-1/2 protocol); this document covers task *authoring* for rounds 3 onward
-->

# Design — Clean-Room Task-Design Methodology (Rounds 3-5 and onward)

## 1. Scope and relationship to DD-003

`DD-003-claude-quality-steering-cleanroom.md` designs a single **fixed task** (the import
subcommand) and the treatment/control protocol around it. That protocol still stands for
any round using an already-built task.

This document covers the harder, separate problem that emerged starting at Round 3: **how
do we build the *next* task** so it is uncontaminated, discriminating, and gradeable —
without secretly biasing the result toward or against the seed? It is the methodology, not
a single experiment; it is meant to be reused every time a new clean-room task is needed.

## 2. Decision question

Given the seed's public claims (§3), how do we produce a task, a withheld oracle, and a
difficulty screen that can **falsify** a specific claim, while keeping the task designer
blind to the seed's steering text and to the treatment arm's behavior?

## 3. The seed's public claims (design against these only)

A task-design pass must target one or more of these claims. A designer must not read the
seed's steering/skill text to reverse-engineer behavior — only these claims are in scope:

1. **Testing discipline** — writes and runs real tests, including failure branches.
2. **Input validation & error paths** — rejects malformed/adversarial input.
3. **Data conservation & atomicity** — never leaves persisted state half-mutated on failure.
4. **Invariant preservation** — holds stated invariants across operations and against
   existing state.
5. **Idempotency / recovery** — re-running or resuming an interrupted operation converges.
6. **Revertibility / commit hygiene** — commits only intended changes.
7. **Calibrated self-assessment** — an impact record whose claims match ground truth.

## 4. Why contamination and saturation force this design (lessons, not opinions)

- **Public benchmarks are contaminated.** Frontier models were plausibly trained on
  Exercism/LeetCode/SWE-bench items; a model that recalls the answer never exercises the
  discipline under test. Signature: identical, suspiciously-clean pass rates in both arms
  (Round 3's `poker`, 37/37 both arms). Rule: invent the domain and format; never reuse a
  named public problem, kata, or file format.
- **Self-contained, single-file tasks saturate.** `sonnet-4-6` aces "validate-then-atomic-
  save" tasks nearly every time (Round 4: 4 of 5 candidates scored a clean sweep on both
  controls). A saturated task cannot discriminate — both arms pass, and "the skill loaded"
  becomes the only observable difference. Rule: target tasks whose engineering failure mode
  is **recovery, idempotent retry, conflict against already-persisted state, cross-file
  reconciliation, or corrupt-state detection** — axes with demonstrated control-arm
  headroom (Round 4B: 4 of 8 candidates showed real control failures on this axis).
- **The failure mode must be an engineering failure, not an algorithm-discovery failure.**
  The seed claims discipline, not cleverness; a task that is hard because it requires a
  clever algorithm does not test the seed's claims. The failure a wrong solution produces
  should be data corruption, a missed edge/error case, a non-atomic effect, or a broken
  invariant — never "didn't find the trick."

## 5. The Contract-Coverage Gate (mandatory, pre-screen)

This is the fix for the defect that invalidated Rounds 4B and 5: an oracle can prove
**three-way discrimination** (reference passes every subcase; a wrong solution fails; the
bare fixture fails) while still not covering the task's full contract — a differently-wrong
solution could then pass by violating an *untested* clause. "Green preflight" is not proof
of completeness.

**Rule.** Before any control run, produce a coverage matrix: one row per explicit clause in
the task's README (every rejection condition, invariant, and success/idempotency/recovery
behavior, enumerated at the finest granularity the README states), each mapped to a
concrete hidden subcase that exercises it, with a byte-conservation assertion where the
README requires one. A clause with no subcase **fails the gate** — the task is dropped or
redesigned before screening, never patched afterward.

**Known failure mode of the gate itself (Round 5):** the gate can be satisfied
*syntactically* (every clause has a *named* subcase) without being satisfied *semantically*
(the subcase does not exercise the clause at its stated granularity — e.g. testing only one
kind of corruption when the README implies several). Both the coverage matrix and its
audit must be checked against the README text, not against the presence of a plausibly-
named test method.

**The gate must be bounded, not unsatisfiable.** "Finest granularity" combined with "never
repair post-screen" can be applied so strictly that a finer subcase can always be demanded,
causing every slate to self-invalidate (this happened twice — Rounds 4B and 5). The bounded
version: the gate is satisfied when every clause has **at least one** subcase with a
conservation assertion, checked **before** any control run. Once a task passes the gate and
enters the difficulty screen, only *outcome-derived* defects (a real, observed grading bug)
justify invalidation — not a hypothetical finer subcase invented after the fact.

## 6. Oracle-preflight (three-way discrimination)

Independently of the coverage gate, every oracle must be run, before any control run,
against:
- a **reference solution** (must pass every subcase and the conservation check);
- at least one, preferably two, **plausible-wrong solutions** representing realistic
  undisciplined shortcuts (must fail the subcase(s) their shortcut violates, and nothing
  else spuriously);
- the **bare fixture**, unimplemented (must fail everything).

Record the pass/fail matrix. A task whose plausible-wrong solution passes everything the
reference does is not discriminating and must be redesigned.

## 7. Difficulty screen (control-only)

- Run the **control (bare)** arm **twice per candidate task**, independently, before
  building any treatment arm. Nondeterminism means a single control run is not evidence:
  the same task can pass once and fail once (observed directly — Round 5's `shard-wake`:
  28/28 then 27/28, failing `replace_3_failure_retry_converges`).
- **Keep** a task only if at least one control run fails a meaningful hidden subcase.
  **Prefer** a task where both controls fail the same subcase (a reliable-fail task) over
  one where only one of two fails (a flaky-fail task) — but flaky-fail tasks are still
  usable if there is no reliable-fail alternative; label them explicitly as flaky and plan
  for **pass-rate** measurement (§9), not single-run pass/fail.
- **Selection criterion is difficulty only.** Never select, discard, or retune a task based
  on how the *seed* would perform on it. The treatment arm must not be run during design.

## 8. The bias firewall

- **Author/analyst separation.** The person analyzing the seed's results should not also be
  the one writing the tasks that will be used to judge it. Use an independent designer
  (a separate model session or a separate person) briefed only on §3's public claims.
- **No treatment during design.** The designer never runs, reads, or infers from the
  treatment arm while building or screening tasks.
- **No post-screen repair on outcome grounds.** If a real defect is found after screening
  has begun, the task is invalidated and excluded, never patched-and-rerun with the same
  screening data — patching after seeing outcomes contaminates the measurement.
- **Physical workspace isolation (strongest available guarantee).** An instruction not to
  read prior rounds' work is weaker than making it physically unreachable: an autonomous
  designer can `ls`/`grep`/`cat` anything present in its workspace. Give the designer a
  workspace containing *only* the current brief and the credentials it needs to run
  control screens — not the prior rounds' task pools, scores, or reports. Check any copied
  configuration for embedded breadcrumbs (e.g. session directories named after prior task
  identifiers) before use.
- **Anti-contamination.** Invent the domain and format; do not reuse a named public
  problem, kata, benchmark item, or well-known file format. If a task feels recognizable,
  redesign it.
- **Independent verification of self-reported invalidation.** A designer that
  self-invalidates a slate (as happened in Rounds 4B and 5) should still have its diagnosis
  checked against the actual artifacts — run the oracle yourself against the reference and
  wrong variants, and re-grade the specific control trial that reportedly failed, before
  accepting the invalidation as final. A defect can be real without covering the specific
  subcase the eventual measurement would use, in which case the task may still be usable
  with the defect disclosed (see REP-005 §8 for a worked example).

## 9. Measurement: pass-rate, not single-run pass/fail

Because control behavior is nondeterministic near the difficulty boundary, and the most
informative tasks sit near a 50% control pass rate, a single treatment run vs a single
control run is not a measurement. Compare **pass rates across repeated trials per arm**
(a practical minimum is on the order of ten trials per arm per task), reporting the rate
with an interval and treating the result as directional unless the trial count is large
enough to support a formal test.

## 10. Structure-vs-content controls (borrowed, see REP-006)

Independent published studies of comparable prompt-skill claims (REP-006) show that an
apparent effect from a steering scaffold is frequently the *structure* of the scaffold
(section headers, having any organized instructions at all) rather than its specific
*content* (the procedural or philosophical substance). A design that only compares
seed-present vs bare cannot separate these. Where the question is whether the seed's
*content* matters, add:
- a **labels-only** arm — the seed's section headers with the procedure stripped out;
- a **length-matched placebo** arm — generic best-practice text of equal length, no seed
  content.
Both are **seed-derived**, not task-derived, so adding them does not touch the task-design
firewall in §8. See `DD-004-structure-vs-content.md` for a worked design using this pattern.

## 11. Harness protocol (shared across rounds)

- **Runtime:** Claude Code (version recorded per round; 2.1.211 for Round 1, 2.1.212 from
  Round 2 onward). **Model:** `us.anthropic.claude-sonnet-4-6`, effort `medium`.
- **Isolation:** a scratch `CLAUDE_CONFIG_DIR` containing only the provider `env` block
  (no operator plugins, no prior session history). Do **not** use `--bare` — it also
  disables native skill discovery, which the treatment arm requires.
- **Tool policy:** an explicit, broad local `--allowedTools` (bare `Bash`, not narrow
  per-subcommand patterns — narrow allowlists have twice produced false harness failures
  that were misread as agent behavior) with `--disallowedTools` denying network and
  `git push`/`pull`/`fetch`.
- **Required flags:** `--verbose` (required for `--output-format stream-json`),
  `--permission-mode dontAsk`, `--no-session-persistence`, `--no-chrome`.
- **Prompt discipline:** the task prompt is byte-identical across arms (verify by hash) and
  seed-neutral — it must never mention tests, quality, conventions, validation, atomicity,
  or the skill by name. Behavior is observed, not instructed.
- **Trial construction:** treatment = run `seed/generate.py` into the trial directory
  (scaffold stays **untracked**) before committing the task fixture; control = commit the
  same fixture with no scaffold. This also lets scaffold-leak-into-commit be measured for
  free.
- **Artifact retention:** keep every trace, stderr stream, git log/status/diff, and score
  per run. Do not delete trial directories after scoring; they are the audit trail.

## 12. Reusable process (checklist form)

1. Pick a public claim (§3) and a target axis with demonstrated headroom (§4).
2. Author 5-8 candidate tasks: fixture, seed-neutral prompt, README contract, withheld
   oracle, reference solution, ≥1 plausible-wrong solution.
3. Run the Contract-Coverage Gate (§5) per task. Drop or redesign any failure before
   proceeding — do not screen a task that has not passed the gate.
4. Run oracle-preflight (§6) per task. Drop or redesign any task that fails to discriminate.
5. Run the difficulty screen (§7): two control runs per task, no treatment. Keep only tasks
   with genuine headroom; label reliable-fail vs flaky-fail.
6. Independently verify any self-reported pass/fail/invalidation against the raw artifacts
   (§8) before trusting it.
7. Decide the measurement: single-run pass/fail only for reliable-fail tasks with enough
   surviving candidates; pass-rate over repeated trials (§9) for flaky-fail tasks or small
   slates. Add structure/content controls (§10) if that is the open question.
8. Pre-register the hypotheses, exact hidden subcases, and stopping rule before running the
   treatment arm.
9. Run the treatment arm, grade with the withheld oracle, and report — including the
   provenance of any rescued or previously-flagged task, and all confounds found along the
   way.

## 13. Related records

- `DD-003-claude-quality-steering-cleanroom.md` — the fixed-task protocol this document
  extends.
- `REP-004-claude-quality-steering-cleanroom-result.md` — results produced under this
  methodology (Rounds 1-3, corrected).
- `REP-005-falsification-program-narrative.md` — the full narrative, including the two
  self-invalidation episodes that motivated §5, §7, and §8.
- `REP-006-prior-art-related-work.md` — the external studies behind §10.
- `DD-004-structure-vs-content.md` — the terminal experiment applying §10.
