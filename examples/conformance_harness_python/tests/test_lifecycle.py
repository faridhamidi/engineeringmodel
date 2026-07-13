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
    def _synthetic_historical_manifest(self) -> HarnessManifest:
        manifest = load_harness_manifest()
        first = manifest.active_rules[0]
        second = manifest.active_rules[1]
        retired = replace(
            first,
            id="CORE.TEST.900",
            lifecycle="retired",
            enforcement_mode=None,
            kind=None,
            severity=None,
            scope=(),
            config=None,
            positive_test=None,
            refutation_test=None,
            known_violations=(),
            retirement_reason="Synthetic lifecycle fixture.",
            superseded_by=None,
        )
        superseded = replace(
            second,
            id="CORE.TEST.901",
            lifecycle="superseded",
            enforcement_mode=None,
            kind=None,
            severity=None,
            scope=(),
            config=None,
            positive_test=None,
            refutation_test=None,
            known_violations=(),
            retirement_reason="Synthetic lifecycle fixture.",
            superseded_by="CORE.TEST.900",
        )
        return HarnessManifest(manifest.manifest_version, (retired, superseded), manifest.audit)

    def test_live_manifest_contains_only_active_rules(self) -> None:
        manifest = load_harness_manifest()
        self.assertTrue(all(rule.lifecycle == "active" for rule in manifest.rules))
        self.assertEqual(manifest.historical_rules, ())

    def test_historical_rules_do_not_execute(self) -> None:
        manifest = self._synthetic_historical_manifest()
        self.assertEqual(manifest.active_rules, ())
        self.assertEqual({rule.id for rule in manifest.historical_rules}, {"CORE.TEST.900", "CORE.TEST.901"})

    def test_missing_successor_fails(self) -> None:
        manifest = self._synthetic_historical_manifest()
        rules = tuple(
            replace(rule, superseded_by="CORE.TEST.999") if rule.id == "CORE.TEST.901" else rule
            for rule in manifest.rules
        )
        changed = HarnessManifest(manifest.manifest_version, rules, manifest.audit)
        messages = [item.message for item in validate_manifest(changed)]
        self.assertTrue(any("successor does not exist" in message for message in messages))

    def test_supersession_cycle_fails(self) -> None:
        manifest = self._synthetic_historical_manifest()
        rules = tuple(
            replace(rule, lifecycle="superseded", superseded_by="CORE.TEST.901", retirement_reason="fixture")
            if rule.id == "CORE.TEST.900"
            else rule
            for rule in manifest.rules
        )
        changed = HarnessManifest(manifest.manifest_version, rules, manifest.audit)
        messages = [item.message for item in validate_manifest(changed)]
        self.assertTrue(any("cycle" in message for message in messages))

    def test_audit_renders_synthetic_historical_rules(self) -> None:
        manifest = self._synthetic_historical_manifest()
        checks = (AuditResult("tests", ("python",), 0, 0.01, "ok", ""),)
        report = render_report(manifest, (), checks)
        self.assertIn("## Historical Rules", report)
        self.assertIn("CORE.TEST.900", report)
        self.assertIn("CORE.TEST.901", report)


if __name__ == "__main__":
    unittest.main()
