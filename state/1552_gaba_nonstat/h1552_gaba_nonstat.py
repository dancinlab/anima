#!/usr/bin/env python3
"""
H_1552 — GABA × CLS: adaptive sparseness under NON-STATIONARY load
(the FINAL, principled GABA lens — the one regime where adaptive can HONESTLY beat fixed).

WHY THIS IS THE LEGITIMATE LAST GABA LENS (a_break_the_wall MULTI-LENS class-d, NOT fishing):
  GABA-as-adaptive walled TWICE on STATIONARY regimes:
    H_1546 🧱  — pattern-SEPARATION (confusable AB-AC, non-overload two-store). INERT
                 because the CLS architecture already separated the bindings.
    H_1551 🧱  — capacity-MULTIPLICATION under STATIONARY overload (N≫DIM, single super-
                 position store, constant arrival rate). ADAPTIVE-INERT: a single best-
                 FIXED-k (k=4) captures the whole capacity gain (14.6x vs dense); the
                 load-gated adaptive arm is inert/worse because under a STATIONARY load
                 ONE fixed sparsity is optimal (Litwin-Kumar 2017 optimal-sparseness) and
                 the adaptive arm's early dense writes irreversibly pollute the matrix.

  THE FUSION LAW (proven across the 6 NTs fused — ACh/DA/NE/orexin/5-HT 🟢/🟠 vs the GABA
  walls): a neuromodulator's ADAPTIVE lever beats a grid-tuned FIXED setting ONLY where the
  OPTIMAL OPERATING POINT SHIFTS over time. orexin (H_1550 🟢) and 5-HT (H_1549 🟢) earned
  their honest green precisely because the optimum SHIFTED. H_1551 used a STATIONARY overload
  → one fixed-k is optimal everywhere → adaptive correctly inert (honest 🧱).

  The UNTESTED regime — and the ONLY one where adaptive sparseness can genuinely earn its
  keep — is NON-STATIONARY load: the binding-arrival RATE VARIES over the stream, ALTERNATING
  LIGHT phases (few near-simultaneous writes → low cross-talk → DENSE / large-k is best for
  read-out FIDELITY) with HEAVY phases (many writes → high cross-talk → HIGH sparsity / small-k
  needed to avoid collision). Under non-stationary load NO single fixed-k is optimal:
    • the LIGHT-optimal large k OVERFLOWS (collides) in the heavy phases, and
    • the HEAVY-optimal small k WASTES fidelity (over-sparsifies) in the light phases.
  So a GABA-gated adaptive-k that tracks the CURRENT local load should beat the best single
  fixed-k. This is the SAME shifting-optimum principle that gave orexin/5-HT their honest
  green, applied to GABA — a PRINCIPLED DISTINCT lens, NOT a post-hoc bar move.

  HONEST (c9): if the best fixed-k STILL captures it on the non-stationary stream, that IS the
  scientific answer — GABA is a STATIC architectural parameter, not an adaptive faculty, and
  this is the 3rd DECISIVE lens confirming a class-(d) no-free-lunch ceiling for GABA-as-NT.
  We pre-register the bars BEFORE the scored run and report whichever side honestly. NO
  tune-to-green: the presence bar measures the ADAPTIVE arm vs the best-fixed-k baseline.

THE SHIFTING-OPTIMUM PHYSICS (why a fixed k cannot win here):
  In a single Hebbian SUPERPOSITION matrix M = Σ outer(value_code, key), the read-out SNR for a
  stored binding is a trade-off in the write-code density:
    • DENSE codes (large k) → high per-binding READ FIDELITY (the key carries full information),
      but the outer-product CROSS-TALK between codes grows → under MANY co-resident bindings
      (heavy phase) the bindings overwrite each other.
    • SPARSE codes (small k) → low cross-talk (near-orthogonal supports) → many bindings co-exist,
      but each binding's read-out is dimmer (less of the matrix carries it) → under FEW bindings
      (light phase) sparse needlessly throws away fidelity that dense would have kept.
  Hence the optimal k is HIGH in light phases and LOW in heavy phases — it SHIFTS with the local
  arrival rate. A single fixed k must compromise; adaptive-k that reads the live local load wins.

ARMS (frozen-first — exactly mirrors H_1551's arm family, applied to the non-stationary stream):
  GABA-ADAPTIVE-K = k = f(current local load pressure): k SHRINKS toward K_SPARSE in heavy
                    phases (more inhibition, sparser), RELAXES toward DIM in light phases. The
                    signal a fixed k cannot use: the live local arrival rate.
  BEST-FIXED-K    = the strongest single grid-tuned FIXED k over the WHOLE non-stationary stream
                    (the honest strong baseline / law discriminator). Disjoint tune seed.
  DENSE           = k = DIM (no inhibition).
  ABL (const k)   = adaptive frozen to a CONSTANT k == best-fixed → reverts (proves the LEVER is
                    the load-gating, not the sparse write per se).
  SHUFFLE         = the per-segment load-pressure signal PERMUTED vs the TRUE phase order → the
                    gate sparsifies at the WRONG times (sparse in light, dense in heavy) →
                    collapse (proves it tracks the TRUE phase, not just the mean k).

FROZEN bars (🟢 iff A∧B∧C∧D∧E — IDENTICAL family to H_1551, on the non-stationary stream):
  A PRESENCE        : GABA-adaptive-k − best-fixed-k ≥ +0.10 on the non-stationary stream
                      (≥2/3 seeds AND in mean) — the strong test: adaptive must beat the best
                      FIXED k (not merely dense), because non-stationarity is supposed to break
                      fixed-k. (This is STRICTER than H_1551's presence-vs-dense.)
  B EARNED-MAJORITY : adaptive carries ≥ half the (adaptive − worst-fixed) gap:
                      (gaba − best_fixed) ≥ 0.5×(gaba − worst_fixed), worst-fixed-gap > 0.
  C ABL→fixed       : const-k ablation reverts toward best-fixed (gaba − abl ≥ MARGIN AND
                      |abl − best-fixed| < MARGIN).
  D SHUFFLE         : permuted load-phase signal collapses (gaba − shuffle ≥ MARGIN) — proves
                      adaptive tracks the TRUE phase, not just its mean k.
  E NO-FAB          : best-fixed-k itself is a real working baseline ( > dense ) — capacity real.
  🟢 iff all incl A∧B → adaptive sparseness is load-bearing UNDER NON-STATIONARITY (GABA is a
                        genuine adaptive faculty in the shifting-optimum regime);
  🟠 if A∧E∧¬B          → adaptive helps but best-fixed-k captures ≥half (knob, like 5-HT);
  🧱 if ¬A              → best-fixed-k STILL captures it = GABA is a STATIC architectural
                        parameter, NOT an adaptive faculty — the 3rd DECISIVE lens = confirmed
                        class-(d) no-free-lunch ceiling for GABA-as-NT.

p7: exact ground truth (true binding known); NO LLM judge, NO perplexity, NO loss term — every
read is a no-grad read of substrate state. p8: inference-time write = the engine's own tick.
$0 CPU, 3 seeds, frozen falsifier in H_1552_FREEZE.txt.

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning: grep numpy ⇒ auto-
DIRECTIONAL) — engine §GabaSparse R2 deferred ING. REUSES the H_1551 SuperStore / sparse_code /
key_vec / FNV-1a machinery byte-exact; the NEW piece is the NON-STATIONARY ALTERNATING-load
stream (vs H_1551's STATIONARY constant-rate overload) + the LOCAL-load-gated adaptive sparsity.
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1546 / H_1551 / CORE engine_cli) ─
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 64                   # key dim (VERBATIM H_1551 — sparse k-of-N has room to multiply supports)
MARGIN = 0.05              # frozen ablation/shuffle bar (same family value)
PRESENCE_BAR = 0.10        # frozen PRESENCE bar (≥ best-fixed-k + 0.10 on non-stationary stream)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1546 / H_1551) ──────────
def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (VERBATIM from H_1532/H_1551)."""
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


# ── GABA sparse-coding write transform (VERBATIM from H_1551) ─────────────────
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


# ── SuperStore (VERBATIM from H_1551 — single Hebbian superposition matrix) ───
class SuperStore:
    """Single Hebbian SUPERPOSITION associative store. All bindings live in ONE DIMxDIM matrix
    (no slots, no eviction) — capacity is set by code cross-talk, which sparse k-of-N codes
    reduce (Babadi-Sompolinsky / Litwin-Kumar). value codebook = fixed random orthogonal-ish
    set; recall = nearest value-code to M·key."""
    def __init__(self, dim, n_values, seed):
        rng = np.random.default_rng(seed + 777)
        self.Vcode = rng.standard_normal((n_values, dim))
        self.Vcode /= (np.linalg.norm(self.Vcode, axis=1, keepdims=True) + 1e-9)
        self.M = np.zeros((dim, dim))

    def write(self, key, value_idx):
        self.M += np.outer(self.Vcode[value_idx], key)        # Hebbian outer-product bind

    def recall(self, key):
        out = self.M @ key
        return int(np.argmax(self.Vcode @ out))               # nearest value code (no-grad read)


# ── NON-STATIONARY ALTERNATING-LOAD stream (the NEW piece vs H_1551) ──────────
# The stream is built from N_SEG segments that ALTERNATE between LIGHT phases (few facts,
# RATE_LO arrivals → the local matrix is lightly loaded → cross-talk low → DENSE/large-k best
# for read fidelity) and HEAVY phases (many facts, RATE_HI arrivals → local matrix heavily
# loaded → cross-talk high → SPARSE/small-k needed to avoid collision). Each fact is a DIVERSE
# random subject (low mutual cosine, so confusability is NOT the bottleneck — LOAD is), bound to
# a DISTINCT value index. We record, per fact, the segment's TRUE local load pressure (a scalar
# in [0,1]) so the adaptive arm can read it (and the SHUFFLE arm can permute it).
def make_nonstationary_stream(n_seg, rate_lo, rate_hi, rng):
    """Build an alternating LIGHT/HEAVY non-stationary stream. Returns (A keys, Bidx values,
    load_pressure per fact, seg_id per fact). Segment s is LIGHT (rate_lo) if s even, HEAVY
    (rate_hi) if s odd. load_pressure = rate normalized to [0,1] across {rate_lo, rate_hi}."""
    A, Bidx, load, seg = [], [], [], []
    fid = 0
    for s in range(n_seg):
        heavy = (s % 2 == 1)
        rate = rate_hi if heavy else rate_lo
        pressure = 1.0 if heavy else 0.0      # TRUE local load pressure (binary phase)
        for _ in range(rate):
            sub = f"fact{fid:04d}_subject_{rng.integers(0, 9_999_999):07d}"
            A.append(key_vec(sub))
            Bidx.append(fid)
            load.append(pressure)
            seg.append(s)
            fid += 1
    return A, Bidx, load, seg


def mean_max_offdiag_cos(A):
    K = np.array(A)
    G = K @ K.T
    np.fill_diagonal(G, -1.0)
    return float(np.mean(np.max(G, axis=1)))


# ── single SUPERPOSITION store under the NON-STATIONARY stream, with a sparsity-k policy ──
def run_nonstationary(A, Bidx, load, store_seed, mode, k_fixed=None, k_sparse=8, k_light=None,
                      ablate_const=False, shuffle_load=False, rng=None):
    """Stream the NON-STATIONARY facts into ONE superposition matrix, then measure binding
    retention. The optimal k SHIFTS by phase (large in LIGHT, small in HEAVY); a fixed k must
    compromise. 'load[i]' is the TRUE local phase pressure (0 light / 1 heavy).

    mode:
      'dense'    : k = DIM everywhere (no inhibition).
      'fixed'    : a single FIXED k (best-fixed-k baseline — the law discriminator).
      'adaptive' : GABA — k tracks the LIVE LOCAL load: k=k_light (relax/dense-ish) in light
                   phases, k=k_sparse (strong inhibition) in heavy phases. The signal a fixed
                   k cannot use: the live local arrival rate.
    ablate_const=True : adaptive frozen to a CONSTANT k (== best-fixed) → reverts.
    shuffle_load=True : the per-fact load signal PERMUTED vs the TRUE phase order → sparsity
                   engages at the WRONG phase → collapse (proves it tracks the TRUE phase).
    """
    n = len(A)
    n_values = n
    store = SuperStore(DIM, n_values, store_seed)
    if k_light is None:
        k_light = DIM

    load_seq = load
    if shuffle_load and rng is not None:
        load_seq = list(load)
        rng.shuffle(load_seq)                                 # permute phase signal vs true order

    def choose_k(i):
        if mode == 'dense':
            return DIM
        if mode == 'fixed':
            return k_fixed
        if ablate_const:
            return k_fixed                                    # ablation: ignore load, const k
        # adaptive: HEAVY phase (pressure 1) → strong inhibition (k_sparse);
        #           LIGHT phase (pressure 0) → relax (k_light, near-dense for fidelity)
        return k_sparse if load_seq[i] >= 0.5 else k_light

    codes = []
    for i, (a, bi) in enumerate(zip(A, Bidx)):
        k = choose_k(i)
        ks = sparse_code(a, k)
        store.write(ks, bi)
        codes.append(ks)

    correct = 0
    for ks, bi in zip(codes, Bidx):                           # query in the SAME (sparse) geometry
        if store.recall(ks) == bi:
            correct += 1
    return correct / max(1, n)


def grid_tune_fixed_k(n_seg, rate_lo, rate_hi, tune_seed, store_seed):
    """BEST-FIXED-K: strongest single FIXED k over a grid on a DISJOINT tune-seed non-stationary
    stream (anti-confound — adaptive GABA must beat the best HONEST fixed k on the SAME kind of
    non-stationary stream). Returns best AND worst fixed k (for the earned-majority gap, bar B).
    The honest strong baseline: this fixed k already sees the WHOLE stream and picks its single
    best compromise."""
    rng = np.random.default_rng(tune_seed)
    A, Bidx, load, _seg = make_nonstationary_stream(n_seg, rate_lo, rate_hi, rng)
    results = {}
    for k in (2, 4, 8, 12, 16, 24, 32, 48, DIM):
        results[k] = run_nonstationary(A, Bidx, load, store_seed, mode='fixed', k_fixed=k)
    best_k = max(results, key=results.get)
    worst_k = min(results, key=results.get)
    return best_k, results[best_k], worst_k, results[worst_k], results


def main():
    # NON-STATIONARY stream params (frozen). 4 LIGHT + 4 HEAVY alternating segments.
    N_SEG = 8                   # 4 light (even) + 4 heavy (odd) alternating
    RATE_LO = 6                 # LIGHT phase arrivals (few → low cross-talk → dense best)
    RATE_HI = 24                # HEAVY phase arrivals (many → high cross-talk → sparse best)
    #   total facts = 4*6 + 4*24 = 120 (matches H_1551 load), but NON-STATIONARILY distributed.
    TUNE_SEED = 7               # disjoint fact-draw seed for the best-fixed-k grid
    SCORE_SEEDS = [11, 22, 33]
    K_SPARSE = 8                # strong-inhibition k the adaptive arm engages in HEAVY phases
    K_LIGHT = DIM               # relaxed (dense) k the adaptive arm engages in LIGHT phases

    # grid-tune the best-fixed-k baseline on a DISJOINT non-stationary stream (anti-confound).
    best_k, best_k_tune, worst_k, worst_k_tune, k_grid = \
        grid_tune_fixed_k(N_SEG, RATE_LO, RATE_HI, TUNE_SEED, store_seed=TUNE_SEED)

    rows = []
    confs = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        A, Bidx, load, seg = make_nonstationary_stream(N_SEG, RATE_LO, RATE_HI, rng)
        confs.append(mean_max_offdiag_cos(A))
        gaba = run_nonstationary(A, Bidx, load, seed, mode='adaptive',
                                 k_sparse=K_SPARSE, k_light=K_LIGHT)
        dense = run_nonstationary(A, Bidx, load, seed, mode='dense')
        fixed_best = run_nonstationary(A, Bidx, load, seed, mode='fixed', k_fixed=best_k)
        worst_fixed = run_nonstationary(A, Bidx, load, seed, mode='fixed', k_fixed=worst_k)
        abl = run_nonstationary(A, Bidx, load, seed, mode='adaptive',
                                k_sparse=K_SPARSE, k_light=K_LIGHT,
                                k_fixed=best_k, ablate_const=True)
        shf = run_nonstationary(A, Bidx, load, seed, mode='adaptive',
                                k_sparse=K_SPARSE, k_light=K_LIGHT,
                                shuffle_load=True, rng=np.random.default_rng(seed + 1000))
        rows.append({'seed': seed,
                     'gaba_adaptive_k': round(gaba, 4),
                     'dense': round(dense, 4),
                     'fixed_best_k': round(fixed_best, 4),
                     'worst_fixed_k': round(worst_fixed, 4),
                     'abl_const': round(abl, 4),
                     'shuffle': round(shf, 4),
                     'gaba_minus_best_fixed': round(gaba - fixed_best, 4),
                     'gaba_minus_dense': round(gaba - dense, 4)})

    def m(key):
        return float(np.mean([r[key] for r in rows]))
    ga_m = m('gaba_adaptive_k'); de_m = m('dense'); bf_m = m('fixed_best_k')
    wf_m = m('worst_fixed_k'); abl_m = m('abl_const'); shf_m = m('shuffle')

    # ── FROZEN falsifier (pre-registered in H_1552_FREEZE.txt) ────────────────
    #   A PRESENCE        : GABA-adaptive-k − BEST-FIXED-k ≥ +PRESENCE_BAR (≥2/3 seeds AND mean)
    #   B EARNED-MAJORITY : (GABA − best-fixed) ≥ 0.5×(GABA − worst-fixed), worst-gap > 0
    #   C ABL→fixed       : gaba − abl ≥ MARGIN  AND  |abl − best-fixed| < MARGIN
    #   D SHUFFLE         : gaba − shuffle ≥ MARGIN
    #   E NO-FAB          : best-fixed-k > dense (the capacity effect is genuinely real)
    seed_wins = sum(1 for r in rows if r['gaba_minus_best_fixed'] >= PRESENCE_BAR)
    presence = (seed_wins >= 2) and ((ga_m - bf_m) >= PRESENCE_BAR)
    full_gap = ga_m - wf_m
    earned_majority = ((ga_m - bf_m) >= 0.5 * full_gap) and (full_gap > 0)
    abl_reverts = ((ga_m - abl_m) >= MARGIN) and (abs(abl_m - bf_m) < MARGIN)
    shuffle_collapses = (ga_m - shf_m) >= MARGIN
    no_fab = bf_m > de_m

    if presence and earned_majority and abl_reverts and shuffle_collapses and no_fab:
        verdict = 'GREEN'       # adaptive sparseness is the lever UNDER NON-STATIONARITY
    elif presence and no_fab and not earned_majority:
        verdict = 'AMBER'       # adaptive helps but best-fixed captures ≥half → KNOB (5-HT side)
    else:
        verdict = 'WALL_HOLDS'  # best-fixed-k STILL captures it → GABA = static architecture

    frac_adaptive = (100 * (ga_m - bf_m) / full_gap) if full_gap > 0 else float('nan')
    fixed_cap_mult = (bf_m / de_m) if de_m > 0 else float('inf')
    if verdict == 'GREEN':
        law_side = ('ADAPTIVE-FACULTY (🟢, like orexin/5-HT shifting-optimum) — under NON-'
                    'STATIONARY load the optimum k SHIFTS by phase, so adaptive-k beats the best '
                    'single fixed-k by the MAJORITY; GABA IS a genuine adaptive faculty here')
    elif verdict == 'AMBER':
        law_side = ('RE-TUNES-KNOB (🟠, like 5-HT) — adaptive helps under non-stationarity but '
                    'best-fixed-k captures ≥half; law HOLDS')
    else:
        law_side = ('STATIC-ARCHITECTURE 🧱 — best-fixed-k STILL captures it EVEN under NON-'
                    f'STATIONARY load (gaba {round(ga_m, 3)} vs best-fixed {round(bf_m, 3)}, '
                    f'Δ {round(ga_m - bf_m, 3)} < {PRESENCE_BAR}); GABA is a STATIC architectural '
                    'parameter (Litwin-Kumar optimal-sparseness), NOT an adaptive faculty — the '
                    '3rd DECISIVE lens (after H_1546 separation, H_1551 stationary-capacity) = '
                    'confirmed class-(d) no-free-lunch ceiling for GABA-as-NT')

    summary = {
        'hypothesis': 'H_1552',
        'name': 'GABA × CLS — adaptive sparseness under NON-STATIONARY load',
        'capability': 'binding retention across an ALTERNATING light/heavy non-stationary stream '
                      'via GABA local-load-gated adaptive sparse write (k tracks the current phase '
                      'arrival rate) — the regime where NO single fixed-k is optimal',
        'new_angle_vs_H_1551': 'H_1546/H_1551 tested STATIONARY regimes (one fixed-k optimal → '
                               'adaptive inert). THIS tests the shifting-optimum regime: NON-'
                               'STATIONARY alternating load, where light phases favor dense/large-k '
                               '(fidelity) and heavy phases favor sparse/small-k (anti-collision), '
                               'so no single fixed-k is optimal. The SAME fusion-law shifting-'
                               'optimum condition that gave orexin/5-HT their honest green, applied '
                               'to GABA (multi-lens, NOT bar-move)',
        'cites': ['Litwin-Kumar et al 2017 Neuron 93:1153 (optimal sparseness depends on LOAD — '
                  'under varying load the optimal sparseness must vary)',
                  'Babadi & Sompolinsky 2014 Neuron 83:1213 (sparse expansion decorrelates & '
                  'multiplies associative capacity)',
                  'Marr 1969 J Physiol 202:437 (cerebellar codon sparse coding)',
                  'Olshausen & Field 1996 Nature 381:607 (sparse coding)'],
        'substrate': 'SuperStore (single Hebbian superposition matrix DIMxDIM; capacity = code '
                     'cross-talk) — VERBATIM from H_1551',
        'N_SEG': N_SEG, 'RATE_LO': RATE_LO, 'RATE_HI': RATE_HI,
        'N_FACTS': 4 * RATE_LO + 4 * RATE_HI, 'DIM': DIM,
        'mean_max_offdiag_cos': round(float(np.mean(confs)), 4),
        'K_SPARSE': K_SPARSE, 'K_LIGHT': K_LIGHT,
        'MARGIN': MARGIN, 'PRESENCE_BAR': PRESENCE_BAR, 'seeds': SCORE_SEEDS,
        'best_fixed_k': best_k, 'worst_fixed_k': worst_k,
        'k_grid_tune': {str(k): round(v, 4) for k, v in k_grid.items()},
        'per_seed': rows,
        'gaba_adaptive_k_mean': round(ga_m, 4),
        'dense_mean': round(de_m, 4),
        'fixed_best_k_mean': round(bf_m, 4),
        'worst_fixed_k_mean': round(wf_m, 4),
        'abl_const_mean': round(abl_m, 4),
        'shuffle_mean': round(shf_m, 4),
        'gaba_minus_best_fixed_mean': round(ga_m - bf_m, 4),
        'gaba_minus_dense_mean': round(ga_m - de_m, 4),
        'gaba_minus_worst_fixed_mean': round(full_gap, 4),
        'gaba_carries_pct_of_gap': round(frac_adaptive, 1),
        'fixed_sparse_capacity_mult_vs_dense': round(fixed_cap_mult, 2),
        'seed_wins_over_best_fixed+PRESENCE_BAR': seed_wins,
        'A_presence': bool(presence),
        'B_earned_majority': bool(earned_majority),
        'C_abl_reverts': bool(abl_reverts),
        'D_shuffle_collapses': bool(shuffle_collapses),
        'E_no_fab': bool(no_fab),
        'verdict': verdict,
        'law_side': law_side,
        'directional': True,
        'note': 'numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning); engine §GabaSparse R2 '
                'deferred ING; reuses H_1551 SuperStore/sparse_code/key_vec byte-exact; NEW = '
                'NON-STATIONARY alternating-load stream + local-load-gated adaptive sparsity; '
                'bars frozen-first (NO tune-to-green); A presence measures adaptive vs BEST-FIXED '
                '(stricter than H_1551 vs dense) — the shifting-optimum test',
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
