"""Runtime retrieval, measurement evidence, grounding, and identity controls."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Iterable

try:
    from .cognitive_workspace import Fact
    from .workspace_adapters import load_fact_anchors, write_fact_anchor
except ImportError:
    from cognitive_workspace import Fact
    from workspace_adapters import load_fact_anchors, write_fact_anchor


class TypedFactStore:
    """Exact typed retrieval; no prose reinterpretation or benchmark pair table."""

    def __init__(self, facts: Iterable[Fact] = ()):
        self._facts = {fact.key: fact for fact in facts}

    @classmethod
    def load(cls, directory: str) -> "TypedFactStore":
        return cls(load_fact_anchors(directory))

    def put(self, fact: Fact) -> None:
        self._facts[fact.key] = fact

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

    def evidence(self) -> Fact:
        if self.direction not in ("above", "not_above"):
            raise ValueError("direction must be above or not_above")
        above = self.observed > self.control
        supported = above if self.direction == "above" else not above
        verdict = "supported" if supported else "contradicted"
        return Fact(self.claim_id, "has_verdict", verdict, (self.source,))


def collect_measurement_evidence(measurements: Iterable[Measurement]) -> tuple[Fact, ...]:
    """Convert actual numeric comparisons to the sole accepted verdict spelling."""
    return tuple(measurement.evidence() for measurement in measurements)


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
