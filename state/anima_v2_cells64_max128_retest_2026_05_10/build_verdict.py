"""build_verdict.py — post-process result.json into verdict.md (own 38).

Generates:
  - verdict.md: human-readable summary, race-vs-marathon, cap diagnostic, falsifier ledger
  - Comparison vs §37 (state/anima_v5mitosis_d384_sweep_2026_05_10/result.json)

raw#9: local-only build script (gitignored)
own 38: doc-save deliverable

Usage:
  python build_verdict.py [--in result.json] [--out verdict.md]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def closest_at(traj: List[List], t_target: int) -> Optional[List]:
    if not traj:
        return None
    return min(traj, key=lambda e: abs(e[0] - t_target))


def fmt_run(label: str, run: Dict, t_targets=(50, 100, 150, 200, 250, 299)) -> str:
    lines = [f"### {label}"]
    lines.append(f"- final: n_cells={run['final_n_cells']} phi={run['phi_final']:.2f} phi/c={run['phi_per_cell_final']:.3f}")
    lines.append(f"- best: phi={run['phi_best']:.2f} phi/c={run['phi_per_cell_best']:.3f}")
    lines.append(f"- max_n_cells_observed={run['max_n_cells_observed']}  splits={run['splits']} (dispersion={run['splits_by_dispersion']})  ratchets={run['ratchets']}  merges={run['merges']}")
    if run.get('alpha_v2') is not None:
        lines.append(f"- alpha_v2={run['alpha_v2']:.4f}")
    lines.append("- trajectory checkpoints (turn → n_cells, phi, phi/c):")
    for t in t_targets:
        e = closest_at(run['phi_trajectory'], t)
        if e is None:
            continue
        lines.append(f"  - t≈{e[0]}: n={e[1]} phi={e[2]:.2f} phi/c={e[3]:.3f}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", default="result.json")
    ap.add_argument("--out", dest="out_path", default="verdict.md")
    ap.add_argument("--ref-37", default="/Users/ghost/core/anima/state/anima_v5mitosis_d384_sweep_2026_05_10/result.json")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent
    in_path = (base / args.in_path) if not Path(args.in_path).is_absolute() else Path(args.in_path)
    out_path = (base / args.out_path) if not Path(args.out_path).is_absolute() else Path(args.out_path)

    with in_path.open() as f:
        r = json.load(f)
    cfg = r["config"]
    t_run = r["trained"]
    rs = r["random"]
    v = r["v14_verdict"]

    n_turns = cfg["turns"]
    max_cells = cfg["max_cells"]

    # Race-vs-marathon checkpoints
    pcts = [int(n_turns * f) for f in (0.1, 0.33, 0.5, 0.67, 1.0)]
    pcts = sorted(set(pcts))

    # Cap-bound diagnostics: which turn did each run first reach max_cells?
    def first_at_cap(traj):
        for e in traj:
            if e[1] >= max_cells:
                return e[0]
        return None

    cap_t_trained = first_at_cap(t_run["phi_trajectory"])
    cap_t_random = [first_at_cap(rr["phi_trajectory"]) for rr in rs]

    # §37 reference
    ref37 = None
    try:
        with open(args.ref_37) as f:
            ref37 = json.load(f)
    except Exception:
        ref37 = None

    # Verdict matrix (mission)
    cap_bound_now = v["cap_bound_at_max_cells"]
    trained_pass = v["trained_beats_all_random_phi"] and v["trained_beats_all_random_phi_per_cell"]
    if cap_t_trained is not None and cap_t_trained < 100:
        meta_verdict = "V14_INDETERMINATE_CAP_HIT_BEFORE_100 (F-1 fired)"
    elif cap_bound_now and not trained_pass:
        meta_verdict = "V14_VIOLATED_CONFIRMED (★★★★ substrate-polarity reinforced; max=128 cap still hit)"
    elif (not cap_bound_now) and trained_pass:
        meta_verdict = "V14_VIOLATED_CAP_ARTIFACT (F-2 fired; §37 polarity downgraded)"
    elif (not cap_bound_now) and (not trained_pass):
        meta_verdict = "V14_VIOLATED_CONFIRMED_CAP_FREE (★★★★★ strongest substrate-polarity evidence)"
    elif cap_bound_now and trained_pass:
        meta_verdict = "V14_PARTIAL_CAP_BOUND (substrate-polarity at max=128 cap; cap-free still untested)"
    else:
        meta_verdict = "V14_INDETERMINATE"

    # Marathon attrition: phi_best - phi_final
    def attrition(run):
        return run["phi_best"] - run["phi_final"]

    out_lines = []
    out_lines.append(f"# BG-V2-CELLS64-MAX128-RETEST — verdict")
    out_lines.append("")
    out_lines.append(f"**Meta-verdict**: {meta_verdict}")
    out_lines.append(f"**Engine verdict (5-seed strict)**: {v['verdict']}")
    out_lines.append(f"**ts (result.json)**: {r['ts']}")
    out_lines.append("")
    out_lines.append("## Config (override key)")
    out_lines.append(f"- d_model={cfg['d_model']}, n_head={cfg['n_head']}, ffn_dim={cfg['ffn_dim']}, max_seq={cfg['max_seq']}")
    out_lines.append(f"- initial_cells={cfg['initial_cells']}, **max_cells={max_cells}** (§37 was 64)")
    out_lines.append(f"- turns={n_turns} (§37 was 200)")
    out_lines.append(f"- seeds={cfg['seeds']} (mirror §37)")
    out_lines.append(f"- §30 all-fix: {cfg['all_fix_30']}")
    out_lines.append("")

    out_lines.append("## V14 verdict (engine)")
    out_lines.append(f"- trained: phi={v['trained_phi_final']:.2f} phi/c={v['trained_phi_per_cell_final']:.3f} n={v['trained_n_cells_final']} α={v['trained_alpha_v2']}")
    out_lines.append(f"- random_mean: phi={v['random_phi_final_mean']:.2f} phi/c={v['random_phi_per_cell_final_mean']:.3f} n={v['random_n_cells_final_mean']:.1f} α={v['random_alpha_v2_mean']}")
    out_lines.append(f"- separation: phi={v['separation_phi']:+.2f} phi/c={v['separation_phi_per_cell']:+.3f} α={v['separation_alpha']}")
    out_lines.append(f"- trained_beats_all: phi={v['trained_beats_all_random_phi']} phi/c={v['trained_beats_all_random_phi_per_cell']}")
    out_lines.append(f"- cap_bound_at_max_cells={v['cap_bound_at_max_cells']} (max={max_cells})")
    out_lines.append("")

    out_lines.append("## Cap-bound diagnostic")
    out_lines.append(f"- TRAINED first reached n_cells={max_cells} at turn={cap_t_trained}")
    for rr, ct in zip(rs, cap_t_random):
        out_lines.append(f"- RANDOM_s{rr['seed']} first reached n_cells={max_cells} at turn={ct}")
    out_lines.append("")

    out_lines.append("## Race-vs-marathon")
    chkpts = sorted({pcts[0], pcts[len(pcts)//2], pcts[-1]} | {100, n_turns//2 if n_turns//2 >= 200 else n_turns - 1, n_turns - 1})
    out_lines.append(f"Checkpoints: {chkpts}")
    out_lines.append("")
    out_lines.append("| label | " + " | ".join(f"t≈{c}" for c in chkpts) + " | best | attrition |")
    out_lines.append("|---|" + "|".join("---" for _ in chkpts) + "|---|---|")
    for label, run in [("TRAINED", t_run)] + [(f"RANDOM_s{rr['seed']}", rr) for rr in rs]:
        cells = []
        for c in chkpts:
            e = closest_at(run["phi_trajectory"], c)
            if e is None:
                cells.append("—")
            else:
                cells.append(f"n={e[1]} phi={e[2]:.0f}")
        cells.append(f"phi_best={run['phi_best']:.0f}")
        cells.append(f"{attrition(run):+.0f}")
        out_lines.append(f"| {label} | " + " | ".join(cells) + " |")
    out_lines.append("")

    out_lines.append("## Per-run detail")
    out_lines.append(fmt_run("TRAINED", t_run))
    out_lines.append("")
    for rr in rs:
        out_lines.append(fmt_run(f"RANDOM_s{rr['seed']}", rr))
        out_lines.append("")

    out_lines.append("## Comparison to §37 (max=64, 200 turns)")
    if ref37 is not None:
        ref_v = ref37["v14_verdict"]
        ref_t = ref37["trained"]
        ref_rs = ref37["random"]
        out_lines.append(f"- §37 verdict: {ref_v['verdict']}, max_cells={ref_v['max_cells_setting']}")
        out_lines.append(f"  - §37 trained: phi={ref_t['phi_final']:.2f} phi/c={ref_t['phi_per_cell_final']:.3f} n={ref_t['final_n_cells']}")
        out_lines.append(f"  - §37 random_mean: phi={ref_v['random_phi_final_mean']:.2f}")
        out_lines.append(f"  - §37 sep_phi={ref_v['separation_phi']:+.2f}, this sep_phi={v['separation_phi']:+.2f}")
        # cap-hit comparison
        ref_cap = max(ref_t['max_n_cells_observed'], max(rr['max_n_cells_observed'] for rr in ref_rs))
        out_lines.append(f"  - §37 max_n_cells_observed across all runs: {ref_cap}")
    out_lines.append("")

    out_lines.append("## Falsifier ledger")
    f1 = "FIRED" if (cap_t_trained is not None and cap_t_trained < 100) else "NOT FIRED"
    out_lines.append(f"- F-V2-CELLS64-MAX128-1 (cap-bound before turn 100, §30 fundamental limit): {f1}")
    f2 = "FIRED" if ((not cap_bound_now) and trained_pass) else "NOT FIRED"
    out_lines.append(f"- F-V2-CELLS64-MAX128-2 (trained PASS at cap-free → §37 simple cap artifact): {f2}")
    # F-3: marathon attrition. Compare attrition vs §37
    if ref37 is not None:
        ref_t = ref37["trained"]
        f3_now = attrition(t_run)
        f3_ref = attrition(ref_t)
        f3 = "FIRED" if f3_now > f3_ref * 1.5 else "NOT FIRED"
        out_lines.append(f"- F-V2-CELLS64-MAX128-3 (1K marathon attrition > §37): {f3} (this trained attrition={f3_now:.1f}, §37 trained attrition={f3_ref:.1f})")
    out_lines.append("")

    out_path.write_text("\n".join(out_lines))
    print(f"[saved] {out_path}")
    print(f"\n=== META-VERDICT: {meta_verdict} ===")
    print(f"Engine: {v['verdict']}")


if __name__ == "__main__":
    main()
