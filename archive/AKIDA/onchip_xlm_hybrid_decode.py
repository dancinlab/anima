#!/usr/bin/env python3
"""Lane A HYBRID RUNG — on-chip AKD1000 ENCODER ⊕ off-chip autoregressive DECODE HEAD.
substrate = HYBRID (on-chip encoder ⊕ off-chip decode) — NOT pure on-chip, NOT Lane G/GPU.
a_lane_akida_gpu_split (the on-chip part is AKIDA Lane A; the decode head is explicitly host-side) ·
a_scale_honest_scope (toy 250-anchor) · g63 (the CHIP part has NO sw fallback — device==[] -> abort).

WHERE WE ARE (THREE consecutive on-chip closed-negatives — the hard ceiling):
  PR#1686 (stateless rollout)  : decay [0.4287, 0.0277, 0.0090]  — hop-1 GREEN, hop-2 collapses INTO shuffle-NULL.
  PR#1689 (state-carry input)  : decay [0.4234, 0.0282, 0.0122]  — input-side context-carry does NOT break the wall.
  PR#1690 (multi-FC depth)     : decay [0.1612, 0.0298, 0.0149]  — a SECOND learned on-chip FC does NOT break it
                                  (and even DEGRADES hop-1 0.42->0.16). chance=0.0204.
  VERDICT (triply confirmed): AKD1000 1-bit edge-learn caps at SINGLE-STEP generation regardless of input-state or
  depth at 256-unit/8MB-SRAM capacity. The transition structure has nowhere to LIVE across steps when the only
  learnable surface is a 1-bit Hebbian FC. The named bridges all agreed on ONE remaining path: an OFF-CHIP DECODE HEAD.

THIS RUNG (HYBRID — does off-chip recurrence break the wall the pure chip hit?):
  We KEEP the chip in its proven 🟢 role: the AKD1000 is the on-chip ENCODER / single-step transition surface.
  For each (concept, lang) we run FC1 ON CHIP and read its binarized output code — exactly the codes the chip
  produces today (byte-identical encoder/binarize to onchip_xlm_state_rollout.py). The chip provides the GROUNDED
  concept/transition code; that is all it does. NO chip-to-chip feedback (that is what collapsed 3x).
  The MULTI-STEP recurrence — the thing the 1-bit FC structurally CANNOT carry — lives in a small OFF-CHIP
  autoregressive decode head on the HOST CPU (pure numpy, no sklearn, no GPU, no torch):
    state:  h_0 = 0 (D_H float hidden state, host-side)
    per hop k, given the chip code c_k (on-chip binarized output for the current concept):
        h_{k+1} = tanh( Wxh @ c_k + Whh @ h_k )            # REAL recurrence carried off-chip (RNN cell)
        logits  = Wo @ h_{k+1}                              # next-concept distribution over the codebook
        pred    = argmax over allowed concepts (ban last)
        next chip input concept = pred -> re-encode ON CHIP -> c_{k+1}                  (chip stays the encoder)
    The head is trained (host CPU, BPTT over the teacher-forced on-chip-code sequences) to predict the NEXT concept
    from the running state. Recurrence/state is the OFF-CHIP contribution; grounding/transition code is ON-CHIP.
  HONEST: the chip codes are produced live on AKD1000 (g63, no sw fallback for the chip part). The decode head is
  EXPLICITLY host-CPU — this is the hybrid by design, NOT a a_train_flame_forge violation (it is the reference/eval
  decode head, kept small + honest, NOT the production flame+forge trainer). Tag everything HYBRID(on-chip⊕off-chip).

PRE-REGISTERED FALSIFIERS (g63 honest, declared BEFORE the run):
  metric: hyb_acc[k] = P(argmax decode of the HYBRID head at hop k == concept[ti+k]), k=1..K, over all (seed t,
          query-lang) starts with >=K real successors. Open-vocab over the full concept codebook, ban last emit.
  NULL-A (SHUFFLE) per hop k: hybrid hop-k decode with (seed->gt_k) labels permuted (B=200); per-hop hi+p.
  CHANCE: 1/(NC-1) open-vocab uniform.
  PURE-ON-CHIP BASELINES (the wall we must break): best pure-on-chip multi-step hop2 = 0.0298 (PR#1690), hop2 across
          all three = {0.0277, 0.0282, 0.0298}; hop3 = {0.0090, 0.0122, 0.0149}. best_pure_hop2 = 0.0298.
  FALSIFIER F-HYBRID-1 (off-chip recurrence breaks the 1-hop wall): "the hybrid multi-step (K>=3) accuracy does NOT
          stay above the shuffle-NULL at hop-2 AND hop-3." -> REFUTED iff for k in {2,3}:
          hyb_acc[k] ci_lo > shuffle_null[k] hi AND p[k] < 0.05.   [THE HEADLINE]
  FALSIFIER F-HYBRID-2 (material beat over the best pure-on-chip multi-step baseline): "the hybrid does NOT beat the
          best pure-on-chip hop2 (0.0298) by a material margin." -> REFUTED iff hyb_acc[2] > best_pure_hop2 + 0.01
          (strictly more than +1% over the best pure-on-chip multi-step result).
  HONEST: we ALWAYS report the full hybrid decay curve, the per-hop chance/shuffle NULLs, and the per-hop delta vs
          the pure-on-chip baselines, regardless of disposition. Hop-1 sanity must reproduce the single-step GREEN.

DISPOSITION (a_paper_negative_ok — a clean STILL-COLLAPSES is a VALID closed-negative; success closes Lane-A PUBLIC
             ONLY as a HONESTLY-SCOPED HYBRID artifact, never as pure-AKIDA):
  F-HYBRID-1 REFUTED (hop2&3 above shuffle-NULL) -> THE OFF-CHIP HEAD BREAKS THE WALL: hybrid multi-step composition
    works where all-on-chip failed; Lane A EMERGENCE axis (multi-step) LIFTS. Lane A PUBLIC may close AS A HYBRID
    (on-chip encoder ⊕ off-chip decode), explicitly scoped — NOT a pure-AKIDA result. STILL toy 250-anchor.
  F-HYBRID-1 NOT-refuted -> the off-chip head does NOT break the wall either -> HYBRID CLOSED-NEGATIVE
    (a_paper_negative_ok): even an off-chip recurrent decode over the on-chip codes cannot recover multi-step at
    this toy capacity -> the on-chip single-step code is too information-poor to seed an off-chip rollout. Lane A
    PUBLIC stays scoped to SINGLE-STEP. EMERGENCE axis stays NULL, recorded honestly.
  NO fabricated PUBLIC. NO sw fallback labelled on-chip. The off-chip head is labelled OFF-CHIP everywhere.
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
UNITS, NW, LCOMP = 256, 8, 0.1     # ON-CHIP FC: byte-match generation/rollout/state/depth rung
SHIFT = 37                          # byte-match onchip_xlm_state_rollout encoder/bind
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
K_ROLL = 3
SEED = 20260602
# ---- OFF-CHIP decode head (host CPU, numpy) hyperparams (small + honest) ----
D_H = 64           # off-chip hidden state width (the recurrence the 1-bit chip FC cannot carry)
EPOCHS = 60        # BPTT epochs over teacher-forced on-chip-code sequences (host CPU)
LR = 0.05
GRAD_CLIP = 5.0

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
# ----------------------------------------------------------------------------
count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
NC = len(concepts_sorted)
cidx = {c: i for i, c in enumerate(concepts_sorted)}
print("[hybrid] corpus_big count=%d concepts=%d langs=%d shift=%d units=%d D_H=%d K=%d" %
      (count, NC, len(langs), SHIFT, UNITS, D_H, K_ROLL)); sys.stdout.flush()
codes_enc = enc_whitened(H)
def code_of(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc[idx[0]] if len(idx) else None

# teacher-forced transition inputs for the ON-CHIP FC (byte-match state/depth rung)
train_codes, train_succ = [], []
for l in langs:
    for ci_ in range(NC - 1):
        a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
        if a is None or b is None: continue
        train_codes.append(bind(a, b)); train_succ.append(concepts_sorted[ci_ + 1])
train_codes = np.stack(train_codes)
n_train = train_codes.shape[0]
print("[hybrid] teacher-forced ON-CHIP train transitions=%d" % n_train); sys.stdout.flush()

# rollout starts (>=K real successors), identical selection to state/depth rungs
roll_starts = []
for ti in range(NC - K_ROLL):
    t = concepts_sorted[ti]
    for ql in langs:
        a = code_of(t, ql)
        if a is None: continue
        roll_starts.append((ti, ql, a))
print("[hybrid] rollout starts (>=%d real successors)=%d" % (K_ROLL, len(roll_starts))); sys.stdout.flush()

# ---- OFF-CHIP recurrent decode head (host CPU, numpy BPTT) ----
def softmax(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()
class OffChipHead:
    """Small host-CPU Elman RNN: h_{k+1}=tanh(Wxh@c_k + Whh@h_k); logits = Wo@h_{k+1}.
    Carries REAL float recurrence/state across hops — the off-chip contribution. Trained by BPTT over the
    teacher-forced ON-CHIP code sequences. NO sklearn, NO torch, NO GPU. Explicitly host-side."""
    def __init__(self, d_in, d_h, n_out, seed=0):
        rng = np.random.default_rng(seed)
        s1 = 1.0/np.sqrt(d_in); s2 = 1.0/np.sqrt(d_h)
        self.Wxh = rng.normal(0, s1, (d_h, d_in))
        self.Whh = rng.normal(0, s2, (d_h, d_h))
        self.Wo  = rng.normal(0, s2, (n_out, d_h))
        self.d_h = d_h
    def fit(self, seqs, epochs, lr, clip):
        """seqs = list of (codes[T,d_in], targets[T] int). Full BPTT per sequence, SGD."""
        for ep in range(epochs):
            order = np.random.default_rng(SEED + ep).permutation(len(seqs))
            tot_loss = 0.0; ntok = 0
            for si in order:
                C, Y = seqs[si]; T = C.shape[0]
                hs = [np.zeros(self.d_h)]; ps = []; pre = []
                for t in range(T):
                    a = self.Wxh @ C[t] + self.Whh @ hs[-1]
                    h = np.tanh(a); pre.append(a); hs.append(h)
                    ps.append(softmax(self.Wo @ h))
                gWxh = np.zeros_like(self.Wxh); gWhh = np.zeros_like(self.Whh); gWo = np.zeros_like(self.Wo)
                dh_next = np.zeros(self.d_h)
                for t in reversed(range(T)):
                    p = ps[t].copy(); p[Y[t]] -= 1.0           # dL/dlogits (CE)
                    tot_loss += -np.log(max(ps[t][Y[t]], 1e-12)); ntok += 1
                    gWo += np.outer(p, hs[t+1])
                    dh = self.Wo.T @ p + dh_next
                    da = (1.0 - hs[t+1]**2) * dh
                    gWxh += np.outer(da, C[t]); gWhh += np.outer(da, hs[t])
                    dh_next = self.Whh.T @ da
                for g in (gWxh, gWhh, gWo):
                    n = np.linalg.norm(g)
                    if n > clip: g *= clip / n
                self.Wxh -= lr * gWxh; self.Whh -= lr * gWhh; self.Wo -= lr * gWo
            if ep == epochs - 1 or ep % 20 == 0:
                print("[hybrid]   off-chip head BPTT epoch %d/%d  CE=%.4f" %
                      (ep + 1, epochs, tot_loss / max(1, ntok))); sys.stdout.flush()
    def step(self, c, h):
        h2 = np.tanh(self.Wxh @ c + self.Whh @ h)
        logits = self.Wo @ h2
        return logits, h2

def chip_code_for_concept(m, c, ql, med):
    """ON-CHIP single-step transition code for concept c in lang ql: encode bind(code(c), code(c)) through the
    LIVE chip FC and binarize. neutral_bind keeps the chip input construction identical to the proven rung's
    hop-1 input. The chip is the encoder; this is the ONLY thing the chip does in the hybrid."""
    a = code_of(c, ql)
    if a is None:
        a = code_of(concepts_sorted[0], ql)
    x = neutral_bind(a)
    g_soft = chip_forward(m, x)
    return binarize_rows(g_soft, med)[0].astype(np.float64)

def build_train_seqs(m, med):
    """teacher-forced sequences of ON-CHIP codes for the off-chip head: for each lang, the consecutive concept
    chain c_0..c_{NC-1}; input at step t = on-chip code of concept t, target = next concept index. The head
    learns to map (running state over on-chip codes) -> next concept. ON-CHIP encode is shared/cached per (c,ql)."""
    seqs = []
    code_cache = {}
    def cc(c, l):
        k = (c, l)
        if k not in code_cache: code_cache[k] = chip_code_for_concept(m, c, l, med)
        return code_cache[k]
    for l in langs:
        chain = [c for c in concepts_sorted if code_of(c, l) is not None]
        if len(chain) < 2: continue
        C = np.stack([cc(chain[i], l) for i in range(len(chain) - 1)])
        Y = np.array([cidx[chain[i + 1]] for i in range(len(chain) - 1)], dtype=np.int64)
        seqs.append((C, Y))
    return seqs, code_cache

def rollout_hybrid(m, head, med, code_cache):
    """drive the HYBRID autoregressively for K hops: chip encodes the current concept -> off-chip RNN carries
    state and predicts next concept -> re-encode that concept ON CHIP -> repeat. The chip is the encoder; the
    off-chip head carries the recurrence. ban last emit (open-vocab full codebook)."""
    preds = [[] for _ in range(K_ROLL)]
    def cc(c, l):
        k = (c, l)
        if k not in code_cache: code_cache[k] = chip_code_for_concept(m, c, l, med)
        return code_cache[k]
    for (ti, ql, _seed) in roll_starts:
        cur = concepts_sorted[ti]; banned = cur
        h = np.zeros(head.d_h)
        for k in range(K_ROLL):
            c_code = cc(cur, ql)                          # ON-CHIP code of current concept
            logits, h = head.step(c_code, h)             # OFF-CHIP recurrence carries state
            order = np.argsort(-logits)
            pred = None
            for j in order:
                cj = concepts_sorted[j]
                if cj != banned: pred = cj; break
            preds[k].append((ti, ql, pred))
            banned = pred if pred is not None else banned
            cur = pred if pred is not None else cur       # feed predicted concept back -> chip re-encodes it
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

PURE_HOP2 = [0.0277, 0.0282, 0.0298]   # PR#1686 / #1689 / #1690 hop-2
PURE_HOP3 = [0.0090, 0.0122, 0.0149]   # PR#1686 / #1689 / #1690 hop-3
BEST_PURE_HOP2 = max(PURE_HOP2)        # 0.0298 — the wall we must beat materially
RESULTS = {"substrate": "HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)",
           "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "off_chip_hidden": D_H, "off_chip_epochs": EPOCHS, "K_roll": K_ROLL,
           "architecture": "on-chip FC1 encoder (1-bit AkidaUnsupervised, byte-match state/depth rung) produces the "
                           "grounded single-step transition code; OFF-CHIP host-CPU Elman RNN decode head "
                           "(h=tanh(Wxh@c+Whh@h); logits=Wo@h) carries the multi-step recurrence and predicts the "
                           "next concept; the predicted concept is re-encoded ON CHIP each hop. NO chip-to-chip "
                           "feedback (that collapsed 3x). NO GPU/torch/sklearn in the head.",
           "encoder": "whitened (byte-match onchip_xlm_state_rollout.enc_whitened) ON CHIP",
           "corpus": "corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs",
           "pure_onchip_baselines": {"PR1686_stateless": [0.4287, 0.0277, 0.0090],
                                      "PR1689_state": [0.4234, 0.0282, 0.0122],
                                      "PR1690_depth2": [0.1612, 0.0298, 0.0149],
                                      "best_pure_hop2": BEST_PURE_HOP2},
           "task": "HYBRID autoregressive K-hop generation: on-chip encoder ⊕ off-chip recurrent decode head; "
                   "open-vocab full-codebook argmax decode; per-hop shuffle-NULL",
           "metric": "hyb_acc[k]=P(off-chip-head argmax decode at hop k == concept[ti+k]), k=1..K",
           "trials": []}
print("[hybrid] SUBSTRATE = HYBRID(on-chip⊕off-chip) — NOT pure AKIDA, NOT Lane G")
print("[hybrid] akida %s device %s ip %s N=%d trials units=%d D_H=%d K=%d" %
      (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS, D_H, K_ROLL)); sys.stdout.flush()

hyb_trials = [[] for _ in range(K_ROLL)]
learn_all = True
last_hyb_preds = None
for tr in range(NTRIALS):
    init = get_w(build_fc(1))
    m, learned = chip_make(init, train_codes, do_fit=True)   # ON-CHIP encoder, fit live on AKD1000
    train_soft = chip_forward(m, train_codes)
    med = np.median(train_soft, axis=0)
    # build teacher-forced ON-CHIP code sequences + train the OFF-CHIP head (host CPU)
    seqs, code_cache = build_train_seqs(m, med)
    head = OffChipHead(d_in=INC, d_h=D_H, n_out=NC, seed=SEED + tr)
    head.fit(seqs, epochs=EPOCHS, lr=LR, clip=GRAD_CLIP)
    hyb_preds = rollout_hybrid(m, head, med, code_cache)
    del m
    learn_all = learn_all and learned
    trial_row = {"trial": tr, "learned_hw_encoder": learned, "hyb_acc": [], "n_q": []}
    for k0 in range(K_ROLL):
        ha, n = acc_at(hyb_preds, k0)
        hyb_trials[k0].append(ha); trial_row["hyb_acc"].append(ha); trial_row["n_q"].append(n)
    RESULTS["trials"].append(trial_row)
    last_hyb_preds = hyb_preds
    print("[hybrid] trial %d: hyb(k1..K)=%s encoder_learned=%s" %
          (tr, ["%.4f" % x for x in trial_row["hyb_acc"]], learned)); sys.stdout.flush()
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_hybrid_decode.json"), "w"), indent=2)

chance = 1.0/(NC - 1)
per_hop = []
print("[hybrid] computing per-hop shuffle-NULL (B=%d) ..." % B_SHUFFLE); sys.stdout.flush()
for k0 in range(K_ROLL):
    hm, hsd, hsem, hlo, hhi = ci(hyb_trials[k0])
    null = shuffle_null_at(last_hyb_preds, k0, B=B_SHUFFLE, seed=SEED)
    nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
    p = float((null >= hm).sum() + 1) / (len(null) + 1)
    above_shuf = bool(learn_all and hlo > nhi and p < 0.05)
    per_hop.append({"hop": k0 + 1,
                    "hyb_acc": {"mean": hm, "sd": hsd, "ci_lo": hlo, "ci_hi": hhi},
                    "shuffle_null": {"mean": nmean, "sd": nsd, "hi": nhi, "p_value": p, "B": B_SHUFFLE},
                    "chance": chance, "above_shuffle_null": above_shuf,
                    "delta_vs_best_pure_hop2": round(hm - BEST_PURE_HOP2, 4) if k0 == 1 else None})
    print("[hybrid] hop %d: hyb=%.4f ci_lo=%.4f | shufNULL hi=%.4f p=%.4f | chance=%.4f | aboveShuf=%s"
          % (k0 + 1, hm, hlo, nhi, p, chance, above_shuf)); sys.stdout.flush()

# F-HYBRID-1: hop2 AND hop3 above shuffle-NULL (the hops that collapsed in ALL pure-on-chip rungs)
F_HYBRID_1 = bool(per_hop[1]["above_shuffle_null"] and per_hop[2]["above_shuffle_null"])
# F-HYBRID-2: hybrid hop2 beats best pure-on-chip hop2 (0.0298) by MORE than +1%
F_HYBRID_2 = bool(per_hop[1]["hyb_acc"]["mean"] > BEST_PURE_HOP2 + 0.01)
RESULTS["summary"] = {
    "learn_all_hw_encoder": learn_all, "chance": chance, "K_roll": K_ROLL,
    "decay_curve_hybrid": [round(per_hop[k]["hyb_acc"]["mean"], 4) for k in range(K_ROLL)],
    "best_pure_onchip_hop2": BEST_PURE_HOP2,
    "per_hop": per_hop,
    "F_HYBRID_1_breaks_1hop_wall": (
        "REFUTED: the off-chip recurrent head keeps hop-2 AND hop-3 ABOVE the shuffle-NULL (each ci_lo>NULL hi AND "
        "p<0.05) -> off-chip recurrence over the on-chip codes BREAKS the 1-hop wall that all-on-chip hit 3x"
        if F_HYBRID_1 else
        "NOT-REFUTED: hop-2 and/or hop-3 hybrid acc DROPS INTO the shuffle-NULL -> even an off-chip recurrent decode "
        "head over the on-chip codes does NOT recover multi-step at this toy capacity (CLOSED-NEGATIVE, a_paper_negative_ok)"),
    "F_HYBRID_2_material_beat": (
        "REFUTED: hybrid hop-2 (%.4f) beats the best pure-on-chip hop-2 (%.4f) by >1%% -> material multi-step gain "
        "from moving recurrence off-chip" % (per_hop[1]["hyb_acc"]["mean"], BEST_PURE_HOP2)
        if F_HYBRID_2 else
        "NOT-REFUTED: hybrid hop-2 (%.4f) does NOT beat the best pure-on-chip hop-2 (%.4f) by >1%% -> no material "
        "multi-step gain (a_paper_negative_ok)" % (per_hop[1]["hyb_acc"]["mean"], BEST_PURE_HOP2)),
    "F_HYBRID_1_pass": F_HYBRID_1, "F_HYBRID_2_pass": F_HYBRID_2,
    "hybrid_breaks_wall": bool(F_HYBRID_1),
}
if F_HYBRID_1:
    disp = ("HYBRID BREAKS THE 1-HOP WALL (on-chip encoder ⊕ off-chip decode): the off-chip recurrent head carries "
            "the multi-step state the 1-bit on-chip FC structurally cannot, and recovers hop-2/3 composition over "
            "the live on-chip codes. Lane A EMERGENCE axis (multi-step composition) LIFTS. Lane A PUBLIC may close "
            "AS A HYBRID artifact (honestly scoped: on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT "
            "a pure-AKIDA result, NOT Lane G. STILL toy 250-anchor (a_scale_honest_scope); scale-transfer UNVERIFIED. "
            "a_lane_akida_gpu_split: the on-chip part is Lane A, the head is host-side; never merged with Lane G.")
else:
    disp = ("HYBRID CLOSED-NEGATIVE (a_paper_negative_ok): even an OFF-CHIP recurrent decode head over the live "
            "on-chip codes does NOT break the 1-hop wall (hop-2/3 still in the shuffle-NULL) -> the on-chip "
            "single-step code is too information-poor to seed an off-chip multi-step rollout at this toy capacity; "
            "the limit is the 1-bit/256-unit ENCODE, not only the missing recurrence. Lane A PUBLIC stays scoped to "
            "SINGLE-STEP generation. EMERGENCE axis stays NULL, recorded honestly. Substrate = HYBRID(on-chip⊕off-"
            "chip), NOT pure-AKIDA, NOT Lane G. Toy 250-anchor (a_scale_honest_scope).")
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_hybrid_decode.json"), "w"), indent=2)
print("\n[hybrid] ========== DISPOSITION ==========")
print("[hybrid] SUBSTRATE             : HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)")
print("[hybrid] learn_all_hw_encoder  :", learn_all)
print("[hybrid] chance                : %.4f  K=%d  D_H=%d" % (chance, K_ROLL, D_H))
print("[hybrid] decay HYBRID (k1..K)  :", ["%.4f" % per_hop[k]["hyb_acc"]["mean"] for k in range(K_ROLL)])
print("[hybrid] PR#1686 stateless     : [0.4287, 0.0277, 0.0090]")
print("[hybrid] PR#1689 state-carry   : [0.4234, 0.0282, 0.0122]")
print("[hybrid] PR#1690 depth-2       : [0.1612, 0.0298, 0.0149]")
print("[hybrid] best pure-onchip hop2 : %.4f" % BEST_PURE_HOP2)
for k0 in range(K_ROLL):
    h = per_hop[k0]
    extra = "" if h["delta_vs_best_pure_hop2"] is None else " | delta_vs_best_pure_hop2=%+.4f" % h["delta_vs_best_pure_hop2"]
    print("[hybrid] hop %d  hyb=%.4f ci_lo=%.4f | shufNULL hi=%.4f p=%.4f | chance=%.4f | aboveShuf=%s%s"
          % (h["hop"], h["hyb_acc"]["mean"], h["hyb_acc"]["ci_lo"], h["shuffle_null"]["hi"],
             h["shuffle_null"]["p_value"], h["chance"], h["above_shuffle_null"], extra))
print("[hybrid] F-HYBRID-1 wall       :", RESULTS["summary"]["F_HYBRID_1_breaks_1hop_wall"])
print("[hybrid] F-HYBRID-2 material   :", RESULTS["summary"]["F_HYBRID_2_material_beat"])
print("[hybrid] DISPOSITION           :", RESULTS["DISPOSITION"])
print("[hybrid] wrote " + os.path.join(OUT, "result_onchip_xlm_hybrid_decode.json"))
