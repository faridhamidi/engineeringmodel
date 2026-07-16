"""Structural contract for the packaged always-on steering block."""
from __future__ import annotations

from typing import Mapping

REQUIRED_NORMS: Mapping[str, str] = {
    "start_marker": "<!-- engineering-model-steering:start -->",
    "end_marker": "<!-- engineering-model-steering:end -->",
    "fail_closed": "fail closed",
    "skill_invocation": "$engineering-model",
    "skill_install_fallback": "install the packaged skill before continuing",
    "git_checkpoint_boundary": "coherent, verified task boundaries",
    "git_checkpoint_scope": "only task-owned changes",
    "git_checkpoint_isolation": "leave the work uncommitted and report why",
    "external_effect": "external-substrate effect",
    "human_approval": "explicit human approval",
    "git_limit": "cannot undo an external effect",
}


def missing_norms(text: str) -> set[str]:
    lowered = text.lower()
    return {
        name
        for name, phrase in REQUIRED_NORMS.items()
        if phrase.lower() not in lowered
    }


def extract_steering_block(text: str) -> str:
    start = REQUIRED_NORMS["start_marker"]
    end = REQUIRED_NORMS["end_marker"]
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError("steering markers must appear exactly once")
    start_index = text.find(start)
    end_index = text.find(end)
    if start_index < 0 or end_index < start_index:
        raise ValueError("steering markers are missing or out of order")
    return text[start_index : end_index + len(end)] + "\n"
