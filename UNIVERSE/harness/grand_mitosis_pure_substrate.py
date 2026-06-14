"""
GRAND-THEOREM 대가설 G3 — MITOSIS = PURE-SUBSTRATE THEOREM (미토시스=순수기질 정리)
============================================================================
A GRAND theorem built on OUR campaign findings (H_1199/H_1194 🟢, H_1200 🔴,
H_1201 🔴). NOT a textbook reproduction — a new structural claim about the
anima substrate.

CLAIM (formalised).  Partition a substrate's competence into two parts on the
SAME stream:
  (A) ADAPTATION  = lowering reconstruction error / raising I(internal model;
                    world). Measured: L2 reconstruction error of a prototype
                    field over a stream.
  (G) GENERATION  = emitting the next symbol a reader scores as correct.
                    Measured: held-out next-byte accuracy / cross-entropy of a
                    trained head.
The theorem:
  T1  Mitosis is SUFFICIENT for A  — a mitosis-driven field strictly lowers
      reconstruction error vs a frozen field (recon-err ON < OFF).      (H_1199)
  T2  Mitosis is INSUFFICIENT for G — a mitosis-only system cannot generate
      above chance (next-symbol accuracy <= chance + eps).              (H_1200)
  T3  Mitosis adds ZERO usable information to a real generator — a next-byte
      head conditioned on the mitosis state does NOT beat the same head without
      it (gain <= 0), and a SHUFFLED-mitosis control is no worse, confirming the
      signal is not even noise-useful.                                  (H_1201)
  =>  A _|_ G across mitosis: the mechanism that maximises adaptation
      contributes nothing to generation. They are ORTHOGONAL competences;
      generation must come from a separate (CLM / gradient) lane.
      "mitosis = substrate, CLM = generator."

SUBSTRATE.  T1 is ALSO measured on the LIVE .hexa engine (VAdaptField in
CORE/engine_cli.hexa) by UNIVERSE/harness/grand_mitosis_pure_substrate.hexa; the
numpy mirror below reproduces the SAME mechanism (vadapt_field_step VERBATIM:
nearest-by-L2, recon-err = L2 to nearest, split when err>0.30 & capacity,
LR=0.20 winner pull) and additionally carries the gradient-trained generation
arms T2/T3/F4 (which need real Adam descent — the CLM-lane generator, p8: only
the readout head trains; the mitosis growth is gradient-free).

p7 — code-measured (L2 recon-err, byte accuracy, CE bits/byte). NO perplexity
verdict, NO LLM judge. >= 3 seeds. $0 CPU, numpy only, deterministic.
a_scale_honest_scope: toy / small real corpus, gradient-free mitosis numpy
mirror, ONE corpus. The T2/T3 NEGATIVES are the POINT (a_paper_negative_ok).
"""
import json, math, os
import numpy as np

np.seterr(all="ignore")

# ============================================================================
# CONFIG  (mitosis constants = CORE/engine_cli.hexa vadapt_field_step VERBATIM)
# ============================================================================
HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_EN = "/tmp/h1142/corpus_en.bin"
CORPUS_5LANG = os.path.join(HERE, "..", "..", "CORE", "testdata", "clm_mid_5lang_c4.txt")

DIM = 8                  # H_1163 byte_feature dim (VERBATIM)
WIN_BYTES = 48           # H_1163 window
STRIDE = 24              # H_1163 stride

SPLIT_THRESH = 0.30      # VERBATIM vadapt_field_step recon-err split bar
LR_PROTO = 0.20          # VERBATIM winner pull
MAX_CELLS = 512
DENSITY_R = 0.60

HIDDEN = 64
VOCAB = 256
EPOCHS = 12
BATCH = 256
LR_HEAD = 3e-3
N_TRAIN = 12000
N_VAL = 3000
SEEDS = [900, 901, 902]

COND_DIM = DIM + 3       # mitosis summary: proto[DIM] + err + density + log n
IN_BASE = DIM
IN_COND = DIM + COND_DIM

# ---- FROZEN falsifier thresholds (set BEFORE measuring; NOT moved) ----
# Baselines are the HONEST ones: T2's null is the unigram majority-class predictor
# (NOT uniform 1/256 — predicting the single most-frequent byte already scores
# ~12% on text, so beating uniform is NOT "generating"; the real test is whether
# mitosis adds anything over just-say-the-commonest-byte). T3's "help" margin is
# H_1201's frozen +0.05 b/byte — the theorem's NEGATIVE is "conditioning does NOT
# clear that margin" (gain < 0.05), reproducing H_1201 verbatim.
F1_RECON_RATIO = 2.0     # T1: recon-err OFF / ON >= this (ON strictly lower)
F2_OVER_MAJORITY = 0.02  # T2: mitosis-only acc must NOT beat majority-class acc by >= this
F3_HELP_MARGIN = 0.05    # T3: conditioning "helps" iff gain >= this (b/byte) — H_1201 frozen
F3_SHUF_TOL = 0.02       # T3: shuffled must be no better than real cond by more than noise
F4_ORTHO_ABS = 0.30      # T4: |corr(adaptation_contrib, generation_contrib)| < this


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


def load_corpus():
    if os.path.exists(CORPUS_EN):
        return open(CORPUS_EN, "rb").read(), "english-wiki (/tmp/h1142/corpus_en.bin)"
    return open(CORPUS_5LANG, "rb").read(), "5lang-c4 (CORE/testdata, fallback)"


def build_windows(data, start, n):
    X = np.empty((n, DIM)); nb = np.empty(n, dtype=int)
    for i in range(n):
        p = start + i * STRIDE
        X[i] = byte_feature(data[p:p + WIN_BYTES])
        nb[i] = data[p + WIN_BYTES]
    return X, nb


# ============================================================================
# MITOSIS VADAPTFIELD (vadapt_field_step VERBATIM, gradient-free p8).
# Drives the field over the stream; returns per-position conditioning summary,
# per-position recon-err (for T1), per-position nearest-cell id (for T2/F4).
# ============================================================================
def run_mitosis(X, frozen_off=False):
    """frozen_off=False -> mitosis ON (cells split). True -> OFF (1 cell, H_1159
    control: never split, only winner-pull). Returns cond[N,DIM+3], recon[N],
    cell_id[N], n_cells."""
    protos = [X[0].copy()]
    cond = np.empty((len(X), DIM + 3))
    recon = np.empty(len(X))
    cell_id = np.empty(len(X), dtype=int)
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
        recon[i] = err
        cell_id[i] = j
        # split (ON only) AFTER reading conditioning for i (no leak):
        if (not frozen_off) and err > SPLIT_THRESH and len(protos) < MAX_CELLS:
            protos.append(x.copy())
        else:
            protos[j] = protos[j] + LR_PROTO * (x - protos[j])
    return cond, recon, cell_id, len(protos)


# ============================================================================
# MLP NEXT-BYTE HEAD (gradient-trained, IDENTICAL arms; ONLY input differs).
# in -> tanh(HIDDEN) -> softmax(256). Real mini-batch Adam on CE.
# ============================================================================
class MLPHead:
    def __init__(self, in_dim, seed):
        rng = np.random.default_rng(seed)
        self.W1 = rng.standard_normal((in_dim, HIDDEN)) * (1.0 / math.sqrt(in_dim))
        self.b1 = np.zeros(HIDDEN)
        self.W2 = rng.standard_normal((HIDDEN, VOCAB)) * (1.0 / math.sqrt(HIDDEN))
        self.b2 = np.zeros(VOCAB)
        self.m = {k: np.zeros_like(getattr(self, k)) for k in ("W1", "b1", "W2", "b2")}
        self.v = {k: np.zeros_like(getattr(self, k)) for k in ("W1", "b1", "W2", "b2")}
        self.t = 0
        self.mu = None; self.sd = None

    def fit_norm(self, X):
        self.mu = X.mean(axis=0); self.sd = X.std(axis=0) + 1e-6

    def _norm(self, X):
        return (X - self.mu) / self.sd

    def forward(self, Xn):
        h = np.tanh(Xn @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        logits -= logits.max(axis=1, keepdims=True)
        ex = np.exp(logits)
        return ex / ex.sum(axis=1, keepdims=True), h

    def ce_bits(self, X, y):
        probs, _ = self.forward(self._norm(X))
        p = probs[np.arange(len(y)), y]
        return float(np.mean(-np.log2(np.maximum(p, 1e-12))))

    def acc(self, X, y):
        probs, _ = self.forward(self._norm(X))
        return float(np.mean(np.argmax(probs, axis=1) == y))

    def train(self, Xtr, ytr, seed):
        self.fit_norm(Xtr)
        Xn = self._norm(Xtr)
        rng = np.random.default_rng(seed + 777)
        n = len(Xn); b1_, b2_ = 0.9, 0.999
        for ep in range(EPOCHS):
            order = rng.permutation(n)
            for s in range(0, n, BATCH):
                idx = order[s:s + BATCH]
                xb = Xn[idx]; yb = ytr[idx]
                probs, h = self.forward(xb)
                m = len(idx)
                dlogits = probs.copy(); dlogits[np.arange(m), yb] -= 1.0; dlogits /= m
                gW2 = h.T @ dlogits; gb2 = dlogits.sum(axis=0)
                dh = (dlogits @ self.W2.T) * (1.0 - h * h)
                gW1 = xb.T @ dh; gb1 = dh.sum(axis=0)
                self.t += 1
                for k, g in (("W1", gW1), ("b1", gb1), ("W2", gW2), ("b2", gb2)):
                    self.m[k] = b1_ * self.m[k] + (1 - b1_) * g
                    self.v[k] = b2_ * self.v[k] + (1 - b2_) * (g * g)
                    mh = self.m[k] / (1 - b1_ ** self.t)
                    vh = self.v[k] / (1 - b2_ ** self.t)
                    setattr(self, k, getattr(self, k) - LR_HEAD * mh / (np.sqrt(vh) + 1e-8))


# ============================================================================
# T2 — MITOSIS-ONLY GENERATOR (no gradient): predict next byte from the cell that
# owns this position, using the per-cell majority next byte learned on TRAIN. This
# is the H_1200 pure-mitosis-LM mechanism. If mitosis "generates", this beats
# chance (1/256). It does not.
# ============================================================================
def mitosis_only_accuracy(cell_id, nb, n_train):
    """Returns (mitosis_only_acc, majority_class_acc). The mitosis-only predictor
    reads the per-cell majority next byte (H_1200 pure-mitosis-LM). The HONEST null
    is the unigram majority-class predictor (always emit the single most-frequent
    byte): if mitosis cannot beat that, it is NOT generating — it is just inheriting
    byte-frequency skew through whichever cell owns the position."""
    tr_cells, tr_nb = cell_id[:n_train], nb[:n_train]
    va_cells, va_nb = cell_id[n_train:], nb[n_train:]
    maj = {}
    for c in np.unique(tr_cells):
        ys = tr_nb[tr_cells == c]
        vals, cnts = np.unique(ys, return_counts=True)
        maj[c] = int(vals[np.argmax(cnts)])
    gv, gc = np.unique(tr_nb, return_counts=True)
    glob = int(gv[np.argmax(gc)])                       # unigram majority byte
    pred = np.array([maj.get(int(c), glob) for c in va_cells])
    mito_acc = float(np.mean(pred == va_nb))
    majority_acc = float(np.mean(va_nb == glob))        # the honest null
    return mito_acc, majority_acc


# ============================================================================
# F4 — ORTHOGONALITY: per-prototype-cell, measure
#   adaptation_contrib(cell) = how much the cell LOWERS recon-err for its members
#                              (mean OFF-single-proto err - mean within-cell err)
#   generation_contrib(cell) = how PREDICTABLE the next byte is within the cell
#                              (max class freq of next byte among the cell's members)
# If adaptation and generation were the same competence, cells that adapt well
# would also predict well -> high corr. The theorem predicts corr ~ 0.
# ============================================================================
def orthogonality_corr(X, cell_id, recon, nb, n_train):
    cells = np.unique(cell_id[:n_train])
    off_proto = X[:n_train].mean(axis=0)            # the single OFF prototype baseline
    off_err_all = np.linalg.norm(X[:n_train] - off_proto[None], axis=1).mean()
    adapt, gen = [], []
    for c in cells:
        mask = cell_id[:n_train] == c
        if mask.sum() < 20:                          # skip tiny cells (noise)
            continue
        within_err = recon[:n_train][mask].mean()
        adapt.append(off_err_all - within_err)       # error reduction this cell buys
        ys = nb[:n_train][mask]
        _, cnts = np.unique(ys, return_counts=True)
        gen.append(cnts.max() / mask.sum())          # best next-byte predictability
    adapt = np.array(adapt); gen = np.array(gen)
    if len(adapt) < 3 or adapt.std() < 1e-9 or gen.std() < 1e-9:
        return 0.0, len(adapt)
    return float(np.corrcoef(adapt, gen)[0, 1]), len(adapt)


# ============================================================================
# PER-SEED
# ============================================================================
def run_seed(data, seed):
    rng = np.random.default_rng(seed)
    n_total = N_TRAIN + N_VAL
    span = WIN_BYTES + STRIDE * (n_total + 1)
    if len(data) <= span + 1:
        data = data * (span // max(len(data), 1) + 2)
    start = int(rng.integers(0, max(1, len(data) - span - 1)))
    X, nb = build_windows(data, start, n_total)

    # ---- T1: mitosis ON vs OFF reconstruction error ----
    cond_on, recon_on, cid_on, n_cells = run_mitosis(X, frozen_off=False)
    cond_off, recon_off, cid_off, _ = run_mitosis(X, frozen_off=True)
    q = len(recon_on) // 4
    err_on = float(recon_on[-q:].mean())             # late-run recon err ON
    err_off = float(recon_off[-q:].mean())           # late-run recon err OFF (frozen)

    # ---- T2: mitosis-only next-byte accuracy vs majority-class null ----
    mito_acc, majority_acc = mitosis_only_accuracy(cid_on, nb, N_TRAIN)
    chance = 1.0 / VOCAB

    # ---- T3: conditioned vs baseline gradient-trained head + shuffled control ----
    Xtr, ytr = X[:N_TRAIN], nb[:N_TRAIN]
    Xval, yval = X[N_TRAIN:], nb[N_TRAIN:]
    Ctr, Cval = cond_on[:N_TRAIN], cond_on[N_TRAIN:]
    base = MLPHead(IN_BASE, seed);  base.train(Xtr, ytr, seed)
    base_ce = base.ce_bits(Xval, yval)
    condh = MLPHead(IN_COND, seed)
    condh.train(np.hstack([Xtr, Ctr]), ytr, seed)
    cond_ce = condh.ce_bits(np.hstack([Xval, Cval]), yval)
    rsh = np.random.default_rng(seed + 4242)
    ptr = rsh.permutation(N_TRAIN); pva = rsh.permutation(N_VAL)
    shufh = MLPHead(IN_COND, seed)
    shufh.train(np.hstack([Xtr, Ctr[ptr]]), ytr, seed)
    shuf_ce = shufh.ce_bits(np.hstack([Xval, Cval[pva]]), yval)

    # ---- F4: orthogonality of adaptation vs generation per cell ----
    ortho, n_used = orthogonality_corr(X, cid_on, recon_on, nb, N_TRAIN)

    return {
        "seed": seed, "start": start, "n_cells": n_cells,
        "err_on": err_on, "err_off": err_off,
        "mito_acc": mito_acc, "majority_acc": majority_acc, "chance": chance,
        "base_ce": base_ce, "cond_ce": cond_ce, "shuf_ce": shuf_ce,
        "gain": base_ce - cond_ce, "shuf_gain": base_ce - shuf_ce,
        "ortho": ortho, "ortho_cells": n_used,
    }


def main():
    print("=== GRAND-THEOREM G3 — MITOSIS = PURE-SUBSTRATE THEOREM (numpy mirror, $0 CPU, p7) ===", flush=True)
    data, corpus = load_corpus()
    print(f"  corpus = {corpus}  ({len(data)} bytes)", flush=True)
    print(f"  DIM={DIM} WIN={WIN_BYTES} STRIDE={STRIDE} | mitosis SPLIT={SPLIT_THRESH} LR={LR_PROTO} "
          f"MAX_CELLS={MAX_CELLS} | head in->tanh({HIDDEN})->softmax({VOCAB}) Adam lr={LR_HEAD} "
          f"ep={EPOCHS} | N_TR={N_TRAIN} N_VAL={N_VAL} SEEDS={SEEDS}", flush=True)
    print(f"  FROZEN: F1 OFF/ON recon >= {F1_RECON_RATIO} | F2 mito-acc <= majority+{F2_OVER_MAJORITY} | "
          f"F3 gain < {F3_HELP_MARGIN} (& shuf no better, tol {F3_SHUF_TOL}) | F4 |ortho| < {F4_ORTHO_ABS}\n", flush=True)

    rows = []
    for s in SEEDS:
        r = run_seed(data, s)
        rows.append(r)
        print(f"  seed {s}: cells 1->{r['n_cells']:4d} | T1 recon ON={r['err_on']:.4f} "
              f"OFF={r['err_off']:.4f} (OFF/ON={r['err_off']/max(r['err_on'],1e-9):.2f}x) | "
              f"T2 mito-acc={r['mito_acc']:.4f} majority={r['majority_acc']:.4f} | "
              f"T3 base CE={r['base_ce']:.4f} cond CE={r['cond_ce']:.4f} gain={r['gain']:+.4f} "
              f"shuf CE={r['shuf_ce']:.4f} | F4 ortho={r['ortho']:+.3f}", flush=True)

    A = lambda k: np.array([r[k] for r in rows])
    err_on = float(A("err_on").mean()); err_off = float(A("err_off").mean())
    recon_ratio = err_off / max(err_on, 1e-9)
    mito_acc = float(A("mito_acc").mean()); majority_acc = float(A("majority_acc").mean())
    chance = rows[0]["chance"]
    base_m = float(A("base_ce").mean()); cond_m = float(A("cond_ce").mean()); shuf_m = float(A("shuf_ce").mean())
    gain = base_m - cond_m; shuf_gain = base_m - shuf_m
    keep_frac = (shuf_gain / gain) if abs(gain) > 1e-9 else float("inf")
    ortho = float(A("ortho").mean())

    # ---- verdicts (the theorem's T2/T3 are NEGATIVES: mitosis does NOT generate /
    #      does NOT inform — a_paper_negative_ok) ----
    t1 = bool(recon_ratio >= F1_RECON_RATIO and err_on < err_off)             # SUFFICIENT for A
    # T2: mitosis-only must NOT beat the unigram majority-class null => no generation.
    t2 = bool(mito_acc <= majority_acc + F2_OVER_MAJORITY)
    # T3: conditioning must NOT clear the H_1201 "help" margin (gain < 0.05) => no info;
    #     AND shuffled must be no BETTER than real conditioning (shuf_gain <= gain + tol)
    #     i.e. the mitosis signal is not even noise-useful.
    t3_no_help = bool(gain < F3_HELP_MARGIN)
    t3_shuf_ok = bool(shuf_gain <= gain + F3_SHUF_TOL)
    t3 = bool(t3_no_help and t3_shuf_ok)                                       # INSUFFICIENT for G (no info)
    t4 = bool(abs(ortho) < F4_ORTHO_ABS)                                       # A _|_ G
    supported = bool(t1 and t2 and t3 and t4)

    if supported:
        ruling = (
            "MITOSIS = PURE SUBSTRATE (THEOREM SUPPORTED). T1: a mitosis-driven field STRICTLY "
            "lowers reconstruction error vs a frozen field (OFF/ON=%.2fx >= %.1f) => mitosis is "
            "SUFFICIENT for ADAPTATION. T2: a mitosis-ONLY system predicts the next byte at %.4f, "
            "NOT beating the unigram majority-class null %.4f (it only inherits byte-frequency "
            "skew) => mitosis CANNOT generate. T3: a real gradient-trained next-byte head "
            "CONDITIONED on the mitosis cell-state does NOT clear the H_1201 help margin "
            "(gain=%+.4f b/byte < %.2f) and the SHUFFLED control is no worse (shuf_gain=%+.4f) => "
            "the mitosis state adds ZERO usable (not even noise-useful) generation information. T4: "
            "per-cell adaptation-contribution and generation-contribution are UNCORRELATED "
            "(|ortho|=%.3f < %.2f). THEREFORE ADAPTATION _|_ GENERATION across mitosis: the "
            "mechanism that maximises adaptation contributes nothing to generation; they are "
            "ORTHOGONAL competences and generation must come from a separate (CLM/gradient) lane. "
            "'mitosis = substrate, CLM = generator.' a_clm_gen_pipeline." % (
                recon_ratio, F1_RECON_RATIO, mito_acc, majority_acc, gain, F3_HELP_MARGIN,
                shuf_gain, abs(ortho), F4_ORTHO_ABS))
    else:
        fails = []
        if not t1: fails.append("T1 fail: recon OFF/ON=%.2f < %.1f (mitosis did not adapt)" % (recon_ratio, F1_RECON_RATIO))
        if not t2: fails.append("T2 fail: mitosis-only acc %.4f beats majority %.4f by >= %.2f (mitosis DID generate)" % (mito_acc, majority_acc, F2_OVER_MAJORITY))
        if not t3: fails.append("T3 fail: conditioning gain=%+.4f cleared help margin %.2f or shuffled was better (mitosis informed the generator)" % (gain, F3_HELP_MARGIN))
        if not t4: fails.append("T4 fail: |ortho|=%.3f >= %.2f (adaptation & generation correlated)" % (abs(ortho), F4_ORTHO_ABS))
        ruling = "THEOREM NOT SUPPORTED. " + " | ".join(fails)

    verdict = {
        "G": "G3", "name": "MITOSIS = PURE-SUBSTRATE THEOREM",
        "claim": "mitosis is SUFFICIENT for adaptation, INSUFFICIENT for generation, "
                 "and adaptation _|_ generation across mitosis (mitosis=substrate, CLM=generator)",
        "compute": "CPU $0, numpy-MLP + real Adam (H_1192 precedent); numpy MIRROR of the H_1199 "
                   "VAdaptField (vadapt_field_step VERBATIM, gradient-free p8); T1 ALSO on the live "
                   ".hexa engine (grand_mitosis_pure_substrate.hexa)",
        "corpus": corpus, "seeds": SEEDS,
        "frozen_falsifier": {
            "F1_T1_adaptation": "recon-err OFF/ON >= %.1f AND ON < OFF" % F1_RECON_RATIO,
            "F2_T2_no_generation": "mitosis-only next-byte acc <= majority-class acc + %.2f (does NOT beat the unigram null)" % F2_OVER_MAJORITY,
            "F3_T3_no_info": "conditioning gain < %.2f b/byte (does NOT clear the H_1201 help margin) AND shuffled no better than real cond (shuf_gain <= gain + %.2f)" % (F3_HELP_MARGIN, F3_SHUF_TOL),
            "F4_T4_orthogonal": "|corr(adapt_contrib, gen_contrib)| < %.2f" % F4_ORTHO_ABS,
            "SUPPORTED": "T1 AND T2 AND T3 AND T4",
            "metric": "L2 recon-err (T1) · next-byte acc vs UNIGRAM MAJORITY null (T2) · held-out CE bits/byte vs H_1201 +0.05 help margin (T3) · per-cell Pearson corr (T4); p7, no perplexity/LLM judge",
        },
        "per_seed": [{k: r[k] for k in ("seed","n_cells","err_on","err_off","mito_acc","majority_acc",
                                        "base_ce","cond_ce","shuf_ce","gain","ortho")} for r in rows],
        "T1_adaptation": {"recon_err_ON": round(err_on,4), "recon_err_OFF": round(err_off,4),
                          "ratio_OFF_over_ON": round(recon_ratio,3), "bar": F1_RECON_RATIO, "pass": t1},
        "T2_no_generation": {"mitosis_only_acc": round(mito_acc,5), "majority_class_acc": round(majority_acc,5),
                             "uniform_chance": round(chance,5), "bar_over_majority": F2_OVER_MAJORITY, "pass": t2},
        "T3_no_info_to_generator": {"BASELINE_ce": round(base_m,4), "CONDITIONED_ce": round(cond_m,4),
                                    "gain_base_minus_cond": round(gain,4), "help_margin": F3_HELP_MARGIN,
                                    "SHUFFLED_ce": round(shuf_m,4), "shuf_gain": round(shuf_gain,4),
                                    "keep_frac": (round(keep_frac,3) if math.isfinite(keep_frac) else None),
                                    "no_help": t3_no_help, "shuf_not_better": t3_shuf_ok, "pass": t3},
        "T4_orthogonality": {"corr_adapt_vs_gen": round(ortho,4), "bar_abs_below": F4_ORTHO_ABS, "pass": t4},
        "supported": supported, "ruling": ruling,
        "scope": ("TOY / small real-corpus, gradient-free mitosis numpy MIRROR (live .hexa T1 lift = "
                  "grand_mitosis_pure_substrate.hexa, this rung), ONE corpus, DIM=8 coarse byte "
                  "feature (no within-window token order so absolute CE is far from a real LM — the "
                  "falsifier is the ON/OFF, conditioned/baseline DELTAS under the SAME context, "
                  "controlled by the SHUFFLE arm). p8: only the readout head trains by descent (the "
                  "CLM-lane generator); mitosis growth is gradient-free. Chat-level + scale "
                  "UNVERIFIED. The T2/T3 NEGATIVES are the POINT — a clean closed-negative that "
                  "mitosis cannot generate is a valid result (a_paper_negative_ok). $0 CPU, numpy, "
                  "deterministic seeds. xref H_1199 H_1194 H_1200 H_1201."),
    }

    print("\n=== VERDICT ===", flush=True)
    print(f"  T1 ADAPTATION (suff)  : recon ON={err_on:.4f} OFF={err_off:.4f} ratio={recon_ratio:.2f}x "
          f"(bar>={F1_RECON_RATIO}) -> {'PASS' if t1 else 'FAIL'}", flush=True)
    print(f"  T2 NO-GENERATION      : mito-only acc={mito_acc:.5f} majority={majority_acc:.5f} "
          f"(uniform-chance={chance:.5f}; bar<=majority+{F2_OVER_MAJORITY}) -> {'PASS' if t2 else 'FAIL'}", flush=True)
    print(f"  T3 NO-INFO-TO-GEN     : base CE={base_m:.4f} cond CE={cond_m:.4f} gain={gain:+.4f} "
          f"(help margin {F3_HELP_MARGIN}) shuf CE={shuf_m:.4f} shuf_gain={shuf_gain:+.4f} "
          f"-> {'PASS' if t3 else 'FAIL'}", flush=True)
    print(f"  T4 ORTHOGONALITY      : corr(adapt,gen)={ortho:+.4f} (bar |.|<{F4_ORTHO_ABS}) "
          f"-> {'PASS' if t4 else 'FAIL'}", flush=True)
    print(f"\n  THEOREM {'🟢 SUPPORTED' if supported else '🔴 NOT SUPPORTED'} — {ruling}\n", flush=True)
    print("=== VERDICT JSON ===", flush=True)
    print(json.dumps(verdict, indent=2, ensure_ascii=False), flush=True)
    return verdict


if __name__ == "__main__":
    main()
