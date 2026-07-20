"""Typed-workspace wrapper for a model mouth.

Atomic prompts remain byte-identical to the wrapped mouth. Compound prompts are
parsed into two clauses, composed in the typed workspace, and realized as an
explicit measurable hypothesis. No benchmark concept table is embedded here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

try:
    from .cognitive_workspace import CognitiveWorkspace, CompositionRule, Fact
except ImportError:
    from cognitive_workspace import CognitiveWorkspace, CompositionRule, Fact


_STRUCTURAL = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "if",
    "in", "is", "it", "of", "on", "or", "still", "the", "then", "to", "when",
}


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def split_compound(seed: str) -> tuple[str, ...] | None:
    clean = seed.strip().rstrip(":").strip()
    match = re.match(r"^if\s+(.+?),\s*then\s+(.+)$", clean, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
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


def claim_ids(seed: str) -> tuple[str, str]:
    """Stable public IDs used by typed evidence anchors."""
    return _claim_id(seed, 0), _claim_id(seed, 1)


@dataclass(frozen=True)
class WorkspaceDecision:
    text: str
    candidate_claim_ids: tuple[str, str]
    selected_claim_id: str | None
    rejected_claim_ids: tuple[str, ...]
    abstained: bool


def decide_seed(seed: str, evidence: Iterable[Fact] = ()) -> WorkspaceDecision | None:
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
    primary = proposition
    alternative = Fact(
        proposition.subject,
        "does_not_interact_with",
        proposition.object,
        proposition.provenance + ("counter-hypothesis",),
    )
    workspace.add_facts([alternative])
    workspace.add_facts(evidence)
    claims = []
    for index, candidate in enumerate((primary, alternative)):
        falsifier = Fact(ids[index], "has_verdict", "contradicted")
        claims.append(workspace.propose(candidate, [falsifier]))
    try:
        selected = workspace.select(claims)
    except RuntimeError:
        return WorkspaceDecision(
            text="insufficient grounded evidence",
            candidate_claim_ids=ids,
            selected_claim_id=None,
            rejected_claim_ids=ids,
            abstained=True,
        )
    comparator, measure = _realizer_axes(proposition.subject, proposition.object)
    selected_index = 0 if selected is claims[0] else 1
    if selected_index == 0:
        text = proposition.subject + " " + comparator + " " + proposition.object + " " + measure
    else:
        text = proposition.subject + " decreases " + proposition.object + " " + measure
    rejected = tuple(ids[i] for i, claim in enumerate(claims) if claim.status.value == "falsified")
    return WorkspaceDecision(text, ids, ids[selected_index], rejected, False)


def compose_seed(seed: str, evidence: Iterable[Fact] = ()) -> str | None:
    decision = decide_seed(seed, evidence)
    return None if decision is None else decision.text


class TypedWorkspaceMouth:
    """Drop-in ``ideate`` wrapper; atomic calls delegate without alteration."""

    def __init__(self, mouth, evidence: Iterable[Fact] = ()):
        self.mouth = mouth
        self.evidence = tuple(evidence)
        self.decisions: list[WorkspaceDecision] = []

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        decision = decide_seed(seed, self.evidence)
        if decision is None:
            return self.mouth.ideate(seed, gen, top_k, temp, seed_rng)
        self.decisions.append(decision)
        return decision.text
