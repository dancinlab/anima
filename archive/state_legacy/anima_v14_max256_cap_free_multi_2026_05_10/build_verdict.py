"""Build unified verdict.md from per-substrate result_*.json files."""
import json
from pathlib import Path

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_v14_max256_cap_free_multi_2026_05_10")
SUBSTRATES = ["A_phase2_cotrain", "C_cells64_aware", "E_convo5k_ft"]

def _classify(verdict):
    """Map any verdict variant (incl _PARTIAL_n2 suffixed) to family."""
    if verdict is None:
        return "MISSING"
    v = verdict.upper()
    if v.startswith("V14_PASS") or v.startswith("V14_PARTIAL"):
        return "PASS"
    if v.startswith("V14_VIOLATED"):
        return "VIOLATED"
    if v.startswith("V14_AMBIGUOUS"):
        return "AMBIGUOUS"
    if "TRAINED_ONLY" in v:
        return "PARTIAL_NO_MIRRORS"
    return "OTHER"


PASS_FAMILY = {"V14_PASS", "V14_PARTIAL"}
VIOL_FAMILY = {"V14_VIOLATED"}


def load_result(sub_id):
    p = THIS_DIR / f"result_{sub_id}.json"
    if not p.exists():
        return None
    with p.open() as f:
        return json.load(f)


def main():
    results = {s: load_result(s) for s in SUBSTRATES}
    missing = [s for s, r in results.items() if r is None]
    if missing:
        print(f"WARN: missing results for {missing}")

    rows = []
    for sub_id in SUBSTRATES:
        r = results[sub_id]
        if r is None:
            rows.append((sub_id, "MISSING", None, None, None, None, None, None, None, None))
            continue
        verdict = r["verdict"]
        cap_bound_trained = r.get("trained_cap_bound_turns", -1)
        first_cap_trained = r.get("trained_first_cap_turn", None)
        cap_bound_random = r.get("random_cap_bound_turns", [])
        first_cap_random = r.get("random_first_cap_turn", [])
        if r["schema"] == "engine_ag":
            metric = "iit_phi_unnorm_b16"
            tphi = r["trained_phi"]
            rphi = r["random_phi"]
            n_beats = r["n_random_beats"]
            n_total = r["n_random_total"]
            p_phi = r["sign_test_p_two_sided"]
            tcells = r["trained_n_cells"]
            rcells = r["random_n_cells"]
        else:
            metric = "phi (intrinsic)"
            tphi = r["trained_phi"]
            rphi = r["random_phi"]
            n_beats = r["n_random_beats_phi"]
            n_total = r["n_random_total"]
            p_phi = r["sign_test_p_phi"]
            tcells = r["trained_n_cells"]
            rcells = r["random_n_cells"]
        rows.append((
            sub_id, verdict, metric, tphi, rphi, n_beats, n_total, p_phi,
            cap_bound_trained, first_cap_trained, cap_bound_random, first_cap_random,
            tcells, rcells, r["paradigm"], r["arch"]
        ))

    # === Cap-conditional vs cotrain-exercise hypothesis disambiguation ===
    verdicts = {s: results[s]["verdict"] if results[s] else "MISSING" for s in SUBSTRATES}
    a_v, c_v, e_v = verdicts["A_phase2_cotrain"], verdicts["C_cells64_aware"], verdicts["E_convo5k_ft"]
    a_class = _classify(a_v)
    c_class = _classify(c_v)
    e_class = _classify(e_v)
    pass_count = sum(1 for v in (a_class, c_class, e_class) if v == "PASS")
    fail_count = sum(1 for v in (a_class, c_class, e_class) if v == "VIOLATED")

    # Falsifier scoring
    f_max256_1_fired = False
    f_max256_3_fired = False
    f_max256_2_fired = False
    cap_universal = True
    cap_early_universal = True
    for sub_id in SUBSTRATES:
        r = results[sub_id]
        if r is None:
            continue
        first_cap_t = r.get("trained_first_cap_turn", None)
        first_cap_r = r.get("random_first_cap_turn", []) or []
        all_first_caps = [first_cap_t] + first_cap_r
        nonnull_caps = [c for c in all_first_caps if c is not None]
        if not nonnull_caps:
            cap_early_universal = False
            cap_universal = False
        else:
            if not all(c is not None for c in all_first_caps):
                cap_universal = False
            min_cap = min(nonnull_caps) if nonnull_caps else None
            if min_cap is None or min_cap >= 100:
                cap_early_universal = False
    f_max256_1_fired = cap_early_universal  # all cap-bound before turn 100
    f_max256_3_fired = (a_class == "PASS" and c_class == "PASS" and e_class == "PASS")
    f_max256_2_fired = (a_class == "PASS" and c_class == "VIOLATED" and e_class == "VIOLATED")

    # Unified verdict
    if f_max256_3_fired:
        meta_verdict = "UNIVERSAL_CAP_CONDITIONAL_PASS_★★★★★"
        meta_explain = "all 3 substrates PASS at max=256 → cap-conditional polarity confirmed substrate-agnostic"
    elif f_max256_2_fired:
        meta_verdict = "COTRAIN_EXERCISE_DOMINANT_★★★★"
        meta_explain = "only A PASS, C+E VIOLATED → cotrain-exercise hypothesis (§47) > cap-conditional"
    elif pass_count == 3:
        meta_verdict = "UNIVERSAL_CAP_CONDITIONAL_PASS_★★★★★"
        meta_explain = "all 3 substrates in PASS family at max=256"
    elif a_class == "PASS" and (c_class == "PASS" or e_class == "PASS"):
        meta_verdict = "MULTI_FACTORIAL_★★★"
        meta_explain = "mixed outcome — both capacity-cap and cotrain-exercise contribute"
    elif fail_count == 3:
        meta_verdict = "POLARITY_FALSIFIED"
        meta_explain = "all 3 V14_VIOLATED at max=256 → both cap-conditional and cotrain-exercise falsified"
    elif cap_early_universal:
        meta_verdict = "MITOSIS_FUNDAMENTAL_LIMIT_★★★"
        meta_explain = "all cap-bound before turn 100 at max=256 → architecture dispersion fundamental limit"
    else:
        meta_verdict = "MIXED_INDETERMINATE"
        meta_explain = f"verdicts: {verdicts}"

    # === Build markdown ===
    out = []
    out.append("# BG-V14-MAX256-CAP-FREE-MULTI — verdict")
    out.append("")
    out.append(f"**Meta-verdict**: `{meta_verdict}`")
    out.append("")
    out.append(f"{meta_explain}")
    out.append("")
    out.append(f"## Per-substrate V14 result table (3 substrate × 6 run × max=256)")
    out.append("")
    out.append("| ID | paradigm | metric | trained Φ | random Φ (range) | n_beats | sign-p | cells (T) | cells (R range) | first_cap (T / R range) | cap_bound_turns (T / R range) | verdict |")
    out.append("|----|----------|--------|-----------|------------------|---------|--------|-----------|-----------------|--------------------------|------------------------------|---------|")
    for row in rows:
        if row[1] == "MISSING":
            out.append(f"| {row[0]} | MISSING | - | - | - | - | - | - | - | - | - | MISSING |")
            continue
        sub_id, verdict, metric, tphi, rphi, nb, nt, p, cb_t, fc_t, cb_r, fc_r, tc, rc, paradigm, arch = row
        rphi_range = f"{min(rphi):.2f}-{max(rphi):.2f}"
        rcells_range = f"{min(rc)}-{max(rc)}"
        nonnull_fc_r = [x for x in fc_r if x is not None]
        fc_r_str = f"{min(nonnull_fc_r)}-{max(nonnull_fc_r)}" if nonnull_fc_r else "none"
        cb_r_str = f"{min(cb_r)}-{max(cb_r)}" if cb_r else "none"
        out.append(f"| {sub_id} | {paradigm} | {metric} | {tphi:.2f} | {rphi_range} | {nb}/{nt} | {p:.4f} | {tc} | {rcells_range} | {fc_t} / {fc_r_str} | {cb_t} / {cb_r_str} | {verdict} |")
    out.append("")

    # Cap-bound diagnostics
    out.append("## Cap-bound check per substrate per run")
    out.append("")
    out.append("| ID | run | first_cap_turn | cap_bound_turns | reached cap=256? |")
    out.append("|----|-----|----------------|-----------------|-------------------|")
    for sub_id in SUBSTRATES:
        r = results[sub_id]
        if r is None:
            continue
        out.append(f"| {sub_id} | TRAINED | {r.get('trained_first_cap_turn')} | {r.get('trained_cap_bound_turns')} | {'YES' if r.get('trained_first_cap_turn') is not None else 'NO'} |")
        for s, fc, cb in zip(r["random_seeds"], r.get("random_first_cap_turn", []), r.get("random_cap_bound_turns", [])):
            out.append(f"| {sub_id} | s{s} | {fc} | {cb} | {'YES' if fc is not None else 'NO'} |")
    out.append("")

    # Hypothesis disambiguation
    out.append("## Cap-conditional vs cotrain-exercise hypothesis disambiguation")
    out.append("")
    out.append("### Hypothesis predictions")
    out.append("- **Cap-conditional**: trained PASS scales with cap. At max=256 cap-free, ALL substrates PASS. (§45 partial evidence: trained leads at max=128 vs loses at max=64.)")
    out.append("- **Cotrain-exercise (§47)**: only Phase 2 cotrain (substrate A) PASS, regardless of cap. C/E remain VIOLATED at any cap.")
    out.append("")
    out.append("### Observed at max=256")
    out.append(f"- A_phase2_cotrain: `{a_v}`")
    out.append(f"- C_cells64_aware: `{c_v}`")
    out.append(f"- E_convo5k_ft: `{e_v}`")
    out.append("")
    out.append("### Falsifier ledger")
    out.append(f"- **F-MAX256-1** (universal cap-bound before turn 100): {'**FIRED**' if f_max256_1_fired else 'NOT FIRED'}")
    out.append(f"- **F-MAX256-2** (only A PASS → cotrain-exercise dominant): {'**FIRED**' if f_max256_2_fired else 'NOT FIRED'}")
    out.append(f"- **F-MAX256-3** (all 3 PASS → universal cap-conditional): {'**FIRED**' if f_max256_3_fired else 'NOT FIRED'}")
    out.append("")

    out.append("## Unified verdict")
    out.append("")
    out.append(f"**`{meta_verdict}`** — {meta_explain}")
    out.append("")

    out_path = THIS_DIR / "verdict.md"
    with out_path.open("w") as f:
        f.write("\n".join(out))
    print(f"[saved] {out_path}")
    print(f"meta_verdict: {meta_verdict}")
    return meta_verdict, results


if __name__ == "__main__":
    main()
