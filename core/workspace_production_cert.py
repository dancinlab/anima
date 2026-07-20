"""Ckpt-free certification for the opt-in production workspace path."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
import json
import os
import tempfile

try:
    from .cognitive_workspace import Fact
    from .workspace_evidence import (
        CausalGraph, DurableEvidenceLedger, EvidenceAuthorityRegistry,
        EvidenceEnvelope, EvidenceRecord, ExperimentRegistration,
        StatisticalMeasurement, StratifiedResult, assess_statistical_measurement,
        detects_simpsons_paradox,
    )
    from .workspace_logic import (
        compose_extracted_logic, extract_typed_logic, make_proof_artifact,
        verify_proof_artifact,
    )
    from .workspace_mouth import diverge_seed, select_divergence
    from .workspace_production import (
        WorkspaceProductionSession, active_falsification_state,
        make_decision_proof, verify_decision_proof,
    )
    from .workspace_runtime import EvidenceLedger
except ImportError:
    from cognitive_workspace import Fact
    from workspace_evidence import (
        CausalGraph, DurableEvidenceLedger, EvidenceAuthorityRegistry,
        EvidenceEnvelope, EvidenceRecord, ExperimentRegistration,
        StatisticalMeasurement, StratifiedResult, assess_statistical_measurement,
        detects_simpsons_paradox,
    )
    from workspace_logic import (
        compose_extracted_logic, extract_typed_logic, make_proof_artifact,
        verify_proof_artifact,
    )
    from workspace_mouth import diverge_seed, select_divergence
    from workspace_production import (
        WorkspaceProductionSession, active_falsification_state,
        make_decision_proof, verify_decision_proof,
    )
    from workspace_runtime import EvidenceLedger


def _record(evidence_id: str, claim_id: str, verdict: str,
            experiment_id: str, source: str = "lab-a",
            observed_at: str = "2026-07-21T01:00:00Z") -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id, claim_id, verdict, source, observed_at, experiment_id,
        "reactor-v1", 200, .05,
    )


def run_logic_production_certification() -> dict:
    english = extract_typed_logic("all birds are animals; tweety is a bird")
    english_workspace = compose_extracted_logic(english)
    english_target = ("tweety", "is_a", "animal")
    korean = extract_typed_logic("모든 새는 동물이다; 참새는 새이다")
    korean_workspace = compose_extracted_logic(korean)
    korean_target = ("참새", "is_a", "동물")
    temporal = compose_extracted_logic(extract_typed_logic(
        "dose before response; response before recovery"))
    conjunction = compose_extracted_logic(extract_typed_logic(
        "identity verified and consent verified imply access granted"))
    disjunction = compose_extracted_logic(extract_typed_logic(
        "solar available or battery available imply power available"))
    xor_unresolved = compose_extracted_logic(extract_typed_logic(
        "exactly one of key a or key b implies door opens"))
    xor_resolved = compose_extracted_logic(extract_typed_logic(
        "only key a, not key b, implies door opens"))
    double_negation = compose_extracted_logic(extract_typed_logic(
        "pump is not not active"))
    ambiguous = extract_typed_logic("birds might perhaps be animals unless context changes")

    artifact = make_proof_artifact(english_workspace, english_target)
    tampered = json.loads(json.dumps(artifact))
    tampered["facts"][-1]["object"] = "machine"

    with tempfile.TemporaryDirectory() as directory:
        first = WorkspaceProductionSession(directory)
        one = first.ingest("all birds are animals")
        second = WorkspaceProductionSession(directory)
        two = second.ingest("tweety is a bird")
        proof_path = os.path.join(directory, "proofs.jsonl")
        with open(proof_path, "r", encoding="utf-8") as handle:
            persisted = [json.loads(line) for line in handle if line.strip()]
    with tempfile.TemporaryDirectory() as directory:
        exception_session = WorkspaceProductionSession(directory)
        exception_session.ingest("normally bird implies fly")
        cleared = exception_session.ingest("bird has no exception to fly")
        blocked = exception_session.ingest("bird has an exception to fly")
        invalidation_path = os.path.join(directory, "proof-invalidations.jsonl")
        with open(invalidation_path, "r", encoding="utf-8") as handle:
            invalidations = [json.loads(line) for line in handle if line.strip()]

    checks = {
        "english_universal_derives": english_target in english_workspace.facts,
        "english_proof_replays": english_workspace.verify_proof(english_target),
        "korean_universal_derives": korean_target in korean_workspace.facts,
        "korean_proof_replays": korean_workspace.verify_proof(korean_target),
        "and_requires_both": ("identity_verified & consent_verified", "implies",
                              "access_granted") in conjunction.facts,
        "or_either_branch_derives": ("solar_available", "implies", "power_available")
            in disjunction.facts and ("battery_available", "implies", "power_available")
            in disjunction.facts,
        "xor_without_observed_branch_abstains": not xor_unresolved.derivations,
        "xor_explicit_single_branch_derives":
            ("key_a", "implies", "door_opens") in xor_resolved.facts,
        "double_negation_scope_derives": ("pump", "is", "active") in double_negation.facts,
        "temporal_order_composes": ("dose", "before", "recovery") in temporal.facts,
        "ambiguous_language_abstains": ambiguous.ambiguous and not ambiguous.facts,
        "portable_proof_verifies": verify_proof_artifact(artifact),
        "tampered_proof_rejected": not verify_proof_artifact(tampered),
        "cross_session_logic_composes": one.accepted and two.accepted and two.proof_count >= 1,
        "cross_session_proof_verifies": bool(persisted)
            and all(verify_proof_artifact(item) for item in persisted),
        "late_exception_invalidates_persisted_proof": cleared.proof_count >= 1
            and blocked.accepted and bool(invalidations),
    }
    return {"schema": "anima.workspace-production-logic/v1",
            "ok": all(checks.values()), "checks": checks}


def run_evidence_production_certification() -> dict:
    claim_id = "workspace-claim-production-0"
    registration = ExperimentRegistration(
        "exp-a", claim_id, "lab-a", "reactor-v1")
    registry = EvidenceAuthorityRegistry({"lab-a": b"secret-a"}, [registration])
    record = _record("e-a", claim_id, "supported", "exp-a")
    envelope = registry.sign(record)
    signature_ok = registry.verify(envelope)
    tampered = EvidenceEnvelope(
        EvidenceRecord(**{**asdict(record), "verdict": "contradicted"}),
        envelope.signature,
    )
    shuffled_claim = EvidenceEnvelope(
        EvidenceRecord(**{**asdict(record), "claim_id": claim_id + ":shuffle"}),
        envelope.signature,
    )

    strong = assess_statistical_measurement(StatisticalMeasurement(
        claim_id, 1.0, 0.0, 1.0, 1.0, 400, 400, "above", "lab-a",
        "2026-07-21T01:00:00Z", "exp-a", "reactor-v1"))
    contradicted = assess_statistical_measurement(StatisticalMeasurement(
        claim_id, 0.0, 1.0, 1.0, 1.0, 400, 400, "above", "lab-a",
        "2026-07-21T01:00:00Z", "exp-a", "reactor-v1"))
    uncertain = assess_statistical_measurement(StatisticalMeasurement(
        claim_id, .02, 0.0, 1.0, 1.0, 30, 30, "above", "lab-a",
        "2026-07-21T01:00:00Z", "exp-a", "reactor-v1"))
    missing = assess_statistical_measurement(StatisticalMeasurement(
        claim_id, 1.0, 0.0, 1.0, 1.0, 400, 400, "above", "lab-a",
        "2026-07-21T01:00:00Z", "exp-a", "reactor-v1", missing=True))

    graph = CausalGraph((
        ("temperature", "dose"), ("temperature", "response"),
        ("dose", "response"),
    ))
    cycle_rejected = False
    try:
        CausalGraph((("a", "b"), ("b", "a")))
    except ValueError:
        cycle_rejected = True
    simpson = detects_simpsons_paradox((
        StratifiedResult(.90, .80, 10, 100),
        StratifiedResult(.30, .20, 100, 10),
    ))
    missing_registered = registry.missing_registered_experiments(())

    backward_correction_rejected = False
    original = _record("original", claim_id, "supported", "exp-a",
                       observed_at="2026-07-21T02:00:00Z")
    correction = EvidenceRecord(**{
        **asdict(original), "evidence_id": "correction", "verdict": "contradicted",
        "observed_at": "2026-07-21T01:00:00Z", "supersedes": "original",
    })
    try:
        EvidenceLedger([original, correction])
    except ValueError:
        backward_correction_rejected = True

    checks = {
        "valid_signature_accepts": signature_ok,
        "payload_tamper_rejected": not registry.verify(tampered),
        "claim_id_substitution_rejected": not registry.verify(shuffled_claim),
        "statistical_support_from_ci": strong.status == "supported" and strong.ci_low > 0,
        "statistical_contradiction_from_ci":
            contradicted.status == "contradicted" and contradicted.ci_high <= 0,
        "overlapping_ci_inconclusive": uncertain.status == "INCONCLUSIVE",
        "missing_data_inconclusive": missing.status == "INCONCLUSIVE",
        "confounder_detected": graph.direct_confounders("dose", "response") == ("temperature",),
        "unadjusted_observation_not_identified":
            not graph.intervention_identified("dose", "response"),
        "adjustment_identifies_direct_confounder":
            graph.intervention_identified("dose", "response", ("temperature",)),
        "randomization_identifies": graph.intervention_identified("dose", "response", randomized=True),
        "causal_cycle_rejected": cycle_rejected,
        "simpsons_paradox_detected": simpson,
        "selective_reporting_visible": missing_registered == ("exp-a",),
        "backward_correction_rejected": backward_correction_rejected,
    }
    return {"schema": "anima.workspace-production-evidence/v1",
            "ok": all(checks.values()), "checks": checks}


def run_durability_certification() -> dict:
    claim_id = "workspace-claim-durable"
    count = 12
    registrations = tuple(ExperimentRegistration(
        "exp-%02d" % index, claim_id, "lab-%02d" % index, "context-a")
        for index in range(count + 2))
    keys = {"lab-%02d" % index: ("key-%02d" % index).encode("ascii")
            for index in range(count + 2)}
    registry = EvidenceAuthorityRegistry(keys, registrations)
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "evidence.jsonl")
        durable = DurableEvidenceLedger(path, registry)

        def append_index(index):
            record = EvidenceRecord(
                "e-%02d" % index, claim_id, "supported", "lab-%02d" % index,
                "2026-07-21T%02d:00:00Z" % index, "exp-%02d" % index,
                "context-a", 100, .05,
            )
            durable.append(registry.sign(record))

        with ThreadPoolExecutor(max_workers=6) as pool:
            tuple(pool.map(append_index, range(count)))
        concurrent = durable.load()
        checkpoint_path = durable.checkpoint()
        with open(checkpoint_path, "r", encoding="utf-8") as handle:
            checkpoint = json.load(handle)
        with open(path, "ab") as handle:
            handle.write(b'{"torn":')
        recovered = durable.load()
        append_index(count)
        after_repair = durable.load()
        interior_corrupt = os.path.join(directory, "interior.jsonl")
        with open(interior_corrupt, "w", encoding="utf-8") as handle:
            handle.write('{"bad":true}\n{"also":"bad"}\n')
        corruption_rejected = False
        try:
            DurableEvidenceLedger(interior_corrupt, registry).load()
        except ValueError:
            corruption_rejected = True

        state_directory = os.path.join(directory, "state")
        state = WorkspaceProductionSession(state_directory)
        state.ingest("all birds are animals")
        with open(state.logic_path, "ab") as handle:
            handle.write(b'{"torn":')
        logic_repaired = state.ingest("tweety is a bird")
        with open(state.proof_path, "ab") as handle:
            handle.write(b'{"torn":')
        proof_repaired = state.ingest("robin is a bird")
        with open(state.logic_path, "r", encoding="utf-8") as handle:
            logic_rows = [json.loads(line) for line in handle if line.strip()]
        with open(state.proof_path, "r", encoding="utf-8") as handle:
            proof_rows = [json.loads(line) for line in handle if line.strip()]

    checks = {
        "concurrent_appends_complete": len(concurrent.envelopes) == count,
        "concurrent_ids_unique": len({item.record.evidence_id for item in concurrent.envelopes}) == count,
        "checkpoint_preserves_history_root": checkpoint["record_count"] == count
            and len(checkpoint["history_root"]) == 64,
        "torn_tail_detected": recovered.recovered_trailing_partial,
        "append_repairs_torn_tail": len(after_repair.envelopes) == count + 1
            and not after_repair.recovered_trailing_partial,
        "interior_corruption_rejected": corruption_rejected,
        "logic_torn_tail_repaired": logic_repaired.accepted
            and all(len(row.get("sha256", "")) == 64 for row in logic_rows),
        "proof_torn_tail_repaired": proof_repaired.accepted
            and all(verify_proof_artifact(row) for row in proof_rows),
    }
    return {"schema": "anima.workspace-production-durability/v1",
            "ok": all(checks.values()), "checks": checks}


def run_active_production_certification() -> dict:
    seed = "if catalyst increases yield, then reactor reduces waste"
    hypotheses = diverge_seed(seed)
    ids = tuple(item.spec.claim_id for item in hypotheses)
    records = [_record("reject-%d" % index, claim_id, "contradicted",
                       "active-%d" % index, "lab-%d" % index,
                       "2026-07-21T%02d:00:00Z" % index)
               for index, claim_id in enumerate(ids[:-1])]
    initial = active_falsification_state(seed, EvidenceLedger())
    narrowed = active_falsification_state(seed, EvidenceLedger(records))

    evidence = (Fact(ids[0], "has_verdict", "contradicted", ("measured",)),)
    decision = select_divergence(seed, evidence, require_evidence=False)
    proof = make_decision_proof(seed, True, False, evidence, decision)
    altered = dict(proof)
    altered["selected_claim_id"] = "forged"

    session_ok = False
    session_rejects_unsigned = False
    with tempfile.TemporaryDirectory() as directory:
        registration = ExperimentRegistration(
            "session-exp", ids[0], "session-lab", "reactor-v1")
        registry = EvidenceAuthorityRegistry({"session-lab": b"session-secret"}, [registration])
        session = WorkspaceProductionSession(directory, registry)
        measurement = StatisticalMeasurement(
            ids[0], 0.0, 1.0, 1.0, 1.0, 400, 400, "above", "session-lab",
            "2026-07-21T01:00:00Z", "session-exp", "reactor-v1")
        signed_measurement = {
            "measurement": asdict(measurement),
            "signature": registry.sign_measurement(measurement),
        }
        result = session.ingest("MEASUREMENT " + json.dumps(signed_measurement))
        observed_state = session.observe_active_state(seed)
        session_ok = (result.accepted and observed_state.rejected_claim_ids == (ids[0],)
                      and session.summary()["active_updates"] == 1)
        unsigned_with_registry = session.ingest(
            "MEASUREMENT " + json.dumps({"measurement": asdict(measurement)}))
        unsigned_session = WorkspaceProductionSession(os.path.join(directory, "unsigned"))
        unsigned = unsigned_session.ingest("MEASUREMENT " + json.dumps(signed_measurement))
        session_rejects_unsigned = not unsigned.accepted and not unsigned_with_registry.accepted

    checks = {
        "six_dynamic_alternatives": len(ids) == 6 and len(set(ids)) == 6,
        "initial_loop_requests_experiment": initial.reason == "experiment_required"
            and initial.next_experiment is not None and initial.next_information_value > 0,
        "falsified_candidates_removed": narrowed.rejected_claim_ids == ids[:-1],
        "single_survivor_selected": narrowed.selected_claim_id == ids[-1]
            and narrowed.reason == "single_survivor",
        "decision_proof_replays": verify_decision_proof(proof),
        "decision_proof_tamper_rejected": not verify_decision_proof(altered),
        "production_session_uses_ledger": session_ok,
        "production_session_rejects_unsigned_measurement": session_rejects_unsigned,
    }
    return {"schema": "anima.workspace-production-active/v1",
            "ok": all(checks.values()), "checks": checks}


def run_workspace_production_certification() -> dict:
    groups = {
        "logic": run_logic_production_certification(),
        "evidence": run_evidence_production_certification(),
        "durability": run_durability_certification(),
        "active": run_active_production_certification(),
    }
    return {"schema": "anima.workspace-production/v1",
            "ok": all(group["ok"] for group in groups.values()), "groups": groups}


def format_production_report(report: dict) -> str:
    lines = ["=== anima workspace production certification ==="]
    for name, group in report["groups"].items():
        lines.append(("PASS " if group["ok"] else "FAIL ") + name)
        lines.extend("  " + ("PASS " if ok else "FAIL ") + check
                     for check, ok in group["checks"].items())
    lines.append("WORKSPACE_PRODUCTION: " + ("CERTIFIED" if report["ok"] else "FAIL"))
    return "\n".join(lines)
