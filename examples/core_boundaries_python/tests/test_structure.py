from __future__ import annotations

import ast
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "core_boundary_example"


class CoreBoundaryStructureTests(unittest.TestCase):
    def test_decision_module_has_no_external_runtime_imports(self) -> None:
        tree = ast.parse((SRC / "decisions.py").read_text(encoding="utf-8"))
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

        forbidden = {"boto3", "requests", "socket", "subprocess", "sqlite3"}
        self.assertEqual(imported_roots & forbidden, set())

    def test_vendor_client_construction_ratchet(self) -> None:
        found: set[str] = set()
        for path in SRC.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id == "VendorClient":
                        found.add(path.name)

        # In a legacy codebase this set may temporarily contain known violations.
        # Any new call site fails until the allowed set is deliberately reviewed.
        allowed_construction_sites = {"integrations.py"}
        self.assertEqual(found, allowed_construction_sites)


if __name__ == "__main__":
    unittest.main()
