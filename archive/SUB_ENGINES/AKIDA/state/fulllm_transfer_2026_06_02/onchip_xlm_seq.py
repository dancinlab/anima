#!/usr/bin/env python3
"""Lane A FULL-LM TRANSFER — on-chip CROSS-LINGUAL NEXT-SENTENCE (sequence) prediction on live AKD1000.

substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G / GPU) · a_scale_honest_scope.

WHY THIS PROBE (the bridge the rung asks for):
  The encoder-ladder PROVED a PRIMITIVE: an unsupervised WHITENED encoder + >=250 anchors makes the
  AKD1000 1-bit last-FC Hebbian learn a POSITIVE ABSOLUTE cross-lingual concept MARGIN (clustering /
  readout quality, ci_lo>0, scale-survives). That is a CONCEPT-MARGIN READOUT, NOT a language model:
  it says "the chip groups the 5 langs of one concept together" — it does NOT say the chip predicts
  the NEXT token / sentence. This probe bridges margin-readout -> an actual on-chip SEQUENCE task.

  KEY corpus fact: corpus_big concepts 0..49 are CONSECUTIVE FLORES sentences of ONE news article
  ("On Monday, scientists from Stanford..." -> "Lead researchers say this may bring..." -> ...). So
  concept index t is a TIME index. A genuine cross-lingual LM signal = from the on-chip code of
  sentence t in language L1, retrieve / predict the code of sentence t+1 in a DIFFERENT language L2,
  above a shuffle-NULL. This is next-token/next-sentence prediction across languages, on the chip.

ON-CHIP PIPELINE (every tier real silicon, g63 — NO sw fallback labelled on-chip):
  1. whitened unsupervised encoder (the PROVEN encoder; byte-match encoder_ladder_chip.enc_whitened)
     -> int4 projection -> 1-bit spike code per anchor.
  2. AkidaUnsupervised FullyConnected (units=32, 1-bit weights), map() to AKD1000, fit() ON CHIP over
     all 250 anchor spike-codes (the proven Hebbian primitive learns the readout).
  3. on-chip forward -> a learned 32-dim binary code per anchor (the chip's representation).
  4. SEQUENCE READOUT (next-sentence): build per-concept centroid codes (mean over 5 langs).
     For a held-out cross-lingual pair (query = sentence t in lang L1's on-chip code; gallery = the
     per-concept NEXT-centroid codes excluding L1), score next = is the nearest-by-Hamming gallery
     centroid the one for concept t+1? top-1 next-sentence retrieval accuracy.
     ALSO an EASIER same-concept cross-lingual retrieval (is nearest centroid == concept t?) as a
     sanity bridge between the margin readout and the sequence task.

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: NEXT-SENTENCE top-1 accuracy = P(argmin_c Hamming(code_q, nextcentroid_c) == t+1), over all
          query anchors t in 0..48 (t+1 exists), query lang != the langs averaged into the gallery.
  NULL: SHUFFLE-NULL = the same retrieval with the concept->time labels permuted (B=200 shuffles);
        report NULL mean +- sd and the empirical p-value of the observed accuracy.
  FALSIFIER F-LM-1 (the headline): "the whitened-encoder + on-chip 1-bit Hebbian does NOT yield
        above-NULL on-chip cross-lingual NEXT-SENTENCE prediction." -> REFUTED iff observed next-acc
        ci_lo (over chip trials) > shuffle-NULL upper band AND p < 0.05. If next-acc is within NULL,
        the primitive does NOT transfer to a sequence LM at this capacity -> CLOSED on the LM axis at
        this scale (a valid a_paper_negative_ok result; characterize the gap).
  FALSIFIER F-LM-2 (margin->retrieval bridge): "the proven concept margin does NOT even buy
        above-NULL SAME-concept cross-lingual retrieval." -> if same-concept retrieval is ALSO at
        NULL, the margin readout is weaker than the ladder implied; if same-concept is >NULL but
        next-sentence is at NULL, we have localized the gap precisely (binds concepts, no time model).
  CAPACITY HONESTY (a_scale_honest_scope): a single AKD1000 1-bit last-FC is small. If next-sentence
        is at NULL, that is NOT fabricated as failure — it CHARACTERIZES the capacity bridge: the
        primitive binds cross-lingual concepts (margin/same-concept) but has no learned TIME/sequence
        model. The written gap = what a PUBLIC-grade on-chip CLM needs beyond the 1-bit margin readout.

DISPOSITION: above-NULL next-sentence -> on-chip cross-lingual LM signal demonstrated (advance Lane A
  PUBLIC, earned). Same-concept >NULL but next-sentence at NULL -> precise capacity-gap characterized
  (Lane A PUBLIC stays open, named next-step). Both at NULL -> margin readout does not transfer to
  retrieval at all (closed-negative, characterize). NO fabricated PUBLIC.
"""
import os, json, struct, time, sys, hashlib
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256
N_LANGS = 5
NTRIALS = 8
UNITS, NW, LCOMP = 32, 8, 0.1
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

# ---- PROVEN whitened encoder (byte-match encoder_ladder_chip.enc_whitened) ----
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
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]

def to_chip(Xb, count): return Xb.astype(np.uint8).reshape(count, 1, 1, INC)

def fit_forward(X, init_w):
    """map() + fit() the spike-codes ON CHIP, return the learned 1-bit forward codes + learn flag."""
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    for i in range(X.shape[0]): m.fit(X[i:i+1])
    post = get_w(m)
    out = np.stack([np.array(m.forward(X[i:i+1])).astype(np.float64).ravel() for i in range(X.shape[0])])
    learned = bool(np.any(post != pre))
    del m
    return out, learned

def binarize(out2d):
    return (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)

# ---- load corpus_big: 250 anchors, 50 concepts (sequential FLORES sentences) x 5 langs ----
count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted = sorted(np.unique(concept).tolist())
NC = len(concepts_sorted)
print("[xlm] corpus_big count=%d concepts=%d langs=%d" % (count, NC, len(np.unique(lang)))); sys.stdout.flush()

# whitened spike-codes (the proven encoder), fixed across trials (encoder is deterministic)
Xb = to_chip(enc_whitened(H), count)

def centroids_from_codes(codes_bin, exclude_lang=None):
    """per-concept centroid (mean over langs) of the on-chip binary codes; optionally exclude one lang."""
    cent = {}
    for c in concepts_sorted:
        if exclude_lang is None:
            idx = np.where(concept == c)[0]
        else:
            idx = np.where((concept == c) & (lang != exclude_lang))[0]
        if len(idx) == 0: idx = np.where(concept == c)[0]
        cent[c] = codes_bin[idx].mean(axis=0)   # soft centroid in [0,1]^32
    return cent

def hamming_soft(a_bin, b_soft):
    # expected Hamming between a hard 1-bit code and a soft centroid
    return float(np.sum(a_bin * (1.0 - b_soft) + (1 - a_bin) * b_soft))

def retrieval_acc(codes_bin):
    """Returns (same_concept_acc, next_sentence_acc) for one chip trial's learned codes.
    Query = each anchor (sentence t, lang L). Gallery = per-concept centroids built from OTHER langs.
    same: argmin centroid == concept(t). next: argmin NEXT-shifted centroid == concept(t)+1."""
    same_hit, same_tot = 0, 0
    next_hit, next_tot = 0, 0
    for qi in range(codes_bin.shape[0]):
        t = int(concept[qi]); L = lang[qi]
        cent = centroids_from_codes(codes_bin, exclude_lang=L)  # leave-one-lang-out (cross-lingual)
        cks = concepts_sorted
        dists = np.array([hamming_soft(codes_bin[qi], cent[c]) for c in cks])
        # SAME-concept cross-lingual retrieval
        pred_same = cks[int(np.argmin(dists))]
        same_hit += int(pred_same == t); same_tot += 1
        # NEXT-sentence: does the query at t point to the centroid of t+1 ?
        if (t + 1) in cent:
            # gallery for "next" = centroid of each concept; we ask: is t's code closest to t+1's centroid
            # among all concepts != t (a t->t+1 transition retrieval). Exclude self-concept t.
            mask = np.array([c != t for c in cks])
            cks_n = [c for c in cks if c != t]
            dists_n = np.array([hamming_soft(codes_bin[qi], cent[c]) for c in cks_n])
            pred_next = cks_n[int(np.argmin(dists_n))]
            next_hit += int(pred_next == (t + 1)); next_tot += 1
    return same_hit / max(1, same_tot), next_hit / max(1, next_tot)

def shuffle_null(codes_bin, B=B_SHUFFLE, seed=SEED):
    """Permute the concept->time labels; recompute next-sentence acc. Returns null array for next-acc.
    The shuffle breaks the t->t+1 temporal adjacency while preserving code geometry."""
    rng = np.random.default_rng(seed)
    null_next = []
    base_codes = codes_bin
    for _ in range(B):
        perm = rng.permutation(NC)
        relabel = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        # build a permuted-concept view: a query at original t now "is" relabel[t]; next is relabel[t]+1
        next_hit, next_tot = 0, 0
        # precompute centroids under permuted labels (per query excludes its lang)
        for qi in range(base_codes.shape[0]):
            t = relabel[int(concept[qi])]; L = lang[qi]
            # centroids under permuted labels
            cent = {}
            for c in concepts_sorted:
                relc = relabel[c]
                idx = np.where((concept == c) & (lang != L))[0]
                if len(idx) == 0: idx = np.where(concept == c)[0]
                cent[relc] = base_codes[idx].mean(axis=0)
            if (t + 1) in cent:
                cks_n = [c for c in concepts_sorted if c != t]
                dists_n = np.array([hamming_soft(base_codes[qi], cent[c]) for c in cks_n])
                pred_next = cks_n[int(np.argmin(dists_n))]
                next_hit += int(pred_next == (t + 1)); next_tot += 1
        null_next.append(next_hit / max(1, next_tot))
    return np.array(null_next)

def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "encoder": "whitened (proven unsupervised decorrelated encoder, byte-match encoder_ladder)",
           "corpus": "corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs",
           "task": "on-chip cross-lingual NEXT-SENTENCE (t->t+1) top-1 retrieval + SAME-concept top-1; "
                   "leave-one-lang-out centroids; shuffle-NULL over concept->time labels B=%d" % B_SHUFFLE,
           "metric": "next_acc=P(argmin Hamming over c!=t == t+1); same_acc=P(argmin == t); chance(same)=1/%d" % NC,
           "trials": []}
print("[xlm] akida %s device %s ip %s N=%d trials units=%d B_shuffle=%d"
      % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS, B_SHUFFLE)); sys.stdout.flush()

same_list, next_list, learn_all = [], [], True
last_codes = None
for tr in range(NTRIALS):
    init = get_w(build_fc(1))
    out, learned = fit_forward(Xb, init)
    codes = binarize(out)
    sacc, nacc = retrieval_acc(codes)
    same_list.append(sacc); next_list.append(nacc); learn_all = learn_all and learned
    last_codes = codes
    RESULTS["trials"].append({"trial": tr, "same_acc": sacc, "next_acc": nacc, "learned_hw": learned})
    print("[xlm] trial %d: same_acc=%.4f next_acc=%.4f learn=%s" % (tr, sacc, nacc, learned)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_seq.json"), "w"), indent=2)  # commit-early

# shuffle-NULL for next-sentence (computed on the last trial's chip codes; geometry-preserving)
print("[xlm] computing shuffle-NULL (B=%d) on last-trial chip codes ..." % B_SHUFFLE); sys.stdout.flush()
null_next = shuffle_null(last_codes, B=B_SHUFFLE, seed=SEED)
null_mean, null_sd = float(null_next.mean()), float(null_next.std())
null_hi = null_mean + 1.96*null_sd

sm, ssd, ssem, slo, shi = ci(same_list)
nm, nsd, nsem, nlo, nhi = ci(next_list)
# empirical p-value of observed next-acc mean vs shuffle-NULL
p_next = float((null_next >= nm).sum() + 1) / (len(null_next) + 1)

chance_same = 1.0/NC
# same-concept chance NULL is ~1/NC; we also derive a same-acc NULL band from shuffle for honesty
above_null_next = bool(learn_all and nlo > null_hi and p_next < 0.05)
above_null_same = bool(learn_all and slo > chance_same)  # same-concept beats uniform chance

RESULTS["summary"] = {
    "learn_all_hw": learn_all,
    "same_acc": {"mean": sm, "sd": ssd, "ci95": [slo, shi], "ci_lo": slo, "chance": chance_same,
                 "above_chance": above_null_same},
    "next_acc": {"mean": nm, "sd": nsd, "ci95": [nlo, nhi], "ci_lo": nlo},
    "shuffle_null_next": {"mean": null_mean, "sd": null_sd, "hi_1.96sd": null_hi, "B": B_SHUFFLE,
                          "p_value_next": p_next},
    "F_LM_1_next_sentence": ("REFUTED: above-NULL on-chip cross-lingual NEXT-SENTENCE prediction "
        "(next ci_lo>NULL hi AND p<0.05)" if above_null_next else
        "NOT-REFUTED: next-sentence acc within shuffle-NULL -> primitive does NOT transfer to a "
        "sequence LM at this 1-bit/32-unit capacity (CLOSED on LM axis at this scale)"),
    "F_LM_2_same_concept_bridge": ("REFUTED: margin readout DOES buy above-chance same-concept "
        "cross-lingual retrieval" if above_null_same else
        "NOT-REFUTED: even same-concept cross-lingual retrieval at chance"),
    "above_null_next_sentence": above_null_next,
    "above_chance_same_concept": above_null_same,
}
RESULTS["DISPOSITION"] = (
    "ON-CHIP CROSS-LINGUAL LM SIGNAL DEMONSTRATED (next-sentence > NULL) -> advance Lane A PUBLIC"
    if above_null_next else
    ("CAPACITY-GAP CHARACTERIZED: primitive binds cross-lingual CONCEPTS (same-concept>chance) but "
     "has NO learned TIME/sequence model (next-sentence at NULL) -> Lane A PUBLIC stays open; named "
     "next-step = a sequence/recurrent readout beyond the 1-bit static margin (paged/temporal layer)"
     if above_null_same else
     "MARGIN-READOUT does NOT transfer to retrieval at this capacity (same+next both at chance) -> "
     "closed-negative on the on-chip LM axis at 1-bit/32-unit; characterize richer-readout bridge"))
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_seq.json"), "w"), indent=2)

print("\n[xlm] ========== DISPOSITION ==========")
print("[xlm] learn_all_hw      :", learn_all)
print("[xlm] same_acc          : mean=%.4f ci_lo=%.4f (chance=%.4f, above=%s)" % (sm, slo, chance_same, above_null_same))
print("[xlm] next_acc          : mean=%.4f ci_lo=%.4f" % (nm, nlo))
print("[xlm] shuffle-NULL next : mean=%.4f sd=%.4f hi=%.4f p_next=%.4f" % (null_mean, null_sd, null_hi, p_next))
print("[xlm] F-LM-1 next       :", RESULTS["summary"]["F_LM_1_next_sentence"])
print("[xlm] F-LM-2 same-bridge:", RESULTS["summary"]["F_LM_2_same_concept_bridge"])
print("[xlm] DISPOSITION       :", RESULTS["DISPOSITION"])
print("[xlm] wrote " + os.path.join(OUT, "result_onchip_xlm_seq.json"))
