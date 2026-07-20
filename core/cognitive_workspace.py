"""Typed cognitive workspace for explicit composition and falsification.

This module intentionally has no model, decoder, numpy, or torch dependency.  It
is the seam between a future extractor/retriever and the existing CLM mouth:
the mouth receives only a selected claim, never opaque intermediate activations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Sequence


@dataclass(frozen=True, order=True)
class Fact:
    subject: str
    relation: str
    object: str
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.subject or not self.relation or not self.object:
            raise ValueError("a fact requires non-empty subject, relation, and object")

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.subject, self.relation, self.object)


@dataclass(frozen=True)
class CompositionRule:
    """Compose ``A -left-> B`` and ``B -right-> C`` into ``A -out-> C``."""

    name: str
    left_relation: str
    right_relation: str
    output_relation: str

    def apply(self, left: Fact, right: Fact) -> Fact | None:
        if left.relation != self.left_relation:
            return None
        if right.relation != self.right_relation or left.object != right.subject:
            return None
        sources = tuple(dict.fromkeys((*left.provenance, *right.provenance, self.name)))
        return Fact(left.subject, self.output_relation, right.object, sources)


class ClaimStatus(str, Enum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    FALSIFIED = "falsified"
    UNGROUNDED = "ungrounded"
    SELECTED = "selected"


@dataclass
class Claim:
    proposition: Fact
    falsifiers: tuple[Fact, ...]
    status: ClaimStatus = ClaimStatus.PROPOSED
    evidence: tuple[Fact, ...] = ()

    def __post_init__(self) -> None:
        if not self.falsifiers:
            raise ValueError("a claim requires at least one explicit falsifier")


@dataclass
class CognitiveWorkspace:
    """Small deterministic state machine shared by the G1 and G6 paths."""

    facts: dict[tuple[str, str, str], Fact] = field(default_factory=dict)
    derivations: list[Fact] = field(default_factory=list)
    claims: list[Claim] = field(default_factory=list)
    selected: Claim | None = None

    def add_facts(self, facts: Iterable[Fact]) -> None:
        for fact in facts:
            self.facts[fact.key] = fact

    def compose(self, rule: CompositionRule) -> list[Fact]:
        """Run a two-operand join; unary echo cannot create a derivation."""

        snapshot = tuple(self.facts.values())
        produced: list[Fact] = []
        for left in snapshot:
            for right in snapshot:
                result = rule.apply(left, right)
                if result is None or result.key in self.facts:
                    continue
                self.facts[result.key] = result
                self.derivations.append(result)
                produced.append(result)
        return produced

    def propose(self, proposition: Fact, falsifiers: Sequence[Fact]) -> Claim:
        claim = Claim(proposition, tuple(falsifiers))
        self.claims.append(claim)
        return claim

    def test(self, claim: Claim) -> ClaimStatus:
        """Ground a claim and test its preregistered counterexamples."""

        hits = tuple(self.facts[f.key] for f in claim.falsifiers if f.key in self.facts)
        claim.evidence = hits
        if hits:
            claim.status = ClaimStatus.FALSIFIED
        elif claim.proposition.key in self.facts:
            claim.status = ClaimStatus.SUPPORTED
        else:
            claim.status = ClaimStatus.UNGROUNDED
        return claim.status

    def select(self, claims: Sequence[Claim] | None = None) -> Claim:
        pool = tuple(self.claims if claims is None else claims)
        viable = [claim for claim in pool if self.test(claim) is ClaimStatus.SUPPORTED]
        if not viable:
            raise RuntimeError("no grounded, non-falsified claim is selectable")
        self.selected = viable[0]
        self.selected.status = ClaimStatus.SELECTED
        return self.selected

    def render_for_mouth(self) -> str:
        """Serialize only a selected typed result; generation is outside this core."""

        if self.selected is None or self.selected.status is not ClaimStatus.SELECTED:
            raise RuntimeError("mouth is gated until a claim is selected")
        fact = self.selected.proposition
        return f"{fact.subject} {fact.relation} {fact.object}"
