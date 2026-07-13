from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tempfile
import unittest
from check_manifest import validate_manifest
from harness import load_harness_manifest


class OwnershipBindingTests(unittest.TestCase):
    def test_repository_binding_matches(self) -> None:
        self.assertEqual(validate_manifest(load_harness_manifest()), [])

    def test_missing_manifest_coverage_fails(self) -> None:
        manifest = load_harness_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CODEOWNERS"
            path.write_text("/unrelated @faridhamidi\n", encoding="utf-8")
            messages = [item.message for item in validate_manifest(manifest, codeowners_path=path)]
            self.assertTrue(any("does not cover" in message for message in messages))

    def test_incompatible_owner_fails(self) -> None:
        manifest = load_harness_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "CODEOWNERS"
            source = (Path(__file__).resolve().parents[3] / ".github" / "CODEOWNERS").read_text(encoding="utf-8")
            path.write_text(source.replace("@faridhamidi", "@different-owner"), encoding="utf-8")
            messages = [item.message for item in validate_manifest(manifest, codeowners_path=path)]
            self.assertTrue(any("do not match" in message or "incompatible" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
