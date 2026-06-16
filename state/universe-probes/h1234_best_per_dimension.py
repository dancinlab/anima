"""
H_1234 — BEST-PER-DIMENSION combination search (exhaustive, not greedy)
Clarified goal: "차원" = combination ORDER k (2개조합·3개조합·4개조합...). The existing
matrix stopped at k=2 (pairwise E×F). Go to k=3,4,... and for EACH dimension find the
OPTIMAL k-subset EXHAUSTIVELY (all C(N,k) combos), then locate the peak dimension —
the optimal combination overall. Generalizes pairwise cross-links to high-order.
Framework MATRIX.md §0. $0 LOCAL numpy. Reuses H_1232 ECA substrate + axes + 4-way target.

For each k = 1..N: best_k = argmax over all C(N,k) axis-subsets of held-out macro-AUROC
(4-way Wolfram class, dominance-free). Report best subset + AUROC per dimension, the
marginal gain best_k − best_{k-1}, and the PEAK dimension (first k whose gain < EPS).

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1 HIGH-ORDER-OPTIMUM — the exhaustive optimum sits at dimension k* >= 3 AND the best
                          3-combo beats the best 2-combo by >= EPS (0.01) — i.e. going
                          beyond pairwise (the old matrix limit) genuinely helps.
  H_1234 SUPPORTED iff F1 (the optimal combination is genuinely high-order, k>=3).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff best-3 ≤ best-2 + EPS — pairwise is already
  optimal; high-order combination adds nothing (the matrix's 2D limit was sufficient).

scope: small ECA, proxy-Φ pre-screen (a_phi_iit4_tool · a_scale_honest_scope). seed-fixed.
"""
import os, math, json
from itertools import combinations
import numpy as np
import importlib.util

_spec = importlib.util.spec_from_file_location("h1232", os.path.join(os.path.dirname(__file__), "h1232_research_axis_climb.py"))
h = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(h)
_s2 = importlib.util.spec_from_file_location("h1233", os.path.join(os.path.dirname(__file__), "h1233_dominancefree_axis_climb.py"))
h33 = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(h33)

SEED = 7; np.random.seed(SEED)
AXES = h.AXES; CLASS = h.CLASS; CIDX = h33.CIDX; EPS = 0.01
OUTDIR = os.path.join(os.path.dirname(__file__), "..", ".verdicts", "1234_best_per_dimension")


def main():
    print("=== H_1234 best-per-dimension (exhaustive) ===", flush=True)
    rows = []
    for rule in CLASS:
        for d in h.DENS:
            for sd in h.SEEDS:
                sp = h.eca_run(rule, h.W, h.T, d, sd)
                feats = {"B-PHI":h.phi_proxy(sp),"E-SI":h.savant_index(sp),"F-SYNC":h.sync_param(sp),
                         "G-LZ":h.lz76_simple(sp.flatten()),"density":float(sp.mean()),"col-ent":h.col_entropy(sp)}
                rows.append((CIDX[CLASS[rule]], feats))
    rng = np.random.RandomState(SEED); order = rng.permutation(len(rows)); rows=[rows[i] for i in order]
    ym = np.array([r[0] for r in rows]); feats={a:np.array([r[1][a] for r in rows]) for a in AXES}
    half=len(ym)//2; ytr,yte=ym[:half],ym[half:]
    print(f"[data] {len(rows)} runs · classes {dict((k,int((ym==v).sum())) for k,v in CIDX.items())}", flush=True)
    def Xof(sel,sl): return np.stack([feats[a][sl] for a in sel],axis=1)

    best_per_k = {}
    for k in range(1, len(AXES)+1):
        best_au, best_sub = -1, None
        for sub in combinations(AXES, k):
            au = h33.macro_auroc(Xof(list(sub), slice(0,half)), ytr, Xof(list(sub), slice(half,None)), yte)
            if not math.isnan(au) and au > best_au: best_au, best_sub = au, list(sub)
        best_per_k[k] = {"best_subset": best_sub, "macro_auroc": best_au}
        print(f"  dim k={k}: best={best_sub} macroAUROC={best_au:.4f}", flush=True)

    # peak dimension: first k where best_k − best_{k-1} < EPS
    peak_k = len(AXES); prev = 0.5
    for k in range(1, len(AXES)+1):
        gain = best_per_k[k]["macro_auroc"] - prev
        best_per_k[k]["gain_over_prev"] = gain
        if k >= 2 and gain < EPS: peak_k = k-1; break
        prev = best_per_k[k]["macro_auroc"]
    optimal = best_per_k[peak_k]
    gain_3_over_2 = best_per_k[3]["macro_auroc"] - best_per_k[2]["macro_auroc"] if len(AXES) >= 3 else float("nan")

    f1 = (peak_k >= 3) and (gain_3_over_2 >= EPS)
    supported = bool(f1)
    if supported:
        ruling = f"SUPPORTED: optimal combination is HIGH-ORDER — peak dimension k*={peak_k} {optimal['best_subset']} (macroAUROC {optimal['macro_auroc']:.3f}); best-3 beats best-2 by {gain_3_over_2:+.3f} ⇒ going beyond pairwise (the old 2D matrix) genuinely helps"
    else:
        ruling = f"CLOSED-NEGATIVE: pairwise is optimal — peak dimension k*={peak_k} (best-3 vs best-2 = {gain_3_over_2:+.3f} < {EPS}); the optimal combination is {optimal['best_subset']} (macroAUROC {optimal['macro_auroc']:.3f}). High-order combination adds nothing; the 2D matrix limit was sufficient."

    verdict = {
        "H":"H_1234","title":"best-per-dimension exhaustive combination search","axes":AXES,
        "best_per_dimension":best_per_k,"peak_dimension":peak_k,"optimal_combination":optimal["best_subset"],
        "optimal_macro_auroc":optimal["macro_auroc"],"gain_3_over_2":gain_3_over_2,
        "F1_high_order_optimum":{"peak_k":peak_k,"gain_3_over_2":gain_3_over_2,"bars":"peak_k>=3 AND gain_3>=0.01","pass":bool(f1)},
        "supported":supported,"ruling":ruling,
        "framework":"MATRIX.md §0 — best-per-dimension (차원=조합차수 k, exhaustive)",
        "caveat":"variance-partition Φ-proxy pre-screen (a_phi_iit4_tool); small ECA (a_scale_honest_scope)","seed":SEED,
    }
    print("=== VERDICT ===", flush=True); print(json.dumps(verdict, indent=2), flush=True)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(verdict, open(os.path.join(OUTDIR,"result.json"),"w"), indent=2)
    print(f"[saved] {OUTDIR}/result.json", flush=True)


if __name__ == "__main__":
    main()
