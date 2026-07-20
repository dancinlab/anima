"""Engine-native, ckpt-free causal smoke for the typed G1/G6 workspace."""

from __future__ import annotations

import tempfile

try:
    from .cognitive_workspace import ClaimStatus, CognitiveWorkspace, CompositionRule, Fact
    from .workspace_adapters import (
        contradiction_evidence,
        ingest_fact_anchors,
        selected_grounded_texts,
        write_fact_anchor,
    )
    from .engine_cli import immune_embed_key, immune_grow_new
except ImportError:
    from cognitive_workspace import ClaimStatus, CognitiveWorkspace, CompositionRule, Fact
    from workspace_adapters import (
        contradiction_evidence,
        ingest_fact_anchors,
        selected_grounded_texts,
        write_fact_anchor,
    )
    from engine_cli import immune_embed_key, immune_grow_new


def run_smoke() -> dict:
    rule = CompositionRule("power-chain", "generates", "powers", "can_power")
    left = Fact("solar_panel", "generates", "electricity", ("sensor:a",))
    right = Fact("electricity", "powers", "pump", ("manual:b",))
    shuffled = Fact("heat", "powers", "pump", ("shuffle:b",))

    with tempfile.TemporaryDirectory() as directory:
        write_fact_anchor(directory, "left", left)
        write_fact_anchor(directory, "right", right)
        live = CognitiveWorkspace()
        persisted = ingest_fact_anchors(live, directory)
        derived = live.compose(rule)

    unary = CognitiveWorkspace()
    unary.add_facts([left])
    unary_derived = unary.compose(rule)
    shuffle = CognitiveWorkspace()
    shuffle.add_facts([left, shuffled])
    shuffle_derived = shuffle.compose(rule)

    good = derived[0] if derived else Fact("missing", "missing", "missing")
    bad = Fact("battery", "can_power", "pump", ("proposal",))
    falsifier = Fact("battery-claim", "has_verdict", "contradicted")

    # The live engine's grounded referent comparator supplies the falsifier.
    key = immune_embed_key("battery-state")
    mem = immune_grow_new(key, "depleted", 2, 2, "fixed")
    evidence = contradiction_evidence(mem, key, "charged", "battery-claim")

    g6 = CognitiveWorkspace()
    g6.add_facts([good, bad] + ([evidence] if evidence else []))
    rejected = g6.propose(bad, [falsifier])
    accepted = g6.propose(good, [Fact("solar_panel", "has_state", "disconnected")])
    selected = g6.select()

    # OFF control: withholding the comparator evidence must select the bad first candidate.
    off = CognitiveWorkspace()
    off.add_facts([good, bad])
    off_bad = off.propose(bad, [falsifier])
    off.propose(good, [Fact("solar_panel", "has_state", "disconnected")])
    off_selected = off.select()

    checks = {
        "kosmos_roundtrip": len(persisted) == 2,
        "g1_live_composes": len(derived) == 1 and derived[0].key == good.key,
        "g1_unary_collapses": len(unary_derived) == 0,
        "g1_pair_shuffle_collapses": len(shuffle_derived) == 0,
        "g1_provenance_both": set(good.provenance) >= {"sensor:a", "manual:b"},
        "g6_engine_contradiction_fires": evidence is not None,
        "g6_bad_falsified": rejected.status is ClaimStatus.FALSIFIED,
        "g6_good_selected": selected is accepted,
        "g6_off_changes_selection": off_selected is off_bad,
        "mouth_selected_only": selected_grounded_texts(g6) == ["solar_panel can_power pump"],
    }
    return {
        "schema": "anima-workspace-smoke/v1",
        "ok": all(checks.values()),
        "checks": checks,
        "selected": selected_grounded_texts(g6)[0],
        "scope": "causal orchestration smoke; not a frozen G1/G6 capability verdict",
    }


def format_report(report: dict) -> str:
    lines = ["=== anima workspace smoke — typed G1 compose + G6 falsify ==="]
    for name, passed in report["checks"].items():
        lines.append(("PASS " if passed else "FAIL ") + name)
    lines.append("selected: " + report["selected"])
    lines.append("scope: " + report["scope"])
    lines.append("WORKSPACE_SMOKE: " + ("OK" if report["ok"] else "FAIL"))
    return "\n".join(lines)

