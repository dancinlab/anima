import hashlib
import tempfile
import unittest
from unittest import mock

from core.cognitive_workspace import (
    ClaimStatus,
    ConjunctiveRule,
    CognitiveWorkspace,
    CompositionRule,
    Fact,
    ProofStep,
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
from core.workspace_mouth import (
    TypedWorkspaceMouth, certify_divergence, claim_ids, compose_seed, decide_seed,
    divergence_preserves, diverge_seed, realization_surface_quality, realization_training_rows, realize_divergence,
    select_divergence,
)
from core.workspace_runtime import (
    EvidenceLedger, EvidenceRecord, Measurement, TypedFactStore,
    auto_workspace_mode, collect_measurement_evidence, grounded_answer,
    grounded_query_step, identity_control, parse_persistable_fact, persist_workspace_fact,
    measurement_falsification_step, persist_measurement_evidence,
    resolve_evidence_verdicts,
    resolve_workspace_input, spoken_divergence_step,
    spoken_workspace_step,
)
from core.workspace_semantic import realizer_adversarial_panel, realizer_heldout_panel, run_semantic_certification
from core.workspace_longrun import run_workspace_longrun
from core.workspace_deep import run_workspace_deep_certification
from core.workspace_deeper import run_workspace_deeper_certification
from core.workspace_production_cert import run_workspace_production_certification
from core.workspace_regression import run_workspace_regression
from core.workspace_system_rho import run_workspace_system_rho, store_report_passes
from core.workspace_release_verify import verify_workspace_release
from core.rho_fan import (
    _rho_fan_dict_load,
    _rho_fan_is_falsifiable,
    _rho_fan_known_word_ratio,
)


def _valid_realizer_evidence(ckpt_sha="b" * 64):
    cases = []
    for name, seed in realizer_heldout_panel():
        cases.append({
            "name": name, "seed": seed,
            "results": [
                {"lens": hypothesis.lens, "text": hypothesis.text, "valid": True,
                 "realized_by": "model_rerank", "candidate_count": 3}
                for hypothesis in diverge_seed(seed)
            ],
        })
    return {
        "schema": "anima.workspace-divergence-realizer/v1", "panel": "heldout",
        "ckpt_sha256": ckpt_sha, "safe": True, "hypotheses": 36,
        "model_semantic_accept": 36, "fallback": 0,
        "meaning_locked_candidates": 108, "meaning_locked_candidate_total": 108,
        "cases": cases,
    }


class CognitiveWorkspaceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = CompositionRule("power-chain", "generates", "powers", "can_power")
        self.left = Fact("solar_panel", "generates", "electricity", ("sensor:a",))
        self.right = Fact("electricity", "powers", "pump", ("manual:b",))

    def test_explicit_fact_declaration_persists_across_sessions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = persist_workspace_fact(td, "FACT pump | powered_by | solar panel", "session-a")
            self.assertIsNotNone(path)
            session_b = TypedFactStore.load(td)
            self.assertEqual(grounded_answer(session_b, "pump", "powered_by"), "solar panel")
            self.assertEqual(grounded_answer(session_b, "solar panel", "powered_by"), "UNGROUNDED")
            self.assertIsNone(persist_workspace_fact(td, "pump is powered by solar", "session-a"))

    def test_fact_declaration_parser_fails_closed(self) -> None:
        fact = parse_persistable_fact("FACT 온도 | exceeds | 기준값")
        self.assertEqual(fact.key, ("온도", "exceeds", "기준값"))
        for malformed in ("", "FACT only two | fields", "FACT a | b | c | d", "ordinary prose"):
            self.assertIsNone(parse_persistable_fact(malformed))

    def test_adversarial_realizer_panel_preserves_all_semantic_slots(self) -> None:
        for name, seed in realizer_adversarial_panel():
            report = certify_divergence(seed)
            self.assertTrue(report["ok"], name)
            for hypothesis in report["hypotheses"]:
                for candidate in __import__(
                        "core.workspace_mouth", fromlist=["divergence_realization_candidates"]
                ).divergence_realization_candidates(hypothesis):
                    self.assertTrue(divergence_preserves(hypothesis, candidate), name)
                    self.assertTrue(realization_surface_quality(candidate), name)

    def test_workspace_longrun_100_and_500_ticks(self) -> None:
        for ticks in (100, 500):
            report = run_workspace_longrun(ticks)
            self.assertTrue(report["ok"], report)
            self.assertEqual(report["ticks"], ticks)

    def test_g1_g6_deep_certification(self) -> None:
        report = run_workspace_deep_certification()
        self.assertTrue(report["ok"], report)
        self.assertEqual([row["case"] for row in report["g1"]["cases"]],
                         ["chain_6", "chain_8", "chain_10", "branch_merge",
                          "cycle", "typed_homonym"])

    def test_g1_g6_deeper_certification(self) -> None:
        report = run_workspace_deeper_certification()
        self.assertTrue(report["ok"], report)
        self.assertEqual([row["case"] for row in report["g1"]["cases"]], [
            "necessary_sufficient", "conjunction", "inclusive_or", "exclusive_or", "exception",
            "quantifier", "negation_scope", "temporal_order", "proof_object",
        ])

    def test_workspace_production_certification(self) -> None:
        report = run_workspace_production_certification()
        self.assertTrue(report["ok"], report)
        self.assertEqual(set(report["groups"]), {"logic", "evidence", "durability", "active"})

    def test_proof_object_replays_and_detects_rule_tampering(self) -> None:
        workspace = CognitiveWorkspace()
        workspace.add_facts([self.left, self.right])
        target = workspace.compose(self.rule)[0]
        proof = workspace.proof_for(target)
        self.assertEqual([step.rule_name for step in proof],
                         ["axiom", "axiom", "power-chain"])
        self.assertTrue(workspace.verify_proof(target))
        step = workspace.proofs[target.key]
        workspace.proofs[target.key] = ProofStep(step.conclusion, "wrong-rule", step.premises)
        self.assertFalse(workspace.verify_proof(target))

    def test_evidence_ledger_quality_conflict_and_latest_controls(self) -> None:
        seed = "if catalyst increases yield, then reactor reduces waste"
        claim_id = claim_ids(seed)[0]

        def record(name, verdict, source, hour, sample_size=100):
            return EvidenceRecord(
                name, claim_id, verdict, source,
                "2026-07-21T%02d:00:00Z" % hour, name, "reactor-v1",
                sample_size, .05,
            )

        weak = EvidenceLedger([record("weak", "supported", "lab-a", 1, 5)])
        self.assertEqual(weak.resolve(claim_id).status, "INCONCLUSIVE")
        tied = EvidenceLedger([
            record("tie-a", "supported", "lab-a", 1),
            record("tie-b", "contradicted", "lab-b", 2),
        ])
        self.assertEqual(tied.resolve(claim_id).reason, "tied_cross_experiment_conflict")
        majority = EvidenceLedger([
            record("old-a", "contradicted", "lab-a", 1),
            record("old-b", "contradicted", "lab-b", 2),
            record("latest", "supported", "lab-c", 23),
        ])
        self.assertEqual(majority.resolve(claim_id).status, "contradicted")
        self.assertEqual(majority.resolve(claim_id).reason, "replicated_majority")
        with self.assertRaises(ValueError):
            EvidenceRecord(
                "bad", claim_id, "supported", "lab", "2026-07-21T01:00:00Z",
                "bad-exp", sample_size=100, uncertainty=.05, control_valid="false",
            )

    def test_conjunctive_merge_requires_both_typed_relations(self) -> None:
        workspace = CognitiveWorkspace()
        workspace.add_facts([
            Fact("left", "enables", "hub", ("left-source",)),
            Fact("right", "permits", "hub", ("right-source",)),
        ])
        made = workspace.compose(ConjunctiveRule(
            "join", "enables", "permits", "jointly_enables"))
        self.assertEqual(made[0].key, ("left & right", "jointly_enables", "hub"))
        missing = CognitiveWorkspace()
        missing.add_facts([Fact("left", "enables", "hub")])
        self.assertEqual(missing.compose(ConjunctiveRule(
            "join", "enables", "permits", "jointly_enables")), [])

    def test_support_contradiction_conflict_always_abstains(self) -> None:
        seed = "if catalyst increases yield, then reactor reduces waste"
        claim_id = claim_ids(seed)[0]
        evidence = [support_fact(claim_id, "lab-a"), falsifier_fact(claim_id, "lab-b")]
        decision = decide_seed(seed, evidence, require_evidence=False)
        fan_id = diverge_seed(seed)[0].spec.claim_id
        fan_evidence = [support_fact(fan_id, "lab-a"), falsifier_fact(fan_id, "lab-b")]
        divergent = select_divergence(seed, fan_evidence, require_evidence=False)
        self.assertTrue(decision.abstained)
        self.assertEqual(decision.rejected_claim_ids, ())
        self.assertTrue(divergent.abstained)
        self.assertEqual(divergent.selection_reason, "conflicting_evidence")

    def test_measurement_loop_persists_source_time_and_conflict(self) -> None:
        seed = "if catalyst increases yield, then reactor reduces waste"
        claim_id = claim_ids(seed)[0]
        measurements = [
            Measurement(claim_id, .8, .5, "above", "lab-a", "2026-07-21T01:00:00Z"),
            Measurement(claim_id, .2, .5, "above", "lab-b", "2026-07-21T02:00:00Z"),
        ]
        result = measurement_falsification_step(seed, measurements,
                                                require_evidence=False)
        self.assertEqual(result.verdicts[claim_id], "UNGROUNDED")
        self.assertTrue(result.decision.abstained)
        with tempfile.TemporaryDirectory() as directory:
            persist_measurement_evidence(directory, measurements)
            reloaded = load_fact_anchors(directory)
        self.assertEqual(resolve_evidence_verdicts(reloaded)[claim_id], "UNGROUNDED")
        provenance = {item for fact in reloaded for item in fact.provenance}
        self.assertIn("lab-a", provenance)
        self.assertIn("observed_at=2026-07-21T02:00:00Z", provenance)

    def test_duplicate_typed_fact_merges_provenance_instead_of_losing_source(self) -> None:
        facts = [
            Fact("claim", "has_verdict", "supported", ("lab-a", "observed_at=t1")),
            Fact("claim", "has_verdict", "supported", ("lab-b", "observed_at=t2")),
        ]
        store = TypedFactStore(facts)
        merged = store.exact("claim", "has_verdict", "supported")
        self.assertEqual(merged.provenance,
                         ("lab-a", "observed_at=t1", "lab-b", "observed_at=t2"))
        workspace = CognitiveWorkspace()
        workspace.add_facts(facts)
        self.assertEqual(workspace.facts[merged.key].provenance, merged.provenance)

    def test_greedy_decode_cache_requires_exact_model_input(self) -> None:
        from core import generator
        backend = {
            "kind": "clm", "loaded": True, "decodable": True, "ckpt": "fake.clm",
            "_decode_cache": {}, "_decode_cache_enabled": True,
        }
        ctx = {"phase": "REM", "deliberation_k": 1}
        anchors = [{"name": "percept", "text_payload": "same input"}]
        with mock.patch.object(generator, "_gen_clm_decode", return_value="same bytes") as decode:
            first = generator.generate(backend, ctx, True, anchors)
            # Anchored decode does not consume deliberation_k; changing that
            # non-input must still reuse the exact grounded model result.
            second = generator.generate(
                backend, {"phase": "REM", "deliberation_k": 4}, True, list(anchors))
            changed = generator.generate(
                backend, ctx, True,
                [{"name": "percept", "text_payload": "different input"}],
            )
        self.assertEqual(first, second)
        self.assertEqual(changed["text"], "same bytes")
        self.assertEqual(decode.call_count, 2)
        self.assertEqual(backend["_decode_cache_hits"], 1)
        self.assertEqual(backend["_decode_cache_misses"], 2)

    def test_decode_cache_never_reuses_sampled_mouth(self) -> None:
        from core import generator
        backend = {
            "kind": "clm", "loaded": True, "decodable": True, "ckpt": "fake.clm",
            "_decode_cache": {}, "_decode_cache_enabled": True,
        }
        mouth = {"temp": 1.0, "top_k": 40, "seed_rng": 7}
        with mock.patch.object(generator, "_gen_clm_decode", side_effect=("a", "b")) as decode:
            one = generator.generate(backend, {"phase": "REM"}, True, [], mouth)
            two = generator.generate(backend, {"phase": "REM"}, True, [], mouth)
        self.assertEqual((one["text"], two["text"]), ("a", "b"))
        self.assertEqual(decode.call_count, 2)

    def test_decode_cache_disabled_keeps_greedy_path_uncached(self) -> None:
        from core import generator
        backend = {
            "kind": "clm", "loaded": True, "decodable": True, "ckpt": "fake.clm",
            "_decode_cache": {}, "_decode_cache_enabled": False,
        }
        with mock.patch.object(generator, "_gen_clm_decode", side_effect=("a", "b")) as decode:
            one = generator.generate(backend, {"phase": "REM"}, True, [])
            two = generator.generate(backend, {"phase": "REM"}, True, [])
        self.assertEqual((one["text"], two["text"]), ("a", "b"))
        self.assertEqual(decode.call_count, 2)

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
            def ideate(self, prompt, *args):
                return prompt.split("Structured hypothesis: ", 1)[1].split(". Restate", 1)[0]

        class DroppingMouth:
            def ideate(self, *args):
                return "This is an interesting possibility."

        seed = "if copper conducts heat, then water drives turbines: "
        good = TypedWorkspaceMouth(PreservingMouth(), realizer="model")
        bad = TypedWorkspaceMouth(DroppingMouth(), realizer="model")
        self.assertEqual(good.ideate(seed, 40, 40, 0.7, 7), compose_seed(seed))
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
        primary_id, alternative_id = claim_ids(seed)[:2]
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

    def test_store_retrieval_persistence_and_controls(self) -> None:
        fact = Fact("pump", "has_state", "ready", ("meter",))
        with tempfile.TemporaryDirectory() as directory:
            store = TypedFactStore()
            store.persist(directory, "pump_ready", fact)
            loaded = TypedFactStore.load(directory)
            self.assertEqual(loaded.query("pump", "has_state")[0].key, fact.key)
            self.assertIn("pump_ready", loaded.query("pump", "has_state")[0].provenance)
            self.assertEqual(loaded.query("other", "has_state"), ())
            self.assertIsNone(loaded.exact("pump", "wrong_relation", "ready"))

    def test_numeric_measurement_collects_content_verdicts(self) -> None:
        ids = claim_ids("alpha rises. beta responds.")
        evidence = collect_measurement_evidence([
            Measurement(ids[0], 0.2, 0.5, "above", "trial"),
            Measurement(ids[1], 0.2, 0.5, "not_above", "trial"),
        ])
        self.assertEqual(evidence[0].object, "contradicted")
        self.assertEqual(evidence[1].object, "supported")

    def test_three_candidates_can_fall_through_to_uncertain(self) -> None:
        seed = "alpha rises. beta responds."
        ids = claim_ids(seed)
        decision = decide_seed(seed, [falsifier_fact(ids[0]), falsifier_fact(ids[1])])
        self.assertEqual(decision.selected_claim_id, ids[2])
        self.assertIn("uncertain", decision.text)

    def test_korean_conditional_and_negation_are_preserved(self) -> None:
        text = compose_seed("만약 비가 오지 않으면, 그러면 도로는 젖지 않는다")
        for term in ("비가", "오지", "도로는", "젖지"):
            self.assertIn(term, text)

    def test_english_middle_concepts_and_negation_are_preserved(self) -> None:
        physical = compose_seed(
            "if magnetic flux changes rapidly, then copper coil induces current")
        negative = compose_seed(
            "if cooling does not fail, then server avoids shutdown")
        for term in ("magnetic", "flux", "changes", "rapidly", "copper", "coil",
                     "induces", "current"):
            self.assertIn(term, physical)
        for term in ("cooling", "not", "fail", "server", "avoids", "shutdown"):
            self.assertIn(term, negative)

    def test_tether_abstains_and_self_controls_collapse(self) -> None:
        store = TypedFactStore([
            Fact("library", "opens_at", "09:00", ("sign",)),
            Fact("anima", "has_identity_anchor", "anchor-a", ("self",)),
        ])
        self.assertEqual(grounded_answer(store, "library", "opens_at"), "09:00")
        self.assertEqual(grounded_answer(store, "library", "closes_at"), "UNGROUNDED")
        self.assertEqual(identity_control(store, "anima", "anchor-a", "other"),
                         {"on": True, "off": False, "shuffle": False})

    def test_spoken_seam_changes_only_output_and_training_rows_are_complete(self) -> None:
        substrate = {"psi": b"unchanged", "memory": [1, 2, 3]}
        before = repr(substrate)
        seed = "alpha rises. beta responds."
        text, decision = spoken_workspace_step("base", seed)
        self.assertNotEqual(text, "base")
        self.assertIsNotNone(decision)
        self.assertEqual(repr(substrate), before)
        rows = realization_training_rows([seed, "atomic"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["target"], decision.text)
        self.assertEqual(len(rows[0]["candidate_specs"]), 3)

    def test_divergence_is_content_distinct_and_controls_collapse(self) -> None:
        report = certify_divergence("if copper conducts heat, then water drives turbines")
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["live"], 6)
        self.assertEqual(report["unique_specs"], 6)
        self.assertLessEqual(report["pairwise_max"], 0.5)
        self.assertEqual(report["missing_admit"], 0)
        self.assertEqual(report["shuffle_admit"], 0)

    def test_korean_divergence_preserves_negation_and_six_localized_lenses(self) -> None:
        seed = "만약 비가 오지 않으면, 그러면 도로는 젖지 않는다"
        report = certify_divergence(seed)
        self.assertTrue(report["ok"], report)
        texts = [hypothesis.text for hypothesis in report["hypotheses"]]
        for text in texts:
            for term in ("비가", "오지", "않", "도로는", "젖지", "않는다"):
                self.assertIn(term, text)
        for lens in ("양의", "음의", "문턱", "지연", "맥락", "영가설"):
            self.assertTrue(any(lens in text for text in texts))
        self.assertEqual(report["missing_admit"], 0)
        self.assertEqual(report["shuffle_admit"], 0)

    def test_multistep_divergence_preserves_middle_operands(self) -> None:
        seed = ("alpha starts beta. beta enables gamma. gamma activates delta. "
                "delta stabilizes epsilon. epsilon preserves zeta.")
        report = certify_divergence(seed)
        self.assertTrue(report["ok"], report)
        for hypothesis in report["hypotheses"]:
            for term in ("alpha", "beta", "gamma", "delta", "epsilon", "zeta"):
                self.assertIn(term, hypothesis.text)

    def test_divergent_evidence_rejects_reranks_and_abstains(self) -> None:
        seed = "if copper conducts heat, then water drives turbines"
        hypotheses = diverge_seed(seed)
        ids = tuple(h.spec.claim_id for h in hypotheses)
        off = select_divergence(seed)
        on = select_divergence(seed, [falsifier_fact(ids[0])])
        shuffled = select_divergence(seed, [falsifier_fact("workspace-claim-deadbeef-0")])
        grounded = select_divergence(seed, [support_fact(ids[2])], require_evidence=True)
        all_off = select_divergence(seed, [falsifier_fact(x) for x in ids])
        strict = select_divergence(seed, require_evidence=True)

        self.assertEqual(off.selected_claim_id, ids[0])
        self.assertEqual(on.selected_claim_id, ids[1])
        self.assertEqual(on.rejected_claim_ids, (ids[0],))
        self.assertEqual(shuffled.selected_claim_id, ids[0])
        self.assertEqual(grounded.selected_claim_id, ids[2])
        self.assertEqual(grounded.selection_reason, "supported_evidence")
        self.assertTrue(all_off.abstained)
        self.assertEqual(all_off.rejected_claim_ids, ids)
        self.assertTrue(strict.abstained)
        self.assertEqual(strict.selection_reason, "no_supported_candidate")

    def test_divergent_spoken_seam_preserves_substrate_and_uses_numeric_evidence(self) -> None:
        seed = "if copper conducts heat, then water drives turbines"
        hypotheses = diverge_seed(seed)
        substrate = {"psi": 0.5, "memory": b"same"}
        before = repr(substrate)
        evidence = collect_measurement_evidence([
            Measurement(hypotheses[0].spec.claim_id, 0.1, 0.5, "above")
        ])
        text, decision = spoken_divergence_step("base", seed, evidence)
        self.assertEqual(decision.selected_claim_id, hypotheses[1].spec.claim_id)
        self.assertEqual(text, hypotheses[1].text)
        self.assertEqual(repr(substrate), before)

    def test_auto_workspace_routes_only_compound_inputs(self) -> None:
        self.assertEqual(auto_workspace_mode(""), "off")
        self.assertEqual(auto_workspace_mode("copper conducts heat"), "off")
        self.assertEqual(
            auto_workspace_mode("if copper conducts heat, then water drives turbines"),
            "divergent",
        )

    def test_auto_workspace_uses_compound_percept_only_without_explicit_seed(self) -> None:
        compound = "if rain increases, then streets become wet"
        self.assertEqual(resolve_workspace_input("auto", "", compound),
                         ("divergent", compound))
        self.assertEqual(resolve_workspace_input("auto", "", "atomic percept"),
                         ("off", "atomic percept"))
        self.assertEqual(resolve_workspace_input("auto", "explicit atomic", compound),
                         ("off", "explicit atomic"))
        self.assertEqual(resolve_workspace_input("off", "", compound), ("off", ""))
        self.assertEqual(
            auto_workspace_mode("만약 비가 오지 않으면, 그러면 도로는 젖지 않는다"),
            "divergent",
        )

    def test_grounded_query_requires_unique_store_hit_and_controls_collapse(self) -> None:
        facts = [Fact("library", "opens_at", "09:00", ("sign",))]
        live, live_decision = grounded_query_step("model fabrication", "library|opens_at", facts)
        absent, absent_decision = grounded_query_step("model fabrication", "library|closes_at", facts)
        shuffled, shuffled_decision = grounded_query_step(
            "model fabrication", "other_library|opens_at", facts)
        ambiguous, ambiguous_decision = grounded_query_step(
            "model fabrication", "library|opens_at",
            facts + [Fact("library", "opens_at", "10:00", ("conflict",))],
        )
        self.assertEqual(live, "09:00")
        self.assertFalse(live_decision.abstained)
        for text, decision in ((absent, absent_decision), (shuffled, shuffled_decision),
                               (ambiguous, ambiguous_decision)):
            self.assertEqual(text, "UNGROUNDED")
            self.assertTrue(decision.abstained)
        with self.assertRaises(ValueError):
            grounded_query_step("base", "malformed", facts)

    def test_divergent_realizer_fails_closed_on_direction_or_lens_loss(self) -> None:
        hypothesis = diverge_seed("if copper conducts heat, then water drives turbines")[0]

        class Preserving:
            def ideate(self, *args):
                return hypothesis.text

        class Dropping:
            def ideate(self, *args):
                return "copper heat and water turbines may have a relationship"

        good = realize_divergence(Preserving(), hypothesis, 40, 40, 0.7, 1)
        bad = realize_divergence(Dropping(), hypothesis, 40, 40, 0.7, 1)
        self.assertTrue(good.valid)
        self.assertEqual(good.realized_by, "model")
        self.assertFalse(bad.valid)
        self.assertEqual(bad.text, hypothesis.text)
        self.assertEqual(bad.realized_by, "workspace_fallback")

    def test_divergent_realizer_can_use_model_score_without_mutating_semantics(self) -> None:
        hypothesis = diverge_seed("if copper conducts heat, then water drives turbines")[0]

        class ScoringMouth:
            def score(self, text):
                return 0.0 if text.startswith("Under the") else 1.0

            def ideate(self, *args):
                raise AssertionError("ranking path must not regenerate semantic slots")

        result = realize_divergence(ScoringMouth(), hypothesis, 40, 40, 0.7, 1)
        self.assertTrue(result.valid)
        self.assertEqual(result.realized_by, "model_rerank")
        self.assertEqual(result.candidate_count, 3)
        self.assertTrue(result.text.startswith("Under the"))
        self.assertTrue(divergence_preserves(hypothesis, result.text))

    def test_divergent_realizer_uses_score_many_once(self) -> None:
        hypothesis = diverge_seed("if copper conducts heat, then water drives turbines")[0]

        class BatchScoringMouth:
            def __init__(self):
                self.calls = 0

            def score(self, text):
                raise AssertionError("score_many must own the batch")

            def score_many(self, texts):
                self.calls += 1
                return [2.0, 0.0, 1.0]

        mouth = BatchScoringMouth()
        result = realize_divergence(mouth, hypothesis, 40, 40, 0.7, 1)
        self.assertEqual(mouth.calls, 1)
        self.assertEqual(result.realized_by, "model_rerank")
        self.assertTrue(result.text.startswith("Hypothesis"))
        self.assertTrue(divergence_preserves(hypothesis, result.text))

    def test_workspace_regression_passes_system_but_blocks_default_promotion(self) -> None:
        report = run_workspace_regression()
        self.assertTrue(report["system_pass"], report)
        self.assertFalse(report["default_promotable"])
        self.assertEqual(
            set(report["promotion_blockers"]),
            {"bare_store", "bare_fan", "bare_tether", "bare_self",
             "model_realizer_semantic_accept"},
        )

    def test_workspace_regression_accepts_only_complete_heldout_realizer_evidence(self) -> None:
        evidence = _valid_realizer_evidence()
        accepted = run_workspace_regression(evidence)
        self.assertTrue(accepted["promotion_blockers"]["model_realizer_semantic_accept"])
        evidence["fallback"] = 1
        rejected = run_workspace_regression(evidence)
        self.assertFalse(rejected["promotion_blockers"]["model_realizer_semantic_accept"])

    def test_workspace_system_rho_requires_measured_store_and_realizer_controls(self) -> None:
        realizer = _valid_realizer_evidence()
        store = {
            "schema": "anima.model-candidate.v1", "candidate_sha256": "a" * 64,
            "base_sha256": "b" * 64, "base_plus_slw_byte_parity": True,
            "training": {"freeze_trunk": True, "slw_restored": True,
                         "final_store_accuracy": 1.0, "final_address_accuracy": 1.0},
            "heldout_store": {"verdict": "PASS", "live": .96, "oracle": 1.0,
                              "shuffle": .40, "shuffle_balance_floor": .43,
                              "shuffle_fixed_points": 0,
                              "flip_coherence_baseline_correct": .98,
                              "lambda_zero": .47, "seen_heldout_gap": 0.0},
        }
        self.assertTrue(store_report_passes(store))
        report = run_workspace_system_rho(store, realizer)
        self.assertTrue(report["reach_closed"], report)
        self.assertFalse(report["bare_model_promoted"])
        store["heldout_store"]["shuffle"] = .50
        self.assertFalse(run_workspace_system_rho(store, realizer)["reach_closed"])
        store["heldout_store"]["shuffle"] = .40
        realizer["ckpt_sha256"] = "c" * 64
        self.assertFalse(run_workspace_system_rho(store, realizer)["reach_closed"])

    def test_release_verifier_rehashes_files_and_rejects_tampering(self) -> None:
        base = b"frozen-base-mouth"
        candidate = base + b"CLMS-trailer"
        base_sha = hashlib.sha256(base).hexdigest()
        candidate_sha = hashlib.sha256(candidate).hexdigest()
        realizer = _valid_realizer_evidence(base_sha)
        store = {
            "schema": "anima.model-candidate.v1", "candidate_sha256": candidate_sha,
            "base_sha256": base_sha, "base_plus_slw_prefix_sha256": base_sha,
            "base_plus_slw_byte_parity": True,
            "training": {"freeze_trunk": True, "slw_restored": True,
                         "final_store_accuracy": 1.0, "final_address_accuracy": 1.0},
            "heldout_store": {"verdict": "PASS", "live": .96, "oracle": 1.0,
                              "shuffle": .40, "shuffle_balance_floor": .43,
                              "shuffle_fixed_points": 0,
                              "flip_coherence_baseline_correct": .98,
                              "lambda_zero": .47, "seen_heldout_gap": 0.0},
        }
        with tempfile.TemporaryDirectory() as td:
            base_path, candidate_path = td + "/base.clm", td + "/candidate.clm"
            with open(base_path, "wb") as handle:
                handle.write(base)
            with open(candidate_path, "wb") as handle:
                handle.write(candidate)
            verified = verify_workspace_release(candidate_path, base_path, store, realizer)
            self.assertTrue(verified["release_verified"], verified)
            with open(candidate_path, "ab") as handle:
                handle.write(b"tamper")
            rejected = verify_workspace_release(candidate_path, base_path, store, realizer)
            self.assertFalse(rejected["release_verified"])
            self.assertFalse(rejected["checks"]["candidate_sha_matches_report"])

    def test_realizer_report_recomputes_text_semantics(self) -> None:
        evidence = _valid_realizer_evidence()
        evidence["cases"][0]["results"][0]["text"] = "valid true but operands missing"
        report = run_workspace_regression(evidence)
        self.assertFalse(report["promotion_blockers"]["model_realizer_semantic_accept"])

    def test_malformed_release_reports_fail_closed(self) -> None:
        realizer = _valid_realizer_evidence()
        realizer["hypotheses"] = "not-a-number"
        self.assertFalse(
            run_workspace_regression(realizer)["promotion_blockers"]
            ["model_realizer_semantic_accept"])
        malformed_store = {
            "schema": "anima.model-candidate.v1", "candidate_sha256": "a" * 64,
            "base_sha256": "b" * 64, "base_plus_slw_byte_parity": True,
            "training": {"freeze_trunk": True, "slw_restored": True,
                         "final_store_accuracy": "not-a-number",
                         "final_address_accuracy": 1.0},
            "heldout_store": {},
        }
        self.assertFalse(store_report_passes(malformed_store))


if __name__ == "__main__":
    unittest.main()
