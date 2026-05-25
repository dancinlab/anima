"""state/anima_v5mitosis_cotrain_2026_05_12/softmax_T_sweep.py

F-PERSONA-4 inference-time softmax-temperature sweep audit.

PURPOSE
    Hypothesis (b) of the cotrain BG 4-alternative future-path:
      "softmax τ tunable" — can a single inference-time temperature scaling
      recover F-PERSONA-4 category specialization (KL ≥ 0.5) WITHOUT any
      retraining of the v5-mitosis cotrain ckpt?

    BG context:
      - cotrain v1 ckpt (581 MB) frozen
      - F-V5MIT-1..5 5/5 PASS (V14-STRICT 10/10)
      - F-PERSONA-4 cotrained: KL=0.0 across all 10 5C2 pairs
      - root cause audit (prior): cell-0 tension ≈ 793 dominates;
        every other cell ≈ 0.1; standard softmax → one-hot regardless of T
        until T ≫ tension_spread.

    This sweep is the explicit AUDIT path: 10 temperature values
    (1.0 / 1.5 / 2.0 / 3.0 / 5.0 / 7.0 / 10.0 / 15.0 / 20.0 / 50.0).
    For each T:
        - softmax(tension / T) per prompt
        - per-category mean weight distribution
        - F-PERSONA-4 KL across 5C2 = 10 pairs (mean / min)
        - entropy of weight distribution (cell-pool diversity)
        - cell-dominance ratio (max_p / mean_p)

OUTPUT
    results/softmax_T_sweep_results.json  (machine-readable verdict)

VERDICT
    KL ≥ 0.5 at any T → cond #3 ☑ via inference-time hypothesis (b) only.
    KL <  0.5 for all T → hypothesis (b) FALSIFIED — escalate to (a) cotrain v2
                          or (c) metric redefinition or (d) per-session pool.

HONEST C3 (raw#10):
    1. The prior root_cause json already shows KL=0.0 at T∈{1.0, 2.0, 5.0, 50.0}
       and KL≤0.005 at T=500. This sweep is therefore expected to confirm
       FALSIFICATION of hypothesis (b). The audit is run anyway because the
       finer-grained T-grid (1.5 / 3.0 / 7.0 / 10.0 / 15.0 / 20.0) was not
       previously measured, and because hypothesis (b) deserves an explicit
       single-purpose harness rather than a sub-section of an investigation.
    2. The model is byte-level (utf-8 → ids); prompt truncation to max_seq
       (256 bytes) preserves identity_probe semantic content.
    3. Forward pass is deterministic on eval/no_grad; Lorenz buffer is read
       but not stepped (no mitosis_step inside collect_tensions).
    4. KL is computed on category-mean weight vectors (50 prompts → 5 cat
       averages → 10 pairs); within-category variance is NOT propagated.
       This mirrors the original F-PERSONA-4 definition exactly.
    5. Tension magnitudes vary by ~4 orders of magnitude across cells; we
       use float64 for the KL arithmetic to avoid catastrophic underflow at
       low-T softmax.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch

HERE = Path(__file__).resolve().parent
# Make mitosis_model_v5 importable without depending on repo layout
sys.path.insert(0, str(HERE))

from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


T_GRID: List[float] = [1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 50.0]
KL_THRESHOLD: float = 0.5  # F-PERSONA-4 pass bar


# ─── Loader ──────────────────────────────────────────────────────────

def load_engine(ckpt_path: Path, device: torch.device) -> Tuple[MitosisModelEngine, Dict]:
    try:
        ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    except TypeError:
        ckpt = torch.load(ckpt_path, map_location="cpu")
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
    return engine, ckpt


def text_to_bytes(text: str, max_len: int) -> List[int]:
    return list(text.encode("utf-8"))[:max_len]


def collect_raw_tensions(engine: MitosisModelEngine,
                          probes: List[Dict],
                          device: torch.device) -> Tuple[List[List[float]], List[str]]:
    max_seq = engine.cfg.max_seq
    tens: List[List[float]] = []
    cats: List[str] = []
    for p in probes:
        ids = text_to_bytes(p["prompt"], max_seq)
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        tens.append([float(t) for t in info["tensions"]])
        cats.append(p["category"])
    return tens, cats


# ─── Softmax with temperature (numerically stable, float64) ──────────

def softmax_T(tensions: List[float], T: float) -> List[float]:
    if T <= 0:
        raise ValueError(f"T must be > 0, got {T}")
    scaled = [t / T for t in tensions]
    mx = max(scaled)
    exps = [math.exp(s - mx) for s in scaled]
    s = sum(exps)
    return [e / s for e in exps]


# ─── Metrics ─────────────────────────────────────────────────────────

def entropy_nats(p: List[float]) -> float:
    return -sum(pi * math.log(pi) for pi in p if pi > 1e-12)


def kl_div(p: List[float], q: List[float]) -> float:
    kl = 0.0
    for i in range(len(p)):
        pi = p[i]
        qi = max(q[i], 1e-12)
        if pi > 1e-12:
            kl += pi * math.log(pi / qi)
    return kl


def per_category_avg_weights(weights: List[List[float]],
                              cats: List[str]) -> Tuple[List[str], List[List[float]]]:
    by_cat: Dict[str, List[List[float]]] = {}
    for w, c in zip(weights, cats):
        by_cat.setdefault(c, []).append(w)
    cat_names = sorted(by_cat.keys())
    n_cells = len(weights[0]) if weights else 0
    avgs: List[List[float]] = []
    for c in cat_names:
        rows = by_cat[c]
        agg = [0.0] * n_cells
        for r in rows:
            for i in range(n_cells):
                agg[i] += r[i]
        avgs.append([v / len(rows) for v in agg])
    return cat_names, avgs


def f_persona_4_kl(weights: List[List[float]],
                    cats: List[str]) -> Tuple[float, float, int, List[List[float]], List[str]]:
    cat_names, avgs = per_category_avg_weights(weights, cats)
    pairs: List[float] = []
    n = len(cat_names)
    kl_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            kl = kl_div(avgs[i], avgs[j])
            kl_matrix[i][j] = kl
            if j > i:
                pairs.append(kl)
    mean_kl = sum(pairs) / max(len(pairs), 1)
    min_kl = min(pairs) if pairs else 0.0
    return mean_kl, min_kl, len(pairs), kl_matrix, cat_names


def cell_dominance_stats(weights: List[List[float]]) -> Dict[str, float]:
    """Per-prompt max_p / mean_p (a.k.a. "dominance ratio"). Averaged across prompts.

    A dominance ratio of n_cells (= 64) means one-hot. A ratio of 1.0 means uniform.
    """
    if not weights:
        return {"dominance_mean": 0.0, "dominance_min": 0.0, "dominance_max": 0.0}
    ratios: List[float] = []
    for w in weights:
        n = len(w)
        mean_p = sum(w) / n
        max_p = max(w)
        ratios.append(max_p / mean_p if mean_p > 0 else 0.0)
    return {
        "dominance_mean": sum(ratios) / len(ratios),
        "dominance_min": min(ratios),
        "dominance_max": max(ratios),
    }


def entropy_stats(weights: List[List[float]]) -> Dict[str, float]:
    if not weights:
        return {"entropy_mean": 0.0, "entropy_min": 0.0, "entropy_max": 0.0}
    ents = [entropy_nats(w) for w in weights]
    return {
        "entropy_mean": sum(ents) / len(ents),
        "entropy_min": min(ents),
        "entropy_max": max(ents),
    }


# ─── Sweep driver ────────────────────────────────────────────────────

def run_sweep(raw_tens: List[List[float]],
              cats: List[str],
              T_values: List[float]) -> List[Dict]:
    results: List[Dict] = []
    for T in T_values:
        weights = [softmax_T(t, T) for t in raw_tens]
        mean_kl, min_kl, n_pairs, kl_matrix, cat_names = f_persona_4_kl(weights, cats)
        ent = entropy_stats(weights)
        dom = cell_dominance_stats(weights)
        verdict = "PASS" if mean_kl >= KL_THRESHOLD else "FAIL"
        results.append({
            "T": T,
            "mean_kl": mean_kl,
            "min_kl": min_kl,
            "n_pairs": n_pairs,
            "kl_threshold": KL_THRESHOLD,
            "verdict": verdict,
            "entropy_mean_nats": ent["entropy_mean"],
            "entropy_min_nats": ent["entropy_min"],
            "entropy_max_nats": ent["entropy_max"],
            "dominance_mean": dom["dominance_mean"],
            "dominance_min": dom["dominance_min"],
            "dominance_max": dom["dominance_max"],
            "kl_matrix": kl_matrix,
            "categories": cat_names,
        })
    return results


# ─── Main ────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", type=str, required=True, help="path to cotrain ckpt")
    ap.add_argument("--probe", type=str, default=str(HERE / "identity_probe.jsonl"),
                    help="identity_probe.jsonl")
    ap.add_argument("--output", type=str, required=True, help="output JSON path")
    ap.add_argument("--device", type=str, default="auto", help="cuda / cpu / auto")
    args = ap.parse_args()

    if args.device == "auto":
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
    else:
        device = torch.device(args.device)
    print(f"[INFO] device={device}")
    if device.type == "cuda":
        print(f"[INFO] GPU={torch.cuda.get_device_name(0)} mem_free="
              f"{torch.cuda.mem_get_info()[0] / 1024 ** 3:.2f} GB")

    ckpt_path = Path(args.ckpt)
    engine, ckpt = load_engine(ckpt_path, device)
    print(f"[LOAD] n_cells={engine.n_cells} d_model={engine.cfg.d_model}")

    probes: List[Dict] = []
    with open(args.probe, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    print(f"[INFO] {len(probes)} probes")

    try:
        raw_tens, cats = collect_raw_tensions(engine, probes, device)
    except Exception as e:
        print(f"[WARN] {device} forward failed: {e} — fallback cpu")
        engine = engine.to("cpu")
        device = torch.device("cpu")
        raw_tens, cats = collect_raw_tensions(engine, probes, device)
    print(f"[COLLECT] tensions collected: {len(raw_tens)} prompts × {len(raw_tens[0])} cells")

    # Quick sanity: tension stats on prompt 0
    t0 = raw_tens[0]
    print(f"[RAW] prompt 0: max={max(t0):.4f} min={min(t0):.4f} mean={sum(t0)/len(t0):.4f}")

    print(f"[SWEEP] T values = {T_GRID}")
    sweep = run_sweep(raw_tens, cats, T_GRID)

    # Console report
    print("\n=== softmax-T sweep (F-PERSONA-4 inference-time hypothesis b) ===")
    print(f"{'T':>8} {'mean_KL':>10} {'min_KL':>10} {'verdict':>8} "
          f"{'H_mean':>8} {'dom_mean':>9}")
    for r in sweep:
        print(f"{r['T']:>8.2f} {r['mean_kl']:>10.6f} {r['min_kl']:>10.6f} "
              f"{r['verdict']:>8} {r['entropy_mean_nats']:>8.4f} "
              f"{r['dominance_mean']:>9.2f}")

    any_pass = any(r["verdict"] == "PASS" for r in sweep)
    if any_pass:
        passing_Ts = [r["T"] for r in sweep if r["verdict"] == "PASS"]
        verdict_overall = "PASS"
        verdict_msg = (
            f"hypothesis_b CONFIRMED: F-PERSONA-4 KL≥{KL_THRESHOLD} achievable "
            f"via inference-time softmax-T scaling alone. Passing T values: "
            f"{passing_Ts}. cond #3 ☑ via inference-time-only."
        )
    else:
        max_kl = max(r["mean_kl"] for r in sweep)
        best_T = max(sweep, key=lambda r: r["mean_kl"])["T"]
        verdict_overall = "FAIL"
        verdict_msg = (
            f"hypothesis_b FALSIFIED: no T in {T_GRID} achieves mean_KL ≥ "
            f"{KL_THRESHOLD}. Best mean_KL={max_kl:.6f} at T={best_T}. "
            f"single-cell monopoly (cell-0 tension ≫ others) cannot be broken "
            f"by softmax temperature alone. Escalate to (a) cotrain v2 / "
            f"(c) metric redefine / (d) per-session pool."
        )

    out: Dict = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ckpt_path": str(ckpt_path),
        "n_cells": engine.n_cells,
        "d_model": engine.cfg.d_model,
        "device": str(device),
        "n_probes": len(probes),
        "T_grid": T_GRID,
        "kl_threshold": KL_THRESHOLD,
        "raw_tension_prompt0_top5": sorted(raw_tens[0], reverse=True)[:5],
        "raw_tension_prompt0_bottom5": sorted(raw_tens[0])[:5],
        "sweep": sweep,
        "hypothesis_b_verdict": verdict_overall,
        "verdict_summary": verdict_msg,
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, default=str))
    print(f"\n[RESULT] {out_path}")
    print(f"[VERDICT] hypothesis_b = {verdict_overall}")
    print(f"[VERDICT] {verdict_msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
