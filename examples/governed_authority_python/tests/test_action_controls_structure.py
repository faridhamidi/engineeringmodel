from __future__ import annotations

import ast
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "governed_authority_example"


def function_call_sites(function_name: str) -> set[str]:
    found: set[str] = set()
    for path in SRC.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == function_name:
                    found.add(path.name)
    return found


def name_reference_sites(name: str) -> set[str]:
    found: set[str] = set()
    for path in SRC.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if any(isinstance(node, ast.Name) and node.id == name for node in ast.walk(tree)):
            found.add(path.name)
    return found


def imported_local_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.lstrip("."))
    return modules


class ProtectedActionStructureTests(unittest.TestCase):
    def test_runtime_evaluator_is_the_only_source_consumer_of_control_selection(self) -> None:
        self.assertEqual(function_call_sites("required_controls"), {"control_evaluation.py"})

    def test_registry_is_not_read_directly_outside_its_owner(self) -> None:
        self.assertEqual(name_reference_sites("ACTION_REGISTRY"), {"protected_actions.py"})

    def test_static_selection_does_not_import_runtime_state_modules(self) -> None:
        imports = imported_local_modules(SRC / "protected_actions.py")
        forbidden = {"store", "external", "policy", "reconciler", "recovery"}
        self.assertEqual(imports & forbidden, set())

    def test_runtime_evaluation_does_not_gain_mutation_or_commit_access(self) -> None:
        imports = imported_local_modules(SRC / "control_evaluation.py")
        forbidden = {"store", "external", "commit", "reconciler", "recovery"}
        self.assertEqual(imports & forbidden, set())


if __name__ == "__main__":
    unittest.main()