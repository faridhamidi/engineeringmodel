<!--
Type: Design document
Status: completed (historical; archived in place to preserve stable links)
Origin: promoted from .meta/builder-accessible-layer.md (forward document)
Owner: repository maintainer (assign on adoption)
Last verified against: builder-layer implementation dated 2026-07-16
Supersedes / superseded by: durable rules promoted to ADR-001-builder-accessible-layer.md
-->

# Design Document — Builder-Accessible Layer

**Historical worked plan** (per [`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md)).
This records how the builder-accessible layer was built and verified. Durable rules now
live in [ADR-001](ADR-001-builder-accessible-layer.md). Direction lives in the
[forward document](builder-accessible-layer.md). This document remains at its stable
path because the implemented package and earlier records link to its skill outline.

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
- Every autonomous authoring change stays revertible; external-substrate effects
  require explicit human approval.
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
  │   - commits coherent, verified, task-owned increments       │
  │   - ALWAYS asks approval before external-substrate effects  │
  │   - calls the engine skill when depth/judgment is needed    │
  ├───────────────────────────────────────────────────────────┤
  │ ENGINE (skill, on-demand)   generated engine projection      │  the depth
  │   - loaded when the steering calls for it                   │
  │   - carries parity-checked copies for standalone install    │
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
  c. **Checkpoint discipline:** at coherent, verified task boundaries, commit only
     task-owned changes (undo stack + audit trail + provenance in one). Never commit
     secrets, junk, unrelated changes, or pre-existing user work. When ownership cannot
     be isolated safely, leave the work uncommitted and report why.
  d. **External-substrate rule:** always ask for explicit human approval before any
     external-substrate involvement; do not proceed without it.
  e. Call the engine skill when depth or judgment is required.
- Must reference the engine skill and the [human front door](../builders/START_HERE.md);
  must **not** restate engine rationale (canonical concept ownership).
- The canonical block is
  [`skills/engineering-model/assets/steering.md`](../skills/engineering-model/assets/steering.md).
  Installation places the exact marked block in the runtime's native always-on surface.
  This repository exercises both [`AGENTS.md`](../AGENTS.md) and
  [`CLAUDE.md`](../CLAUDE.md); packaged templates keep both forms installable.

### 3.2 Engine as a skill — on-demand depth

The reusable [`engineering-model` skill](../skills/engineering-model/SKILL.md) follows
the open [Agent Skills specification](https://agentskills.io/specification). The
package applies a predictability-first skill structure: one model-invoked entry point,
checkable completion criteria, progressive disclosure, one-level context pointers, and
no auxiliary skill README or duplicated rationale.

**Invocation.** The skill is model-invoked because the always-on steering must reach it
without relying on the human to remember a command. Its description carries one trigger
per branch: non-trivial system change, shared or external state, and authority/evidence/
recovery risk. **Revertible envelope** is the leading phrase shared by steering and
execution.

**Information hierarchy.** `SKILL.md` contains only the ordered process and routing
conditions. Each of its five steps ends in a checkable completion criterion:

1. classify every intended action;
2. record Core-only, selected-model, or complete-layer adoption;
3. protect every load-bearing seam with paired positive and known-bad evidence;
4. keep local authoring recoverable and gate each exact external effect;
5. report semantic, enforcement, authority, external-effect, and residual-risk impact.

Canonical methodology is disclosed only when its branch fires. The package layout is:

```text
skills/engineering-model/
  SKILL.md                       model-invoked process and context pointers
  agents/openai.yaml             optional Codex UI metadata
  assets/steering.md             canonical always-on steering block
  assets/AGENTS.md               Codex-compatible placement template
  assets/CLAUDE.md               Claude placement template
  references/core-*.md           generated Core engine projection
  references/governed-*.md       generated Governed Automation projection
```

**Standalone installation and canonicality.** An installed package cannot depend on
paths in its source repository, so it carries generated copies of the engine. The
source of truth remains `core/` and `governed-automation/`.
[`sync_skill_references.py`](../builders/_witness/sync_skill_references.py) owns the
source-to-package mapping; CI rejects missing, extra, or byte-different projections.
This is generated delivery, not a second methodology.

**Installation.** Consuming agents place the skill in their platform-specific skill
location and merge the appropriate packaged steering template into every native
always-on instruction file they use. For the reference runtimes, that includes
`AGENTS.md` for Codex-compatible agents and `CLAUDE.md` for Claude. Another runtime
requires its own placement template and parity evidence before this repository claims
support. A runtime without always-on instructions may use the skill on demand, but must
disclose that the external-effect pause is not continuously steered.

### 3.3 Git — the required revertibility substrate

- **Git is a hard prerequisite.** Git must be installed **and** the project must be a
  git repository (`git init`). Without a repo, the revertible envelope does not exist.
- The project README links to [`builders/GIT_SETUP.md`](../builders/GIT_SETUP.md), which
  documents install + verify across operating systems:
  - macOS (`xcode-select --install` or Homebrew `brew install git`);
  - Windows (winget `winget install --id Git.Git -e`, or the Git for Windows installer);
  - Linux — Ubuntu/Debian (`sudo apt install git`) and Fedora (`sudo dnf install git`);
  - verify with `git --version`.
- The agent **operates git for the user** (hidden from the non-technical persona):
  inspect the existing worktree, then commit autonomously at coherent, verified task
  boundaries using only task-owned changes. It does not rewrite existing history
  automatically.
- **Honest limit:** git reverts *authoring*, not *acting* — a commit undoes the code
  that caused an external effect, not the effect. External effects therefore still go
  through §3.1(d).

### 3.4 Human-facing surface

- [`builders/START_HERE.md`](../builders/START_HERE.md): the blast-radius line as one
  plain-language question. *Implemented, tested.*
- [`builders/SAFE_OPERATION.md`](../builders/SAFE_OPERATION.md): the plain-language
  safe-operation floor. *Implemented, structurally tested.*
- [`builders/GIT_SETUP.md`](../builders/GIT_SETUP.md): the cross-platform revertibility
  prerequisite. *Implemented; platform installation is not demonstrated.*

## 4. Workflow discipline (behavior)

The whole-sequence rule: **keep everything inside the revertible envelope; hard-stop
only at the edge.**

```text
1. Ensure the project is a git repository and inspect its existing worktree.
2. Make one coherent change without absorbing pre-existing user work.
3. Run the checks that define completion for that increment.
4. Stage only task-owned changes with explicit paths or selective hunks, then commit
   with a clear message. If ownership cannot be isolated, leave the work uncommitted
   and report why. Never rewrite existing history automatically.
5. Is the next action an external-substrate effect (push, open a pull request, deploy,
   delete shared data,
   grant access, send to others, mutate a live service)?
     - Yes -> STOP. Ask the human for explicit approval. Do not proceed without it.
     - No  -> continue autonomously; the user can revert any result they dislike.
6. Repeat.
```

Below the line, autonomy is the default and asking is the exception. The
non-negotiable pause is an external-substrate effect.

## 5. Decisions (resolved open questions)

| # | Decision | Residual / trade-off |
|---|---|---|
| 1 | Triggering lives in always-on steering across the whole workflow; **no keyword set**. Conditions are semantic and model-evaluated. | Relies on model judgment; mitigated by the **fail-closed** default. |
| 2 | The engine is packaged as the model-invoked, Agent Skills-compatible `engineering-model` skill. It carries parity-checked engine projections and steering templates for `AGENTS.md` and `CLAUDE.md`; consumers place both the skill and the native steering surface. | Coupling is to an open standard, while always-on placement remains runtime-specific. Generated copies add maintenance cost controlled by parity checks. |
| 3 | External-substrate effects stay under **explicit human approval**, steered as a standing norm; no wall is built here. | **Procedural** safety, not a hard wall. The seed *recommends* a substrate control for hard guarantees. |
| 4 | **Git is required** and the repo must be initialized; README documents install across OSes. | Adds a prerequisite; justified because it is the revertibility substrate. |

## 6. Verification plan (walk the talk)

**Implemented and in CI** (`.github/workflows/executable-witnesses.yml`):

- decision-oracle witness — both signals load-bearing, uncertainty fails closed;
- reference-integrity ratchet across every builder and skill surface, with a missing
  reference as the known-bad case;
- structural presence checks for fail-closed classification, skill invocation, git
  checkpoints, exact external-effect approval, and git's limit, with each removed norm
  acting as a minimal falsifier;
- parity checks proving the canonical block is present in `AGENTS.md`, `CLAUDE.md`, and
  both packaged templates, with a changed block as the known-bad case;
- the action oracle: below-line work continues, above-line local work pauses for review,
  an external effect requires approval, and uncertainty fails closed;
- Agent Skills frontmatter, one-level reference, and canonical engine-projection checks,
  with missing, stale, and extra references as known-bad cases.

A change that weakens a norm, its checker, and its falsifier together to make CI pass
is not evidence of safety; it must state which protected property changed.

These checks are structural and oracle-level, not behavioral: a green result shows the
surface is well-formed and the norms are present, not that the agent will always obey
them at runtime. Runtime adherence rests on the steering and the human-approval pause,
not on these witnesses.

## 7. Accepted trade-offs and residual risks

- **Procedural, not enforced, safety for external effects.** Rests on the steering
  norm holding. Recommend a real substrate control for anyone needing hard guarantees.
- **Skill coupling → open standard.** The skill targets the open Agent Skills spec.
  Native always-on surfaces still vary, so `AGENTS.md` and `CLAUDE.md` are explicit
  templates and other runtimes require their own placement. The spec is young and
  client support varies.
- **Generated engine projection.** Standalone installation requires carried reference
  files. Byte-parity checks prevent repository drift, but a separately installed copy
  remains a point-in-time package until upgraded.
- **Steering is non-deterministic.** The fail-closed default, the human-approval pause,
  and the git envelope are mitigations — none is a guarantee. The layer is honest that
  it *helps decide*; it is not the wall.

## 8. Evidence boundary and status

- **Implemented / tested:** the human front door, safe-operation and git surfaces,
  native `AGENTS.md` and `CLAUDE.md` steering, the reusable skill package, generated
  engine projection, and the structural/oracle verification described in section 6.
- **Not demonstrated:** behavior across every agent runtime, automatic installation or
  upgrade in Codex or Claude, other native instruction formats, substrate-side
  enforcement, and operational risk reduction.

## 9. Promoted Decisions

The durable rules were promoted to
[ADR-001](ADR-001-builder-accessible-layer.md) after implementation, verification, and
maintainer approval.

## 10. Promotion record

- **Origin:** [forward document](builder-accessible-layer.md). (An interim synthesis
  note was folded into this document and removed; it remains in git history.)
- **Completion:** implementation, verification, and maintainer approval completed on
  2026-07-16. The forward document was reconciled, this design was archived in place,
  and durable rules were promoted to
  [ADR-001](ADR-001-builder-accessible-layer.md) using the promotion loop in
  [`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md).
