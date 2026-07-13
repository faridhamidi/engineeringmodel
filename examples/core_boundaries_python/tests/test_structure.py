from __future__ import annotations

import ast
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "core_boundary_example"


def constructor_call_count(source: str, target: str) -> int:
    tree = ast.parse(source)
    direct_aliases = {target}

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == target:
                    direct_aliases.add(alias.asname or alias.name)

    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in direct_aliases:
            count += 1
        elif isinstance(node.func, ast.Attribute) and node.func.attr == target:
            count += 1
    return count


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

    def test_constructor_detector_catches_direct_qualified_and_aliased_calls(self) -> None:
        source = """
from package.integrations import VendorClient as VC
import package.integrations as integrations
VendorClient()
VC()
integrations.VendorClient()
"""
        self.assertEqual(constructor_call_count(source, "VendorClient"), 3)

    def test_vendor_client_construction_ratchet(self) -> None:
        found: set[str] = set()
        for path in SRC.glob("*.py"):
            source = path.read_text(encoding="utf-8")
            if constructor_call_count(source, "VendorClient"):
                found.add(path.name)

        # In a legacy codebase this set may temporarily contain known violations.
        # Any new call site fails until the allowed set is deliberately reviewed.
        allowed_construction_sites = {"integrations.py"}
        self.assertEqual(found, allowed_construction_sites)


if __name__ == "__main__":
    unittest.main()
