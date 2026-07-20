"""Controlled natural-language extraction and portable workspace proof artifacts.

This is intentionally a small, fail-closed grammar.  It extracts only structures
whose scope is explicit; unmatched or mixed statements are never guessed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
import hashlib
import json
import re
from typing import Iterable

try:
    from .cognitive_workspace import (
        CognitiveWorkspace, CompositionRule, ConjunctiveRule, DisjunctiveRule,
        ExceptionRule, ExclusiveRule, Fact, QuantifiedRule, UnaryRule,
    )
except ImportError:
    from cognitive_workspace import (
        CognitiveWorkspace, CompositionRule, ConjunctiveRule, DisjunctiveRule,
        ExceptionRule, ExclusiveRule, Fact, QuantifiedRule, UnaryRule,
    )


Rule = (CompositionRule | ConjunctiveRule | DisjunctiveRule | ExceptionRule
        | ExclusiveRule | QuantifiedRule | UnaryRule)


@dataclass(frozen=True)
class LogicExtraction:
    facts: tuple[Fact, ...]
    rules: tuple[Rule, ...]
    statements: tuple[str, ...]
    ambiguous: bool = False
    reason: str = ""


def _atom(text: str) -> str:
    clean = re.sub(r"[^\w가-힣:-]+", "_", text.strip().lower(), flags=re.UNICODE)
    return clean.strip("_")


def _class_atom(text: str) -> str:
    atom = _atom(text)
    if atom.endswith("ies") and len(atom) > 3:
        return atom[:-3] + "y"
    if atom.endswith("s") and not atom.endswith(("ss", "us")) and len(atom) > 2:
        return atom[:-1]
    return atom


def _rule_name(prefix: str, statement: str) -> str:
    digest = hashlib.sha256(statement.encode("utf-8")).hexdigest()[:12]
    return "%s:%s" % (prefix, digest)


def _fact(subject: str, relation: str, object_: str, statement: str) -> Fact:
    return Fact(_atom(subject), relation, _atom(object_), ("extract:" + statement,))


def extract_typed_logic(text: str) -> LogicExtraction:
    """Extract a conservative English/Korean controlled-logic subset.

    Multiple statements must be separated by ``;`` or newlines.  One unknown
    statement rejects the whole input so partial parsing cannot silently change
    negation, quantifier, or exception scope.
    """
    statements = tuple(part.strip().rstrip(".") for part in re.split(r"[;\n]+", str(text))
                       if part.strip())
    if not statements:
        return LogicExtraction((), (), (), True, "empty")
    facts: list[Fact] = []
    rules: list[Rule] = []
    for statement in statements:
        lowered = statement.lower().strip()
        match = re.fullmatch(r"all\s+(.+?)\s+are\s+(.+)", lowered)
        if match:
            facts.append(Fact(_class_atom(match.group(1)), "all_imply",
                              _class_atom(match.group(2)), ("extract:" + statement,)))
            rules.append(QuantifiedRule(_rule_name("universal", statement)))
            continue
        match = re.fullmatch(r"모든\s+(.+?)(?:은|는)\s+(.+?)(?:이다|다)", statement)
        if match:
            facts.append(_fact(match.group(1), "all_imply", match.group(2), statement))
            rules.append(QuantifiedRule(_rule_name("universal", statement)))
            continue
        match = re.fullmatch(r"(.+?)\s+is\s+(?:an?\s+)?not\s+not\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "not_not_is", match.group(2), statement))
            rules.append(UnaryRule(_rule_name("double-negation", statement),
                                   "not_not_is", "is"))
            continue
        match = re.fullmatch(r"exactly\s+one\s+of\s+(.+?)\s+or\s+(.+?)\s+implies\s+(.+)", lowered)
        if match:
            rules.append(ExclusiveRule(_rule_name("xor", statement),
                                       "xor_left", "xor_right", "implies"))
            continue
        match = re.fullmatch(r"only\s+(.+?),\s*not\s+(.+?),\s*implies\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "xor_left", match.group(3), statement))
            rules.append(ExclusiveRule(_rule_name("xor", statement),
                                       "xor_left", "xor_right", "implies"))
            continue
        match = re.fullmatch(r"(.+?)\s+and\s+(.+?)\s+imply\s+(.+)", lowered)
        if match:
            facts.extend((_fact(match.group(1), "and_left", match.group(3), statement),
                          _fact(match.group(2), "and_right", match.group(3), statement)))
            rules.append(ConjunctiveRule(_rule_name("and", statement),
                                         "and_left", "and_right", "implies"))
            continue
        match = re.fullmatch(r"(.+?)\s+or\s+(.+?)\s+imply\s+(.+)", lowered)
        if match:
            facts.extend((_fact(match.group(1), "or_left", match.group(3), statement),
                          _fact(match.group(2), "or_right", match.group(3), statement)))
            rules.append(DisjunctiveRule(_rule_name("or", statement),
                                         "or_left", "or_right", "implies"))
            continue
        match = re.fullmatch(r"(.+?)\s+그리고\s+(.+?)(?:이면|라면)\s+(.+)", statement)
        if match:
            facts.extend((_fact(match.group(1), "and_left", match.group(3), statement),
                          _fact(match.group(2), "and_right", match.group(3), statement)))
            rules.append(ConjunctiveRule(_rule_name("and", statement),
                                         "and_left", "and_right", "implies"))
            continue
        match = re.fullmatch(r"(.+?)\s+또는\s+(.+?)(?:이면|라면)\s+(.+)", statement)
        if match:
            facts.extend((_fact(match.group(1), "or_left", match.group(3), statement),
                          _fact(match.group(2), "or_right", match.group(3), statement)))
            rules.append(DisjunctiveRule(_rule_name("or", statement),
                                         "or_left", "or_right", "implies"))
            continue
        match = re.fullmatch(r"normally\s+(.+?)\s+implies\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "normally_implies", match.group(2), statement))
            rules.append(ExceptionRule(_rule_name("exception", statement),
                                       "normally_implies", "has_exception", "implies"))
            continue
        match = re.fullmatch(r"(.+?)\s+has\s+no\s+exception\s+to\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "has_no_exception", match.group(2), statement))
            continue
        match = re.fullmatch(r"(.+?)\s+has\s+(?:an?\s+)?exception\s+to\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "has_exception", match.group(2), statement))
            continue
        match = re.fullmatch(r"(.+?)\s+before\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "before", match.group(2), statement))
            rules.append(CompositionRule("before-transitive", "before", "before", "before"))
            continue
        match = re.fullmatch(r"(.+?)\s+전에\s+(.+)", statement)
        if match:
            facts.append(_fact(match.group(1), "before", match.group(2), statement))
            rules.append(CompositionRule("before-transitive", "before", "before", "before"))
            continue
        match = re.fullmatch(r"(.+?)\s+is\s+an?\s+(.+)", lowered)
        if match:
            facts.append(Fact(_atom(match.group(1)), "is_a", _class_atom(match.group(2)),
                              ("extract:" + statement,)))
            rules.append(QuantifiedRule("universal-instantiation"))
            continue
        match = re.fullmatch(r"(.+?)(?:은|는)\s+(.+?)(?:이다|다)", statement)
        if match:
            facts.append(_fact(match.group(1), "is_a", match.group(2), statement))
            rules.append(QuantifiedRule("universal-instantiation"))
            continue
        match = re.fullmatch(r"(.+?)\s+implies\s+(.+)", lowered)
        if match:
            facts.append(_fact(match.group(1), "implies", match.group(2), statement))
            continue
        return LogicExtraction((), (), statements, True,
                               "unrecognized_or_ambiguous:" + statement)
    unique_rules = []
    seen_rules = set()
    for rule in rules:
        key = (type(rule).__name__, tuple(asdict(rule).items()))
        if key not in seen_rules:
            seen_rules.add(key)
            unique_rules.append(rule)
    return LogicExtraction(tuple(facts), tuple(unique_rules), statements)


def compose_extracted_logic(extraction: LogicExtraction) -> CognitiveWorkspace:
    if extraction.ambiguous:
        raise ValueError("ambiguous logic extraction: " + extraction.reason)
    workspace = CognitiveWorkspace()
    workspace.add_facts(extraction.facts)
    if extraction.rules:
        workspace.compose_until_stable(extraction.rules)
    return workspace


def _rule_spec(rule: Rule) -> dict:
    return {"type": type(rule).__name__,
            "params": {item.name: getattr(rule, item.name) for item in fields(rule)}}


_RULE_TYPES = {
    cls.__name__: cls for cls in (
        CompositionRule, ConjunctiveRule, DisjunctiveRule, ExceptionRule,
        ExclusiveRule, QuantifiedRule, UnaryRule,
    )
}


def _rule_from_spec(spec: dict) -> Rule:
    cls = _RULE_TYPES.get(spec.get("type"))
    params = spec.get("params")
    if cls is None or not isinstance(params, dict):
        raise ValueError("unknown proof rule")
    return cls(**params)


def make_proof_artifact(workspace: CognitiveWorkspace,
                        conclusion: Fact | tuple[str, str, str]) -> dict:
    key = conclusion.key if isinstance(conclusion, Fact) else conclusion
    if not workspace.verify_proof(key):
        raise ValueError("cannot persist an invalid proof")
    steps = workspace.proof_for(key)
    fact_keys = {step.conclusion for step in steps}
    rule_names = {step.rule_name for step in steps if not step.is_axiom}
    payload = {
        "schema": "anima.workspace-proof/v1",
        "conclusion": list(key),
        "facts": [asdict(workspace.facts[fact_key]) for fact_key in sorted(fact_keys)],
        "steps": [asdict(step) for step in steps],
        "rules": [_rule_spec(workspace.rule_catalog[name]) for name in sorted(rule_names)],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    payload["sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def verify_proof_artifact(artifact: dict) -> bool:
    try:
        payload = dict(artifact)
        digest = payload.pop("sha256")
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")).encode("utf-8")
        if not isinstance(digest, str) or not hashlib.sha256(canonical).hexdigest() == digest:
            return False
        if payload.get("schema") != "anima.workspace-proof/v1":
            return False
        workspace = CognitiveWorkspace()
        step_rows = payload["steps"]
        axiom_keys = {tuple(row["conclusion"]) for row in step_rows
                      if row["rule_name"] == "axiom"}
        facts = {tuple(row[key] for key in ("subject", "relation", "object")):
                 Fact(row["subject"], row["relation"], row["object"],
                      tuple(row.get("provenance", ()))) for row in payload["facts"]}
        workspace.add_facts(facts[key] for key in axiom_keys)
        rules = tuple(_rule_from_spec(spec) for spec in payload["rules"])
        if rules:
            workspace.compose_until_stable(rules)
        conclusion = tuple(payload["conclusion"])
        return conclusion in workspace.facts and workspace.verify_proof(conclusion)
    except (KeyError, TypeError, ValueError):
        return False


def proof_artifacts_for_derivations(workspace: CognitiveWorkspace) -> tuple[dict, ...]:
    return tuple(make_proof_artifact(workspace, fact) for fact in workspace.derivations
                 if workspace.verify_proof(fact))
