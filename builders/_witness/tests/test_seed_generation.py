from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from seed.generate import (  # noqa: E402
    SeedError,
    generate_seed,
    seed_drift,
    source_identity,
    verify_seed,
)

SKILL_ROOT = REPO_ROOT / "skills" / "engineering-model"
REVISION = "test-source-revision"
SOURCE_STATE = "clean"
EXPECTED_TOP_LEVEL = {
    ".agents",
    ".claude",
    ".engineering-model",
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
}
SOURCE_ONLY_ROOTS = {
    ".github",
    ".meta",
    "builders",
    "case-studies",
    "core",
    "examples",
    "governed-automation",
    "seed",
    "skills",
}


def files_below(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class SeedGenerationTests(unittest.TestCase):
    def generate(self, root: Path) -> Path:
        return generate_seed(
            root,
            revision=REVISION,
            source_state=SOURCE_STATE,
        )

    def test_generated_seed_has_only_the_minimal_top_level_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            self.assertEqual({path.name for path in output.iterdir()}, EXPECTED_TOP_LEVEL)
            self.assertEqual(
                {path.name for path in output.iterdir()} & SOURCE_ONLY_ROOTS,
                set(),
            )

    def test_both_runtime_skill_adapters_match_the_canonical_package(self) -> None:
        canonical = files_below(SKILL_ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            adapters = (
                output / ".agents" / "skills" / "engineering-model",
                output / ".claude" / "skills" / "engineering-model",
            )
            for adapter in adapters:
                with self.subTest(adapter=adapter):
                    self.assertEqual(files_below(adapter), canonical)

    def test_native_steering_files_match_packaged_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            for filename in ("AGENTS.md", "CLAUDE.md"):
                with self.subTest(filename=filename):
                    expected = SKILL_ROOT / "assets" / filename
                    self.assertEqual((output / filename).read_bytes(), expected.read_bytes())

    def test_output_manifest_hashes_every_managed_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            manifest_path = output / ".engineering-model" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            actual = files_below(output)
            actual.pop(".engineering-model/manifest.json")
            expected_hashes = {
                relative: hashlib.sha256(content).hexdigest()
                for relative, content in actual.items()
            }
            self.assertEqual(manifest["managed_files"], expected_hashes)
            self.assertEqual(manifest["source"]["revision"], REVISION)
            self.assertEqual(manifest["source"]["state"], SOURCE_STATE)

    def test_generation_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = self.generate(Path(tmp) / "first")
            second = self.generate(Path(tmp) / "second")
            self.assertEqual(files_below(first), files_below(second))

    def test_drift_check_detects_missing_changed_and_unexpected_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            (output / "AGENTS.md").write_text("changed\n", encoding="utf-8")
            (output / "CLAUDE.md").unlink()
            (output / "unexpected.txt").write_text("extra\n", encoding="utf-8")
            drift = seed_drift(
                output,
                revision=REVISION,
                source_state=SOURCE_STATE,
            )
            self.assertEqual(drift["AGENTS.md"], "changed")
            self.assertEqual(drift["CLAUDE.md"], "missing")
            self.assertEqual(drift["unexpected.txt"], "unexpected")

    def test_manifest_verification_is_independent_of_the_source_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            with patch(
                "seed.generate.source_identity",
                side_effect=AssertionError("verification must not inspect git"),
            ):
                self.assertEqual(verify_seed(output), {})

    def test_manifest_verification_detects_managed_and_unexpected_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            (output / "AGENTS.md").write_text("changed\n", encoding="utf-8")
            (output / "CLAUDE.md").unlink()
            (output / "unexpected.txt").write_text("extra\n", encoding="utf-8")
            drift = verify_seed(output)
            self.assertEqual(drift["AGENTS.md"], "changed")
            self.assertEqual(drift["CLAUDE.md"], "missing")
            self.assertEqual(drift["unexpected.txt"], "unexpected")

    def test_manifest_verification_rejects_an_invalid_digest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            manifest_path = output / ".engineering-model" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["managed_files"]["AGENTS.md"] = "not-a-sha256-digest"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(SeedError, "digest is invalid"):
                verify_seed(output)

    def test_canonical_check_treats_a_different_source_revision_as_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            drift = seed_drift(
                output,
                revision="new-source-revision",
                source_state=SOURCE_STATE,
            )
            self.assertEqual(
                drift,
                {".engineering-model/manifest.json": "changed"},
            )

    def test_source_identity_reports_clean_and_modified_worktrees(self) -> None:
        repo_root = Path("/example/repo")
        for status, expected_state in (("", "clean"), (" M seed/generate.py\n", "modified")):
            with self.subTest(expected_state=expected_state):
                completed = (
                    subprocess.CompletedProcess([], 0, stdout="abc123\n", stderr=""),
                    subprocess.CompletedProcess([], 0, stdout=status, stderr=""),
                )
                with patch("seed.generate.subprocess.run", side_effect=completed) as run:
                    self.assertEqual(source_identity(repo_root), ("abc123", expected_state))
                self.assertEqual(run.call_count, 2)
                self.assertEqual(run.call_args_list[0].args[0], ["git", "rev-parse", "HEAD"])
                self.assertEqual(
                    run.call_args_list[1].args[0],
                    ["git", "status", "--porcelain", "--untracked-files=all"],
                )
                self.assertEqual(run.call_args_list[0].kwargs["cwd"], repo_root)

    def test_source_identity_wraps_git_execution_failures(self) -> None:
        failures = (
            FileNotFoundError("git"),
            subprocess.CalledProcessError(1, ["git", "rev-parse", "HEAD"]),
        )
        for failure in failures:
            with self.subTest(failure=type(failure).__name__):
                with patch("seed.generate.subprocess.run", side_effect=failure):
                    with self.assertRaisesRegex(SeedError, "identity is unavailable"):
                        source_identity(Path("/example/repo"))

    def test_generation_refuses_a_nonempty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "seed"
            output.mkdir()
            (output / "user-work.txt").write_text("keep\n", encoding="utf-8")
            with self.assertRaisesRegex(SeedError, "not empty"):
                self.generate(output)
            self.assertEqual((output / "user-work.txt").read_text(), "keep\n")

    def test_generation_refuses_output_inside_a_canonical_source_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / "repo"
            source = repo_root / "package"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("skill\n", encoding="utf-8")
            spec = {
                "format_version": 1,
                "source_repository": "https://example.invalid/source",
                "files": [],
                "trees": [{"source": "package", "targets": ["installed"]}],
                "expected_top_level": [".engineering-model", "installed"],
            }
            spec_path = repo_root / "manifest.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            output = source / "generated"
            with self.assertRaisesRegex(SeedError, "inside a source tree"):
                generate_seed(
                    output,
                    repo_root=repo_root,
                    spec_path=spec_path,
                    revision=REVISION,
                    source_state=SOURCE_STATE,
                )
            self.assertFalse(output.exists())

    def test_generation_rejects_projection_junk_in_a_source_tree(self) -> None:
        junk_paths = (".DS_Store", ".git/config", "__pycache__/module.pyc")
        for junk_path in junk_paths:
            with self.subTest(junk_path=junk_path), tempfile.TemporaryDirectory() as tmp:
                repo_root = Path(tmp) / "repo"
                source = repo_root / "package"
                source.mkdir(parents=True)
                (source / "SKILL.md").write_text("skill\n", encoding="utf-8")
                junk = source / junk_path
                junk.parent.mkdir(parents=True, exist_ok=True)
                junk.write_text("junk\n", encoding="utf-8")
                spec = {
                    "format_version": 1,
                    "source_repository": "https://example.invalid/source",
                    "files": [],
                    "trees": [{"source": "package", "targets": ["installed"]}],
                    "expected_top_level": [".engineering-model", "installed"],
                }
                spec_path = repo_root / "manifest.json"
                spec_path.write_text(json.dumps(spec), encoding="utf-8")
                with self.assertRaisesRegex(SeedError, "projection junk"):
                    generate_seed(
                        Path(tmp) / "output",
                        repo_root=repo_root,
                        spec_path=spec_path,
                        revision=REVISION,
                        source_state=SOURCE_STATE,
                    )

    def test_generated_readme_does_not_turn_the_seed_into_methodology_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = self.generate(Path(tmp) / "seed")
            readme = (output / "README.md").read_text(encoding="utf-8").lower()
            self.assertNotIn("engineering model", readme)
            self.assertNotIn("governed automation", readme)
            self.assertNotIn("methodology", readme)


if __name__ == "__main__":
    unittest.main()
