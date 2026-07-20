"""Held-out semantic certification for the typed G1/G6 workspace.

The panel scores exact derived triples, not keyword coverage.  Domains and surface
languages vary while the same two-operand join and falsification state machine run.
"""

from __future__ import annotations

from dataclasses import dataclass

try:
    from .cognitive_workspace import ClaimStatus, CognitiveWorkspace, CompositionRule, Fact
except ImportError:
    from cognitive_workspace import ClaimStatus, CognitiveWorkspace, CompositionRule, Fact


@dataclass(frozen=True)
class SemanticCase:
    name: str
    left: Fact
    right: Fact
    rule: CompositionRule
    expected: tuple[str, str, str]


def _cases() -> tuple[SemanticCase, ...]:
    return (
        SemanticCase(
            "energy",
            Fact("solar_panel", "generates", "electricity", ("heldout:energy:a",)),
            Fact("electricity", "powers", "pump", ("heldout:energy:b",)),
            CompositionRule("energy-chain", "generates", "powers", "can_power"),
            ("solar_panel", "can_power", "pump"),
        ),
        SemanticCase(
            "biology",
            Fact("enzyme", "catalyzes", "reaction", ("heldout:biology:a",)),
            Fact("reaction", "produces", "metabolite", ("heldout:biology:b",)),
            CompositionRule("metabolic-chain", "catalyzes", "produces", "enables_product"),
            ("enzyme", "enables_product", "metabolite"),
        ),
        SemanticCase(
            "navigation",
            Fact("bronze_key", "opens", "north_door", ("heldout:navigation:a",)),
            Fact("north_door", "leads_to", "garden", ("heldout:navigation:b",)),
            CompositionRule("access-chain", "opens", "leads_to", "grants_access"),
            ("bronze_key", "grants_access", "garden"),
        ),
        SemanticCase(
            "korean_growth",
            Fact("비", "적신다", "땅", ("heldout:ko:a",)),
            Fact("땅", "기른다", "새싹", ("heldout:ko:b",)),
            CompositionRule("성장-연쇄", "적신다", "기른다", "성장을_돕는다"),
            ("비", "성장을_돕는다", "새싹"),
        ),
        SemanticCase(
            "software",
            Fact("parser", "emits", "syntax_tree", ("heldout:software:a",)),
            Fact("syntax_tree", "feeds", "optimizer", ("heldout:software:b",)),
            CompositionRule("compiler-chain", "emits", "feeds", "can_feed"),
            ("parser", "can_feed", "optimizer"),
        ),
        SemanticCase(
            "everyday",
            Fact("alarm", "wakes", "owner", ("heldout:everyday:a",)),
            Fact("owner", "opens", "shop", ("heldout:everyday:b",)),
            CompositionRule("morning-chain", "wakes", "opens", "enables_opening"),
            ("alarm", "enables_opening", "shop"),
        ),
        SemanticCase(
            "negative_causal",
            Fact("cooling", "prevents", "overheat", ("heldout:negative:a",)),
            Fact("overheat", "causes", "shutdown", ("heldout:negative:b",)),
            CompositionRule("prevention-chain", "prevents", "causes", "reduces_risk_of"),
            ("cooling", "reduces_risk_of", "shutdown"),
        ),
        SemanticCase(
            "conditional",
            Fact("launch", "requires", "authorization", ("heldout:conditional:a",)),
            Fact("authorization", "requires", "quorum", ("heldout:conditional:b",)),
            CompositionRule("requirement-chain", "requires", "requires", "requires_indirectly"),
            ("launch", "requires_indirectly", "quorum"),
        ),
    )


def realizer_heldout_panel() -> tuple[tuple[str, str], ...]:
    """Frozen cross-domain surfaces for mounted-mouth semantic realization."""
    return (
        ("physics", "if magnetic flux changes rapidly, then copper coil induces current"),
        ("biology", "if enzyme activates receptor, then cell expresses protein"),
        ("everyday", "if morning alarm rings, then shop owner opens doors"),
        ("korean_negation", "만약 비가 오지 않으면, 그러면 도로는 젖지 않는다"),
        ("negative_conditional", "if cooling does not fail, then server avoids shutdown"),
        ("five_step", "alpha starts beta. beta enables gamma. gamma activates delta. "
         "delta stabilizes epsilon. epsilon preserves zeta."),
    )


def _derive(case: SemanticCase, facts: list[Fact]) -> list[Fact]:
    workspace = CognitiveWorkspace()
    workspace.add_facts(facts)
    return workspace.compose(case.rule)


def _falsification_checks(case: SemanticCase, proposition: Fact) -> dict[str, bool]:
    primary_id = "semantic:" + case.name + ":primary"
    alternative_id = "semantic:" + case.name + ":alternative"
    primary_f = Fact(primary_id, "has_verdict", "contradicted")
    alternative_f = Fact(alternative_id, "has_verdict", "contradicted")
    alternative = Fact(
        proposition.subject,
        "cannot_" + proposition.relation,
        proposition.object,
        proposition.provenance + ("counter-hypothesis",),
    )

    def decide(evidence: list[Fact]):
        workspace = CognitiveWorkspace()
        workspace.add_facts([proposition, alternative, *evidence])
        claims = [
            workspace.propose(proposition, [primary_f]),
            workspace.propose(alternative, [alternative_f]),
        ]
        try:
            selected = workspace.select(claims)
            return selected, claims
        except RuntimeError:
            return None, claims

    off, _ = decide([])
    on, on_claims = decide([primary_f])
    shuffled, _ = decide([Fact(primary_id + ":shuffle", "has_verdict", "contradicted")])
    abstained, all_claims = decide([primary_f, alternative_f])
    return {
        "falsify_off_primary": off is not None and off.proposition == proposition,
        "falsify_on_alternative": on is not None and on.proposition == alternative,
        "falsify_on_rejected": on_claims[0].status is ClaimStatus.FALSIFIED,
        "falsify_shuffle_inert": shuffled is not None and shuffled.proposition == proposition,
        "falsify_all_abstains": abstained is None
        and all(c.status is ClaimStatus.FALSIFIED for c in all_claims),
    }


def _closure(facts: list[Fact]) -> CognitiveWorkspace:
    workspace = CognitiveWorkspace()
    workspace.add_facts(facts)
    transitive = CompositionRule("transitive-chain", "leads_to", "leads_to", "leads_to")
    while workspace.compose(transitive):
        pass
    return workspace


def _multihop_row(length: int) -> dict:
    facts = [
        Fact("node%d" % i, "leads_to", "node%d" % (i + 1), ("heldout:hop%d" % i,))
        for i in range(length)
    ]
    expected = ("node0", "leads_to", "node%d" % length)
    live = _closure(facts)
    missing = _closure(facts[: length // 2] + facts[length // 2 + 1 :])
    shuffled_facts = list(facts)
    mid = length // 2
    shuffled_facts[mid] = Fact("unrelated", "leads_to", facts[mid].object)
    shuffled = _closure(shuffled_facts)
    irrelevant = _closure([*facts, Fact("noise", "decorates", "nothing")])
    reverse = _closure([Fact(f.object, f.relation, f.subject) for f in facts])
    proposition = live.facts.get(expected)
    checks = {
        "live_exact": proposition is not None,
        "direction_reversal_collapses": expected not in reverse.facts,
        "pair_shuffle_collapses": expected not in shuffled.facts,
        "missing_middle_collapses": expected not in missing.facts,
        "irrelevant_fact_inert": expected in irrelevant.facts,
        "all_edges_provenance": proposition is not None
        and all("heldout:hop%d" % i in proposition.provenance for i in range(length)),
    }
    if proposition is not None:
        pseudo_case = SemanticCase(
            "chain_%d" % length, facts[0], facts[-1],
            CompositionRule("transitive-chain", "leads_to", "leads_to", "leads_to"), expected,
        )
        checks.update(_falsification_checks(pseudo_case, proposition))
    return {"case": "chain_%d_hop" % length, "checks": checks, "ok": all(checks.values())}


def run_semantic_certification() -> dict:
    rows = []
    for case in _cases():
        live = _derive(case, [case.left, case.right])
        reverse_storage = _derive(case, [case.right, case.left])
        reverse_direction = _derive(
            case,
            [
                Fact(case.left.object, case.left.relation, case.left.subject),
                Fact(case.right.object, case.right.relation, case.right.subject),
            ],
        )
        pair_shuffle = _derive(
            case,
            [case.left, Fact("unrelated_middle", case.right.relation, case.right.object)],
        )
        missing = _derive(case, [case.left])
        irrelevant = Fact("noise", "decorates", "nothing", ("control:irrelevant",))
        with_irrelevant = _derive(case, [case.left, irrelevant, case.right])
        exact = len(live) == 1 and live[0].key == case.expected
        checks = {
            "live_exact": exact,
            "storage_order_invariant": len(reverse_storage) == 1
            and reverse_storage[0].key == case.expected,
            "direction_reversal_collapses": case.expected not in {x.key for x in reverse_direction},
            "pair_shuffle_collapses": case.expected not in {x.key for x in pair_shuffle},
            "missing_middle_collapses": case.expected not in {x.key for x in missing},
            "irrelevant_fact_inert": len(with_irrelevant) == 1
            and with_irrelevant[0].key == case.expected,
        }
        if exact:
            checks.update(_falsification_checks(case, live[0]))
        rows.append({"case": case.name, "checks": checks, "ok": all(checks.values())})
    rows.extend(_multihop_row(length) for length in (3, 4, 5))
    return {
        "schema": "anima-workspace-semantic/v1",
        "ok": all(row["ok"] for row in rows),
        "cases": rows,
        "scope": "exact held-out triples + causal controls; no keyword scoring",
    }


def format_report(report: dict) -> str:
    lines = ["=== anima workspace semantic certification ==="]
    for row in report["cases"]:
        lines.append(("PASS " if row["ok"] else "FAIL ") + row["case"])
        for name, passed in row["checks"].items():
            lines.append("  " + ("PASS " if passed else "FAIL ") + name)
    lines.append("scope: " + report["scope"])
    lines.append("WORKSPACE_SEMANTIC: " + ("CERTIFIED" if report["ok"] else "FAIL"))
    return "\n".join(lines)
