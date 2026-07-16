"""Generate or verify the minimal share-ready engineering-model seed."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = Path(__file__).with_name("manifest.json")
OUTPUT_MANIFEST = PurePosixPath(".engineering-model/manifest.json")


class SeedError(ValueError):
    """Raised when seed input or output violates the generation contract."""


def _relative_path(value: str) -> Path:
    posix_path = PurePosixPath(value)
    if posix_path.is_absolute() or not posix_path.parts or ".." in posix_path.parts:
        raise SeedError(f"path must remain relative: {value!r}")
    return Path(*posix_path.parts)


def _source_path(repo_root: Path, value: str) -> Path:
    root = repo_root.resolve()
    candidate = (root / _relative_path(value)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise SeedError(f"source escapes repository: {value!r}") from exc
    return candidate


def load_spec(spec_path: Path = SPEC_PATH) -> Mapping[str, Any]:
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SeedError(f"cannot read seed manifest: {exc}") from exc

    required = {
        "format_version",
        "source_repository",
        "files",
        "trees",
        "expected_top_level",
    }
    if not isinstance(spec, dict) or set(spec) != required:
        raise SeedError("seed manifest fields do not match the generation contract")
    if spec["format_version"] != 1:
        raise SeedError("unsupported seed manifest format")
    if not isinstance(spec["source_repository"], str):
        raise SeedError("source_repository must be a string")
    if not isinstance(spec["files"], list) or not isinstance(spec["trees"], list):
        raise SeedError("files and trees must be lists")
    if not isinstance(spec["expected_top_level"], list):
        raise SeedError("expected_top_level must be a list")
    return spec


def source_identity(repo_root: Path = REPO_ROOT) -> tuple[str, str]:
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SeedError("source repository identity is unavailable") from exc
    return revision, "modified" if status else "clean"


def _write_file(source: Path, target: Path) -> None:
    if source.is_symlink():
        raise SeedError(f"seed source must not be a symlink: {source}")
    if not source.is_file():
        raise SeedError(f"seed source file is missing: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source.read_bytes())


def _copy_tree(source: Path, target: Path) -> None:
    if source.is_symlink() or not source.is_dir():
        raise SeedError(f"seed source tree is invalid: {source}")
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise SeedError(f"seed source must not contain symlinks: {path}")
        if path.is_file():
            _write_file(path, target / path.relative_to(source))


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _files_below(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _validate_top_level(output: Path, expected: Sequence[str]) -> None:
    actual = sorted(path.name for path in output.iterdir())
    if actual != sorted(expected):
        raise SeedError(
            "generated top-level paths differ from the manifest: "
            f"expected {sorted(expected)!r}, observed {actual!r}"
        )


def generate_seed(
    output: Path,
    *,
    repo_root: Path = REPO_ROOT,
    spec_path: Path = SPEC_PATH,
    revision: str | None = None,
    source_state: str | None = None,
) -> Path:
    if revision is None or source_state is None:
        detected_revision, detected_state = source_identity(repo_root)
        revision = revision or detected_revision
        source_state = source_state or detected_state
    if source_state not in {"clean", "modified"}:
        raise SeedError("source_state must be clean or modified")

    spec = load_spec(spec_path)
    file_mappings: list[tuple[Path, Path]] = []
    for entry in spec["files"]:
        if not isinstance(entry, dict) or set(entry) != {"source", "target"}:
            raise SeedError("each file mapping needs source and target")
        file_mappings.append(
            (
                _source_path(repo_root, entry["source"]),
                _relative_path(entry["target"]),
            )
        )

    tree_mappings: list[tuple[Path, list[Path]]] = []
    for entry in spec["trees"]:
        if not isinstance(entry, dict) or set(entry) != {"source", "targets"}:
            raise SeedError("each tree mapping needs source and targets")
        if not isinstance(entry["targets"], list):
            raise SeedError("tree targets must be a list")
        tree_mappings.append(
            (
                _source_path(repo_root, entry["source"]),
                [_relative_path(target) for target in entry["targets"]],
            )
        )

    output = output.resolve()
    for source, _targets in tree_mappings:
        try:
            output.relative_to(source)
        except ValueError:
            continue
        raise SeedError(f"output must not be inside a source tree: {source}")
    if output.exists():
        if not output.is_dir() or any(output.iterdir()):
            raise SeedError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    for source, target in file_mappings:
        _write_file(source, output / target)

    for source, targets in tree_mappings:
        for target in targets:
            _copy_tree(source, output / target)

    managed_files = {
        relative: _file_hash(path)
        for relative, path in _files_below(output).items()
    }
    manifest = {
        "format_version": spec["format_version"],
        "source": {
            "repository": spec["source_repository"],
            "revision": revision,
            "state": source_state,
        },
        "runtime_adapters": {
            "claude": {
                "instructions": "CLAUDE.md",
                "skill": ".claude/skills/engineering-model/SKILL.md",
            },
            "codex": {
                "instructions": "AGENTS.md",
                "skill": ".agents/skills/engineering-model/SKILL.md",
            },
        },
        "managed_files": managed_files,
    }
    manifest_path = output / Path(*OUTPUT_MANIFEST.parts)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _validate_top_level(output, spec["expected_top_level"])
    return output


def seed_drift(
    output: Path,
    *,
    repo_root: Path = REPO_ROOT,
    spec_path: Path = SPEC_PATH,
    revision: str | None = None,
    source_state: str | None = None,
) -> dict[str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        expected_root = generate_seed(
            Path(tmp) / "seed",
            repo_root=repo_root,
            spec_path=spec_path,
            revision=revision,
            source_state=source_state,
        )
        expected = _files_below(expected_root)
        actual = _files_below(output)

        drift: dict[str, str] = {}
        for relative in sorted(expected.keys() | actual.keys()):
            if relative not in actual:
                drift[relative] = "missing"
            elif relative not in expected:
                drift[relative] = "unexpected"
            elif expected[relative].read_bytes() != actual[relative].read_bytes():
                drift[relative] = "changed"
        return drift


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--output", type=Path, help="write a new seed directory")
    operation.add_argument("--check", type=Path, help="verify an existing seed directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.output is not None:
            output = generate_seed(args.output)
            print(f"Generated seed: {output}")
            return 0

        drift = seed_drift(args.check)
        if drift:
            for relative, reason in drift.items():
                print(f"{reason}: {relative}")
            return 1
        print(f"Seed matches canonical sources: {args.check.resolve()}")
        return 0
    except SeedError as exc:
        print(f"Seed generation failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
