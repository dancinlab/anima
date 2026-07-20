import unittest

from core.cognitive_workspace import (
    ClaimStatus,
    CognitiveWorkspace,
    CompositionRule,
    Fact,
)


class CognitiveWorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = CompositionRule("power-chain", "generates", "powers", "can_power")
        self.left = Fact("solar_panel", "generates", "electricity", ("sensor:a",))
        self.right = Fact("electricity", "powers", "pump", ("manual:b",))

    def test_g1_composition_requires_both_operands_and_records_provenance(self) -> None:
        workspace = CognitiveWorkspace()
        workspace.add_facts([self.left])
        self.assertEqual(workspace.compose(self.rule), [])

        workspace.add_facts([self.right])
        derived = workspace.compose(self.rule)
        self.assertEqual(len(derived), 1)
        self.assertEqual(derived[0].key, ("solar_panel", "can_power", "pump"))
        self.assertEqual(derived[0].provenance, ("sensor:a", "manual:b", "power-chain"))

    def test_g6_falsifier_blocks_candidate_and_selector_uses_grounded_alternative(self) -> None:
        workspace = CognitiveWorkspace()
        good = Fact("solar_panel", "can_power", "pump", ("power-chain",))
        bad = Fact("battery", "can_power", "pump", ("proposal",))
        depleted = Fact("battery", "has_state", "depleted", ("meter",))
        workspace.add_facts([good, bad, depleted])

        rejected = workspace.propose(bad, [depleted])
        accepted = workspace.propose(
            good, [Fact("solar_panel", "has_state", "disconnected")]
        )

        selected = workspace.select()
        self.assertIs(selected, accepted)
        self.assertEqual(rejected.status, ClaimStatus.FALSIFIED)
        self.assertEqual(rejected.evidence, (depleted,))
        self.assertEqual(workspace.render_for_mouth(), "solar_panel can_power pump")

    def test_ungrounded_claim_cannot_reach_mouth(self) -> None:
        workspace = CognitiveWorkspace()
        workspace.propose(
            Fact("unknown", "cures", "everything"),
            [Fact("trial", "result", "negative")],
        )
        with self.assertRaises(RuntimeError):
            workspace.select()
        with self.assertRaises(RuntimeError):
            workspace.render_for_mouth()

    def test_claim_without_falsifier_is_rejected_at_boundary(self) -> None:
        workspace = CognitiveWorkspace()
        with self.assertRaises(ValueError):
            workspace.propose(Fact("a", "relates", "b"), [])


if __name__ == "__main__":
    unittest.main()

