"""
H_1377 — CP N-SCALING: does the H_1375 D*=3 concentration break VANISH once per-dimension sample
DENSITY (not raw N) is held constant?  DIRECTIONAL numpy MIRROR ($0 CPU, gradient-free).
engine-transfer UNVERIFIED. live CORE UNTOUCHED.

Frozen design: .verdicts/1377_cp_nscaling/FREEZE.txt (pre-registered BEFORE this scoring;
frozen-first, c9/c16/p7, NO tune-to-green). 3 seeds [4333,4334,4335] (reuse H_1375), p7.

DECISIVE FOLLOW-ON to H_1375 (🧱 BREAKS-AT-D*=3 at CONSTANT N=169). H_1375 found move-the-cells
RELOCATION dimension-invariant but bounded CONCENTRATION COH_D collapsing below COH_MIN=0.50 from
D=3 — the classic curse-of-dimensionality signature at a FIXED sample budget. THE OPEN QUESTION:
is D*=3 a FUNDAMENTAL dimensional ceiling, or a constant-N SPARSITY artifact (c16 cause #3)?

THE ONLY CHANGE vs H_1375: the sampling rule. Hold per-axis LINEAR density k = N^(1/D) constant.
H_1375 anchor D=2,N=169 = 13/axis →  N_density(D) = round(13^D), capped at N_CAP=4000 (compute-
sane, a_scale_honest_scope). D=2→169 (= H_1375 anchor), D=3→2197 (UNCAPPED, DECISIVE rung),
D=4/6/8→4000 (CAPPED, honest truncation: true density-constant 28561/4.8M/815M infeasible on $0
CPU). Every metric / arm / leg / threshold / seed / hyperplane is VERBATIM from H_1375. NO bar moved.

p1/p2/p3/p6: discrimination reads ONLY representational distance; NO injected boundary at test;
the re-pack keys on a cell's BIRTH PHASE + own source position (structural, NO injected
target/persona/RLHF); labels enter ONLY at training. NO-RETRAIN + SHUFFLE = anti-Goodhart
discriminators; SPLIT-ONLY (eta=0.0) isolates the geometric drift as the lever. ONLY D (and N(D),
the density rule) is varied (w orientation held constant per seed).
"""
import numpy as np

# ── frozen constants (from FREEZE.txt; verbatim H_1375 except the N rule) ─────────────────
LADDER  = [2, 3, 4, 6, 8]        # the dimensional ladder
K_BASE  = 13                     # per-axis linear density (= H_1375 D=2 N=169 -> 13/axis)
N_CAP   = 4000                   # compute ceiling (a_scale_honest_scope); see FREEZE.txt
K_CTR   = 64                     # RBF centers -> DIM=64 (LOW, fixed across D, = H_1375)
DIM     = K_CTR
Q_A     = 1.0 / 3.0             # phase-1 cut = 1/3 quantile of the projection
Q_A2    = 2.0 / 3.0            # phase-2 moved cut = 2/3 quantile of the projection
GROW1   = 48                    # phase-1 split budget (FIXED LOW, = H_1375)
GROW2   = 48                    # phase-2 split budget (FIXED LOW, NO inflation; same every arm)
BETA_POST = 18.0                # softmin posterior temperature (family verbatim)
KNN     = 4                     # k nearest sample neighbors for the discrimination field
SEEDS   = [4333, 4334, 4335]
REPACK_ETA = 0.15               # FROZEN gate value

# frozen bar thresholds (verbatim mirror of H_1369 R2 / H_1375; NO threshold moved)
LOC_TOL      = 0.12
COH_MIN      = 0.50
COH_SEP      = 0.10
SHUF_COH_MAX = 0.20
S_STD_REF    = 0.20             # projection-spread reference (= H_1369 U_STD_REF)


def n_density(D):
    """DENSITY-CONSTANT rule: N(D)=min(N_CAP, round(13^D)); 13/axis linear density (=H_1375 anchor).
    Returns (N_used, n_target, capped)."""
    n_target = int(round(K_BASE ** D))
    n_used = min(N_CAP, n_target)
    return n_used, n_target, (n_used < n_target)


# ── per-seed-per-D fixed geometry (verbatim H_1375; whiten path dropped — not this lane's angle) ──
def make_geom(seed, D, N_samp):
    """Fixed unit normal w in R^D, RBF centers, Monte-Carlo sample of size N_samp, cuts c_A/c_A'.
    w orientation is the per-seed RNG draw — held CONSTANT regardless of which arm runs (ONLY D and
    N(D) vary across the ladder). c_A,c_A' = projection quantiles of a FIXED REFERENCE sample
    (frozen, NOT the scored sample) so both phases see a balanced split at every D."""
    rb = np.random.default_rng(seed + 7000 + 13 * D)
    w = rb.normal(size=D)
    w = w / np.linalg.norm(w)
    centers = rb.uniform(0.0, 1.0, size=(K_CTR, D))
    width = float(rb.uniform(0.10, 0.13))
    samp = rb.uniform(0.0, 1.0, size=(N_samp, D))     # the density-constant cloud
    ref = rb.uniform(0.0, 1.0, size=(4000, D))         # frozen reference for the cuts (verbatim)
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
        P = np.array(self.protos)
        d = np.linalg.norm(P - key, axis=1)
        i = int(np.argmin(d))
        return i, float(d[i])

    def _owners_all(self, X):
        """vectorized owner assignment for ALL stim (speed for large N; identical argmin result)."""
        P = np.array(self.protos)                       # (C, DIM)
        d = np.linalg.norm(X[:, None, :] - P[None, :, :], axis=2)   # (M, C)
        return np.argmin(d, axis=1)

    def fit_phase1(self, X, Y, positions, grow):
        M = len(X)
        c0 = X.mean(axis=0); n = np.linalg.norm(c0); c0 = c0 / n if n > 0 else c0
        seed_stim = int(np.argmin(np.linalg.norm(X - c0, axis=1)))
        self.protos = [c0]; self.labels = [int(Y[seed_stim])]
        self.pos = [positions[seed_stim].copy()]; self.phase = [1]
        for _ in range(grow):
            if len(self.protos) >= 1 + grow:
                break
            owners = self._owners_all(X)
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y)[0]
            if len(mism) == 0:
                break                                  # error is the ONLY growth driver (p8)
            Pm = np.array(self.protos)[owners[mism]]
            md = np.linalg.norm(X[mism] - Pm, axis=1)
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
        splits = 0
        for _ in range(grow):
            if splits >= grow:
                break
            owners = self._owners_all(X)
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y2)[0]
            if len(mism) == 0:
                self._repack_phase1(); break
            Pm = np.array(self.protos)[owners[mism]]
            md = np.linalg.norm(X[mism] - Pm, axis=1)
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy()); self.labels.append(int(Y2[s]))
            self.pos.append(positions[s].copy()); self.phase.append(2)
            splits += 1
            self._repack_phase1()
        return self

    def posterior_all(self, X):
        P = np.array(self.protos)                       # (C, DIM)
        d = np.linalg.norm(X[:, None, :] - P[None, :, :], axis=2)   # (M, C)
        w = np.exp(-BETA_POST * (d - d.min(axis=1, keepdims=True)))
        s = w.sum(axis=1, keepdims=True)
        w = np.divide(w, s, out=np.zeros_like(w), where=s > 0)
        lab = np.array(self.labels, dtype=np.float64)
        return (w * lab[None, :]).sum(axis=1)           # (M,)


# ── N-D discrimination field, ridge, projection-spread coherence + relocation (verbatim H_1375) ──
def discrim_field(cells, X, pos):
    """D(node) = max |Δ posterior| to its KNN nearest sample neighbors (N-D analog of the H_1369
    4-grid-neighbor field; kNN because the Monte-Carlo cloud has no lattice neighbors)."""
    P = cells.posterior_all(X)
    N = len(X)
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
def run_arm(seed, D, N_samp, eta, kind, retrain=True):
    g = make_geom(seed, D, N_samp)
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


# ── one full density-constant ladder pass ─────────────────────────────────────
def ladder():
    rows = []
    for D in LADDER:
        N_used, n_target, capped = n_density(D)
        rp_du, so_du, nr_du = [], [], []
        rp_coh, so_coh, sh_coh = [], [], []
        cA_list, cA2_list = [], []
        for seed in SEEDS:
            rp = run_arm(seed, D, N_used, REPACK_ETA, "A2")
            so = run_arm(seed, D, N_used, 0.0, "A2")
            nr = run_arm(seed, D, N_used, 0.0, "A2", retrain=False)
            sh = run_arm(seed, D, N_used, REPACK_ETA, "shuffle")
            rp_du.append(abs(rp["rs"] - rp["c_A2"])); rp_coh.append(rp["coh"])
            so_du.append(abs(so["rs"] - so["c_A2"])); so_coh.append(so["coh"])
            nr_du.append(abs(nr["rs"] - nr["c_A"])); sh_coh.append(sh["coh"])
            cA_list.append(rp["c_A"]); cA2_list.append(rp["c_A2"])
        rows.append(dict(D=D, N=N_used, n_target=n_target, capped=capped,
            rp_du=rp_du, so_du=so_du, nr_du=nr_du,
            rp_coh=rp_coh, so_coh=so_coh, sh_coh=sh_coh,
            rp_du_m=float(np.mean(rp_du)), so_du_m=float(np.mean(so_du)),
            nr_du_m=float(np.mean(nr_du)),
            rp_coh_m=float(np.mean(rp_coh)), so_coh_m=float(np.mean(so_coh)),
            sh_coh_m=float(np.mean(sh_coh)),
            cA=float(np.mean(cA_list)), cA2=float(np.mean(cA2_list))))
        r = rows[-1]
        print(f"    [done] D={D} N={N_used}{'(CAP)' if capped else ''} "
              f"reloc={r['rp_du_m']:.3f} COH_D={r['rp_coh_m']:.3f} "
              f"(split {r['so_coh_m']:.3f} shuf {r['sh_coh_m']:.3f})", flush=True)
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
    print("-" * 108)
    print(f"  bars: LOC_TOL={LOC_TOL} COH_MIN={COH_MIN} COH_SEP={COH_SEP} SHUF_COH_MAX={SHUF_COH_MAX} "
          f"S_STD_REF={S_STD_REF}  (N(D)=min({N_CAP}, 13^D) DENSITY-CONSTANT, DIM={DIM}, eta={REPACK_ETA}, seeds={SEEDS})")
    print(f"  {'D':>2} | {'N(D)':>9} | {'reloc|rs-cA2|':>13} | {'COH_D rp/split/shuf':>26} | "
          f"{'c1':>3} {'c2':>3} {'c3':>3} {'c4':>3} | PASS")
    fails = []
    for r in rows:
        s = score_row(r)
        reloc = f"{r['rp_du_m']:.3f}"
        cohs = f"{r['rp_coh_m']:.3f}/{r['so_coh_m']:.3f}/{r['sh_coh_m']:.3f}"
        nstr = f"{r['N']}{'(CAP)' if r['capped'] else ''}"
        mark = lambda b: " ✅" if b else " ❌"
        print(f"  {r['D']:>2} | {nstr:>9} | {reloc:>13} | {cohs:>26} |"
              f"{mark(s['c1'])}{mark(s['c2'])}{mark(s['c3'])}{mark(s['c4'])} | "
              f"{'PASS' if s['allpass'] else 'FAIL'}")
        if not s["allpass"]:
            fails.append((r["D"], s))
    print("")
    print(f"  per-D detail (RELOCATION per-seed |rs-c_A2|, NO-RETRAIN per-seed |rs-c_A|):")
    for r in rows:
        print(f"    D={r['D']} N={r['N']}{'(CAP, true density-N='+str(r['n_target'])+')' if r['capped'] else ''}: "
              f"reloc {[round(x,3) for x in r['rp_du']]} | split-only {[round(x,3) for x in r['so_du']]} | "
              f"no-retrain {[round(x,3) for x in r['nr_du']]} | COH rp {[round(x,3) for x in r['rp_coh']]} "
              f"shuf {[round(x,3) for x in r['sh_coh']]}")
    print("")
    return fails


def main():
    print("H_1377 — CP N-SCALING: does the H_1375 D*=3 break VANISH under per-dimension density-constant N?")
    print("=" * 108)
    print("DIRECTIONAL numpy mirror ($0 CPU). DECISIVE follow-on to H_1375 (🧱 BREAKS-AT-D*=3 @ CONSTANT N=169).")
    print("ONLY the sampling rule changes: N(D)=min(4000, 13^D) DENSITY-CONSTANT (13/axis = H_1375 anchor).")
    print("D=2→169(anchor) D=3→2197(UNCAPPED, DECISIVE) D=4/6/8→4000(CAPPED, honest truncation). a_break_the_wall.")
    print("")

    rows = ladder()
    print("")
    fails = print_ladder(rows, "DENSITY-CONSTANT LADDER (N(D)=min(4000, 13^D)):")

    # ── compare vs H_1375 constant-N=169 COH_D at the SAME D (context, NON-gating) ──
    h1375_coh = {2: 0.714, 3: 0.428, 4: 0.201, 6: 0.079, 8: 0.038}
    print("  context (NON-gating) — COH_D: density-constant (this) vs H_1375 constant-N=169:")
    for r in rows:
        d = r["D"]
        print(f"    D={d}: COH_D density={r['rp_coh_m']:.3f}  vs  H_1375 const-N={h1375_coh[d]:.3f}  "
              f"(Δ {r['rp_coh_m']-h1375_coh[d]:+.3f})")
    print("")

    # ── ladder verdict ──
    print("=" * 108)
    d3 = next(r for r in rows if r["D"] == 3)
    d3_c2 = score_row(d3)["c2"]
    if not fails:
        print("LADDER VERDICT: 🟢 DIMENSION-INVARIANT-UNDER-DENSITY — the H_1375 D*=3 concentration break")
        print("  VANISHES once per-dimension sample density is held constant; every D passes all four frozen")
        print("  bars under N(D)=min(4000, 13^D). The break was a constant-N SAMPLING ARTIFACT (c16 cause #3),")
        print("  NOT a fundamental dimensional ceiling. move-the-cells RELOCATION + CONCENTRATION are both")
        print("  dimension-invariant under realistic density-constant sampling. NO bar moved (c9/c16/p7).")
        return 0

    Dstar = fails[0][0]
    print(f"LADDER VERDICT: 🧱 CURSE-CEILING-TERMINAL — COH_D STILL breaks at D*={Dstar} even under the")
    print("  density-constant rule. The curse-of-dimensionality concentration ceiling is REAL.")
    for D, s in fails:
        bad = [k for k in ("c1", "c2", "c3", "c4") if not s[k]]
        print(f"    D={D} FAILED bars: {bad}")
    print("")
    print(f"  DECISIVE RUNG (D=3, UNCAPPED N=2197): c2 COHERENCE {'PASS ✅' if d3_c2 else 'FAIL ❌'} "
          f"(COH_D={d3['rp_coh_m']:.3f} vs H_1375 const-N=0.428).")
    if d3_c2:
        print("    → at the UNCAPPED decisive rung the D*=3 break VANISHED: COH_D recovered above COH_MIN once")
        print("      density was held constant. Any remaining FAIL at D≥4 is AMBIGUOUS (N_CAP truncation, NOT")
        print("      true density-constant — a_scale_honest_scope). The break is a SAMPLING ARTIFACT at D=3,")
        print("      with high-D left honestly UNVERIFIED (true density-constant N infeasible on $0 CPU).")
    else:
        print("    → even at the UNCAPPED decisive rung the D*=3 break PERSISTED: holding density constant did")
        print("      NOT rescue COH_D. The curse-of-dimensionality concentration ceiling is REAL/terminal.")
    print("")
    print("  NO bar moved (every threshold VERBATIM from H_1375 / H_1369 R2; c9/c16/p7).")
    return 3


if __name__ == "__main__":
    import sys
    sys.exit(main())
