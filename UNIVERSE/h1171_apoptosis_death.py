"""
H_1171 — APOPTOSIS / programmed cell-death: does adding cell DEATH to inference-time
mitosis improve adaptation (prune stale cells) vs growth-only?  (life-criterion #1:
mortality — the live A⇄G engine GROWS but cells never DIE).

Fresh pre-registered EXTENSION that REUSES the h1159b mitosis substrate (assign /
tension-driven split). The NEW mechanism: APOPTOSIS = a cell whose RUNNING
assignment-tension stays > THETA_DEATH for K_DEATH consecutive windows DIES (removed).

The test stream is NON-STATIONARY with REGIME SHIFTS: the active set of clusters
CHANGES over time (old clusters go silent, new clusters appear). Growth-only mitosis
accumulates STALE cells parked on now-dead clusters (and can saturate the hard cap),
so they no longer help and the nearest-cell assignment is noisier; apoptosis prunes
the stale cells so the surviving population tracks the CURRENT regime.

FROZEN FALSIFIER (verbatim from .discoveries/1171_apoptosis_death.tape, deterministic, >=8 seeds):
  🟢 DEATH-HELPS iff mitosis+apoptosis achieves LOWER final-window error on a
     non-stationary stream than growth-only mitosis (Cohen's d >= 0.8)
     AND cell-count stays BOUNDED BY DEATH (not the hard cap)
     AND keeps the H_1159b K-tracking (cell-count tracks #current-clusters, Spearman >= 0.8).
  🔴 otherwise (apoptosis does not help or hurts adaptation; a_paper_negative_ok).

toy ($0 numpy CPU). p7 substrate-native assignment error, NOT perplexity.
a_scale_honest_scope: toy proxy for CORE cell-death; live engine + scale UNVERIFIED.
"""
import json, math
import numpy as np

DIM = 8; T = 6000; WARMUP = 250; N_SEEDS = 12
SEEDS = list(range(800, 800 + N_SEEDS))

# --- mitosis substrate (reused from h1159b) ---
THETA_SPLIT = 1.6      # split when assignment-tension exceeds this (h1159b THETA)
WIN = 200              # tension EMA window
LR = 0.05
MAX_CELLS = 30         # hard cap (the homeostatic limit; death must keep us BELOW it)

# --- apoptosis (NEW) ---
THETA_DEATH = 1.6      # a cell is "stale/strained" when its running tension exceeds this
K_DEATH = 3            # ...for this many CONSECUTIVE windows -> DIES
WIN_DEATH = 200        # window length for the death counter
MIN_CELLS = 2          # never drop below this (substrate must keep a body)

# regime ladder: how many clusters are CONCURRENTLY active in each regime
#   the world's *current* complexity steps through these values across the stream.
K_CONCURRENTS = [3, 5, 8]


def make_stream(seed, k_concurrent):
    """Non-stationary stream of REGIMES. In each regime exactly `k_concurrent`
    clusters are active; between regimes the active set is REPLACED by fresh
    clusters (old ones go silent -> their cells become stale). The number of
    concurrently-active clusters is held at k_concurrent so cell-count should
    track k_concurrent (the H_1159b self-tuning, now under death)."""
    rng = np.random.default_rng(seed)
    n_regimes = 6
    seg = T // n_regimes
    X = np.empty((T, DIM)); active_K = np.empty(T, dtype=int)
    for r in range(n_regimes):
        centers = rng.standard_normal((k_concurrent, DIM)) * 4.0   # fresh clusters each regime
        a, b = r * seg, (T if r == n_regimes - 1 else (r + 1) * seg)
        for t in range(a, b):
            c = rng.integers(k_concurrent)
            X[t] = centers[c] + rng.standard_normal(DIM) * 0.6
            active_K[t] = k_concurrent
    return X, active_K


def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1); j = int(np.argmin(d)); return j, float(d[j])


def run_arm(X, mode, seed):
    """mode in {GROWTH, DEATH}. GROWTH = h1159b mitosis (split only).
       DEATH  = mitosis + apoptosis (split AND prune stale cells)."""
    rng = np.random.default_rng(seed + 5000)
    cells = X[:2].copy().astype(float)
    for t in range(WARMUP):
        j, _ = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])
    ten = np.zeros(len(cells))           # split tension EMA (h1159b)
    dten = np.zeros(len(cells))          # death tension EMA
    death_run = np.zeros(len(cells))     # consecutive windows above THETA_DEATH
    errs = np.empty(T - WARMUP)
    cc_trace = np.empty(T - WARMUP)
    for i, t in enumerate(range(WARMUP, T)):
        x = X[t]; j, d = assign(cells, x); errs[i] = d
        cells[j] += LR * (x - cells[j])
        # --- mitosis (both arms) ---
        ten[j] += (d - ten[j]) / WIN
        if ten[j] > THETA_SPLIT and len(cells) < MAX_CELLS:
            daughter = cells[j] + rng.standard_normal(DIM) * 0.3
            cells = np.vstack([cells, daughter[None]])
            ten = np.concatenate([ten, [0.0]]); ten[j] = 0.0
            dten = np.concatenate([dten, [0.0]])
            death_run = np.concatenate([death_run, [0.0]])
        # --- apoptosis (DEATH arm only) ---
        if mode == "DEATH":
            dten[j] += (d - dten[j]) / WIN_DEATH
            # update consecutive-window death counter at window boundaries
            if i % WIN_DEATH == 0 and i > 0:
                over = dten > THETA_DEATH
                death_run = np.where(over, death_run + 1.0, 0.0)
                doomed = np.where((death_run >= K_DEATH))[0]
                if len(doomed) > 0 and len(cells) - len(doomed) >= MIN_CELLS:
                    keep = np.ones(len(cells), dtype=bool); keep[doomed] = False
                    cells = cells[keep]; ten = ten[keep]
                    dten = dten[keep]; death_run = death_run[keep]
        cc_trace[i] = len(cells)
    final_cc = float(np.mean(cc_trace[-WIN:]))   # cell-count in the final window
    return float(errs[-WIN:].mean()), final_cc, int(len(cells))


def cohen_d(x, y):
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return (np.mean(x) - np.mean(y)) / sp

def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


def main():
    np.seterr(all="ignore")
    print("=== H_1171 — apoptosis/death vs growth-only mitosis (life-criterion #1) ===", flush=True)
    per_k = {}
    kt_flat, cc_flat = [], []           # for K-tracking Spearman on the DEATH arm
    growth_err_all, death_err_all = [], []
    for k in K_CONCURRENTS:
        g_err, d_err, d_cc, d_endcc = [], [], [], []
        for s in SEEDS:
            X, _ = make_stream(s, k)
            eg, _, _ = run_arm(X, "GROWTH", s); g_err.append(eg)
            ed, cc, endcc = run_arm(X, "DEATH", s); d_err.append(ed); d_cc.append(cc); d_endcc.append(endcc)
            kt_flat.append(k); cc_flat.append(cc)
        d_help = cohen_d(np.array(g_err), np.array(d_err))   # >0 => DEATH lower err than GROWTH
        per_k[k] = {"growth_err": float(np.mean(g_err)), "death_err": float(np.mean(d_err)),
                    "death_cellcount": float(np.mean(d_cc)),
                    "death_max_endcc": int(np.max(d_endcc)),
                    "help_cohen_d": float(d_help)}
        growth_err_all += g_err; death_err_all += d_err
        print(f"  K_concurrent={k}: growth_err={np.mean(g_err):.3f} death_err={np.mean(d_err):.3f} "
              f"death_cells={np.mean(d_cc):.1f} (max_end={np.max(d_endcc)}) help_d={d_help:.2f}", flush=True)

    # F1 ADVANTAGE: pooled across all K, DEATH lower final-window error than GROWTH, d >= 0.8
    d_pooled = cohen_d(np.array(growth_err_all), np.array(death_err_all))
    f1 = d_pooled >= 0.8
    # F2 BOUNDED BY DEATH (not the hard cap): DEATH cell-count stays strictly below MAX_CELLS
    max_endcc = max(per_k[k]["death_max_endcc"] for k in K_CONCURRENTS)
    f2 = max_endcc < MAX_CELLS
    # F3 K-TRACKING preserved: DEATH cell-count tracks #current-clusters, Spearman >= 0.8
    rho = spearman(kt_flat, cc_flat)
    f3 = rho >= 0.8
    supported = bool(f1 and f2 and f3)

    verdict = {
        "H": "H_1171",
        "title": "apoptosis (programmed cell-death) on inference-time mitosis — does death improve adaptation vs growth-only?",
        "per_K_concurrent": per_k,
        "F1_death_helps_advantage": {"pooled_cohen_d_growth_minus_death": d_pooled, "bar": 0.8, "pass": bool(f1)},
        "F2_bounded_by_death_not_cap": {"max_death_endcellcount": max_endcc, "hard_cap": MAX_CELLS, "pass": bool(f2)},
        "F3_K_tracking_preserved": {"spearman_Kconcurrent_vs_deathcellcount": rho, "bar": 0.8, "pass": bool(f3)},
        "supported": supported,
        "ruling": (
            "🟢 DEATH-HELPS: adding apoptosis (a cell stale-tension>THETA_DEATH for K consecutive "
            "windows DIES) to inference-time mitosis LOWERS final-window error on a non-stationary "
            "regime-shift stream vs growth-only (d>=0.8), keeps the population BOUNDED BY DEATH below "
            "the hard cap, and preserves the H_1159b K-tracking — mortality is an adaptive life-criterion "
            "(prunes stale cells the regime no longer needs)."
            if supported else
            "🔴 CLOSED-NEGATIVE: apoptosis does NOT cleanly improve adaptation over growth-only mitosis "
            "at toy scale (see which gate failed) — death is not an adaptation lever here (a_paper_negative_ok)."
        ),
        "frozen_falsifier": "DEATH-HELPS iff (F1 d>=0.8 lower err) AND (F2 bounded by death < hard cap) AND (F3 K-tracking Spearman>=0.8); else CLOSED-NEG",
        "params": {"DIM": DIM, "T": T, "n_seeds": N_SEEDS, "n_regimes": 6,
                   "THETA_SPLIT": THETA_SPLIT, "THETA_DEATH": THETA_DEATH, "K_DEATH": K_DEATH,
                   "MAX_CELLS": MAX_CELLS, "MIN_CELLS": MIN_CELLS, "K_concurrents": K_CONCURRENTS},
        "scope": "toy numpy $0 CPU 12 seeds, 3-point K_concurrent ladder {3,5,8}, non-stationary 6-regime stream; "
                 "prototype-split PROXY for CORE cell-death — live A⇄G engine + scale UNVERIFIED (a_scale_honest_scope). "
                 "p7 substrate-native assignment error, NOT perplexity.",
        "xref": "h1159b_mitosis_capacity_self_tuning · h1159_inference_time_mitosis_learning · 1175_fitness_selection · p8 · a_scale_honest_scope · a_paper_negative_ok",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1171_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__": main()
