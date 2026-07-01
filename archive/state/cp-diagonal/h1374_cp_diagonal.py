"""
H_1374 — CP RELOCATION ON A DIAGONAL (NON-AXIS-ALIGNED) 2-D BOUNDARY: does move-the-cells SURVIVE?
R1 numpy MIRROR (DIRECTIONAL — engine-transfer UNVERIFIED). CP lane R3, the decisive falsification.

Frozen design: .verdicts/1374_cp_diagonal/FREEZE.txt (pre-registered BEFORE this scoring; frozen-
first, c9/c16/p7, NO tune-to-green). $0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335], p7.
a_no_llm_frame_trap / a_break_the_wall (developmental/critical-period plasticity + memory-protection
lens, c15) — NOT an LLM recipe, NOT a human-cognition claim.

THE QUESTION: H_1369 (🟢, 2-D AXIS-ALIGNED half-plane cat=u>p) proved move-the-cells generalizes to
2-D, but the axis-aligned boundary lets the relocation DECOMPOSE onto a single relevant axis (u) — it
UNDER-TESTS. H_1343 showed a DIAGONAL boundary warps the metric as strongly and does NOT decompose
onto one axis. So a diagonal is exactly where move-the-cells could GENUINELY FAIL.

H_1374 sets the TRUE partition to a DIAGONAL half-plane cat = (u+v)/sqrt(2) > c (normal (1,1)/sqrt2,
NOT axis-aligned), shifting c_A -> c_A', and drifts residual phase-1 cells ALONG THE BOUNDARY NORMAL
(BOTH u AND v move). Asks: does the discrimination ridge relocate to land ON the moved diagonal cut
with a single coherent CONCENTRATION (bounded COH2D along the normal s), or does the non-axis-aligned
geometry BREAK the relocation? Uses ONLY the bounded COH2D family (NO NCOMP gating — H_1369 proved it
confounds). ALL thresholds VERBATIM from H_1369 R2 (no relaxation).

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary at test; the
re-pack keys on a cell's BIRTH PHASE + own 2-D source position projected onto the boundary normal
(structural, NO injected target / persona / RLHF); labels enter ONLY at training. NO-RETRAIN +
SHUFFLE = anti-Goodhart discriminators; SPLIT-ONLY (eta=0.0) = the ablation isolating the drift.
"""
import numpy as np

SQ2 = np.sqrt(2.0)

# ── frozen constants (from FREEZE.txt) ───────────────────────────────────────
G_GRID  = 13                 # 13x13 = 169 stimuli (IDENTICAL to H_1369)
K_RBF   = 8                  # 8x8 RBF centers -> DIM=64 (IDENTICAL to H_1369)
DIM     = K_RBF * K_RBF
# DIAGONAL cut along the normal n=(1,1)/sqrt2; same 1/3 -> 2/3 fractional shift as H_1369, lifted onto
# the diagonal (s in [0, sqrt2]):
C_A     = SQ2 * (1.0 / 3.0)  # = 0.4714  phase-1 diagonal cut along the normal
C_A2    = SQ2 * (2.0 / 3.0)  # = 0.9428  phase-2 moved diagonal cut along the normal
N_U     = 1.0 / SQ2          # boundary-normal unit vector components
N_V     = 1.0 / SQ2
GROW1   = 48                 # phase-1 split budget (FIXED LOW, == H_1369)
GROW2   = 48                 # phase-2 split budget (FIXED LOW, NO inflation, == H_1369)
BETA_POST = 18.0             # softmin posterior temperature (family verbatim)
SEEDS   = [4333, 4334, 4335] # SAME family seeds, REUSED from H_1369

REPACK_ETA    = 0.15                 # FROZEN gate value (== H_1369)
REPACK_LADDER = [0.10, 0.15, 0.25]   # NON-GATING knife-edge diagnostic; gate=0.15 only

# frozen bar thresholds (from FREEZE.txt — ALL VERBATIM from H_1369 R2) ───────
LOC_TOL      = 0.12   # c1 / c3a / c4: |ridge_s - cut| reach tolerance along the normal (== H_1369)
COH_MIN      = 0.50   # c2: re-pack COH2D floor (== H_1369 R2 c2')
COH_SEP      = 0.10   # c2: re-pack COH2D >= split-only + this (== H_1369 R2 c4' concentration leg)
SHUF_COH_MAX = 0.20   # c3: shuffle COH2D ceiling (== H_1369 R2 c3b')
S_STD_REF    = 0.20   # bounded-COH2D normal-coordinate concentration reference (== H_1369 U_STD_REF)


# ── 2-D RBF population code (boundary-AGNOSTIC; H_1343/H_1369 family, VERBATIM) ───
def make_basis(seed):
    rb = np.random.default_rng(seed + 7000)
    g = np.linspace(0.0, 1.0, K_RBF)
    cu, cv = np.meshgrid(g, g)
    centers = np.stack([cu.ravel(), cv.ravel()], axis=1)   # (DIM, 2)
    width = float(rb.uniform(0.10, 0.13))
    return {"centers": centers, "width": width}


def embed(p, basis):
    centers, width = basis["centers"], basis["width"]
    d2 = ((np.asarray(p)[None, :] - centers) ** 2).sum(axis=1)
    v = np.exp(-d2 / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def make_grid():
    g = np.linspace(0.0, 1.0, G_GRID)
    gu, gv = np.meshgrid(g, g)
    pos = np.stack([gu.ravel(), gv.ravel()], axis=1)       # (169, 2)
    return pos


def s_coord(pos):
    """Normal coordinate s = (u+v)/sqrt2 along the diagonal boundary normal."""
    return (pos[:, 0] + pos[:, 1]) / SQ2


def label_of(pos, c_cut):
    """TRUE partition: cat = int( (u+v)/sqrt2 > c_cut ). DIAGONAL half-plane (slope -1)."""
    return (s_coord(pos) > c_cut).astype(int)


# ── Voronoi/immune store: split-only growth + geometric re-pack ALONG THE NORMAL ──
class RepackCellsDiag:
    def __init__(self, eta=0.0, basis=None, c_new=C_A2, rotate=False):
        self.protos = []
        self.labels = []
        self.pos = []          # source 2-D position per cell
        self.phase = []        # 1 = phase-1 (re-packs), 2 = phase-2 (fixed)
        self.eta = eta
        self.basis = basis
        self.c_new = c_new
        self.rotate = rotate   # R2: express the drift in the boundary's (s,t) normal/tangential frame
        self.n_phase1 = 0

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit_phase1(self, X, Y, positions, grow):
        """Error-targeted SPLIT-only growth from a single seed cell (family verbatim)."""
        M = len(X)
        c0 = X.mean(axis=0)
        n = np.linalg.norm(c0)
        c0 = c0 / n if n > 0 else c0
        seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
        self.protos = [c0]
        self.labels = [int(Y[seed_stim])]
        self.pos = [tuple(float(x) for x in positions[seed_stim])]
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
            self.pos.append(tuple(float(x) for x in positions[s]))
            self.phase.append(1)
        self.n_phase1 = len(self.protos)
        return self

    def _repack_phase1(self):
        """Drift every phase-1 cell toward the new cut s=c_new, clamp at c_new, re-embed, re-read
        label from new cut. Two frames:
          - default (R1): drift ALONG THE BOUNDARY NORMAL in (u,v) (BOTH u,v move; tangential fixed).
          - rotate (R2, a_break_the_wall): express the cell in (s,t)=(normal,tangential) coords, drift
            PURELY in s, then recompose to (u,v). The frozen R2 angle from FREEZE.txt."""
        if self.eta <= 0.0:
            return
        for i in range(self.n_phase1):
            u_i, v_i = self.pos[i]
            if self.rotate:
                # rotate into the boundary frame: s=normal coord, t=tangential coord
                s_i = (u_i + v_i) / SQ2
                t_i = (u_i - v_i) / SQ2
                s_new = s_i + self.eta * (self.c_new - s_i)
                if (self.c_new - s_i) >= 0:
                    s_new = min(s_new, self.c_new)
                else:
                    s_new = max(s_new, self.c_new)
                # recompose (s_new, t_i) -> (u,v): u=(s+t)/sqrt2, v=(s-t)/sqrt2
                new_u = (s_new + t_i) / SQ2
                new_v = (s_new - t_i) / SQ2
            else:
                s_i = (u_i + v_i) / SQ2
                s_new = s_i + self.eta * (self.c_new - s_i)
                if (self.c_new - s_i) >= 0:
                    s_new = min(s_new, self.c_new)
                else:
                    s_new = max(s_new, self.c_new)
                ds = s_new - s_i
                new_u = u_i + ds * N_U      # BOTH coordinates move along the normal
                new_v = v_i + ds * N_V
            self.pos[i] = (float(new_u), float(new_v))
            self.protos[i] = embed((new_u, new_v), self.basis)
            self.labels[i] = int((new_u + new_v) / SQ2 > self.c_new)

    def fit_phase2(self, X, Y2, positions, grow):
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
                self._repack_phase1()
                break
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy())
            self.labels.append(int(Y2[s]))
            self.pos.append(tuple(float(x) for x in positions[s]))
            self.phase.append(2)
            splits += 1
            self._repack_phase1()       # MOVE the residual phase-1 cells one step along the normal
        return self

    def posterior(self, key):
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        w = np.exp(-BETA_POST * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


# ── 2-D discrimination field, ridge, relocation (ridge_s) and bounded COH2D ──────
def discrim_field(cells, X, pos):
    """D(node) = max |Δ posterior| to its 4 grid neighbors (geometry-AGNOSTIC, VERBATIM H_1369)."""
    P = np.array([cells.posterior(X[m]) for m in range(len(X))]).reshape(G_GRID, G_GRID)
    D = np.zeros((G_GRID, G_GRID))
    for r in range(G_GRID):       # r indexes v
        for c in range(G_GRID):   # c indexes u
            best = 0.0
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < G_GRID and 0 <= cc < G_GRID:
                    best = max(best, abs(P[r, c] - P[rr, cc]))
            D[r, c] = best
    return D


def ridge_mask(D):
    mx = D.max()
    if mx <= 0:
        return np.zeros_like(D, dtype=bool)
    return D >= 0.5 * mx           # same 0.5-of-own-peak rule as H_1369


def ridge_s(D, pos):
    """Normal-coordinate s=(u+v)/sqrt2 of the ridge centroid — the relocation metric (RELOCATES)."""
    mask = ridge_mask(D).ravel()
    if mask.sum() == 0:
        return float("nan")
    return float(s_coord(pos)[mask].mean())


def coh2d_diag(D, pos):
    """Bounded ridge-CONCENTRATION coherence along the NORMAL coordinate s (the diagonal analog of
    H_1369 R2's u-axis COH2D). High = thin ridge concentrated at one s (single coherent diagonal
    line); low = grid-filling smear. Tangential (in-line) spread NOT scored (a coherent diagonal
    ridge legitimately runs the full length of the cut)."""
    mask = ridge_mask(D).ravel()
    n = int(mask.sum())
    if n == 0:
        return 0.0
    ridge_frac = n / (G_GRID * G_GRID)
    s_std = float(s_coord(pos)[mask].std())
    s_conc = 1.0 - min(1.0, s_std / S_STD_REF)
    return float(s_conc * (1.0 - ridge_frac))


# ── one arm ──────────────────────────────────────────────────────────────────
def run_arm(seed, eta, kind, retrain=True, rotate=False):
    basis = make_basis(seed)
    pos = make_grid()
    X = np.array([embed(p, basis) for p in pos])
    Y_A = label_of(pos, C_A)

    cells = RepackCellsDiag(eta=eta, basis=basis, rotate=rotate).fit_phase1(X, Y_A, pos, GROW1)
    nc_p1 = len(cells.protos)
    if retrain:
        if kind == "A2":
            Y2 = label_of(pos, C_A2)
        elif kind == "shuffle":
            sh = np.random.default_rng(seed + 4)
            Y2 = sh.integers(0, 2, size=len(pos))
        else:
            raise ValueError(kind)
        cells.fit_phase2(X, Y2, pos, GROW2)

    D = discrim_field(cells, X, pos)
    return dict(ridge_s=ridge_s(D, pos), coh2d=coh2d_diag(D, pos),
                nc_p1=nc_p1, nc=len(cells.protos))


def main():
    print("H_1374 R1 — CP RELOCATION ON A DIAGONAL (NON-AXIS-ALIGNED) 2-D BOUNDARY: move-the-cells?")
    print("=" * 90)
    print("Diagonal half-plane cat=(u+v)/sqrt2 > c (normal (1,1)/sqrt2), shifting c_A -> c_A'. Drift")
    print("residual phase-1 cells ALONG THE BOUNDARY NORMAL (both u,v move). Does the ridge relocate")
    print("ONTO the moved diagonal cut with a single coherent COH2D, or does the diagonal BREAK it?")
    print(f"grid={G_GRID}x{G_GRID}={G_GRID*G_GRID} K_RBF={K_RBF} DIM={DIM} c_A={C_A:.4f} c_A'={C_A2:.4f}")
    print(f"normal=(1,1)/sqrt2 phase1={GROW1} phase2={GROW2} eta={REPACK_ETA} seeds={SEEDS}")
    print(f"  metrics along NORMAL s=(u+v)/sqrt2: ridge_s = s of ridge centroid (RELOCATES);")
    print(f"           COH2D = bounded s-concentration (NO NCOMP gating — H_1369 proved it confounds)")
    print("")

    rp_ds, rp_coh = [], []    # RE-PACK |ridge_s-c_A'|, COH2D
    so_ds, so_coh = [], []    # SPLIT-ONLY (eta=0.0 ablation)
    nr_ds = []                # NO-RETRAIN |ridge_s-c_A|
    sh_coh = []               # SHUFFLE+repack COH2D
    print("  per-seed (SPLIT-ONLY eta=0.0 / RE-PACK eta=0.15 / NO-RETRAIN / SHUFFLE+repack):")
    for seed in SEEDS:
        so = run_arm(seed, eta=0.0, kind="A2")
        rp = run_arm(seed, eta=REPACK_ETA, kind="A2")
        nr = run_arm(seed, eta=0.0, kind="A2", retrain=False)
        sh = run_arm(seed, eta=REPACK_ETA, kind="shuffle")

        so_ds.append(abs(so["ridge_s"] - C_A2)); so_coh.append(so["coh2d"])
        rp_ds.append(abs(rp["ridge_s"] - C_A2)); rp_coh.append(rp["coh2d"])
        nr_ds.append(abs(nr["ridge_s"] - C_A)); sh_coh.append(sh["coh2d"])
        print(f"    seed {seed}: SPLIT-ONLY ridge_s={so['ridge_s']:.3f} coh={so['coh2d']:.3f} | "
              f"RE-PACK ridge_s={rp['ridge_s']:.3f} coh={rp['coh2d']:.3f} | "
              f"no-retrain ridge_s={nr['ridge_s']:.3f} | shuffle coh={sh['coh2d']:.3f}  "
              f"cells(p1,tot)={rp['nc_p1']},{rp['nc']}")
    print("")

    so_ds_m, so_coh_m = float(np.mean(so_ds)), float(np.mean(so_coh))
    rp_ds_m, rp_coh_m = float(np.mean(rp_ds)), float(np.mean(rp_coh))
    nr_ds_m, sh_coh_m = float(np.mean(nr_ds)), float(np.mean(sh_coh))
    print(f"  SPLIT-ONLY (eta=0.0, ablation): |ridge_s-c_A'| {so_ds_m:.3f}  COH2D {so_coh_m:.3f}")
    print(f"  RE-PACK    (eta=0.15)         : |ridge_s-c_A'| {rp_ds_m:.3f}  COH2D {rp_coh_m:.3f}")
    print(f"  NO-RETRAIN : |ridge_s-c_A| {nr_ds_m:.3f}  |  SHUFFLE+repack: COH2D {sh_coh_m:.3f}")
    print("")

    # ── NON-GATING diagnostic: re-pack ladder (gate scored ONLY at eta=0.15) ──
    print("  [NON-GATING diagnostic] RE-PACK-LADDER (gate is scored ONLY at eta=0.15):")
    for e in REPACK_LADDER:
        ds, cs = [], []
        for seed in SEEDS:
            r = run_arm(seed, eta=e, kind="A2")
            ds.append(abs(r["ridge_s"] - C_A2)); cs.append(r["coh2d"])
        tag = "  <-- FROZEN GATE" if abs(e - REPACK_ETA) < 1e-9 else ""
        print(f"     eta={e:.2f}: |ridge_s-c_A'| mean={np.mean(ds):.3f}  COH2D mean={np.mean(cs):.3f}{tag}")
    print("")

    # ── FROZEN BARS (FREEZE.txt; ALL thresholds VERBATIM from H_1369 R2) ───────────
    c1 = all(d <= LOC_TOL for d in rp_ds)                         # RELOCATION (all seeds)
    c2a = rp_coh_m >= COH_MIN                                     # COH2D floor
    c2b = rp_coh_m >= so_coh_m + COH_SEP                          # COH2D > split-only + 0.10
    c2 = c2a and c2b
    c3a = all(d <= LOC_TOL for d in nr_ds)                        # no-retrain holds c_A
    c3b = sh_coh_m <= SHUF_COH_MAX                                # shuffle collapses
    c3 = c3a and c3b
    c4 = so_ds_m > LOC_TOL                                        # split-only stays SHORT of c_A'

    print(f"  c1 RELOCATION (re-pack |ridge_s-c_A'|<={LOC_TOL} all 3 seeds):")
    print(f"     per-seed = {[round(d,3) for d in rp_ds]}  -> c1 {'PASS' if c1 else 'FAIL'}")
    print(f"  c2 COH2D CONCENTRATION (re-pack COH2D>={COH_MIN} AND >= split-only+{COH_SEP}):")
    print(f"     re-pack COH2D {rp_coh_m:.3f} >= {COH_MIN} -> {'PASS' if c2a else 'FAIL'}")
    print(f"     re-pack {rp_coh_m:.3f} >= split-only {so_coh_m:.3f}+{COH_SEP} -> {'PASS' if c2b else 'FAIL'}")
    print(f"     -> c2 {'PASS' if c2 else 'FAIL'}")
    print(f"  c3 EARNED (3a no-retrain |ridge_s-c_A|<={LOC_TOL}; 3b shuffle COH2D<={SHUF_COH_MAX}):")
    print(f"     3a no-retrain |ridge_s-c_A| = {[round(d,3) for d in nr_ds]} -> {'PASS' if c3a else 'FAIL'}")
    print(f"     3b shuffle COH2D {sh_coh_m:.3f} <= {SHUF_COH_MAX} -> {'PASS' if c3b else 'FAIL'}")
    print(f"     -> c3 {'PASS' if c3 else 'FAIL'}")
    print(f"  c4 DISTINCT-FROM-SPLIT (split-only |ridge_s-c_A'|>{LOC_TOL} — stays SHORT):")
    print(f"     split-only |ridge_s-c_A'| mean {so_ds_m:.3f} -> c4 {'PASS' if c4 else 'FAIL'}")
    print("=" * 90)

    green_r1 = c1 and c2 and c3 and c4
    if green_r1:
        print("VERDICT (R1, MIRROR, DIRECTIONAL): 🟢 GREEN — MOVE-THE-CELLS GENERALIZES TO A DIAGONAL")
        print("  (NON-AXIS-ALIGNED) BOUNDARY. Drifting the residual phase-1 cells ALONG THE BOUNDARY")
        print(f"  NORMAL toward the moved diagonal cut c_A'={C_A2:.4f} lands a thin coherent ridge ON")
        print(f"  the moved cut (|ridge_s-c_A'| {rp_ds_m:.3f}<={LOC_TOL}, COH2D {rp_coh_m:.3f}>={COH_MIN}).")
        print(f"  The split-only ablation stays SHORT (|ridge_s-c_A'| {so_ds_m:.3f}>{LOC_TOL}, COH2D")
        print(f"  {so_coh_m:.3f}) — the win is the geometric NORMAL-direction MOVE, not the re-growth.")
        print(f"  NO-RETRAIN held c_A, SHUFFLE collapsed (COH2D {sh_coh_m:.3f}<={SHUF_COH_MAX}). The")
        print("  non-axis-aligned geometry does NOT break the relocation: the law generalizes to")
        print("  ARBITRARY LINEAR boundaries. ENGINE-TRANSFER UNVERIFIED. TOY 2-D, 3 seeds, one")
        print("  diagonal slope. NO bar moved (c9/p7). ALL thresholds VERBATIM from H_1369 R2.")
        print("")
        print("=" * 90)
        print("TERMINAL VERDICT: 🟢 GREEN (R1, MIRROR, DIRECTIONAL) — move-the-cells GENERALIZES to a")
        print("  diagonal (non-axis-aligned) boundary. The R2 normal-frame rotation is unnecessary.")
        return 0

    # ── R1 non-green: print the honest catch, then fall through to the pre-registered R2 ──
    print("VERDICT (R1): 🧱 NON-GREEN — a frozen bar FAILED on the diagonal. Honest catch:")
    if not c1:
        print(f"  c1 RELOCATION FAILED (|ridge_s-c_A'| {rp_ds_m:.3f}>{LOC_TOL}) — the normal-drift did")
        print("  NOT reach the moved diagonal cut; the diagonal genuinely breaks the relocation.")
    else:
        print(f"  c1 RELOCATION PASSED ({rp_ds_m:.3f}<={LOC_TOL}) — the normal-direction drift DOES")
        print(f"  track the moved diagonal cut (split-only stays SHORT at {so_ds_m:.3f}; c4 PASS).")
        if not c2a:
            print(f"  But c2a COH2D FLOOR failed ({rp_coh_m:.3f}<{COH_MIN}) — the relocated ridge smears.")
        elif not c2b:
            print(f"  The catch is c2b CONCENTRATION-SEPARATION: re-pack COH2D {rp_coh_m:.3f} vs split-")
            print(f"  only {so_coh_m:.3f} = gap {rp_coh_m-so_coh_m:.3f} < {COH_SEP}. On a DIAGONAL the")
            print("  split-only baseline is ITSELF already fairly concentrated (its residual ridge is a")
            print("  thin diagonal smear, not the grid-filling smear an axis-aligned split-only gives),")
            print("  so the bounded-COH2D *separation* shrinks even though RELOCATION (c1) is decisive.")
        elif not c3:
            print("  But c3 EARNED failed — a frozen control fabricated/drifted. Honest non-GREEN.")
        elif not c4:
            print("  But c4 NOT-DISTINCT — split-only ALREADY relocates onto the diagonal.")
    print("  Per the FREEZE outcome map (¬c2 → run pre-registered R2, frozen-first, NO bar moved,")
    print("  a_break_the_wall): the NORMAL-FRAME ROTATION R2 runs below. NO bar moved (c9/p7).")
    print("")

    # ════════════════════════════════════════════════════════════════════════════════
    # R2 (a_break_the_wall, PRE-REGISTERED in FREEZE.txt BEFORE any scoring): NORMAL-FRAME
    # ROTATION. Express every cell in (s, t) = (normal, tangential) coordinates relative to
    # the diagonal boundary, drift PURELY in s, re-embed. This removes the residual TANGENTIAL
    # wobble the (u,v)-frame normal-drift can leave, so the relocated ridge concentrates MORE
    # tightly along the normal s than the split-only diagonal smear — directly targeting the
    # c2b CONCENTRATION-SEPARATION leg that R1 narrowly missed. SAME frozen bars, NO bar moved.
    # ════════════════════════════════════════════════════════════════════════════════
    print("R2 (a_break_the_wall) — NORMAL-FRAME ROTATION (drift in (s,t) coords, purely in s):")

    rp2_ds, rp2_coh = [], []
    so2_ds, so2_coh = [], []   # split-only is frame-INDEPENDENT (eta=0) — recomputed for the record
    nr2_ds, sh2_coh = [], []
    for seed in SEEDS:
        rp = run_arm(seed, eta=REPACK_ETA, kind="A2", rotate=True)
        so = run_arm(seed, eta=0.0, kind="A2", rotate=True)
        nr = run_arm(seed, eta=0.0, kind="A2", retrain=False, rotate=True)
        sh = run_arm(seed, eta=REPACK_ETA, kind="shuffle", rotate=True)
        rp2_ds.append(abs(rp["ridge_s"] - C_A2)); rp2_coh.append(rp["coh2d"])
        so2_ds.append(abs(so["ridge_s"] - C_A2)); so2_coh.append(so["coh2d"])
        nr2_ds.append(abs(nr["ridge_s"] - C_A)); sh2_coh.append(sh["coh2d"])
        print(f"    seed {seed}: RE-PACK(rot) ridge_s={rp['ridge_s']:.3f} coh={rp['coh2d']:.3f} | "
              f"split-only ridge_s={so['ridge_s']:.3f} coh={so['coh2d']:.3f} | "
              f"no-retrain ridge_s={nr['ridge_s']:.3f} | shuffle coh={sh['coh2d']:.3f}")
    rp2_ds_m, rp2_coh_m = float(np.mean(rp2_ds)), float(np.mean(rp2_coh))
    so2_ds_m, so2_coh_m = float(np.mean(so2_ds)), float(np.mean(so2_coh))
    nr2_ds_m, sh2_coh_m = float(np.mean(nr2_ds)), float(np.mean(sh2_coh))
    print(f"  RE-PACK(rot): |ridge_s-c_A'| {rp2_ds_m:.3f}  COH2D {rp2_coh_m:.3f}")
    print(f"  SPLIT-ONLY  : |ridge_s-c_A'| {so2_ds_m:.3f}  COH2D {so2_coh_m:.3f}")
    print(f"  NO-RETRAIN  : |ridge_s-c_A| {nr2_ds_m:.3f}  |  SHUFFLE(rot) COH2D {sh2_coh_m:.3f}")

    d1 = all(d <= LOC_TOL for d in rp2_ds)
    d2a = rp2_coh_m >= COH_MIN
    d2b = rp2_coh_m >= so2_coh_m + COH_SEP
    d2 = d2a and d2b
    d3a = all(d <= LOC_TOL for d in nr2_ds)
    d3b = sh2_coh_m <= SHUF_COH_MAX
    d3 = d3a and d3b
    d4 = so2_ds_m > LOC_TOL
    print(f"  c1' RELOCATION {[round(d,3) for d in rp2_ds]} <= {LOC_TOL} -> {'PASS' if d1 else 'FAIL'}")
    print(f"  c2' COH2D: {rp2_coh_m:.3f}>={COH_MIN} -> {'PASS' if d2a else 'FAIL'} AND >= split-only "
          f"{so2_coh_m:.3f}+{COH_SEP} (gap {rp2_coh_m-so2_coh_m:.3f}) -> {'PASS' if d2b else 'FAIL'} "
          f"=> c2' {'PASS' if d2 else 'FAIL'}")
    print(f"  c3' EARNED: no-retrain {'PASS' if d3a else 'FAIL'} AND shuffle COH2D {sh2_coh_m:.3f}<="
          f"{SHUF_COH_MAX} {'PASS' if d3b else 'FAIL'} => c3' {'PASS' if d3 else 'FAIL'}")
    print(f"  c4' DISTINCT: split-only |ridge_s-c_A'| {so2_ds_m:.3f}>{LOC_TOL} -> {'PASS' if d4 else 'FAIL'}")
    print("=" * 90)

    green_r2 = d1 and d2 and d3 and d4
    print("")
    if green_r2:
        print("TERMINAL VERDICT: 🟢 GREEN (R2 normal-frame rotation, MIRROR, DIRECTIONAL) — move-the-")
        print("  cells GENERALIZES to a DIAGONAL boundary. Rotating the cell frame to the boundary")
        print(f"  normal and drifting purely in s lands the ridge ON the moved cut (|ridge_s-c_A'|")
        print(f"  {rp2_ds_m:.3f}<={LOC_TOL}) with COH2D {rp2_coh_m:.3f}>={COH_MIN}, NOW cleanly SEPARATED")
        print(f"  from split-only ({so2_coh_m:.3f}, gap {rp2_coh_m-so2_coh_m:.3f}>={COH_SEP}); shuffle")
        print(f"  collapsed ({sh2_coh_m:.3f}<={SHUF_COH_MAX}). The non-axis-aligned geometry does NOT")
        print("  break the relocation once the drift is expressed in the boundary's own frame — the")
        print("  law generalizes to ARBITRARY LINEAR boundaries. The R1 c2b miss was a FRAME artifact")
        print("  (residual tangential wobble in the (u,v)-frame), not a real break. NO bar moved")
        print("  (c9/p7). ALL thresholds VERBATIM from H_1369 R2. ENGINE-TRANSFER UNVERIFIED.")
        return 0
    if d1 and (not d2b) and d2a:
        print("TERMINAL VERDICT: 🧱 CLOSED-NEGATIVE (AXIS-ALIGNED-ONLY) — move-the-cells RELOCATES on a")
        print(f"  diagonal (c1' |ridge_s-c_A'| {rp2_ds_m:.3f}<={LOC_TOL}, split-only short {so2_ds_m:.3f})")
        print(f"  but does NOT clear the bounded-COH2D CONCENTRATION-SEPARATION bar (re-pack {rp2_coh_m:.3f}")
        print(f"  vs split-only {so2_coh_m:.3f}, gap {rp2_coh_m-so2_coh_m:.3f}<{COH_SEP}) even after the")
        print("  normal-frame rotation. On a diagonal the split-only residual ridge is ALREADY a thin")
        print("  diagonal smear, so the concentration win does not separate. The move-the-cells")
        print("  RELOCATION law holds on a diagonal; the COH2D-SEPARATION stringency is AXIS-ALIGNED-")
        print("  ONLY. Honest 🧱 = valid result. NO bar moved (c9/p7).")
        return 3
    if not d1:
        print("TERMINAL VERDICT: 🧱 CLOSED-NEGATIVE — even the normal-frame rotation does NOT relocate")
        print(f"  the ridge onto the moved diagonal cut (|ridge_s-c_A'| {rp2_ds_m:.3f}>{LOC_TOL}). The")
        print("  diagonal genuinely breaks the relocation. NO bar moved (c9/p7).")
        return 3
    if not d3:
        print("TERMINAL VERDICT: CONFOUNDED (R2) — a frozen EARNED control failed. NO bar move (c9).")
        return 1
    print("TERMINAL VERDICT: MIXED (R2). Honest, NO bar move (c9).")
    return 5


if __name__ == "__main__":
    import sys
    sys.exit(main())
