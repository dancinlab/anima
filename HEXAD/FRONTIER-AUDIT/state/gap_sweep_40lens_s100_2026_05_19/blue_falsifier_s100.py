"""
B-S100-1..5 sidecar — §100 EXHAUSTIVE 40-LENS GAP SWEEP structural battery.

Sidecar only. Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py is
0-line-diff (sha256 prefix c93e160a8a376a94) — verified by B-S100-5.

g3: §100 surfaces gaps. The battery proves the §100 *survey* is structurally
honest (exhaustive 40-lens coverage; closed verdict partition; shortlist
sub-set of gap-set; central-sha 0-line-diff; verdict cites real arc §s).
It does NOT prove the gaps are correctly prioritised — priority is judgement,
captured in B-S100-NOTE.

f1/f2 safe — no σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation.
"""
import json
import hashlib
import sys
from pathlib import Path


HERE = Path(__file__).parent
ANIMA_ROOT = HERE.parent.parent
RESULT_JSON = HERE / "result.json"
GAP_SWEEP_MD = HERE / "GAP_SWEEP.md"
CENTRAL_BLUE = ANIMA_ROOT / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"

EXPECTED_FAMILIES = [
    "F1_math_structural",
    "F2_adversarial_stress",
    "F3_economic_resource",
    "F4_epistemic_evidence",
    "F5_convergence_closure",
    "F6_simplicity_canonical",
    "F7_temporal_dynamics",
    "F8_coverage_consistency",
]

EXPECTED_LENSES = {
    "F1_math_structural": ["functor", "operadic", "persistent_homology", "tropical", "bisimulation"],
    "F2_adversarial_stress": ["adversarial", "byzantine", "edge_chaos", "perturbation", "ablation"],
    "F3_economic_resource": ["pareto", "landauer", "info_budget", "optimal_transport", "dynamic_programming"],
    "F4_epistemic_evidence": ["assumption_surfacing", "bayesian", "counterfactual", "falsifier", "honesty_triad"],
    "F5_convergence_closure": ["fixpoint", "success_criteria", "closed_loop", "regression_streak", "defense_in_depth"],
    "F6_simplicity_canonical": ["minimum_viable", "architectural_simplicity", "canonical_ssot", "duplicated_helper", "surgical_scope"],
    "F7_temporal_dynamics": ["temporal_decay", "temporal_hierarchy", "heuristic_promotion", "fix_introduces_axis", "active_acquisition"],
    "F8_coverage_consistency": ["axis_coverage", "cross_tool_consistency", "parallel_fanout", "unowned_load_bearing", "landscape"],
}

CLOSED_VERDICTS = {"gap", "clean", "n/a"}

CENTRAL_SHA256_EXPECTED_PREFIX = "c93e160a8a376a94"

# Arc §s the §100 priority shortlist must cite (real arc landings)
ARC_S_CITED = ["§1.1", "§9", "§11-B", "§15", "§16", "§17", "§51", "§63", "§72",
               "§80", "§82", "§85", "§87", "§94", "§95", "§96", "§98", "§99"]


def load_result():
    return json.loads(RESULT_JSON.read_text())


def b_s100_1_exhaustive_40_lens_coverage(res):
    """40 lenses present, exactly 5 per family, exactly 8 families — no skip."""
    fams = list(res["lens_verdicts"].keys())
    assert fams == EXPECTED_FAMILIES, f"family list mismatch: {fams}"
    total = 0
    for fam, exp_lenses in EXPECTED_LENSES.items():
        got = list(res["lens_verdicts"][fam].keys())
        assert got == exp_lenses, f"{fam} lens list mismatch: {got}"
        assert len(got) == 5
        total += len(got)
    assert total == 40, f"expected 40 lenses, got {total}"
    assert res["counts"]["total_lenses"] == 40
    return {"families": 8, "lenses_per_family": 5, "total_lenses": 40, "no_lens_skipped": True}


def b_s100_2_verdict_closed_partition(res):
    """Every verdict ∈ {gap, clean, n/a}; counts add to 40; no missing/extra category."""
    counts = {"gap": 0, "clean": 0, "n/a": 0}
    for fam in EXPECTED_FAMILIES:
        for lens in EXPECTED_LENSES[fam]:
            v = res["lens_verdicts"][fam][lens]
            assert v in CLOSED_VERDICTS, f"{fam}/{lens} verdict {v!r} not in {CLOSED_VERDICTS}"
            counts[v] += 1
    assert counts["gap"] + counts["clean"] + counts["n/a"] == 40
    assert counts == {"gap": res["counts"]["gap"],
                      "clean": res["counts"]["clean"],
                      "n/a": res["counts"]["n_a"]}, f"count mismatch: {counts} vs json"
    return {"closed_partition": True, "counts": counts}


def b_s100_3_priority_subset_of_gap_set(res):
    """Priority-shortlist lenses ⊆ gap-set (cannot prioritise a clean/n-a lens)."""
    gap_lenses = set()
    for fam in EXPECTED_FAMILIES:
        # collect "Fx_lens" form
        fam_short = fam[:2]  # F1..F8
        for lens, verdict in res["lens_verdicts"][fam].items():
            if verdict == "gap":
                gap_lenses.add(f"{fam_short}_{lens}")
    shortlist = res["priority_shortlist"]
    assert len(shortlist) >= 3 and len(shortlist) <= 5, f"shortlist length {len(shortlist)} not in [3,5]"
    for item in shortlist:
        for lens_ref in item["lenses"]:
            assert lens_ref in gap_lenses, f"shortlist lens {lens_ref!r} not in gap-set"
    return {"shortlist_size": len(shortlist), "subset_of_gap": True}


def b_s100_4_connection_point_cites_real_arc(res):
    """GAP_SWEEP.md cites the actual §94/§95/§98 arc verdicts — survey is grounded in real arc."""
    text = GAP_SWEEP_MD.read_text()
    must_cite = ["§94", "§95", "§98", "§9", "§1.1", "§11-B"]
    for s in must_cite:
        assert s in text, f"GAP_SWEEP.md missing arc citation {s!r}"
    # §94 must be linked to the integration-collapse finding (F1 functor lens)
    assert "INTEGRATION-COLLAPSES" in text or "integration" in text.lower()
    # §95 must be linked to substrate
    assert "substrate" in text.lower()
    # §1.1 must be linked to data-regime
    assert "data-regime" in text.lower() or "data regime" in text.lower()
    # honest C3 caveats ≥ 10
    c3_section = text.split("HONEST C3 CAVEATS")[1] if "HONEST C3 CAVEATS" in text else ""
    import re
    numbered = re.findall(r"^\d+\.", c3_section, flags=re.MULTILINE)
    assert len(numbered) >= 10, f"need ≥10 honest C3 caveats, got {len(numbered)}"
    return {"arc_citations_present": True, "honest_c3_count": len(numbered)}


def b_s100_5_central_blue_zero_line_diff(res):
    """Central blue_falsifier.py sha256 prefix must match expected c93e160a8a376a94."""
    data = CENTRAL_BLUE.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    prefix = sha[:16]
    assert prefix == CENTRAL_SHA256_EXPECTED_PREFIX, (
        f"central blue_falsifier.py sha mismatch: got {prefix} "
        f"expected {CENTRAL_SHA256_EXPECTED_PREFIX} — sidecar-only mandate violated"
    )
    assert res["central_blue_falsifier_sha256_prefix"] == CENTRAL_SHA256_EXPECTED_PREFIX
    assert res["central_blue_falsifier_zero_line_diff"] is True
    return {"central_sha_prefix": prefix, "zero_line_diff": True}


def main():
    res = load_result()
    battery = [
        ("B-S100-1", "EXHAUSTIVE-40-LENS-COVERAGE", b_s100_1_exhaustive_40_lens_coverage),
        ("B-S100-2", "VERDICT-CLOSED-PARTITION", b_s100_2_verdict_closed_partition),
        ("B-S100-3", "PRIORITY-SUBSET-OF-GAP-SET", b_s100_3_priority_subset_of_gap_set),
        ("B-S100-4", "CONNECTION-POINT-CITES-REAL-ARC", b_s100_4_connection_point_cites_real_arc),
        ("B-S100-5", "CENTRAL-BLUE-ZERO-LINE-DIFF", b_s100_5_central_blue_zero_line_diff),
    ]
    results = {}
    passes = 0
    for bid, name, fn in battery:
        try:
            results[bid] = {"name": name, "verdict": "PASS", "detail": fn(res)}
            passes += 1
        except AssertionError as e:
            results[bid] = {"name": name, "verdict": "FAIL", "detail": str(e)}

    note = (
        "B-S100-NOTE empirical carve-out: this battery proves §100 is structurally "
        "honest (40-lens exhaustive, closed verdict partition, shortlist⊆gap, real "
        "arc citations, central 0-line-diff). It does NOT prove the gaps are "
        "correctly prioritised — priority is judgement, ranked by impact on "
        "reaching the GOAL. necessary-not-sufficient at the §100 layer "
        "(B-EMERGE-7 family). g3: §100 surfaces and prioritises ONLY; it "
        "fires nothing, fixes nothing, claims no capability. north-star + "
        "§15/§51/§72 milestones UNCHANGED, GOAL 미도달."
    )

    out = {
        "battery": "B-S100",
        "section": "§100",
        "passes": passes,
        "total": len(battery),
        "all_pass": passes == len(battery),
        "results": results,
        "B-S100-NOTE": note,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if passes == len(battery) else 1)


if __name__ == "__main__":
    main()
