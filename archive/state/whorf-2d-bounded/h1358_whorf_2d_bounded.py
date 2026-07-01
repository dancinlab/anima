"""
H_1358 — SAPIR-WHORF / 2-D CATEGORICAL PERCEPTION, BOUNDED warp metric.
R3 of H_1343 (🟠 PARTIAL). numpy MIRROR (DIRECTIONAL — engine-transfer UNVERIFIED).

Frozen design: .verdicts/1358_whorf_2d_bounded/FREEZE.txt (pre-registered BEFORE this
scoring; frozen-first, c9 / p7 NO tune-to-green). $0 CPU, gradient-free, 3 seeds
[4334,4335,4336], deterministic. a_no_llm_frame_trap (cognitive-science / categorical-
perception lens, c15) — NOT an LLM recipe, NOT a human-cognition claim.

WHY R3 RE-SPECIFIES THE METRIC (CORRECTION, NOT bar relaxation): H_1343 found the 2-D CP
warp is decisively PRESENT (c1 ✅; diagonal warps as strongly as axis-aligned, refuting
H_1334's grid-geometry read) but its warp metric ratio = mean|Δg|_BETWEEN / mean|Δg|_WITHIN
is SCALE-UNBOUNDED: after training within-|Δg| compresses to ~0, the ratio explodes to ~45,
and a RANDOM carving compresses within-|Δg| too, so the label-shuffle null FLOATED at +9.28
instead of collapsing to chance. R3 replaces the ratio with a BOUNDED separation-AUC ∈[0,1]
(Mann-Whitney-U probability that a random BETWEEN step exceeds a random WITHIN step). Chance =
0.5 is a FIXED constant independent of within-compression, so a label-shuffle null MUST
collapse to 0.5 if the warp is not earned.

p1/p2/p3/p6: the AUC reads ONLY representational distance (|Δ soft posterior|) + the store's
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

AUC_MIN    = 0.70                  # c1 presence
CHANCE_TOL = 0.05                  # c2 |null mean - 0.5| ceiling
SEP        = 0.10                  # c2 separation above null-q95
COMP_TOL   = 0.08                  # c3 |comp-shuffle AUC - 0.5| ceiling
DIAG_TOL   = 0.15                  # c4 |AUC_diag - AUC_Lshape| ceiling
N_SHUF     = 200                   # label-permutation null draws
N_COMP     = 50                    # component-shuffle draws
NULL_Q     = 0.95                  # percentile of shuffle null for the SEP gate
CHANCE     = 0.5                   # bounded-metric chance value


# ── 2-D RBF population code (boundary-AGNOSTIC) — VERBATIM from H_1343 ────────
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
    Verbatim family of H_1334/H_1343. Recall posterior = softmin-weighted vote."""

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


# ── grid + edges (VERBATIM from H_1343) ──────────────────────────────────────
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


# ── BOUNDED warp metric: separation-AUC (Mann-Whitney-U) ──────────────────────
def split_deltas(g, edges, cat):
    """Partition adjacent-pair |Δg| into WITHIN vs BETWEEN by the category partition.
    Returns (within_array, between_array). Boundary-curve-AGNOSTIC."""
    dwithin, dbetween = [], []
    for (i, j) in edges:
        dg = abs(g[i] - g[j])
        if cat[i] == cat[j]:
            dwithin.append(dg)
        else:
            dbetween.append(dg)
    return np.array(dwithin), np.array(dbetween)


def separation_auc(within, between):
    """BOUNDED warp metric: AUC = P(|Δg|_between > |Δg|_within), Mann-Whitney-U rank form.
    AUC ∈ [0,1]; chance = 0.5; AUC -> 1.0 = perfect between-expansion / within-compression.
    Independent of within-compression scale (the H_1343 ratio defect is removed)."""
    nb, nw = len(between), len(within)
    if nb == 0 or nw == 0:
        return 0.5                                   # no separation possible -> chance
    # rank-sum form of Mann-Whitney U (handles ties as 0.5)
    allv = np.concatenate([between, within])
    order = np.argsort(allv, kind="mergesort")
    ranks = np.empty_like(order, dtype=np.float64)
    sorted_v = allv[order]
    i = 0
    N = len(allv)
    while i < N:                                     # average ranks within tie groups
        j = i
        while j + 1 < N and sorted_v[j + 1] == sorted_v[i]:
            j += 1
        avg_rank = 0.5 * (i + j) + 1.0               # 1-based average rank
        ranks[order[i:j + 1]] = avg_rank
        i = j + 1
    rank_between = ranks[:nb].sum()
    u_between = rank_between - nb * (nb + 1) / 2.0    # U statistic for the BETWEEN group
    return float(u_between / (nb * nw))              # = AUC


def cohens_d(within, between):
    """Secondary NON-gating diagnostic: standardized between-vs-within |Δg| effect size."""
    nb, nw = len(between), len(within)
    if nb < 2 or nw < 2:
        return 0.0
    mb, mw = between.mean(), within.mean()
    vb, vw = between.var(ddof=1), within.var(ddof=1)
    sp = np.sqrt(((nb - 1) * vb + (nw - 1) * vw) / (nb + nw - 2))
    return float((mb - mw) / sp) if sp > 1e-12 else 0.0


def fit_posteriors(X, Y, edges):
    cells = VoronoiCells().fit(X, Y, GROW_MAX, SPLIT_PASSES)
    g = np.array([cells.posterior(X[m]) for m in range(len(X))])
    cat = (g >= 0.5).astype(int)                 # store's OWN learned category (no label read)
    return g, cat, len(cells.protos)


def warp_auc(g, cat, edges):
    w, b = split_deltas(g, edges, cat)
    return separation_auc(w, b), cohens_d(w, b)


# ── per-density run ──────────────────────────────────────────────────────────
def run_density(seed, k_rbf, want_controls):
    basis = make_basis(seed, k_rbf)
    pos = make_grid()
    X = np.array([embed(p, basis) for p in pos])
    edges = grid_edges()
    M = len(pos)

    # boundary-AGNOSTIC pre-language baseline coordinate (no carving cut). Reported as a
    # diagnostic only — the bounded AUC needs no baseline subtraction.
    g0 = np.array([0.5 * (pos[m, 0] + pos[m, 1]) for m in range(M)])
    g0 = (g0 - g0.min()) / (g0.max() - g0.min() + 1e-12)

    out = {}
    for kind in ["diag", "Lshape"]:
        Ytrue = np.array([label_of(pos[m], kind) for m in range(M)])
        g_lang, cat_lang, nc = fit_posteriors(X, Ytrue, edges)
        auc, d = warp_auc(g_lang, cat_lang, edges)
        # baseline AUC: language ground-truth partition but the boundary-agnostic g0 metric
        w0, b0 = split_deltas(g0, edges, Ytrue)
        base_auc = separation_auc(w0, b0)
        out[kind] = dict(auc=auc, dcoh=d, base_auc=base_auc, ncells=nc,
                         g_lang=g_lang, cat_lang=cat_lang, X=X, edges=edges, pos=pos, g0=g0,
                         Ytrue=Ytrue)
    if not want_controls:
        return out

    # ── c2 label-permutation null (N_SHUF) at this density ───────────────────
    shuf_rng = np.random.default_rng(seed + 99000 + k_rbf)
    shuf_aucs = []
    for _ in range(N_SHUF):
        Yp = shuf_rng.permutation(out["diag"]["Ytrue"])     # permute one language's labels
        g_s, cat_s, _ = fit_posteriors(X, Yp, edges)
        auc_s, _ = warp_auc(g_s, cat_s, edges)
        shuf_aucs.append(auc_s)
    out["_shuf"] = np.array(shuf_aucs)

    # ── c3 component-shuffle control (N_COMP) ────────────────────────────────
    # tie the BETWEEN/WITHIN partition to a SINGLE randomly-chosen feature component
    # (one RBF basis axis) thresholded at its median, instead of the trained 2-D category.
    comp_rng = np.random.default_rng(seed + 77000 + k_rbf)
    DIM = X.shape[1]
    for kind in ["diag", "Lshape"]:
        g_lang = out[kind]["g_lang"]
        caucs = []
        for _ in range(N_COMP):
            comp = int(comp_rng.integers(0, DIM))
            vals = X[:, comp]
            cat_comp = (vals >= np.median(vals)).astype(int)
            auc_c, _ = warp_auc(g_lang, cat_comp, edges)
            caucs.append(auc_c)
        out[kind]["comp_auc"] = float(np.mean(caucs))
    return out


def main():
    print("H_1358 r3 — SAPIR-WHORF 2-D CATEGORICAL PERCEPTION, BOUNDED warp metric (separation-AUC)")
    print("=" * 88)
    print("BOUNDED WARP = separation-AUC ∈[0,1] = P(|Δposterior|_BETWEEN > |Δposterior|_WITHIN),")
    print("Mann-Whitney-U rank form. CHANCE = 0.5 (FIXED constant, independent of within-compression),")
    print("so a label-shuffle null MUST collapse to 0.5 if the warp is not earned — fixing the")
    print("H_1343 unbounded-ratio defect (null floated +9.28). c2 = label-permutation null")
    print("(N_SHUF=%d); c3 = component-shuffle (N_COMP=%d); c4 = diagonal≈axis under bounded metric." % (N_SHUF, N_COMP))
    print("3 seeds %s, gradient-free, $0 CPU, DIRECTIONAL mirror." % SEEDS)
    print(f"G={G_GRID} ({G_GRID*G_GRID} stim) ladder K_RBF={K_RBF_LADDER} prod={K_RBF_PROD} "
          f"(DIM={K_RBF_PROD*K_RBF_PROD}) diag:u+v>{T_DIAG} L:u>{T_LX}&v>{T_LY}")
    print("")

    # ── density ladder: bounded AUC vs RBF density (mean of 3 seeds) ──────────
    print("  DENSITY LADDER — separation-AUC vs RBF density (mean of 3 seeds):")
    print("    K_RBF  DIM    AUC(L_DIAG)   AUC(L_LSHAPE)")
    for k in K_RBF_LADDER:
        ad, al = [], []
        for seed in SEEDS:
            o = run_density(seed, k, want_controls=False)
            ad.append(o["diag"]["auc"]); al.append(o["Lshape"]["auc"])
        print(f"    {k:3d}  {k*k:4d}    {np.mean(ad):.4f}        {np.mean(al):.4f}")
    print("")

    # ── production density: full controls ─────────────────────────────────────
    per = {kind: dict(auc=[], dcoh=[], base_auc=[], ncells=[], comp=[]) for kind in ["diag", "Lshape"]}
    shuf_pool = []
    for seed in SEEDS:
        o = run_density(seed, K_RBF_PROD, want_controls=True)
        for kind in ["diag", "Lshape"]:
            per[kind]["auc"].append(o[kind]["auc"])
            per[kind]["dcoh"].append(o[kind]["dcoh"])
            per[kind]["base_auc"].append(o[kind]["base_auc"])
            per[kind]["ncells"].append(o[kind]["ncells"])
            per[kind]["comp"].append(o[kind]["comp_auc"])
        shuf_pool.append(o["_shuf"])
    shuf_all = np.concatenate(shuf_pool)        # pooled N_SHUF*3 null

    def m(kind, f):
        return float(np.mean(per[kind][f]))

    print(f"  PRODUCTION density K_RBF={K_RBF_PROD} (DIM={K_RBF_PROD*K_RBF_PROD}) — per-seed detail:")
    print("    seed | L_DIAG: AUC  d(diag)  base  comp | L_LSHAPE: AUC  d(L)  base  comp")
    for si, seed in enumerate(SEEDS):
        d, l = per["diag"], per["Lshape"]
        print(f"    {seed} | {d['auc'][si]:.4f} {d['dcoh'][si]:+.2f}  {d['base_auc'][si]:.3f} {d['comp'][si]:.3f} "
              f"| {l['auc'][si]:.4f} {l['dcoh'][si]:+.2f}  {l['base_auc'][si]:.3f} {l['comp'][si]:.3f}")
    print(f"    ncells (mean): L_DIAG={m('diag','ncells'):.1f}  L_LSHAPE={m('Lshape','ncells'):.1f}")
    print(f"    baseline AUC (diagnostic, expect ~0.5): L_DIAG={m('diag','base_auc'):.3f}  L_LSHAPE={m('Lshape','base_auc'):.3f}")
    print("")

    null_q95 = float(np.quantile(shuf_all, NULL_Q))
    print(f"  c2 label-permutation NULL (N_SHUF={N_SHUF}/seed, pooled {len(shuf_all)}):")
    print(f"    AUC null: mean={shuf_all.mean():.4f} q95={null_q95:.4f} "
          f"max={shuf_all.max():.4f} min={shuf_all.min():.4f}")
    print("")

    # ── c1 PRESENCE ───────────────────────────────────────────────────────────
    def all_ge(kind, thr):
        return all(v >= thr for v in per[kind]["auc"]) and m(kind, "auc") >= thr
    c1_diag = all_ge("diag", AUC_MIN)
    c1_lsh = all_ge("Lshape", AUC_MIN)
    c1 = c1_diag and c1_lsh
    print(f"  c1 PRESENCE — separation-AUC >= {AUC_MIN} each seed AND mean, both languages:")
    print(f"     L_DIAG  : per-seed {[round(v,4) for v in per['diag']['auc']]} mean {m('diag','auc'):.4f} -> {'PASS' if c1_diag else 'FAIL'}")
    print(f"     L_LSHAPE: per-seed {[round(v,4) for v in per['Lshape']['auc']]} mean {m('Lshape','auc'):.4f} -> {'PASS' if c1_lsh else 'FAIL'}")
    print(f"     -> c1 {'PASS' if c1 else 'FAIL'}")

    # ── c2 EARNED-SHUFFLE ──────────────────────────────────────────────────────
    null_chance_ok = abs(shuf_all.mean() - CHANCE) <= CHANCE_TOL
    sep_diag = m("diag", "auc") >= null_q95 + SEP
    sep_lsh = m("Lshape", "auc") >= null_q95 + SEP
    c2 = null_chance_ok and sep_diag and sep_lsh
    print(f"  c2 EARNED-SHUFFLE — |null mean - {CHANCE}| <= {CHANCE_TOL} AND each lang >= null-q95 + {SEP}:")
    print(f"     |null mean {shuf_all.mean():.4f} - {CHANCE}| = {abs(shuf_all.mean()-CHANCE):.4f} <= {CHANCE_TOL} -> {'PASS' if null_chance_ok else 'FAIL'}")
    print(f"     L_DIAG  mean {m('diag','auc'):.4f} >= q95+{SEP}={null_q95+SEP:.4f} -> {'PASS' if sep_diag else 'FAIL'}")
    print(f"     L_LSHAPE mean {m('Lshape','auc'):.4f} >= q95+{SEP}={null_q95+SEP:.4f} -> {'PASS' if sep_lsh else 'FAIL'}")
    print(f"     -> c2 {'PASS' if c2 else 'FAIL'}")

    # ── c3 COMPONENT-COUNT ─────────────────────────────────────────────────────
    comp_diag_ok = abs(m("diag", "comp") - CHANCE) <= COMP_TOL
    comp_lsh_ok = abs(m("Lshape", "comp") - CHANCE) <= COMP_TOL
    c3 = comp_diag_ok and comp_lsh_ok
    print(f"  c3 COMPONENT-COUNT — |component-shuffle AUC - {CHANCE}| <= {COMP_TOL}, both languages:")
    print(f"     L_DIAG  comp-AUC {m('diag','comp'):.4f} (|Δ|={abs(m('diag','comp')-CHANCE):.4f}) <= {COMP_TOL} -> {'PASS' if comp_diag_ok else 'FAIL'}")
    print(f"     L_LSHAPE comp-AUC {m('Lshape','comp'):.4f} (|Δ|={abs(m('Lshape','comp')-CHANCE):.4f}) <= {COMP_TOL} -> {'PASS' if comp_lsh_ok else 'FAIL'}")
    print(f"     -> c3 {'PASS' if c3 else 'FAIL'}")

    # ── c4 DIAGONAL ────────────────────────────────────────────────────────────
    diag_gap = abs(m("diag", "auc") - m("Lshape", "auc"))
    c4_gap_ok = diag_gap <= DIAG_TOL
    c4_both = (m("diag", "auc") >= AUC_MIN) and (m("Lshape", "auc") >= AUC_MIN)
    c4 = c4_gap_ok and c4_both
    print(f"  c4 DIAGONAL — |AUC_diag - AUC_Lshape| <= {DIAG_TOL} AND both >= {AUC_MIN}:")
    print(f"     |{m('diag','auc'):.4f} - {m('Lshape','auc'):.4f}| = {diag_gap:.4f} <= {DIAG_TOL} -> {'PASS' if c4_gap_ok else 'FAIL'}")
    print(f"     both >= {AUC_MIN} -> {'PASS' if c4_both else 'FAIL'}")
    print(f"     -> c4 {'PASS' if c4 else 'FAIL'}")
    print("")
    print("=" * 88)

    green = c1 and c2 and c3 and c4
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — WHORFIAN 2-D CATEGORICAL PERCEPTION")
        print("  CLEARS ALL CONTROLS under a BOUNDED warp metric. The 2-D CP warp is PRESENT for")
        print("  both languages (c1, separation-AUC >= %.2f); the label-shuffle null COLLAPSES to" % AUC_MIN)
        print("  chance 0.5 (c2 — the H_1343 unbounded-ratio defect is FIXED by the bounded AUC);")
        print("  component-shuffle collapses to chance (c3 — the warp lives in the trained 2-D")
        print("  metric); and the DIAGONAL warps comparably to the axis-aligned boundary (c4 —")
        print("  preserving the H_1343 load-bearing diagonal=axis finding that refutes H_1334's")
        print("  grid-geometry read). ENGINE-TRANSFER UNVERIFIED — follow-on. TOY synthetic 2-D")
        print("  continuum, 3 seeds; NO human-cognition claim (a_scale_honest_scope).")
        return 0
    if not c1:
        print("VERDICT: 🧱 GENUINE 2-D LIMIT — even the BOUNDED warp metric does not clear AUC_MIN.")
        print("  CP does not generalize to 2-D as a metric warp. Honest, NO bar move (c9).")
        return 3
    if not c2:
        print("VERDICT: 🧱 DEEPER LIMIT — the label-shuffle null STILL floats under the BOUNDED")
        print("  metric: the warp is present (c1) but not cleanly label-earned even with a bounded")
        print("  chance-0.5 readout (metric-space-blob is deeper than the ratio). NO bar move (c9).")
        return 4
    if not c3:
        print("VERDICT: 🟠 PARTIAL — bounded warp present (c1) & earned (c2) but the component-")
        print("  shuffle did not collapse to chance (c3): warp not isolated to the trained 2-D")
        print("  metric. Honest, NO bar move (c9).")
        return 5
    if not c4:
        print("VERDICT: 🟠 PARTIAL — bounded warp present/earned/component-isolated but diagonal and")
        print("  axis-aligned AUC differ beyond DIAG_TOL (c4): asymmetry under the bounded metric.")
        print("  Honest, NO bar move (c9).")
        return 6
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
