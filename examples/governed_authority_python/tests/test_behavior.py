from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from governed_authority_example.commit import CommitAuthority, ValidationError
from governed_authority_example.external import ManagedResource
from governed_authority_example.model import CanonicalDecision, Proposal
from governed_authority_example.reconciler import Reconciler
from governed_authority_example.recovery import Recovery
from governed_authority_example.security import AuthorizationError, Identity, Role
from governed_authority_example.store import CanonicalStore


COMMIT_ID = Identity("commit-service", Role.COMMIT)
RECONCILER_ID = Identity("reconciler-service", Role.RECONCILER)
RECOVERY_ID = Identity("recovery-service", Role.RECOVERY)


class GovernedAuthorityBehaviorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = CanonicalStore()
        self.resource = ManagedResource()
        self.committer = CommitAuthority(self.store, COMMIT_ID)
        self.reconciler = Reconciler(self.store, self.resource, RECONCILER_ID)
        self.recovery = Recovery(self.reconciler, RECOVERY_ID)

    def test_proposal_has_no_external_effect(self) -> None:
        proposal = Proposal("case-1", True, True, True)
        self.assertTrue(proposal.requested_enabled)
        self.assertEqual(self.store.records, {})
        self.assertEqual(self.resource.states, {})

    def test_stale_evidence_fails_closed_before_canonical_write(self) -> None:
        proposal = Proposal("case-2", True, True, False)
        with self.assertRaisesRegex(ValidationError, "stale evidence"):
            self.committer.commit(proposal)
        self.assertEqual(self.store.records, {})
        self.assertEqual(self.resource.states, {})

    def test_commit_and_execute_are_separate(self) -> None:
        self.committer.commit(Proposal("case-3", True, True, True))
        self.assertIn("case-3", self.store.records)
        self.assertNotIn("case-3", self.resource.states)

        effective = self.reconciler.reconcile("case-3")
        self.assertTrue(effective.enabled)
        self.assertEqual(self.resource.states["case-3"], True)

    def test_reconciliation_is_idempotent(self) -> None:
        self.committer.commit(Proposal("case-4", True, True, True))
        self.reconciler.reconcile("case-4")
        self.reconciler.reconcile("case-4")
        self.assertEqual(self.resource.mutation_count, 1)

    def test_runtime_roles_prevent_impersonation(self) -> None:
        decision = CanonicalDecision("case-5", True, True, True, version=1)
        with self.assertRaises(AuthorizationError):
            self.store.write_canonical(decision, identity=RECOVERY_ID)
        with self.assertRaises(AuthorizationError):
            self.resource.mutate_managed_resource(
                "case-5",
                enabled=True,
                identity=COMMIT_ID,
            )

    def test_recovery_reenters_execution_without_stronger_identity(self) -> None:
        self.committer.commit(Proposal("case-6", True, True, True))
        effective = self.recovery.retry_committed("case-6")
        self.assertTrue(effective.enabled)
        self.assertEqual(self.resource.states["case-6"], True)


if __name__ == "__main__":
    unittest.main()
