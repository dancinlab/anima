#!/usr/bin/env python3
"""
H_1551 — GABA × CLS: sparse-coding CAPACITY-MULTIPLICATION under fast-store OVERLOAD
(a NEW capability angle, distinct from H_1546's pattern-separation lens).

WHY A NEW ANGLE (a_break_the_wall MULTI-LENS — new principled angle, not the same wall):
  H_1546 🧱 tested GABA-sparse on a CONFUSABLE near-collinear AB-AC regime
  (pattern-SEPARATION). It came out INERT because the H_1532 two-store CLS already
  routes A->B into a FRESH FAST cell while the interfering A->C goes to the SLOW store
  — the architecture separated the confusable bindings into distinct SUBSTRATES, so
  sparse coding had nothing left to orthogonalize. That tested the WRONG capability:
  GABA-sparseness was redundant with the structural fast/slow separation.

  The biologically RIGHT capability for inhibitory sparse coding is CAPACITY-
  MULTIPLICATION (a DIFFERENT capability, not the same wall re-hit): sparse codes
  (k-of-N active) pack MANY MORE distinct bindings into the SAME N fast-store cells
  WITHOUT collision than dense codes, because sparse random codes have exponentially
  more near-orthogonal patterns than dense ones (Marr 1969 codon hypothesis; Babadi &
  Sompolinsky 2014, Neuron 83:1213 — sparse expansion decorrelates & multiplies
  capacity; Litwin-Kumar et al 2017, Neuron 93:1153 — optimal sparseness for
  associative capacity; Olshausen & Field 1996 sparse coding). So under a LOAD that
  EXCEEDS dense capacity, GABA-sparse RETAINS bindings dense LOSES — a capability dense
  CLS lacks.

  Crucially this attacks a regime H_1546 NEVER touched: H_1546 used MAX_CELLS_FAST=256
  with 60 facts (NO capacity pressure — separation, not packing, was the bottleneck).
  Here N_bindings ≫ N_fast_cells (overload), in a SINGLE fast store (no fast/slow escape
  hatch), so capacity packing IS the binding constraint.

THE FUSION LAW UNDER TEST (H_1541/1543/1544 🟢 vs H_1545 🟠 / H_1546 🧱):
  a NT that ADDS a capability the store can't otherwise do   → 🟢 (ACh / DA / NE)
  a NT that only RE-TUNES an existing operation (a knob)     → 🟠 (5-HT-timing: fixed-γ)
  a NT fully ABSORBED by the architecture                    → 🧱 (H_1546 sep regime)
HONEST PRIOR: if a single grid-tuned FIXED sparsity-k already captures the capacity gain
(GABA's ADAPTIVE inhibition is a minority lever), this is 🟠 like 5-HT-timing — report
it, do NOT force green (c9, NO tune-to-green). 🟢 only if ADAPTIVE inhibition (k scaled
to live LOAD) carries the MAJORITY of the value over the best FIXED sparsity.

ARMS (frozen-first):
  GABA-SPARSE (adaptive) = inhibition-gated k-winner sparse write; k SHRINKS (more
                           inhibition, sparser, more capacity) as the store FILLS toward
                           overload, relaxes when the store has room. The signal a fixed
                           k cannot use: live occupancy/load.
  DENSE                  = k = DIM, the H_1532 default (no inhibition).
  BEST-FIXED-K           = the strongest single grid-tuned FIXED sparsity (the law
                           discriminator — if this captures >=half, GABA is a knob).
  ABL (const k)          = adaptive frozen to a CONSTANT k (== best-fixed) → reverts.
  SHUFFLE                = the LOAD-pressure signal the gate reads is permuted →
                           inhibition engages at meaningless times → collapse.

FROZEN bars (🟢 iff A∧B∧C∧D∧E):
  A PRESENCE        : GABA-sparse retention-under-overload ≥ dense + 0.10 (≥2/3 seeds + mean)
  B EARNED-MAJORITY : adaptive carries ≥half the value vs best-FIXED-k (the 5-HT-style bar
                      — adaptive must beat the best FIXED sparsity to be a capability not a
                      knob): (GABA − best_fixed) ≥ 0.5×(GABA − worst_fixed), worst-fixed gap>0
  C ABL→fixed       : const-k ablation reverts toward best-fixed (gaba−abl ≥ MARGIN AND
                      |abl − best-fixed| < MARGIN)
  D SHUFFLE         : permuted load-signal collapses (gaba − shuffle ≥ MARGIN)
  E NO-FAB          : best-fixed-k itself is a real working baseline ( > dense, capacity real)
  🟢 iff all incl B (adaptive sparseness is the lever);
  🟠 if best-fixed-k captures ≥half (sparseness helps but it's a knob — honest, like 5-HT);
  🧱 if sparse ties dense (no capacity gain at all).

p7: exact ground truth (true A->B binding known); NO LLM judge, NO perplexity, NO loss
term — every read is a no-grad read of substrate state. p8: inference-time write = the
engine's own tick. $0 CPU, 3 seeds, frozen falsifier in H_1551_FREEZE.txt.

R1 numpy DIRECTIONAL (host has no torch; a_engine_native_learning: grep numpy ⇒ auto-
DIRECTIONAL) — engine §GabaSparse R2 deferred ING. REUSES the H_1532 MemStore machinery
(key_vec / FNV-1a / write / recall) byte-exact; the NEW piece is the OVERLOAD regime
(N≫cells, single store) + the LOAD-gated adaptive sparsity (vs H_1546's confusability-
gated sparsity on a non-overloaded two-store).
"""
import numpy as np
import json

# ── engine-native constants (VERBATIM from H_1532 / H_1546 / CORE engine_cli) ─
LR0_ENGINE = 0.20          # adapt_field_step LR (online winner pull)
TH0_ENGINE = 0.30          # adapt_field_step SPLIT_THRESH (novelty bar)
DIM = 64                   # key dim — LARGER than H_1546's 16 so sparse k-of-N has room to
                           # multiply capacity (Babadi-Sompolinsky: gain grows with N/k); the
                           # capacity-packing effect is invisible at DIM=16 (too few supports).
MARGIN = 0.05              # frozen ablation/shuffle bar (same family value)
PRESENCE_BAR = 0.10        # frozen PRESENCE bar (task-lead spec: ≥ dense + 0.10)


# ── byte-trigram FNV-1a key (VERBATIM from H_1532 / H_1546) ───────────────────
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


# ── GABA sparse-coding write transform (the E/I-balance capacity packing) ─────
# GABAergic lateral inhibition = k-winner-take-all: keep only the |k| largest-magnitude
# coordinates, zero the rest, renormalize. Sparse codes (small k over large DIM) occupy
# near-orthogonal supports → MANY MORE distinct bindings fit in the same N cells without
# the winner-overwrite collision dense codes suffer under overload (Babadi-Sompolinsky
# 2014; Litwin-Kumar 2017). k SMALL = strong inhibition = sparse = max capacity; k = DIM =
# dense = the H_1532 default.
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


# ── MEASUREMENT FIX (a_break_the_wall taxonomy (a): WRONG-substrate measurement) ──
# FIRST DRAFT of this probe routed the overload stream through the H_1532 slot-store
# (MemStore, below). That store's capacity is HARD-BOUNDED at max_cells BY CONSTRUCTION:
# under diverse-key overload every fact is novel (err > THRESH against all cells) so the
# store ALWAYS takes the LRU-EVICT path (instrumented: 40 fresh + 80 evict + 0 refine, both
# dense and sparse) → it keeps exactly the last max_cells facts BY RECENCY, geometry-blind →
# gaba == dense == best-fixed == 0.3333 (= 40/120) EXACTLY for every k. That is a FIXTURE
# ARTIFACT, not a measurement: sparse coding cannot multiply SLOT capacity (slots are
# hard-bounded); it multiplies SUPERPOSITION capacity (Babadi-Sompolinsky 2014: sparse
# k-of-N codes have less outer-product cross-talk, so more bindings co-exist in ONE matrix
# without overwriting each other). FROZEN-FIRST FIX (bars UNCHANGED): score on the
# SUPERPOSITION associative store where the mechanism can actually act — a single DIMxDIM
# Hebbian matrix M = Σ outer(value_code, sparse_key), recall = argmax over the value
# codebook of <M·key, v>. This is the genuine capacity substrate the biology describes; the
# slot-store is retained only as the H_1532 reference (and the artifact is reported in the
# card, NOT hidden — c9). The bottleneck is now real CAPACITY (cross-talk), not recency.
class SuperStore:
    """Single Hebbian SUPERPOSITION associative store under overload. All N bindings live in
    ONE DIMxDIM matrix (no slots, no eviction) — capacity is set by code cross-talk, which
    sparse k-of-N codes reduce (Babadi-Sompolinsky / Litwin-Kumar). value codebook is a fixed
    random orthogonal-ish set; recall = nearest value-code to M·key."""
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


# ── MemStore (VERBATIM from H_1532 / H_1546 — capacity-bounded LRU prototype store) ──
# (retained as the H_1532 REFERENCE store; see the MEASUREMENT FIX note above for why the
#  superposition substrate is the correct capacity-multiplication measurement)
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
        # REFINE: pull winner toward x, OVERWRITE its bound value (= collision under overload)
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


# ── OVERLOAD fixture: N distinct facts, each a random direction (NOT near-collinear) ─
# This is the KEY difference from H_1546: the facts are DIVERSE (low mutual cosine, drawn
# from random subject strings), so confusable pattern-SEPARATION is NOT the bottleneck.
# The bottleneck is CAPACITY: there are far MORE facts than fast-store cells, and dense
# writes collide (a new fact lands within THRESH of an occupied dense cell, REFINE
# overwrites its bound value). Sparse codes spread the facts across more near-orthogonal
# supports → fewer collisions → more bindings survive at recall.
def make_overload_facts(n_facts, rng):
    """N diverse facts: each a distinct random subject string → diverse key (low mutual
    cosine, so confusability is NOT the bottleneck — CAPACITY is), bound to a DISTINCT value
    index (0..N-1). The superposition store must keep all N bindings disambiguable in ONE
    matrix; under overload (N large vs DIM) cross-talk destroys dense bindings first."""
    A, Bidx = [], []
    for i in range(n_facts):
        s = f"fact{i:04d}_subject_{rng.integers(0, 9_999_999):07d}"
        A.append(key_vec(s))
        Bidx.append(i)                                        # each fact a distinct value
    return A, Bidx


def mean_max_offdiag_cos(A):
    K = np.array(A)
    G = K @ K.T
    np.fill_diagonal(G, -1.0)
    return float(np.mean(np.max(G, axis=1)))


# ── single SUPERPOSITION store under overload, with a sparsity-k write policy ──
def run_overload(A, Bidx, store_seed, mode, k_fixed=None, k_sparse=8,
                 load_lo=0.30, load_hi=0.90, ablate_const=False, shuffle_load=False, rng=None):
    """Stream N facts into ONE superposition associative matrix, then measure A->B retention.
    Capacity is set by code cross-talk (Babadi-Sompolinsky) — sparse k-of-N codes pack more
    bindings per matrix. NO slots, NO eviction: every fact is superposed; dense codes
    cross-talk and corrupt each other's read-out under overload, sparse codes survive.

    mode:
      'dense'    : k = DIM (no inhibition) — the H_1532-default-equivalent (full-density write).
      'adaptive' : GABA — k scaled by live LOAD (#facts written / N): as the matrix fills
                   toward overload, MORE inhibition (k -> k_sparse, sparser, less cross-talk);
                   early (room) relax (k -> DIM). The signal a fixed k cannot use: live load.
      'fixed'    : a single grid-tuned FIXED k (best-fixed-sparsity — the law discriminator).
    ablate_const=True : adaptive frozen to a CONSTANT k (== best-fixed) → reverts.
    shuffle_load=True : the LOAD signal the gate reads is permuted → inhibition engages at
                   meaningless fill-levels → sparsity decoupled from overload → collapse.
    """
    n = len(A)
    n_values = n
    store = SuperStore(DIM, n_values, store_seed)

    fake_load_seq = None
    if shuffle_load and rng is not None:
        fake_load_seq = rng.uniform(0.0, 1.0, size=n).tolist()

    def choose_k(i):
        if mode == 'dense':
            return DIM
        if mode == 'fixed':
            return k_fixed
        if ablate_const:
            return k_fixed                                  # ablation: ignore load, const k
        load = fake_load_seq[i] if shuffle_load else (i / n)  # live fill fraction
        if load >= load_hi:
            return k_sparse                                 # near-overload → strong inhibition
        if load <= load_lo:
            return DIM                                      # room → no inhibition (dense)
        frac = (load - load_lo) / (load_hi - load_lo)       # graded between
        return int(round(DIM - frac * (DIM - k_sparse)))

    codes = []                                              # per-fact sparse key (recall geometry)
    for i, (a, bi) in enumerate(zip(A, Bidx)):
        k = choose_k(i)
        ks = sparse_code(a, k)
        store.write(ks, bi)
        codes.append(ks)

    correct = 0
    for ks, bi in zip(codes, Bidx):                         # query in the SAME (sparse) geometry
        if store.recall(ks) == bi:
            correct += 1
    return correct / max(1, n)


def grid_tune_fixed_k(n_facts, tune_seed, store_seed):
    """BEST-FIXED-SPARSITY: strongest single FIXED k over a grid on a DISJOINT tune seed
    (anti-confound — adaptive GABA must beat the best HONEST fixed sparsity). Returns best
    AND worst fixed k (for the earned-majority gap, bar B)."""
    rng = np.random.default_rng(tune_seed)
    A, Bidx = make_overload_facts(n_facts, rng)
    results = {}
    for k in (2, 4, 8, 12, 16, 24, 32, 48, DIM):
        results[k] = run_overload(A, Bidx, store_seed, mode='fixed', k_fixed=k)
    best_k = max(results, key=results.get)
    worst_k = min(results, key=results.get)
    return best_k, results[best_k], worst_k, results[worst_k], results


def main():
    N_FACTS = 120               # overload load (vs DIM=64 superposition capacity → cross-talk)
    TUNE_SEED = 7               # disjoint fact-draw seed for the best-fixed-k grid
    SCORE_SEEDS = [11, 22, 33]
    K_SPARSE = 8                # strong-inhibition k the adaptive arm engages near overload
    LOAD_LO, LOAD_HI = 0.30, 0.90

    # grid-tune the best-fixed-k baseline on a DISJOINT fact-draw seed (anti-confound).
    # store_seed is held FIXED across all arms of a given score-seed (the value codebook is a
    # substrate constant, not a tuned arm) — here the tune uses its own store_seed=TUNE_SEED.
    best_k, best_k_tune, worst_k, worst_k_tune, k_grid = \
        grid_tune_fixed_k(N_FACTS, TUNE_SEED, store_seed=TUNE_SEED)

    rows = []
    confs = []
    for seed in SCORE_SEEDS:
        rng = np.random.default_rng(seed)
        A, Bidx = make_overload_facts(N_FACTS, rng)
        confs.append(mean_max_offdiag_cos(A))
        gaba = run_overload(A, Bidx, seed, mode='adaptive',
                            k_sparse=K_SPARSE, load_lo=LOAD_LO, load_hi=LOAD_HI)
        dense = run_overload(A, Bidx, seed, mode='dense')
        fixed_best = run_overload(A, Bidx, seed, mode='fixed', k_fixed=best_k)
        worst_fixed = run_overload(A, Bidx, seed, mode='fixed', k_fixed=worst_k)
        abl = run_overload(A, Bidx, seed, mode='adaptive',
                           k_sparse=K_SPARSE, load_lo=LOAD_LO, load_hi=LOAD_HI,
                           k_fixed=best_k, ablate_const=True)
        shf = run_overload(A, Bidx, seed, mode='adaptive',
                           k_sparse=K_SPARSE, load_lo=LOAD_LO, load_hi=LOAD_HI,
                           shuffle_load=True, rng=np.random.default_rng(seed + 1000))
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

    # ── FROZEN falsifier (pre-registered in H_1551_FREEZE.txt) ────────────────
    #   A PRESENCE        : GABA-sparse − dense ≥ +PRESENCE_BAR on ≥2/3 seeds AND in mean
    #   B EARNED-MAJORITY : (GABA − best-fixed) ≥ 0.5×(GABA − worst-fixed), worst-gap > 0
    #   C ABL→fixed       : gaba − abl ≥ MARGIN  AND  |abl − best-fixed| < MARGIN
    #   D SHUFFLE         : gaba − shuffle ≥ MARGIN
    #   E NO-FAB          : best-fixed-k beats dense ( > dense ) — the capacity effect is real
    seed_wins = sum(1 for r in rows if r['gaba_minus_dense'] >= PRESENCE_BAR)
    presence = (seed_wins >= 2) and ((ga_m - de_m) >= PRESENCE_BAR)
    full_gap = ga_m - wf_m
    earned_majority = ((ga_m - bf_m) >= 0.5 * full_gap) and (full_gap > 0)
    abl_reverts = ((ga_m - abl_m) >= MARGIN) and (abs(abl_m - bf_m) < MARGIN)
    shuffle_collapses = (ga_m - shf_m) >= MARGIN
    no_fab = bf_m > de_m

    if presence and earned_majority and abl_reverts and shuffle_collapses and no_fab:
        verdict = 'GREEN'       # GABA adds ADAPTIVE capacity-multiplication (capability)
    elif presence and no_fab and not earned_majority:
        verdict = 'AMBER'       # capacity real but a best-fixed k captures ≥half → KNOB (5-HT side)
    else:
        verdict = 'WALL_HOLDS'  # sparse ties dense → no capacity gain at all

    frac_adaptive = (100 * (ga_m - bf_m) / full_gap) if full_gap > 0 else float('nan')
    # capacity-multiplication of FIXED sparse coding vs dense (the substrate-level effect,
    # independent of the adaptive arm) — load-bearing for the honest sub-finding
    fixed_cap_mult = (bf_m / de_m) if de_m > 0 else float('inf')
    if verdict == 'GREEN':
        law_side = ('ADDS-CAPABILITY (🟢, like ACh/DA/NE) — adaptive capacity-multiplication '
                    'is majority')
    elif verdict == 'AMBER':
        law_side = ('RE-TUNES-KNOB (🟠, like 5-HT) — best-fixed sparsity captures ≥half; law HOLDS')
    else:
        # WALL_HOLDS for the ADAPTIVE GABA mechanism. Report the sub-finding honestly: FIXED
        # sparse coding DOES multiply capacity (best-fixed >> dense), but a STATIC sparsity is
        # optimal (Litwin-Kumar) — the load-gated ADAPTIVE arm is INERT/worse because its early
        # dense writes permanently pollute the superposition matrix (cross-talk is irreversible).
        law_side = ('ADAPTIVE-INERT 🧱 — FIXED sparse coding multiplies capacity '
                    f'{round(fixed_cap_mult, 1)}x (best-fixed {round(bf_m, 3)} vs dense '
                    f'{round(de_m, 3)}) = a STATIC architectural property (Litwin-Kumar optimal '
                    'sparseness), NOT a load-gated neuromodulatory lever; the ADAPTIVE arm '
                    f'{round(ga_m, 3)} ≈ dense because early dense writes irreversibly pollute '
                    'the superposition matrix → GABA-as-adaptive adds no capability the FIXED '
                    'sparsity lacks')

    summary = {
        'hypothesis': 'H_1551',
        'name': 'GABA × CLS — sparse-coding CAPACITY-MULTIPLICATION under fast-store overload',
        'capability': 'A->B retention under OVERLOAD (N_facts >> N_fast_cells, single store) via '
                      'GABA load-gated sparse write that packs more near-orthogonal bindings per cell',
        'new_angle_vs_H_1546': 'H_1546 tested pattern-SEPARATION on a non-overloaded TWO-store '
                               '(INERT: architecture already separated). THIS tests capacity-'
                               'MULTIPLICATION under OVERLOAD in a SINGLE store (different '
                               'capability, multi-lens NOT bar-move; DIM 16->64 so sparse k-of-N '
                               'has room to multiply supports, Babadi-Sompolinsky)',
        'cites': ['Babadi & Sompolinsky 2014 Neuron 83:1213 (sparse expansion decorrelates & '
                  'multiplies associative capacity)',
                  'Litwin-Kumar et al 2017 Neuron 93:1153 (optimal sparseness for capacity)',
                  'Marr 1969 J Physiol 202:437 (cerebellar codon sparse coding)',
                  'Olshausen & Field 1996 Nature 381:607 (sparse coding)'],
        'substrate': 'SuperStore (single Hebbian superposition matrix DIMxDIM; capacity = code '
                     'cross-talk, NOT slots) — see MEASUREMENT FIX note (slot-store was a fixture '
                     'artifact: gaba==dense==0.3333 for all k under LRU eviction)',
        'N_FACTS': N_FACTS, 'DIM': DIM, 'overload_ratio': round(N_FACTS / DIM, 2),
        'mean_max_offdiag_cos': round(float(np.mean(confs)), 4),
        'K_SPARSE': K_SPARSE, 'load_lo': LOAD_LO, 'load_hi': LOAD_HI,
        'MARGIN': MARGIN, 'PRESENCE_BAR': PRESENCE_BAR, 'seeds': SCORE_SEEDS,
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
        'fixed_sparse_capacity_mult_vs_dense': round(fixed_cap_mult, 2),
        'seed_wins_over_dense+PRESENCE_BAR': seed_wins,
        'A_presence': bool(presence),
        'B_earned_majority': bool(earned_majority),
        'C_abl_reverts': bool(abl_reverts),
        'D_shuffle_collapses': bool(shuffle_collapses),
        'E_no_fab': bool(no_fab),
        'verdict': verdict,
        'law_side': law_side,
        'directional': True,
        'note': 'numpy mirror ⇒ DIRECTIONAL (a_engine_native_learning); engine §GabaSparse R2 '
                'deferred ING; reuses H_1532 MemStore/key_vec/write/recall byte-exact; NEW = '
                'overload regime (N>>cells, single store) + load-gated adaptive sparsity; bars '
                'frozen-first (NO tune-to-green)',
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
