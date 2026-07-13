from __future__ import annotations

from dataclasses import dataclass

from .model import CanonicalDecision, Proposal
from .security import Identity, Role, require_role
from .store import CanonicalStore


class ValidationError(ValueError):
    pass


@dataclass
class CommitAuthority:
    store: CanonicalStore
    identity: Identity

    def commit(self, proposal: Proposal) -> CanonicalDecision:
        require_role(self.identity, Role.COMMIT)
        if not proposal.decision_id.strip():
            raise ValidationError("decision_id is required")
        if not proposal.evidence_fresh:
            raise ValidationError("stale evidence cannot authorize commitment")
        if proposal.requested_enabled and not proposal.approved:
            raise ValidationError("enablement requires approval")

        decision = CanonicalDecision(
            decision_id=proposal.decision_id,
            requested_enabled=proposal.requested_enabled,
            approved=proposal.approved,
            evidence_fresh=proposal.evidence_fresh,
            version=proposal.expected_version + 1,
        )
        self.store.write_canonical(decision, identity=self.identity)
        return decision
