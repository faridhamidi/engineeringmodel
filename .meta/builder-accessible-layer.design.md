<!--
Type: Design document
Status: active (binding while active)
Origin: promoted from .meta/builder-accessible-layer.md (forward document)
Owner: repository maintainer (assign on adoption)
Last verified against: repository state at commit acf34b9 (main)
Supersedes / superseded by: —
-->

# Design Document — Builder-Accessible Layer

**Binding while active** (per [`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md)).
This specifies *how* the builder-accessible layer is built and verified. Direction
lives in the [forward document](builder-accessible-layer.md). This document links to
the engine; it does not restate it.

---

## 1. Scope

**In scope.** A layer that lets an AI-fluent builder — technical or not — use the
existing methodology *through their agent*, without lowering the methodology's
fidelity, by projecting it into agent behavior and keeping all work inside a
revertible envelope.

**Out of scope.** Modifying the engine (`core/`, `governed-automation/`); building or
provisioning any substrate-side control; a builder-operated conformance harness.

## 2. Goals and non-goals

**Goals.**

- The methodology shapes agent behavior across the whole workflow, with no reliance on
  the human reading engine documents.
- Works identically for technical and non-technical builders — it steers the agent,
  not the person.
- Every autonomous change stays revertible; irreversible external effects require
  explicit human approval.
- The layer references the engine and never restates or weakens it.

**Non-goals.**

- Not a deterministic wall for external effects (that lives in the substrate;
  recommended, not enforced here).
- Not a keyword-trigger system.
- Not a second methodology.

## 3. Architecture

One line:

> **steering front matter** (always adhered, whole-workflow) → **engine as an
> on-demand skill** → **git as the revertibility substrate**, with **human approval**
> as the external-effect gate.

```text
  ┌───────────────────────────────────────────────────────────┐
  │ STEERING (front matter)   always in context, whole workflow │  the front
  │   - draws the blast-radius line (semantic, fail-closed)     │
  │   - acts autonomously below the line                        │
  │   - commits every change (undo + audit + provenance)        │
  │   - ALWAYS asks approval before external-substrate effects  │
  │   - calls the engine skill when depth/judgment is needed    │
  ├───────────────────────────────────────────────────────────┤
  │ ENGINE (skill, on-demand)   core/ + governed-automation/    │  the depth
  │   - loaded when the steering calls for it                   │
  │   - references engine files; never duplicates them          │
  ├───────────────────────────────────────────────────────────┤
  │ GIT (required substrate)   the revertible envelope           │  the safety net
  │   - installed + repo initialized; agent commits for the user │
  └───────────────────────────────────────────────────────────┘
     Human front door: builders/START_HERE.md  (already implemented)
```

### 3.1 Steering front matter — the always-on front

- **Always in context**, applies to the **entire workflow**, and is **not gated by
  keywords**. It encodes *semantic conditions* the model evaluates ("about to touch
  shared or external state / do something hard to undo"), not literal word matches.
- **Fail-closed:** when a condition is uncertain, treat the action as above the line.
- Responsibilities:
  a. Draw the blast-radius line — *does it touch shared/external ground?* and *can you
     undo it yourself in one step?*
  b. **Below the line:** act autonomously.
  c. **Auto-commit discipline:** ensure each change is committed (undo stack + audit
     trail + provenance in one); never commit secrets or junk.
  d. **External-substrate rule:** always ask for explicit human approval before any
     external-substrate involvement; do not proceed without it.
  e. Call the engine skill when depth or judgment is required.
- Must reference the engine skill and the [human front door](../builders/START_HERE.md);
  must **not** restate engine rationale (canonical concept ownership).

### 3.2 Engine as a skill — on-demand depth

- The engine (`core/`, `governed-automation/`) is exposed as a skill the steering
  invokes. Its description is what causes it to load when the steering calls for it
  (progressive disclosure).
- The skill **references** the engine files as its resources; it does not duplicate
  them.
- **Accepted trade-off:** this ties the layer to agents that support skills. Graceful
  degradation is an `AGENTS.md`-style instruction file for agents that do not.

### 3.3 Git — the required revertibility substrate

- **Git is a hard prerequisite.** Git must be installed **and** the project must be a
  git repository (`git init`). Without a repo, the revertible envelope does not exist.
- The project README documents install + verify across operating systems:
  - macOS (`xcode-select --install` or Homebrew `brew install git`);
  - Windows (winget `winget install --id Git.Git -e`, or the Git for Windows installer);
  - Linux — Ubuntu/Debian (`sudo apt install git`) and Fedora (`sudo dnf install git`);
  - verify with `git --version`.
- The agent **operates git for the user** (hidden from the non-technical persona):
  commit generously and automatically.
- **Honest limit:** git reverts *authoring*, not *acting* — a commit undoes the code
  that caused an external effect, not the effect. External effects therefore still go
  through §3.1(d).

### 3.4 Human front door — existing

- [`builders/START_HERE.md`](../builders/START_HERE.md): the blast-radius line as one
  plain-language question. *Implemented.*

## 4. Workflow discipline (behavior)

The whole-sequence rule: **keep everything inside the revertible envelope; hard-stop
only at the edge.**

```text
1. Ensure the project is a git repository.
2. Make the change.
3. Commit it automatically, with a clear message. Never commit secrets or junk.
4. Is the next action an external-substrate effect (deploy, delete shared data,
   grant access, send to others, mutate a live service)?
     - Yes -> STOP. Ask the human for explicit approval. Do not proceed without it.
     - No  -> continue autonomously; the user can revert any result they dislike.
5. Repeat.
```

Below the line, autonomy is the default and asking is the exception. The only
non-negotiable pause is an irreversible external effect.

## 5. Decisions (resolved open questions)

| # | Decision | Residual / trade-off |
|---|---|---|
| 1 | Triggering lives in always-on steering across the whole workflow; **no keyword set**. Conditions are semantic and model-evaluated. | Relies on model judgment; mitigated by the **fail-closed** default. |
| 2 | The engine's home is a **skill**; steering (front matter) calls it. | Couples the layer to skill-supporting agents; `AGENTS.md` fallback exists. |
| 3 | External-substrate effects stay under **explicit human approval**, steered as a standing norm; no wall is built here. | **Procedural** safety, not a hard wall. The seed *recommends* a substrate control for hard guarantees. |
| 4 | **Git is required** and the repo must be initialized; README documents install across OSes. | Adds a prerequisite; justified because it is the revertibility substrate. |

## 6. Verification plan (walk the talk)

**Already implemented and in CI** (`.github/workflows/executable-witnesses.yml`):

- decision-oracle witness — both signals load-bearing, uncertainty fails closed;
- reference-integrity ratchet on `START_HERE.md` — zero-violation, with a known-bad case.

**To add (each: stdlib only, no credentials, a known-bad case, runs in CI):**

- extend reference-integrity to the steering front matter and the skill document —
  every engine reference must resolve (zero-violation);
- a structural presence check that the steering front matter carries its load-bearing
  norms — the external-approval rule, the auto-commit rule, and the fail-closed
  default are present; removing any one is the minimal falsifier;
- the two-case falsification: one clearly-below case continues autonomously; one
  clearly-above case (an external effect) triggers the approval pause.

A change that weakens a norm, its checker, and its falsifier together to make CI pass
is not evidence of safety; it must state which protected property changed.

## 7. Accepted trade-offs and residual risks

- **Procedural, not enforced, safety for external effects.** Rests on the steering
  norm holding. Recommend a real substrate control for anyone needing hard guarantees.
- **Skill coupling.** Ties the layer to skill-supporting agents; `AGENTS.md` fallback.
- **Steering is non-deterministic.** The fail-closed default, the human-approval pause,
  and the git envelope are mitigations — none is a guarantee. The layer is honest that
  it *helps decide*; it is not the wall.

## 8. Evidence boundary and status

- **Implemented / tested** (commits `037112a`, `acf34b9`): `builders/START_HERE.md`
  and `builders/_witness/`.
- **Proposed** (this document): the steering front matter, the engine-as-skill
  packaging, the git-prerequisite README, and the extended verification.

No proposed item should inherit the confidence of the implemented, tested witnesses.

## 9. Candidate ADRs (promote after implementation)

- The AI is never the enforcement layer.
- The builder surface translates the engine; it never restates or weakens it.
- Steering references the engine; drift is checked mechanically.
- Keep everything in the revertible envelope: the agent commits automatically; it
  pauses only at irreversible external effects.
- No harness in the builder-facing layer.
- Engine-as-skill, with an `AGENTS.md` fallback for non-skill agents.

## 10. Promotion record

- **Origin:** [forward document](builder-accessible-layer.md). (An interim synthesis
  note was folded into this document and removed; it remains in git history.)
- **On completion:** archive this design document, promote the durable rules in §9 to
  ADRs, and update the forward document (per the promotion loop in
  [`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md)).
