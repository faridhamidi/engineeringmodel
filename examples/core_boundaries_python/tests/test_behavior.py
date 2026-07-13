from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from core_boundary_example.integrations import VendorClient, VendorAdapter
from core_boundary_example.service import EnablementService


class CoreBoundaryBehaviorTests(unittest.TestCase):
    def test_stale_evidence_fails_closed_without_external_call(self) -> None:
        client = VendorClient()
        service = EnablementService(effect_port=VendorAdapter(client))

        result = service.run(
            requested=True,
            evidence_fresh=False,
            operation_id="op-stale",
        )

        self.assertFalse(result.should_apply)
        self.assertEqual(result.reason, "stale_evidence")
        self.assertEqual(client.calls, [])

    def test_operation_context_reaches_external_effect(self) -> None:
        client = VendorClient()
        service = EnablementService(effect_port=VendorAdapter(client))

        result = service.run(
            requested=True,
            evidence_fresh=True,
            operation_id="op-123",
        )

        self.assertTrue(result.should_apply)
        self.assertEqual(client.calls, [{"enabled": True, "operation_id": "op-123"}])


if __name__ == "__main__":
    unittest.main()
