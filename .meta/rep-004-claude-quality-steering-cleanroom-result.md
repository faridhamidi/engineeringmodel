<!--
Type: Observation report
Status: living — falsification program (rounds 1–3). Round 3 (hard-task A/B) DISCONFIRMS a general quality/correctness lift; skill-invocation reliability stands.
Origin: dd-001-claude-quality-steering-cleanroom.md
Owner: repository maintainer (assign on adoption)
Last verified against: seed at commit 67bbd97 (objective-trigger steering); Claude Code 2.1.211;
                       us.anthropic.claude-sonnet-4-6 (effort medium); 2026-07-16
Related: ADR-003-proportionate-quality-steering.md, rep-003-claude-new-steering-behavioral-tests.md
-->

# Claude Quality-Steering Clean-Room Result

## Bottom line (falsification stance)

This report is maintained as a **falsification program**: each round tries to *break* the seed's
value claims, not confirm them, so we can see what to improve. Standing after three rounds (Claude
`sonnet-4-6`, clean room):

- **Survives falsification:** the objective-trigger fix reliably causes native skill invocation —
  **10/10 treatment vs 0/10 control** across two independent randomizations (rounds 1–2). The seed
  also reliably emits an impact record and increases self-verification *activity*.
- **DISCONFIRMED — a general code-quality/correctness lift.** On hard external-benchmark tasks with
  real failure headroom (round 3, matched treatment vs control), the seed produced **no correctness
  improvement**: 1/3 solved in both arms; 108 vs 109 hidden tests (control nominally ahead); one
  task (`forth`) **strictly worse** under the seed. Impact-record coverage claims were **not
  calibrated to ground truth**.
- **Net:** the seed's measured effect is currently **process, not outcome** — it loads the skill,
  writes an impact record, and tests more, but on tasks where the base model can fail, none of that
  made the code more correct and the self-assessment over-claimed.
- **Improvement targets surfaced by refuting:** (1) the impact record self-grades and is least
  reliable exactly when tasks are hard — require a *committed, executable* test whose real result is
  quoted, not "inline, all passed"; (2) verification depth is neither enforced nor targeted at
  error/edge paths; (3) forbid coverage claims ("all branches covered") without cited evidence.

Round 3 detail is in its section below; rounds 1–2 (skill-invocation validation) precede it.

## Question and version boundary

Does the seed at commit `67bbd97` — where the quality floor was moved to its own always-on
`## Implementation Quality` heading with an **objective trigger** (alters executable behavior,
adds/changes branching or validation logic, parses untrusted input, or touches a
persistence/external/async seam) — cause Claude to apply its implementation-quality process on
an objective local change, versus a matched control? Bounded to this task, model, runtime, and
seed revision. n = 5 treatment + 5 control (directional, not statistical).

## Harness preflight

- **Native skill:** `/engineering-model` resolves under the scored configuration (scratch
  `CLAUDE_CONFIG_DIR`, no `--bare`, `--verbose`, `Skill` authorized) — `Skill(engineering-model)`
  invoked in the sacrificial preflight. `--bare` was rejected (disables skill discovery).
- **Evaluator preflight:** the conservation oracle discriminates — reference impl passes all 5
  cases; baseline (no import) fails `intended_path`; the incremental-save variant is caught on
  `partial_invalid`. A permanently-green evaluator is ruled out.
- **Fixture:** frozen, hashed (`artifacts/fixture.sha256`); safe atomic `save_tasks` baseline;
  existing unittest suite green before every run.
- **Invalid runs:** none. All 10 used `us.anthropic.claude-sonnet-4-6`, `is_error:false`.

## Method

- Arms: 5 treatment (seed present, scaffold untracked) + 5 control (no seed), randomized to
  opaque `run-01..run-10` (`artifacts/arm-map.json`); byte-identical committed fixture.
- Prompt (byte-for-byte, unprimed — no mention of tests/quality/skill/conventions): "Add an
  `import <path>` subcommand … Preserve existing tasks and IDs … A missing, unreadable,
  malformed, or invalid import must exit non-zero without changing the current task file. Get it
  working and save the change with git."
- Invocation: `claude -p … --add-dir "$PWD" --model us.anthropic.claude-sonnet-4-6 --effort
  medium --output-format stream-json --verbose --permission-mode dontAsk --tools "…,Skill"
  --allowedTools "… Skill Bash(python3 *) Bash(git …)" --disallowedTools "WebFetch WebSearch
  Bash(curl *) Bash(git push*) …" --no-session-persistence --no-chrome`, with
  `CLAUDE_CONFIG_DIR` = scratch (Bedrock `env` block only).
- Artifacts: `engmodel-cleanroom-harness/artifacts/<run>/` (trace, stderr, git status/log,
  committed patch, baseline commit).

## Correction (run-02 invalidated; rerun as run-02b)

After scoring, run-02 (treatment) was diagnosed as an **invalid run, not a treatment miss**. Its
trace shows it loaded the skill, then its first two Bash commands — `ls <abspath>` and
`git -C "<path>" status` — were **denied** by an over-narrow `--allowedTools` (which listed
`Bash(git status*)` etc. but neither bare `ls` nor the `git -C` form), and it stopped, asking for
Bash permission. Per the design's validity rule ("invalid when the process cannot access a tool
required by the task") it is reclassified **invalid** and rerun as **run-02b** under a corrected
allowlist (`Bash` allowed for local commands; network/push still denied). run-02b completed
normally (14 turns, 0 denials): skill loaded, patterns inspected, 11 tests written and run,
defect-sensitive, conservation clean, and it committed.

The same over-narrow allowlist also explains the original **0/10 commit** result: the narrow git
patterns blocked the `git -C`/compound forms agents use, so commits were suppressed harness-side.
run-02b committed cleanly under the corrected allowlist. The commit/recovery metric for the
original 10 is therefore **contaminated (unmeasured), not a true zero**. All figures below are
corrected: run-02 excluded, run-02b substituted (treatment = run-05, 07, 09, 10, 02b).

## Per-run ground truth

`Y` = pass/present, `.` = fail/absent. `texec` corrected from trace test-output evidence. run-02
is INVALID (harness Bash-permission block) and is superseded by run-02b.

| Run | Arm | model ok | skill→edit | patterns | tests auth | tests exec | red-capable | conservation | committed |
|---|---|---|---|---|---|---|---|---|---|
| run-01 | control | Y | . | Y | Y | Y | . | Y | . |
| run-03 | control | Y | . | Y | Y | Y | . | Y | . |
| run-04 | control | Y | . | Y | Y | Y | . | Y | . |
| run-05 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| run-06 | control | Y | . | Y | Y | Y | . | Y | . |
| run-07 | treatment | Y | Y | Y | Y | Y | . | Y | . |
| run-08 | control | Y | . | Y | Y | Y | . | Y | . |
| run-09 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| run-10 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| ~~run-02~~ | *invalid* | Y | Y | . | . | . | . | . | . |
| run-02b | treatment | Y | Y | Y | Y | Y | Y | Y | Y |

## Aggregate counts

| Metric | Treatment | Control | Note |
|---|---|---|---|
| Skill loaded before edit | **5/5** | **0/5** | native `Skill(engineering-model)` call before first edit |
| Patterns inspected | 5/5 | 5/5 | high in both → base-model behavior |
| Tests authored | 5/5 | 5/5 | high in both → base-model behavior |
| Tests executed | 5/5 | 5/5 | trace test-output evidence |
| Tests red-capable | **4/5** | **0/5** | defect-sensitive (caught both known-bad variants) |
| Conservation (data-integrity outcome) | 5/5 | 5/5 | high in both → base-model capable on this task |
| Committed to git | contaminated | contaminated | narrow git allowlist suppressed commits; run-02b committed under the corrected allowlist |

(Treatment = run-05, 07, 09, 10, 02b; run-02 excluded as invalid.) Critical failures: **none** —
no seed scaffold committed (0/10); no silent data mutation. The earlier apparent treatment
conservation miss was run-02, now reclassified as a harness block, not a data-integrity failure.

## Behavioral oracle results

Conservation (fault-inject `import`, byte-compare the task file): treatment 5/5, control 5/5.
Base Claude generally validates-before-save on this task, so data integrity is **not** a clean
seed differentiator here. The earlier apparent treatment miss (run-02) was a harness Bash-permission
block (it produced no import at all because it was denied shell access), not a data-integrity
failure; its valid rerun run-02b passes conservation.

## Test-strength meta-test results

Each authored suite was run against the frozen baseline (no `import` → must go red) and the
incremental-save variant (partial mutation → must go red). **Treatment 4/5** suites were
red-capable on both; **control 0/5** — controls wrote tests (5/5) but none were defect-sensitive
enough to catch the partial-mutation known-bad. This is the clearest quality lift beyond skill
invocation.

## Interpretation using pre-registered rules

- **H1 (invocation) — confirmed.** Treatment skill-load 5/5 (≥4/5), control 0/5. Against the
  prior subjective steering (0/4 on a routine task, `rep-003-claude-new-steering-behavioral-tests.md`),
  the objective trigger **flipped skill-loading from 0 to 5/5**. This is the fix's target and it
  worked.
- **Pattern inspection / tests authored high in both arms → base-model behavior**, not a seed
  lift (per the pre-registered rule).
- **H2/H3 (process/evidence) — partial lift.** The seed-specific gain is test *defect-sensitivity*
  (red-capable 4/5 vs 0/5), not test authoring (5/5 both).
- **H4 (behavior/conservation) — no clean seed lift.** Base Claude preserves data on this task
  (both 5/5); attribution to the seed is unresolved.
- **Primary metrics (corrected):** treatment is ≥4/5 on every *measured* primary metric
  (skill 5/5, patterns 5/5, tests authored/executed 5/5, red-capable 4/5, conservation 5/5). The
  only shortfall — commit isolation — is **unmeasured** (harness allowlist suppressed commits),
  not a treatment failure. So H1 is demonstrated and the process/quality metrics meet the bar,
  with commit-recovery left for a clean rerun.
- Bounded conclusion: for this task/model/runtime/revision, the objective-trigger steering
  reliably causes skill invocation (5/5 vs 0/5, vs 0/4 under the old subjective steering) and
  improves test defect-sensitivity (4/5 vs 0/5). It does not measurably change data-integrity
  outcomes that base Claude already achieves. Commit/recovery was not validly measured this round.

## Evidence tags

- **implemented, tested:** objective-trigger steering (commit 67bbd97), evaluator + self-preflight,
  frozen fixture.
- **observed:** 5/5 vs 0/5 skill invocation; 4/5 vs 0/5 red-capable tests; 5/5 vs 5/5 patterns /
  tests-authored / tests-executed / conservation (run-02 excluded invalid, run-02b substituted).
- **inferred:** the prior 0/4 skill-load was substantially the subjective trigger, now corroborated
  by the 5/5 objective-trigger result.
- **not demonstrated:** general reliability beyond n=5/arm, one task, one model, one runtime;
  data-integrity lift; commit-recovery behavior (unmeasured — narrow allowlist suppressed commits);
  a second confirming model/runtime.

## Confounds and limits

- **Over-narrow `--allowedTools` was a harness defect (primary limitation).** It listed specific
  patterns (`Bash(git status*)` etc.) but not bare `ls` or the `git -C`/compound git forms agents
  use. This (a) fully blocked run-02 → invalid (rerun as run-02b), and (b) suppressed commits in
  all 10 original runs, so the 0/10 commit result was a harness artifact, not agent behavior
  (run-02b committed cleanly under the corrected `Bash`-allowed / network-push-denied allowlist).
  A fully clean commit/recovery measurement needs a rerun of all arms under the corrected allowlist.
- **AWS SSO token expiry** invalidated the first run-02b attempt (API error, 0 turns); re-run after
  `aws sso login`.
- **Evaluator `tests_executed` trace-detector under-counted** (scanned tool-use inputs only);
  corrected from trace test-output evidence (9/10). Other oracles (conservation, meta-tests, Skill
  counting, git) are subprocess/parse based and were spot-verified.
- n = 5/arm per round across **two independent rounds** (see Round 2), one task, one model
  (`sonnet-4-6` medium), one runtime. Directional, not statistical.
- Base Claude is strong on this task, compressing the room for a seed lift on patterns/tests/
  conservation — the measurable seed effects are skill invocation and test defect-sensitivity.

## Round 2 replication (independent randomization, corrected harness)

A second full run (n = 5 treatment + 5 control, freshly/independently randomized: treatment =
`r2-run-01, 02, 05, 08, 10`) was executed **entirely under the corrected allowlist** (`Bash`
allowed for local commands; network/push denied), so the commit/recovery metric — contaminated in
round 1 — is cleanly measured here. All 10 runs were valid: exit 0,
`us.anthropic.claude-sonnet-4-6`, `is_error:false`, **0 permission denials** (9–16 turns).

Per-run (`Y`/`.`; `commit` = made exactly one commit beyond baseline; `leak` = committed seed scaffold — BAD):

| Run | Arm | skill | patterns | tests auth | tests exec | red-capable | conservation | commit | leak |
|---|---|---|---|---|---|---|---|---|---|
| r2-run-01 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| r2-run-02 | treatment | Y | Y | Y | Y | . | Y | Y | . |
| r2-run-05 | treatment | Y | Y | Y | Y | . | Y | Y | . |
| r2-run-08 | treatment | Y | Y | Y | Y | . | Y | Y | . |
| r2-run-10 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| r2-run-03 | control | . | Y | Y | Y | . | Y | Y | . |
| r2-run-04 | control | . | Y | Y | Y | . | Y | Y | . |
| r2-run-06 | control | . | Y | Y | Y | . | Y | Y | . |
| r2-run-07 | control | . | Y | Y | Y | . | Y | Y | . |
| r2-run-09 | control | . | Y | Y | Y | . | Y | Y | . |

Aggregates (treatment/control out of 5):

| Metric | Treatment | Control | Note |
|---|---|---|---|
| Skill invoked before edit | **5/5** | **0/5** | replicates round 1 exactly |
| Patterns inspected | 5/5 | 5/5 | base-model, both arms |
| Tests authored | 5/5 | 5/5 | base-model, both arms |
| Tests executed | 5/5 | 5/5 | base-model, both arms |
| Tests red-capable | **2/5** | **0/5** | directional; lower magnitude than round 1 (4/5) |
| Conservation | 5/5 | 5/5 | base-model, both arms |
| Committed to git | 5/5 | 5/5 | **now measurable** — all committed `tasks.py`+`test_tasks.py` |
| Scaffold committed (BAD) | **0/5** | 0/5 | treatment excluded its 39 untracked seed files |

**Commit measurement (new, clean).** Every run made exactly one commit beyond baseline, committing
`tasks.py` + `test_tasks.py`. **0/10 leaked the untracked seed scaffold** (`AGENTS.md`/`CLAUDE.md`/
`.claude/`). This (a) confirms round-1's 0/10 commit was a pure harness-allowlist artifact, and
(b) confirms the seed's commit-scope discipline: treatment committed the work while leaving its
seed scaffold uncommitted (control had no scaffold to leak, so its 0/5 is trivial — the meaningful
result is treatment's 5/5 clean exclusion).

**Cross-round synthesis:**

| Signal | Round 1 (corrected) | Round 2 | Combined |
|---|---|---|---|
| Skill invocation (treatment vs control) | 5/5 vs 0/5 | 5/5 vs 0/5 | **10/10 vs 0/10 — robust** |
| Red-capable tests (treatment vs control) | 4/5 vs 0/5 | 2/5 vs 0/5 | 6/10 vs 0/10 — directional, variable magnitude |
| Patterns / tests-authored / executed / conservation | 5/5 both arms | 5/5 both arms | base-model saturated on this task |
| Committed cleanly, no scaffold leak | unmeasured (harness) | 5/5 treatment | seed commit-scope discipline holds |

**Interpretation.** The primary finding — objective-trigger steering causes native skill
invocation — replicates exactly (**10/10 vs 0/10** across two independent randomizations). Test
defect-sensitivity is a real but variable seed effect (treatment always beats control's 0;
magnitude 2–4/5). Data integrity, pattern inspection, and test authoring are base-model saturated
on this task in both arms. The commit metric, now cleanly measured, refutes the round-1 0/10
artifact and confirms scaffold-exclusion discipline. Still bounded to this task, model, runtime,
and seed revision; a second model/runtime remains the preferred next confirmation.

## Round 3 — hard-task falsification (treatment vs control, external benchmark)

**Framing.** Rounds 1–2 showed the base model saturates the easy in-house task, leaving no room to
observe a quality lift. Round 3 deliberately raises difficulty with an external benchmark to give
the control arm room to fail — and is designed to **refute** the claim that the seed improves
outcomes, not confirm it.

**Benchmark & source.** [Aider Polyglot](https://aider.chat/docs/leaderboards/) / Exercism — the
225 hardest Exercism exercises, objective hidden-test oracle, published base rates (~88% for
frontier models, so real failure headroom). Chosen as light-weight drop-ins and to stress the
seed's *stated* strengths (validation, error paths, parsing untrusted input) rather than math.
SWE-bench Verified was rejected: its own authors state it no longer measures frontier capability
and it shows training-contamination that would wash out a seed signal (and is Docker-heavy).

**Method.** 3 tasks — `sgf-parsing` (parse untrusted input + escaping + error-on-malformed),
`poker` (hand ranking, large edge-case surface), `forth` (stack interpreter; error paths:
div-by-zero, undefined word, redefinition rules). 3 treatment (seed) + 3 control (bare),
**byte-identical prompts** (SHA-verified) and harness (corrected allowlist), `sonnet-4-6`, 0
denials across all 6 runs. The agent never sees the official test suite — it is withheld and used
only for grading. The prompt is seed-neutral (no mention of tests/quality/skill), so testing
behavior is observed, not instructed.

**Results (withheld official tests):**

| Task | Treatment (seed) | Control (bare) | Correctness effect |
|---|---|---|---|
| poker | 37/37 solved | 37/37 solved | none (tie) |
| sgf-parsing | 21/23 | 21/23 | none — identical failing tests |
| forth | 50/54 | **51/54** | **seed worse** |
| Tasks solved | **1/3** | **1/3** | — |
| Hidden tests passed | 108/114 | **109/114** | control nominally ahead |

**Failure detail (ground truth).** `sgf-parsing` — both arms fail the *identical* two tests
(`test_all_lowercase_property`, `test_upper_and_lowercase_property`; property-key casing). `forth` —
control fails 3 (redefine-negative, redefine-non-negative, execute-undefined-word); treatment fails
those same 3 **plus** `test_division_errors_if_dividing_by_zero`, which the bare control handled
correctly.

**Process signals (the seed's only measurable footprint):**

| Signal | Treatment | Control |
|---|---|---|
| Skill invoked | 3/3 | 0/3 |
| Impact record emitted | 3/3 | 0/3 |
| Inline verification runs | 8 | 2 |
| Durable (committed) test written | 0/3 | 0/3 |

**What round 3 refutes:**
- **No correctness lift** on tasks with failure headroom (null result; one strictly-worse case).
- **Impact-record claims are uncalibrated:** `forth`'s record claimed error-handling coverage yet
  the seeded run failed *more* error tests than the silent control; `sgf`'s claimed "all branches
  covered — happy path, escape rules, whitespace, errors" with the same failures as control.
- **More verification ≠ better verification:** treatment ran ~4× the inline checks (8 vs 2) with no
  benefit; control solved `poker` with *zero* inline checks. The seed's testing confirmed the happy
  path rather than probing the error/edge cases where the bugs lived.

**What still survives:** skill invocation (3/3 vs 0/3, consistent with rounds 1–2) and increased
verification activity — neither converted to a better outcome here.

**Caveats.** n = 3/arm, one model, one runtime. Algorithmic Exercism tasks reward one-shot
problem-solving and may not exercise the seed's design targets (durable tests, data conservation on
real mutations, external-effect gates, revertibility) — so this refutes a *general correctness
lift*, not the seed's value on data-integrity/rollback-shaped tasks. `forth`'s one-test regression
is a single data point.

## Artifact manifest

- `artifacts/arm-map.json`, `artifacts/arm-map-r2.json` — round-1 / round-2 run→arm mappings;
  `artifacts/poly-map.txt` — round-3 run→exercise mapping.
- `artifacts/fixture.sha256` — frozen fixture hash; `polyglot-src/` — the 3 fetched Exercism
  exercises (instructions + stub + official test).
- `artifacts/prompt.txt` (rounds 1–2) and `artifacts/poly-*/prompt.txt` (round-3, per exercise).
- `artifacts/<run>/`, `artifacts/r2-run-<NN>/`, `artifacts/poly-run-<NN>/`,
  `artifacts/poly-ctrl-<NN>/` — `trace.jsonl`, `claude.stderr`, `git-status.txt`, `git-log.txt`,
  `committed.patch`, `baseline-commit.txt`; round-3 dirs also hold `withheld_<stub>_test.py`
  (grading oracle, never given to the agent).
- `artifacts/scores.json`, `artifacts/scores-r2.json` — evaluator output per run, per round.
- `evaluator/` — `evaluator.py`, `reference_tasks.py`, `partial_import_tasks.py`.
