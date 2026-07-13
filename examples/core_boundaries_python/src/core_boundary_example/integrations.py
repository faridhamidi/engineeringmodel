"""The one module that constructs and adapts the external client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class ExternalEffectPort(Protocol):
    def apply(self, *, enabled: bool, operation_id: str) -> None: ...


@dataclass
class VendorClient:
    calls: list[dict[str, object]] = field(default_factory=list)

    def set_enabled(self, *, enabled: bool, operation_id: str) -> None:
        self.calls.append({"enabled": enabled, "operation_id": operation_id})


@dataclass
class VendorAdapter:
    client: VendorClient

    def apply(self, *, enabled: bool, operation_id: str) -> None:
        self.client.set_enabled(enabled=enabled, operation_id=operation_id)


def build_vendor_adapter() -> VendorAdapter:
    return VendorAdapter(client=VendorClient())
