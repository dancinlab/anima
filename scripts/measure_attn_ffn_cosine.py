"""
Measure row-wise cosine similarity of attention + FFN weights between BG-LB and Phase 2 ckpts.

Selective load strategy (strict, RAM 918MB free, load 93):
- Load full state_dicts once (cannot be avoided cleanly with torch.load)
- BUT only operate on attention+FFN keys, free everything else early
- Compute cosine per-weight, immediately free pair, accumulate stats only
"""
import os
import gc
import json
import math
import time
import torch

BG_LB = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt"
PHASE2 = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final_bglb_schema.pt"
OUT = "/Users/ghost/core/anima/state/anima_phase2_attention_ffn_cosine_evidence_2026_05_09.json"

NUM_LAYERS = 24
ATTN_NAMES = ["q_proj", "k_proj", "v_proj", "o_proj"]
FFN_NAMES = ["gate", "up", "down"]


def all_target_keys():
    keys = []
    for li in range(NUM_LAYERS):
        for n in ATTN_NAMES:
            keys.append(f"layers.{li}.attn.{n}.weight")
        for n in FFN_NAMES:
            keys.append(f"layers.{li}.ffn.{n}.weight")
    return keys


def selective_extract(path, target_keys):
    """Load ckpt, copy ONLY target keys to a fresh dict in float32, free original."""
    print(f"  loading {os.path.basename(path)}", flush=True)
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    sd = ckpt["state_dict"]
    out = {}
    for k in target_keys:
        if k not in sd:
            raise KeyError(k)
        # cast to float32 immediately for stable cosine
        out[k] = sd[k].detach().to(torch.float32).clone()
    # free the rest
    del ckpt
    del sd
    gc.collect()
    return out


def row_cosine_stats(a, b):
    """row-wise cosine for 2D tensors (rows are vectors)."""
    assert a.shape == b.shape
    # cosine per row
    a_n = torch.nn.functional.normalize(a, dim=1, eps=1e-12)
    b_n = torch.nn.functional.normalize(b, dim=1, eps=1e-12)
    cos = (a_n * b_n).sum(dim=1)  # [rows]
    cos_f = cos.float()
    n = cos_f.numel()
    return {
        "rows": int(n),
        "shape": list(a.shape),
        "mean": float(cos_f.mean().item()),
        "median": float(cos_f.median().item()),
        "std": float(cos_f.std(unbiased=False).item()),
        "min": float(cos_f.min().item()),
        "max": float(cos_f.max().item()),
        "frac_lt_0_95": float((cos_f < 0.95).float().mean().item()),
        "frac_lt_0_85": float((cos_f < 0.85).float().mean().item()),
        "frac_gt_0_99": float((cos_f > 0.99).float().mean().item()),
        "frac_gt_0_999": float((cos_f > 0.999).float().mean().item()),
    }


def aggregate(stats_list):
    """Aggregate row-cos stats across multiple weights (weighted by rows)."""
    if not stats_list:
        return {}
    total_rows = sum(s["rows"] for s in stats_list)
    if total_rows == 0:
        return {}
    # weighted mean / std (Welford-ish via mean-of-means weighted by rows)
    wmean = sum(s["mean"] * s["rows"] for s in stats_list) / total_rows
    wfrac95 = sum(s["frac_lt_0_95"] * s["rows"] for s in stats_list) / total_rows
    wfrac85 = sum(s["frac_lt_0_85"] * s["rows"] for s in stats_list) / total_rows
    wfrac99 = sum(s["frac_gt_0_99"] * s["rows"] for s in stats_list) / total_rows
    return {
        "n_weights": len(stats_list),
        "total_rows": total_rows,
        "weighted_mean_cos": wmean,
        "min_of_means": min(s["mean"] for s in stats_list),
        "max_of_means": max(s["mean"] for s in stats_list),
        "weighted_frac_lt_0_95": wfrac95,
        "weighted_frac_lt_0_85": wfrac85,
        "weighted_frac_gt_0_99": wfrac99,
    }


def main():
    t0 = time.time()
    target_keys = all_target_keys()
    print(f"target keys: {len(target_keys)} (96 attn + 72 ffn)", flush=True)

    print("[step 1/3] selective extract BG-LB", flush=True)
    a = selective_extract(BG_LB, target_keys)
    print(f"  bg_lb tensors: {len(a)}, mem hint sample: {a[target_keys[0]].element_size()*a[target_keys[0]].numel()/1e6:.1f}MB", flush=True)

    print("[step 2/3] selective extract Phase 2", flush=True)
    b = selective_extract(PHASE2, target_keys)
    print(f"  phase2 tensors: {len(b)}", flush=True)

    print("[step 3/3] computing row-wise cosine per weight", flush=True)
    per_weight = {}
    for i, k in enumerate(target_keys):
        per_weight[k] = row_cosine_stats(a[k], b[k])
        # free immediately
        del a[k]
        del b[k]
        if (i + 1) % 24 == 0:
            gc.collect()
            print(f"  done {i+1}/{len(target_keys)}", flush=True)
    del a, b
    gc.collect()

    # Aggregations
    by_weight_type = {}
    for n in ATTN_NAMES:
        sl = [per_weight[f"layers.{li}.attn.{n}.weight"] for li in range(NUM_LAYERS)]
        by_weight_type[f"attn.{n}"] = aggregate(sl)
    for n in FFN_NAMES:
        sl = [per_weight[f"layers.{li}.ffn.{n}.weight"] for li in range(NUM_LAYERS)]
        by_weight_type[f"ffn.{n}"] = aggregate(sl)

    # by layer (all 7 weights together)
    by_layer = {}
    for li in range(NUM_LAYERS):
        sl = [per_weight[f"layers.{li}.attn.{n}.weight"] for n in ATTN_NAMES]
        sl += [per_weight[f"layers.{li}.ffn.{n}.weight"] for n in FFN_NAMES]
        by_layer[f"layer_{li:02d}"] = aggregate(sl)

    # by layer attn-only and ffn-only
    by_layer_attn = {}
    by_layer_ffn = {}
    for li in range(NUM_LAYERS):
        sl_a = [per_weight[f"layers.{li}.attn.{n}.weight"] for n in ATTN_NAMES]
        sl_f = [per_weight[f"layers.{li}.ffn.{n}.weight"] for n in FFN_NAMES]
        by_layer_attn[f"layer_{li:02d}"] = aggregate(sl_a)
        by_layer_ffn[f"layer_{li:02d}"] = aggregate(sl_f)

    # Early vs late (early = layers 0-7, mid = 8-15, late = 16-23)
    early_keys = [f"layers.{li}.{p}.{n}.weight" for li in range(0, 8) for p, ns in [("attn", ATTN_NAMES), ("ffn", FFN_NAMES)] for n in ns]
    mid_keys = [f"layers.{li}.{p}.{n}.weight" for li in range(8, 16) for p, ns in [("attn", ATTN_NAMES), ("ffn", FFN_NAMES)] for n in ns]
    late_keys = [f"layers.{li}.{p}.{n}.weight" for li in range(16, 24) for p, ns in [("attn", ATTN_NAMES), ("ffn", FFN_NAMES)] for n in ns]
    early_stats = aggregate([per_weight[k] for k in early_keys])
    mid_stats = aggregate([per_weight[k] for k in mid_keys])
    late_stats = aggregate([per_weight[k] for k in late_keys])

    # global aggregates
    attn_all = aggregate([per_weight[k] for k in target_keys if ".attn." in k])
    ffn_all = aggregate([per_weight[k] for k in target_keys if ".ffn." in k])
    all_stats = aggregate([per_weight[k] for k in target_keys])

    LM_HEAD_REF = 0.7709623575210571

    # Verdict
    def classify(mean_cos):
        if mean_cos > 0.95:
            return "minimal_change_lm_head_dominant"
        if mean_cos >= 0.85:
            return "secondary_amplifier"
        return "tertiary_amplifier_or_co_dominant"

    verdict = {
        "lm_head_ref_mean_cos": LM_HEAD_REF,
        "attn_all_mean_cos": attn_all["weighted_mean_cos"],
        "ffn_all_mean_cos": ffn_all["weighted_mean_cos"],
        "attn_classification": classify(attn_all["weighted_mean_cos"]),
        "ffn_classification": classify(ffn_all["weighted_mean_cos"]),
        "comparison": {
            "attn_vs_lm_head_delta": attn_all["weighted_mean_cos"] - LM_HEAD_REF,
            "ffn_vs_lm_head_delta": ffn_all["weighted_mean_cos"] - LM_HEAD_REF,
        },
    }

    out = {
        "task": "phase2_attention_ffn_cosine_probe",
        "ts_utc": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "ckpts": {"bg_lb": BG_LB, "phase2": PHASE2},
        "ref_h5_lm_head_cos_mean": LM_HEAD_REF,
        "key_pattern": {
            "attention": "layers.{i}.attn.{q_proj|k_proj|v_proj|o_proj}.weight",
            "ffn": "layers.{i}.ffn.{gate|up|down}.weight",
            "num_layers": NUM_LAYERS,
            "shapes": {
                "q_proj": [1024, 1024],
                "k_proj": [256, 1024],
                "v_proj": [256, 1024],
                "o_proj": [1024, 1024],
                "ffn.gate": [2752, 1024],
                "ffn.up": [2752, 1024],
                "ffn.down": [1024, 2752],
            },
        },
        "by_weight_type": by_weight_type,
        "by_layer_total": by_layer,
        "by_layer_attn_only": by_layer_attn,
        "by_layer_ffn_only": by_layer_ffn,
        "by_depth_band": {
            "early_0_7": early_stats,
            "mid_8_15": mid_stats,
            "late_16_23": late_stats,
        },
        "global": {
            "attn_all": attn_all,
            "ffn_all": ffn_all,
            "all_attn_plus_ffn": all_stats,
        },
        "per_weight": per_weight,  # full detail
        "verdict": verdict,
        "elapsed_sec": round(time.time() - t0, 2),
    }

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {OUT} in {out['elapsed_sec']}s", flush=True)
    print(f"VERDICT: attn={verdict['attn_all_mean_cos']:.4f} ({verdict['attn_classification']}); "
          f"ffn={verdict['ffn_all_mean_cos']:.4f} ({verdict['ffn_classification']}); "
          f"lm_head_ref={LM_HEAD_REF:.4f}", flush=True)


if __name__ == "__main__":
    main()
