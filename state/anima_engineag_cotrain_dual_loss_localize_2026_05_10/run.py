#!/usr/bin/env python3
"""
BG-ENGINEAG-COTRAIN-DUAL-LOSS-LOCALIZE — component-level diff analyzer

§57 promoted §50 to PROVEN-AT-BODY-LOCUS at slab granularity (3 slabs of 8
layers).  This BG drills one level deeper: 24 layers × 9 components per layer
= 216 measurements.  Substrate A = Phase 2 cotrain (BG-LB pretrain → chat
dual-loss curriculum w=0.3→0.5).  Substrate B = BG-LA persona-only pretrain.
For each (layer, component) pair we compute, on the bf16-cast tensors loaded
read-only into memory:

    L2(A), L2(B), cos(A,B), L2(A-B), relative_l2 = L2(A-B)/L2(A),
    effective_rank(A), effective_rank(B), sparsity (|w|<1e-4 fraction),
    delta_singular_value_l1.

Constraints honoured:
- raw#9   training/*.py local-only — this script lives under state/, gitignored.
- raw#15  ckpts loaded read-only via torch.load + .clone(); no file mutation.
- own 16  $0 local CPU; both ckpts are 350M bf16 ≈ 600MB each, comfortably
          within free RAM (≈2GB free at start).
- own 22  every metric scalar emitted to JSON.
- own 38  artefacts under
          state/anima_engineag_cotrain_dual_loss_localize_2026_05_10/
          {spec.md, component_metrics.json, heatmap_table.md, verdict.md}.

The analysis is pure numpy/torch on the weight tensors — no model forward,
no training, no GPU.  Wall-clock ~1-2 min on Mac CPU.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch

# ─── paths (own 38) ────────────────────────────────────────────────
ANIMA = "/Users/ghost/core/anima"
OUT_DIR = Path(f"{ANIMA}/state/anima_engineag_cotrain_dual_loss_localize_2026_05_10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CKPT_A = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_B = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt"

N_LAYERS = 24
COMPONENTS = [
    "norm1.weight",
    "attn.q_proj.weight",
    "attn.k_proj.weight",
    "attn.v_proj.weight",
    "attn.o_proj.weight",
    "norm2.weight",
    "ffn.gate.weight",
    "ffn.up.weight",
    "ffn.down.weight",
]
SLABS = {
    "slab1_early":  list(range(0, 8)),
    "slab2_middle": list(range(8, 16)),
    "slab3_late":   list(range(16, 24)),
}


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)


def load_state_dict(ckpt_path: str) -> dict:
    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    if "model" in payload:
        return payload["model"]
    if "state_dict" in payload:
        return payload["state_dict"]
    return payload


def effective_rank(W: torch.Tensor) -> float:
    """Stable-rank proxy via normalized singular-value entropy.
    For 1D tensors (norms) returns 1.0 by definition.
    """
    if W.dim() == 1:
        return 1.0
    Wf = W.float()
    try:
        s = torch.linalg.svdvals(Wf)
    except Exception:
        # fallback via SVD
        _, s, _ = torch.linalg.svd(Wf, full_matrices=False)
    s = s[s > 0]
    if s.numel() == 0:
        return 0.0
    p = s / s.sum()
    H = -(p * torch.log(p + 1e-30)).sum().item()
    return float(torch.exp(torch.tensor(H)).item())


def sparsity(W: torch.Tensor, thresh: float = 1e-4) -> float:
    return float((W.float().abs() < thresh).float().mean().item())


def cosine(a: torch.Tensor, b: torch.Tensor) -> float:
    af = a.float().flatten()
    bf = b.float().flatten()
    na = af.norm()
    nb = bf.norm()
    if na == 0 or nb == 0:
        return 0.0
    return float((af @ bf / (na * nb)).item())


def l2(a: torch.Tensor) -> float:
    return float(a.float().flatten().norm().item())


def singular_value_l1_diff(A: torch.Tensor, B: torch.Tensor) -> float:
    if A.dim() == 1:
        return float((A.float() - B.float()).abs().sum().item())
    sa = torch.linalg.svdvals(A.float())
    sb = torch.linalg.svdvals(B.float())
    n = min(sa.numel(), sb.numel())
    return float((sa[:n] - sb[:n]).abs().sum().item())


def main() -> None:
    t0 = time.time()
    log("loading A (Phase 2 cotrain)")
    sd_a = load_state_dict(CKPT_A)
    log(f"  A: {len(sd_a)} tensors loaded, {time.time()-t0:.1f}s")

    log("loading B (BG-LA pretrain)")
    sd_b = load_state_dict(CKPT_B)
    log(f"  B: {len(sd_b)} tensors loaded, {time.time()-t0:.1f}s")

    # sanity: are tok_emb shared structurally?
    assert sd_a["tok_emb.weight"].shape == sd_b["tok_emb.weight"].shape, "vocab mismatch"

    # ─── per-(layer, component) ─────────────────────────────────────
    results = {
        "meta": {
            "ckpt_A": CKPT_A,
            "ckpt_B": CKPT_B,
            "n_layers": N_LAYERS,
            "components": COMPONENTS,
            "dtype": str(next(iter(sd_a.values())).dtype),
            "started_at": datetime.now(timezone.utc).isoformat(),
        },
        "per_pair": [],   # flat list of dicts
        "per_component_aggregate": {},
        "per_layer_aggregate": {},
        "per_slab_aggregate": {},
        "global_extras": {},
    }

    log("computing per-(layer, component) metrics")
    for li in range(N_LAYERS):
        for cname in COMPONENTS:
            fq = f"layers.{li}.{cname}"
            A = sd_a[fq]
            B = sd_b[fq]
            assert A.shape == B.shape, f"shape mismatch {fq}"
            l2_a = l2(A)
            l2_b = l2(B)
            l2_diff = l2(A - B)
            cos_ab = cosine(A, B)
            rel_l2 = l2_diff / (l2_a + 1e-12)
            er_a = effective_rank(A)
            er_b = effective_rank(B)
            sp_a = sparsity(A)
            sp_b = sparsity(B)
            try:
                sv_l1 = singular_value_l1_diff(A, B)
            except Exception as e:
                sv_l1 = float("nan")
            results["per_pair"].append({
                "layer": li,
                "component": cname,
                "shape": list(A.shape),
                "n_params": int(A.numel()),
                "l2_A": l2_a,
                "l2_B": l2_b,
                "l2_diff": l2_diff,
                "cos_AB": cos_ab,
                "relative_l2_diff": rel_l2,
                "effective_rank_A": er_a,
                "effective_rank_B": er_b,
                "sparsity_A": sp_a,
                "sparsity_B": sp_b,
                "singular_value_l1_diff": sv_l1,
            })
        log(f"  layer {li:2d}: done ({time.time()-t0:.1f}s)")

    # ─── per-component aggregate (mean across 24 layers) ────────────
    log("computing aggregates")
    for cname in COMPONENTS:
        rows = [r for r in results["per_pair"] if r["component"] == cname]
        results["per_component_aggregate"][cname] = {
            "n_layers": len(rows),
            "mean_cos_AB": sum(r["cos_AB"] for r in rows) / len(rows),
            "min_cos_AB": min(r["cos_AB"] for r in rows),
            "max_cos_AB": max(r["cos_AB"] for r in rows),
            "mean_relative_l2_diff": sum(r["relative_l2_diff"] for r in rows) / len(rows),
            "mean_l2_diff": sum(r["l2_diff"] for r in rows) / len(rows),
            "mean_effective_rank_A": sum(r["effective_rank_A"] for r in rows) / len(rows),
            "mean_effective_rank_B": sum(r["effective_rank_B"] for r in rows) / len(rows),
            "mean_sparsity_A": sum(r["sparsity_A"] for r in rows) / len(rows),
            "mean_sparsity_B": sum(r["sparsity_B"] for r in rows) / len(rows),
            "total_params_per_layer": rows[0]["n_params"],
        }

    # ─── per-layer aggregate (mean across 9 components within layer) ─
    for li in range(N_LAYERS):
        rows = [r for r in results["per_pair"] if r["layer"] == li]
        wsum_cos = sum(r["cos_AB"] * r["n_params"] for r in rows)
        wsum_n = sum(r["n_params"] for r in rows)
        results["per_layer_aggregate"][f"layer_{li:02d}"] = {
            "n_components": len(rows),
            "mean_cos_AB": sum(r["cos_AB"] for r in rows) / len(rows),
            "param_weighted_cos_AB": wsum_cos / wsum_n,
            "mean_relative_l2_diff": sum(r["relative_l2_diff"] for r in rows) / len(rows),
            "n_params": wsum_n,
        }

    # ─── per-slab aggregate (mean across 8 layers × 9 components) ────
    for slab_name, lis in SLABS.items():
        rows = [r for r in results["per_pair"] if r["layer"] in lis]
        per_comp = {}
        for cname in COMPONENTS:
            cr = [r for r in rows if r["component"] == cname]
            per_comp[cname] = {
                "mean_cos_AB": sum(r["cos_AB"] for r in cr) / len(cr),
                "mean_relative_l2_diff": sum(r["relative_l2_diff"] for r in cr) / len(cr),
            }
        results["per_slab_aggregate"][slab_name] = {
            "layers": lis,
            "mean_cos_AB": sum(r["cos_AB"] for r in rows) / len(rows),
            "mean_relative_l2_diff": sum(r["relative_l2_diff"] for r in rows) / len(rows),
            "per_component": per_comp,
        }

    # ─── global extras: tok_emb / norm_f / lm_head ──────────────────
    log("global extras (tok_emb, norm_f, lm_head)")
    for k in ["tok_emb.weight", "norm_f.weight", "lm_head.weight"]:
        if k in sd_a and k in sd_b:
            A = sd_a[k]
            B = sd_b[k]
            results["global_extras"][k] = {
                "shape": list(A.shape),
                "cos_AB": cosine(A, B),
                "l2_A": l2(A),
                "l2_B": l2(B),
                "relative_l2_diff": l2(A - B) / (l2(A) + 1e-12),
            }

    results["meta"]["elapsed_s"] = time.time() - t0

    # ─── emit ────────────────────────────────────────────────────────
    out_json = OUT_DIR / "component_metrics.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    log(f"wrote {out_json} ({out_json.stat().st_size/1024:.1f} KB)")

    # ─── emit heatmap_table.md ──────────────────────────────────────
    log("rendering heatmap_table.md")
    lines = []
    lines.append("# heatmap_table — cosine_AB × layer × component")
    lines.append("")
    lines.append("**Date**: 2026-05-10")
    lines.append("**A** = Phase 2 cotrain (BG-LB pretrain → chat dual-loss w=0.3→0.5)")
    lines.append("**B** = BG-LA persona-only pretrain (no chat dual loss)")
    lines.append("")
    lines.append("Lower cos = larger drift A-vs-B = greater cotrain effect.")
    lines.append("")

    short = {
        "norm1.weight": "n1",
        "attn.q_proj.weight": "q",
        "attn.k_proj.weight": "k",
        "attn.v_proj.weight": "v",
        "attn.o_proj.weight": "o",
        "norm2.weight": "n2",
        "ffn.gate.weight": "gate",
        "ffn.up.weight": "up",
        "ffn.down.weight": "down",
    }
    header = "| layer | " + " | ".join(short[c] for c in COMPONENTS) + " | row_mean |"
    sep    = "|---|" + "|".join(["---"]*len(COMPONENTS)) + "|---|"
    lines.append("## cosine_AB heatmap (4-decimal)")
    lines.append("")
    lines.append(header)
    lines.append(sep)
    for li in range(N_LAYERS):
        row = [r for r in results["per_pair"] if r["layer"] == li]
        row_by_c = {r["component"]: r for r in row}
        cells = [f"{row_by_c[c]['cos_AB']:.4f}" for c in COMPONENTS]
        rm = sum(row_by_c[c]["cos_AB"] for c in COMPONENTS) / len(COMPONENTS)
        lines.append(f"| {li:2d} | " + " | ".join(cells) + f" | {rm:.4f} |")
    # column means
    col_means = []
    for c in COMPONENTS:
        rows = [r for r in results["per_pair"] if r["component"] == c]
        col_means.append(sum(r["cos_AB"] for r in rows) / len(rows))
    lines.append("| **col_mean** | " + " | ".join(f"**{m:.4f}**" for m in col_means) + " | — |")
    lines.append("")

    # heat-band classification
    lines.append("## heat-band classification (cos_AB)")
    lines.append("")
    lines.append("| band | range | meaning |")
    lines.append("|---|---|---|")
    lines.append("| HOT (most-changed)  | cos < 0.40 | cotrain dramatically reshaped this slot |")
    lines.append("| WARM | 0.40 ≤ cos < 0.65 | substantial drift |")
    lines.append("| COOL | 0.65 ≤ cos < 0.85 | moderate drift |")
    lines.append("| COLD (preserved)    | cos ≥ 0.85 | barely touched by cotrain |")
    lines.append("")

    def band(c):
        if c < 0.40: return "HOT"
        if c < 0.65: return "WARM"
        if c < 0.85: return "COOL"
        return "COLD"

    lines.append("## per-component summary (mean over 24 layers)")
    lines.append("")
    lines.append("| component | mean_cos | min_cos | max_cos | mean_rel_L2 | band(mean) |")
    lines.append("|---|---|---|---|---|---|")
    for c in COMPONENTS:
        agg = results["per_component_aggregate"][c]
        lines.append(
            f"| `{c}` | {agg['mean_cos_AB']:.4f} | {agg['min_cos_AB']:.4f} | "
            f"{agg['max_cos_AB']:.4f} | {agg['mean_relative_l2_diff']:.4f} | "
            f"{band(agg['mean_cos_AB'])} |"
        )
    lines.append("")

    # per-slab summary
    lines.append("## per-slab summary (cross-link with §57)")
    lines.append("")
    lines.append("| slab | layers | mean_cos | mean_rel_L2 |")
    lines.append("|---|---|---|---|")
    for sn, sd in results["per_slab_aggregate"].items():
        lines.append(f"| `{sn}` | {sd['layers'][0]}..{sd['layers'][-1]} | "
                     f"{sd['mean_cos_AB']:.4f} | {sd['mean_relative_l2_diff']:.4f} |")
    lines.append("")

    # per-slab × component
    lines.append("## per-slab × component cosine")
    lines.append("")
    h = "| slab | " + " | ".join(short[c] for c in COMPONENTS) + " |"
    s = "|---|" + "|".join(["---"]*len(COMPONENTS)) + "|"
    lines.append(h)
    lines.append(s)
    for sn, sd in results["per_slab_aggregate"].items():
        cells = [f"{sd['per_component'][c]['mean_cos_AB']:.4f}" for c in COMPONENTS]
        lines.append(f"| `{sn}` | " + " | ".join(cells) + " |")
    lines.append("")

    # global extras
    lines.append("## global extras (untouched by §57 swap)")
    lines.append("")
    lines.append("| tensor | shape | cos_AB | rel_L2 |")
    lines.append("|---|---|---|---|")
    for k, v in results["global_extras"].items():
        lines.append(f"| `{k}` | {v['shape']} | {v['cos_AB']:.4f} | {v['relative_l2_diff']:.4f} |")
    lines.append("")

    out_md = OUT_DIR / "heatmap_table.md"
    with open(out_md, "w") as f:
        f.write("\n".join(lines))
    log(f"wrote {out_md}")

    log(f"DONE in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
