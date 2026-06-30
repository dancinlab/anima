#!/usr/bin/env python3
"""Lane A ON-CHIP MULTI-FC DEPTH ROLLOUT RUNG — does a SECOND learned FC break the 1-hop generation wall on live AKD1000?
substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G / GPU) · a_scale_honest_scope · g63 (NO sw fallback).

WHERE WE ARE (verbatim from the frontier — TWO closed-negatives):
  PR #1686 (STATELESS rollout, onchip_xlm_rollout.py): single-step on-chip generation COLLAPSES after exactly
    ONE hop. decay roll_acc[1..3] = [0.4287, 0.0277, 0.0090]. hop-1 cleared the shuffle+identity NULL, hop-2 fell
    INTO the shuffle-NULL, hop-3 below chance.
  PR #1689 (STATE-CARRY rollout, onchip_xlm_state_rollout.py): binding ACCUMULATED CONTEXT into each hop's input
    gave only a PERMILLE lift. decay STATE = [0.4234, 0.0282, 0.0122]; hop-2 p=0.2338, hop-3 p=0.8905 — STILL in
    the shuffle-NULL. F-STATE-1 NOT-refuted (wall holds), F-STATE-2 refuted (beats stateless by +0.0048/+0.0005,
    permille). VERDICT sharpened: "AKIDA edge-learn has a hard generation-DEPTH ceiling that INPUT-SIDE state-carry
    alone cannot lift at 256-unit capacity. The transition structure has NOWHERE TO LIVE across steps when the only
    learnable surface is one 1-bit Hebbian FC." NAMED next bridge (verbatim): ON-CHIP MULTI-FC DEPTH — a SECOND
    learned FC so the composition has a place to live, NOT further input engineering.

THIS RUNG (the named bridge — give the generation step on-chip DEPTH via a SECOND learned FC):
  We stack TWO plastic AkidaUnsupervised FCs, BOTH trained on the live AKD1000 by WEIGHT-PAGING (the chip-native
  primitive proved GREEN in onchip_layerpage_compose.py: only ONE FC chip-resident at a time on the single 8MB-SRAM
  NPU mesh; L1 fit -> page weights OFF to host -> L2 mapped to the SAME mesh -> fit on L1's on-chip forward output).
    FC1 (units=256, nw=8) = the TRANSITION ENCODER (byte-identical to the single FC of PR#1686/#1689): it maps a
         bound transition code -> a successor-ish code. This is the surface that ALREADY works at hop-1.
    FC2 (units=256, nw=8) = a learned COMPOSITION / RECURRENCE surface. It is trained ON CHIP on FC1's on-chip
         binarized output for the SAME teacher-forced transitions, so it learns to RE-PROJECT a once-transformed
         code back onto the codebook manifold — i.e. a learned "stay-on-manifold" map that the input-only state-carry
         lacked. At generation time each hop runs the paged depth-2 pipeline:
             g1_soft = FC1.forward(x)        ; g1_bin = binarize(g1_soft, med1)   [on chip]
             g2_soft = FC2.forward(g1_bin)   ; g_bin  = binarize(g2_soft, med2)   [on chip, paged]
         The decode + ban-set + context-carry feedback are IDENTICAL to PR#1689 (we KEEP the input-side state-carry
         that won F-STATE-2, and ADD depth on top — the bridge is depth, not a different input).
  Everything else is BYTE-IDENTICAL to onchip_xlm_state_rollout.py: enc_whitened, SHIFT=37, neutral_bind, bind,
  ctx_update (3-vote majority, history 2x), AkidaUnsupervised(num_weights=8, learning_competition=0.1), the
  successor-centroid codebook (built from the DEPTH-2 on-chip output of the teacher-forced transitions), the
  frozen-median binarize (med1 for FC1, med2 for FC2), open-vocab full-codebook decode, ban-set, K_ROLL=3,
  NTRIALS=8, the per-hop shuffle-NULL (B=200) and identity-NULL. NO GPU. NO sw fallback labelled on-chip
  (g63: device==[] -> OPEN-BLOCKED, abort). We run the 1-FC STATE-CARRY arm IN-PROCESS (same chip, same trial,
  FC1-only) as the head-to-head baseline that reproduces PR#1689 [0.4234, 0.0282, 0.0122] within trial noise.

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: depth_acc[k] = P(open-vocab argmax decode of the DEPTH-2 g_hat at hop k == concept[ti+k]), k=1..K,
          over all (seed t, query-lang) starts with >=K real successors. onefc_acc[k] = the SAME on the 1-FC
          state-carry arm (FC1 only; reproduces PR#1689 [0.4234,0.0282,0.0122] within trial noise — sanity).
  NULL-A (SHUFFLE) per hop k: depth-2 hop-k decode with (seed->gt_k) labels permuted (B=200); per-hop hi+p.
  NULL-B (IDENTITY) per hop: the SAME depth-2 feedback chain through UNTRAINED (do_fit=False) FC1 AND FC2.
  CHANCE: 1/(NC-1) open-vocab uniform.
  FALSIFIER F-DEPTH-1 (2-FC depth breaks the 1-hop wall): "with a second learned FC, hop-2 AND hop-3 rollout acc
          do NOT stay above the shuffle-NULL." -> REFUTED iff for k in {2,3}: depth_acc[k] ci_lo > shuffle_null[k]
          hi AND p[k] < 0.05 (the hops that COLLAPSED for a single FC now clear the NULL). [the headline]
  FALSIFIER F-DEPTH-2 (2-FC beats the 1-FC state-carry baseline by more than permille): "depth does NOT beat the
          1-FC state-carry baseline (hop2=0.0282) by more than permille." -> REFUTED iff
          depth_acc[2] - onefc_acc[2] > 0.01 AND depth_acc[3] - onefc_acc[3] > 0.005 (real depth, MATERIAL gain,
          not the permille tug PR#1689 saw). [margin thresholds pre-registered: >1% @ hop2, >0.5% @ hop3]
  HONEST: we ALWAYS report BOTH decay curves (depth-2 vs 1-FC), the per-hop chance/shuffle/identity NULLs, and the
          per-hop delta, regardless of disposition.

DISPOSITION (a_paper_negative_ok — a clean STILL-COLLAPSES is a VALID closed-negative, NOT forced green):
  F-DEPTH-1 REFUTED (hop2&3 above shuffle-NULL) -> ON-CHIP DEPTH BREAKS THE 1-HOP WALL: the second learned FC gives
    the transition structure a place to live; Lane A EMERGENCE axis (multi-step composition) advances toward
    earned-green (STILL toy 250-anchor / 2x 1-bit 256-unit FCs; PUBLIC checkbox NOT flipped).
  F-DEPTH-1 NOT-refuted but F-DEPTH-2 REFUTED -> depth HELPS materially but does not fully clear the NULL: partial
    lift, decay curve quantifies the residual; names the next bridge (deeper paged ladder / off-chip decode head).
  BOTH NOT-refuted (depth-2 collapses like the single FC) -> MULTI-FC DEPTH CLOSED-NEGATIVE (a_paper_negative_ok):
    a SECOND learned 1-bit FC is NOT enough to break the wall at 256-unit capacity -> SHARPENS the finding to
    "AKD1000 edge-learn caps at SINGLE-STEP generation regardless of depth" -> names the next bridge = off-chip
    decode head OR accept single-step as the Lane-A PUBLIC scope. EMERGENCE axis stays NULL, recorded honestly.
  NO fabricated PUBLIC. NO sw fallback labelled on-chip. a_scale_honest_scope: toy 250-anchor / 2x 256-unit FC.
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
UNITS, NW, LCOMP = 256, 8, 0.1     # byte-match generation/rollout/state rung (BOTH FCs use these)
SHIFT = 37                          # byte-match onchip_xlm_state_rollout
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
    """1-bit running context accumulator (chip-native: pure bit ops) — byte-identical to onchip_xlm_state_rollout.
    3-vote majority (ctx, ctx, g_bin): result==1 iff at least 2 of {ctx,ctx,g_bin} are 1 (history weighted 2x)."""
    ctx = ctx.astype(np.uint8); g_bin = g_bin.astype(np.uint8)
    votes = ctx.astype(np.int32) + ctx.astype(np.int32) + g_bin.astype(np.int32)
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
def chip_fit_forward(init_w, Xb_train, do_fit=True):
    """page ONE FC onto the single NPU mesh: map, (optionally) fit on chip, forward the SAME train set, return
    (learned, post_w, train_soft). Caller pages the weights OFF (keeps post_w on host) and del's the model so the
    mesh is free for the next FC. byte-match chip_make+forward of onchip_xlm_state_rollout, split for paging."""
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    Xt = to_chip(Xb_train)
    if do_fit:
        for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    learned = bool(np.any(post != pre))
    train_soft = np.stack([np.array(m.forward(Xt[i:i+1])).astype(np.float64).ravel() for i in range(Xt.shape[0])])
    del m  # page this FC OFF — mesh now free for the next paged FC (single-residency, layerpage primitive)
    return learned, post, train_soft
def chip_forward_paged(post_w, Xb):
    """map a paged FC back onto the mesh with its host-persisted weights, forward Xb, page off. one FC resident."""
    m = build_fc(1); set_w(m, post_w); m.map(DEV); set_w(m, post_w)
    Xe = to_chip(Xb)
    out = np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])
    del m
    return out
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
print("[depth] corpus_big count=%d concepts=%d langs=%d shift=%d units=%d K=%d (2-FC paged depth)" % (count, NC, len(langs), SHIFT, UNITS, K_ROLL)); sys.stdout.flush()
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
print("[depth] teacher-forced train transitions=%d" % n_train); sys.stdout.flush()
roll_starts = []
for ti in range(NC - K_ROLL):
    t = concepts_sorted[ti]
    for ql in langs:
        a = code_of(t, ql)
        if a is None: continue
        roll_starts.append((ti, ql, a))
print("[depth] rollout starts (>=%d real successors)=%d" % (K_ROLL, len(roll_starts))); sys.stdout.flush()
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
def rollout_depth(post1, med1, post2, med2, codebook, mode):
    """drive the LIVE chip autoregressively for K hops through a PAGED depth-2 stack.
    mode='depth2'  -> per hop: g1=FC1.forward(x) -> g1_bin -> g2=FC2.forward(g1_bin) -> g_bin=binarize(g2,med2);
                      input-side state-carry retained (ctx + bind), byte-match PR#1689 feedback.
    mode='onefc'   -> per hop: g_bin=binarize(FC1.forward(x), med1); state-carry feedback [== PR#1689 1-FC arm].
    NOTE: each FC.forward maps that single FC onto the mesh, forwards, pages off (single-residency).
    To keep chip ops batched we forward ALL rollout starts at once per hop (the chain state is per-start)."""
    n = len(roll_starts)
    ctx = np.stack([sc.astype(np.uint8).copy() for (_, _, sc) in roll_starts])     # (n, INC)
    x = np.stack([neutral_bind(sc) for (_, _, sc) in roll_starts])                 # hop-1 input == PR#1689 seed
    banned = [concepts_sorted[ti] for (ti, _, _) in roll_starts]
    preds = [[] for _ in range(K_ROLL)]
    for k in range(K_ROLL):
        g1_soft = chip_forward_paged(post1, x)            # FC1 resident, forward all starts, page off
        g1_bin = binarize_rows(g1_soft, med1)
        if mode == "depth2":
            g2_soft = chip_forward_paged(post2, g1_bin)   # FC2 resident on FC1's on-chip output, page off
            g_bin = binarize_rows(g2_soft, med2)
        else:
            g_bin = g1_bin                                 # 1-FC arm: stop after FC1
        for j, (ti, ql, _) in enumerate(roll_starts):
            pred = decode(g_bin[j], codebook, banned[j])
            preds[k].append((ti, ql, pred))
            banned[j] = pred if pred is not None else banned[j]
        # input-side state-carry feedback (retained from PR#1689 — KEEP what won F-STATE-2, ADD depth)
        new_x = np.empty_like(x)
        for j in range(n):
            ctx[j] = ctx_update(ctx[j], g_bin[j])
            new_x[j] = bind(g_bin[j], ctx[j])
        x = new_x
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
           "depth_mechanism": "PAGED 2-FC on a single AKD1000 (layerpage primitive): FC1(256u,8w)=transition "
                              "encoder, FC2(256u,8w)=learned composition/recurrence surface trained ON CHIP on "
                              "FC1's on-chip binarized output; per hop g1=FC1(x)->g1_bin->g2=FC2(g1_bin)->g_bin; "
                              "input-side state-carry (ctx 3-vote majority + bind) retained from PR#1689",
           "binding": "bind(a,b)=a XOR roll(b,%d); neutral=a XOR roll(a,%d)" % (SHIFT, NEUTRAL_ROLL),
           "encoder": "whitened (byte-match onchip_xlm_state_rollout.enc_whitened)",
           "corpus": "corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs",
           "onefc_baseline_PR1689": [0.4234, 0.0282, 0.0122],
           "stateless_baseline_PR1686": [0.4287, 0.0277, 0.0090],
           "task": "ON-CHIP MULTI-FC DEPTH autoregressive ROLLOUT: K-hop chained generation through a paged depth-2 "
                   "FC stack (both FCs learned on chip); open-vocab full-codebook decode; per-hop shuffle+identity NULL",
           "metric": "depth_acc[k]=P(open-vocab decode of depth-2 g_hat at hop k == concept[ti+k]), k=1..K",
           "trials": []}
print("[depth] akida %s device %s ip %s N=%d trials units=%d K=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS, K_ROLL)); sys.stdout.flush()
depth_trials = [[] for _ in range(K_ROLL)]
onefc_trials = [[] for _ in range(K_ROLL)]
ident_trials = [[] for _ in range(K_ROLL)]
learn_all = True
last_depth_preds, last_id_preds = None, None
for tr in range(NTRIALS):
    init1 = get_w(build_fc(1))
    # ---- PAGE 1: FC1 (transition encoder) trained on chip on the bound transitions, paged off ----
    l1_learned, post1, fc1_train_soft = chip_fit_forward(init1, train_codes, do_fit=True)
    med1 = np.median(fc1_train_soft, axis=0)
    fc1_train_bin = binarize_rows(fc1_train_soft, med1)
    # ---- PAGE 2: FC2 (composition surface) trained on chip on FC1's ON-CHIP binarized output, paged off ----
    init2 = get_w(build_fc(1))
    l2_learned, post2, fc2_train_soft = chip_fit_forward(init2, fc1_train_bin, do_fit=True)
    med2 = np.median(fc2_train_soft, axis=0)
    fc2_train_bin = binarize_rows(fc2_train_soft, med2)
    learned = bool(l1_learned and l2_learned)
    # codebook from the DEPTH-2 on-chip output of the teacher-forced transitions (matches the depth-2 rollout space)
    codebook = build_codebook(fc2_train_bin)
    depth_preds = rollout_depth(post1, med1, post2, med2, codebook, mode="depth2")
    onefc_preds = rollout_depth(post1, med1, post2, med2, codebook, mode="onefc")
    # identity arm: BOTH FCs untrained (do_fit=False), same paged depth-2 feedback chain
    initI1 = get_w(build_fc(1)); _, postI1, fcI1_soft = chip_fit_forward(initI1, train_codes, do_fit=False)
    medI1 = np.median(fcI1_soft, axis=0); fcI1_bin = binarize_rows(fcI1_soft, medI1)
    initI2 = get_w(build_fc(1)); _, postI2, fcI2_soft = chip_fit_forward(initI2, fcI1_bin, do_fit=False)
    medI2 = np.median(fcI2_soft, axis=0)
    id_preds = rollout_depth(postI1, medI1, postI2, medI2, codebook, mode="depth2")
    learn_all = learn_all and learned
    trial_row = {"trial": tr, "learned_hw": learned, "l1_learned": l1_learned, "l2_learned": l2_learned,
                 "depth_acc": [], "onefc_acc": [], "identity_acc": [], "n_q": []}
    for k0 in range(K_ROLL):
        da, n = acc_at(depth_preds, k0); ba, _ = acc_at(onefc_preds, k0); ia, _ = acc_at(id_preds, k0)
        depth_trials[k0].append(da); onefc_trials[k0].append(ba); ident_trials[k0].append(ia)
        trial_row["depth_acc"].append(da); trial_row["onefc_acc"].append(ba); trial_row["identity_acc"].append(ia); trial_row["n_q"].append(n)
    RESULTS["trials"].append(trial_row)
    last_depth_preds, last_id_preds = depth_preds, id_preds
    print("[depth] trial %d: depth2(k1..K)=%s onefc=%s identity=%s l1=%s l2=%s" %
          (tr, ["%.4f" % x for x in trial_row["depth_acc"]], ["%.4f" % x for x in trial_row["onefc_acc"]],
           ["%.4f" % x for x in trial_row["identity_acc"]], l1_learned, l2_learned)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_depth_rollout.json"), "w"), indent=2)
chance = 1.0/(NC - 1)
per_hop = []
print("[depth] computing per-hop shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
for k0 in range(K_ROLL):
    dm, dsd, dsem, dlo, dhi = ci(depth_trials[k0])
    bm, bsd, bsem, blo, bhi = ci(onefc_trials[k0])
    im, isd, isem, ilo, ihi = ci(ident_trials[k0])
    null = shuffle_null_at(last_depth_preds, k0, B=B_SHUFFLE, seed=SEED)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= dm).sum() + 1) / (len(null) + 1)
    above_shuf = bool(learn_all and dlo > nhi and p < 0.05)
    above_id = bool(learn_all and dlo > ihi)
    beats_onefc = bool(dm > bm)
    per_hop.append({"hop": k0 + 1,
                    "depth_acc": {"mean": dm, "sd": dsd, "ci_lo": dlo, "ci_hi": dhi},
                    "onefc_acc": {"mean": bm, "ci_lo": blo, "ci_hi": bhi},
                    "delta_depth_minus_onefc": round(dm - bm, 4),
                    "identity_null": {"mean": im, "hi": ihi},
                    "shuffle_null": {"mean": nmean, "sd": nsd, "hi": nhi, "p_value": p, "B": B_SHUFFLE},
                    "chance": chance, "above_shuffle_null": above_shuf, "above_identity_null": above_id,
                    "beats_onefc": beats_onefc})
    print("[depth] hop %d: depth2=%.4f ci_lo=%.4f | onefc=%.4f | delta=%+.4f | shufNULL hi=%.4f p=%.4f | idNULL hi=%.4f | chance=%.4f | aboveShuf=%s beats1FC=%s"
          % (k0 + 1, dm, dlo, bm, dm - bm, nhi, p, ihi, chance, above_shuf, beats_onefc)); sys.stdout.flush()
# F-DEPTH-1: hop2 AND hop3 above shuffle-NULL (the hops that collapsed for a single FC)
F_DEPTH_1 = bool(per_hop[1]["above_shuffle_null"] and per_hop[2]["above_shuffle_null"])
# F-DEPTH-2: depth beats 1-FC state-carry baseline by MORE THAN PERMILLE (pre-registered: >1% @ hop2, >0.5% @ hop3)
F_DEPTH_2 = bool((per_hop[1]["depth_acc"]["mean"] - per_hop[1]["onefc_acc"]["mean"] > 0.01)
                 and (per_hop[2]["depth_acc"]["mean"] - per_hop[2]["onefc_acc"]["mean"] > 0.005))
RESULTS["summary"] = {
    "learn_all_hw": learn_all, "chance": chance, "K_roll": K_ROLL,
    "decay_curve_depth2":  [round(per_hop[k]["depth_acc"]["mean"], 4) for k in range(K_ROLL)],
    "decay_curve_onefc":   [round(per_hop[k]["onefc_acc"]["mean"], 4) for k in range(K_ROLL)],
    "per_hop": per_hop,
    "F_DEPTH_1_breaks_1hop_wall": (
        "REFUTED: with a SECOND learned FC, hop-2 AND hop-3 rollout acc STAY ABOVE the shuffle-NULL (each ci_lo>NULL "
        "hi AND p<0.05) -> on-chip depth breaks the 1-hop wall; the transition structure now has a place to live"
        if F_DEPTH_1 else
        "NOT-REFUTED: hop-2 and/or hop-3 depth-2 acc DROPS INTO the shuffle-NULL -> a second learned FC does NOT "
        "break the 1-hop wall at 1-bit/%d-unit (CLOSED-NEGATIVE, a_paper_negative_ok)" % UNITS),
    "F_DEPTH_2_beats_onefc_material": (
        "REFUTED: depth-2 acc beats the 1-FC state-carry baseline by >1%% @hop2 AND >0.5%% @hop3 -> MATERIAL depth "
        "gain over the PR#1689 permille tug [0.0282, 0.0122]"
        if F_DEPTH_2 else
        "NOT-REFUTED: depth-2 does NOT beat the 1-FC state-carry baseline by more than permille at hop-2/3 -> a "
        "second FC adds no MATERIAL depth at this capacity (a_paper_negative_ok)"),
    "F_DEPTH_1_pass": F_DEPTH_1, "F_DEPTH_2_pass": F_DEPTH_2,
    "depth_breaks_wall": bool(F_DEPTH_1),
}
if F_DEPTH_1:
    disp = ("ON-CHIP MULTI-FC DEPTH BREAKS THE 1-HOP WALL on live AKD1000 (hop-2 AND hop-3 above shuffle-NULL): the "
            "second learned FC gives the transition structure a place to live across hops; Lane A EMERGENCE axis "
            "(multi-step composition) advances toward earned-green (STILL toy 250-anchor / 2x 1-bit %d-unit FCs; "
            "PUBLIC checkbox NOT flipped). a_lane_akida_gpu_split: Lane A on-chip, NEVER merged with Lane G." % UNITS)
elif F_DEPTH_2:
    disp = ("MULTI-FC DEPTH MATERIAL PARTIAL LIFT (a_paper_negative_ok): depth-2 beats the 1-FC state-carry baseline "
            "by more than permille at hop-2/3 but does NOT fully clear the shuffle-NULL -> a second learned FC HELPS "
            "materially but is insufficient depth at 1-bit/%d-unit; decay curve quantifies the residual; names next "
            "bridge = deeper paged ladder / off-chip decode head. EMERGENCE axis partial. Lane A on-chip, toy scale." % UNITS)
else:
    disp = ("MULTI-FC DEPTH CLOSED-NEGATIVE (a_paper_negative_ok): a SECOND learned 1-bit FC does NOT break the "
            "1-hop wall (hop-2/3 still in the shuffle-NULL, no material gain over the 1-FC state-carry baseline) -> "
            "SHARPENS the finding to 'AKD1000 edge-learn caps at SINGLE-STEP generation REGARDLESS OF DEPTH' at "
            "256-unit capacity; the wall is not an input/state problem and not a depth problem at this scale. Named "
            "next bridge = off-chip decode head OR accept single-step as the Lane-A PUBLIC scope. EMERGENCE axis "
            "NULL. Retrieval+single-step UNAFFECTED. Lane A on-chip (a_lane_akida_gpu_split), toy 250-anchor scale "
            "(a_scale_honest_scope).")
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_depth_rollout.json"), "w"), indent=2)
print("\n[depth] ========== DISPOSITION ==========")
print("[depth] learn_all_hw         :", learn_all)
print("[depth] chance               : %.4f  K=%d" % (chance, K_ROLL))
print("[depth] decay DEPTH-2 (k1..K):", ["%.4f" % per_hop[k]["depth_acc"]["mean"] for k in range(K_ROLL)])
print("[depth] decay 1-FC base      :", ["%.4f" % per_hop[k]["onefc_acc"]["mean"] for k in range(K_ROLL)])
print("[depth] PR#1689 1-FC baseline: [0.4234, 0.0282, 0.0122]")
print("[depth] PR#1686 stateless    : [0.4287, 0.0277, 0.0090]")
for k0 in range(K_ROLL):
    h = per_hop[k0]
    print("[depth] hop %d  depth2=%.4f ci_lo=%.4f | onefc=%.4f delta=%+.4f | shufNULL hi=%.4f p=%.4f | idNULL hi=%.4f | aboveShuf=%s beats1FC=%s"
          % (h["hop"], h["depth_acc"]["mean"], h["depth_acc"]["ci_lo"], h["onefc_acc"]["mean"],
             h["delta_depth_minus_onefc"], h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"],
             h["identity_null"]["hi"], h["above_shuffle_null"], h["beats_onefc"]))
print("[depth] F-DEPTH-1 wall       :", RESULTS["summary"]["F_DEPTH_1_breaks_1hop_wall"])
print("[depth] F-DEPTH-2 material   :", RESULTS["summary"]["F_DEPTH_2_beats_onefc_material"])
print("[depth] DISPOSITION          :", RESULTS["DISPOSITION"])
print("[depth] wrote " + os.path.join(OUT, "result_onchip_xlm_depth_rollout.json"))
