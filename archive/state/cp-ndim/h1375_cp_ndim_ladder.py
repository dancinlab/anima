"""
H_1375 — CP DIMENSIONAL LADDER: does move-the-cells RELOCATION survive as feature dimension D grows?
DIRECTIONAL numpy MIRROR ($0 CPU, gradient-free). engine-transfer UNVERIFIED. live CORE UNTOUCHED.

Frozen design: .verdicts/1375_cp_ndim_ladder/FREEZE.txt (pre-registered BEFORE this scoring; frozen-
first, c9/c16/p7, NO tune-to-green). 3 seeds [4333,4334,4335], p7. Realizes the user direction
"2d 말고도 차원늘려봐" — push categorical-perception move-the-cells BEYOND 2-D up a dimensional ladder
D ∈ {2,3,4,6,8}. a_no_llm_frame_trap (geometry-of-representation / curse-of-dimensionality lens, c15),
a_break_the_wall, a_scale_honest_scope.

THE QUESTION: H_1360 (1-D) → H_1369 (2-D axis) → H_1374 (2-D diagonal, RELOCATION generalizes) proved
move-the-cells RELOCATION is a geometric law. Does it SURVIVE a CONSTANT Monte-Carlo sample size N as
the feature dimension D grows? Constant-N in growing-D is itself the curse-of-dimensionality stressor —
that IS the point. Headline = the CURVE over D: relocation |ridge_s−c'| along the normal, and a bounded
N-D concentration COH_D (generalizes H_1369's COH2D, projection-onto-normal spread).

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary at test; the
re-pack keys on a cell's BIRTH PHASE + own source position (structural, NO injected target/persona/RLHF);
labels enter ONLY at training. NO-RETRAIN + SHUFFLE = anti-Goodhart discriminators; SPLIT-ONLY (eta=0.0)
isolates the geometric drift as the lever. ONLY D is varied (w orientation held constant per seed).
"""
import numpy as np

# ── frozen constants (from FREEZE.txt) ───────────────────────────────────────
LADDER  = [2, 3, 4, 6, 8]        # the dimensional ladder
N_SAMP  = 169                    # CONSTANT Monte-Carlo sample size across D (= H_1369 13x13 budget)
K_CTR   = 64                     # RBF centers -> DIM=64 (LOW, fixed across D, = H_1369)
DIM     = K_CTR
Q_A     = 1.0 / 3.0             # phase-1 cut = 1/3 quantile of the projection
Q_A2    = 2.0 / 3.0            # phase-2 moved cut = 2/3 quantile of the projection
GROW1   = 48                    # phase-1 split budget (FIXED LOW, = H_1369)
GROW2   = 48                    # phase-2 split budget (FIXED LOW, NO inflation; same every arm)
BETA_POST = 18.0                # softmin posterior temperature (family verbatim)
KNN     = 4                     # k nearest sample neighbors for the discrimination field
SEEDS   = [4333, 4334, 4335]
REPACK_ETA = 0.15               # FROZEN gate value

# frozen bar thresholds (verbatim mirror of H_1369 R2; NO threshold moved)
LOC_TOL      = 0.12
COH_MIN      = 0.50
COH_SEP      = 0.10
SHUF_COH_MAX = 0.20
S_STD_REF    = 0.20             # projection-spread reference (= H_1369 U_STD_REF)


# ── per-seed-per-D fixed geometry ────────────────────────────────────────────
def make_geom(seed, D, whiten=False):
    """Fixed unit normal w in R^D, RBF centers, Monte-Carlo sample, projection cuts c_A/c_A'.
    w orientation is the per-seed RNG draw — held CONSTANT regardless of which arm runs (ONLY D varies
    across the ladder). c_A,c_A' = projection quantiles of a FIXED REFERENCE sample (frozen, NOT the
    scored sample) so both phases see a balanced split at every D."""
    rb = np.random.default_rng(seed + 7000 + 13 * D)
    w = rb.normal(size=D)
    w = w / np.linalg.norm(w)
    centers = rb.uniform(0.0, 1.0, size=(K_CTR, D))
    width = float(rb.uniform(0.10, 0.13))
    # Monte-Carlo sample (the constant-N cloud) + a separate frozen reference for the cuts
    samp = rb.uniform(0.0, 1.0, size=(N_SAMP, D))
    ref = rb.uniform(0.0, 1.0, size=(4000, D))
    if whiten:
        # standardize the sample by per-axis std so the constant-N cloud is isotropic (a_break_the_wall
        # angle). Apply the SAME affine to centers, sample, ref, and re-derive the normal in the
        # whitened frame; positions/projections all live in the whitened coords.
        mu = samp.mean(axis=0)
        sd = samp.std(axis=0)
        sd = np.where(sd < 1e-9, 1.0, sd)
        centers = (centers - mu) / sd
        samp = (samp - mu) / sd
        ref = (ref - mu) / sd
        w = w / sd                      # normal transforms as inverse of the position scaling
        w = w / np.linalg.norm(w)
    proj_ref = ref @ w
    c_A = float(np.quantile(proj_ref, Q_A))
    c_A2 = float(np.quantile(proj_ref, Q_A2))
    return dict(w=w, centers=centers, width=width, samp=samp, c_A=c_A, c_A2=c_A2)


def embed(p, geom):
    centers, width = geom["centers"], geom["width"]
    d2 = ((np.asarray(p)[None, :] - centers) ** 2).sum(axis=1)
    v = np.exp(-d2 / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def label_of(pos, w, c_cut):
    """TRUE partition: cat = int(<w,x> > c_cut). (D-1)-dim hyperplane, normal w."""
    return (pos @ w > c_cut).astype(int)


# ── Voronoi/immune store: split-only growth + geometric re-pack (H_1360/H_1369 family, N-D) ──
class RepackCellsND:
    def __init__(self, geom, eta=0.0):
        self.g = geom
        self.eta = eta
        self.protos, self.labels, self.pos, self.phase = [], [], [], []
        self.n_phase1 = 0

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit_phase1(self, X, Y, positions, grow):
        M = len(X)
        c0 = X.mean(axis=0); n = np.linalg.norm(c0); c0 = c0 / n if n > 0 else c0
        seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
        self.protos = [c0]; self.labels = [int(Y[seed_stim])]
        self.pos = [positions[seed_stim].copy()]; self.phase = [1]
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
            self.protos.append(X[s].copy()); self.labels.append(int(Y[s]))
            self.pos.append(positions[s].copy()); self.phase.append(1)
        self.n_phase1 = len(self.protos)
        return self

    def _repack_phase1(self):
        """Drift each phase-1 cell's SOURCE position ALONG +w so its projection s_i moves toward c_A'
        (orthogonal complement unchanged = the irrelevant axes), clamp at c_A', re-embed, re-read label."""
        if self.eta <= 0.0:
            return
        w, c2 = self.g["w"], self.g["c_A2"]
        for i in range(self.n_phase1):
            p = self.pos[i]
            s_i = float(p @ w)
            new_s = s_i + self.eta * (c2 - s_i)
            if (c2 - s_i) >= 0:
                new_s = min(new_s, c2)
            else:
                new_s = max(new_s, c2)
            p = p + (new_s - s_i) * w                  # move ONLY along the normal
            self.pos[i] = p
            self.protos[i] = embed(p, self.g)
            self.labels[i] = int((p @ w) > c2)

    def fit_phase2(self, X, Y2, positions, grow):
        M = len(X); splits = 0
        for _ in range(grow):
            if splits >= grow:
                break
            owners = np.array([self._owner(X[m])[0] for m in range(M)])
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y2)[0]
            if len(mism) == 0:
                self._repack_phase1(); break
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy()); self.labels.append(int(Y2[s]))
            self.pos.append(positions[s].copy()); self.phase.append(2)
            splits += 1
            self._repack_phase1()
        return self

    def posterior(self, key):
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        w = np.exp(-BETA_POST * (d - d.min())); s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


# ── N-D discrimination field, ridge, projection-spread coherence + relocation ────────
def discrim_field(cells, X, pos):
    """D(node) = max |Δ posterior| to its KNN nearest sample neighbors (N-D analog of the H_1369
    4-grid-neighbor field; kNN because the Monte-Carlo cloud has no lattice neighbors)."""
    P = np.array([cells.posterior(X[m]) for m in range(len(X))])
    N = len(X)
    # pairwise distances in POSITION space
    diff = pos[:, None, :] - pos[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=2))
    np.fill_diagonal(dist, np.inf)
    D = np.zeros(N)
    for i in range(N):
        nn = np.argsort(dist[i])[:KNN]
        D[i] = float(np.max(np.abs(P[i] - P[nn])))
    return D


def ridge_mask(D):
    mx = D.max()
    if mx <= 0:
        return np.zeros_like(D, dtype=bool)
    return D >= 0.5 * mx


def ridge_s(D, pos, w):
    """projection-onto-normal centroid of the ridge nodes (the relocation metric, along the normal)."""
    mask = ridge_mask(D)
    if mask.sum() == 0:
        return float("nan")
    return float((pos[mask] @ w).mean())


def coh_d(D, pos, w):
    """COH_D in [0,1] = S_CONC * (1 - RIDGE_FRAC), S_CONC scores ONLY the normal-projection spread
    (orthogonal complement spread NOT scored — a coherent hyperplane legitimately spans it). Bounded
    -> no NCOMP saturation (the H_1369 R1 lesson, carried by design)."""
    mask = ridge_mask(D)
    n = int(mask.sum())
    if n == 0:
        return 0.0
    ridge_frac = n / len(D)
    s_std = float((pos[mask] @ w).std())
    s_conc = 1.0 - min(1.0, s_std / S_STD_REF)
    return float(s_conc * (1.0 - ridge_frac))


# ── one arm ──────────────────────────────────────────────────────────────────
def run_arm(seed, D, eta, kind, retrain=True, whiten=False):
    g = make_geom(seed, D, whiten=whiten)
    pos = g["samp"]
    X = np.array([embed(p, g) for p in pos])
    Y_A = label_of(pos, g["w"], g["c_A"])
    cells = RepackCellsND(g, eta=eta).fit_phase1(X, Y_A, pos, GROW1)
    nc_p1 = len(cells.protos)
    if retrain:
        if kind == "A2":
            Y2 = label_of(pos, g["w"], g["c_A2"])
        elif kind == "shuffle":
            sh = np.random.default_rng(seed + 4 + D)
            Y2 = sh.integers(0, 2, size=len(pos))
        else:
            raise ValueError(kind)
        cells.fit_phase2(X, Y2, pos, GROW2)
    Dfield = discrim_field(cells, X, pos)
    return dict(rs=ridge_s(Dfield, pos, g["w"]), coh=coh_d(Dfield, pos, g["w"]),
                c_A=g["c_A"], c_A2=g["c_A2"], nc_p1=nc_p1, nc=len(cells.protos))


# ── one full ladder pass (whiten False = primary, True = a_break_the_wall angle) ──
def ladder(whiten=False):
    rows = []
    for D in LADDER:
        rp_du, so_du, nr_du = [], [], []
        rp_coh, so_coh, sh_coh = [], [], []
        cA_list, cA2_list = [], []
        for seed in SEEDS:
            rp = run_arm(seed, D, REPACK_ETA, "A2", whiten=whiten)
            so = run_arm(seed, D, 0.0, "A2", whiten=whiten)
            nr = run_arm(seed, D, 0.0, "A2", retrain=False, whiten=whiten)
            sh = run_arm(seed, D, REPACK_ETA, "shuffle", whiten=whiten)
            rp_du.append(abs(rp["rs"] - rp["c_A2"])); rp_coh.append(rp["coh"])
            so_du.append(abs(so["rs"] - so["c_A2"])); so_coh.append(so["coh"])
            nr_du.append(abs(nr["rs"] - nr["c_A"])); sh_coh.append(sh["coh"])
            cA_list.append(rp["c_A"]); cA2_list.append(rp["c_A2"])
        rows.append(dict(D=D,
            rp_du=rp_du, so_du=so_du, nr_du=nr_du,
            rp_coh=rp_coh, so_coh=so_coh, sh_coh=sh_coh,
            rp_du_m=float(np.mean(rp_du)), so_du_m=float(np.mean(so_du)),
            nr_du_m=float(np.mean(nr_du)),
            rp_coh_m=float(np.mean(rp_coh)), so_coh_m=float(np.mean(so_coh)),
            sh_coh_m=float(np.mean(sh_coh)),
            cA=float(np.mean(cA_list)), cA2=float(np.mean(cA2_list))))
    return rows


def score_row(r):
    c1 = all(d <= LOC_TOL for d in r["rp_du"])
    c2 = (r["rp_coh_m"] >= COH_MIN) and (r["rp_coh_m"] >= r["so_coh_m"] + COH_SEP)
    c3a = all(d <= LOC_TOL for d in r["nr_du"])
    c3b = r["sh_coh_m"] <= SHUF_COH_MAX
    c3 = c3a and c3b
    c4 = r["so_du_m"] > LOC_TOL
    return dict(c1=c1, c2=c2, c3=c3, c3a=c3a, c3b=c3b, c4=c4,
                allpass=(c1 and c2 and c3 and c4))


def print_ladder(rows, title):
    print(title)
    print("-" * 100)
    print(f"  bars: LOC_TOL={LOC_TOL} COH_MIN={COH_MIN} COH_SEP={COH_SEP} SHUF_COH_MAX={SHUF_COH_MAX} "
          f"S_STD_REF={S_STD_REF}  (N={N_SAMP} CONSTANT across D, DIM={DIM}, eta={REPACK_ETA}, seeds={SEEDS})")
    print(f"  {'D':>2} | {'reloc|rs-cA2|':>13} | {'COH_D rp/split/shuf':>26} | {'c_A,c_A2':>13} | "
          f"{'c1':>3} {'c2':>3} {'c3':>3} {'c4':>3} | PASS")
    fails = []
    for r in rows:
        s = score_row(r)
        reloc = f"{r['rp_du_m']:.3f}"
        cohs = f"{r['rp_coh_m']:.3f}/{r['so_coh_m']:.3f}/{r['sh_coh_m']:.3f}"
        cuts = f"{r['cA']:.3f},{r['cA2']:.3f}"
        mark = lambda b: " ✅" if b else " ❌"
        print(f"  {r['D']:>2} | {reloc:>13} | {cohs:>26} | {cuts:>13} |"
              f"{mark(s['c1'])}{mark(s['c2'])}{mark(s['c3'])}{mark(s['c4'])} | "
              f"{'PASS' if s['allpass'] else 'FAIL'}")
        if not s["allpass"]:
            fails.append((r["D"], s))
    print("")
    print(f"  per-D detail (RELOCATION per-seed |rs-c_A2|, NO-RETRAIN per-seed |rs-c_A|):")
    for r in rows:
        print(f"    D={r['D']}: reloc {[round(x,3) for x in r['rp_du']]} | split-only "
              f"{[round(x,3) for x in r['so_du']]} | no-retrain {[round(x,3) for x in r['nr_du']]} | "
              f"COH rp {[round(x,3) for x in r['rp_coh']]} shuf {[round(x,3) for x in r['sh_coh']]}")
    print("")
    return fails


def main():
    print("H_1375 — CP DIMENSIONAL LADDER: does move-the-cells RELOCATION survive growing D?")
    print("=" * 100)
    print("DIRECTIONAL numpy mirror ($0 CPU). User: '2d 말고도 차원늘려봐'. D ∈ {2,3,4,6,8}, CONSTANT N=169.")
    print("Constant-N in growing-D = the curse-of-dimensionality stressor (the point). a_no_llm_frame_trap.")
    print("")

    rows = ladder(whiten=False)
    fails = print_ladder(rows, "PRIMARY LADDER (un-whitened):")

    # ── ladder verdict ──
    print("=" * 100)
    if not fails:
        print("LADDER VERDICT: 🟢 DIMENSION-INVARIANT — move-the-cells RELOCATION survives the WHOLE")
        print(f"  ladder D ∈ {LADDER} at CONSTANT N={N_SAMP}; every D passes all four frozen bars.")
        print("  DIRECTIONAL mirror, engine-transfer UNVERIFIED, TOY constant-N stressor. NO bar moved.")
        return 0

    Dstar = fails[0][0]
    print(f"LADDER VERDICT (primary): 🧱 BREAKS-AT-D*={Dstar} — relocation/coherence first fails at D={Dstar}.")
    for D, s in fails:
        bad = [k for k in ("c1", "c2", "c3", "c4") if not s[k]]
        print(f"    D={D} FAILED bars: {bad}")
    print("")
    print("a_break_the_wall (frozen-first, pre-registered): re-run the FULL ladder WHITENED")
    print("  (drift+score in the per-axis-standardized isotropic frame). SAME frozen bars. SECOND block:")
    print("=" * 100)
    rows_w = ladder(whiten=True)
    fails_w = print_ladder(rows_w, "WHITENED LADDER (a_break_the_wall angle):")
    print("=" * 100)
    if not fails_w:
        print(f"LADDER VERDICT (after a_break_the_wall): 🟢 DIMENSION-INVARIANT under WHITENING — the")
        print(f"  break at D*={Dstar} was a metric-geometry (anisotropic constant-N cloud) confound;")
        print("  whitening the frame restores relocation+coherence across the whole ladder. NO bar moved.")
        return 0
    Dstar_w = fails_w[0][0]
    print(f"LADDER VERDICT (after a_break_the_wall): 🧱 BREAKS-AT-D*={Dstar_w} EVEN WHITENED — the")
    print("  dimensional break is REAL, not a frame artifact. Whitening does NOT rescue it. Honest")
    print("  curse-of-dimensionality ceiling under constant-N. NO bar moved (c9/c16/p7).")
    for D, s in fails_w:
        bad = [k for k in ("c1", "c2", "c3", "c4") if not s[k]]
        print(f"    D={D} FAILED bars: {bad}")
    return 3


if __name__ == "__main__":
    import sys
    sys.exit(main())
