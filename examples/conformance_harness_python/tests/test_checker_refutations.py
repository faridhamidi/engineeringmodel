from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tempfile
import unittest
from check_contracts import evaluate_rule
from harness import load_harness_manifest


class CheckerRefutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = {rule.id: rule for rule in load_harness_manifest().active_rules}

    def test_core_arch_001(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "sample_project" / "decisions.py"
            path.parent.mkdir(parents=True)
            path.write_text("from sample_project.integrations import VendorClient\n", encoding="utf-8")
            result = evaluate_rule(self.rules["CORE.ARCH.001"], root)
            self.assertFalse(result.ok)
            self.assertEqual(result.violations[0].rule_id, "CORE.ARCH.001")

    def test_core_arch_002(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "sample_project"
            project.mkdir(parents=True)
            (project / "integrations.py").write_text("class VendorClient: pass\nVendorClient()\n", encoding="utf-8")
            (project / "known_constructor_site.py").write_text(
                "from sample_project.integrations import VendorClient\nVendorClient()\n", encoding="utf-8"
            )
            (project / "bypass.py").write_text(
                "import sample_project.integrations as integrations\nintegrations.VendorClient()\n", encoding="utf-8"
            )
            result = evaluate_rule(self.rules["CORE.ARCH.002"], root)
            self.assertFalse(result.ok)
            self.assertIn("sample_project/bypass.py", result.observed_paths)
            self.assertTrue(any(item.rule_id == "CORE.ARCH.002" for item in result.violations))

    def test_core_context_001(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "sample_project" / "service.py"
            path.parent.mkdir(parents=True)
            path.write_text("def run_operation(raw: str):\n    return raw\n", encoding="utf-8")
            result = evaluate_rule(self.rules["CORE.CONTEXT.001"], root)
            self.assertFalse(result.ok)
            self.assertEqual(result.violations[0].rule_id, "CORE.CONTEXT.001")


if __name__ == "__main__":
    unittest.main()
