#!/usr/bin/env python3
"""H_9235 fork-A retrieval-value branch — pointer/continuous-cache swap-margin (Fable Step-1 design).

The parametric-value fork-A lane died no-crack (on == pool-shuffle to 3 decimals): a gate-smoothing
backdoor + a value map (W1/W2) that never saw the held-out concepts (non-transferable). Fable's surviving
un-falsified family = RETRIEVAL value: the lane's value is taken FROM the context itself, not from lane
weights, so held-out generalization is by construction and no weight matrix can hide a smoothing/memorization
solution. Cheapest member ($0, inference-only, no gradient, CPU):

  continuous cache (Grave-style / kNN-LM in trunk hidden space):
    at gen position t (predicting tok[t+1]), over prior positions i<t:
      score_i   = <yn_t, yn_i> / T
      p_cache(w)= sum_{i<t : tok[i+1]==w} softmax_i(score)
    p = (1-lambda)*p_trunk + lambda*p_cache
  the value at key yn_i is tok[i+1] = the ACTUAL next byte that followed yn_i in THIS context (non-parametric).

Also Step-0 tied-unembed pooled bias (geometry sanity, no cache): p_bias = softmax(logits + alpha * W_U·LN(c_t))
reusing the trunk unembed — but Step-1 cache is the real shot.

Bar = swap-margin Delta_zero (same as parametric run) with the CORRECTED control:
  - pool-shuffle is INVALID for retrieval (position-permutation-equivariant -> cache survives).
  - fair killer = PAIRING-SHUFFLE: permute the key->value alignment (vals=tok[1:] shuffled vs keys=yn) ->
    destroys retrieval, preserves value marginal.
  - second control = CROSS-DOC cache (keys/vals from a DIFFERENT context).
Taxonomy inverts for a cache: LIT-overlap = POSITIVE CONTROL (a cache that can't win where D's bytes recur is
broken -> INVALID), ZERO-overlap = the real recombination bar. n>=48 pairs (CPU-cheap).

CRACK (pre-registered): EXISTS (lambda,T) with zero-overlap Delta_on>0 bootstrap-CI excluding 0, AND same-(l,T)
Delta_pairshuf CI containing 0, AND lit-overlap Delta_on>0 (positive control passes). Else family dead (scoped).
No tune-to-green: full grid reported with each config's own pairing-shuffle null.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "8")
import sys
import json
import glob
import argparse
import itertools

import numpy as np

_cands = sorted(glob.glob(os.path.expanduser("~/.local/lib/python3.*/site-packages/anima_py"))
                + glob.glob("/usr/local/lib/python3.*/dist-packages/anima_py")
                + glob.glob("/opt/conda/lib/python3.*/site-packages/anima_py"))
BASE = _cands[-1] if _cands else os.path.expanduser("~/.local/lib/python3.12/site-packages/anima_py")
for sub in ("core", "cli"):
    p = os.path.join(BASE, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
import decode
import evaluate as E


def _softmax(x):
    x = x - x.max()
    e = np.exp(x)
    return e / e.sum()


def build_items(n_target):
    """>=n ordered (D,R,Dp) pairs from the 12 SG1 concepts. D=distal(first), R=recent, Dp=swap concept.
    zero-overlap continuation uses kD[2:5] (disjoint from ctx kD[:2]); lit-overlap reuses kD[:2]."""
    C = E._SG1_CONCEPTS
    names = list(C)
    N = len(names)
    pairs = [(i, j) for i in range(N) for j in range(N) if i != j]
    # deterministic spread: stride through the ordered-pair list
    items = []
    stride = max(1, len(pairs) // n_target)
    for k in range(0, len(pairs), stride):
        i, j = pairs[k]
        D, R = names[i], names[j]
        Dp = names[(i + 5) % N]
        if Dp in (D, R):
            Dp = names[(i + 4) % N]
        kD, kR, kDp = C[D], C[R], C[Dp]
        if min(len(kD), len(kDp)) < 5:
            continue
        ctx = "%s: %s %s. %s: %s %s. it " % (D, kD[0], kD[1], R, kR[0], kR[1])
        items.append({
            "D": D, "R": R, "Dp": Dp, "ctx": ctx,
            "match_z": "needs %s and %s and %s" % (kD[2], kD[3], kD[4]),
            "swap_z": "needs %s and %s and %s" % (kDp[2], kDp[3], kDp[4]),
            "match_l": "needs %s and %s" % (kD[0], kD[1]),
            "swap_l": "needs %s and %s" % (kDp[0], kDp[1]),
        })
        if len(items) >= n_target:
            break
    return items


def cache_ce(W, ctx, cont, lam, T, mode="on", rng=None, foreign_tok=None, foreign_yn=None):
    """teacher-forced CE (nat/byte) over the continuation, mixing trunk prob with a continuous cache.
    mode: off | on | pairshuf | crossdoc. Returns mean CE over continuation bytes."""
    cb = ctx.encode("utf-8", "ignore")
    kb = cont.encode("utf-8", "ignore")
    tok = np.array([b for b in (cb + kb)], dtype=np.float64)
    Tn = len(tok)
    yn, logits = decode.clm_forward_hidden_logits(W, tok, Tn)   # pure trunk (lane-OFF)
    yn = np.asarray(yn, dtype=np.float64)
    s = len(cb)
    # cache key/value bank over ALL positions (value at i = tok[i+1], for i in 0..Tn-2)
    keys = yn                                    # [Tn, d]
    vals = np.empty(Tn, dtype=np.int64)
    vals[:Tn - 1] = tok[1:].astype(np.int64)
    vals[Tn - 1] = -1
    if mode == "pairshuf":
        perm = rng.permutation(Tn - 1)           # shuffle key->value alignment over valid positions
        vals = vals.copy()
        vals[:Tn - 1] = vals[:Tn - 1][perm]
    ce = 0.0
    nn = 0
    V = logits.shape[1]
    for t in range(s - 1, Tn - 1):               # logits[t] predicts tok[t+1]
        pt = _softmax(logits[t].astype(np.float64))
        if mode == "off" or lam <= 0.0:
            p = pt
        else:
            if mode == "crossdoc" and foreign_yn is not None:
                kk = foreign_yn                  # [M,d] keys from a different context
                vv = foreign_tok                 # [M] values
                m = kk.shape[0]
                sc = (kk @ yn[t]) / T
                w = _softmax(sc)
                pc = np.zeros(V)
                np.add.at(pc, vv[:m], w)
            else:
                # positions i < t
                if t <= 0:
                    p = pt
                    ce += -np.log(p[int(tok[t + 1])] + 1e-12); nn += 1; continue
                sc = (keys[:t] @ yn[t]) / T       # [t]
                w = _softmax(sc)
                pc = np.zeros(V)
                np.add.at(pc, vals[:t], w)
            p = (1.0 - lam) * pt + lam * pc
        ce += -np.log(p[int(tok[t + 1])] + 1e-12)
        nn += 1
    return ce / max(nn, 1)


def boot_ci(x, iters=2000, seed=1):
    x = np.asarray(x, dtype=np.float64)
    r = np.random.RandomState(seed)
    n = len(x)
    m = np.array([x[r.randint(0, n, n)].mean() for _ in range(iters)])
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def run(out_path, n_pairs, grid_lam, grid_T, ckpt=None):
    ckpt = ckpt or os.path.expanduser("~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm")
    mouth = E._Mouth(ckpt)
    W = mouth.W
    items = build_items(n_pairs)
    print("n_items=%d ckpt=%s" % (len(items), os.path.basename(ckpt)), flush=True)
    # foreign context bank for crossdoc: use item[(k+ n/2) % n]'s context tokens+hiddens
    fyn, ftok = {}, {}
    for k, it in enumerate(items):
        fb = items[(k + len(items) // 2) % len(items)]["ctx"].encode("utf-8", "ignore")
        ft = np.array([b for b in fb], dtype=np.float64)
        fy, _ = decode.clm_forward_hidden_logits(W, ft, len(ft))
        fyn[k] = np.asarray(fy, dtype=np.float64)
        ftok[k] = ft.astype(np.int64)

    # off baseline (config-independent)
    off_z, off_l = [], []
    for it in items:
        off_z.append(cache_ce(W, it["ctx"], it["swap_z"], 0, 1, "off") - cache_ce(W, it["ctx"], it["match_z"], 0, 1, "off"))
        off_l.append(cache_ce(W, it["ctx"], it["swap_l"], 0, 1, "off") - cache_ce(W, it["ctx"], it["match_l"], 0, 1, "off"))
    off_z = np.array(off_z); off_l = np.array(off_l)
    print("off m_zero_mean=%+.4f m_lit_mean=%+.4f" % (off_z.mean(), off_l.mean()), flush=True)

    res = {"ckpt": ckpt, "n": len(items), "off_m_zero_mean": float(off_z.mean()),
           "off_m_lit_mean": float(off_l.mean()), "grid": []}
    crack = False
    for lam, T in itertools.product(grid_lam, grid_T):
        rng = np.random.RandomState(777)
        on_z, on_l, ps_z, cd_z = [], [], [], []
        for k, it in enumerate(items):
            on_z.append(cache_ce(W, it["ctx"], it["swap_z"], lam, T, "on") - cache_ce(W, it["ctx"], it["match_z"], lam, T, "on"))
            on_l.append(cache_ce(W, it["ctx"], it["swap_l"], lam, T, "on") - cache_ce(W, it["ctx"], it["match_l"], lam, T, "on"))
            ps_z.append(cache_ce(W, it["ctx"], it["swap_z"], lam, T, "pairshuf", rng=rng) - cache_ce(W, it["ctx"], it["match_z"], lam, T, "pairshuf", rng=rng))
            cd_z.append(cache_ce(W, it["ctx"], it["swap_z"], lam, T, "crossdoc", foreign_tok=ftok[k], foreign_yn=fyn[k]) - cache_ce(W, it["ctx"], it["match_z"], lam, T, "crossdoc", foreign_tok=ftok[k], foreign_yn=fyn[k]))
        on_z = np.array(on_z); on_l = np.array(on_l); ps_z = np.array(ps_z); cd_z = np.array(cd_z)
        dz = on_z - off_z; dl = on_l - off_l; dps = ps_z - off_z; dcd = cd_z - off_z
        lo, hi = boot_ci(dz); plo, phi = boot_ci(dps)
        llo, lhi = boot_ci(dl)
        cell = {"lam": lam, "T": T,
                "delta_zero_mean": float(dz.mean()), "delta_zero_ci": [lo, hi],
                "delta_lit_mean": float(dl.mean()), "delta_lit_ci": [llo, lhi],
                "delta_pairshuf_mean": float(dps.mean()), "delta_pairshuf_ci": [plo, phi],
                "delta_crossdoc_mean": float(dcd.mean())}
        # crack: zero-overlap on CI>0 AND pairshuf CI contains 0 AND lit-overlap positive control > 0
        cell_crack = (lo > 0 and plo <= 0 <= phi and dl.mean() > 0)
        cell["crack"] = bool(cell_crack)
        crack = crack or cell_crack
        res["grid"].append(cell)
        print("  lam=%.2f T=%.3f | Dz=%+.4f CI[%+.4f,%+.4f] | pairshuf=%+.4f CI[%+.4f,%+.4f] | crossdoc=%+.4f | lit=%+.4f | crack=%s"
              % (lam, T, dz.mean(), lo, hi, dps.mean(), plo, phi, dcd.mean(), dl.mean(), cell_crack), flush=True)
    res["CRACK"] = bool(crack)
    res["verdict"] = ("GREEN retrieval-routing crack" if crack else
                      "no-crack retrieval branch -> frozen-readout class CLOSED (scoped, trunk-side reopen = gamma)")
    json.dump(res, open(out_path, "w"), indent=2)
    print("\n=== POINTER-CACHE RESULT ===\nCRACK=%s -> %s\nDONE -> %s" % (res["CRACK"], res["verdict"], out_path), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--lam", default="0.1,0.2,0.4")
    ap.add_argument("--T", default="0.05,0.1")
    ap.add_argument("--out", default="pointer_cache.json")
    ap.add_argument("--ckpt", default=None)
    a = ap.parse_args()
    run(a.out, a.n, [float(x) for x in a.lam.split(",")], [float(x) for x in a.T.split(",")], ckpt=a.ckpt)
