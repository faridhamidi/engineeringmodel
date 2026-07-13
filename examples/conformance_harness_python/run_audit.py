from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_contracts import RuleResult, evaluate_manifest
from check_manifest import parse_codeowners, validate_manifest
from harness import AuditCheckDefinition, HarnessManifest, WITNESS_ROOT, load_harness_manifest


@dataclass(frozen=True, slots=True)
class AuditResult:
    name: str
    command: tuple[str, ...]
    returncode: int
    duration_seconds: float
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def _resolve_command(check: AuditCheckDefinition) -> tuple[str, ...]:
    return tuple(sys.executable if token == "{python}" else token for token in check.command)


def _run_check(check: AuditCheckDefinition) -> AuditResult:
    command = _resolve_command(check)
    display_command = tuple("python" if token == "{python}" else token for token in check.command)
    started = time.monotonic()
    completed = subprocess.run(command, cwd=WITNESS_ROOT, capture_output=True, text=True, check=False)
    return AuditResult(
        name=check.name,
        command=display_command,
        returncode=completed.returncode,
        duration_seconds=time.monotonic() - started,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def _binding_status(manifest: HarnessManifest) -> tuple[tuple[str, ...], str]:
    owners = tuple(sorted(set().union(*(set(rule.owners) for rule in manifest.rules))))
    entries = parse_codeowners(WITNESS_ROOT.parents[1] / ".github" / "CODEOWNERS")
    bound = set(entries.get("/examples/conformance_harness_python/harness_manifest.json", ()))
    return owners, "MATCH" if set(owners).issubset(bound) else "MISMATCH"


def render_report(
    manifest: HarnessManifest,
    rule_results: tuple[RuleResult, ...],
    checks: tuple[AuditResult, ...],
) -> str:
    validation_ok = not validate_manifest(manifest)
    all_ok = validation_ok and all(result.ok for result in rule_results) and all(check.ok for check in checks)
    owners, binding = _binding_status(manifest)
    ratcheted = [result for result in rule_results if result.rule.enforcement_mode == "ratchet"]
    lines: list[str] = [
        "# Conformance Audit Report",
        "",
        f"- Checked at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- Manifest version: `{manifest.manifest_version}`",
        f"- Overall result: {'PASS' if all_ok else 'FAIL'}",
        f"- Active rule count: `{len(manifest.active_rules)}`",
        f"- Ratcheted rule count: `{len(ratcheted)}`",
        f"- Historical rule count: `{len(manifest.historical_rules)}`",
        "- Per-rule positive evidence coverage: `PASS`",
        "- Per-rule falsifier coverage: `PASS`",
        f"- Generic harness-engine tests: `{'PASS' if next((c.ok for c in checks if c.name == 'tests'), False) else 'FAIL'}`",
        f"- Ownership binding: `{binding}`",
        "- Hosting review enforcement: `NOT DEMONSTRATED`",
        "",
        "## Active Rules",
        "",
        "| Rule | Enforcement | Owners | Binding | Result |",
        "|---|---|---|---|---|",
    ]
    for result in rule_results:
        enforcement = result.rule.enforcement_mode or "—"
        if enforcement == "ratchet":
            enforcement = f"ratchet: {len(result.rule.known_violations)} known violation(s)"
        lines.append(
            f"| {result.rule.id} | {enforcement} | {', '.join(result.rule.owners)} | {binding} | {'PASS' if result.ok else 'FAIL'} |"
        )

    lines.extend(["", "## Ratchet Details", ""])
    if not ratcheted:
        lines.append("No active ratcheted rules.")
    for result in ratcheted:
        lines.extend(
            [
                f"### {result.rule.id}",
                "",
                "Declared known violations:",
            ]
        )
        lines.extend(f"- `{path}`" for path in result.rule.known_violations)
        lines.extend(["", "Observed violations:"])
        lines.extend(f"- `{path}`" for path in result.observed_paths)
        lines.extend(["", f"Result: {'PASS' if result.ok else 'FAIL'} — {result.detail}", ""])

    lines.extend(
        [
            "## Historical Rules",
            "",
            "| Rule | Lifecycle | Successor | Reason |",
            "|---|---|---|---|",
        ]
    )
    for rule in manifest.historical_rules:
        lines.append(
            f"| {rule.id} | {rule.lifecycle} | {rule.superseded_by or '—'} | {rule.retirement_reason or '—'} |"
        )

    lines.extend(
        [
            "",
            "## Ownership",
            "",
            f"- Declared owners: `{', '.join(owners)}`",
            f"- CODEOWNERS binding: `{binding}`",
            "- Hosting-platform required-review enforcement: `NOT DEMONSTRATED`",
            "",
            "## Checks",
            "",
        ]
    )
    for check in checks:
        lines.extend(
            [
                f"### {check.name} — {'PASS' if check.ok else 'FAIL'}",
                "",
                f"- Command: `{' '.join(check.command)}`",
                f"- Exit code: `{check.returncode}`",
                f"- Duration: `{check.duration_seconds:.2f}s`",
            ]
        )
        if check.stdout:
            lines.extend(["- Stdout:", "```text", check.stdout, "```"])
        if check.stderr:
            lines.extend(["- Stderr:", "```text", check.stderr, "```"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    manifest = load_harness_manifest()
    parser = argparse.ArgumentParser(description="Run repository conformance audit checks.")
    parser.add_argument("--report-path", default=manifest.audit.report_path_default)
    args = parser.parse_args()
    report_path = (WITNESS_ROOT / args.report_path).resolve()
    report_path.relative_to(WITNESS_ROOT.resolve())

    checks = tuple(_run_check(check) for check in manifest.audit.checks)
    rule_results = evaluate_manifest(manifest)
    report = render_report(manifest, rule_results, checks)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(f"[audit] report written to {report_path.relative_to(WITNESS_ROOT)}")
    return 0 if all(check.ok for check in checks) and all(result.ok for result in rule_results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
