# Claude Instructions

<!-- engineering-model-steering:start -->
## Revertible Envelope

Classify each intended action before performing it:

- If it is local and reversible in one step, continue autonomously.
- For every non-trivial implementation, load the installed `engineering-model` skill
  before editing and use only the depth the work earns. If the skill is unavailable,
  install the packaged skill before continuing.
- If it touches shared ground, is hard to undo, or is uncertain, fail closed and load
  the installed `engineering-model` skill for the depth the decision earns.
- Protect changed load-bearing behavior with the lightest test that would fail on a
  realistic defect. Add diagnostic context at external, asynchronous, or persistence
  seams only when failure would otherwise be silent; never silently discard or corrupt
  data. Run the tests and checks you cite.
- Keep agent-authored work recoverable. At coherent, verified task boundaries, commit
  only task-owned changes with a focused message. Never commit secrets, generated junk,
  unrelated changes, or pre-existing user work. If the task cannot be isolated safely,
  leave the work uncommitted and report why.
- Before relying on git as recovery, verify that the project can create a checkpoint.
  If it cannot, keep the changes local and report the missing recovery mechanism.
- Before any external-substrate effect, stop and obtain explicit human approval for the
  exact target, consequence, and action. Do not treat approval for one effect as
  approval for a broader effect.
- Git can undo authoring; it cannot undo an external effect.
<!-- engineering-model-steering:end -->

Read [AGENTS.md](AGENTS.md) for the repository's contributor map, canonical reading
order, required checks, and change discipline.
