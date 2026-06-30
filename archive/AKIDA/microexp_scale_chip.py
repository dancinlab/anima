#!/usr/bin/env python3
"""Lane A micro-exp μ3 SCALE — capacity-bound vs algorithm-bound, on live AKD1000.
substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G/GPU) · a_scale_honest_scope · g63 (NO sw fallback).

QUESTION: does multi-FC TILING (N independent on-chip FCs, paged/sequential on the 1 chip, routed+voted) lift the
multi-hop wall (the hop-2 collapse) as N grows? Paging N FCs through ONE chip = the closed paged-depth primitive
applied to WIDTH. BE EXPLICIT if it reduces to the closed result.

DESIGN: N independent FCs, each a distinct random PROJECTION (column permutation) of the same 256-d code (distinct
seed per FC), each trained on-chip on the SAME teacher-forced transitions, each producing a 256-unit code; the
per-hop prediction is a PLURALITY VOTE across the N FC decodes (open-vocab full-codebook, ban-set). Everything else
byte-identical to onchip_xlm_state_rollout.py: enc_whitened, SHIFT=37, neutral_bind, bind,
AkidaUnsupervised(num_weights=8, lc=0.1), successor-centroid codebook, frozen-median binarize, K_ROLL=3,
shuffle-NULL B=200, bootstrap CI. STATELESS feedback (byte-match PR#1686 baseline) so any lift is attributable to
WIDTH, not state. N FCs paged through the single chip one at a time (single /dev/akida0 lock; never two at once).

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: hop2_acc(N) = plurality-vote open-vocab decode acc at hop-2 over N tiled FCs, N in {1,2,4}.
  NULL: per-(N,hop) shuffle-NULL (B=200) on the voted preds; chance=1/(NC-1).
  F-SCALE-1 (capacity-bound, multi-chip WOULD help) -> REFUTED iff hop-2 above-NULL acc scales MONOTONICALLY with
    N (N in {1,2,4}) AND at N=4 hop-2 ci_lo > shuffle-NULL hi at p<=0.01.
  ELSE F-SCALE-0 (algorithm-bound = multi-chip won't help, confirms TERMINAL): hop-2 does NOT scale with N / N=4
    does not clear the NULL -> the wall is algorithmic; tiling (the closed paged-WIDTH primitive) does not lift it.
  HONEST: always report the full hop2_acc(N) curve + per-N shuffle-NULL + monotonicity + the N=4 ruling.
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
K_ROLL = 3
SEED = 20260603
N_TILES = [1, 2, 4]

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
    """distinct random projection per tile FC: permute the 256 bit-columns by a tile-specific permutation
    (a bijective, information-preserving distinct view -> distinct learned FC). seed-driven, deterministic."""
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
print("[scale] corpus_big count=%d concepts=%d langs=%d shift=%d units=%d K=%d N_tiles=%s" %
      (count, NC, len(langs), SHIFT, UNITS, K_ROLL, N_TILES)); sys.stdout.flush()
def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None
train_codes = []
for l in langs:
    for ci_ in range(NC - 1):
        a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b))
train_codes = np.stack(train_codes)
n_train = train_codes.shape[0]
roll_starts = []
for ti in range(NC - K_ROLL):
    for ql in langs:
        a = code_of(concepts_sorted[ti], ql)
        if a is None: continue
        roll_starts.append((ti, ql, a))
print("[scale] train transitions=%d rollout starts=%d" % (n_train, len(roll_starts))); sys.stdout.flush()

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

def run_one_fc(init, tile_seed):
    """train one tiled FC (distinct projection) on-chip; return per-hop decode preds for every rollout start —
    paged through the single chip (one FC at a time)."""
    tr_codes = rand_proj(train_codes, tile_seed)
    m, learned = chip_make(init, tr_codes, do_fit=True)
    train_soft = chip_forward(m, tr_codes)
    med = np.median(train_soft, axis=0)
    chip_train_bin = binarize_rows(train_soft, med)
    codebook = build_codebook(chip_train_bin)
    per_start = []  # per roll_start: list over K of (ti,ql,pred)
    for (ti, ql, seed_code) in roll_starts:
        x = neutral_bind(rand_proj(seed_code, tile_seed)[0])
        banned = concepts_sorted[ti]
        hops = []
        for k in range(K_ROLL):
            g_soft = chip_forward(m, x)
            g_bin = binarize_rows(g_soft, med)[0]
            pred = decode_pred(g_bin, codebook, banned)
            hops.append((ti, ql, pred))
            banned = pred if pred is not None else banned
            x = neutral_bind(g_bin)
        per_start.append(hops)
    del m
    return learned, per_start

def vote_preds(fc_per_starts, k0):
    N = len(fc_per_starts); out = []
    for si in range(len(fc_per_starts[0])):
        ti, ql, _ = fc_per_starts[0][si][k0]
        tally = {}
        for f in range(N):
            p = fc_per_starts[f][si][k0][2]
            if p is None: continue
            tally[p] = tally.get(p, 0.0) + 1.0
        pred = max(tally.items(), key=lambda kv: kv[1])[0] if tally else None
        out.append((ti, ql, pred))
    return out
def acc_at(preds, k0):
    hit, tot = 0, 0
    for (ti, ql, pred) in preds:
        if pred is None: continue
        hit += int(pred == concepts_sorted[ti + k0 + 1]); tot += 1
    return hit / max(1, tot), tot
def shuffle_null(preds, k0, B=B_SHUFFLE, seed=SEED):
    rng = np.random.default_rng(seed + 1009 * (k0 + 1)); null = []
    for _ in range(B):
        perm = rng.permutation(NC)
        smap = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for (ti, ql, pred) in preds:
            if pred is None: continue
            hit += int(pred == smap[concepts_sorted[ti]]); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)

chance = 1.0/(NC - 1)
print("[scale] akida %s device %s ip %s N_trials=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS)); sys.stdout.flush()
RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "K_roll": K_ROLL, "N_tiles": N_TILES, "chance": chance,
           "task": "micro-exp mu3 SCALE: N independent tiled on-chip FCs (distinct random projection, paged through "
                   "1 chip), plurality-voted open-vocab decode; stateless feedback (byte-match PR#1686); does hop-2 "
                   "above-NULL acc scale monotonically with N and clear the NULL at N=4 (p<=0.01)?",
           "stateless_baseline_PR1686": [0.4287, 0.0277, 0.0090], "trials": []}
acc_by_N = {N: [[] for _ in range(K_ROLL)] for N in N_TILES}
last_voted = {N: None for N in N_TILES}
learn_all = True
for tr in range(NTRIALS):
    fc_starts = []
    init = get_w(build_fc(1))
    for f in range(max(N_TILES)):
        learned, per_start = run_one_fc(init, tile_seed=f)
        learn_all = learn_all and learned
        fc_starts.append(per_start)
    trial_row = {"trial": tr, "learned_hw": learn_all, "by_N": {}}
    for N in N_TILES:
        sub = fc_starts[:N]; accs = []
        for k0 in range(K_ROLL):
            a, n = acc_at(vote_preds(sub, k0), k0)
            acc_by_N[N][k0].append(a); accs.append(a)
        last_voted[N] = [vote_preds(sub, kk) for kk in range(K_ROLL)]
        trial_row["by_N"][str(N)] = accs
    RESULTS["trials"].append(trial_row)
    msg = " ".join("N%d=%s" % (N, ["%.4f" % x for x in trial_row["by_N"][str(N)]]) for N in N_TILES)
    print("[scale] trial %d: %s learn=%s" % (tr, msg, learn_all)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_microexp_scale.json"), "w"), indent=2)

print("[scale] computing per-(N,hop) shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
per_N = {}; hop2_curve = []; hop2_above = []
for N in N_TILES:
    hops = []
    for k0 in range(K_ROLL):
        m_, sd_, sem_, lo_, hi_ = ci(acc_by_N[N][k0])
        null = shuffle_null(last_voted[N][k0], k0, B=B_SHUFFLE, seed=SEED)
        nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
        p = float((null >= m_).sum() + 1) / (len(null) + 1)
        above01 = bool(learn_all and lo_ > nhi and p <= 0.01)
        hops.append({"hop": k0+1, "acc_mean": m_, "ci_lo": lo_, "ci_hi": hi_,
                     "shuffle_null_hi": nhi, "p_value": p, "above_null_p01": above01})
        print("[scale] N=%d hop %d: acc=%.4f ci_lo=%.4f | shufNULL hi=%.4f p=%.4f | chance=%.4f | aboveNULL(p<=.01)=%s"
              % (N, k0+1, m_, lo_, nhi, p, chance, above01)); sys.stdout.flush()
    per_N[str(N)] = hops
    hop2_curve.append(round(hops[1]["acc_mean"], 4)); hop2_above.append(hops[1]["above_null_p01"])
mono = all(hop2_curve[i+1] >= hop2_curve[i] - 1e-9 for i in range(len(hop2_curve)-1))
n4_clears = per_N[str(N_TILES[-1])][1]["above_null_p01"]
F_SCALE_1 = bool(mono and n4_clears)
RESULTS["summary"] = {
    "learn_all_hw": learn_all, "chance": chance, "N_tiles": N_TILES,
    "hop2_acc_curve_by_N": hop2_curve, "hop2_above_null_by_N": hop2_above,
    "hop2_monotonic_in_N": mono, "N4_hop2_clears_null_p01": n4_clears, "per_N": per_N,
    "F_SCALE_1_capacity_bound": (
        "REFUTED(capacity-bound): hop-2 above-NULL acc scales MONOTONICALLY with N AND N=4 hop-2 ci_lo>shuffle-NULL "
        "hi at p<=0.01 -> the multi-hop wall is CAPACITY-bound; multi-chip tiling WOULD help. Lane A WIDTH/SCALE "
        "axis advances (toy 250-anchor, paged-WIDTH primitive)."
        if F_SCALE_1 else
        "F-SCALE-0 (algorithm-bound, TERMINAL confirmed): hop-2 acc does NOT scale monotonically with N and/or N=4 "
        "does NOT clear the shuffle-NULL at p<=0.01 -> the multi-hop wall is ALGORITHMIC, not capacity; tiling "
        "(paging N FCs through 1 chip = the closed paged-WIDTH primitive) does NOT lift it -> multi-chip won't help. "
        "CLOSED-NEGATIVE (a_paper_negative_ok). Reduces to the closed paged-depth result applied to width: voting "
        "independent stateless FCs cannot manufacture cross-hop transition structure that no single FC has."),
    "F_SCALE_1_pass": F_SCALE_1,
}
json.dump(RESULTS, open(os.path.join(OUT, "result_microexp_scale.json"), "w"), indent=2)
print("\n[scale] ========== DISPOSITION ==========")
print("[scale] learn_all_hw      :", learn_all)
print("[scale] chance            : %.4f" % chance)
print("[scale] hop2 acc by N     :", hop2_curve, " N=", N_TILES)
print("[scale] hop2 aboveNULL byN:", hop2_above)
print("[scale] hop2 monotonic    :", mono, " | N=4 clears NULL p<=.01:", n4_clears)
print("[scale] F-SCALE ruling    :", RESULTS["summary"]["F_SCALE_1_capacity_bound"])
print("[scale] NOTE: paging N FCs through 1 chip = the closed paged-depth primitive applied to WIDTH (single /dev/akida0 lock).")
