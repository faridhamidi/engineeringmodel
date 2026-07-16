<!--
Type: Forward document (meta-operation)
Status: draft
Origin: exploration of whether the seed is usable by AI-fluent builders without a software-engineering background
Owner: repository maintainer (assign on adoption)
Last verified against: repository state at commit 9005440 (main)
Revision note: scope narrowed to translation. Earlier drafts carried a deterministic
"subsystem / harness" and a two-tier enforcement model; that material was removed as
out of scope. Enforcement of consequential actions belongs to the system that owns
the state, not to this layer. This layer translates and guides only.
Supersedes / superseded by: —
-->

# Forward Document — A Builder-Accessible Translation

**Non-binding direction.** This document proposes where the repository could go and
in what order. It commits to nothing. When an item here is selected, it becomes a
design document; when it establishes a durable rule, that rule becomes an ADR. See
[`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md).

The single idea: **translate the interface, leave the engine untouched.**

---

## Who this document is for

Two audiences at once:

- **Curious senior people without a software-engineering background.** You direct,
  build, and operate real systems through an AI assistant. You may not know terms
  like *boundary* or *blast radius*. Every such term is defined in plain words in the
  [Glossary](#glossary). You should be able to read this top to bottom and understand
  the shape of the proposal.
- **People who already know this repository in its raw state.** The key claims for
  you: this operation adds a plain-language translation surface over the engine,
  changes nothing in the engine, and obeys the repository's own rules.

If you are the first kind of reader and hit a term you do not recognise, jump to the
Glossary and come back. That round-trip is the whole idea of this plan.

---

## The problem

The methodology here is written by experienced engineers for experienced engineers.
It is *compression*: each instruction ("name the boundaries", "declare the system's
language") stands for a large body of hard-won experience. A reader with that
experience decompresses it instantly. A reader without it sees an instruction with no
mechanism and no way to tell when it applies.

Meanwhile, a growing group builds and operates real systems **through AI, without
that background**. They meet the exact failure modes this repository exists to prevent
— mixing decisions with side effects, acting on stale data, doing things they cannot
undo — but by a different path, and they cannot decompress the current text.

**Goal:** make the methodology usable for that group **without lowering its
fidelity**. Not a simpler methodology — the same methodology, reached through a
different interface.

---

## What this operation is *not*

1. **Not "dumbing it down."** Dumbing down removes the hard parts and loses fidelity.
   That produces a friendly document that makes an unqualified operator *feel* safe
   while stripping out the nuance that kept them safe. A false sense of safety is
   worse than none. We relocate complexity; we do not delete it.
2. **Not a fork or a rewrite of the engine.** The existing layers are the engine and
   **remain exactly as they are.** We add an interface over them, nothing more.
3. **Not optimised for any one substrate.** The consequential system a builder acts on
   may be a cloud account, a shared database, a hosted-application admin console, a
   production server, a billing system, a content platform, or a messaging system.
   The plan names several only as examples; it privileges none.
4. **Not an enforcement mechanism.** This layer translates and guides. It does not by
   itself prevent anything. Where a consequential action must actually be prevented,
   that control lives in the system that owns the state, and is out of scope here.

---

## Guiding principles

1. **Translate the interface, keep the engine.** Like an automatic transmission: the
   gear-changing complexity does not disappear, it moves behind the interface into the
   machine. The driver still makes the decisions that need a human — where to go, when
   to stop — but is relieved of the mechanics. The engine underneath is unchanged;
   only what the driver touches is different.
2. **Two regimes, drawn by a blast-radius line.** *Below* the line (a local, throwaway,
   easily-remade artifact) little or no translation is needed — there was no risk to
   encode. *Above* the line (touches shared state, or cannot be undone) translate fully
   and plainly.
3. **The human sees consequences, not mechanisms.** Questions surface as "what could
   this hurt / can it be undone", not as architecture vocabulary.
4. **Proportionality governs how much to translate.** Translate where the risk earns
   it; leave the low-risk common case light.
5. **The AI carries the translation to the moment it is needed.** A translated document
   the human never reads is inert; the AI is what brings the right plain-language
   question to them when it matters. *How* the AI is packaged and delivered is
   deliberately out of scope for this pass (see open questions).
6. **Enforcement of irreversible actions is not this layer's job.** It lives in the
   substrate, set up once by someone competent. This layer helps a person understand
   and decide; it does not pretend to be the wall.
7. **The operation obeys the repository's own rules.** Proportionality; canonical
   concept ownership (link to the engine, do not restate it); evidence tags;
   confidentiality; plain writing.

---

## The audience model and the two regimes

The persona (generalised, no organisational detail):

> An AI-fluent builder who produces genuine working artifacts — documents,
> presentations, and small applications for a team — and who sometimes operates on
> shared systems on behalf of others. They think in outcomes, not mechanisms. They
> may not use version control directly. Their AI writes the code; they direct and
> operate it.

The persona spans **two risk profiles**, and the whole design turns on telling them
apart:

```text
                      the blast-radius line
                              |
  BELOW  (build freely)       |   ABOVE  (stop and think)
  --------------------------- | ---------------------------
  local tool, personal doc,   |   changes shared state,
  easily re-created output    |   grants access, or cannot
                              |   be undone in one step
  risk ≈ losing your own work |   risk ≈ affecting others /
                              |   irreversible effect
  need: build freely +        |   need: plain-language
        a save point          |   consequence questions
```

A single instruction like "be careful" fails because it does not tell the persona
*where the line is*. The translation's first job is to **draw that line for them**,
in plain language.

---

## How the pieces relate

Three things, one of which does not change:

- **The engine** — the existing `core/` and `governed-automation/` layers. The source
  of truth. **Unchanged.** The AI reads it; the human need not.
- **The translation surface** — a plain-language interface that restates the engine's
  *questions and consequences* (never its mechanisms) for a reader without an
  engineering background, and links back to the engine for the "why".
- **The AI** — reads both, and brings the right plain-language question to the human at
  the moment it matters. Its packaging and delivery are out of scope for this pass.

Real prevention of irreversible actions is not on this list. It lives in whichever
system owns the shared state (a scoped role, deletion protection, a backup), set up
once by someone competent. This layer helps a person understand and decide; it is not
the wall.

---

## Scope: what stays, what is translated, what is new

### A. Engine — keep as-is (the AI reads it; the human need not)

Already written for a competent reader, and an AI is a competent reader. Translating
them would be the dumbing-down mistake.

- `core/FOUNDATION.md`, `core/SEMANTIC_CONSISTENCY.md`, `core/TESTING.md`,
  `core/CONFORMANCE_HARNESS.md`, `core/DOCUMENTATION.md`
- `governed-automation/PRINCIPLES.md`, `MODELS.md`, `VOCABULARY.md`,
  `ADOPTION_CHECK.md`, `AUTOMATED_AUTHORITY.md`
- `examples/`

### B. Translate — only the human-judgment surfaces

Small, high-value. Each becomes a plain-language question that links to its engine
source:

- the "choose your layer" gate in `README.md` → the plain-language blast-radius line;
- the adoption gates in `governed-automation/ADOPTION_CHECK.md` → consequence questions;
- `governed-automation/DECISION_TREE.md` → already the closest to translated; the
  natural starting point;
- the foundation checklist in `core/FOUNDATION.md` → the "basics" for below-the-line
  work.

### C. Net-new — the "safe operation" floor

Does not exist today; the highest-value gap for the audience. It sits *below* Core
Hygiene, in plain language:

- what "publish / deploy / apply / send" actually does, and how it differs from "save";
- make an undo point (backup / snapshot) before anything irreversible;
- least privilege — do not operate as the most powerful role for an everyday task;
- version history as plain "save points";
- "what does this touch that other people rely on?" as a habitual question.

---

## Proposed deliverables

A plain-language translation surface over the engine. Placement to be confirmed (see
open questions); working assumption is a top-level `builders/` directory so the
surface stays linked to the engine it points at.

1. **`builders/START_HERE.md`** — the blast-radius line as a *human question*. Routes
   below → "build it, here are the basics"; above → "stop, answer these first."
   Highest leverage; everything else depends on where it draws the line.
2. **`builders/SAFE_OPERATION.md`** — the net-new floor (Bucket C), plain language.

The surface **links** into `core/` and `governed-automation/` for all mechanisms; it
does not restate them (canonical concept ownership).

*Deferred (out of scope for this pass):* how an AI is packaged to deliver these in the
moment.

---

## Phased order

```text
Phase 0  Direction                    (this document)
Phase 1  Translate the line           (START_HERE)
Phase 2  Translate the safe floor      (SAFE_OPERATION, net-new)
Phase 3  Translate remaining surfaces  (bucket B)
Phase 4  Validate by falsification     (does the line route two contrasting cases
                                        correctly? fix the line first if not)
Phase 5  Promote durable rules to ADRs
```

**Candidate ADR:** *The builder surface is a translation over the engine, not a second
methodology.* It may pose questions and link to mechanisms; it may not restate or
weaken them.

---

## Validation and falsification design

The translated line must correctly route at least one clearly-*below* case and one
clearly-*above* case — for example, a purely local personal tool (must route below)
and an action that changes state other people depend on (must route above). Misrouting
either is a defect fixed before anything downstream.

A change that softens the line's wording merely to make an awkward case pass must state
which distinction it gave up.

---

## Meta-consistency self-audit

The operation is held to the same rules it distributes:

| Repository rule | How this plan complies |
|---|---|
| Engine untouched | The engine layers are read, never modified |
| Proportionality | Translate above the line; leave the low-risk case light |
| Canonical concept ownership | The surface links to `core/`/`governed-automation/`; it does not restate mechanisms |
| Evidence tags | Every claim here is **proposed** / **inferred**; nothing is implemented |
| Confidentiality | Persona and substrates are generalised; no organisational detail |
| Writing rules | Plain language; no "production-ready" or framework comparisons as value claims |

---

## Risks, open questions, evidence boundary

**Primary risk.** A translation that reads as *reassurance* — making a reader feel safe
— without a real control behind it. The translation must state plainly when a genuine
control is required and that it lives in the substrate, not in these words.

**Open questions.**

- Does the builder surface live in this repository (`builders/`) or a companion?
- How is the AI packaged to deliver the translation in the moment? (Deferred here.)
- Should the below/above line also be a first-class Core Hygiene check, or remain
  builder-surface only?

**Evidence boundary.** Everything here is **proposed** and **inferred**. No
implementation, no operating record. No claim should inherit the confidence of the
engine's existing, tested witnesses. This is a direction to be tested, not a result.

---

## Glossary

Plain-language definitions for readers without a software-engineering background.
Informal on purpose; the precise treatments live in the engine layers.

- **Substrate** — the system that actually holds the shared, valuable state you might
  affect (a cloud account, a shared database, an admin console, a production server, a
  payments system, and so on).
- **Blast radius** — how far the damage spreads if something goes wrong. A personal
  draft has a small blast radius; changing a system many people rely on has a large one.
- **Boundary** — a clean line between the part of a system that *decides* something and
  the part that *acts* on the outside world, so each can be understood on its own.
- **Irreversible / cannot be undone** — an action with no easy "undo": deleting shared
  data, sending a message to many people, changing who has access.
- **Least privilege** — use the least powerful access that gets the job done, so a
  mistake cannot reach further than the task.
- **Save point / version history** — a saved snapshot you can return to. The everyday
  face of what engineers call version control.
- **Ergonomics** — how easy and low-effort something is for a person to use. Here, the
  AI's job is ergonomics: making the safe path the easy path.
