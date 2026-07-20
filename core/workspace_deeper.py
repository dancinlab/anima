"""Second-stage G1/G6 certification: proof logic and evidence governance."""

from __future__ import annotations

from dataclasses import replace
import math
import tempfile

try:
    from .cognitive_workspace import (
        CognitiveWorkspace, CompositionRule, ConjunctiveRule, DisjunctiveRule, ExceptionRule,
        ExclusiveRule, Fact, ProofStep, QuantifiedRule, UnaryRule,
    )
    from .workspace_mouth import claim_ids
    from .workspace_runtime import (
        EvidenceLedger, EvidenceRecord, ExperimentDesign, Measurement,
        load_evidence_ledger, measurement_ledger_step, persist_evidence_ledger,
        rank_discriminating_experiments,
    )
except ImportError:
    from cognitive_workspace import (
        CognitiveWorkspace, CompositionRule, ConjunctiveRule, DisjunctiveRule, ExceptionRule,
        ExclusiveRule, Fact, ProofStep, QuantifiedRule, UnaryRule,
    )
    from workspace_mouth import claim_ids
    from workspace_runtime import (
        EvidenceLedger, EvidenceRecord, ExperimentDesign, Measurement,
        load_evidence_ledger, measurement_ledger_step, persist_evidence_ledger,
        rank_discriminating_experiments,
    )


def _workspace(facts, rules):
    workspace = CognitiveWorkspace()
    workspace.add_facts(facts)
    workspace.compose_until_stable(rules)
    return workspace


def run_g1_logic_certification() -> dict:
    rows = []

    implication = CompositionRule(
        "sufficient-forward", "sufficient_for", "implies", "implies")
    forward = _workspace([
        Fact("rain", "sufficient_for", "wet_ground", ("premise:rain",)),
        Fact("wet_ground", "implies", "slippery", ("premise:wet",)),
    ], [implication])
    reversed_direction = _workspace([
        Fact("wet_ground", "necessary_for", "rain"),
        Fact("wet_ground", "implies", "slippery"),
    ], [implication])
    target = ("rain", "implies", "slippery")
    checks = {
        "sufficient_direction_derives": target in forward.facts,
        "necessary_not_reversed": target not in reversed_direction.facts,
        "implication_proof_replays": forward.verify_proof(target),
    }
    rows.append({"case": "necessary_sufficient", "checks": checks,
                 "ok": all(checks.values())})

    conjunction = ConjunctiveRule(
        "access-and", "identity_verified", "consent_verified", "access_granted")
    both_inputs = _workspace([
        Fact("identity", "identity_verified", "vault", ("id-check",)),
        Fact("consent", "consent_verified", "vault", ("consent-check",)),
    ], [conjunction])
    one_input = _workspace([
        Fact("identity", "identity_verified", "vault", ("id-check",)),
    ], [conjunction])
    and_target = ("identity & consent", "access_granted", "vault")
    checks = {
        "and_both_derive": and_target in both_inputs.facts,
        "and_one_collapses": and_target not in one_input.facts,
        "and_proof_replays": both_inputs.verify_proof(and_target),
    }
    rows.append({"case": "conjunction", "checks": checks, "ok": all(checks.values())})

    disjunction = DisjunctiveRule(
        "energy-or", "solar_available", "battery_available", "power_available")
    solar = _workspace([Fact("site", "solar_available", "grid", ("solar",))],
                       [disjunction])
    battery = _workspace([Fact("site", "battery_available", "grid", ("battery",))],
                         [disjunction])
    none = _workspace([Fact("site", "wind_unmeasured", "grid")], [disjunction])
    or_target = ("site", "power_available", "grid")
    checks = {
        "or_left_derives": or_target in solar.facts,
        "or_right_derives": or_target in battery.facts,
        "or_without_branch_collapses": or_target not in none.facts,
        "or_proof_names_branch": "or:solar_available" in solar.facts[or_target].provenance,
    }
    rows.append({"case": "inclusive_or", "checks": checks, "ok": all(checks.values())})

    exclusive = ExclusiveRule(
        "exclusive-key", "key_a_active", "key_b_active", "exactly_one_key")
    one = _workspace([Fact("lock", "key_a_active", "door")], [exclusive])
    both = _workspace([
        Fact("lock", "key_a_active", "door"),
        Fact("lock", "key_b_active", "door"),
    ], [exclusive])
    xor_target = ("lock", "exactly_one_key", "door")
    xor_valid_before = one.verify_proof(xor_target)
    one.add_facts([Fact("lock", "key_b_active", "door", ("late-second-key",))])
    checks = {
        "xor_one_derives": xor_target in one.facts,
        "xor_both_collapses": xor_target not in both.facts,
        "xor_proof_replays": xor_valid_before,
        "late_second_branch_invalidates_proof": not one.verify_proof(xor_target),
    }
    rows.append({"case": "exclusive_or", "checks": checks, "ok": all(checks.values())})

    exception = ExceptionRule(
        "default-flight", "normally_can", "has_exception", "can")
    clear = _workspace([
        Fact("sparrow", "normally_can", "fly", ("taxonomy",)),
        Fact("sparrow", "has_no_exception", "fly", ("health-check",)),
    ], [exception])
    blocked = _workspace([
        Fact("sparrow", "normally_can", "fly"),
        Fact("sparrow", "has_no_exception", "fly"),
        Fact("sparrow", "has_exception", "fly", ("injury",)),
    ], [exception])
    exception_target = ("sparrow", "can", "fly")
    exception_claim = clear.propose(
        clear.facts[exception_target], [Fact("flight-test", "result", "failed")])
    clear.add_facts([Fact("sparrow", "has_exception", "fly", ("late-injury",))])
    checks = {
        "explicit_clearance_derives": exception_target in clear.facts,
        "exception_blocks_default": exception_target not in blocked.facts,
        "late_exception_invalidates_proof": not clear.verify_proof(exception_target),
        "invalid_proof_cannot_be_selected": clear.test(exception_claim).value == "ungrounded",
    }
    rows.append({"case": "exception", "checks": checks, "ok": all(checks.values())})

    quantified = QuantifiedRule("universal-instantiation")
    universal = _workspace([
        Fact("tweety", "is_a", "bird", ("observation",)),
        Fact("bird", "all_imply", "animal", ("universal",)),
    ], [quantified])
    existential = _workspace([
        Fact("tweety", "is_a", "bird"),
        Fact("bird", "some_imply", "animal"),
    ], [quantified])
    quant_target = ("tweety", "is_a", "animal")
    checks = {
        "universal_instantiates": quant_target in universal.facts,
        "some_does_not_license_all": quant_target not in existential.facts,
        "quantified_proof_replays": universal.verify_proof(quant_target),
    }
    rows.append({"case": "quantifier", "checks": checks, "ok": all(checks.values())})

    double_negation = UnaryRule("double-negation", "not_not_active", "active")
    double = _workspace([Fact("pump", "not_not_active", "line", ("scope:double",))],
                        [double_negation])
    single = _workspace([Fact("pump", "not_active", "line", ("scope:single",))],
                        [double_negation])
    neg_target = ("pump", "active", "line")
    checks = {
        "double_negation_eliminates": neg_target in double.facts,
        "single_negation_preserved": neg_target not in single.facts,
        "scope_proof_replays": double.verify_proof(neg_target),
    }
    rows.append({"case": "negation_scope", "checks": checks, "ok": all(checks.values())})

    temporal = CompositionRule("before-transitive", "before", "before", "before")
    ordered = _workspace([
        Fact("dose", "before", "response", ("t=1",)),
        Fact("response", "before", "recovery", ("t=2",)),
    ], [temporal])
    shuffled = _workspace([
        Fact("response", "before", "dose"),
        Fact("response", "before", "recovery"),
    ], [temporal])
    time_target = ("dose", "before", "recovery")
    checks = {
        "ordered_time_derives": time_target in ordered.facts,
        "time_order_shuffle_collapses": time_target not in shuffled.facts,
        "temporal_proof_replays": ordered.verify_proof(time_target),
    }
    rows.append({"case": "temporal_order", "checks": checks, "ok": all(checks.values())})

    proof = _workspace([
        Fact("a", "reaches", "b", ("edge:a",)),
        Fact("b", "reaches", "c", ("edge:b",)),
        Fact("c", "reaches", "d", ("edge:c",)),
    ], [CompositionRule("proof-chain", "reaches", "reaches", "reaches")])
    proof_target = ("a", "reaches", "d")
    proof_slice = proof.proof_for(proof_target)
    valid_before = proof.verify_proof(proof_target)
    original = proof.proofs[proof_target]
    proof.proofs[proof_target] = ProofStep(original.conclusion, "fabricated-rule",
                                          original.premises)
    tamper_detected = not proof.verify_proof(proof_target)
    proof.proofs[proof_target] = original
    removed_key = original.premises[0]
    removed_fact = proof.facts.pop(removed_key)
    parent_loss_detected = not proof.verify_proof(proof_target)
    proof.facts[removed_key] = removed_fact
    checks = {
        "proof_dag_contains_axioms": sum(step.is_axiom for step in proof_slice) >= 3,
        "proof_dag_replays": valid_before,
        "rule_tamper_detected": tamper_detected,
        "parent_loss_detected": parent_loss_detected,
    }
    rows.append({"case": "proof_object", "checks": checks, "ok": all(checks.values())})

    return {"schema": "anima.workspace-g1-logic/v1",
            "ok": all(row["ok"] for row in rows), "cases": rows}


def _measurement(claim_id: str, verdict: str, experiment: str, source: str,
                 observed_at: str, **kwargs) -> Measurement:
    observed = 0.8 if verdict == "supported" else 0.2
    return Measurement(
        claim_id, observed, 0.5, "above", source, observed_at,
        experiment_id=experiment, context=kwargs.pop("context", "reactor-v1"),
        sample_size=kwargs.pop("sample_size", 100),
        uncertainty=kwargs.pop("uncertainty", 0.05), **kwargs)


def _record(evidence_id: str, claim_id: str, verdict: str, experiment: str,
            source: str, observed_at: str, **kwargs) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id, claim_id, verdict, source, observed_at, experiment,
        context=kwargs.pop("context", "reactor-v1"),
        sample_size=kwargs.pop("sample_size", 100),
        uncertainty=kwargs.pop("uncertainty", 0.05), **kwargs)


def run_g6_evidence_certification() -> dict:
    seed = "if catalyst increases yield, then reactor reduces waste"
    ids = claim_ids(seed)
    primary = ids[0]

    strong_contradiction = measurement_ledger_step(seed, [
        _measurement(primary, "contradicted", "exp-1", "lab-a",
                     "2026-07-21T01:00:00Z")
    ])
    weak = measurement_ledger_step(seed, [
        _measurement(primary, "supported", "weak-1", "lab-a",
                     "2026-07-21T01:00:00Z", sample_size=8, uncertainty=0.6)
    ])
    missing = measurement_ledger_step(seed, [
        _measurement(primary, "supported", "missing-1", "lab-a",
                     "2026-07-21T01:00:00Z", missing=True)
    ])
    tied = measurement_ledger_step(seed, [
        _measurement(primary, "supported", "tie-a", "lab-a",
                     "2026-07-21T01:00:00Z"),
        _measurement(primary, "contradicted", "tie-b", "lab-b",
                     "2026-07-21T02:00:00Z"),
    ])
    replicated = measurement_ledger_step(seed, [
        _measurement(primary, "contradicted", "rep-a", "lab-a",
                     "2026-07-21T01:00:00Z"),
        _measurement(primary, "contradicted", "rep-b", "lab-b",
                     "2026-07-21T02:00:00Z"),
        # Deliberately latest: recency alone must not override two replications.
        _measurement(primary, "supported", "rep-c", "lab-c",
                     "2026-07-21T23:00:00Z"),
    ])
    duplicated_source = measurement_ledger_step(seed, [
        _measurement(primary, "contradicted", "dup-a", "same-lab",
                     "2026-07-21T01:00:00Z"),
        _measurement(primary, "contradicted", "dup-b", "same-lab",
                     "2026-07-21T02:00:00Z"),
        _measurement(primary, "supported", "dup-c", "other-lab",
                     "2026-07-21T03:00:00Z"),
    ])
    cross_context = measurement_ledger_step(seed, [
        _measurement(primary, "contradicted", "ctx-a", "lab-a",
                     "2026-07-21T01:00:00Z", context="reactor-v1"),
        _measurement(primary, "contradicted", "ctx-b", "lab-b",
                     "2026-07-21T02:00:00Z", context="reactor-v2"),
    ])
    observational_causal = measurement_ledger_step(seed, [
        _measurement(primary, "supported", "obs-a", "lab-a",
                     "2026-07-21T01:00:00Z", study_type="observational")
    ], target_inference="causal")
    intervention = measurement_ledger_step(seed, [
        _measurement(primary, "contradicted", "do-a", "lab-a",
                     "2026-07-21T01:00:00Z", study_type="interventional",
                     randomized=True)
    ], target_inference="causal")
    shuffled = measurement_ledger_step(seed, [
        _measurement(primary + ":shuffle", "contradicted", "shuffle", "lab-a",
                     "2026-07-21T01:00:00Z")
    ])

    original = _record("r1", primary, "supported", "corrected-exp", "lab-a",
                       "2026-07-21T01:00:00Z")
    correction = _record("r2", primary, "contradicted", "corrected-exp", "lab-a",
                         "2026-07-21T02:00:00Z", supersedes="r1")
    retraction = _record("r3", primary, "contradicted", "corrected-exp", "lab-a",
                         "2026-07-21T03:00:00Z", supersedes="r2", retracted=True)
    correction_ledger = EvidenceLedger([original, correction])
    correction_status = correction_ledger.resolve(primary)
    correction_ledger.append(retraction)
    retracted_status = correction_ledger.resolve(primary)
    with tempfile.TemporaryDirectory() as directory:
        path = persist_evidence_ledger(directory, [original, correction, retraction])
        reloaded = load_evidence_ledger(path)
        persisted_status = reloaded.resolve(primary)
        persisted_rows = len(reloaded.records)

    malformed_time_rejected = False
    cross_claim_correction_rejected = False
    try:
        replace(original, evidence_id="bad-time", observed_at="2026-07-21 01:00:00")
    except ValueError:
        malformed_time_rejected = True
    try:
        EvidenceLedger([original]).append(replace(
            correction, evidence_id="cross", claim_id=ids[1]))
    except ValueError:
        cross_claim_correction_rejected = True

    designs = (
        ExperimentDesign("uninformative", tuple((claim_id, "same") for claim_id in ids)),
        ExperimentDesign("binary", ((ids[0], "up"), (ids[1], "down"), (ids[2], "down"))),
        ExperimentDesign("fully-discriminating",
                         ((ids[0], "up"), (ids[1], "down"), (ids[2], "flat"))),
    )
    ranked = rank_discriminating_experiments(ids, designs)

    checks = {
        "strong_contradiction_removes_primary":
            strong_contradiction.decision.selected_claim_id == ids[1],
        "weak_evidence_inconclusive": weak.resolutions[primary].status == "INCONCLUSIVE"
            and weak.decision.abstained,
        "missing_data_inconclusive": missing.resolutions[primary].status == "INCONCLUSIVE"
            and missing.decision.abstained,
        "tied_conflict_ungrounded": tied.resolutions[primary].status == "UNGROUNDED"
            and tied.decision.abstained,
        "replicated_majority_resolves": replicated.resolutions[primary].status == "contradicted"
            and replicated.resolutions[primary].reason == "replicated_majority",
        "latest_does_not_win": replicated.decision.selected_claim_id == ids[1],
        "duplicate_source_not_replication":
            duplicated_source.resolutions[primary].reason == "insufficient_independent_replication",
        "cross_context_not_combined":
            cross_context.resolutions[primary].reason == "incomparable_contexts",
        "observation_cannot_ground_cause":
            observational_causal.resolutions[primary].status == "INCONCLUSIVE",
        "randomized_intervention_can_falsify":
            intervention.resolutions[primary].status == "contradicted",
        "claim_id_shuffle_inert": shuffled.decision.abstained,
        "correction_supersedes_without_mutation": correction_status.status == "contradicted"
            and len(correction_ledger.records) == 3,
        "retraction_yields_inconclusive": retracted_status.status == "INCONCLUSIVE",
        "ledger_roundtrip_preserves_history": persisted_rows == 3
            and persisted_status.status == "INCONCLUSIVE",
        "malformed_timestamp_rejected": malformed_time_rejected,
        "cross_claim_correction_rejected": cross_claim_correction_rejected,
        "best_experiment_maximizes_information": ranked[0][0].name == "fully-discriminating"
            and math.isclose(ranked[0][1], math.log(3, 2)),
        "uninformative_experiment_scores_zero": ranked[-1][0].name == "uninformative"
            and ranked[-1][1] == 0.0,
    }
    return {"schema": "anima.workspace-g6-evidence/v1", "ok": all(checks.values()),
            "checks": checks}


def run_workspace_deeper_certification() -> dict:
    g1 = run_g1_logic_certification()
    g6 = run_g6_evidence_certification()
    return {"schema": "anima.workspace-deeper/v1", "ok": g1["ok"] and g6["ok"],
            "g1": g1, "g6": g6}


def format_deeper_report(report: dict) -> str:
    lines = ["=== anima workspace G1/G6 deeper certification ==="]
    for row in report["g1"]["cases"]:
        lines.append(("PASS " if row["ok"] else "FAIL ") + "G1 " + row["case"])
        lines.extend("  " + ("PASS " if ok else "FAIL ") + name
                     for name, ok in row["checks"].items())
    lines.append(("PASS " if report["g6"]["ok"] else "FAIL ") + "G6 evidence ledger")
    lines.extend("  " + ("PASS " if ok else "FAIL ") + name
                 for name, ok in report["g6"]["checks"].items())
    lines.append("WORKSPACE_DEEPER: " + ("CERTIFIED" if report["ok"] else "FAIL"))
    return "\n".join(lines)
