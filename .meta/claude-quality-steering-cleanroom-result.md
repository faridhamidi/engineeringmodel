<!--
Type: Observation report
Status: complete (see "Correction": run-02 invalid → rerun run-02b; commit metric contaminated by harness allowlist)
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
  prior subjective steering (0/4 on a routine task, `claude-new-steering-behavioral-tests.md`),
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
