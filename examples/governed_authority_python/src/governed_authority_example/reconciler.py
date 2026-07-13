from __future__ import annotations

from dataclasses import dataclass

from .external import ManagedResource
from .model import EffectiveDecision
from .policy import derive_effective
from .security import Identity, Role, require_role
from .store import CanonicalStore


@dataclass
class Reconciler:
    store: CanonicalStore
    resource: ManagedResource
    identity: Identity

    def reconcile(self, decision_id: str) -> EffectiveDecision:
        require_role(self.identity, Role.RECONCILER)
        canonical = self.store.get(decision_id)
        effective = derive_effective(canonical)
        self.resource.mutate_managed_resource(
            decision_id,
            enabled=effective.enabled,
            identity=self.identity,
        )
        return effective
