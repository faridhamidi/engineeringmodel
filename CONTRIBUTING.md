# Contributing

This repository preserves engineering reasoning rather than advertising tools, architecture labels, or the author.

## Choose the layer first

A contribution belongs in **Core Hygiene** when it:

- applies to many non-trivial codebases;
- can begin with low implementation cost;
- prevents a concrete design, testing, or diagnostic failure;
- has an observable or executable conformance condition;
- remains useful without governance, approval, or shared-resource mutation.

A contribution belongs in **Governed Automation** only when it addresses consequential external effects, durable authority, material blast radius, evidence-sensitive action, or recovery bypass risk.

Do not place a specialized authority mechanism in the core layer merely because it improved one complex system.

## Canonical concept ownership

A concept is explained fully in one place and referenced elsewhere.

- `governed-automation/MODELS.md` owns model definitions, triggers, mechanisms, invariants, costs, security implications, and skip conditions.
- `DECISION_TREE.md` may ask trigger questions and link to models, but should not restate full mechanisms.
- `VOCABULARY.md` may define a term in one or two sentences and link to its model.
- `PRINCIPLES.md` contains cross-cutting positions, not a second model catalog.
- `AUTOMATED_AUTHORITY.md` owns composition of the seven powers, not duplicate per-model guidance.

## Required model structure

A new or revised model should state:

- trigger condition;
- definition and problem;
- mechanism;
- invariant;
- adoption cost;
- security implications;
- evidence;
- skip or rejection condition;
- what was deliberately not built.

## Executable witnesses

An executable witness demonstrates a narrow property without becoming a product template.

It should:

- use no credentials, network calls, or organization-specific data;
- depend only on standard tooling where practical;
- state the exact claims it demonstrates;
- include a known-bad or bypass case that the test rejects;
- run in repository CI;
- remain small enough to read in one sitting;
- avoid implying that its language, framework, or directory structure is mandatory.

Do not label a witness `deployed` or `operationally used`. It is evidence that a constraint is executable, not that it has an operating history.

## Conformance harness contributions

A repository conformance harness is an optional Core Hygiene escalation. Product-specific rule sets remain in product repositories; this repository accepts generalized lessons and sanitized executable witnesses.

A new or changed harness rule should include:

- a canonical rationale reference;
- a stable namespaced rule identifier in `<layer>.<domain>.<number>` form;
- lifecycle and enforcement mode;
- an exact known-violation set when ratcheted;
- exact public owner principals;
- CODEOWNERS correspondence;
- an approval-policy reference;
- a deterministic checker adapter;
- one positive conformance test;
- one minimal falsifier;
- generic fixture coverage when harness mechanics change;
- CI execution;
- an evidence boundary;
- adoption cost and a skip condition;
- historical lineage when retired or superseded.

Choose an existing rule domain when it fits. Do not create a domain for one implementation detail, renumber rules, or recycle retired identifiers. Fixture rules use `FIXTURE.*` and remain outside the live manifest.

Naming conventions, directory placement, and agent instructions are not executable evidence by themselves. Do not weaken a rule, checker, and falsifier together merely to restore a passing build; state which architectural decision changed.

## Conformance-rule approval

Adding, activating, weakening, expanding, narrowing, ratcheting, retiring, or superseding a rule requires review through the repository's protected change process by the declared owners.

This includes changes to:

- lifecycle or enforcement mode;
- known-violation sets;
- scope, checker kind, severity, or checker configuration;
- owners or approval references;
- positive tests or falsifiers;
- historical lineage;
- CODEOWNERS coverage;
- the workflow that executes the harness.

The manifest validates ownership declarations and approval-policy references. The executable witness does not prove that the hosting platform requires code-owner review, enables branch protection, or prevents administrative bypass. Record that hosting-platform evidence separately before claiming enforced review.

Historical rule identifiers are immutable and never reused. Retired and superseded records remain visible with equivalent fidelity across manifest versions. Any deliberate weakening of that retention requires a separate architecture decision whose explicit subject is lineage reduction.

## Commit messages

Use Conventional Commits:

```text
<type>(<optional-scope>): <description>
```

Supported types:

```text
feat
fix
docs
test
refactor
ci
chore
```

Recommended scopes include `core`, `harness`, `conformance`, `governed-automation`, `examples`, `case-studies`, and `ci`.

Examples:

```text
feat(harness): namespace conformance rule identifiers
docs(core): define rule identifier format
test(conformance): add namespace validation cases
fix(harness): reject fixture identifiers in the live manifest
ci(witnesses): run conformance audit
```

Commit messages describe the semantic change, not the editing activity. Avoid messages such as `update files`, `make changes`, `fix stuff`, or `address feedback`.

This repository documents the convention but does not enforce commit-message linting. Add enforcement only when release, changelog, or versioning automation materially depends on commit classification.

## Evidence tags

Use these tags explicitly in case studies and material conclusions:

- **implemented** — visible in code;
- **tested** — protected by a named executable check;
- **deployed** — running in a real environment;
- **operationally used** — consumed by a real workflow or operator;
- **proposed** — documented direction, not current behavior;
- **inferred** — a conclusion drawn from evidence but not directly measured.

Recommended lesson block:

```markdown
### Lesson

**Evidence:** implemented, tested  
**Scope:** one bounded system  
**Conclusion:** ...
```

Do not let an inference inherit the confidence of the implementation evidence beneath it.

## Case-study rules

A positive case must show why the adoption gate was satisfied.

A negative or non-adoption case must be one of:

- an observed misapplication with evidence of its cost; or
- a clearly labelled counterfactual analysis grounded in a real system.

Never present a constructed counterexample as an operational failure. Do not manufacture examples in untested domains merely to imply portability.

## Writing rules

Use plain technical language. Prefer property statements such as “external effects cross named seams” over architecture-brand requirements.

Avoid:

- revolutionary or next-generation;
- enterprise-grade without defined evidence;
- production-ready without an operating record;
- best practice without context;
- zero-error or zero-downtime as unqualified objectives;
- provider-independent when only one provider is implemented;
- AI-powered when a model is incidental to the value;
- comparisons to large frameworks without stating the exact shared property.

## Confidentiality

Do not include:

- employer or customer names;
- account, tenant, host, or internal system identifiers;
- internal domains, paths, credentials, or network details;
- proprietary source code;
- unapproved adoption metrics;
- incident details that identify affected parties;
- screenshots, logs, prompts, or generated artifacts containing personal or operational metadata;
- private organization handles, internal team names, or unapproved email addresses in ownership configuration.

Sanitize the example while preserving the decision, state model, failure mode, and evidence class. Public source material may still contain details that should not be repeated in a generalized case study.

Before adding a CODEOWNERS principal, confirm that the identity is already public and deliberately approved for association with this repository. Do not introduce employer, customer, private-organization, or internal-team identifiers solely to demonstrate ownership.

## Revision rule

Corrections are more valuable than consistency with an earlier claim. When code or evidence changes, revise the model and retain the boundary. Do not defend wording that the implementation no longer supports.
