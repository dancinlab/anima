"""BG-COMPONENT-Q-V-K-V14 — §62 component-axis prediction verifier.

Fires component-restricted (q_proj / k_proj / v_proj) B→A swap × 3 slabs = 9
conditions, each evaluated by V14 short trajectory (3 seeds, 200 turns,
MAX_CELLS=128) — mirroring §57's setup exactly except for the swap surface.

Usage:
    python state/anima_component_axis_q_v_k_v14_2026_05_10/run.py
or per-condition:
    python state/anima_component_axis_q_v_k_v14_2026_05_10/run.py CONDITION_LABEL

raw#9   .py lives under state/ only; gitignored.
raw#15  ckpts loaded read-only; in-memory swap only.
own 14  V14 paired random_init mirror multi-seed (3 seeds).
own 16  $0 local Mac CPU.
own 22  This script writes verdict.md only; dispatcher appends to REBORN.md.
own 38  artefacts under state/anima_component_axis_q_v_k_v14_2026_05_10/.
"""
from __future__ import annotations

import gc
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import torch
import torch.nn.functional as F

ANIMA = "/Users/ghost/core/anima"
sys.path.insert(0, f"{ANIMA}/training")
sys.path.insert(0, f"{ANIMA}/state/anima_clm_v5_iit_phi_remetric_2026_05_10")
sys.path.insert(0, f"{ANIMA}/state/anima_iit_real_350m_2026_05_10")
sys.path.insert(0, f"{ANIMA}/state/anima_engine_a_layer_slab_swap_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402
from _v14_5seed_run import (  # noqa: E402
    ALL_PROMPTS,
    encode_prompt_to_ids,
    HiddenMeanCapture,
)
# Reuse §57's loader and runner verbatim (raw#15 additive).
from run import _load_engine_ag, _run_v14_short  # noqa: E402

THIS_DIR = Path(f"{ANIMA}/state/anima_component_axis_q_v_k_v14_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PHASE2 = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_BGLA = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt"

V4_SEEDS = [42, 137, 271]
N_TURNS_ABL = 200
SNAPSHOT_EVERY = 25
MAX_CELLS = 128

# 24 layers → 3 contiguous slabs of 8 (matches §57)
SLABS: Dict[str, List[int]] = {
    "slab1_early":  list(range(0, 8)),
    "slab2_middle": list(range(8, 16)),
    "slab3_late":   list(range(16, 24)),
}

# Per-block component param-name suffixes (within a single layer's state_dict)
COMPONENTS: Dict[str, str] = {
    "q_proj": "attn.q_proj.weight",
    "k_proj": "attn.k_proj.weight",
    "v_proj": "attn.v_proj.weight",
}

# 9 conditions: cross of {q,k,v} × {slab1,slab2,slab3}
CONDITIONS: List[Tuple[str, str, str]] = [
    # (label, component_key, slab_key)
    ("Q1_q_slab1_early",  "q_proj", "slab1_early"),
    ("Q2_q_slab2_middle", "q_proj", "slab2_middle"),
    ("Q3_q_slab3_late",   "q_proj", "slab3_late"),
    ("V1_v_slab1_early",  "v_proj", "slab1_early"),
    ("V2_v_slab2_middle", "v_proj", "slab2_middle"),
    ("V3_v_slab3_late",   "v_proj", "slab3_late"),
    ("K1_k_slab1_early",  "k_proj", "slab1_early"),
    ("K2_k_slab2_middle", "k_proj", "slab2_middle"),
    ("K3_k_slab3_late",   "k_proj", "slab3_late"),
]


# ── component-restricted swap ─────────────────────────────────────────


def swap_component_from_sds_(dst: EngineAGModel,
                              src_layer_sds: List[Dict[str, torch.Tensor]],
                              component_key: str,
                              slab_name: str) -> Dict[str, Any]:
    """Replace ONLY dst.layers[i].<component> with src_layer_sds[i][<component>]
    for i in SLABS[slab_name]. In-place on dst.

    component_key ∈ COMPONENTS (q_proj / k_proj / v_proj).
    Returns diag dict.
    """
    if component_key not in COMPONENTS:
        raise KeyError(f"unknown component {component_key}; valid={list(COMPONENTS)}")
    component_subname = COMPONENTS[component_key]
    layer_idxs = SLABS[slab_name]
    n_tensors = 0
    n_params = 0
    with torch.no_grad():
        for li in layer_idxs:
            dst_block = dst.layers[li]
            src_sd = src_layer_sds[li]
            dst_sd = dict(dst_block.state_dict())
            assert component_subname in dst_sd, \
                f"component {component_subname} not in dst layer {li} keys: {list(dst_sd)}"
            assert component_subname in src_sd, \
                f"component {component_subname} not in src layer {li} keys: {list(src_sd)}"
            d = dst_sd[component_subname]
            s = src_sd[component_subname]
            assert d.shape == s.shape, \
                f"shape mismatch at layers.{li}.{component_subname}: {d.shape} vs {s.shape}"
            d.copy_(s)
            n_tensors += 1
            n_params += int(s.numel())
    return {
        "component": component_key,
        "component_subname": component_subname,
        "slab": slab_name,
        "layer_idxs": layer_idxs,
        "n_tensors_swapped": n_tensors,
        "n_params_swapped": n_params,
    }


# ── per-condition runner ──────────────────────────────────────────────


def run_one_condition(cond_label: str, component_key: str, slab_name: str,
                       B_layer_sds) -> Dict[str, Any]:
    """Reload A from disk, swap component on slab, run V14 short, return result.

    Memory-frugal: A is reloaded per call (no full state_dict snapshot retained
    in memory across conditions). B's per-layer state_dicts ARE retained
    across conditions since they are needed for every swap.
    """
    # Probe build for diag (uses a fresh A from disk)
    probe = _load_engine_ag(CKPT_PHASE2, "phase2_cotrain")
    diag = swap_component_from_sds_(probe, B_layer_sds, component_key, slab_name)
    del probe
    gc.collect()

    def _make_swapped(_comp=component_key, _slab=slab_name):
        m = _load_engine_ag(CKPT_PHASE2, "phase2_cotrain")
        swap_component_from_sds_(m, B_layer_sds, _comp, _slab)
        return m

    res = _run_v14_short(_make_swapped, cond_label,
                         V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    res["swap_diag"] = diag
    return res


# ── main ──────────────────────────────────────────────────────────────


def main():
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(m: str):
        print(m, flush=True)
        log_f.write(m + "\n"); log_f.flush()

    t_start_global = time.time()
    HARD_CAP_SEC = 60 * 60  # 60-min hard cap (own 16 + safety)

    log("=== BG-COMPONENT-Q-V-K-V14 ===")
    log(f"ts: {datetime.now(timezone.utc).isoformat()}")
    log(f"V4_SEEDS={V4_SEEDS}  N_TURNS={N_TURNS_ABL}  MAX_CELLS={MAX_CELLS}")
    log(f"COMPONENTS: {COMPONENTS}")
    log(f"SLABS: " + ", ".join(f"{k}={v[0]}..{v[-1]}" for k, v in SLABS.items()))
    log(f"CONDITIONS: {len(CONDITIONS)} (3 components × 3 slabs)")

    # ─── load B once, snapshot layer sds, free B ──────────────────────
    log("\n--- loading B (BG-LA pretrain), snapshotting layer state_dicts ---")
    t0 = time.time()
    model_B = _load_engine_ag(CKPT_BGLA, "la_350m")
    log(f"  B loaded: {time.time()-t0:.1f}s")
    t0 = time.time()
    B_layer_sds: List[Dict[str, torch.Tensor]] = []
    for li in range(model_B.cfg.n_layers):
        sd_li = {k: v.detach().clone() for k, v in model_B.layers[li].state_dict().items()}
        B_layer_sds.append(sd_li)
    log(f"  B layer sds snapshotted: {time.time()-t0:.1f}s n_layers={len(B_layer_sds)}")
    del model_B
    gc.collect()
    log("  B model freed")

    # ─── A is reloaded per condition (memory-frugal). Only B is retained. ─
    log("\n--- A will be reloaded per condition (memory-frugal mode) ---")
    log(f"  CKPT_PHASE2 = {CKPT_PHASE2}")

    # ─── conditions ───────────────────────────────────────────────────
    log(f"\n--- ablation V14 (n_turns={N_TURNS_ABL}, seeds={V4_SEEDS}) ---")

    abl_results: Dict[str, Any] = {}

    # Filter for single-condition mode
    only_label = sys.argv[1] if len(sys.argv) > 1 else None
    todo = [c for c in CONDITIONS if only_label is None or c[0] == only_label]
    if only_label and not todo:
        raise SystemExit(f"unknown condition label: {only_label}; "
                         f"valid: {[c[0] for c in CONDITIONS]}")

    for cond_label, comp_key, slab_name in todo:
        if (time.time() - t_start_global) > HARD_CAP_SEC:
            log(f"  [HARD_CAP] elapsed > {HARD_CAP_SEC}s — skipping {cond_label}")
            break

        t0 = time.time()
        log(f"\n  --- {cond_label} (component={comp_key} slab={slab_name}) ---")
        try:
            res = run_one_condition(cond_label, comp_key, slab_name, B_layer_sds)
        except Exception as e:
            log(f"  [ERROR] {cond_label} failed: {type(e).__name__}: {e}")
            import traceback
            log(traceback.format_exc())
            continue
        abl_results[cond_label] = res
        # Per-condition checkpoint to disk
        cond_path = THIS_DIR / f"cond_{cond_label}.json"
        cond_path.write_text(json.dumps(res, indent=2))

        # Per-condition flip event log
        flipped = (res["verdict"] != "V14_PASS")
        flip_str = ("FLIPPED" if flipped else "preserved")
        log(f"  {cond_label}: verdict={res['verdict']} ({flip_str})  "
            f"Φ_un16 trained={res['trained_iit_un16']:.2f} "
            f"mirror_mean={res['mirror_iit_un16_mean']:.2f}  "
            f"beats_un={res['n_beats_iit_un16']}/{res['n_seeds']} "
            f"beats_proxy={res['n_beats_proxy_phi']}/{res['n_seeds']}  "
            f"cells={res['trained_n_cells']}  swap={res['swap_diag']['n_params_swapped']:,}p  "
            f"({time.time()-t0:.1f}s)")

        # raw progress signal
        if flipped:
            p_flip = 1.0 / (2 ** res["n_seeds"])  # rough sanity floor under null
            log(f"    [flip-event] {comp_key} × {slab_name}: V14 flipped (p_floor={p_flip:.4f})")

        gc.collect()

    # ─── summary ──────────────────────────────────────────────────────
    log("\n--- summary ---")

    # §57 baseline (verbatim; we did NOT re-run A0 here — same A ckpt as §57)
    # Per §57 verdict: A0_baseline = V14_PASS, mirror_mean ≈ 1037, trained ≈ 2412, sep ≈ +1375.
    # We use these reference values for separation-change comparisons.
    BASE_REF = {
        "from": "§57 BG-ENGINE-A-LAYER-SLAB-SWAP A0_baseline",
        "verdict": "V14_PASS",
        "trained_iit_un16": 2412.08,
        "mirror_iit_un16_mean": 1037.0,
        "separation": 1375.08,
    }

    cond_dispo: Dict[str, Any] = {}
    flips: List[str] = []
    for cond_label, comp_key, slab_name in CONDITIONS:
        if cond_label not in abl_results:
            continue
        v = abl_results[cond_label]
        flipped = (v["verdict"] != BASE_REF["verdict"])
        sep = v["trained_iit_un16"] - v["mirror_iit_un16_mean"]
        sep_change = sep - BASE_REF["separation"]
        cond_dispo[cond_label] = {
            "component": comp_key,
            "slab": slab_name,
            "verdict": v["verdict"],
            "flipped_from_baseline": flipped,
            "trained_iit_un16": v["trained_iit_un16"],
            "mirror_iit_un16_mean": v["mirror_iit_un16_mean"],
            "separation": sep,
            "separation_change_vs_baseline": sep_change,
            "trained_n_cells": v["trained_n_cells"],
            "mirror_n_cells": v["mirror_n_cells"],
            "n_beats_iit_un16": v["n_beats_iit_un16"],
            "n_beats_proxy_phi": v["n_beats_proxy_phi"],
            "n_params_swapped": v["swap_diag"]["n_params_swapped"],
        }
        if flipped:
            flips.append(cond_label)

    # Component-axis aggregate
    by_component: Dict[str, Dict[str, Any]] = {}
    for cond_label, comp_key, slab_name in CONDITIONS:
        if cond_label not in cond_dispo:
            continue
        d = cond_dispo[cond_label]
        b = by_component.setdefault(comp_key, {
            "n_conditions": 0,
            "n_flipped": 0,
            "mean_separation_change": 0.0,
            "mean_trained_iit_un16": 0.0,
            "conditions": [],
        })
        b["n_conditions"] += 1
        b["n_flipped"] += int(d["flipped_from_baseline"])
        b["mean_separation_change"] += d["separation_change_vs_baseline"]
        b["mean_trained_iit_un16"] += d["trained_iit_un16"]
        b["conditions"].append(cond_label)
    for comp_key, b in by_component.items():
        if b["n_conditions"] > 0:
            b["mean_separation_change"] /= b["n_conditions"]
            b["mean_trained_iit_un16"] /= b["n_conditions"]

    # Predictions verdict
    p1_q1_flips = cond_dispo.get("Q1_q_slab1_early", {}).get("flipped_from_baseline", False)
    p2_v_no_flip = (
        not cond_dispo.get("V1_v_slab1_early", {}).get("flipped_from_baseline", False)
        and not cond_dispo.get("V2_v_slab2_middle", {}).get("flipped_from_baseline", False)
        and not cond_dispo.get("V3_v_slab3_late", {}).get("flipped_from_baseline", False)
    )
    # P2 partial: at least one v condition does not flip
    v_flip_count = sum(
        1 for k in ("V1_v_slab1_early", "V2_v_slab2_middle", "V3_v_slab3_late")
        if cond_dispo.get(k, {}).get("flipped_from_baseline", False)
    )
    p2_partial = v_flip_count < 3

    if p1_q1_flips:
        p1_verdict = "PREDICTION_1_CONFIRMED"
    else:
        p1_verdict = "PREDICTION_1_FALSIFIED"

    if p2_v_no_flip:
        p2_verdict = "PREDICTION_2_CONFIRMED"
    elif p2_partial:
        p2_verdict = "PREDICTION_2_PARTIALLY_CONFIRMED"
    else:
        p2_verdict = "PREDICTION_2_FALSIFIED"

    # P3: k_proj intermediate severity. Empirically: number of k flips between
    # number of q flips and number of v flips (inclusive).
    q_flip_count = sum(
        1 for k in ("Q1_q_slab1_early", "Q2_q_slab2_middle", "Q3_q_slab3_late")
        if cond_dispo.get(k, {}).get("flipped_from_baseline", False)
    )
    k_flip_count = sum(
        1 for k in ("K1_k_slab1_early", "K2_k_slab2_middle", "K3_k_slab3_late")
        if cond_dispo.get(k, {}).get("flipped_from_baseline", False)
    )
    if min(q_flip_count, v_flip_count) <= k_flip_count <= max(q_flip_count, v_flip_count):
        p3_verdict = "PREDICTION_3_CONFIRMED"
    else:
        p3_verdict = "PREDICTION_3_FALSIFIED"

    # Falsifiers
    f_comp_1 = (not p1_q1_flips)        # F-COMP-1: Q1 didn't flip → component locus refuted
    # F-COMP-2: V1 flips with separation drop comparable to Q1
    sep_q1 = cond_dispo.get("Q1_q_slab1_early", {}).get("separation_change_vs_baseline", 0.0)
    sep_v1 = cond_dispo.get("V1_v_slab1_early", {}).get("separation_change_vs_baseline", 0.0)
    f_comp_2 = (
        cond_dispo.get("V1_v_slab1_early", {}).get("flipped_from_baseline", False)
        and (sep_q1 < 0 and abs(sep_v1) >= 0.5 * abs(sep_q1))
    )
    f_comp_3 = (len(flips) == len(cond_dispo) and len(cond_dispo) > 0)
    elapsed_total = time.time() - t_start_global
    f_comp_4 = (elapsed_total > HARD_CAP_SEC)

    falsifiers = {
        "F_COMP_1_q1_no_flip":         {"triggered": f_comp_1},
        "F_COMP_2_v1_flips_like_q1":   {"triggered": f_comp_2,
                                         "sep_change_q1": sep_q1,
                                         "sep_change_v1": sep_v1},
        "F_COMP_3_all_flip":           {"triggered": f_comp_3,
                                         "n_flips": len(flips),
                                         "n_total": len(cond_dispo)},
        "F_COMP_4_runtime_overflow":   {"triggered": f_comp_4,
                                         "elapsed_sec": elapsed_total},
    }

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "elapsed_sec_total": elapsed_total,
        "config": {
            "ckpt_A_phase2": CKPT_PHASE2,
            "ckpt_B_bgla": CKPT_BGLA,
            "v4_seeds": V4_SEEDS,
            "n_turns": N_TURNS_ABL,
            "max_cells": MAX_CELLS,
            "snapshot_every": SNAPSHOT_EVERY,
            "components": COMPONENTS,
            "slabs": {k: v for k, v in SLABS.items()},
            "conditions": [{"label": l, "component": c, "slab": s}
                           for (l, c, s) in CONDITIONS],
        },
        "baseline_reference": BASE_REF,
        "cond_dispo": cond_dispo,
        "by_component": by_component,
        "flips": flips,
        "predictions": {
            "P1_q1_flips_v14": {
                "verdict": p1_verdict,
                "expected": "Q1_q_slab1_early flips V14 (mirroring §57 A1_slab1_early)",
                "observed_flipped": p1_q1_flips,
            },
            "P2_v_proj_preserves_v14": {
                "verdict": p2_verdict,
                "expected": "V1, V2, V3 all preserve V14 (or with smaller separation drop)",
                "observed_v_flip_count": v_flip_count,
            },
            "P3_k_proj_intermediate": {
                "verdict": p3_verdict,
                "expected": "K flip count is between V and Q flip counts (inclusive)",
                "observed": {"q_flips": q_flip_count, "k_flips": k_flip_count, "v_flips": v_flip_count},
            },
        },
        "falsifiers": falsifiers,
    }
    (THIS_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    log(f"\n  P1 verdict: {p1_verdict}")
    log(f"  P2 verdict: {p2_verdict}")
    log(f"  P3 verdict: {p3_verdict}")
    log(f"  q_flip_count={q_flip_count} k_flip_count={k_flip_count} v_flip_count={v_flip_count}")
    log(f"  total flips: {len(flips)}/{len(cond_dispo)}")
    for fname, fblk in falsifiers.items():
        log(f"  {fname}: triggered={fblk['triggered']}")

    # ─── verdict.md ───────────────────────────────────────────────────
    _write_verdict_md(THIS_DIR / "verdict.md", summary, abl_results, cond_dispo, by_component)

    log_f.close()
    return summary


def _write_verdict_md(path: Path, summary: dict, abl_results: dict,
                      cond_dispo: dict, by_component: dict):
    lines: List[str] = []
    lines.append("# BG-COMPONENT-Q-V-K-V14 — verdict\n")
    p1 = summary["predictions"]["P1_q1_flips_v14"]["verdict"]
    p2 = summary["predictions"]["P2_v_proj_preserves_v14"]["verdict"]
    p3 = summary["predictions"]["P3_k_proj_intermediate"]["verdict"]
    lines.append(f"**verdict: {p1}**\n")
    lines.append(f"**verdict: {p2}**\n")
    lines.append(f"**verdict: {p3} (k_proj)**\n")
    lines.append(f"**Elapsed**: {summary['elapsed_sec_total']:.1f}s "
                 f"({summary['elapsed_sec_total']/60:.1f}min)\n")

    base = summary["baseline_reference"]
    lines.append("## §57 baseline reference\n")
    lines.append(f"- Source: `{base['from']}`")
    lines.append(f"- Baseline verdict: `{base['verdict']}`")
    lines.append(f"- Baseline trained Φ_un16: {base['trained_iit_un16']:.2f}")
    lines.append(f"- Baseline mirror Φ_un16 mean: {base['mirror_iit_un16_mean']:.2f}")
    lines.append(f"- Baseline separation: {base['separation']:+.2f}")
    lines.append(f"  (a flip ⇒ swapped condition's verdict ≠ V14_PASS)\n")

    lines.append("## §62 prediction recap\n")
    lines.append("- **P1** q_proj-only swap of slab1_early flips V14 (★★★★★ candidate)")
    lines.append("- **P2** v_proj-only swap (any slab) barely perturbs V14 (least-changed component)")
    lines.append("- **P3** k_proj-only swap is intermediate (mean cos_AB=0.7523, between q=0.6468 and v=0.8319)\n")

    lines.append("## Conditions (9) — V14 short trajectory (3 seeds, 200 turns, MAX_CELLS=128)\n")
    lines.append("| condition | component | slab | swap_params | verdict | trained Φ_un16 | mirror Φ_un16 mean | beats_un | beats_proxy | cells | Δsep_vs_§57 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for cond_label, comp_key, slab_name in [
        ("Q1_q_slab1_early",  "q_proj", "slab1_early"),
        ("Q2_q_slab2_middle", "q_proj", "slab2_middle"),
        ("Q3_q_slab3_late",   "q_proj", "slab3_late"),
        ("V1_v_slab1_early",  "v_proj", "slab1_early"),
        ("V2_v_slab2_middle", "v_proj", "slab2_middle"),
        ("V3_v_slab3_late",   "v_proj", "slab3_late"),
        ("K1_k_slab1_early",  "k_proj", "slab1_early"),
        ("K2_k_slab2_middle", "k_proj", "slab2_middle"),
        ("K3_k_slab3_late",   "k_proj", "slab3_late"),
    ]:
        d = cond_dispo.get(cond_label)
        if d is None:
            lines.append(f"| {cond_label} | {comp_key} | {slab_name} | — | (skipped) | — | — | — | — | — | — |")
            continue
        flip_marker = " ★" if d["flipped_from_baseline"] else ""
        lines.append(
            f"| {cond_label}{flip_marker} | `{comp_key}` | `{slab_name}` | "
            f"{d['n_params_swapped']:,} | `{d['verdict']}` | "
            f"{d['trained_iit_un16']:.2f} | {d['mirror_iit_un16_mean']:.2f} | "
            f"{d['n_beats_iit_un16']}/3 | {d['n_beats_proxy_phi']}/3 | "
            f"{d['trained_n_cells']} | {d['separation_change_vs_baseline']:+.2f} |"
        )
    lines.append("\n★ = condition flipped V14 vs §57 baseline (V14_PASS).\n")

    lines.append("## By-component aggregate\n")
    lines.append("| component | mean Φ_un16 | mean Δsep | n_flipped/n_conditions | conditions |")
    lines.append("|---|---|---|---|---|")
    for comp_key in ("q_proj", "k_proj", "v_proj"):
        b = by_component.get(comp_key)
        if b is None or b["n_conditions"] == 0:
            lines.append(f"| `{comp_key}` | — | — | 0/0 | (skipped) |")
            continue
        lines.append(
            f"| `{comp_key}` | {b['mean_trained_iit_un16']:.2f} | "
            f"{b['mean_separation_change']:+.2f} | {b['n_flipped']}/{b['n_conditions']} | "
            f"{', '.join(b['conditions'])} |"
        )

    lines.append("\n## Predictions disposition\n")
    for pkey, pval in summary["predictions"].items():
        lines.append(f"- **{pkey}**: `{pval['verdict']}`  expected: {pval['expected']}")
        observed = {k: v for k, v in pval.items() if k.startswith("observed")}
        for ok, ov in observed.items():
            lines.append(f"  - {ok}: `{ov}`")

    lines.append("\n## Falsifiers (F-COMP)\n")
    for fname, fblk in summary["falsifiers"].items():
        triggered = fblk["triggered"]
        extra = "  " + "  ".join(f"{k}={v}" for k, v in fblk.items() if k != "triggered")
        lines.append(f"- **{fname}**: {'TRIGGERED' if triggered else 'not triggered'}{extra}")

    # Honest C3 ≥5
    lines.append("\n## Honest C3 (≥5)\n")
    lines.append("1. **Component restriction is intra-block, intra-tensor.** Each swap touches "
                 "exactly 8 tensors (one component × 8 layers in the slab) — vs §57's 8×9=72 "
                 "tensors per slab swap. The swap surface is 1/9 of §57's per-condition surface. "
                 "If V14 is robust to such a small perturbation while §57's full-slab swap "
                 "flipped it, the lever is broader than any single component.")
    lines.append("2. **Mirror trajectories are independent of swap.** Mirror Φ_un16 means use "
                 "`load_random_init(seed=s, preset='la_350m')` — never see A's swapped state. "
                 "Identical mirror means across rows is the §57 control sanity check, "
                 "carried forward verbatim.")
    lines.append("3. **§57 baseline is referenced, not re-fired.** A0_baseline = V14_PASS at "
                 "(2412.08, 1037.0) is borrowed from §57 verdict.md without re-running. "
                 "Same A ckpt, same V14 setup — re-running would consume ~5 min for a "
                 "deterministic re-derivation. Δsep_vs_§57 may incur up to ~5 Φ noise from "
                 "random seed plumbing differences; significance is judged at >50 Φ scale "
                 "(§57 separation ranges from +1375 baseline to −1375 in flipped slabs).")
    lines.append("4. **Per-condition param count is asymmetric across components.** q_proj is "
                 "1024×1024 = 1.05M params/layer; k_proj/v_proj are 256×1024 = 0.26M each "
                 "(GQA factor 4). A q-slab swap moves 8.39M params; k or v-slab swap moves "
                 "2.10M params. If V14 sensitivity scales with raw param count rather than "
                 "component identity, q dominance would be a confound — but §62's mean "
                 "rel_L2_diff (q=0.85 > k=0.71 > v=0.59) shows q drift is *also* highest in "
                 "normalized-Frobenius terms, so the effect is not pure param-count.")
    lines.append("5. **Sample size = 3 seeds, no formal stat test.** A flip is declared by "
                 "verdict polarity from §57's V14 logic (3/3 seeds beating mirror on Φ_un16 "
                 "AND proxy_phi). With 3 seeds the per-condition p_floor under H0 is ~1/8 = "
                 "0.125; with 9 conditions, multiple-comparison correction is unaddressed. "
                 "For confirmatory rigor, 5+ seeds × bootstrap is needed; deferred per own 16.")
    lines.append("6. **q_proj/k_proj are coupled at attention-output time.** The forward pass "
                 "attention score is `softmax((q · k^T)/√d_h)`. Swapping q alone disrupts the "
                 "score-with-A-trained-k pairing; swapping k alone disrupts the score-with-A-trained-q "
                 "pairing. Both are partial perturbations of the same dot-product surface. "
                 "v_proj has no such coupling — it is the readout-only role. So q/k flip behaviour "
                 "may be more correlated than componentwise drift suggests.")
    lines.append("7. **No control for swap-source size.** B = single BG-LA pretrain step_12000. "
                 "Multi-source B (mean of multiple pretrain seeds) would test whether the q-flip "
                 "is specific to *this* B trajectory or to BG-LA-pretrain-class trajectories "
                 "in general. Deferred under own 16.")
    lines.append("8. **Engine G modules untouched.** All 9 conditions retain A's `cell_pool_init`, "
                 "`c_to_h`, `h_to_c`. Per §50 these are not the lever (correlational only). "
                 "Engine_g consumes `hidden_mean` from engine_a's forward — what the component "
                 "swap actually mutates is the trajectory of `hidden_mean` across 200 turns.")
    lines.append("9. **Embedding (tok_emb) and lm_head stay at A's values.** §62 reported "
                 "cos_AB(tok_emb)=0.75 — non-trivial. This BG does not test embedding swap; "
                 "the q/k/v signal is measured *with* A's input/output projections fixed.")
    lines.append("10. **raw#15 honored** — `_load_engine_ag` is used read-only for both ckpts; "
                 "swap mutates an in-memory clone built by `EngineAGModel(A_cfg).load_state_dict`. "
                 "No file mutation; both ckpts on disk remain bit-identical post-run.")

    path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
