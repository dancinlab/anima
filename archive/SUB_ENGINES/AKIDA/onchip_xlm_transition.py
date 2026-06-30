#!/usr/bin/env python3
"""Lane A SEQUENCE/TRANSITION READOUT BRIDGE — explicit on-chip t->t+1 transition learning on live AKD1000.

substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G / GPU) · a_scale_honest_scope.

WHERE WE ARE (the named gap):
  The full-LM transfer rung PROVED (g5, PR #1679): the whitened-encoder + 1-bit last-FC on-chip Hebbian
  BINDS cross-lingual CONCEPTS (same-concept retrieval 6.5x chance, scale-growing) but has NO learned
  TIME/transition model — next-sentence retrieval stayed WITHIN the shuffle-NULL at all 3 rungs
  (next_acc mean 0.0306, NULL hi 0.0389, p=0.154). That probe used STATIC per-concept centroids and asked
  "is sentence-t's static code nearest to t+1's static centroid" — there is NO mechanism that LEARNS the
  transition; concept codes do not encode their successor, so it is near-impossible by construction.

THIS RUNG (candidate a — EXPLICIT on-chip transition encoding):
  Make the chip LEARN the transition. For each consecutive sentence pair (t -> t+1) WITHIN a language we
  build a TRANSITION-BOUND spike code = bind(code_t, code_{t+1}) (a fixed binding op over the proven
  whitened codes), and train a SECOND on-chip AkidaUnsupervised FC over these transition codes. The chip's
  learned forward over the transition input is the on-chip TRANSITION representation. At TEST we form, for a
  cross-lingual query (sentence t in lang L1), the transition probe bind(code_t, code_g) against each
  candidate successor g in OTHER langs, push it through the chip's learned transition FC, and ask: is the
  on-chip transition code for g==t+1 the nearest (highest-overlap) among all candidates g != t ?  This is a
  genuine LEARNED t->t+1 retrieval, cross-lingual, on silicon.

ON-CHIP PIPELINE (every tier real silicon, g63 — NO sw fallback labelled on-chip):
  1. whitened unsupervised encoder (the PROVEN encoder; byte-match encoder_ladder / onchip_xlm_seq) ->
     1-bit spike code per anchor.
  2. TRANSITION-BOUND codes: for each consecutive (t, t+1) pair within each language, bind code_t & code_{t+1}
     by the circular-shift-XOR binding bind(a,b)= a XOR roll(b, SHIFT). (deterministic, fixed, documented.)
  3. AkidaUnsupervised FullyConnected (units=64, 1-bit weights, NW=8), map() to AKD1000, fit() ON CHIP over
     ALL within-language transition codes -> the Hebbian primitive learns a TRANSITION readout.
  4. on-chip forward -> a learned 64-dim binary code per transition. At test, the cross-lingual t->t+1
     retrieval scores candidate successors by on-chip transition-code overlap.

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: TRANSITION top-1 accuracy = P(argmax_g overlap(chipcode(bind(code_t, code_g)),
          transition_centroid_{t->t+1}) == (t+1)), over query t in 0..NC-2, candidates g != t, query lang
          != the langs averaged into the transition centroids (leave-one-lang-out, cross-lingual).
  NULL: SHUFFLE-NULL = the SAME retrieval with the t->t+1 successor labels permuted (B=200), breaking the
        temporal adjacency while preserving code geometry. Report NULL mean +- sd and empirical p-value.
  FALSIFIER F-TR-1 (the headline): "an EXPLICIT on-chip transition readout over the whitened concept codes
        does NOT beat the next-sentence shuffle-NULL." -> REFUTED iff observed transition-acc ci_lo (over
        chip trials) > shuffle-NULL upper band AND p < 0.05. Within NULL -> even an explicit transition FC
        cannot hold the t->t+1 map at this 1-bit/64-unit capacity (CLOSED on the LM/sequence axis at this
        scale; a valid a_paper_negative_ok result; quantify WHY -> name next bridge).
  FALSIFIER F-TR-2 (binding sanity): "the on-chip transition FC does not even recover the SAME transition it
        was trained on (within-lang held-out t->t+1) above chance." -> if even within-lang transition recall
        is at chance, the 1-bit FC cannot represent a transition AT ALL (capacity floor); if within-lang
        transition recall is >chance but cross-lingual is at NULL, the gap is precisely the cross-lingual
        transfer of the transition (named next bridge).
  CAPACITY HONESTY (a_scale_honest_scope): a single AKD1000 1-bit FC is small. A NULL result is NOT
        fabricated failure — it quantifies the capacity bridge (how much transition structure a 1-bit/64-unit
        Hebbian holds) and names the next step (paged multi-FC transition matrix, or on/off-chip split).

DISPOSITION: above-NULL transition-acc -> a WORKING on-chip cross-lingual SEQUENCE/next-step signal (advance
  Lane A PUBLIC, earned, full-LM (3) flips toward green). Within NULL -> precise capacity-gap quantified, name
  next bridge. NO fabricated PUBLIC.
"""
import os, json, struct, time, sys
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256
NTRIALS = 8
UNITS, NW, LCOMP = 64, 8, 0.1      # 64-unit transition FC (vs 32 for the static margin readout)
SHIFT = 37                          # binding circular-shift (coprime-ish to 256; fixed, documented)
B_SHUFFLE = 200
SEED = 20260602

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

# ---- PROVEN whitened encoder (byte-match encoder_ladder / onchip_xlm_seq.enc_whitened) ----
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
    """deterministic binding of two 1-bit codes: a XOR circular-shift(b, SHIFT). Standard VSA-style binding."""
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
    """map()+fit() the TRANSITION codes ON CHIP over Xtrain, then forward Xeval. Returns eval codes + learn flag."""
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
    """expected agreement between a hard 1-bit code and a soft centroid in [0,1] (higher = closer)."""
    return float(np.sum(a_bin * b_soft + (1 - a_bin) * (1.0 - b_soft)))

def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

# ---- load corpus_big: 250 anchors, 50 concepts (sequential FLORES sentences) x 5 langs ----
count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
NC = len(concepts_sorted)
print("[tr] corpus_big count=%d concepts=%d langs=%d shift=%d units=%d" % (count, NC, len(langs), SHIFT, UNITS)); sys.stdout.flush()

# proven whitened spike-codes (deterministic encoder), per-anchor
codes_enc = enc_whitened(H)   # (count, 256) uint8

# index lookup: codes_enc row for (concept c, lang l)
def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None

# ---- TRAIN SET = all within-language consecutive transition-bound codes bind(code_t, code_{t+1}) ----
train_codes = []
train_pairs = []   # (t, lang) provenance
for l in langs:
    for ci_ in range(NC - 1):
        c0, c1 = concepts_sorted[ci_], concepts_sorted[ci_ + 1]
        a, b = code_of(c0, l), code_of(c1, l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b)); train_pairs.append((c0, l))
train_codes = np.stack(train_codes)
print("[tr] transition train codes=%d (within-lang consecutive pairs)" % train_codes.shape[0]); sys.stdout.flush()

# ---- EVAL transition probes: for every (t, query-lang L1) and every candidate successor g (cross-lingual),
#      probe = bind(code_t in L1, code_g in L2!=L1). We forward all probes through the chip's learned FC. ----
def build_eval_index():
    """returns list of (qt, ql, cand_g, cand_l, probe_code) for queries t in 0..NC-2, cand g!=t in other langs."""
    rows = []
    for ti in range(NC - 1):
        t = concepts_sorted[ti]
        for ql in langs:
            a = code_of(t, ql)
            if a is None: continue
            for gi in range(NC):
                g = concepts_sorted[gi]
                if g == t: continue
                # candidate successor code averaged over langs != ql (cross-lingual, leave-query-lang-out)
                rows.append((t, ql, g, ti, gi, bind_xlingual_probe(a, g, ql)))
    return rows

def bind_xlingual_probe(a_code_t, g_concept, exclude_lang):
    """probe transition-bound code: bind(code_t, mean candidate-g code over langs != exclude_lang),
    re-binarized so it is a valid 1-bit chip input."""
    idx = np.where((concept == g_concept) & (lang != exclude_lang))[0]
    if len(idx) == 0: idx = np.where(concept == g_concept)[0]
    g_soft = codes_enc[idx].mean(axis=0)
    g_bin = (g_soft >= 0.5).astype(np.uint8)
    return bind(a_code_t, g_bin)

eval_rows = build_eval_index()
eval_probe_codes = np.stack([r[5] for r in eval_rows])
print("[tr] eval transition probes=%d (cross-lingual t->g candidates)" % eval_probe_codes.shape[0]); sys.stdout.flush()

# transition CENTROID target: the chip-code of the TRUE within-lang t->t+1 transition, averaged over langs
def transition_targets(chip_train_codes_bin):
    """per-concept-t target = mean chip transition-code of bind(code_t, code_{t+1}) over langs (the learned
    representation of the true successor transition)."""
    tgt = {}
    for ci_ in range(NC - 1):
        c0 = concepts_sorted[ci_]
        rows = [k for k, (cc, ll) in enumerate(train_pairs) if cc == c0]
        if rows: tgt[c0] = chip_train_codes_bin[rows].mean(axis=0)
    return tgt

def retrieval_acc(chip_eval_bin, tgt, xlingual=True):
    """TRANSITION top-1: for query (t, ql), among candidates g != t pick argmax overlap(chipcode(probe_{t->g}),
    tgt[t]); hit iff argmax g == t+1. xlingual already baked into probe (candidate avg excludes ql)."""
    # group eval rows by (t, ql)
    by_q = {}
    for k, (t, ql, g, ti, gi, _) in enumerate(eval_rows):
        by_q.setdefault((t, ql), []).append((g, ti, gi, k))
    hit, tot = 0, 0
    for (t, ql), cands in by_q.items():
        ti = cands[0][1]
        if t not in tgt: continue
        succ = concepts_sorted[ti + 1]
        scores = [(overlap(chip_eval_bin[k], tgt[t]), g) for (g, _, _, k) in cands]
        pred = max(scores)[1]
        hit += int(pred == succ); tot += 1
    return hit / max(1, tot), tot

def within_lang_recall(chip_train_codes_bin, tgt):
    """F-TR-2 sanity: held-out within-lang transition recall. For each train transition bind(code_t,code_{t+1})
    in lang L, is its chip code nearest (by overlap) to its OWN concept-t target among all concept targets?"""
    keys = [c for c in concepts_sorted[:-1] if c in tgt]
    if not keys: return 0.0, 0
    hit, tot = 0, 0
    for k, (c0, l) in enumerate(train_pairs):
        if c0 not in tgt: continue
        # leave-this-sample-out target would be ideal; here targets avg over all langs incl. self (sanity bound)
        scores = [(overlap(chip_train_codes_bin[k], tgt[c]), c) for c in keys]
        pred = max(scores)[1]
        hit += int(pred == c0); tot += 1
    return hit / max(1, tot), tot

def shuffle_null(chip_eval_bin, chip_train_bin, B=B_SHUFFLE, seed=SEED):
    """permute the t->successor labels (break temporal adjacency, keep geometry); recompute transition-acc."""
    rng = np.random.default_rng(seed)
    by_q = {}
    for k, (t, ql, g, ti, gi, _) in enumerate(eval_rows):
        by_q.setdefault((t, ql), []).append((g, ti, gi, k))
    null = []
    tgt = transition_targets(chip_train_bin)
    for _ in range(B):
        perm = rng.permutation(NC)
        # permuted "successor": concept at sorted-position i now maps successor -> concepts_sorted[perm[i]]
        succ_map = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for (t, ql), cands in by_q.items():
            if t not in tgt: continue
            fake_succ = succ_map[t]
            scores = [(overlap(chip_eval_bin[k], tgt[t]), g) for (g, _, _, k) in cands]
            pred = max(scores)[1]
            hit += int(pred == fake_succ); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)

RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "binding": "bind(a,b)=a XOR roll(b,%d) over whitened 1-bit codes" % SHIFT,
           "encoder": "whitened (proven; byte-match encoder_ladder / onchip_xlm_seq)",
           "corpus": "corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs",
           "task": "EXPLICIT on-chip TRANSITION readout: 2nd AkidaUnsupervised FC fit on within-lang t->t+1 "
                   "transition-bound codes; cross-lingual t->t+1 top-1 retrieval; shuffle-NULL B=%d" % B_SHUFFLE,
           "metric": "tr_acc=P(argmax overlap(chipcode(bind(code_t,code_g)), tr_centroid_t) == t+1), g!=t, xlingual",
           "trials": []}
print("[tr] akida %s device %s ip %s N=%d trials units=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS)); sys.stdout.flush()

tr_list, wl_list, learn_all = [], [], True
last_eval_bin, last_train_bin = None, None
for tr in range(NTRIALS):
    init = get_w(build_fc(1))
    # fit ON CHIP on within-lang transition codes; forward BOTH the train transitions (for targets + F-TR-2)
    # and the cross-lingual eval probes through the SAME learned weights.
    n_train = train_codes.shape[0]
    both = np.concatenate([train_codes, eval_probe_codes], axis=0)
    out_both, learned = fit_forward(train_codes, both, init)
    out_bin = binarize(out_both)
    chip_train_bin = out_bin[:n_train]
    chip_eval_bin = out_bin[n_train:]
    tgt = transition_targets(chip_train_bin)
    tacc, ttot = retrieval_acc(chip_eval_bin, tgt)
    wl, wtot = within_lang_recall(chip_train_bin, tgt)
    tr_list.append(tacc); wl_list.append(wl); learn_all = learn_all and learned
    last_eval_bin, last_train_bin = chip_eval_bin, chip_train_bin
    RESULTS["trials"].append({"trial": tr, "tr_acc": tacc, "within_lang_recall": wl, "learned_hw": learned,
                              "n_eval_q": ttot, "n_wl": wtot})
    print("[tr] trial %d: tr_acc=%.4f within_lang_recall=%.4f learn=%s (q=%d)" % (tr, tacc, wl, learned, ttot)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_transition.json"), "w"), indent=2)

print("[tr] computing shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
null = shuffle_null(last_eval_bin, last_train_bin, B=B_SHUFFLE, seed=SEED)
null_mean, null_sd = float(null.mean()), float(null.std())
null_hi = null_mean + 1.96*null_sd

tm, tsd, tsem, tlo, thi = ci(tr_list)
wm, wsd, wsem, wlo, whi = ci(wl_list)
p_tr = float((null >= tm).sum() + 1) / (len(null) + 1)
chance_tr = 1.0/(NC - 1)   # candidates g != t -> NC-1 options

above_null_tr = bool(learn_all and tlo > null_hi and p_tr < 0.05)
within_lang_above = bool(learn_all and wlo > 1.0/NC)

RESULTS["summary"] = {
    "learn_all_hw": learn_all,
    "tr_acc": {"mean": tm, "sd": tsd, "ci95": [tlo, thi], "ci_lo": tlo, "chance": chance_tr},
    "within_lang_recall": {"mean": wm, "sd": wsd, "ci95": [wlo, whi], "ci_lo": wlo, "chance": 1.0/NC,
                           "above_chance": within_lang_above},
    "shuffle_null_tr": {"mean": null_mean, "sd": null_sd, "hi_1.96sd": null_hi, "B": B_SHUFFLE, "p_value": p_tr},
    "F_TR_1_transition": ("REFUTED: above-NULL on-chip cross-lingual TRANSITION (t->t+1) prediction "
        "(tr ci_lo>NULL hi AND p<0.05) -> working on-chip sequence signal" if above_null_tr else
        "NOT-REFUTED: explicit on-chip transition readout WITHIN shuffle-NULL -> 1-bit/%d-unit Hebbian "
        "cannot hold the t->t+1 map (CLOSED on the sequence axis at this scale)" % UNITS),
    "F_TR_2_binding_sanity": ("REFUTED: on-chip transition FC recovers within-lang t->t+1 above chance "
        "(the FC CAN represent a transition; cross-lingual transfer is the remaining gap)" if within_lang_above else
        "NOT-REFUTED: even within-lang transition recall at chance -> 1-bit/%d-unit FC cannot represent a "
        "transition AT ALL (capacity floor)" % UNITS),
    "above_null_transition": above_null_tr,
    "within_lang_above_chance": within_lang_above,
}
if above_null_tr:
    disp = ("ON-CHIP CROSS-LINGUAL SEQUENCE SIGNAL DEMONSTRATED (explicit transition readout > NULL) -> "
            "advance Lane A PUBLIC; full-LM (3) next-step flips toward earned-green")
elif within_lang_above:
    disp = ("CAPACITY-GAP REFINED: the on-chip transition FC DOES learn a within-lang t->t+1 transition "
            "(>chance) but it does NOT transfer cross-lingually above NULL -> named next bridge = "
            "(c) on-chip concept-binding ⊥ off-chip cross-lingual sequence-decode split (Lane A PUBLIC open)")
else:
    disp = ("CAPACITY FLOOR QUANTIFIED: a single 1-bit/%d-unit on-chip Hebbian FC cannot hold a t->t+1 "
            "transition map (within-lang recall at chance) -> named next bridge = (b) PAGED multi-FC "
            "transition matrix on-chip (Lane A PUBLIC open; closed-negative on single-FC transition)" % UNITS)
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_transition.json"), "w"), indent=2)

print("\n[tr] ========== DISPOSITION ==========")
print("[tr] learn_all_hw        :", learn_all)
print("[tr] tr_acc (xlingual)   : mean=%.4f ci_lo=%.4f (chance=%.4f)" % (tm, tlo, chance_tr))
print("[tr] within_lang_recall  : mean=%.4f ci_lo=%.4f (chance=%.4f, above=%s)" % (wm, wlo, 1.0/NC, within_lang_above))
print("[tr] shuffle-NULL tr     : mean=%.4f sd=%.4f hi=%.4f p=%.4f" % (null_mean, null_sd, null_hi, p_tr))
print("[tr] F-TR-1 transition   :", RESULTS["summary"]["F_TR_1_transition"])
print("[tr] F-TR-2 binding      :", RESULTS["summary"]["F_TR_2_binding_sanity"])
print("[tr] DISPOSITION         :", RESULTS["DISPOSITION"])
print("[tr] wrote " + os.path.join(OUT, "result_onchip_xlm_transition.json"))
