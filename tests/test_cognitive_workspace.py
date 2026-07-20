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
    falsifier_fact,
    support_fact,
    write_fact_anchor,
    write_falsifier_anchor,
)
from core.engine_cli import immune_embed_key, immune_grow_new
from core.workspace_smoke import run_smoke
from core.workspace_mouth import TypedWorkspaceMouth, claim_ids, compose_seed, decide_seed
from core.workspace_semantic import run_semantic_certification
from core.rho_fan import (
    _rho_fan_dict_load,
    _rho_fan_is_falsifiable,
    _rho_fan_known_word_ratio,
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

    def test_workspace_mouth_is_generic_and_atomic_prompts_are_unchanged(self) -> None:
        class StubMouth:
            def __init__(self):
                self.calls = []

            def ideate(self, seed, gen, top_k, temp, seed_rng):
                self.calls.append(seed)
                return "base-output"

        stub = StubMouth()
        mouth = TypedWorkspaceMouth(stub)
        self.assertEqual(mouth.ideate("one clause: ", 40, 40, 0.7, 7), "base-output")
        self.assertEqual(stub.calls, ["one clause: "])
        text = mouth.ideate("if copper conducts heat, then water drives turbines: ", 40, 40, 0.7, 8)
        self.assertIn("copper", text)
        self.assertIn("turbines", text)
        self.assertTrue(any(word in text for word in ("score", "rate", "frequency", "strength", "level", "ratio")))

    def test_model_realizer_is_accepted_only_when_semantics_survive(self) -> None:
        class PreservingMouth:
            def ideate(self, *args):
                return "copper heat predicts water turbines score"

        class DroppingMouth:
            def ideate(self, *args):
                return "This is an interesting possibility."

        seed = "if copper conducts heat, then water drives turbines: "
        good = TypedWorkspaceMouth(PreservingMouth(), realizer="model")
        bad = TypedWorkspaceMouth(DroppingMouth(), realizer="model")
        self.assertEqual(good.ideate(seed, 40, 40, 0.7, 7),
                         "copper heat predicts water turbines score")
        fallback = bad.ideate(seed, 40, 40, 0.7, 7)
        self.assertIn("copper", fallback)
        self.assertEqual(good.decisions[0].realized_by, "model")
        self.assertEqual(bad.decisions[0].realized_by, "workspace_fallback")
        self.assertFalse(bad.decisions[0].realizer_valid)

    def test_workspace_composition_is_coherent_and_explicitly_falsifiable(self) -> None:
        text = compose_seed(
            "if memory composes into new meaning, then silence still carries information: "
        )
        known = _rho_fan_dict_load()
        self.assertGreaterEqual(_rho_fan_known_word_ratio(text, known), 0.5)
        self.assertTrue(_rho_fan_is_falsifiable(text, known))

    def test_multiclause_composition_accumulates_every_operand(self) -> None:
        text = compose_seed("alpha cells. beta tension. gamma memory. delta silence. epsilon dream. ")
        for operand in ("cells", "tension", "memory", "silence", "dream"):
            self.assertIn(operand, text)

    def test_production_decision_rejects_primary_and_selects_alternative(self) -> None:
        seed = "if copper conducts heat, then water drives turbines: "
        primary_id, alternative_id = claim_ids(seed)
        off = decide_seed(seed)
        on = decide_seed(seed, [falsifier_fact(primary_id, "meter")])
        shuffled = decide_seed(seed, [falsifier_fact(alternative_id + "-shuffle", "meter")])

        self.assertEqual(off.selected_claim_id, primary_id)
        self.assertEqual(on.selected_claim_id, alternative_id)
        self.assertEqual(on.rejected_claim_ids, (primary_id,))
        self.assertNotEqual(on.text, off.text)
        self.assertEqual(shuffled.text, off.text)

    def test_all_candidates_falsified_abstains(self) -> None:
        seed = "if copper conducts heat, then water drives turbines: "
        ids = claim_ids(seed)
        decision = decide_seed(seed, [falsifier_fact(x, "meter") for x in ids])
        self.assertTrue(decision.abstained)
        self.assertIsNone(decision.selected_claim_id)
        self.assertEqual(decision.rejected_claim_ids, ids)
        self.assertEqual(decision.text, "insufficient grounded evidence")

    def test_strict_grounding_holds_without_evidence_and_exposes_g6_spec(self) -> None:
        seed = "if copper conducts heat, then water drives turbines: "
        ids = claim_ids(seed)
        held = decide_seed(seed, require_evidence=True)
        supported = decide_seed(seed, [support_fact(ids[0], "meter")], require_evidence=True)
        contradicted = decide_seed(seed, [falsifier_fact(ids[0], "meter")], require_evidence=True)

        self.assertTrue(held.abstained)
        self.assertEqual(supported.selected_claim_id, ids[0])
        self.assertEqual(contradicted.selected_claim_id, ids[1])
        spec = supported.candidate_specs[0]
        self.assertTrue(spec.measure)
        self.assertEqual(spec.control, "each_operand_alone")
        self.assertEqual(spec.falsified_when, "interaction_not_above_control")

    def test_kosmos_falsifier_changes_live_mouth_selection(self) -> None:
        seed = "if copper conducts heat, then water drives turbines: "
        with tempfile.TemporaryDirectory() as directory:
            write_falsifier_anchor(directory, "reject_primary", claim_ids(seed)[0], "lab")
            evidence = load_fact_anchors(directory)
            mouth = TypedWorkspaceMouth(None, evidence)
            text = mouth.ideate(seed, 40, 40, 0.7, 7)
            self.assertIn("decreases", text)
            self.assertEqual(mouth.decisions[0].rejected_claim_ids, (claim_ids(seed)[0],))

    def test_heldout_semantic_certification(self) -> None:
        report = run_semantic_certification()
        self.assertTrue(report["ok"], report)
        self.assertEqual(len(report["cases"]), 11)


if __name__ == "__main__":
    unittest.main()
