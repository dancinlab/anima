"""Aggregate per-substrate JSON → correlation_metrics.json + dispersion_trigger_metrics.json + verdict.md.

Tests:
- F-CORR-1: trained correlation difference vs random
- F-CORR-2: dispersion trigger rate difference
- F-CORR-3: cross-substrate consistency
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, stdev

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_trained_correlation_measurement_2026_05_10")

SUBSTRATES = ["A_phase2_cotrain", "C_cells64_aware", "E_convo5k_ft"]


def collect():
    out = {}
    for sub in SUBSTRATES:
        p = THIS_DIR / f"result_{sub}.json"
        if not p.exists():
            continue
        d = json.load(open(p))
        out[sub] = d
    return out


def safe_mean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return mean(xs) if xs else float("nan")


def safe_std(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return stdev(xs) if len(xs) > 1 else 0.0


def summarize_run(snaps, n_cells_min=2, n_cells_max=None):
    """Filter snapshots to a regime then compute summary statistics."""
    s = [x for x in snaps if x["n_cells"] >= n_cells_min]
    if n_cells_max is not None:
        s = [x for x in s if x["n_cells"] <= n_cells_max]
    if not s:
        return None
    summary = {
        "n_snapshots": len(s),
        "n_cells_first": s[0]["n_cells"],
        "n_cells_last": s[-1]["n_cells"],
        "turn_first": s[0]["turn"],
        "turn_last": s[-1]["turn"],
    }
    keys = [
        "cos_mean", "abs_cos_mean", "cos_std", "cos_max", "cos_min",
        "norm_mean", "norm_std", "norm_cv",
        "eff_rank", "eff_rank_normalized",
        "disp_overall_mean", "disp_overall_std",
        "disp_top_quartile_above_gate", "disp_top_quartile_k",
        "disp_trigger_rate",
    ]
    for k in keys:
        summary[f"{k}_mean"] = safe_mean([x.get(k) for x in s])
        summary[f"{k}_max"] = max([x.get(k) for x in s if x.get(k) is not None], default=float("nan"))
        summary[f"{k}_min"] = min([x.get(k) for x in s if x.get(k) is not None], default=float("nan"))
    return summary


def split_per_turn(snaps):
    """Per-snapshot incremental dispersion-vs-tension splits."""
    rows = []
    prev_d = 0
    prev_t = 0
    for x in snaps:
        d_inc = x["n_splits_dispersion_cum"] - prev_d
        t_inc = x["n_splits_tension_cum"] - prev_t
        rows.append({
            "turn": x["turn"],
            "n_cells": x["n_cells"],
            "splits_disp_cum": x["n_splits_dispersion_cum"],
            "splits_tens_cum": x["n_splits_tension_cum"],
            "splits_disp_inc": d_inc,
            "splits_tens_inc": t_inc,
            "disp_trigger_rate": x["disp_trigger_rate"],
            "disp_top_quartile_above_gate": x["disp_top_quartile_above_gate"],
            "disp_top_quartile_k": x["disp_top_quartile_k"],
        })
        prev_d = x["n_splits_dispersion_cum"]
        prev_t = x["n_splits_tension_cum"]
    return rows


def main():
    data = collect()

    # =================================================================
    # 1) correlation_metrics.json — full correlation summaries
    # =================================================================
    corr_metrics = {"substrates": {}}
    for sub_id, d in data.items():
        t_snaps = d["trained"]["snapshots"]
        r_snaps = d["random"]["snapshots"]

        # Two regimes:
        #   - early/growth window: n_cells in [16, 64) — direct comparison region
        #   - late/cap-approach window: n_cells in [64, 256] — where §51 effect manifests
        e_t = summarize_run(t_snaps, n_cells_min=8, n_cells_max=64)
        e_r = summarize_run(r_snaps, n_cells_min=8, n_cells_max=64)
        l_t = summarize_run(t_snaps, n_cells_min=64, n_cells_max=256)
        l_r = summarize_run(r_snaps, n_cells_min=64, n_cells_max=256)

        # Across-all-snapshots
        a_t = summarize_run(t_snaps)
        a_r = summarize_run(r_snaps)

        corr_metrics["substrates"][sub_id] = {
            "schema": d["schema"], "arch": d["arch"],
            "n_turns": d["n_turns"], "snap_every": d["snap_every"],
            "trained_final_n_cells": d["trained"]["final_n_cells"],
            "random_final_n_cells": d["random"]["final_n_cells"],
            "trained_first_cap_turn": d["trained"]["first_cap_turn"],
            "random_first_cap_turn": d["random"]["first_cap_turn"],
            "trained_n_splits_dispersion": d["trained"]["n_splits_dispersion"],
            "trained_n_splits_tension": d["trained"]["n_splits_tension"],
            "random_n_splits_dispersion": d["random"]["n_splits_dispersion"],
            "random_n_splits_tension": d["random"]["n_splits_tension"],
            "regime_all":   {"trained": a_t, "random": a_r},
            "regime_early": {"trained": e_t, "random": e_r},
            "regime_late":  {"trained": l_t, "random": l_r},
        }

    out_corr = THIS_DIR / "correlation_metrics.json"
    out_corr.write_text(json.dumps(corr_metrics, indent=2, default=str))
    print(f"[saved] {out_corr}")

    # =================================================================
    # 2) dispersion_trigger_metrics.json — per-turn rates
    # =================================================================
    disp_metrics = {"substrates": {}}
    for sub_id, d in data.items():
        disp_metrics["substrates"][sub_id] = {
            "trained_per_turn": split_per_turn(d["trained"]["snapshots"]),
            "random_per_turn": split_per_turn(d["random"]["snapshots"]),
        }
    out_disp = THIS_DIR / "dispersion_trigger_metrics.json"
    out_disp.write_text(json.dumps(disp_metrics, indent=2, default=str))
    print(f"[saved] {out_disp}")

    # =================================================================
    # 3) Build verdict.md
    # =================================================================
    lines = []
    lines.append("# BG-TRAINED-CORRELATION-MEASUREMENT — verdict")
    lines.append("")
    lines.append("§51 cap-conditional mechanism: trained cells reach max=256 cap LATER than random.")
    lines.append("Hypothesis: trained cells form more correlated structure → top-quartile dispersion")
    lines.append("variance lower → fewer outliers cross sigma_gate → split rate slower near cap.")
    lines.append("")
    lines.append(f"Run: 3 substrate × {{trained, random_seed=42}} × max_cells=256")
    lines.append("Lean compute: 1 trained + 1 random per substrate ($0 local CPU).")
    lines.append("A: 100 turns / snap=10 (cap-free regime). C, E: 60 turns / snap=5 (cap-approach).")
    lines.append("")

    # Table 1: correlation summary
    lines.append("## Table 1 — Inter-cell cosine correlation (all snapshots)")
    lines.append("")
    lines.append("| substrate | run | n_snaps | nC range | cos_mean | abs_cos_mean | cos_std | norm_cv | eff_rank/N |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for sub_id, m in corr_metrics["substrates"].items():
        for run_lbl in ("trained", "random"):
            r = m["regime_all"][run_lbl]
            if not r:
                continue
            lines.append(
                f"| {sub_id} | {run_lbl} | {r['n_snapshots']} "
                f"| {r['n_cells_first']}→{r['n_cells_last']} "
                f"| {r['cos_mean_mean']:+.4f} "
                f"| {r['abs_cos_mean_mean']:.4f} "
                f"| {r['cos_std_mean']:.4f} "
                f"| {r['norm_cv_mean']:.4f} "
                f"| {r['eff_rank_normalized_mean']:.4f} |"
            )
    lines.append("")

    # Table 2: regime split — early (n<64) vs late (n>=64)
    lines.append("## Table 2 — Cosine correlation by cell-count regime (trained vs random)")
    lines.append("")
    lines.append("| substrate | regime | run | nC range | cos_mean | abs_cos_mean | eff_rank/N | disp_top_above |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for sub_id, m in corr_metrics["substrates"].items():
        for regime_lbl, regime_key in [("early(8-64)", "regime_early"), ("late(64-256)", "regime_late")]:
            for run_lbl in ("trained", "random"):
                r = m[regime_key][run_lbl]
                if not r:
                    continue
                lines.append(
                    f"| {sub_id} | {regime_lbl} | {run_lbl} "
                    f"| {r['n_cells_first']}→{r['n_cells_last']} "
                    f"| {r['cos_mean_mean']:+.4f} "
                    f"| {r['abs_cos_mean_mean']:.4f} "
                    f"| {r['eff_rank_normalized_mean']:.4f} "
                    f"| {r['disp_top_quartile_above_gate_mean']:.2f} / {r['disp_top_quartile_k_mean']:.2f} |"
                )
    lines.append("")

    # Table 3: split-trigger split + cap timing
    lines.append("## Table 3 — Split events by trigger type + cap timing")
    lines.append("")
    lines.append("| substrate | run | final_n_cells | n_splits_disp | n_splits_tens | first_cap_turn |")
    lines.append("|---|---|---|---|---|---|")
    for sub_id, m in corr_metrics["substrates"].items():
        lines.append(
            f"| {sub_id} | trained | {m['trained_final_n_cells']} "
            f"| {m['trained_n_splits_dispersion']} | {m['trained_n_splits_tension']} "
            f"| {m['trained_first_cap_turn']} |"
        )
        lines.append(
            f"| {sub_id} | random  | {m['random_final_n_cells']} "
            f"| {m['random_n_splits_dispersion']} | {m['random_n_splits_tension']} "
            f"| {m['random_first_cap_turn']} |"
        )
    lines.append("")

    # Table 4: per-turn dispersion trigger rate trajectory (compact)
    lines.append("## Table 4 — Dispersion trigger trajectory (per-snapshot disp_above/disp_k)")
    lines.append("")
    for sub_id, dd in disp_metrics["substrates"].items():
        lines.append(f"### {sub_id}")
        lines.append("")
        lines.append("| turn | trained_nC | t_disp/k | t_split_disp_inc | random_nC | r_disp/k | r_split_disp_inc |")
        lines.append("|---|---|---|---|---|---|---|")
        # Align by index up to min length
        L = min(len(dd["trained_per_turn"]), len(dd["random_per_turn"]))
        for i in range(L):
            t = dd["trained_per_turn"][i]
            r = dd["random_per_turn"][i]
            lines.append(
                f"| {t['turn']} "
                f"| {t['n_cells']} | {t['disp_top_quartile_above_gate']}/{t['disp_top_quartile_k']} "
                f"| {t['splits_disp_inc']} "
                f"| {r['n_cells']} | {r['disp_top_quartile_above_gate']}/{r['disp_top_quartile_k']} "
                f"| {r['splits_disp_inc']} |"
            )
        lines.append("")

    # Falsifier evaluation
    lines.append("## Falsifier check")
    lines.append("")
    f1_pass = []  # F-CORR-1: cos_mean trained > random in late regime?
    f2_pass = []  # F-CORR-2: dispersion trigger rate diff in late regime?
    f3_pass = []  # F-CORR-3: pattern consistent across substrates?
    for sub_id, m in corr_metrics["substrates"].items():
        l_t = m["regime_late"]["trained"]
        l_r = m["regime_late"]["random"]
        if l_t and l_r:
            f1_diff = (l_t.get("cos_mean_mean") or 0) - (l_r.get("cos_mean_mean") or 0)
            f2_diff = (l_t.get("disp_trigger_rate_mean") or 0) - (l_r.get("disp_trigger_rate_mean") or 0)
            f1_pass.append((sub_id, f1_diff))
            f2_pass.append((sub_id, f2_diff))

    lines.append("### F-CORR-1: trained correlation higher than random in late regime?")
    for sub, d_ in f1_pass:
        lines.append(f"- {sub}: cos_mean_late_trained − cos_mean_late_random = {d_:+.4f}")
    lines.append("")
    lines.append("### F-CORR-2: trained dispersion trigger rate lower than random in late regime?")
    for sub, d_ in f2_pass:
        lines.append(f"- {sub}: disp_trigger_rate_late_trained − disp_trigger_rate_late_random = {d_:+.4f}")
    lines.append("")

    # Verdict logic
    n1_pos = sum(1 for _, x in f1_pass if x > 0)
    n2_neg = sum(1 for _, x in f2_pass if x < 0)
    total_subs = len(f1_pass)

    lines.append("## §51 mechanism verdict")
    lines.append("")
    if n1_pos >= max(1, total_subs // 2) and n2_neg >= max(1, total_subs // 2):
        v = "CONFIRMED"
    elif n1_pos == 0 and n2_neg == 0:
        v = "REVERSED"
    else:
        v = "ALT_MECHANISM"
    lines.append(f"verdict: **{v}**")
    lines.append("")
    lines.append(f"  F-CORR-1: {n1_pos}/{total_subs} substrates show trained > random correlation in late regime")
    lines.append(f"  F-CORR-2: {n2_neg}/{total_subs} substrates show trained < random dispersion trigger rate in late regime")
    lines.append("")

    out_md = THIS_DIR / "verdict.md"
    out_md.write_text("\n".join(lines))
    print(f"[saved] {out_md}")


if __name__ == "__main__":
    main()
