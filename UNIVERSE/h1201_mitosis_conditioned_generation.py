"""
H_1201 — MITOSIS-CONDITIONED-GENERATION (MITOSIS-ENGINE · Lane-2), the rung that decides
whether the mitosis substrate stays in the LANGUAGE-GENERATION loop at all, AFTER H_1200
falsified pure-mitosis-as-LM.

WHAT H_1200 ESTABLISHED (the predecessor, 🔴 CLOSED-NEG)
------------------------------------------------------
A GRADIENT-FREE prototype-count LM — growing prototype cells (the H_1199 VAdaptField
mechanism) and reading next-byte counts off the nearest cell — makes next-byte CE WORSE
(-0.76 b/byte, count-fragmentation across ~170 cells). So mitosis-as-a-standalone-LM is
dead. H_1200's redirect: generation is the CLM lane (a real gradient-trained next-byte
head); mitosis is a structural/adaptation lane.

THE OPEN QUESTION THIS RUNG TESTS
---------------------------------
H_1200 falsified mitosis GENERATING by itself. It did NOT test whether the mitosis
CELL-STATE carries information a REAL gradient-trained generative head can USE. So:
  Does CONDITIONING a proper next-byte head on the mitosis substrate BEAT the SAME head
  without it?
If YES, mitosis stays in the generation loop as a conditioning signal (the CLM-lane
generator can read the mitosis adaptation state). If NO, mitosis is PURE SUBSTRATE and
"conversational level" is pure CLM-lane scale-up — a clean architecture-settling result.

MECHANISM (p8: mitosis stays GRADIENT-FREE; only the readout head trains by descent)
------------------------------------------------------------------------------------
Two SMALL gradient-trained next-byte heads, IDENTICAL architecture + params + data + seed,
differing ONLY in the INPUT:
  * BASELINE head  : input = the DIM=8 byte-context feature window (H_1163 byte_feature,
                     VERBATIM — the SAME coarse context H_1199/H_1200 used).
  * CONDITIONED head: input = the SAME DIM=8 features CONCATENATED with the live mitosis
                     cell-state at that position — a compact summary of the H_1199
                     VAdaptField state produced by running the FROZEN mitosis growth over
                     the SAME stream. The summary (all gradient-free, read-only):
                       - nearest-cell prototype vector (DIM=8): WHICH regime cell owns this
                         position (its learned centroid),
                       - recon-err to that cell (1): how well the cell tiles this position,
                       - local cell-density (1): #cells within radius R of this feature
                         (how finely mitosis has carved this neighbourhood),
                       - log1p(n_cells_so_far) (1): how grown the field is at this tick.
                     => +(DIM+3)=11 conditioning dims. The mitosis growth is the H_1199/
                     H_1200 VAdaptField mechanism VERBATIM; we only EXPOSE its state as a
                     feature, we do NOT train it (p8).
Both heads = the SAME MLP (in -> tanh(H) -> softmax(256)), SAME init seed, SAME Adam, SAME
data, SAME epochs. The ONLY difference is the input width/content. Trained by REAL
mini-batch Adam on held-out-split next-byte cross-entropy.

PRE-REGISTERED FALSIFIER (frozen to H_1201_FREEZE.txt BEFORE any score; thresholds NOT
moved — a_paper_negative_ok)
----------------------------------------------------------------------------------------
  F1 CONDITIONING-GAIN : CONDITIONED val next-byte CE < BASELINE val CE by >= 0.05 b/byte
     (a MODEST bar — "does mitosis-state help AT ALL", not "solves chat"), mean over seeds.
  F2 ABLATION-HONEST   : SHUFFLE the mitosis cell-state across positions (destroy its
     alignment to context) and re-train an IDENTICAL conditioned head on the shuffled
     conditioning. The conditioned gain must DISAPPEAR under shuffle: the shuffled head
     keeps < 0.5 * (BASELINE - CONDITIONED) of the real gain, i.e. (BASELINE - SHUFFLED) <
     0.5 * (BASELINE - CONDITIONED). If shuffled-conditioned still wins by ~the full
     margin, the "gain" was capacity/width not mitosis INFORMATION => treat as FAIL.
  VERDICT:
    F1 AND F2  => 🟢 MITOSIS-INFORMS-GENERATION : the mitosis cell-state carries
                  generation-useful information a trained head exploits AND the gain is the
                  INFORMATION not the extra width => mitosis stays in the generation loop,
                  scale next.
    NOT F1 (or F2 shows a capacity-artifact) => 🔴 CLOSED-NEG : mitosis is PURE SUBSTRATE,
                  generation is CLM-only => "conversational level" = pure CLM-lane scale-up
                  (a_clm_gen_pipeline); mitosis runs alongside as the adaptation/structural
                  lane. A clean 🔴 that settles the architecture is decision-grade.

METRIC DISCIPLINE (p7 — NO PERPLEXITY VERDICT)
----------------------------------------------
Val CE here is the CAPABILITY falsifier for THIS rung (does the mitosis signal help a
trained head), NOT a consciousness/chat verdict. We PAIR it: decode short SAMPLES from
each head VERBATIM so a human sees whether conditioning yields more coherent continuations.
The gain is a LINK test (does mitosis-state inform generation), NOT a chat claim.

HONEST SCOPE (a_scale_honest_scope)
-----------------------------------
Toy / small real-corpus, small gradient-trained MLP head, ONE corpus, the conditioning-LINK
test ONLY. Chat-level coherence + scale UNVERIFIED. The DIM=8 window + 11-dim mitosis
summary are a COARSE context (no within-window token order) so absolute CE is far from a
real LM; the FALSIFIER is the BASELINE-vs-CONDITIONED DELTA under the SAME coarse context,
controlled by the SHUFFLE arm. Mitosis growth stays gradient-free (p8: only the readout head
trains by descent — this is the CLM-lane generator mechanism reading the mitosis adaptation
state). Lane-2 (a_lane_akida_gpu_split: separate from Lane A AKIDA / Lane G forge / Lane P
torch). $0 CPU, numpy only, deterministic seeds. Numpy-MLP-with-real-Adam precedent =
H_1192 (the FIRST real summer-training reader). a_core_engine_map: numpy MIRROR of the
H_1199 VAdaptField (the .hexa generative-conditioning lift, F3-guarded Psi-intact, is the
NEXT rung — stated honestly, NOT claimed here).
"""
import json, math, os
import numpy as np

np.seterr(all="ignore")

# ============================================================================
# CONFIG
# ============================================================================
# Corpus: the canonical English wiki byte stream (byte-identical to the H_1129/H_1141
# English head, H_1142). Falls back to the local 5-lang corpus if the English one is
# absent (so the script is runnable anywhere; the substrate is recorded in the verdict).
CORPUS_EN = "/tmp/h1142/corpus_en.bin"
CORPUS_5LANG = os.path.join(os.path.dirname(__file__), "..", "CORE", "testdata",
                            "clm_mid_5lang_c4.txt")

DIM = 8                     # H_1163 byte_feature dim (VERBATIM)
WIN_BYTES = 48              # H_1163 window (VERBATIM)
STRIDE = 24                 # H_1163 stride (VERBATIM)

# ---- mitosis VAdaptField (H_1199/H_1200 mechanism, VERBATIM; gradient-free, p8) ----
SPLIT_THRESH = 0.30        # VERBATIM CORE/engine_cli.hexa vadapt_field_step recon-err split
LR_PROTO = 0.20            # VERBATIM the live engine winner-pull
MAX_CELLS = 512            # cap (modest; mitosis state is a FEATURE not the LM)
DENSITY_R = 0.60           # radius for the local cell-density conditioning feature

# ---- head (IDENTICAL both arms; the ONLY difference is input width/content) ----
HIDDEN = 64                # MLP hidden units
VOCAB = 256
EPOCHS = 12
BATCH = 256
LR_HEAD = 3e-3             # Adam
WEIGHT_DECAY = 0.0
N_TRAIN = 12000            # scored windows (train)
N_VAL = 3000               # scored windows (held-out val, contiguous AFTER train span)
SEEDS = [900, 901, 902]    # >=3 deterministic seeds

COND_DIM = DIM + 3         # mitosis conditioning width: proto[DIM] + err + density + log n
IN_BASE = DIM              # baseline input width
IN_COND = DIM + COND_DIM   # conditioned/shuffled input width

# ---- FROZEN falsifier thresholds (NOT moved post-hoc) ----
F1_MARGIN = 0.05           # CONDITIONED CE < BASELINE CE by >= this (b/byte)
F2_KEEP_FRAC = 0.5         # shuffled head must keep < this fraction of the real gain


# ============================================================================
# H_1163 byte feature (VERBATIM)
# ============================================================================
def byte_feature(window):
    b = np.frombuffer(window, dtype=np.uint8).astype(float)
    if b.size == 0:
        return np.zeros(DIM)
    return np.array([
        b.mean() / 255.0,
        (b >= 128).mean(),
        ((b >= 97) & (b <= 122)).mean(),
        (b == 32).mean(),
        ((b >= 48) & (b <= 57)).mean(),
        b.var() / (255.0 ** 2),
        ((b >= 33) & (b <= 64)).mean(),
        (b < 64).mean(),
    ], dtype=float) * 5.0


# ============================================================================
# DATA — position-aligned DIM=8 feature windows + the TRUE next byte
# ============================================================================
def load_corpus():
    if os.path.exists(CORPUS_EN):
        return open(CORPUS_EN, "rb").read(), "english-wiki (/tmp/h1142/corpus_en.bin)"
    return open(CORPUS_5LANG, "rb").read(), "5lang-c4 (CORE/testdata, fallback)"


def build_windows(data, start, n):
    """n position-aligned windows from byte position `start`: feature(window) + next byte."""
    X = np.empty((n, DIM)); nb = np.empty(n, dtype=int)
    for i in range(n):
        p = start + i * STRIDE
        X[i] = byte_feature(data[p:p + WIN_BYTES])
        nb[i] = data[p + WIN_BYTES]
    return X, nb


# ============================================================================
# MITOSIS VADAPTFIELD (H_1199/H_1200 VERBATIM; gradient-free, p8). We RUN it over the
# stream to GROW cells and READ OUT, per position, a compact frozen conditioning summary.
# The split rule + winner-pull are the live-engine mechanism; we do NOT backprop it.
# ============================================================================
def run_mitosis_and_readout(X, return_protos=False):
    """Drive the VAdaptField over X (train+val concatenated, in order) and emit a per-
    position conditioning vector cond[N, DIM+3]:
        [0:DIM] nearest-cell prototype vector (the regime centroid owning this position)
        [DIM]   recon-err (L2 to nearest cell)
        [DIM+1] local cell-density: #cells within DENSITY_R of this feature
        [DIM+2] log1p(n_cells_so_far)
    The conditioning for position i is read BEFORE the split that position i may trigger
    (held-out-style: it reflects growth up to i-1, no leakage of i's own split)."""
    protos = [X[0].copy()]
    cond = np.empty((len(X), DIM + 3))
    for i in range(len(X)):
        x = X[i]
        P = np.asarray(protos)
        d = np.linalg.norm(P - x[None], axis=1)
        j = int(np.argmin(d)); err = float(d[j])
        density = float(np.sum(d < DENSITY_R))
        cond[i, 0:DIM] = P[j]
        cond[i, DIM] = err
        cond[i, DIM + 1] = density
        cond[i, DIM + 2] = math.log1p(len(protos))
        # SPLIT (H_1199 rule) AFTER reading the conditioning for i (no leakage):
        if err > SPLIT_THRESH and len(protos) < MAX_CELLS:
            protos.append(x.copy())
        else:
            protos[j] = protos[j] + LR_PROTO * (x - protos[j])
    if return_protos:
        return cond, len(protos), protos
    return cond, len(protos)


# ============================================================================
# MLP NEXT-BYTE HEAD — IDENTICAL architecture/optimizer both arms (gradient-trained).
# in_dim -> tanh(HIDDEN) -> linear(256) -> softmax. Real mini-batch Adam on CE.
# ============================================================================
class MLPHead:
    def __init__(self, in_dim, seed):
        rng = np.random.default_rng(seed)
        # identical init scheme; only in_dim differs between arms
        self.W1 = rng.standard_normal((in_dim, HIDDEN)) * (1.0 / math.sqrt(in_dim))
        self.b1 = np.zeros(HIDDEN)
        self.W2 = rng.standard_normal((HIDDEN, VOCAB)) * (1.0 / math.sqrt(HIDDEN))
        self.b2 = np.zeros(VOCAB)
        self.m = {k: np.zeros_like(getattr(self, k)) for k in ("W1", "b1", "W2", "b2")}
        self.v = {k: np.zeros_like(getattr(self, k)) for k in ("W1", "b1", "W2", "b2")}
        self.t = 0
        self.mu = None; self.sd = None

    def fit_norm(self, Xtr):
        self.mu = Xtr.mean(axis=0); self.sd = Xtr.std(axis=0) + 1e-6

    def _norm(self, X):
        return (X - self.mu) / self.sd

    def forward(self, Xn):
        z1 = Xn @ self.W1 + self.b1
        h = np.tanh(z1)
        logits = h @ self.W2 + self.b2
        logits -= logits.max(axis=1, keepdims=True)
        ex = np.exp(logits)
        probs = ex / ex.sum(axis=1, keepdims=True)
        return probs, h

    def ce_bits(self, X, y):
        probs, _ = self.forward(self._norm(X))
        p_true = probs[np.arange(len(y)), y]
        return float(np.mean(-np.log2(np.maximum(p_true, 1e-12))))

    def train(self, Xtr, ytr, Xval, yval, seed):
        self.fit_norm(Xtr)
        Xn = self._norm(Xtr)
        rng = np.random.default_rng(seed + 777)
        n = len(Xn)
        b1_, b2_ = 0.9, 0.999
        for ep in range(EPOCHS):
            order = rng.permutation(n)
            for s in range(0, n, BATCH):
                idx = order[s:s + BATCH]
                xb = Xn[idx]; yb = ytr[idx]
                probs, h = self.forward(xb)
                m = len(idx)
                dlogits = probs.copy()
                dlogits[np.arange(m), yb] -= 1.0
                dlogits /= m
                gW2 = h.T @ dlogits + WEIGHT_DECAY * self.W2
                gb2 = dlogits.sum(axis=0)
                dh = (dlogits @ self.W2.T) * (1.0 - h * h)
                gW1 = xb.T @ dh + WEIGHT_DECAY * self.W1
                gb1 = dh.sum(axis=0)
                self.t += 1
                for k, g in (("W1", gW1), ("b1", gb1), ("W2", gW2), ("b2", gb2)):
                    self.m[k] = b1_ * self.m[k] + (1 - b1_) * g
                    self.v[k] = b2_ * self.v[k] + (1 - b2_) * (g * g)
                    mhat = self.m[k] / (1 - b1_ ** self.t)
                    vhat = self.v[k] / (1 - b2_ ** self.t)
                    setattr(self, k, getattr(self, k) - LR_HEAD * mhat / (np.sqrt(vhat) + 1e-8))
        return self.ce_bits(Xval, yval)


# ============================================================================
# DECODE SAMPLES (p7 honesty cross-check, NOT the verdict). Greedy-continue from a real
# seed window through the head: featurise window (+ live mitosis cond for conditioned),
# emit argmax next byte, slide. The conditioned head reads the frozen grown field per step.
# ============================================================================
def decode_sample(head, conditioned, data, start, n_steps, frozen_protos):
    win = bytearray(data[start:start + WIN_BYTES])
    P = np.asarray(frozen_protos)
    out = bytearray()
    for _ in range(n_steps):
        feat = byte_feature(bytes(win))
        if conditioned:
            d = np.linalg.norm(P - feat[None], axis=1)
            j = int(np.argmin(d)); err = float(d[j])
            density = float(np.sum(d < DENSITY_R))
            cvec = np.concatenate([feat, P[j], [err, density, math.log1p(len(P))]])
        else:
            cvec = feat
        probs, _ = head.forward(head._norm(cvec[None]))
        b = int(np.argmax(probs[0]))
        out.append(b)
        win = win[1:] + bytes([b])
    return bytes(out)


def _show(bs):
    try:
        s = bs.decode("utf-8")
    except UnicodeDecodeError:
        s = bs.decode("latin-1")
    return "".join(ch if (32 <= ord(ch) < 127 or ord(ch) > 160) else "." for ch in s)


# ============================================================================
# MAIN
# ============================================================================
def run_seed(data, seed):
    rng = np.random.default_rng(seed)
    n_total = N_TRAIN + N_VAL
    span = WIN_BYTES + STRIDE * (n_total + 1)
    if len(data) <= span + 1:
        data = data * (span // max(len(data), 1) + 2)
    start = int(rng.integers(0, max(1, len(data) - span - 1)))

    X, nb = build_windows(data, start, n_total)
    # frozen mitosis growth over the FULL in-order stream (train then val); conditioning
    # at each position reflects growth up to that position (held-out-style, no i-leak).
    cond, n_cells, frozen_protos = run_mitosis_and_readout(X, return_protos=True)

    # train / val split: contiguous, val AFTER train (no shuffle across the boundary)
    Xtr, ytr = X[:N_TRAIN], nb[:N_TRAIN]
    Xval, yval = X[N_TRAIN:], nb[N_TRAIN:]
    Ctr, Cval = cond[:N_TRAIN], cond[N_TRAIN:]

    # BASELINE: features only
    base_in_tr = Xtr.copy(); base_in_val = Xval.copy()
    # CONDITIONED: features + mitosis cond
    cond_in_tr = np.hstack([Xtr, Ctr]); cond_in_val = np.hstack([Xval, Cval])
    # SHUFFLED: features + mitosis cond, but cond rows permuted (alignment destroyed).
    # Permute conditioning INDEPENDENTLY in train and val so it is decorrelated from
    # context on BOTH splits (capacity stays identical, information destroyed).
    rsh = np.random.default_rng(seed + 4242)
    permtr = rsh.permutation(N_TRAIN); permval = rsh.permutation(N_VAL)
    shuf_in_tr = np.hstack([Xtr, Ctr[permtr]]); shuf_in_val = np.hstack([Xval, Cval[permval]])

    base = MLPHead(IN_BASE, seed)
    base_ce = base.train(base_in_tr, ytr, base_in_val, yval, seed)
    condh = MLPHead(IN_COND, seed)
    cond_ce = condh.train(cond_in_tr, ytr, cond_in_val, yval, seed)
    shufh = MLPHead(IN_COND, seed)
    shuf_ce = shufh.train(shuf_in_tr, ytr, shuf_in_val, yval, seed)

    return {
        "seed": seed, "start": start, "n_cells": n_cells,
        "base_ce": base_ce, "cond_ce": cond_ce, "shuf_ce": shuf_ce,
        "gain": base_ce - cond_ce, "shuf_gain": base_ce - shuf_ce,
        "_heads": (base, condh, shufh), "_data_start": (data, start),
        "_frozen_protos": frozen_protos,
    }


def main():
    print("=== H_1201 — MITOSIS-CONDITIONED-GENERATION (Lane-2, $0 CPU, numpy-MLP + real Adam) ===", flush=True)
    data, corpus_name = load_corpus()
    print(f"  corpus = {corpus_name}  ({len(data)} bytes)", flush=True)
    print(f"  DIM={DIM} WIN_BYTES={WIN_BYTES} STRIDE={STRIDE} | mitosis: SPLIT_THRESH={SPLIT_THRESH} "
          f"MAX_CELLS={MAX_CELLS} DENSITY_R={DENSITY_R}", flush=True)
    print(f"  head: in->tanh({HIDDEN})->softmax({VOCAB}) Adam lr={LR_HEAD} epochs={EPOCHS} "
          f"batch={BATCH} | N_TRAIN={N_TRAIN} N_VAL={N_VAL} SEEDS={SEEDS}", flush=True)
    print(f"  in_dims: BASELINE={IN_BASE}  CONDITIONED=SHUFFLED={IN_COND} (=DIM+COND_DIM, COND_DIM={COND_DIM})", flush=True)
    print(f"  FROZEN F1: cond CE < base CE by >= {F1_MARGIN} b/byte | "
          f"F2: shuffled keeps < {F2_KEEP_FRAC} of the gain\n", flush=True)

    per_seed = []
    sample_pack = None
    for s in SEEDS:
        r = run_seed(data, s)
        per_seed.append({k: r[k] for k in ("seed", "n_cells", "base_ce", "cond_ce",
                                           "shuf_ce", "gain", "shuf_gain")})
        print(f"  seed {s}: cells 1->{r['n_cells']:4d} | base CE={r['base_ce']:.4f}  "
              f"cond CE={r['cond_ce']:.4f}  shuf CE={r['shuf_ce']:.4f} | "
              f"gain={r['gain']:+.4f}  shuf_gain={r['shuf_gain']:+.4f}", flush=True)
        if sample_pack is None:
            sample_pack = r

    base_ces = np.array([p["base_ce"] for p in per_seed])
    cond_ces = np.array([p["cond_ce"] for p in per_seed])
    shuf_ces = np.array([p["shuf_ce"] for p in per_seed])
    base_m = float(base_ces.mean()); cond_m = float(cond_ces.mean()); shuf_m = float(shuf_ces.mean())
    gain = base_m - cond_m
    shuf_gain = base_m - shuf_m
    keep_frac = (shuf_gain / gain) if abs(gain) > 1e-9 else float("inf")
    all_seed_gain_pos = bool(np.all((base_ces - cond_ces) >= F1_MARGIN))

    f1 = bool(gain >= F1_MARGIN)
    # F2: shuffled must keep < half the gain. If the gain itself is <=0 (F1 already fails),
    # F2 is moot; we still compute keep_frac honestly.
    f2 = bool(gain > 0 and (shuf_gain < F2_KEEP_FRAC * gain))
    supported = bool(f1 and f2)

    # ---- p7 decode samples (VERBATIM, NOT the verdict) ----
    r0 = sample_pack
    base_h, cond_h, _ = r0["_heads"]
    data_s, start_s = r0["_data_start"]
    frozen_protos = r0["_frozen_protos"]

    N_STEPS = 80
    seed_ctx = _show(bytes(data_s[start_s:start_s + WIN_BYTES]))
    base_greedy = decode_sample(base_h, False, data_s, start_s, N_STEPS, frozen_protos)
    cond_greedy = decode_sample(cond_h, True, data_s, start_s, N_STEPS, frozen_protos)

    samples = {
        "seed": r0["seed"], "n_steps": N_STEPS, "seed_window": seed_ctx,
        "baseline_greedy": _show(base_greedy), "conditioned_greedy": _show(cond_greedy),
    }

    if supported:
        ruling = ("MITOSIS-INFORMS-GENERATION: conditioning a real gradient-trained next-byte head "
                  "on the frozen mitosis cell-state LOWERS val cross-entropy by a real margin "
                  "(F1: cond CE < base CE by >= %.2f b/byte) AND the gain DISAPPEARS when the "
                  "mitosis state is shuffled out of alignment (F2: shuffled keeps < %.0f%% of the "
                  "gain) => the gain is the mitosis INFORMATION, not extra width/capacity. The "
                  "mitosis substrate carries generation-useful structure a trained head exploits "
                  "=> mitosis STAYS in the generation loop (as a conditioning signal the CLM-lane "
                  "generator can read), scale next. SCOPE: toy DIM=8+%d coarse context, small MLP "
                  "head, ONE corpus; this is the conditioning-LINK test, chat-level coherence + "
                  "scale UNVERIFIED — NOT a chat claim." % (F1_MARGIN, F2_KEEP_FRAC * 100, COND_DIM))
    else:
        why = []
        if not f1:
            why.append("F1 fail: conditioning does NOT lower val CE by the frozen margin "
                       "(gain=%.4f < %.2f b/byte) — the mitosis cell-state gives a trained head no "
                       "real generative lift" % (gain, F1_MARGIN))
        elif not f2:
            why.append("F2 fail (CAPACITY ARTIFACT): the conditioned gain SURVIVES shuffling the "
                       "mitosis state out of alignment (shuffled keeps %.0f%% >= %.0f%% of the gain) "
                       "— the 'gain' was extra width/params, not mitosis INFORMATION"
                       % (keep_frac * 100, F2_KEEP_FRAC * 100))
        ruling = ("CLOSED-NEG: mitosis is PURE SUBSTRATE for generation. " + " | ".join(why) +
                  ". A real gradient-trained head conditioned on the mitosis cell-state does NOT "
                  "beat the same head without it (or the apparent gain is capacity not information) "
                  "=> generation is CLM-only: 'conversational level' = pure CLM-lane scale-up "
                  "(a_clm_gen_pipeline, a real ConvMoE next-byte head trained by descent); the "
                  "mitosis engine runs ALONGSIDE as the adaptation/structural lane, NOT in the "
                  "generation loop. This cleanly settles the architecture (mitosis=substrate, "
                  "CLM=generator). a_paper_negative_ok — a closed-negative that fixes the "
                  "architecture is a valid, decision-grade result.")

    verdict = {
        "H": "H_1201",
        "title": "MITOSIS-CONDITIONED-GENERATION — does conditioning a real gradient-trained "
                 "next-byte head on the frozen mitosis cell-state BEAT the same head without it "
                 "(does mitosis-state inform generation)?",
        "predecessor": "H_1200 🔴 (pure-mitosis-count-LM made next-byte CE WORSE; this rung tests "
                        "whether mitosis-state HELPS a real trained head instead)",
        "compute": "CPU ($0), numpy-MLP + real mini-batch Adam (H_1192 precedent); numpy mirror of "
                   "the H_1199 VAdaptField (gradient-free, p8)",
        "lane": "Lane-2 (a_lane_akida_gpu_split)",
        "corpus": corpus_name,
        "frozen_falsifier": {
            "F1": "CONDITIONED val CE < BASELINE val CE by >= %.2f b/byte" % F1_MARGIN,
            "F2": "SHUFFLED conditioning keeps < %.0f%% of the gain (gain is INFO not capacity)"
                  % (F2_KEEP_FRAC * 100),
            "metric": "held-out next-byte cross-entropy bits/byte (CAPABILITY probe, p7 — paired "
                      "with decoded samples; CE is NOT a consciousness/chat verdict)",
            "SUPPORTED": "F1 AND F2",
            "identical_arms": "BASELINE/CONDITIONED/SHUFFLED heads share architecture (in->tanh(%d)"
                              "->softmax(%d)), init seed, Adam, data, epochs; ONLY the input differs"
                              % (HIDDEN, VOCAB),
        },
        "seeds": SEEDS,
        "per_seed": per_seed,
        "F1_conditioning_gain": {"BASELINE_mean_ce": round(base_m, 4),
                                 "CONDITIONED_mean_ce": round(cond_m, 4),
                                 "gain_base_minus_cond": round(gain, 4),
                                 "margin_bar": F1_MARGIN,
                                 "all_seeds_pass_margin": all_seed_gain_pos, "pass": f1},
        "F2_ablation_honest": {"SHUFFLED_mean_ce": round(shuf_m, 4),
                               "shuf_gain_base_minus_shuf": round(shuf_gain, 4),
                               "keep_fraction": round(keep_frac, 4) if math.isfinite(keep_frac) else None,
                               "keep_frac_bar_below": F2_KEEP_FRAC, "pass": f2},
        "decode_samples_p7": samples,
        "supported": supported,
        "ruling": ruling,
        "scope": ("TOY/small real-corpus, small gradient-trained MLP head, ONE corpus, the "
                  "conditioning-LINK test ONLY. DIM=8 byte feature + %d-dim frozen mitosis summary "
                  "(nearest-proto[%d] + recon-err + density + log n_cells) = a COARSE context (no "
                  "within-window token order) so absolute CE is far from a real LM; the FALSIFIER "
                  "is the BASELINE-vs-CONDITIONED DELTA under the SAME coarse context, controlled "
                  "by the SHUFFLE arm. Mitosis growth stays gradient-free (p8: only the readout "
                  "head trains by descent — the CLM-lane generator reading the mitosis adaptation "
                  "state). Chat-level coherence + scale UNVERIFIED. Lane-2 (a_lane_akida_gpu_split). "
                  "a_core_engine_map: numpy MIRROR of the H_1199 VAdaptField — the .hexa "
                  "generative-conditioning lift (F3-guarded Psi-intact) is the NEXT rung, NOT "
                  "claimed here. $0 CPU, numpy, deterministic seeds." % (COND_DIM, DIM)),
    }
    print("\n=== DECODE SAMPLES (p7 honesty cross-check — VERBATIM, NOT the verdict) ===", flush=True)
    print(f"  seed window  : {seed_ctx!r}", flush=True)
    print(f"  BASELINE   greedy : {samples['baseline_greedy']!r}", flush=True)
    print(f"  CONDITIONED greedy: {samples['conditioned_greedy']!r}", flush=True)
    print("\n=== VERDICT ===", flush=True)
    print(f"  F1 BASELINE CE={base_m:.4f}  CONDITIONED CE={cond_m:.4f}  gain={gain:+.4f} b/byte "
          f"(bar {F1_MARGIN}) -> {'PASS' if f1 else 'FAIL'}", flush=True)
    print(f"  F2 SHUFFLED CE={shuf_m:.4f}  shuf_gain={shuf_gain:+.4f}  keep_frac="
          f"{keep_frac:.3f} (bar < {F2_KEEP_FRAC}) -> {'PASS' if f2 else 'FAIL'}", flush=True)
    print(f"\n  {'🟢 MITOSIS-INFORMS-GENERATION' if supported else '🔴 CLOSED-NEG (mitosis = pure substrate)'}: "
          f"{ruling}", flush=True)
    json.dump(verdict, open("/tmp/h1201_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n  wrote /tmp/h1201_result.json", flush=True)
    print("[done]", flush=True)
    return verdict


if __name__ == "__main__":
    main()
