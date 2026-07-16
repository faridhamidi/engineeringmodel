from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from line import ABOVE, BELOW, classify  # noqa: E402


class BlastRadiusLineTests(unittest.TestCase):
    def test_decision_table(self) -> None:
        cases = {
            (False, True): BELOW,   # local + reversible -> build freely
            (True, True): ABOVE,    # shared -> stop, even if reversible
            (True, False): ABOVE,   # shared + irreversible -> stop
            (False, False): ABOVE,  # irreversible -> stop, even if local
        }
        for (shared, reversible), expected in cases.items():
            with self.subTest(shared=shared, reversible=reversible):
                self.assertEqual(classify(shared, reversible), expected)

    def test_only_local_and_reversible_routes_below(self) -> None:
        self.assertEqual(classify(False, True), BELOW)

    def test_shared_signal_is_load_bearing(self) -> None:
        # A rule that ignored 'shared' and checked only reversibility would
        # misroute this case to BELOW. The correct oracle routes ABOVE.
        self.assertEqual(classify(True, True), ABOVE)

    def test_irreversible_signal_is_load_bearing(self) -> None:
        # A rule that ignored reversibility would misroute this case to BELOW.
        self.assertEqual(classify(False, False), ABOVE)

    def test_uncertainty_fails_closed(self) -> None:
        self.assertEqual(classify(None, True), ABOVE)
        self.assertEqual(classify(True, None), ABOVE)
        self.assertEqual(classify(None, None), ABOVE)


if __name__ == "__main__":
    unittest.main()
