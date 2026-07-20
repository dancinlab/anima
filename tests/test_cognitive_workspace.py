import tempfile
import unittest

from core.cognitive_workspace import (
    ClaimStatus,
    CognitiveWorkspace,
    CompositionRule,
    Fact,
)
from core.workspace_adapters import (
    contradiction_evidence,
    ingest_fact_anchors,
    load_fact_anchors,
    selected_grounded_texts,
    write_fact_anchor,
)
from core.engine_cli import immune_embed_key, immune_grow_new
from core.workspace_smoke import run_smoke


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

    def test_kosmos_roundtrip_feeds_composition_and_selected_decode_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            write_fact_anchor(directory, "left", self.left)
            write_fact_anchor(directory, "right", self.right)
            facts = load_fact_anchors(directory)
            self.assertEqual(len(facts), 2)

            workspace = CognitiveWorkspace()
            ingest_fact_anchors(workspace, directory)
            derived = workspace.compose(self.rule)[0]
            claim = workspace.propose(
                derived, [Fact("solar_panel", "has_state", "disconnected")]
            )
            self.assertIs(workspace.select(), claim)
            self.assertEqual(selected_grounded_texts(workspace), ["solar_panel can_power pump"])

    def test_plain_kosmos_anchor_is_not_reinterpreted_as_a_fact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            from core.kosmos_io import create_anchor

            create_anchor(
                directory, "memory", "plain memory", 0.0, 0.0, "memory", 1.0,
                2, "memory", "none", "a resembles b", [0.0] * 5, "seed", "",
            )
            self.assertEqual(load_fact_anchors(directory), [])

    def test_live_affect_comparator_becomes_falsifier_only_when_grounded(self) -> None:
        key = immune_embed_key("battery-state")
        memory = immune_grow_new(key, "depleted", 2, 2, "fixed")
        evidence = contradiction_evidence(memory, key, "charged", "battery-claim")
        self.assertEqual(evidence.key, ("battery-claim", "has_verdict", "contradicted"))
        self.assertIsNone(contradiction_evidence(memory, key, "depleted", "battery-claim"))
        self.assertIsNone(
            contradiction_evidence(
                memory, immune_embed_key("unrelated-referent"), "charged", "battery-claim"
            )
        )

    def test_integrated_smoke_has_live_and_collapse_controls(self) -> None:
        report = run_smoke()
        self.assertTrue(report["ok"], report)
        self.assertEqual(len(report["checks"]), 10)


if __name__ == "__main__":
    unittest.main()
