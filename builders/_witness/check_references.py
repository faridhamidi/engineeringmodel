"""Reference-integrity checker for the builder translation surface.

Walk-the-talk ratchet. The builder surface must *link* to the engine, never restate
it (canonical concept ownership). This checker enumerates the repo-relative links in
a builder document and reports any that do not resolve to a real file.

The known-violation set is empty: this is a zero-violation rule. Any broken engine
link is a defect. Web links and pure section anchors are ignored.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def referenced_paths(doc_path: Path) -> List[Path]:
    """Return resolved repo-relative link targets in a markdown document."""
    text = doc_path.read_text(encoding="utf-8")
    base = doc_path.parent
    targets: List[Path] = []
    for raw in _LINK_RE.findall(text):
        link = raw.strip()
        if link.startswith(_SKIP_PREFIXES):
            continue
        link = link.split("#", 1)[0]  # drop any section anchor
        if not link:
            continue
        targets.append((base / link).resolve())
    return targets


def unresolved_references(doc_path: Path) -> List[Path]:
    """Return the link targets that do not resolve to an existing file."""
    return [p for p in referenced_paths(doc_path) if not p.exists()]
