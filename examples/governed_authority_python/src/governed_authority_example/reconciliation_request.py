from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .model import EffectiveDecision
from .reconciler import Reconciler
from .security import Identity, Role, require_role


class ReconciliationRequestPort(Protocol):
    def request_reconciliation(
        self,
        decision_id: str,
        *,
        caller: Identity,
    ) -> EffectiveDecision: ...


@dataclass
class ReconciliationGateway:
    """Authenticated request boundary in front of the privileged reconciler."""

    _reconciler: Reconciler

    def request_reconciliation(
        self,
        decision_id: str,
        *,
        caller: Identity,
    ) -> EffectiveDecision:
        require_role(caller, Role.RECOVERY)
        return self._reconciler.reconcile(decision_id)
