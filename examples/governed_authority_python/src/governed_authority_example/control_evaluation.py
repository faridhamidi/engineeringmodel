from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .protected_actions import (
    Control,
    ProtectedAction,
    UnknownProtectedAction,
    action_spec,
    required_controls,
)
from .security import Role


class HoldReason(str, Enum):
    UNKNOWN_PROTECTED_ACTION = "unknown_protected_action"
    ROLE_MISMATCH = "role_mismatch"
    APPROVAL_REQUIRED = "approval_required"
    STALE_EVIDENCE = "stale_evidence"
    MISSING_CANONICAL_DECISION = "missing_canonical_decision"
    UNAUTHENTICATED_REQUEST = "unauthenticated_request"


HOLD_MESSAGES: dict[HoldReason, str] = {
    HoldReason.UNKNOWN_PROTECTED_ACTION: "The protected action is not declared.",
    HoldReason.ROLE_MISMATCH: "The caller does not hold the required role.",
    HoldReason.APPROVAL_REQUIRED: "Required approval is absent.",
    HoldReason.STALE_EVIDENCE: "Required evidence is stale or unavailable.",
    HoldReason.MISSING_CANONICAL_DECISION: "No canonical decision authorizes execution.",
    HoldReason.UNAUTHENTICATED_REQUEST: "The recovery request is not authenticated.",
}


@dataclass(frozen=True)
class ControlContext:
    caller_role: Role
    approved: bool = False
    evidence_fresh: bool = False
    canonical_decision_present: bool = False
    request_authenticated: bool = False


@dataclass(frozen=True)
class ControlResult:
    allowed: bool
    reason: HoldReason | None

    @property
    def message(self) -> str | None:
        return None if self.reason is None else HOLD_MESSAGES[self.reason]


_CONTROL_ORDER: tuple[tuple[Control, HoldReason], ...] = (
    (Control.ROLE_MATCH, HoldReason.ROLE_MISMATCH),
    (Control.APPROVED, HoldReason.APPROVAL_REQUIRED),
    (Control.FRESH_EVIDENCE, HoldReason.STALE_EVIDENCE),
    (Control.CANONICAL_DECISION, HoldReason.MISSING_CANONICAL_DECISION),
    (Control.AUTHENTICATED_REQUEST, HoldReason.UNAUTHENTICATED_REQUEST),
)


def evaluate_controls(
    action: ProtectedAction | str,
    context: ControlContext,
) -> ControlResult:
    """Evaluate runtime facts after static control selection."""

    try:
        spec = action_spec(action)
        selected = required_controls(action)
    except UnknownProtectedAction:
        return ControlResult(
            allowed=False,
            reason=HoldReason.UNKNOWN_PROTECTED_ACTION,
        )

    passed = {
        Control.ROLE_MATCH: context.caller_role is spec.role,
        Control.APPROVED: context.approved,
        Control.FRESH_EVIDENCE: context.evidence_fresh,
        Control.CANONICAL_DECISION: context.canonical_decision_present,
        Control.AUTHENTICATED_REQUEST: context.request_authenticated,
    }

    for control, reason in _CONTROL_ORDER:
        if control in selected and not passed[control]:
            return ControlResult(allowed=False, reason=reason)

    return ControlResult(allowed=True, reason=None)