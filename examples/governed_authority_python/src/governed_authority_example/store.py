from __future__ import annotations

from dataclasses import dataclass, field

from .model import CanonicalDecision
from .security import Identity, Role, require_role


class ConcurrencyError(RuntimeError):
    pass


@dataclass
class CanonicalStore:
    records: dict[str, CanonicalDecision] = field(default_factory=dict)

    def write_canonical(self, decision: CanonicalDecision, *, identity: Identity) -> None:
        require_role(identity, Role.COMMIT)
        current = self.records.get(decision.decision_id)
        current_version = 0 if current is None else current.version
        if decision.version != current_version + 1:
            raise ConcurrencyError("canonical version is stale or non-sequential")
        self.records[decision.decision_id] = decision

    def get(self, decision_id: str) -> CanonicalDecision:
        return self.records[decision_id]
