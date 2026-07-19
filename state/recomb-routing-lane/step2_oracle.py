#!/usr/bin/env python3
"""H_9235 fork-A Step-2 ORACLE-POOL readout — the family-bounding member (Fable pre-registered).

Replaces the LEARNED cross-attention with a FIXED uniform pool over the KNOWN concept-block span (where the
mean-pool probe already reads concept identity at 0.95). Trains ONLY Wo with the identical InfoNCE swap-contrast
loss. This hands routing over for free, so it is the maximally-favorable member: if oracle-pool + swap-contrast
ALSO lands held-out eval Δ≈0 (lit alive), the frozen-final-state readout class is 🧱 terminal — identity is
linearly present in pooled final states but not mappable to target-byte logits transferably across concepts.

block span derived from tok (no re-precompute): concept-name bytes .. first "." after -> [block_lo, block_hi].
Oracle lane bias at position t: c = mean_{i in block}(yn_i);  bias = τ·tanh((c @ Wo)/τ)  (g=1, no gate/attention).
Trains on paired match+2swap (InfoNCE on lane-Δlogp, T=0.1), evals on the 12 held-out geometry-matched concepts.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "8")
import sys
import glob
import json
import math
import argparse

import numpy as np
import torch
import torch.nn.functional as Fnn

_c = sorted(glob.glob(os.path.expanduser("~/.local/lib/python3.*/site-packages/anima_py")))
BASE = _c[-1] if _c else os.path.expanduser("~/.local/lib/python3.12/site-packages/anima_py")
for sub in ("core", "cli"):
    p = os.path.join(BASE, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
sys.path.insert(0, os.path.expanduser("~/g1_gamma"))
import decode
import evaluate as E
import step2_eval as SE               # reuse _EVAL_CONCEPTS, _block, _FIXGAP/_FIXFILL/_FIXSTEM, build_items geometry

DEV = "cuda" if torch.cuda.is_available() else "cpu"
TAU = 8.0; EXCL = 64; T_NCE = 0.1


def block_span(tok, concept):
    """[block_lo, block_hi): concept-name start .. first '.'(46) after it (inclusive)."""
    cb = concept.encode()
    n = len(tok)
    for i in range(n - len(cb)):
        if all(int(tok[i + j]) == cb[j] for j in range(len(cb))):
            lo = i
            for k in range(i + len(cb), n):
                if int(tok[k]) == 46:
                    return lo, k + 1
            return lo, n
    return None


def oracle_bias(Wo, yn, blo, bhi, span_positions):
    """bias[T,V] but only meaningful at span_positions; c = mean yn over [blo,bhi); block must be < t-64 (distal)."""
    c = yn[blo:bhi].mean(0)                                    # [d]
    b = TAU * torch.tanh((c @ Wo) / TAU)                       # [V]  (block-invariant across positions -> broadcast)
    return b


def delta_oracle(Wo, yn, base, tok, span_lo, span_hi, blo, bhi):
    T = yn.shape[0]
    ps = [t for t in range(max(span_lo - 1, 0), min(span_hi - 1, T - 1)) if (t - EXCL) > bhi]
    if not ps:
        return None
    pos = torch.tensor(ps, device=DEV); y = tok[pos + 1]
    b = oracle_bias(Wo, yn, blo, bhi, pos)                     # [V]
    lp_on = Fnn.log_softmax(base[pos] + b[None, :], -1).gather(1, y[:, None]).squeeze(1)
    with torch.no_grad():
        lp_off = Fnn.log_softmax(base[pos], -1).gather(1, y[:, None]).squeeze(1)
    return (lp_on - lp_off).mean()


def load_item(states, rec):
    z = np.load(os.path.join(states, rec["fn"]))
    lo, hi, retr = z["meta"].tolist()
    out = {}
    for v, suf, cc in (("m", "m", rec["concept"]), ("s0", "s0", rec["donors"][0]), ("s1", "s1", rec["donors"][1])):
        tok = z["tok_" + suf].astype(np.int64)
        bs = block_span(tok, cc)
        out[v] = (torch.from_numpy(z["yn_" + suf].astype(np.float32)).to(DEV),
                  torch.from_numpy(z["base_" + suf].astype(np.float32)).to(DEV),
                  torch.from_numpy(tok).to(DEV), bs)
    return out, lo, hi


def geo_eval_oracle(Wo, W, n):
    """geometry-matched swap-margin with the oracle-pool bias on the 12 held-out concepts (block-pool)."""
    items = SE.build_items(n)
    ZM = ("off", "on"); dz = {m: [] for m in ZM}; dl = {m: [] for m in ZM}; clus = []
    Won = Wo.detach().cpu().numpy().astype(np.float64)
    def cont(ctx, tgt, concept, on):
        cb = ctx.encode("utf-8", "ignore"); kb = tgt.encode("utf-8", "ignore")
        tok = np.array([b for b in (cb + kb)], dtype=np.float64); T = len(tok)
        yn, logits = decode.clm_forward_hidden_logits(W, tok, T)
        bs = block_span(tok.astype(np.int64), concept)
        s = len(cb); ce = 0.0; nn = 0
        c = yn[bs[0]:bs[1]].mean(0) if bs else None
        bias = TAU * np.tanh((c @ Won) / TAU) if (on and bs) else None
        for t in range(s - 1, T - 1):
            lg = logits[t].astype(np.float64)
            if bias is not None and (t - EXCL) > (bs[1] if bs else 0):
                lg = lg + bias
            lg = lg - lg.max(); p = np.exp(lg); p /= p.sum()
            ce += -np.log(p[int(tok[t + 1])] + 1e-12); nn += 1
        return ce / max(nn, 1)
    for k, it in enumerate(items):
        D = it["D"]; Dp = it["Dp"]
        # match ctx has D block; swap ctx has Dp block. target fixed = D's kws.
        for on, tagz in ((False, "off"), (True, "on")):
            mz = cont(it["ctx_m"], it["tgt_z"], D, on); sz = cont(it["ctx_s"], it["tgt_z"], Dp, on)
            dz[tagz].append(sz - mz)
            ml = cont(it["ctx_m"], it["tgt_l"], D, on); sl = cont(it["ctx_s"], it["tgt_l"], Dp, on)
            dl[tagz].append(sl - ml)
        clus.append(D)
        if (k + 1) % 20 == 0:
            print("  oracle-eval %d/%d" % (k + 1, len(items)), flush=True)
    Dz = np.array(dz["on"]) - np.array(dz["off"]); Dl = np.array(dl["on"]) - np.array(dl["off"])
    loz, hiz = SE_cluster(Dz, clus); lol, hil = SE_cluster(Dl, clus)
    return {"n": len(items), "delta_zero_mean": float(Dz.mean()), "delta_zero_ci": [loz, hiz],
            "delta_lit_mean": float(Dl.mean()), "delta_lit_ci": [lol, hil],
            "lit_alive": bool(lol > 0), "CRACK": bool(loz > 0 and lol > 0)}


def SE_cluster(vals, clusters, iters=10000, seed=1):
    vals = np.asarray(vals, float); cl = np.array(clusters); uniq = list(dict.fromkeys(cl))
    r = np.random.RandomState(seed); means = []
    for _ in range(iters):
        pick = [uniq[r.randint(0, len(uniq))] for _ in range(len(uniq))]
        sel = np.concatenate([np.where(cl == c)[0] for c in pick]); means.append(vals[sel].mean())
    m = np.array(means); return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", default=os.path.expanduser("~/g1_gamma/step2_paired"))
    ap.add_argument("--ckpt", default=os.path.expanduser("~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm"))
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--n", type=int, default=132)
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/step2_oracle.json"))
    a = ap.parse_args()
    print("DEV=%s" % DEV, flush=True)
    man = json.load(open(os.path.join(a.states, "manifest.json")))
    items = man["items"]
    z0 = np.load(os.path.join(a.states, items[0]["fn"])); V = z0["base_m"].shape[1]; d = z0["yn_m"].shape[1]
    Wo = torch.nn.Parameter(torch.randn(d, V, device=DEV) * 0.01)
    opt = torch.optim.AdamW([Wo], lr=1e-3, weight_decay=0.01)
    import random as _r; rng = _r.Random(0)
    step = 0
    for ep in range(a.epochs):
        rng.shuffle(items); opt.zero_grad(); acc = 0; skip = 0
        for rec in items:
            t, lo, hi = load_item(a.states, rec)
            ds = []
            ok = True
            for v in ("m", "s0", "s1"):
                yn, base, tok, bs = t[v]
                if bs is None:
                    ok = False; break
                dv = delta_oracle(Wo, yn, base, tok, lo, hi, bs[0], bs[1])
                if dv is None:
                    ok = False; break
                ds.append(dv)
            if not ok:
                skip += 1; continue
            L_c = -Fnn.log_softmax(torch.stack(ds) / T_NCE, 0)[0]
            (L_c / a.bs).backward(); acc += 1
            if acc % a.bs == 0:
                torch.nn.utils.clip_grad_norm_([Wo], 1.0); opt.step(); opt.zero_grad(); step += 1
        print("== ep%d Wo=%.4f skip=%d ==" % (ep, Wo.detach().abs().mean().item(), skip), flush=True)
    W = E._Mouth(a.ckpt).W
    print("=== ORACLE GEO-EVAL n=%d ===" % a.n, flush=True)
    res = geo_eval_oracle(Wo, W, a.n)
    res["Wo_norm"] = float(Wo.detach().abs().mean())
    res["verdict"] = ("A: oracle CRACK 🟢" if res["CRACK"] else
                      "C: lit-dead (harness)" if not res["lit_alive"] else
                      "B/TERMINAL: oracle-pool fails => frozen-final-state readout class 🧱")
    json.dump(res, open(a.out, "w"), indent=2)
    print("\n=== ORACLE-POOL RESULT ===", flush=True)
    print("Δzero=%+.4f CI[%+.4f,%+.4f]" % (res["delta_zero_mean"], *res["delta_zero_ci"]), flush=True)
    print("Δlit=%+.4f CI[%+.4f,%+.4f] alive=%s" % (res["delta_lit_mean"], *res["delta_lit_ci"], res["lit_alive"]), flush=True)
    print("Wo_norm=%.4f CRACK=%s -> %s" % (res["Wo_norm"], res["CRACK"], res["verdict"]), flush=True)


if __name__ == "__main__":
    main()
