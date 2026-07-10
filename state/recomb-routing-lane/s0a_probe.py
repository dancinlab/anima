#!/usr/bin/env python3
"""H_9264 STEP-0 S0-A — association-accessibility probe (Fable design · $0 CPU · no lane training).

Does the associative payload (concept -> UNSHOWN keyword) exist read-side at ANY tap depth of the frozen 303M
CLMConvMoE trunk? Multi-tap forward (EC/T2/T4/MOE/YN) via anima_py decode helpers (op-for-op mirror of
_fwd_logits; production untouched). For each tap ℓ: pooled doc vector p_ℓ(doc) over the block span, pooled kw
vector q_ℓ(kw) from an isolated forward; a bilinear ridge score = p·M·q trained on 40 train concepts (pos = the
doc-concept's kws incl. 3 UNSHOWN; neg = matched distractor kws), evaluated as held-out-concept AUC on
UNSHOWN-kws vs distractors, cluster-bootstrap by concept. KILL: if unshown-kw AUC CI ≤ chance at EVERY tap, the
associative payload is absent read-side anywhere -> family 🧱, only trunk training (γ) can add it.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import sys
import glob
import json
import argparse

import numpy as np

_c = sorted(glob.glob("/usr/local/lib/python3.*/dist-packages/anima_py"))
BASE = _c[-1] if _c else "/usr/local/lib/python3.11/dist-packages/anima_py"
for sub in ("core", "cli"):
    p = os.path.join(BASE, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
import decode as D
import evaluate as E

TAPS = ("ec", "t2", "t4", "moe", "yn")


def forward_taps(W, tok, T):
    """op-for-op mirror of decode._fwd_logits, collecting intermediate taps. Returns {name:[T,d]}."""
    d = W["d"]; Ex = W["E"]; K = W["K"]; L = W["L"]
    ids = np.asarray(tok).astype(np.int64)
    xe = W["embed"][ids]
    xt = D._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    out = {"ec": xt.copy()}
    dil = 1
    for li in range(L):
        de = dil if dil <= 512 else 512
        h = D._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, de)
        hg = D.nn_gelu_fwd(D.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1))
        xt = xt + hg.reshape(T, d)
        if li + 1 == 2:
            out["t2"] = xt.copy()
        if li + 1 == 4:
            out["t4"] = xt.copy()
        dil *= 2
    logits_r = D._conv1d(xt, W["rWt"], W["rB"], T, d, Ex, 1, 1)
    ex_out = np.empty((Ex, T, d), dtype=np.float64)
    for ej in range(Ex):
        ex_out[ej] = D.nn_gelu_fwd(D._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)).reshape(T, d)
    y = D.nn_moe_router_fwd(logits_r, ex_out, T, Ex, d)
    out["moe"] = y.copy()
    out["yn"] = D.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    return out


def pooled(W, text, lo=None, hi=None):
    """forward `text`; return {tap: mean-pool over [lo,hi) (or whole seq)} as [d] each."""
    tok = np.array([b for b in text.encode("utf-8", "ignore")], dtype=np.float64)
    T = len(tok)
    if T == 0:
        return None
    taps = forward_taps(W, tok, T)
    a, b = (0, T) if lo is None else (lo, hi)
    a = max(0, a); b = min(T, b)
    if b <= a:
        a, b = 0, T
    return {k: v[a:b].mean(0) for k, v in taps.items()}


def _block(concept, shown):
    return "%s: %s %s %s %s %s. " % (concept, shown[0], shown[1], shown[2], shown[3], shown[4])


def cluster_auc(scores, labels, clusters, iters=5000, seed=1):
    """AUC + cluster-bootstrap CI (resample concepts)."""
    s = np.asarray(scores, float); y = np.asarray(labels, int); cl = np.asarray(clusters)
    def auc(sv, yv):
        pos = sv[yv == 1]; neg = sv[yv == 0]
        if len(pos) == 0 or len(neg) == 0:
            return 0.5
        r = np.argsort(np.argsort(np.concatenate([pos, neg])))
        rp = r[:len(pos)].sum() + len(pos)
        return (rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
    base = auc(s, y)
    uniq = list(dict.fromkeys(cl.tolist())); rng = np.random.RandomState(seed)
    idx = {c: np.where(cl == c)[0] for c in uniq}
    bs = []
    for _ in range(iters):
        pick = [uniq[rng.randint(0, len(uniq))] for _ in range(len(uniq))]
        sel = np.concatenate([idx[c] for c in pick])
        bs.append(auc(s[sel], y[sel]))
    return float(base), (float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.expanduser("~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm"))
    ap.add_argument("--bank", default=os.path.expanduser("~/g1_gamma/expanded_concepts.json"))
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/s0a_probe.json"))
    ap.add_argument("--ntrain", type=int, default=16)
    ap.add_argument("--lam", type=float, default=1.0)
    a = ap.parse_args()
    W = E._Mouth(a.ckpt).W
    bank = json.load(open(a.bank))
    names = list(bank)
    ntr = min(a.ntrain, len(names) - 4)
    train, held = names[:ntr], names[ntr:]
    print("concepts: train=%d held=%d · taps=%s" % (len(train), len(held), TAPS), flush=True)

    # kw pooled vectors (isolated forward, whole-seq pool) — cache per unique kw
    kwvec = {}
    def kwv(kw):
        if kw not in kwvec:
            kwvec[kw] = pooled(W, " " + kw + " ")
        return kwvec[kw]
    # doc pooled vectors over block span
    docv = {}
    for i, c in enumerate(names):
        kws = bank[c]; shown = kws[:5]
        blk = _block(c, shown)
        docv[c] = pooled(W, blk, 0, len(blk.encode()))
        for kw in kws:
            kwv(kw)
        if (i + 1) % 6 == 0:
            print("  forwarded %d/%d concepts" % (i + 1, len(names)), flush=True)

    res = {}
    for tap in TAPS:
        # bilinear ridge on vec(M) is d*d≈14M features (infeasible dense) → random-project p,q to r dims
        # (fixed Gaussian), fit ridge on the reduced bilinear outer(p·Rp, q·Rq). Same seed across taps.
        d = docv[train[0]][tap].shape[0]
        Rp = np.random.RandomState(11).randn(d, 48) / np.sqrt(d)
        Rq = np.random.RandomState(12).randn(d, 48) / np.sqrt(d)
        def feat(pv, qv):
            return np.outer(pv @ Rp, qv @ Rq).ravel()
        rng = np.random.RandomState(7)
        Xtr, ytr = [], []
        for c in train:
            p = docv[c][tap]; own = bank[c]
            for kw in own:                                       # pos = concept's own kws (incl unshown)
                Xtr.append(feat(p, kwv(kw)[tap])); ytr.append(1)
            others = [k for oc in train if oc != c for k in bank[oc]]
            for kw in rng.choice(others, size=len(own), replace=False):  # neg = matched distractors
                Xtr.append(feat(p, kwv(kw)[tap])); ytr.append(0)
        Xtr = np.asarray(Xtr); ytr = np.asarray(ytr, float)
        A = Xtr.T @ Xtr + a.lam * np.eye(Xtr.shape[1])
        w = np.linalg.solve(A, Xtr.T @ ytr)
        # held-out eval: unshown-kws (pos) vs matched distractors (neg), per held concept
        sc, lb, cl = [], [], []
        for c in held:
            p = docv[c][tap]; kws = bank[c]; unshown = kws[5:8]
            for kw in unshown:
                sc.append(feat(p, kwv(kw)[tap]) @ w); lb.append(1); cl.append(c)
            others = [k for oc in held if oc != c for k in bank[oc]]
            for kw in rng.choice(others, size=len(unshown), replace=False):
                sc.append(feat(p, kwv(kw)[tap]) @ w); lb.append(0); cl.append(c)
        auc, ci = cluster_auc(sc, lb, cl)
        res[tap] = {"auc": auc, "ci": list(ci), "sig": bool(ci[0] > 0.5)}
        print("  tap=%-4s held-out unshown-kw AUC=%.3f CI[%.3f,%.3f] sig=%s"
              % (tap, auc, ci[0], ci[1], ci[0] > 0.5), flush=True)

    any_sig = any(v["sig"] for v in res.values())
    verdict = ("S0-A: association payload ACCESSIBLE read-side (≥1 tap AUC CI>chance) → proceed S0-B causal floor"
               if any_sig else
               "S0-A: 🧱 KILL — association payload ABSENT read-side at every tap → concept→content assoc not in "
               "303M substrate read-side; only γ trunk-training can add it")
    out = {"taps": res, "any_sig": bool(any_sig), "verdict": verdict}
    json.dump(out, open(a.out, "w"), indent=2)
    print("\n=== S0-A VERDICT ===\n" + verdict, flush=True)


if __name__ == "__main__":
    main()
