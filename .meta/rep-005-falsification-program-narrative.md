<!--
Type: Narrative report (program history)
Status: living — audit trail through Round 5 COMPLETE (slate self-invalidated a 2nd time; two probes — orbit-slots + shard-wake — rescued by ground-truth verification; home-turf pass-rate A/B is next)
Origin: synthesizes rep-001-seed-cleanroom-observation.md, rep-002-seed-codex-cleanroom.md, rep-003-claude-new-steering-behavioral-tests.md,
        dd-001-claude-quality-steering-cleanroom.md, rep-004-claude-quality-steering-cleanroom-result.md,
        and the round-4/4b/5 clean-room work in the (out-of-repo) harness.
Last updated: 2026-07-17 (Round 5 complete)
-->

# The Engineering-Model Falsification Program — A Complete Narrative

## 0. Why this document exists

This is the connected story of how we tested whether the **engineering-model seed** actually works —
told in full, with the reasoning at each turn, not just the results. It spans from the earliest
Kiro-steered sessions, through the Codex clean-room, the Claude A/B rounds, the pivot to novel
uncontaminated tasks, and into Round 5 (running as this is written).

The single most important thing to understand about this program is its **stance**. We are not trying
to prove the seed is good. We are trying to **break it** — to falsify its value claims — so that we
learn where it actually helps and where it only *appears* to. The operating philosophy, in the
maintainer's words, is *"so I don't syok sendiri"* — so we don't get high on our own supply, fall in
love with our own idea, and mistake ritual for substance. Everything below is built to make
self-deception hard: matched controls, withheld graders, ground truth over self-report, an
independent task author, and pre-registration.

A recurring theme emerges and is worth flagging up front, because it is almost poetic: **a coverage
claim outran reality — three times, at three levels.** First the *seed's* impact record claimed "all
branches covered" while missing edge cases (Round 3). Then our own *experimental oracle* claimed
discrimination while missing contract clauses (Round 4B). Then the very *Contract-Coverage Gate*
built to prevent that was itself implemented only syntactically — it checked that clauses were named,
not that they were fully exercised (Round 5). The same discipline caught all three, including when
turned on our own instruments. The method ate its own tail, repeatedly and honestly — which is
exactly what a falsification program is supposed to do.

---

## 1. What the seed is, and the claim under test

The "seed" is a portable engineering-discipline package for AI coding agents — a Claude/Codex
**Skill** plus `AGENTS.md` / `CLAUDE.md` steering. Installed into a repo, it is supposed to make an
agent behave like a disciplined engineer rather than a hasty one. Its **public claims** are:

1. **Testing discipline** — writes and runs real tests, including for failure branches.
2. **Input validation & error paths** — rejects malformed/adversarial input.
3. **Data conservation & atomicity** — never leaves persisted state half-mutated on failure.
4. **Invariant preservation** — holds stated invariants across operations and against existing state.
5. **Idempotency / recovery** — re-running or resuming an interrupted operation converges cleanly.
6. **Revertibility / commit hygiene** — commits only intended changes.
7. **Calibrated self-assessment** — an "impact record" whose quality claims match ground truth.

The question the whole program asks: **does installing the seed change an agent's behavior and — more
demandingly — its outcomes, in a clean runtime, versus a matched agent without it?**

---

## 2. Act I — The 10 Kiro-steered sessions, and the doubt they created

The starting point was a body of work done in Kiro with the maintainer's global steering active
(the always-on `code-quality.md`, `security-best-practices.md`, etc.). Across those sessions the
observed quality was strikingly high — on the order of **10/10 sessions producing unit tests and
10/10 producing structured logging**. On its face, this looked like strong evidence that "the
methodology works."

**The why-we-doubted:** those sessions were saturated with *operator steering*. Kiro's global
steering explicitly demands tests-at-implementation-time and logging-at-every-seam. So the 10/10 was
not clean evidence about the *seed* — it was evidence about the *operator's steering layer*. The
seed is meant to be portable to a bare runtime with none of that. The honest question became: strip
away the operator's steering and the tool's built-in habits — **does the seed itself carry the
discipline?** You cannot answer that inside the very environment that supplies the discipline for
free. You need a clean room.

---

## 3. Act II — The Codex clean room: isolating the seed from the operator

**How:** we ran Codex (`gpt-5.5`, medium) in a clean room — `--ignore-user-config` to strip the
operator's config, `--sandbox workspace-write` — on a simple build task, 4 runs split 2 control
(no seed) and 2 treatment (seed present).

**What:** bare Codex wrote **0/4 tests and 0/4 logging**. And — critically — the **seed did not add
them either**. The disciplined behavior that looked like "the methodology" in Kiro was revealed to
be the *operator's* steering, not the seed's and not the base model's. One confound: the
`workspace-write` sandbox blocked `.git`, so commit behavior couldn't be read that round.

**Why it mattered:** this was the first honest, deflating result. It reframed everything — the seed
had not yet been shown to do anything a bare model wouldn't do. That is exactly the kind of finding
the program exists to surface.

We then **cross-checked on a second runtime**: Claude (`us.anthropic.claude-sonnet-4-6`), 4 runs
(2+2). Quality replicated Codex (0/4 tests/logging). But here git worked, which recovered a real
signal: **2/2 treatment runs excluded the seed scaffold from their commits; 2/2 control runs
committed a stray README** — a first hint that the seed does affect *commit scope*, even if not
tests. Findings folded into `rep-002-seed-codex-cleanroom.md`.

---

## 4. The steering defect and its repair

Investigation of *why* the seed wasn't triggering surfaced a concrete defect. The seed's quality
floor sat under a **"Revertible Envelope"** heading and was gated by the **subjective** word
*"non-trivial."* An agent deciding whether its change was "non-trivial" mostly decided "no," so the
quality process never fired. There was also no stated precedence that safety/data-integrity should
override existing conventions.

**The fix (commit `67bbd97`):** split the steering into a dedicated, always-on `## Implementation
Quality` heading with an **objective trigger** — the process engages when a change *"alters
executable behavior, adds/changes branching or validation logic, parses untrusted input, or touches
a persistence/external/async seam."* We removed "non-trivial," added *"safety and data integrity
override existing conventions,"* applied the block byte-identically across all five steering files,
and ratcheted it into the witness contract (`steering_contract.py`, 47/47 witnesses passing, engine
untouched). This converted a subjective, rarely-fired gate into an objective one — a change we then
had to *measure*, not assume.

---

## 5. Act III — Claude A/B Rounds 1–2: invocation works; outcomes saturate

**How:** a clean-room A/B harness. Treatment = seed scaffold present (untracked); control = bare.
Byte-identical, seed-neutral prompts (never mention tests/quality/skill). A **withheld** evaluator
graded ground truth via fault injection and conservation checks. `sonnet-4-6`, medium, corrected
tool allowlist, `--verbose`, scratch `CLAUDE_CONFIG_DIR` with only the Bedrock env. 5 treatment + 5
control, **run twice** with independent randomization.

**What:**
- **Skill invocation: 5/5 treatment vs 0/5 control, both rounds → 10/10 vs 0/10 combined.** The
  objective-trigger fix reliably causes the agent to load the skill. This is the one claim that has
  survived every subsequent attempt to break it.
- **Everything downstream saturated.** Pattern inspection, tests authored, tests executed, and data
  conservation all came back **5/5 in *both* arms**. The base model already aces the easy task, so
  there was no room to see a seed-driven quality *lift*.
- **A harness bug, honestly chased.** One treatment run (`run-02`) scored as a total miss. Ground
  truth showed it was not a model failure — its `ls` and `git -C … status` commands were **denied**
  by an over-narrow tool allowlist, and it gave up. Reclassified **invalid**, rerun as `run-02b`
  under a corrected allowlist: it then behaved fully. This also revealed the round's **0/10 commit**
  figure was itself a harness artifact (the narrow git allowlist suppressed commits); rerun clean,
  **10/10 committed, 0/10 leaked the scaffold.**

**Why it mattered:** Round 2's real lesson was not the headline. It was that **an easy task cannot
discriminate**. If both arms score 5/5, "the skill loaded" is the only observable effect, and we
still don't know whether loading it makes the *code better*. That realization is what drove
everything after: **change the task difficulty, not the seed.**

---

## 6. Act IV — Round 3: the first successful falsification

**How:** we deliberately raised difficulty using an *external* benchmark with real failure headroom
— **Aider Polyglot / Exercism**, three of the hardest Python exercises chosen to stress the seed's
*stated* strengths (validation, error paths, parsing untrusted input): `sgf-parsing`, `poker`,
`forth`. 3 treatment + 3 control, byte-identical prompts, the exercise's **official test suite
withheld** and used only to grade. (We rejected SWE-bench Verified: its own authors say it no longer
measures frontier capability, and it shows training contamination — plus it's infra-heavy.)

**What (this is the pivotal result):**
- **No correctness lift.** 1/3 solved in both arms; **108 vs 109** withheld tests passed — control
  *nominally ahead*; `forth` was **strictly worse** under the seed (it failed a division-by-zero
  error case the bare control handled).
- **`sgf-parsing` failed identically in both arms** (the same two property-key-casing tests).
- **The seed's footprint was process, not outcome:** impact record 3/3 vs 0/3, ~4× the inline
  verification (8 vs 2 runs) — none of which converted to a better result.
- **The impact record over-claimed.** `forth`'s record claimed error-handling coverage while the
  seeded run failed *more* error tests than the silent control; `sgf`'s claimed "all branches
  covered" with the same failures as control.

**Why it mattered:** this is the finding the program was built to find. On tasks where the base model
can fail, the seed did **not** make the code more correct, and its self-assessment was **not
calibrated** to ground truth. A confirmation-seeking evaluator stops at Round 2's 10/10 skill
invocation and ships. We kept going until the seed failed to help — and *that* told us where to
improve: the impact record self-grades and over-claims, and verification isn't targeted at the
error/edge paths where the bugs live.

**The contamination realization:** `poker` solved 37/37 in *both* arms — the signature of *recall*.
Exercism is public; frontier models were likely trained on it. Contamination doesn't bias one arm
over the other, but it **bypasses the very discipline we're testing** — the model recalls the answer
instead of working the problem. To keep probing, we needed tasks the model has *not* seen.

---

## 7. Act V — Novel tasks, an independent author, and a firewall

Two design principles fell out of Round 3:

1. **Novel on two axes.** A good task must have an **unseen surface** (an invented domain/format, so
   recall can't shortcut it) *and* an **engineering failure mode** (data corruption, missed
   validation, unhandled error path, non-atomicity) rather than an algorithm-discovery failure —
   because the seed's claim is about *discipline*, not cleverness.
2. **Separate the author from the analyst.** I (the analyst who wants to understand the seed) should
   not also write the traps. So the maintainer brought in **Codex as an independent task designer**,
   briefed only on the seed's *public claims* — explicitly forbidden from reading the seed's steering
   text, from running the treatment arm during design, and from selecting tasks on "does the seed
   win" (only on difficulty). This is deliberate **blinding**: the person writing the trap isn't the
   one hoping for a result.

**Round 4 (first design pass):** Codex authored 5 bespoke "validate-then-atomically-save" tasks. The
difficulty screen (control arm only) showed the base model **aced 4 of 5** — no headroom, the same
saturation wall as the easy task. Only one task (**Orbit Slots**) produced a control failure (it
accepted a non-canonical leading-zero field — a subtle *representational* validation gap). An
undersized slate; not run. Honest outcome: the *task family* was wrong.

**Round 4B (harder axis):** Codex escalated — 8 candidates on a **different, harder axis**:
interrupted-operation recovery/retry, cross-file journaled publishing, subprocess error propagation,
supplied-view reconciliation and rollback, hierarchical resource accounting, idempotent replay. It
ran **two** control runs per task (16 total, **US$3.21**) to guard against sampling luck, and built
real screening tooling with **two** plausible-wrong solutions per oracle. This axis *worked*:
**4 of 8** tasks showed real control failures (versus 1 of 5 in Round 4) — e.g. `beacon` 7/7 then
6/7, the same task failing on a re-run, the "probabilistic curve" made visible.

**And then Round 4B falsified itself.** In final review Codex found that **every** hidden oracle
omitted some explicit rejection clause from its own README. Three-way discrimination was satisfied
(reference passes, a wrong solution fails, bare fixture fails) — yet a wrong solution could still
pass by violating an *untested* clause. **Green preflight did not prove contract compliance.** Per
the brief's firewall (a post-screen oracle defect must be **invalidated**, never patched-and-rerun,
because patching after seeing control outcomes contaminates the design), Codex **invalidated its
entire slate**. No A/B was run.

**Independent verification:** I did not take that self-report at face value. I checked `canopy-slots`
by hand: its README specifies a long rejection contract, but the oracle's `test_all_contract_shapes`
exercised only 6 grouped subcases and never tested non-list input, extra keys, empty band,
non-string fields, or width bounds. A wrong solution accepting `width=0` would have passed. **The
defect was real; the self-invalidation was justified, not performative.**

**The poetry:** this is the *same failure mode as the seed's* in Round 3. The seed's impact record
claimed "all branches covered" while missing edge cases; Codex's oracle's "green preflight" claimed
discrimination while missing contract clauses. A coverage *claim* outrunning actual coverage — and
the falsification discipline, applied reflexively to our own instrument, caught it. The sub-agent
held itself to the standard and killed its own work rather than ship a compromised slate. The
philosophy propagated down.

---

## 8. Act VI — Brief v2, an isolated clean room, and Round 5 (complete)

Round 4B's failure was also partly a **defect in my brief**: its oracle-preflight required only
three-way discrimination, which proves an oracle can tell *one* wrong solution from the reference —
not that it covers the whole contract. So I wrote **Brief v2**, whose central addition is a
mandatory **Contract-Coverage Gate**: before any control run, every explicit README clause must map
to a concrete hidden subcase, at fine granularity (e.g. `width<1`, `width>20`, non-integer, boolean
each get their own row); an uncovered clause is a hard blocker, and you may **not** weaken the README
to match a thin oracle. v2 also: (a) targets the *validated* recovery/persisted-state axis;
(b) requires pre-registration to enumerate concrete subcases, not grouped method names; (c) states
the correct scoring rules up front (fixing the three scorer defects Codex found — durable-test
isolation, real-runner requirement, negation/contraction handling in calibration); (d) hardens the
firewall.

**The isolation step (Round 5 workspace).** The maintainer pressed the sharpest question yet: could
the *presence* of the prior attempts contaminate the v2 design? An instruction ("don't read
`tasks-r4b/`") is weaker than making prior work **physically unreachable** — an autonomous agent can
`ls`, `grep`, and `cat` anything in its workspace. So instead of hunting down every contaminant to
move out, we **inverted it**: a brand-new workspace (`engmodel-cleanroom-r5/`) containing *only* the
v2 brief and a minimal Bedrock config. During setup we caught a real leak — copying the Claude config
dragged in `projects/`/`sessions/` folders whose names embedded the prior round and task identifiers
— and stripped it to the bare `env` block. A scan confirmed the workspace is clean of prior-round
references (except the brief's own methodology-level mentions). The old harness is untouched as the
archive; nothing was deleted.

**Round 5 completed — and self-invalidated a second time.** The fresh, isolated Codex session
designed five bespoke tasks on the recovery/persisted-state axis (`canopy-relay`, `duet-locker`,
`shard-wake`, `tide-share`, `counterweight-transfer`), coverage-gated, pre-registered, and ran the
control-only difficulty screen with **two** control runs per task (ten runs, `sonnet-4-6`).

The screen hit the saturation wall again: **four of five tasks were solved by both controls**
(27/27, 29/29, 27/27, 29/29 — no headroom). Only **`shard-wake` showed headroom, and it was flaky** —
control 1 solved 28/28; control 2 failed one subcase (`replace_3_failure_retry_converges`) plus
conservation.

Then, in mandated final review, Codex found that its **Contract-Coverage Gate had been implemented
*syntactically*, not semantically** — it verified that every README clause had a *named* subcase,
but not that each subcase exercised the clause at its finest stated granularity (e.g. `C26` tested
revision corruption but not operation-index corruption; `C29` deleted only a derived view, not the
canonical half). Per the brief's Part 10 ("invalidate, do not repair post-screen"), Codex
**invalidated the entire slate a second time** — again refusing to patch-and-rerun, again honest to a
fault.

**Ground-truth review — and a course correction.** Rather than accept the blanket invalidation at
face value, the analyst verified the artifacts directly. Three findings:

1. **The oracle is real.** Running `shard-wake`'s grader independently: reference **28/28**, `wrong_a`
   **19/28**, `wrong_b` **25/28** (failing exactly the recovery-journal cases `corrupt_pending`,
   `replace_2`, `replace_3`), bare fixture **12/28**. Genuine three-way discrimination. Re-grading
   control-2's committed solution reproduced **27/28, failing precisely
   `replace_3_failure_retry_converges`** — a *real* control failure on convergence/conservation under
   interrupted recovery, squarely on the seed's home turf.
2. **`orbit-slots` (the lone Round-4 survivor) holds up too.** Its oracle: reference **5/5** pass,
   plausible-wrong **4/5 fail**, bare fixture **5/5 fail**. Its control failure — accepting `A@01+2`,
   a leading-zero, non-canonical field — is a real **input-validation** gap (representational, not
   semantic: the model checks whether the range is valid but not whether its decimal spelling is
   canonical).
3. **The coverage gaps do not touch the signals.** `shard-wake`'s flagged gaps (C26/C29/C30/C41) are
   *untested variants of other clauses*; they do not affect the C33 headroom failure we would
   measure. `orbit-slots`' headroom is on its preregistered noncanonical-validation clause.

The important meta-finding is about the *method itself*: **the coverage rule as written is
unsatisfiable.** "Finest stated granularity" combined with "never repair post-screen" means one can
*always* argue a clause needs a finer sub-variant, so every slate self-invalidates. Round 4B and
Round 5 both died on this — three design rounds, zero "clean" runnable tasks, not because the tasks
were bad but because the acceptance criterion can never be met. The correction is a **bounded**
completeness standard (every README clause has ≥1 executable subcase with a conservation assertion),
enforced as a **hard pre-screen gate** so contract-derived completion happens *before* controls run,
with post-screen invalidation reserved for *outcome-derived* defects only.

**Net position after Round 5.** By ground truth we have **two usable, complementary probes** —
rescued from over-strict invalidation, and to be disclosed honestly as exactly that (ground-truth-
validated, not clean preregistered survivors):
- **`orbit-slots`** — canonical/representational **input validation** (seed claim #2). Caveats: only
  one control run, and a non-preregistered post-screen oracle amendment (for the A/B, use the
  preregistered oracle version and re-baseline with two clean controls).
- **`shard-wake`** — **data conservation + recovery convergence** (seed claims #3, #5). Cleaner: two
  controls, real flaky headroom, and a coverage gap that does not touch the measured subcase.

Because both tasks' headroom is **flaky (~50% control pass)**, the next step is the program's first
real treatment-vs-control A/B on the seed's home turf, designed as a **pass-rate comparison** —
roughly ten trials per arm per task — measuring whether the seed shifts the pass rate on each task's
headroom subcase (`orbit-slots`: canonical-validation rejection; `shard-wake`: `replace_3`
convergence/conservation). This is the fairest test the program has mounted, and the first that puts
the seed where it is supposed to be strongest. It has not yet been run.

---

## 9. The methodology, crystallized

What began as "run the tool and see" became a small but real experimental apparatus:

- **Two LLMs, three roles, deliberately separated:** Kiro/Claude as analyst + experimenter; Codex as
  independent task author; Claude `sonnet-4-6` as the *subject under test*. The roles that care about
  the outcome are separated from the role that writes and grades the traps.
- **Matched A/B with byte-identical, seed-neutral prompts** — behavior is *observed*, not instructed.
- **Withheld oracles + ground truth over self-report** — no LLM-as-judge; grading is executable tests
  and fault injection. The seed's own impact record is treated as a *claim to be checked*, never as
  evidence.
- **Pre-registration** of hypotheses, concrete subcases, and calibration mappings *before* any run.
- **Difficulty screening on the control arm only**, keeping tasks where the bare model genuinely
  fails — selecting on *difficulty*, never on whether the seed wins.
- **Contract-Coverage Gate** — the fix born from our own instrument's failure.
- **Physical isolation** of the design workspace — the strongest available guarantee against
  contamination.
- **Cost is negligible** (~US$0.2–0.5 per run; a full control screen is ~US$4), so rigor is not
  budget-limited.

---

## 10. Why it is hard, and the line between learning and fitting

It is worth saying plainly why five rounds produced so few runnable tasks, because the difficulty is
not incidental — it is structural, and understanding it is half the result.

The goal sounds trivial ("does the seed make the agent write better code?"), yet nearly every
obvious way to measure it is booby-trapped, and each difficulty is *forced* by solving the one
before it. To see a benefit you need a task the bare model can *fail* — but a frontier model rarely
fails a self-contained task, so the usable difficulty band is narrow (rounds 1–2, and four of five
tasks in both R4 and R5, saturated). The obvious source of hard tasks — public benchmarks — is
*contaminated*, so the model recalls instead of reasoning, bypassing the very discipline under test;
hence bespoke, novel tasks. Inventing your own tasks invites *author bias*, hence an independent
designer (Codex) — but that designer is itself an LLM that may share blind spots with the subject.
And grading a novel task *perfectly* is genuinely hard: miss one contract clause and a sloppy
solution passes anyway, so a "pass" is a lie — which is exactly what sank R4B and R5. Layered on top,
the system is *nondeterministic*, so single runs mean little and you must compare *pass rates* over
many trials — and the most informative tasks (the flaky, near-50% ones) need the *most* trials to
separate signal from luck.

The scarce resource, then, is not money — runs cost pennies — it is **the yield of valid,
discriminating tasks.** Across three design rounds we authored roughly eighteen candidates and
salvaged two: `orbit-slots` and `shard-wake`. Every usable task costs a full design session, a
self-invalidation cycle, and an independent ground-truth review. The ambition of the question is
broad (seven claims, general code quality, across models); the evidence any one round can
manufacture is narrow. The correct response is not to inflate the budget but to **scope the claim to
the evidence** — which is precisely what the program has done as it narrowed from "does the seed
improve quality?" to "on this recovery-shaped task, for this model, does the seed shift the pass
rate?"

This raises the obvious, tempting idea: since we have learned so much from the tasks that failed, why
not *fit the next tasks toward the ones that half-worked*? The answer is a single, load-bearing
distinction — the line this whole program exists to hold.

**Learning the genre is legitimate; fitting to the outcome is not.** From the failures we can and
should learn *task shape and difficulty*: validate-then-save saturates; recovery/convergence,
conflict-against-existing-state, and representational validation produce headroom. Feeding those
*design principles* into the next round is good science — it is exactly why we pivoted to the
recovery axis. What we must never do is tune an individual task or its oracle based on the *outcomes
we observed* — above all, anything the *seeded* arm did. The moment task design is driven by the
results it produces, you have stopped *measuring* the seed and started *manufacturing* a contrast. In
statistical terms that is **selecting on the dependent variable**: you can always tweak a task until
it yields the answer you were hoping for, and then neither a skeptic nor your later self can tell
whether the effect was real or engineered. That is syok-sendiri wearing a lab coat, and it is the
precise failure the firewall exists to prevent — hence "do not run the treatment arm during design"
and "never repair an oracle on observed results."

There is also a plainer reason not to fit to the half-successes yet: **we do not know the direction
finely enough to fit to it.** `shard-wake`'s headroom is a one-of-two coin flip on a single subcase;
with n = 2 we cannot tell whether `replace_3` is reliably hard or simply got unlucky once. To fit to
it now would be to optimise on noise. You must first *establish* the signal, then converge on it.

The honest way to converge — and the real answer to "we need hundreds of tests" — is therefore
**population-level, not per-task**:

1. Extract the working genre as design principles (recovery seams, existing-state conflicts,
   interrupted-operation retry, representational validation).
2. Have an independent, treatment-blind designer **mass-produce** that genre — dozens to hundreds of
   tasks.
3. Run them all through the **control-only difficulty screen** (cheap — pennies per run).
4. Keep only the tasks with *reliable* headroom, selected on control-difficulty and **pre-registered
   before the seed ever runs.**
5. Only then run the seed against the survivors, as a pass-rate comparison.

This "fits toward the successful profile" honestly: the failures teach the genre, the screen filters
for difficulty, and the selection is blind to the seed — so the eventual measurement stays clean. It
is how two flaky probes become a powered experiment without anyone, ourselves included, tipping the
scale.

## 11. What we actually know (stated honestly)

**Survives falsification:**
- The objective-trigger steering fix **reliably causes native skill invocation** — 10/10 treatment
  vs 0/10 control across two independent randomizations. Robust.
- The seed reliably **emits an impact record** and **increases self-verification activity** (~4×).
- The seed shows **cleaner commit scope** (excludes untracked scaffold; 0 leaks when measured).

**Disconfirmed / not supported:**
- A **general code-quality or correctness lift**. On the one round with real failure headroom
  (Round 3), the seed produced no improvement (1/3 vs 1/3; 108 vs 109; one task worse).
- **Calibrated self-assessment.** The impact record over-claimed coverage relative to ground truth,
  precisely on the error/edge cases it named.

**Not yet measured (the immediate next step):** whether, on **novel, uncontaminated** tasks in the
seed's own claimed home turf, the seed produces a real, calibrated outcome difference. Round 5 did
not run this A/B — its slate self-invalidated on the coverage-gate regress — but it produced **two
ground-truth-validated probes** (`orbit-slots` for input validation, `shard-wake` for
conservation/recovery). The pending experiment is a **pass-rate A/B** on those two tasks, the
strongest fair test yet because it puts the seed where it *should* be strongest.

---

## 12. Limits, honestly named

- **Small n, one model, one runtime.** Everything is bounded to `sonnet-4-6` (CLI 2.1.211 for
  Round 1, 2.1.212 thereafter) via Bedrock; results are **directional, not statistical**.
- **The independent author is itself an LLM.** Codex may share blind spots with the model under
  test, so a "novel-to-us" task might still sit in a region both models reason about identically.
  This is the largest residual threat and cannot be fully closed from inside the LLM ecosystem.
- **Reactive design.** Round 3 onward was designed *after* seeing earlier results. We mitigated with
  external benchmarks, withheld oracles, an independent author, physical isolation, and
  pre-registration — but the ideal (a fully pre-committed protocol) is only approximated.
- **Contamination is a moving target.** Public benchmarks are contaminated; bespoke tasks are novel
  but author-biased. There is no perfectly clean option, only trade-offs we name.

---

## 13. Closing

The honest state of the program: **the seed reliably changes an agent's *process* — it loads, it
narrates an impact record, it tests more — but it has not yet been shown to change *outcomes* on
tasks hard enough to matter, and its self-assessment over-claims.** That is not a failure of the
program; it *is* the program working. We set out to falsify, and we found the seed's real edge
(reliable invocation, commit hygiene) and its real weakness (uncalibrated, unfocused quality
evidence) rather than a flattering story.

Round 5 will tell us whether the seed earns its keep on its own home turf, measured by an oracle we
have finally taught to cover the whole contract. Whatever it shows, it will be ground truth — not
syok sendiri.
