#!/usr/bin/env python3
"""FREEZE2 screen: latent-factor NON-symmetric interaction world (headroom) for candidate (1).

Reuses the validated micro-autograd + arms from toy_gamma_contrastive.py; only the WORLD changes
(so gamma can be isolated where S_4 gave no headroom). DIRECTIONAL only (torch-free numpy).
"""
import argparse, json
import numpy as np
import toy_gamma_contrastive as core  # micro-autograd + model + train/evaluate

def build_factored(seed, P, C, N, shuffle):
    rng = np.random.default_rng(seed)
    fac = np.array([s % P for s in range(N)])[rng.permutation(N)]   # 4 symbols/factor, shuffled
    R = rng.integers(0, C, size=(P, P))                            # random NON-symmetric table
    pairs = [(a, b) for a in range(N) for b in range(N)]
    if shuffle:
        labels = rng.integers(0, C, size=len(pairs))               # destroys factor structure
        tab = None
    else:
        labels = np.array([R[fac[a], fac[b]] for a, b in pairs])
        tab = R
    order = rng.permutation(len(pairs))
    ntr = int(round(0.40 * len(pairs)))
    tr = set(order[:ntr].tolist())
    # cover every symbol (both slots) AND every factor-pair in train => headroom
    cova, covb, covfp = set(), set(), set()
    for k in tr:
        a, b = pairs[k]; cova.add(a); covb.add(b); covfp.add((fac[a], fac[b]))
    for k in order:
        a, b = pairs[k]; fp = (fac[a], fac[b])
        if a not in cova or b not in covb or fp not in covfp:
            tr.add(k); cova.add(a); covb.add(b); covfp.add(fp)
    tr = sorted(tr); ho = [k for k in range(len(pairs)) if k not in set(tr)]
    return pairs, labels, tr, ho, fac, R

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[0, 1, 2, 3])
    ap.add_argument("--P", type=int, default=6)
    ap.add_argument("--C", type=int, default=12)
    ap.add_argument("--N", type=int, default=24)
    ap.add_argument("--d", type=int, default=24)
    ap.add_argument("--h", type=int, default=64)
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--tau", type=float, default=0.1)
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--out", default="result_factored.json")
    A = ap.parse_args()

    ARMS = ["ADD", "CE", "G_trunk", "G_read"]
    NCLS = A.N  # class-anchor table U must span the C labels; use N>=C anchors, labels in 0..C-1
    out = {"config": vars(A), "runs": {}}
    for shuffle in (False, True):
        tag = "GROUP" if not shuffle else "SHUFFLE"
        print(f"\n########## FACTORED {tag} (N={A.N} P={A.P} C={A.C}, chance={1/A.C:.4f}) ##########", flush=True)
        out["runs"][tag] = {}
        for seed in A.seeds:
            pairs, labels, tr, ho, fac, R = build_factored(seed, A.P, A.C, A.N, shuffle)
            if not shuffle:
                noncomm = [k for k in ho if R[fac[pairs[k][0]], fac[pairs[k][1]]] !=
                           R[fac[pairs[k][1]], fac[pairs[k][0]]]]
            else:
                noncomm = []
            out["runs"][tag][seed] = {"n_train": len(tr), "n_ho": len(ho), "n_ho_noncomm": len(noncomm)}
            print(f"-- seed {seed} | train={len(tr)} heldout={len(ho)} (noncomm={len(noncomm)}) --", flush=True)
            for arm in ARMS:
                P = core.init_params(NCLS, A.d, A.h, seed, arm)
                fl = core.train(P, pairs, labels, tr, arm, A.tau,
                                A.gamma if arm != "CE" else 0.0, A.steps, A.lr)
                tr_acc, _, _, _, _ = core.evaluate(P, pairs, labels, tr, arm, A.tau)
                ho_acc, reach, unreach, pred, y = core.evaluate(P, pairs, labels, ho, arm, A.tau)
                nc_acc = float("nan")
                if noncomm:
                    nc_acc, _, _, _, _ = core.evaluate(P, pairs, labels, noncomm, arm, A.tau)
                distinct = int(np.unique(pred[pred == y]).size)
                out["runs"][tag][seed][arm] = {"train_acc": round(tr_acc, 4), "ho_acc": round(ho_acc, 4),
                    "ho_noncomm_acc": round(nc_acc, 4), "reach": round(reach, 4),
                    "unreach": round(unreach, 5), "distinct": distinct, "final_loss": round(fl, 4)}
                print(f"   {arm:8s} train={tr_acc:.3f} ho={ho_acc:.3f} ho_nc={nc_acc:.3f} "
                      f"reach={reach:.3f} unreach={unreach:.4f} distinct={distinct:2d}", flush=True)

    g = out["runs"]["GROUP"]; sh = out["runs"]["SHUFFLE"]; S = A.seeds; ns = len(S)
    c1 = sum(g[s]["G_trunk"]["ho_acc"] >= g[s]["CE"]["ho_acc"] + 0.10 for s in S)
    c2a = sum(g[s]["G_trunk"]["ho_acc"] >= g[s]["ADD"]["ho_acc"] + 0.15 for s in S)
    c2b = sum((g[s]["ADD"]["ho_noncomm_acc"] <= 0.55) and
              (g[s]["G_trunk"]["ho_noncomm_acc"] > g[s]["ADD"]["ho_noncomm_acc"] + 0.15) for s in S)
    c3 = sum(g[s]["G_trunk"]["ho_acc"] >= g[s]["G_read"]["ho_acc"] + 0.08 for s in S)
    c4_headroom = sum(max(g[s][a]["ho_acc"] for a in ARMS) >= 0.20 for s in S)
    c5_shuf = sum(sh[s]["G_trunk"]["ho_acc"] >= sh[s]["CE"]["ho_acc"] + 0.10 for s in S)
    clauses = {"c1_reach_earned_ge_CE+.10": f"{c1}/{ns}",
               "c2a_DPI_escape_ge_ADD+.15": f"{c2a}/{ns}",
               "c2b_noncomm_ADD<=.55_and_Gtrunk>ADD+.15": f"{c2b}/{ns}",
               "c3_trunk_ne_readout_ge_Gread+.08": f"{c3}/{ns}",
               "c4_headroom_any_arm>=.20 (else INCONCLUSIVE)": f"{c4_headroom}/{ns}",
               "c5_SHUFFLE_advantage_must_vanish (want 0)": f"{c5_shuf}/{ns}"}
    learnable = c4_headroom >= 3
    passed = learnable and (c1 >= 3) and (c2a >= 3) and (c2b >= 3) and (c3 >= 3) and (c5_shuf == 0)
    verdict = "PASS" if passed else ("FAIL" if learnable else "INCONCLUSIVE-no-headroom")
    out["frozen_bar"] = {"clauses": clauses, "verdict": verdict, "step1_gpu_authorized": passed}
    print("\n=== FROZEN BAR (FREEZE2.md) ===", flush=True)
    for k, v in clauses.items(): print(f"  {k}: {v}", flush=True)
    print(f"  => VERDICT: {verdict} | STEP-1 authorized: {passed}", flush=True)
    with open(A.out, "w") as f: json.dump(out, f, indent=2)
    print(f"wrote {A.out}", flush=True)

if __name__ == "__main__":
    main()
