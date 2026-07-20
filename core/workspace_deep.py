"""Deep G1/G6 causal certification beyond the frozen release panel."""

from __future__ import annotations

import tempfile

try:
    from .cognitive_workspace import CognitiveWorkspace, CompositionRule, ConjunctiveRule, Fact
    from .workspace_adapters import load_fact_anchors
    from .workspace_mouth import claim_ids, decide_seed
    from .workspace_runtime import (
        Measurement, measurement_falsification_step, persist_measurement_evidence,
        resolve_evidence_verdicts,
    )
except ImportError:
    from cognitive_workspace import CognitiveWorkspace, CompositionRule, ConjunctiveRule, Fact
    from workspace_adapters import load_fact_anchors
    from workspace_mouth import claim_ids, decide_seed
    from workspace_runtime import (
        Measurement, measurement_falsification_step, persist_measurement_evidence,
        resolve_evidence_verdicts,
    )


def _closure(facts, rules):
    workspace = CognitiveWorkspace()
    workspace.add_facts(facts)
    workspace.compose_until_stable(rules)
    return workspace


def _chain_checks(length: int) -> dict[str, bool]:
    facts = [
        Fact("n%d" % i, "leads_to", "n%d" % (i + 1), ("deep:edge:%d" % i,))
        for i in range(length)
    ]
    rule = CompositionRule("deep-transitive", "leads_to", "leads_to", "leads_to")
    expected = ("n0", "leads_to", "n%d" % length)
    live = _closure(facts, [rule])
    mid = length // 2
    pairing = list(facts)
    pairing[mid] = Fact("unpaired", "leads_to", facts[mid].object, ("control:pair",))
    negated = list(facts)
    negated[mid] = Fact(facts[mid].subject, "not_leads_to", facts[mid].object,
                        ("control:negation",))
    quantified = list(facts)
    quantified[mid] = Fact(facts[mid].subject, "leads_to_every", facts[mid].object,
                           ("control:quantifier",))
    wrong_rule = CompositionRule("wrong", "decorates", "leads_to", "leads_to")
    proposition = live.facts.get(expected)
    return {
        "live_exact": proposition is not None,
        "all_edges_provenance": proposition is not None and all(
            "deep:edge:%d" % i in proposition.provenance for i in range(length)),
        "pairing_shuffle_collapses": expected not in _closure(pairing, [rule]).facts,
        "negation_scope_collapses": expected not in _closure(negated, [rule]).facts,
        "quantifier_change_collapses": expected not in _closure(quantified, [rule]).facts,
        "wrong_rule_collapses": expected not in _closure(facts, [wrong_rule]).facts,
        "irrelevant_insertion_inert": expected in _closure(
            [*facts, Fact("noise", "decorates", "nobody")], [rule]).facts,
    }


def run_g1_deep_certification() -> dict:
    rows = []
    for length in (6, 8, 10):
        checks = _chain_checks(length)
        rows.append({"case": "chain_%d" % length, "checks": checks,
                     "ok": all(checks.values())})

    branch_facts = [
        Fact("left_branch", "enables", "hub", ("deep:left",)),
        Fact("right_branch", "permits", "hub", ("deep:right",)),
        Fact("hub", "leads_to", "goal", ("deep:goal",)),
    ]
    join = ConjunctiveRule("branch-join", "enables", "permits", "jointly_enables")
    finish = CompositionRule("join-finish", "jointly_enables", "leads_to", "reaches")
    expected = ("left_branch & right_branch", "reaches", "goal")
    live = _closure(branch_facts, [join, finish])
    swapped_pair = [branch_facts[0], Fact("right_branch", "enables", "hub"), branch_facts[2]]
    branch_checks = {
        "branch_merge_exact": expected in live.facts,
        "both_branches_provenance": expected in live.facts
        and all(x in live.facts[expected].provenance for x in ("deep:left", "deep:right")),
        "missing_branch_collapses": expected not in _closure(branch_facts[:1] + branch_facts[2:],
                                                               [join, finish]).facts,
        "relation_pairing_collapses": expected not in _closure(swapped_pair, [join, finish]).facts,
    }
    rows.append({"case": "branch_merge", "checks": branch_checks,
                 "ok": all(branch_checks.values())})

    cycle_rule = CompositionRule("cycle-transitive", "reaches", "reaches", "reaches")
    cycle = _closure([
        Fact("a", "reaches", "b", ("cycle:a",)),
        Fact("b", "reaches", "c", ("cycle:b",)),
        Fact("c", "reaches", "a", ("cycle:c",)),
    ], [cycle_rule])
    cycle_checks = {
        "cycle_stabilizes": len(cycle.facts) == 9,
        "cycle_self_reach": all((x, "reaches", x) in cycle.facts for x in "abc"),
        "cycle_provenance": all(
            set(("cycle:a", "cycle:b", "cycle:c")).issubset(cycle.facts[(x, "reaches", x)].provenance)
            for x in "abc"),
    }
    rows.append({"case": "cycle", "checks": cycle_checks, "ok": all(cycle_checks.values())})

    homonym = _closure([
        Fact("bank:finance", "stores", "money"),
        Fact("money", "funds", "loan"),
        Fact("bank:river", "borders", "water"),
        Fact("water", "erodes", "shore"),
    ], [CompositionRule("finance", "stores", "funds", "can_fund"),
        CompositionRule("river", "borders", "erodes", "can_erode")])
    homonym_checks = {
        "finance_exact": ("bank:finance", "can_fund", "loan") in homonym.facts,
        "river_exact": ("bank:river", "can_erode", "shore") in homonym.facts,
        "homonym_no_cross_join": ("bank:finance", "can_erode", "shore") not in homonym.facts
        and ("bank:river", "can_fund", "loan") not in homonym.facts,
    }
    rows.append({"case": "typed_homonym", "checks": homonym_checks,
                 "ok": all(homonym_checks.values())})
    return {"schema": "anima.workspace-g1-deep/v1", "ok": all(r["ok"] for r in rows),
            "cases": rows}


def run_g6_deep_certification() -> dict:
    seed = "if catalyst increases yield, then reactor reduces waste"
    ids = claim_ids(seed)
    off = decide_seed(seed, require_evidence=True)
    on = measurement_falsification_step(seed, [
        Measurement(ids[0], 0.2, 0.5, "above", "lab-A", "2026-07-21T01:00:00Z")
    ])
    shuffled = measurement_falsification_step(seed, [
        Measurement(ids[0] + ":shuffle", 0.2, 0.5, "above", "lab-A",
                    "2026-07-21T01:00:00Z")
    ])
    conflict_measurements = [
        Measurement(ids[0], 0.8, 0.5, "above", "lab-A", "2026-07-21T01:00:00Z"),
        Measurement(ids[0], 0.2, 0.5, "above", "lab-B", "2026-07-21T02:00:00Z"),
    ]
    conflict = measurement_falsification_step(
        seed, conflict_measurements, require_evidence=False)
    alternative_specs = on.decision.candidate_specs if on.decision is not None else ()
    with tempfile.TemporaryDirectory() as directory:
        persist_measurement_evidence(directory, conflict_measurements)
        reloaded = load_fact_anchors(directory)
        session_verdicts = resolve_evidence_verdicts(reloaded)
        provenance_ok = all(
            any(p.startswith("observed_at=") for p in fact.provenance)
            and any(p in ("lab-A", "lab-B") for p in fact.provenance)
            for fact in reloaded
        )
    checks = {
        "off_ungrounded": off is not None and off.abstained,
        "contradiction_rejects_primary": on.decision is not None
        and ids[0] in on.decision.rejected_claim_ids,
        "alternative_selected": on.decision is not None
        and on.decision.selected_claim_id == ids[1],
        "alternative_distinguishable": len({spec.falsified_when for spec in alternative_specs}) == 3,
        "claim_id_shuffle_inert": shuffled.decision is not None and shuffled.decision.abstained,
        "support_contradiction_ungrounded": conflict.verdicts.get(ids[0]) == "UNGROUNDED"
        and conflict.decision is not None and conflict.decision.abstained,
        "session_conflict_preserved": session_verdicts.get(ids[0]) == "UNGROUNDED",
        "source_time_preserved": provenance_ok,
    }
    return {"schema": "anima.workspace-g6-deep/v1", "ok": all(checks.values()),
            "checks": checks}


def run_workspace_deep_certification() -> dict:
    g1 = run_g1_deep_certification()
    g6 = run_g6_deep_certification()
    return {"schema": "anima.workspace-deep/v1", "ok": g1["ok"] and g6["ok"],
            "g1": g1, "g6": g6}


def format_deep_report(report: dict) -> str:
    lines = ["=== anima workspace G1/G6 deep certification ==="]
    for row in report["g1"]["cases"]:
        lines.append(("PASS " if row["ok"] else "FAIL ") + "G1 " + row["case"])
        lines.extend("  " + ("PASS " if ok else "FAIL ") + name
                     for name, ok in row["checks"].items())
    lines.append(("PASS " if report["g6"]["ok"] else "FAIL ") + "G6 measured loop")
    lines.extend("  " + ("PASS " if ok else "FAIL ") + name
                 for name, ok in report["g6"]["checks"].items())
    lines.append("WORKSPACE_DEEP: " + ("CERTIFIED" if report["ok"] else "FAIL"))
    return "\n".join(lines)
