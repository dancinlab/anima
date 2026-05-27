"""aggregate.py — collect cond_*.json results, build slab_mapping.json,
ablation_per_slab.json, summary.json, verdict.md.

Run after run_one_condition.py for all 4 conditions has emitted cond_*.json.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import torch

ANIMA = "/Users/ghost/core/anima"
sys.path.insert(0, f"{ANIMA}/training")
sys.path.insert(0, f"{ANIMA}/state/anima_engine_a_layer_slab_swap_2026_05_10")

from engine_a_g_arch import EngineAGConfig, EngineAGModel  # noqa
from run import build_slab_mapping, SLABS, V4_SEEDS, N_TURNS_ABL, MAX_CELLS  # noqa
from run import _write_verdict_md  # noqa

THIS_DIR = Path(f"{ANIMA}/state/anima_engine_a_layer_slab_swap_2026_05_10")

CONDITIONS = [
    ("A0_baseline",     None),
    ("A1_slab1_early",  "slab1_early"),
    ("A2_slab2_middle", "slab2_middle"),
    ("A3_slab3_late",   "slab3_late"),
]


def main():
    # Build slab_mapping.json from a fresh A model (no ckpt load required, just config)
    cfg = EngineAGConfig.phase2_cotrain_350m()
    dummy = EngineAGModel(cfg)
    slab_map = build_slab_mapping(dummy)
    (THIS_DIR / "slab_mapping.json").write_text(json.dumps(slab_map, indent=2))
    del dummy

    # Load each cond_*.json
    abl_results: Dict[str, Any] = {}
    for cond_label, slab_name in CONDITIONS:
        path = THIS_DIR / f"cond_{cond_label}.json"
        if not path.exists():
            print(f"MISSING: {path}", file=sys.stderr)
            sys.exit(2)
        abl_results[cond_label] = json.loads(path.read_text())

    # ─── verdict logic ────────────────────────────────────────────────
    base_v = abl_results["A0_baseline"]["verdict"]
    base_phi = abl_results["A0_baseline"]["trained_iit_un16"]
    base_mirror = abl_results["A0_baseline"]["mirror_iit_un16_mean"]
    base_sep = base_phi - base_mirror

    slab_dispo: Dict[str, Any] = {}
    flips: List[str] = []
    cond_to_slab = [(c, s) for c, s in CONDITIONS if s is not None]
    for cond_label, slab_name in cond_to_slab:
        v = abl_results[cond_label]
        flipped = (v["verdict"] != base_v)
        sep = v["trained_iit_un16"] - v["mirror_iit_un16_mean"]
        sep_change = sep - base_sep
        slab_dispo[cond_label] = {
            "slab": slab_name,
            "verdict": v["verdict"],
            "flipped_from_baseline": flipped,
            "trained_iit_un16": v["trained_iit_un16"],
            "mirror_iit_un16_mean": v["mirror_iit_un16_mean"],
            "separation": sep,
            "separation_change_vs_baseline": sep_change,
            "trained_n_cells": v["trained_n_cells"],
        }
        if flipped:
            flips.append(cond_label)

    f_slab_1 = (len(flips) == 0)
    f_slab_2 = (flips == ["A1_slab1_early"])

    # Sum elapsed across conds
    elapsed_total = sum(abl_results[c]["elapsed_total_sec_with_load"] for c, _ in CONDITIONS)
    f_slab_3 = (elapsed_total > 5 * 3600)

    if f_slab_1:
        dominant_slab = "DISTRIBUTED"
        verdict_label = "F-SLAB-1 PASSED — V14 lever distributed across 24 layers"
        star_credit = "★★★★ partial credit (refined hypothesis preserved at body-level)"
    else:
        flipped_dispo = [(k, slab_dispo[k]["separation_change_vs_baseline"])
                         for k in flips]
        flipped_dispo.sort(key=lambda x: x[1])
        dominant_slab = flipped_dispo[0][0] if flipped_dispo else "NONE"
        if len(flips) == 1:
            verdict_label = f"single-slab flip — {dominant_slab}"
            star_credit = "★★★★★ candidate (specific layer locus localized)"
        else:
            verdict_label = f"multi-slab flip — dominant={dominant_slab} (largest separation drop)"
            star_credit = "★★★★ partial (multiple slabs implicated)"

    # ablation_per_slab.json
    (THIS_DIR / "ablation_per_slab.json").write_text(json.dumps(abl_results, indent=2))

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "elapsed_sec_total": elapsed_total,
        "config": {
            "ckpt_A_phase2": "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
            "ckpt_B_bgla":  "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt",
            "v4_seeds": V4_SEEDS,
            "n_turns": N_TURNS_ABL,
            "max_cells": MAX_CELLS,
            "snapshot_every": 25,
            "slabs": {k: list(v) for k, v in SLABS.items()},
        },
        "slab_dispo": slab_dispo,
        "baseline": {
            "verdict": base_v,
            "trained_iit_un16": base_phi,
            "mirror_iit_un16_mean": base_mirror,
            "separation": base_sep,
        },
        "falsifiers": {
            "F_SLAB_1_distributed_all_pass": {"triggered": f_slab_1},
            "F_SLAB_2_early_only_flips":     {"triggered": f_slab_2},
            "F_SLAB_3_runtime_overflow":     {"triggered": f_slab_3, "elapsed_sec": elapsed_total},
        },
        "flips": flips,
        "dominant_slab": dominant_slab,
        "verdict_label": verdict_label,
        "star_credit": star_credit,
    }
    (THIS_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    _write_verdict_md(THIS_DIR / "verdict.md", summary, slab_map, abl_results, slab_dispo)

    print("=== aggregate done ===")
    print(f"baseline verdict: {base_v}  Φ_un16={base_phi:.2f}  mirror_mean={base_mirror:.2f}")
    for c, _ in cond_to_slab:
        d = slab_dispo[c]
        print(f"  {c}: verdict={d['verdict']} flipped={d['flipped_from_baseline']}"
              f" Φ_sep={d['separation']:+.2f} (Δ={d['separation_change_vs_baseline']:+.2f})")
    print(f"dominant_slab={dominant_slab}")
    print(f"verdict_label={verdict_label}")
    print(f"star_credit={star_credit}")


if __name__ == "__main__":
    main()
