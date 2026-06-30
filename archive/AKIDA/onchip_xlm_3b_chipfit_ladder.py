#!/usr/bin/env python3
"""Lane A 3B MILESTONE — HYBRID chip-fit / weight-PAGING capacity ladder (on-chip AKD1000 encoder ⊕ off-chip host-CPU
   decode head), scaling the ON-CHIP encoder capacity toward 3B-class params via the layerpage primitive, while
   preserving the branching-validated multi-step composition (held-out hop-2/3 above shuffle-NULL).
substrate = HYBRID (on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure on-chip, NOT Lane G/GPU.
a_lane_akida_gpu_split (the on-chip ENCODER part is AKIDA Lane A; the decode head is explicitly host-side) ·
a_scale_honest_scope (chip-fit/paging ladder >=3 rungs; toy->3B transfer reported HONESTLY — a quantified chip-fit
   SRAM/paging CEILING is a VALID closed result, NOT a failure) · g63 (the CHIP part has NO sw fallback —
   device==[] -> abort) · a_completeness_over_cheap (the ladder probes the REAL chip-fit frontier, not a cheap stop) ·
a_paper_negative_ok (a precise chip-fit ceiling before 3B-class = a VALID closed result that names the hardware limit).

WHERE WE ARE (verbatim from the branching rung, PR#1697, .verdicts/lane-a-branch/F-BRANCH.txt):
  The branching corpus (succ(i)={(i+d) mod NC : d in {1,7,19}}, B=3) PROVED REAL multi-step composition on a HYBRID
  substrate: held-out hop-2/3 set-membership 0.8967/0.9600 >> shuffle-NULL (p=0.005), 3-rung NC={30,40,50} codebook
  ladder, on a 256-UNIT single on-chip FC encoder + D_H=64 off-chip RNN head. That rung's ladder was a CODEBOOK-SIZE
  ladder (NC). The 3B MILESTONE needs a CHIP-FIT / PARAMETER-CAPACITY ladder: how far does the ON-CHIP encoder scale
  on the single 8MB-SRAM AKD1000 mesh (toward 3B-class params) WHILE the branching composition survives — and where
  EXACTLY does the SRAM/paging ceiling bite?

THE 3B CHIP-FIT / PAGING LADDER (this rung — scale on-chip encoder capacity via the layerpage primitive):
  The AKD1000 has ONE NPU mesh with ~8 MB on-chip SRAM. The layerpage primitive (proved GREEN in
  onchip_layerpage_compose / onchip_xlm_depth_rollout: chip_fit_forward + chip_forward_paged) keeps only ONE FC
  chip-resident at a time: map FC -> fit on chip -> page weights OFF to host -> del -> map the next FC. This lets us
  STACK an arbitrary number D of plastic FCs (a deep paged encoder) and WIDEN each FC's unit count U, with only ONE
  FC ever resident -> the on-chip PARAMETER COUNT we can TRAIN is bounded by (one FC fits the mesh), while the TOTAL
  paged-model param count (D x per-FC) can grow toward 3B-class on host-resident pages.
  We sweep a CAPACITY ladder of rungs of increasing (D paged FCs, U units), each a multiple of the branching
  baseline's single 256-unit FC, computing the on-chip encoder PARAMETER COUNT per rung:
      per_fc_params  = U(units) * INC(256 inputs) * NW(8 weights-per-unit)        [AkidaUnsupervised FC]
      paged_params   = D * per_fc_params                                          [total trainable paged-encoder params]
  The deep paged encoder is a depth-D composition pipeline (byte-match onchip_xlm_depth_rollout's 2-FC paging,
  generalized to D FCs): FC1 fit on the bound branching transitions, page off; FC2 fit on FC1's on-chip binarized
  output, page off; ... ; FC_D fit on FC_{D-1}'s output. The encoder code fed to the off-chip head is the depth-D
  on-chip binarized output. Each FC's chip-fit (map + learn on the live mesh) is asserted per rung (g63, no fallback).
  CEILING DETECTION: at each rung we record, per paged FC, whether it (a) MAPPED onto the mesh and (b) LEARNED on
  silicon (post_w != pre_w). The chip-fit CEILING = the largest (D,U) rung where EVERY paged FC maps AND learns; a rung
  that fails to map (SRAM overflow) OR fails to learn (saturated mesh) NAMES the precise hardware ceiling (a_scale_honest_scope).

BRANCHING COMPOSITION (KEEP byte-identical to PR#1697 onchip_xlm_branching.py — this is the validated test surface):
  succ(i) = { (i + delta) mod NC : delta in DELTAS }   DELTAS={1,7,19}  B=3 ; held-out concept split (last 30%);
  off-chip Elman RNN head (D_H=64, numpy BPTT, NO torch/sklearn/GPU) trained on RANDOM branching walks with TRAIN-only
  targets; branching-aware set-membership metric setacc[k]=P(pred in succ(current)); shuffle-NULL B=200. We feed the
  off-chip head the DEPTH-D PAGED on-chip code instead of the single-FC code; everything downstream is byte-identical.
  At the largest chip-fit rung we ALSO grow the codebook NC to the corpus ceiling (NC=50) so the composition test is
  at full toy scale on top of the deepest paged encoder.

PRE-REGISTERED FALSIFIERS (g63 honest, declared in-file BEFORE the run):
  metric: per rung, held-out hop-2/3 branching set-membership vs shuffle-NULL (B=200); plus per-FC chip-fit (map+learn).
  CHANCE: B/(NC-1).
  FALSIFIER F-3B-1 (composition survives the capacity ladder): "held-out hop-2 AND hop-3 set-membership do NOT stay
          ABOVE the shuffle-NULL at EACH ladder rung up to the largest chip-fit scale reached."
          -> REFUTED iff for EVERY chip-fit rung, for k in {2,3}: heldout_setacc[k] ci_lo > shuffle_null[k] hi AND p[k]<0.05.
          [does the branching-validated composition SURVIVE as on-chip capacity scales toward 3B-class?]
  FALSIFIER F-3B-2 (ladder reaches 3B-class OR records the precise chip-fit ceiling): "the ladder neither reaches a
          stated 3B-class param/anchor count NOR records a precise chip-fit (SRAM/paging) ceiling that blocks it."
          -> REFUTED iff EITHER paged_params >= 3e9 at some chip-fit rung (3B-class reached) OR a precise rung is
          recorded where a paged FC fails to map/learn (the named SRAM/paging hardware ceiling). A QUANTIFIED CEILING
          is a VALID closed result (a_scale_honest_scope) — F-3B-2 is REFUTED by reaching 3B-class OR by a clean ceiling.
  HONEST: we ALWAYS report the per-rung (D,U,NC) scale, paged param count, per-FC chip-fit, and the held-out decay
          curve + shuffle-NULL, regardless of disposition. We do NOT fabricate a 3B claim; a chip-fit size limit is
          HARDWARE, not a science failure (a_scale_honest_scope).

DISPOSITION (a_scale_honest_scope · a_paper_negative_ok):
  3B-class param/anchor count reached AND composition preserved (F-3B-1 & F-3B-2 both REFUTED via 3B-reached)
    -> Lane A 3B milestone CLOSES (flip [x]).
  A precise chip-fit CEILING reached before 3B-class, composition preserved up to it (F-3B-1 REFUTED to the ceiling,
    F-3B-2 REFUTED via ceiling-recorded) -> Lane A 3B milestone STAYS OPEN with the NAMED hardware limit (record the
    quantified ceiling; do NOT fabricate a 3B claim). This is a VALID closed result, not a failure.
  Composition BREAKS at some rung below the ceiling (F-3B-1 NOT-refuted) -> honest closed-negative: capacity scaling
    DEGRADES the branching composition at (D,U,NC); record the rung where it breaks.
  NO fabricated 3B PUBLIC. NO sw fallback labelled on-chip. The off-chip head is labelled OFF-CHIP everywhere.
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
NW, LCOMP = 8, 0.1                  # byte-match branching/depth rung AkidaUnsupervised config
SHIFT = 37                          # byte-match onchip_xlm_branching encoder/bind
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
K_ROLL = 3
SEED = 20260602
# ---- OFF-CHIP decode head (host CPU, numpy) hyperparams — byte-match PR#1697 branching head ----
D_H = 64
EPOCHS = 60
LR = 0.05
GRAD_CLIP = 5.0
# ---- branching operator + held-out split (byte-match PR#1697) ----
DELTAS = [1, 7, 19]
B_FACTOR = len(DELTAS)
WALK_LEN = 6
WALKS_PER_LANG = 24
GEN_FACTOR = 2.0
N_TEST_FRAC = 0.30
# ---- 3B CHIP-FIT / PAGING CAPACITY LADDER (pre-registered; >=3 rungs of increasing on-chip capacity) ----
# Each rung = (D paged FCs, U units, NC codebook). per-FC params = U*INC*NW; paged = D*per-FC. The single-FC 256-unit
# branching baseline (D=1,U=256) is rung 0. We scale depth D and width U toward 3B-class while measuring chip-fit.
LADDER = [
    {"D": 1, "U": 256,  "NC": 50, "tag": "baseline(branching PR#1697)"},
    {"D": 2, "U": 512,  "NC": 50, "tag": "depth2 x width2"},
    {"D": 3, "U": 1024, "NC": 50, "tag": "depth3 x width4"},
    {"D": 4, "U": 2048, "NC": 50, "tag": "depth4 x width8 (chip-fit frontier probe)"},
]
TARGET_3B = 3e9                      # F-3B-2: paged_params >= 3e9 == 3B-class reached

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
def build_fc(units, wbits=1):
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=units, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()
devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback for the chip encoder")
DEV = devs[0]
def to_chip(Xb):
    Xb = np.atleast_2d(Xb).astype(np.uint8)
    return Xb.reshape(Xb.shape[0], 1, 1, INC)

def chip_fit_forward(units, Xb_train, do_fit=True):
    """layerpage primitive (byte-match onchip_xlm_depth_rollout.chip_fit_forward, parameterized by units): map ONE FC
    of `units` onto the single NPU mesh, fit on chip, forward the train set, PAGE OFF (del). Returns
    (mapped, learned, post_w, train_soft). mapped=False on a map() exception (SRAM overflow = chip-fit ceiling)."""
    try:
        m = build_fc(units, 1); init = get_w(m); m.map(DEV); set_w(m, init)
    except Exception as e:
        return False, False, None, None, "MAP_FAIL: %s" % str(e)[:160]
    pre = get_w(m)
    Xt = to_chip(Xb_train)
    if do_fit:
        for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    learned = bool(np.any(post != pre))
    # binarize the soft forward to INC-width 1-bit code so the depth-D pipeline keeps a fixed INC interface
    soft = np.stack([np.array(m.forward(Xt[i:i+1])).astype(np.float64).ravel() for i in range(Xt.shape[0])])
    del m   # PAGE this FC OFF — mesh free for the next paged FC (single-residency, layerpage)
    return True, learned, post, soft, "OK"
def chip_forward_paged(units, post_w, Xb):
    """map a paged FC back with host-persisted weights, forward, page off. one FC resident."""
    m = build_fc(units, 1); set_w(m, post_w); m.map(DEV); set_w(m, post_w)
    Xe = to_chip(Xb)
    out = np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])
    del m
    return out
def fold_to_inc(soft):
    """fold a U-wide soft output back to a fixed INC(256)-wide channel (sum-pool over U/INC groups when U>INC, tile
    when U<INC) so the depth-D paged pipeline + the off-chip head keep a fixed INC interface across rungs."""
    U = soft.shape[1]
    if U == INC: return soft
    if U > INC:
        g = U // INC
        return soft[:, :g*INC].reshape(soft.shape[0], INC, g).sum(axis=2)
    reps = int(np.ceil(INC / U))
    return np.tile(soft, (1, reps))[:, :INC]
def binarize_rows(out2d, med):
    return (out2d > med[None, :]).astype(np.uint8)
def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem
def softmax(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()

class OffChipHead:
    """host-CPU Elman RNN — byte-match PR#1697 branching head. NO torch/sklearn/GPU. Explicitly host-side."""
    def __init__(self, d_in, d_h, n_out, seed=0):
        rng = np.random.default_rng(seed)
        s1 = 1.0/np.sqrt(d_in); s2 = 1.0/np.sqrt(d_h)
        self.Wxh = rng.normal(0, s1, (d_h, d_in)); self.Whh = rng.normal(0, s2, (d_h, d_h))
        self.Wo  = rng.normal(0, s2, (n_out, d_h)); self.d_h = d_h
    def fit(self, seqs, epochs, lr, clip):
        for ep in range(epochs):
            order = np.random.default_rng(SEED + ep).permutation(len(seqs))
            tot_loss = 0.0; ntok = 0
            for si in order:
                C, Y = seqs[si]; T = C.shape[0]
                hs = [np.zeros(self.d_h)]; ps = []
                for t in range(T):
                    a = self.Wxh @ C[t] + self.Whh @ hs[-1]; h = np.tanh(a); hs.append(h)
                    ps.append(softmax(self.Wo @ h))
                gWxh = np.zeros_like(self.Wxh); gWhh = np.zeros_like(self.Whh); gWo = np.zeros_like(self.Wo)
                dh_next = np.zeros(self.d_h)
                for t in reversed(range(T)):
                    p = ps[t].copy(); p[Y[t]] -= 1.0
                    tot_loss += -np.log(max(ps[t][Y[t]], 1e-12)); ntok += 1
                    gWo += np.outer(p, hs[t+1]); dh = self.Wo.T @ p + dh_next
                    da = (1.0 - hs[t+1]**2) * dh
                    gWxh += np.outer(da, C[t]); gWhh += np.outer(da, hs[t]); dh_next = self.Whh.T @ da
                for g in (gWxh, gWhh, gWo):
                    n = np.linalg.norm(g)
                    if n > clip: g *= clip / n
                self.Wxh -= lr*gWxh; self.Whh -= lr*gWhh; self.Wo -= lr*gWo
            if ep == epochs-1 or ep % 20 == 0:
                print("[3b]   off-chip head BPTT epoch %d/%d CE=%.4f" % (ep+1, epochs, tot_loss/max(1,ntok))); sys.stdout.flush()
    def step(self, c, h):
        h2 = np.tanh(self.Wxh @ c + self.Whh @ h); return self.Wo @ h2, h2

# ----------------------------------------------------------------------------
count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted_full = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
NC_FULL = len(concepts_sorted_full)
codes_enc_full = enc_whitened(H)
def code_of_full(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc_full[idx[0]] if len(idx) else None
def succ_set(i, NC): return sorted(set((i + d) % NC for d in DELTAS))

print("[3b] SUBSTRATE = HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure AKIDA, NOT Lane G")
print("[3b] akida %s device %s ip %s  corpus concepts=%d langs=%d anchors=%d  DELTAS=%s B=%d" %
      (akida.__version__, DEV.version, DEV.ip_version, NC_FULL, len(langs), count, DELTAS, B_FACTOR)); sys.stdout.flush()
print("[3b] ===== 3B CHIP-FIT / PAGING CAPACITY LADDER (a_scale_honest_scope, %d rungs) =====" % len(LADDER)); sys.stdout.flush()

def run_rung(D, U, NC):
    """Depth-D paged encoder of U-unit FCs (single-residency layerpage) feeding the byte-match branching held-out
    composition test at codebook size NC. Returns a per-rung result dict."""
    concepts_sorted = concepts_sorted_full[:NC]
    N_TRAIN = NC - max(K_ROLL + 1, int(round(NC * N_TEST_FRAC)))
    TRAIN_IDX = set(range(0, N_TRAIN))
    def code_of(c, l): return code_of_full(c, l)
    # bound branching transition train set (byte-match branching encoder fit surface)
    train_codes = []
    for l in langs:
        for i in range(NC):
            a = code_of(concepts_sorted[i], l)
            if a is None: continue
            for j in succ_set(i, NC):
                b = code_of(concepts_sorted[j], l)
                if b is None: continue
                train_codes.append(bind(a, b))
    train_codes = np.stack(train_codes)
    per_fc_params = U * INC * NW
    paged_params = D * per_fc_params
    print("[3b] --- RUNG D=%d U=%d NC=%d : per_fc_params=%d paged_params=%d (%.4g) train_transitions=%d ---" %
          (D, U, NC, per_fc_params, paged_params, paged_params, train_codes.shape[0])); sys.stdout.flush()

    train_acc_trials = [[] for _ in range(K_ROLL)]; held_acc_trials = [[] for _ in range(K_ROLL)]
    fc_map_all = True; fc_learn_all = True; last_held_preds = None; ceiling_note = "OK"
    for tr in range(NTRIALS):
        # --- DEPTH-D PAGED ENCODER fit on the live mesh (single-residency) ---
        paged_w = []; cur_in = train_codes; ok = True
        for d in range(D):
            mapped, learned, post_w, soft, note = chip_fit_forward(U, cur_in, do_fit=True)
            if not mapped:
                fc_map_all = False; ok = False; ceiling_note = "RUNG-CEILING(map): FC%d U=%d %s" % (d+1, U, note)
                print("[3b] CHIP-FIT CEILING at D=%d U=%d FC%d: %s" % (D, U, d+1, note)); sys.stdout.flush(); break
            fc_learn_all = fc_learn_all and learned
            paged_w.append(post_w)
            # fold U-wide soft -> INC, binarize on its own median -> next FC's 1-bit input
            soft_inc = fold_to_inc(soft); med = np.median(soft_inc, axis=0)
            cur_in = binarize_rows(soft_inc, med)
        if not ok:
            break
        # encoder code for a concept = depth-D paged forward of its neutral-bound code, folded to INC, binarized
        med_chain = []
        def enc_concept(c, ql):
            a = code_of(c, ql)
            if a is None: a = code_of(concepts_sorted[0], ql)
            x = neutral_bind(a)[None, :]
            for d in range(D):
                soft = chip_forward_paged(U, paged_w[d], x)
                soft_inc = fold_to_inc(soft)
                if len(med_chain) <= d: med_chain.append(np.median(soft_inc, axis=0)) if soft_inc.shape[0] > 1 else med_chain.append(np.zeros(INC))
                x = (soft_inc > 0.0).astype(np.uint8)  # per-row sign threshold (single row at gen time)
            return x[0].astype(np.float64)

        code_cache = {}
        def cc(c, l):
            k = (c, l)
            if k not in code_cache: code_cache[k] = enc_concept(c, l)
            return code_cache[k]
        # off-chip head training seqs (byte-match branching: random branching walks, TRAIN-only targets)
        walk_rng = np.random.default_rng(SEED + 7919 * tr)
        train_concepts = [i for i in range(N_TRAIN) if code_of(concepts_sorted[i], langs[0]) is not None]
        seqs = []
        for l in langs:
            for _w in range(WALKS_PER_LANG):
                cur = int(walk_rng.choice(train_concepts)); Cseq = []; Yseq = []
                for _s in range(WALK_LEN):
                    nxts = [j for j in succ_set(cur, NC) if j in TRAIN_IDX]
                    if not nxts: break
                    nxt = int(walk_rng.choice(nxts)); Cseq.append(cc(concepts_sorted[cur], l)); Yseq.append(nxt); cur = nxt
                if len(Cseq) >= 2:
                    Y = np.array(Yseq, dtype=np.int64)
                    assert all(int(y) in TRAIN_IDX for y in Y), "held-out leak"
                    seqs.append((np.stack(Cseq), Y))
        head = OffChipHead(d_in=INC, d_h=D_H, n_out=NC, seed=SEED + tr)
        head.fit(seqs, epochs=EPOCHS, lr=LR, clip=GRAD_CLIP)

        def rollout(start_idxs):
            preds = [[] for _ in range(K_ROLL)]
            for (ti, ql) in start_idxs:
                cur = ti; banned = concepts_sorted[cur]; h = np.zeros(head.d_h)
                for k in range(K_ROLL):
                    logits, h = head.step(cc(concepts_sorted[cur], ql), h)
                    order = np.argsort(-logits); pred = None
                    for j in order:
                        if j < NC and concepts_sorted[j] != banned: pred = j; break
                    preds[k].append((ti, cur, ql, pred))
                    if pred is None: break
                    banned = concepts_sorted[pred]; cur = pred
            return preds
        train_starts = [(i, l) for i in range(N_TRAIN) for l in langs if code_of(concepts_sorted[i], l) is not None]
        held_starts = [(i, l) for i in range(N_TRAIN, NC) for l in langs if code_of(concepts_sorted[i], l) is not None]
        tr_preds = rollout(train_starts); he_preds = rollout(held_starts)
        def setacc_at(preds, k0):
            hit, tot = 0, 0
            for (ti, cur, ql, pred) in preds[k0]:
                if pred is None: continue
                tot += 1; hit += int(pred in succ_set(cur, NC))
            return hit / max(1, tot)
        for k0 in range(K_ROLL):
            train_acc_trials[k0].append(setacc_at(tr_preds, k0)); held_acc_trials[k0].append(setacc_at(he_preds, k0))
        last_held_preds = he_preds
        print("[3b] RUNG D=%d U=%d trial %d: TRAIN=%s HELD=%s map_all=%s learn_all=%s" %
              (D, U, tr, ["%.4f" % train_acc_trials[k][-1] for k in range(K_ROLL)],
               ["%.4f" % held_acc_trials[k][-1] for k in range(K_ROLL)], fc_map_all, fc_learn_all)); sys.stdout.flush()

    chip_fit = bool(fc_map_all and fc_learn_all and last_held_preds is not None)
    chance = B_FACTOR / (NC - 1)
    per_hop = []
    if last_held_preds is not None:
        def shuffle_null_set_at(preds, k0, B=B_SHUFFLE, seed=SEED):
            rng = np.random.default_rng(seed + 1009 * (k0 + 1)); null = []
            for _ in range(B):
                perm = rng.permutation(NC); hit, tot = 0, 0
                for (ti, cur, ql, pred) in preds[k0]:
                    if pred is None: continue
                    tot += 1; hit += int(pred in succ_set(int(perm[cur]), NC))
                null.append(hit / max(1, tot))
            return np.array(null)
        for k0 in range(K_ROLL):
            tm, tsd, tsem, tlo, thi = ci(train_acc_trials[k0]); hm, hsd, hsem, hlo, hhi = ci(held_acc_trials[k0])
            null = shuffle_null_set_at(last_held_preds, k0); nmean, nsd = float(null.mean()), float(null.std())
            nhi = nmean + 1.96*nsd; p = float((null >= hm).sum() + 1) / (len(null) + 1)
            above = bool(chip_fit and hlo > nhi and p < 0.05)
            per_hop.append({"hop": k0+1, "train": round(tm, 4), "held": round(hm, 4), "held_ci_lo": round(hlo, 4),
                            "shuf_null_hi": round(nhi, 4), "p": round(p, 4), "chance": round(chance, 4),
                            "held_above_null": above})
            print("[3b] RUNG D=%d U=%d hop %d: TRAIN=%.4f HELD=%.4f | held ci_lo=%.4f NULL hi=%.4f p=%.4f | aboveNULL=%s"
                  % (D, U, k0+1, tm, hm, hlo, nhi, p, above)); sys.stdout.flush()
    comp_survives = bool(per_hop and per_hop[1]["held_above_null"] and per_hop[2]["held_above_null"])
    return {"D": D, "U": U, "NC": NC, "per_fc_params": per_fc_params, "paged_params": paged_params,
            "fc_map_all": fc_map_all, "fc_learn_all": fc_learn_all, "chip_fit": chip_fit,
            "ceiling_note": ceiling_note, "per_hop": per_hop, "comp_survives": comp_survives,
            "decay_TRAIN": [per_hop[k]["train"] for k in range(len(per_hop))] if per_hop else [],
            "decay_HELD": [per_hop[k]["held"] for k in range(len(per_hop))] if per_hop else []}

RESULTS = {"substrate": "HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)",
           "milestone": "Lane A 3B — chip-fit/paging capacity ladder (a_scale_honest_scope >=3 rungs)",
           "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "INC": INC, "NW": NW,
           "off_chip_hidden": D_H, "off_chip_epochs": EPOCHS, "K_roll": K_ROLL,
           "branching_operator": {"deltas": DELTAS, "B_factor": B_FACTOR, "rule": "succ(i)={(i+d) mod NC}"},
           "target_3b_params": TARGET_3B, "n_anchors": int(count),
           "layerpage": "single-FC-residency on 8MB SRAM mesh; depth-D paged encoder, each FC fit live then paged OFF to host",
           "ladder_spec": LADDER, "rungs": []}
ladder_results = []
for rung in LADDER:
    r = run_rung(rung["D"], rung["U"], rung["NC"]); r["tag"] = rung["tag"]
    ladder_results.append(r); RESULTS["rungs"].append(r)
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_3b_chipfit.json"), "w"), indent=2)

# ---- falsifier dispositions ----
chipfit_rungs = [r for r in ladder_results if r["chip_fit"]]
max_paged = max((r["paged_params"] for r in chipfit_rungs), default=0)
reached_3b = bool(max_paged >= TARGET_3B)
# the chip-fit ceiling = the first rung that FAILED to map/learn (named precisely), else the largest chip-fit rung
ceiling_rung = next((r for r in ladder_results if not r["chip_fit"]), None)
ceiling_recorded = ceiling_rung is not None
# F-3B-1: composition survives at EVERY chip-fit rung
F_3B_1 = bool(chipfit_rungs) and all(r["comp_survives"] for r in chipfit_rungs)
# F-3B-2: reached 3B-class OR a precise chip-fit ceiling recorded
F_3B_2 = bool(reached_3b or ceiling_recorded)
RESULTS["headline"] = {
    "chip_fit_rungs": [(r["D"], r["U"], r["NC"], r["paged_params"]) for r in chipfit_rungs],
    "max_chip_fit_paged_params": max_paged, "reached_3b_class": reached_3b,
    "ceiling_rung": ({"D": ceiling_rung["D"], "U": ceiling_rung["U"], "paged_params": ceiling_rung["paged_params"],
                      "note": ceiling_rung["ceiling_note"]} if ceiling_rung else None),
    "F_3B_1_composition_survives_ladder": F_3B_1, "F_3B_2_reached_3b_or_ceiling": F_3B_2,
}
if reached_3b and F_3B_1:
    disp = ("3B-CLASS REACHED + COMPOSITION PRESERVED — the depth-D paged encoder scaled to >=3e9 paged params on the "
            "single 8MB-SRAM AKD1000 mesh (layerpage single-residency) WHILE the branching held-out hop-2/3 composition "
            "stayed above the shuffle-NULL at every chip-fit rung. Lane A 3B milestone CLOSES (HYBRID-scoped). max paged "
            "params=%.4g." % max_paged)
elif F_3B_1 and ceiling_recorded:
    disp = ("CHIP-FIT CEILING REACHED BEFORE 3B-CLASS (a_scale_honest_scope — a QUANTIFIED hardware ceiling is a VALID "
            "closed result, NOT a failure). Composition (held-out hop-2/3 above shuffle-NULL) was PRESERVED at every "
            "chip-fit rung up to the ceiling. The ladder reached max chip-fit paged params=%.4g; the precise ceiling = "
            "rung D=%d U=%d (paged_params=%.4g): %s. Lane A 3B milestone STAYS OPEN with the named SRAM/paging limit; "
            "no 3B claim fabricated." % (max_paged, ceiling_rung["D"], ceiling_rung["U"], ceiling_rung["paged_params"],
            ceiling_rung["ceiling_note"]))
elif F_3B_1 and not ceiling_recorded:
    disp = ("LADDER COMPLETED WITHOUT A MAP/LEARN CEILING but did NOT reach 3B-class paged params (max=%.4g). Composition "
            "preserved at every rung. The ladder's stated top rung is the chip-fit frontier PROBED; extending toward 3B "
            "needs more/wider paged FCs. Lane A 3B milestone STAYS OPEN; honest sub-3B scope recorded (no fabricated 3B)."
            % max_paged)
else:
    breaks = [(r["D"], r["U"], r["NC"]) for r in chipfit_rungs if not r["comp_survives"]]
    disp = ("COMPOSITION DEGRADES UNDER CAPACITY SCALING (honest closed-negative, a_paper_negative_ok) — the branching "
            "held-out composition dropped into the shuffle-NULL at chip-fit rung(s) %s before reaching 3B-class. Capacity "
            "scaling via deeper/wider paged FCs does NOT preserve the multi-step composition at this toy corpus. Lane A 3B "
            "milestone STAYS OPEN; the rung where composition breaks is recorded." % breaks)
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_3b_chipfit.json"), "w"), indent=2)

print("\n[3b] ========== 3B CHIP-FIT / PAGING LADDER DISPOSITION ==========")
print("[3b] SUBSTRATE : HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)")
print("[3b] LADDER (per rung: D paged FCs x U units x NC codebook -> paged params; chip-fit; held-out decay):")
for r in ladder_results:
    print("[3b]   D=%d U=%-4d NC=%d  paged_params=%-12d (%.4g)  map_all=%s learn_all=%s chip_fit=%s comp_survives=%s  decay_HELD=%s  %s"
          % (r["D"], r["U"], r["NC"], r["paged_params"], r["paged_params"], r["fc_map_all"], r["fc_learn_all"],
             r["chip_fit"], r["comp_survives"], r["decay_HELD"], r["tag"]))
    if not r["chip_fit"] and r["ceiling_note"] != "OK":
        print("[3b]      ^ CEILING: %s" % r["ceiling_note"])
print("[3b] max chip-fit paged params : %.4g  (3B target=%.4g)" % (max_paged, TARGET_3B))
print("[3b] reached 3B-class          :", reached_3b)
print("[3b] chip-fit ceiling recorded :", ceiling_recorded, ("" if not ceiling_rung else
      "rung D=%d U=%d paged=%.4g : %s" % (ceiling_rung["D"], ceiling_rung["U"], ceiling_rung["paged_params"], ceiling_rung["ceiling_note"])))
print("[3b] F-3B-1 (comp survives ladder) :", F_3B_1)
print("[3b] F-3B-2 (3B reached OR ceiling):", F_3B_2)
print("[3b] DISPOSITION :", RESULTS["DISPOSITION"])
print("[3b] wrote " + os.path.join(OUT, "result_onchip_xlm_3b_chipfit.json"))
