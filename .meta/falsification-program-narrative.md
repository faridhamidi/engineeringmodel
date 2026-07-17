<!--
Type: Narrative report (program history)
Status: living — brings the audit trail from the first Kiro-steered sessions through Round 5 (in progress)
Origin: synthesizes seed-cleanroom-observation.md, seed-codex-cleanroom.md, claude-new-steering-behavioral-tests.md,
        claude-quality-steering-cleanroom.design.md, claude-quality-steering-cleanroom-result.md,
        and the round-4/4b/5 clean-room work in the (out-of-repo) harness.
Last updated: 2026-07-17
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

A recurring theme emerges and is worth flagging up front, because it is almost poetic: **the seed's
core weakness turned out to be a coverage claim that outran reality — and later our own experimental
oracle failed in exactly the same way, and the same discipline caught it.** The method ate its own
tail, honestly.

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
tests. Findings folded into `seed-codex-cleanroom.md`.

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

## 8. Act VI — Brief v2, an isolated clean room, and Round 5 (now)

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

**Round 5 is running now.** A fresh, isolated Codex session is designing a new pool on the
recovery/persisted-state axis, coverage-gated, pre-registered, and difficulty-screened on the control
arm only. When it finishes, the plan is the same ground-truth review applied to Round 4B: run each
oracle against both wrong-variants, confirm the Coverage Gate is real rather than asserted, and verify
pre-registration preceded any run — *then* run the treatment-vs-control A/B (kept out of the design
session to preserve the firewall).

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

## 10. What we actually know (stated honestly)

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

**Not yet measured (Round 5's job):** whether, on **novel, uncontaminated** tasks in the seed's own
claimed home turf (recovery/atomicity/consistency), the seed produces a real, calibrated outcome
difference — the strongest fair test yet, because it puts the seed where it *should* be strongest.

---

## 11. Limits, honestly named

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

## 12. Closing

The honest state of the program: **the seed reliably changes an agent's *process* — it loads, it
narrates an impact record, it tests more — but it has not yet been shown to change *outcomes* on
tasks hard enough to matter, and its self-assessment over-claims.** That is not a failure of the
program; it *is* the program working. We set out to falsify, and we found the seed's real edge
(reliable invocation, commit hygiene) and its real weakness (uncalibrated, unfocused quality
evidence) rather than a flattering story.

Round 5 will tell us whether the seed earns its keep on its own home turf, measured by an oracle we
have finally taught to cover the whole contract. Whatever it shows, it will be ground truth — not
syok sendiri.
