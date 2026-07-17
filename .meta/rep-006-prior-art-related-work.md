<!--
Type: Related-work / prior-art note
Status: living — external studies that bear on the falsification program
Origin: web review 2026-07-17; companion to rep-005-falsification-program-narrative.md
Last updated: 2026-07-17
-->

# Prior Art & Related Work — has anyone tested agent steering like this?

Short answer: **the question is being actively studied in 2026, and the results converge with
ours** — steering changes an agent's *process* (more testing/exploration/thinking) but not its
*outcomes*; any lift comes from *structure*, not content. What appears uncommon is our specific
*format*: a practitioner shipping a steering seed **plus a reusable, contamination-controlled
falsification harness** in the same repo, for others to run themselves.

## The two closest studies

### 1. "Scaffold, Not Vocabulary?" — arXiv 2606.06454 (our near-twin)

A pre-registered, controlled study of a **Popperian falsificationist coding skill** — a `SKILL.md`
that switches an agent from verification ("does this look right?") to falsification ("what severe
test would break this?"), with invariants like *oracle independence (never self-grade with the same
model)*, *abstain as a first-class outcome*, and *"corroborated ≠ verified/proven."* This is a
formalized version of our seed's philosophy, and it is tested on **the same model we use (Claude
Sonnet 4.6).**

- **Method:** pre-registered; execution oracle (HumanEval+ unit tests), **no LLM-judge** for the
  correctness call; a two-tier design (frontier + weak model); three controls — a **length-matched
  placebo**, a **labels-only scaffold** (section headers kept, procedure stripped), plus a
  **vocabulary-halo sentinel** and a self-judge audit.
- **Findings:**
  - Sonnet 4.6 (N=163): all conditions ~95% and **do not separate** (V 95.1, F 95.7, L 95.7,
    P 96.9) — a *ceiling-limited non-detection*. (Same saturation wall we hit.)
  - Qwen2.5-Coder-0.5B (headroom): structured arms +≈22 pts, but the **full skill content shows no
    separable benefit over labels-only** (F@8 = L@8 = 56.7%); length-matched placebo trails by a
    non-significant 2.4 pts. The **self-judge doesn't beat random** (position bias).
  - Verdict: the gain is **scaffold *structure*, not the falsification *vocabulary/content*.** A
    calibrated negative result.
- **Notes the same confound we design around:** *"vanilla in an agentic CLI can be silently
  contaminated by operator scaffolds."*
- Skill + protocol released: `github.com/PhiniteLab/popperian-coding-skill`.

### 2. "Are Repository-Level Context Files Helpful for Coding Agents?" (Evaluating AGENTS.md) — arXiv 2602.11988 (ETH Zurich)

Built **AGENTbench** — 138 tasks from 12 *niche* repos with developer-written context files
(deliberately less contaminated than SWE-bench), plus SWE-bench Lite; graded by withheld unit tests.
Four agents (Claude Code/Sonnet-4.5, Codex/GPT-5.2, GPT-5.1-mini, Qwen).

- **Findings:** LLM-generated context files **reduce** success (≈−3%) and add **20%+ cost**;
  developer-written ones help marginally (≈+4%). Both cause **more testing, exploration, and
  reasoning tokens**; instructions *are* followed (so it is not an instruction-following failure) —
  the extra requirements simply *make tasks harder*.
- **Nuance:** when all *other* documentation is removed, LLM context files help (+2.7%) — i.e. they
  are largely *redundant documentation* for well-documented/popular repos. Python's heavy training
  presence may also nullify the effect (a contamination angle).
- This is essentially our Round-3 result ("process up, outcome flat") at n=138.

### Tooling analogues (frameworks, not shipped-with-a-repo)
- **Scylla** (arXiv 2602.08765) — ablation tiers T0–T6 for coding agents.
- **Arbiter** (arXiv 2603.08993) — treats system prompts as testable software; detects interference.
- **ABTest** (arXiv 2604.03362) — turns failure reports into repo-grounded behavioral tests.
- **Cross-module prompt interference / "compositional behavioral leakage"** (arXiv 2606.26356).

## How our findings relate

- **Convergence (validation):** two independent 2026 studies — one on our exact model with our exact
  skill-concept — reach our conclusion: reliable **process** change, no **outcome** lift, gains are
  **structure not content**, and frontier models **saturate**.
- **Where we remain distinctive/stronger:** both lean on public or semi-public benchmarks
  (SWE-bench Lite is contaminated; AGENTbench is real GitHub PRs). Our fully **bespoke, novel,
  uncontaminated** tasks + **independent author** + **physical workspace isolation** are more
  contamination-proof; we target the seed's **home turf** (data-integrity / recovery), which
  HumanEval+/SWE-bench do not probe; and we ship a **reusable falsification harness** for others.

## Controls to borrow (concrete upgrades to our A/B)

1. **Labels-only control (highest value).** We currently test *seed vs nothing*, so we cannot tell a
   real effect from "any structured scaffold helps." Add a third arm: the seed's headers/section
   structure with the procedure stripped. `Δcontent = seed − labels-only` isolates whether the
   seed's *substance* matters beyond its *structure*.
2. **Length-matched placebo.** Generic best-practice text of equal length. Rules out "the seed just
   adds tokens → more thinking/exploration" — the mechanism both papers pin the process change on.
3. **Weak-model screening tier.** Our saturation / low task-yield problem is exactly what killed
   their frontier tier; their answer (Qwen ~0.5B, local, near-free) is far cheaper than manufacturing
   bespoke hard tasks for Sonnet. Screen candidate effects on a weak model with headroom first.
4. **(Optional) vocabulary-halo sentinel** — only relevant if/when an LLM-judge is used; detects a
   judge rewarding the seed's jargon. We currently avoid LLM-judging, so this is a guard for later.

## Interpretation for our program

Finding no *outcome* lift is now the **expected** result, not a surprising one — it is where the
frontier of evidence sits. The sharpest remaining question our home-turf A/B can answer is the one
these papers frame best: **structure vs content.** Adding the labels-only + placebo arms turns our
"seed vs bare" test into a "seed-content vs seed-structure vs length vs bare" test — the design that
would let us state, on firmer ground than either paper (uncontaminated, home-turf), whether our
seed's *content* does anything its *structure* doesn't.
