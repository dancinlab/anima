#!/usr/bin/env python3
"""Lane A 3B MILESTONE — HYBRID OFF-CHIP HEAD SCALE-UP ladder (the NAMED BRIDGE from PR#1705/F-3B).
   substrate = HYBRID (on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure-AKIDA, NOT Lane G/GPU.

WHERE WE ARE (PR#1705/F-3B closed-negative): scaling the ON-CHIP encoder via deeper/wider 1-bit Hebbian paged FCs
  DESTROYS the single-step transition signal (composition survives ONLY at D=1/256-unit/~524K-param). The KEY
  HARDWARE FINDING named the bridge: the composition surface that SCALES is the OFF-CHIP head (which already
  generalized at D=1, PR#1697 held-out hop-2/3 0.90/0.96 > shuffle-NULL). paged 1-bit Hebbian depth = CLOSED axis.

THIS RUNG (a_completeness_over_cheap primary path): KEEP the chip as the PROVEN D=1 single 256-unit FC encoder
  (~524K params; byte-identical build_fc/chip_make/chip_forward/enc_whitened/bind to PR#1697 onchip_xlm_branching.py)
  and SCALE THE OFF-CHIP HOST DECODE HEAD toward 3B-class params. The off-chip head is plain host compute (capacity is
  free there). We sweep >=3 head-capacity rungs (wider hidden D_H + stacked recurrent layers) toward 3B-class and run
  the byte-match BRANCHING held-out split (disjoint successors, set-membership metric, shuffle-NULL B=200) at each rung.

OFF-CHIP HEAD = a MULTI-LAYER Elman RNN (host CPU, numpy, NO torch/sklearn/GPU). Layer-0 input = the FIXED on-chip
  256-unit 1-bit code (INC=256). Each recurrent layer l: h_l = tanh(Wxh_l @ x_l + Whh_l @ h_l_prev). Output: Wo @ h_top.
  byte-match the PR#1697 single-layer head at the D=1 rung (NLAYERS=1, D_H=64) so the baseline reproduces.
  HEAD PARAM COUNT (the off-chip capacity we scale): for L layers of width D_H, input INC, NC outputs:
      layer0 : Wxh = D_H*INC ; Whh = D_H*D_H
      layer1..L-1 : Wxh = D_H*D_H ; Whh = D_H*D_H
      output : Wo = NC*D_H
      head_params = D_H*INC + D_H*D_H + (L-1)*(2*D_H*D_H) + NC*D_H
  TOTAL HYBRID params = head_params + CHIP_ENCODER_PARAMS (fixed 524288 = 256 units * 256 inputs * 8 weights).
  chip_fraction = CHIP_ENCODER_PARAMS / total_params (DEFINITIONAL HONESTY: a 3B head + 524K chip = HYBRID 3B, and if
  the chip becomes a trivial fraction we say so explicitly — that is NOT a pure-AKIDA 3B; a_scale_honest_scope).

LADDER (>=3 rungs of increasing OFF-CHIP head capacity toward 3B-class; the chip encoder is FIXED at D=1/256-unit/524K):
  rung 0 : NLAYERS=1  D_H=64    — branching baseline (byte-match PR#1697)              ~few-x-10K head params
  rung 1 : NLAYERS=2  D_H=512   — wider + 2-layer                                       ~1M head params
  rung 2 : NLAYERS=3  D_H=2048  — deep + wide                                           ~30M head params
  rung 3 : NLAYERS=4  D_H=8192  — 3B-class probe (head_params ~ (L-1)*2*D_H^2)          ~400M head params
  rung 4 : NLAYERS=6  D_H=24576 — 3B-class reach probe ((6-1)*2*24576^2 ~ 6.04e9)        >3B head params
  (we COMPUTE the exact param count per rung and report whether >=3e9 is reached; the BPTT actually RUNS the head at
   each rung on the live chip codes. For the very large rungs we cap BPTT EPOCHS lower so the wall time is bounded —
   the falsifier is about composition SURVIVING the capacity, and a larger head should not LOSE the operator it learns
   at small capacity; if it cannot fit at all that is itself the finding.)

PRE-REGISTERED FALSIFIERS (g63 honest, declared in-file BEFORE the run):
  metric: per rung, held-out hop-2/3 branching set-membership vs shuffle-NULL (B=200). CHANCE = B/(NC-1).
  F-3B-HYBRID-1 (composition survives as the off-chip head scales toward 3B-class): "held-out hop-2 AND hop-3
          set-membership do NOT stay ABOVE the shuffle-NULL as the off-chip head scales."
          -> REFUTED iff for EVERY head-scale rung, for k in {2,3}: heldout_setacc[k] ci_lo > shuffle_null[k] hi AND p<0.05.
  F-3B-HYBRID-2 (a 3B-class param count is reached WITH composition intact): "the ladder neither reaches a 3B-class
          total param count NOR preserves composition at the largest rung that DOES reach 3B-class."
          -> REFUTED iff at some rung total_params >= 3e9 AND that rung's held-out hop-2/3 are above the shuffle-NULL.
  DEFINITIONAL-HONESTY GATE (a_scale_honest_scope, the HARD gate): we ALWAYS report chip_fraction at the 3B-class rung.
          If reaching 3B-class requires the chip to be a TRIVIAL fraction (chip_fraction < 1e-3) we record the HONEST
          terminal: a 3B-class HYBRID exists but it is essentially ALL off-chip host compute; the on-chip AKIDA
          contribution is the fixed ~524K D=1 encoder. We do NOT relabel a host model as "AKIDA 3B".
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
UNITS, NW, LCOMP = 256, 8, 0.1     # ON-CHIP FC: FIXED D=1 256-unit encoder — byte-match PR#1697 branching rung
SHIFT = 37
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
K_ROLL = 3
SEED = 20260602
CHIP_ENCODER_PARAMS = UNITS * INC * NW   # 524288 — the fixed on-chip D=1 contribution (a_scale_honest_scope honesty)
# ---- OFF-CHIP head BPTT hyperparams — byte-match PR#1697 at the baseline rung ----
LR = 0.05
GRAD_CLIP = 5.0
# ---- branching operator + held-out split (byte-match PR#1697) ----
DELTAS = [1, 7, 19]
B_FACTOR = len(DELTAS)
WALK_LEN = 6
WALKS_PER_LANG = 24
GEN_FACTOR = 2.0
N_TEST_FRAC = 0.30
NC = 50                            # full toy codebook (the composition test scale)
TARGET_3B = 3e9
# ---- 3B OFF-CHIP HEAD SCALE-UP LADDER (pre-registered; >=3 rungs of increasing OFF-CHIP head capacity) ----
# Each rung scales the OFF-CHIP head (NLAYERS x D_H) toward 3B-class; the chip encoder is FIXED D=1/256-unit/524K.
# EPOCHS scaled down for the very large rungs to bound wall time (the falsifier is composition SURVIVAL under capacity).
LADDER = [
    {"NLAYERS": 1, "D_H": 64,    "EPOCHS": 60, "tag": "baseline(branching PR#1697) NLAYERS=1 D_H=64"},
    {"NLAYERS": 2, "D_H": 512,   "EPOCHS": 40, "tag": "wide+2-layer"},
    {"NLAYERS": 3, "D_H": 2048,  "EPOCHS": 24, "tag": "deep+wide ~30M head"},
    {"NLAYERS": 4, "D_H": 8192,  "EPOCHS": 10, "tag": "3B-class probe ~400M head"},
    {"NLAYERS": 6, "D_H": 24576, "EPOCHS": 4,  "tag": "3B-class REACH probe (>3e9 head params)"},
]

def head_param_count(NLAYERS, D_H, n_out=NC, d_in=INC):
    p = D_H * d_in + D_H * D_H            # layer 0: Wxh + Whh
    p += (NLAYERS - 1) * (2 * D_H * D_H)  # layers 1..L-1: Wxh(D_H*D_H) + Whh(D_H*D_H)
    p += n_out * D_H                      # output Wo
    return p

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
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback for the chip encoder")
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
def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem
def softmax(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()

class OffChipHeadML:
    """MULTI-LAYER host-CPU Elman RNN (numpy, NO torch/sklearn/GPU). NLAYERS recurrent layers of width D_H.
    NLAYERS=1,D_H=64 is byte-identical to the PR#1697 single-layer head (same Wxh/Whh/Wo shapes + BPTT).
    Explicitly OFF-CHIP host-side; the on-chip 256-unit code is the FIXED layer-0 input."""
    def __init__(self, d_in, d_h, n_layers, n_out, seed=0):
        rng = np.random.default_rng(seed)
        self.L = n_layers; self.d_h = d_h
        self.Wxh = []; self.Whh = []
        for l in range(n_layers):
            din = d_in if l == 0 else d_h
            s1 = 1.0/np.sqrt(din); s2 = 1.0/np.sqrt(d_h)
            self.Wxh.append(rng.normal(0, s1, (d_h, din)))
            self.Whh.append(rng.normal(0, s2, (d_h, d_h)))
        self.Wo = rng.normal(0, 1.0/np.sqrt(d_h), (n_out, d_h))
    def fit(self, seqs, epochs, lr, clip):
        for ep in range(epochs):
            order = np.random.default_rng(SEED + ep).permutation(len(seqs))
            tot_loss = 0.0; ntok = 0
            for si in order:
                C, Y = seqs[si]; T = C.shape[0]
                # forward: per-layer hidden states over time
                hs = [[np.zeros(self.d_h) for _ in range(self.L)]]  # hs[t][l]
                xs = []  # xs[t][l] = input to layer l at time t (for grads)
                ps = []
                for t in range(T):
                    layer_in = C[t]; new_h = []; xrow = []
                    for l in range(self.L):
                        xrow.append(layer_in)
                        a = self.Wxh[l] @ layer_in + self.Whh[l] @ hs[-1][l]
                        h = np.tanh(a); new_h.append(h); layer_in = h
                    xs.append(xrow); hs.append(new_h)
                    ps.append(softmax(self.Wo @ new_h[-1]))
                gWxh = [np.zeros_like(w) for w in self.Wxh]
                gWhh = [np.zeros_like(w) for w in self.Whh]
                gWo = np.zeros_like(self.Wo)
                dh_next = [np.zeros(self.d_h) for _ in range(self.L)]
                for t in reversed(range(T)):
                    p = ps[t].copy(); p[Y[t]] -= 1.0
                    tot_loss += -np.log(max(ps[t][Y[t]], 1e-12)); ntok += 1
                    gWo += np.outer(p, hs[t+1][self.L-1])
                    dh_top = self.Wo.T @ p
                    dh_in_above = dh_top
                    for l in reversed(range(self.L)):
                        dh = dh_in_above + dh_next[l]
                        da = (1.0 - hs[t+1][l]**2) * dh
                        gWxh[l] += np.outer(da, xs[t][l])
                        gWhh[l] += np.outer(da, hs[t][l])
                        dh_next[l] = self.Whh[l].T @ da
                        dh_in_above = self.Wxh[l].T @ da  # gradient flowing to the layer below (its output = this input)
                allg = gWxh + gWhh + [gWo]
                for g in allg:
                    n = np.linalg.norm(g)
                    if n > clip: g *= clip / n
                for l in range(self.L):
                    self.Wxh[l] -= lr * gWxh[l]; self.Whh[l] -= lr * gWhh[l]
                self.Wo -= lr * gWo
            if ep == epochs - 1 or ep % max(1, epochs//3) == 0:
                print("[3bH]   off-chip head BPTT epoch %d/%d  CE=%.4f" % (ep+1, epochs, tot_loss/max(1,ntok)))
                sys.stdout.flush()
    def step(self, c, hstate):
        layer_in = c; new_h = []
        for l in range(self.L):
            h = np.tanh(self.Wxh[l] @ layer_in + self.Whh[l] @ hstate[l]); new_h.append(h); layer_in = h
        return self.Wo @ new_h[-1], new_h
    def zero_state(self):
        return [np.zeros(self.d_h) for _ in range(self.L)]

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
def succ_set(i, NCv): return sorted(set((i + d) % NCv for d in DELTAS))

print("[3bH] SUBSTRATE = HYBRID(on-chip AKD1000 D=1 256-unit encoder ⊕ off-chip host-CPU MULTI-LAYER decode head) — NOT pure AKIDA, NOT Lane G")
print("[3bH] akida %s device %s ip %s  corpus concepts=%d langs=%d anchors=%d  DELTAS=%s B=%d  NC=%d" %
      (akida.__version__, DEV.version, DEV.ip_version, NC_FULL, len(langs), count, DELTAS, B_FACTOR, NC)); sys.stdout.flush()
print("[3bH] CHIP encoder FIXED at D=1/256-unit = %d params (%.4g). Scaling the OFF-CHIP head toward 3B-class." %
      (CHIP_ENCODER_PARAMS, CHIP_ENCODER_PARAMS)); sys.stdout.flush()
print("[3bH] ===== 3B OFF-CHIP HEAD SCALE-UP LADDER (a_scale_honest_scope, %d rungs) =====" % len(LADDER)); sys.stdout.flush()

concepts_sorted = concepts_sorted_full[:NC]
N_TRAIN = NC - max(K_ROLL + 1, int(round(NC * N_TEST_FRAC)))
TRAIN_IDX = set(range(0, N_TRAIN)); TEST_IDX = set(range(N_TRAIN, NC))
def code_of(c, l): return code_of_full(c, l)
# ON-CHIP encoder fit transitions (full branching edges; byte-match PR#1697)
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
print("[3bH] NC=%d N_TRAIN=%d (idx 0..%d) N_TEST=%d (idx %d..%d) on-chip enc transitions=%d" %
      (NC, N_TRAIN, N_TRAIN-1, NC-N_TRAIN, N_TRAIN, NC-1, train_codes.shape[0])); sys.stdout.flush()

def chip_code_for_concept(m, c, ql, med):
    a = code_of(c, ql)
    if a is None: a = code_of(concepts_sorted[0], ql)
    g_soft = chip_forward(m, neutral_bind(a))
    return binarize_rows(g_soft, med)[0].astype(np.float64)

def run_rung(NLAYERS, D_H, EPOCHS):
    head_params = head_param_count(NLAYERS, D_H)
    total_params = head_params + CHIP_ENCODER_PARAMS
    chip_fraction = CHIP_ENCODER_PARAMS / total_params
    print("[3bH] --- RUNG NLAYERS=%d D_H=%d EPOCHS=%d : head_params=%d (%.4g) +chip %d = total %d (%.4g) chip_frac=%.3g ---" %
          (NLAYERS, D_H, EPOCHS, head_params, head_params, CHIP_ENCODER_PARAMS, total_params, total_params, chip_fraction))
    sys.stdout.flush()
    train_starts = [(i, l) for i in range(N_TRAIN) for l in langs if code_of(concepts_sorted[i], l) is not None]
    held_starts = [(i, l) for i in range(N_TRAIN, NC) for l in langs if code_of(concepts_sorted[i], l) is not None]
    train_acc_trials = [[] for _ in range(K_ROLL)]; held_acc_trials = [[] for _ in range(K_ROLL)]
    learn_all = True; last_held_preds = None
    for tr in range(NTRIALS):
        init = get_w(build_fc(1))
        m, learned = chip_make(init, train_codes, do_fit=True)   # FIXED D=1 on-chip encoder, live AKD1000
        train_soft = chip_forward(m, train_codes); med = np.median(train_soft, axis=0)
        code_cache = {}
        def cc(c, l):
            k = (c, l)
            if k not in code_cache: code_cache[k] = chip_code_for_concept(m, c, l, med)
            return code_cache[k]
        # off-chip head training seqs (byte-match PR#1697: random branching walks, TRAIN-only targets)
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
        head = OffChipHeadML(d_in=INC, d_h=D_H, n_layers=NLAYERS, n_out=NC, seed=SEED + tr)
        head.fit(seqs, epochs=EPOCHS, lr=LR, clip=GRAD_CLIP)
        def rollout(start_idxs):
            preds = [[] for _ in range(K_ROLL)]
            for (ti, ql) in start_idxs:
                cur = ti; banned = concepts_sorted[cur]; h = head.zero_state()
                for k in range(K_ROLL):
                    logits, h = head.step(cc(concepts_sorted[cur], ql), h)
                    order = np.argsort(-logits); pred = None
                    for j in order:
                        if j < NC and concepts_sorted[j] != banned: pred = j; break
                    preds[k].append((ti, cur, ql, pred))
                    if pred is None: break
                    banned = concepts_sorted[pred]; cur = pred
            return preds
        tr_preds = rollout(train_starts); he_preds = rollout(held_starts)
        del m
        learn_all = learn_all and learned
        def setacc_at(preds, k0):
            hit, tot = 0, 0
            for (ti, cur, ql, pred) in preds[k0]:
                if pred is None: continue
                tot += 1; hit += int(pred in succ_set(cur, NC))
            return hit / max(1, tot)
        for k0 in range(K_ROLL):
            train_acc_trials[k0].append(setacc_at(tr_preds, k0)); held_acc_trials[k0].append(setacc_at(he_preds, k0))
        last_held_preds = he_preds
        print("[3bH] RUNG NL=%d D_H=%d trial %d: TRAIN=%s HELD=%s enc_learned=%s" %
              (NLAYERS, D_H, tr, ["%.4f" % train_acc_trials[k][-1] for k in range(K_ROLL)],
               ["%.4f" % held_acc_trials[k][-1] for k in range(K_ROLL)], learned)); sys.stdout.flush()
    chance = B_FACTOR / (NC - 1)
    def shuffle_null_set_at(preds, k0, B=B_SHUFFLE, seed=SEED):
        rng = np.random.default_rng(seed + 1009 * (k0 + 1)); null = []
        for _ in range(B):
            perm = rng.permutation(NC); hit, tot = 0, 0
            for (ti, cur, ql, pred) in preds[k0]:
                if pred is None: continue
                tot += 1; hit += int(pred in succ_set(int(perm[cur]), NC))
            null.append(hit / max(1, tot))
        return np.array(null)
    per_hop = []
    for k0 in range(K_ROLL):
        tm, tsd, tsem, tlo, thi = ci(train_acc_trials[k0]); hm, hsd, hsem, hlo, hhi = ci(held_acc_trials[k0])
        null = shuffle_null_set_at(last_held_preds, k0); nmean, nsd = float(null.mean()), float(null.std())
        nhi = nmean + 1.96*nsd; p = float((null >= hm).sum() + 1) / (len(null) + 1)
        above = bool(learn_all and hlo > nhi and p < 0.05)
        per_hop.append({"hop": k0+1, "train": round(tm, 4), "held": round(hm, 4), "held_ci_lo": round(hlo, 4),
                        "shuf_null_hi": round(nhi, 4), "p": round(p, 4), "chance": round(chance, 4),
                        "held_above_null": above})
        print("[3bH] RUNG NL=%d D_H=%d hop %d: TRAIN=%.4f HELD=%.4f | held ci_lo=%.4f NULL hi=%.4f p=%.4f | aboveNULL=%s"
              % (NLAYERS, D_H, k0+1, tm, hm, hlo, nhi, p, above)); sys.stdout.flush()
    comp_survives = bool(per_hop[1]["held_above_null"] and per_hop[2]["held_above_null"])
    return {"NLAYERS": NLAYERS, "D_H": D_H, "EPOCHS": EPOCHS, "head_params": head_params,
            "chip_encoder_params": CHIP_ENCODER_PARAMS, "total_params": total_params,
            "chip_fraction": chip_fraction, "learn_all": learn_all, "per_hop": per_hop,
            "comp_survives": comp_survives,
            "decay_TRAIN": [per_hop[k]["train"] for k in range(K_ROLL)],
            "decay_HELD": [per_hop[k]["held"] for k in range(K_ROLL)]}

RESULTS = {"substrate": "HYBRID(on-chip AKD1000 D=1 256-unit encoder ⊕ off-chip host-CPU multi-layer decode head)",
           "milestone": "Lane A 3B — OFF-CHIP HEAD SCALE-UP ladder (the named bridge from PR#1705/F-3B; a_scale_honest_scope >=3 rungs)",
           "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "INC": INC, "NW": NW,
           "chip_encoder_params": CHIP_ENCODER_PARAMS, "K_roll": K_ROLL, "NC": NC,
           "branching_operator": {"deltas": DELTAS, "B_factor": B_FACTOR, "rule": "succ(i)={(i+d) mod NC}"},
           "target_3b_params": TARGET_3B, "n_anchors": int(count), "ladder_spec": LADDER, "rungs": []}
ladder_results = []
for rung in LADDER:
    r = run_rung(rung["NLAYERS"], rung["D_H"], rung["EPOCHS"]); r["tag"] = rung["tag"]
    ladder_results.append(r); RESULTS["rungs"].append(r)
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_3b_offchip_head.json"), "w"), indent=2)

# ---- falsifier dispositions ----
# F-3B-HYBRID-1: composition survives at EVERY head-scale rung
F_1 = all(r["comp_survives"] for r in ladder_results)
# 3B-class rungs (total params >= 3e9) with composition intact
rungs_3b = [r for r in ladder_results if r["total_params"] >= TARGET_3B]
rungs_3b_comp = [r for r in rungs_3b if r["comp_survives"]]
reached_3b = bool(rungs_3b)
F_2 = bool(rungs_3b_comp)
# chip fraction at the smallest 3B-class rung (definitional honesty)
chip_frac_at_3b = min((r["chip_fraction"] for r in rungs_3b), default=None)
TRIVIAL_CHIP = 1e-3
chip_trivial_at_3b = bool(chip_frac_at_3b is not None and chip_frac_at_3b < TRIVIAL_CHIP)
RESULTS["headline"] = {
    "F_3B_HYBRID_1_composition_survives_scaleup": F_1,
    "F_3B_HYBRID_2_3b_reached_with_composition": F_2,
    "reached_3b_class": reached_3b,
    "max_total_params": max(r["total_params"] for r in ladder_results),
    "chip_fraction_at_3b": chip_frac_at_3b,
    "chip_trivial_at_3b": chip_trivial_at_3b,
    "rungs_3b_class": [(r["NLAYERS"], r["D_H"], r["total_params"], r["comp_survives"], r["chip_fraction"]) for r in rungs_3b],
}
if F_2 and not chip_trivial_at_3b:
    disp = ("HYBRID 3B REACHED WITH COMPOSITION INTACT (honestly hybrid-scoped) — the off-chip head scaled to >=3e9 total "
            "params WHILE held-out hop-2/3 composition stayed above the shuffle-NULL, and the chip is NOT a trivial fraction. "
            "Lane A 3B milestone may flip [x] AS A HYBRID (on-chip D=1 encoder ⊕ off-chip 3B head). NOT pure-AKIDA.")
elif F_2 and chip_trivial_at_3b:
    disp = ("3B-CLASS HYBRID PARAM COUNT REACHED but the on-chip AKIDA contribution is a TRIVIAL fraction (chip_fraction=%.3g "
            "< %.0e) — this is essentially an ALL-OFF-CHIP host model with a fixed ~524K D=1 chip encoder bolted on. "
            "DEFINITIONAL HONESTY (a_scale_honest_scope): this is NOT an honest 'AKIDA/Lane-A 3B'. HONEST TERMINAL — Lane A "
            "on-chip caps at PUBLIC (~524K composition-preserving D=1 encoder); 3B/7B are NOT reachable ON the AKIDA substrate "
            "(quantified hardware capacity ceiling, a closed-negative on the scale axis, a_paper_negative_ok). Lane A 3B stays [ ] "
            "with the documented on-chip ceiling." % (chip_frac_at_3b, TRIVIAL_CHIP))
elif reached_3b and not F_2:
    disp = ("3B-CLASS PARAM COUNT REACHED but COMPOSITION DID NOT SURVIVE at the 3B-class rung(s) (held-out hop-2/3 dropped into "
            "the shuffle-NULL) — scaling the off-chip head to 3B-class did NOT preserve the branching composition. honest "
            "closed-negative (a_paper_negative_ok). Lane A 3B stays [ ] OPEN.")
else:
    disp = ("LADDER DID NOT REACH 3B-CLASS total params (max=%.4g < 3e9). Composition survival across the scaled rungs: F-3B-HYBRID-1=%s. "
            "Honest sub-3B scope recorded; Lane A 3B stays [ ] OPEN (no fabricated 3B)." %
            (RESULTS["headline"]["max_total_params"], F_1))
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_3b_offchip_head.json"), "w"), indent=2)

print("\n[3bH] ========== 3B OFF-CHIP HEAD SCALE-UP LADDER DISPOSITION ==========")
print("[3bH] SUBSTRATE : HYBRID(on-chip AKD1000 D=1 256-unit encoder ⊕ off-chip host-CPU multi-layer decode head)")
print("[3bH] CHIP encoder FIXED = %d params (the on-chip AKIDA contribution, a_scale_honest_scope)" % CHIP_ENCODER_PARAMS)
print("[3bH] LADDER (per rung: NLAYERS x D_H -> head/total params; chip_frac; comp_survives; held-out decay):")
for r in ladder_results:
    print("[3bH]   NL=%d D_H=%-6d head=%-12d total=%-12d (%.4g) chip_frac=%.3g learn_all=%s comp_survives=%s decay_HELD=%s  %s"
          % (r["NLAYERS"], r["D_H"], r["head_params"], r["total_params"], r["total_params"], r["chip_fraction"],
             r["learn_all"], r["comp_survives"], r["decay_HELD"], r["tag"]))
print("[3bH] max total params       : %.4g  (3B target=%.4g)" % (RESULTS["headline"]["max_total_params"], TARGET_3B))
print("[3bH] reached 3B-class        :", reached_3b)
print("[3bH] chip_fraction at 3B     :", chip_frac_at_3b, ("(TRIVIAL <%.0e)" % TRIVIAL_CHIP if chip_trivial_at_3b else ""))
print("[3bH] F-3B-HYBRID-1 (comp survives scale-up):", F_1)
print("[3bH] F-3B-HYBRID-2 (3B reached w/ composition):", F_2)
print("[3bH] DISPOSITION :", RESULTS["DISPOSITION"])
print("[3bH] wrote " + os.path.join(OUT, "result_onchip_xlm_3b_offchip_head.json"))
