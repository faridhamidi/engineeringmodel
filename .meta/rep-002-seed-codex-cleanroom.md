<!--
Type: Observation report (behavioural + quality evidence)
Status: complete (two real runtimes: Codex CLI gpt-5.5 medium + Claude Code sonnet-4.6 medium; n=2 control + 2 treatment each)
Origin: follow-up to rep-001-seed-cleanroom-observation.md, run on Codex then Claude to remove the operator-steering confound
Owner: repository maintainer (assign on adoption)
Last verified against: source revision 7929550; Codex CLI 0.144.5 (gpt-5.5) + Claude Code 2.1.211 (us.anthropic.claude-sonnet-4-6), 2026-07-16
Related: rep-001-seed-cleanroom-observation.md (Kiro rounds), ADR-001-builder-accessible-layer.md, ADR-002-share-ready-seed.md, ADR-003-proportionate-quality-steering.md
Revision note: ADR-003 implements the proposed quality, skill-loading, and constrained-git changes after this observation. Its post-change behavioral effect has not yet been measured.
-->

# Clean-Room Report — Does the Seed Steer Behaviour and Quality on Bare Runtimes? (Codex + Claude)

> **Version boundary:** every result below describes the seed at source revision
> `7929550`, before the proportionate quality floor in
> [ADR-003](ADR-003-proportionate-quality-steering.md). The current structural
> implementation is tested, but a matched runtime rerun is still required before
> claiming that it changes agent behavior or code quality.

## Why this run exists

The earlier [clean-room observation](rep-001-seed-cleanroom-observation.md) ran through the Kiro
subagent harness, which inherits the operator's four-file global Kiro steering bundle
(`code-quality.md`, `security-best-practices.md`, `collaboration-style.md`, and
`project-conventions.md`, all `inclusion: always`). That confound **voided** its quality
round — the tests and seam-logging seen there came from operator steering, not the seed.

This run removes that confound by using **Codex CLI**, the seed's real target runtime:
Codex natively auto-loads `AGENTS.md` (so the seed's steering is genuinely always-on),
and `--ignore-user-config` strips Codex's own config, plugins, and MCP servers. The result
is the cleanest available isolation: **base model + (treatment only) the packaged seed**,
nothing else. It answers two things: does the seed steer behaviour on a bare runtime, and
**does the seed need its own code-quality steering?**

## Method

- **4 non-interactive runs:** `codex exec`, **model `gpt-5.5`, reasoning effort `medium`**
  (verified in every run log: `model: gpt-5.5`), passed explicitly and with
  `--ignore-user-config`.
- **`--sandbox workspace-write`** (writes confined to the workspace; **network disabled**).
- **2 control** (bare directory: only a placeholder `README.md`) + **2 treatment**
  (a freshly generated seed: `AGENTS.md` + `CLAUDE.md` + the `engineering-model` skill).
- **Identical task, no priming:** build a robust JSON-backed task-tracker CLI
  (`add`/`list`/`done`), get it working, save with git. No mention of steering, the skill,
  tests, or quality.
- **Every output was executed and code-reviewed** (smoke `add`/`list`/`done`, plus a
  robustness scan of each `tasks.py`).

> **Two runtimes.** This report was first run on Codex (Runtime 1), then replicated on
> Claude Code (Runtime 2) to test whether the findings hold beyond a single model/CLI. The
> Codex findings are below; the Claude replication and the cross-runtime synthesis follow.

## Findings — Runtime 1: Codex (gpt-5.5 medium)

### 1. Functionality: 4/4 run flawlessly

Every tool passed the `add`/`list`/`done` smoke path. Base `gpt-5.5` reliably produced
structured code (8–9 functions), error handling (7–9 `try/except`), input validation, and
correct exit codes — **with or without the seed**. That is the model's baseline.

### 2. The decisive contrast: no tests, no logging on a bare runtime

| Practice | Bare Codex (this run, 4/4) | Kiro run (operator steering, 10/10) |
|---|---|---|
| Unit tests written | **0 / 4** | 10 / 10 |
| Seam logging | **0 / 4** | 10 / 10 |

Bare `gpt-5.5` wrote **no tests and no seam-logging in any run**. The Kiro agents wrote
both every time. This proves *by contrast* that those practices in the earlier study came
from the operator's `code-quality.md` steering — **not from the model, and not from the
seed.**

### 3. The seed did not supply quality either

Treatment matched control on every quality axis: **0/2 tests, 0/2 logging**, same error
handling, same structure. Atomic writes appeared in 2 of 4 (one control, one treatment) —
model variance, not a seed effect. Notably, `treatment-1` *did* read `SKILL.md` and emit
the skill's impact record with **"Enforcement: direct test"** — yet wrote **no test file**.
The seed's quality guidance lives in the *on-demand skill*, and even when the skill was
read, it did not translate into the practice.

**Conclusion: the tested pre-change seed did not steer code quality.**

### 4. Behavioural (seed) signal: present but partial

- **`treatment-1`** — strong seed engagement: read `SKILL.md`, emitted the
  `Layer / Semantic / Enforcement / Authority / External / Residual` impact record,
  explicitly left the pre-existing scaffold untracked (the commit-scope norm), and worked
  around the git block with a separate git-dir.
- **`treatment-2`** — weak: ran `git status` first (a seed norm) but otherwise behaved like
  a control (no impact record).
- **Controls** — neither the impact record nor the envelope vocabulary. (`control-2`
  independently worked around the git block — base-model resourcefulness, not the seed.)

So seed engagement was **1/2 strong, 1/2 weak** — consistent with the earlier finding that
*discovery ≠ reliable application*, and that the simple always-on norms land more reliably
than the on-demand skill's process.

### 5. Confound this run — the git sandbox

`--sandbox workspace-write` blocked creating `.git` (and `rm -rf`), so "save with git" was
environmentally hobbled. Agents diverged (two worked around it with a separate git-dir; two
reported the blocker and stopped). This **muddies the commit-scope behavioural dimension**
for this run — but does **not** affect the tests/logging quality finding, which is the
central result.

## Findings — Runtime 2: Claude Code (Sonnet 4.6 medium)

Same task, same design, on **Claude Code 2.1.211** via Bedrock, **model
`us.anthropic.claude-sonnet-4-6`, `--effort medium`** (verified in every run's JSON:
`modelUsage` = `us.anthropic.claude-sonnet-4-6`; all `is_error:false`). Claude Code has no OS
sandbox, so tool access was confined by permission instead: filesystem limited to the trial
dir (no `--add-dir`), network tools (`WebFetch`/`WebSearch`) disallowed, only
`Bash`/`Edit`/`Write`/`Read` pre-approved. Crucially, **git worked here**, so the
commit-scope dimension that the Codex sandbox blocked is recovered.

**Functionality:** 4/4 tools pass the smoke path. Claude wrote more compact code (92–99
lines vs Codex's 143–184), parsed `sys.argv` by hand (no `argparse`), and used fewer guards
— model style, not a seed effect.

**Quality — replicates Codex exactly:** **0/4 tests, 0/4 seam-logging, 0/4 atomic writes**,
seeded or not. Treatment matched control. Neither the model nor the seed produced tests or
logging.

**Behaviour — the recovered commit-scope test, the cleanest signal yet:**

| Run | Committed | Pre-existing files (README + scaffold) |
|---|---|---|
| control-1 | `README.md`, `tasks.py` | committed the pre-existing README |
| control-2 | `README.md`, `tasks.py` | committed the pre-existing README |
| treatment-1 | `.gitignore`, `tasks.py` | **excluded** scaffold **and** README |
| treatment-2 | `.gitignore`, `tasks.py` | **excluded** scaffold **and** README |

**Both** seeded runs committed only task-owned files and left every pre-existing file
untracked (the `AGENTS.md`/`CLAUDE.md`/`.agents`/`.claude`/`.engineering-model` scaffold
*and* the README) — the seed's "commit only task-owned work, never pre-existing files" norm,
which lives in the **always-on** steering block. Both controls committed the pre-existing
README. So the always-on norm landed **2/2** — more reliably than on Codex (where the
sandbox hobbled git).

**But the on-demand skill ritual did not transfer:** the `Layer / Semantic / Authority /
Residual` impact record appeared in **0/4** Claude reports (Codex: 1/2). Again the always-on
front steers; the skill ritual does not.

## Cross-runtime synthesis (8 runs: Codex gpt-5.5 + Claude sonnet-4.6)

- **Quality is not free, and the tested pre-change seed did not add it — replicated on two
  independent runtimes.** Tests: **0/8**. Seam-logging: **0/8**. Bare or seeded, Codex or
  Claude — no tests, no logging. The only condition that ever produced them was always-on
  operator steering (Kiro, 10/10). This is now a two-runtime replication, not a single
  observation.
- **The always-on front is the reliable steering channel; the on-demand skill is not.** The
  always-on commit-scope norm produced clean, matching behaviour on Claude (2/2 excluded
  pre-existing files vs 0/2 controls). The skill's impact-record ritual was inconsistent
  (Codex 1/2, Claude 0/2). Whatever the seed must reliably steer — including any quality
  baseline — belongs in the always-on block, not the skill.

## What the seed can be improved (from this test)

1. **Promote a proportionate quality nudge into the *always-on* steering front — not the
   skill.** The skill-buried quality guidance did not produce tests or logging even when the
   skill was read. The always-on block is what reliably lands. A single short line in the
   engine's *proportionate* voice would do it, e.g.: *"protect the load-bearing seams with
   the lightest test that catches the real risk; log at the seams that matter; never lose
   data silently."* This routes to `core/TESTING.md` and `core/FOUNDATION.md` for depth.
2. **Close the cite-but-don't-do gap.** `treatment-1` claimed "Enforcement: direct test"
   without a test file. The skill's completion criterion for step 3 should require that a
   claimed test actually exists (a checkable artifact, not a claim).
3. **Make skill consultation more reliable for non-trivial builds.** Only 1/2 treatment
   agents ran the skill's process. The always-on steering could more firmly direct the agent
   to load the skill when the work is non-trivial, rather than leaving it to chance.
4. **Acknowledge constrained environments.** The revertible-envelope premise assumes git
   works; in a sandbox that blocks `.git`, it silently breaks. The seed could tell the agent
   to detect this and report it rather than proceed as if saved.

## Does code-quality steering need to be in the seed?

**Evidence-based answer: yes — a proportionate quality baseline should be added to the
seed's always-on front — but not the operator's absolutist standard.**

- Neither bare runtime provided tests or logging (**0/8 across Codex + Claude**), and the
  **tested pre-change seed did not add them** (treatment 0/4). The only thing that reliably produced
  them was always-on operator steering (Kiro, 10/10). So if the seed is meant to steer
  quality for someone on a bare runtime — the whole point of a shareable seed — **it must
  carry that steering itself, always-on.** This is now replicated on two independent runtimes.
- **Do not import the Kiro bundle verbatim.** `code-quality.md` is absolutist ("log at
  *every* seam," "tests for *every* implementation"), which conflicts with the engine's
  proportionality ("the lightest mechanism that protects the actual risk"). The bundle
  also includes project-specific conventions that do not belong in a reusable seed. Keep
  the portable self-audit and pattern-consistency behavior, then point at the engine's
  own `TESTING.md`/`FOUNDATION.md` for proportionate depth.
- **Open question to settle:** whether the quality nudge is unconditional or gated (e.g.
  only for non-trivial or above-the-line work), to preserve proportionality for throwaway
  scripts.

## Evidence tags

- **tested:** 8/8 tools executed (4 Codex + 4 Claude) — smoke paths pass.
- **confirmed:** model `gpt-5.5` on all Codex runs and `us.anthropic.claude-sonnet-4-6` on all
  Claude runs; **0/8 tests and 0/8 seam-logging** across both runtimes (all arms); the seed's
  always-on commit-scope norm applied in 2/2 Claude treatment runs vs 0/2 controls; contrast
  with the Kiro run's 10/10.
- **observed:** on-demand skill ritual (impact record) inconsistent — Codex 1/2, Claude 0/2;
  quality parity between arms on both runtimes.
- **inferred:** the earlier Kiro quality came from operator steering (now corroborated by the
  bare-runtime absence on two runtimes).
- **implemented structurally / not behaviorally demonstrated:** the four improvements
  above now live in ADR-003; their runtime effect remains untested, as do results beyond
  n=2/arm/runtime, one task, and one model per runtime.

## Confounds and limits

- **n = 2 per arm per runtime, one task, one model each (`gpt-5.5` medium, `sonnet-4.6`
  medium).** Directional, not statistical.
- **Git-sandbox confound on Codex only** (see Finding 5) muddied its commit-scope dimension;
  Claude (git working) recovered it.
- Base models supply structure/error-handling for free (Codex more than Claude), narrowing
  the room for the seed to show a quality lift on those axes.
- The commit-scope read rests on treatment excluding pre-existing files while controls
  committed the README — a real contrast, but Claude may also scope commits tightly by
  disposition; the seed norm and the model tendency point the same way here.

## Appendix — per-run ground truth

### Appendix A — Codex (gpt-5.5 medium)

| Run | Model | Tool works | Tests | Logging | Atomic write | Seed engagement | Git |
|---|---|---|---|---|---|---|---|
| control-1 | gpt-5.5 | yes | none | 0 | yes | n/a | reported blocked, gave steps |
| control-2 | gpt-5.5 | yes | none | 0 | no | n/a | worked around (separate git-dir in /tmp) |
| treatment-1 | gpt-5.5 | yes | none | 0 | yes | strong (read skill, impact record, scaffold untracked) | worked around (`.repo.git`) |
| treatment-2 | gpt-5.5 | yes | none | 0 | no | weak (`git status` first only) | reported blocked, stopped |

### Appendix B — Claude (sonnet-4.6 medium)

| Run | Model | Tool works | Tests | Logging | Committed | Pre-existing files |
|---|---|---|---|---|---|---|
| control-1 | sonnet-4-6 | yes | none | 0 | `README.md`, `tasks.py` | committed README |
| control-2 | sonnet-4-6 | yes | none | 0 | `README.md`, `tasks.py` | committed README |
| treatment-1 | sonnet-4-6 | yes | none | 0 | `.gitignore`, `tasks.py` | excluded scaffold + README |
| treatment-2 | sonnet-4-6 | yes | none | 0 | `.gitignore`, `tasks.py` | excluded scaffold + README |
