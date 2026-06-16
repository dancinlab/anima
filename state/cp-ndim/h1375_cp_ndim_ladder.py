"""
H_1375 — CP DIMENSIONAL LADDER: does move-the-cells relocation survive as feature-space dim D grows?
R1 numpy MIRROR (DIRECTIONAL — engine-transfer UNVERIFIED). User direction: "2d 말고도 차원늘려봐".

Frozen design: .verdicts/1375_cp_ndim_ladder/FREEZE.txt (pre-registered BEFORE this scoring;
frozen-first, c9/c16/p7, NO tune-to-green). $0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335], p7.
a_no_llm_frame_trap / a_break_the_wall (developmental-plasticity + curse-of-dimensionality lens, c15)
— NOT an LLM recipe, NOT a human-cognition claim.

THE QUESTION: H_1360 (🟢, 1-D) + H_1369 (🟢, 2-D axis-aligned) proved CARVING RELOCATION IS
MOVE-THE-CELLS — drifting residual phase-1 prototypes toward the moved boundary lands a coherent,
concentrated discrimination ridge AT the moved boundary, where split-only stays short. Does it
SURVIVE up a DIMENSIONAL ladder D ∈ {2,3,4,6,8}? The TRUE boundary is a (D-1)-dim HYPERPLANE
cat = <w,x> > c (w = fixed generic unit normal, held constant orientation; ONLY D varies). The cells
relocate along the normal w toward the moved hyperplane c_A → c_A'. The curse of dimensionality
(volume concentration, distance flattening) at constant N could break the cell-concentration that
makes relocation coherent. Is move-the-cells DIMENSION-INVARIANT, or is there a smallest D* break?

Monte-Carlo sample (N=400 points) replaces the full grid (infeasible past D≈4); ridge concentration
is measured ON THE SAMPLED CLOUD (stated honestly). REUSES family machinery: RBF population code
(H_1343), error-targeted SPLIT-ONLY Voronoi growth (p8, H_1360), softmin-vote posterior, geometric
RE-PACK (H_1360/H_1369). The ONLY new piece is the D-dim lift + drift along the boundary NORMAL.

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary at test; the
re-pack keys on a cell's BIRTH PHASE + own D-dim source position (structural, NO injected target /
persona / RLHF); labels enter ONLY at training. NO-RETRAIN + SHUFFLE = anti-Goodhart discriminators;
SPLIT-ONLY (eta=0.0) = the H_1364 ablation isolating the geometric drift as the lever.
"""
import numpy as np

# ── frozen constants (from FREEZE.txt) ───────────────────────────────────────
SEEDS       = [4333, 4334, 4335]
D_LADDER    = [2, 3, 4, 6, 8]
N           = 400                  # FIXED Monte-Carlo sample size across ALL D (curse stressor)
M_CENTERS   = 64                   # FIXED RBF center count across D (LOW/fixed density)
GROW1       = 48                   # phase-1 split budget (FIXED LOW, every arm & every D)
GROW2       = 48                   # phase-2 split budget (FIXED LOW, NO inflation)
BETA_POST   = 18.0                 # softmin posterior temperature (family verbatim)
REPACK_ETA  = 0.15                 # FROZEN gate value (same as H_1360/H_1369)
KNN_DISC    = 6                    # discrimination-field kNN (D-dim analog of 2-D 4-grid-neighbors)

# frozen bar thresholds (from FREEZE.txt)
RELOC_TOL    = 0.18   # c1: |ridge_tau - 2/3| on the span-NORMALIZED normal coordinate
COH_MIN      = 0.50   # c2: RE-PACK mean COH_D
COH_SEP      = 0.10   # c2/c4: RE-PACK vs SPLIT-ONLY separation
SHUF_COH_MAX = 0.20   # c3: SHUFFLE mean COH_D collapse
TAU_STD_REF  = 0.20   # COH_D ridge tau-spread reference (frozen)

REPACK_LADDER = [0.10, 0.15, 0.25]   # NON-GATING knife-edge diagnostic; gate=0.15 only


# ── D-dim RBF population code (boundary-AGNOSTIC; H_1343 family lifted to D) ──
def make_basis(seed, D):
    rb = np.random.default_rng(seed + 7000)
    centers = rb.uniform(0.0, 1.0, size=(M_CENTERS, D))      # (M_CENTERS, D) sampled centers
    width = float(rb.uniform(0.18, 0.24))                    # per-seed width jitter (wider for D-dim)
    return {"centers": centers, "width": width, "D": D}


def embed(x, basis):
    centers, width = basis["centers"], basis["width"]
    d2 = ((np.asarray(x)[None, :] - centers) ** 2).sum(axis=1)
    v = np.exp(-d2 / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def make_cloud(seed, D):
    rc = np.random.default_rng(seed + 9000)
    return rc.uniform(0.0, 1.0, size=(N, D))                 # (N, D) Monte-Carlo stimulus cloud


def normal_of(D):
    """FIXED GENERIC unit normal = all-ones / sqrt(D) (same generic orientation at every D)."""
    w = np.ones(D, dtype=np.float64)
    return w / np.linalg.norm(w)


def cut_levels(cloud, w):
    """Place c_A, c_A' at 1/3, 2/3 of the [5th,95th]-pctile span of the normal coord t=<w,x>.
    Returns (c_A, c_A2, t_lo, t_hi) — frozen per (D,seed), identical across arms."""
    t = cloud @ w
    t_lo, t_hi = float(np.percentile(t, 5)), float(np.percentile(t, 95))
    span = t_hi - t_lo
    c_A  = t_lo + (1.0 / 3.0) * span
    c_A2 = t_lo + (2.0 / 3.0) * span
    return c_A, c_A2, t_lo, t_hi


def label_of(cloud, w, c):
    """TRUE partition: cat = int(<w,x> > c). Boundary is the hyperplane <w,x>=c."""
    return (cloud @ w > c).astype(int)


# ── Voronoi/immune store: split-only growth + geometric re-pack along the normal ──
class RepackCellsND:
    def __init__(self, w, c_new, eta=0.0, basis=None):
        self.protos = []
        self.labels = []
        self.src = []          # source D-dim position per cell (parallel to protos)
        self.phase = []        # 1 = phase-1 (re-packs), 2 = phase-2 (fixed)
        self.eta = eta
        self.basis = basis
        self.w = w
        self.c_new = c_new
        self.n_phase1 = 0

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit_phase1(self, X, Y, cloud, grow):
        """Error-targeted SPLIT-only growth from a single seed cell (family verbatim)."""
        M = len(X)
        c0 = X.mean(axis=0)
        n = np.linalg.norm(c0)
        c0 = c0 / n if n > 0 else c0
        seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
        self.protos = [c0]
        self.labels = [int(Y[seed_stim])]
        self.src = [cloud[seed_stim].astype(np.float64).copy()]
        self.phase = [1]
        for _ in range(grow):
            if len(self.protos) >= 1 + grow:
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
            self.src.append(cloud[s].astype(np.float64).copy())
            self.phase.append(1)
        self.n_phase1 = len(self.protos)
        return self

    def _repack_phase1(self):
        """Drift every phase-1 cell ALONG THE NORMAL w toward c_new (in-plane fixed), clamp at
        c_new, re-embed at the drifted D-dim position, re-read label from the new hyperplane."""
        if self.eta <= 0.0:
            return
        for i in range(self.n_phase1):
            x_i = self.src[i]
            t_i = float(self.w @ x_i)
            t_new = t_i + self.eta * (self.c_new - t_i)
            if (self.c_new - t_i) >= 0:
                t_new = min(t_new, self.c_new)
            else:
                t_new = max(t_new, self.c_new)
            x_new = x_i + (t_new - t_i) * self.w        # move ONLY along the normal
            self.src[i] = x_new
            self.protos[i] = embed(x_new, self.basis)
            self.labels[i] = int(self.w @ x_new > self.c_new)

    def fit_phase2(self, X, Y2, cloud, grow):
        """Phase-2 re-growth on the moved labels (split-only, SAME store, NO reset) with a geometric
        re-pack of the residual phase-1 cells after EACH split. New cells are phase-2 (no drift)."""
        M = len(X)
        splits = 0
        for _ in range(grow):
            if splits >= grow:
                break
            owners = np.array([self._owner(X[m])[0] for m in range(M)])
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y2)[0]
            if len(mism) == 0:
                self._repack_phase1()   # keep migrating the residual even with no error
                break
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy())
            self.labels.append(int(Y2[s]))
            self.src.append(cloud[s].astype(np.float64).copy())
            self.phase.append(2)
            splits += 1
            self._repack_phase1()       # MOVE the residual phase-1 cells one step
        return self

    def posterior(self, key):
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        w = np.exp(-BETA_POST * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


# ── D-dim discrimination field (kNN), ridge, relocation + bounded concentration COH_D ─────
def knn_index(cloud):
    """Precompute the KNN_DISC nearest-neighbor indices for each cloud point (excl self)."""
    M = len(cloud)
    nbr = np.zeros((M, KNN_DISC), dtype=int)
    for m in range(M):
        d2 = ((cloud - cloud[m]) ** 2).sum(axis=1)
        order = np.argsort(d2)
        nbr[m] = order[1:1 + KNN_DISC]
    return nbr


def discrim_field(cells, X, nbr):
    """D(node) = max |Δposterior| over its KNN_DISC nearest neighbors (D-dim analog of the 2-D
    4-grid-neighbor |Δposterior|; kNN adjacency replaces the lattice since the cloud is sampled)."""
    P = np.array([cells.posterior(X[m]) for m in range(len(X))])
    Dfield = np.zeros(len(X))
    for m in range(len(X)):
        Dfield[m] = float(np.max(np.abs(P[m] - P[nbr[m]])))
    return Dfield


def ridge_mask(Dfield):
    mx = Dfield.max()
    if mx <= 0:
        return np.zeros_like(Dfield, dtype=bool)
    return Dfield >= 0.5 * mx          # same 0.5-of-own-peak rule as H_1369


def ridge_tau(Dfield, cloud, w, t_lo, t_hi):
    """Span-NORMALIZED normal coordinate of the ridge centroid: tau = (t - t_lo)/(t_hi - t_lo),
    averaged over ridge nodes (the relocation metric, comparable across D)."""
    mask = ridge_mask(Dfield)
    if mask.sum() == 0:
        return float("nan")
    t = cloud[mask] @ w
    tau = (t - t_lo) / (t_hi - t_lo)
    return float(tau.mean())


def coh_d(Dfield, cloud, w, t_lo, t_hi):
    """COH_D in [0,1] = t_conc * (1 - ridge_frac). High = a THIN ridge concentrated at one normal
    coordinate (a single coherent hyperplane slab); low = a cloud-filling smear. In-plane (D-1)
    spread NOT scored (a coherent hyperplane ridge legitimately spans all in-plane directions)."""
    mask = ridge_mask(Dfield)
    n = int(mask.sum())
    if n == 0:
        return 0.0
    ridge_frac = n / len(cloud)
    t = cloud[mask] @ w
    tau = (t - t_lo) / (t_hi - t_lo)
    tau_std = float(tau.std())
    t_conc = 1.0 - min(1.0, tau_std / TAU_STD_REF)
    return float(t_conc * (1.0 - ridge_frac))


# ── one arm (at fixed D, seed) ────────────────────────────────────────────────
def run_arm(seed, D, eta, kind, retrain=True, whiten=False):
    """kind='A2' moved hyperplane | 'shuffle' permuted phase-2 labels. retrain=False = NO-RETRAIN.
    whiten=True = a_break_the_wall fallback: z-score the embedding per feature before owner/posterior
    distances (only invoked if a D breaks; frozen-first, re-scores the SAME bars)."""
    basis = make_basis(seed, D)
    cloud = make_cloud(seed, D)
    w = normal_of(D)
    c_A, c_A2, t_lo, t_hi = cut_levels(cloud, w)
    X = np.array([embed(cloud[m], basis) for m in range(N)])

    if whiten:
        mu, sd = X.mean(axis=0), X.std(axis=0) + 1e-9
        Xw = (X - mu) / sd
    else:
        Xw, mu, sd = X, None, None

    def emb_for_store(xpos):
        e = embed(xpos, basis)
        return (e - mu) / sd if whiten else e

    Y_A = label_of(cloud, w, c_A)
    cells = RepackCellsND(w, c_A2, eta=eta, basis=basis)
    # patch embed used by the store to the whitened space when requested
    if whiten:
        cells._emb = emb_for_store
        # monkey-route: re-embedding inside re-pack must also whiten
        orig_repack = cells._repack_phase1
        def _wrepack():
            if cells.eta <= 0.0:
                return
            for i in range(cells.n_phase1):
                x_i = cells.src[i]; t_i = float(cells.w @ x_i)
                t_new = t_i + cells.eta * (cells.c_new - t_i)
                t_new = min(t_new, cells.c_new) if (cells.c_new - t_i) >= 0 else max(t_new, cells.c_new)
                x_new = x_i + (t_new - t_i) * cells.w
                cells.src[i] = x_new
                cells.protos[i] = emb_for_store(x_new)
                cells.labels[i] = int(cells.w @ x_new > cells.c_new)
        cells._repack_phase1 = _wrepack

    cells.fit_phase1(Xw, Y_A, cloud, GROW1)
    if retrain:
        if kind == "A2":
            Y2 = label_of(cloud, w, c_A2)
        elif kind == "shuffle":
            sh = np.random.default_rng(seed + 4)
            Y2 = sh.integers(0, 2, size=N)
        else:
            raise ValueError(kind)
        cells.fit_phase2(Xw, Y2, cloud, GROW2)

    nbr = run_arm._nbr_cache.get((seed, D))
    if nbr is None:
        nbr = knn_index(cloud)
        run_arm._nbr_cache[(seed, D)] = nbr
    Dfield = discrim_field(cells, Xw, nbr)
    return dict(
        ridge_tau=ridge_tau(Dfield, cloud, w, t_lo, t_hi),
        coh=coh_d(Dfield, cloud, w, t_lo, t_hi),
        nc=len(cells.protos),
    )
run_arm._nbr_cache = {}


def score_D(D, whiten=False):
    """Score all 4 arms over 3 seeds at a fixed D. Returns the per-D summary dict + bar booleans."""
    rp_du, rp_coh, so_du, so_coh, sh_coh, nr_du = [], [], [], [], [], []
    per_seed = []
    for seed in SEEDS:
        so = run_arm(seed, D, eta=0.0, kind="A2", whiten=whiten)
        rp = run_arm(seed, D, eta=REPACK_ETA, kind="A2", whiten=whiten)
        sh = run_arm(seed, D, eta=REPACK_ETA, kind="shuffle", whiten=whiten)
        nr = run_arm(seed, D, eta=0.0, kind="A2", retrain=False, whiten=whiten)
        so_du.append(abs(so["ridge_tau"] - 2.0 / 3.0)); so_coh.append(so["coh"])
        rp_du.append(abs(rp["ridge_tau"] - 2.0 / 3.0)); rp_coh.append(rp["coh"])
        sh_coh.append(sh["coh"]); nr_du.append(abs(nr["ridge_tau"] - 1.0 / 3.0))
        per_seed.append((seed, so, rp, sh, nr))
    rp_du_m, rp_coh_m = float(np.mean(rp_du)), float(np.mean(rp_coh))
    so_du_m, so_coh_m = float(np.mean(so_du)), float(np.mean(so_coh))
    sh_coh_m, nr_du_m = float(np.mean(sh_coh)), float(np.mean(nr_du))

    c1 = all(d <= RELOC_TOL for d in rp_du)                                  # RELOCATION
    c2 = (rp_coh_m >= COH_MIN) and (rp_coh_m >= so_coh_m + COH_SEP)          # COH_D concentration
    c3 = sh_coh_m <= SHUF_COH_MAX                                            # EARNED (shuffle)
    c4 = (so_du_m > RELOC_TOL) or (so_coh_m < rp_coh_m - COH_SEP)            # DISTINCT vs split-only
    green = c1 and c2 and c3 and c4
    return dict(D=D, whiten=whiten, rp_du=rp_du, rp_du_m=rp_du_m, rp_coh=rp_coh, rp_coh_m=rp_coh_m,
                so_du_m=so_du_m, so_coh=so_coh, so_coh_m=so_coh_m, sh_coh=sh_coh, sh_coh_m=sh_coh_m,
                nr_du_m=nr_du_m, c1=c1, c2=c2, c3=c3, c4=c4, green=green, per_seed=per_seed)


def main():
    print("H_1375 R1 — CP DIMENSIONAL LADDER: does move-the-cells survive as dim D grows?")
    print("=" * 96)
    print('USER DIRECTION (verbatim): "2d 말고도 차원늘려봐" — push move-the-cells BEYOND 2-D up a D-ladder.')
    print("D-ladder = {2,3,4,6,8}; TRUE boundary = hyperplane <w,x>=c (w=ones/√D, FIXED orientation,")
    print("ONLY D varies); cells drift along the normal w toward the moved hyperplane c_A→c_A'.")
    print(f"N={N} Monte-Carlo points (FIXED across D = curse-of-dim stressor) · M_CENTERS={M_CENTERS} ·")
    print(f"GROW1={GROW1} GROW2={GROW2} eta={REPACK_ETA} kNN_DISC={KNN_DISC} seeds={SEEDS}")
    print("metrics: ridge_tau = span-normalized normal coord of ridge centroid (RELOCATES, c_A→1/3,")
    print("         c_A'→2/3); COH_D = t_conc·(1-ridge_frac) bounded concentration (generalizes COH2D)")
    print("HONEST: ridge concentration measured on the SAMPLED cloud, not an exhaustive lattice.")
    print("")

    print(f"FROZEN BARS (per D): c1 RE-PACK |ridge_tau-2/3|<={RELOC_TOL} all 3 seeds · c2 RE-PACK COH_D")
    print(f"  >={COH_MIN} AND >=SPLIT-ONLY+{COH_SEP} · c3 SHUFFLE COH_D<={SHUF_COH_MAX} · c4 SPLIT-ONLY short/less-conc")
    print("=" * 96)

    rows = []
    for D in D_LADDER:
        r = score_D(D)
        rows.append(r)
        print(f"\n── D = {D} ──────────────────────────────────────────────────────────────────────")
        for (seed, so, rp, sh, nr) in r["per_seed"]:
            print(f"  seed {seed}: SPLIT-ONLY tau={so['ridge_tau']:.3f} coh={so['coh']:.3f} (nc={so['nc']}) | "
                  f"RE-PACK tau={rp['ridge_tau']:.3f} coh={rp['coh']:.3f} (nc={rp['nc']}) | "
                  f"shuffle coh={sh['coh']:.3f} | no-retrain tau={nr['ridge_tau']:.3f}")
        print(f"  MEAN: RE-PACK |tau-2/3|={r['rp_du_m']:.3f} COH_D={r['rp_coh_m']:.3f} | "
              f"SPLIT-ONLY |tau-2/3|={r['so_du_m']:.3f} COH_D={r['so_coh_m']:.3f} | "
              f"SHUFFLE COH_D={r['sh_coh_m']:.3f} | NO-RETRAIN |tau-1/3|={r['nr_du_m']:.3f}")
        print(f"  c1 RELOCATION {'PASS' if r['c1'] else 'FAIL'} (per-seed {[round(d,3) for d in r['rp_du']]}<={RELOC_TOL}) · "
              f"c2 COH_D {'PASS' if r['c2'] else 'FAIL'} ({r['rp_coh_m']:.3f}>={COH_MIN} & >=split {r['so_coh_m']:.3f}+{COH_SEP}) · "
              f"c3 EARNED {'PASS' if r['c3'] else 'FAIL'} · c4 DISTINCT {'PASS' if r['c4'] else 'FAIL'}")
        print(f"  => D={D}: {'🟢 PASS' if r['green'] else '🧱 FAIL'}")

    print("\n" + "=" * 96)
    print("LADDER CURVE (per D):")
    print(f"  {'D':>3} | {'RE-PACK|tau-2/3|':>16} | {'RE-PACK COH_D':>13} | {'SPLIT COH_D':>11} | "
          f"{'SHUF COH_D':>10} | {'c1c2c3c4':>9} | verdict")
    for r in rows:
        bars = f"{int(r['c1'])}{int(r['c2'])}{int(r['c3'])}{int(r['c4'])}"
        print(f"  {r['D']:>3} | {r['rp_du_m']:>16.3f} | {r['rp_coh_m']:>13.3f} | {r['so_coh_m']:>11.3f} | "
              f"{r['sh_coh_m']:>10.3f} | {bars:>9} | {'🟢 PASS' if r['green'] else '🧱 FAIL'}")

    # NON-GATING re-pack ladder (gate at eta=0.15) at the HIGHEST D as a knife-edge check
    print("\n[NON-GATING diagnostic] RE-PACK-LADDER at D=8 (gate scored ONLY at eta=0.15):")
    for e in REPACK_LADDER:
        ds, cs = [], []
        for seed in SEEDS:
            rr = run_arm(seed, 8, eta=e, kind="A2")
            ds.append(abs(rr["ridge_tau"] - 2.0 / 3.0)); cs.append(rr["coh"])
        tag = "  <-- FROZEN GATE" if abs(e - REPACK_ETA) < 1e-9 else ""
        print(f"   eta={e:.2f}: |tau-2/3| mean={np.mean(ds):.3f}  COH_D mean={np.mean(cs):.3f}{tag}")

    print("\n" + "=" * 96)
    all_green = all(r["green"] for r in rows)
    if all_green:
        print("LADDER VERDICT: 🟢 DIMENSION-INVARIANT — move-the-cells relocation SURVIVES across the")
        print(f"  ENTIRE ladder D ∈ {D_LADDER}. c1∧c2∧c3∧c4 hold at every D. The 1-D (H_1360) / 2-D")
        print("  (H_1369) move-the-cells win GENERALIZES to higher dimension: residual phase-1 cells")
        print("  drift along the boundary normal to track the moved hyperplane, landing a coherent")
        print("  concentrated ridge AT c_A', where split-only stays short. The curse of dimensionality")
        print("  (constant N, growing D) does NOT break the cell-concentration. ENGINE-TRANSFER")
        print("  UNVERIFIED. TOY synthetic D-dim cloud, 3 seeds, fixed generic normal. NO bar moved (c9/p7).")
        return 0

    # smallest D* where c1 (RELOCATION) or c2 (COH_D) fails
    dstar = next((r["D"] for r in rows if not (r["c1"] and r["c2"])), None)
    print(f"LADDER VERDICT: 🧱 BREAKS-AT-D* = {dstar} — move-the-cells is DIMENSION-BOUNDED. The first")
    print(f"  D where RELOCATION (c1) or COH_D (c2) fails is D*={dstar}. Per-D curve above is the headline.")
    print("  a_break_the_wall: re-scoring the SAME frozen bars under a WHITENED metric (z-score the")
    print("  embedding per feature, removing raw-distance flattening) — frozen-first, N & D unchanged:")
    print("  " + "-" * 92)
    wrows = []
    for D in D_LADDER:
        rw = score_D(D, whiten=True)
        wrows.append(rw)
        bars = f"{int(rw['c1'])}{int(rw['c2'])}{int(rw['c3'])}{int(rw['c4'])}"
        print(f"   D={rw['D']} [WHITEN]: RE-PACK |tau-2/3|={rw['rp_du_m']:.3f} COH_D={rw['rp_coh_m']:.3f} "
              f"SPLIT COH_D={rw['so_coh_m']:.3f} SHUF COH_D={rw['sh_coh_m']:.3f} "
              f"bars={bars} {'🟢' if rw['green'] else '🧱'}")
    w_all_green = all(r["green"] for r in wrows)
    w_dstar = next((r["D"] for r in wrows if not (r["c1"] and r["c2"])), None)
    print("  " + "-" * 92)
    if w_all_green:
        print("  WHITEN BREAKTHROUGH: under the whitened metric the WHOLE ladder passes → the raw break")
        print(f"  at D*={dstar} was a METRIC-GEOMETRY (distance-flattening) artifact, NOT an intrinsic")
        print("  dimension ceiling. Move-the-cells is dimension-invariant in a whitened feature space.")
        print("  TERMINAL: 🟢 DIMENSION-INVARIANT (whitened metric). NO bar moved (c9/c16/p7).")
        return 0
    print(f"  WHITEN did NOT rescue (whitened-break-at D*={w_dstar}) → the break at D*={dstar} is")
    print("  INTRINSIC (constant-N curse-of-dimensionality genuinely flattens the cell-concentration).")
    print(f"  TERMINAL: 🧱 BREAKS-AT-D* = {dstar} (intrinsic) — move-the-cells is dimension-bounded.")
    print("  Honest, NO bar move (c9/c16/p7). ENGINE-TRANSFER UNVERIFIED. TOY synthetic D-dim cloud.")
    return 3


if __name__ == "__main__":
    import sys
    sys.exit(main())
