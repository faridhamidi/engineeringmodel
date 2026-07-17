<!--
Type: Forward document (meta-operation)
Status: realized (historical direction retained for provenance)
Origin: exploration of whether the seed is usable by AI-fluent builders without a software-engineering background
Owner: repository maintainer (assign on adoption)
Last verified against: builder-layer implementation dated 2026-07-16
Revision note: (1) scope was first narrowed to translation; an earlier deterministic
"subsystem / harness" and two-tier enforcement model were removed. (2) The direction
then evolved (delivery, git, human approval, autonomy) and was promoted to
DD-001-builder-accessible-layer.md, which now owns the worked plan. This document was
reconciled to state the current direction and defers all "how" detail to the design
document.
Supersedes / superseded by: realized through DD-001-builder-accessible-layer.md; durable rules in ADR-001-builder-accessible-layer.md
-->

# Forward Document — A Builder-Accessible Translation

**Historical non-binding direction.** This document records where the repository chose
to go and in what order. The implementation is complete and approved; durable rules
live in [ADR-001](ADR-001-builder-accessible-layer.md). See
[`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md).

The single idea: **translate the interface, leave the engine untouched.**

**Realized through:**
[`DD-001-builder-accessible-layer.md`](DD-001-builder-accessible-layer.md), the
historical worked design. This document states direction and provenance only.

---

## Current direction (evolved)

Beyond the original translation-only framing, the direction settled on four points.
Each is specified in the design document; stated here at direction level:

1. **Delivery is decided (no longer deferred).** The translation reaches the moment of
   work as **always-on steering** — front matter, whole-workflow, no keyword triggers —
   that calls the **engine as an on-demand skill** in the open
   [Agent Skills format](https://agentskills.io/specification). The reusable
   `engineering-model` package carries parity-checked engine projections and steering
   templates. Consuming agents install the skill and place the marked steering block
   in native always-on surfaces; this repository exercises both `AGENTS.md` and
   `CLAUDE.md`.
2. **Git is the revertibility substrate.** Git is a requirement; the agent commits
   coherent, verified, task-owned increments *for* the user (undo + audit + provenance
   in one). Ambiguous ownership remains uncommitted. This is what lets the agent act
   autonomously and still be safe.
3. **External effects need a human.** The agent is steered to **always ask for explicit
   human approval before any external-substrate effect.** This is a procedural norm,
   not a technical wall; a real wall is recommended and lives in the substrate.
4. **Autonomy below the line, a hard stop above it.** Below the line the agent acts
   freely and the user reverts anything they dislike; the only non-negotiable pause is
   an external-substrate effect.

---

## Who this document is for

Two audiences at once:

- **Curious senior people without a software-engineering background.** You direct,
  build, and operate real systems through an AI assistant. You may not know terms like
  *boundary* or *blast radius*; every such term is defined in the [Glossary](#glossary).
- **People who already know this repository in its raw state.** The key claims: this
  operation adds a plain-language interface over the engine, changes nothing in the
  engine, and obeys the repository's own rules.

---

## The problem

The methodology here is written by experienced engineers for experienced engineers.
It is *compression*: each instruction ("name the boundaries", "declare the system's
language") stands for a large body of hard-won experience. A reader with that
experience decompresses it instantly; a reader without it sees an instruction with no
mechanism and no way to tell when it applies.

Meanwhile, a growing group builds and operates real systems **through AI, without that
background**. They meet the exact failure modes this repository exists to prevent —
mixing decisions with side effects, acting on stale data, doing things they cannot undo
— but by a different path, and they cannot decompress the current text.

**Goal:** make the methodology usable for that group **without lowering its fidelity**.
Not a simpler methodology — the same methodology, reached through a different interface.

---

## What this operation is *not*

1. **Not "dumbing it down."** Dumbing down removes the hard parts and loses fidelity,
   producing a friendly document that makes an unqualified operator *feel* safe while
   stripping out the nuance that kept them safe. A false sense of safety is worse than
   none. We relocate complexity; we do not delete it.
2. **Not a fork or a rewrite of the engine.** The existing layers are the engine and
   **remain exactly as they are.** We add an interface over them.
3. **Not optimised for any one substrate.** The consequential system a builder acts on
   may be a cloud account, a shared database, an admin console, a production server, a
   billing system, a content platform, or a messaging system. The plan names several
   only as examples; it privileges none.
4. **Not a technical wall.** This layer translates, guides, and steers the agent to ask
   a human before external-substrate effects. It does not itself *prevent* those effects
   — a real control for that lives in the system that owns the state
   (recommended, out of scope here).

---

## Guiding principles

1. **Translate the interface, keep the engine.** Like an automatic transmission: the
   gear-changing complexity does not disappear, it moves behind the interface into the
   machine. The driver still makes the decisions that need a human; the engine
   underneath is unchanged.
2. **Two regimes, drawn by a blast-radius line.** *Below* the line (a local, throwaway,
   easily-remade artifact) act freely. *Above* the line (touches shared state, or
   cannot be undone) stop and think.
3. **The human sees consequences, not mechanisms.** Questions surface as "what could
   this hurt / can it be undone", not as architecture vocabulary.
4. **Proportionality governs how much to translate.** Translate where the risk earns
   it; leave the low-risk common case light.
5. **Delivery is always-on steering that calls the engine as a skill.** A document the
   human never reads is inert; always-adhered steering brings the right plain-language
   question when it matters, and pulls in the engine (an on-demand skill) for depth.
   *(Decided; specified in the design document.)*
6. **External effects require a human, not a wall in this layer.** The
   agent is steered to always ask for explicit approval before an external effect; the
   un-bypassable wall, if wanted, lives in the substrate, set up once by someone
   competent. This layer helps decide and pauses; it does not pretend to be the wall.
7. **Keep work inside a revertible envelope.** The agent commits at coherent, verified
   task boundaries and includes only task-owned changes. Git is the substrate that lets
   work below the line be undone; ambiguous ownership fails closed to an uncommitted
   report.
8. **The operation obeys the repository's own rules.** Proportionality; canonical
   concept ownership (link to the engine, do not restate it); evidence tags;
   confidentiality; plain writing.

---

## The audience model and the two regimes

The persona (generalised, no organisational detail):

> An AI-fluent builder who produces genuine working artifacts — documents,
> presentations, and small applications for a team — and who sometimes operates on
> shared systems on behalf of others. They think in outcomes, not mechanisms. They may
> not use version control directly. Their AI writes the code; they direct and operate it.

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
  need: act freely +          |   need: ask a human first
        auto-committed         |   (explicit approval)
```

The layer's first job is to **draw that line** — in plain language for the human, and
as an always-on semantic condition for the agent (fail-closed: when unsure, treat as
above the line).

---

## How the pieces relate

- **The engine** — `core/` and `governed-automation/`. The source of truth,
  **unchanged**, delivered to the agent through generated, parity-checked references in
  the on-demand `engineering-model` skill.
- **The steering front matter** — always adhered, whole-workflow: draws the line, acts
  below it, commits coherent, verified, task-owned increments, asks a human before
  external effects, and calls the engine skill for depth. The package owns the canonical
  block; native `AGENTS.md` and `CLAUDE.md` surfaces carry exact checked copies.
- **The human front door** — [`builders/START_HERE.md`](../builders/START_HERE.md): the
  same line in plain language for the person.
- **Git** — the required revertibility substrate the agent operates *for* the user.

Real prevention of irreversible effects is a substrate control (recommended), not part
of this layer. The [design document](DD-001-builder-accessible-layer.md) specifies each
piece and how it is verified.

---

## Scope: what stays, what is translated, what is new

### A. Engine — keep as-is (the AI reads it; the human need not)

- `core/FOUNDATION.md`, `core/SEMANTIC_CONSISTENCY.md`, `core/TESTING.md`,
  `core/CONFORMANCE_HARNESS.md`, `core/DOCUMENTATION.md`
- `governed-automation/PRINCIPLES.md`, `MODELS.md`, `VOCABULARY.md`,
  `ADOPTION_CHECK.md`, `AUTOMATED_AUTHORITY.md`
- `examples/`

### B. Translate — only the human-judgment surfaces

Each becomes a plain-language question that links to its engine source:

- the "choose your layer" gate in `README.md` → the plain-language blast-radius line;
- the adoption gates in `governed-automation/ADOPTION_CHECK.md` → consequence questions;
- `governed-automation/DECISION_TREE.md` → already closest to translated;
- the foundation checklist in `core/FOUNDATION.md` → the below-the-line "basics".

### C. Net-new — the "safe operation" floor

Sits *below* Core Hygiene, in plain language:

- what "publish / deploy / apply / send" actually does, versus "save";
- make an undo point before anything irreversible;
- least privilege — do not operate as the most powerful role for an everyday task;
- **git installed and the project initialized** as a repository — the requirement that
  makes the save-point habit real, and the always-ask-before-external-effects habit.

---

## Deliverables and plan

The worked deliverables, phased order, and verification plan now live in the
[design document](DD-001-builder-accessible-layer.md) (§3–§6). At direction level:

- human front door — `builders/START_HERE.md` — *implemented, tested*;
- the safe-operation floor — `builders/SAFE_OPERATION.md` — *implemented, structurally tested*;
- cross-platform git prerequisite — `builders/GIT_SETUP.md` — *implemented; platform installation not demonstrated*;
- always-on steering in `AGENTS.md` and `CLAUDE.md` — *implemented, parity-tested*;
- reusable `skills/engineering-model/` package — *implemented, structurally tested*;
- generated standalone engine references — *implemented, parity-tested*;
- executable witnesses for each load-bearing property, run in CI — *implemented*.

Candidate durable rules are tracked in the design document (§9).

---

## Meta-consistency self-audit

| Repository rule | How this plan complies |
|---|---|
| Engine untouched | Canonical engine layers are unchanged; generated skill copies are byte-parity checked |
| Proportionality | Translate/guard above the line; leave the low-risk case light |
| Canonical concept ownership | Surfaces link to the engine; detail lives in the design document |
| Evidence tags | Implemented/tested claims stay separate from runtime and operational claims that remain unproven |
| Confidentiality | Persona and substrates are generalised; no organisational detail |
| Writing rules | Plain language; no "production-ready" or framework comparisons as value claims |

---

## Risks, open questions, evidence boundary

**Primary risk.** A translation that reads as *reassurance* — making a reader feel safe
— without a real control behind it. The layer must state plainly when a genuine control
is required and that it lives in the substrate, not in these words.

**Resolved questions.** Surface placement, AI packaging, and executable treatment of
the blast-radius line were resolved in the design document and promoted to ADR-001.

**Evidence boundary.** The builder surfaces, native steering files, skill package, and
their structural/oracle witnesses are implemented and tested. This proves document
shape, deterministic routing, reference parity, and the presence of load-bearing
norms. It does not prove runtime obedience across every agent, installation behavior on
every client, substrate enforcement, or operational risk reduction.

---

## Glossary

Plain-language definitions for readers without a software-engineering background.

- **Substrate** — the system that holds the shared, valuable state you might affect (a
  cloud account, a shared database, an admin console, a production server, and so on).
- **Blast radius** — how far damage spreads if something goes wrong.
- **Boundary** — a clean line between the part of a system that *decides* and the part
  that *acts* on the outside world.
- **Irreversible / cannot be undone** — an action with no easy "undo": deleting shared
  data, sending to many people, changing who has access.
- **Least privilege** — use the least powerful access that gets the job done.
- **Save point / version history** — a saved snapshot you can return to; the everyday
  face of version control (git).
- **Steering** — always-on instructions the AI reads every time, shaping how it works
  without the person having to manage them.
- **Skill** — a package that gives the AI the engine's depth on demand, loaded only when
  relevant, in the open [Agent Skills format](https://agentskills.io/specification).
  The skill does not make steering always-on by itself; its marked block must also be
  placed in the runtime's native instruction file, such as `AGENTS.md` or `CLAUDE.md`.
- **Revertible envelope** — the zone where anything done can be undone (via git save
  points); the agent acts freely inside it and stops at its edge.
- **Ergonomics** — how easy something is to use. The AI's job is ergonomics: making the
  safe path the easy path.
