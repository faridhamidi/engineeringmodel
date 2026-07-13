from __future__ import annotations

import ast
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "governed_authority_example"


def call_sites(method_name: str) -> set[str]:
    found: set[str] = set()
    for path in SRC.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == method_name:
                    found.add(path.name)
    return found


def imported_local_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.lstrip("."))
    return modules


class GovernedAuthorityStructureTests(unittest.TestCase):
    def test_canonical_write_call_site_is_commit_only(self) -> None:
        self.assertEqual(call_sites("write_canonical"), {"commit.py"})

    def test_managed_mutation_call_site_is_reconciler_only(self) -> None:
        self.assertEqual(call_sites("mutate_managed_resource"), {"reconciler.py"})

    def test_recovery_requests_reconciliation_without_direct_reconciler_access(self) -> None:
        self.assertEqual(call_sites("reconcile"), {"reconciliation_request.py"})
        recovery_imports = imported_local_modules(SRC / "recovery.py")
        self.assertNotIn("reconciler", recovery_imports)

    def test_policy_is_pure_of_store_external_and_security_modules(self) -> None:
        tree = ast.parse((SRC / "policy.py").read_text(encoding="utf-8"))
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module
        }
        forbidden = {"store", "external", "security", ".store", ".external", ".security"}
        self.assertEqual(imported_modules & forbidden, set())


if __name__ == "__main__":
    unittest.main()
