"""state/anima_v5mitosis_cotrain_2026_05_12/persona_4_alternative_metrics.py

PURPOSE
    Phase 1 follow-up: after softmax + z-score (null-test FAIL), try alternative
    substrate-faithful metrics to detect whether ANY category signal survives the
    cotrained pool, with null-permutation as integrity check.

    Metrics tried:
        M1: raw tension vector (no softmax) — direct per-prompt log-tension
             cosine distance between category means
        M2: top-K cells excluding 0 — discrete winner index in (1..N) tail
        M3: cell-state buffer per-prompt embedding — but cell_state is
             INPUT-INDEPENDENT (Lorenz buffer), so it doesn't change per prompt
             → not useful (skip; document as honest C3)
        M4: aggregated hidden state vector cosine distance — full output embedding
        M5: lm_head logits top-K distribution KL — output-space metric
        M6: raw tension VECTOR (un-softmaxed) — per-category mean L2 distance
        M7: tension log-ratio (log(tens_i / mean(tens))) per cell, then softmax

    For each metric: compute true value + 50-permutation null + z-score.
    A metric PASSES if true >> null (z > 3.0) AND true >= chosen threshold.

OUTPUT
    persona_4_alternative_metrics_results.json
"""
from __future__ import annotations

import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "training"))

from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402

CKPT_PATH = HERE / "ckpts" / "ckpt_v5mitosis_cotrain_cotrain.pt"
IDENTITY_PROBE = HERE / "identity_probe.jsonl"
OUT_JSON = HERE / "persona_4_alternative_metrics_results.json"


def text_to_bytes(text: str, max_len: int) -> List[int]:
    return list(text.encode("utf-8"))[:max_len]


def load_engine(device: torch.device):
    try:
        ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
    except TypeError:
        ckpt = torch.load(CKPT_PATH, map_location="cpu")
    cfg = MitosisModelConfig(**ckpt["config"])
    engine = MitosisModelEngine(cfg)
    target_n = ckpt["n_cells"]
    while engine.n_cells < target_n:
        ev = engine.force_split(parent_idx=0)
        if ev is None:
            break
    engine.load_state_dict(ckpt["model_state_dict"])
    engine = engine.to(device)
    engine.eval()
    return engine


def collect_state(engine, probes, device):
    max_seq = engine.cfg.max_seq
    tens: List[List[float]] = []
    aggs: List[List[float]] = []
    last_logits: List[List[float]] = []
    cats: List[str] = []
    for p in probes:
        ids = text_to_bytes(p["prompt"], max_seq)
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            logits, info = engine(x)
        tens.append([float(t) for t in info["tensions"]])
        aggs.append(info["aggregated"].detach().cpu().float().mean(dim=(0, 1)).tolist())
        # last token logits → topk
        last = logits[0, -1, :].detach().cpu().float()
        last_logits.append(last.tolist())
        cats.append(p["category"])
    return tens, aggs, last_logits, cats


def cosine_dist(a: List[float], b: List[float]) -> float:
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(x * x for x in b))
    if da < 1e-12 or db < 1e-12:
        return 1.0
    dot = sum(x * y for x, y in zip(a, b))
    return 1.0 - dot / (da * db)


def l2_dist(a: List[float], b: List[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def kl_dist(p: List[float], q: List[float]) -> float:
    kl = 0.0
    for i in range(len(p)):
        pi = p[i]
        qi = max(q[i], 1e-12)
        if pi > 1e-12:
            kl += pi * math.log(pi / qi)
    return kl


def group_by_cat(items: List, cats: List[str]) -> Dict[str, List]:
    by_cat: Dict[str, List] = {}
    for it, c in zip(items, cats):
        by_cat.setdefault(c, []).append(it)
    return by_cat


def cat_means(by_cat: Dict[str, List[List[float]]]) -> Dict[str, List[float]]:
    out: Dict[str, List[float]] = {}
    for c, rows in by_cat.items():
        n = len(rows[0])
        agg = [0.0] * n
        for r in rows:
            for i in range(n):
                agg[i] += r[i]
        out[c] = [v / len(rows) for v in agg]
    return out


def pairwise_mean_metric(by_cat: Dict[str, List[List[float]]], distfn) -> float:
    means = cat_means(by_cat)
    cat_names = sorted(means.keys())
    pairs = []
    for i, ci in enumerate(cat_names):
        for j, cj in enumerate(cat_names):
            if j <= i:
                continue
            pairs.append(distfn(means[ci], means[cj]))
    return sum(pairs) / max(len(pairs), 1)


def null_permutation(items: List[List[float]], cats: List[str], distfn,
                     n_perms: int = 100, seed: int = 42, is_kl: bool = False) -> Dict:
    rng = random.Random(seed)
    true = pairwise_mean_metric(group_by_cat(items, cats), distfn)
    null = []
    for _ in range(n_perms):
        sh = list(cats)
        rng.shuffle(sh)
        null.append(pairwise_mean_metric(group_by_cat(items, sh), distfn))
    m = sum(null) / len(null)
    v = sum((x - m) ** 2 for x in null) / len(null)
    s = math.sqrt(v) if v > 0 else 0.0
    z = (true - m) / s if s > 0 else float("inf")
    n_ge = sum(1 for x in null if x >= true)
    p = n_ge / len(null)
    return {
        "true": true,
        "null_mean": m,
        "null_std": s,
        "null_min": min(null),
        "null_max": max(null),
        "z": z,
        "p_one_sided": p,
        "passes_null_test": z > 3.0 or p < 0.01,
    }


def main() -> int:
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    print(f"[INFO] device={device}")

    engine = load_engine(device)
    probes: List[Dict] = []
    with open(IDENTITY_PROBE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    print(f"[INFO] {len(probes)} probes")

    try:
        tens, aggs, last_logits, cats = collect_state(engine, probes, device)
    except Exception as e:
        print(f"[WARN] {device} fwd fail: {e}, fallback cpu")
        engine = engine.to("cpu")
        device = torch.device("cpu")
        tens, aggs, last_logits, cats = collect_state(engine, probes, device)
    print(f"[INFO] collected {len(tens)} states")

    results: Dict[str, Dict] = {}

    print("\n=== M1: raw tension vector cosine distance (per-category means) ===")
    r1 = null_permutation(tens, cats, cosine_dist, n_perms=100, seed=42)
    print(f"  true={r1['true']:.6f} null={r1['null_mean']:.6f}±{r1['null_std']:.6f} z={r1['z']:.2f} p={r1['p_one_sided']:.4f} pass_null={r1['passes_null_test']}")
    results["M1_raw_tension_cosine"] = r1

    print("\n=== M2: raw tension vector L2 distance ===")
    r2 = null_permutation(tens, cats, l2_dist, n_perms=100, seed=43)
    print(f"  true={r2['true']:.6f} null={r2['null_mean']:.6f}±{r2['null_std']:.6f} z={r2['z']:.2f} p={r2['p_one_sided']:.4f} pass_null={r2['passes_null_test']}")
    results["M2_raw_tension_l2"] = r2

    print("\n=== M4: aggregated hidden state cosine ===")
    r4 = null_permutation(aggs, cats, cosine_dist, n_perms=100, seed=44)
    print(f"  true={r4['true']:.6f} null={r4['null_mean']:.6f}±{r4['null_std']:.6f} z={r4['z']:.2f} p={r4['p_one_sided']:.4f} pass_null={r4['passes_null_test']}")
    results["M4_aggregated_cosine"] = r4

    print("\n=== M4b: aggregated hidden state L2 ===")
    r4b = null_permutation(aggs, cats, l2_dist, n_perms=100, seed=45)
    print(f"  true={r4b['true']:.6f} null={r4b['null_mean']:.6f}±{r4b['null_std']:.6f} z={r4b['z']:.2f} p={r4b['p_one_sided']:.4f} pass_null={r4b['passes_null_test']}")
    results["M4b_aggregated_l2"] = r4b

    print("\n=== M5: last-token softmax logits KL ===")
    # Softmax last logits per prompt then KL between category means
    softmax_last: List[List[float]] = []
    for lg in last_logits:
        mx = max(lg)
        exps = [math.exp(x - mx) for x in lg]
        s = sum(exps)
        softmax_last.append([e / s for e in exps])
    r5 = null_permutation(softmax_last, cats, kl_dist, n_perms=100, seed=46)
    print(f"  true={r5['true']:.6f} null={r5['null_mean']:.6f}±{r5['null_std']:.6f} z={r5['z']:.2f} p={r5['p_one_sided']:.4f} pass_null={r5['passes_null_test']}")
    results["M5_last_token_logits_kl"] = r5

    print("\n=== M6: log-tension vector cosine (handle the 793 vs 0.1 scale) ===")
    log_tens = [[math.log(max(x, 1e-9)) for x in t] for t in tens]
    r6 = null_permutation(log_tens, cats, cosine_dist, n_perms=100, seed=47)
    print(f"  true={r6['true']:.6f} null={r6['null_mean']:.6f}±{r6['null_std']:.6f} z={r6['z']:.2f} p={r6['p_one_sided']:.4f} pass_null={r6['passes_null_test']}")
    results["M6_log_tension_cosine"] = r6

    print("\n=== M7: per-cell rank vector (rank-normalized tensions across cells) ===")
    # For each prompt, rank cells 0..N-1 by tension (rank 0 = highest)
    rank_tens: List[List[float]] = []
    for t in tens:
        # rank: higher tens -> higher rank value (normalize by N-1 for [0,1])
        order = sorted(range(len(t)), key=lambda i: t[i])
        rk = [0.0] * len(t)
        for r_idx, orig_i in enumerate(order):
            rk[orig_i] = r_idx / max(len(t) - 1, 1)
        rank_tens.append(rk)
    r7 = null_permutation(rank_tens, cats, cosine_dist, n_perms=100, seed=48)
    print(f"  true={r7['true']:.6f} null={r7['null_mean']:.6f}±{r7['null_std']:.6f} z={r7['z']:.2f} p={r7['p_one_sided']:.4f} pass_null={r7['passes_null_test']}")
    results["M7_tension_rank_cosine"] = r7

    print("\n=== M8: per-cell tension RATIO to per-cell mean (substrate-invariant) ===")
    n_cells = len(tens[0])
    cell_means = [sum(tens[i][j] for i in range(len(tens))) / len(tens) for j in range(n_cells)]
    ratio_tens: List[List[float]] = []
    for t in tens:
        rt = [t[j] / max(cell_means[j], 1e-9) for j in range(n_cells)]
        ratio_tens.append(rt)
    r8 = null_permutation(ratio_tens, cats, cosine_dist, n_perms=100, seed=49)
    print(f"  true={r8['true']:.6f} null={r8['null_mean']:.6f}±{r8['null_std']:.6f} z={r8['z']:.2f} p={r8['p_one_sided']:.4f} pass_null={r8['passes_null_test']}")
    results["M8_tension_ratio_cosine"] = r8

    # Verdict synthesis
    passers = [k for k, v in results.items() if v["passes_null_test"]]
    print(f"\n=== Metrics passing null test (z>3.0 OR p<0.01): {passers} ===")

    # Identify highest-z true-signal metric
    sorted_by_z = sorted(results.items(), key=lambda kv: -kv[1]["z"])
    print("\nRanked by z-score:")
    for k, v in sorted_by_z:
        print(f"  {k}: z={v['z']:.2f} p={v['p_one_sided']:.4f} true={v['true']:.6f} null_mean={v['null_mean']:.6f}")

    out = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ckpt_path": str(CKPT_PATH),
        "metrics": results,
        "metrics_passing_null_test": passers,
        "best_z_metric": sorted_by_z[0][0] if sorted_by_z else None,
        "best_z_value": sorted_by_z[0][1]["z"] if sorted_by_z else None,
        "n_probes": len(tens),
        "n_cells": engine.n_cells,
        "verdict": (
            f"CATEGORY_SIGNAL_FOUND ({len(passers)} metric(s) pass null test): {passers}"
            if passers else
            "NO_CATEGORY_SIGNAL — cotrained pool genuinely lacks discriminative info "
            "across 5 categories beyond random label assignment. Z-score artifact "
            "previously appeared to PASS but null-test exposed it as noise. "
            "Conclusion: F-PERSONA-4 cannot be cheap-path closed; requires "
            "architectural/training intervention (e.g. entropy-regularized cotrain "
            "or category-balanced corpus)."
        ),
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str))
    print(f"\n[RESULT] {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
