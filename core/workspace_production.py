"""Opt-in production orchestration for proof-carrying falsification sessions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
from typing import Iterable

try:
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None

try:
    from .cognitive_workspace import Fact
    from .workspace_evidence import (
        DurableEvidenceLedger, EvidenceAuthorityRegistry, EvidenceEnvelope, EvidenceRecord,
        StatisticalMeasurement, append_proof_artifact, assess_statistical_measurement,
    )
    from .workspace_logic import (
        compose_extracted_logic, extract_typed_logic, proof_artifacts_for_derivations,
        verify_proof_artifact,
    )
    from .workspace_mouth import claim_ids, diverge_seed
    from .workspace_runtime import (
        EvidenceLedger, ExperimentDesign, rank_discriminating_experiments,
    )
except ImportError:
    from cognitive_workspace import Fact
    from workspace_evidence import (
        DurableEvidenceLedger, EvidenceAuthorityRegistry, EvidenceEnvelope, EvidenceRecord,
        StatisticalMeasurement, append_proof_artifact, assess_statistical_measurement,
    )
    from workspace_logic import (
        compose_extracted_logic, extract_typed_logic, proof_artifacts_for_derivations,
        verify_proof_artifact,
    )
    from workspace_mouth import claim_ids, diverge_seed
    from workspace_runtime import EvidenceLedger, ExperimentDesign, rank_discriminating_experiments


def _canonical(payload: dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _checksummed(payload: dict) -> dict:
    row = dict(payload)
    row["sha256"] = hashlib.sha256(_canonical(payload)).hexdigest()
    return row


def _verify_checksummed(row: dict) -> bool:
    try:
        payload = dict(row)
        digest = payload.pop("sha256")
        return isinstance(digest, str) and hashlib.sha256(_canonical(payload)).hexdigest() == digest
    except (TypeError, ValueError):
        return False


def _append_jsonl_locked(path: str, row: dict, dedupe_key: str = "sha256") -> bool:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a+", encoding="utf-8") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        existing = []
        line_no = 0
        needs_separator = False
        while True:
            position = handle.tell()
            line = handle.readline()
            if line == "":
                break
            line_no += 1
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                next_position = handle.tell()
                handle.seek(0, os.SEEK_END)
                at_end = next_position == handle.tell()
                if not line.endswith("\n") and at_end:
                    handle.seek(position)
                    handle.truncate()
                    break
                raise ValueError("corrupt checksummed row %d" % line_no) from exc
            if not _verify_checksummed(item):
                raise ValueError("invalid checksummed row %d" % line_no)
            existing.append(item)
            needs_separator = not line.endswith("\n")
        if any(item.get(dedupe_key) == row.get(dedupe_key) for item in existing):
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            return False
        handle.seek(0, os.SEEK_END)
        if needs_separator:
            handle.write("\n")
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    return True


def _read_checksummed_jsonl(path: str) -> tuple[dict, ...]:
    """Read verified rows and repair only an interrupted final JSON write."""
    if not os.path.exists(path):
        return ()
    rows = []
    with open(path, "r+", encoding="utf-8") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        line_no = 0
        while True:
            position = handle.tell()
            line = handle.readline()
            if line == "":
                break
            line_no += 1
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                next_position = handle.tell()
                handle.seek(0, os.SEEK_END)
                at_end = next_position == handle.tell()
                if not line.endswith("\n") and at_end:
                    handle.seek(position)
                    handle.truncate()
                    handle.flush()
                    os.fsync(handle.fileno())
                    break
                raise ValueError("corrupt checksummed row %d" % line_no) from exc
            if not _verify_checksummed(row):
                raise ValueError("invalid checksummed row %d" % line_no)
            rows.append(row)
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    return tuple(rows)


@dataclass(frozen=True)
class ActiveLoopState:
    candidate_ids: tuple[str, ...]
    rejected_claim_ids: tuple[str, ...]
    supported_claim_ids: tuple[str, ...]
    viable_claim_ids: tuple[str, ...]
    selected_claim_id: str | None
    next_experiment: str | None
    next_information_value: float
    abstained: bool
    reason: str


def candidate_experiment_designs(candidate_ids: Iterable[str]) -> tuple[ExperimentDesign, ...]:
    ids = tuple(candidate_ids)
    return tuple(ExperimentDesign(
        "falsify:" + claim_id,
        tuple((other, "target_fails" if other == claim_id else "target_survives")
              for other in ids),
    ) for claim_id in ids)


def active_falsification_state(seed: str, ledger: EvidenceLedger,
                               *, divergent: bool = True,
                               target_inference: str = "associational",
                               designs: Iterable[ExperimentDesign] = ()) -> ActiveLoopState:
    ids = (tuple(item.spec.claim_id for item in diverge_seed(seed)) if divergent
           else claim_ids(seed))
    resolutions = {claim_id: ledger.resolve(claim_id, target_inference=target_inference)
                   for claim_id in ids}
    rejected = tuple(claim_id for claim_id in ids
                     if resolutions[claim_id].status == "contradicted")
    supported = tuple(claim_id for claim_id in ids
                      if resolutions[claim_id].status == "supported")
    viable = tuple(claim_id for claim_id in ids if claim_id not in rejected)
    selected = supported[0] if supported else (viable[0] if len(viable) == 1 else None)
    pool = tuple(designs) or candidate_experiment_designs(viable)
    ranked = rank_discriminating_experiments(viable, pool) if len(viable) > 1 else ()
    next_experiment = ranked[0][0].name if ranked and ranked[0][1] > 0 else None
    next_value = ranked[0][1] if ranked else 0.0
    abstained = not viable
    reason = ("all_falsified" if abstained else "supported_candidate" if supported
              else "single_survivor" if selected else "experiment_required")
    return ActiveLoopState(ids, rejected, supported, viable, selected,
                           next_experiment, next_value, abstained, reason)


@dataclass(frozen=True)
class IngestResult:
    kind: str
    accepted: bool
    reason: str
    proof_count: int = 0
    evidence_id: str = ""
    status: str = ""


def make_decision_proof(seed: str, divergent: bool, require_evidence: bool,
                        evidence: Iterable[Fact], decision) -> dict:
    payload = {
        "schema": "anima.workspace-decision-proof/v1",
        "seed": seed,
        "divergent": bool(divergent),
        "require_evidence": bool(require_evidence),
        "evidence": [asdict(fact) for fact in evidence],
        "selected_claim_id": getattr(decision, "selected_claim_id", None),
        "rejected_claim_ids": list(getattr(decision, "rejected_claim_ids", ())),
        "abstained": bool(getattr(decision, "abstained", True)),
    }
    return _checksummed(payload)


def verify_decision_proof(proof: dict) -> bool:
    if not _verify_checksummed(proof) or proof.get("schema") != "anima.workspace-decision-proof/v1":
        return False
    try:
        try:
            from .workspace_mouth import decide_seed, select_divergence
        except ImportError:
            from workspace_mouth import decide_seed, select_divergence
        evidence = tuple(Fact(row["subject"], row["relation"], row["object"],
                              tuple(row.get("provenance", ()))) for row in proof["evidence"])
        fn = select_divergence if proof["divergent"] else decide_seed
        decision = fn(proof["seed"], evidence, proof["require_evidence"])
        return (decision is not None
                and decision.selected_claim_id == proof["selected_claim_id"]
                and list(decision.rejected_claim_ids) == proof["rejected_claim_ids"]
                and decision.abstained == proof["abstained"])
    except (KeyError, TypeError, ValueError):
        return False


class WorkspaceProductionSession:
    """Stateful opt-in bridge used by chat without touching substrate state."""

    def __init__(self, directory: str,
                 registry: EvidenceAuthorityRegistry | None = None,
                 target_inference: str = "associational"):
        if not directory:
            raise ValueError("production workspace requires a directory")
        if target_inference not in ("associational", "causal"):
            raise ValueError("invalid target inference")
        self.directory = os.path.abspath(directory)
        os.makedirs(self.directory, exist_ok=True)
        self.registry = registry
        self.target_inference = target_inference
        self.ledger = DurableEvidenceLedger(
            os.path.join(self.directory, "evidence.jsonl"), registry)
        self.logic_path = os.path.join(self.directory, "logic.jsonl")
        self.proof_path = os.path.join(self.directory, "proofs.jsonl")
        self.proof_invalidation_path = os.path.join(
            self.directory, "proof-invalidations.jsonl")
        self.decision_path = os.path.join(self.directory, "decision-proofs.jsonl")
        self.telemetry_path = os.path.join(self.directory, "telemetry.jsonl")
        self.counters = {
            "logic_accepted": 0, "logic_ambiguous": 0, "proofs": 0,
            "proofs_invalidated": 0,
            "evidence_accepted": 0, "evidence_rejected": 0,
            "stat_inconclusive": 0, "active_updates": 0, "decisions": 0,
        }
        self.latest_active_state: ActiveLoopState | None = None

    def _telemetry(self, event: str, **fields) -> None:
        payload = {"schema": "anima.workspace-production-telemetry/v1", "event": event}
        payload.update(fields)
        _append_jsonl_locked(self.telemetry_path, _checksummed(payload))

    def _logic_statements(self) -> tuple[str, ...]:
        statements = []
        for line_no, row in enumerate(_read_checksummed_jsonl(self.logic_path), start=1):
            if row.get("schema") != "anima.workspace-logic/v1":
                raise ValueError("corrupt logic row %d" % line_no)
            statements.append(row["statement"])
        return tuple(statements)

    def _proof_artifacts(self) -> tuple[dict, ...]:
        if not os.path.exists(self.proof_path):
            return ()
        artifacts = []
        with open(self.proof_path, "r+", encoding="utf-8") as handle:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            line_no = 0
            while True:
                position = handle.tell()
                line = handle.readline()
                if line == "":
                    break
                line_no += 1
                if not line.strip():
                    continue
                try:
                    artifact = json.loads(line)
                except json.JSONDecodeError as exc:
                    next_position = handle.tell()
                    handle.seek(0, os.SEEK_END)
                    at_end = next_position == handle.tell()
                    if not line.endswith("\n") and at_end:
                        handle.seek(position)
                        handle.truncate()
                        handle.flush()
                        os.fsync(handle.fileno())
                        break
                    raise ValueError("corrupt proof row %d" % line_no) from exc
                if not verify_proof_artifact(artifact):
                    raise ValueError("invalid proof row %d" % line_no)
                artifacts.append(artifact)
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return tuple(artifacts)

    def ingest(self, percept: str) -> IngestResult:
        text = str(percept).strip()
        if text.startswith("EVIDENCE "):
            try:
                row = json.loads(text[len("EVIDENCE "):])
                if self.registry is None:
                    raise ValueError("no evidence authority registry")
                envelope = EvidenceEnvelope(
                    record=EvidenceRecord(**row["record"]),
                    signature=str(row["signature"]),
                )
                self.ledger.append(envelope)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                self.counters["evidence_rejected"] += 1
                self._telemetry("evidence_rejected", reason=type(exc).__name__)
                return IngestResult("evidence", False, "invalid_or_unauthenticated")
            self.counters["evidence_accepted"] += 1
            self._telemetry("evidence_accepted", evidence_id=envelope.record.evidence_id)
            return IngestResult("evidence", True, "authenticated",
                                evidence_id=envelope.record.evidence_id,
                                status=envelope.record.verdict)
        if text.startswith("MEASUREMENT "):
            try:
                row = json.loads(text[len("MEASUREMENT "):])
                measurement = StatisticalMeasurement(**row["measurement"])
                signature = str(row["signature"])
                if self.registry is None or not self.registry.verify_measurement(
                        measurement, signature):
                    raise ValueError("unauthenticated measurement")
                assessment = assess_statistical_measurement(measurement)
                if assessment.record is None:
                    self.counters["stat_inconclusive"] += 1
                    self._telemetry("measurement_inconclusive", reason=assessment.reason)
                    return IngestResult("measurement", False, assessment.reason,
                                        status=assessment.status)
                envelope = self.registry.sign(assessment.record)
                self.ledger.append(envelope)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                self.counters["evidence_rejected"] += 1
                self._telemetry("measurement_rejected", reason=type(exc).__name__)
                return IngestResult("measurement", False, "invalid_or_unauthenticated")
            self.counters["evidence_accepted"] += 1
            self._telemetry("measurement_accepted", evidence_id=assessment.record.evidence_id,
                            verdict=assessment.record.verdict)
            return IngestResult("measurement", True, assessment.reason,
                                evidence_id=assessment.record.evidence_id,
                                status=assessment.record.verdict)

        extraction = extract_typed_logic(text)
        if extraction.ambiguous:
            self.counters["logic_ambiguous"] += 1
            self._telemetry("logic_ambiguous", reason=extraction.reason)
            return IngestResult("logic", False, extraction.reason)
        existing = self._logic_statements()
        for statement in extraction.statements:
            row = _checksummed({"schema": "anima.workspace-logic/v1",
                                "statement": statement})
            _append_jsonl_locked(self.logic_path, row)
        combined = extract_typed_logic(";".join((*existing, *extraction.statements)))
        workspace = compose_extracted_logic(combined)
        invalidated = 0
        for prior in self._proof_artifacts():
            conclusion = tuple(prior.get("conclusion", ()))
            if (len(conclusion) != 3 or conclusion not in workspace.facts
                    or not workspace.verify_proof(conclusion)):
                event = _checksummed({
                    "schema": "anima.workspace-proof-invalidation/v1",
                    "proof_sha256": prior.get("sha256", ""),
                    "reason": "new_typed_fact_invalidated_conclusion",
                })
                invalidated += int(_append_jsonl_locked(
                    self.proof_invalidation_path, event))
        self.counters["proofs_invalidated"] += invalidated
        proofs = proof_artifacts_for_derivations(workspace)
        before = self.counters["proofs"]
        for proof in proofs:
            self.counters["proofs"] += int(append_proof_artifact(self.proof_path, proof))
        self.counters["logic_accepted"] += 1
        made = self.counters["proofs"] - before
        self._telemetry("logic_accepted", statements=len(extraction.statements),
                        proofs=made, invalidated=invalidated)
        return IngestResult("logic", True, "typed", made)

    def evidence_for(self, seed: str, divergent: bool = True) -> tuple[Fact, ...]:
        if self.registry is None:
            return ()
        loaded = self.ledger.load()
        ids = (tuple(item.spec.claim_id for item in diverge_seed(seed)) if divergent
               else claim_ids(seed))
        return loaded.ledger.resolved_facts(ids, target_inference=self.target_inference)

    def active_state(self, seed: str, divergent: bool = True) -> ActiveLoopState:
        if self.registry is None:
            return active_falsification_state(
                seed, EvidenceLedger(), divergent=divergent,
                target_inference=self.target_inference)
        return active_falsification_state(
            seed, self.ledger.load().ledger, divergent=divergent,
            target_inference=self.target_inference)

    def observe_active_state(self, seed: str, divergent: bool = True) -> ActiveLoopState:
        """Persist only state transitions in the live falsification loop."""
        state = self.active_state(seed, divergent)
        self.latest_active_state = state
        payload = _checksummed({
            "schema": "anima.workspace-active-state/v1",
            "seed_sha256": hashlib.sha256(seed.encode("utf-8")).hexdigest(),
            "divergent": bool(divergent),
            "target_inference": self.target_inference,
            **asdict(state),
        })
        appended = _append_jsonl_locked(self.telemetry_path, payload)
        self.counters["active_updates"] += int(appended)
        return state

    def record_decision(self, seed: str, divergent: bool, require_evidence: bool,
                        evidence: Iterable[Fact], decision) -> dict:
        proof = make_decision_proof(seed, divergent, require_evidence, evidence, decision)
        if not verify_decision_proof(proof):
            raise ValueError("decision proof did not replay")
        _append_jsonl_locked(self.decision_path, proof)
        self.counters["decisions"] += 1
        self._telemetry("decision", abstained=decision.abstained,
                        rejected=len(decision.rejected_claim_ids),
                        selected=decision.selected_claim_id or "")
        return proof

    def checkpoint(self) -> str:
        if self.registry is None and os.path.exists(self.ledger.path):
            raise ValueError("cannot checkpoint evidence without its authority registry")
        return self.ledger.checkpoint()

    def summary(self) -> dict[str, int]:
        return dict(self.counters)
