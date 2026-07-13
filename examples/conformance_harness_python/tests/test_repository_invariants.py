from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest

from check_contracts import evaluate_manifest
from harness import load_harness_manifest


class RepositoryInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.results = {result.rule.id: result for result in evaluate_manifest(load_harness_manifest())}

    def test_core001(self) -> None:
        self.assertTrue(self.results["CORE001"].ok, self.results["CORE001"].detail)

    def test_core002(self) -> None:
        result = self.results["CORE002"]
        self.assertTrue(result.ok, result.detail)
        self.assertEqual(result.observed_paths, ("sample_project/legacy_adapter.py",))

    def test_core003(self) -> None:
        self.assertTrue(self.results["CORE003"].ok, self.results["CORE003"].detail)


if __name__ == "__main__":
    unittest.main()
