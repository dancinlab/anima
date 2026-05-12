"""BG-COTRAIN-EXERCISE-CAUSAL-PROOF — §47 cotrain-exercise causal evidence pipeline.

Three streams:
  1) weight-space statistics — Phase 2 (A) vs BG-LA (B) vs random_init on
     engine_g.cell_pool_init, c_to_h.weight, h_to_c.weight
        L2 norm | rank | top-k SVD spectrum | sparsity (<0.01) | cos-sim to random_init
  2) forward-pass diversity — same prompt set fed to A vs B; capture hidden_mean
     (post-norm, pre-engine_g.step) AND c_to_h(hidden_mean); measure per-dim
     variance and average pairwise cosine across N samples.
  3) ablation — start from Phase 2 (A) ckpt; mutate engine_g.{cell_pool_init,
     c_to_h, h_to_c} individually with random_init or BG-LA values; re-run
     V14 mirror short-trajectory; see if PASS direction flips.

raw#9   training/*.py local-only; this lives under state/ which is gitignored.
raw#15  additive — both ckpts loaded read-only; in-memory mutation only.
own 14  V14 mirror multi-seed.
own 16  $0 local Mac CPU.
own 22  honest emit — verdicts, edges, no fabrication.
own 38  artefacts under state/anima_cotrain_exercise_causal_proof_2026_05_10/
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import torch
import torch.nn.functional as F

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

THIS_DIR = Path(f"{ANIMA}/state/anima_cotrain_exercise_causal_proof_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PHASE2 = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_BGLA = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt"

V4_SEEDS = [42, 137, 271]                # 3 seeds × 5 conditions
N_TURNS_ABL = 200                        # short trajectory for ablation (own 16 budget)
SNAPSHOT_EVERY = 25
MAX_CELLS = 128
N_DIV_PROMPTS = 80                       # forward-diversity sample size
RANDOM_INIT_SEED = 42                    # baseline random_init for ablation


# ── ckpt loaders ──────────────────────────────────────────────────────


def _load_engine_ag(ckpt_path: str, lineage: str) -> EngineAGModel:
    cfg = (
        EngineAGConfig.phase2_cotrain_350m()
        if lineage == "phase2_cotrain"
        else EngineAGConfig.la_350m()
    )
    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    # Schema variance: phase2 uses 'model'; bg_la uses 'state_dict'
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


# ── Phase 1: weight-space statistics ─────────────────────────────────


def _matrix_stats(W: torch.Tensor, baseline: torch.Tensor | None = None) -> Dict[str, Any]:
    """L2 norm + rank (rcond=1e-3) + top-k SVD + sparsity + optional cos-sim to baseline."""
    W32 = W.detach().float().cpu()
    out: Dict[str, Any] = {
        "shape": list(W32.shape),
        "n_params": int(W32.numel()),
        "l2_norm": float(W32.norm().item()),
        "frobenius_per_param": float(W32.norm().item() / max(1, W32.numel()) ** 0.5),
    }
    if W32.dim() == 2:
        # SVD: matrix
        try:
            U, S, Vt = torch.linalg.svd(W32, full_matrices=False)
            S_np = S.numpy()
            tol = max(W32.shape) * S_np.max() * 1e-7
            out["rank_machine"] = int((S_np > tol).sum())
            # Effective rank @ rcond=1e-3 of max
            rcond = 1e-3
            out["rank_rcond_1e-3"] = int((S_np > rcond * S_np.max()).sum())
            out["singular_top10"] = [float(s) for s in S_np[:10].tolist()]
            out["singular_max"] = float(S_np.max())
            out["singular_min"] = float(S_np.min())
            out["singular_geomean"] = float(np.exp(np.mean(np.log(S_np + 1e-12))))
            # Effective rank (Roy & Vetterli) = exp(H(p)) with p = s_i / sum(s)
            p = S_np / (S_np.sum() + 1e-12)
            ent = -np.sum(p * np.log(p + 1e-12))
            out["effective_rank"] = float(np.exp(ent))
        except Exception as e:
            out["svd_error"] = str(e)
    else:
        # 1D / vector — flatten
        flat = W32.flatten()
        out["singular_top10"] = []
        out["effective_rank"] = float("nan")
    # sparsity: fraction of |w| < 0.01
    out["sparsity_lt_001"] = float((W32.abs() < 0.01).float().mean().item())
    out["sparsity_lt_0001"] = float((W32.abs() < 0.001).float().mean().item())
    out["mean_abs"] = float(W32.abs().mean().item())
    out["std"] = float(W32.std().item())
    if baseline is not None:
        b32 = baseline.detach().float().cpu()
        out["cos_sim_to_baseline"] = float(
            F.cosine_similarity(W32.flatten().unsqueeze(0), b32.flatten().unsqueeze(0)).item()
        )
        out["l2_diff_to_baseline"] = float((W32 - b32).norm().item())
    return out


def weight_statistics(model_A: EngineAGModel, model_B: EngineAGModel,
                      model_R: EngineAGModel) -> Dict[str, Any]:
    """A=Phase 2 cotrain, B=BG-LA pretrain, R=random_init seed=42."""
    targets = ["cell_pool_init", "c_to_h.weight", "h_to_c.weight"]
    out: Dict[str, Any] = {"random_init_seed": RANDOM_INIT_SEED, "stats": {}}
    for tgt in targets:
        wA = _get_engine_g_param(model_A, tgt)
        wB = _get_engine_g_param(model_B, tgt)
        wR = _get_engine_g_param(model_R, tgt)
        sA = _matrix_stats(wA, baseline=wR)
        sB = _matrix_stats(wB, baseline=wR)
        sR = _matrix_stats(wR)  # baseline is itself; cos = 1
        out["stats"][tgt] = {
            "A_phase2_cotrain": sA,
            "B_bgla_pretrain": sB,
            "R_random_init": sR,
            "delta_A_minus_B": {
                "l2_norm": sA["l2_norm"] - sB["l2_norm"],
                "effective_rank": sA.get("effective_rank", float("nan")) - sB.get("effective_rank", float("nan")),
                "sparsity_lt_001": sA["sparsity_lt_001"] - sB["sparsity_lt_001"],
                "cos_to_random_baseline": sA.get("cos_sim_to_baseline", 0.0) - sB.get("cos_sim_to_baseline", 0.0),
            },
            "cos_A_vs_B": float(
                F.cosine_similarity(
                    wA.detach().float().flatten().unsqueeze(0),
                    wB.detach().float().flatten().unsqueeze(0),
                ).item()
            ),
        }
    return out


def _get_engine_g_param(model: EngineAGModel, name: str) -> torch.Tensor:
    """Return engine_g.<name> as a Tensor (cell_pool_init / c_to_h.weight / h_to_c.weight)."""
    eg = model.engine_g
    if name == "cell_pool_init":
        return eg.cell_pool_init.data
    elif name == "c_to_h.weight":
        return eg.c_to_h.weight.data
    elif name == "h_to_c.weight":
        return eg.h_to_c.weight.data
    raise KeyError(name)


# ── Phase 2: forward-pass diversity ───────────────────────────────────


def forward_diversity(model: EngineAGModel, label: str, n_prompts: int = N_DIV_PROMPTS,
                      ctx_T: int = 16) -> Dict[str, Any]:
    """Capture engine_g.step's hidden_mean input across N prompts → measure
       (a) variance across samples per-dim (mean+sum of variances),
       (b) average pairwise cosine,
       (c) entropy proxy via ln(det(cov+eps)) of c_to_h projection.
    """
    model.eval()
    cap = HiddenMeanCapture(model.engine_g)
    eg = model.engine_g
    hm_list: List[torch.Tensor] = []
    cproj_list: List[torch.Tensor] = []
    with torch.no_grad():
        n_used = 0
        for cat, prompt in ALL_PROMPTS:
            if n_used >= n_prompts:
                break
            ids = encode_prompt_to_ids(prompt, T=ctx_T)
            _ = model(ids, output_hidden_states=False, output_attentions=False)
            hm = cap.last_hidden_mean
            if hm is None:
                continue
            # hm shape (B=1, d_model)
            hm_v = hm.detach().squeeze(0).float()  # (1024,)
            hm_list.append(hm_v)
            cproj_list.append(eg.h_to_c(hm_v.unsqueeze(0)).squeeze(0).float().detach())  # (64,)
            n_used += 1
    H = torch.stack(hm_list, dim=0)   # (N, 1024)
    C = torch.stack(cproj_list, dim=0)  # (N, 64)

    def _stats(X: torch.Tensor, name: str) -> Dict[str, Any]:
        N = X.shape[0]
        # per-dim variance
        var_per = X.var(dim=0)  # (D,)
        mean_var = float(var_per.mean().item())
        sum_var = float(var_per.sum().item())
        # pairwise cosine (avg, off-diag)
        Xn = F.normalize(X, dim=-1, eps=1e-8)
        cos = Xn @ Xn.T  # (N, N)
        mask = ~torch.eye(N, dtype=torch.bool)
        avg_pairwise_cos = float(cos[mask].mean().item())
        # cov entropy proxy: log-det of cov + eps*I
        Xc = X - X.mean(dim=0, keepdim=True)
        cov = (Xc.T @ Xc) / max(1, N - 1)
        eps = 1e-4
        cov_reg = cov + eps * torch.eye(cov.shape[0])
        try:
            sign, logdet = torch.linalg.slogdet(cov_reg)
            logdet_v = float(logdet.item())
        except Exception:
            logdet_v = float("nan")
        # effective dim (Roy-Vetterli on cov eigvals)
        try:
            evals = torch.linalg.eigvalsh(cov_reg).clamp(min=1e-12)
            p = evals / evals.sum()
            ent = float(-(p * p.log()).sum().item())
            eff_dim = float(math.exp(ent))
        except Exception:
            eff_dim = float("nan")
        return {
            "tensor": name,
            "n_samples": int(N),
            "dim": int(X.shape[1]),
            "mean_per_dim_variance": mean_var,
            "sum_variance": sum_var,
            "avg_pairwise_cosine": avg_pairwise_cos,
            "logdet_cov": logdet_v,
            "effective_dim": eff_dim,
        }

    return {
        "label": label,
        "n_prompts_used": int(H.shape[0]),
        "hidden_mean": _stats(H, "hidden_mean"),
        "c_to_h_proj": _stats(C, "c_to_h(hidden_mean)"),
    }


# ── Phase 3: ablation V14 short trajectories ─────────────────────────


def _run_v14_short(model: EngineAGModel, label: str, seeds: List[int],
                   n_turns: int, snap_every: int, max_cells: int,
                   ctx_T: int = 16) -> Dict[str, Any]:
    """Run trained vs len(seeds) random_init mirror seeds. Returns aggregate verdict."""

    def run_one(M: EngineAGModel, sublabel: str, seed: int) -> Dict[str, Any]:
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

    # trained
    tr = run_one(model, f"{label}_trained", seed=42)

    # random mirrors (load_random_init la_350m preset, since arch params identical)
    mirrors = []
    for s in seeds:
        rm = load_random_init(seed=s, preset="la_350m")
        mr = run_one(rm, f"{label}_mirror_s{s}", seed=s)
        mirrors.append(mr)
        del rm

    rs_un = [m["final_iit_un16"] for m in mirrors]
    rs_proxy = [m["final_proxy_phi"] for m in mirrors]
    rs_cells = [m["final_n_cells"] for m in mirrors]
    n_beats_un = sum(1 for r in rs_un if tr["final_iit_un16"] > r)
    n_beats_proxy = sum(1 for r in rs_proxy if tr["final_proxy_phi"] > r)
    if n_beats_un == len(seeds) and n_beats_proxy == len(seeds):
        verdict = "V14_PASS"
    elif n_beats_un == len(seeds) or n_beats_proxy == len(seeds):
        verdict = "V14_PARTIAL"
    else:
        verdict = "V14_VIOLATED"
    return {
        "label": label,
        "trained": tr,
        "mirrors": mirrors,
        "verdict": verdict,
        "n_beats_iit_un16": n_beats_un,
        "n_beats_proxy_phi": n_beats_proxy,
        "n_seeds": len(seeds),
        "trained_iit_un16": tr["final_iit_un16"],
        "mirror_iit_un16_mean": float(np.mean(rs_un)),
        "mirror_iit_un16_min": float(np.min(rs_un)),
        "mirror_iit_un16_max": float(np.max(rs_un)),
        "trained_proxy_phi": tr["final_proxy_phi"],
        "mirror_proxy_phi_mean": float(np.mean(rs_proxy)),
        "trained_n_cells": tr["final_n_cells"],
        "mirror_n_cells": rs_cells,
    }


def _swap_param(model: EngineAGModel, name: str, new_value: torch.Tensor):
    """Replace engine_g.<name> with new_value (shape-checked, in-place)."""
    eg = model.engine_g
    if name == "cell_pool_init":
        assert eg.cell_pool_init.data.shape == new_value.shape
        eg.cell_pool_init.data.copy_(new_value)
    elif name == "c_to_h":
        assert eg.c_to_h.weight.data.shape == new_value.shape
        eg.c_to_h.weight.data.copy_(new_value)
    elif name == "h_to_c":
        assert eg.h_to_c.weight.data.shape == new_value.shape
        eg.h_to_c.weight.data.copy_(new_value)
    else:
        raise KeyError(name)


# ── Main ──────────────────────────────────────────────────────────────


def main():
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(m: str):
        print(m, flush=True)
        log_f.write(m + "\n"); log_f.flush()

    log("=== BG-COTRAIN-EXERCISE-CAUSAL-PROOF ===")
    log(f"ts: {datetime.now(timezone.utc).isoformat()}")
    log(f"V4_SEEDS={V4_SEEDS}  N_TURNS_ABL={N_TURNS_ABL}  MAX_CELLS={MAX_CELLS}")

    # ─── load all three substrates ───
    log("\n--- loading ckpts ---")
    t0 = time.time()
    model_A = _load_engine_ag(CKPT_PHASE2, "phase2_cotrain")
    log(f"  Phase 2 (A) loaded: {time.time()-t0:.1f}s")
    t0 = time.time()
    model_B = _load_engine_ag(CKPT_BGLA, "la_350m")
    log(f"  BG-LA   (B) loaded: {time.time()-t0:.1f}s")
    t0 = time.time()
    model_R = load_random_init(seed=RANDOM_INIT_SEED, preset="la_350m")
    log(f"  random  (R) seed={RANDOM_INIT_SEED}: {time.time()-t0:.1f}s")

    # ─── Phase 1 — weight-space statistics ───
    log("\n--- Phase 1: weight-space statistics ---")
    t0 = time.time()
    ws = weight_statistics(model_A, model_B, model_R)
    elapsed1 = time.time() - t0
    log(f"  weight_statistics done: {elapsed1:.1f}s")
    (THIS_DIR / "weight_statistics.json").write_text(json.dumps(ws, indent=2))
    for tgt, blk in ws["stats"].items():
        a = blk["A_phase2_cotrain"]; b = blk["B_bgla_pretrain"]; r = blk["R_random_init"]
        log(f"  {tgt:>20s}  l2 A={a['l2_norm']:.3f} B={b['l2_norm']:.3f} R={r['l2_norm']:.3f}"
            f"  effrank A={a.get('effective_rank', float('nan')):.2f}"
            f" B={b.get('effective_rank', float('nan')):.2f}"
            f"  spar<.01 A={a['sparsity_lt_001']:.3f} B={b['sparsity_lt_001']:.3f}"
            f"  cosA-vs-B={blk['cos_A_vs_B']:.4f}")

    # ─── Phase 2 — forward-pass diversity ───
    log(f"\n--- Phase 2: forward-pass diversity (n_prompts={N_DIV_PROMPTS}) ---")
    t0 = time.time()
    div_A = forward_diversity(model_A, label="A_phase2_cotrain")
    log(f"  diversity A done: {time.time()-t0:.1f}s")
    t0 = time.time()
    div_B = forward_diversity(model_B, label="B_bgla_pretrain")
    log(f"  diversity B done: {time.time()-t0:.1f}s")
    t0 = time.time()
    div_R = forward_diversity(model_R, label="R_random_init")
    log(f"  diversity R done: {time.time()-t0:.1f}s")
    div_all = {"A": div_A, "B": div_B, "R": div_R}
    (THIS_DIR / "forward_diversity.json").write_text(json.dumps(div_all, indent=2))
    for tag, d in div_all.items():
        h = d["hidden_mean"]; c = d["c_to_h_proj"]
        log(f"  {tag}: hm avg_cos={h['avg_pairwise_cosine']:.4f}"
            f" eff_dim={h['effective_dim']:.2f}"
            f"  c_to_h(hm) avg_cos={c['avg_pairwise_cosine']:.4f}"
            f" eff_dim={c['effective_dim']:.2f}")

    # ─── Phase 3 — ablation V14 ───
    log(f"\n--- Phase 3: ablation V14 (n_turns={N_TURNS_ABL}, seeds={V4_SEEDS}) ---")
    # free B before phase 3 — only A and R needed
    cell_pool_R = _get_engine_g_param(model_R, "cell_pool_init").clone()
    c_to_h_R = _get_engine_g_param(model_R, "c_to_h.weight").clone()
    h_to_c_R = _get_engine_g_param(model_R, "h_to_c.weight").clone()
    del model_B, model_R
    import gc; gc.collect()

    # Baseline: pristine A (no swap)
    t0 = time.time()
    abl_baseline = _run_v14_short(_clone_engine_ag_from(model_A), "ABL0_baseline_A",
                                  V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    log(f"  baseline A (no swap): verdict={abl_baseline['verdict']} ({time.time()-t0:.1f}s)")
    log(f"    trained Φ_un16={abl_baseline['trained_iit_un16']:.2f} mirror_mean={abl_baseline['mirror_iit_un16_mean']:.2f}"
        f" beats={abl_baseline['n_beats_iit_un16']}/{abl_baseline['n_seeds']}"
        f" cells={abl_baseline['trained_n_cells']} mirror_cells={abl_baseline['mirror_n_cells']}")

    # Ablation 1: c_to_h ← random_init
    t0 = time.time()
    M1 = _clone_engine_ag_from(model_A)
    _swap_param(M1, "c_to_h", c_to_h_R)
    abl_c2h = _run_v14_short(M1, "ABL1_c_to_h_random",
                             V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    del M1; gc.collect()
    log(f"  ABL1 c_to_h←random: verdict={abl_c2h['verdict']} ({time.time()-t0:.1f}s)")
    log(f"    trained Φ_un16={abl_c2h['trained_iit_un16']:.2f} mirror_mean={abl_c2h['mirror_iit_un16_mean']:.2f}"
        f" beats={abl_c2h['n_beats_iit_un16']}/{abl_c2h['n_seeds']}"
        f" cells={abl_c2h['trained_n_cells']} mirror_cells={abl_c2h['mirror_n_cells']}")

    # Ablation 2: h_to_c ← random_init
    t0 = time.time()
    M2 = _clone_engine_ag_from(model_A)
    _swap_param(M2, "h_to_c", h_to_c_R)
    abl_h2c = _run_v14_short(M2, "ABL2_h_to_c_random",
                             V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    del M2; gc.collect()
    log(f"  ABL2 h_to_c←random: verdict={abl_h2c['verdict']} ({time.time()-t0:.1f}s)")
    log(f"    trained Φ_un16={abl_h2c['trained_iit_un16']:.2f} mirror_mean={abl_h2c['mirror_iit_un16_mean']:.2f}"
        f" beats={abl_h2c['n_beats_iit_un16']}/{abl_h2c['n_seeds']}"
        f" cells={abl_h2c['trained_n_cells']} mirror_cells={abl_h2c['mirror_n_cells']}")

    # Ablation 3: both random
    t0 = time.time()
    M3 = _clone_engine_ag_from(model_A)
    _swap_param(M3, "c_to_h", c_to_h_R)
    _swap_param(M3, "h_to_c", h_to_c_R)
    abl_both = _run_v14_short(M3, "ABL3_both_random",
                              V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    del M3; gc.collect()
    log(f"  ABL3 both←random: verdict={abl_both['verdict']} ({time.time()-t0:.1f}s)")
    log(f"    trained Φ_un16={abl_both['trained_iit_un16']:.2f} mirror_mean={abl_both['mirror_iit_un16_mean']:.2f}"
        f" beats={abl_both['n_beats_iit_un16']}/{abl_both['n_seeds']}"
        f" cells={abl_both['trained_n_cells']} mirror_cells={abl_both['mirror_n_cells']}")

    # Ablation 4: cell_pool_init ← random_init (extra)
    t0 = time.time()
    M4 = _clone_engine_ag_from(model_A)
    _swap_param(M4, "cell_pool_init", cell_pool_R)
    abl_pool = _run_v14_short(M4, "ABL4_cell_pool_random",
                              V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    del M4; gc.collect()
    log(f"  ABL4 pool←random: verdict={abl_pool['verdict']} ({time.time()-t0:.1f}s)")
    log(f"    trained Φ_un16={abl_pool['trained_iit_un16']:.2f} mirror_mean={abl_pool['mirror_iit_un16_mean']:.2f}"
        f" beats={abl_pool['n_beats_iit_un16']}/{abl_pool['n_seeds']}"
        f" cells={abl_pool['trained_n_cells']} mirror_cells={abl_pool['mirror_n_cells']}")

    abl_results = {
        "baseline_A": abl_baseline,
        "ABL1_c_to_h_random": abl_c2h,
        "ABL2_h_to_c_random": abl_h2c,
        "ABL3_both_random": abl_both,
        "ABL4_cell_pool_random": abl_pool,
    }
    (THIS_DIR / "ablation_result.json").write_text(json.dumps(abl_results, indent=2))

    # ─── verdict logic ───
    log("\n--- verdict logic ---")
    # F-COTRAIN-EXERCISE-1: weight stats — A vs B differ on at least 2 of 3 targets
    diffs = []
    for tgt in ["cell_pool_init", "c_to_h.weight", "h_to_c.weight"]:
        d = ws["stats"][tgt]["delta_A_minus_B"]
        # significant if l2_norm relative diff > 1% OR cos_A_vs_B < 0.99
        cos_ab = ws["stats"][tgt]["cos_A_vs_B"]
        l2A = ws["stats"][tgt]["A_phase2_cotrain"]["l2_norm"]
        l2B = ws["stats"][tgt]["B_bgla_pretrain"]["l2_norm"]
        rel_l2 = abs(l2A - l2B) / max(l2A, l2B)
        sig = (rel_l2 > 0.01) or (cos_ab < 0.99)
        diffs.append({"target": tgt, "rel_l2": rel_l2, "cos_AB": cos_ab, "significant": sig})
    f1_falsified = sum(1 for d in diffs if d["significant"]) < 2
    log(f"  F-COTRAIN-EXERCISE-1 weight-stats falsifier: {'FALSIFIED' if f1_falsified else 'PASSED (diffs present)'}")
    for d in diffs:
        log(f"    {d['target']}: rel_l2={d['rel_l2']:.4f} cos_AB={d['cos_AB']:.4f} sig={d['significant']}")

    # F-COTRAIN-EXERCISE-2: ablation polarity flip — V14 verdict changes from baseline
    base_v = abl_baseline["verdict"]
    abl_verdicts = {k: v["verdict"] for k, v in abl_results.items()}
    flips = [k for k, v in abl_verdicts.items() if k != "baseline_A" and v != base_v]
    f2_falsified = (len(flips) == 0)
    log(f"  F-COTRAIN-EXERCISE-2 ablation polarity flip: {'FALSIFIED' if f2_falsified else 'PASSED (flips: '+','.join(flips)+')'}")
    log(f"    baseline_A={base_v}")
    for k, v in abl_verdicts.items():
        if k != "baseline_A":
            log(f"    {k}: {v} (flip={v != base_v})")

    # F-COTRAIN-EXERCISE-3: forward-pass diversity — A's c_to_h projection more diverse than B's
    a_eff = div_A["c_to_h_proj"]["effective_dim"]
    b_eff = div_B["c_to_h_proj"]["effective_dim"]
    a_cos = div_A["c_to_h_proj"]["avg_pairwise_cosine"]
    b_cos = div_B["c_to_h_proj"]["avg_pairwise_cosine"]
    # diversity = higher eff_dim, LOWER avg pairwise cosine
    f3_falsified = (a_eff <= b_eff * 1.001) and (a_cos >= b_cos * 0.999)
    log(f"  F-COTRAIN-EXERCISE-3 fwd diversity: {'FALSIFIED' if f3_falsified else 'PASSED'}")
    log(f"    c_to_h(hm) eff_dim A={a_eff:.2f} B={b_eff:.2f}; avg_cos A={a_cos:.4f} B={b_cos:.4f}")

    # Final verdict
    n_pass = sum(1 for x in [not f1_falsified, not f2_falsified, not f3_falsified] if x)
    if not f1_falsified and not f2_falsified:
        final = "PROVEN"   # weight diff present + ablation flips
    elif not f1_falsified and f2_falsified:
        final = "CORRELATIONAL"  # weight diffs but ablation does not flip
    elif f1_falsified:
        final = "FALSIFIED"
    else:
        final = "CORRELATIONAL"
    log(f"\n=== FINAL VERDICT: {final}  (falsifier-pass {n_pass}/3) ===")

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "config": {
            "ckpt_phase2": CKPT_PHASE2, "ckpt_bgla": CKPT_BGLA,
            "random_init_seed": RANDOM_INIT_SEED,
            "ablation_seeds": V4_SEEDS, "n_turns": N_TURNS_ABL, "max_cells": MAX_CELLS,
            "snapshot_every": SNAPSHOT_EVERY, "n_div_prompts": N_DIV_PROMPTS,
        },
        "weight_stats_summary": [
            {
                "target": tgt,
                "l2_A": ws["stats"][tgt]["A_phase2_cotrain"]["l2_norm"],
                "l2_B": ws["stats"][tgt]["B_bgla_pretrain"]["l2_norm"],
                "l2_R": ws["stats"][tgt]["R_random_init"]["l2_norm"],
                "effrank_A": ws["stats"][tgt]["A_phase2_cotrain"].get("effective_rank"),
                "effrank_B": ws["stats"][tgt]["B_bgla_pretrain"].get("effective_rank"),
                "effrank_R": ws["stats"][tgt]["R_random_init"].get("effective_rank"),
                "sparsity_lt_001_A": ws["stats"][tgt]["A_phase2_cotrain"]["sparsity_lt_001"],
                "sparsity_lt_001_B": ws["stats"][tgt]["B_bgla_pretrain"]["sparsity_lt_001"],
                "cos_A_vs_B": ws["stats"][tgt]["cos_A_vs_B"],
                "cos_A_vs_R": ws["stats"][tgt]["A_phase2_cotrain"].get("cos_sim_to_baseline"),
                "cos_B_vs_R": ws["stats"][tgt]["B_bgla_pretrain"].get("cos_sim_to_baseline"),
            }
            for tgt in ["cell_pool_init", "c_to_h.weight", "h_to_c.weight"]
        ],
        "diversity_summary": {
            tag: {
                "hm_avg_pairwise_cos": div[tag]["hidden_mean"]["avg_pairwise_cosine"],
                "hm_eff_dim": div[tag]["hidden_mean"]["effective_dim"],
                "c_to_h_avg_pairwise_cos": div[tag]["c_to_h_proj"]["avg_pairwise_cosine"],
                "c_to_h_eff_dim": div[tag]["c_to_h_proj"]["effective_dim"],
            }
            for tag, div in [("A", div_all), ("B", div_all), ("R", div_all)]
        } if False else {
            "A": {
                "hm_avg_pairwise_cos": div_A["hidden_mean"]["avg_pairwise_cosine"],
                "hm_eff_dim": div_A["hidden_mean"]["effective_dim"],
                "c_to_h_avg_pairwise_cos": div_A["c_to_h_proj"]["avg_pairwise_cosine"],
                "c_to_h_eff_dim": div_A["c_to_h_proj"]["effective_dim"],
            },
            "B": {
                "hm_avg_pairwise_cos": div_B["hidden_mean"]["avg_pairwise_cosine"],
                "hm_eff_dim": div_B["hidden_mean"]["effective_dim"],
                "c_to_h_avg_pairwise_cos": div_B["c_to_h_proj"]["avg_pairwise_cosine"],
                "c_to_h_eff_dim": div_B["c_to_h_proj"]["effective_dim"],
            },
            "R": {
                "hm_avg_pairwise_cos": div_R["hidden_mean"]["avg_pairwise_cosine"],
                "hm_eff_dim": div_R["hidden_mean"]["effective_dim"],
                "c_to_h_avg_pairwise_cos": div_R["c_to_h_proj"]["avg_pairwise_cosine"],
                "c_to_h_eff_dim": div_R["c_to_h_proj"]["effective_dim"],
            },
        },
        "ablation_summary": {
            k: {
                "verdict": v["verdict"],
                "trained_iit_un16": v["trained_iit_un16"],
                "mirror_iit_un16_mean": v["mirror_iit_un16_mean"],
                "n_beats_iit_un16": v["n_beats_iit_un16"],
                "n_beats_proxy_phi": v["n_beats_proxy_phi"],
                "n_seeds": v["n_seeds"],
                "trained_n_cells": v["trained_n_cells"],
                "mirror_n_cells": v["mirror_n_cells"],
            } for k, v in abl_results.items()
        },
        "falsifiers": {
            "F1_weight_stats": {"falsified": f1_falsified, "details": diffs},
            "F2_ablation_flip": {"falsified": f2_falsified, "flips": flips, "verdicts": abl_verdicts},
            "F3_fwd_diversity": {
                "falsified": f3_falsified,
                "A_eff_dim": a_eff, "B_eff_dim": b_eff, "A_avg_cos": a_cos, "B_avg_cos": b_cos,
            },
        },
        "final_verdict": final,
        "n_falsifier_passes": n_pass,
    }
    (THIS_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    # verdict.md
    _write_verdict_md(THIS_DIR / "verdict.md", summary, ws, div_all, abl_results)

    log_f.close()
    return summary


def _clone_engine_ag_from(src: EngineAGModel) -> EngineAGModel:
    """Build a fresh model with same cfg, copy weights from src. (Avoids mutating src.)"""
    cfg = src.cfg
    m = EngineAGModel(cfg)
    m.load_state_dict(src.state_dict(), strict=True)
    return m


def _write_verdict_md(path: Path, summary: dict, ws: dict, div_all: dict, abl: dict):
    lines: List[str] = []
    lines.append("# BG-COTRAIN-EXERCISE-CAUSAL-PROOF — verdict\n")
    lines.append(f"**FINAL_VERDICT**: `{summary['final_verdict']}`  "
                 f"(falsifier-pass {summary['n_falsifier_passes']}/3)\n")
    lines.append("## Stream 1 — weight-space statistics\n")
    lines.append("| target | l2_A | l2_B | l2_R | effrank_A | effrank_B | effrank_R | "
                 "sparsity<.01_A | sparsity<.01_B | cos(A,B) | cos(A,R) | cos(B,R) |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for row in summary["weight_stats_summary"]:
        lines.append(
            f"| `{row['target']}` | {row['l2_A']:.4f} | {row['l2_B']:.4f} | {row['l2_R']:.4f} | "
            f"{row['effrank_A']:.2f} | {row['effrank_B']:.2f} | {row['effrank_R']:.2f} | "
            f"{row['sparsity_lt_001_A']:.4f} | {row['sparsity_lt_001_B']:.4f} | "
            f"{row['cos_A_vs_B']:.4f} | {row['cos_A_vs_R']:.4f} | {row['cos_B_vs_R']:.4f} |"
        )
    lines.append("")
    lines.append("## Stream 2 — forward-pass diversity (n=100 prompts)\n")
    lines.append("| substrate | hm_avg_pairwise_cos | hm_eff_dim | c_to_h_avg_cos | c_to_h_eff_dim |")
    lines.append("|---|---|---|---|---|")
    for tag in ["A", "B", "R"]:
        d = summary["diversity_summary"][tag]
        lines.append(f"| {tag} | {d['hm_avg_pairwise_cos']:.4f} | {d['hm_eff_dim']:.2f} | "
                     f"{d['c_to_h_avg_pairwise_cos']:.4f} | {d['c_to_h_eff_dim']:.2f} |")
    lines.append("")
    lines.append(f"## Stream 3 — ablation V14 (n_turns={summary['config']['n_turns']}, seeds={summary['config']['ablation_seeds']})\n")
    lines.append("| condition | verdict | trained Φ_un16 | mirror Φ_un16 mean | beats_un | beats_proxy | trained_cells | mirror_cells |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for k in ["baseline_A", "ABL1_c_to_h_random", "ABL2_h_to_c_random", "ABL3_both_random", "ABL4_cell_pool_random"]:
        v = summary["ablation_summary"][k]
        lines.append(
            f"| {k} | `{v['verdict']}` | {v['trained_iit_un16']:.2f} | {v['mirror_iit_un16_mean']:.2f} | "
            f"{v['n_beats_iit_un16']}/{v['n_seeds']} | {v['n_beats_proxy_phi']}/{v['n_seeds']} | "
            f"{v['trained_n_cells']} | {v['mirror_n_cells']} |"
        )
    lines.append("")
    lines.append("## Falsifiers\n")
    fl = summary["falsifiers"]
    lines.append(f"- **F-COTRAIN-EXERCISE-1** weight-stats: "
                 f"{'FALSIFIED' if fl['F1_weight_stats']['falsified'] else 'PASSED'}")
    lines.append(f"- **F-COTRAIN-EXERCISE-2** ablation-flip: "
                 f"{'FALSIFIED' if fl['F2_ablation_flip']['falsified'] else 'PASSED'} "
                 f"(flips: {fl['F2_ablation_flip']['flips']})")
    lines.append(f"- **F-COTRAIN-EXERCISE-3** fwd-diversity: "
                 f"{'FALSIFIED' if fl['F3_fwd_diversity']['falsified'] else 'PASSED'}")
    lines.append("")
    path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
