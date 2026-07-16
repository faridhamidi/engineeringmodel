from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sync_skill_references import (  # noqa: E402
    ENGINE_REFERENCES,
    REFERENCE_ROOT,
    REPO_ROOT,
    SKILL_ROOT,
    reference_drift,
    sync_references,
)

FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_matches_agent_skills_contract(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        self.assertIsNotNone(match)
        fields = {
            key.strip(): value.strip()
            for key, value in (
                line.split(":", 1)
                for line in match.group("body").splitlines()
                if ":" in line
            )
        }
        self.assertEqual(set(fields), {"name", "description"})
        self.assertEqual(fields["name"], SKILL_ROOT.name)
        self.assertRegex(fields["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertGreater(len(fields["description"]), 0)
        self.assertLessEqual(len(fields["description"]), 1024)

    def test_carried_engine_references_match_canonical_sources(self) -> None:
        self.assertEqual(reference_drift(), {})

    def test_skill_uses_one_level_reference_pointers(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in ENGINE_REFERENCES:
            self.assertIn(f"references/{name}", text)

    def test_skill_body_stays_below_progressive_disclosure_limit(self) -> None:
        lines = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 500)

    def test_skill_defines_bounded_commit_protocol(self) -> None:
        text = " ".join(
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").split()
        )
        required = (
            "Inspect `git status` before editing",
            "explicit paths or selective hunks",
            "Do not rewrite existing history automatically",
            "leave the work uncommitted",
            "without reporting the increment as complete",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_skill_quality_claims_require_proportionate_executable_evidence(self) -> None:
        text = " ".join(
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").split()
        )
        required = (
            "inspect how the repository already handles the same concern",
            "unused or misplaced imports",
            "dead parameters or dependencies",
            "unsafe collection access",
            "fragile parsing",
            "fix findings in the same pass or record why a departure is intentional",
            "lightest test that would fail on a realistic defect",
            "cover the intended path",
            "failure, fallback, or guard paths whose outcomes carry material risk",
            "Replace external services with test doubles",
            "existing executable artifact",
            "has run successfully in the current increment",
            "Do not log every function",
            "Record an exception before intentionally swallowing it",
            "failures cannot silently discard or corrupt accepted data",
            "executed test artifact or a recorded reason that no test is proportionate",
            "every named test or check was actually run",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_skill_impact_record_exposes_quality_and_recovery_evidence(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Quality evidence:", text)
        self.assertIn("Recovery:", text)

    def test_skill_reports_when_git_cannot_supply_recovery(self) -> None:
        text = " ".join(
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").split()
        )
        self.assertIn("a checkpoint can be created before relying on git as recovery", text)
        self.assertIn("do not create a shadow repository merely to satisfy the ritual", text)

    def test_codex_interface_metadata_names_the_skill(self) -> None:
        text = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Engineering Model"', text)
        self.assertIn("$engineering-model", text)

    def test_reference_checker_detects_missing_stale_and_extra_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            reference_root = Path(tmp)
            sync_references(repo_root=REPO_ROOT, reference_root=reference_root)
            stale_name = next(iter(ENGINE_REFERENCES))
            (reference_root / stale_name).write_text("stale\n", encoding="utf-8")
            missing_name = list(ENGINE_REFERENCES)[1]
            (reference_root / missing_name).unlink()
            (reference_root / "extra.md").write_text("extra\n", encoding="utf-8")

            drift = reference_drift(
                repo_root=REPO_ROOT,
                reference_root=reference_root,
            )
            self.assertIn(stale_name, drift)
            self.assertIn(missing_name, drift)
            self.assertIn("extra.md", drift)

    def test_no_nested_reference_directories(self) -> None:
        self.assertEqual(
            [path for path in REFERENCE_ROOT.rglob("*") if path.is_dir()],
            [],
        )


if __name__ == "__main__":
    unittest.main()
