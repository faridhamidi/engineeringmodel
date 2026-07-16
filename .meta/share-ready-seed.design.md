<!--
Type: Design document
Status: completed (historical; publication remains a separate approved action)
Origin: ADR-002-share-ready-seed.md
Owner: repository maintainer (assign on adoption)
Last verified against: local seed generator implementation dated 2026-07-16
Supersedes / superseded by: durable direction accepted in ADR-002-share-ready-seed.md
-->

# Design Document: Share-Ready Project Seed

**Historical worked plan** (per [`core/DOCUMENTATION.md`](../core/DOCUMENTATION.md)).
The local generator and verification surface are complete. Remote publication remains
a separate external effect governed by the accepted ADR and this document's publication
boundary.

## 1. Scope

Generate a minimal project tree from this canonical repository so a user can begin a
new project with native steering and the `engineering-model` skill already available to
Codex and Claude.

Remote repository creation, credentials, branch protection, publishing, and managed
updates to existing product repositories remain outside this local implementation.

## 2. Output Interface

```text
AGENTS.md
CLAUDE.md
.agents/skills/engineering-model/
.claude/skills/engineering-model/
.engineering-model/manifest.json
.gitignore
README.md
```

Root instruction files come from the packaged templates. Both skill directories are
exact copies of the canonical package. The generated README contains no methodology
orientation, and no source-only top-level directory is admitted.

## 3. Generator Interface

```bash
python seed/generate.py --output dist/engineeringmodel-seed
python seed/generate.py --verify dist/engineeringmodel-seed
python seed/generate.py --check dist/engineeringmodel-seed
```

Generation requires a new or empty destination and never initializes git or contacts a
remote system. Verify mode checks managed-file hashes and the top-level surface implied
by the output's embedded manifest without consulting the canonical checkout. Check mode
regenerates expected output from the current canonical checkout in a temporary directory
and reports missing, changed, or unexpected files without modifying the target. Because
source revision and state are part of that projection, a new source commit intentionally
makes an older seed stale in check mode.

[`seed/manifest.json`](../seed/manifest.json) is the structured projection spec. It
declares source-to-target mappings, runtime destinations, format version, source
repository, and the exact top-level output set.

## 4. Provenance And Ownership

The output manifest records:

- source repository, revision, and clean or modified state;
- native instruction and skill location for each runtime;
- a SHA-256 digest for every managed file except the manifest itself.

The manifest creates an ownership envelope for future update and removal operations. It
does not claim that a dirty source tree equals its recorded commit; the explicit source
state preserves that distinction. Manifest verification proves internal consistency,
not provenance authenticity: the local manifest is intentionally unsigned and could be
changed together with its files. Canonical check mode provides the stronger comparison
when the source repository is available.

## 5. Runtime Adapters

[Codex](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills) discovers the
project skill below `.agents/skills/`; [Claude](https://code.claude.com/docs/en/skills#where-skills-live)
discovers it below `.claude/skills/`. Both receive the same open Agent Skills package.
Each runtime reads its own native steering file and skill location, so generated
duplication does not duplicate always-on context.

The canonical steering block uses the runtime-neutral phrase "installed
`engineering-model` skill." Runtime-native command syntax remains in the skill's
installation guidance and UI metadata, not in the shared block.

## 6. Verification

Direct witnesses prove:

1. only the declared top-level paths are generated;
2. source-only directories do not leak into the project;
3. both runtime skill trees equal the canonical package byte for byte;
4. root steering equals the packaged native templates;
5. every managed file has the expected digest;
6. repeated generation with the same source identity is deterministic;
7. missing, changed, and unexpected output is detected;
8. a non-empty destination is rejected without changing user work;
9. the project README does not become methodology documentation;
10. VCS, OS, and cache artifacts below projected source trees are rejected;
11. source identity reports clean and modified worktrees and wraps git failures;
12. manifest verification does not inspect the source checkout;
13. canonical check mode treats a different source revision as stale.

CI generates, verifies, and checks a fresh seed in runner-local temporary storage. These
witnesses do not prove manifest authenticity, remote publication, client behavior,
agent adherence, or safe updates to an already-diverged product repository.

## 7. Publication Boundary

After maintainer ratification, create a separate `engineeringmodel-seed` repository and
mark it as a template. Publication should generate from a clean accepted source commit,
open a reviewable update in the template repository, and avoid direct unreviewed writes
to its default branch.

Creating that repository or publishing generated content is an external-substrate
effect and requires explicit approval for the owner, repository name, visibility, and
action.
