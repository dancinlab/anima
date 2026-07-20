"""Authenticated statistics, causal guards, and durable workspace ledgers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import hmac
import json
import math
import os
from statistics import NormalDist
import tempfile
from typing import Iterable

try:
    import fcntl
except ImportError:  # pragma: no cover - production targets are POSIX
    fcntl = None

try:
    from .workspace_runtime import EvidenceLedger, EvidenceRecord
except ImportError:
    from workspace_runtime import EvidenceLedger, EvidenceRecord


def _canonical_record(record: EvidenceRecord) -> bytes:
    return json.dumps(asdict(record), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class ExperimentRegistration:
    experiment_id: str
    claim_id: str
    source: str
    context: str
    target_inference: str = "associational"
    intervention: str = ""
    outcome: str = ""

    def __post_init__(self) -> None:
        if not all((self.experiment_id, self.claim_id, self.source, self.context)):
            raise ValueError("registered experiment requires id, claim, source, and context")
        if self.target_inference not in ("associational", "causal"):
            raise ValueError("invalid registered target inference")


@dataclass(frozen=True)
class EvidenceEnvelope:
    record: EvidenceRecord
    signature: str


class EvidenceAuthorityRegistry:
    """HMAC source authentication plus a preregistered experiment allow-list."""

    def __init__(self, source_keys: dict[str, bytes],
                 experiments: Iterable[ExperimentRegistration]):
        if not source_keys or any(not key for key in source_keys.values()):
            raise ValueError("at least one non-empty source key is required")
        self.source_keys = dict(source_keys)
        experiment_rows = tuple(experiments)
        self.experiments = {item.experiment_id: item for item in experiment_rows}
        if len(self.experiments) != len(experiment_rows):
            raise ValueError("duplicate experiment registration")

    @classmethod
    def from_json(cls, path: str) -> "EvidenceAuthorityRegistry":
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        sources = raw.get("sources", {})
        keys = {}
        for source, config in sources.items():
            if not isinstance(config, dict) or not isinstance(config.get("key_env"), str):
                raise ValueError("source keys must reference a key_env")
            value = os.environ.get(config["key_env"], "")
            if not value:
                raise ValueError("missing source key environment variable")
            keys[str(source)] = value.encode("utf-8")
        experiments = tuple(ExperimentRegistration(**row)
                            for row in raw.get("experiments", ()))
        return cls(keys, experiments)

    def sign(self, record: EvidenceRecord) -> EvidenceEnvelope:
        registration = self._registration_for(record)
        key = self.source_keys.get(registration.source)
        if key is None:
            raise ValueError("untrusted evidence source")
        signature = hmac.new(key, _canonical_record(record), hashlib.sha256).hexdigest()
        return EvidenceEnvelope(record, signature)

    def _registration_for(self, record: EvidenceRecord) -> ExperimentRegistration:
        registration = self.experiments.get(record.experiment_id)
        if registration is None:
            raise ValueError("unregistered experiment_id")
        if (registration.claim_id, registration.source, registration.context) != (
                record.claim_id, record.source, record.context):
            raise ValueError("evidence does not match its experiment registration")
        if registration.target_inference == "causal" and (
                record.study_type != "interventional" or not record.randomized):
            raise ValueError("registered causal evidence must be randomized and interventional")
        return registration

    def verify(self, envelope: EvidenceEnvelope) -> bool:
        try:
            registration = self._registration_for(envelope.record)
            key = self.source_keys[registration.source]
            expected = hmac.new(key, _canonical_record(envelope.record),
                                hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected, envelope.signature)
        except (KeyError, ValueError):
            return False

    def _measurement_registration(self, measurement) -> ExperimentRegistration:
        registration = self.experiments.get(measurement.experiment_id)
        if registration is None:
            raise ValueError("unregistered experiment_id")
        if (registration.claim_id, registration.source, registration.context) != (
                measurement.claim_id, measurement.source, measurement.context):
            raise ValueError("measurement does not match its experiment registration")
        if registration.target_inference == "causal" and (
                measurement.study_type != "interventional" or not measurement.randomized):
            raise ValueError("registered causal measurement must be randomized and interventional")
        return registration

    def sign_measurement(self, measurement: "StatisticalMeasurement") -> str:
        """Source-side helper; production ingestion accepts only this signed payload."""
        registration = self._measurement_registration(measurement)
        key = self.source_keys.get(registration.source)
        if key is None:
            raise ValueError("untrusted measurement source")
        return hmac.new(key, _canonical_measurement(measurement), hashlib.sha256).hexdigest()

    def verify_measurement(self, measurement: "StatisticalMeasurement",
                           signature: str) -> bool:
        try:
            registration = self._measurement_registration(measurement)
            key = self.source_keys[registration.source]
            expected = hmac.new(key, _canonical_measurement(measurement),
                                hashlib.sha256).hexdigest()
            return isinstance(signature, str) and hmac.compare_digest(expected, signature)
        except (KeyError, ValueError):
            return False

    def missing_registered_experiments(self,
                                       records: Iterable[EvidenceRecord]) -> tuple[str, ...]:
        observed = {record.experiment_id for record in records}
        return tuple(sorted(set(self.experiments) - observed))


@dataclass(frozen=True)
class StatisticalMeasurement:
    claim_id: str
    treatment_mean: float
    control_mean: float
    treatment_sd: float
    control_sd: float
    treatment_n: int
    control_n: int
    direction: str
    source: str
    observed_at: str
    experiment_id: str
    context: str = "default"
    study_type: str = "observational"
    randomized: bool = False
    control_valid: bool = True
    missing: bool = False
    evidence_id: str = ""

    def __post_init__(self) -> None:
        numeric = (self.treatment_mean, self.control_mean,
                   self.treatment_sd, self.control_sd)
        if any(isinstance(value, bool) or not isinstance(value, (int, float))
               or not math.isfinite(value) for value in numeric):
            raise ValueError("statistical values must be finite numbers")
        if self.treatment_sd < 0 or self.control_sd < 0:
            raise ValueError("standard deviations cannot be negative")
        if (isinstance(self.treatment_n, bool) or isinstance(self.control_n, bool)
                or not isinstance(self.treatment_n, int)
                or not isinstance(self.control_n, int)
                or self.treatment_n < 2 or self.control_n < 2):
            raise ValueError("both groups require at least two observations")
        if self.direction not in ("above", "below"):
            raise ValueError("direction must be above or below")


def _canonical_measurement(measurement: StatisticalMeasurement) -> bytes:
    return json.dumps(asdict(measurement), ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


@dataclass(frozen=True)
class StatisticalAssessment:
    status: str
    difference: float
    standard_error: float
    ci_low: float
    ci_high: float
    standardized_effect: float
    reason: str
    record: EvidenceRecord | None = None


@dataclass(frozen=True)
class StratifiedResult:
    treatment_mean: float
    control_mean: float
    treatment_n: int
    control_n: int


def detects_simpsons_paradox(strata: Iterable[StratifiedResult]) -> bool:
    """Detect an aggregate sign reversal when every reported stratum agrees."""
    rows = tuple(strata)
    if len(rows) < 2:
        return False
    differences = [row.treatment_mean - row.control_mean for row in rows]
    if any(value == 0 for value in differences) or not (
            all(value > 0 for value in differences)
            or all(value < 0 for value in differences)):
        return False
    treatment_n = sum(row.treatment_n for row in rows)
    control_n = sum(row.control_n for row in rows)
    if treatment_n <= 0 or control_n <= 0:
        raise ValueError("stratified sample sizes must be positive")
    treatment = sum(row.treatment_mean * row.treatment_n for row in rows) / treatment_n
    control = sum(row.control_mean * row.control_n for row in rows) / control_n
    aggregate = treatment - control
    return aggregate != 0 and (aggregate > 0) != (differences[0] > 0)


def assess_statistical_measurement(measurement: StatisticalMeasurement,
                                   confidence: float = 0.95) -> StatisticalAssessment:
    if not (0.5 < confidence < 1.0):
        raise ValueError("confidence must be between 0.5 and 1")
    difference = measurement.treatment_mean - measurement.control_mean
    variance = ((measurement.treatment_sd ** 2) / measurement.treatment_n
                + (measurement.control_sd ** 2) / measurement.control_n)
    standard_error = math.sqrt(variance)
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    half_width = z * standard_error
    low, high = difference - half_width, difference + half_width
    pooled_denom = measurement.treatment_n + measurement.control_n - 2
    pooled_var = (((measurement.treatment_n - 1) * measurement.treatment_sd ** 2
                   + (measurement.control_n - 1) * measurement.control_sd ** 2)
                  / pooled_denom)
    pooled_sd = math.sqrt(pooled_var) if pooled_var > 0 else 0.0
    effect = difference / pooled_sd if pooled_sd > 0 else 0.0
    if measurement.missing or not measurement.control_valid:
        status, reason = "INCONCLUSIVE", "missing_or_invalid_control"
    elif standard_error == 0:
        status, reason = "INCONCLUSIVE", "zero_variance"
    elif measurement.direction == "above" and low > 0:
        status, reason = "supported", "confidence_interval_above_control"
    elif measurement.direction == "above" and high <= 0:
        status, reason = "contradicted", "confidence_interval_not_above_control"
    elif measurement.direction == "below" and high < 0:
        status, reason = "supported", "confidence_interval_below_control"
    elif measurement.direction == "below" and low >= 0:
        status, reason = "contradicted", "confidence_interval_not_below_control"
    else:
        status, reason = "INCONCLUSIVE", "confidence_interval_crosses_control"
    record = None
    if status in ("supported", "contradicted"):
        evidence_id = measurement.evidence_id
        if not evidence_id:
            digest = hashlib.sha256(json.dumps(
                asdict(measurement), sort_keys=True, separators=(",", ":")
            ).encode("utf-8")).hexdigest()[:20]
            evidence_id = "stat-" + digest
        record = EvidenceRecord(
            evidence_id=evidence_id, claim_id=measurement.claim_id,
            verdict=status, source=measurement.source,
            observed_at=measurement.observed_at,
            experiment_id=measurement.experiment_id, context=measurement.context,
            sample_size=measurement.treatment_n + measurement.control_n,
            # Keep uncertainty in the same standardized units as the effect.
            # The evidence policy can then compare studies measured on different
            # physical scales without dividing by the observed effect itself.
            uncertainty=half_width / pooled_sd if pooled_sd > 0 else half_width,
            control_valid=measurement.control_valid, missing=measurement.missing,
            study_type=measurement.study_type, randomized=measurement.randomized,
        )
    return StatisticalAssessment(status, difference, standard_error, low, high,
                                 effect, reason, record)


@dataclass(frozen=True)
class CausalGraph:
    edges: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if any(len(edge) != 2 or not edge[0] or not edge[1] for edge in self.edges):
            raise ValueError("causal edges require two non-empty nodes")
        if self.has_cycle():
            raise ValueError("causal graph must be acyclic")

    def has_cycle(self) -> bool:
        children: dict[str, set[str]] = {}
        nodes = set()
        for source, target in self.edges:
            children.setdefault(source, set()).add(target)
            nodes.update((source, target))
        visiting, visited = set(), set()

        def visit(node):
            if node in visiting:
                return True
            if node in visited:
                return False
            visiting.add(node)
            if any(visit(child) for child in children.get(node, ())):
                return True
            visiting.remove(node)
            visited.add(node)
            return False

        return any(visit(node) for node in nodes)

    def direct_confounders(self, cause: str, effect: str) -> tuple[str, ...]:
        parents_cause = {source for source, target in self.edges if target == cause}
        parents_effect = {source for source, target in self.edges if target == effect}
        return tuple(sorted(parents_cause & parents_effect))

    def intervention_identified(self, cause: str, effect: str,
                                adjusted_for: Iterable[str] = (),
                                randomized: bool = False) -> bool:
        if randomized:
            return True
        return set(self.direct_confounders(cause, effect)).issubset(set(adjusted_for))


def _envelope_row(envelope: EvidenceEnvelope) -> dict:
    payload = {"schema": "anima.workspace-evidence-envelope/v1",
               "record": asdict(envelope.record), "signature": envelope.signature}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    payload["sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def _row_envelope(row: dict) -> EvidenceEnvelope:
    payload = dict(row)
    digest = payload.pop("sha256")
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    if payload.get("schema") != "anima.workspace-evidence-envelope/v1":
        raise ValueError("unknown durable ledger schema")
    if not hmac.compare_digest(hashlib.sha256(canonical).hexdigest(), str(digest)):
        raise ValueError("durable ledger checksum mismatch")
    return EvidenceEnvelope(EvidenceRecord(**payload["record"]), payload["signature"])


@dataclass(frozen=True)
class DurableLedgerLoad:
    ledger: EvidenceLedger
    envelopes: tuple[EvidenceEnvelope, ...]
    recovered_trailing_partial: bool = False


class DurableEvidenceLedger:
    """Locked, checksummed JSONL. A torn final write is recoverable; interior damage is not."""

    def __init__(self, path: str, registry: EvidenceAuthorityRegistry | None = None):
        self.path = path
        self.registry = registry

    def load(self) -> DurableLedgerLoad:
        if not os.path.exists(self.path):
            return DurableLedgerLoad(EvidenceLedger(), ())
        envelopes = []
        recovered = False
        with open(self.path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
        for index, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                envelope = _row_envelope(json.loads(line))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                if index == len(lines) - 1 and not line.endswith("\n"):
                    recovered = True
                    break
                raise ValueError("corrupt durable ledger row %d" % (index + 1)) from exc
            if self.registry is not None and not self.registry.verify(envelope):
                raise ValueError("unauthenticated durable ledger row %d" % (index + 1))
            envelopes.append(envelope)
        return DurableLedgerLoad(EvidenceLedger(item.record for item in envelopes),
                                 tuple(envelopes), recovered)

    def append(self, envelope: EvidenceEnvelope) -> None:
        if self.registry is not None and not self.registry.verify(envelope):
            raise ValueError("refusing unauthenticated evidence")
        directory = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(directory, exist_ok=True)
        with open(self.path, "a+", encoding="utf-8") as handle:
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
                    existing_envelope = _row_envelope(json.loads(line))
                except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                    next_position = handle.tell()
                    handle.seek(0, os.SEEK_END)
                    at_end = next_position == handle.tell()
                    if not line.endswith("\n") and at_end:
                        handle.seek(position)
                        handle.truncate()
                        break
                    raise ValueError("cannot append after corrupt row %d" % line_no) from exc
                if self.registry is not None and not self.registry.verify(existing_envelope):
                    raise ValueError("cannot append after unauthenticated row %d" % line_no)
                existing.append(existing_envelope)
                needs_separator = not line.endswith("\n")
            ledger = EvidenceLedger(item.record for item in existing)
            ledger.append(envelope.record)
            row = _envelope_row(envelope)
            handle.seek(0, os.SEEK_END)
            if needs_separator:
                handle.write("\n")
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def checkpoint(self, path: str | None = None) -> str:
        """Atomically snapshot resolutions while leaving append-only history untouched."""
        loaded = self.load()
        claim_ids = sorted({item.record.claim_id for item in loaded.envelopes})
        payload = {
            "schema": "anima.workspace-evidence-checkpoint/v1",
            "ledger_path": os.path.basename(self.path),
            "record_count": len(loaded.envelopes),
            "history_root": hashlib.sha256(b"".join(
                _canonical_record(item.record) for item in loaded.envelopes)).hexdigest(),
            "resolutions": {claim_id: asdict(loaded.ledger.resolve(claim_id))
                            for claim_id in claim_ids},
        }
        target = path or self.path + ".checkpoint.json"
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".workspace-checkpoint-",
                                         dir=os.path.dirname(os.path.abspath(target)))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return target


def append_proof_artifact(path: str, artifact: dict) -> bool:
    try:
        from .workspace_logic import verify_proof_artifact
    except ImportError:
        from workspace_logic import verify_proof_artifact
    if not verify_proof_artifact(artifact):
        raise ValueError("refusing invalid proof artifact")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a+", encoding="utf-8") as handle:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        hashes = set()
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
                existing = json.loads(line)
            except json.JSONDecodeError as exc:
                next_position = handle.tell()
                handle.seek(0, os.SEEK_END)
                at_end = next_position == handle.tell()
                if not line.endswith("\n") and at_end:
                    handle.seek(position)
                    handle.truncate()
                    break
                raise ValueError("corrupt proof artifact row %d" % line_no) from exc
            if not verify_proof_artifact(existing):
                raise ValueError("invalid proof artifact row %d" % line_no)
            hashes.add(existing.get("sha256"))
            needs_separator = not line.endswith("\n")
        if artifact["sha256"] not in hashes:
            handle.seek(0, os.SEEK_END)
            if needs_separator:
                handle.write("\n")
            handle.write(json.dumps(artifact, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            appended = True
        else:
            appended = False
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    return appended
