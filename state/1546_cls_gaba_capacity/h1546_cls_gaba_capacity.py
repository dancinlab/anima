#!/usr/bin/env python3
"""
H_1546 — GABA × CLS: inhibitory E/I-balance gating of fast-store effective capacity
(the 5th neurotransmitter fused into the H_1532 two-store CLS module — completes the
"신경전달물질 모두 융합" goal; tail candidate #6 of census H_1542 §rank-6).

FUSION of two prior lanes (a_no_llm_frame_trap — biological structure first):
  • H_1532 🟢 (PR #2514/#2522) MULTI-STORE / Complementary Learning Systems broke the
    H_1284 neuromodulation wall on AB-AC interference: TWO phase-separated stores (a FAST
    episodic store written in Hasselmo encode-mode + a SLOW store fed by interleaved
    REPLAY) keep confusable A->B / A->C bindings in separate substrates. The win is
    HAVING SEPARATE STORES. But H_1532's fast store wrote each binding into a DENSE
    representation (the raw key_vec) — near-collinear keys still COLLIDE in the fast
    store's geometry (the H_1533 modern-Hopfield wall regime).
  • H_1533 🧱 (PR #2515) MODERN/DENSE associative memory did NOT break the confusable
    near-collinear recall regime (LINEAR 0.889 = DENSE 0.889 > MODERN 0.839): a
    monotone sharpening of the RETRIEVAL energy preserves the single-step winner, so on
    a confusable basin it cannot orthogonalize. The retrieval rule cannot separate what
    the WRITE laid down collinear.

THE GABA REOPEN (this hypothesis): the missing lever is not the retrieval energy but the
WRITE geometry — pattern SEPARATION at encode time. GABAergic inhibition in the dentate
gyrus enforces SPARSE coding (k-winner-take-all, E/I balance): only the k most-active
units survive lateral inhibition, so two near-collinear inputs that share a dense
sub-space are written into DISJOINT sparse supports → orthogonalized → they no longer
collide at recall. This is the genuine pattern-separation CAPABILITY a dense store lacks
(Sahay et al 2011 Nature — DG inhibition & pattern separation; Stefanelli et al 2016
Neuron — engram size set by inhibition; Olshausen & Field 1996 sparse coding; Fiete et al
2008 grid-cell sparse codes). Inside CLS, GABA gates the FAST store's per-episode cell
budget: SPARSE = better confusable separation, DENSE = the H_1532 default.

THE LAW UNDER TEST (the H_1541/1543/1544 vs H_1545 fusion law):
  a NT that ADDS a capability the two-store can't do   → 🟢 (ACh-mode, DA-rank, NE-flush)
  a NT that only RE-TUNES an existing operation (a knob) → 🟠 (5-HT-timing: fixed-γ ~half)
HONEST PRIOR (census §rank-6, §3): GABA-as-sparseness is LARGELY a single-store
representation-geometry knob (the H_1527 family) → probably 🟠/🧱 UNLESS adaptive
inhibition (sparsity scaled to LOCAL confusability) carries the MAJORITY over a
best-fixed k. If a best-fixed sparsity captures ≥half the value, the law HOLDS and GABA
is a capacity knob (🟠). Test it cleanly either way (c9, NO tune-to-green).

ARMS (frozen-first):
  GABA-SPARSE         = adaptive inhibition-gated k-winner sparse write: k shrinks (more
                        inhibition, sparser, MORE separation) when local confusability is
                        high, relaxes when low. The 5-HT-style ADAPTIVE arm.
  DENSE               = no inhibition, full-density write (the H_1532 two-store default).
  BEST-FIXED-SPARSITY = the strongest single grid-tuned FIXED k (the law's discriminator —
                        if this captures >=half the GABA-sparse lift, GABA is a knob).
  ABL                 = adaptive inhibition frozen to a CONSTANT k (== best-fixed) → reverts.
  SHUFFLE             = the sparsity SIGNAL (confusability the gate reads) permuted →
                        sparsity applied at meaningless times → collapse.

p7: exact ground truth (the true A->B binding is known); NO LLM judge, NO perplexity, NO
loss term — every read is a no-grad read of substrate state. p8: inference-time write =
the engine's own tick. $0 CPU, 3 seeds, frozen falsifier in H_1546_FREEZE.txt.

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning: grep numpy ⇒ auto-
DIRECTIONAL) — engine §GabaSparse R2 deferred ING. REUSES the H_1532 MemStore machinery
(key_vec / FNV-1a / suppress_retrieval encode-mode) and the H_1533 confusable near-
collinear key construction byte-exact.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1533 / CORE engine_cli) ─
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 16                   # key dim (H_1227 byte-trigram FNV-1a; toy 16, same as H_1532)
MARGIN = 0.05              # frozen lift bar (same as H_1532 / H_1284 / H_1533)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1533) ───────────────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1532)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        tri = bs[i:i + 3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM); v[fnv1a(bs) % DIM] = 1.0; n = 1.0
    return v / n


# ── GABA sparse-coding write transform (the E/I-balance pattern separation) ───
# GABAergic lateral inhibition = k-winner-take-all: keep only the |k| largest-magnitude
# coordinates of the key, zero the rest, renormalize. Two near-collinear keys that share
# a dense sub-space are forced onto DISJOINT sparse supports (different top-k indices) →
# their sparse codes are MORE orthogonal than their dense codes → pattern separation.
# k SMALL = strong inhibition = sparse = max separation; k = DIM = no inhibition = dense.
def sparse_code(x: np.ndarray, k: int) -> np.ndarray:
    """k-winner-take-all sparse code (GABA inhibition). k>=DIM ⇒ identity (dense)."""
    if k >= DIM:
        return x
    if k <= 0:
        k = 1
    idx = np.argsort(-np.abs(x))[:k]          # |k| strongest-driven units survive inhibition
    s = np.zeros_like(x)
    s[idx] = x[idx]
    n = np.linalg.norm(s)
    if n < 1e-9:
        return x
    return s / n


def local_confusability(kv: np.ndarray, recent: list) -> float:
    """The 5-HT-style substrate read the GABA gate uses: how collinear THIS key is to the
    recently-written fast-store keys (max cosine to the last few). HIGH = a confusable
    burst → engage MORE inhibition (sparser k). This is the adaptive signal a fixed k
    cannot use — it is what the law tests (does adapting to it carry the majority?)."""
    if not recent:
        return 0.0
    sims = [float(np.dot(kv, r)) for r in recent]
    return max(sims)


# ── MemStore (VERBATIM from H_1532 — capacity-bounded LRU prototype store) ────
class MemStore:
    def __init__(self, max_cells, abstain_margin, LR, THRESH):
        self.protos = []
        self.values = []
        self.lru = []
        self.max_cells = max_cells
        self.abstain_margin = abstain_margin
        self.LR = LR
        self.THRESH = THRESH
        self.tick = 0

    def _nearest(self, x):
        if not self.protos:
            return -1, 1e9, 1e9
        d = [np.linalg.norm(p - x) for p in self.protos]
        order = np.argsort(d)
        win = int(order[0]); bestd = d[win]
        second = d[int(order[1])] if len(d) > 1 else 1e9
        return win, bestd, second

    def write(self, x, value, suppress_retrieval=False):
        """vadapt_field_step write (VERBATIM H_1532). suppress_retrieval = Hasselmo ACh
        encode-mode: lay a fact in a FRESH cell instead of refining the winner."""
        self.tick += 1
        win, err, _ = self._nearest(x)
        if suppress_retrieval and len(self.protos) < self.max_cells:
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if win < 0 or (err > self.THRESH and len(self.protos) < self.max_cells):
            self.protos.append(x.copy()); self.values.append(value)
            self.lru.append(self.tick)
            return
        if err > self.THRESH and len(self.protos) >= self.max_cells:
            ev = int(np.argmin(self.lru))
            self.protos[ev] = x.copy(); self.values[ev] = value
            self.lru[ev] = self.tick
            return
        # REFINE: pull winner toward x, OVERWRITE its bound value (= interference)
        self.protos[win] = self.protos[win] + self.LR * (x - self.protos[win])
        self.values[win] = value
        self.lru[win] = self.tick

    def recall(self, x):
        self.tick += 1
        win, err, second = self._nearest(x)
        if win < 0 or err > self.abstain_margin:
            return None, err, second
        self.lru[win] = self.tick
        return self.values[win], err, second


# ── CONFUSABLE near-collinear AB-AC fixture (H_1533 key geometry × H_1532 task) ─
# Each cluster shares an anchor direction; members are near-collinear (cos ~0.97-0.99,
# the genuine collision regime). Each member is an A_i key with an OLD value B_i (encoded
# into the fast store) and a later interfering value C_i (routed to the slow store). The
# CAPABILITY = retain A_i->B_i after the confusable A_i->C_i re-bindings — a regime the
# DENSE fast store cannot separate (near-collinear A_i collide in the fast geometry).
def make_confusable_abac(n_anchors, n_per_cluster, rng, pert_sigma=0.045):
    A, B, C = [], [], []
    for a in range(n_anchors):
        anchor = key_vec(f"anchor{a:03d}_subject")
        for m in range(n_per_cluster):
            pert = rng.normal(0, pert_sigma, DIM)
            k = anchor + pert
            k = k / (np.linalg.norm(k) + 1e-9)
            A.append(k)
            B.append(f"val_B{rng.integers(0, 99999):05d}")
            c = f"val_C{rng.integers(0, 99999):05d}"
            while c == B[-1]:
                c = f"val_C{rng.integers(0, 99999):05d}"
            C.append(c)
    return A, B, C


def confusability(A):
    K = np.array(A)
    G = K @ K.T
    np.fill_diagonal(G, -1.0)
    return float(np.mean(np.max(G, axis=1)))


# ── two-store CLS with GABA-gated sparse fast-store write ─────────────────────
def run_cls_gaba(A, B, C, max_cells_fast, max_cells_slow, LR, THRESH, abstain,
                 mode, k_fixed=None, conf_lo=0.90, conf_hi=0.98, k_sparse=4,
                 ablate_const=False, shuffle_sparsity=False, rng=None):
    """One pass over the confusable AB-AC stream with a fast-store WRITE-sparsity policy.

    fast = FAST episodic store (Hasselmo encode-mode): A->B bindings encode here, each
           passed through the GABA sparse_code transform BEFORE the write (and the same
           transform is applied to the RECALL query — the store geometry is the sparse
           code). slow = SLOW store: A->C interfering re-bindings (dense, H_1532 default).

    mode:
      'dense'    : k = DIM (no inhibition) — the H_1532 two-store default fast write.
      'adaptive' : GABA — k scaled by LOCAL confusability: a confusable burst (high cos
                   to recent fast keys) engages MORE inhibition (k = k_sparse, sparser,
                   max separation); an isolated key relaxes (k = DIM, dense). The signal
                   a fixed k cannot use.
      'fixed'    : a single grid-tuned FIXED k (best-fixed-sparsity — the law discriminator).
    ablate_const=True : adaptive frozen to a CONSTANT k (== best-fixed) → reverts.
    shuffle_sparsity=True : the confusability SIGNAL the gate reads is permuted → inhibition
                   engages at meaningless keys → sparsity decoupled from collision → collapse.
    """
    fast = MemStore(max_cells_fast, abstain, LR, THRESH)
    slow = MemStore(max_cells_slow, abstain, LR, THRESH)

    fake_conf_seq = None
    if shuffle_sparsity and rng is not None:
        fake_conf_seq = rng.uniform(conf_lo - 0.05, conf_hi + 0.05, size=len(A)).tolist()

    recent = []                                   # recently-written RAW fast keys (for the gate)

    def choose_k(kv, i):
        if mode == 'dense':
            return DIM
        if mode == 'fixed':
            return k_fixed
        # adaptive (GABA)
        if ablate_const:
            return k_fixed                        # ablation: ignore confusability, const k
        conf = fake_conf_seq[i] if shuffle_sparsity else local_confusability(kv, recent[-6:])
        if conf >= conf_hi:
            return k_sparse                       # dense collision → strong inhibition (sparse)
        if conf <= conf_lo:
            return DIM                            # isolated → no inhibition (dense)
        # graded between
        frac = (conf - conf_lo) / (conf_hi - conf_lo)
        return int(round(DIM - frac * (DIM - k_sparse)))

    # store the sparsity-code FUNCTION used per fast cell so recall uses the SAME geometry.
    fast_codes = []                               # parallel to fast.protos: the k each used
    # phase 1: A->B into FAST episodic store, GABA-sparse encode-mode
    for i, (a, b) in enumerate(zip(A, B)):
        k = choose_k(a, i)
        sc = sparse_code(a, k)
        # encode-mode fresh-cell write of the SPARSE code
        fast.write(sc, b, suppress_retrieval=True)
        fast_codes.append(k)
        recent.append(a)
    # phase 2: A->C interfering re-bindings into the SLOW store (dense, H_1532 default)
    for a, c in zip(A, C):
        slow.write(a, c, suppress_retrieval=False)

    return _score_two(fast, slow, fast_codes, A, B, mode, k_fixed, conf_lo, conf_hi,
                      k_sparse, ablate_const)


def _score_two(fast, slow, fast_codes, A, B, mode, k_fixed, conf_lo, conf_hi,
               k_sparse, ablate_const):
    """A->B retained if EITHER store still returns B. The fast store holds the SPARSE code,
    so the recall query must be sparse-coded the SAME way (pattern separation only helps if
    query and store share the geometry). The slow store holds the dense A->C, so it returns
    the wrong (C) value for A — only the SEPARATED fast code recovers B."""
    correct = 0
    for i, (a, b) in enumerate(zip(A, B)):
        # query the fast store in its sparse geometry (use the per-cell code k)
        kf = fast_codes[i] if i < len(fast_codes) else DIM
        qf = sparse_code(a, kf)
        pf, _, _ = fast.recall(qf)
        ps, _, _ = slow.recall(a)
        if pf == b or ps == b:
            correct += 1
    return correct / max(1, len(A))


def grid_tune_fixed_k(n_anchors, n_per_cluster, tune_seed, mcf, mcs, LR, THRESH, abstain):
    """BEST-FIXED-SPARSITY: the strongest single FIXED k over a grid on a DISJOINT tune
    seed (anti-confound — adaptive GABA must beat the best honest fixed sparsity, NOT a
    strawman). Returns best AND worst fixed k (for the earned-majority gap, bar B)."""
    rng = np.random.default_rng(tune_seed)
    A, B, C = make_confusable_abac(n_anchors, n_per_cluster, rng)
    results = {}
    for k in (1, 2, 3, 4, 6, 8, 12, DIM):
        r = run_cls_gaba(A, B, C, mcf, mcs, LR, THRESH, abstain, mode='fixed', k_fixed=k)
        results[k] = r
    best_k = max(results, key=results.get)
    worst_k = min(results, key=results.get)
    return best_k, results[best_k], worst_k, results[worst_k], results


def main():
    N_ANCHORS = 12
    N_PER_CLUSTER = 5            # 60 confusable near-collinear AB-AC pairs (H_1533 geometry)
    ABSTAIN0 = 0.45
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    K_SPARSE = 4                 # the sparse (strong-inhibition) k the adaptive arm engages
    CONF_LO, CONF_HI = 0.90, 0.98
    MAX_CELLS_FAST = 256         # ample fast capacity (separation, not capacity, is the test)
    MAX_CELLS_SLOW = 256
    LR_star, TH_star = LR0_ENGINE, TH0_ENGINE

    # grid-tune the best-fixed-k baseline on a DISJOINT seed
    best_k, best_k_tune, worst_k, worst_k_tune, k_grid = \
        grid_tune_fixed_k(N_ANCHORS, N_PER_CLUSTER, TUNE_SEED, MAX_CELLS_FAST,
                          MAX_CELLS_SLOW, LR_star, TH_star, ABSTAIN0)

    rows = []
    confs = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        A, B, C = make_confusable_abac(N_ANCHORS, N_PER_CLUSTER, rng)
        confs.append(confusability(A))
        gaba = run_cls_gaba(A, B, C, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                            ABSTAIN0, mode='adaptive', k_sparse=K_SPARSE,
                            conf_lo=CONF_LO, conf_hi=CONF_HI)
        dense = run_cls_gaba(A, B, C, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                             ABSTAIN0, mode='dense')
        fixed_best = run_cls_gaba(A, B, C, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                                  ABSTAIN0, mode='fixed', k_fixed=best_k)
        worst_fixed = run_cls_gaba(A, B, C, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                                   ABSTAIN0, mode='fixed', k_fixed=worst_k)
        # bar-C ablation: adaptive sparsity frozen to a CONSTANT k (best-fixed)
        abl = run_cls_gaba(A, B, C, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                           ABSTAIN0, mode='adaptive', k_sparse=K_SPARSE,
                           conf_lo=CONF_LO, conf_hi=CONF_HI,
                           k_fixed=best_k, ablate_const=True)
        # bar-D shuffle: confusability SIGNAL permuted → inhibition at meaningless keys
        shf = run_cls_gaba(A, B, C, MAX_CELLS_FAST, MAX_CELLS_SLOW, LR_star, TH_star,
                           ABSTAIN0, mode='adaptive', k_sparse=K_SPARSE,
                           conf_lo=CONF_LO, conf_hi=CONF_HI,
                           shuffle_sparsity=True, rng=np.random.default_rng(seed + 1000))
        rows.append({'seed': seed,
                     'gaba_sparse': round(gaba, 4),
                     'dense': round(dense, 4),
                     'fixed_best_k': round(fixed_best, 4),
                     'worst_fixed_k': round(worst_fixed, 4),
                     'abl_const': round(abl, 4),
                     'shuffle': round(shf, 4),
                     'gaba_minus_dense': round(gaba - dense, 4),
                     'gaba_minus_best_fixed': round(gaba - fixed_best, 4)})

    def m(key):
        return float(np.mean([r[key] for r in rows]))
    ga_m = m('gaba_sparse'); de_m = m('dense'); bf_m = m('fixed_best_k')
    wf_m = m('worst_fixed_k'); abl_m = m('abl_const'); shf_m = m('shuffle')

    # ── FROZEN falsifier (pre-registered in H_1546_FREEZE.txt) ────────────────
    #   A PRESENCE        : GABA-sparse − dense ≥ +MARGIN on ≥2/3 seeds AND in mean
    #                       (sparse coding ADDS confusable-recall the dense store lacks)
    #   B EARNED-MAJORITY : GABA-sparse − best-fixed-k ≥ 0.5×(GABA-sparse − worst-fixed-k)
    #                       (the 5-HT-style law bar: ADAPTIVE inhibition must carry the
    #                       MAJORITY of the value, not a minority a fixed k already has —
    #                       if a best-fixed k captures ≥half, GABA is a CAPACITY KNOB → 🟠)
    #   C ABL→fixed       : const-k ablation reverts toward best-fixed
    #                       (gaba − abl ≥ MARGIN  AND  |abl − best-fixed| < MARGIN)
    #   D SHUFFLE         : permuted-confusability sparsity collapses (gaba − shuffle ≥ MARGIN)
    #   E NO-FAB          : best-fixed-k itself is a real working baseline (> 0)
    seed_wins = sum(1 for r in rows if r['gaba_minus_dense'] >= MARGIN)
    presence = (seed_wins >= 2) and ((ga_m - de_m) >= MARGIN)
    full_gap = ga_m - wf_m
    earned_majority = ((ga_m - bf_m) >= 0.5 * full_gap) and (full_gap > 0)
    abl_reverts = ((ga_m - abl_m) >= MARGIN) and (abs(abl_m - bf_m) < MARGIN)
    shuffle_collapses = (ga_m - shf_m) >= MARGIN
    no_fab = bf_m > 0.0

    if presence and earned_majority and abl_reverts and shuffle_collapses and no_fab:
        verdict = 'GREEN'      # GABA adds ADAPTIVE pattern-separation (capability, not knob)
    elif presence and no_fab and not earned_majority:
        # PRESENT (sparse separation real) but a best-fixed k captures >=half → CAPACITY KNOB
        verdict = 'AMBER'      # the LAW HOLDS: GABA is a re-tuning knob, not a new capability
    else:
        verdict = 'WALL_HOLDS'  # sparse coding ties dense → no separation lever at all

    frac_adaptive = (100 * (ga_m - bf_m) / full_gap) if full_gap > 0 else float('nan')
    # which side of the fusion law this lands
    if verdict == 'GREEN':
        law_side = 'ADDS-CAPABILITY (🟢, like ACh/DA/NE) — adaptive pattern-separation is majority'
    elif verdict == 'AMBER':
        law_side = 'RE-TUNES-KNOB (🟠, like 5-HT) — best-fixed sparsity captures ≥half; law HOLDS'
    else:
        law_side = 'INERT — sparse coding does not separate confusable bindings here'

    summary = {
        'hypothesis': 'H_1546',
        'name': 'GABA × CLS — inhibitory E/I-balance gating of fast-store effective capacity',
        'capability': 'AB-AC retention on a CONFUSABLE near-collinear key set via GABA-gated sparse fast-store write',
        'cites': ['Sahay et al 2011 Nature 472:466 (DG inhibition & pattern separation)',
                  'Stefanelli et al 2016 Neuron 89:1074 (engram size set by inhibition)',
                  'Olshausen & Field 1996 Nature 381:607 (sparse coding)',
                  'Fiete et al 2008 (sparse grid codes)',
                  'H_1533 (confusable regime the dense store fails)'],
        'LR_star': LR_star, 'TH_star': TH_star,
        'N_ANCHORS': N_ANCHORS, 'N_PER_CLUSTER': N_PER_CLUSTER,
        'n_facts': N_ANCHORS * N_PER_CLUSTER,
        'mean_max_offdiag_cos': round(float(np.mean(confs)), 4),
        'K_SPARSE': K_SPARSE, 'conf_lo': CONF_LO, 'conf_hi': CONF_HI, 'DIM': DIM,
        'MAX_CELLS_FAST': MAX_CELLS_FAST, 'MAX_CELLS_SLOW': MAX_CELLS_SLOW,
        'MARGIN': MARGIN, 'seeds': SCORE_SEEDS,
        'best_fixed_k': best_k, 'worst_fixed_k': worst_k,
        'k_grid_tune': {str(k): round(v, 4) for k, v in k_grid.items()},
        'per_seed': rows,
        'gaba_sparse_mean': round(ga_m, 4),
        'dense_mean': round(de_m, 4),
        'fixed_best_k_mean': round(bf_m, 4),
        'worst_fixed_k_mean': round(wf_m, 4),
        'abl_const_mean': round(abl_m, 4),
        'shuffle_mean': round(shf_m, 4),
        'gaba_minus_dense_mean': round(ga_m - de_m, 4),
        'gaba_minus_best_fixed_mean': round(ga_m - bf_m, 4),
        'gaba_minus_worst_fixed_mean': round(full_gap, 4),
        'gaba_carries_pct_of_gap': round(frac_adaptive, 1),
        'seed_wins_over_dense+MARGIN': seed_wins,
        'A_presence': bool(presence),
        'B_earned_majority': bool(earned_majority),
        'C_abl_reverts': bool(abl_reverts),
        'D_shuffle_collapses': bool(shuffle_collapses),
        'E_no_fab': bool(no_fab),
        'verdict': verdict,
        'law_side': law_side,
        'directional': True,
        'note': 'numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning); engine §GabaSparse R2 '
                'deferred ING; reuses H_1532 MemStore/key_vec/encode-mode + H_1533 confusable '
                'key geometry byte-exact; bars frozen-first (NO tune-to-green)',
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
