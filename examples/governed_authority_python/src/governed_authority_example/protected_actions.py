from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .security import Role


class ProtectedAction(str, Enum):
    COMMIT_DECISION = "commit_decision"
    APPLY_EFFECT = "apply_effect"
    REQUEST_RECOVERY = "request_recovery"


class Control(str, Enum):
    ROLE_MATCH = "role_match"
    APPROVED = "approved"
    FRESH_EVIDENCE = "fresh_evidence"
    CANONICAL_DECISION = "canonical_decision"
    AUTHENTICATED_REQUEST = "authenticated_request"


@dataclass(frozen=True)
class ActionSpec:
    role: Role
    controls: frozenset[Control]


ACTION_REGISTRY: dict[ProtectedAction, ActionSpec] = {
    ProtectedAction.COMMIT_DECISION: ActionSpec(
        role=Role.COMMIT,
        controls=frozenset(
            {
                Control.ROLE_MATCH,
                Control.APPROVED,
                Control.FRESH_EVIDENCE,
            }
        ),
    ),
    ProtectedAction.APPLY_EFFECT: ActionSpec(
        role=Role.RECONCILER,
        controls=frozenset(
            {
                Control.ROLE_MATCH,
                Control.CANONICAL_DECISION,
            }
        ),
    ),
    ProtectedAction.REQUEST_RECOVERY: ActionSpec(
        role=Role.RECOVERY,
        controls=frozenset(
            {
                Control.ROLE_MATCH,
                Control.AUTHENTICATED_REQUEST,
                Control.CANONICAL_DECISION,
            }
        ),
    ),
}


class UnknownProtectedAction(KeyError):
    pass


def action_spec(action: ProtectedAction | str) -> ActionSpec:
    try:
        normalized = action if isinstance(action, ProtectedAction) else ProtectedAction(action)
    except ValueError as exc:
        raise UnknownProtectedAction(str(action)) from exc

    try:
        return ACTION_REGISTRY[normalized]
    except KeyError as exc:
        raise UnknownProtectedAction(normalized.value) from exc


def required_controls(action: ProtectedAction | str) -> frozenset[Control]:
    """Select controls from declared action semantics only."""

    return action_spec(action).controls