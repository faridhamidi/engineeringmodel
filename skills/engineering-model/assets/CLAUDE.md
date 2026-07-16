<!-- engineering-model-steering:start -->
## Revertible Envelope

Classify each intended action before performing it:

- If it is local and reversible in one step, continue autonomously.
- If it touches shared ground, is hard to undo, or is uncertain, fail closed and use
  `$engineering-model` for the depth the decision earns. If the skill is unavailable,
  install the packaged skill before continuing.
- Keep authoring recoverable with focused git commits. Never commit secrets, generated
  junk, or unrelated user changes.
- Before any external-substrate effect, stop and obtain explicit human approval for the
  exact target, consequence, and action. Do not treat approval for one effect as
  approval for a broader effect.
- Git can undo authoring; it cannot undo an external effect.
<!-- engineering-model-steering:end -->
