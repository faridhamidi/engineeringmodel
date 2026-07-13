from __future__ import annotations

from dataclasses import dataclass, field

from .security import Identity, Role, require_role


@dataclass
class ManagedResource:
    states: dict[str, bool] = field(default_factory=dict)
    mutation_count: int = 0

    def mutate_managed_resource(
        self,
        decision_id: str,
        *,
        enabled: bool,
        identity: Identity,
    ) -> None:
        require_role(identity, Role.RECONCILER)
        if self.states.get(decision_id) == enabled:
            return
        self.states[decision_id] = enabled
        self.mutation_count += 1
