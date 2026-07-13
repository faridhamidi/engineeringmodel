from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import HarnessManifest, MANIFEST_PATH, REPO_ROOT, RuleDefinition, WITNESS_ROOT, load_harness_manifest

RULE_ID_RE = re.compile(r"^CORE\d{3}$")
OWNER_RE = re.compile(r"^@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:/[A-Za-z0-9_.-]+)?$")
SUPPORTED_LIFECYCLES = {"proposed", "active", "retired", "superseded"}
SUPPORTED_MODES = {"zero_violation", "ratchet"}
SUPPORTED_KINDS = {"forbidden_import", "exclusive_constructor_owner", "required_context_parameter"}
SUPPORTED_SEVERITIES = {"error", "warning"}
PROTECTED_PATHS = {
    "/core/CONFORMANCE_HARNESS.md",
    "/examples/conformance_harness_python/harness_manifest.json",
    "/examples/conformance_harness_python/harness.py",
    "/examples/conformance_harness_python/check_manifest.py",
    "/examples/conformance_harness_python/check_contracts.py",
    "/examples/conformance_harness_python/run_audit.py",
    "/examples/conformance_harness_python/tests/",
    "/.github/workflows/executable-witnesses.yml",
    "/CONTRIBUTING.md",
    "/.github/CODEOWNERS",
}


@dataclass(frozen=True, slots=True)
class Violation:
    message: str


def _slug(text: str) -> str:
    value = text.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value)
    value = re.sub(r"\s+", "-", value)
    return value.strip("-")


def _markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if not match:
            continue
        base = _slug(match.group(1))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def _validate_reference(ref: str, *, field: str, base: Path) -> list[Violation]:
    violations: list[Violation] = []
    if "://" in ref or ref.startswith(("/", "~")):
        return [Violation(f"{field} must be a repository-relative Markdown reference: {ref}")]
    if "#" not in ref:
        return [Violation(f"{field} must include a Markdown anchor: {ref}")]
    raw_path, anchor = ref.split("#", 1)
    if not raw_path.endswith(".md") or not anchor:
        return [Violation(f"{field} must use relative/path.md#anchor form: {ref}")]
    resolved = (base / raw_path).resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return [Violation(f"{field} escapes the repository: {ref}")]
    if not resolved.is_file():
        return [Violation(f"{field} target does not exist: {ref}")]
    if anchor not in _markdown_anchors(resolved):
        violations.append(Violation(f"{field} anchor does not exist: {ref}"))
    return violations


def parse_codeowners(path: Path) -> dict[str, tuple[str, ...]]:
    entries: dict[str, tuple[str, ...]] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        entries[parts[0]] = tuple(parts[1:])
    return entries


def _validate_rule(rule: RuleDefinition, ids: set[str]) -> list[Violation]:
    violations: list[Violation] = []
    if not RULE_ID_RE.fullmatch(rule.id):
        violations.append(Violation(f"rule ID must match CORE###: {rule.id}"))
    if rule.lifecycle not in SUPPORTED_LIFECYCLES:
        violations.append(Violation(f"{rule.id} has unsupported lifecycle: {rule.lifecycle}"))
    if len(rule.statement) > 160:
        violations.append(Violation(f"{rule.id} statement exceeds 160 characters"))
    if tuple(sorted(set(rule.owners))) != rule.owners:
        violations.append(Violation(f"{rule.id} owners must be unique and sorted"))
    for owner in rule.owners:
        if not OWNER_RE.fullmatch(owner):
            violations.append(Violation(f"{rule.id} owner is not a CODEOWNERS principal: {owner}"))
    violations.extend(_validate_reference(rule.rationale_ref, field=f"{rule.id}.rationale_ref", base=WITNESS_ROOT))
    violations.extend(
        _validate_reference(
            rule.approval_control_ref,
            field=f"{rule.id}.approval_control_ref",
            base=WITNESS_ROOT,
        )
    )

    if rule.lifecycle == "active":
        if rule.enforcement_mode not in SUPPORTED_MODES:
            violations.append(Violation(f"{rule.id} active rule requires a supported enforcement_mode"))
        if rule.kind not in SUPPORTED_KINDS:
            violations.append(Violation(f"{rule.id} active rule requires a supported checker kind"))
        if rule.severity not in SUPPORTED_SEVERITIES:
            violations.append(Violation(f"{rule.id} active rule requires a supported severity"))
        if not rule.scope:
            violations.append(Violation(f"{rule.id} active rule requires non-empty scope"))
        if rule.config is None:
            violations.append(Violation(f"{rule.id} active rule requires config"))
        if not rule.positive_test or not rule.refutation_test:
            violations.append(Violation(f"{rule.id} active rule requires positive_test and refutation_test"))
        if rule.enforcement_mode == "zero_violation" and rule.known_violations:
            violations.append(Violation(f"{rule.id} zero_violation rule must not declare known_violations"))
        if rule.enforcement_mode == "ratchet":
            if not rule.known_violations:
                violations.append(Violation(f"{rule.id} ratchet rule requires known_violations"))
            if tuple(sorted(set(rule.known_violations))) != rule.known_violations:
                violations.append(Violation(f"{rule.id} known_violations must be unique and sorted"))
        for rel in (*rule.scope, *rule.known_violations):
            if Path(rel).is_absolute() or ".." in Path(rel).parts:
                violations.append(Violation(f"{rule.id} path must be witness-relative: {rel}"))
    elif rule.lifecycle == "retired":
        if not rule.retirement_reason:
            violations.append(Violation(f"{rule.id} retired rule requires retirement_reason"))
    elif rule.lifecycle == "superseded":
        if not rule.retirement_reason or not rule.superseded_by:
            violations.append(Violation(f"{rule.id} superseded rule requires successor and reason"))
        elif rule.superseded_by == rule.id:
            violations.append(Violation(f"{rule.id} cannot supersede itself"))
        elif rule.superseded_by not in ids:
            violations.append(Violation(f"{rule.id} successor does not exist: {rule.superseded_by}"))
    return violations


def _validate_supersession_cycles(manifest: HarnessManifest) -> list[Violation]:
    successors = {rule.id: rule.superseded_by for rule in manifest.rules if rule.superseded_by}
    violations: list[Violation] = []
    for start in successors:
        seen: set[str] = set()
        current: str | None = start
        while current in successors:
            if current in seen:
                violations.append(Violation(f"supersession cycle detected from {start}"))
                break
            seen.add(current)
            current = successors[current]
    return violations


def _validate_ownership(manifest: HarnessManifest, codeowners_path: Path) -> list[Violation]:
    violations: list[Violation] = []
    if not codeowners_path.is_file():
        return [Violation(".github/CODEOWNERS does not exist")]
    entries = parse_codeowners(codeowners_path)
    manifest_pattern = "/examples/conformance_harness_python/harness_manifest.json"
    declared = set().union(*(set(rule.owners) for rule in manifest.rules))
    actual = set(entries.get(manifest_pattern, ()))
    if not actual:
        violations.append(Violation(f"CODEOWNERS does not cover {manifest_pattern}"))
    elif not declared.issubset(actual):
        violations.append(Violation(f"manifest owners {sorted(declared)} do not match CODEOWNERS {sorted(actual)}"))
    for protected in sorted(PROTECTED_PATHS):
        owners = set(entries.get(protected, ()))
        if not owners:
            violations.append(Violation(f"CODEOWNERS does not explicitly cover {protected}"))
        elif not declared.issubset(owners):
            violations.append(Violation(f"CODEOWNERS entry for {protected} is incompatible with manifest owners"))
    return violations


def validate_manifest(
    manifest: HarnessManifest,
    *,
    manifest_path: Path = MANIFEST_PATH,
    codeowners_path: Path | None = None,
) -> list[Violation]:
    violations: list[Violation] = []
    ids = [rule.id for rule in manifest.rules]
    if len(ids) != len(set(ids)):
        violations.append(Violation("rule IDs must be unique and never reused"))
    id_set = set(ids)
    for rule in manifest.rules:
        violations.extend(_validate_rule(rule, id_set))
    violations.extend(_validate_supersession_cycles(manifest))

    check_names = [check.name for check in manifest.audit.checks]
    if len(check_names) != len(set(check_names)):
        violations.append(Violation("audit check names must be unique"))
    report_path = Path(manifest.audit.report_path_default)
    if report_path.is_absolute() or ".." in report_path.parts:
        violations.append(Violation("audit report path must be witness-relative"))
    for check in manifest.audit.checks:
        if "{python}" not in check.command:
            violations.append(Violation(f"audit check {check.name} must include {{python}}"))
        for token in check.command:
            if token.endswith(".py") and not (WITNESS_ROOT / token).is_file():
                violations.append(Violation(f"audit check {check.name} references missing script: {token}"))

    owners_path = codeowners_path or (REPO_ROOT / ".github" / "CODEOWNERS")
    violations.extend(_validate_ownership(manifest, owners_path))
    return violations


def main() -> int:
    try:
        manifest = load_harness_manifest()
        violations = validate_manifest(manifest)
    except Exception as exc:
        print(f"[manifest] failed to load {MANIFEST_PATH}: {exc}")
        return 1
    if violations:
        print("[manifest] validation failed:")
        for violation in violations:
            print(f"- {violation.message}")
        return 1
    print("[manifest] validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
