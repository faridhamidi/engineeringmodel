"""Application service: decides, then crosses one named external-effect seam."""

from __future__ import annotations

from dataclasses import dataclass

from .decisions import Decision, decide_enablement
from .integrations import ExternalEffectPort


@dataclass
class EnablementService:
    effect_port: ExternalEffectPort

    def run(self, *, requested: bool, evidence_fresh: bool, operation_id: str) -> Decision:
        decision = decide_enablement(requested=requested, evidence_fresh=evidence_fresh)
        if decision.should_apply:
            self.effect_port.apply(enabled=True, operation_id=operation_id)
        return decision
