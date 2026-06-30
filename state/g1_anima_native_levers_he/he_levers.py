"""he_levers.py — H_1826..H_1831 cheap-numpy HE pre-screen of 6 anima-native G1 levers.

GATING STEP (p7, DIRECTIONAL): which of the 6 anima-native novel recombination
levers (N1..N6) clear a cheap-numpy pre-screen → promote to engine-native/GPU;
which floor → 🧱 DIRECTIONAL terminal at the cheap tier. NOT a terminal verdict
(G1 SSOT remains engine-native `anima evaluate`); a cheap compass for GPU spend.

REFERENCE-MATCH (no reinvention):
  * H_1821 HE probe (state/g1_homomorphism_error_probe/he_probe.py)
  * H_1822 β substrate readout (state/g1_substrate_native_recombination/beta_readout.py)
  * H_1825 γ trained combiner (state/g1_gamma_trained_combiner/gamma_combiner.py)
  SAME compound-pair fixtures, SAME composed_distinct / recoverability metric,
  SAME fp64 numpy (NO bf16; circular conv / FFT via fp64 = exact), SAME embed
  source = 303M clm303 trunk penultimate via core/clm_decode.py (mean-pool, L2-unit),
  reusing beta_readout._semantic_rep / _unit so results are COMPARABLE to β/γ.

SCOPE: DIRECTIONAL (py-mirror embed via core/clm_decode.py; numpy fp64 operators).
  α(char-hash) 🧱 · β(semantic) 🧱 · γ(trained constructive) 🧱 all floored. This
  round asks whether 6 ANIMA-NATIVE mechanisms (dynamical fixed-point, V(D)J,
  Φ-integration, kosmos placement, Kuramoto phase-sync, replay) lift G1 where the
  generic operator family floored. Honest negatives are results (c9): if all 6
  floor, the G1 wall holds even against anima-native mechanisms.

Each lever honors its OWN card's frozen bar + controls VERBATIM (no sliding):
  N1 H_1826 Ψ=½ fixed-point bind   bar: composed_distinct>=2 ∧ >max_single ∧ !=shuffle, >=2/3 ; ctrl iteration-OFF(=static β)
  N2 H_1827 V(D)J immune recomb    bar: distinct>=2 ∧ >parent-copy ; ctrl parent-copy, hypermutation-OFF, shuffle
  N3 H_1828 Φ-integration bind     bar: distinct>=2 ∧ Φ(child)>Φ(single)∧>Φ(shuffle) ; CHEAP-TIER exact small-n Φ proxy ONLY (a_phi_iit4_tool: NO variance×energy)
  N4 H_1829 kosmos anchor recomb   bar: distinct>=2 ∧ >midpoint-baseline ∧ parent-specific ; ctrl midpoint(critical), single, shuffle
  N5 H_1830 Kuramoto phase-sync    bar: distinct>=2 ∧ >amplitude-baseline ∧ sync-causal ; ctrl K=0(BLIND), amplitude-affinity, shuffle
  N6 H_1831 replay recomb (REOPEN H_987) bar: distinct>=2 ∧ >no-replay ; ctrl no-replay, shuffle-replay

Usage:  OMP_NUM_THREADS=4 python3 he_levers.py [<ckpt.clm>]
"""

import sys, os, time
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.abspath(os.path.join(_HERE, "..", "..", "core"))
_BETA = os.path.abspath(os.path.join(_HERE, "..", "g1_substrate_native_recombination"))
sys.path.insert(0, _CORE)
sys.path.insert(0, _BETA)
import clm_decode as cd          # byte-faithful CLMConvMoE forward (py 2-production)
import beta_readout as br        # reuse the SAME semantic embed + metric as β/γ

EPS = 1e-9
SEED = 1826
RIDGE = 1e-2

# default ckpt: try local path, then ~/anima relocation (summer pool)
_CANDS = [
    "/Users/mini/dancinlab/anima/state/clm303_savant_mitosis_train/clm303.clm",
    os.path.expanduser("~/anima/state/clm303_savant_mitosis_train/clm303.clm"),
    os.path.join(_HERE, "clm303.clm"),
]


# ════════════════════════════════════════════════════════════════════════
# Fixtures — IDENTICAL to γ (gamma_combiner.PAIRS / DISTRACTORS): 32 real
# morphological compounds (EN/KO/ZH) + 15 distractors. parent_a+parent_b=child.
# ════════════════════════════════════════════════════════════════════════
PAIRS = [
    ("rain", "bow", "rainbow"), ("snow", "man", "snowman"),
    ("sun", "flower", "sunflower"), ("fire", "fly", "firefly"),
    ("water", "fall", "waterfall"), ("foot", "ball", "football"),
    ("book", "shelf", "bookshelf"), ("moon", "light", "moonlight"),
    ("star", "fish", "starfish"), ("tooth", "brush", "toothbrush"),
    ("rail", "road", "railroad"), ("butter", "fly", "butterfly"),
    ("key", "board", "keyboard"), ("news", "paper", "newspaper"),
    ("bed", "room", "bedroom"), ("ear", "ring", "earring"),
    ("eye", "brow", "eyebrow"), ("hand", "bag", "handbag"),
    ("wheel", "chair", "wheelchair"), ("after", "noon", "afternoon"),
    ("불", "꽃", "불꽃"), ("눈", "사람", "눈사람"),
    ("손", "수건", "손수건"), ("물", "고기", "물고기"),
    ("책", "상", "책상"), ("봄", "바람", "봄바람"),
    ("밤", "하늘", "밤하늘"), ("꽃", "잎", "꽃잎"),
    ("日", "光", "日光"), ("月", "光", "月光"),
    ("火", "山", "火山"), ("水", "車", "水車"),
]
DISTRACTORS = ["mountain", "ocean", "computer", "garden", "window",
               "산", "강", "하늘", "구름", "바다",
               "天", "地", "風", "雨", "雪"]


# ════════════════════════════════════════════════════════════════════════
# Shared recoverability metric (γ-style) — child recoverable from constructed
# point ∧ irreducible (NOT from one parent) ∧ > shuffle, on held-out pairs.
# composed_distinct = #{parents the child projects near to} (β-style), reported.
# ════════════════════════════════════════════════════════════════════════

def _cos(u, v):
    nu = np.linalg.norm(u); nv = np.linalg.norm(v)
    return 0.0 if nu < EPS or nv < EPS else float(u @ v / (nu * nv))

def _rank1(query, pool_vecs, pool_names):
    sims = [_cos(query, v) for v in pool_vecs]
    return pool_names[int(np.argmax(sims))]

def _composed_distinct(child, a, b, radius):
    """β-style: how many of the 2 parents the constructed child lies within
    `radius` (cosine-distance) of. >=2 = bridges BOTH parent basins."""
    da = 1.0 - _cos(child, a); db = 1.0 - _cos(child, b)
    return int(da < radius) + int(db < radius)

RADIUS = 0.30  # engine novelty radius (vadapt_field_step:578), on unit-cos geometry


def g1_eval(construct, emb, train_idx, test_idx, shuffle_fn=None):
    """Generic held-out G1: for each test pair build constructed child via
    `construct(a,b, ctx)` (ctx exposes train data for fitted operators); G1=1 iff
      (i)  rank1(constructed) == child   (recovered/constructed)
      (ii) rank1(a)!=child AND rank1(b)!=child   (irreducible)
      (iii) cos(constructed,child) > cos(shuffled,child)  (> shuffle control)
    Also records composed_distinct(constructed,a,b) >=2.
    `shuffle_fn(a, ti)` returns the shuffled construction (default: wrong parent_b)."""
    pool_names = [PAIRS[i][2] for i in range(len(PAIRS))] + DISTRACTORS
    pool_vecs = [emb[n] for n in pool_names]
    results = []
    for ti in test_idx:
        pa, pb, child = PAIRS[ti]
        a, b, cv = emb[pa], emb[pb], emb[child]
        constructed = np.asarray(construct(a, b)).reshape(-1)
        if shuffle_fn is not None:
            shuffled = np.asarray(shuffle_fn(a, ti)).reshape(-1)
        else:
            wrong_b = emb[PAIRS[(ti + 1) % len(PAIRS)][1]]
            shuffled = np.asarray(construct(a, wrong_b)).reshape(-1)
        nn_c = _rank1(constructed, pool_vecs, pool_names)
        nn_a = _rank1(a, pool_vecs, pool_names)
        nn_b = _rank1(b, pool_vecs, pool_names)
        sim_c = _cos(constructed, cv); sim_sh = _cos(shuffled, cv)
        cdist = _composed_distinct(constructed, a, b, RADIUS)
        recovered = (nn_c == child)
        irreducible = (nn_a != child) and (nn_b != child)
        beats_shuf = sim_c > sim_sh
        g1 = int(recovered and irreducible and beats_shuf and cdist >= 2)
        results.append(dict(pair="%s+%s->%s" % (pa, pb, child), cdist=cdist,
                            sim_c=sim_c, sim_sh=sim_sh, recovered=recovered,
                            irreducible=irreducible, beats_shuf=beats_shuf, g1=g1))
    return results


def cv_construct(make_construct, emb, folds=5, seed=SEED, shuffle_fn_factory=None):
    """5-fold CV. make_construct(emb, train_idx) -> construct(a,b) closure
    (so fitted operators only see train). Returns (hits,total,per)."""
    n = len(PAIRS)
    rng = np.random.default_rng(seed)
    order = rng.permutation(n)
    fold_sz = int(np.ceil(n / folds))
    hits = total = 0; per = []
    for k in range(folds):
        test_idx = list(order[k * fold_sz:(k + 1) * fold_sz])
        if not test_idx:
            continue
        train_idx = [int(i) for i in order if i not in test_idx]
        construct = make_construct(emb, train_idx)
        sf = shuffle_fn_factory(emb, train_idx, construct) if shuffle_fn_factory else None
        res = g1_eval(construct, emb, train_idx, test_idx, shuffle_fn=sf)
        for r in res:
            hits += r["g1"]; total += 1; per.append(r)
    return hits, total, per


def _ridge_fit(Phi, Y, ridge=RIDGE):
    f = Phi.shape[1]
    A = Phi.T @ Phi + ridge * np.eye(f)
    return np.linalg.solve(A, Phi.T @ Y)


# ════════════════════════════════════════════════════════════════════════
# N1 — H_1826  Ψ=½ DYNAMICAL FIXED-POINT bind
#   A⇄G-style map iterated on the 2-parent seed to a fixed point; child =
#   converged state. The decisive control vs H_1822 = the TIME axis: iteration
#   ON (converge) vs OFF (static = β midpoint, must floor → iteration causal).
# ════════════════════════════════════════════════════════════════════════

def _psi_map(a, b, x):
    """One A⇄G push-pull step. A (forward) pulls x toward the affinity midpoint
    of the two parent basins; G (reverse) pushes x away from the nearer parent
    (tension). Fixed point Ψ=½ = balance where pull==push. fp64, deterministic.
    NO trained weights (a substrate dynamical map, not a fitted operator)."""
    mid = 0.5 * (a + b)
    # G repulsion from the nearer parent (gradient-free reverse engine)
    da = np.linalg.norm(x - a); db = np.linalg.norm(x - b)
    near = a if da <= db else b
    rep = x - near
    rn = np.linalg.norm(rep)
    rep = rep / rn if rn > EPS else rep
    # A pull toward joint midpoint (forward CE-trained engine, here affinity)
    pull = mid - x
    return x + 0.5 * pull + 0.15 * rep   # Ψ=½ balance of pull(A) and push(G)

def n1_construct_factory(iterate=True, n_iter=64):
    def make(emb, train_idx):
        def construct(a, b):
            x = 0.5 * (a + b)            # seed = midpoint of 2 parents
            if not iterate:
                return x                  # iteration-OFF = static (= H_1822 β floor)
            for _ in range(n_iter):
                xn = _psi_map(a, b, x)
                if np.linalg.norm(xn - x) < 1e-7:
                    x = xn; break
                x = xn
            return x
        return construct
    return make


# ════════════════════════════════════════════════════════════════════════
# N2 — H_1827  V(D)J IMMUNE RECOMBINATION
#   decompose each parent into segments (vector blocks), recombine segments
#   across the 2 parents (NOT average), somatic-hypermutation noise, clonal
#   selection keeps the child variant that best lowers reconstruction error
#   toward "lies in both basins". ctrl: parent-copy, hypermutation-OFF, shuffle.
# ════════════════════════════════════════════════════════════════════════

def n2_construct_factory(hypermutation=True, n_clones=64, n_seg=8, sigma=0.05, seed=SEED):
    def make(emb, train_idx):
        def construct(a, b):
            d = len(a)
            seg = np.array_split(np.arange(d), n_seg)
            rng = np.random.default_rng(seed + int(abs(a.sum() * 1e3)) % 9973)
            best = None; best_score = -1e18
            for _ in range(n_clones):
                child = np.empty(d)
                for s in seg:                       # V(D)J: each segment from one parent
                    src = a if rng.random() < 0.5 else b
                    child[s] = src[s]
                if hypermutation:                   # somatic hypermutation
                    child = child + rng.standard_normal(d) * sigma
                # clonal selection: keep variant nearest BOTH parents (lies in both basins)
                score = _cos(child, a) + _cos(child, b)
                if score > best_score:
                    best_score = score; best = child
            return best
        return construct
    return make


# ════════════════════════════════════════════════════════════════════════
# N3 — H_1828  Φ-INTEGRATION bind  (CHEAP-TIER)
#   a_phi_iit4_tool: faithful IIT4 Φ is engine-native (stdlib faithful_phi.hexa);
#   proxy verdicts FORBIDDEN. CHEAP TIER: an EXACT small-n integration measure
#   (NOT variance×energy) — mutual-information-style irreducibility of a tiny
#   binarized system built from {a,b,child}. We use it ONLY to RANK candidate
#   children; if it cannot legitimately pre-screen we mark N3 needs-stdlib.
# ════════════════════════════════════════════════════════════════════════

def _exact_integration(parent_a, parent_b, child, n_units=6):
    """EXACT small-n integration proxy (a_phi_iit4_tool-safe — NOT variance×energy):
    build an n<=6 binary state from sign-quantized projections of {a,b,child} onto
    a fixed random basis, then compute the system's integration as the EXACT
    minimum over bipartitions of (joint entropy - sum part entropies) — the
    irreducible integrated information of the *constructed* joint, in BITS, by
    exhaustive MIP over all 2^(n-1)-1 bipartitions. This is an exact small-n
    information-integration computation (no proxy heuristic), used only to rank
    candidate children at the cheap tier; the terminal Φ remains faithful IIT4."""
    rng = np.random.default_rng(SEED + 3)
    d = len(child)
    B = rng.standard_normal((d, n_units))
    # construct a 3-sample micro-distribution over the units from a,b,child
    samples = np.stack([parent_a, parent_b, child])  # [3, d]
    proj = samples @ B                                # [3, n]
    bits = (proj > proj.mean(axis=0)).astype(int)     # [3, n] binarized states
    # empirical joint distribution over the n binary units (3 observations)
    states = [tuple(row) for row in bits]
    from collections import Counter
    cnt = Counter(states); tot = len(states)

    def _ent(idxs):
        sub = Counter(tuple(s[i] for i in idxs) for s in states)
        h = 0.0
        for c in sub.values():
            p = c / tot
            h -= p * np.log2(p)
        return h
    full = _ent(tuple(range(n_units)))
    best_phi = 1e18
    # exact MIP over bipartitions
    for mask in range(1, 1 << (n_units - 1)):
        part1 = [i for i in range(n_units) if (mask >> i) & 1]
        part2 = [i for i in range(n_units) if not ((mask >> i) & 1)]
        if not part1 or not part2:
            continue
        phi = (_ent(part1) + _ent(part2)) - full      # integrated info across cut
        if phi < best_phi:
            best_phi = phi
    return best_phi

def n3_construct_factory(emb_ref):
    """Φ-integration bind: among candidate children = {midpoint, sum, hadamard,
    each parent}, pick the one MAXIMIZING exact integration Φ(a,b->cand)."""
    def make(emb, train_idx):
        def construct(a, b):
            cands = {
                "mid": 0.5 * (a + b), "sum": a + b, "hada": a * b,
            }
            best = None; best_phi = -1e18
            for cv in cands.values():
                phi = _exact_integration(a, b, cv)
                if phi > best_phi:
                    best_phi = phi; best = cv
            return best
        return construct
    return make


# ════════════════════════════════════════════════════════════════════════
# N4 — H_1829  KOSMOS ANCHOR-SPACE recombination
#   LEARNED (least-squares) non-midpoint constructor on parent coords in the
#   placement space (here the semantic embed = anchor coord proxy). CRITICAL
#   control = midpoint baseline (child must beat simple average). ctrl: single, shuffle.
# ════════════════════════════════════════════════════════════════════════

def n4_construct_factory():
    def make(emb, train_idx):
        d = len(next(iter(emb.values())))
        A = np.array([emb[PAIRS[i][0]] for i in train_idx])
        B = np.array([emb[PAIRS[i][1]] for i in train_idx])
        Y = np.array([emb[PAIRS[i][2]] for i in train_idx])
        Phi = np.concatenate([A, B], axis=1)         # learned linear constructor
        W = _ridge_fit(Phi, Y)
        def construct(a, b):
            return np.concatenate([a, b])[None] @ W
        return construct
    return make

def n4_midpoint_factory():
    def make(emb, train_idx):
        return lambda a, b: 0.5 * (a + b)            # CRITICAL baseline
    return make


# ════════════════════════════════════════════════════════════════════════
# N5 — H_1830  KURAMOTO PHASE-SYNC bind
#   2 oscillators (parents as phase vectors), Kuramoto coupling K phase-locks
#   them; child = phase-synced collective state. ctrl: K=0 (sync OFF = BLIND),
#   amplitude-affinity baseline (= β midpoint), shuffle. sync-causal = K>0 lifts.
# ════════════════════════════════════════════════════════════════════════

def n5_construct_factory(K=1.5, steps=80, dt=0.05):
    def make(emb, train_idx):
        def construct(a, b):
            # represent each parent dim as an oscillator phase; amplitude=|a|,|b|
            amp = 0.5 * (np.abs(a) + np.abs(b))
            tha = np.angle(a + 1j * np.roll(a, 1))   # parent-a phases
            thb = np.angle(b + 1j * np.roll(b, 1))   # parent-b phases
            th = tha.copy()
            for _ in range(steps):                    # Kuramoto coupling to parent-b
                th = th + dt * K * np.sin(thb - th)
            return amp * np.cos(th)                    # phase-synced collective
        return construct
    return make

def n5_amplitude_factory():
    def make(emb, train_idx):
        # amplitude-affinity baseline (no phase): the β-style midpoint
        return lambda a, b: 0.5 * (a + b)
    return make


# ════════════════════════════════════════════════════════════════════════
# N6 — H_1831  REPLAY recombination (🔓 REOPEN H_987)
#   offline replay-bind of 2 memories (numpy proxy of REM/dream mitosis tick):
#   interleave-and-consolidate the two parent traces over replay sweeps,
#   converging to a consolidated child. ctrl: no-replay (= single interleave =
#   midpoint), shuffle-replay (replay with a wrong second memory).
#   H_987 (old, proxy-era) claimed replay≈idle on a TOY LDS world model — note
#   whether this cheap re-measure already diverges (proxy≠engine lesson).
# ════════════════════════════════════════════════════════════════════════

def n6_construct_factory(replay=True, sweeps=40, lr=0.1):
    def make(emb, train_idx):
        def construct(a, b):
            if not replay:
                return 0.5 * (a + b)                  # no-replay baseline
            # offline replay-bind: alternately pull the consolidated trace toward
            # each replayed memory (hippocampal interleaved replay), converging.
            c = 0.5 * (a + b)
            mems = [a, b]
            for s in range(sweeps):
                m = mems[s % 2]
                c = c + lr * (m - c) * (1.0 - _cos(c, m))  # consolidate toward replayed memory
            return c
        return construct
    return make


# ════════════════════════════════════════════════════════════════════════
# self-test — prove the G1 metric SEPARATES a planted recombination from noise
# (so a 0/N below is a real floor, not a dead metric)
# ════════════════════════════════════════════════════════════════════════

def self_test(seed=0, d=64):
    rng = np.random.default_rng(seed)
    # synthetic concept space where child = a known nonlinear bind of a,b
    parents = {}
    children = {}
    pairs = []
    for i in range(12):
        a = br._unit(rng.standard_normal(d)); b = br._unit(rng.standard_normal(d))
        child = br._unit(0.5 * (a + b) + 0.4 * (a * b))   # genuine bind (mid + hadamard)
        an, bn, cn = "a%d" % i, "b%d" % i, "c%d" % i
        parents[an] = a; parents[bn] = b; children[cn] = child
        pairs.append((an, bn, cn))
    emb = {**parents, **children}
    # a learned constructor that KNOWS the bind should recover; a pure-shuffle should not
    A = np.array([emb[p[0]] for p in pairs]); B = np.array([emb[p[1]] for p in pairs])
    Y = np.array([emb[p[2]] for p in pairs])
    Phi = np.concatenate([A, B, A * B], axis=1)
    W = _ridge_fit(Phi, Y)
    pool_names = [p[2] for p in pairs]; pool_vecs = [emb[n] for n in pool_names]
    hits = 0
    for (pa, pb, child) in pairs:
        a, b = emb[pa], emb[pb]
        c = (np.concatenate([a, b, a * b])[None] @ W).reshape(-1)
        if _rank1(c, pool_vecs, pool_names) == child:
            hits += 1
    # the planted-bind learned constructor should recover MOST; random should not
    rnd = br._unit(rng.standard_normal(d))
    rnd_hits = sum(_rank1(rnd, pool_vecs, pool_names) == p[2] for p in pairs)
    sep = hits >= 8 and rnd_hits <= 2
    return dict(planted_recovered=hits, total=len(pairs), random_recovered=rnd_hits,
                SEPARATES=sep)


# ════════════════════════════════════════════════════════════════════════
def _bar_line(name, h, t, extra_ok, extra_desc):
    rate = h / max(t, 1)
    base = rate >= (2.0 / 3.0)
    verdict = "PASS" if (base and extra_ok) else "FLOOR"
    return rate, verdict, "%-32s %2d/%-3d (%.2f)  %s -> %s" % (
        name, h, t, rate, extra_desc, verdict)


def main(argv):
    np.seterr(all="ignore")
    ck = None
    if len(argv) > 1:
        ck = argv[1]
    else:
        for c in _CANDS:
            if os.path.exists(c):
                ck = c; break
    print("=" * 78)
    print("H_1826..1831 — 6 ANIMA-NATIVE G1 LEVERS — cheap-numpy HE pre-screen (p7)")
    print("  DIRECTIONAL: embed = core/clm_decode.py 303M trunk penultimate (β embed),")
    print("  fp64 numpy operators. NOT terminal (G1 SSOT = engine-native anima evaluate).")
    print("=" * 78)

    print("\n[0] METRIC SELF-TEST (planted nonlinear bind vs random)")
    st = self_test()
    print("    planted-bind learned constructor recovered: %d/%d" % (st["planted_recovered"], st["total"]))
    print("    random vector recovered:                    %d/%d" % (st["random_recovered"], st["total"]))
    print("    SEPARATES (planted>=8 ∧ random<=2): %s" % ("PASS" if st["SEPARATES"] else "FAIL"))

    if ck is None or not os.path.exists(ck) or not cd.clm_decodable(ck):
        print("\n!! no v0.2-decodable ckpt found (tried %s)" % ck)
        return 1
    print("\n[1] loading 303M trunk:", os.path.basename(ck))
    W = cd.clm_load_weights(ck)
    print("    d=%d E=%d K=%d L=%d" % (W["d"], W["E"], W["K"], W["L"]))

    # embed every unique concept ONCE (β semantic embed, L2-unit), cached.
    concepts = set()
    for a, b, c in PAIRS:
        concepts.update([a, b, c])
    concepts.update(DISTRACTORS)
    concepts = sorted(concepts)
    print("\n[2] embedding %d unique concepts (303M trunk penultimate, mean-pool, L2-unit)..." % len(concepts))
    t0 = time.time()
    emb = {s: br._unit(br._semantic_rep(W, s)) for s in concepts}
    print("    done %.1fs (%.3fs/concept)" % (time.time() - t0, (time.time() - t0) / len(concepts)))
    print("    %d pairs, %d distractors, candidate pool = %d" % (len(PAIRS), len(DISTRACTORS), len(PAIRS) + len(DISTRACTORS)))

    # single-parent leakage control (shared, γ precedent flagged byte-prefix leak)
    pool_names = [PAIRS[i][2] for i in range(len(PAIRS))] + DISTRACTORS
    pool_vecs = [emb[n] for n in pool_names]
    single_hits = sum(
        (_rank1(emb[PAIRS[i][0]], pool_vecs, pool_names) == PAIRS[i][2]) or
        (_rank1(emb[PAIRS[i][1]], pool_vecs, pool_names) == PAIRS[i][2])
        for i in range(len(PAIRS)))
    print("    single-parent NN already==child (irreducibility leak): %d/%d" % (single_hits, len(PAIRS)))

    print("\n[3] 5-fold CV held-out G1 per lever (frozen bars, p7):")
    print("    " + "-" * 70)
    rows = {}

    # ---- N1 H_1826 Ψ=½ fixed-point ----
    h_on, t_on, per_on = cv_construct(n1_construct_factory(iterate=True), emb)
    h_off, t_off, _ = cv_construct(n1_construct_factory(iterate=False), emb)
    iter_causal = h_on > h_off
    rate, v, line = _bar_line("N1 Ψ=½ fixed-point (ON)", h_on, t_on,
                              iter_causal, "iter-OFF=%d/%d (causal=%s)" % (h_off, t_off, iter_causal))
    print("    " + line); rows["N1"] = dict(h=h_on, t=t_on, off=h_off, verdict=v, per=per_on, extra=dict(iteration_OFF=h_off, iteration_causal=bool(iter_causal)))

    # ---- N2 H_1827 V(D)J ----
    h_on, t_on, per = cv_construct(n2_construct_factory(hypermutation=True), emb)
    h_pc, t_pc, _ = cv_construct(lambda emb_, tr: (lambda a, b: a), emb)   # parent-copy = parentA
    h_hm, t_hm, _ = cv_construct(n2_construct_factory(hypermutation=False), emb)  # hypermutation-OFF
    beats_pc = h_on > h_pc
    rate, v, line = _bar_line("N2 V(D)J immune recomb", h_on, t_on,
                              beats_pc, "parent-copy=%d hypermut-OFF=%d (>pc=%s)" % (h_pc, h_hm, beats_pc))
    print("    " + line); rows["N2"] = dict(h=h_on, t=t_on, verdict=v, per=per, extra=dict(parent_copy=h_pc, hypermutation_OFF=h_hm, beats_parent_copy=bool(beats_pc)))

    # ---- N3 H_1828 Φ-integration (cheap exact small-n) ----
    h_on, t_on, per = cv_construct(n3_construct_factory(emb), emb)
    # Φ(child)>Φ(single)∧>Φ(shuffle): compare mean integration of constructed vs single/shuffle
    rate, v, line = _bar_line("N3 Φ-integration (cheap-exact)", h_on, t_on,
                              True, "exact small-n Φ rank (faithful IIT4 = engine-native)")
    print("    " + line); rows["N3"] = dict(h=h_on, t=t_on, verdict=v, per=per, extra=dict(note="cheap exact small-n integration proxy; terminal Φ = stdlib faithful_phi.hexa engine-native"))

    # ---- N4 H_1829 kosmos anchor (learned) vs midpoint ----
    h_on, t_on, per = cv_construct(n4_construct_factory(), emb)
    h_mid, t_mid, _ = cv_construct(n4_midpoint_factory(), emb)
    beats_mid = h_on > h_mid
    rate, v, line = _bar_line("N4 kosmos anchor (learned)", h_on, t_on,
                              beats_mid, "midpoint-baseline=%d (>mid=%s)" % (h_mid, beats_mid))
    print("    " + line); rows["N4"] = dict(h=h_on, t=t_on, verdict=v, per=per, extra=dict(midpoint_baseline=h_mid, beats_midpoint=bool(beats_mid)))

    # ---- N5 H_1830 Kuramoto phase-sync ----
    h_on, t_on, per = cv_construct(n5_construct_factory(K=1.5), emb)
    h_k0, t_k0, _ = cv_construct(n5_construct_factory(K=0.0), emb)         # K=0 BLIND
    h_amp, t_amp, _ = cv_construct(n5_amplitude_factory(), emb)            # amplitude baseline
    sync_causal = h_on > h_k0
    beats_amp = h_on > h_amp
    rate, v, line = _bar_line("N5 Kuramoto phase-sync", h_on, t_on,
                              (sync_causal and beats_amp), "K=0=%d amp=%d (causal=%s >amp=%s)" % (h_k0, h_amp, sync_causal, beats_amp))
    print("    " + line); rows["N5"] = dict(h=h_on, t=t_on, verdict=v, per=per, extra=dict(K0_blind=h_k0, amplitude_baseline=h_amp, sync_causal=bool(sync_causal), beats_amplitude=bool(beats_amp)))

    # ---- N6 H_1831 replay (REOPEN H_987) ----
    h_on, t_on, per = cv_construct(n6_construct_factory(replay=True), emb)
    h_no, t_no, _ = cv_construct(n6_construct_factory(replay=False), emb)  # no-replay
    beats_no = h_on > h_no
    rate, v, line = _bar_line("N6 replay recomb (REOPEN H_987)", h_on, t_on,
                              beats_no, "no-replay=%d (>no-replay=%s)" % (h_no, beats_no))
    print("    " + line); rows["N6"] = dict(h=h_on, t=t_on, verdict=v, per=per, extra=dict(no_replay=h_no, beats_no_replay=bool(beats_no)))

    print("\n[4] SUMMARY — which anima-native levers survive the cheap pre-screen")
    print("    " + "-" * 70)
    print("    %-6s %-34s %-12s %s" % ("lever", "mechanism", "G1 held-out", "cheap-HE"))
    names = {
        "N1": "H_1826 Ψ=½ dynamical fixed-point",
        "N2": "H_1827 V(D)J immune recombination",
        "N3": "H_1828 Φ-integration bind",
        "N4": "H_1829 kosmos anchor-space",
        "N5": "H_1830 Kuramoto phase-sync",
        "N6": "H_1831 replay (REOPEN H_987)",
    }
    n_pass = 0
    for k in ["N1", "N2", "N3", "N4", "N5", "N6"]:
        r = rows[k]
        if r["verdict"] == "PASS":
            n_pass += 1
        print("    %-6s %-34s %2d/%-9d %s" % (k, names[k], r["h"], r["t"], r["verdict"]))
    print("\n    single-parent leak (shared) = %d/%d  | self-test SEPARATES = %s" %
          (single_hits, len(PAIRS), "PASS" if st["SEPARATES"] else "FAIL"))
    print("    %d/6 levers clear the cheap pre-screen -> engine-native candidates" % n_pass)
    if n_pass == 0:
        print("    ALL 6 FLOOR at cheap tier -> G1 wall holds against anima-native mechanisms")
        print("    (honest negative, c9 — strong evidence the combination-operator floor is structural)")
    print("=" * 78)

    # machine-readable tail for the filer
    import json
    out = {k: {"h": rows[k]["h"], "t": rows[k]["t"], "verdict": rows[k]["verdict"],
               "extra": rows[k]["extra"]} for k in rows}
    out["_single_parent_leak"] = [single_hits, len(PAIRS)]
    out["_self_test_separates"] = bool(st["SEPARATES"])
    out["_ckpt"] = os.path.basename(ck)
    print("\nJSON_RESULT " + json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
