from __future__ import annotations

from dataclasses import dataclass

from .model import EffectiveDecision
from .reconciler import Reconciler
from .security import Identity, Role, require_role


@dataclass
class Recovery:
    reconciler: Reconciler
    identity: Identity

    def retry_committed(self, decision_id: str) -> EffectiveDecision:
        require_role(self.identity, Role.RECOVERY)
        # Recovery holds no commit or mutation credential. It requests re-entry
        # through the component that already owns execution authority.
        return self.reconciler.reconcile(decision_id)
