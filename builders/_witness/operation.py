"""Decision oracle for operating at the edge of the revertible envelope."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from line import ABOVE, BELOW, classify

CONTINUE = "continue"
REVIEW = "review"
APPROVAL_REQUIRED = "approval_required"


@dataclass(frozen=True)
class Disposition:
    line: str
    next_step: str


def decide_operation(
    *,
    touches_shared: Optional[bool],
    reversible: Optional[bool],
    external_effect: Optional[bool],
) -> Disposition:
    """Classify authoring risk separately from permission to perform an effect."""
    line = classify(touches_shared, reversible)
    if external_effect is not False:
        return Disposition(line=ABOVE, next_step=APPROVAL_REQUIRED)
    if line == BELOW:
        return Disposition(line=BELOW, next_step=CONTINUE)
    return Disposition(line=ABOVE, next_step=REVIEW)
