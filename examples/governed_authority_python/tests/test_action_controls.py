from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from governed_authority_example.control_evaluation import (
    HOLD_MESSAGES,
    ControlContext,
    HoldReason,
    evaluate_controls,
)
from governed_authority_example.protected_actions import (
    ACTION_REGISTRY,
    Control,
    ProtectedAction,
    required_controls,
)
from governed_authority_example.security import Role


class ProtectedActionControlTests(unittest.TestCase):
    def test_registry_is_complete_for_declared_actions(self) -> None:
        self.assertEqual(set(ACTION_REGISTRY), set(ProtectedAction))

    def test_control_selector_has_no_runtime_context_parameter(self) -> None:
        self.assertEqual(list(inspect.signature(required_controls).parameters), ["action"])

    def test_each_action_selects_its_declared_controls(self) -> None:
        self.assertEqual(
            required_controls(ProtectedAction.COMMIT_DECISION),
            frozenset(
                {
                    Control.ROLE_MATCH,
                    Control.APPROVED,
                    Control.FRESH_EVIDENCE,
                }
            ),
        )
        self.assertEqual(
            required_controls(ProtectedAction.APPLY_EFFECT),
            frozenset(
                {
                    Control.ROLE_MATCH,
                    Control.CANONICAL_DECISION,
                }
            ),
        )
        self.assertEqual(
            required_controls(ProtectedAction.REQUEST_RECOVERY),
            frozenset(
                {
                    Control.ROLE_MATCH,
                    Control.AUTHENTICATED_REQUEST,
                    Control.CANONICAL_DECISION,
                }
            ),
        )

    def test_unknown_action_fails_closed_with_visible_reason(self) -> None:
        result = evaluate_controls(
            "unregistered_action",
            ControlContext(
                caller_role=Role.RECONCILER,
                approved=True,
                evidence_fresh=True,
                canonical_decision_present=True,
                request_authenticated=True,
            ),
        )

        self.assertFalse(result.allowed)
        self.assertIs(result.reason, HoldReason.UNKNOWN_PROTECTED_ACTION)
        self.assertEqual(result.message, HOLD_MESSAGES[result.reason])

    def test_commit_controls_cannot_be_weakened_by_unrelated_runtime_facts(self) -> None:
        result = evaluate_controls(
            ProtectedAction.COMMIT_DECISION,
            ControlContext(
                caller_role=Role.COMMIT,
                approved=False,
                evidence_fresh=True,
                canonical_decision_present=True,
                request_authenticated=True,
            ),
        )

        self.assertFalse(result.allowed)
        self.assertIs(result.reason, HoldReason.APPROVAL_REQUIRED)

    def test_effect_execution_requires_reconciler_role_and_canonical_decision(self) -> None:
        denied = evaluate_controls(
            ProtectedAction.APPLY_EFFECT,
            ControlContext(
                caller_role=Role.COMMIT,
                canonical_decision_present=True,
            ),
        )
        allowed = evaluate_controls(
            ProtectedAction.APPLY_EFFECT,
            ControlContext(
                caller_role=Role.RECONCILER,
                canonical_decision_present=True,
            ),
        )

        self.assertFalse(denied.allowed)
        self.assertIs(denied.reason, HoldReason.ROLE_MISMATCH)
        self.assertTrue(allowed.allowed)
        self.assertIsNone(allowed.reason)
        self.assertIsNone(allowed.message)

    def test_recovery_is_only_an_authenticated_request_for_committed_work(self) -> None:
        unauthenticated = evaluate_controls(
            ProtectedAction.REQUEST_RECOVERY,
            ControlContext(
                caller_role=Role.RECOVERY,
                canonical_decision_present=True,
                request_authenticated=False,
            ),
        )
        missing_decision = evaluate_controls(
            ProtectedAction.REQUEST_RECOVERY,
            ControlContext(
                caller_role=Role.RECOVERY,
                canonical_decision_present=False,
                request_authenticated=True,
            ),
        )
        allowed = evaluate_controls(
            ProtectedAction.REQUEST_RECOVERY,
            ControlContext(
                caller_role=Role.RECOVERY,
                canonical_decision_present=True,
                request_authenticated=True,
            ),
        )

        self.assertIs(unauthenticated.reason, HoldReason.UNAUTHENTICATED_REQUEST)
        self.assertIs(missing_decision.reason, HoldReason.MISSING_CANONICAL_DECISION)
        self.assertTrue(allowed.allowed)

    def test_hold_reason_remains_stable_until_inputs_change(self) -> None:
        held_context = ControlContext(
            caller_role=Role.COMMIT,
            approved=True,
            evidence_fresh=False,
        )

        first = evaluate_controls(ProtectedAction.COMMIT_DECISION, held_context)
        second = evaluate_controls(ProtectedAction.COMMIT_DECISION, held_context)
        resolved = evaluate_controls(
            ProtectedAction.COMMIT_DECISION,
            ControlContext(
                caller_role=Role.COMMIT,
                approved=True,
                evidence_fresh=True,
            ),
        )

        self.assertEqual(first, second)
        self.assertIs(first.reason, HoldReason.STALE_EVIDENCE)
        self.assertEqual(first.message, HOLD_MESSAGES[HoldReason.STALE_EVIDENCE])
        self.assertTrue(resolved.allowed)

    def test_every_hold_reason_has_canonical_presentation(self) -> None:
        self.assertEqual(set(HOLD_MESSAGES), set(HoldReason))
        self.assertTrue(all(message.strip() for message in HOLD_MESSAGES.values()))


if __name__ == "__main__":
    unittest.main()