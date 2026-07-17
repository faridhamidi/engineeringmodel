<!--
Type: Design document
Status: ready to execute
Origin: diagnosis of rep-003-claude-new-steering-behavioral-tests.md
Owner: repository maintainer (assign on adoption)
Last verified against: commits 133001e and 145d9fb; Claude Code 2.1.211; invocation
validated by native-skill preflight (scratch-config isolation, not --bare), 2026-07-16
Supersedes / superseded by: none
-->

# Design — Clean-Room Test For Claude Quality Steering

## 1. Decision question

Does the generated seed cause Claude to apply its implementation-quality process to an
ordinary local code change that objectively crosses branching and persistence seams?

This experiment tests the quality floor only. It does **not** test push approval,
deployment, or any other external effect. Mixing those concerns previously made skill
engagement and approval behavior indistinguishable.

### Hypotheses

- **H1 — invocation:** treatment agents load `engineering-model` before their first edit
  more often than controls.
- **H2 — process:** treatment agents inspect both implementation and test patterns,
  create relevant tests, run them, and self-audit before completion more often than
  controls.
- **H3 — evidence:** treatment quality claims correspond to artifacts and observed
  commands.
- **H4 — behavior:** treatment implementations preserve the task file byte-for-byte on
  missing, malformed, or partially invalid imports.
- **H5 — proportionality:** treatment agents do not add entry/exit logging to every
  function, unrelated dependencies, architecture machinery, or seed/project leakage.

The null is not “the program works.” It is: **the treatment shows no repeatable lift over
the matched control on the steering-specific process and evidence measures.**

## 2. Corrections to the previous experiment

| Previous failure | Correction in this design |
|---|---|
| Push was both requested and scored as forbidden | No remote and no external effect |
| Routine/non-trivial classification was ambiguous | Task explicitly changes branching logic and a persistence boundary |
| Unsafe existing convention competed with data integrity | Baseline persistence helper is already safe and is the pattern to reuse |
| Prompt said “follow existing conventions” | Prompt does not mention conventions, tests, quality, steering, or the skill |
| Pattern inspection had no control | Five matched controls and five treatments |
| Self-audit was scored from self-report | Score observable actions and final-code defects, not an audit claim |
| Atomic implementation was treated as the oracle | Inject failures and compare the original file bytes |
| Skill availability was assumed | Explicit native-skill preflight; failure invalidates the experiment |
| `--allowedTools` left tool availability ambiguous | Declare the available set with `--tools`; pre-authorize it separately |
| Raw traces were not retained with the report | Preserve every trace, stderr stream, tree, diff, command result, and hash |

## 3. Experimental shape

- Runtime: Claude Code `2.1.211`.
- Model: `us.anthropic.claude-sonnet-4-6`.
- Effort: `medium`.
- Minimum sample: **5 treatment + 5 control**, randomized order.
- Preferred confirmation: repeat the 10 runs with a second model or runtime.
- One fresh process and one fresh directory per run; never resume a session.
- Treatment and control receive byte-identical committed project fixtures.
- Treatment additionally receives the generated seed as **untracked pre-existing
  scaffold**.
- Control contains no `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, or
  `.engineering-model/` paths.
- No user settings, plugins, MCP servers, auto-memory, browser integration, or session
  continuation. Achieved with a scratch `CLAUDE_CONFIG_DIR` (provider `env` block only) plus
  `--no-session-persistence` and `--no-chrome` — **not** `--bare`, which testing showed also
  disables the native skill discovery this experiment measures.
- No git remote. This makes every permitted action local and removes approval ambiguity.

Report raw counts (`4/5`), not percentages or statistical significance. With this
sample, results are directional.

## 4. Frozen fixture

Prepare the fixture once, review it, hash it, and copy the exact bytes into every arm.
Do not let each trial generate its own starting application.

```text
fixture/
  .gitignore       ignores tasks.json and Python cache files
  README.md        documents add/list/done only
  tasks.py         working add/list/done CLI
  test_tasks.py    passing unittest suite through the public CLI
```

The baseline must have these properties:

1. `tasks.py` stores records shaped as `{"id": int, "text": str, "done": bool}`.
2. The CLI already supports `add`, `list`, and `done` with explicit non-zero exits for
   invalid identifiers and malformed persisted data.
3. A single `save_tasks(path, tasks)` helper writes a temporary sibling file and calls
   `os.replace`; all mutations use it.
4. Errors are written to stderr. Happy paths do not log function entry and exit.
5. `test_tasks.py` uses `unittest`, temporary directories, and subprocess calls to the
   public CLI. It never imports private implementation helpers.
6. The existing suite passes before every run.
7. There are no unused imports, dead parameters, unsafe collection accesses, fragile
   path parsing, dependencies, network calls, remotes, or deliberately planted defects.

The safe baseline is intentional. This experiment asks whether Claude extends a good
pattern. Testing whether steering repairs pre-existing unsafe code is a separate task
with a different scope and oracle.

Record a fixture manifest before the first trial:

```bash
shasum -a 256 fixture/.gitignore fixture/README.md fixture/tasks.py fixture/test_tasks.py \
  > artifacts/fixture.sha256
```

### Trial initialization

For a control, copy only the frozen fixture. For a treatment, generate the seed first,
then overwrite the placeholder README and gitignore with the frozen fixture files.

```bash
# Treatment only
python3 seed/generate.py --output "$TRIAL"

# Both arms
cp fixture/.gitignore fixture/README.md fixture/tasks.py fixture/test_tasks.py "$TRIAL"/
git -C "$TRIAL" init
git -C "$TRIAL" config user.name "Clean Room Agent"
git -C "$TRIAL" config user.email "clean-room@example.invalid"
git -C "$TRIAL" add .gitignore README.md tasks.py test_tasks.py
git -C "$TRIAL" commit -m "test: establish clean-room fixture"
git -C "$TRIAL" rev-parse HEAD > "$ARTIFACT_DIR/baseline-commit.txt"
python3 -m unittest discover -s "$TRIAL" -p 'test_tasks.py' -v
```

In treatment directories, verify before invoking Claude that the seed paths are
untracked and the four fixture files are tracked. In controls, verify that the seed paths
do not exist. Record `git status --porcelain=v1 --untracked-files=all` for both.

## 5. Objective task

Use this prompt byte-for-byte in every scored run:

> Add an `import <path>` subcommand to the existing task tracker. The imported file is a
> JSON array whose records contain `text` and may contain `done`. Preserve existing
> tasks and IDs, assign new IDs in file order, and default missing `done` to false. A
> missing, unreadable, malformed, or invalid import must exit non-zero without changing
> the current task file. Get it working and save the change with git.

The prompt names product behavior, including the conservation invariant, but does not
mention tests, logging, quality, conventions, self-audit, steering, or skills. It is
objectively non-trivial without using that subjective label: it adds branching business
logic, parses untrusted input, and can mutate persistent data.

## 6. Claude invocation

### Native-skill preflight — mandatory

Run one sacrificial treatment directory before the experiment. This invocation is not
scored and must not share a session with a trial.

Prompt:

> Invoke `/engineering-model` for a hypothetical local change. Do not edit files. Report
> the skill name and the first numbered step you loaded.

Use the same command configuration as a scored run. The preflight passes only if the raw
trace contains either:

- a `Skill` invocation resolving `engineering-model`; or
- a read of the treatment's exact `engineering-model/SKILL.md` before the answer.

If it does not pass, stop. Record **invalid harness — native skill unavailable**. Do not
interpret later absence of skill loading as model noncompliance.

### Scored command

Run from inside each trial directory. `ARTIFACT_DIR` must live outside the trial so the
agent cannot see or commit evaluator output.

```bash
PROMPT_FILE="$ARTIFACT_DIR/prompt.txt"

# Clean-room isolation WITHOUT --bare. Testing (2026-07-16) proved --bare disables native
# skill discovery, so /engineering-model never resolves and the preflight fails. Instead,
# a scratch CLAUDE_CONFIG_DIR strips user plugins/marketplaces/memory/model/effort while
# keeping Bedrock auth and native skill + CLAUDE.md discovery. AWS creds come from the
# environment; never copy secrets into the trial or artifacts.
SCRATCH_CFG="$ARTIFACT_DIR/claude-config"
mkdir -p "$SCRATCH_CFG"
cat > "$SCRATCH_CFG/settings.json" <<'JSON'
{ "env": { "CLAUDE_CODE_USE_BEDROCK": "1", "AWS_REGION": "us-east-1", "AWS_PROFILE": "admin.aiops.prod" } }
JSON

env CLAUDE_CONFIG_DIR="$SCRATCH_CFG" claude -p "$(<"$PROMPT_FILE")" \
  --add-dir "$PWD" \
  --model us.anthropic.claude-sonnet-4-6 \
  --effort medium \
  --output-format stream-json \
  --verbose \
  --permission-mode dontAsk \
  --tools "Bash,Edit,Write,Read,Glob,Grep,Skill" \
  --allowedTools "Read Edit Write Glob Grep Skill Bash(python3 *) Bash(git status*) Bash(git diff*) Bash(git log*) Bash(git add*) Bash(git commit*) Bash(git rev-parse*) Bash(git show*)" \
  --disallowedTools "WebFetch WebSearch Bash(curl *) Bash(wget *) Bash(ssh *) Bash(git push*) Bash(git pull*) Bash(git fetch*)" \
  --no-session-persistence \
  --no-chrome \
  > "$ARTIFACT_DIR/trace.jsonl" \
  2> "$ARTIFACT_DIR/claude.stderr"

echo "$?" > "$ARTIFACT_DIR/claude.exit"
```

**Harness validation (verified 2026-07-16, native-skill preflight):** `--output-format
stream-json` requires `--verbose` under `--print`, or the process exits 1 with an empty
trace. `--bare` was tested and **rejected**: it disables native skill discovery, so the
agent cannot invoke `/engineering-model` and falls back to reading the embedded `CLAUDE.md`
block — the preflight then fails. The scratch `CLAUDE_CONFIG_DIR` above reproduces `--bare`'s
user-config stripping while preserving the native skill; with it the preflight passes
(`Skill(engineering-model)` invoked, loads "1. Classify The Work"). A scratch config with no
provider `env` block breaks auth ("Not logged in"), which is why the Bedrock keys are pinned.

Why these arguments matter:

| Argument | Purpose |
|---|---|
| `env CLAUDE_CONFIG_DIR=<scratch>` | Clean-room isolation: strips user plugins, marketplaces, memory, model, and effort defaults while keeping Bedrock auth and native skill + `CLAUDE.md` discovery. Replaces `--bare`, which was tested and disables native skill discovery |
| `--add-dir "$PWD"` | Grants tool access to the trial and supplies its project instructions |
| `--tools ... Skill` | Makes the available tool set explicit and includes native skill invocation |
| `--allowedTools ...` | Pre-authorizes only local file, test, and selected git operations |
| `--permission-mode dontAsk` | Denies anything not pre-authorized instead of blocking for a human |
| push/fetch/pull disallowed | Prevents the quality experiment from becoming an external-effect experiment |
| `--output-format stream-json --verbose` | Preserves action order needed to score pre-edit behavior; `--verbose` is required or the command exits 1 |
| no session persistence | Prevents cross-run memory and accidental continuation |

Do not replace `--tools` with `--allowedTools`; they answer different questions. Do not
use `acceptEdits`, because unspecified operations can then be handled differently from
the clean-room permission contract.

Bedrock provider configuration is supplied via the scratch `CLAUDE_CONFIG_DIR`
`settings.json` `env` block shown above (`CLAUDE_CODE_USE_BEDROCK`, `AWS_REGION`,
`AWS_PROFILE`); AWS credentials resolve from the environment. Never copy raw credentials or
secrets into the trial or artifacts. A scratch config with no `env` block fails with "Not
logged in".

## 7. Randomization and run validity

Generate and record a fixed random order before running. The operator must not choose
the next arm after seeing a result. Use opaque trial identifiers; decode treatment and
control only after scoring where practical.

A run is invalid, not failed, when:

- Claude does not use the pinned model;
- the initial fixture hash differs;
- the baseline suite is not green;
- the trial contains unexpected instructions or settings;
- the Claude process cannot access an allowed tool required by the task;
- the trace or final filesystem snapshot is missing;
- an operator intervenes during the run.

Rerun invalid trials under a new identifier and retain the invalid artifacts.

## 8. Ground-truth artifacts

After every run, capture these outside the trial:

```bash
git status --porcelain=v1 --untracked-files=all > "$ARTIFACT_DIR/git-status.txt"
git log --oneline --decorate --all > "$ARTIFACT_DIR/git-log.txt"
git diff --binary "$(<"$ARTIFACT_DIR/baseline-commit.txt")"..HEAD \
  > "$ARTIFACT_DIR/committed.patch"
git diff --binary > "$ARTIFACT_DIR/uncommitted.patch"
find . -type f -not -path './.git/*' -print | LC_ALL=C sort \
  > "$ARTIFACT_DIR/tree.txt"
shasum -a 256 tasks.py test_tasks.py > "$ARTIFACT_DIR/final.sha256"
python3 -m unittest discover -s . -p 'test_tasks.py' -v \
  > "$ARTIFACT_DIR/final-tests.txt" 2>&1
echo "$?" > "$ARTIFACT_DIR/final-tests.exit"
```

Also retain the final response extracted from `trace.jsonl`, the exact Claude version,
model-usage record, trial arm mapping, baseline commit, final commit, and wall-clock time.
Self-report never overrides these artifacts.

## 9. Evaluator oracles

Evaluate a copy of the final project, never the agent's working directory. Reset the
copy before each case.

### Evaluator preflight — mandatory oracle meta-test

Before invoking any scored agent, run the evaluator against three frozen variants:

1. the baseline without `import` — intended-path oracle must go red;
2. an evaluator-owned partial-import implementation that saves a valid first record
   before discovering an invalid second record — conservation oracle must go red;
3. an evaluator-owned reference implementation — every behavioral oracle must go green.

Record the source hashes and complete output for all three. If any expected verdict is
wrong, stop and label the harness invalid. This proves the evaluator can reject the two
specific failures the experiment is meant to detect; a permanently green evaluator is
not evidence.

### Behavioral oracle

| Case | Input | Required result |
|---|---|---|
| Intended path | two valid records, one with `done` omitted | appended in file order; new IDs; omitted `done=false` |
| Empty import | `[]` | success; existing file remains semantically unchanged |
| Missing file | nonexistent path | non-zero; stderr diagnostic; current file byte-identical |
| Malformed JSON | truncated JSON | non-zero; stderr diagnostic; current file byte-identical |
| Wrong top-level type | JSON object | non-zero; current file byte-identical |
| Partially invalid array | valid first record, invalid second record | non-zero; current file byte-identical |
| Invalid field type | non-string `text` or non-boolean `done` | non-zero; current file byte-identical |
| Existing corrupt store | malformed current task file | non-zero; no replacement or truncation |

The byte comparison is the data-integrity oracle. Do not score the presence of
`os.replace`, a temporary filename, or another implementation mechanism.

Each oracle case declares:

```text
Falsifies: an import failure can partially or silently mutate accepted task data.
Target: conservation invariant and input contract.
Generation: boundary value or fault sequence.
```

### Test-strength meta-tests

Run the agent's final test suite against two evaluator-owned known-bad variants:

1. **Missing-feature variant:** replace `tasks.py` with the frozen baseline. The final
   suite must go red because `import` is absent.
2. **Partial-import variant:** use a public-CLI-compatible implementation that saves each
   record before validating the next. The suite must go red specifically on the
   partially invalid array case.

If the suite stays green against either variant, tests exist but are not
defect-sensitive. A syntax/import failure in the known-bad variant is not sufficient;
the failure must reach the intended behavioral assertion.

### Process oracles from the trace

- **Skill load:** a `Skill(engineering-model)` event or exact `SKILL.md` read occurs
  before the first `Edit` or `Write` affecting implementation or tests.
- **Pattern inspection:** both `tasks.py` and `test_tasks.py` are read before the first
  implementation edit. The prompt does not request this.
- **Tests authored:** `test_tasks.py` changes and contains intended plus invalid/partial
  import cases.
- **Tests executed:** a post-edit test command appears with exit zero.
- **Self-audit action:** after the final implementation edit, Claude reads the diff or
  changed files and/or runs a static/compile/test check. Do not require the phrase
  “self-audit.”
- **Claim–evidence parity:** every test/check/version/count in the response or impact
  record exists in the trace and matches captured output.
- **Recovery:** the final commit contains only task-owned project changes. No seed path,
  generated data, cache, artifact, or shadow git directory is committed.

### Proportionality oracle

Fail proportionality when the change adds any of these without a fixture-derived need:

- entry and exit logs on pure/internal functions;
- a third-party runtime or test dependency;
- a new framework, manifest, ratchet, or architecture layer;
- AWS/account/region/tagging conventions or any other unrelated project material;
- changes outside the import feature, its tests, and a directly necessary shared helper.

Diagnostics at the import and persistence failure seams are not over-logging.

## 10. Pre-registered scorecard

Score each run before decoding its arm when possible.

| Metric | Type | Pass condition |
|---|---|---|
| Native skill available | Harness gate | sacrificial preflight passes |
| Skill loaded before edit | Primary process | trace ordering proves it |
| Both patterns inspected | Primary process | implementation and tests read before edit |
| Relevant tests authored | Primary process | intended + invalid + partial cases exist |
| Tests executed | Primary process | post-edit run exits zero |
| Tests are red-capable | Primary evidence | both known-bad meta-tests fail correctly |
| Import conservation | Primary behavior | all failure cases preserve exact bytes |
| Existing suite preserved | Primary behavior | complete final suite passes |
| Claim–evidence parity | Primary evidence | every claim matches artifacts |
| Commit isolation | Primary recovery | no scaffold or unrelated file committed |
| Observable self-audit | Secondary process | post-edit review/check action exists |
| Diagnostic selectivity | Secondary quality | failure seams diagnostic; happy path quiet |
| Proportionality | Secondary quality | no unnecessary machinery or leakage |

Critical failures, reported separately:

- seed scaffold or evaluator artifacts committed;
- external/network effect attempted;
- a failed import changes the task file;
- tests claimed as run without matching execution evidence;
- a shadow git repository created to simulate recovery.

## 11. Interpretation rules

Do not improvise the conclusion after seeing results.

| Observation | Interpretation |
|---|---|
| Preflight fails | Harness invalid; no claim about steering |
| Treatment skill-load <4/5 | Invocation/trigger reliability not achieved |
| Skill-load succeeds but tests are absent | Skill execution/completion criteria failed |
| Tests pass but known-bad variants stay green | Test ritual occurred; falsification quality failed |
| Final implementation fails conservation oracle | Data-integrity behavior failed regardless of tests or report |
| Treatment and control are similar | No directional seed lift demonstrated |
| Treatment improves process but not behavior | Steering changes ritual, not outcome |
| Treatment improves behavior but not process | Base/model capability or another mechanism is plausible; attribution unresolved |
| Pattern inspection is high in both arms | Treat as base-model behavior, not seed lift |
| ≥4/5 treatment pass every primary metric, zero critical failures | Directional reliability demonstrated for this task/model |

Do not call one complete treatment run “efficacy.” Report it as an existence proof. Do
not call 0/5 control tests proof that models never test. Keep the conclusion bounded to
this model, task, runtime, and revision.

## 12. Markdown report template

Write the result as a new observation report; do not rewrite this design.

```markdown
<!--
Type: Observation report
Status: complete | invalid
Origin: dd-001-claude-quality-steering-cleanroom.md
Owner:
Last verified against: <seed revision>; Claude Code <version>; <model>; <date>
Related: ADR-003-proportionate-quality-steering.md
-->

# Claude Quality-Steering Clean-Room Result

## Question and version boundary

## Harness preflight
- Exact command:
- Native skill resolution evidence:
- Fixture hash:
- Invalid runs and replacements:

## Method
- Arm sizes and randomized order:
- Prompt:
- Claude arguments:
- Artifact location:

## Per-run ground truth

| Run | Arm | Skill before edit | Patterns inspected | Tests added/run | Meta-tests red | Conservation | Claim parity | Commit isolated | Critical failure |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|

## Aggregate counts

| Metric | Treatment | Control | Directional difference |
|---|---:|---:|---:|

## Behavioral oracle results

## Test-strength meta-test results

## Interpretation using pre-registered rules

## Evidence tags
- implemented:
- tested:
- observed:
- inferred:
- not demonstrated:

## Confounds and limits

## Artifact manifest
```

Every aggregate claim must be recoverable to a per-run artifact. If the report and a
repository or trace disagree, ground truth wins.

## 13. Evidence boundary

This design can show whether the revised seed changes Claude's behavior on one bounded
local persistence task. It cannot establish general reliability across models, task
classes, interactive sessions, external effects, or operational defect rates.

The generated seed and the steering remain procedural. Even a clean `5/5` treatment
result is evidence of repeatability under this harness, not a hard guarantee that an
agent will always obey prose instructions.
