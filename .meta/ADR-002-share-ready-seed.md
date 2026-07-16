<!--
Type: Architecture decision record
Status: proposed (implemented locally; awaiting maintainer ratification)
Origin: share-readiness review following ADR-001-builder-accessible-layer.md
Owner: repository maintainer (assign on adoption)
Last verified against: local seed generator implementation dated 2026-07-16
Supersedes / superseded by: extends ADR-001-builder-accessible-layer.md
-->

# ADR-002: Publish A Generated Project Seed

## Decision

Keep this repository as the canonical engineering-model source and generate a separate,
minimal project seed from it.

- The source repository owns steering, skill content, templates, generation logic, and
  verification.
- A future `engineeringmodel-seed` repository is a generated projection and must not be
  edited as an independent source of truth.
- The generated project contains root `AGENTS.md` and `CLAUDE.md`, exact project-local
  skill copies in `.agents/skills/engineering-model/` and
  `.claude/skills/engineering-model/`, a provenance manifest, and minimal project
  placeholders.
- Source-only methodology, examples, meta records, contributor instructions, and CI do
  not enter the generated project.
- Shared steering names the installed skill without runtime command syntax. Native
  invocation remains `$engineering-model` in Codex and `/engineering-model` in Claude.
- Publication is a distinct external effect. Generation remains local; publishing to a
  remote template requires an explicit target, visibility decision, credentials, and
  reviewed action.

## Rationale

Using the canonical repository as a project shell makes agents read contributor maps,
methodology inventories, and witness commands that do not belong to the product. A
generated seed gives users a small interface while preserving locality: canonical
changes and verification remain in one source repository.

Both runtimes require native discovery paths. Duplicating the skill in generated output
is acceptable because the generator, hashes, and parity witnesses own that duplication;
maintainers never edit either projection directly.

## Consequences

- A new project can start with steering and the skill already discoverable; no first-use
  installation is required.
- Generated projects carry two hidden skill copies when both runtimes are supported.
- A distributed seed can verify internal file integrity against its embedded manifest
  without access to this repository. Because that manifest is unsigned, this is not an
  authenticity claim.
- Canonical parity includes source revision and state, so a seed generated from an older
  commit is intentionally stale even when its own manifest remains internally coherent.
- Template users receive a point-in-time version. Updating an existing project requires
  a later managed update interface; GitHub template creation alone does not propagate
  updates.
- The remote template repository, publication credentials, branch protection, and
  operational use are not established by the local generator.

## Evidence

**Implemented, tested locally:** deterministic generation, exact dual-runtime skill
projection, native steering parity, managed-file hashes, minimal top-level output,
non-empty destination refusal, projection-junk rejection, source-independent manifest
verification, git identity adaptation, and canonical drift detection.

**Proposed / not demonstrated:** maintainer ratification, remote template creation,
reviewed publication automation, installation from the template, update behavior in a
real product repository, and runtime adherence.
