"""Production-boundary adapters for :mod:`cognitive_workspace`.

Workspace facts use the existing ``.kosmos`` byte format.  Their text payload is
strict JSON rather than guessed natural-language triples, so extraction cannot
silently turn prose into evidence.
"""

from __future__ import annotations

import json
from typing import Iterable

try:  # package install
    from .cognitive_workspace import CognitiveWorkspace, Fact
    from .kosmos_io import create_anchor, load_anchors
except ImportError:  # repo's historical top-level core import mode
    from cognitive_workspace import CognitiveWorkspace, Fact
    from kosmos_io import create_anchor, load_anchors


WORKSPACE_LANE = "workspace"
WORKSPACE_SCHEMA = "anima.workspace.fact/1"


def encode_fact(fact: Fact) -> str:
    return json.dumps(
        {
            "schema": WORKSPACE_SCHEMA,
            "subject": fact.subject,
            "relation": fact.relation,
            "object": fact.object,
            "provenance": list(fact.provenance),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def decode_fact(payload: str, source: str) -> Fact:
    # kosmos_io.load_anchors intentionally returns the escaped payload spelling
    # (its historical consumers compare text bytes directly). Undo exactly one
    # JSON-string escape layer for workspace records written by encode_fact.
    if isinstance(payload, str) and "\\\"" in payload:
        try:
            payload = json.loads('"' + payload + '"')
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid kosmos escaping from {source}") from exc
    try:
        row = json.loads(payload)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid workspace fact payload from {source}") from exc
    if not isinstance(row, dict) or row.get("schema") != WORKSPACE_SCHEMA:
        raise ValueError(f"unsupported workspace schema from {source}")
    provenance = row.get("provenance", [])
    if not isinstance(provenance, list) or not all(isinstance(x, str) for x in provenance):
        raise ValueError(f"invalid workspace provenance from {source}")
    return Fact(
        str(row.get("subject", "")),
        str(row.get("relation", "")),
        str(row.get("object", "")),
        tuple(dict.fromkeys((*provenance, source))),
    )


def write_fact_anchor(out_dir: str, name: str, fact: Fact) -> str:
    """Persist one typed fact through the canonical kosmos writer."""

    return create_anchor(
        out_dir,
        name,
        f"workspace fact {fact.subject}/{fact.relation}",
        0.0,
        0.0,
        WORKSPACE_LANE,
        1.0,
        2,
        "workspace_fact",
        "grounded",
        encode_fact(fact),
        [0.0] * 5,
        "typed-workspace",
        "",
    )


def load_fact_anchors(dir_path: str, *, strict: bool = True) -> list[Fact]:
    """Load only typed workspace anchors; prose anchors are never reinterpreted."""

    facts: list[Fact] = []
    for anchor in load_anchors(dir_path):
        fields = anchor.get("fields", {})
        if fields.get("lane") != WORKSPACE_LANE:
            continue
        try:
            facts.append(decode_fact(anchor.get("text_payload", ""), anchor["name"]))
        except ValueError:
            if strict:
                raise
    return facts


def ingest_fact_anchors(workspace: CognitiveWorkspace, dir_path: str) -> list[Fact]:
    facts = load_fact_anchors(dir_path)
    workspace.add_facts(facts)
    return facts


def contradiction_evidence(mem, key, expected: str, claim_id: str) -> Fact | None:
    """Convert the live affect comparator result into an explicit G6 fact.

    The returned fact is evidence only when the referent is grounded and differs
    from ``expected``.  Ungrounded lookup is absence of evidence, not contradiction.
    """

    try:
        from .engine_cli import affect_substrate_features
    except ImportError:
        from engine_cli import affect_substrate_features

    result = affect_substrate_features(mem, key, expected)
    if not result.grounded or result.contradiction == 0.0:
        return None
    return Fact(claim_id, "has_verdict", "contradicted", ("affect_substrate",))


def selected_grounded_texts(workspace: CognitiveWorkspace) -> list[str]:
    """The sole adapter from verified workspace state to grounded decode context."""

    return [workspace.render_for_mouth()]
