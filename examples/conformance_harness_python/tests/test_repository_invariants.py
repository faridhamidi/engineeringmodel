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

    def test_core_arch_001(self) -> None:
        self.assertTrue(self.results["CORE.ARCH.001"].ok, self.results["CORE.ARCH.001"].detail)

    def test_core_arch_002(self) -> None:
        result = self.results["CORE.ARCH.002"]
        self.assertTrue(result.ok, result.detail)
        self.assertEqual(result.observed_paths, ("sample_project/known_constructor_site.py",))

    def test_core_context_001(self) -> None:
        self.assertTrue(self.results["CORE.CONTEXT.001"].ok, self.results["CORE.CONTEXT.001"].detail)


if __name__ == "__main__":
    unittest.main()
