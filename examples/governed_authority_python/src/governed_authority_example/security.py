from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    DISCOVERY = "discovery"
    COMMIT = "commit"
    RECONCILER = "reconciler"
    RECOVERY = "recovery"


@dataclass(frozen=True)
class Identity:
    name: str
    role: Role


class AuthorizationError(PermissionError):
    pass


def require_role(identity: Identity, required: Role) -> None:
    if identity.role is not required:
        raise AuthorizationError(
            f"identity {identity.name!r} has role {identity.role.value!r}; "
            f"required {required.value!r}"
        )
