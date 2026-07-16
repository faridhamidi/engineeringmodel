from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from steering_contract import (  # noqa: E402
    REQUIRED_NORMS,
    extract_steering_block,
    missing_norms,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
STEERING = REPO_ROOT / "skills" / "engineering-model" / "assets" / "steering.md"
INSTALLED_SURFACES = (
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "skills" / "engineering-model" / "assets" / "AGENTS.md",
    REPO_ROOT / "skills" / "engineering-model" / "assets" / "CLAUDE.md",
)


class SteeringContractTests(unittest.TestCase):
    def test_packaged_steering_contains_every_load_bearing_norm(self) -> None:
        self.assertEqual(missing_norms(STEERING.read_text(encoding="utf-8")), set())

    def test_removing_any_norm_is_detected(self) -> None:
        source = STEERING.read_text(encoding="utf-8")
        for name, phrase in REQUIRED_NORMS.items():
            with self.subTest(norm=name):
                known_bad = source.replace(phrase, "", 1)
                self.assertIn(name, missing_norms(known_bad))

    def test_native_instruction_surfaces_match_packaged_canonical_block(self) -> None:
        expected = STEERING.read_text(encoding="utf-8")
        for surface in INSTALLED_SURFACES:
            with self.subTest(surface=surface.name):
                actual = extract_steering_block(surface.read_text(encoding="utf-8"))
                self.assertEqual(actual, expected)

    def test_parity_check_rejects_changed_installed_block(self) -> None:
        expected = STEERING.read_text(encoding="utf-8")
        known_bad = expected.replace("fail closed", "continue", 1)
        self.assertNotEqual(extract_steering_block(known_bad), expected)

    def test_parity_check_rejects_duplicate_installed_block(self) -> None:
        expected = STEERING.read_text(encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exactly once"):
            extract_steering_block(expected + expected)


if __name__ == "__main__":
    unittest.main()
