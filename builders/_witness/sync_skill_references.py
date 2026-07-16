"""Build or check the installable skill's carried engine references."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Mapping

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "skills" / "engineering-model"
REFERENCE_ROOT = SKILL_ROOT / "references"

ENGINE_REFERENCES: Mapping[str, str] = {
    "core-readme.md": "core/README.md",
    "core-foundation.md": "core/FOUNDATION.md",
    "core-semantic-consistency.md": "core/SEMANTIC_CONSISTENCY.md",
    "core-testing.md": "core/TESTING.md",
    "core-documentation.md": "core/DOCUMENTATION.md",
    "core-conformance-harness.md": "core/CONFORMANCE_HARNESS.md",
    "governed-readme.md": "governed-automation/README.md",
    "governed-adoption-check.md": "governed-automation/ADOPTION_CHECK.md",
    "governed-decision-tree.md": "governed-automation/DECISION_TREE.md",
    "governed-models.md": "governed-automation/MODELS.md",
    "governed-principles.md": "governed-automation/PRINCIPLES.md",
    "governed-vocabulary.md": "governed-automation/VOCABULARY.md",
    "governed-automated-authority.md": "governed-automation/AUTOMATED_AUTHORITY.md",
}


def reference_drift(
    *,
    repo_root: Path = REPO_ROOT,
    reference_root: Path = REFERENCE_ROOT,
) -> dict[str, str]:
    drift: dict[str, str] = {}
    expected = set(ENGINE_REFERENCES)
    observed = {path.name for path in reference_root.glob("*.md")}

    for extra in sorted(observed - expected):
        drift[extra] = "unexpected generated reference"
    for name, source_name in ENGINE_REFERENCES.items():
        source = repo_root / source_name
        target = reference_root / name
        if not target.exists():
            drift[name] = "missing generated reference"
        elif target.read_bytes() != source.read_bytes():
            drift[name] = f"differs from {source_name}"
    return drift


def sync_references(
    *,
    repo_root: Path = REPO_ROOT,
    reference_root: Path = REFERENCE_ROOT,
) -> None:
    reference_root.mkdir(parents=True, exist_ok=True)
    expected = set(ENGINE_REFERENCES)
    for path in reference_root.glob("*.md"):
        if path.name not in expected:
            path.unlink()
    for name, source_name in ENGINE_REFERENCES.items():
        (reference_root / name).write_bytes((repo_root / source_name).read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift without updating generated references",
    )
    args = parser.parse_args()

    if args.check:
        drift = reference_drift()
        for name, detail in sorted(drift.items()):
            print(f"[skill-reference] {name}: {detail}")
        return 1 if drift else 0

    sync_references()
    print(f"[skill-reference] synchronized {len(ENGINE_REFERENCES)} references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
