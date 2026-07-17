<!--
Type: Experiment design (terminal measurement round)
Status: proposed — ready to pre-register and run
Origin: rep-005-falsification-program-narrative.md §10; rep-006-prior-art-related-work.md (borrowed controls)
Last updated: 2026-07-17
-->

# Structure-vs-Content Home-Turf A/B — the terminal measurement round

## Purpose

Answer the single sharpest question left about the current seed, on the ground where it should be
strongest: **does the seed's *content* do anything its *structure* does not?** Prior rounds tested
*seed vs bare* and found no outcome lift; two 2026 studies (see `rep-006-prior-art-related-work.md`) show any
effect is *scaffold structure*, not *content*. This round adds the controls those studies used
(labels-only, length-matched placebo) so we can separate the two — uncontaminated, on the seed's
home turf.

## Stopping rule (pre-committed, read first)

This is the **last measurement round on the current (rhetorical) seed.** After it:
- If **content does not separate from structure** (F ≈ L), the measurement phase ends. We consolidate
  the narrative + harness and pivot to an **executable-discipline seed** (force a committed, executed
  test whose result is quoted — not narrated discipline).
- If **content separates** (F meaningfully > L on home turf), that is the one positive result worth
  developing, and it defines what to keep in the seed.
Either way we do **not** open another rhetorical-seed round. This prevents an endless tunnel.

## Arms (4)

Applied identically to each task; nothing differs but the injected scaffold.

| Arm | Scaffold present | What it isolates |
|---|---|---|
| **V** — bare | none | base-model baseline |
| **P** — placebo | generic best-practice text, **length-matched** to the full seed, no seed procedure / impact-record / objective-trigger content | prompt-length / "more tokens → more thinking" confound |
| **L** — labels-only | the seed's section **headers / structure only**, procedure stripped | scaffold *structure* effect |
| **F** — full seed | the current seed scaffold (unchanged) | full seed |

The P and L variants are **seed-derived** (produced from the seed, not the tasks), so building them
does not breach the task-design firewall — the tasks stay fixed and independently authored.

## Tasks (the two ground-truth-validated probes)

Use the probes already verified by ground truth (`rep-005-falsification-program-narrative.md` §8):
- **`shard-wake`** (r5) — conservation + recovery convergence; headroom on `replace_3`. Cleaner
  probe (2 controls). Freeze its current oracle.
- **`orbit-slots`** (r4) — canonical input validation; headroom on the leading-zero clause. Use its
  **preregistered** oracle version (not the post-screen amendment), and first run **2 fresh bare
  controls** so it has a 2-control baseline comparable to shard-wake. Disclose its "rescued from an
  invalidated slate" provenance.

Both graded by their **withheld** oracles (already shown to discriminate; no LLM-judge).

## Measurement — pass-rate A/B

Headroom on both tasks is **flaky (~50% control pass)**, so single runs are uninformative; we compare
**pass rates over repeated trials.**
- **N = 12 trials per arm per task** (4 arms × 2 tasks × 12 = **96 runs**, ≈ $24 at ~$0.25/run).
- Per run record: solved? (all withheld subcases pass), the headroom-subcase result, conservation,
  durable-test committed?, impact-record calibration (claim vs oracle), commit hygiene (scaffold
  leak?).
- Report pass **rates** per arm per task with bootstrap intervals; **directional, not powered** for
  small effects (n is modest — state this plainly).

## Primary contrasts

- **Δcontent = F − L** — *the key quantity.* Does the seed's procedure add anything beyond its
  section structure?
- **Δstructure = L − V** — does having the scaffold structure help at all?
- **Δlength = P − V** — does equal-length generic text alone move outcomes?
- **Δtotal = F − V** — total seed effect (continuity with rounds 1–3).

## Pre-registration (before any run)

Commit, before generating any trial: the four contrasts, the directional hypotheses, the
"separates" threshold (e.g. Δcontent ≥ a stated margin with a CI excluding 0), the trial count N,
and the stopping rule above. Freeze both oracles and the four scaffold variants by hash.

## Firewall & isolation

- Arms are seed-derived; tasks are fixed → no task-tuning to outcomes.
- Run in a clean workspace with only: the frozen tasks + oracles, the four scaffold variants, the
  Bedrock config. Grade with withheld oracles after each run.
- Do not alter a task or oracle based on observed outcomes (invalidate, never repair).

## Interpretation (pre-registered readings)

- **F ≈ L** → seed *content* adds nothing beyond structure (matches literature) → measurement ends,
  pivot to executable-discipline seed.
- **F > L** → real home-turf content effect → the positive result; identify which seed content carries it.
- **L ≈ P ≈ V** → not even structure helps on these tasks (base model handles them) → null across the
  board; same pivot.
- **P > V but F ≈ P** → the "effect" is just prompt length / extra thinking, not the seed.

## After this round

Regardless of outcome: consolidate the program (narrative + harness + this result) and, as the
forward line of work, build and test an **executable-discipline seed** — one that requires running a
real test against a real oracle and quoting the result, rather than narrating a falsification
posture. That is a fresh question, tested with this same apparatus.
