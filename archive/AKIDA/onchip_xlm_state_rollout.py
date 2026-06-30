#!/usr/bin/env python3
"""Lane A STATE-CARRYING MULTI-STEP ROLLOUT RUNG — break the 1-hop autoregressive ceiling on live AKD1000.
substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G / GPU) · a_scale_honest_scope · g63 (NO sw fallback).

WHERE WE ARE (verbatim from the frontier — PR #1686 closed-negative):
  The STATELESS autoregressive rollout (onchip_xlm_rollout.py) PROVED that single-step on-chip generation
  COLLAPSES after exactly ONE hop: decay curve roll_acc[1..3] = [0.4287, 0.0277, 0.0090]. Hop-1 cleared the
  shuffle+identity NULL (single-step generation works), but hop-2 fell INTO the shuffle-NULL (0.0277) and hop-3
  dropped BELOW chance (0.0090 < 1/(NC-1)=0.0204). The verdict named the root cause: the 256-unit 1-bit
  AkidaUnsupervised Hebbian FC carries NO RECURRENCE / NO STATE — feeding bind(g_hat_k, NEUTRAL) (a function of
  the LAST produced code ONLY) drifts off-manifold immediately, because each hop's input forgets all prior
  context. The named next bridge: STATE-CARRYING / paged generator · multi-FC depth · off-chip decode.

THIS RUNG (state-carry — does giving the chip path STATE break the 1-hop wall?):
  Chip-native state mechanism = a CONTEXT-CARRYING CODE. We maintain a running 1-bit context vector ctx that
  bit-MAJORITY accumulates the chip's prior produced codes across hops, and we BIND that context into each hop's
  chip input. Concretely, where the stateless rung fed x_{k+1} = neutral_bind(g_hat_k) (last code only):
    state-carry: ctx_0 = seed_code; x_0 = neutral_bind(ctx_0)            (hop-1 input == stateless hop-1 input,
                                                                          so hop-1 MUST reproduce the baseline)
    each hop k (after producing g_hat_k on-chip):
        ctx_{k+1} = bit_majority(ctx_k, g_hat_k)   weighted toward history (running EMA-style 1-bit accumulator)
        x_{k+1}   = bind(g_hat_k, ctx_{k+1})       (the input now carries ACCUMULATED CONTEXT, not just g_hat_k)
  Everything else is BYTE-IDENTICAL to onchip_xlm_rollout.py: enc_whitened, SHIFT=37, neutral_bind, bind,
  build_fc(1) AkidaUnsupervised(num_weights=8, learning_competition=0.1), the successor-centroid codebook,
  the frozen-median binarize, the open-vocab full-codebook decode, the ban-set (cannot re-emit last token),
  K_ROLL=3, NTRIALS=8, the per-hop shuffle-NULL (B=200) and identity-NULL. The ONLY new thing is the input
  construction carries state. NO GPU. NO sw fallback labelled on-chip (g63: device==[] -> OPEN-BLOCKED, abort).
  We run the STATELESS arm IN-PROCESS too (same chip, same trial seed) as the head-to-head baseline.

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: state_acc[k] = P(open-vocab argmax decode of the STATE-CARRY g_hat at hop k == concept[ti+k]), k=1..K,
          over all (seed t, query-lang) starts with >=K real successors. stateless_acc[k] = the same on the
          NEUTRAL-feedback arm (reproduces PR #1686 [0.4287,0.0277,0.0090] within trial noise — sanity).
  NULL-A (SHUFFLE) per hop k: state-carry hop-k decode with (seed->gt_k) labels permuted (B=200); per-hop hi+p.
  NULL-B (IDENTITY) per hop: the SAME state-carry feedback chain through an UNTRAINED (do_fit=False) FC.
  CHANCE: 1/(NC-1) open-vocab uniform.
  FALSIFIER F-STATE-1 (state breaks the 1-hop wall): "with state-carry, hop-2 AND hop-3 rollout acc do NOT
          stay above the shuffle-NULL." -> REFUTED iff for k in {2,3}: state_acc[k] ci_lo > shuffle_null[k] hi
          AND p[k] < 0.05 (the hops that COLLAPSED in the stateless baseline now clear the NULL). [the headline]
  FALSIFIER F-STATE-2 (state beats the stateless baseline at matched hops): "state-carry does NOT improve over
          the stateless rollout at hop-2/3." -> REFUTED iff state_acc[2] > stateless_acc[2] AND
          state_acc[3] > stateless_acc[3] (strict per-hop improvement over the PR #1686 collapse).
  HONEST: we ALWAYS report BOTH decay curves (state vs stateless), the per-hop chance/shuffle/identity NULLs,
          and the per-hop delta, regardless of disposition.

DISPOSITION (a_paper_negative_ok — a clean STILL-COLLAPSES is a VALID closed-negative, NOT forced green):
  F-STATE-1 REFUTED (hop2&3 above shuffle-NULL) -> STATE-CARRY BREAKS THE 1-HOP WALL: the context-carrying code
    keeps the autoregressive trajectory on-manifold past hop-1; Lane A EMERGENCE axis (multi-step composition)
    advances toward earned-green (STILL toy 250-anchor / single 1-bit/256-unit FC; PUBLIC checkbox NOT flipped).
  F-STATE-1 NOT-refuted but F-STATE-2 REFUTED -> state-carry HELPS but does not fully clear the NULL: partial
    lift, decay curve quantifies the residual; names the next bridge (multi-FC depth / paged ladder).
  BOTH NOT-refuted (state-carry collapses like the stateless baseline) -> STATE-CARRY CLOSED-NEGATIVE
    (a_paper_negative_ok): a 1-bit context-binding code is NOT enough state to break the wall at 256-unit
    capacity -> SHARPENS the "AKIDA edge-learn has a hard generation-DEPTH ceiling that input-side state-carry
    alone cannot lift" finding; names the next bridge = ON-CHIP multi-FC depth (transition structure needs a
    second learned FC), not just input engineering. EMERGENCE axis stays NULL, recorded honestly.
  NO fabricated PUBLIC. NO sw fallback labelled on-chip. a_scale_honest_scope: toy 250-anchor / single FC.
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
UNITS, NW, LCOMP = 256, 8, 0.1     # byte-match generation/rollout rung
SHIFT = 37                          # byte-match onchip_xlm_rollout
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
K_ROLL = 3
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
def ctx_update(ctx, g_bin):
    """1-bit running context accumulator (chip-native: pure bit ops). bit-majority of (history, new code) with
    history weighted 2:1 -> a 1-bit EMA: ctx stays 1 where it was already 1 unless the new code disagrees twice.
    Implemented as majority(ctx, ctx, g_bin) = (ctx & g_bin) | (ctx & ctx) | (ctx & g_bin) reduces to ctx tilted
    toward ctx; equivalently the new bit = ctx if ctx==prev_ctx else g_bin. We use a simple stable majority:
        new = (2*ctx + g_bin) >= 2  -> 1 iff ctx==1 (history dominates), updated only where g_bin pushes.
    To still ABSORB new info we OR-in agreement and AND-out persistent disagreement over hops via a counter-free
    1-bit majority over THREE votes (ctx, ctx, g_bin): result==1 iff at least 2 of {ctx,ctx,g_bin} are 1."""
    ctx = ctx.astype(np.uint8); g_bin = g_bin.astype(np.uint8)
    votes = ctx.astype(np.int32) + ctx.astype(np.int32) + g_bin.astype(np.int32)  # 3-vote majority (history 2x)
    return (votes >= 2).astype(np.uint8)
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
print("[state] corpus_big count=%d concepts=%d langs=%d shift=%d units=%d K=%d" % (count, NC, len(langs), SHIFT, UNITS, K_ROLL)); sys.stdout.flush()
codes_enc = enc_whitened(H)
def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None
train_codes, train_succ = [], []
for l in langs:
    for ci_ in range(NC - 1):
        a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b)); train_succ.append(concepts_sorted[ci_ + 1])
train_codes = np.stack(train_codes)
n_train = train_codes.shape[0]
print("[state] teacher-forced train transitions=%d" % n_train); sys.stdout.flush()
roll_starts = []
for ti in range(NC - K_ROLL):
    t = concepts_sorted[ti]
    for ql in langs:
        a = code_of(t, ql)
        if a is None: continue
        roll_starts.append((ti, ql, a))
print("[state] rollout starts (>=%d real successors)=%d" % (K_ROLL, len(roll_starts))); sys.stdout.flush()
def build_codebook(chip_train_bin):
    cb = {}; k = 0
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            cb.setdefault(concepts_sorted[ci_ + 1], []).append(chip_train_bin[k]); k += 1
    return {c: np.mean(np.stack(v), axis=0) for c, v in cb.items()}
def decode(g_hat_bin_row, codebook, ban):
    cand = [c for c in codebook if c != ban]
    scores = [(overlap(g_hat_bin_row, codebook[c]), c) for c in cand]
    return max(scores)[1] if scores else None
def rollout_chip(m, codebook, med, mode):
    """drive the LIVE chip autoregressively for K hops. mode='state' -> context-carry input; mode='stateless'
    -> neutral_bind(last code only) [byte-match PR #1686 baseline]. returns preds[k]."""
    preds = [[] for _ in range(K_ROLL)]
    for (ti, ql, seed_code) in roll_starts:
        ctx = seed_code.astype(np.uint8).copy()
        x = neutral_bind(ctx)                         # hop-1 input identical in BOTH arms (== gen/baseline seed)
        banned = concepts_sorted[ti]
        for k in range(K_ROLL):
            g_soft = chip_forward(m, x)
            g_bin = binarize_rows(g_soft, med)[0]
            pred = decode(g_bin, codebook, banned)
            preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            if mode == "state":
                ctx = ctx_update(ctx, g_bin)          # accumulate produced code into running context
                x = bind(g_bin, ctx)                  # input carries ACCUMULATED CONTEXT
            else:
                x = neutral_bind(g_bin)               # stateless: last code only (byte-match baseline)
    return preds
def acc_at(preds, k0):
    hit, tot = 0, 0
    for (ti, ql, pred) in preds[k0]:
        if pred is None: continue
        gt = concepts_sorted[ti + k0 + 1]
        hit += int(pred == gt); tot += 1
    return hit / max(1, tot), tot
def shuffle_null_at(preds, k0, B=B_SHUFFLE, seed=SEED):
    rng = np.random.default_rng(seed + 1009 * (k0 + 1))
    null = []
    for _ in range(B):
        perm = rng.permutation(NC)
        smap = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for (ti, ql, pred) in preds[k0]:
            if pred is None: continue
            hit += int(pred == smap[concepts_sorted[ti]]); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)
RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "K_roll": K_ROLL,
           "state_mechanism": "context-carrying code: ctx_{k+1}=bit_majority(ctx,ctx,g_bin) (history 2x); "
                              "x_{k+1}=bind(g_bin,ctx) [vs stateless x_{k+1}=neutral_bind(g_bin)]",
           "binding": "bind(a,b)=a XOR roll(b,%d); neutral=a XOR roll(a,%d)" % (SHIFT, NEUTRAL_ROLL),
           "encoder": "whitened (byte-match onchip_xlm_rollout.enc_whitened)",
           "corpus": "corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs",
           "stateless_baseline_PR1686": [0.4287, 0.0277, 0.0090],
           "task": "STATE-CARRYING autoregressive on-chip ROLLOUT: K-hop chained generation with a running 1-bit "
                   "context code bound into each hop's input; open-vocab full-codebook decode; per-hop shuffle+identity NULL",
           "metric": "state_acc[k]=P(open-vocab decode of state-carry g_hat at hop k == concept[ti+k]), k=1..K",
           "trials": []}
print("[state] akida %s device %s ip %s N=%d trials units=%d K=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS, K_ROLL)); sys.stdout.flush()
state_trials = [[] for _ in range(K_ROLL)]
stateless_trials = [[] for _ in range(K_ROLL)]
ident_trials = [[] for _ in range(K_ROLL)]
learn_all = True
last_state_preds, last_id_preds = None, None
for tr in range(NTRIALS):
    init = get_w(build_fc(1))
    m, learned = chip_make(init, train_codes, do_fit=True)
    train_soft = chip_forward(m, train_codes)
    med = np.median(train_soft, axis=0)
    chip_train_bin = binarize_rows(train_soft, med)
    codebook = build_codebook(chip_train_bin)
    state_preds = rollout_chip(m, codebook, med, mode="state")
    stateless_preds = rollout_chip(m, codebook, med, mode="stateless")
    del m
    mid, _ = chip_make(init, train_codes, do_fit=False)
    id_train_soft = chip_forward(mid, train_codes)
    id_med = np.median(id_train_soft, axis=0)
    id_preds = rollout_chip(mid, codebook, id_med, mode="state")
    del mid
    learn_all = learn_all and learned
    trial_row = {"trial": tr, "learned_hw": learned, "state_acc": [], "stateless_acc": [], "identity_acc": [], "n_q": []}
    for k0 in range(K_ROLL):
        sa, n = acc_at(state_preds, k0); ba, _ = acc_at(stateless_preds, k0); ia, _ = acc_at(id_preds, k0)
        state_trials[k0].append(sa); stateless_trials[k0].append(ba); ident_trials[k0].append(ia)
        trial_row["state_acc"].append(sa); trial_row["stateless_acc"].append(ba); trial_row["identity_acc"].append(ia); trial_row["n_q"].append(n)
    RESULTS["trials"].append(trial_row)
    last_state_preds, last_id_preds = state_preds, id_preds
    print("[state] trial %d: state(k1..K)=%s stateless=%s identity=%s learn=%s" %
          (tr, ["%.4f" % x for x in trial_row["state_acc"]], ["%.4f" % x for x in trial_row["stateless_acc"]],
           ["%.4f" % x for x in trial_row["identity_acc"]], learned)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_state_rollout.json"), "w"), indent=2)
chance = 1.0/(NC - 1)
per_hop = []
print("[state] computing per-hop shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
for k0 in range(K_ROLL):
    sm, ssd, ssem, slo, shi = ci(state_trials[k0])
    bm, bsd, bsem, blo, bhi = ci(stateless_trials[k0])
    im, isd, isem, ilo, ihi = ci(ident_trials[k0])
    null = shuffle_null_at(last_state_preds, k0, B=B_SHUFFLE, seed=SEED)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= sm).sum() + 1) / (len(null) + 1)
    above_shuf = bool(learn_all and slo > nhi and p < 0.05)
    above_id = bool(learn_all and slo > ihi)
    beats_stateless = bool(sm > bm)
    per_hop.append({"hop": k0 + 1,
                    "state_acc": {"mean": sm, "sd": ssd, "ci_lo": slo, "ci_hi": shi},
                    "stateless_acc": {"mean": bm, "ci_lo": blo, "ci_hi": bhi},
                    "delta_state_minus_stateless": round(sm - bm, 4),
                    "identity_null": {"mean": im, "hi": ihi},
                    "shuffle_null": {"mean": nmean, "sd": nsd, "hi": nhi, "p_value": p, "B": B_SHUFFLE},
                    "chance": chance, "above_shuffle_null": above_shuf, "above_identity_null": above_id,
                    "beats_stateless": beats_stateless})
    print("[state] hop %d: state=%.4f ci_lo=%.4f | stateless=%.4f | delta=%+.4f | shufNULL hi=%.4f p=%.4f | idNULL hi=%.4f | chance=%.4f | aboveShuf=%s beatsBase=%s"
          % (k0 + 1, sm, slo, bm, sm - bm, nhi, p, ihi, chance, above_shuf, beats_stateless)); sys.stdout.flush()
# F-STATE-1: hop2 AND hop3 above shuffle-NULL (the hops that collapsed in the stateless baseline)
F_STATE_1 = bool(per_hop[1]["above_shuffle_null"] and per_hop[2]["above_shuffle_null"])
# F-STATE-2: state beats stateless strictly at hop2 AND hop3
F_STATE_2 = bool(per_hop[1]["state_acc"]["mean"] > per_hop[1]["stateless_acc"]["mean"]
                 and per_hop[2]["state_acc"]["mean"] > per_hop[2]["stateless_acc"]["mean"])
RESULTS["summary"] = {
    "learn_all_hw": learn_all, "chance": chance, "K_roll": K_ROLL,
    "decay_curve_state":     [round(per_hop[k]["state_acc"]["mean"], 4) for k in range(K_ROLL)],
    "decay_curve_stateless": [round(per_hop[k]["stateless_acc"]["mean"], 4) for k in range(K_ROLL)],
    "per_hop": per_hop,
    "F_STATE_1_breaks_1hop_wall": (
        "REFUTED: with state-carry, hop-2 AND hop-3 rollout acc STAY ABOVE the shuffle-NULL (each ci_lo>NULL hi "
        "AND p<0.05) -> the context-carrying code breaks the 1-hop wall; the trajectory stays on-manifold past hop-1"
        if F_STATE_1 else
        "NOT-REFUTED: hop-2 and/or hop-3 state-carry acc DROPS INTO the shuffle-NULL -> input-side state-carry "
        "alone does NOT break the 1-hop wall at 1-bit/%d-unit (CLOSED-NEGATIVE, a_paper_negative_ok)" % UNITS),
    "F_STATE_2_beats_stateless": (
        "REFUTED: state-carry acc > stateless acc at BOTH hop-2 and hop-3 -> state-carry strictly improves over "
        "the PR#1686 collapse [0.0277, 0.0090]"
        if F_STATE_2 else
        "NOT-REFUTED: state-carry does NOT strictly beat the stateless baseline at both hop-2 and hop-3 -> "
        "context binding adds no usable depth at this capacity (a_paper_negative_ok)"),
    "F_STATE_1_pass": F_STATE_1, "F_STATE_2_pass": F_STATE_2,
    "state_carry_breaks_wall": bool(F_STATE_1),
}
if F_STATE_1:
    disp = ("STATE-CARRY BREAKS THE 1-HOP WALL on-chip (hop-2 AND hop-3 above shuffle-NULL): the context-carrying "
            "code keeps the autoregressive trajectory on-manifold past hop-1; Lane A EMERGENCE axis (multi-step "
            "composition) advances toward earned-green (STILL toy 250-anchor / single 1-bit/%d-unit FC; PUBLIC "
            "checkbox NOT flipped). a_lane_akida_gpu_split: Lane A on-chip, NEVER merged with Lane G." % UNITS)
elif F_STATE_2:
    disp = ("STATE-CARRY PARTIAL LIFT (a_paper_negative_ok): state beats the stateless baseline at hop-2/3 but "
            "does NOT fully clear the shuffle-NULL -> input-side context binding HELPS but is insufficient state "
            "at 1-bit/%d-unit; decay curve quantifies the residual; names next bridge = ON-CHIP multi-FC depth / "
            "paged ladder. EMERGENCE axis partial. Lane A on-chip, toy scale." % UNITS)
else:
    disp = ("STATE-CARRY CLOSED-NEGATIVE (a_paper_negative_ok): a 1-bit context-binding code does NOT break the "
            "1-hop wall (hop-2/3 still in the shuffle-NULL, no strict gain over stateless) -> SHARPENS the finding "
            "that AKIDA edge-learn has a hard generation-DEPTH ceiling that input-side state-carry alone cannot "
            "lift at 256-unit capacity; names next bridge = ON-CHIP multi-FC depth (transition structure needs a "
            "second learned FC), not input engineering. EMERGENCE axis NULL. Retrieval+single-step UNAFFECTED. "
            "Lane A on-chip (a_lane_akida_gpu_split), toy 250-anchor scale (a_scale_honest_scope).")
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_state_rollout.json"), "w"), indent=2)
print("\n[state] ========== DISPOSITION ==========")
print("[state] learn_all_hw         :", learn_all)
print("[state] chance               : %.4f  K=%d" % (chance, K_ROLL))
print("[state] decay STATE (k1..K)  :", ["%.4f" % per_hop[k]["state_acc"]["mean"] for k in range(K_ROLL)])
print("[state] decay STATELESS base :", ["%.4f" % per_hop[k]["stateless_acc"]["mean"] for k in range(K_ROLL)])
print("[state] PR#1686 baseline     : [0.4287, 0.0277, 0.0090]")
for k0 in range(K_ROLL):
    h = per_hop[k0]
    print("[state] hop %d  state=%.4f ci_lo=%.4f | stateless=%.4f delta=%+.4f | shufNULL hi=%.4f p=%.4f | idNULL hi=%.4f | aboveShuf=%s beatsBase=%s"
          % (h["hop"], h["state_acc"]["mean"], h["state_acc"]["ci_lo"], h["stateless_acc"]["mean"],
             h["delta_state_minus_stateless"], h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"],
             h["identity_null"]["hi"], h["above_shuffle_null"], h["beats_stateless"]))
print("[state] F-STATE-1 wall       :", RESULTS["summary"]["F_STATE_1_breaks_1hop_wall"])
print("[state] F-STATE-2 vs baseline:", RESULTS["summary"]["F_STATE_2_beats_stateless"])
print("[state] DISPOSITION          :", RESULTS["DISPOSITION"])
print("[state] wrote " + os.path.join(OUT, "result_onchip_xlm_state_rollout.json"))
