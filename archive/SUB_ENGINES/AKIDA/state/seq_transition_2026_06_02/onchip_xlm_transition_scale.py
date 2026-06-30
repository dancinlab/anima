#!/usr/bin/env python3
"""Lane A SEQUENCE/TRANSITION READOUT scale-ladder — on-chip cross-lingual t->t+1 at 25/125/250 anchors.

substrate=AKIDA · a_lane_akida_gpu_split · a_scale_honest_scope (>=3 rungs, REAL FLORES subsets).

PURPOSE: the headline onchip_xlm_transition probe (250 anchors) showed (g5) the EXPLICIT on-chip transition
FC produces an ABOVE-NULL cross-lingual t->t+1 signal (tr_acc 0.2801 ci_lo 0.2600 vs NULL hi 0.0397, p=0.005;
within-lang recall 0.4867 > 1/50). This addendum confirms the sequence signal is SCALE-ROBUST, not a 250-only
artifact, by re-running the SAME on-chip transition pipeline at 3 real scales.

SCALE RUNGS (no fabricated corpus — exactly the encoder_ladder / onchip_xlm_seq construction):
  25  = corpus (hand-seeded 5-concept fixture)  -> chance(tr)=1/4
  125 = corpus_big[:25 concepts] (real FLORES)  -> chance(tr)=1/24
  250 = corpus_big (real FLORES, 50 concepts)   -> chance(tr)=1/49

FALSIFIER (pre-registered): F-TRSCALE: the above-NULL on-chip cross-lingual transition signal HOLDS at every
  rung (tr ci_lo > shuffle-NULL hi AND p<0.05 at 25/125/250). If it COLLAPSES into NULL at any rung, the
  sequence signal is scale-fragile (honest a_scale_honest_scope downgrade). If it holds at all -> the on-chip
  cross-lingual sequence readout is scale-robust (earned Lane A PUBLIC support across the ladder).
g63: HW only, NO sw fallback.
"""
import os, json, struct, time, sys
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256; NTRIALS = 8; UNITS, NW, LCOMP = 64, 8, 0.1
SHIFT = 37; B_SHUFFLE = 200; SEED = 20260602

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

def bind(a, b):
    return (a.astype(np.uint8) ^ np.roll(b.astype(np.uint8), SHIFT)).astype(np.uint8)

def build_fc(wbits=1):
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]

def to_chip(Xb):
    Xb = np.atleast_2d(Xb).astype(np.uint8)
    return Xb.reshape(Xb.shape[0], 1, 1, INC)

def fit_forward(Xtrain, Xeval, init_w):
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    Xt = to_chip(Xtrain)
    for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    Xe = to_chip(Xeval)
    out = np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])
    learned = bool(np.any(post != pre))
    del m
    return out, learned

def binarize(out2d):
    return (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)

def overlap(a_bin, b_soft):
    return float(np.sum(a_bin * b_soft + (1 - a_bin) * (1.0 - b_soft)))

def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

def load_rung(path, max_concepts=None):
    count, recs = read_limen(path)
    concept = np.array([h["concept"] for (h, _) in recs])
    lang = np.array([h["lang"] for (h, _) in recs])
    H = np.stack([byte_hist(p) for (_, p) in recs])
    cs = sorted(np.unique(concept).tolist())
    if max_concepts is not None: cs = cs[:max_concepts]
    keep = np.isin(concept, cs)
    return concept[keep], lang[keep], H[keep], cs

def run_rung(name, concept, lang, H, concepts_sorted):
    langs = sorted(np.unique(lang).tolist()); NC = len(concepts_sorted)
    codes_enc = enc_whitened(H)
    cidx = {(int(concept[i]), lang[i]): i for i in range(len(concept))}
    def code_of(c, l):
        i = cidx.get((c, l)); return codes_enc[i] if i is not None else None
    # train: within-lang consecutive transition-bound codes
    train_codes, train_pairs = [], []
    for l in langs:
        for k in range(NC - 1):
            a, b = code_of(concepts_sorted[k], l), code_of(concepts_sorted[k+1], l)
            if a is None or b is None: continue
            train_codes.append(bind(a, b)); train_pairs.append(concepts_sorted[k])
    train_codes = np.stack(train_codes)
    # eval: cross-lingual t->g candidate probes
    eval_rows = []
    for ti in range(NC - 1):
        t = concepts_sorted[ti]
        for ql in langs:
            a = code_of(t, ql)
            if a is None: continue
            for gi in range(NC):
                g = concepts_sorted[gi]
                if g == t: continue
                idx = np.where((concept == g) & (lang != ql))[0]
                if len(idx) == 0: idx = np.where(concept == g)[0]
                g_bin = (codes_enc[idx].mean(axis=0) >= 0.5).astype(np.uint8)
                eval_rows.append((t, ql, g, ti, bind(a, g_bin)))
    eval_probe_codes = np.stack([r[4] for r in eval_rows])
    n_train = train_codes.shape[0]
    def targets(train_bin):
        tgt = {}
        for k in range(NC - 1):
            c0 = concepts_sorted[k]; rows = [j for j, cc in enumerate(train_pairs) if cc == c0]
            if rows: tgt[c0] = train_bin[rows].mean(axis=0)
        return tgt
    by_q = {}
    for k, (t, ql, g, ti, _) in enumerate(eval_rows): by_q.setdefault((t, ql), []).append((g, ti, k))
    def tr_acc(eval_bin, tgt):
        hit, tot = 0, 0
        for (t, ql), cands in by_q.items():
            ti = cands[0][1]
            if t not in tgt: continue
            succ = concepts_sorted[ti + 1]
            pred = max((overlap(eval_bin[k], tgt[t]), g) for (g, _, k) in cands)[1]
            hit += int(pred == succ); tot += 1
        return hit / max(1, tot), tot
    def wl_recall(train_bin, tgt):
        keys = [c for c in concepts_sorted[:-1] if c in tgt]
        hit, tot = 0, 0
        for k, c0 in enumerate(train_pairs):
            if c0 not in tgt: continue
            pred = max((overlap(train_bin[k], tgt[c]), c) for c in keys)[1]
            hit += int(pred == c0); tot += 1
        return hit / max(1, tot), tot
    tr_list, wl_list, learn_all = [], [], True
    last_eval, last_train = None, None
    for tr in range(NTRIALS):
        init = get_w(build_fc(1))
        both = np.concatenate([train_codes, eval_probe_codes], axis=0)
        out, learned = fit_forward(train_codes, both, init)
        ob = binarize(out); tb, eb = ob[:n_train], ob[n_train:]
        tgt = targets(tb)
        ta, _ = tr_acc(eb, tgt); wl, _ = wl_recall(tb, tgt)
        tr_list.append(ta); wl_list.append(wl); learn_all = learn_all and learned
        last_eval, last_train = eb, tb
        print("[trsc:%s] trial %d tr_acc=%.4f wl=%.4f learn=%s" % (name, tr, ta, wl, learned)); sys.stdout.flush()
    # shuffle-NULL
    rng = np.random.default_rng(SEED); tgt = targets(last_train); null = []
    for _ in range(B_SHUFFLE):
        perm = rng.permutation(NC); succ_map = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for (t, ql), cands in by_q.items():
            if t not in tgt: continue
            pred = max((overlap(last_eval[k], tgt[t]), g) for (g, _, k) in cands)[1]
            hit += int(pred == succ_map[t]); tot += 1
        null.append(hit / max(1, tot))
    null = np.array(null); nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    tm, tsd, _, tlo, thi = ci(tr_list); wm, wsd, _, wlo, whi = ci(wl_list)
    p = float((null >= tm).sum() + 1) / (len(null) + 1)
    chance = 1.0/(NC - 1)
    above = bool(learn_all and tlo > nhi and p < 0.05)
    return {"rung": name, "n_anchors": int(len(concept)), "NC": NC, "units": UNITS,
            "tr_acc": {"mean": tm, "sd": tsd, "ci_lo": tlo, "ci_hi": thi, "chance": chance},
            "within_lang_recall": {"mean": wm, "ci_lo": wlo},
            "shuffle_null": {"mean": nmean, "sd": nsd, "hi_1.96sd": nhi, "B": B_SHUFFLE, "p_value": p},
            "learn_all_hw": learn_all, "above_null": above}

RUNGS = [
    ("25",  os.path.join(ROOT, "corpus", "parallel.limen"), None),
    ("125", os.path.join(ROOT, "corpus_big", "parallel.limen"), 25),
    ("250", os.path.join(ROOT, "corpus_big", "parallel.limen"), 50),
]
RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "binding": "bind(a,b)=a XOR roll(b,%d)" % SHIFT,
           "task": "scale-ladder of EXPLICIT on-chip cross-lingual t->t+1 transition readout (25/125/250)",
           "pre_registered": "F-TRSCALE: above-NULL transition signal HOLDS at all 3 rungs", "rungs": []}
print("[trsc] akida %s device %s" % (akida.__version__, DEV.version)); sys.stdout.flush()
for name, path, mc in RUNGS:
    c, l, H, cs = load_rung(path, mc)
    print("[trsc] === rung %s: anchors=%d concepts=%d ===" % (name, len(c), len(cs))); sys.stdout.flush()
    r = run_rung(name, c, l, H, cs)
    RESULTS["rungs"].append(r)
    print("[trsc] rung %s: tr_acc=%.4f ci_lo=%.4f NULL_hi=%.4f p=%.4f above_null=%s" %
          (name, r["tr_acc"]["mean"], r["tr_acc"]["ci_lo"], r["shuffle_null"]["hi_1.96sd"],
           r["shuffle_null"]["p_value"], r["above_null"])); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_transition_scale.json"), "w"), indent=2)

all_above = all(r["above_null"] for r in RESULTS["rungs"])
RESULTS["F_TRSCALE"] = ("REFUTED-of-null: above-NULL on-chip cross-lingual transition signal HOLDS at all 3 "
    "rungs (25/125/250) -> scale-robust on-chip sequence readout (earned Lane A PUBLIC support)" if all_above else
    "NOT-uniform: the transition signal collapses into NULL at >=1 rung -> scale-fragile (honest downgrade)")
RESULTS["DISPOSITION"] = ("SCALE-ROBUST on-chip cross-lingual SEQUENCE signal across 25/125/250" if all_above else
    "scale-fragile transition signal — see per-rung above_null")
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_transition_scale.json"), "w"), indent=2)
print("\n[trsc] ===== LADDER =====");
for r in RESULTS["rungs"]:
    print("[trsc] %3s anchors=%3d tr_acc=%.4f ci_lo=%.4f NULL_hi=%.4f p=%.4f above=%s" %
          (r["rung"], r["n_anchors"], r["tr_acc"]["mean"], r["tr_acc"]["ci_lo"],
           r["shuffle_null"]["hi_1.96sd"], r["shuffle_null"]["p_value"], r["above_null"]))
print("[trsc] F-TRSCALE:", RESULTS["F_TRSCALE"])
print("[trsc] DISPOSITION:", RESULTS["DISPOSITION"])
print("[trsc] wrote " + os.path.join(OUT, "result_onchip_xlm_transition_scale.json"))
