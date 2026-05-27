#!/usr/bin/env python3
"""
BG-CELL-POOL-WEIGHT-STATISTICS audit script.

Phase 2 cotrain-exercise hypothesis: chat loss backward pass during cotrain
exercises engine_g.cell_pool_init / c_to_h / h_to_c projections, producing
statistically distinguishable weight signature vs. random_init.

5 ckpts:
  A: Phase 2 cotrain 350M
  B: BG-LA pretrain 350M  (no cotrain)
  C: v2 cells64 (no h_to_c — engine_g is dual-FFN)
  D: v2 cells128
  E: v2 convo_5k FT (extended)

raw#15 additive: in-memory analysis only, no ckpt mutation.
: $0 local CPU.
"""
from __future__ import annotations
import os
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import torch
import numpy as np
from scipy.stats import skew, kurtosis
from scipy.optimize import linear_sum_assignment

CKPT_PATHS = {
    "A_phase2_cotrain_350m": (
        "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
        "model",
    ),
    "B_bg_la_pretrain_350m": (
        "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt",
        "state_dict",
    ),
    "C_v2_cells64": (
        "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt",
        "model_state",
    ),
    "D_v2_cells128": (
        "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells128_step_35000.pt",
        "model_state",
    ),
    "E_v2_convo_5k_ft": (
        "/Users/ghost/core/anima/state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt",
        "model_state",
    ),
}

OUT_DIR = Path("/Users/ghost/core/anima/state/anima_cell_pool_weight_statistics_2026_05_10")

# Tensors to audit per ckpt — focus on cell_pool / c_to_h / h_to_c (where present)
# plus a control set of shared layers.
FOCUS_TENSORS_350M = [
    "engine_g.cell_pool_init",
    "engine_g.h_to_c.weight",
    "engine_g.c_to_h.weight",
]
CONTROL_TENSORS_350M = [
    "tok_emb.weight",
    "layers.0.attn.q_proj.weight",
    "layers.0.ffn.gate.weight",
    "layers.11.attn.q_proj.weight",
    "layers.23.ffn.down.weight",
]
# v2 has no cell_pool / c_to_h / h_to_c — engine_g is dual-FFN
CONTROL_TENSORS_V2 = [
    "tok_emb.weight",
    "blocks.0.attn.c_attn.weight",
    "blocks.0.ffn.engine_a.0.weight",
    "blocks.0.ffn.engine_g.0.weight",
    "blocks.5.ffn.engine_g.3.weight",
]


# -------------------- metric helpers --------------------

def tensor_stats(W: torch.Tensor) -> Dict[str, Any]:
    """Compute 10+ weight-space metrics for a tensor."""
    W = W.detach().to(torch.float32).cpu()
    if W.dim() == 0:
        return {"shape": [], "scalar": float(W.item())}
    if W.dim() > 2:
        # flatten extra dims to 2D for SVD analysis (e.g., causal mask is 4D — skip)
        if W.dim() == 4 and (W.shape[0] == 1 and W.shape[1] == 1):
            return {"shape": list(W.shape), "skipped": "attn_mask_4d"}
        W = W.reshape(W.shape[0], -1)

    flat = W.flatten()
    n = flat.numel()
    abs_flat = flat.abs()

    # basic norms
    l2 = float(flat.norm(p=2).item())
    linf = float(abs_flat.max().item())
    fro = float(W.norm(p="fro").item())  # same as l2 for matrices flattened

    # sparsity at thresholds
    s_001 = float((abs_flat < 1e-3).float().mean().item())
    s_01 = float((abs_flat < 1e-2).float().mean().item())

    # magnitude distribution
    mean = float(flat.mean().item())
    std = float(flat.std().item())
    np_flat = flat.numpy()
    sk = float(skew(np_flat))
    kt = float(kurtosis(np_flat))  # excess kurtosis

    out: Dict[str, Any] = {
        "shape": list(W.shape),
        "numel": n,
        "l2_norm": l2,
        "linf_norm": linf,
        "fro_norm": fro,
        "sparsity_lt_1e-3": s_001,
        "sparsity_lt_1e-2": s_01,
        "mean": mean,
        "std": std,
        "skew": sk,
        "kurtosis": kt,
    }

    if W.dim() == 2:
        # SVD-based metrics
        try:
            # economy SVD; for moderate sizes this is fine on CPU
            # skip very large matrices' full SVD (use truncated for tok_emb 32000x1024)
            m, k = W.shape
            if min(m, k) <= 4096:
                U, S, Vh = torch.linalg.svd(W, full_matrices=False)
                S_np = S.numpy()
            else:
                # truncated top-k via numpy svd on smaller dim
                # For 32000x1024 we want top 1024 singular values
                # Use torch SVD on full matrix (works but expensive); approximate with
                # eigendecomp of W W^T or W^T W (smaller dim).
                small_dim = min(m, k)
                if k <= m:
                    G = (W.T @ W).numpy()  # k x k
                else:
                    G = (W @ W.T).numpy()  # m x m
                eigs = np.linalg.eigvalsh(G)
                eigs = np.sort(eigs)[::-1]
                eigs = np.clip(eigs, 0.0, None)
                S_np = np.sqrt(eigs)
        except Exception as e:
            out["svd_error"] = f"{type(e).__name__}: {e}"
            return out

        S_np = np.asarray(S_np, dtype=np.float64)
        S_np = S_np[S_np > 1e-12]  # drop numerical zeros
        if S_np.size == 0:
            out["svd_empty"] = True
            return out

        spectral = float(S_np[0])
        # stable rank
        stable_rank = float((S_np ** 2).sum() / (S_np[0] ** 2 + 1e-30))
        # effective rank: entropy of normalized squared singular values
        s2 = S_np ** 2
        p = s2 / (s2.sum() + 1e-30)
        p_pos = p[p > 1e-30]
        H = float(-(p_pos * np.log(p_pos)).sum())
        eff_rank = float(np.exp(H))
        # top-10 + cumulative variance
        topk = min(10, S_np.size)
        top_sv = S_np[:topk].tolist()
        cum_var = float(s2[:topk].sum() / (s2.sum() + 1e-30))
        # Marchenko-Pastur: for an mxk random matrix with i.i.d. entries var=sigma^2,
        # the singular values' squared distribution (eigvals of W^T W / m) follows MP
        # with c = k/m. Compare empirical bulk edge vs MP upper edge sigma^2*(1+sqrt(c))^2.
        m_, k_ = W.shape
        c = min(m_, k_) / max(m_, k_)
        sigma_emp = float(np.sqrt((W.numpy() ** 2).mean()))  # entrywise stdev (assumes mean~0)
        mp_upper = sigma_emp * (1.0 + math.sqrt(c)) * math.sqrt(max(m_, k_))
        # We expect random-like matrix to have spectral norm ~ mp_upper
        mp_ratio = float(spectral / (mp_upper + 1e-30))

        out.update({
            "spectral_norm": spectral,
            "stable_rank": stable_rank,
            "effective_rank": eff_rank,
            "top10_sv": top_sv,
            "cum_var_top10": cum_var,
            "mp_sigma_emp": sigma_emp,
            "mp_upper_pred": mp_upper,
            "mp_spectral_ratio": mp_ratio,
        })
    return out


def cosine_sim(a: torch.Tensor, b: torch.Tensor) -> float:
    a = a.detach().to(torch.float32).cpu().flatten()
    b = b.detach().to(torch.float32).cpu().flatten()
    if a.numel() != b.numel():
        return float("nan")
    na = a.norm()
    nb = b.norm()
    if na < 1e-30 or nb < 1e-30:
        return 0.0
    return float((a @ b / (na * nb)).item())


def per_row_cosine(a: torch.Tensor, b: torch.Tensor) -> Tuple[float, float, float]:
    """Per-row cosine similarity stats (mean, std, median)."""
    a = a.detach().to(torch.float32).cpu()
    b = b.detach().to(torch.float32).cpu()
    if a.shape != b.shape:
        return (float("nan"),) * 3
    if a.dim() == 1:
        return (cosine_sim(a, b), 0.0, cosine_sim(a, b))
    a2 = a.reshape(a.shape[0], -1)
    b2 = b.reshape(b.shape[0], -1)
    na = a2.norm(dim=1, keepdim=True).clamp_min(1e-30)
    nb = b2.norm(dim=1, keepdim=True).clamp_min(1e-30)
    cs = (a2 / na * b2 / nb).sum(dim=1).numpy()
    return float(cs.mean()), float(cs.std()), float(np.median(cs))


# -------------------- random init baseline --------------------

def random_init_like(t: torch.Tensor, std: float, seed: int) -> torch.Tensor:
    g = torch.Generator()
    g.manual_seed(seed)
    return torch.randn(t.shape, generator=g, dtype=torch.float32) * std


def random_baseline_stats(shape: List[int], std: float, n_seeds: int = 5) -> Dict[str, Any]:
    """Compute baseline statistics over multiple random seeds (median + IQR)."""
    seeds = [42, 137, 271, 314, 1729][:n_seeds]
    rows: List[Dict[str, float]] = []
    keep_keys = [
        "l2_norm", "linf_norm", "fro_norm",
        "sparsity_lt_1e-3", "sparsity_lt_1e-2",
        "mean", "std", "skew", "kurtosis",
        "spectral_norm", "stable_rank", "effective_rank",
        "cum_var_top10", "mp_sigma_emp", "mp_upper_pred",
        "mp_spectral_ratio",
    ]
    for s in seeds:
        g = torch.Generator()
        g.manual_seed(s)
        if len(shape) == 1:
            T = torch.randn(shape, generator=g, dtype=torch.float32) * std
        else:
            T = torch.randn(shape, generator=g, dtype=torch.float32) * std
        st = tensor_stats(T)
        rows.append({k: st.get(k, float("nan")) for k in keep_keys if k in st})
    # aggregate (median, p25, p75)
    out: Dict[str, Any] = {"n_seeds": n_seeds, "seeds": seeds, "shape": shape, "init_std": std}
    for k in keep_keys:
        vals = [r[k] for r in rows if k in r and not (isinstance(r[k], float) and math.isnan(r[k]))]
        if vals:
            arr = np.asarray(vals)
            out[f"{k}_median"] = float(np.median(arr))
            out[f"{k}_p25"] = float(np.percentile(arr, 25))
            out[f"{k}_p75"] = float(np.percentile(arr, 75))
    return out


# -------------------- ckpt loader --------------------

def load_state_dict(path: str, sd_key: Optional[str]) -> Dict[str, torch.Tensor]:
    obj = torch.load(path, map_location="cpu", weights_only=False)
    if isinstance(obj, dict) and sd_key and sd_key in obj:
        return obj[sd_key]
    return obj  # already a state_dict


# -------------------- cross-substrate alignment --------------------

def cell_pool_alignment(A: torch.Tensor, B: torch.Tensor) -> Dict[str, Any]:
    """A vs B cell_pool alignment — Hungarian assignment + similarity stats."""
    A = A.detach().to(torch.float32).cpu().numpy()
    B = B.detach().to(torch.float32).cpu().numpy()
    if A.shape != B.shape:
        return {"error": f"shape mismatch {A.shape} vs {B.shape}"}
    n_cells, dim = A.shape
    # row-normalized cosine similarity matrix
    An = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-30)
    Bn = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-30)
    sim = An @ Bn.T  # n x n
    # raw diagonal (cell-i to cell-i correspondence)
    diag = np.diag(sim).copy()
    # Hungarian: maximize total similarity
    row_ind, col_ind = linear_sum_assignment(-sim)
    matched = sim[row_ind, col_ind]
    # entropy of A and B cell distributions (using cell norms)
    norms_A = np.linalg.norm(A, axis=1)
    norms_B = np.linalg.norm(B, axis=1)
    pA = norms_A / (norms_A.sum() + 1e-30)
    pB = norms_B / (norms_B.sum() + 1e-30)
    H_A = float(-(pA * np.log(pA + 1e-30)).sum())
    H_B = float(-(pB * np.log(pB + 1e-30)).sum())
    # cell-cell variance
    var_A = float(np.var(norms_A))
    var_B = float(np.var(norms_B))
    # gram matrix off-diagonal — measures how "spread out" cells are
    GA = An @ An.T
    GB = Bn @ Bn.T
    off_A = (GA - np.eye(n_cells))
    off_B = (GB - np.eye(n_cells))
    mean_off_A = float(np.abs(off_A).sum() / (n_cells * (n_cells - 1)))
    mean_off_B = float(np.abs(off_B).sum() / (n_cells * (n_cells - 1)))
    return {
        "n_cells": int(n_cells),
        "dim": int(dim),
        "diag_cosine_mean": float(diag.mean()),
        "diag_cosine_std": float(diag.std()),
        "diag_cosine_min": float(diag.min()),
        "diag_cosine_max": float(diag.max()),
        "hungarian_matched_mean": float(matched.mean()),
        "hungarian_total": float(matched.sum()),
        "hungarian_assignment": col_ind.tolist(),
        "cell_norm_entropy_A": H_A,
        "cell_norm_entropy_B": H_B,
        "cell_norm_var_A": var_A,
        "cell_norm_var_B": var_B,
        "gram_offdiag_abs_mean_A": mean_off_A,
        "gram_offdiag_abs_mean_B": mean_off_B,
    }


# -------------------- main --------------------

def audit_one(name: str, path: str, sd_key: str) -> Dict[str, Any]:
    print(f"[audit] loading {name} from {path}")
    sd = load_state_dict(path, sd_key)
    out: Dict[str, Any] = {"name": name, "path": path, "sd_key": sd_key}

    # decide tensor list per arch
    if "350m" in name.lower() or "phase2" in name.lower() or "bg_la" in name.lower():
        focus = FOCUS_TENSORS_350M
        ctrl = CONTROL_TENSORS_350M
    else:
        focus = []
        ctrl = CONTROL_TENSORS_V2

    out["focus_tensors"] = {}
    for k in focus:
        if k in sd:
            out["focus_tensors"][k] = tensor_stats(sd[k])
        else:
            out["focus_tensors"][k] = {"missing": True}

    out["control_tensors"] = {}
    for k in ctrl:
        if k in sd:
            out["control_tensors"][k] = tensor_stats(sd[k])
        else:
            out["control_tensors"][k] = {"missing": True}

    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: audit each ckpt
    per_ckpt: Dict[str, Any] = {}
    sds: Dict[str, Dict[str, torch.Tensor]] = {}
    for name, (path, sd_key) in CKPT_PATHS.items():
        per_ckpt[name] = audit_one(name, path, sd_key)
        sds[name] = load_state_dict(path, sd_key)

    # Step 2: random init baselines for the focus tensors (350M only — v2 has none)
    print("[audit] computing random baselines (init_std=0.02, 5 seeds)")
    baselines: Dict[str, Any] = {}
    init_std = 0.02
    for k in FOCUS_TENSORS_350M:
        if k in sds["A_phase2_cotrain_350m"]:
            shape = list(sds["A_phase2_cotrain_350m"][k].shape)
            baselines[k] = random_baseline_stats(shape, init_std, n_seeds=5)

    # Step 3: cosine similarity to random_init baseline (single seed=42 for shape match)
    print("[audit] cosine similarity to random_init seed=42")
    cos_to_rnd: Dict[str, Dict[str, Any]] = {}
    for ckpt_name in ["A_phase2_cotrain_350m", "B_bg_la_pretrain_350m"]:
        cos_to_rnd[ckpt_name] = {}
        for k in FOCUS_TENSORS_350M + CONTROL_TENSORS_350M:
            if k not in sds[ckpt_name]:
                continue
            t = sds[ckpt_name][k]
            r = random_init_like(t, init_std, seed=42)
            global_cos = cosine_sim(t, r)
            row_mean, row_std, row_med = per_row_cosine(t, r)
            cos_to_rnd[ckpt_name][k] = {
                "global_cosine": global_cos,
                "row_cosine_mean": row_mean,
                "row_cosine_std": row_std,
                "row_cosine_median": row_med,
            }

    # Step 4: cross-substrate alignment A vs B (cell_pool, c_to_h, h_to_c)
    print("[audit] A vs B cross-substrate alignment")
    align: Dict[str, Any] = {}
    for k in FOCUS_TENSORS_350M:
        a_t = sds["A_phase2_cotrain_350m"].get(k)
        b_t = sds["B_bg_la_pretrain_350m"].get(k)
        if a_t is None or b_t is None:
            align[k] = {"missing": True}
            continue
        align[k] = {
            "global_cosine": cosine_sim(a_t, b_t),
            "row_cosine": dict(zip(["mean", "std", "median"], per_row_cosine(a_t, b_t))),
            "l2_diff": float((a_t.float() - b_t.float()).norm().item()),
            "fro_normalized_diff": float(
                (a_t.float() - b_t.float()).norm().item()
                / (a_t.float().norm().item() + 1e-30)
            ),
        }
        # cell_pool specific Hungarian alignment
        if k == "engine_g.cell_pool_init":
            align[k]["cell_pool_alignment"] = cell_pool_alignment(a_t, b_t)

    # Step 5: also v2 path — A's cell_pool stats vs random baselines (effective rank etc.)
    # already covered in per_ckpt + baselines

    # Save
    out_per_ckpt = {
        "schema": "bg_cell_pool_weight_statistics/v1",
        "ts": "2026-05-10",
        "per_ckpt": per_ckpt,
        "random_baselines": baselines,
        "cosine_to_random_init": cos_to_rnd,
    }
    (OUT_DIR / "statistics_per_ckpt.json").write_text(
        json.dumps(out_per_ckpt, indent=2, default=str)
    )
    (OUT_DIR / "cross_substrate_alignment.json").write_text(
        json.dumps({"schema": "bg_cell_pool_align/v1", "alignment": align}, indent=2, default=str)
    )
    print(f"[audit] DONE. Wrote outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
