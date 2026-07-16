<!--
Type: Synthesis note (design conclusions + candidate ADRs)
Status: draft
Origin: design discussion on making the seed usable by AI-fluent builders without a software-engineering background
Owner: repository maintainer (assign on adoption)
Last verified against: repository state at commit 037112a (main)
Related: .meta/builder-accessible-layer.md (forward document)
-->

# Synthesis — Making the Seed Usable by AI-Native Builders

This note compiles the durable conclusions from a design discussion. The worked
direction and phased plan live in the [forward document](builder-accessible-layer.md);
this records the *settled principles*, the *candidate durable rules*, and the *open
questions*, so the reasoning is not lost and does not have to be reconstructed.

**Evidence:** everything here is **proposed** / **inferred** except where marked
*implemented*. Only Phase 1 (below) has code and tests.

## The problem in one line

The methodology is an *engine* written by experienced engineers for experienced
engineers — compression that a reader must already have the experience to decompress.
A growing group builds and operates real systems **through AI, without that
background**, meets the same failure modes by a different path, and cannot decompress
the current text.

---

## Settled conclusions

### A. Framing

1. **Engine vs. interface (the automatic transmission).** Make the methodology usable
   without lowering fidelity by *relocating* complexity behind an interface, not
   deleting it. The engine stays unchanged; only what the user touches changes.
2. **Do not "dumb it down."** Dumbing down lowers fidelity and produces a *false sense
   of safety* — worse than none. The correct move is translation, not simplification.
3. **Two regimes, one line.** A blast-radius line splits work by two observable
   signals — *does it touch shared ground?* and *can you undo it yourself easily?*
   Below the line: build freely. Above: stop and think.

### B. Roles, and what *not* to build

4. **AI for ergonomics; determinism for authority.** Three roles: the human judges
   consequences; the AI proposes and unburdens; a control in the owning system is the
   only real wall for irreversible effects. The AI is never the wall.
5. **No harness in the builder-facing layer.** A harness *reports* and demands
   interpretation, so it presupposes exactly the understanding this audience lacks.
   Three responses to "the operator does not understand X": **teach it** (AI guide),
   **remove the need** (a silent guardrail / the substrate wall), or **report it**
   (a harness — the wrong tool here).
6. **The elaborate deterministic subsystem was over-built.** It ironically violated
   the engine's own proportionality rule. The core collapses to **translated prose +
   an AI that guides** — plus a real control in the substrate for irreversible actions.

### C. The active ingredient

7. **Steering is the expression; the engine is the genome.** The methodology is inert
   as prose in a repository; it *acts* only when it shapes an agent's behavior at the
   moment of work. Steering is that projection — and it is what makes the seed grow in
   someone else's soil, and what serves technical and non-technical users alike
   (because it steers the AI, not the person). Steering must **reference** the engine,
   never restate it, or it drifts into confident, cargo-cult wrongness.
8. **Simple front, full engine behind.** The front is a *thin router* — observable
   triggers, imperatives, and a fail-closed default — that routes into the unchanged
   engine. "Simple" must mean *thin router*, not *lossy summary*; the latter is the
   dumbing-down trap one level up. Triggers must be *observable events*, not concepts.
9. **Two front doors, one engine.** [`builders/START_HERE.md`](../builders/START_HERE.md)
   is the human's front door; an agent-facing steering router is the agent's. One
   routing table, two projections, one engine. A reference ratchet keeps both from
   drifting off the engine.

### D. Autonomy and safety

10. **Act-first, revert-if-disliked** is optimal *below* the line and catastrophic
    *above* it — because "above the line" is defined as the place where revert is not
    available.
11. **The whole-sequence discipline reduces to one rule:** keep everything inside the
    revertible envelope, and hard-stop only when about to leave it. Everywhere inside,
    full autonomy, no asking.
12. **Revertibility ≈ git.** The concrete mechanism is: the agent **commits
    generously and automatically**, operating git *for* the user (hidden from the
    non-technical persona). One mechanism yields three things at once — an undo stack,
    an audit trail, and provenance. Guard: **never commit secrets or junk**, because
    git history is the one save point a commit cannot cheaply undo. Honest limit:
    **git makes *authoring* revertible, not *acting*** — a commit undoes the code that
    caused a deploy, not the deploy. So the hard stop stays at irreversible *substrate
    effects*.
13. **Consent follows revertibility.** Acting without asking is legitimate while the
    user can always undo. Where there is no undo, explicit consent is the user's only
    chance to judge — so that, and only that, is where the agent pauses.

### E. Feasibility

14. **The unburdening is buildable today.** What produces seamless unburdening
    (reconciling "master" → "main"; adding a `.gitignore` unprompted) is base-model
    disposition + steering/system-prompt + tools + the agent loop — not a bespoke
    fine-tune and not a deterministic harness. Fine-tuning would only make the
    dispositions cheaper and more reliable; it is an optimization, not a prerequisite.

---

## Candidate durable rules (ADRs)

Worth deciding once and recording as ADRs:

- **The AI is never the enforcement layer.** Ergonomics may be non-deterministic;
  authority over irreversible effects is not the AI's to grant.
- **The builder surface is a translation over the engine, not a second methodology.**
  It may pose questions and link to mechanisms; it may not restate or weaken them.
- **Steering references the engine; it never restates it.** Drift is checked
  mechanically (reference integrity).
- **Keep everything in the revertible envelope.** The agent commits automatically;
  it pauses only at irreversible substrate effects.
- **No harness in the builder-facing layer.**

---

## Current implementation state

*Implemented and pushed (commit 037112a):*

- the [forward document](builder-accessible-layer.md) (translation-scoped);
- [`builders/START_HERE.md`](../builders/START_HERE.md) — the human front door (the
  blast-radius line as one plain-language question);
- [`builders/_witness/`](../builders/_witness/) — a decision oracle with minimal
  falsifiers and a zero-violation reference-integrity ratchet, wired into CI
  (*implemented, tested*).

The engine layers (`core/`, `governed-automation/`) are unchanged.

---

## Open questions (unresolved)

1. **The minimal trigger set for the front.** We agreed on observable triggers
   (deploy / delete / grant / change-shared-state) and a fail-closed default, but the
   complete set is not enumerated. This is the main design work still owed.
2. **Packaging of the agent-facing front** — an `AGENTS.md` entry, a steering file, or
   a skill. The *shape* (thin router) is settled; the concrete home is not.
3. **The substrate-wall handoff.** The front states that a real control lives in the
   substrate, but nothing ensures that control exists, and — for the non-technical
   persona especially — who establishes it and how the front verifies or reminds is
   unresolved. This is the safety-critical gap.
4. **Git bootstrapping for the non-technical persona.** "The agent commits for them"
   assumes a git repository exists; initializing git for someone who has never used it
   is an unaddressed first step.

---

## Evidence boundary

Everything here is a direction to be tested, not a result. No claim should inherit the
confidence of the engine's existing tested witnesses. Only Phase 1 is implemented and
tested; the rest is reasoning that awaits validation against real cases.
