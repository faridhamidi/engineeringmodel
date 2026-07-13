from __future__ import annotations

from dataclasses import dataclass

from .model import EffectiveDecision
from .reconciliation_request import ReconciliationRequestPort
from .security import Identity, Role, require_role


@dataclass
class Recovery:
    request_port: ReconciliationRequestPort
    identity: Identity

    def retry_committed(self, decision_id: str) -> EffectiveDecision:
        require_role(self.identity, Role.RECOVERY)
        # Recovery owns only a request capability. It does not receive the
        # reconciler object, its workload identity, or the managed resource.
        return self.request_port.request_reconciliation(
            decision_id,
            caller=self.identity,
        )
