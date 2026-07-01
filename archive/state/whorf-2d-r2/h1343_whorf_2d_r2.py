"""
H_1343 — SAPIR-WHORF / 2-D CATEGORICAL PERCEPTION as a representational-metric WARP.
R2 of H_1334. numpy MIRROR (DIRECTIONAL — engine-transfer UNVERIFIED).

Frozen design: .verdicts/1343_whorf_2d_r2/FREEZE.txt (pre-registered BEFORE this scoring;
frozen-first, c9 / p7 NO tune-to-green). $0 CPU, gradient-free, 3 seeds [4334,4335,4336],
deterministic. a_no_llm_frame_trap (cognitive-science / categorical-perception lens, c15)
— NOT an LLM recipe, NOT a human-cognition claim.

WHY r2 RE-SPECIFIES THE METRIC: H_1334 scored CP by RIDGE-ALIGNMENT to a known boundary
CURVE; that fails for a DIAGONAL boundary on a coarse RBF grid (a grid-geometry artifact,
not absence of CP — its discrimination margins were the LARGEST of any arm). The prior
H_1343 ridge attempt swept density to K_RBF=14 and the diagonal align STILL failed. r2
uses the TEXTBOOK CP operationalization that is boundary-curve-AGNOSTIC: the WARP of the
learned representational metric (WITHIN-category COMPRESSION + BETWEEN-category EXPANSION),
referenced to a boundary-agnostic PRE-LANGUAGE baseline. Plus two controls: a label-
PERMUTATION null (c2 EARNED) and a COMPONENT-COUNT control that shuffles WHICH feature axis
carries the boundary (c3 — warp lives in the trained 2-D metric, not raw variance).

p1/p2/p3/p6: the warp reads ONLY representational distance (|Δ soft posterior|) + the store's
OWN learned category partition; NO injected boundary, NO persona/RLHF. The language label
enters ONLY during training, NEVER into the warp readout.
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
G_GRID       = 11                  # 11x11 = 121 stimuli
K_RBF_LADDER = [6, 9, 12]          # density ladder; production = densest
K_RBF_PROD   = 12                  # DIM = 144
T_DIAG       = 1.0                 # L_DIAG : u + v > 1.0 (diagonal)
T_LX         = 0.5                 # L_LSHAPE : u > 0.5
T_LY         = 0.5                 #            and v > 0.5
GROW_MAX     = 40
SPLIT_PASSES = 40
BETA_POST    = 18.0
SEEDS        = [4334, 4335, 4336]

WARP_MIN   = 0.20                  # c1 presence
CHANCE_TOL = 0.05                  # c2 shuffle null mean ceiling
SEP        = 0.10                  # c2 separation above null-q95
COMP_MAX   = 0.05                  # c3 component-shuffle ceiling
N_SHUF     = 200                   # label-permutation null draws
N_COMP     = 50                    # component-shuffle draws
NULL_Q     = 0.95                  # percentile of shuffle null for the SEP gate


# ── 2-D RBF population code (boundary-AGNOSTIC) ──────────────────────────────
def make_basis(seed, k_rbf):
    rb = np.random.default_rng(seed + 7000 + k_rbf)
    g = np.linspace(0.0, 1.0, k_rbf)
    cu, cv = np.meshgrid(g, g)
    centers = np.stack([cu.ravel(), cv.ravel()], axis=1)   # (DIM, 2)
    width = float(rb.uniform(0.14, 0.18))                   # mild per-seed width jitter
    return {"centers": centers, "width": width}


def embed(p, basis):
    centers, width = basis["centers"], basis["width"]
    d2 = ((p[None, :] - centers) ** 2).sum(axis=1)
    v = np.exp(-d2 / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


# ── languages: 2-D carvings of the SAME square ───────────────────────────────
def label_of(p, kind):
    u, vv = float(p[0]), float(p[1])
    if kind == "diag":
        return int((u + vv) > T_DIAG)
    if kind == "Lshape":
        return int((u > T_LX) and (vv > T_LY))
    raise ValueError(kind)


class VoronoiCells:
    """Immune/Voronoi prototype store, error-targeted SPLIT-only growth (p8 mirror).
    Verbatim family of H_1334. Recall posterior = softmin-weighted vote of bound labels."""

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
                break                                  # error is the ONLY growth driver (p8)
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy())
            self.labels.append(int(Y[s]))
        return self

    def posterior(self, key):
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        w = np.exp(-BETA_POST * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


# ── grid + edges ─────────────────────────────────────────────────────────────
def make_grid():
    g = np.linspace(0.0, 1.0, G_GRID)
    return np.array([[u, v] for v in g for u in g])     # row-major (v outer, u inner)


def grid_edges():
    def idx(r, c):
        return r * G_GRID + c
    edges = []
    for r in range(G_GRID):
        for c in range(G_GRID):
            if c + 1 < G_GRID:
                edges.append((idx(r, c), idx(r, c + 1)))
            if r + 1 < G_GRID:
                edges.append((idx(r, c), idx(r + 1, c)))
    return edges


# ── CP-WARP metric: within-compression + between-expansion vs baseline ───────
def warp_ratio(g, edges, cat):
    """g = per-stimulus learned category coordinate (soft posterior in [0,1]).
    cat = per-stimulus integer category used to partition edges into WITHIN / BETWEEN.
    Returns ( mean |Δg| over BETWEEN edges / mean |Δg| over WITHIN edges ).
    Boundary-curve-AGNOSTIC: depends only on the category partition, not on any
    known boundary geometry."""
    dwithin, dbetween = [], []
    for (i, j) in edges:
        dg = abs(g[i] - g[j])
        if cat[i] == cat[j]:
            dwithin.append(dg)
        else:
            dbetween.append(dg)
    mw = float(np.mean(dwithin)) if dwithin else 0.0
    mb = float(np.mean(dbetween)) if dbetween else 0.0
    if mw <= 1e-12:
        # degenerate: no within variation. return mb scaled large only if mb>0; else 0.
        return (mb / 1e-12) if mb > 0 else 0.0
    return mb / mw


def cp_warp(g_lang, cat_lang, g_base, cat_base, edges):
    """CP-WARP = ratio(language metric, language partition)
                 - ratio(baseline metric, baseline partition).
    Subtracting the baseline removes any expansion/compression ratio the raw RBF geometry
    already carries, so a positive warp is the language-INDUCED warping of the metric."""
    r_lang = warp_ratio(g_lang, edges, cat_lang)
    r_base = warp_ratio(g_base, edges, cat_base)
    return r_lang - r_base, r_lang, r_base


def fit_posteriors(X, Y, edges):
    cells = VoronoiCells().fit(X, Y, GROW_MAX, SPLIT_PASSES)
    g = np.array([cells.posterior(X[m]) for m in range(len(X))])
    cat = (g >= 0.5).astype(int)                 # store's OWN learned category (no label read)
    return g, cat, len(cells.protos)


# ── per-density run ──────────────────────────────────────────────────────────
def run_density(seed, k_rbf, want_controls):
    basis = make_basis(seed, k_rbf)
    pos = make_grid()
    X = np.array([embed(p, basis) for p in pos])
    edges = grid_edges()
    M = len(pos)

    # PRE-LANGUAGE baseline metric: boundary-agnostic. We use the raw embedding-induced
    # 1-D coordinate (1st principal axis of g would need a carving; instead use the
    # unsupervised "nearest-corner" smooth coordinate = the embedding itself projected).
    # Simplest boundary-agnostic baseline: a store trained on an all-zero carving gives a
    # FLAT posterior (no metric warp at all), which makes the baseline ratio ill-defined.
    # So baseline metric = the raw position-faithful coordinate g0 = normalized (u+v)/2,
    # which is the boundary-AGNOSTIC smooth feature gradient (it carries NO category cut).
    g0 = np.array([0.5 * (pos[m, 0] + pos[m, 1]) for m in range(M)])
    # rescale g0 into [0,1] to match posterior scale (monotone, partition-irrelevant)
    g0 = (g0 - g0.min()) / (g0.max() - g0.min() + 1e-12)

    out = {}
    for kind in ["diag", "Lshape"]:
        Ytrue = np.array([label_of(pos[m], kind) for m in range(M)])
        g_lang, cat_lang, nc = fit_posteriors(X, Ytrue, edges)
        # baseline partition uses the language's GROUND-TRUTH labels but baseline metric g0
        warp, r_lang, r_base = cp_warp(g_lang, cat_lang, g0, Ytrue, edges)
        out[kind] = dict(warp=warp, r_lang=r_lang, r_base=r_base, ncells=nc,
                         g_lang=g_lang, cat_lang=cat_lang, X=X, edges=edges, pos=pos, g0=g0,
                         Ytrue=Ytrue)
    if not want_controls:
        return out

    # ── c2 label-permutation null (N_SHUF) at this density ───────────────────
    shuf_rng = np.random.default_rng(seed + 99000 + k_rbf)
    shuf_warps = []
    for _ in range(N_SHUF):
        Yp = shuf_rng.permutation(out["diag"]["Ytrue"])     # permute one language's labels
        g_s, cat_s, _ = fit_posteriors(X, Yp, edges)
        w_s, _, _ = cp_warp(g_s, cat_s, g0, Yp, edges)
        shuf_warps.append(w_s)
    out["_shuf"] = np.array(shuf_warps)

    # ── c3 component-shuffle control (N_COMP) ────────────────────────────────
    # tie the BETWEEN/WITHIN partition to a SINGLE randomly-chosen feature component
    # (one RBF basis axis) thresholded at its median, instead of the trained 2-D category.
    comp_rng = np.random.default_rng(seed + 77000 + k_rbf)
    DIM = X.shape[1]
    for kind in ["diag", "Lshape"]:
        g_lang = out[kind]["g_lang"]
        cwarps = []
        for _ in range(N_COMP):
            comp = int(comp_rng.integers(0, DIM))
            vals = X[:, comp]
            cat_comp = (vals >= np.median(vals)).astype(int)
            # warp of the LANGUAGE metric g_lang but partitioned by an arbitrary component,
            # referenced to the same baseline under that arbitrary component partition.
            r_lang = warp_ratio(g_lang, edges, cat_comp)
            r_base = warp_ratio(g0, edges, cat_comp)
            cwarps.append(r_lang - r_base)
        out[kind]["comp_warp"] = float(np.mean(cwarps))
    return out


def main():
    print("H_1343 r2 — SAPIR-WHORF 2-D CATEGORICAL PERCEPTION as a representational-metric WARP")
    print("=" * 84)
    print("CP-WARP = (mean |Δposterior| BETWEEN-category / WITHIN-category) MINUS the same ratio")
    print("under a boundary-AGNOSTIC pre-language baseline metric. Boundary-curve-agnostic, so")
    print("it does NOT suffer the H_1334 diagonal-ridge grid-geometry artifact. c2 = label-")
    print("permutation null (N_SHUF=%d); c3 = component-shuffle (N_COMP=%d, warp must live in the" % (N_SHUF, N_COMP))
    print("trained 2-D metric). 3 seeds %s, gradient-free, $0 CPU, DIRECTIONAL mirror." % SEEDS)
    print(f"G={G_GRID} ({G_GRID*G_GRID} stim) ladder K_RBF={K_RBF_LADDER} prod={K_RBF_PROD} "
          f"(DIM={K_RBF_PROD*K_RBF_PROD}) diag:u+v>{T_DIAG} L:u>{T_LX}&v>{T_LY}")
    print("")

    # ── FIX1 density ladder: CP-WARP vs RBF density (mean of 3 seeds) ─────────
    print("  DENSITY LADDER — CP-WARP(own boundary) vs RBF density (mean of 3 seeds):")
    print("    K_RBF  DIM    warp(L_DIAG)   warp(L_LSHAPE)")
    for k in K_RBF_LADDER:
        wd, wl = [], []
        for seed in SEEDS:
            o = run_density(seed, k, want_controls=False)
            wd.append(o["diag"]["warp"]); wl.append(o["Lshape"]["warp"])
        print(f"    {k:3d}  {k*k:4d}    {np.mean(wd):+.3f}          {np.mean(wl):+.3f}")
    print("")

    # ── production density: full controls ─────────────────────────────────────
    per = {kind: dict(warp=[], r_lang=[], r_base=[], ncells=[], comp=[]) for kind in ["diag", "Lshape"]}
    shuf_pool = []
    for seed in SEEDS:
        o = run_density(seed, K_RBF_PROD, want_controls=True)
        for kind in ["diag", "Lshape"]:
            per[kind]["warp"].append(o[kind]["warp"])
            per[kind]["r_lang"].append(o[kind]["r_lang"])
            per[kind]["r_base"].append(o[kind]["r_base"])
            per[kind]["ncells"].append(o[kind]["ncells"])
            per[kind]["comp"].append(o[kind]["comp_warp"])
        shuf_pool.append(o["_shuf"])
    shuf_all = np.concatenate(shuf_pool)        # pooled N_SHUF*3 null

    def m(kind, f):
        return float(np.mean(per[kind][f]))

    print(f"  PRODUCTION density K_RBF={K_RBF_PROD} (DIM={K_RBF_PROD*K_RBF_PROD}) — per-seed detail:")
    print("    seed | L_DIAG: r_lang r_base  warp  comp | L_LSHAPE: r_lang r_base  warp  comp")
    for si, seed in enumerate(SEEDS):
        d, l = per["diag"], per["Lshape"]
        print(f"    {seed} | {d['r_lang'][si]:5.2f} {d['r_base'][si]:5.2f} {d['warp'][si]:+.3f} {d['comp'][si]:+.3f} "
              f"| {l['r_lang'][si]:5.2f} {l['r_base'][si]:5.2f} {l['warp'][si]:+.3f} {l['comp'][si]:+.3f}")
    print(f"    ncells (mean): L_DIAG={m('diag','ncells'):.1f}  L_LSHAPE={m('Lshape','ncells'):.1f}")
    print("")

    null_q95 = float(np.quantile(shuf_all, NULL_Q))
    print(f"  c2 label-permutation NULL (N_SHUF={N_SHUF}/seed, pooled {len(shuf_all)}):")
    print(f"    warp null: mean={shuf_all.mean():+.3f} q95={null_q95:+.3f} "
          f"max={shuf_all.max():+.3f} min={shuf_all.min():+.3f}")
    print("")

    # ── c1 PRESENCE ───────────────────────────────────────────────────────────
    def all_ge(kind, thr):
        return all(v >= thr for v in per[kind]["warp"]) and m(kind, "warp") >= thr
    c1_diag = all_ge("diag", WARP_MIN)
    c1_lsh = all_ge("Lshape", WARP_MIN)
    c1 = c1_diag and c1_lsh
    print(f"  c1 PRESENCE — CP-WARP >= {WARP_MIN} each seed AND mean, both languages:")
    print(f"     L_DIAG  : per-seed {[round(v,3) for v in per['diag']['warp']]} mean {m('diag','warp'):+.3f} -> {'PASS' if c1_diag else 'FAIL'}")
    print(f"     L_LSHAPE: per-seed {[round(v,3) for v in per['Lshape']['warp']]} mean {m('Lshape','warp'):+.3f} -> {'PASS' if c1_lsh else 'FAIL'}")
    print(f"     -> c1 {'PASS' if c1 else 'FAIL'}")

    # ── c2 EARNED-SHUFFLE ──────────────────────────────────────────────────────
    null_mean_ok = shuf_all.mean() <= CHANCE_TOL
    sep_diag = m("diag", "warp") >= null_q95 + SEP
    sep_lsh = m("Lshape", "warp") >= null_q95 + SEP
    c2 = null_mean_ok and sep_diag and sep_lsh
    print(f"  c2 EARNED-SHUFFLE — null mean <= {CHANCE_TOL} AND each lang >= null-q95 + {SEP}:")
    print(f"     null mean={shuf_all.mean():+.3f} <= {CHANCE_TOL} -> {'PASS' if null_mean_ok else 'FAIL'}")
    print(f"     L_DIAG  mean {m('diag','warp'):+.3f} >= q95+{SEP}={null_q95+SEP:+.3f} -> {'PASS' if sep_diag else 'FAIL'}")
    print(f"     L_LSHAPE mean {m('Lshape','warp'):+.3f} >= q95+{SEP}={null_q95+SEP:+.3f} -> {'PASS' if sep_lsh else 'FAIL'}")
    print(f"     -> c2 {'PASS' if c2 else 'FAIL'}")

    # ── c3 COMPONENT-COUNT ─────────────────────────────────────────────────────
    comp_diag_ok = m("diag", "comp") <= COMP_MAX
    comp_lsh_ok = m("Lshape", "comp") <= COMP_MAX
    c3 = comp_diag_ok and comp_lsh_ok
    print(f"  c3 COMPONENT-COUNT — component-shuffled warp <= {COMP_MAX}, both languages:")
    print(f"     L_DIAG  comp-warp {m('diag','comp'):+.3f} <= {COMP_MAX} -> {'PASS' if comp_diag_ok else 'FAIL'}")
    print(f"     L_LSHAPE comp-warp {m('Lshape','comp'):+.3f} <= {COMP_MAX} -> {'PASS' if comp_lsh_ok else 'FAIL'}")
    print(f"     -> c3 {'PASS' if c3 else 'FAIL'}")
    print("")
    print("=" * 84)

    green = c1 and c2 and c3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — WHORFIAN CATEGORICAL PERCEPTION")
        print("  GENERALIZES TO A 2-D / FEATURAL SPACE as a representational-metric WARP.")
        print("  Both languages warp the learned metric (within-category compression +")
        print("  between-category expansion) above WARP_MIN (c1); a label-permutation null")
        print("  collapses the warp (c2 earned); a component-shuffle collapses it (c3 — the")
        print("  warp lives in the trained 2-D metric, not raw variance). The H_1334 ridge-")
        print("  ALIGN negative is re-read as a boundary-curve grid-geometry artifact: the")
        print("  boundary-agnostic warp shows the effect cleanly for BOTH a diagonal AND an")
        print("  axis-aligned boundary. ENGINE-TRANSFER UNVERIFIED — follow-on. TOY synthetic")
        print("  2-D continuum, 3 seeds; NO human-cognition claim (a_scale_honest_scope).")
        return 0
    if not c1:
        print("VERDICT: 🧱 GENUINE 2-D LIMIT — even the boundary-agnostic warp metric does not")
        print("  clear WARP_MIN at the densest grid. CP does not generalize to 2-D as a metric")
        print("  warp. Honest, NO bar move (c9).")
        return 3
    if c1 and not c2:
        print("VERDICT: 🟠 PARTIAL — 2-D CP warp present (c1) but the label-shuffle null did not")
        print("  collapse (c2): the warp is not cleanly earned. Honest, NO bar move (c9).")
        return 4
    if c1 and c2 and not c3:
        print("VERDICT: 🟠 PARTIAL — 2-D CP warp present (c1) & earned (c2) but the component-")
        print("  shuffle did not collapse it (c3): the warp does not require the trained 2-D")
        print("  metric. Honest, NO bar move (c9).")
        return 5
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
