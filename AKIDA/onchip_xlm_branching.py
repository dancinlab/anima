#!/usr/bin/env python3
"""Lane A HYBRID BRANCHING-CORPUS HELD-OUT RUNG — on-chip AKD1000 ENCODER ⊕ off-chip host-CPU DECODE HEAD,
   evaluated on a CONCEPT-LEVEL HELD-OUT split over a *BRANCHING / NON-DETERMINISTIC* transition operator.
substrate = HYBRID (on-chip encoder ⊕ off-chip decode) — NOT pure on-chip, NOT Lane G/GPU.
a_lane_akida_gpu_split (the on-chip part is AKIDA Lane A; the decode head is explicitly host-side) ·
a_scale_honest_scope (toy; ≥3-rung codebook ladder reported) · g63 (the CHIP part has NO sw fallback — device==[] -> abort) ·
a_completeness_over_cheap (root-cause redesign of the corpus, NOT a cheap stop) ·
a_paper_negative_ok (a clean COLLAPSE on the branching corpus too = a VALID closed-negative naming the next bridge).

ROOT CAUSE THIS RUNG REPAIRS (named in PR#1694 / F-GEN-HOLDOUT, a_completeness_over_cheap):
  The held-out generalization rung (PR#1694) found HELD-OUT acc = EXACTLY 0.0000 at every hop, all 8 chip trials,
  while TRAIN(in-dist) reproduced ~0.28. RULING: the toy corpus is a DETERMINISTIC SINGLE CHAIN (concept i -> i+1),
  so "next concept" is a PURE PER-CONCEPT LOOKUP BY CONSTRUCTION. The off-chip head memorized "after TRAIN concept i,
  emit i+1"; TEST-block output rows (Wo) never received a positive CE gradient (never a target), so their logits sit
  at init and argmax NEVER selects a TEST concept -> structural 0.0000. NO corpus that is a single deterministic chain
  could ever force a transferable operator. The named next bridge: a BRANCHING / NON-DETERMINISTIC corpus.

THE BRANCHING CORPUS (root-cause redesign — a transition DISTRIBUTION, not a single next):
  We KEEP the on-chip encoder byte-identical (whitened FC1 over byte-histograms, SHIFT=37 bind), and KEEP the same
  50 FLORES concepts x 5 langs as the grounded codebook. We REPLACE the deterministic i->i+1 chain with a
  CONCEPT-IDENTITY-INDEPENDENT transition OPERATOR over the concept-index ring Z_NC:
       succ(i) = { (i + delta) mod NC : delta in DELTAS }      DELTAS = {1, 7, 19}  (branching factor B=3)
  This operator is a genuine RULE (add-offset-mod-ring), it is BRANCHING (B=3 plausible successors per concept), and
  it is concept-IDENTITY-INDEPENDENT (the same three offsets apply to EVERY concept) so it CAN transfer to concepts
  held out of training. Because (i+delta) mod NC WRAPS, a TEST concept's valid successors include TRAIN-block
  concepts — so the off-chip head's argmax over TRAIN-trained output rows CAN land on a valid successor. This is the
  structural fix that makes held-out generalization POSSIBLE at all (unlike the deterministic chain's structural 0).
  The head MUST learn the OFFSET OPERATOR (a transition rule conditioned on the current concept code), not a
  per-concept lookup, because each training target is a RANDOM valid successor drawn from the B-element successor set
  (so no single deterministic target exists to memorize).

THE HELD-OUT SPLIT (concept-level; the off-chip head's TRAINING TARGETS are TRAIN-block only):
  TRAIN concepts = idx [0:N_TRAIN); TEST concepts = idx [N_TRAIN:NC).
  OFF-CHIP HEAD TRAINING (BPTT, host CPU): training walks start at TRAIN concepts and step via the branching operator,
  but a step is ONLY kept as a (input, target) training pair when the chosen successor is ALSO a TRAIN concept (so
  every training TARGET index is in the TRAIN block — the head NEVER sees a TEST concept as a target). The on-chip
  encoder is fit on the full concept set (unsupervised grounding surface, byte-match prior rungs).
  EVAL — two decay curves on the BRANCHING-AWARE metric, side by side:
    (A) TRAIN-set rollout : starts whose concept is in the TRAIN block (in-distribution).
    (B) HELD-OUT rollout  : starts whose concept is in the TEST block (operator must transfer to unseen concepts).
  Open-vocab argmax decode over the FULL concept codebook (ban last emit) in BOTH curves.

BRANCHING-AWARE METRIC (pre-registered — multiple successors are correct, so do NOT exact-match one arbitrary next):
  setacc[k] = P( off-chip-head argmax decode at hop k  IS A MEMBER OF the valid successor set of the concept the
                 rollout is currently AT at hop k-1 ),  k=1..K.   The rollout is autoregressive: at each hop the head
  predicts from the running state + current on-chip code; correctness = the prediction lands in succ(current). This
  is set-membership against the B-element valid-successor set (the branching-aware metric), NOT exact-match against
  one arbitrary successor. We ALSO report top1-exact (predicted == one randomly-fixed canonical successor) for
  reference, and the chance-of-set-membership = B/(NC-1) (open-vocab uniform hitting any of B valid successors,
  minus the banned last emit).

PRE-REGISTERED FALSIFIERS (g63 honest, declared in-file BEFORE the run):
  NULL-A (SHUFFLE) per hop k: held-out set-membership with the (seed concept -> its valid successor SET) mapping
          permuted across concepts (B=200 permutations); per-hop hi + p. (Scores a prediction against a RANDOM
          concept's successor set -> the chance a random valid-set is hit.)
  CHANCE: B/(NC-1) open-vocab uniform set-membership.
  IN-DIST REFERENCE: the TRAIN-set held-in set-membership decay curve A.
  FALSIFIER F-BRANCH-1 (held-out above shuffle-NULL at hop-2 AND hop-3 on the branching metric):
          "the HELD-OUT branching set-membership accuracy does NOT stay above the shuffle-NULL at hop-2 AND hop-3."
          -> REFUTED iff for k in {2,3}: heldout_setacc[k] ci_lo > shuffle_null[k] hi AND p[k] < 0.05.
          [does a branching corpus force a TRANSFERABLE operator, breaking the per-concept lookup ceiling?]
  FALSIFIER F-BRANCH-2 (held-out within a stated factor of in-dist train):
          "the HELD-OUT hop-2 set-membership accuracy is NOT within FACTOR (=2.0x) of the in-distribution (TRAIN-set)
          hop-2 set-membership accuracy." -> REFUTED iff heldout_setacc[2] >= train_setacc[2] / GEN_FACTOR.
  CODEBOOK LADDER (a_scale_honest_scope, >=3 rungs): NC in {30, 40, 50} (subset of the same 50-concept pool); we
          report the held-out hop-2 set-membership at each rung so the conclusion has a ladder curve, not a single point.
  HONEST: we ALWAYS report BOTH decay curves (train vs held-out), per-hop chance/shuffle NULLs, the held-out/in-dist
          ratio, AND the ladder, regardless of disposition.

DISPOSITION (a_paper_negative_ok):
  F-BRANCH-1 REFUTED (held-out hop2&3 above shuffle-NULL) AND F-BRANCH-2 REFUTED (held-out within factor of in-dist)
    -> GENERALIZES: a branching corpus FORCES a transferable transition OPERATOR; multi-step composition is REAL (the
    off-chip head learned an offset-operator that applies to concepts it was never trained to emit). Lane A HYBRID
    PUBLIC re-upgrades (hybrid-scoped, branching-validated; still toy). next = 3B.
  F-BRANCH-1 NOT-refuted -> COLLAPSES (closed-negative): even a branching corpus cannot lift it at this toy capacity
    -> name the next bridge (e.g. larger off-chip head / different recurrence / GPU off-chip). NO fabricated green.
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
UNITS, NW, LCOMP = 256, 8, 0.1     # ON-CHIP FC: byte-match generation/rollout/state/depth/hybrid/holdout rung
SHIFT = 37                          # byte-match onchip_xlm_state_rollout encoder/bind
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
# K_ROLL = rollout depth. default 3 (proven hop-2/3). LANE_A_K_ROLL=5 pushes the DEEPER-composition axis (hop-4/5);
# the F-BRANCH-DEEP falsifier (below) tests whether held-out composition holds at hop-4 AND hop-5 or decays.
K_ROLL = int(os.environ.get("LANE_A_K_ROLL", "3"))
SEED = 20260602
# ---- OFF-CHIP decode head (host CPU, numpy) hyperparams — byte-match PR#1692/#1694 hybrid head ----
D_H = 64           # off-chip hidden state width
EPOCHS = 60        # BPTT epochs over teacher-forced on-chip-code sequences (host CPU)
LR = 0.05
GRAD_CLIP = 5.0
# ---- BRANCHING operator + held-out split hyperparams (pre-registered) ----
# env overrides (Lane A-multi LARGER rung): LANE_A_DELTAS="1,7,13,19,29" -> wider branching B=5;
#   LANE_A_LADDER_NC="40,45,50" -> larger codebook ladder. Defaults reproduce the proven B=3 / NC{30,40,50} rung.
DELTAS = [int(x) for x in os.environ.get("LANE_A_DELTAS", "1,7,19").split(",")]  # offsets on the concept-index ring (branching factor B)
B_FACTOR = len(DELTAS)
WALK_LEN = max(6, K_ROLL + 1)  # length of each random branching walk; >= K_ROLL+1 so deep rollouts have targets
WALKS_PER_LANG = 24          # number of random branching walks per language used for off-chip BPTT
GEN_FACTOR = 2.0             # F-BRANCH-2: held-out hop-2 must be >= in-dist hop-2 / GEN_FACTOR
N_TEST_FRAC = 0.30           # held-out TEST block = last 30% of the concept index axis
LADDER_NC = [int(x) for x in os.environ.get("LANE_A_LADDER_NC", "30,40,50").split(",")]  # >=3-rung codebook-size ladder (a_scale_honest_scope)

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

class OffChipHead:
    """Small host-CPU Elman RNN: h_{k+1}=tanh(Wxh@c_k + Whh@h_k); logits = Wo@h_{k+1}. byte-match PR#1692/#1694 head.
    Trained by BPTT over teacher-forced ON-CHIP code walks on the BRANCHING operator, TRUNCATED to TRAIN concepts as
    targets. NO sklearn, NO torch, NO GPU. Explicitly host-side."""
    def __init__(self, d_in, d_h, n_out, seed=0):
        rng = np.random.default_rng(seed)
        s1 = 1.0/np.sqrt(d_in); s2 = 1.0/np.sqrt(d_h)
        self.Wxh = rng.normal(0, s1, (d_h, d_in))
        self.Whh = rng.normal(0, s2, (d_h, d_h))
        self.Wo  = rng.normal(0, s2, (n_out, d_h))
        self.d_h = d_h
    def fit(self, seqs, epochs, lr, clip):
        for ep in range(epochs):
            order = np.random.default_rng(SEED + ep).permutation(len(seqs))
            tot_loss = 0.0; ntok = 0
            for si in order:
                C, Y = seqs[si]; T = C.shape[0]
                hs = [np.zeros(self.d_h)]; ps = []
                for t in range(T):
                    a = self.Wxh @ C[t] + self.Whh @ hs[-1]
                    h = np.tanh(a); hs.append(h)
                    ps.append(softmax(self.Wo @ h))
                gWxh = np.zeros_like(self.Wxh); gWhh = np.zeros_like(self.Whh); gWo = np.zeros_like(self.Wo)
                dh_next = np.zeros(self.d_h)
                for t in reversed(range(T)):
                    p = ps[t].copy(); p[Y[t]] -= 1.0
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
                print("[branch]   off-chip head BPTT epoch %d/%d  CE=%.4f (branching walks, TRAIN targets only)" %
                      (ep + 1, epochs, tot_loss / max(1, ntok))); sys.stdout.flush()
    def step(self, c, h):
        h2 = np.tanh(self.Wxh @ c + self.Whh @ h)
        logits = self.Wo @ h2
        return logits, h2

# ----------------------------------------------------------------------------
# default = corpus_big (real 50-concept FLORES). LANE_A_CORPUS overrides for the larger-NC frontier (e.g.
# "corpus_synth" — distinguishable synthetic anchors past the 50-concept real ceiling; labelled synthetic below).
CORPUS_DIR = os.environ.get("LANE_A_CORPUS", "corpus_big")
count, recs = read_limen(os.path.join(ROOT, CORPUS_DIR, "parallel.limen"))
concept = np.array([h["concept"] for (h, _) in recs])
lang = np.array([h["lang"] for (h, _) in recs])
H = np.stack([byte_hist(p) for (_, p) in recs])
concepts_sorted_full = sorted(np.unique(concept).tolist())
langs = sorted(np.unique(lang).tolist())
NC_FULL = len(concepts_sorted_full)
codes_enc_full = enc_whitened(H)   # on-chip encoder input codes (whitened byte-histograms) computed once

def code_of_full(c, l):
    idx = np.where((concept == c) & (lang == l))[0]
    return codes_enc_full[idx[0]] if len(idx) else None

print("[branch] SUBSTRATE = HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure AKIDA, NOT Lane G")
print("[branch] akida %s device %s ip %s  corpus concepts=%d langs=%d  DELTAS=%s B=%d  ladder=%s" %
      (akida.__version__, DEV.version, DEV.ip_version, NC_FULL, len(langs), DELTAS, B_FACTOR, LADDER_NC)); sys.stdout.flush()

def succ_set(i, NC):
    return sorted(set((i + d) % NC for d in DELTAS))

def run_one_nc(NC, do_full_curves):
    """Run the full branching held-out experiment for codebook size NC (first NC sorted concepts).
    Returns (per_hop list, summary dict). do_full_curves=True only for the headline NC (shuffle-NULL + falsifiers)."""
    concepts_sorted = concepts_sorted_full[:NC]
    cidx = {c: i for i, c in enumerate(concepts_sorted)}
    N_TRAIN = NC - max(K_ROLL + 1, int(round(NC * N_TEST_FRAC)))
    TRAIN_IDX = set(range(0, N_TRAIN)); TEST_IDX = set(range(N_TRAIN, NC))
    codes_enc = codes_enc_full  # same encoder input codes; we just restrict the concept set
    def code_of(c, l): return code_of_full(c, l)

    # ON-CHIP encoder fit transitions: ALL branching operator edges over the full NC concept set (unsupervised
    # grounding; the chip encode is the shared surface — byte-match prior rungs' bind(a,b)).
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
    print("[branch] NC=%d  N_TRAIN=%d (idx 0..%d)  N_TEST=%d (idx %d..%d)  on-chip enc transitions=%d" %
          (NC, N_TRAIN, N_TRAIN - 1, NC - N_TRAIN, N_TRAIN, NC - 1, train_codes.shape[0])); sys.stdout.flush()

    def chip_code_for_concept(m, c, ql, med):
        a = code_of(c, ql)
        if a is None: a = code_of(concepts_sorted[0], ql)
        g_soft = chip_forward(m, neutral_bind(a))
        return binarize_rows(g_soft, med)[0].astype(np.float64)

    def build_train_seqs(m, med, walk_rng):
        """Teacher-forced ON-CHIP code walks on the BRANCHING operator. Each walk: start at a random TRAIN concept,
        step via a RANDOM valid successor; KEEP a (code(cur), target=next) pair ONLY when BOTH cur and next are TRAIN
        concepts -> every training TARGET is a TRAIN concept (the head NEVER sees a TEST concept as a target). Because
        the successor is RANDOM over the B-set, no single deterministic target exists to memorize."""
        seqs = []; code_cache = {}
        def cc(c, l):
            k = (c, l)
            if k not in code_cache: code_cache[k] = chip_code_for_concept(m, c, l, med)
            return code_cache[k]
        train_concepts = [i for i in range(N_TRAIN) if code_of(concepts_sorted[i], langs[0]) is not None]
        for l in langs:
            for _w in range(WALKS_PER_LANG):
                cur = int(walk_rng.choice(train_concepts))
                Cseq = []; Yseq = []
                for _s in range(WALK_LEN):
                    nxts = [j for j in succ_set(cur, NC) if j in TRAIN_IDX]
                    if not nxts: break
                    nxt = int(walk_rng.choice(nxts))
                    cc_cur = cc(concepts_sorted[cur], l)
                    Cseq.append(cc_cur); Yseq.append(nxt)
                    cur = nxt
                if len(Cseq) >= 2:
                    Y = np.array(Yseq, dtype=np.int64)
                    assert all(int(y) in TRAIN_IDX for y in Y), "held-out leak: a training target is a TEST concept"
                    seqs.append((np.stack(Cseq), Y))
        return seqs, code_cache

    def rollout(m, head, med, code_cache, start_idxs):
        """Autoregressive branching rollout. preds[k] = list of (start_concept_idx, current_idx_before_hop, ql, pred_idx).
        current_idx_before_hop is the concept the rollout is AT before hop k (so set-membership scores pred against
        succ(current))."""
        preds = [[] for _ in range(K_ROLL)]
        def cc(c, l):
            k = (c, l)
            if k not in code_cache: code_cache[k] = chip_code_for_concept(m, c, l, med)
            return code_cache[k]
        for (ti, ql) in start_idxs:
            cur = ti; banned = concepts_sorted[cur]
            h = np.zeros(head.d_h)
            for k in range(K_ROLL):
                c_code = cc(concepts_sorted[cur], ql)
                logits, h = head.step(c_code, h)
                order = np.argsort(-logits)
                pred = None
                for j in order:
                    if j < NC and concepts_sorted[j] != banned: pred = j; break
                preds[k].append((ti, cur, ql, pred))
                if pred is None: break
                banned = concepts_sorted[pred]; cur = pred
        return preds

    def setacc_at(preds, k0):
        """branching-aware set-membership: pred in succ(current concept at this hop)."""
        hit, tot = 0, 0
        for (ti, cur, ql, pred) in preds[k0]:
            if pred is None: continue
            tot += 1; hit += int(pred in succ_set(cur, NC))
        return hit / max(1, tot), tot
    def shuffle_null_set_at(preds, k0, B=B_SHUFFLE, seed=SEED):
        """NULL: score pred against a RANDOM concept's successor set (permute concept->succ-set mapping)."""
        rng = np.random.default_rng(seed + 1009 * (k0 + 1))
        null = []
        for _ in range(B):
            perm = rng.permutation(NC)
            hit, tot = 0, 0
            for (ti, cur, ql, pred) in preds[k0]:
                if pred is None: continue
                tot += 1; hit += int(pred in succ_set(int(perm[cur]), NC))
            null.append(hit / max(1, tot))
        return np.array(null)

    train_starts = [(i, l) for i in range(N_TRAIN) for l in langs if code_of(concepts_sorted[i], l) is not None]
    held_starts = [(i, l) for i in range(N_TRAIN, NC) for l in langs if code_of(concepts_sorted[i], l) is not None]

    train_acc_trials = [[] for _ in range(K_ROLL)]; held_acc_trials = [[] for _ in range(K_ROLL)]
    learn_all = True; last_held_preds = None; ce_last = None
    for tr in range(NTRIALS):
        init = get_w(build_fc(1))
        m, learned = chip_make(init, train_codes, do_fit=True)   # ON-CHIP encoder, fit live on AKD1000
        train_soft = chip_forward(m, train_codes); med = np.median(train_soft, axis=0)
        walk_rng = np.random.default_rng(SEED + 7919 * tr)
        seqs, code_cache = build_train_seqs(m, med, walk_rng)
        head = OffChipHead(d_in=INC, d_h=D_H, n_out=NC, seed=SEED + tr)
        head.fit(seqs, epochs=EPOCHS, lr=LR, clip=GRAD_CLIP)
        tr_preds = rollout(m, head, med, code_cache, train_starts)
        he_preds = rollout(m, head, med, code_cache, held_starts)
        del m
        learn_all = learn_all and learned
        for k0 in range(K_ROLL):
            ta, _ = setacc_at(tr_preds, k0); ha, _ = setacc_at(he_preds, k0)
            train_acc_trials[k0].append(ta); held_acc_trials[k0].append(ha)
        last_held_preds = he_preds
        print("[branch] NC=%d trial %d: TRAIN-set(k1..K)=%s HELD-OUT(k1..K)=%s enc_learned=%s" %
              (NC, tr, ["%.4f" % train_acc_trials[k][-1] for k in range(K_ROLL)],
               ["%.4f" % held_acc_trials[k][-1] for k in range(K_ROLL)], learned)); sys.stdout.flush()

    chance = B_FACTOR / (NC - 1)
    per_hop = []
    for k0 in range(K_ROLL):
        tm, tsd, tsem, tlo, thi = ci(train_acc_trials[k0])
        hm, hsd, hsem, hlo, hhi = ci(held_acc_trials[k0])
        if do_full_curves:
            null = shuffle_null_set_at(last_held_preds, k0, B=B_SHUFFLE, seed=SEED)
            nmean, nsd = float(null.mean()), float(null.std()); nhi = nmean + 1.96*nsd
            p = float((null >= hm).sum() + 1) / (len(null) + 1)
            above_shuf = bool(learn_all and hlo > nhi and p < 0.05)
        else:
            nmean = nsd = nhi = float("nan"); p = float("nan"); above_shuf = None
        ratio = (hm / tm) if tm > 1e-9 else 0.0
        per_hop.append({"hop": k0 + 1,
                        "train_setacc": {"mean": tm, "sd": tsd, "ci_lo": tlo, "ci_hi": thi},
                        "heldout_setacc": {"mean": hm, "sd": hsd, "ci_lo": hlo, "ci_hi": hhi},
                        "heldout_over_train_ratio": round(ratio, 4),
                        "shuffle_null": {"mean": nmean, "sd": nsd, "hi": nhi, "p_value": p, "B": B_SHUFFLE},
                        "chance": chance, "heldout_above_shuffle_null": above_shuf})
        if do_full_curves:
            print("[branch] NC=%d hop %d: TRAIN=%.4f HELD=%.4f (ratio=%.3f) | held ci_lo=%.4f shufNULL hi=%.4f p=%.4f | chance=%.4f | heldAboveShuf=%s"
                  % (NC, k0 + 1, tm, hm, ratio, hlo, nhi, p, chance, above_shuf)); sys.stdout.flush()
    summary = {"NC": NC, "N_TRAIN": N_TRAIN, "N_TEST": NC - N_TRAIN, "chance": chance, "learn_all": learn_all,
               "decay_TRAIN": [round(per_hop[k]["train_setacc"]["mean"], 4) for k in range(K_ROLL)],
               "decay_HELD_OUT": [round(per_hop[k]["heldout_setacc"]["mean"], 4) for k in range(K_ROLL)],
               "heldout_over_train_ratio_per_hop": [per_hop[k]["heldout_over_train_ratio"] for k in range(K_ROLL)]}
    return per_hop, summary

RESULTS = {"substrate": "HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)",
           "rung": "BRANCHING-CORPUS HELD-OUT GENERALIZATION (non-deterministic transition operator; set-membership metric)",
           "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS, "units": UNITS,
           "off_chip_hidden": D_H, "off_chip_epochs": EPOCHS, "K_roll": K_ROLL,
           "branching_operator": {"deltas": DELTAS, "B_factor": B_FACTOR, "ring": "Z_NC", "rule": "succ(i)={(i+d) mod NC : d in DELTAS}"},
           "metric": "setacc[k]=P(off-chip-head argmax decode at hop k IS A MEMBER OF succ(current concept)) — branching-aware set-membership",
           "gen_factor": GEN_FACTOR, "n_test_frac": N_TEST_FRAC, "ladder_NC": LADDER_NC,
           "corpus": (("corpus_big 250 anchors / 50 sequential FLORES concepts x 5 langs; BRANCHING operator REPLACES the deterministic chain"
                       if CORPUS_DIR == "corpus_big" else
                       "%s SYNTHETIC distinguishable byte-pattern anchors (NC past the 50-concept real-corpus ceiling; "
                       "NOT a semantic claim, a_scale_honest_scope); BRANCHING operator over the index ring" % CORPUS_DIR)),
           "corpus_dir": CORPUS_DIR,
           "prior_holdout_PR1694_heldout_decay": [0.0000, 0.0000, 0.0000],
           "architecture": "on-chip FC1 encoder (1-bit AkidaUnsupervised, byte-match prior rungs) grounds the transition code; "
                           "OFF-CHIP host-CPU Elman RNN decode head trained by BPTT on random BRANCHING walks with TRAIN-only "
                           "targets; rollout decoded over the FULL codebook. NO chip-to-chip feedback. NO GPU/torch/sklearn.",
           "ladder": [], "headline": {}}
print("[branch] ===== CODEBOOK LADDER (a_scale_honest_scope, %d rungs) =====" % len(LADDER_NC)); sys.stdout.flush()
headline_NC = LADDER_NC[-1]
for NC in LADDER_NC:
    per_hop, summ = run_one_nc(NC, do_full_curves=(NC == headline_NC))
    RESULTS["ladder"].append(summ)
    if NC == headline_NC:
        RESULTS["headline_per_hop"] = per_hop
    json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_branching.json"), "w"), indent=2)

ph = RESULTS["headline_per_hop"]
F_BRANCH_1 = bool(ph[1]["heldout_above_shuffle_null"] and ph[2]["heldout_above_shuffle_null"])
train_hop2 = ph[1]["train_setacc"]["mean"]; held_hop2 = ph[1]["heldout_setacc"]["mean"]
F_BRANCH_2 = bool(held_hop2 >= train_hop2 / GEN_FACTOR)
GENERALIZES = bool(F_BRANCH_1 and F_BRANCH_2)
# ---- F-BRANCH-DEEP (pre-registered, A-multi rung+1 DEEPER axis): does held-out composition HOLD at hop-4 AND hop-5? ----
# REFUTED iff for every k in {4,5} (1-indexed) present in the rollout: heldout ci_lo>shuffle-NULL hi AND p<0.05.
# NOT-REFUTED -> composition DECAYS at deeper hops; the per-hop curve names the DEPTH CEILING (a_paper_negative_ok).
DEEP_HOPS = [h for h in (4, 5) if h <= K_ROLL]
deep_above = {}
for h in DEEP_HOPS:
    deep_above[h] = bool(ph[h - 1]["heldout_above_shuffle_null"])
F_BRANCH_DEEP = bool(DEEP_HOPS) and all(deep_above[h] for h in DEEP_HOPS)
# depth ceiling = deepest hop that stays above shuffle-NULL (held-out), else the last sub-NULL hop
depth_above_null = [h for h in range(1, K_ROLL + 1) if ph[h - 1]["heldout_above_shuffle_null"]]
DEPTH_CEILING = max(depth_above_null) if depth_above_null else 0
RESULTS["headline"] = {
    "NC": headline_NC, "chance": ph[0]["chance"],
    "decay_curve_TRAIN_in_dist": [round(ph[k]["train_setacc"]["mean"], 4) for k in range(K_ROLL)],
    "decay_curve_HELD_OUT": [round(ph[k]["heldout_setacc"]["mean"], 4) for k in range(K_ROLL)],
    "heldout_over_train_ratio_per_hop": [ph[k]["heldout_over_train_ratio"] for k in range(K_ROLL)],
    "F_BRANCH_1_heldout_above_null": (
        "REFUTED: held-out hop-2 AND hop-3 STAY ABOVE the shuffle-NULL on the branching set-membership metric "
        "(each ci_lo>NULL hi AND p<0.05) -> a branching corpus FORCES a TRANSFERABLE transition OPERATOR; the off-chip "
        "head composes on concepts held out of training -> GENUINE multi-step composition, NOT a per-concept lookup"
        if F_BRANCH_1 else
        "NOT-REFUTED: held-out hop-2 and/or hop-3 DROPS INTO the shuffle-NULL -> even a branching corpus does NOT force "
        "a transferable operator at this toy capacity (CLOSED-NEGATIVE, a_paper_negative_ok)"),
    "F_BRANCH_2_within_factor": (
        "REFUTED: held-out hop-2 (%.4f) is within %.1fx of in-dist hop-2 (%.4f) [>= %.4f] -> held-out tracks in-dist"
        % (held_hop2, GEN_FACTOR, train_hop2, train_hop2 / GEN_FACTOR) if F_BRANCH_2 else
        "NOT-REFUTED: held-out hop-2 (%.4f) is NOT within %.1fx of in-dist hop-2 (%.4f) [< %.4f]"
        % (held_hop2, GEN_FACTOR, train_hop2, train_hop2 / GEN_FACTOR)),
    "F_BRANCH_1_pass": F_BRANCH_1, "F_BRANCH_2_pass": F_BRANCH_2, "GENERALIZES": GENERALIZES,
    "K_roll": K_ROLL, "deep_hops_tested": DEEP_HOPS, "deep_hop_above_null": deep_above,
    "depth_ceiling_hop": DEPTH_CEILING,
    "F_BRANCH_DEEP_holds_at_hop4_5": (
        ("REFUTED: held-out composition STAYS ABOVE shuffle-NULL at hop %s (each ci_lo>NULL hi AND p<0.05) -> the "
         "transferable operator HOLDS at deeper hops; no depth ceiling within hop-%d"
         % (DEEP_HOPS, K_ROLL)) if F_BRANCH_DEEP else
        ("NOT-REFUTED: held-out composition DECAYS INTO the shuffle-NULL at deeper hops -> DEPTH CEILING at hop-%d "
         "(deepest hop still above-NULL); composition does NOT hold to hop-%s (CLOSED-NEGATIVE, a_paper_negative_ok)"
         % (DEPTH_CEILING, DEEP_HOPS if DEEP_HOPS else "[none tested: K_ROLL<4]"))),
    "F_BRANCH_DEEP_pass": F_BRANCH_DEEP,
}
if GENERALIZES:
    disp = ("GENERALIZES — a BRANCHING corpus FORCES a transferable transition OPERATOR. The off-chip recurrent head, "
            "trained on random branching walks with TRAIN-concept targets ONLY, decodes hop-2/3 successors for TEST "
            "concepts it was NEVER trained to emit, landing in the valid (B=%d) successor set ABOVE the shuffle-NULL AND "
            "within %.1fx of in-dist. Multi-step composition is REAL (the head learned the offset operator, not a "
            "per-concept lookup). The PR#1694 exact-0.0000 was an ARTEFACT of the deterministic single-chain corpus, "
            "REPAIRED at the root cause. Lane A HYBRID PUBLIC RE-UPGRADES (hybrid-scoped, branching-validated; on-chip "
            "AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure-AKIDA, NOT Lane G. STILL toy (a_scale_honest_scope, "
            "%d-rung ladder reported); next rung = 3B." % (B_FACTOR, GEN_FACTOR, len(LADDER_NC)))
else:
    disp = ("STILL-LOOKUP / COLLAPSES (a_paper_negative_ok, closed-negative) — even a BRANCHING / non-deterministic "
            "corpus does NOT lift held-out composition at this toy capacity: held-out branching set-membership %s the "
            "discriminators (F-BRANCH-1 %s, F-BRANCH-2 %s). The off-chip Elman head over 1-bit on-chip codes cannot "
            "learn a transferable offset operator at D_H=64 / 256-unit encoder / toy NC. The Lane A HYBRID PUBLIC stays "
            "DOWNGRADED (no multi-step composition claim). NEXT BRIDGE: a larger off-chip head (wider D_H / multi-layer / "
            "attention) and/or richer on-chip codes (>256 units), and a larger codebook before any composition claim. "
            "Substrate = HYBRID(on-chip⊕off-chip), NOT pure-AKIDA, NOT Lane G." %
            ("FAILS" if not F_BRANCH_1 else "is below-factor on",
             "REFUTED" if F_BRANCH_1 else "NOT-refuted", "REFUTED" if F_BRANCH_2 else "NOT-refuted"))
RESULTS["DISPOSITION"] = disp
json.dump(RESULTS, open(os.path.join(OUT, "result_onchip_xlm_branching.json"), "w"), indent=2)
print("\n[branch] ========== DISPOSITION ==========")
print("[branch] SUBSTRATE               : HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)")
print("[branch] branching operator      : succ(i)={(i+d) mod NC : d in %s}  B=%d" % (DELTAS, B_FACTOR))
print("[branch] LADDER (held-out hop-2 set-membership across NC rungs):")
for s in RESULTS["ladder"]:
    print("[branch]   NC=%2d  chance=%.4f  decay_TRAIN=%s  decay_HELD-OUT=%s  ratio=%s"
          % (s["NC"], s["chance"], s["decay_TRAIN"], s["decay_HELD_OUT"], s["heldout_over_train_ratio_per_hop"]))
print("[branch] HEADLINE NC=%d chance=%.4f" % (headline_NC, ph[0]["chance"]))
print("[branch] decay TRAIN  (in-dist)  :", ["%.4f" % ph[k]["train_setacc"]["mean"] for k in range(K_ROLL)])
print("[branch] decay HELD-OUT          :", ["%.4f" % ph[k]["heldout_setacc"]["mean"] for k in range(K_ROLL)])
print("[branch] PR#1694 holdout (det)   : [0.0000, 0.0000, 0.0000]  (the deterministic-chain collapse this rung repairs)")
for k0 in range(K_ROLL):
    h = ph[k0]
    print("[branch] hop %d  TRAIN=%.4f HELD=%.4f ratio=%.3f | held ci_lo=%.4f shufNULL hi=%.4f p=%.4f | chance=%.4f | heldAboveShuf=%s"
          % (h["hop"], h["train_setacc"]["mean"], h["heldout_setacc"]["mean"], h["heldout_over_train_ratio"],
             h["heldout_setacc"]["ci_lo"], h["shuffle_null"]["hi"], h["shuffle_null"]["p_value"], h["chance"],
             h["heldout_above_shuffle_null"]))
print("[branch] F-BRANCH-1 (held>NULL)   :", RESULTS["headline"]["F_BRANCH_1_heldout_above_null"])
print("[branch] F-BRANCH-2 (within %.1fx) :" % GEN_FACTOR, RESULTS["headline"]["F_BRANCH_2_within_factor"])
print("[branch] F-BRANCH-DEEP (hop4/5)   :", RESULTS["headline"]["F_BRANCH_DEEP_holds_at_hop4_5"])
print("[branch] depth ceiling (hop)      :", DEPTH_CEILING, " (deepest held-out hop above shuffle-NULL; K_roll=%d)" % K_ROLL)
print("[branch] GENERALIZES              :", GENERALIZES)
print("[branch] DISPOSITION              :", RESULTS["DISPOSITION"])
print("[branch] wrote " + os.path.join(OUT, "result_onchip_xlm_branching.json"))
