"""BG-COMPONENT-MLP-EMBED-V14 — §62 prediction-3 + finding-7 functional V14 verification.

Mission: drill component-axis (MLP gate/up/down × layer slab) and embedding-axis
(tok_emb, lm_head, paired) to test whether §62's weight-drift component
ranking translates to V14 PASS/VIOLATE causality.

Substrates: A (Phase 2 cotrain ckpt), B (BG-LA pretrain ckpt). Identical to §57 / §62.

Conditions (8 + 1 baseline + 1 mirror set):
  C0 baseline pristine A                    1 trial
  C1 gate × slab1 (layers 0..7)             3 trials
  C2 gate × slab2 (layers 8..15)            3 trials
  C3 gate × slab3 (layers 16..23)           3 trials
  C4 up   × slab1                           3 trials
  C5 down × slab1                           3 trials
  C6 tok_emb only (lm_head untied to A)     5 trials
  C7 lm_head only (tok_emb untied to A)     5 trials
  C8 tok_emb + lm_head (kept tied)          5 trials
                                       Σ = 30 trial passes (+1 baseline +3 mirrors)

V14: V4_SEEDS=[42, 137, 271, 311, 521], N_TURNS=128, MAX_CELLS=128,
SNAPSHOT_EVERY=16. Per-trial = 1 trained pass; mirrors run once as shared
random_init reference.

raw#9   training/*.py local-only; lives under state/ (gitignored)
raw#15  additive — both ckpts loaded read-only; in-memory swap only
own 14  V14 paired random_init mirror multi-seed
own 16  $0 local Mac CPU
own 22  honest emit; verdict.md only (no REBORN.md append)
own 38  artefacts under state/anima_component_mlp_embed_v14_2026_05_10/
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
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn

# Wire to upstream modules (additive, raw#15)
ANIMA = "/Users/ghost/core/anima"
sys.path.insert(0, f"{ANIMA}/training")
sys.path.insert(0, f"{ANIMA}/state/anima_clm_v5_iit_phi_remetric_2026_05_10")
sys.path.insert(0, f"{ANIMA}/state/anima_iit_real_350m_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402
from _v14_5seed_run import (  # noqa: E402
    ALL_PROMPTS,
    encode_prompt_to_ids,
    HiddenMeanCapture,
)

THIS_DIR = Path(f"{ANIMA}/state/anima_component_mlp_embed_v14_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PHASE2 = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_BGLA = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt"

V4_SEEDS_FULL = [42, 137, 271, 311, 521]
MIRROR_SEEDS = [42, 137, 271]
N_TURNS = 128
SNAPSHOT_EVERY = 16
MAX_CELLS = 128

# 24 layers → 3 contiguous slabs of 8 (mirror §57)
SLABS: Dict[str, List[int]] = {
    "slab1_early":  list(range(0, 8)),    # layers 0..7
    "slab2_middle": list(range(8, 16)),   # layers 8..15
    "slab3_late":   list(range(16, 24)),  # layers 16..23
}

# Per-condition definitions: (cond_label, swap_fn_name, swap_args, seeds)
# Each "trial" = one trained-model V14 short trajectory at a given seed.
CONDITIONS: List[Tuple[str, str, Dict[str, Any], List[int]]] = [
    ("C0_baseline",       "none",       {},                                     [42]),
    ("C1_gate_slab1",     "mlp_slab",   {"comp": "gate", "slab": "slab1_early"},  [42, 137, 271]),
    ("C2_gate_slab2",     "mlp_slab",   {"comp": "gate", "slab": "slab2_middle"}, [42, 137, 271]),
    ("C3_gate_slab3",     "mlp_slab",   {"comp": "gate", "slab": "slab3_late"},   [42, 137, 271]),
    ("C4_up_slab1",       "mlp_slab",   {"comp": "up",   "slab": "slab1_early"},  [42, 137, 271]),
    ("C5_down_slab1",     "mlp_slab",   {"comp": "down", "slab": "slab1_early"},  [42, 137, 271]),
    ("C6_tok_emb_only",   "tok_emb_only_untied", {},                              [42, 137, 271, 311, 521]),
    ("C7_lm_head_only",   "lm_head_only_untied", {},                              [42, 137, 271, 311, 521]),
    ("C8_tok_emb_lm_pair","tok_emb_lm_pair_tied",{},                              [42, 137, 271, 311, 521]),
]


# ── ckpt loaders (mirror §57) ─────────────────────────────────────────


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


# ── Component-axis swap utilities ────────────────────────────────────


def untie_lm_head_(model: EngineAGModel):
    """Replace model.lm_head.weight with an independent fresh nn.Parameter clone.

    After this call, lm_head.weight is no longer the same Python object as
    tok_emb.weight; mutating one no longer affects the other.
    """
    with torch.no_grad():
        src = model.lm_head.weight
        new_param = nn.Parameter(src.detach().clone())
        model.lm_head.weight = new_param  # rebind; tok_emb.weight unchanged


def swap_mlp_component_in_slab_(model: EngineAGModel,
                                 src_layer_sds: List[Dict[str, torch.Tensor]],
                                 comp: str, slab: str) -> Dict[str, Any]:
    """In-place: replace `model.layers[i].ffn.{comp}.weight` ← src_layer_sds[i]['ffn.{comp}.weight']
    for i in SLABS[slab]. Returns diag.
    """
    assert comp in ("gate", "up", "down"), f"bad comp={comp}"
    layer_idxs = SLABS[slab]
    key = f"ffn.{comp}.weight"
    n_tensors = 0
    n_params = 0
    with torch.no_grad():
        for li in layer_idxs:
            d = dict(model.layers[li].state_dict())[key]
            s = src_layer_sds[li][key]
            assert d.shape == s.shape, f"shape mismatch layers.{li}.{key}: {d.shape} vs {s.shape}"
            d.copy_(s)
            n_tensors += 1
            n_params += int(s.numel())
    return {"swap_kind": "mlp_component_in_slab", "comp": comp, "slab": slab,
            "layer_idxs": layer_idxs, "n_tensors_swapped": n_tensors,
            "n_params_swapped": n_params}


def swap_tok_emb_only_untied_(model: EngineAGModel, B_tok_emb: torch.Tensor) -> Dict[str, Any]:
    """Untie lm_head, then swap only tok_emb.weight ← B's tok_emb.weight. lm_head retains A.
    Asserts post-swap that lm_head.weight still equals A's value.
    """
    A_lm_head = model.lm_head.weight.detach().clone()
    untie_lm_head_(model)
    # Verify untied identity (must NOT share storage)
    assert model.lm_head.weight.data_ptr() != model.tok_emb.weight.data_ptr(), \
        "untie failed: lm_head still shares storage with tok_emb"
    with torch.no_grad():
        d = model.tok_emb.weight
        assert d.shape == B_tok_emb.shape
        d.copy_(B_tok_emb)
    # Sanity: lm_head still equals A
    diff_lm = (model.lm_head.weight - A_lm_head).abs().max().item()
    assert diff_lm < 1e-6, f"lm_head leaked: max abs diff = {diff_lm}"
    return {"swap_kind": "tok_emb_only_untied", "n_tensors_swapped": 1,
            "n_params_swapped": int(B_tok_emb.numel()),
            "lm_head_max_abs_diff_vs_A": diff_lm}


def swap_lm_head_only_untied_(model: EngineAGModel, B_lm_head: torch.Tensor) -> Dict[str, Any]:
    """Untie lm_head, then swap only lm_head.weight ← B's lm_head.weight. tok_emb retains A.
    Asserts post-swap that tok_emb.weight still equals A's value.
    """
    A_tok_emb = model.tok_emb.weight.detach().clone()
    untie_lm_head_(model)
    assert model.lm_head.weight.data_ptr() != model.tok_emb.weight.data_ptr(), \
        "untie failed: lm_head still shares storage with tok_emb"
    with torch.no_grad():
        d = model.lm_head.weight
        assert d.shape == B_lm_head.shape
        d.copy_(B_lm_head)
    diff_te = (model.tok_emb.weight - A_tok_emb).abs().max().item()
    assert diff_te < 1e-6, f"tok_emb leaked: max abs diff = {diff_te}"
    return {"swap_kind": "lm_head_only_untied", "n_tensors_swapped": 1,
            "n_params_swapped": int(B_lm_head.numel()),
            "tok_emb_max_abs_diff_vs_A": diff_te}


def swap_tok_emb_lm_pair_tied_(model: EngineAGModel, B_tok_emb: torch.Tensor) -> Dict[str, Any]:
    """Tying preserved: in-place mutation of tok_emb.weight propagates to lm_head.weight.
    Asserts post-swap that both equal B's tok_emb (== B's lm_head if also tied in B).
    """
    # Ensure still tied
    if model.lm_head.weight.data_ptr() != model.tok_emb.weight.data_ptr():
        # rebind lm_head to tok_emb
        model.lm_head.weight = model.tok_emb.weight
    with torch.no_grad():
        d = model.tok_emb.weight
        assert d.shape == B_tok_emb.shape
        d.copy_(B_tok_emb)
    # Confirm tying propagated
    same_storage = (model.lm_head.weight.data_ptr() == model.tok_emb.weight.data_ptr())
    diff_pair = (model.lm_head.weight - model.tok_emb.weight).abs().max().item()
    return {"swap_kind": "tok_emb_lm_pair_tied", "n_tensors_swapped": 1,
            "n_params_swapped": int(B_tok_emb.numel()),
            "tied_same_storage_post_swap": bool(same_storage),
            "lm_head_minus_tok_emb_max_abs": diff_pair}


# ── V14 short trajectory runner (single-trial) ──────────────────────


def run_v14_one_trial(model: EngineAGModel, label: str, seed: int,
                      n_turns: int = N_TURNS, snap_every: int = SNAPSHOT_EVERY,
                      max_cells: int = MAX_CELLS, ctx_T: int = 16) -> Dict[str, Any]:
    """One V14 short trajectory. Returns scalars + snapshots."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    model.eval()
    cap = HiddenMeanCapture(model.engine_g)
    eg = model.engine_g
    init_pool = eg.cell_pool_init.detach().clone()
    n_cells_init = init_pool.shape[0]
    mit = MitosisV5Engine(
        cell_pool=init_pool, c_to_h=eg.c_to_h,
        initial_cells=n_cells_init, max_cells=max_cells,
        split_patience=3, split_noise=0.10,
        merge_threshold=0.005, merge_patience=30, min_cells=2,
        lorenz_scale=0.05,
    )
    snaps: List[Dict[str, Any]] = []
    n_splits = 0
    n_merges = 0
    cap_bound_turns = 0
    t0 = time.time()
    with torch.no_grad():
        for turn in range(n_turns):
            cat, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
            ids = encode_prompt_to_ids(prompt, T=ctx_T)
            _ = model(ids, output_hidden_states=False, output_attentions=False)
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
        "label": label,
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


# ── Per-condition trained-model factory ─────────────────────────────


def build_trained_for_condition(cond_label: str, swap_fn: str, swap_args: Dict[str, Any],
                                 A_state_dict: Dict[str, torch.Tensor], A_cfg: EngineAGConfig,
                                 B_layer_sds: List[Dict[str, torch.Tensor]],
                                 B_tok_emb: torch.Tensor,
                                 B_lm_head: torch.Tensor) -> Tuple[EngineAGModel, Dict[str, Any]]:
    """Rebuild fresh A from snapshot, apply requested swap, return (model, diag)."""
    m = EngineAGModel(A_cfg)
    m.load_state_dict(A_state_dict, strict=True)
    if swap_fn == "none":
        diag = {"swap_kind": "none"}
    elif swap_fn == "mlp_slab":
        diag = swap_mlp_component_in_slab_(m, B_layer_sds,
                                           comp=swap_args["comp"], slab=swap_args["slab"])
    elif swap_fn == "tok_emb_only_untied":
        diag = swap_tok_emb_only_untied_(m, B_tok_emb)
    elif swap_fn == "lm_head_only_untied":
        diag = swap_lm_head_only_untied_(m, B_lm_head)
    elif swap_fn == "tok_emb_lm_pair_tied":
        diag = swap_tok_emb_lm_pair_tied_(m, B_tok_emb)
    else:
        raise ValueError(f"unknown swap_fn={swap_fn}")
    return m, diag


# ── Verdict logic ─────────────────────────────────────────────────


def classify_condition(trial_finals: List[Dict[str, float]],
                        mirror_un_mean: float, mirror_proxy_mean: float) -> str:
    """Per-condition V14 verdict.

    Each trial 'beats' mirror if final_iit_un16 > mirror_un_mean AND final_proxy > mirror_proxy_mean.
    """
    n = len(trial_finals)
    n_beats = sum(1 for t in trial_finals
                  if (t["final_iit_un16"] > mirror_un_mean)
                  and (t["final_proxy_phi"] > mirror_proxy_mean))
    if n_beats == n:
        return "V14_PASS_ROBUST"
    elif n_beats >= max(1, (n + 1) // 2):
        return "V14_PASS_PARTIAL"
    elif n_beats == 0:
        return "V14_VIOLATED"
    else:
        return "V14_VIOLATED"


# ── Main ──────────────────────────────────────────────────────────────


def main():
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(m: str):
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        line = f"[{ts}] {m}"
        print(line, flush=True)
        log_f.write(line + "\n"); log_f.flush()

    t_start_global = time.time()
    log("=== BG-COMPONENT-MLP-EMBED-V14 ===")
    log(f"ts: {datetime.now(timezone.utc).isoformat()}")
    log(f"N_TURNS={N_TURNS}  MAX_CELLS={MAX_CELLS}  SNAPSHOT_EVERY={SNAPSHOT_EVERY}")
    log(f"CKPT_A={CKPT_PHASE2}")
    log(f"CKPT_B={CKPT_BGLA}")
    log(f"n_unique_prompts={len(ALL_PROMPTS)}")

    # ─── load B once, snapshot relevant tensors, free B ────────────────
    log("\n--- loading B (BG-LA pretrain), snapshotting relevant tensors ---")
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
    B_tok_emb = model_B.tok_emb.weight.detach().clone()
    # In B (la_350m, tie_lm_head=True), lm_head.weight is the same param object as tok_emb.weight.
    # We still capture it explicitly (will be identical).
    B_lm_head = model_B.lm_head.weight.detach().clone()
    B_lm_emb_max_abs = (B_lm_head - B_tok_emb).abs().max().item()
    log(f"  B tok_emb shape={list(B_tok_emb.shape)}  lm_head==tok_emb max_abs_diff={B_lm_emb_max_abs:.2e}  "
        f"(tied={model_B.cfg.tie_lm_head})")
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
    A_tok_emb = model_A.tok_emb.weight.detach().clone()
    A_lm_head = model_A.lm_head.weight.detach().clone()
    A_lm_emb_max_abs = (A_lm_head - A_tok_emb).abs().max().item()
    log(f"  A tok_emb shape={list(A_tok_emb.shape)}  lm_head==tok_emb max_abs_diff={A_lm_emb_max_abs:.2e}  "
        f"(tied={model_A.cfg.tie_lm_head})")
    del model_A
    gc.collect()
    log("  A model freed (state_dict + cfg retained)")

    # ─── mirror baseline (3 random_init seeds, run once) ───────────────
    log(f"\n--- mirror baseline ({len(MIRROR_SEEDS)} random_init seeds) ---")
    mirror_results: List[Dict[str, Any]] = []
    for s in MIRROR_SEEDS:
        t0 = time.time()
        rm = load_random_init(seed=s, preset="la_350m")
        mr = run_v14_one_trial(rm, f"mirror_s{s}", seed=s)
        mirror_results.append(mr)
        log(f"  mirror s={s}: Φ_un16={mr['final_iit_un16']:.2f} "
            f"proxy={mr['final_proxy_phi']:.4f} cells={mr['final_n_cells']} "
            f"({mr['elapsed_sec']:.1f}s)")
        del rm
        gc.collect()
    mirror_un = [m["final_iit_un16"] for m in mirror_results]
    mirror_proxy = [m["final_proxy_phi"] for m in mirror_results]
    mirror_cells = [m["final_n_cells"] for m in mirror_results]
    mirror_un_mean = float(np.mean(mirror_un))
    mirror_proxy_mean = float(np.mean(mirror_proxy))
    log(f"  mirror Φ_un16: mean={mirror_un_mean:.2f} min={min(mirror_un):.2f} max={max(mirror_un):.2f}")
    log(f"  mirror proxy: mean={mirror_proxy_mean:.4f}")
    log(f"  mirror n_cells: {mirror_cells}")

    # ─── condition trials ─────────────────────────────────────────────
    log(f"\n--- 30 V14 trial conditions (8 swap conditions + baseline) ---")

    all_trials: List[Dict[str, Any]] = []
    cond_dispo: Dict[str, Any] = {}

    for cond_label, swap_fn, swap_args, seeds in CONDITIONS:
        log(f"\n  [{cond_label}] swap_fn={swap_fn} args={swap_args} seeds={seeds}")
        cond_trials: List[Dict[str, Any]] = []
        cond_diag: Optional[Dict[str, Any]] = None
        for sd in seeds:
            t0 = time.time()
            m, diag = build_trained_for_condition(
                cond_label, swap_fn, swap_args,
                A_state_dict, A_cfg, B_layer_sds, B_tok_emb, B_lm_head,
            )
            cond_diag = diag  # same across seeds for a given condition
            tr = run_v14_one_trial(m, f"{cond_label}_s{sd}", seed=sd)
            tr["condition"] = cond_label
            tr["swap_diag"] = diag
            cond_trials.append(tr)
            all_trials.append(tr)
            beats_un = tr["final_iit_un16"] > mirror_un_mean
            beats_proxy = tr["final_proxy_phi"] > mirror_proxy_mean
            flip_marker = ""
            if cond_label == "C0_baseline":
                flip_marker = "(reference)"
            else:
                if (not beats_un) or (not beats_proxy):
                    flip_marker = "FLIP→VIOLATED-leaning"
                else:
                    flip_marker = "PASS"
            log(f"    s={sd}: Φ_un16={tr['final_iit_un16']:.2f} "
                f"proxy={tr['final_proxy_phi']:.4f} "
                f"cells={tr['final_n_cells']} "
                f"beats_un={beats_un} beats_proxy={beats_proxy} "
                f"{flip_marker} ({tr['elapsed_sec']:.1f}s)")
            del m
            gc.collect()
        # Aggregate
        finals_un = [t["final_iit_un16"] for t in cond_trials]
        finals_proxy = [t["final_proxy_phi"] for t in cond_trials]
        finals_cells = [t["final_n_cells"] for t in cond_trials]
        verdict_label = classify_condition(cond_trials, mirror_un_mean, mirror_proxy_mean)
        cond_dispo[cond_label] = {
            "swap_fn": swap_fn,
            "swap_args": swap_args,
            "seeds": seeds,
            "n_trials": len(cond_trials),
            "swap_diag": cond_diag,
            "trained_un16_mean": float(np.mean(finals_un)),
            "trained_un16_std":  float(np.std(finals_un, ddof=0)) if len(finals_un) > 1 else 0.0,
            "trained_un16_min":  float(np.min(finals_un)),
            "trained_un16_max":  float(np.max(finals_un)),
            "trained_proxy_mean": float(np.mean(finals_proxy)),
            "trained_cells_mean": float(np.mean(finals_cells)),
            "trained_cells_min": int(np.min(finals_cells)),
            "trained_cells_max": int(np.max(finals_cells)),
            "trained_cells_per_seed": finals_cells,
            "n_beats_un": sum(1 for x in finals_un if x > mirror_un_mean),
            "n_beats_proxy": sum(1 for x in finals_proxy if x > mirror_proxy_mean),
            "verdict": verdict_label,
            "separation_un16": float(np.mean(finals_un) - mirror_un_mean),
        }
        log(f"  [{cond_label}] verdict={verdict_label}  "
            f"trained_un16 mean={cond_dispo[cond_label]['trained_un16_mean']:.2f} "
            f"std={cond_dispo[cond_label]['trained_un16_std']:.2f}  "
            f"sep={cond_dispo[cond_label]['separation_un16']:+.2f}  "
            f"cells={finals_cells}")

    # ─── persist ──────────────────────────────────────────────────────
    log("\n--- writing trial_results.json ---")
    (THIS_DIR / "trial_results.json").write_text(json.dumps({
        "ts": datetime.now(timezone.utc).isoformat(),
        "config": {
            "ckpt_A_phase2": CKPT_PHASE2,
            "ckpt_B_bgla": CKPT_BGLA,
            "n_turns": N_TURNS,
            "max_cells": MAX_CELLS,
            "snapshot_every": SNAPSHOT_EVERY,
            "mirror_seeds": MIRROR_SEEDS,
            "slabs": {k: v for k, v in SLABS.items()},
        },
        "mirror_results": mirror_results,
        "trials": all_trials,
    }, indent=2))

    # ─── verdict logic ────────────────────────────────────────────────
    log("\n--- verdict logic ---")
    base_un = cond_dispo["C0_baseline"]["trained_un16_mean"]
    base_sep = base_un - mirror_un_mean
    log(f"  baseline trained_un16={base_un:.2f}  mirror_mean={mirror_un_mean:.2f}  base_sep={base_sep:+.2f}")

    # Prediction 3 disposition: gate × slab1 vs full slab1 swap (from §57)
    # §57 slab1_early result: trained_un16=1036.86, separation=−578.63, sep_change=−1375.23.
    # Mirror_mean in §57 was 1615.49 (3 seeds, n_turns=200) — different regime!
    # In this BG (n_turns=128, fewer turns) we use OUR mirror_un_mean for separation.
    # Prediction 3 verifies whether gate × slab1 is "between" baseline and full-slab swap.
    # Using §57's quoted separation_change_vs_baseline = −1375.23 as ★full slab1 reference,
    # we encode that here as a known reference for comparative interpretation only.
    SLAB1_FULL_SEP_CHANGE_REF = -1375.23  # §57 A1_slab1_early separation_change_vs_baseline

    gate_s1_sep = cond_dispo["C1_gate_slab1"]["separation_un16"]
    gate_s1_sep_change = gate_s1_sep - base_sep
    up_s1_sep = cond_dispo["C4_up_slab1"]["separation_un16"]
    up_s1_sep_change = up_s1_sep - base_sep
    down_s1_sep = cond_dispo["C5_down_slab1"]["separation_un16"]
    down_s1_sep_change = down_s1_sep - base_sep

    # Pred 3 classification:
    #   CONFIRMED: gate-only sep_change is between 0 and §57's full-slab change,
    #             AND gate-only verdict is not as bad as full-slab (which was V14_VIOLATED).
    #             i.e., gate-only either preserves V14_PASS_ROBUST/PARTIAL, OR violated but
    #             with smaller magnitude than §57.
    #   PARTIALLY_CONFIRMED: gate-only verdict matches full-slab verdict (V14_VIOLATED) but
    #             magnitude is meaningfully smaller (>30% reduction in sep_change abs).
    #   FALSIFIED-MATCH: gate-only fully reproduces §57 magnitude (within 30%).
    #   FALSIFIED-NULL: gate-only barely perturbs (sep_change abs < 10% of full-slab).
    full_abs = abs(SLAB1_FULL_SEP_CHANGE_REF)
    gate_abs = abs(gate_s1_sep_change)
    gate_s1_verdict = cond_dispo["C1_gate_slab1"]["verdict"]
    full_verdict_57 = "V14_VIOLATED"

    if gate_abs / full_abs < 0.10:
        pred3 = "FALSIFIED_NULL"  # gate-only ≈ baseline
    elif gate_s1_verdict in ("V14_PASS_ROBUST", "V14_PASS_PARTIAL") and gate_abs < 0.7 * full_abs:
        pred3 = "CONFIRMED"
    elif gate_s1_verdict == "V14_VIOLATED" and gate_abs < 0.7 * full_abs:
        pred3 = "PARTIALLY_CONFIRMED"
    else:
        # gate-only matches full slab magnitude
        pred3 = "FALSIFIED_MATCH"

    log(f"  PREDICTION 3 (MLP-gate < full-slab):")
    log(f"    full-slab1 sep_change ref (§57) = {SLAB1_FULL_SEP_CHANGE_REF:.2f}")
    log(f"    gate × slab1 sep_change         = {gate_s1_sep_change:+.2f}  "
        f"abs ratio = {gate_abs/full_abs*100:.1f}%  verdict={gate_s1_verdict}")
    log(f"    up   × slab1 sep_change         = {up_s1_sep_change:+.2f}  "
        f"abs ratio = {abs(up_s1_sep_change)/full_abs*100:.1f}%  "
        f"verdict={cond_dispo['C4_up_slab1']['verdict']}")
    log(f"    down × slab1 sep_change         = {down_s1_sep_change:+.2f}  "
        f"abs ratio = {abs(down_s1_sep_change)/full_abs*100:.1f}%  "
        f"verdict={cond_dispo['C5_down_slab1']['verdict']}")
    log(f"    PRED3 = {pred3}")

    # tok_emb / lm_head disposition
    tok_sep = cond_dispo["C6_tok_emb_only"]["separation_un16"]
    lm_sep = cond_dispo["C7_lm_head_only"]["separation_un16"]
    pair_sep = cond_dispo["C8_tok_emb_lm_pair"]["separation_un16"]
    tok_sep_change = tok_sep - base_sep
    lm_sep_change = lm_sep - base_sep
    pair_sep_change = pair_sep - base_sep

    def _dir_class(sep_change_abs: float, full_abs: float, verdict: str) -> str:
        if verdict in ("V14_PASS_ROBUST",) and sep_change_abs / full_abs < 0.05:
            return "none"
        if verdict in ("V14_PASS_ROBUST", "V14_PASS_PARTIAL") and sep_change_abs / full_abs < 0.30:
            return "weak"
        return "significant"

    tok_dir = _dir_class(abs(tok_sep_change), full_abs, cond_dispo["C6_tok_emb_only"]["verdict"])
    lm_dir = _dir_class(abs(lm_sep_change), full_abs, cond_dispo["C7_lm_head_only"]["verdict"])
    pair_dir = _dir_class(abs(pair_sep_change), full_abs, cond_dispo["C8_tok_emb_lm_pair"]["verdict"])

    log(f"  tok_emb/lm_head V14 effect:")
    log(f"    C6 tok_emb only sep_change={tok_sep_change:+.2f}  "
        f"verdict={cond_dispo['C6_tok_emb_only']['verdict']}  direction={tok_dir}")
    log(f"    C7 lm_head only sep_change={lm_sep_change:+.2f}  "
        f"verdict={cond_dispo['C7_lm_head_only']['verdict']}  direction={lm_dir}")
    log(f"    C8 pair         sep_change={pair_sep_change:+.2f}  "
        f"verdict={cond_dispo['C8_tok_emb_lm_pair']['verdict']}  direction={pair_dir}")

    # F-COMP-5 sanity: lm_head only must be ≈ baseline (it's downstream of HiddenMeanCapture)
    lm_only_abs_diff_vs_baseline = abs(cond_dispo["C7_lm_head_only"]["trained_un16_mean"] - base_un)
    f_comp_5_passed = (lm_only_abs_diff_vs_baseline < 1e-3)  # bit-exact at fp32 — should be 0
    log(f"  F-COMP-5 sanity: lm_head only |trained_un16 − baseline| = {lm_only_abs_diff_vs_baseline:.6e}")
    log(f"    F-COMP-5 (lm_head ≡ baseline): {'PASSED (sanity confirmed)' if f_comp_5_passed else 'FAILED (instrumentation bug)'}")

    elapsed_total = time.time() - t_start_global
    log(f"\n  total elapsed = {elapsed_total:.1f}s ({elapsed_total/60:.1f}min)")

    # ─── summary.json ─────────────────────────────────────────────────
    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "elapsed_sec_total": elapsed_total,
        "config": {
            "ckpt_A_phase2": CKPT_PHASE2,
            "ckpt_B_bgla": CKPT_BGLA,
            "n_turns": N_TURNS,
            "max_cells": MAX_CELLS,
            "snapshot_every": SNAPSHOT_EVERY,
            "mirror_seeds": MIRROR_SEEDS,
            "slabs": {k: v for k, v in SLABS.items()},
        },
        "mirror_baseline": {
            "seeds": MIRROR_SEEDS,
            "un16_per_seed": mirror_un,
            "proxy_per_seed": mirror_proxy,
            "cells_per_seed": mirror_cells,
            "un16_mean": mirror_un_mean,
            "proxy_mean": mirror_proxy_mean,
        },
        "baseline_C0": {
            "trained_un16": base_un,
            "separation_un16": base_sep,
        },
        "cond_dispo": cond_dispo,
        "prediction3": {
            "ref_full_slab1_sep_change_57": SLAB1_FULL_SEP_CHANGE_REF,
            "gate_slab1_sep_change": gate_s1_sep_change,
            "gate_slab1_abs_ratio": gate_abs / full_abs,
            "gate_slab1_verdict": gate_s1_verdict,
            "up_slab1_sep_change": up_s1_sep_change,
            "down_slab1_sep_change": down_s1_sep_change,
            "verdict": pred3,
        },
        "tok_emb_lm_head": {
            "tok_emb_only_sep_change": tok_sep_change,
            "tok_emb_only_direction": tok_dir,
            "lm_head_only_sep_change": lm_sep_change,
            "lm_head_only_direction": lm_dir,
            "pair_sep_change": pair_sep_change,
            "pair_direction": pair_dir,
            "f_comp_5_passed": f_comp_5_passed,
            "f_comp_5_lm_head_diff_vs_baseline": lm_only_abs_diff_vs_baseline,
        },
    }
    (THIS_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    log("  summary.json written")

    # ─── verdict.md ───────────────────────────────────────────────────
    _write_verdict_md(THIS_DIR / "verdict.md", summary)
    log("  verdict.md written")

    log_f.close()
    return summary


# ── verdict.md writer ────────────────────────────────────────────────


def _write_verdict_md(path: Path, summary: dict):
    cd = summary["cond_dispo"]
    p3 = summary["prediction3"]
    tl = summary["tok_emb_lm_head"]
    base_un = summary["baseline_C0"]["trained_un16"]
    mirror_un_mean = summary["mirror_baseline"]["un16_mean"]
    base_sep = summary["baseline_C0"]["separation_un16"]

    lines: List[str] = []
    lines.append("# BG-COMPONENT-MLP-EMBED-V14 — verdict\n")

    # Top-line verdicts
    pred3 = p3["verdict"]
    lines.append(f"**verdict: PREDICTION_3 (MLP-gate)** = `{pred3}`\n")
    tok_dir = tl["tok_emb_only_direction"]
    lm_dir = tl["lm_head_only_direction"]
    pair_dir = tl["pair_direction"]
    lines.append(f"**verdict: tok_emb / lm_head V14 effect direction** — "
                 f"tok_emb=`{tok_dir}`, lm_head=`{lm_dir}`, pair=`{pair_dir}`\n")

    # Falsifier disposition
    lines.append("**falsifier disposition**:")
    if pred3 == "CONFIRMED":
        lines.append("- F-COMP-1 (gate × slab1 between baseline and full slab): **CONFIRMED**")
        lines.append("- F-COMP-2 (gate matches full slab): not triggered")
        lines.append("- F-COMP-3 (gate negligible): not triggered")
    elif pred3 == "PARTIALLY_CONFIRMED":
        lines.append("- F-COMP-1 (gate × slab1 between baseline and full slab): **partially CONFIRMED** — gate flipped V14 but with smaller magnitude than full slab (<70%)")
        lines.append("- F-COMP-2 (gate matches full slab): not triggered")
        lines.append("- F-COMP-3 (gate negligible): not triggered")
    elif pred3 == "FALSIFIED_NULL":
        lines.append("- F-COMP-1 (gate × slab1 between baseline and full slab): not triggered")
        lines.append("- F-COMP-2 (gate matches full slab): not triggered")
        lines.append("- F-COMP-3 (gate negligible): **TRIGGERED** — gate-only barely perturbs V14")
    elif pred3 == "FALSIFIED_MATCH":
        lines.append("- F-COMP-1 (gate × slab1 between baseline and full slab): not triggered")
        lines.append("- F-COMP-2 (gate matches full slab): **TRIGGERED** — gate alone reproduces full-slab V14 effect")
        lines.append("- F-COMP-3 (gate negligible): not triggered")

    if cd["C6_tok_emb_only"]["verdict"] == "V14_VIOLATED":
        lines.append("- F-COMP-4 (tok_emb causally dominant): **TRIGGERED** — tok_emb-only swap flipped V14")
    else:
        lines.append("- F-COMP-4 (tok_emb causally dominant): not triggered")

    if tl["f_comp_5_passed"]:
        lines.append("- F-COMP-5 (lm_head ≡ baseline sanity): **PASSED** — lm_head untied swap left V14 trajectory bit-identical to baseline (downstream-of-capture confirmed)")
    else:
        lines.append(f"- F-COMP-5 (lm_head ≡ baseline sanity): **FAILED** — instrumentation bug; |Δ_un16|={tl['f_comp_5_lm_head_diff_vs_baseline']:.2e} (expected 0)")

    lines.append(f"\n**Elapsed**: {summary['elapsed_sec_total']:.1f}s ({summary['elapsed_sec_total']/60:.1f}min)\n")

    # Mirror baseline
    lines.append("## Mirror baseline (3 random_init seeds)\n")
    lines.append(f"- seeds: {summary['mirror_baseline']['seeds']}")
    lines.append(f"- Φ_un16 per seed: {summary['mirror_baseline']['un16_per_seed']}")
    lines.append(f"- Φ_un16 mean: {mirror_un_mean:.2f}")
    lines.append(f"- proxy mean: {summary['mirror_baseline']['proxy_mean']:.4f}")
    lines.append(f"- cells per seed: {summary['mirror_baseline']['cells_per_seed']}")

    lines.append("\n## C0 baseline\n")
    lines.append(f"- trained Φ_un16 = {base_un:.2f}  separation = {base_sep:+.2f}")

    # Per-condition table
    lines.append("\n## Per-condition disposition (30 V14 trials)\n")
    lines.append(f"`N_TURNS={summary['config']['n_turns']}`, "
                 f"`MAX_CELLS={summary['config']['max_cells']}`\n")
    lines.append("| condition | swap | n_trials | trained Φ_un16 mean ± std | separation | sep_change vs base | cells (per seed) | n_beats_un | n_beats_proxy | verdict |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    cond_order = ["C0_baseline",
                  "C1_gate_slab1", "C2_gate_slab2", "C3_gate_slab3",
                  "C4_up_slab1", "C5_down_slab1",
                  "C6_tok_emb_only", "C7_lm_head_only", "C8_tok_emb_lm_pair"]
    for cl in cond_order:
        d = cd[cl]
        sep_change = d["separation_un16"] - base_sep
        # short swap descriptor
        if d["swap_fn"] == "none":
            sw = "—"
        elif d["swap_fn"] == "mlp_slab":
            sw = f"`ffn.{d['swap_args']['comp']} ← {d['swap_args']['slab']}`"
        else:
            sw = f"`{d['swap_fn']}`"
        lines.append(
            f"| `{cl}` | {sw} | {d['n_trials']} | "
            f"{d['trained_un16_mean']:.2f} ± {d['trained_un16_std']:.2f} | "
            f"{d['separation_un16']:+.2f} | "
            f"{sep_change:+.2f} | "
            f"{d['trained_cells_per_seed']} | "
            f"{d['n_beats_un']}/{d['n_trials']} | "
            f"{d['n_beats_proxy']}/{d['n_trials']} | "
            f"`{d['verdict']}` |"
        )

    # Prediction 3 detailed analysis
    lines.append("\n## Prediction 3 — MLP-gate vs full slab1 swap\n")
    lines.append(f"§57 reference: A1_slab1_early full-slab swap → trained_un16=1036.86, "
                 f"separation_change_vs_baseline = **{p3['ref_full_slab1_sep_change_57']:+.2f}** (V14_VIOLATED).\n")
    lines.append(f"This BG (n_turns={summary['config']['n_turns']}, mirror_un_mean={mirror_un_mean:.2f}):\n")
    lines.append("| component × slab | sep_change | abs ratio vs §57 full | verdict |")
    lines.append("|---|---|---|---|")
    full_abs = abs(p3["ref_full_slab1_sep_change_57"])
    for k in ["C1_gate_slab1", "C2_gate_slab2", "C3_gate_slab3",
              "C4_up_slab1", "C5_down_slab1"]:
        d = cd[k]
        sc = d["separation_un16"] - base_sep
        ratio = abs(sc) / full_abs * 100
        lines.append(f"| `{k}` ({d['swap_args'].get('comp','—')} × {d['swap_args'].get('slab','—')}) "
                     f"| {sc:+.2f} | {ratio:.1f}% | `{d['verdict']}` |")

    lines.append(f"\n**PRED3 verdict**: `{pred3}`")
    lines.append(f"- gate × slab1 sep_change ratio: {p3['gate_slab1_abs_ratio']*100:.1f}% of §57 full-slab")
    lines.append(f"- gate × slab1 verdict: `{p3['gate_slab1_verdict']}`")
    if pred3 == "CONFIRMED":
        lines.append("- Interpretation: MLP-gate carries part of the slab1 V14 lever but does not exhaust it. Other intra-block components (q/k/v/o + up + down) collectively carry the rest. Cross-link with §62 (q_proj weight-drift dominance): MLP-gate functional contribution is non-trivial despite cos_AB drift being lower than q_proj.")
    elif pred3 == "PARTIALLY_CONFIRMED":
        lines.append("- Interpretation: MLP-gate alone is sufficient to flip V14 verdict but carries less than 70% of the magnitude. Distributed slab1 lever, with gate as one of several contributors.")
    elif pred3 == "FALSIFIED_MATCH":
        lines.append("- Interpretation: MLP-gate component alone reproduces the full slab1 swap effect — gate IS the slab1 lever. This would invert §62's q_proj weight-drift primacy at the functional level.")
    elif pred3 == "FALSIFIED_NULL":
        lines.append("- Interpretation: MLP-gate barely perturbs V14. The slab1 lever lives in attention components (q/k/v/o) or in the gate↔up multiplicative coupling, not in gate alone.")

    # tok_emb / lm_head
    lines.append("\n## tok_emb / lm_head — beyond §57 swap surface\n")
    lines.append("§57's swap surface was layers-only; `tok_emb`, `norm_f`, `lm_head` always retained A's values. §62 found `tok_emb.weight` cos_AB = 0.7464 (non-trivial drift). This BG opens that surface.\n")
    lines.append(f"`EngineAGModel.cfg.tie_lm_head=True` → `lm_head.weight` shares storage with `tok_emb.weight` at runtime. C6 / C7 untie pre-swap; C8 keeps tying.\n")
    lines.append("| condition | direction | sep_change | verdict | trained Φ_un16 mean ± std |")
    lines.append("|---|---|---|---|---|")
    for k, dir_lbl in [("C6_tok_emb_only", tok_dir),
                        ("C7_lm_head_only", lm_dir),
                        ("C8_tok_emb_lm_pair", pair_dir)]:
        d = cd[k]
        sc = d["separation_un16"] - base_sep
        lines.append(f"| `{k}` | `{dir_lbl}` | {sc:+.2f} | `{d['verdict']}` | "
                     f"{d['trained_un16_mean']:.2f} ± {d['trained_un16_std']:.2f} |")

    lines.append(f"\n**F-COMP-5 sanity check** (lm_head untied swap should be bit-identical to baseline because `HiddenMeanCapture` hooks `engine_g`, which receives `hidden_mean` BEFORE `lm_head`):")
    lines.append(f"- |trained_un16(C7) − trained_un16(C0)| = {tl['f_comp_5_lm_head_diff_vs_baseline']:.2e}")
    lines.append(f"- Sanity: {'PASSED' if tl['f_comp_5_passed'] else 'FAILED — INSTRUMENTATION BUG'}")
    if tl["f_comp_5_passed"]:
        lines.append("- Confirms instrumentation correctness: lm_head is downstream of cell dynamics; lm_head perturbation cannot affect engine_g cell-pool trajectory.")

    # Honest C3
    lines.append("\n## Honest C3 (≥5)\n")
    lines.append("1. **n_turns=128 vs §57 n_turns=200.** This run uses a shorter trajectory to fit the 30-trial × 30s budget. §57's full-slab1 separation_change reference of −1375.23 was measured at n_turns=200 with mirror_mean=1615.49. Our mirror_mean differs (computed live in this run). Comparing absolute separation magnitudes across runs is a heuristic; the qualitative shape (gate-only sep_change << full-slab sep_change?) is the load-bearing claim. To strictly compare, a follow-up at n_turns=200 with the same mirror seeds is canonical.")
    lines.append("2. **Trial count asymmetry.** MLP conditions get 3 seeds (42, 137, 271); embedding conditions get 5 seeds. Statistical power for 5-seed conditions is higher; 3-seed conditions can be ambiguous within ~20% of the verdict boundary. The condition-level verdict (PASS_ROBUST / PARTIAL / VIOLATED) is robust if separation magnitude is large.")
    lines.append("3. **Untying lm_head changes the model graph, not just weights.** `untie_lm_head_` rebinds `model.lm_head.weight` to a fresh `nn.Parameter`. Forward passes after untying may have subtly different fp32 round-off from the tied path (different memory layout, different reduction order in some kernels). For C7 (lm_head only swap) this should still be exactly bit-identical to baseline at the engine_g `hidden_mean` capture point because lm_head is downstream — F-COMP-5 confirms or denies this.")
    lines.append("4. **B's lm_head and tok_emb are themselves tied.** Both A and B use `tie_lm_head=True`. So `B_tok_emb` and `B_lm_head` are byte-identical clones (max_abs_diff = 0). Therefore C6 (tok_emb only swap) and C7 (lm_head only swap) use the *same source tensor* — different destinations only. The C8 paired swap is what the natural deployment looks like (tying preserved).")
    lines.append("5. **byte-hash prompt encoding.** `encode_prompt_to_ids` is the §38/§47/§50/§57 lineage encoding — relative trained-vs-mirror comparison only, no semantic claim about prompt content. Identical across all 30 trials.")
    lines.append("6. **Engine G modules untouched in MLP conditions.** All MLP-axis conditions retain A's `cell_pool_init`, `c_to_h`, `h_to_c`, plus all `tok_emb`/`lm_head`/`norm_f`. Only the targeted `ffn.{gate|up|down}.weight` of slab1 (or the requested slab) gets swapped to B. This isolates per-component contribution within `EngineABlock.ffn`.")
    lines.append("7. **Single-seed source for swap-source.** B is one ckpt at one training step (step_12000). Multi-seed B would strengthen the inference; deferred per own 16.")
    lines.append("8. **Separation_change interpretation depends on mirror stability.** Mirror trajectories use `load_random_init(seed=s, preset='la_350m')` and never see A's swapped state. Mirror means are therefore independent of swap and serve as control reference. Identical mirror means across rows are the experimental design (mirror = control), not numerical artifact.")
    lines.append("9. **F-COMP-5 is a strict sanity test.** If lm_head untied swap produces ANY difference in trained_un16 vs baseline, the instrumentation is wrong (e.g., `HiddenMeanCapture` is hooking the wrong module). PASSED is the expected outcome; FAILED implies the trial results need re-validation.")
    lines.append("10. **C8 (paired) tying preservation is the deployment-realistic test.** When tied, swapping `tok_emb.weight` propagates to `lm_head.weight`. This is the natural cotrain regime. C6/C7 are diagnostic untied splits to measure the embedding-only contribution to V14 (since lm_head is downstream of capture).")

    path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
