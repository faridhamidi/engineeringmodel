"""Pure policy derivation: canonical input to classified effective state."""

from __future__ import annotations

from .model import CanonicalDecision, EffectiveDecision


def derive_effective(decision: CanonicalDecision) -> EffectiveDecision:
    if not decision.evidence_fresh:
        return EffectiveDecision(enabled=False, reason="stale_evidence")
    if not decision.approved:
        return EffectiveDecision(enabled=False, reason="not_approved")
    if not decision.requested_enabled:
        return EffectiveDecision(enabled=False, reason="not_requested")
    return EffectiveDecision(enabled=True, reason="approved_requested_and_fresh")
