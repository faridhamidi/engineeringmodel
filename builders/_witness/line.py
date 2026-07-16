"""Blast-radius line — a decision oracle (executable witness).

This is NOT a runtime tool a builder operates. It is a witness that the
plain-language blast-radius line in ``builders/START_HERE.md`` is precise enough
to be expressed as a deterministic decision over two observable signals, and that
both signals are load-bearing.

Signals:
    touches_shared: does the action change or reach state outside the builder's own
                    workspace that other people or systems rely on?
    reversible:     can the builder undo it themselves in one easy step?

Routing:
    "above" -> stop and think (a real control may be required in the substrate)
    "below" -> build freely (a save point is enough)

Fail-closed: an unknown signal (None) routes "above" — uncertainty routes to caution.
"""
from __future__ import annotations

from typing import Optional

ABOVE = "above"
BELOW = "below"


def classify(touches_shared: Optional[bool], reversible: Optional[bool]) -> str:
    """Route an action below or above the blast-radius line.

    Unknown (None) inputs fail closed to ABOVE.
    """
    if touches_shared is None or reversible is None:
        return ABOVE
    if touches_shared or not reversible:
        return ABOVE
    return BELOW
