from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

WITNESS_ROOT = Path(__file__).resolve().parent
REPO_ROOT = WITNESS_ROOT.parents[1]
MANIFEST_PATH = WITNESS_ROOT / "harness_manifest.json"

_RULE_FIELDS = {
    "id",
    "lifecycle",
    "enforcement_mode",
    "statement",
    "rationale_ref",
    "owners",
    "approval_control_ref",
    "kind",
    "severity",
    "scope",
    "config",
    "positive_test",
    "refutation_test",
    "known_violations",
    "retirement_reason",
    "superseded_by",
}


@dataclass(frozen=True, slots=True)
class RuleDefinition:
    id: str
    lifecycle: str
    statement: str
    rationale_ref: str
    owners: tuple[str, ...]
    approval_control_ref: str
    enforcement_mode: str | None = None
    kind: str | None = None
    severity: str | None = None
    scope: tuple[str, ...] = ()
    config: dict[str, Any] | None = None
    positive_test: str | None = None
    refutation_test: str | None = None
    known_violations: tuple[str, ...] = ()
    retirement_reason: str | None = None
    superseded_by: str | None = None


@dataclass(frozen=True, slots=True)
class AuditCheckDefinition:
    name: str
    command: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AuditDefinition:
    report_path_default: str
    checks: tuple[AuditCheckDefinition, ...]


@dataclass(frozen=True, slots=True)
class HarnessManifest:
    manifest_version: int
    rules: tuple[RuleDefinition, ...]
    audit: AuditDefinition

    @property
    def active_rules(self) -> tuple[RuleDefinition, ...]:
        return tuple(rule for rule in self.rules if rule.lifecycle == "active")

    @property
    def historical_rules(self) -> tuple[RuleDefinition, ...]:
        return tuple(rule for rule in self.rules if rule.lifecycle in {"retired", "superseded"})


def _expect_dict(value: object, *, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _expect_text(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_text(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return _expect_text(value, field=field)


def _expect_text_list(value: object, *, field: str, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list of strings")
    if not allow_empty and not value:
        raise ValueError(f"{field} must not be empty")
    return tuple(_expect_text(item, field=f"{field}[{index}]") for index, item in enumerate(value))


def load_harness_manifest(path: Path | None = None) -> HarnessManifest:
    manifest_path = path or MANIFEST_PATH
    root = _expect_dict(json.loads(manifest_path.read_text(encoding="utf-8")), field="manifest")
    unknown_root = set(root) - {"manifest_version", "rules", "audit"}
    if unknown_root:
        raise ValueError(f"manifest contains unknown fields: {sorted(unknown_root)}")

    version = root.get("manifest_version")
    if not isinstance(version, int) or version < 1:
        raise ValueError("manifest_version must be an integer >= 1")

    raw_rules = root.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("rules must be a non-empty list")

    rules: list[RuleDefinition] = []
    for index, raw in enumerate(raw_rules):
        item = _expect_dict(raw, field=f"rules[{index}]")
        unknown = set(item) - _RULE_FIELDS
        if unknown:
            raise ValueError(f"rules[{index}] contains unknown fields: {sorted(unknown)}")
        config_raw = item.get("config")
        config = None if config_raw is None else _expect_dict(config_raw, field=f"rules[{index}].config")
        owners = _expect_text_list(item.get("owners"), field=f"rules[{index}].owners")
        scope_raw = item.get("scope", [])
        known_raw = item.get("known_violations", [])
        rules.append(
            RuleDefinition(
                id=_expect_text(item.get("id"), field=f"rules[{index}].id"),
                lifecycle=_expect_text(item.get("lifecycle"), field=f"rules[{index}].lifecycle"),
                statement=_expect_text(item.get("statement"), field=f"rules[{index}].statement"),
                rationale_ref=_expect_text(item.get("rationale_ref"), field=f"rules[{index}].rationale_ref"),
                owners=owners,
                approval_control_ref=_expect_text(
                    item.get("approval_control_ref"), field=f"rules[{index}].approval_control_ref"
                ),
                enforcement_mode=_optional_text(
                    item.get("enforcement_mode"), field=f"rules[{index}].enforcement_mode"
                ),
                kind=_optional_text(item.get("kind"), field=f"rules[{index}].kind"),
                severity=_optional_text(item.get("severity"), field=f"rules[{index}].severity"),
                scope=_expect_text_list(scope_raw, field=f"rules[{index}].scope", allow_empty=True),
                config=config,
                positive_test=_optional_text(item.get("positive_test"), field=f"rules[{index}].positive_test"),
                refutation_test=_optional_text(
                    item.get("refutation_test"), field=f"rules[{index}].refutation_test"
                ),
                known_violations=_expect_text_list(
                    known_raw, field=f"rules[{index}].known_violations", allow_empty=True
                ),
                retirement_reason=_optional_text(
                    item.get("retirement_reason"), field=f"rules[{index}].retirement_reason"
                ),
                superseded_by=_optional_text(item.get("superseded_by"), field=f"rules[{index}].superseded_by"),
            )
        )

    audit_raw = _expect_dict(root.get("audit"), field="audit")
    unknown_audit = set(audit_raw) - {"report_path_default", "checks"}
    if unknown_audit:
        raise ValueError(f"audit contains unknown fields: {sorted(unknown_audit)}")
    checks_raw = audit_raw.get("checks")
    if not isinstance(checks_raw, list) or not checks_raw:
        raise ValueError("audit.checks must be a non-empty list")
    checks: list[AuditCheckDefinition] = []
    for index, raw in enumerate(checks_raw):
        item = _expect_dict(raw, field=f"audit.checks[{index}]")
        unknown = set(item) - {"name", "command"}
        if unknown:
            raise ValueError(f"audit.checks[{index}] contains unknown fields: {sorted(unknown)}")
        checks.append(
            AuditCheckDefinition(
                name=_expect_text(item.get("name"), field=f"audit.checks[{index}].name"),
                command=_expect_text_list(item.get("command"), field=f"audit.checks[{index}].command"),
            )
        )

    return HarnessManifest(
        manifest_version=version,
        rules=tuple(rules),
        audit=AuditDefinition(
            report_path_default=_expect_text(audit_raw.get("report_path_default"), field="audit.report_path_default"),
            checks=tuple(checks),
        ),
    )
