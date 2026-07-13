from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import tempfile
import unittest
from dataclasses import replace

from check_manifest import validate_manifest
from harness import MANIFEST_PATH, load_harness_manifest


class ManifestTests(unittest.TestCase):
    def test_repository_manifest_is_valid(self) -> None:
        manifest = load_harness_manifest()
        self.assertEqual(validate_manifest(manifest), [])

    def test_unknown_rule_field_is_rejected(self) -> None:
        raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        raw["rules"][0]["explanation"] = "must not become rationale"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown fields"):
                load_harness_manifest(path)

    def test_duplicate_rule_ids_are_rejected(self) -> None:
        manifest = load_harness_manifest()
        duplicate = type(manifest)(
            manifest_version=manifest.manifest_version,
            rules=manifest.rules + (manifest.rules[0],),
            audit=manifest.audit,
        )
        messages = [item.message for item in validate_manifest(duplicate)]
        self.assertTrue(any("unique" in message for message in messages))

    def test_flat_rule_id_is_rejected(self) -> None:
        manifest = load_harness_manifest()
        changed_rule = replace(manifest.rules[0], id="CORE001")
        changed = type(manifest)(manifest.manifest_version, (changed_rule, *manifest.rules[1:]), manifest.audit)
        messages = [item.message for item in validate_manifest(changed)]
        self.assertTrue(any("<layer>.<domain>.<number>" in message for message in messages))

    def test_fixture_namespace_is_rejected_in_live_manifest(self) -> None:
        manifest = load_harness_manifest()
        changed_rule = replace(manifest.rules[0], id="FIXTURE.ARCH.001")
        changed = type(manifest)(manifest.manifest_version, (changed_rule, *manifest.rules[1:]), manifest.audit)
        messages = [item.message for item in validate_manifest(changed)]
        self.assertTrue(any("must not use FIXTURE namespace" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
