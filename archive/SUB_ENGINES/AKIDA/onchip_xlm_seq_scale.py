#!/usr/bin/env python3
"""Lane A FULL-LM TRANSFER scale-ladder — on-chip cross-lingual retrieval at 25/125/250 anchors.

substrate=AKIDA · a_lane_akida_gpu_split · a_scale_honest_scope (>=3 rungs, REAL FLORES subsets).

PURPOSE: the headline onchip_xlm_seq probe (250 anchors) showed (g5): same-concept cross-lingual
retrieval is 6.5x chance (margin->retrieval bridge HOLDS) but next-sentence is WITHIN shuffle-NULL
(no learned time/sequence model at 1-bit/32-unit). This addendum confirms BOTH findings are scale-
robust, not a 250-only artifact: it re-runs the SAME on-chip pipeline at 3 real scales.

SCALE RUNGS (no fabricated corpus — exactly the encoder_ladder construction):
  25  = corpus (hand-seeded 5-concept fixture)  -> chance(same)=1/5
  125 = corpus_big[:25 concepts] (real FLORES)  -> chance(same)=1/25
  250 = corpus_big (real FLORES, 50 concepts)   -> chance(same)=1/50

FALSIFIERS (pre-registered):
  F-SCALE-1 (same-concept bridge scales): same-concept retrieval stays ABOVE chance at every rung
        (lift = acc - chance > 0 across 25/125/250). REFUTED-of-null = bridge holds at all scales.
  F-SCALE-2 (next-sentence NULL holds at scale): next-sentence acc stays WITHIN shuffle-NULL at every
        rung. If it CROSSES NULL at any rung -> a sequence signal emerges with scale (would advance
        Lane A PUBLIC). If it stays at NULL across all -> the capacity gap is scale-robust (honest).
g63: HW only, NO sw fallback.
"""
import os, json, struct, time, sys, hashlib
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256; NTRIALS = 8; UNITS, NW, LCOMP = 32, 8, 0.1
B_SHUFFLE = 200; SEED = 20260602

def read_limen(path):
    blob = open(path, "rb").read(); assert blob[:8] == LIMEN_MAGIC
    off = 8; struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off+rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4+hlen].decode()); recs.append((head, rec[4+hlen:]))
    return count, recs

def byte_hist(payload):
    pres = np.zeros(INC, dtype=np.float64)
    for b in payload: pres[b] += 1.0
    return pres

def enc_whitened(H):
    Hc = H - H.mean(axis=0, keepdims=True)
    cov = (Hc.T @ Hc)/max(1, Hc.shape[0]-1) + 1e-3*np.eye(INC)
    w, V = np.linalg.eigh(cov)
    W = V @ np.diag(1.0/np.sqrt(np.maximum(w, 1e-9))) @ V.T
    scale = 7.0/(np.max(np.abs(W))+1e-12)
    Pq = np.clip(np.round(W*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def build_fc(wbits=1):
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

devs = akida.devices()
if not devs: raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device — NO SW fallback")
DEV = devs[0]
def to_chip(Xb, count): return Xb.astype(np.uint8).reshape(count, 1, 1, INC)

def fit_forward(X, init_w):
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    for i in range(X.shape[0]): m.fit(X[i:i+1])
    post = get_w(m)
    out = np.stack([np.array(m.forward(X[i:i+1])).astype(np.float64).ravel() for i in range(X.shape[0])])
    learned = bool(np.any(post != pre)); del m
    return out, learned

def binarize(out2d): return (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
def hamming_soft(a_bin, b_soft): return float(np.sum(a_bin*(1.0-b_soft) + (1-a_bin)*b_soft))

def retrieval(codes_bin, concept, lang, concepts_sorted):
    same_hit = same_tot = next_hit = next_tot = 0
    for qi in range(codes_bin.shape[0]):
        t = int(concept[qi]); L = lang[qi]
        cent = {}
        for c in concepts_sorted:
            idx = np.where((concept == c) & (lang != L))[0]
            if len(idx) == 0: idx = np.where(concept == c)[0]
            cent[c] = codes_bin[idx].mean(axis=0)
        cks = concepts_sorted
        dists = np.array([hamming_soft(codes_bin[qi], cent[c]) for c in cks])
        same_hit += int(cks[int(np.argmin(dists))] == t); same_tot += 1
        if (t+1) in cent:
            cks_n = [c for c in cks if c != t]
            dn = np.array([hamming_soft(codes_bin[qi], cent[c]) for c in cks_n])
            next_hit += int(cks_n[int(np.argmin(dn))] == (t+1)); next_tot += 1
    return same_hit/max(1,same_tot), next_hit/max(1,next_tot)

def shuffle_null_next(codes_bin, concept, lang, concepts_sorted, B=B_SHUFFLE, seed=SEED):
    rng = np.random.default_rng(seed); NC = len(concepts_sorted); nulls = []
    for _ in range(B):
        perm = rng.permutation(NC)
        relabel = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        nh = nt = 0
        for qi in range(codes_bin.shape[0]):
            t = relabel[int(concept[qi])]; L = lang[qi]
            cent = {}
            for c in concepts_sorted:
                idx = np.where((concept == c) & (lang != L))[0]
                if len(idx) == 0: idx = np.where(concept == c)[0]
                cent[relabel[c]] = codes_bin[idx].mean(axis=0)
            if (t+1) in cent:
                cks_n = [c for c in concepts_sorted if c != t]
                dn = np.array([hamming_soft(codes_bin[qi], cent[c]) for c in cks_n])
                nh += int(cks_n[int(np.argmin(dn))] == (t+1)); nt += 1
        nulls.append(nh/max(1,nt))
    return np.array(nulls)

def ci(arr):
    arr = np.array(arr); m = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr)>1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr)>1 else 0.0
    return m, sd, m-1.96*sem, m+1.96*sem

# ---- load 3 scale rungs (real subsets, encoder_ladder construction) ----
def load(name):
    c, recs = read_limen(os.path.join(ROOT, name, "parallel.limen"))
    concept = np.array([h["concept"] for (h,_) in recs]); lang = np.array([h["lang"] for (h,_) in recs])
    H = np.stack([byte_hist(p) for (_,p) in recs]); return c, concept, lang, H

c25, k25, l25, H25 = load("corpus")
c250, k250, l250, H250 = load("corpus_big")
keep = sorted(np.unique(k250).tolist())[:25]; mask = np.isin(k250, keep)
H125, k125, l125 = H250[mask], k250[mask], l250[mask]; c125 = int(mask.sum())

RUNGS = [("c25", c25, k25, l25, H25), ("c125", c125, k125, l125, H125), ("c250", c250, k250, l250, H250)]
RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "task": "scale-ladder of on-chip cross-lingual same-concept + next-sentence retrieval (whitened enc)",
           "n_trials": NTRIALS, "B_shuffle": B_SHUFFLE, "rungs": {}}
print("[scale] akida %s device %s rungs 25/%d/%d" % (akida.__version__, DEV.version, c125, c250)); sys.stdout.flush()

for (name, cnt, concept, lang, H) in RUNGS:
    cs = sorted(np.unique(concept).tolist()); NC = len(cs); chance = 1.0/NC
    Xb = to_chip(enc_whitened(H), cnt)
    same_l, next_l, learn_all, last = [], [], True, None
    for tr in range(NTRIALS):
        init = get_w(build_fc(1)); out, learned = fit_forward(Xb, init); codes = binarize(out)
        s, n = retrieval(codes, concept, lang, cs); same_l.append(s); next_l.append(n)
        learn_all = learn_all and learned; last = codes
        print("[scale] %-5s trial %d same=%.4f next=%.4f learn=%s" % (name, tr, s, n, learned)); sys.stdout.flush()
    null_n = shuffle_null_next(last, concept, lang, cs)
    nm_null, nsd_null = float(null_n.mean()), float(null_n.std())
    sm, ssd, slo, shi = ci(same_l); nm, nsd, nlo, nhi = ci(next_l)
    p_next = float((null_n >= nm).sum()+1)/(len(null_n)+1)
    same_above = bool(learn_all and slo > chance)
    next_above = bool(learn_all and nlo > nm_null+1.96*nsd_null and p_next < 0.05)
    RESULTS["rungs"][name] = {"count": cnt, "n_concepts": NC, "chance_same": chance, "learn_all_hw": learn_all,
        "same_acc": {"mean": sm, "ci_lo": slo, "lift_over_chance": sm-chance, "above_chance": same_above},
        "next_acc": {"mean": nm, "ci_lo": nlo}, "shuffle_null_next": {"mean": nm_null, "sd": nsd_null,
            "hi": nm_null+1.96*nsd_null, "p_value": p_next}, "next_above_null": next_above}
    print("[scale] %-5s SAME mean=%.4f ci_lo=%.4f chance=%.4f above=%s | NEXT mean=%.4f null=%.4f p=%.4f above=%s"
          % (name, sm, slo, chance, same_above, nm, nm_null, p_next, next_above)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_scale.json"), "w"), indent=2)

order = ["c25", "c125", "c250"]
same_lift_curve = [RESULTS["rungs"][s]["same_acc"]["lift_over_chance"] for s in order]
next_above_any = any(RESULTS["rungs"][s]["next_above_null"] for s in order)
same_above_all = all(RESULTS["rungs"][s]["same_acc"]["above_chance"] for s in order)
RESULTS["disposition"] = {
    "same_lift_over_chance_curve_25_125_250": same_lift_curve,
    "F_SCALE_1_bridge_scales": ("CONFIRMED: same-concept retrieval above chance at ALL 3 rungs"
        if same_above_all else "PARTIAL: bridge above chance at some but not all rungs"),
    "F_SCALE_2_next_sentence": ("CROSSES-NULL at >=1 rung -> sequence signal emerges with scale (Lane A PUBLIC candidate)"
        if next_above_any else "NULL HOLDS at every rung -> capacity gap (no time model) is scale-robust"),
    "bottom_line": ("on-chip cross-lingual LM (sequence) signal emerges with scale" if next_above_any
        else "scale-robust: margin->concept-retrieval bridge holds; next-sentence/time model absent at 1-bit/32-unit")}
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_scale.json"), "w"), indent=2)
print("\n[scale] ===== DISPOSITION =====")
print("[scale] same-lift curve 25/125/250:", same_lift_curve)
print("[scale] F-SCALE-1:", RESULTS["disposition"]["F_SCALE_1_bridge_scales"])
print("[scale] F-SCALE-2:", RESULTS["disposition"]["F_SCALE_2_next_sentence"])
print("[scale] BOTTOM LINE:", RESULTS["disposition"]["bottom_line"])
print("[scale] wrote " + os.path.join(OUT, "result_onchip_xlm_scale.json"))
