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
class ProofStep:
    """One independently replayable edge in a typed derivation DAG."""

    conclusion: tuple[str, str, str]
    rule_name: str
    premises: tuple[tuple[str, str, str], ...] = ()

    @property
    def is_axiom(self) -> bool:
        return self.rule_name == "axiom"


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


@dataclass(frozen=True)
class ConjunctiveRule:
    """Require two distinct incoming relations to the same typed object."""

    name: str
    left_relation: str
    right_relation: str
    output_relation: str

    def apply(self, left: Fact, right: Fact) -> Fact | None:
        if left.relation != self.left_relation or right.relation != self.right_relation:
            return None
        if left.object != right.object or left.subject == right.subject:
            return None
        sources = tuple(dict.fromkeys((*left.provenance, *right.provenance, self.name)))
        subject = left.subject + " & " + right.subject
        return Fact(subject, self.output_relation, left.object, sources)


@dataclass(frozen=True)
class DisjunctiveRule:
    """Derive from either explicitly named relation (inclusive OR)."""

    name: str
    left_relation: str
    right_relation: str
    output_relation: str

    def applications(self, facts: Sequence[Fact]):
        for fact in facts:
            if fact.relation in (self.left_relation, self.right_relation):
                branch = "or:" + fact.relation
                yield (Fact(fact.subject, self.output_relation, fact.object,
                            tuple(dict.fromkeys((*fact.provenance, self.name, branch)))),
                       (fact,))

    def validate(self, premises: Sequence[Fact], conclusion: Fact) -> bool:
        if len(premises) != 1:
            return False
        fact = premises[0]
        return (fact.relation in (self.left_relation, self.right_relation)
                and conclusion.key == (fact.subject, self.output_relation, fact.object))


@dataclass(frozen=True)
class ExclusiveRule:
    """Derive only when exactly one of two alternatives is present (XOR)."""

    name: str
    left_relation: str
    right_relation: str
    output_relation: str

    def applications(self, facts: Sequence[Fact]):
        grouped: dict[tuple[str, str], list[Fact]] = {}
        for fact in facts:
            if fact.relation in (self.left_relation, self.right_relation):
                grouped.setdefault((fact.subject, fact.object), []).append(fact)
        for (subject, object_), matches in grouped.items():
            relations = {fact.relation for fact in matches}
            if len(relations) != 1:
                continue
            premise = matches[0]
            yield (Fact(subject, self.output_relation, object_,
                        tuple(dict.fromkeys((*premise.provenance, self.name,
                                            "xor:" + premise.relation)))),
                   (premise,))

    def validate(self, premises: Sequence[Fact], conclusion: Fact) -> bool:
        if len(premises) != 1:
            return False
        fact = premises[0]
        return (fact.relation in (self.left_relation, self.right_relation)
                and conclusion.key == (fact.subject, self.output_relation, fact.object))

    def validate_in_workspace(self, premises: Sequence[Fact], conclusion: Fact,
                              facts: dict[tuple[str, str, str], Fact]) -> bool:
        if not self.validate(premises, conclusion):
            return False
        premise = premises[0]
        other = (self.right_relation if premise.relation == self.left_relation
                 else self.left_relation)
        return (premise.subject, other, premise.object) not in facts


@dataclass(frozen=True)
class ExceptionRule:
    """Apply a default only with explicit clearance and no typed exception."""

    name: str
    base_relation: str
    exception_relation: str
    output_relation: str
    clearance_relation: str = "has_no_exception"

    def applications(self, facts: Sequence[Fact]):
        blocked = {(fact.subject, fact.object) for fact in facts
                   if fact.relation == self.exception_relation}
        clearances = {(fact.subject, fact.object): fact for fact in facts
                      if fact.relation == self.clearance_relation}
        for fact in facts:
            if (fact.relation == self.base_relation
                    and (fact.subject, fact.object) not in blocked
                    and (fact.subject, fact.object) in clearances):
                clearance = clearances[(fact.subject, fact.object)]
                yield (Fact(fact.subject, self.output_relation, fact.object,
                            tuple(dict.fromkeys((*fact.provenance,
                                                *clearance.provenance, self.name)))),
                       (fact, clearance))

    def validate(self, premises: Sequence[Fact], conclusion: Fact) -> bool:
        if len(premises) != 2:
            return False
        fact, clearance = premises
        return (fact.relation == self.base_relation
                and clearance.relation == self.clearance_relation
                and (fact.subject, fact.object) == (clearance.subject, clearance.object)
                and conclusion.key == (fact.subject, self.output_relation, fact.object))

    def validate_in_workspace(self, premises: Sequence[Fact], conclusion: Fact,
                              facts: dict[tuple[str, str, str], Fact]) -> bool:
        return (self.validate(premises, conclusion)
                and (conclusion.subject, self.exception_relation, conclusion.object)
                not in facts)


@dataclass(frozen=True)
class UnaryRule:
    """Explicit unary rewrite, used for scoped double-negation elimination."""

    name: str
    input_relation: str
    output_relation: str

    def applications(self, facts: Sequence[Fact]):
        for fact in facts:
            if fact.relation == self.input_relation:
                yield (Fact(fact.subject, self.output_relation, fact.object,
                            tuple(dict.fromkeys((*fact.provenance, self.name)))),
                       (fact,))

    def validate(self, premises: Sequence[Fact], conclusion: Fact) -> bool:
        if len(premises) != 1:
            return False
        fact = premises[0]
        return (fact.relation == self.input_relation
                and conclusion.key == (fact.subject, self.output_relation, fact.object))


@dataclass(frozen=True)
class QuantifiedRule:
    """Apply a universal type implication to one explicitly typed member."""

    name: str
    membership_relation: str = "is_a"
    universal_relation: str = "all_imply"
    output_relation: str = "is_a"

    def applications(self, facts: Sequence[Fact]):
        members = [fact for fact in facts if fact.relation == self.membership_relation]
        universals = [fact for fact in facts if fact.relation == self.universal_relation]
        for member in members:
            for universal in universals:
                if member.object != universal.subject:
                    continue
                provenance = tuple(dict.fromkeys(
                    (*member.provenance, *universal.provenance, self.name)))
                yield (Fact(member.subject, self.output_relation, universal.object, provenance),
                       (member, universal))

    def validate(self, premises: Sequence[Fact], conclusion: Fact) -> bool:
        if len(premises) != 2:
            return False
        member, universal = premises
        return (member.relation == self.membership_relation
                and universal.relation == self.universal_relation
                and member.object == universal.subject
                and conclusion.key == (member.subject, self.output_relation, universal.object))


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
    grounds: tuple[Fact, ...] = ()
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
    proofs: dict[tuple[str, str, str], ProofStep] = field(default_factory=dict)
    rule_catalog: dict[str, object] = field(default_factory=dict)

    def add_facts(self, facts: Iterable[Fact]) -> None:
        for fact in facts:
            existing = self.facts.get(fact.key)
            if existing is None:
                self.facts[fact.key] = fact
                self.proofs.setdefault(fact.key, ProofStep(fact.key, "axiom"))
            else:
                provenance = tuple(dict.fromkeys((*existing.provenance, *fact.provenance)))
                self.facts[fact.key] = Fact(*fact.key, provenance)

    def _record_derivation(self, result: Fact, rule, premises: Sequence[Fact],
                           produced: list[Fact]) -> None:
        if result.key in self.facts:
            return
        self.facts[result.key] = result
        self.derivations.append(result)
        self.proofs[result.key] = ProofStep(
            result.key, rule.name, tuple(fact.key for fact in premises))
        produced.append(result)

    def compose(self, rule) -> list[Fact]:
        """Run one typed rule and record every newly derived proof edge."""

        snapshot = tuple(self.facts.values())
        produced: list[Fact] = []
        self.rule_catalog[rule.name] = rule
        applications = getattr(rule, "applications", None)
        if applications is not None:
            for result, premises in applications(snapshot):
                self._record_derivation(result, rule, premises, produced)
            return produced
        for left in snapshot:
            for right in snapshot:
                result = rule.apply(left, right)
                if result is None:
                    continue
                self._record_derivation(result, rule, (left, right), produced)
        return produced

    def compose_until_stable(self, rules: Sequence[object],
                             max_rounds: int = 64) -> tuple[Fact, ...]:
        """Apply a rule set to closure, terminating even for cyclic graphs.

        Facts are keyed triples, so a cycle can derive self-reachability but can
        never grow the store indefinitely. ``max_rounds`` is a fail-closed guard
        against a future rule type that violates that finite-closure invariant.
        """
        if not rules:
            raise ValueError("composition closure requires at least one rule")
        if max_rounds <= 0:
            raise ValueError("max_rounds must be positive")
        produced: list[Fact] = []
        for _ in range(max_rounds):
            round_facts = []
            for rule in rules:
                round_facts.extend(self.compose(rule))
            if not round_facts:
                return tuple(produced)
            produced.extend(round_facts)
        raise RuntimeError("composition closure did not stabilize")

    def proof_for(self, fact: Fact | tuple[str, str, str]) -> tuple[ProofStep, ...]:
        """Return a topologically ordered proof slice for one conclusion."""

        key = fact.key if isinstance(fact, Fact) else fact
        if key not in self.proofs:
            raise KeyError("no proof for fact %r" % (key,))
        ordered: list[ProofStep] = []
        visited: set[tuple[str, str, str]] = set()

        def visit(current):
            if current in visited:
                return
            visited.add(current)
            step = self.proofs[current]
            for premise in step.premises:
                visit(premise)
            ordered.append(step)

        visit(key)
        return tuple(ordered)

    def verify_proof(self, fact: Fact | tuple[str, str, str]) -> bool:
        """Replay every proof edge; tampered rules, parents, or conclusions fail closed."""

        try:
            steps = self.proof_for(fact)
        except (KeyError, RecursionError):
            return False
        verified: set[tuple[str, str, str]] = set()
        for step in steps:
            conclusion = self.facts.get(step.conclusion)
            if conclusion is None:
                return False
            if step.is_axiom:
                if step.premises:
                    return False
                verified.add(step.conclusion)
                continue
            rule = self.rule_catalog.get(step.rule_name)
            if rule is None or any(key not in verified for key in step.premises):
                return False
            premises = tuple(self.facts[key] for key in step.premises)
            workspace_validator = getattr(rule, "validate_in_workspace", None)
            validator = getattr(rule, "validate", None)
            if workspace_validator is not None:
                valid = workspace_validator(premises, conclusion, self.facts)
            elif validator is not None:
                valid = validator(premises, conclusion)
            elif len(premises) == 2:
                replayed = rule.apply(*premises)
                valid = replayed is not None and replayed.key == conclusion.key
            else:
                valid = False
            if not valid:
                return False
            verified.add(step.conclusion)
        key = fact.key if isinstance(fact, Fact) else fact
        return key in verified

    def propose(self, proposition: Fact, falsifiers: Sequence[Fact],
                grounds: Sequence[Fact] = ()) -> Claim:
        claim = Claim(proposition, tuple(falsifiers), tuple(grounds))
        self.claims.append(claim)
        return claim

    def test(self, claim: Claim) -> ClaimStatus:
        """Ground a claim and test its preregistered counterexamples."""

        hits = tuple(self.facts[f.key] for f in claim.falsifiers if f.key in self.facts)
        grounding = tuple(self.facts[f.key] for f in claim.grounds if f.key in self.facts)
        claim.evidence = hits + grounding
        if hits and grounding:
            claim.status = ClaimStatus.UNGROUNDED
        elif hits:
            claim.status = ClaimStatus.FALSIFIED
        elif claim.grounds and not grounding:
            claim.status = ClaimStatus.UNGROUNDED
        elif (claim.proposition.key in self.proofs
              and not self.verify_proof(claim.proposition)):
            claim.status = ClaimStatus.UNGROUNDED
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
