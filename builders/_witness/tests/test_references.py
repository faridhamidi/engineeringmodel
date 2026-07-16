from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_references import referenced_paths, unresolved_references  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
START_HERE = REPO_ROOT / "builders" / "START_HERE.md"


class ReferenceIntegrityTests(unittest.TestCase):
    def test_start_here_exists(self) -> None:
        self.assertTrue(START_HERE.exists(), f"missing {START_HERE}")

    def test_all_engine_references_resolve(self) -> None:
        # Zero-violation ratchet: no broken repo-relative links are allowed.
        self.assertEqual(unresolved_references(START_HERE), [])

    def test_surface_actually_links_to_engine(self) -> None:
        # Canonical ownership: the surface must point at the engine, so it must
        # contain at least one resolvable link into core/ or governed-automation/.
        targets = referenced_paths(START_HERE)
        engine = [
            p
            for p in targets
            if p.exists()
            and ("/core/" in p.as_posix() or "/governed-automation/" in p.as_posix())
        ]
        self.assertTrue(engine, "START_HERE must link into the engine layers")

    def test_checker_detects_a_missing_reference(self) -> None:
        # Known-bad: a link to a nonexistent file must be reported.
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "doc.md"
            doc.write_text("See [x](./does_not_exist.md)\n", encoding="utf-8")
            self.assertEqual(len(unresolved_references(doc)), 1)


if __name__ == "__main__":
    unittest.main()
