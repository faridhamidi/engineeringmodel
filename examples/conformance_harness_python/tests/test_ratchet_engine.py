from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import shutil
import tempfile
import unittest
from dataclasses import replace
from check_contracts import evaluate_rule
from harness import load_harness_manifest

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class RatchetEngineTests(unittest.TestCase):
    def _copy_fixture(self, destination: Path) -> None:
        shutil.copytree(FIXTURES / "ratchet_project", destination, dirs_exist_ok=True)

    def _fixture_rule(self):
        manifest = load_harness_manifest(FIXTURES / "ratchet_manifest.json")
        rule = manifest.active_rules[0]
        self.assertEqual(rule.id, "FIXTURE.ARCH.001")
        return rule

    def test_declared_set_equal_to_observed_set_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._copy_fixture(root)
            self.assertTrue(evaluate_rule(self._fixture_rule(), root).ok)

    def test_new_violation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._copy_fixture(root)
            (root / "new_bypass.py").write_text("from integrations import VendorClient\nVendorClient()\n", encoding="utf-8")
            self.assertFalse(evaluate_rule(self._fixture_rule(), root).ok)

    def test_cleanup_without_manifest_shrink_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._copy_fixture(root)
            (root / "known_b.py").unlink()
            self.assertFalse(evaluate_rule(self._fixture_rule(), root).ok)

    def test_cleanup_with_manifest_shrink_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._copy_fixture(root)
            (root / "known_b.py").unlink()
            rule = replace(self._fixture_rule(), known_violations=("known_a.py",))
            self.assertTrue(evaluate_rule(rule, root).ok)

    def test_transition_to_zero_requires_empty_observed_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._copy_fixture(root)
            zero_rule = replace(self._fixture_rule(), enforcement_mode="zero_violation", known_violations=())
            self.assertFalse(evaluate_rule(zero_rule, root).ok)
            (root / "known_a.py").unlink()
            (root / "known_b.py").unlink()
            self.assertTrue(evaluate_rule(zero_rule, root).ok)


if __name__ == "__main__":
    unittest.main()
