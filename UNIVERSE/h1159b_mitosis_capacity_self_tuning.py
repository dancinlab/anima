"""
H_1159b — does inference-time MITOSIS SELF-TUNE its capacity to the world's
complexity (cell-count tracks the true #clusters), the way H_931's SOC homeostat
self-tunes to the critical point? Clean fresh-pre-registered EXTENSION of H_1159
(p8) that connects to the criticality triangle (H_1153/H_1158/H_931).

NOT a re-litigation of H_1159's err-advantage (that was already d=6.69, untweaked).
The NEW claim: capacity SELF-ORGANIZATION — sweep the true cluster count
K_true ∈ {3,5,8}; does the tension-driven mitosis cell-count GROW WITH K_true
(self-tuning to world complexity), stay BOUNDED (self-limiting, not runaway), and
keep the err-advantage over a frozen model at every K_true?

FROZEN FALSIFIER (fresh pre-reg, deterministic, >=10 seeds):
  F1 SELF-TUNING: Spearman(K_true, final mitosis cell-count) >= 0.8 — capacity tracks the world.
  F2 ADVANTAGE: at EVERY K_true, MITOSIS final err < FROZEN final err, Cohen's d >= 2.0.
  F3 SELF-LIMITING: final mitosis cell-count < MAX_CELLS at every K_true (does not run away to the cap).
  SUPPORTED iff F1 & F2 & F3 → p8 mitosis self-organizes capacity to world complexity (SOC-like).
toy ($0 numpy CPU). a_scale_honest_scope.
"""
import json, math
import numpy as np

DIM = 8; T = 4000; WARMUP = 250; N_SEEDS = 10
SEEDS = list(range(800, 800 + N_SEEDS))
THETA = 1.6; WIN = 200; LR = 0.05; MAX_CELLS = 20
K_TRUES = [3, 5, 8]


def make_stream(seed, k_true):
    rng = np.random.default_rng(seed)
    centers = rng.standard_normal((k_true, DIM)) * 4.0
    onsets = np.linspace(0, T * 0.85, k_true).astype(int)   # clusters appear spread over time
    X = np.empty((T, DIM)); active = []; oi = 0
    for t in range(T):
        while oi < k_true and t >= onsets[oi]:
            active.append(oi); oi += 1
        c = active[rng.integers(len(active))]
        X[t] = centers[c] + rng.standard_normal(DIM) * 0.6
    return X


def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1); j = int(np.argmin(d)); return j, float(d[j])


def run_arm(X, mode, seed):
    rng = np.random.default_rng(seed + 5000)
    cells = X[:2].copy().astype(float)
    for t in range(WARMUP):
        j, _ = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])
    ten = np.zeros(len(cells)); errs = np.empty(T - WARMUP)
    for i, t in enumerate(range(WARMUP, T)):
        x = X[t]; j, d = assign(cells, x); errs[i] = d
        if mode == "FROZEN":
            continue
        cells[j] += LR * (x - cells[j])
        if mode == "MITOSIS":
            ten[j] += (d - ten[j]) / WIN
            if ten[j] > THETA and len(cells) < MAX_CELLS:
                daughter = cells[j] + rng.standard_normal(DIM) * 0.3
                cells = np.vstack([cells, daughter[None]])
                ten = np.concatenate([ten, [0.0]]); ten[j] = 0.0
    return float(errs[-WIN:].mean()), len(cells)


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
    print("=== H_1159b — mitosis capacity self-tuning to world complexity (p8 x SOC) ===", flush=True)
    per_k = {}
    kt_flat, cc_flat = [], []
    for k in K_TRUES:
        mit_err, mit_cc, frz_err = [], [], []
        for s in SEEDS:
            X = make_stream(s, k)
            e, c = run_arm(X, "MITOSIS", s); mit_err.append(e); mit_cc.append(c)
            ef, _ = run_arm(X, "FROZEN", s); frz_err.append(ef)
            kt_flat.append(k); cc_flat.append(c)
        d_adv = cohen_d(np.array(frz_err), np.array(mit_err))
        per_k[k] = {"mit_err": float(np.mean(mit_err)), "frozen_err": float(np.mean(frz_err)),
                    "mit_cellcount": float(np.mean(mit_cc)), "adv_cohen_d": float(d_adv),
                    "max_cc": int(np.max(mit_cc))}
        print(f"  K_true={k}: mit_cells={np.mean(mit_cc):.1f} mit_err={np.mean(mit_err):.3f} "
              f"frozen_err={np.mean(frz_err):.3f} adv_d={d_adv:.2f}", flush=True)

    rho = spearman(kt_flat, cc_flat)
    f1 = rho >= 0.8
    f2 = all(per_k[k]["adv_cohen_d"] >= 2.0 for k in K_TRUES)
    f3 = all(per_k[k]["max_cc"] < MAX_CELLS for k in K_TRUES)
    supported = bool(f1 and f2 and f3)
    verdict = {
        "H": "H_1159b", "title": "mitosis self-tunes capacity to world complexity (p8 x SOC self-organization)",
        "per_K_true": per_k,
        "F1_self_tuning": {"spearman_Ktrue_vs_cellcount": rho, "bar": 0.8, "pass": bool(f1)},
        "F2_advantage_all_K": {"min_adv_d": min(per_k[k]["adv_cohen_d"] for k in K_TRUES), "bar": 2.0, "pass": bool(f2)},
        "F3_self_limiting": {"max_cellcount_any_K": max(per_k[k]["max_cc"] for k in K_TRUES), "cap": MAX_CELLS, "pass": bool(f3)},
        "supported": supported,
        "ruling": ("SUPPORTED: inference-time mitosis SELF-ORGANIZES its capacity to the world's complexity (cell-count tracks #clusters, Spearman>=0.8), stays self-limiting (no runaway), and keeps the err-advantage at every scale — the p8 analog of H_931 SOC self-tuning to the critical point"
                   if supported else
                   "CLOSED-NEGATIVE: mitosis capacity does NOT cleanly self-tune to world complexity (see which gate failed)"),
        "scope": "toy numpy $0 CPU 10 seeds, 3-point K_true ladder {3,5,8}; prototype-split PROXY for the CORE cell-division — live engine + scale UNVERIFIED (a_scale_honest_scope)",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1159b_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__": main()
