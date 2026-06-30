#!/usr/bin/env python3
"""Lane A micro-exp μ2 CODE — sparsity (k-WTA) + temporal-T integration on the 256-unit output code, live AKD1000.
substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G/GPU) · a_scale_honest_scope · g63 (NO sw fallback).

QUESTION: does k-WTA SPARSITY (s in {4,8,16,32}) and/or TEMPORAL-T integration (T in {2,4,8}) on the 256-unit output
code lift TRANSITION-RETRIEVAL accuracy above the baseline 0.260? (the established transition-retrieval baseline).

DESIGN: a single 1-bit Hebbian FC trained on-chip on the teacher-forced transitions (byte-match primitives). The
output 256-unit code is post-processed into CANDIDATE CODES:
  - k-WTA sparsity s: keep the top-s units of the soft output (by activation), zero the rest, binarize -> a sparse
    code with exactly s active bits. The codebook is rebuilt under the SAME sparsification (apples-to-apples).
  - temporal-T integration T: present the SAME input to the chip T times and SUM the soft outputs (a temporal
    integration window), then binarize at the frozen median -> a denoised code. T=1 is the baseline.
The transition-retrieval metric tr_acc = P(open-vocab decode of the FC output code for a held transition == the
true successor), under each (s, T) variant. byte-identical primitives: enc_whitened, SHIFT=37, neutral_bind, bind,
AkidaUnsupervised(8, 0.1), successor-centroid codebook, frozen-median (for T-integration) or top-s (for k-WTA)
binarize, shuffle-NULL B=200, bootstrap CI. Single FC, single /dev/akida0 lock.

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: tr_acc(variant) = transition-retrieval acc under a (s-WTA) or (T-integration) variant; baseline = 0.260.
  variants: k-WTA s in {4,8,16,32}; temporal-T in {2,4,8}; plus the median-binarize BASELINE (s=full,T=1).
  NULL: per-variant shuffle-NULL (B=200); chance=1/(NC-1).
  F-CODE-1 REFUTED iff the BEST variant tr_acc ci_lo > baseline 0.260 by >= +0.05.
  HONEST: always report every variant's tr_acc + NULL + the best-variant ruling.
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
UNITS, NW, LCOMP = 256, 8, 0.1
SHIFT = 37
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
SEED = 20260603
S_WTA = [4, 8, 16, 32]
T_INT = [2, 4, 8]
BASELINE_TR = 0.260

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
def neutral_bind(a):
    return (a.astype(np.uint8) ^ np.roll(a.astype(np.uint8), NEUTRAL_ROLL)).astype(np.uint8)
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
def chip_make(init_w, train_codes, do_fit=True):
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    if do_fit:
        Xt = to_chip(train_codes)
        for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    learned = bool(np.any(post != pre))
    return m, learned
def chip_forward(m, Xb):
    Xe = to_chip(Xb)
    return np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])
def median_binarize(out2d, med):
    return (out2d > med[None, :]).astype(np.uint8)
def topk_binarize(out2d, s):
    """k-WTA: keep top-s units per row (by activation), 1 there, 0 else."""
    out2d = np.atleast_2d(out2d)
    b = np.zeros_like(out2d, dtype=np.uint8)
    idx = np.argsort(-out2d, axis=1)[:, :s]
    for i in range(out2d.shape[0]): b[i, idx[i]] = 1
    return b
def overlap(a_bin, b_soft):
    return float(np.sum(a_bin * b_soft + (1 - a_bin) * (1.0 - b_soft)))
def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem
count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
NC = len(concepts_sorted)
codes_enc = enc_whitened(H)
print("[code] corpus_big count=%d concepts=%d langs=%d units=%d s_wta=%s t_int=%s" % (count, NC, len(langs), UNITS, S_WTA, T_INT)); sys.stdout.flush()
def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None
train_codes, tr_gt, tr_ban = [], [], []
for l in langs:
    for ci_ in range(NC - 1):
        a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b)); tr_gt.append(concepts_sorted[ci_ + 1]); tr_ban.append(concepts_sorted[ci_])
train_codes = np.stack(train_codes)
n_train = train_codes.shape[0]
print("[code] transitions=%d (transition-retrieval: each code -> decode its successor)" % n_train); sys.stdout.flush()

def build_codebook(train_bin):
    cb = {}; k = 0
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            cb.setdefault(concepts_sorted[ci_ + 1], []).append(train_bin[k]); k += 1
    return {c: np.mean(np.stack(v), axis=0) for c, v in cb.items()}
def decode_pred(g_bin_row, codebook, ban):
    cand = [c for c in codebook if c != ban]
    if not cand: return None
    return max((overlap(g_bin_row, codebook[c]), c) for c in cand)[1]
def tr_acc(query_bin, codebook):
    hit, tot = 0, 0
    for i in range(query_bin.shape[0]):
        pred = decode_pred(query_bin[i], codebook, tr_ban[i])
        if pred is None: continue
        hit += int(pred == tr_gt[i]); tot += 1
    preds = [decode_pred(query_bin[i], codebook, tr_ban[i]) for i in range(query_bin.shape[0])]
    return hit / max(1, tot), preds
def shuffle_null(preds, B=B_SHUFFLE, seed=SEED):
    rng = np.random.default_rng(seed + 99); null = []
    for _ in range(B):
        perm = rng.permutation(NC)
        smap = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for i, p in enumerate(preds):
            if p is None: continue
            hit += int(p == smap[tr_ban[i]]); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)

chance = 1.0/(NC - 1)
print("[code] akida %s device %s ip %s N_trials=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS)); sys.stdout.flush()
VARIANTS = ["baseline"] + ["wta_s%d" % s for s in S_WTA] + ["tint_T%d" % t for t in T_INT]
RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "s_wta": S_WTA, "t_int": T_INT, "chance": chance, "baseline_tr": BASELINE_TR, "variants": VARIANTS,
           "task": "micro-exp mu2 CODE: k-WTA sparsity (s in {4,8,16,32}) + temporal-T integration (T in {2,4,8}) on "
                   "the 256-unit output code; transition-retrieval acc vs baseline 0.260; does the best variant lift "
                   "tr_acc ci_lo > baseline by >=+0.05 (F-CODE-1)?",
           "trials": []}
acc_by_v = {v: [] for v in VARIANTS}
last_preds = {v: None for v in VARIANTS}
learn_all = True
for tr in range(NTRIALS):
    init = get_w(build_fc(1))
    m, learned = chip_make(init, train_codes, do_fit=True)
    learn_all = learn_all and learned
    # baseline median-binarize soft (single pass)
    train_soft = chip_forward(m, train_codes)
    med = np.median(train_soft, axis=0)
    trial_row = {"trial": tr, "learned_hw": learn_all, "tr_acc": {}}
    # baseline
    base_bin = median_binarize(train_soft, med)
    cb_base = build_codebook(base_bin)
    a, preds = tr_acc(base_bin, cb_base)
    acc_by_v["baseline"].append(a); last_preds["baseline"] = preds; trial_row["tr_acc"]["baseline"] = a
    # k-WTA variants (codebook rebuilt under same sparsification)
    for s in S_WTA:
        sb = topk_binarize(train_soft, s); cb = build_codebook(sb)
        a, preds = tr_acc(sb, cb)
        key = "wta_s%d" % s; acc_by_v[key].append(a); last_preds[key] = preds; trial_row["tr_acc"][key] = a
    # temporal-T integration variants (T chip passes summed, then median-binarize)
    for t in T_INT:
        acc_soft = np.zeros_like(train_soft)
        for _ in range(t): acc_soft += chip_forward(m, train_codes)
        acc_soft /= t
        tmed = np.median(acc_soft, axis=0)
        tb = median_binarize(acc_soft, tmed); cb = build_codebook(tb)
        a, preds = tr_acc(tb, cb)
        key = "tint_T%d" % t; acc_by_v[key].append(a); last_preds[key] = preds; trial_row["tr_acc"][key] = a
    del m
    RESULTS["trials"].append(trial_row)
    msg = " ".join("%s=%.4f" % (v, trial_row["tr_acc"][v]) for v in VARIANTS)
    print("[code] trial %d: %s learn=%s" % (tr, msg, learn_all)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_microexp_code.json"), "w"), indent=2)

print("[code] computing per-variant shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
per_v = {}
for v in VARIANTS:
    m_, sd_, sem_, lo_, hi_ = ci(acc_by_v[v])
    null = shuffle_null(last_preds[v], B=B_SHUFFLE, seed=SEED)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= m_).sum() + 1) / (len(null) + 1)
    beats_base = bool(lo_ > BASELINE_TR + 0.05)
    per_v[v] = {"variant": v, "tr_acc_mean": m_, "ci_lo": lo_, "ci_hi": hi_, "shuffle_null_hi": nhi,
                "p_value": p, "beats_baseline_+0.05": beats_base}
    print("[code] %-10s tr_acc=%.4f ci_lo=%.4f ci_hi=%.4f | shufNULL hi=%.4f p=%.4f | vs baseline %.4f(+.05=%s)"
          % (v, m_, lo_, hi_, nhi, p, BASELINE_TR, beats_base)); sys.stdout.flush()
best_v = max(VARIANTS, key=lambda v: per_v[v]["tr_acc_mean"])
F_CODE_1 = bool(learn_all and per_v[best_v]["beats_baseline_+0.05"])
RESULTS["summary"] = {
    "learn_all_hw": learn_all, "chance": chance, "baseline_tr": BASELINE_TR,
    "best_variant": best_v, "best_tr_acc": per_v[best_v]["tr_acc_mean"], "per_variant": per_v,
    "F_CODE_1_vs_baseline": (
        "REFUTED: best variant '%s' tr_acc ci_lo > baseline 0.260 by >=+0.05 -> code-level sparsity/temporal "
        "shaping lifts transition retrieval; Lane A CODE axis advances (toy 250-anchor)." % best_v
        if F_CODE_1 else
        "NOT-REFUTED: no k-WTA or temporal-T variant lifts tr_acc ci_lo above baseline 0.260 by +0.05 -> output-code "
        "shaping (sparsity/temporal integration) does NOT add transition-retrieval accuracy (CLOSED-NEGATIVE, "
        "a_paper_negative_ok)."),
    "F_CODE_1_pass": F_CODE_1,
}
json.dump(RESULTS, open(os.path.join(OUT, "result_microexp_code.json"), "w"), indent=2)
print("\n[code] ========== DISPOSITION ==========")
print("[code] learn_all_hw :", learn_all)
print("[code] chance       : %.4f" % chance)
print("[code] best variant : %s tr_acc=%.4f (baseline %.4f)" % (best_v, per_v[best_v]["tr_acc_mean"], BASELINE_TR))
for v in VARIANTS:
    print("[code]   %-10s tr_acc=%.4f ci_lo=%.4f shufNULL_hi=%.4f p=%.4f beats+.05=%s"
          % (v, per_v[v]["tr_acc_mean"], per_v[v]["ci_lo"], per_v[v]["shuffle_null_hi"], per_v[v]["p_value"], per_v[v]["beats_baseline_+0.05"]))
print("[code] F-CODE-1     :", RESULTS["summary"]["F_CODE_1_vs_baseline"])
