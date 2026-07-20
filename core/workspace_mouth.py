"""Typed-workspace wrapper for a model mouth.

Atomic prompts remain byte-identical to the wrapped mouth. Compound prompts are
parsed into two clauses, composed in the typed workspace, and realized as an
explicit measurable hypothesis. No benchmark concept table is embedded here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Iterable

try:
    from .cognitive_workspace import CognitiveWorkspace, CompositionRule, Fact
except ImportError:
    from cognitive_workspace import CognitiveWorkspace, CompositionRule, Fact


_STRUCTURAL = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "if",
    "in", "is", "it", "of", "on", "or", "still", "the", "then", "to", "when",
    "만약", "이면", "라면", "그러면", "그리고", "또는", "은", "는", "이", "가", "을", "를",
}


def _words(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE)


def split_compound(seed: str) -> tuple[str, ...] | None:
    clean = seed.strip().rstrip(":").strip()
    match = re.match(r"^if\s+(.+?),\s*then\s+(.+)$", clean, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    ko = re.match(
        r"^만약\s+(.+?)(?:이면|라면|으면|면)\s*[,，]?\s*(?:그러면\s+)?(.+)$", clean
    )
    if ko:
        return ko.group(1).strip(), ko.group(2).strip()
    clauses = [part.strip() for part in re.split(r"\.\s+", clean) if part.strip()]
    if len(clauses) >= 2:
        return tuple(clauses)
    return None


def _operand(clause: str) -> str:
    content = list(dict.fromkeys(w for w in _words(clause) if w not in _STRUCTURAL))
    if not content:
        raise ValueError("compound clause has no content operand")
    # A compact symbolic handle prevents the realizer boilerplate from dominating
    # pairwise diversity. Selection is lexical and domain-independent.
    # Korean morphology often expresses negation/condition in a middle token (오지 않다).
    # Dropping it flips the proposition, so preserve the full short clause.
    if any(any(ord(ch) > 127 for ch in word) for word in content):
        return " ".join(content)
    return " ".join(content if len(content) <= 2 else (content[0], content[-1]))


def _realizer_axes(left: str, right: str) -> tuple[str, str]:
    comparators = ("predicts", "correlates", "causes", "increases", "decreases", "depends")
    measures = ("score", "rate", "frequency", "strength", "level", "ratio")
    raw = (left + "|" + right).encode("utf-8", "surrogateescape")
    h = 2166136261
    for byte in raw:
        h = ((h ^ byte) * 16777619) & 0xFFFFFFFF
    return comparators[h % len(comparators)], measures[(h // len(comparators)) % len(measures)]


def _claim_id(seed: str, candidate: int) -> str:
    raw = (seed.strip() + "|" + str(candidate)).encode("utf-8", "surrogateescape")
    h = 2166136261
    for byte in raw:
        h = ((h ^ byte) * 16777619) & 0xFFFFFFFF
    return "workspace-claim-%08x-%d" % (h, candidate)


def claim_ids(seed: str) -> tuple[str, str, str]:
    """Stable public IDs used by typed evidence anchors."""
    return _claim_id(seed, 0), _claim_id(seed, 1), _claim_id(seed, 2)


@dataclass(frozen=True)
class HypothesisSpec:
    claim_id: str
    measure: str
    control: str
    falsified_when: str


@dataclass(frozen=True)
class WorkspaceDecision:
    text: str
    candidate_claim_ids: tuple[str, ...]
    candidate_specs: tuple[HypothesisSpec, ...]
    selected_claim_id: str | None
    rejected_claim_ids: tuple[str, ...]
    abstained: bool
    required_terms: tuple[str, ...]
    realized_by: str = "workspace"
    realizer_valid: bool = True


def decide_seed(seed: str, evidence: Iterable[Fact] = (),
                require_evidence: bool = False) -> WorkspaceDecision | None:
    clauses = split_compound(seed)
    if clauses is None:
        return None
    operands = [_operand(clause) for clause in clauses]
    workspace = CognitiveWorkspace()
    accumulated = operands[0]
    provenance = ("seed:0",)
    proposition = None
    for index, operand in enumerate(operands[1:], start=1):
        bridge = "workspace:interaction:" + str(index)
        left = Fact(accumulated, "enters", bridge, provenance)
        right = Fact(bridge, "combines", operand, ("seed:" + str(index),))
        rule = CompositionRule(
            "clause-interaction:" + str(index), "enters", "combines", "interacts_with"
        )
        workspace.add_facts([left, right])
        produced = workspace.compose(rule)
        if len(produced) != 1:
            raise RuntimeError("typed compound did not produce exactly one derivation per rung")
        proposition = produced[0]
        accumulated = proposition.subject + " " + proposition.object
        provenance = proposition.provenance
    if proposition is None:
        raise RuntimeError("compound requires at least two operands")
    ids = claim_ids(seed)
    comparator, measure = _realizer_axes(proposition.subject, proposition.object)
    specs = tuple(
        HypothesisSpec(
            claim_id=claim_id,
            measure=measure,
            control="each_operand_alone",
            falsified_when=("interaction_not_above_control" if index == 0 else
                            "interaction_above_control" if index == 1 else
                            "measurement_resolves_direction"),
        )
        for index, claim_id in enumerate(ids)
    )
    primary = proposition
    alternative = Fact(
        proposition.subject,
        "does_not_interact_with",
        proposition.object,
        proposition.provenance + ("counter-hypothesis",),
    )
    uncertain = Fact(
        proposition.subject,
        "interaction_direction_unresolved",
        proposition.object,
        proposition.provenance + ("uncertainty-hypothesis",),
    )
    workspace.add_facts([alternative, uncertain])
    evidence = tuple(evidence)
    workspace.add_facts(evidence)
    # The two candidates are an exhaustive positive/non-positive split. A measured
    # contradiction of one side grounds the other side unless it is independently
    # contradicted as well.
    if Fact(ids[0], "has_verdict", "contradicted").key in workspace.facts:
        workspace.add_facts([Fact(ids[1], "has_verdict", "supported", ("binary-complement",))])
    if Fact(ids[1], "has_verdict", "contradicted").key in workspace.facts:
        workspace.add_facts([Fact(ids[0], "has_verdict", "supported", ("binary-complement",))])
    claims = []
    for index, candidate in enumerate((primary, alternative, uncertain)):
        falsifier = Fact(ids[index], "has_verdict", "contradicted")
        grounds = [Fact(ids[index], "has_verdict", "supported")] if require_evidence else []
        claims.append(workspace.propose(candidate, [falsifier], grounds))
    try:
        selected = workspace.select(claims)
    except RuntimeError:
        return WorkspaceDecision(
            text="insufficient grounded evidence",
            candidate_claim_ids=ids,
            candidate_specs=specs,
            selected_claim_id=None,
            rejected_claim_ids=ids,
            abstained=True,
            required_terms=tuple(_words(proposition.subject + " " + proposition.object)),
        )
    selected_index = claims.index(selected)
    if selected_index == 0:
        text = proposition.subject + " " + comparator + " " + proposition.object + " " + measure
    elif selected_index == 1:
        text = proposition.subject + " decreases " + proposition.object + " " + measure
    else:
        text = proposition.subject + " relationship with " + proposition.object + " remains uncertain " + measure
    rejected = tuple(ids[i] for i, claim in enumerate(claims) if claim.status.value == "falsified")
    required = tuple(dict.fromkeys(_words(proposition.subject + " " + proposition.object)))
    return WorkspaceDecision(text, ids, specs, ids[selected_index], rejected, False, required)


def compose_seed(seed: str, evidence: Iterable[Fact] = (),
                 require_evidence: bool = False) -> str | None:
    decision = decide_seed(seed, evidence, require_evidence)
    return None if decision is None else decision.text


class TypedWorkspaceMouth:
    """Drop-in ``ideate`` wrapper; atomic calls delegate without alteration."""

    def __init__(self, mouth, evidence: Iterable[Fact] = (), require_evidence: bool = False,
                 realizer: str = "structured"):
        if realizer not in ("structured", "model"):
            raise ValueError("realizer must be structured or model")
        self.mouth = mouth
        self.evidence = tuple(evidence)
        self.require_evidence = require_evidence
        self.realizer = realizer
        self.decisions: list[WorkspaceDecision] = []

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        decision = decide_seed(seed, self.evidence, self.require_evidence)
        if decision is None:
            return self.mouth.ideate(seed, gen, top_k, temp, seed_rng)
        if self.realizer == "model" and not decision.abstained:
            prompt = ("Structured hypothesis: " + decision.text
                      + ". Restate this hypothesis without changing its operands: ")
            candidate = self.mouth.ideate(prompt, gen, top_k, temp, seed_rng)
            if realization_preserves(decision, candidate):
                decision = replace(decision, text=candidate, realized_by="model", realizer_valid=True)
            else:
                decision = replace(decision, realized_by="workspace_fallback", realizer_valid=False)
        self.decisions.append(decision)
        return decision.text


def realization_preserves(decision: WorkspaceDecision, text: str) -> bool:
    """Fail closed unless the mouth preserves operands and falsifiable structure."""
    words = set(_words(text))
    required = set(decision.required_terms)
    comparator = {"predicts", "correlates", "causes", "increases", "decreases", "depends"}
    measurable = {"score", "rate", "frequency", "strength", "level", "ratio"}
    expected_relation = set(_words(decision.text)) & comparator
    return (required.issubset(words) and bool(words & measurable)
            and bool(expected_relation) and expected_relation.issubset(words))


def realization_training_rows(seeds: Iterable[str]) -> tuple[dict[str, object], ...]:
    """Supervision rows for the mouth; targets are verified structured renderings."""
    rows = []
    for seed in seeds:
        decision = decide_seed(seed)
        if decision is None or decision.abstained:
            continue
        rows.append({
            "prompt": "Structured hypothesis: " + decision.text,
            "target": decision.text,
            "required_terms": list(decision.required_terms),
            "candidate_specs": [spec.__dict__ for spec in decision.candidate_specs],
        })
    return tuple(rows)
