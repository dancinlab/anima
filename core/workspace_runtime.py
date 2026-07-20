"""Runtime retrieval, measurement evidence, grounding, and identity controls."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import hashlib
import json
import math
import os
import re
from typing import Iterable, Sequence

try:
    from .cognitive_workspace import Fact
    from .workspace_adapters import load_fact_anchors, write_fact_anchor
except ImportError:
    from cognitive_workspace import Fact
    from workspace_adapters import load_fact_anchors, write_fact_anchor


class TypedFactStore:
    """Exact typed retrieval; no prose reinterpretation or benchmark pair table."""

    def __init__(self, facts: Iterable[Fact] = ()):
        self._facts: dict[tuple[str, str, str], Fact] = {}
        for fact in facts:
            self.put(fact)

    @classmethod
    def load(cls, directory: str) -> "TypedFactStore":
        return cls(load_fact_anchors(directory))

    def put(self, fact: Fact) -> None:
        existing = self._facts.get(fact.key)
        provenance = (fact.provenance if existing is None else
                      tuple(dict.fromkeys((*existing.provenance, *fact.provenance))))
        self._facts[fact.key] = Fact(*fact.key, provenance)

    def persist(self, directory: str, name: str, fact: Fact) -> str:
        self.put(fact)
        return write_fact_anchor(directory, name, fact)

    def query(self, subject: str, relation: str) -> tuple[Fact, ...]:
        return tuple(
            fact for fact in self._facts.values()
            if fact.subject == subject and fact.relation == relation
        )

    def exact(self, subject: str, relation: str, object_: str) -> Fact | None:
        return self._facts.get((subject, relation, object_))


_PERSISTABLE_FACT = re.compile(
    r"^FACT\s+([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*$",
    re.IGNORECASE,
)


def parse_persistable_fact(text: str, source: str = "external-percept") -> Fact | None:
    """Parse an explicitly typed declaration; ordinary prose always stays inert."""
    match = _PERSISTABLE_FACT.match(str(text).strip())
    if match is None:
        return None
    subject, relation, object_ = (part.strip() for part in match.groups())
    if not all((subject, relation, object_)):
        return None
    return Fact(subject, relation, object_, (source,))


def persist_workspace_fact(directory: str, text: str,
                           source: str = "external-percept") -> str | None:
    """Persist one explicit FACT declaration under a content-derived stable name."""
    if not directory:
        return None
    fact = parse_persistable_fact(text, source)
    if fact is None:
        return None
    digest = hashlib.sha256("\0".join(fact.key).encode("utf-8")).hexdigest()[:20]
    return TypedFactStore().persist(directory, "workspace-fact-" + digest, fact)


@dataclass(frozen=True)
class Measurement:
    claim_id: str
    observed: float
    control: float
    direction: str = "above"
    source: str = "measurement"
    observed_at: str = ""
    experiment_id: str = ""
    context: str = "default"
    sample_size: int = 0
    uncertainty: float = 1.0
    control_valid: bool = True
    missing: bool = False
    study_type: str = "observational"
    randomized: bool = False
    evidence_id: str = ""
    supersedes: str = ""
    retracted: bool = False

    def evidence(self) -> Fact:
        if self.direction not in ("above", "not_above"):
            raise ValueError("direction must be above or not_above")
        above = self.observed > self.control
        supported = above if self.direction == "above" else not above
        verdict = "supported" if supported else "contradicted"
        provenance = (self.source,) + (("observed_at=" + self.observed_at,)
                                       if self.observed_at else ())
        return Fact(self.claim_id, "has_verdict", verdict, provenance)

    def evidence_record(self) -> "EvidenceRecord":
        fact = self.evidence()
        experiment_id = self.experiment_id or self.source
        evidence_id = self.evidence_id
        if not evidence_id:
            payload = "\0".join((self.claim_id, fact.object, self.source,
                                  self.observed_at, experiment_id, self.context,
                                  str(self.observed), str(self.control)))
            evidence_id = "evidence-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]
        return EvidenceRecord(
            evidence_id=evidence_id,
            claim_id=self.claim_id,
            verdict=fact.object,
            source=self.source,
            observed_at=self.observed_at,
            experiment_id=experiment_id,
            context=self.context,
            sample_size=self.sample_size,
            uncertainty=self.uncertainty,
            control_valid=self.control_valid,
            missing=self.missing,
            study_type=self.study_type,
            randomized=self.randomized,
            supersedes=self.supersedes,
            retracted=self.retracted,
        )


def _parse_observed_at(value: str) -> datetime:
    if not value:
        raise ValueError("ledger evidence requires observed_at")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("observed_at must include a timezone")
    return parsed


@dataclass(frozen=True)
class EvidenceRecord:
    """Append-only experimental evidence with explicit quality and lineage."""

    evidence_id: str
    claim_id: str
    verdict: str
    source: str
    observed_at: str
    experiment_id: str
    context: str = "default"
    sample_size: int = 0
    uncertainty: float = 1.0
    control_valid: bool = True
    missing: bool = False
    study_type: str = "observational"
    randomized: bool = False
    supersedes: str = ""
    retracted: bool = False

    def __post_init__(self) -> None:
        string_fields = (self.evidence_id, self.claim_id, self.source, self.observed_at,
                         self.experiment_id, self.context, self.verdict, self.study_type,
                         self.supersedes)
        if any(not isinstance(value, str) for value in string_fields):
            raise ValueError("evidence string fields must be strings")
        if not all((self.evidence_id, self.claim_id, self.source,
                    self.experiment_id, self.context)):
            raise ValueError("evidence identity, claim, source, experiment, and context are required")
        if self.verdict not in ("supported", "contradicted"):
            raise ValueError("evidence verdict must be supported or contradicted")
        _parse_observed_at(self.observed_at)
        if isinstance(self.sample_size, bool) or not isinstance(self.sample_size, int):
            raise ValueError("sample_size must be an integer")
        if self.sample_size < 0:
            raise ValueError("sample_size cannot be negative")
        if (isinstance(self.uncertainty, bool)
                or not isinstance(self.uncertainty, (int, float))
                or not math.isfinite(self.uncertainty) or self.uncertainty < 0):
            raise ValueError("uncertainty must be finite and non-negative")
        if any(type(value) is not bool for value in (
                self.control_valid, self.missing, self.randomized, self.retracted)):
            raise ValueError("evidence control flags must be booleans")
        if self.study_type not in ("observational", "interventional"):
            raise ValueError("study_type must be observational or interventional")
        if self.retracted and not self.supersedes:
            raise ValueError("a retraction must identify the superseded evidence")

    def as_fact(self, resolution: str = "direct") -> Fact:
        provenance = (
            "evidence_id=" + self.evidence_id,
            "source=" + self.source,
            "observed_at=" + self.observed_at,
            "experiment_id=" + self.experiment_id,
            "context=" + self.context,
            "resolution=" + resolution,
        )
        return Fact(self.claim_id, "has_verdict", self.verdict, provenance)


@dataclass(frozen=True)
class EvidencePolicy:
    min_sample_size: int = 30
    max_uncertainty: float = 0.20
    min_conflict_winner_experiments: int = 2
    min_conflict_winner_sources: int = 2

    def __post_init__(self) -> None:
        integer_thresholds = (self.min_sample_size,
                              self.min_conflict_winner_experiments,
                              self.min_conflict_winner_sources)
        if (any(isinstance(value, bool) or not isinstance(value, int)
                for value in integer_thresholds)
                or isinstance(self.max_uncertainty, bool)
                or not isinstance(self.max_uncertainty, (int, float))
                or not math.isfinite(self.max_uncertainty)
                or self.min_sample_size < 1 or self.max_uncertainty < 0
                or self.min_conflict_winner_experiments < 2
                or self.min_conflict_winner_sources < 2):
            raise ValueError("evidence policy thresholds must be positive and conflict-safe")


@dataclass(frozen=True)
class EvidenceResolution:
    claim_id: str
    status: str
    reason: str
    accepted_evidence_ids: tuple[str, ...] = ()
    excluded_evidence_ids: tuple[str, ...] = ()
    context: str = ""


class EvidenceLedger:
    """Append-only ledger; corrections never mutate history and latest never wins by itself."""

    def __init__(self, records: Iterable[EvidenceRecord] = ()):
        self.records: list[EvidenceRecord] = []
        for record in records:
            self.append(record)

    def append(self, record: EvidenceRecord) -> None:
        known = {item.evidence_id: item for item in self.records}
        if record.evidence_id in known:
            raise ValueError("duplicate evidence_id: " + record.evidence_id)
        if record.supersedes:
            target = known.get(record.supersedes)
            if target is None:
                raise ValueError("superseded evidence does not exist: " + record.supersedes)
            if any(item.supersedes == record.supersedes for item in self.records):
                raise ValueError("evidence was already superseded: " + record.supersedes)
            if (record.claim_id, record.experiment_id, record.context) != (
                    target.claim_id, target.experiment_id, target.context):
                raise ValueError("correction/retraction cannot cross claim, experiment, or context")
        self.records.append(record)

    def active_records(self) -> tuple[EvidenceRecord, ...]:
        superseded = {item.supersedes for item in self.records if item.supersedes}
        return tuple(item for item in self.records
                     if item.evidence_id not in superseded and not item.retracted)

    @staticmethod
    def _eligible(record: EvidenceRecord, policy: EvidencePolicy,
                  target_inference: str) -> bool:
        if record.missing or not record.control_valid:
            return False
        if record.sample_size < policy.min_sample_size:
            return False
        if record.uncertainty > policy.max_uncertainty:
            return False
        if target_inference == "causal" and (
                record.study_type != "interventional" or not record.randomized):
            return False
        return True

    def resolve(self, claim_id: str, policy: EvidencePolicy = EvidencePolicy(),
                target_inference: str = "associational") -> EvidenceResolution:
        if target_inference not in ("associational", "causal"):
            raise ValueError("target_inference must be associational or causal")
        historical = [item for item in self.records if item.claim_id == claim_id]
        active = [item for item in self.active_records() if item.claim_id == claim_id]
        if not active:
            return EvidenceResolution(
                claim_id, "INCONCLUSIVE" if historical else "UNGROUNDED",
                "all_retracted" if historical else "no_evidence",
                excluded_evidence_ids=tuple(item.evidence_id for item in historical))
        contexts = {item.context for item in active}
        if len(contexts) != 1:
            return EvidenceResolution(
                claim_id, "UNGROUNDED", "incomparable_contexts",
                excluded_evidence_ids=tuple(item.evidence_id for item in active))
        eligible = [item for item in active
                    if self._eligible(item, policy, target_inference)]
        excluded = [item.evidence_id for item in active if item not in eligible]
        if not eligible:
            return EvidenceResolution(
                claim_id, "INCONCLUSIVE", "quality_gate",
                excluded_evidence_ids=tuple(excluded), context=next(iter(contexts)))

        experiments: dict[str, list[EvidenceRecord]] = {}
        for item in eligible:
            experiments.setdefault(item.experiment_id, []).append(item)
        experiment_verdicts: dict[str, str] = {}
        for experiment_id, items in experiments.items():
            verdicts = {item.verdict for item in items}
            if len(verdicts) != 1:
                return EvidenceResolution(
                    claim_id, "UNGROUNDED", "within_experiment_conflict",
                    excluded_evidence_ids=tuple(item.evidence_id for item in eligible),
                    context=next(iter(contexts)))
            experiment_verdicts[experiment_id] = next(iter(verdicts))

        counts = {verdict: sum(value == verdict for value in experiment_verdicts.values())
                  for verdict in ("supported", "contradicted")}
        present = [verdict for verdict, count in counts.items() if count]
        if len(present) == 1:
            winner = present[0]
            reason = "consistent_quality_evidence"
        else:
            if counts["supported"] == counts["contradicted"]:
                return EvidenceResolution(
                    claim_id, "UNGROUNDED", "tied_cross_experiment_conflict",
                    excluded_evidence_ids=tuple(item.evidence_id for item in eligible),
                    context=next(iter(contexts)))
            winner = max(counts, key=counts.get)
            winner_items = [item for item in eligible if item.verdict == winner]
            if (counts[winner] < policy.min_conflict_winner_experiments
                    or len({item.source for item in winner_items})
                    < policy.min_conflict_winner_sources):
                return EvidenceResolution(
                    claim_id, "UNGROUNDED", "insufficient_independent_replication",
                    excluded_evidence_ids=tuple(item.evidence_id for item in eligible),
                    context=next(iter(contexts)))
            reason = "replicated_majority"
        accepted = tuple(item.evidence_id for item in eligible if item.verdict == winner)
        dissent = tuple(item.evidence_id for item in eligible if item.verdict != winner)
        return EvidenceResolution(
            claim_id, winner, reason, accepted, tuple((*excluded, *dissent)),
            next(iter(contexts)))

    def resolved_facts(self, claim_ids: Iterable[str],
                       policy: EvidencePolicy = EvidencePolicy(),
                       target_inference: str = "associational") -> tuple[Fact, ...]:
        facts = []
        active = {item.evidence_id: item for item in self.active_records()}
        for claim_id in claim_ids:
            resolution = self.resolve(claim_id, policy, target_inference)
            if resolution.status not in ("supported", "contradicted"):
                continue
            records = [active[evidence_id] for evidence_id in resolution.accepted_evidence_ids]
            provenance = tuple(dict.fromkeys(
                value for record in records
                for value in record.as_fact(resolution.reason).provenance))
            facts.append(Fact(claim_id, "has_verdict", resolution.status, provenance))
        return tuple(facts)


def persist_evidence_ledger(path: str, records: Iterable[EvidenceRecord]) -> str:
    """Append records to a JSONL ledger after validating it as one history."""
    target = os.path.join(path, "workspace-evidence-ledger.jsonl") if os.path.isdir(path) else path
    existing = load_evidence_ledger(target) if os.path.exists(target) else EvidenceLedger()
    pending = tuple(records)
    for record in pending:
        existing.append(record)
    with open(target, "a", encoding="utf-8") as handle:
        for record in pending:
            handle.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n")
    return target


def load_evidence_ledger(path: str) -> EvidenceLedger:
    target = os.path.join(path, "workspace-evidence-ledger.jsonl") if os.path.isdir(path) else path
    records = []
    with open(target, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(EvidenceRecord(**json.loads(line)))
            except (AttributeError, TypeError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError("invalid evidence ledger row %d in %s" % (line_no, target)) from exc
    return EvidenceLedger(records)


def collect_measurement_evidence(measurements: Iterable[Measurement]) -> tuple[Fact, ...]:
    """Convert actual numeric comparisons to the sole accepted verdict spelling."""
    return tuple(measurement.evidence() for measurement in measurements)


def resolve_evidence_verdicts(evidence: Iterable[Fact]) -> dict[str, str]:
    """Resolve typed claim verdicts; any support/contradiction conflict abstains."""
    grouped: dict[str, set[str]] = {}
    for fact in evidence:
        if fact.relation != "has_verdict" or fact.object not in ("supported", "contradicted"):
            continue
        grouped.setdefault(fact.subject, set()).add(fact.object)
    return {
        claim_id: (next(iter(verdicts)) if len(verdicts) == 1 else "UNGROUNDED")
        for claim_id, verdicts in grouped.items()
    }


def effective_evidence(evidence: Iterable[Fact]) -> tuple[Fact, ...]:
    """Return only non-conflicting typed verdicts while retaining provenance."""
    facts = tuple(evidence)
    verdicts = resolve_evidence_verdicts(facts)
    out = []
    for claim_id, verdict in verdicts.items():
        if verdict == "UNGROUNDED":
            continue
        matching = [fact for fact in facts if fact.subject == claim_id
                    and fact.relation == "has_verdict" and fact.object == verdict]
        provenance = tuple(dict.fromkeys(
            source for fact in matching for source in fact.provenance
        ))
        out.append(Fact(claim_id, "has_verdict", verdict, provenance))
    return tuple(out)


def persist_measurement_evidence(directory: str,
                                 measurements: Iterable[Measurement]) -> tuple[str, ...]:
    """Persist source/time-bearing measurement verdicts for a later process."""
    paths = []
    for fact in collect_measurement_evidence(measurements):
        raw = "\0".join((*fact.key, *fact.provenance)).encode("utf-8")
        name = "workspace-evidence-" + hashlib.sha256(raw).hexdigest()[:20]
        paths.append(write_fact_anchor(directory, name, fact))
    return tuple(paths)


@dataclass(frozen=True)
class MeasurementDecision:
    decision: object
    evidence: tuple[Fact, ...]
    verdicts: dict[str, str]


@dataclass(frozen=True)
class LedgerDecision:
    decision: object
    evidence: tuple[Fact, ...]
    resolutions: dict[str, EvidenceResolution]


def measurement_ledger_step(seed: str, measurements: Iterable[Measurement],
                            *, divergent: bool = False,
                            require_evidence: bool = True,
                            policy: EvidencePolicy = EvidencePolicy(),
                            target_inference: str = "associational") -> LedgerDecision:
    """Resolve quality-controlled history, then expose only its effective verdicts."""
    records = tuple(measurement.evidence_record() for measurement in measurements)
    ledger = EvidenceLedger(records)
    try:
        from .workspace_mouth import claim_ids, decide_seed, diverge_seed, select_divergence
    except ImportError:
        from workspace_mouth import claim_ids, decide_seed, diverge_seed, select_divergence
    ids = (tuple(item.spec.claim_id for item in diverge_seed(seed)) if divergent
           else claim_ids(seed))
    resolutions = {claim_id: ledger.resolve(claim_id, policy, target_inference)
                   for claim_id in ids}
    evidence = ledger.resolved_facts(ids, policy, target_inference)
    decision = (select_divergence(seed, evidence, require_evidence) if divergent
                else decide_seed(seed, evidence, require_evidence))
    return LedgerDecision(decision, evidence, resolutions)


@dataclass(frozen=True)
class ExperimentDesign:
    """Preregistered candidate predictions for one possible experiment."""

    name: str
    predictions: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not self.name or not self.predictions:
            raise ValueError("experiment design requires a name and predictions")
        if len({claim_id for claim_id, _ in self.predictions}) != len(self.predictions):
            raise ValueError("experiment design repeats a claim_id")

    def information_value(self, candidate_ids: Sequence[str]) -> float:
        """Expected bits removed under a uniform candidate prior."""
        candidates = tuple(candidate_ids)
        if not candidates:
            return 0.0
        prediction = dict(self.predictions)
        if any(claim_id not in prediction for claim_id in candidates):
            return 0.0
        groups: dict[str, int] = {}
        for claim_id in candidates:
            outcome = prediction[claim_id]
            groups[outcome] = groups.get(outcome, 0) + 1
        prior = math.log(len(candidates), 2)
        remaining = sum((size / len(candidates)) * math.log(size, 2)
                        for size in groups.values())
        return prior - remaining


def rank_discriminating_experiments(candidate_ids: Sequence[str],
                                    designs: Iterable[ExperimentDesign]
                                    ) -> tuple[tuple[ExperimentDesign, float], ...]:
    """Rank experiments by candidate separation; deterministic name breaks ties."""
    scored = [(design, design.information_value(candidate_ids)) for design in designs]
    return tuple(sorted(scored, key=lambda item: (-item[1], item[0].name)))


def measurement_falsification_step(seed: str, measurements: Iterable[Measurement],
                                   *, divergent: bool = False,
                                   require_evidence: bool = True) -> MeasurementDecision:
    """Complete measured G6 loop: compare, type evidence, reject, select alternative."""
    evidence = collect_measurement_evidence(measurements)
    if divergent:
        try:
            from .workspace_mouth import select_divergence
        except ImportError:
            from workspace_mouth import select_divergence
        decision = select_divergence(seed, evidence, require_evidence)
    else:
        try:
            from .workspace_mouth import decide_seed
        except ImportError:
            from workspace_mouth import decide_seed
        decision = decide_seed(seed, evidence, require_evidence)
    return MeasurementDecision(decision, evidence, resolve_evidence_verdicts(evidence))


def load_measurement_evidence(path: str) -> tuple[Fact, ...]:
    """Read numeric JSONL measurements; malformed or content-free rows fail closed."""
    measurements = []
    with open(path, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            try:
                measurements.append(Measurement(
                    claim_id=str(row["claim_id"]),
                    observed=float(row["observed"]),
                    control=float(row["control"]),
                    direction=str(row.get("direction", "above")),
                    source=str(row.get("source", "%s:%d" % (path, line_no))),
                    observed_at=str(row.get("observed_at", "")),
                ))
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError("invalid measurement row %d in %s" % (line_no, path)) from exc
    return collect_measurement_evidence(measurements)


def grounded_answer(store: TypedFactStore, subject: str, relation: str) -> str:
    """Truth-tether boundary: one grounded value or explicit abstention."""
    hits = store.query(subject, relation)
    values = tuple(dict.fromkeys(f.object for f in hits))
    return values[0] if len(values) == 1 else "UNGROUNDED"


@dataclass(frozen=True)
class GroundedDecision:
    text: str
    selected_claim_id: str | None
    rejected_claim_ids: tuple[str, ...] = ()
    abstained: bool = False
    subject: str = ""
    relation: str = ""


def grounded_query_step(out_text: str, query: str, facts: Iterable[Fact] = ()):
    """Answer `subject|relation` only from a unique typed store record."""
    if "|" not in query:
        raise ValueError("--workspace-query must be subject|relation")
    subject, relation = (part.strip() for part in query.split("|", 1))
    if not subject or not relation:
        raise ValueError("--workspace-query requires non-empty subject and relation")
    answer = grounded_answer(TypedFactStore(facts), subject, relation)
    abstained = answer == "UNGROUNDED"
    decision = GroundedDecision(
        answer, None if abstained else "%s|%s" % (subject, relation),
        (), abstained, subject, relation,
    )
    return decision.text, decision


def identity_control(store: TypedFactStore, self_id: str, expected: str,
                     shuffled_id: str) -> dict[str, bool]:
    """ON/OFF/shuffle identity measurement without persona inference."""
    relation = "has_identity_anchor"
    return {
        "on": store.exact(self_id, relation, expected) is not None,
        "off": TypedFactStore().exact(self_id, relation, expected) is not None,
        "shuffle": store.exact(shuffled_id, relation, expected) is not None,
    }


def auto_workspace_mode(seed: str) -> str:
    """Route only genuine compound inputs; atomic/empty inputs stay exactly off."""
    try:
        from .workspace_mouth import split_compound
    except ImportError:
        from workspace_mouth import split_compound
    return "divergent" if seed.strip() and split_compound(seed) is not None else "off"


def resolve_workspace_input(requested_mode: str, explicit_seed: str,
                            percept_text: str | None = None) -> tuple[str, str]:
    """Resolve one tick without letting atomic percepts activate the workspace.

    An explicit seed always wins. In ``auto`` mode only, the current external
    percept becomes the seed when no explicit seed was supplied. This keeps the
    no-percept and atomic-percept paths exactly OFF while allowing real user text
    to enter without a duplicate ``--workspace-seed`` flag.
    """
    seed = explicit_seed.strip()
    if not seed and requested_mode == "auto" and percept_text:
        seed = str(percept_text).strip()
    mode = auto_workspace_mode(seed) if requested_mode == "auto" else requested_mode
    return mode, seed


def spoken_workspace_step(out_text: str, seed: str, evidence: Iterable[Fact] = (),
                          require_evidence: bool = False):
    """Pure spoken seam used by chat; callers retain all substrate state unchanged."""
    try:
        from .workspace_mouth import decide_seed
    except ImportError:
        from workspace_mouth import decide_seed
    decision = decide_seed(seed or out_text, evidence, require_evidence)
    return (out_text, None) if decision is None else (decision.text, decision)


def spoken_divergence_step(out_text: str, seed: str, evidence: Iterable[Fact] = (),
                           require_evidence: bool = False):
    """Pure six-lens select/reject seam for the opt-in divergent chat mode."""
    try:
        from .workspace_mouth import select_divergence
    except ImportError:
        from workspace_mouth import select_divergence
    decision = select_divergence(seed or out_text, evidence, require_evidence)
    return (out_text, None) if decision is None else (decision.text, decision)
