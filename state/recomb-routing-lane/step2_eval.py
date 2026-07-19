#!/usr/bin/env python3
"""H_9235 fork-A Step-2 — PART 3: GEOMETRY-MATCHED swap-margin eval of the trained xattn lane (Fable spec).

The first eval was INVALID (lit dead) because its two-block "D: .. R: .. it" geometry mismatched the lane's
single-block training geometry ("concept: 5kw. GAP STEM target"). Fable adjudication: fix the eval, don't retrain.
Build the swap-margin in the EXACT training doc geometry, swap carried by the concept BLOCK (not the continuation),
R dropped (the [0,t-64) eligibility window already enforces distal-only reading).

Per item (D, Dp both HELD-OUT 8-kw concepts, never in training; blocks byte-length matched; Dp lexically disjoint
from D incl. substrings):
  ctx_match = FILLER + "D: kD0 kD1 kD2 kD3 kD4. " + GAP + STEM        (5 shown kws, training format)
  ctx_swap  = FILLER + "Dp: kP0 kP1 kP2 kP3 kP4. " + GAP + STEM       (identical but Dp's block)
  target_z  = " kD5 kD6 kD7"   (D's UNSHOWN kws — associative; requires routing D-identity, not copy)
  target_l  = " kD0 kD1 kD2"   (D's SHOWN kws — retrieval/copy; POSITIVE CONTROL, must be alive)
  M(target) = CE(target | ctx_swap) - CE(target | ctx_match)          (>0 => match-ctx helps => D present matters)
  Delta     = M_on - M_off
Controls: shufV (lane V rows permuted among eligible), crossdoc (K/V from a foreign ctx). Cluster-bootstrap by D
concept (items sharing a D are correlated). CRACK = CI_lo(Dzero)>0 AND CI_lo(Dzero-DshufV)>0 AND lit alive;
BREAK = Dzero>=+0.10. Also logs gate-fire fraction (mechanistic mismatch check).
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

_c = sorted(glob.glob(os.path.expanduser("~/.local/lib/python3.*/site-packages/anima_py")))
BASE = _c[-1] if _c else os.path.expanduser("~/.local/lib/python3.12/site-packages/anima_py")
for sub in ("core", "cli"):
    p = os.path.join(BASE, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
sys.path.insert(0, os.path.expanduser("~/g1_gamma"))
import decode
import step2_precompute as SP   # training FILLER/STEM/gap + training concept bank (for disjointness)

DH = 256

# 12 HELD-OUT eval concepts, 8 keywords each, chosen disjoint from the training wordbank (asserted below).
_EVAL_CONCEPTS = {
    "reef": ["polyp", "atoll", "lagoon", "coralhead", "zooid", "calcify", "spawning", "bommie"],
    "desert": ["dune", "mirage", "oasis", "scorpion", "sirocco", "playa", "saguaro", "wadi"],
    "cavern": ["stalactite", "gypsum", "sinkhole", "speleothem", "guano", "flowstone", "karst", "grotto"],
    "aviary": ["plumage", "talon", "fledgling", "roost", "preening", "wingspan", "clutch", "molt"],
    "bazaar": ["haggle", "stall", "spice", "caravan", "trinket", "awning", "peddler", "dinar"],
    "geyser": ["sinterbasin", "travertine2", "mudpot", "steamvent", "rhyolite", "sulfurpool", "geothermal", "erupts"],
    "monastery": ["cloister", "vespers", "scriptorium", "abbot", "psalter", "refectory", "tonsure", "matins"],
    "shipyard": ["keelson", "gantry", "drydock", "rivet", "hawser", "stanchion", "bulkhead", "slipway2"],
    "orchestra": ["timpani", "crescendo", "oboe", "arpeggio", "conductor", "pizzicato", "fermata", "tutti"],
    "glacier": ["moraine", "crevasse", "seracs", "firn", "nunatak", "ablation2", "bergschrund", "moulin"],
    "vineyard2": ["terroir", "veraison", "rootstock", "brix", "espalier", "punchdown", "racking", "lees"],
    "telescope2": ["parallax2", "occultation2", "albedo", "coronagraph", "eyepiece2", "azimuth3", "redshift", "collimate"],
}


_exp = os.path.expanduser("~/g1_gamma/expanded_concepts.json")
if os.path.exists(_exp):
    _EVAL_CONCEPTS = json.load(open(_exp))   # high-power expanded bank (existing 12 + Fable-clean) if present


def _assert_disjoint():
    train, val = SP.build_concepts()
    trainwords = set()
    for kws in list(train.values()) + list(val.values()):
        trainwords.update(kws)
    evalwords = set()
    for kws in _EVAL_CONCEPTS.values():
        evalwords.update(kws)
    leak = trainwords & evalwords
    assert not leak, "eval/train keyword leak: %s" % leak
    return trainwords


def _softmax(x):
    x = x - x.max(); e = np.exp(x); return e / e.sum()


class Lane:
    def __init__(self, npz):
        z = np.load(npz)
        self.Wq = z["Wq"].astype(np.float64); self.Wk = z["Wk"].astype(np.float64)
        self.Wv = z["Wv"].astype(np.float64); self.Wo = z["Wo"].astype(np.float64)
        self.a = float(z["a"]); self.b = float(z["b"]); self.tau = float(z["tau"]); self.excl = int(z["excl"])
        self.gate_fires = 0; self.gate_total = 0

    def bias_at(self, yn, t, mode="on", fk=None, fv=None):
        hi = t - self.excl
        if hi <= 0:
            return None
        q = yn[t] @ self.Wq
        if mode == "crossdoc" and fk is not None:
            K = fk; Vv = fv; n = K.shape[0]
        else:
            K = yn[:hi] @ self.Wk; Vv = yn[:hi] @ self.Wv; n = hi
            if mode == "shufV" and n > 1:
                perm = np.random.RandomState(20260709 + n).permutation(n)
                Vv = Vv[perm]
        sc = (K @ q) / math.sqrt(DH)
        A = _softmax(sc)
        ctx = A @ Vv
        H = -(A * np.log(np.clip(A, 1e-12, None))).sum()
        logN = math.log(max(n, 1)) or 1e-6
        g = 1.0 / (1.0 + math.exp(-(self.a * (logN - H) / (logN if logN else 1e-6) + self.b)))
        if mode == "on":
            self.gate_total += 1
            if g > 0.5:
                self.gate_fires += 1
        return g * self.tau * np.tanh((ctx @ self.Wo) / self.tau)


def cont_ce_modes(W, lane, ctx, target, modes, fk=None, fv=None):
    cb = ctx.encode("utf-8", "ignore"); kb = target.encode("utf-8", "ignore")
    tok = np.array([b for b in (cb + kb)], dtype=np.float64)
    T = len(tok)
    yn, logits = decode.clm_forward_hidden_logits(W, tok, T)
    s = len(cb)
    out = {m: 0.0 for m in modes}; nn = 0
    for t in range(s - 1, T - 1):
        base = logits[t].astype(np.float64); y = int(tok[t + 1])
        for m in modes:
            if m == "off":
                lg = base
            else:
                bz = lane.bias_at(yn, t, mode=m, fk=fk, fv=fv)
                lg = base if bz is None else (base + bz)
            lg = lg - lg.max(); p = np.exp(lg); p /= p.sum()
            out[m] += -np.log(p[y] + 1e-12)
        nn += 1
    return {m: out[m] / max(nn, 1) for m in modes}, (yn, s, T)


_FIXGAP = ("and so the note drifts along on unrelated matters touching nothing in particular for quite a while, "
           "simply passing the time while the page slowly fills with words that carry no special weight at all. ")
_FIXFILL = "a quiet log entry opens without fanfare. "
_FIXSTEM = "the next thing that comes to mind is"


def _block(concept, kws):
    return "%s: %s %s %s %s %s. " % (concept, kws[0], kws[1], kws[2], kws[3], kws[4])


def build_items(n_target):
    _assert_disjoint()
    names = list(_EVAL_CONCEPTS); N = len(names)
    items = []
    for dp_off in range(1, N):
        for i in range(N):
            D = names[i]; Dp = names[(i + dp_off) % N]
            if Dp == D:
                continue
            kD = _EVAL_CONCEPTS[D]; kDp = _EVAL_CONCEPTS[Dp]
            # lexical disjoint (incl substring) between Dp's shown block and D's full kw set
            dwords = set(kD)
            if any(any(w in dw or dw in w for dw in dwords) for w in kDp[:5]):
                continue
            bD = _block(D, kD); bDp = _block(Dp, kDp)
            # byte-length match the blocks so GAP/STEM/target sit at identical positions
            if len(bD.encode()) != len(bDp.encode()):
                # pad the shorter block's trailing space region to equalize (keep it parseable)
                diff = len(bD.encode()) - len(bDp.encode())
                if diff > 0:
                    bDp = bDp[:-1] + (" " * diff) + " "
                else:
                    bD = bD[:-1] + (" " * (-diff)) + " "
            ctx_m = _FIXFILL + bD + _FIXGAP + _FIXSTEM
            ctx_s = _FIXFILL + bDp + _FIXGAP + _FIXSTEM
            items.append({"D": D, "Dp": Dp, "ctx_m": ctx_m, "ctx_s": ctx_s,
                          "tgt_z": " %s %s %s" % (kD[5], kD[6], kD[7]),
                          "tgt_l": " %s %s %s" % (kD[0], kD[1], kD[2])})
            if len(items) >= n_target:
                return items
    return items


def cluster_boot(vals, clusters, iters=10000, seed=1):
    """bootstrap resampling CLUSTERS (concepts), not items — items sharing a D are correlated."""
    vals = np.asarray(vals, float)
    cl = np.array(clusters)
    uniq = list(dict.fromkeys(cl))
    r = np.random.RandomState(seed)
    means = []
    for _ in range(iters):
        pick = [uniq[r.randint(0, len(uniq))] for _ in range(len(uniq))]
        sel = np.concatenate([np.where(cl == c)[0] for c in pick])
        means.append(vals[sel].mean())
    m = np.array(means)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.expanduser("~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm"))
    ap.add_argument("--lane", default=os.path.expanduser("~/g1_gamma/step2_lane.npz"))
    ap.add_argument("--n", type=int, default=132)
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/step2_eval.json"))
    import evaluate as E
    a = ap.parse_args()
    mouth = E._Mouth(a.ckpt); W = mouth.W
    lane = Lane(a.lane)
    items = build_items(a.n)
    print("n_items=%d excl=%d (geometry-matched single-block)" % (len(items), lane.excl), flush=True)
    ZM = ("off", "on", "shufV", "crossdoc"); LM = ("off", "on")
    dz = {m: [] for m in ZM}; dl = {m: [] for m in LM}; clus = []
    for k, it in enumerate(items):
        # foreign ctx (shifted) for crossdoc keys/values
        fctx = items[(k + len(items) // 2) % len(items)]["ctx_m"]
        ftok = np.array([b for b in fctx.encode("utf-8", "ignore")], dtype=np.float64)
        fyn, _ = decode.clm_forward_hidden_logits(W, ftok, len(ftok))
        fk = fyn @ lane.Wk; fv = fyn @ lane.Wv
        mz, _ = cont_ce_modes(W, lane, it["ctx_m"], it["tgt_z"], ZM, fk=fk, fv=fv)
        sz, _ = cont_ce_modes(W, lane, it["ctx_s"], it["tgt_z"], ZM, fk=fk, fv=fv)
        for m in ZM:
            dz[m].append(sz[m] - mz[m])
        ml, _ = cont_ce_modes(W, lane, it["ctx_m"], it["tgt_l"], LM, fk=fk, fv=fv)
        sl, _ = cont_ce_modes(W, lane, it["ctx_s"], it["tgt_l"], LM, fk=fk, fv=fv)
        for m in LM:
            dl[m].append(sl[m] - ml[m])
        clus.append(it["D"])
        if (k + 1) % 20 == 0:
            print("  item %d/%d gate_fire=%.2f" % (k + 1, len(items),
                  lane.gate_fires / max(lane.gate_total, 1)), flush=True)
    off = np.array(dz["off"]); offl = np.array(dl["off"])
    Dzero = np.array(dz["on"]) - off
    DshufV = np.array(dz["shufV"]) - off
    Dcross = np.array(dz["crossdoc"]) - off
    Dlit = np.array(dl["on"]) - offl
    lo_z, hi_z = cluster_boot(Dzero, clus); lo_s, hi_s = cluster_boot(DshufV, clus)
    lo_l, hi_l = cluster_boot(Dlit, clus); lo_d, hi_d = cluster_boot(Dzero - DshufV, clus)
    lit_alive = lo_l > 0
    crack = (lo_z > 0) and (lo_d > 0) and lit_alive
    brk = crack and (Dzero.mean() >= 0.10)
    res = {"n": len(items), "gate_fire_frac": lane.gate_fires / max(lane.gate_total, 1),
           "delta_zero_mean": float(Dzero.mean()), "delta_zero_ci": [lo_z, hi_z],
           "delta_shufV_mean": float(DshufV.mean()), "delta_shufV_ci": [lo_s, hi_s],
           "delta_zero_minus_shufV_ci": [lo_d, hi_d], "delta_crossdoc_mean": float(Dcross.mean()),
           "delta_lit_mean": float(Dlit.mean()), "delta_lit_ci": [lo_l, hi_l], "lit_alive": bool(lit_alive),
           "CRACK": bool(crack), "BREAK": bool(brk),
           "verdict": ("A: BREAK wire-candidate 🟢" if brk else
                       "A: CRACK directional 🟢(Δ<0.10)" if crack else
                       "C: INVALID lit-dead (harness — gate/off-by-one/parity)" if not lit_alive else
                       "B: FAIL specificity — lane generic not distal-routing (T2→🟡DIRECTIONAL) 🔴")}
    json.dump(res, open(a.out, "w"), indent=2)
    print("\n=== STEP-2 GEOMETRY-MATCHED SWAP-MARGIN ===", flush=True)
    print("gate_fire_frac=%.3f" % res["gate_fire_frac"], flush=True)
    print("Δzero=%+.4f CI[%+.4f,%+.4f]" % (res["delta_zero_mean"], lo_z, hi_z), flush=True)
    print("ΔshufV=%+.4f CI[%+.4f,%+.4f]" % (res["delta_shufV_mean"], lo_s, hi_s), flush=True)
    print("Δzero-ΔshufV CI[%+.4f,%+.4f]" % (lo_d, hi_d), flush=True)
    print("Δlit=%+.4f CI[%+.4f,%+.4f] alive=%s" % (res["delta_lit_mean"], lo_l, hi_l, lit_alive), flush=True)
    print("Δcrossdoc=%+.4f" % res["delta_crossdoc_mean"], flush=True)
    print("CRACK=%s BREAK=%s -> %s" % (crack, brk, res["verdict"]), flush=True)


if __name__ == "__main__":
    main()
