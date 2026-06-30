#!/usr/bin/env python3
"""Lane A micro-exp μ1 WIDTH — ENSEMBLE of K independent 1-bit Hebbian FCs, on live AKD1000.
substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G/GPU) · a_scale_honest_scope · g63 (NO sw fallback).

QUESTION: does an ENSEMBLE of K independent 1-bit Hebbian FCs (distinct random projections, voted) lift held-out
GENERATION accuracy above the single-FC headline (0.4234)? Each FC trained on-chip SEQUENTIALLY (1 chip, paged).

DESIGN: K FCs, each a distinct column-permutation projection of the same 256-d transition code, each trained
on-chip on the teacher-forced transitions, each producing a 256-unit code -> open-vocab decode. The ensemble
prediction is a PLURALITY VOTE across the K decodes. We measure the SINGLE-STEP (hop-1) generation acc = held-out
next-concept retrieval, the same metric as the single-FC headline. byte-identical primitives to
onchip_xlm_state_rollout.py: enc_whitened, SHIFT=37, neutral_bind, bind, AkidaUnsupervised(8, 0.1), codebook,
frozen-median binarize, shuffle-NULL B=200, bootstrap CI. K FCs paged through 1 chip (single /dev/akida0 lock).

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: gen_acc(K) = plurality-vote open-vocab decode acc of the hop-1 generated code, K in {3,5,7}.
  references: single-FC headline = 0.4234 ; paged-depth-2 hop-1 = 0.1612.
  F-WIDTH-1 REFUTED iff K-ensemble gen_acc ci_lo > single-FC headline 0.4234 by >= +0.05 (for the best K).
  F-WIDTH-2 REFUTED iff K-ensemble gen_acc > paged-depth-2 hop-1 0.1612 (for the best K).
  NULL: per-K shuffle-NULL (B=200); chance=1/(NC-1).
  HONEST: always report the full gen_acc(K) curve + per-K NULL + both falsifier rulings.
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
K_ENS = [3, 5, 7]
HEADLINE_SINGLE_FC = 0.4234
PAGED_DEPTH2_HOP1 = 0.1612

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
def rand_proj(codes_bin, seed):
    codes_bin = np.atleast_2d(codes_bin)
    rng = np.random.default_rng(SEED + 7919 * (seed + 1))
    perm = rng.permutation(INC)
    return codes_bin[:, perm].astype(np.uint8)
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
def binarize_rows(out2d, med):
    return (out2d > med[None, :]).astype(np.uint8)
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
print("[width] corpus_big count=%d concepts=%d langs=%d units=%d K_ens=%s" % (count, NC, len(langs), UNITS, K_ENS)); sys.stdout.flush()
def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None
# teacher-forced transition codes + the START code per transition (for hop-1 generation)
train_codes, gen_inputs, gen_gt, gen_ban = [], [], [], []
for l in langs:
    for ci_ in range(NC - 1):
        a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b))
        gen_inputs.append(neutral_bind(a))         # hop-1 generation input = neutral_bind(start), byte-match
        gen_gt.append(concepts_sorted[ci_ + 1]); gen_ban.append(concepts_sorted[ci_])
train_codes = np.stack(train_codes); gen_inputs = np.stack(gen_inputs)
n_train = train_codes.shape[0]
print("[width] train transitions=%d gen queries=%d" % (n_train, len(gen_gt))); sys.stdout.flush()

def build_codebook(chip_train_bin):
    cb = {}; k = 0
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            cb.setdefault(concepts_sorted[ci_ + 1], []).append(chip_train_bin[k]); k += 1
    return {c: np.mean(np.stack(v), axis=0) for c, v in cb.items()}
def decode_pred(g_bin_row, codebook, ban):
    cand = [c for c in codebook if c != ban]
    if not cand: return None
    return max((overlap(g_bin_row, codebook[c]), c) for c in cand)[1]

def run_one_fc(init, fc_seed):
    """train one ensemble-member FC (distinct projection) on-chip; return per-query hop-1 decoded preds."""
    tr_codes = rand_proj(train_codes, fc_seed)
    m, learned = chip_make(init, tr_codes, do_fit=True)
    train_soft = chip_forward(m, tr_codes)
    med = np.median(train_soft, axis=0)
    codebook = build_codebook(binarize_rows(train_soft, med))
    gi = rand_proj(gen_inputs, fc_seed)
    g_soft = chip_forward(m, gi)
    g_bin = binarize_rows(g_soft, med)
    preds = [decode_pred(g_bin[i], codebook, gen_ban[i]) for i in range(g_bin.shape[0])]
    del m
    return learned, preds
def vote(fc_preds_list):
    n_q = len(fc_preds_list[0]); out = []
    for qi in range(n_q):
        tally = {}
        for preds in fc_preds_list:
            p = preds[qi]
            if p is None: continue
            tally[p] = tally.get(p, 0.0) + 1.0
        out.append(max(tally.items(), key=lambda kv: kv[1])[0] if tally else None)
    return out
def gen_acc(preds):
    hit, tot = 0, 0
    for qi, p in enumerate(preds):
        if p is None: continue
        hit += int(p == gen_gt[qi]); tot += 1
    return hit / max(1, tot), tot
def shuffle_null(preds, B=B_SHUFFLE, seed=SEED):
    rng = np.random.default_rng(seed + 4242); null = []
    starts = [gen_ban[qi] for qi in range(len(preds))]
    for _ in range(B):
        perm = rng.permutation(NC)
        smap = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for qi, p in enumerate(preds):
            if p is None: continue
            hit += int(p == smap[starts[qi]]); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)

chance = 1.0/(NC - 1)
print("[width] akida %s device %s ip %s N_trials=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS)); sys.stdout.flush()
RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "K_ensemble": K_ENS, "chance": chance, "headline_single_fc": HEADLINE_SINGLE_FC,
           "paged_depth2_hop1": PAGED_DEPTH2_HOP1,
           "task": "micro-exp mu1 WIDTH: K independent 1-bit Hebbian FCs (distinct random projection, paged through "
                   "1 chip), plurality-voted hop-1 open-vocab generation acc; does the K-ensemble lift gen_acc above "
                   "the single-FC headline 0.4234 by >=+0.05 (F-WIDTH-1) or above paged-depth-2 0.1612 (F-WIDTH-2)?",
           "trials": []}
acc_by_K = {K: [] for K in K_ENS}
last_voted = {K: None for K in K_ENS}
learn_all = True
for tr in range(NTRIALS):
    fc_preds = []
    init = get_w(build_fc(1))
    for f in range(max(K_ENS)):
        learned, preds = run_one_fc(init, fc_seed=f)
        learn_all = learn_all and learned
        fc_preds.append(preds)
    trial_row = {"trial": tr, "learned_hw": learn_all, "by_K": {}}
    for K in K_ENS:
        voted = vote(fc_preds[:K])
        a, n = gen_acc(voted)
        acc_by_K[K].append(a); last_voted[K] = voted
        trial_row["by_K"][str(K)] = a
    RESULTS["trials"].append(trial_row)
    msg = " ".join("K%d=%.4f" % (K, trial_row["by_K"][str(K)]) for K in K_ENS)
    print("[width] trial %d: %s learn=%s" % (tr, msg, learn_all)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_microexp_width.json"), "w"), indent=2)

print("[width] computing per-K shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
per_K = {}; curve = []
for K in K_ENS:
    m_, sd_, sem_, lo_, hi_ = ci(acc_by_K[K])
    null = shuffle_null(last_voted[K], B=B_SHUFFLE, seed=SEED)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= m_).sum() + 1) / (len(null) + 1)
    beats_headline = bool(lo_ > HEADLINE_SINGLE_FC + 0.05)
    beats_paged2 = bool(m_ > PAGED_DEPTH2_HOP1)
    per_K[str(K)] = {"K": K, "gen_acc_mean": m_, "ci_lo": lo_, "ci_hi": hi_, "shuffle_null_hi": nhi,
                     "p_value": p, "beats_headline_+0.05": beats_headline, "beats_paged_depth2": beats_paged2}
    curve.append(round(m_, 4))
    print("[width] K=%d gen_acc=%.4f ci_lo=%.4f ci_hi=%.4f | shufNULL hi=%.4f p=%.4f | vs headline %.4f(+.05=%s) | vs paged2 %.4f(%s)"
          % (K, m_, lo_, hi_, nhi, p, HEADLINE_SINGLE_FC, beats_headline, PAGED_DEPTH2_HOP1, beats_paged2)); sys.stdout.flush()
best_K = max(K_ENS, key=lambda K: per_K[str(K)]["gen_acc_mean"])
F_WIDTH_1 = bool(learn_all and per_K[str(best_K)]["beats_headline_+0.05"])
F_WIDTH_2 = bool(learn_all and per_K[str(best_K)]["beats_paged_depth2"])
RESULTS["summary"] = {
    "learn_all_hw": learn_all, "chance": chance, "K_ensemble": K_ENS,
    "gen_acc_curve_by_K": curve, "best_K": best_K, "per_K": per_K,
    "F_WIDTH_1_vs_headline": (
        "REFUTED: best-K ensemble gen_acc ci_lo > single-FC headline 0.4234 by >=+0.05 -> WIDTH lifts generation; "
        "Lane A WIDTH axis advances (toy 250-anchor)."
        if F_WIDTH_1 else
        "NOT-REFUTED: K-ensemble gen_acc ci_lo does NOT exceed headline 0.4234 by +0.05 -> voting independent "
        "random-projection FCs does NOT add generation accuracy beyond a single FC (CLOSED-NEGATIVE, a_paper_negative_ok)."),
    "F_WIDTH_2_vs_paged_depth2": (
        "REFUTED: best-K ensemble gen_acc > paged-depth-2 hop-1 0.1612 -> the ensemble at least matches the simple "
        "single-step regime (a width ensemble does not collapse to the depth-2 wall)."
        if F_WIDTH_2 else
        "NOT-REFUTED: K-ensemble gen_acc <= paged-depth-2 hop-1 0.1612 (a_paper_negative_ok)."),
    "F_WIDTH_1_pass": F_WIDTH_1, "F_WIDTH_2_pass": F_WIDTH_2,
}
json.dump(RESULTS, open(os.path.join(OUT, "result_microexp_width.json"), "w"), indent=2)
print("\n[width] ========== DISPOSITION ==========")
print("[width] learn_all_hw   :", learn_all)
print("[width] chance         : %.4f" % chance)
print("[width] gen_acc by K   :", curve, " K=", K_ENS, " best_K=", best_K)
print("[width] F-WIDTH-1      :", RESULTS["summary"]["F_WIDTH_1_vs_headline"])
print("[width] F-WIDTH-2      :", RESULTS["summary"]["F_WIDTH_2_vs_paged_depth2"])
