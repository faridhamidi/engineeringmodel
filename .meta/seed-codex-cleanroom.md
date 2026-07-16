<!--
Type: Observation report (behavioural + quality evidence)
Status: complete (real runtime: Codex CLI, gpt-5.5 medium; n=2 control + 2 treatment)
Origin: follow-up to seed-cleanroom-observation.md, run on Codex to remove the operator-steering confound
Owner: repository maintainer (assign on adoption)
Last verified against: seed generator on local main; Codex CLI 0.144.5, model gpt-5.5, 2026-07-16
Related: seed-cleanroom-observation.md (Kiro rounds), ADR-001-builder-accessible-layer.md, ADR-002-share-ready-seed.md
-->

# Codex Clean-Room Report — Does the Seed Steer Behaviour and Quality on a Bare Runtime?

## Why this run exists

The earlier [clean-room observation](seed-cleanroom-observation.md) ran through the Kiro
subagent harness, which inherits the operator's global Kiro steering
(`code-quality.md` etc., all `inclusion: always`). That confound **voided** its quality
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

## Findings

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

**Conclusion: the seed does not currently steer code quality.**

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

- The bare runtime does **not** provide tests or logging (0/4), and the **current seed does
  not add them** (treatment 0/2). The only thing that reliably produced them was always-on
  operator steering (Kiro, 10/10). So if the seed is meant to steer quality for someone on a
  bare runtime — the whole point of a shareable seed — **it must carry that steering itself,
  always-on.**
- **Do not import `code-quality.md` verbatim.** It is absolutist ("log at *every* seam,"
  "tests for *every* implementation"), which conflicts with the engine's proportionality
  ("the lightest mechanism that protects the actual risk"); it contains operator/org-specific
  bits; and it re-introduces "how to build" prescription that the design deliberately keeps
  out of the steering. Add a **short, proportionate** line that points at the engine's own
  `TESTING.md`/`FOUNDATION.md`, not the operator's house standard.
- **Open question to settle:** whether the quality nudge is unconditional or gated (e.g.
  only for non-trivial or above-the-line work), to preserve proportionality for throwaway
  scripts.

## Evidence tags

- **tested:** 4/4 tools executed — smoke paths pass.
- **confirmed:** model `gpt-5.5` on all runs; zero tests and zero seam-logging on bare Codex
  (both arms); contrast with the Kiro run's 10/10.
- **observed:** seed behavioural engagement in 1/2 treatment runs; quality parity between arms.
- **inferred:** the earlier Kiro quality came from operator steering (now corroborated by the
  bare-runtime absence).
- **proposed / not demonstrated:** the four improvements above; the effect of adding an
  always-on quality nudge (untested); results beyond n=2/arm, one task, one model, one runtime,
  and with the git-sandbox confound.

## Confounds and limits

- **n = 2 per arm, one task, one model (`gpt-5.5` medium), one runtime (Codex).** Directional,
  not statistical.
- **Git-sandbox confound** (see Finding 5) muddies the commit-scope dimension this run.
- Codex's own base disposition (strong) supplies structure/error-handling for free, which
  narrows the room for the seed to show a quality lift on those axes.

## Appendix — per-run ground truth

| Run | Model | Tool works | Tests | Logging | Atomic write | Seed engagement | Git |
|---|---|---|---|---|---|---|---|
| control-1 | gpt-5.5 | yes | none | 0 | yes | n/a | reported blocked, gave steps |
| control-2 | gpt-5.5 | yes | none | 0 | no | n/a | worked around (separate git-dir in /tmp) |
| treatment-1 | gpt-5.5 | yes | none | 0 | yes | strong (read skill, impact record, scaffold untracked) | worked around (`.repo.git`) |
| treatment-2 | gpt-5.5 | yes | none | 0 | no | weak (`git status` first only) | reported blocked, stopped |
