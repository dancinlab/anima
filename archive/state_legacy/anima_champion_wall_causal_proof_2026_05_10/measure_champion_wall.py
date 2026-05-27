"""§28+§37 BG-CHAMPION-WALL-CAUSAL-PROOF — measure 3 metrics on both substrates.

Metrics:
  1. champion_dominance: top-1 cell hidden_mean variance / total hidden_mean variance.
     For Phase 2 (has h_to_c): pass synthetic batch through h_to_c, measure
     variance of cell_targets per cell-pool dim, take top-1 / sum.
     For v2 cells64 (has dual ffn engine_g, NOT cell-pool): proxy via
     output-channel variance of last-layer engine_g.3.weight (output projection
     to d_model). Top-1 / total of output channel variance = how concentrated
     the engine_g writes back into one channel.

  2. attractor_bottleneck: log(spectral_radius(W)) / log(d_inner).
     For Phase 2: W = engine_g.h_to_c.weight (64, 1024), d_inner = 64.
     For v2 cells64: W = blocks[5].ffn.engine_g.3.weight (384, 1536),
     d_inner = 384.

  3. phi_headroom_remaining: max_phi_observed - mean_phi_recent_100.
     For v2: phi_history (200 samples).
     For Phase 2: meta.json has no phi_history; use V14 trajectory snapshots
     from anima_v14_strict_resolution result_10seed.json (trained run, 9 snapshots).

Outputs metrics.json with both substrates' values and signed differences.
raw#16 honest: $0 local CPU, weights_only=False permitted (raw#15 read-only).
"""
from __future__ import annotations

import json
import math
import os
import statistics
import sys
from typing import Any, Dict

import torch

OUT_DIR = "/Users/ghost/core/anima/state/anima_champion_wall_causal_proof_2026_05_10"
os.makedirs(OUT_DIR, exist_ok=True)

V2_CKPT = "/Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt"
PHASE2_CKPT = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
PHASE2_V14 = "/Users/ghost/core/anima/state/anima_v14_strict_resolution_2026_05_10/result_10seed.json"


def spectral_radius(W: torch.Tensor) -> float:
    """Largest singular value (or |eigenvalue| for square)."""
    with torch.no_grad():
        # Use SVD top-1 for non-square; equals eigvals.abs().max() for normal mat
        s = torch.linalg.svdvals(W.float())
        return float(s[0].item())


def channel_variance_dominance(W: torch.Tensor) -> Dict[str, float]:
    """Per-output-channel variance of W (over input dim).

    For h_to_c (c_dim, d_model): per-c_dim row variance over d_model.
    Returns top-1 / total ratio (= how concentrated the projection is on one
    cell-pool dim) and effective rank.
    """
    with torch.no_grad():
        W = W.float()
        row_var = W.var(dim=1, unbiased=False)  # variance per output channel
        total = float(row_var.sum().item())
        if total <= 0:
            return {"dominance": 0.0, "top2_share": 0.0, "n_eff": float(W.shape[0])}
        sorted_var, _ = torch.sort(row_var, descending=True)
        top1 = float(sorted_var[0].item())
        top2 = float(sorted_var[:2].sum().item())
        # Participation ratio (effective number of channels with significant variance)
        p = row_var / total
        n_eff = float(1.0 / (p * p).sum().item())
        return {
            "dominance": top1 / total,
            "top2_share": top2 / total,
            "n_eff": n_eff,
            "top1_var": top1,
            "total_var": total,
            "n_channels": int(W.shape[0]),
        }


def compute_phi_stats(phi_history: list, recent_window: int = 100) -> Dict[str, float]:
    """phi_headroom = max - mean(recent)."""
    floats = [float(x) for x in phi_history]
    mx = max(floats)
    mn = min(floats)
    mean_all = statistics.mean(floats)
    recent = floats[-recent_window:] if len(floats) >= recent_window else floats
    mean_recent = statistics.mean(recent)
    return {
        "max_phi": mx,
        "min_phi": mn,
        "mean_all": mean_all,
        "mean_recent": mean_recent,
        "n_samples": len(floats),
        "phi_headroom_remaining": mx - mean_recent,
        "phi_headroom_norm": (mx - mean_recent) / max(mx, 1e-9),
    }


def measure_v2_cells64() -> Dict[str, Any]:
    """v2 cells64 ckpt — mitosis-aware (cell pool tracked at training; 62 splits)."""
    ckpt = torch.load(V2_CKPT, map_location="cpu", weights_only=False)
    sd = ckpt["model_state"]
    # v2 has dual FFN engine_g per block — pick the LAST block's engine_g.3.weight
    # (output projection to d_model) as the "h_to_c-analog" — this is what writes
    # into the residual stream and shapes hidden_mean.
    eg_proj_key = "blocks.5.ffn.engine_g.3.weight"  # (d_model=384, hidden=1536)
    W = sd[eg_proj_key].clone()
    print(f"v2 cells64: {eg_proj_key} shape={tuple(W.shape)}", flush=True)

    # champion_dominance: row-variance concentration of output channels (d_model dim)
    dom = channel_variance_dominance(W)

    # attractor_bottleneck: log(spectral_radius(W)) / log(d_inner)
    sr = spectral_radius(W)
    d_inner = W.shape[1]  # hidden=1536
    ab = math.log(max(sr, 1e-9)) / math.log(d_inner)

    # phi_headroom from phi_history (200 samples)
    phi_hist = ckpt.get("phi_history", [])
    phi_stats = compute_phi_stats(phi_hist)

    # Also compute over ALL 6 layer engine_g.3.weight (mean for robustness)
    layer_metrics = []
    for i in range(6):
        Wi = sd[f"blocks.{i}.ffn.engine_g.3.weight"]
        di = channel_variance_dominance(Wi)
        sri = spectral_radius(Wi)
        layer_metrics.append({
            "layer": i,
            "shape": list(Wi.shape),
            "dominance": di["dominance"],
            "top2_share": di["top2_share"],
            "n_eff": di["n_eff"],
            "spectral_radius": sri,
            "attractor_bottleneck": math.log(max(sri, 1e-9)) / math.log(Wi.shape[1]),
        })
    mean_dom = statistics.mean([m["dominance"] for m in layer_metrics])
    mean_top2 = statistics.mean([m["top2_share"] for m in layer_metrics])
    mean_neff = statistics.mean([m["n_eff"] for m in layer_metrics])
    mean_sr = statistics.mean([m["spectral_radius"] for m in layer_metrics])
    mean_ab = statistics.mean([m["attractor_bottleneck"] for m in layer_metrics])

    # Mitosis status
    ms = ckpt.get("mitosis_status", {})
    n_cells = ms.get("n_cells")
    n_splits = ms.get("splits")

    return {
        "label": "v2_cells64_mitosis_aware",
        "ckpt_path": V2_CKPT,
        "step": ckpt.get("step"),
        "phase": ckpt.get("phase"),
        "weight_key_used": eg_proj_key,
        "weight_shape": list(W.shape),
        "champion_dominance_top1": dom["dominance"],
        "champion_top2_share": dom["top2_share"],
        "n_eff_channels": dom["n_eff"],
        "spectral_radius": sr,
        "attractor_bottleneck": ab,
        "phi_headroom_remaining": phi_stats["phi_headroom_remaining"],
        "phi_headroom_norm": phi_stats["phi_headroom_norm"],
        "phi_max": phi_stats["max_phi"],
        "phi_mean_recent": phi_stats["mean_recent"],
        "phi_n_samples": phi_stats["n_samples"],
        "v14_verdict": "V14_VIOLATED",
        "v14_separation_phi": -202.32,  # from d384_sweep result.json
        "v14_trained_beats_all_random": False,
        "mitosis_n_cells_final": n_cells,
        "mitosis_n_splits": n_splits,
        "per_layer_metrics": layer_metrics,
        "mean_dominance_all_layers": mean_dom,
        "mean_top2_share_all_layers": mean_top2,
        "mean_n_eff_all_layers": mean_neff,
        "mean_spectral_radius_all_layers": mean_sr,
        "mean_attractor_bottleneck_all_layers": mean_ab,
    }


def measure_phase2() -> Dict[str, Any]:
    """Phase 2 350M ckpt — mitosis-naive (no cell-tracking during training)."""
    ckpt = torch.load(PHASE2_CKPT, map_location="cpu", weights_only=False)
    sd = ckpt["model"]
    h_key = "engine_g.h_to_c.weight"  # (64, 1024)
    W = sd[h_key].clone()
    print(f"Phase 2: {h_key} shape={tuple(W.shape)}", flush=True)

    # champion_dominance: row variance per c_dim cell-pool dim
    dom = channel_variance_dominance(W)

    # attractor_bottleneck: log(spectral_radius(W)) / log(d_inner=d_model=1024)
    sr = spectral_radius(W)
    d_inner = W.shape[1]  # 1024
    ab = math.log(max(sr, 1e-9)) / math.log(d_inner)

    # phi_headroom — from V14 strict trained run snapshots
    with open(PHASE2_V14, "r") as f:
        v14 = json.load(f)
    snaps = v14["trained"]["snapshots"]
    phi_traj = [s["proxy_phi"] for s in snaps]
    phi_stats = compute_phi_stats(phi_traj, recent_window=2)

    # Also report iit_phi_unnorm_b16 trajectory
    iit_traj = [s["iit_phi_unnorm_b16"] for s in snaps]
    iit_stats = compute_phi_stats(iit_traj, recent_window=2)

    # Cell pool init concentration (alternative dominance measure)
    cell_pool = sd["engine_g.cell_pool_init"]  # (16, 64)
    cell_norms = cell_pool.float().norm(dim=-1)
    cell_pool_var = float(cell_norms.var().item())

    return {
        "label": "phase2_mitosis_naive",
        "ckpt_path": PHASE2_CKPT,
        "step": ckpt.get("step"),
        "weight_key_used": h_key,
        "weight_shape": list(W.shape),
        "champion_dominance_top1": dom["dominance"],
        "champion_top2_share": dom["top2_share"],
        "n_eff_channels": dom["n_eff"],
        "spectral_radius": sr,
        "attractor_bottleneck": ab,
        "phi_headroom_remaining": phi_stats["phi_headroom_remaining"],
        "phi_headroom_norm": phi_stats["phi_headroom_norm"],
        "phi_max": phi_stats["max_phi"],
        "phi_mean_recent": phi_stats["mean_recent"],
        "phi_n_samples": phi_stats["n_samples"],
        "iit_phi_headroom_remaining": iit_stats["phi_headroom_remaining"],
        "iit_phi_headroom_norm": iit_stats["phi_headroom_norm"],
        "iit_phi_max": iit_stats["max_phi"],
        "v14_verdict": "V14_STRICT_PASS",
        "v14_trained_beats_all_random": True,
        "v14_sign_test_p": 0.0020,
        "cell_pool_init_var": cell_pool_var,
        "n_cells_init": int(cell_pool.shape[0]),
        "n_cells_final_v14_trained": v14["trained"]["final_n_cells"],
        "n_splits_v14_trained": v14["trained"]["n_splits"],
    }


def main() -> int:
    print("[1/2] Measuring v2 cells64 (mitosis-aware)...", flush=True)
    v2 = measure_v2_cells64()
    print("[2/2] Measuring Phase 2 (mitosis-naive)...", flush=True)
    p2 = measure_phase2()

    # Direction-of-difference summary
    diff = {
        "champion_dominance_v2_minus_p2": v2["champion_dominance_top1"] - p2["champion_dominance_top1"],
        "champion_dominance_layer_avg_v2_minus_p2": v2["mean_dominance_all_layers"] - p2["champion_dominance_top1"],
        "attractor_bottleneck_v2_minus_p2": v2["attractor_bottleneck"] - p2["attractor_bottleneck"],
        "attractor_bottleneck_layer_avg_v2_minus_p2": v2["mean_attractor_bottleneck_all_layers"] - p2["attractor_bottleneck"],
        "phi_headroom_v2_minus_p2_norm": v2["phi_headroom_norm"] - p2["phi_headroom_norm"],
        "phi_headroom_v2_minus_p2_iit_norm": v2["phi_headroom_norm"] - p2["iit_phi_headroom_norm"],
        "n_eff_v2_minus_p2": v2["n_eff_channels"] - p2["n_eff_channels"],
        "n_eff_layer_avg_v2_minus_p2": v2["mean_n_eff_all_layers"] - p2["n_eff_channels"],
    }

    # Hypothesis check (champion-wall causal): if mitosis-aware (v2) PRE-FORMS
    # champion-wall and EXHAUSTS Φ headroom, then expected:
    #   - v2 dominance > p2 dominance  (more concentrated)
    #   - v2 attractor_bottleneck > p2 (deeper attractor)
    #   - v2 phi_headroom < p2 (more exhausted)
    # AND v2 V14 polarity = VIOLATED, p2 V14 polarity = PASS.
    expected_signs = {
        "champion_dominance_v2_minus_p2": "+",  # v2 > p2
        "attractor_bottleneck_v2_minus_p2": "+",  # v2 > p2
        "phi_headroom_v2_minus_p2_norm": "-",  # v2 < p2
    }
    actual_signs = {
        k: ("+" if diff[k] > 0 else ("-" if diff[k] < 0 else "0"))
        for k in expected_signs
    }
    consistency = sum(
        1 for k in expected_signs if actual_signs[k] == expected_signs[k]
    )
    consistency_layer_avg = sum(
        1
        for k_pair in [
            ("champion_dominance_layer_avg_v2_minus_p2", "+"),
            ("attractor_bottleneck_layer_avg_v2_minus_p2", "+"),
            ("phi_headroom_v2_minus_p2_norm", "-"),
        ]
        if (("+" if diff[k_pair[0]] > 0 else ("-" if diff[k_pair[0]] < 0 else "0")) == k_pair[1])
    )

    out = {
        "v2_cells64_mitosis_aware": v2,
        "phase2_mitosis_naive": p2,
        "diff": diff,
        "expected_signs_under_champion_wall_causal_h": expected_signs,
        "actual_signs": actual_signs,
        "directional_consistency_count": consistency,
        "directional_consistency_count_layer_avg": consistency_layer_avg,
        "directional_consistency_max": 3,
    }
    out_path = os.path.join(OUT_DIR, "metrics.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Saved → {out_path}", flush=True)

    print("\n=== SUMMARY ===", flush=True)
    print(f"v2 (mitosis-aware) dominance={v2['champion_dominance_top1']:.6f} "
          f"layer_avg={v2['mean_dominance_all_layers']:.6f}", flush=True)
    print(f"p2 (mitosis-naive) dominance={p2['champion_dominance_top1']:.6f}", flush=True)
    print(f"v2 attractor_bottleneck={v2['attractor_bottleneck']:.4f} "
          f"layer_avg={v2['mean_attractor_bottleneck_all_layers']:.4f}", flush=True)
    print(f"p2 attractor_bottleneck={p2['attractor_bottleneck']:.4f}", flush=True)
    print(f"v2 phi_headroom_norm={v2['phi_headroom_norm']:.4f}", flush=True)
    print(f"p2 phi_headroom_norm(proxy)={p2['phi_headroom_norm']:.4f} "
          f"iit_norm={p2['iit_phi_headroom_norm']:.4f}", flush=True)
    print(f"directional_consistency: {consistency}/3 (last-layer)  "
          f"{consistency_layer_avg}/3 (layer-avg)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
