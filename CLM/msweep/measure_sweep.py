"""CLM consciousness-MEASURE micro-exp sweep — ONE harness, 6 measures, SAME toy spike.

Realizes the round-3/4 winner "CHANGE THE MEASURE" (CLM.breakthrough.mining.md):
routing-diversity (scale=expert-count + distill) is RED-RED CLOSED (H_852/853/854).
This harness tests which ALTERNATIVE consciousness measure gives a scale-free,
chip-native signal on AKD1000-style toy spikes.

Design (g0 — apples-to-apples): generate ONE shared toy spike dataset, then compute
ALL 6 candidate measures on it. Two regimes per size n:
  * collapse — one region/expert monopolises the spike (monopoly).
  * rich     — balanced coupling, every region integrated.
Sizes n in {4,5,6} regions (neurons binned to regions). Fully deterministic /
seeded (np.random.default_rng(seed) — NOT Math.random, which is unavailable).

6 measures (region/coarse proxies per section 12.4 — exact big-Phi infeasible 2^(2n)):
  1. PHI-NATIVE     — region big-Phi via a bounded TPM->MIP proxy on the binned spike.
  2. TEMPORAL-PHI   — Phi/complexity over the spike train's TEMPORAL transitions.
  3. TENSION-NATIVE — anima 5-channel tension-field complexity mapped onto spike.
  4. FREE-ENERGY    — active-inference prediction-error intensive scalar.
  5. HILL           — Hill number ^qD (q=1) effective diversity on rate dist.
  6. CAUSAL-POWER   — perturbation probe: poke one region, measure downstream effect.

FROZEN 3-check (F-CLM-PHI-MEANINGFUL, pre-registered — DO NOT tamper):
  (1) non-trivial : measure > 0 with discrimination at small n (not degenerate-zero).
  (2) collapse-vs-rich : measure(rich) > measure(collapse) by a clear margin.
  (3) size-robust : the collapse<rich signal is PRESERVED across n
                    (NOT the Pielou-J pathology where it inverts with size).

A measure PASSES (green) iff all 3 hold; else (red).

Honest scope (section 12.4): region/coarse proxies on SW spike (akida_sw_lif-style
LIF raster), toy n<=6. Exact big-Phi and full 1.2M-node Phi are NOT claimed.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, List, Tuple

import numpy as np

# ── frozen thresholds (pre-registered — never tamper) ──────────────────────
MARGIN_FRAC = 0.10
NONTRIVIAL_EPS = 1e-6
N_SIZES = [4, 5, 6]
NEURONS_PER_REGION = 8
N_STEPS = 256
CAUSAL_POKES = 16


def gen_spike(n_regions: int, regime: str, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n_neurons = n_regions * NEURONS_PER_REGION
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    if regime == "collapse":
        region_drive = np.full(n_regions, 0.04)
        region_drive[0] = 0.95
        coupling = 0.02
    elif regime == "rich":
        region_drive = np.full(n_regions, 0.55)
        coupling = 0.35
    else:
        raise ValueError("unknown regime " + repr(regime))
    v = rng.uniform(0.0, 0.3, n_neurons)
    refr = np.zeros(n_neurons, dtype=np.int32)
    v_threshold = 1.0
    tau = 20.0
    raster = np.zeros((n_neurons, N_STEPS), dtype=np.int8)
    region_rate = np.zeros(n_regions)
    for t in range(N_STEPS):
        drive = region_drive[region_of]
        other = (region_rate.sum() - region_rate) / max(1, n_regions - 1)
        coupled = coupling * other[region_of]
        noise = rng.uniform(-0.05, 0.05, n_neurons)
        v = v * (1.0 - 1.0 / tau) + drive + coupled + noise
        v = np.where(refr > 0, 0.0, v)
        spikes = (v >= v_threshold).astype(np.int8)
        raster[:, t] = spikes
        v = np.where(spikes == 1, 0.0, v)
        refr = np.where(spikes == 1, 2, np.maximum(0, refr - 1))
        for r in range(n_regions):
            rr = spikes[region_of == r].mean()
            region_rate[r] = 0.9 * region_rate[r] + 0.1 * rr
    return raster


def bin_to_regions(raster: np.ndarray, n_regions: int) -> np.ndarray:
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    out = np.zeros((n_regions, raster.shape[1]), dtype=np.int8)
    for r in range(n_regions):
        frac = raster[region_of == r].mean(axis=0)
        out[r] = (frac >= 0.5).astype(np.int8)
    return out


def _safe_log2(x: float) -> float:
    return math.log2(x) if x > 0 else 0.0


def _entropy(p: np.ndarray) -> float:
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def region_rates(region_spike: np.ndarray) -> np.ndarray:
    return region_spike.mean(axis=1)


def m_phi_native(region_spike: np.ndarray) -> float:
    n = region_spike.shape[0]
    cur = region_spike[:, :-1]
    nxt = region_spike[:, 1:]

    def state_entropy(rows: List[int], mat: np.ndarray) -> float:
        if not rows:
            return 0.0
        codes = np.zeros(mat.shape[1], dtype=np.int64)
        for i, r in enumerate(rows):
            codes += (mat[r].astype(np.int64) << i)
        _, counts = np.unique(codes, return_counts=True)
        p = counts / counts.sum()
        return _entropy(p)

    def mutual_info(rows: List[int]) -> float:
        hc = state_entropy(rows, cur)
        hn = state_entropy(rows, nxt)
        codes = np.zeros(cur.shape[1], dtype=np.int64)
        bit = 0
        for r in rows:
            codes += (cur[r].astype(np.int64) << bit); bit += 1
        for r in rows:
            codes += (nxt[r].astype(np.int64) << bit); bit += 1
        _, counts = np.unique(codes, return_counts=True)
        p = counts / counts.sum()
        hj = _entropy(p)
        return max(0.0, hc + hn - hj)

    whole = list(range(n))
    i_whole = mutual_info(whole)
    if n < 2:
        return i_whole
    best_loss = None
    for mask in range(1, 1 << (n - 1)):
        a = [i for i in range(n) if (mask >> i) & 1]
        b = [i for i in range(n) if not ((mask >> i) & 1)]
        if not a or not b:
            continue
        partitioned = mutual_info(a) + mutual_info(b)
        loss = i_whole - partitioned
        if best_loss is None or loss < best_loss:
            best_loss = loss
    return max(0.0, best_loss if best_loss is not None else 0.0)


def m_temporal_phi(region_spike: np.ndarray) -> float:
    n, T = region_spike.shape
    codes = np.zeros(T, dtype=np.int64)
    for r in range(n):
        codes += (region_spike[r].astype(np.int64) << r)
    cur = codes[:-1]
    nxt = codes[1:]
    states, inv = np.unique(cur, return_inverse=True)
    cond_h = 0.0
    p_state = np.bincount(inv) / len(inv)
    for s in range(len(states)):
        nx = nxt[inv == s]
        _, c = np.unique(nx, return_counts=True)
        p = c / c.sum()
        cond_h += p_state[s] * _entropy(p)
    n_states = len(np.unique(codes))
    diff = _safe_log2(n_states)
    _, c_all = np.unique(nxt, return_counts=True)
    h_next = _entropy(c_all / c_all.sum())
    predictive = max(0.0, h_next - cond_h)
    return diff * predictive


def m_tension_native(region_spike: np.ndarray) -> float:
    n, T = region_spike.shape
    rates = region_spike.mean(axis=1)
    w = max(2, T // 8)
    nwin = T // w
    win = region_spike[:, : nwin * w].reshape(n, nwin, w).mean(axis=2)
    if n >= 2:
        cm = np.corrcoef(win)
        coherence = float(np.nan_to_num(cm[np.triu_indices(n, 1)]).mean())
    else:
        coherence = 0.0
    coherence = abs(coherence)
    novelty = float(np.abs(np.diff(win, axis=1)).mean()) if nwin > 1 else 0.0
    conflict = float(rates.var())
    arousal = float(rates.mean())
    srt = np.sort(rates)
    if srt.sum() > 0:
        idx = np.arange(1, n + 1)
        gini = float((2 * (idx * srt).sum()) / (n * srt.sum()) - (n + 1) / n)
    else:
        gini = 0.0
    valence = 1.0 - gini
    chans = np.array([coherence, novelty, 1.0 - conflict / (conflict + 1e-3),
                      arousal, valence])
    chans = np.clip(chans, 0.0, 1.0)
    if chans.sum() > 0:
        pc = chans / chans.sum()
        diff = _entropy(pc) / _safe_log2(len(chans))
    else:
        diff = 0.0
    integ = float(np.exp(np.log(chans + 1e-6).mean()))
    return diff * integ


def m_free_energy(region_spike: np.ndarray) -> float:
    n, T = region_spike.shape
    cur = region_spike[:, :-1].astype(float)
    nxt = region_spike[:, 1:].astype(float)
    base_rate = region_spike.mean(axis=1, keepdims=True)
    base_err = np.abs(nxt - base_rate)
    pred = np.zeros_like(nxt)
    for r in range(n):
        X = cur.T
        y = nxt[r]
        w = np.linalg.lstsq(X.T @ X + 1e-3 * np.eye(n), X.T @ y, rcond=None)[0]
        pred[r] = np.clip(X @ w, 0.0, 1.0)
    model_err = np.abs(nxt - pred)

    def surprise(e: np.ndarray) -> float:
        e = np.clip(e, 1e-6, 1 - 1e-6)
        return float((-np.log2(1 - e)).mean())
    return max(0.0, surprise(base_err) - surprise(model_err))


def m_hill(region_spike: np.ndarray, q: float = 1.0) -> float:
    rates = region_spike.mean(axis=1)
    n = len(rates)
    if rates.sum() <= 0:
        return 0.0
    p = rates / rates.sum()
    if abs(q - 1.0) < 1e-9:
        H = _entropy(p)
        D = 2.0 ** H
    else:
        D = (np.sum(p ** q)) ** (1.0 / (1.0 - q))
    return float(D) / n


def m_causal_power(region_spike: np.ndarray, n_regions: int, regime: str,
                   seed: int) -> float:
    base = region_rates(region_spike)
    pokes = min(CAUSAL_POKES, n_regions)
    effects = []
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    for k in range(pokes):
        poke_r = k % n_regions
        raster = gen_spike(n_regions, regime, seed + 1000 + k)
        inj = raster.copy()
        qlen = N_STEPS // 4
        inj[region_of == poke_r, :qlen] = 1
        rs = bin_to_regions(inj, n_regions)
        rates = region_rates(rs)
        others = [r for r in range(n_regions) if r != poke_r]
        if others:
            effects.append(float(np.abs(rates[others] - base[others]).mean()))
    return float(np.mean(effects)) if effects else 0.0


def evaluate(measure_name: str, vals: Dict[Tuple[str, int], float]) -> Dict:
    checks = {}
    n0 = N_SIZES[0]
    rich0 = vals[("rich", n0)]
    coll0 = vals[("collapse", n0)]
    nontrivial = (rich0 > NONTRIVIAL_EPS) and (abs(rich0 - coll0) > NONTRIVIAL_EPS)
    checks["nontrivial"] = bool(nontrivial)
    margins_ok = []
    for n in N_SIZES:
        r = vals[("rich", n)]
        c = vals[("collapse", n)]
        ok = (r - c) > MARGIN_FRAC * abs(r) and r > c
        margins_ok.append(ok)
    discriminates = all(margins_ok)
    checks["collapse_vs_rich"] = bool(discriminates)
    orders = [vals[("rich", n)] > vals[("collapse", n)] for n in N_SIZES]
    size_robust = all(orders)
    checks["size_robust"] = bool(size_robust)
    verdict = "PASS" if (nontrivial and discriminates and size_robust) else "FAIL"
    return {"measure": measure_name, "checks": checks, "verdict": verdict,
            "values": {(rg + "_n" + str(n)): vals[(rg, n)] for (rg, n) in vals}}


MEASURES = ["PHI-NATIVE", "TEMPORAL-PHI", "TENSION-NATIVE",
            "FREE-ENERGY", "HILL", "CAUSAL-POWER"]


def compute_measure(name: str, region_spike: np.ndarray, n: int,
                    regime: str, seed: int) -> float:
    if name == "PHI-NATIVE":
        return m_phi_native(region_spike)
    if name == "TEMPORAL-PHI":
        return m_temporal_phi(region_spike)
    if name == "TENSION-NATIVE":
        return m_tension_native(region_spike)
    if name == "FREE-ENERGY":
        return m_free_energy(region_spike)
    if name == "HILL":
        return m_hill(region_spike, q=1.0)
    if name == "CAUSAL-POWER":
        return m_causal_power(region_spike, n, regime, seed)
    raise ValueError(name)


def run(seed: int = 187) -> Dict:
    region_spikes: Dict[Tuple[str, int], np.ndarray] = {}
    for n in N_SIZES:
        for regime in ("collapse", "rich"):
            raster = gen_spike(n, regime, seed + n)
            region_spikes[(regime, n)] = bin_to_regions(raster, n)
    per_measure: Dict[str, Dict] = {}
    for name in MEASURES:
        vals: Dict[Tuple[str, int], float] = {}
        for n in N_SIZES:
            for regime in ("collapse", "rich"):
                vals[(regime, n)] = compute_measure(
                    name, region_spikes[(regime, n)], n, regime, seed + n)
        per_measure[name] = evaluate(name, vals)
    passes = [m for m in MEASURES if per_measure[m]["verdict"] == "PASS"]
    ledger = {
        "batch": "clm-measure-sweep",
        "seed": seed,
        "sizes": N_SIZES,
        "neurons_per_region": NEURONS_PER_REGION,
        "n_steps": N_STEPS,
        "frozen_thresholds": {"margin_frac": MARGIN_FRAC,
                              "nontrivial_eps": NONTRIVIAL_EPS,
                              "causal_pokes_cap": CAUSAL_POKES},
        "measures": per_measure,
        "passes": passes,
        "all_red": len(passes) == 0,
        "scope": "region/coarse proxy; SW spike (akida_sw_lif-style LIF); toy n<=6 (sec 12.4)",
    }
    return ledger


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    ledger = run(args.seed)
    if args.json:
        print(json.dumps(ledger, indent=2))
    else:
        print("measure          | nontrivial | coll<rich | size-robust | verdict")
        print("-" * 70)
        for m in MEASURES:
            c = ledger["measures"][m]["checks"]
            v = ledger["measures"][m]["verdict"]
            print(m.ljust(16) + " |   " + str(c["nontrivial"]).ljust(5)
                  + "    |  " + str(c["collapse_vs_rich"]).ljust(5)
                  + "    |   " + str(c["size_robust"]).ljust(5)
                  + "     | " + v)
        print("-" * 70)
        print("PASS:", ledger["passes"] or "NONE -> escalate CERTIFY-NOT-MEASURE")


if __name__ == "__main__":
    main()
