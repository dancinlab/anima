"""Typed-workspace wrapper for a model mouth.

Atomic prompts remain byte-identical to the wrapped mouth. Compound prompts are
parsed into two clauses, composed in the typed workspace, and realized as an
explicit measurable hypothesis. No benchmark concept table is embedded here.
"""

from __future__ import annotations

import re

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


def compose_seed(seed: str) -> str | None:
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
    falsifier = Fact(
        proposition.subject + " + " + proposition.object,
        "measured_interaction",
        "not_higher_than_control",
        ("preregistered:falsifier",),
    )
    claim = workspace.propose(proposition, [falsifier])
    workspace.select([claim])
    comparator, measure = _realizer_axes(proposition.subject, proposition.object)
    return proposition.subject + " " + comparator + " " + proposition.object + " " + measure


class TypedWorkspaceMouth:
    """Drop-in ``ideate`` wrapper; atomic calls delegate without alteration."""

    def __init__(self, mouth):
        self.mouth = mouth

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        composed = compose_seed(seed)
        if composed is None:
            return self.mouth.ideate(seed, gen, top_k, temp, seed_rng)
        return composed
