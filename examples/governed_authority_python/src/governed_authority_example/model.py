from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Proposal:
    decision_id: str
    requested_enabled: bool
    approved: bool
    evidence_fresh: bool
    expected_version: int = 0


@dataclass(frozen=True)
class CanonicalDecision:
    decision_id: str
    requested_enabled: bool
    approved: bool
    evidence_fresh: bool
    version: int


@dataclass(frozen=True)
class EffectiveDecision:
    enabled: bool
    reason: str
