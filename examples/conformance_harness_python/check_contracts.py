from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import HarnessManifest, RuleDefinition, WITNESS_ROOT, load_harness_manifest


@dataclass(frozen=True, slots=True)
class Violation:
    rule_id: str
    path: str
    line: int
    message: str


@dataclass(frozen=True, slots=True)
class RuleResult:
    rule: RuleDefinition
    violations: tuple[Violation, ...]
    observed_paths: tuple[str, ...]
    ok: bool
    detail: str


def _iter_python_files(root: Path, scope: str) -> Iterable[Path]:
    target = root / scope
    if target.is_file():
        yield target
        return
    if target.is_dir():
        yield from sorted(target.rglob("*.py"))


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _forbidden_imports(rule: RuleDefinition, root: Path) -> list[Violation]:
    forbidden = tuple((rule.config or {}).get("forbidden_modules", ()))
    violations: list[Violation] = []
    for scope in rule.scope:
        for path in _iter_python_files(root, scope):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                modules: list[str] = []
                if isinstance(node, ast.Import):
                    modules.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules.append(node.module)
                for module in modules:
                    if any(module == target or module.startswith(f"{target}.") for target in forbidden):
                        violations.append(
                            Violation(rule.id, _relative(path, root), node.lineno, f"forbidden import: {module}")
                        )
    return violations


def _constructor_calls(path: Path, constructor: str) -> list[int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    aliases = {constructor}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == constructor:
                    aliases.add(alias.asname or alias.name)
    lines: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in aliases:
            lines.append(node.lineno)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == constructor:
            lines.append(node.lineno)
    return lines


def _exclusive_constructor_owner(rule: RuleDefinition, root: Path) -> list[Violation]:
    config = rule.config or {}
    constructor = str(config.get("constructor", ""))
    allowed = set(config.get("allowed_owners", ()))
    violations: list[Violation] = []
    for scope in rule.scope:
        for path in _iter_python_files(root, scope):
            rel = _relative(path, root)
            for line in _constructor_calls(path, constructor):
                if rel not in allowed:
                    violations.append(
                        Violation(rule.id, rel, line, f"{constructor} constructed outside declared owner")
                    )
    return violations


def _required_context_parameter(rule: RuleDefinition, root: Path) -> list[Violation]:
    config = rule.config or {}
    function_name = str(config.get("function", ""))
    parameter = str(config.get("parameter", ""))
    violations: list[Violation] = []
    for scope in rule.scope:
        for path in _iter_python_files(root, scope):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            functions = [
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name
            ]
            if not functions:
                violations.append(
                    Violation(rule.id, _relative(path, root), 1, f"required function not found: {function_name}")
                )
                continue
            for node in functions:
                names = {arg.arg for arg in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)}
                if parameter not in names:
                    violations.append(
                        Violation(
                            rule.id,
                            _relative(path, root),
                            node.lineno,
                            f"{function_name} missing required parameter: {parameter}",
                        )
                    )
    return violations


def check_rule(rule: RuleDefinition, root: Path = WITNESS_ROOT) -> list[Violation]:
    if rule.kind == "forbidden_import":
        return _forbidden_imports(rule, root)
    if rule.kind == "exclusive_constructor_owner":
        return _exclusive_constructor_owner(rule, root)
    if rule.kind == "required_context_parameter":
        return _required_context_parameter(rule, root)
    raise ValueError(f"unsupported checker kind: {rule.kind}")


def evaluate_rule(rule: RuleDefinition, root: Path = WITNESS_ROOT) -> RuleResult:
    violations = tuple(check_rule(rule, root))
    observed = tuple(sorted({violation.path for violation in violations}))
    if rule.enforcement_mode == "zero_violation":
        ok = not observed
        detail = "no prohibited violations" if ok else f"observed violations: {list(observed)}"
    elif rule.enforcement_mode == "ratchet":
        expected = tuple(rule.known_violations)
        ok = observed == expected
        detail = (
            "observed set matches declared ratchet"
            if ok
            else f"declared={list(expected)} observed={list(observed)}"
        )
    else:
        raise ValueError(f"active rule {rule.id} has unsupported enforcement mode: {rule.enforcement_mode}")
    return RuleResult(rule=rule, violations=violations, observed_paths=observed, ok=ok, detail=detail)


def evaluate_manifest(manifest: HarnessManifest, root: Path = WITNESS_ROOT) -> tuple[RuleResult, ...]:
    return tuple(evaluate_rule(rule, root) for rule in manifest.active_rules)


def main() -> int:
    manifest = load_harness_manifest()
    results = evaluate_manifest(manifest)
    failed = False
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"[{result.rule.id}] {status}: {result.detail}")
        if not result.ok:
            failed = True
            for violation in result.violations:
                print(f"- {violation.path}:{violation.line}: {violation.message}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
