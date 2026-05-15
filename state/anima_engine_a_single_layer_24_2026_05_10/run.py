"""BG-ENGINE-A-SINGLE-LAYER-ABLATION-24 — §57 follow-up at single-layer resolution.

Mission: Localize the V14 PASS lever to specific individual layers within
engine_a's 24 layers by single-layer B↔A swap (24 conditions, one layer at a time).

Predecessor: §57 BG-ENGINE-A-LAYER-SLAB-SWAP. All 3 8-layer slab swaps flipped V14
(★★★★ partial). A1_slab1_early uniquely dominant (its own attractor n=44 Φ≈1037);
A2/A3 bit-identical (shared attractor n=43 Φ≈1343). Single-layer resolution required.

Substrates (mirror §57):
  A = Phase 2 cotrain ckpt (chat dual loss)   path: phase2_cotrain_engine_ag/ckpts/ckpt_final.pt
  B = BG-LA pretrain ckpt (persona only)      path: bg_la_350m_pretrain/ckpts/step_12000_final.pt

Conditions (25):
  A0     : baseline pristine A
  L0..L23: A with layer i ← B's layer i (24 conditions)

V14 mirror: V4_SEEDS=[42, 137, 271], N_TURNS=200, MAX_CELLS=128.

Mirror caching: per §57 C3#1 mirror trajectories are independent of swap. We
compute mirrors once (3 seeds × 200 turns) and reuse across all 25 conditions.

Falsifiers :
  F-SINGLE-1 0 layers flip      → distributed/cumulative effect
  F-SINGLE-2 1-3 layers flip    → ★★★★★ specific locus
  F-SINGLE-3 runtime > 5h       → abort with partial result

raw#9   training/*.py local-only; lives under state/ (gitignored)
raw#15  additive — both ckpts loaded read-only; in-memory swap only
  V14 paired random_init mirror multi-seed
  $0 local Mac CPU
  honest emit; REBORN.md no direct append
  artefacts under state/anima_engine_a_single_layer_24_2026_05_10/
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import torch

# Wire to upstream modules (additive, raw#15)
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

THIS_DIR = Path(f"{ANIMA}/state/anima_engine_a_single_layer_24_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PHASE2 = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_BGLA = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt"

V4_SEEDS = [42, 137, 271]
N_TURNS_ABL = 200
SNAPSHOT_EVERY = 25
MAX_CELLS = 128
N_LAYERS = 24

# ─── ckpt loaders (mirror §57) ────────────────────────────────────────


def _load_engine_ag(ckpt_path: str, lineage: str) -> EngineAGModel:
    cfg = (
        EngineAGConfig.phase2_cotrain_350m()
        if lineage == "phase2_cotrain"
        else EngineAGConfig.la_350m()
    )
    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    if "model" in payload:
        sd = payload["model"]
    elif "state_dict" in payload:
        sd = payload["state_dict"]
    else:
        raise KeyError(f"ckpt has neither 'model' nor 'state_dict' (keys={list(payload.keys())})")
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd.items()}
    model = EngineAGModel(cfg)
    miss, unexp = model.load_state_dict(sd_fp32, strict=True)
    if miss or unexp:
        raise RuntimeError(f"ckpt load mismatch miss={len(miss)} unexp={len(unexp)}")
    return model


# ─── single-layer swap ────────────────────────────────────────────────


def swap_one_layer_(dst: EngineAGModel,
                    src_layer_sds: List[Dict[str, torch.Tensor]],
                    layer_idx: int) -> Dict[str, Any]:
    """Replace dst.layers[layer_idx].* with src_layer_sds[layer_idx]. In-place on dst.

    src_layer_sds is a length-n_layers list of state_dicts (snapshotted from B).
    Returns: diag dict {n_tensors_swapped, n_params_swapped, layer_idx}.
    """
    n_tensors = 0
    n_params = 0
    with torch.no_grad():
        dst_block = dst.layers[layer_idx]
        src_sd = src_layer_sds[layer_idx]
        dst_sd = dict(dst_block.state_dict())
        assert set(dst_sd.keys()) == set(src_sd.keys()), \
            f"key set mismatch at layer {layer_idx}"
        for k in dst_sd.keys():
            d = dst_sd[k]
            s = src_sd[k]
            assert d.shape == s.shape, \
                f"shape mismatch at layers.{layer_idx}.{k}: {d.shape} vs {s.shape}"
            d.copy_(s)
            n_tensors += 1
            n_params += int(s.numel())
    return {
        "layer_idx": layer_idx,
        "n_tensors_swapped": n_tensors,
        "n_params_swapped": n_params,
    }


# ─── single trajectory runner ─────────────────────────────────────────


def _run_one_trajectory(M: EngineAGModel, sublabel: str, seed: int,
                        n_turns: int, snap_every: int, max_cells: int,
                        ctx_T: int = 16) -> Dict[str, Any]:
    """Run a single V14 trajectory (one model, one seed). Returns dict with snapshots."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    M.eval()
    cap = HiddenMeanCapture(M.engine_g)
    eg = M.engine_g
    init_pool = eg.cell_pool_init.detach().clone()
    n_cells_init = init_pool.shape[0]
    mit = MitosisV5Engine(
        cell_pool=init_pool, c_to_h=eg.c_to_h,
        initial_cells=n_cells_init, max_cells=max_cells,
        split_patience=3, split_noise=0.10,
        merge_threshold=0.005, merge_patience=30, min_cells=2,
        lorenz_scale=0.05,
    )
    snaps = []
    n_splits = 0
    n_merges = 0
    cap_bound_turns = 0
    t0 = time.time()
    with torch.no_grad():
        for turn in range(n_turns):
            cat, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
            ids = encode_prompt_to_ids(prompt, T=ctx_T)
            _ = M(ids, output_hidden_states=False, output_attentions=False)
            hm = cap.last_hidden_mean
            if hm is None:
                cell_input = torch.zeros(1, eg.c_dim)
            else:
                cell_input = eg.h_to_c(hm)
            out = mit.process(cell_input)
            for ev in out["events"]:
                if ev["type"] == "split":
                    n_splits += 1
                elif ev["type"] == "merge":
                    n_merges += 1
            if out["n_cells"] >= max_cells:
                cap_bound_turns += 1
            if turn % snap_every == 0 or turn == n_turns - 1:
                cp = mit.cell_pool.detach().cpu().numpy()
                phi_iit = compute_iit_phi(torch.tensor(cp, dtype=torch.float32), n_bins=16)
                snaps.append({
                    "turn": int(turn),
                    "n_cells": int(out["n_cells"]),
                    "proxy_phi": float(out["phi"]),
                    "iit_phi_unnorm_b16": phi_iit["spatial_phi_unnormalized"],
                    "iit_phi_norm_b16": phi_iit["spatial_phi"],
                    "n_splits_cum": int(n_splits),
                })
    return {
        "label": sublabel,
        "seed": seed,
        "elapsed_sec": time.time() - t0,
        "snapshots": snaps,
        "final_n_cells": int(mit.n_cells),
        "n_splits": n_splits,
        "n_merges": n_merges,
        "cap_bound_turns": cap_bound_turns,
        "final_iit_un16": snaps[-1]["iit_phi_unnorm_b16"] if snaps else float("nan"),
        "final_proxy_phi": snaps[-1]["proxy_phi"] if snaps else float("nan"),
    }


def _aggregate_v14(label: str, tr: Dict[str, Any],
                   mirrors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute V14 verdict from one trained run + cached mirror runs."""
    rs_un = [m["final_iit_un16"] for m in mirrors]
    rs_proxy = [m["final_proxy_phi"] for m in mirrors]
    rs_cells = [m["final_n_cells"] for m in mirrors]
    n_beats_un = sum(1 for r in rs_un if tr["final_iit_un16"] > r)
    n_beats_proxy = sum(1 for r in rs_proxy if tr["final_proxy_phi"] > r)
    if n_beats_un == len(mirrors) and n_beats_proxy == len(mirrors):
        verdict = "V14_PASS"
    elif n_beats_un == len(mirrors) or n_beats_proxy == len(mirrors):
        verdict = "V14_PARTIAL"
    else:
        verdict = "V14_VIOLATED"
    return {
        "label": label,
        "trained": tr,
        "verdict": verdict,
        "n_beats_iit_un16": n_beats_un,
        "n_beats_proxy_phi": n_beats_proxy,
        "n_seeds": len(mirrors),
        "trained_iit_un16": tr["final_iit_un16"],
        "mirror_iit_un16_mean": float(np.mean(rs_un)),
        "mirror_iit_un16_min": float(np.min(rs_un)),
        "mirror_iit_un16_max": float(np.max(rs_un)),
        "mirror_iit_un16_per_seed": rs_un,
        "trained_proxy_phi": tr["final_proxy_phi"],
        "mirror_proxy_phi_mean": float(np.mean(rs_proxy)),
        "trained_n_cells": tr["final_n_cells"],
        "mirror_n_cells": rs_cells,
        "elapsed_total_sec": tr["elapsed_sec"],  # mirror time excluded (cached)
    }


# ─── main ─────────────────────────────────────────────────────────────


def main():
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(m: str):
        print(m, flush=True)
        log_f.write(m + "\n"); log_f.flush()

    t_start_global = time.time()
    log("=== BG-ENGINE-A-SINGLE-LAYER-ABLATION-24 ===")
    log(f"ts: {datetime.now(timezone.utc).isoformat()}")
    log(f"V4_SEEDS={V4_SEEDS}  N_TURNS={N_TURNS_ABL}  MAX_CELLS={MAX_CELLS}")
    log(f"N_LAYERS={N_LAYERS}  conditions=A0 + L0..L{N_LAYERS-1} = {1+N_LAYERS}")

    # ─── load B once, snapshot per-layer state_dicts, free B ──────────
    log("\n--- loading B (BG-LA pretrain), snapshotting layer state_dicts ---")
    t0 = time.time()
    model_B = _load_engine_ag(CKPT_BGLA, "la_350m")
    log(f"  B loaded: {time.time()-t0:.1f}s")
    t0 = time.time()
    B_layer_sds: List[Dict[str, torch.Tensor]] = []
    for li in range(model_B.cfg.n_layers):
        sd_li = {k: v.detach().clone() for k, v in model_B.layers[li].state_dict().items()}
        B_layer_sds.append(sd_li)
    log(f"  B layer state_dicts snapshotted: {time.time()-t0:.1f}s "
        f"(n_layers={len(B_layer_sds)})")
    del model_B
    gc.collect()
    log("  B model freed")

    # ─── load A once, snapshot full state_dict, free A ────────────────
    log("\n--- loading A (Phase 2 cotrain), snapshotting full state_dict ---")
    t0 = time.time()
    model_A = _load_engine_ag(CKPT_PHASE2, "phase2_cotrain")
    log(f"  A loaded: {time.time()-t0:.1f}s")
    A_cfg = model_A.cfg
    A_state_dict = {k: v.detach().clone() for k, v in model_A.state_dict().items()}
    log(f"  A state_dict snapshotted: {len(A_state_dict)} tensors")
    del model_A
    gc.collect()
    log("  A model freed (cfg + state_dict + B_layer_sds retained)")

    # Helper: rebuild A from snapshot
    def fresh_A_from_snapshot() -> EngineAGModel:
        m = EngineAGModel(A_cfg)
        m.load_state_dict(A_state_dict, strict=True)
        return m

    # ─── compute mirrors ONCE (cache) ─────────────────────────────────
    # Per §57 C3#1: mirrors use load_random_init(seed=s, preset='la_350m'),
    # never see A's swapped state. Mirror trajectories are identical across
    # all 25 conditions. Cache once, reuse for all V14 verdicts.
    mirror_cache_path = THIS_DIR / "mirror_cache.json"
    if mirror_cache_path.exists():
        log("\n--- mirror cache HIT, loading from disk ---")
        cached = json.loads(mirror_cache_path.read_text())
        mirrors = cached["mirrors"]
        log(f"  mirrors loaded: {len(mirrors)} seeds, "
            f"final_iit_un16={[m['final_iit_un16'] for m in mirrors]}")
    else:
        log("\n--- computing mirror cache (3 seeds × 200 turns) ---")
        mirrors = []
        for s in V4_SEEDS:
            t0 = time.time()
            rm = load_random_init(seed=s, preset="la_350m")
            mr = _run_one_trajectory(rm, f"mirror_s{s}", seed=s,
                                     n_turns=N_TURNS_ABL, snap_every=SNAPSHOT_EVERY,
                                     max_cells=MAX_CELLS)
            mirrors.append(mr)
            del rm; gc.collect()
            log(f"  mirror seed={s}: Φ_un16={mr['final_iit_un16']:.2f} "
                f"cells={mr['final_n_cells']}  ({time.time()-t0:.1f}s)")
        mirror_cache_path.write_text(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "v4_seeds": V4_SEEDS,
            "n_turns": N_TURNS_ABL,
            "max_cells": MAX_CELLS,
            "snapshot_every": SNAPSHOT_EVERY,
            "mirrors": mirrors,
        }, indent=2))
        log(f"  mirror_cache.json written")

    # ─── A0 baseline ──────────────────────────────────────────────────
    log(f"\n--- ablation V14 (n_turns={N_TURNS_ABL}, seeds={V4_SEEDS}) ---")
    abl_results: Dict[str, Any] = {}

    # Time per condition tracker for early-abort estimation
    def estimate_remaining(idx: int, t_per_cond: float) -> float:
        return (N_LAYERS - idx) * t_per_cond

    t0 = time.time()
    log("  [A0_baseline] running trained trajectory (no swap)...")
    M_A0 = fresh_A_from_snapshot()
    tr_A0 = _run_one_trajectory(M_A0, "A0_baseline_trained", seed=42,
                                 n_turns=N_TURNS_ABL, snap_every=SNAPSHOT_EVERY,
                                 max_cells=MAX_CELLS)
    del M_A0; gc.collect()
    abl_results["A0_baseline"] = _aggregate_v14("A0_baseline", tr_A0, mirrors)
    abl_results["A0_baseline"]["swap_diag"] = {
        "layer_idx": None, "n_tensors_swapped": 0, "n_params_swapped": 0,
    }
    t_elapsed_A0 = time.time() - t0
    log(f"  A0_baseline: verdict={abl_results['A0_baseline']['verdict']} "
        f"({t_elapsed_A0:.1f}s)")
    log(f"    trained Φ_un16={abl_results['A0_baseline']['trained_iit_un16']:.2f}"
        f"  mirror_mean={abl_results['A0_baseline']['mirror_iit_un16_mean']:.2f}"
        f"  beats_un={abl_results['A0_baseline']['n_beats_iit_un16']}/"
        f"{abl_results['A0_baseline']['n_seeds']}"
        f"  cells={abl_results['A0_baseline']['trained_n_cells']}")

    # ─── L0..L23: per-layer single swap ───────────────────────────────
    t_per_cond_avg = t_elapsed_A0  # initialize estimate
    f_single_3_aborted = False

    for li in range(N_LAYERS):
        cond_label = f"L{li}"
        # Time check before each condition
        t_total_so_far = time.time() - t_start_global
        t_remaining_est = estimate_remaining(li, t_per_cond_avg)
        if t_total_so_far + t_remaining_est > 5 * 3600:
            log(f"\n  *** F-SINGLE-3 ABORT *** projected total = "
                f"{(t_total_so_far + t_remaining_est)/3600:.2f}h > 5h. "
                f"Stopping at L{li}, partial result emit.")
            f_single_3_aborted = True
            break

        t0 = time.time()
        log(f"\n  [{cond_label}] swapping layer {li} ← B")
        M = fresh_A_from_snapshot()
        diag = swap_one_layer_(M, B_layer_sds, li)
        log(f"    swapped {diag['n_tensors_swapped']} tensors "
            f"({diag['n_params_swapped']:,} params)")
        tr = _run_one_trajectory(M, f"{cond_label}_trained", seed=42,
                                  n_turns=N_TURNS_ABL, snap_every=SNAPSHOT_EVERY,
                                  max_cells=MAX_CELLS)
        del M; gc.collect()
        res = _aggregate_v14(cond_label, tr, mirrors)
        res["swap_diag"] = diag
        abl_results[cond_label] = res
        t_cond = time.time() - t0
        # Update running average
        n_done = li + 1
        t_per_cond_avg = (t_per_cond_avg * n_done + t_cond) / (n_done + 1)
        log(f"  {cond_label}: verdict={res['verdict']} ({t_cond:.1f}s; "
            f"avg_per_cond={t_per_cond_avg:.1f}s)")
        log(f"    trained Φ_un16={res['trained_iit_un16']:.2f}"
            f"  mirror_mean={res['mirror_iit_un16_mean']:.2f}"
            f"  beats_un={res['n_beats_iit_un16']}/{res['n_seeds']}"
            f"  beats_proxy={res['n_beats_proxy_phi']}/{res['n_seeds']}"
            f"  cells={res['trained_n_cells']}")

        # Incremental persistence — every 4 layers, flush partial
        if (li + 1) % 4 == 0 or li == N_LAYERS - 1:
            (THIS_DIR / "ablation_per_layer.json").write_text(
                json.dumps(abl_results, indent=2))
            log(f"  [persist] ablation_per_layer.json updated (n_conds={len(abl_results)})")

    # Final persist
    (THIS_DIR / "ablation_per_layer.json").write_text(json.dumps(abl_results, indent=2))

    # ─── verdict logic ────────────────────────────────────────────────
    log("\n--- verdict logic ---")
    base_v = abl_results["A0_baseline"]["verdict"]
    base_phi = abl_results["A0_baseline"]["trained_iit_un16"]
    base_mirror = abl_results["A0_baseline"]["mirror_iit_un16_mean"]
    base_sep = base_phi - base_mirror

    # Per-layer disposition
    layer_dispo: Dict[str, Any] = {}
    flips: List[int] = []
    for li in range(N_LAYERS):
        cond_label = f"L{li}"
        if cond_label not in abl_results:
            continue  # F-SINGLE-3 partial
        v = abl_results[cond_label]
        flipped = (v["verdict"] != base_v)
        sep = v["trained_iit_un16"] - v["mirror_iit_un16_mean"]
        sep_change = sep - base_sep
        layer_dispo[cond_label] = {
            "layer_idx": li,
            "verdict": v["verdict"],
            "flipped_from_baseline": flipped,
            "trained_iit_un16": v["trained_iit_un16"],
            "trained_proxy_phi": v["trained_proxy_phi"],
            "mirror_iit_un16_mean": v["mirror_iit_un16_mean"],
            "separation": sep,
            "separation_change_vs_baseline": sep_change,
            "trained_n_cells": v["trained_n_cells"],
            "n_beats_iit_un16": v["n_beats_iit_un16"],
            "n_beats_proxy_phi": v["n_beats_proxy_phi"],
        }
        if flipped:
            flips.append(li)
        log(f"  L{li:>2}: verdict={v['verdict']:<14} flipped={str(flipped):<5}"
            f"  Φ_sep={sep:+.2f} (Δ={sep_change:+.2f})  cells={v['trained_n_cells']}")

    # Layer dominance ranking — by absolute separation drop magnitude
    ranking = sorted(
        [(lk, layer_dispo[lk]["separation_change_vs_baseline"])
         for lk in layer_dispo],
        key=lambda x: x[1],
    )
    rank_records = []
    for rank_idx, (lk, sep_change) in enumerate(ranking, 1):
        d = layer_dispo[lk]
        rank_records.append({
            "rank": rank_idx,
            "layer": lk,
            "layer_idx": d["layer_idx"],
            "separation_change_vs_baseline": sep_change,
            "trained_iit_un16": d["trained_iit_un16"],
            "trained_n_cells": d["trained_n_cells"],
            "verdict": d["verdict"],
            "flipped": d["flipped_from_baseline"],
        })
    (THIS_DIR / "layer_dominance_ranking.json").write_text(
        json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "baseline_separation": base_sep,
            "ranking_by_separation_change": rank_records,
        }, indent=2)
    )

    # Cluster analysis: early (0-7), middle (8-15), late (16-23)
    cluster_counts = {"early": 0, "middle": 0, "late": 0}
    cluster_dispo = {"early": [], "middle": [], "late": []}
    for li_int in flips:
        if li_int <= 7:
            cluster_counts["early"] += 1
            cluster_dispo["early"].append(li_int)
        elif li_int <= 15:
            cluster_counts["middle"] += 1
            cluster_dispo["middle"].append(li_int)
        else:
            cluster_counts["late"] += 1
            cluster_dispo["late"].append(li_int)

    n_flipped = len(flips)
    if n_flipped == 0:
        verdict_label = "F-SINGLE-1 PASSED — no single-layer swap flipped V14 (distributed/cumulative)"
        star_credit = "★★★★ slab-level finding preserved; single-layer locus FALSIFIED"
        single_layer_localized = False
    elif 1 <= n_flipped <= 3:
        verdict_label = (f"F-SINGLE-2 PASSED — specific layer locus localized "
                         f"(n_flipped={n_flipped}, layers={flips})")
        star_credit = "★★★★★ specific layer locus localized"
        single_layer_localized = True
    elif 4 <= n_flipped <= 12:
        verdict_label = (f"distributed-cluster (n_flipped={n_flipped}, "
                         f"clusters: early={cluster_counts['early']}, "
                         f"middle={cluster_counts['middle']}, "
                         f"late={cluster_counts['late']})")
        star_credit = "★★★★ partial — cluster identifiable but not single-locus"
        single_layer_localized = False
    else:
        verdict_label = (f"uniformly-distributed (n_flipped={n_flipped}/{len(layer_dispo)}); "
                         f"§57 slab finding confirmed at finer resolution")
        star_credit = "★★★★ confirmation — slab finding holds"
        single_layer_localized = False

    elapsed_total = time.time() - t_start_global

    log(f"\n  n_flipped = {n_flipped} layers (out of {len(layer_dispo)} probed)")
    log(f"  cluster: early={cluster_counts['early']} middle={cluster_counts['middle']} late={cluster_counts['late']}")
    log(f"  flipped layers = {flips}")
    log(f"  F-SINGLE-1 (0 flip — distributed):     {'PASSED' if n_flipped == 0 else 'FALSIFIED'}")
    log(f"  F-SINGLE-2 (1-3 flip — specific locus): {'PASSED' if 1 <= n_flipped <= 3 else 'FALSIFIED'}")
    log(f"  F-SINGLE-3 (runtime > 5h):              {'TRIGGERED' if f_single_3_aborted else 'OK'}  "
        f"elapsed={elapsed_total:.1f}s")
    log(f"\n  verdict_label = {verdict_label}")
    log(f"  star_credit  = {star_credit}")
    log(f"\n  Top-5 dominance ranking (largest negative Δ_sep first):")
    for r in rank_records[:5]:
        log(f"    #{r['rank']} {r['layer']:<5} Δ_sep={r['separation_change_vs_baseline']:+.2f} "
            f"Φ={r['trained_iit_un16']:.1f} cells={r['trained_n_cells']} flipped={r['flipped']}")

    # ─── summary.json ─────────────────────────────────────────────────
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
            "n_layers": N_LAYERS,
        },
        "baseline": {
            "verdict": base_v,
            "trained_iit_un16": base_phi,
            "mirror_iit_un16_mean": base_mirror,
            "separation": base_sep,
        },
        "layer_dispo": layer_dispo,
        "n_flipped": n_flipped,
        "n_layers_probed": len(layer_dispo),
        "flipped_layer_idxs": flips,
        "cluster_counts": cluster_counts,
        "cluster_dispo": cluster_dispo,
        "falsifiers": {
            "F_SINGLE_1_no_flip_distributed":  {"triggered": n_flipped == 0},
            "F_SINGLE_2_specific_locus":       {"triggered": 1 <= n_flipped <= 3},
            "F_SINGLE_3_runtime_overflow":     {"triggered": f_single_3_aborted,
                                                 "elapsed_sec": elapsed_total},
        },
        "verdict_label": verdict_label,
        "star_credit": star_credit,
        "single_layer_localized": single_layer_localized,
        "top5_dominance": rank_records[:5],
    }
    (THIS_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    # ─── verdict.md ───────────────────────────────────────────────────
    _write_verdict_md(THIS_DIR / "verdict.md", summary, abl_results, layer_dispo,
                       rank_records, cluster_counts, cluster_dispo)

    log_f.close()
    return summary


def _write_verdict_md(path: Path, summary: dict, abl_results: dict,
                       layer_dispo: dict, rank_records: list,
                       cluster_counts: dict, cluster_dispo: dict):
    lines: List[str] = []
    lines.append("# BG-ENGINE-A-SINGLE-LAYER-ABLATION-24 — verdict\n")
    lines.append(f"**FINAL_VERDICT**: `{summary['verdict_label']}`\n")
    lines.append(f"**Star credit**: {summary['star_credit']}\n")
    lines.append(f"**Single-layer locus localized**: {summary['single_layer_localized']}\n")
    lines.append(f"**n_flipped**: {summary['n_flipped']} / {summary['n_layers_probed']} probed\n")
    lines.append(f"**Elapsed**: {summary['elapsed_sec_total']:.1f}s ({summary['elapsed_sec_total']/60:.1f}min)\n")

    lines.append("## §57 → §58 lineage\n")
    lines.append("§57 BG-ENGINE-A-LAYER-SLAB-SWAP: 3/3 8-layer slab swaps flipped V14. "
                 "A1 (early) uniquely dominant attractor (n=44, Φ≈1037); A2/A3 (middle, late) "
                 "bit-identical shared attractor (n=43, Φ≈1343). 8-layer resolution insufficient "
                 "to differentiate middle vs late.\n")
    lines.append("§58 (this BG): single-layer ablation × 24 → "
                 f"{summary['n_flipped']} layer(s) flip individually. ")
    if summary["single_layer_localized"]:
        lines.append("**Specific layer locus localized** — ★★★★★ unlocked.\n")
    else:
        if summary["n_flipped"] == 0:
            lines.append("§57 slab effect was cumulative; no single-layer swap suffices. "
                         "Single-layer locus FALSIFIED, slab effect preserved at ★★★★.\n")
        elif 4 <= summary["n_flipped"] <= 12:
            lines.append("Distributed-cluster: multiple layers flip but cluster pattern visible.\n")
        else:
            lines.append("Uniformly distributed across most layers; §57 slab finding "
                         "confirmed at finer resolution.\n")

    lines.append("## Per-layer V14 verdict (24 layers + A0 baseline)\n")
    lines.append(f"`N_TURNS={summary['config']['n_turns']}`, "
                 f"`MAX_CELLS={summary['config']['max_cells']}`, "
                 f"seeds={summary['config']['v4_seeds']}\n")
    lines.append("| condition | layer | verdict | trained Φ_un16 | beats_un | beats_proxy | "
                 "trained_cells | Δ_separation_vs_base | flipped |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    # A0 row
    a0 = abl_results["A0_baseline"]
    lines.append(f"| A0_baseline | — | `{a0['verdict']}` | {a0['trained_iit_un16']:.2f} | "
                 f"{a0['n_beats_iit_un16']}/{a0['n_seeds']} | "
                 f"{a0['n_beats_proxy_phi']}/{a0['n_seeds']} | "
                 f"{a0['trained_n_cells']} | 0.00 (base) | — |")
    for li in range(summary["config"]["n_layers"]):
        lk = f"L{li}"
        if lk not in layer_dispo:
            lines.append(f"| {lk} | {li} | `(not run — F-SINGLE-3 abort)` | - | - | - | - | - | - |")
            continue
        d = layer_dispo[lk]
        v = abl_results[lk]
        lines.append(
            f"| {lk} | {li} | `{d['verdict']}` | {d['trained_iit_un16']:.2f} | "
            f"{d['n_beats_iit_un16']}/{v['n_seeds']} | "
            f"{d['n_beats_proxy_phi']}/{v['n_seeds']} | "
            f"{d['trained_n_cells']} | {d['separation_change_vs_baseline']:+.2f} | "
            f"{d['flipped_from_baseline']} |"
        )

    lines.append("\n## Layer dominance ranking (by largest negative Δ_separation)\n")
    lines.append("| rank | layer | layer_idx | Δ_separation_vs_base | Φ_un16 | n_cells | verdict | flipped |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in rank_records[:24]:
        lines.append(f"| #{r['rank']} | {r['layer']} | {r['layer_idx']} | "
                     f"{r['separation_change_vs_baseline']:+.2f} | "
                     f"{r['trained_iit_un16']:.2f} | {r['trained_n_cells']} | "
                     f"`{r['verdict']}` | {r['flipped']} |")

    lines.append("\n## Cluster analysis (early 0-7, middle 8-15, late 16-23)\n")
    lines.append("| cluster | n_layers | n_flipped | flipped layers |")
    lines.append("|---|---|---|---|")
    lines.append(f"| early (0-7) | 8 | {cluster_counts['early']} | {cluster_dispo['early']} |")
    lines.append(f"| middle (8-15) | 8 | {cluster_counts['middle']} | {cluster_dispo['middle']} |")
    lines.append(f"| late (16-23) | 8 | {cluster_counts['late']} | {cluster_dispo['late']} |")
    lines.append("\n**§57 slab parallel**: §57 found A1=early uniquely dominant attractor; A2/A3 shared. "
                 f"§58 cluster: early={cluster_counts['early']}, middle={cluster_counts['middle']}, "
                 f"late={cluster_counts['late']}. ")
    if cluster_counts["early"] > max(cluster_counts["middle"], cluster_counts["late"]):
        lines.append("Early-cluster dominance **confirmed at finer resolution**.\n")
    elif cluster_counts["early"] == cluster_counts["middle"] == cluster_counts["late"]:
        lines.append("Uniform distribution — §57 A1 dominance was an attractor-collapse artefact, "
                     "not a per-layer effect.\n")
    else:
        lines.append("Cluster pattern differs from §57 slab; per-layer effect not aligned with "
                     "cumulative 8-layer attractor selection.\n")

    lines.append("\n## ★★★★★ unlock evaluation\n")
    if summary["single_layer_localized"]:
        flips = summary["flipped_layer_idxs"]
        lines.append(f"**★★★★★ UNLOCKED** — exactly {len(flips)} layer(s) flip V14 individually: "
                     f"layers {flips}. Engine_a body's V14 PASS lever has a sparse, locus-specific "
                     "weight signature: cotrain modifies these specific layers' hidden_mean dynamics, "
                     "and swapping any one of them back to BG-LA pretrain weights collapses V14.\n")
    else:
        lines.append(f"**★★★★★ NOT unlocked** — n_flipped={summary['n_flipped']} layers. ")
        if summary["n_flipped"] == 0:
            lines.append("F-SINGLE-1 PASSED: V14 lever is not single-layer-localizable; "
                         "the §57 slab effect was cumulative across multiple layers per slab. "
                         "★★★★ slab-level finding (PROVEN-AT-BODY-LOCUS) preserved.\n")
        else:
            lines.append("Multiple layers flip individually → distributed effect, "
                         "no single-locus lock-in possible at single-layer resolution. "
                         "★★★★ slab finding holds; ★★★★★ requires sparser signature.\n")

    lines.append("\n## Falsifiers\n")
    for fname, fblk in summary["falsifiers"].items():
        triggered = fblk["triggered"]
        extra = ""
        if "elapsed_sec" in fblk:
            extra = f" (elapsed={fblk['elapsed_sec']:.1f}s)"
        lines.append(f"- **{fname}**: {'TRIGGERED' if triggered else 'not triggered'}{extra}")

    lines.append("\n## Honest C3 (≥7)\n")
    lines.append("1. **Mirror cache reuse.** Per §57 C3#1, mirrors use `load_random_init(seed=s, "
                 "preset='la_350m')` and never see A's swapped state. Mirror trajectories are "
                 "deterministic functions of seed alone, identical across all 25 conditions. "
                 "We compute them once (3 seeds × 200 turns) and reuse — verdict semantics "
                 "preserved, runtime cut ~75% (100 runs → 28 effective runs). Direct check: "
                 "§57 mirror_iit_un16_mean=1615.49 across A0/A1/A2/A3 (identical).")
    lines.append("2. **Single-seed trained run per condition.** Each L{i} condition uses ONE "
                 "trained-model seed (42), as in §57. Mirror multi-seed (3) provides the V14 PASS "
                 "denominator. A multi-seed trained per condition (e.g., 3 seeds × 25 conditions = 75 "
                 "trained runs) would tighten the verdict polarity for borderline `V14_PARTIAL` "
                 "cases; deferred per 5h envelope.")
    lines.append("3. **Single-layer swap is not a true 'lesion'.** Swapping layer i from A→B "
                 "replaces 11.08M params at one position; the surrounding 23 layers still carry "
                 "A's cotrain weights. The hidden_mean trajectory mutation is local at layer i but "
                 "the downstream effect propagates through 23 cotrain-weighted layers. So a "
                 "'flip' at L_i means '1 layer swap is sufficient to disrupt V14', not 'V14 lives "
                 "only in L_i'.")
    lines.append("4. **B is a trained pretrain ckpt, not random.** As §57 C3#4: this measures "
                 "cotrain-specific delta at layer i, not absolute layer-i functional contribution. "
                 "BG-LA pretrain at layer i still encodes substantial structure (cos_AB ≈ 0.6-0.8 "
                 "on engine_g modules per §50 F1); the swap tests cotrain-induced specialization.")
    lines.append("5. **Engine G modules untouched.** All 25 conditions retain A's cotrain "
                 "`cell_pool_init`, `c_to_h`, `h_to_c`. Per §50 these are NOT the lever (F2 "
                 "falsified). The MitosisV5Engine sees only the engine_a forward path's "
                 "`hidden_mean` trajectory at the final layer (post-norm_f). The lever measured "
                 "here is the per-layer transformer-body contribution to hidden_mean.")
    lines.append("6. **A2/A3 §57 attractor degeneracy may recur at single-layer.** §57 found "
                 "middle-and-late perturbations collapse to a shared mitosis attractor (n=43, "
                 "Φ≈1343). At single-layer resolution, multiple L_i conditions may collapse to the "
                 "same attractor → bit-identical trajectories despite different swapped weights. "
                 "This is verified post-hoc by checking for repeated Φ_un16 values in the table; "
                 "any such cluster indicates attractor-collapse, NOT zero per-layer effect.")
    lines.append("7. **200-turn trajectory is the §57 length.** Φ values directly comparable to "
                 "§57 baseline (2412.08). Verdict polarity tested at this run length only; longer "
                 "trajectories may resolve V14_PARTIAL cases but were budgeted out.")
    lines.append("8. **Embedding (tok_emb), norm_f, lm_head all stay at A's values.** Swap is "
                 "strictly intra-block at layer i. Projections in/out of the layer stack are A's. "
                 "Per-layer effect isolated from embedding-projection contributions.")
    lines.append("9. **raw#15 honored** — both ckpts loaded read-only via `_load_engine_ag`; "
                 "`fresh_A_from_snapshot()` builds a fresh model and copies state_dict; "
                 "`swap_one_layer_` mutates the clone in-place. No file mutation.")
    lines.append("10. **Sample size = 3 mirror seeds, not 5.** Mission specified 3-seed budget. "
                 "Strict V14 used 5 seeds — this study trades seed coverage for layer "
                 "coverage (24 layers × ~1.4min vs 5 seeds × 24 layers × ~1.4min = 168min vs 33min). "
                 "Verdict polarity at 3 seeds is robust if separation magnitude is large; "
                 "ambiguous cases flagged as V14_PARTIAL.")
    lines.append("11. **Runtime monitoring with mid-run F-SINGLE-3 abort.** If projected total "
                 "runtime exceeds 5h, the BG aborts and emits partial result. The running-average "
                 "per-condition time updates each iteration; estimate uses n_remaining × "
                 "avg_per_cond. Ablation persists every 4 layers for crash recovery.")
    lines.append("12. **Single-layer flips comparison vs §57 slab attractors.** §57 A1 attractor: "
                 "n=44, Φ≈1037. §57 A2/A3 attractor: n=43, Φ≈1343. If §58 single-layer flips "
                 "land in the same (n, Φ) clusters, this confirms slab-flips were dominated "
                 "by 1-2 specific layers per slab. If §58 flips show novel attractors, the "
                 "single-layer perturbation regime is qualitatively different from cumulative "
                 "8-layer slab perturbation.")
    path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
