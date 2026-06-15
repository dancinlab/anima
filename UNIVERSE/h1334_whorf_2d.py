"""
H_1334 — SAPIR-WHORF / CATEGORICAL PERCEPTION GENERALIZES TO A 2-D / FEATURAL SPACE?
R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1334_whorf_2d/FREEZE.txt (pre-registered BEFORE this scoring).
$0 CPU numpy, gradient-free, 3 seeds [4334,4335,4336], p7. a_no_llm_frame_trap
(cognitive-science / categorical-perception lens, c15) — NOT an LLM recipe, NOT a
human-cognition claim. ENGINE-TRANSFER UNVERIFIED (directional mirror of the
immune/Voronoi store, same family as H_1323).

THE QUESTION: H_1323/H_1325 🟢/🟠 showed Whorfian categorical perception (CP) on a 1-D
stimulus continuum (CP peak emerges AT a language's boundary, its LOCATION tracks the
language). Does CP GENERALIZE to a 2-D / featural stimulus space — does CP emerge along
a language's 2-D category BOUNDARY (cross-boundary discrim > within-category),
concentrated along the boundary CURVE (a ridge), and track the language's 2-D carving?
Or is the effect 1-D-only?

PARADIGM (toy synthetic 2-D continuum):
  - a G x G grid of stimuli on a [0,1]^2 feature square; each -> a 2-D RBF population
    code over a KxK grid of fixed tuning centers (boundary-AGNOSTIC).
  - TWO languages carve the SAME square: L_2D = LINEAR diagonal (u+v > T_LIN),
    L'_2D = L-SHAPED corner (u > T_LX and v > T_LY). Distinct boundary curves.
  - the SAME gradient-free mitosis/Voronoi store (error-targeted SPLIT-only growth, p8)
    learns each carving -> cells PACK along the 2-D boundary curve (CP origin).
  - NON-LINGUISTIC TEST (NO labels at test): per grid EDGE (4-neighbour adjacent pair),
    discrim = |Δ soft posterior|. High-discrim edges form the CP RIDGE.

RIDGE-COHERENCE METRIC (the 2-D analogue of the 1-D peak-count):
  ridge = top RIDGE_FRAC edges by discrim. RIDGE-ALIGN(arm,curve) = how close ridge
  edges sit to a boundary curve. RIDGE-COHERENCE(arm) = largest-connected-component
  fraction of the ridge edge-set (a real boundary ridge = ONE connected curve;
  shuffle = scattered specks).

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary,
NO persona/RLHF. Language label enters ONLY at training, NEVER at test. PRE-LANGUAGE +
SHUFFLE are the anti-Goodhart discriminators.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
G_GRID   = 11                 # G x G stimulus grid (121 stimuli)
K_RBF    = 6                  # K x K RBF tuning centers -> DIM = 36
DIM      = K_RBF * K_RBF
T_LIN    = 1.0                # L_2D linear boundary: u + v > T_LIN (diagonal)
T_LX     = 0.5               # L'_2D L-shaped: u > T_LX
T_LY     = 0.5               # L'_2D L-shaped: v > T_LY
GROW_MAX = 40                 # max prototype splits per arm (FIXED across arms)
SPLIT_PASSES = 40
BETA_POST = 18.0
SEEDS    = [4334, 4335, 4336]

# frozen bar thresholds
W1_MARGIN    = 0.15           # cross-within margin AND lang-vs-baseline@ridge
BAND_NEAR    = 0.10           # edge "cross-boundary" if midpoint within this of curve
BAND_FAR     = 0.25           # edge "within-category" if midpoint >= this from curve
RIDGE_FRAC   = 0.20           # top fraction of edges = the ridge
ALIGN_MIN    = 0.70           # T1c: ridge-align to own boundary
DISSOC_GAP   = 0.10           # T2: own-boundary align minus other-boundary align
COH_SHUF_MAX = 0.50           # T3: shuffle ridge coherence ceiling
COH_LANG_MIN = 0.70           # T3: language ridge coherence floor
D_MAX        = np.sqrt(2.0) / 2.0   # normalizer for point-to-curve distance


# ── 2-D RBF population code ──────────────────────────────────────────────────
def make_basis(seed):
    rb = np.random.default_rng(seed + 7000)
    g = np.linspace(0.0, 1.0, K_RBF)
    cu, cv = np.meshgrid(g, g)                # FIXED evenly-spaced 2-D tuning centers
    centers = np.stack([cu.ravel(), cv.ravel()], axis=1)   # (DIM, 2)
    width = float(rb.uniform(0.14, 0.18))     # mild per-seed width jitter (substrate noise)
    return {"centers": centers, "width": width}


def embed(p, basis):
    """2-D RBF population code of position p=(u,v): locally-smooth, position-FAITHFUL,
    boundary-AGNOSTIC. Embedding-distance tracks position-distance monotonically."""
    centers = basis["centers"]
    width = basis["width"]
    d2 = ((p[None, :] - centers) ** 2).sum(axis=1)
    v = np.exp(-d2 / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


# ── languages: 2-D carvings of the SAME square ───────────────────────────────
def label_of(p, kind, rng=None):
    u, vv = float(p[0]), float(p[1])
    if kind == "lin":                         # L_2D : diagonal linear boundary
        return int((u + vv) > T_LIN)
    if kind == "Lshape":                      # L'_2D : L-shaped corner boundary
        return int((u > T_LX) and (vv > T_LY))
    if kind == "none":                        # pre-language: all zero (unsupervised)
        return 0
    if kind == "shuffle":                     # incoherent random label (fixed per seed)
        return int(rng.integers(0, 2))
    raise ValueError(kind)


# ── point-to-boundary-curve distance (dense curve sampling) ──────────────────
def boundary_samples(kind, n=400):
    """Dense sampling of a boundary CURVE inside [0,1]^2 (the locus where the category
    flips). Used ONLY for SCORING ridge-align — never seen by the substrate."""
    t = np.linspace(0.0, 1.0, n)
    if kind == "lin":
        # u + v = T_LIN, clipped to the unit square
        us = t
        vs = T_LIN - t
        m = (vs >= 0.0) & (vs <= 1.0)
        return np.stack([us[m], vs[m]], axis=1)
    if kind == "Lshape":
        # the L-corner boundary = two segments: u=T_LX (v>=T_LY) and v=T_LY (u>=T_LX)
        seg1 = np.stack([np.full_like(t, T_LX), T_LY + t * (1.0 - T_LY)], axis=1)
        seg2 = np.stack([T_LX + t * (1.0 - T_LX), np.full_like(t, T_LY)], axis=1)
        return np.concatenate([seg1, seg2], axis=0)
    raise ValueError(kind)


def dist_to_curve(pt, samples):
    d = np.sqrt(((samples - pt[None, :]) ** 2).sum(axis=1))
    return float(d.min())


class VoronoiCells:
    """Immune/Voronoi prototype store, error-targeted SPLIT-only growth (p8 mirror).
    Each cell = (prototype embedding, bound label). Recall = nearest cell's label.
    Growth: split the cell with the most label-error, at its worst-owned stimulus ->
    packs cells DENSER along the 2-D boundary curve where category error concentrates."""

    def __init__(self):
        self.protos = []
        self.labels = []

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit(self, X, Y, grow_max, passes):
        M = len(X)
        c0 = X.mean(axis=0)
        n = np.linalg.norm(c0)
        c0 = c0 / n if n > 0 else c0
        self.protos = [c0]
        seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
        self.labels = [int(Y[seed_stim])]
        for _ in range(passes):
            if len(self.protos) >= 1 + grow_max:
                break
            owners = np.array([self._owner(X[m])[0] for m in range(M)])
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y)[0]
            if len(mism) == 0:
                # STOP when error is gone (error is the ONLY growth driver, p8). An
                # all-zero-label arm classifies all correctly with 1 cell -> stays FLAT.
                break
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy())
            self.labels.append(int(Y[s]))
        return self

    def posterior(self, key):
        """Soft category-posterior P(cat=1) = softmin-weighted vote of nearby prototypes'
        bound labels. NO hard label read. Where cells PACK at a boundary the posterior
        SWINGS sharply -> adjacent pairs straddling it are highly discriminable."""
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        w = np.exp(-BETA_POST * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


# ── grid + edges ─────────────────────────────────────────────────────────────
def make_grid():
    g = np.linspace(0.0, 1.0, G_GRID)
    pos = np.array([[u, v] for v in g for u in g])   # row-major (v outer, u inner)
    return pos


def grid_edges():
    """4-neighbour adjacent pairs on the G x G grid. Returns list of (i, j) index pairs."""
    def idx(r, c):
        return r * G_GRID + c
    edges = []
    for r in range(G_GRID):
        for c in range(G_GRID):
            if c + 1 < G_GRID:
                edges.append((idx(r, c), idx(r, c + 1)))   # horizontal
            if r + 1 < G_GRID:
                edges.append((idx(r, c), idx(r + 1, c)))   # vertical
    return edges


def run_seed(seed):
    basis = make_basis(seed)
    pos = make_grid()
    X = np.array([embed(p, basis) for p in pos])
    edges = grid_edges()
    mids = np.array([0.5 * (pos[i] + pos[j]) for (i, j) in edges])  # (E,2)

    arms = {}
    for kind in ["none", "lin", "Lshape", "shuffle"]:
        lr = np.random.default_rng(seed + {"none": 1, "lin": 2, "Lshape": 3, "shuffle": 4}[kind])
        Y = np.array([label_of(pos[m], kind, lr) for m in range(len(pos))])
        cells = VoronoiCells().fit(X, Y, GROW_MAX, SPLIT_PASSES)
        disc = np.array([abs(cells.posterior(X[i]) - cells.posterior(X[j])) for (i, j) in edges])
        arms[kind] = dict(disc=disc, ncells=len(cells.protos))
    return pos, edges, mids, arms


# ── ridge metrics ────────────────────────────────────────────────────────────
def ridge_mask(disc):
    """top RIDGE_FRAC edges by discrimination = the ridge edge-set (boolean mask)."""
    if disc.max() <= 0:
        return np.zeros_like(disc, dtype=bool)
    k = max(1, int(round(RIDGE_FRAC * len(disc))))
    thresh = np.sort(disc)[::-1][k - 1]
    return disc >= thresh


def ridge_align(mids, mask, curve_samples):
    """mean over ridge edges of [1 - dist(edge_midpoint, boundary_curve)/D_MAX]."""
    if not mask.any():
        return 0.0
    vals = []
    for m in mids[mask]:
        d = dist_to_curve(m, curve_samples)
        vals.append(max(0.0, 1.0 - d / D_MAX))
    return float(np.mean(vals))


def ridge_coherence(edges, mask):
    """largest-connected-component fraction of the ridge edge-set under grid adjacency.
    Two grid edges are adjacent if they share a grid vertex. ONE connected curve -> ~1;
    scattered specks -> low (many tiny components)."""
    ridge_idx = [e for e, on in enumerate(mask) if on]
    if len(ridge_idx) == 0:
        return 0.0
    # vertex -> ridge-edges incident on it
    from collections import defaultdict
    vert2e = defaultdict(list)
    for e in ridge_idx:
        a, b = edges[e]
        vert2e[a].append(e)
        vert2e[b].append(e)
    # union-find over ridge edges via shared vertices
    parent = {e: e for e in ridge_idx}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry
    for e in ridge_idx:
        a, b = edges[e]
        for v in (a, b):
            for f in vert2e[v]:
                if f != e:
                    union(e, f)
    comp = defaultdict(int)
    for e in ridge_idx:
        comp[find(e)] += 1
    largest = max(comp.values())
    return float(largest) / float(len(ridge_idx))


def cross_within_margin(mids, disc, curve_samples):
    """cross-boundary = mean raw discrim of edges within BAND_NEAR of the boundary curve;
    within-category = mean raw discrim of edges >= BAND_FAR from it."""
    dists = np.array([dist_to_curve(m, curve_samples) for m in mids])
    near = dists <= BAND_NEAR
    far = dists >= BAND_FAR
    cross = disc[near].mean() if near.any() else 0.0
    within = disc[far].mean() if far.any() else 0.0
    return cross, within


def main():
    print("H_1334 R1 — SAPIR-WHORF CATEGORICAL PERCEPTION in a 2-D / FEATURAL SPACE")
    print("=" * 82)
    print("paradigm: two-language carving of one 2-D feature square (linear vs L-shaped);")
    print("non-linguistic discrimination = prototype-response distance per grid edge (NO")
    print("labels at test). ridge-coherence metric = the 2-D analogue of the 1-D peak.")
    print(f"G={G_GRID} ({G_GRID*G_GRID} stim) dim={DIM} lin:u+v>{T_LIN} L:u>{T_LX}&v>{T_LY} "
          f"grow_max={GROW_MAX} seeds={SEEDS}")
    print("")

    lin_curve = boundary_samples("lin")
    Lsh_curve = boundary_samples("Lshape")

    # per-seed accumulators
    acc = {k: {"cw_margin": [], "vs_base": [], "align_own": [], "align_lin": [],
               "align_Lsh": [], "coh": [], "ncells": []}
           for k in ["none", "lin", "Lshape", "shuffle"]}

    for seed in SEEDS:
        pos, edges, mids, arms = run_seed(seed)
        base_disc = arms["none"]["disc"]
        for kind in ["none", "lin", "Lshape", "shuffle"]:
            disc = arms[kind]["disc"]
            mask = ridge_mask(disc)
            al_lin = ridge_align(mids, mask, lin_curve)
            al_Lsh = ridge_align(mids, mask, Lsh_curve)
            coh = ridge_coherence(edges, mask)
            acc[kind]["align_lin"].append(al_lin)
            acc[kind]["align_Lsh"].append(al_Lsh)
            acc[kind]["coh"].append(coh)
            acc[kind]["ncells"].append(arms[kind]["ncells"])
            # own-boundary specific quantities for languages
            if kind == "lin":
                cr, wi = cross_within_margin(mids, disc, lin_curve)
                acc[kind]["cw_margin"].append(cr - wi)
                acc[kind]["vs_base"].append((disc[mask].mean() if mask.any() else 0.0)
                                            - (base_disc[mask].mean() if mask.any() else 0.0))
                acc[kind]["align_own"].append(al_lin)
            elif kind == "Lshape":
                cr, wi = cross_within_margin(mids, disc, Lsh_curve)
                acc[kind]["cw_margin"].append(cr - wi)
                acc[kind]["vs_base"].append((disc[mask].mean() if mask.any() else 0.0)
                                            - (base_disc[mask].mean() if mask.any() else 0.0))
                acc[kind]["align_own"].append(al_Lsh)

    def mean(k, f):
        return float(np.mean(acc[k][f])) if acc[k][f] else 0.0

    # ── report: ridge-coherence + margins per arm, per seed ──────────────────
    print("  per-arm summary (mean of 3 seeds):")
    print("    arm        ncells  ridge-COH  align(lin) align(Lsh)")
    for k in ["none", "lin", "Lshape", "shuffle"]:
        print(f"    {k:9s}   {mean(k,'ncells'):4.1f}    {mean(k,'coh'):.3f}     "
              f"{mean(k,'align_lin'):.3f}      {mean(k,'align_Lsh'):.3f}")
    print("")
    print("  per-seed ridge-coherence + cross-within margin (the headline data):")
    print("    seed   L_2D:coh cw_marg vs_base align_own | L'_2D:coh cw_marg vs_base align_own | shuf:coh")
    for si, seed in enumerate(SEEDS):
        print(f"    {seed}   {acc['lin']['coh'][si]:.3f}   {acc['lin']['cw_margin'][si]:+.3f} "
              f"{acc['lin']['vs_base'][si]:+.3f}  {acc['lin']['align_own'][si]:.3f}   |  "
              f"{acc['Lshape']['coh'][si]:.3f}   {acc['Lshape']['cw_margin'][si]:+.3f} "
              f"{acc['Lshape']['vs_base'][si]:+.3f}  {acc['Lshape']['align_own'][si]:.3f}   |  "
              f"{acc['shuffle']['coh'][si]:.3f}")
    print("")

    # ── T1 2D-CP PRESENT (ALL 3 seeds, both languages) ───────────────────────
    def all_seeds(k, f, thr, ge=True):
        return all((v >= thr) if ge else (v <= thr) for v in acc[k][f])
    t1_lin = (all_seeds("lin", "cw_margin", W1_MARGIN) and
              all_seeds("lin", "vs_base", W1_MARGIN) and
              all_seeds("lin", "align_own", ALIGN_MIN))
    t1_Lsh = (all_seeds("Lshape", "cw_margin", W1_MARGIN) and
              all_seeds("Lshape", "vs_base", W1_MARGIN) and
              all_seeds("Lshape", "align_own", ALIGN_MIN))
    t1 = t1_lin and t1_Lsh
    print(f"  T1 2D-CP PRESENT (all 3 seeds, both L: cw-margin>={W1_MARGIN}, vs-baseline>={W1_MARGIN},")
    print(f"     ridge-align(own)>={ALIGN_MIN}):")
    print(f"     L_2D : cw={mean('lin','cw_margin'):+.3f} vsbase={mean('lin','vs_base'):+.3f} "
          f"align={mean('lin','align_own'):.3f}  -> {'PASS' if t1_lin else 'FAIL'}")
    print(f"     L'_2D: cw={mean('Lshape','cw_margin'):+.3f} vsbase={mean('Lshape','vs_base'):+.3f} "
          f"align={mean('Lshape','align_own'):.3f}  -> {'PASS' if t1_Lsh else 'FAIL'}")
    print(f"     -> T1 {'PASS' if t1 else 'FAIL'}")

    # ── T2 2D-DISSOCIATION ───────────────────────────────────────────────────
    lin_gap = mean("lin", "align_lin") - mean("lin", "align_Lsh")
    Lsh_gap = mean("Lshape", "align_Lsh") - mean("Lshape", "align_lin")
    t2 = (lin_gap >= DISSOC_GAP) and (Lsh_gap >= DISSOC_GAP)
    print(f"  T2 2D-DISSOCIATION (each ridge tracks OWN boundary by >= {DISSOC_GAP}):")
    print(f"     L_2D  align(lin)-align(Lsh) = {mean('lin','align_lin'):.3f}-{mean('lin','align_Lsh'):.3f} "
          f"= {lin_gap:+.3f}")
    print(f"     L'_2D align(Lsh)-align(lin) = {mean('Lshape','align_Lsh'):.3f}-{mean('Lshape','align_lin'):.3f} "
          f"= {Lsh_gap:+.3f}")
    print(f"     -> T2 {'PASS' if t2 else 'FAIL'}")

    # ── T3 EARNED (anti-Goodhart shuffle) ────────────────────────────────────
    coh_shuf = mean("shuffle", "coh")
    coh_lang = 0.5 * (mean("lin", "coh") + mean("Lshape", "coh"))
    t3 = (coh_shuf <= COH_SHUF_MAX) and (coh_lang >= COH_LANG_MIN)
    print(f"  T3 EARNED (shuffle ridge-coherence<={COH_SHUF_MAX} & mean-lang ridge-coherence>={COH_LANG_MIN}):")
    print(f"     ridge-coherence: L_2D={mean('lin','coh'):.3f} L'_2D={mean('Lshape','coh'):.3f} "
          f"mean-lang={coh_lang:.3f}  SHUFFLE={coh_shuf:.3f}")
    print(f"     -> T3 {'PASS' if t3 else 'FAIL'}")
    print("")
    print(f"  PRE-LANGUAGE arm: ncells={mean('none','ncells'):.1f} ridge-coherence="
          f"{mean('none','coh'):.3f} (flat = no coherent ridge by construction)")
    print("=" * 82)

    green = t1 and t2 and t3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — WHORFIAN CP GENERALIZES TO 2-D /")
        print("  FEATURAL SPACE. Categorical perception emerges ALONG the language's 2-D")
        print("  boundary CURVE (cross-boundary discrim > within-category, concentrated on a")
        print("  connected ridge), the ridge TRACKS the language's carving (linear vs L-shaped,")
        print("  T2 dissociation), and SHUFFLE gives no coherent ridge (T3). The relativity")
        print("  effect is NOT a 1-D artifact. ENGINE-TRANSFER UNVERIFIED — follow-on.")
        print("  TOY synthetic 2-D continuum, 3 seeds; NO human-cognition claim (a_scale_honest_scope).")
        return 0
    if not t1:
        print("VERDICT: 🧱 CP is 1-D-ONLY — the 2-D-CP-PRESENT bar (T1) fails: categorical")
        print("  perception does NOT survive the move to a 2-D featural space. Honest scope")
        print("  limit on the H_1325 1-D result, reported straight (c9). NO bar move.")
        return 3
    if t1 and not t2:
        print("VERDICT: 🔵 2-D CP PRESENT but language-INDEPENDENT ridge (Whorf REFUTED in 2-D,")
        print("  T2 fails). CP emerges in 2-D but its ridge does not track the language's")
        print("  carving. Honest negative, reported straight (c9).")
        return 2
    if t1 and t2 and not t3:
        print("VERDICT: 🟠 PARTIAL — 2-D relativity holds (T1∧T2: CP ridge tracks each language's")
        print("  2-D boundary) but the anti-Goodhart shuffle control (T3) did not fully clear.")
        print("  NO bar moved (c9/p7) — reported straight. R2: re-freeze the coherence bar anew.")
        return 4
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
