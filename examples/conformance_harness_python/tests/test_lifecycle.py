from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
from dataclasses import replace

from check_manifest import validate_manifest
from harness import HarnessManifest, load_harness_manifest
from run_audit import AuditResult, render_report


class LifecycleTests(unittest.TestCase):
    def test_only_active_rules_execute(self) -> None:
        manifest = load_harness_manifest()
        self.assertTrue(all(rule.lifecycle == "active" for rule in manifest.active_rules))
        self.assertEqual({rule.id for rule in manifest.historical_rules}, {"CORE004", "CORE005"})

    def test_missing_successor_fails(self) -> None:
        manifest = load_harness_manifest()
        rules = tuple(
            replace(rule, superseded_by="CORE999") if rule.id == "CORE005" else rule
            for rule in manifest.rules
        )
        changed = HarnessManifest(manifest.manifest_version, rules, manifest.audit)
        messages = [item.message for item in validate_manifest(changed)]
        self.assertTrue(any("successor does not exist" in message for message in messages))

    def test_supersession_cycle_fails(self) -> None:
        manifest = load_harness_manifest()
        rules = tuple(
            replace(rule, lifecycle="superseded", superseded_by="CORE005", retirement_reason="fixture")
            if rule.id == "CORE003"
            else rule
            for rule in manifest.rules
        )
        changed = HarnessManifest(manifest.manifest_version, rules, manifest.audit)
        messages = [item.message for item in validate_manifest(changed)]
        self.assertTrue(any("cycle" in message for message in messages))

    def test_audit_contains_historical_rules(self) -> None:
        manifest = load_harness_manifest()
        checks = (AuditResult("tests", ("python",), 0, 0.01, "ok", ""),)
        report = render_report(manifest, (), checks)
        self.assertIn("## Historical Rules", report)
        self.assertIn("CORE004", report)
        self.assertIn("CORE005", report)


if __name__ == "__main__":
    unittest.main()
