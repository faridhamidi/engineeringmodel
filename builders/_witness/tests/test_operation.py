from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from line import ABOVE, BELOW  # noqa: E402
from operation import (  # noqa: E402
    APPROVAL_REQUIRED,
    CONTINUE,
    REVIEW,
    decide_operation,
)


class OperationDecisionTests(unittest.TestCase):
    def test_clearly_below_action_continues(self) -> None:
        result = decide_operation(
            touches_shared=False,
            reversible=True,
            external_effect=False,
        )
        self.assertEqual(result.line, BELOW)
        self.assertEqual(result.next_step, CONTINUE)

    def test_external_effect_requires_approval(self) -> None:
        result = decide_operation(
            touches_shared=True,
            reversible=False,
            external_effect=True,
        )
        self.assertEqual(result.line, ABOVE)
        self.assertEqual(result.next_step, APPROVAL_REQUIRED)

    def test_uncertain_external_effect_fails_closed_to_approval(self) -> None:
        result = decide_operation(
            touches_shared=False,
            reversible=True,
            external_effect=None,
        )
        self.assertEqual(result.line, ABOVE)
        self.assertEqual(result.next_step, APPROVAL_REQUIRED)

    def test_above_line_authoring_without_external_effect_requires_review(self) -> None:
        result = decide_operation(
            touches_shared=False,
            reversible=False,
            external_effect=False,
        )
        self.assertEqual(result.line, ABOVE)
        self.assertEqual(result.next_step, REVIEW)


if __name__ == "__main__":
    unittest.main()
