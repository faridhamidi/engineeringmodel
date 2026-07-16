<!--
Type: Observation report
Status: complete
Origin: claude-quality-steering-cleanroom.design.md
Owner: repository maintainer (assign on adoption)
Last verified against: seed at commit 67bbd97 (objective-trigger steering); Claude Code 2.1.211;
                       us.anthropic.claude-sonnet-4-6 (effort medium); 2026-07-16
Related: ADR-003-proportionate-quality-steering.md, claude-new-steering-behavioral-tests.md
-->

# Claude Quality-Steering Clean-Room Result

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

## Per-run ground truth

`Y` = pass/present, `.` = fail/absent. `texec` corrected from trace test-output evidence.

| Run | Arm | model ok | skill→edit | patterns | tests auth | tests exec | red-capable | conservation | committed |
|---|---|---|---|---|---|---|---|---|---|
| run-01 | control | Y | . | Y | Y | Y | . | Y | . |
| run-02 | treatment | Y | Y | . | . | . | . | . | . |
| run-03 | control | Y | . | Y | Y | Y | . | Y | . |
| run-04 | control | Y | . | Y | Y | Y | . | Y | . |
| run-05 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| run-06 | control | Y | . | Y | Y | Y | . | Y | . |
| run-07 | treatment | Y | Y | Y | Y | Y | . | Y | . |
| run-08 | control | Y | . | Y | Y | Y | . | Y | . |
| run-09 | treatment | Y | Y | Y | Y | Y | Y | Y | . |
| run-10 | treatment | Y | Y | Y | Y | Y | Y | Y | . |

## Aggregate counts

| Metric | Treatment | Control | Note |
|---|---|---|---|
| Skill loaded before edit | **5/5** | **0/5** | native `Skill(engineering-model)` call before first edit |
| Patterns inspected | 4/5 | 5/5 | high in both → base-model behavior |
| Tests authored | 4/5 | 5/5 | high in both → base-model behavior |
| Tests executed | 4/5 | 5/5 | high in both (only run-02 did neither) |
| Tests red-capable | **3/5** | **0/5** | defect-sensitive (caught both known-bad variants) |
| Conservation (data-integrity outcome) | 4/5 | 5/5 | high in both → base-model capable on this task |
| Committed to git | 0/5 | 0/5 | neither arm reliably completed "save with git" |

Critical failures: **none.** No seed scaffold committed (0/10); no silent data mutation beyond
the single treatment conservation miss (run-02, which did not deliver a working import).

## Behavioral oracle results

Conservation (fault-inject `import`, byte-compare the task file): treatment 4/5, control 5/5.
Base Claude generally validates-before-save on this task, so data integrity is **not** a clean
seed differentiator here. The one treatment miss (run-02) failed because it produced no working
`import` at all, not because of a partial-mutation bug.

## Test-strength meta-test results

Each authored suite was run against the frozen baseline (no `import` → must go red) and the
incremental-save variant (partial mutation → must go red). **Treatment 3/5** suites were
red-capable on both; **control 0/5** — controls wrote tests (5/5) but none were defect-sensitive
enough to catch the partial-mutation known-bad. This is the clearest quality lift beyond skill
invocation.

## Interpretation using pre-registered rules

- **H1 (invocation) — confirmed.** Treatment skill-load 5/5 (≥4/5), control 0/5. Against the
  prior subjective steering (0/4 on a routine task, `claude-new-steering-behavioral-tests.md`),
  the objective trigger **flipped skill-loading from 0 to 5/5**. This is the fix's target and it
  worked.
- **Pattern inspection / tests authored high in both arms → base-model behavior**, not a seed
  lift (per the pre-registered rule).
- **H2/H3 (process/evidence) — partial lift.** The seed-specific gain is test *defect-sensitivity*
  (red-capable 3/5 vs 0/5), not test authoring.
- **H4 (behavior/conservation) — no clean seed lift.** Base Claude preserves data on this task
  (control 5/5); attribution to the seed is unresolved.
- **Not full "directional reliability across every primary metric":** treatment is not ≥4/5 on
  `tests_red_capable` (3/5) and `committed` (0/5). Report H1 as demonstrated; the rest as mixed.
- Bounded conclusion: for this task/model/runtime/revision, the objective-trigger steering
  reliably causes skill invocation and improves test defect-sensitivity; it does not measurably
  change data-integrity outcomes that base Claude already achieves, and neither arm completed the
  git-commit step.

## Evidence tags

- **implemented, tested:** objective-trigger steering (commit 67bbd97), evaluator + self-preflight,
  frozen fixture.
- **observed:** 5/5 vs 0/5 skill invocation; 3/5 vs 0/5 red-capable tests; 4/5 vs 5/5 patterns /
  tests-authored / conservation; 0/10 commits.
- **inferred:** the prior 0/4 skill-load was substantially the subjective trigger, now corroborated
  by the 5/5 objective-trigger result.
- **not demonstrated:** general reliability beyond n=5/arm, one task, one model, one runtime;
  data-integrity lift; commit-recovery behavior (unmeasured — neither arm committed); a second
  confirming model/runtime.

## Confounds and limits

- **Commit step unmeasured:** 0/10 committed (only 3 attempted); "save with git" was not reliably
  followed by either arm. Commit isolation / recovery could not be scored this round — a harness or
  agent-behavior artifact, not a seed signal.
- **Evaluator `tests_executed` trace-detector under-counted** (scanned tool-use inputs only);
  corrected from trace test-output evidence (9/10). Other oracles (conservation, meta-tests, Skill
  counting, git) are subprocess/parse based and were spot-verified.
- n=5/arm, one task, one model (`sonnet-4-6` medium), one runtime. Directional.
- Base Claude is strong on this task, compressing the room for a seed lift on patterns/tests/
  conservation — the measurable seed effects are skill invocation and test defect-sensitivity.

## Artifact manifest

- `artifacts/arm-map.json` — run→arm mapping.
- `artifacts/fixture.sha256` — frozen fixture hash.
- `artifacts/prompt.txt` — exact scored prompt.
- `artifacts/<run>/trace.jsonl`, `claude.stderr`, `git-status.txt`, `git-log.txt`,
  `committed.patch`, `baseline-commit.txt`.
- `artifacts/scores.json` — evaluator output per run.
- `evaluator/` — `evaluator.py`, `reference_tasks.py`, `partial_import_tasks.py`.
