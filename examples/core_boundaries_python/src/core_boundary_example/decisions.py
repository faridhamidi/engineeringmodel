"""Pure decision logic: no external client, environment, file, or network access."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    should_apply: bool
    reason: str


def decide_enablement(*, requested: bool, evidence_fresh: bool) -> Decision:
    if not evidence_fresh:
        return Decision(should_apply=False, reason="stale_evidence")
    if not requested:
        return Decision(should_apply=False, reason="not_requested")
    return Decision(should_apply=True, reason="requested_and_fresh")
