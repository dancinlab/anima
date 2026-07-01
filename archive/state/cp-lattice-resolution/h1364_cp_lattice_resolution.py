"""
H_1364 — WHORFIAN CP PLASTICITY: LATTICE-RESOLUTION LADDER
R1 numpy MIRROR (DIRECTIONAL). The H_1355 load-bearing follow-on.

Frozen design: .verdicts/1364_cp_lattice_resolution/FREEZE.txt (pre-registered BEFORE this
scoring). $0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335], p7. a_no_llm_frame_trap
(developmental/critical-period plasticity + DISCRETIZATION lens, c15) — NOT an LLM recipe,
NOT a human-cognition claim. ENGINE-TRANSFER UNVERIFIED (directional mirror).

THE QUESTION: H_1355 found CP relocation TRACKS placement geometry, but its ASYM-L rung
(p_A=0.400 -> p_A'=0.200, both cuts left of center) went INCOHERENT at N=21 (peak-count 3>2
on seeds 4333/4335; only seed 4334 relocated coherently). Is that residual incoherence
LATTICE-RESOLUTION-bound (a finer continuum fixes it) or INTRINSIC to split-only re-growth?

H_1364 runs a LATTICE-RESOLUTION LADDER N in [21, 41, 81], scaling N_STIM AND, proportionally,
the RBF basis density DIM and the per-phase split budget GROW_MAX/SPLIT_PASSES (anti-budget-
starvation — the ONLY axis that varies is grid fineness). At each N it re-runs the 5 H_1355
placements and reads (c1) ASYM-L peak-count + CENTER_TOL(N) = max_rung |L - 0.5|. PRE-REGISTERED
DIRECTION (c2): RESOLUTION-BOUND iff ASYM-L coherence recovers (pc<=2 at N=81, fewer incoherent
seeds) AND CENTER_TOL shrinks; INTRINSIC iff incoherence persists at the finest N and/or
CENTER_TOL does not shrink. CHARACTERIZATION ladder — BOTH outcomes VALID (c9).

Machinery (embed / make_basis / VoronoiCells split-only re-growth / soft-posterior discrim /
peak-count coherence) is the H_1333/H_1341/H_1355 algorithm VERBATIM, here parameterized by
(N_STIM, DIM, budget) so the ladder can scale them. At N=21/DIM=16/budget=24 it reproduces
H_1355 EXACTLY (a self-check arm asserts the N=21 ASYM-L landing matches the H_1355 result).
"""
import numpy as np

# ── frozen constants (from FREEZE) ──────────────────────────────────────────
N_BASE       = 21
DIM_BASE     = 16
BUDGET_BASE  = 24
PAIR_STEP    = 1
N_LADDER     = [21, 41, 81]
SEEDS        = [4333, 4334, 4335]

LOC_TOL      = 0.12
COH_MAX_LANG = 2
COH_MIN_SHUF = 3
CENTER       = 0.50

# placements (p_A anchor, p_A' target), H_1355 verbatim
RUNGS = [
    ("RIGHT-REF",  0.333, 0.667),
    ("LEFTWARD-1", 0.667, 0.333),
    ("LEFTWARD-2", 0.800, 0.500),
    ("ASYM-R",     0.600, 0.800),
    ("ASYM-L",     0.400, 0.200),   # the INCOHERENT one at N=21
]


def lattice_params(N):
    """Frozen scaling rule: DIM and per-phase split budget scale PROPORTIONALLY with N so the
    ONLY thing that changes across the ladder is grid fineness (anti-budget-starvation)."""
    dim = int(round(DIM_BASE * N / N_BASE))
    budget = int(round(BUDGET_BASE * N / N_BASE))
    return dim, budget


# ── H_1333 machinery, parameterized by DIM (algorithm byte-identical) ───────
def make_basis(seed, dim):
    rb = np.random.default_rng(seed + 7000)
    centers = np.linspace(0.0, 1.0, dim)
    width = float(rb.uniform(0.10, 0.13))
    return {"centers": centers, "width": width}


def embed(x, basis):
    """RBF population code of scalar x in [0,1] over `dim` evenly-spaced centers (H_1333
    verbatim form). Boundary-AGNOSTIC."""
    centers = basis["centers"]
    width = basis["width"]
    v = np.exp(-((x - centers) ** 2) / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


class VoronoiCells:
    """Immune/Voronoi prototype store, error-targeted SPLIT-only growth (H_1333 verbatim).
    fresh=False grows the EXISTING store further on NEW labels WITHOUT reset (phase-2
    re-train, split-only, never-remove)."""

    def __init__(self):
        self.protos = []
        self.labels = []

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit(self, X, Y, grow_max, passes, fresh=True):
        M = len(X)
        if fresh:
            c0 = X.mean(axis=0)
            n = np.linalg.norm(c0)
            c0 = c0 / n if n > 0 else c0
            self.protos = [c0]
            seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
            self.labels = [int(Y[seed_stim])]
        splits = 0
        for _ in range(passes):
            if splits >= grow_max:
                break
            owners = np.array([self._owner(X[m])[0] for m in range(M)])
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y)[0]
            if len(mism) == 0:
                break
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy())
            self.labels.append(int(Y[s]))
            splits += 1
        return self

    def posterior(self, key):
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        beta = 18.0
        w = np.exp(-beta * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


def discrim_curve(cells, X, positions):
    mids, raw = [], []
    for i in range(0, len(positions) - PAIR_STEP):
        j = i + PAIR_STEP
        d = abs(cells.posterior(X[i]) - cells.posterior(X[j]))
        mids.append(0.5 * (positions[i] + positions[j]))
        raw.append(d)
    mids = np.array(mids)
    raw = np.array(raw)
    mx = raw.max()
    norm = raw / mx if mx > 0 else raw
    return mids, norm, raw


def peak_loc(mids, curve):
    return float(mids[int(np.argmax(curve))])


def peak_count(curve):
    """COHERENCE: # midpoints >= 0.5 * arm's own peak. 1 = single coherent CP peak; >=3 =
    incoherent/scattered."""
    c = np.array(curve)
    if c.max() <= 0:
        return 0
    return int((c >= 0.5 * c.max()).sum())


def labels_cut(positions, cut):
    return (positions > cut).astype(int)


def run_rung(seed, p_a1, p_a2, N, dim, budget):
    """All 4 arms for ONE seed at ONE placement, at lattice resolution N/dim/budget."""
    basis = make_basis(seed, dim)
    positions = np.linspace(0.0, 1.0, N)
    X = np.array([embed(x, basis) for x in positions])

    Y_A  = labels_cut(positions, p_a1)
    Y_A2 = labels_cut(positions, p_a2)
    sh_rng = np.random.default_rng(seed + 4)
    Y_sh = sh_rng.integers(0, 2, size=len(positions))

    out = {}

    cA = VoronoiCells().fit(X, Y_A, budget, budget, fresh=True)
    mids, norm, _ = discrim_curve(cA, X, positions)
    out["A"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cA.protos))

    cR = VoronoiCells().fit(X, Y_A, budget, budget, fresh=True)
    nc_p1 = len(cR.protos)
    cR.fit(X, Y_A2, budget, budget, fresh=False)   # re-train, NO reset
    mids, norm, _ = discrim_curve(cR, X, positions)
    out["A2"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cR.protos),
                     ncells_p1=nc_p1)

    cN = VoronoiCells().fit(X, Y_A, budget, budget, fresh=True)
    mids, norm, _ = discrim_curve(cN, X, positions)
    out["noretrain"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cN.protos))

    cS = VoronoiCells().fit(X, Y_sh, budget, budget, fresh=True)
    mids, norm, _ = discrim_curve(cS, X, positions)
    out["shuffle"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cS.protos))

    return out


def run_N(N):
    """Run all 5 placements x 3 seeds at one lattice resolution N. Returns per-rung aggregate
    and the ASYM-L per-seed detail + CENTER_TOL(N)."""
    dim, budget = lattice_params(N)
    table = []
    asyml_detail = None
    c3_ok = True
    print(f"  --- N={N}  (dim={dim} budget={budget}) ---")
    for name, p_a1, p_a2 in RUNGS:
        peaksR, peaksA, peaksN = [], [], []
        pcA, pcR, pcN, pcS = [], [], [], []
        for seed in SEEDS:
            o = run_rung(seed, p_a1, p_a2, N, dim, budget)
            peaksA.append(o["A"]["peak"]); peaksR.append(o["A2"]["peak"]); peaksN.append(o["noretrain"]["peak"])
            pcA.append(o["A"]["pc"]); pcR.append(o["A2"]["pc"]); pcN.append(o["noretrain"]["pc"])
            pcS.append(o["shuffle"]["pc"])
        mean_pR = float(np.mean(peaksR)); mean_pA = float(np.mean(peaksA)); mean_pN = float(np.mean(peaksN))
        mean_frac = float(np.mean([(r - a) / (p_a2 - p_a1) if (p_a2 - p_a1) != 0 else 0.0
                                   for r, a in zip(peaksR, peaksA)]))
        dist_center = mean_pR - CENTER
        # c3 EARNED at this rung
        c3a = all(abs(p - p_a1) <= LOC_TOL for p in peaksN)        # no-retrain holds anchor
        c3b_shuf = all(p >= COH_MIN_SHUF for p in pcS)             # shuffle incoherent
        # NON-ASYM-L lang arms must be coherent; ASYM-L A2 arm is the QUANTITY UNDER TEST.
        if name == "ASYM-L":
            c3b_lang = all(p <= COH_MAX_LANG for p in pcA + pcN)   # A-trained + no-retrain coherent
        else:
            c3b_lang = all(p <= COH_MAX_LANG for p in pcA + pcR + pcN)
        c3 = c3a and c3b_shuf and c3b_lang
        c3_ok = c3_ok and c3
        table.append(dict(name=name, p_a1=p_a1, p_a2=p_a2, mean_pR=mean_pR, mean_pA=mean_pA,
                          mean_pN=mean_pN, mean_frac=mean_frac, dist_center=dist_center,
                          pcR=list(pcR), mean_pcR=float(np.mean(pcR)),
                          n_incoh=int(sum(1 for p in pcR if p >= COH_MIN_SHUF)),
                          mean_pcS=float(np.mean(pcS)), c3a=c3a, c3b_shuf=c3b_shuf,
                          c3b_lang=c3b_lang, c3=c3))
        if name == "ASYM-L":
            asyml_detail = dict(pcR=list(pcR), peaksR=list(peaksR), mean_pR=mean_pR,
                                mean_pcR=float(np.mean(pcR)), mean_frac=mean_frac,
                                n_incoh=int(sum(1 for p in pcR if p >= COH_MIN_SHUF)))
        print(f"      {name:<11} p_A={p_a1:.3f}->{p_a2:.3f}: ABS land L={mean_pR:.3f} "
              f"(|L-.5|={abs(dist_center):.3f}) frac={mean_frac:+.3f} | A2 pc={pcR} "
              f"(mean {np.mean(pcR):.2f}, incoh {sum(1 for p in pcR if p>=COH_MIN_SHUF)}/3) "
              f"shuf pc(mean {np.mean(pcS):.1f}) c3={'PASS' if c3 else 'FAIL'}")
    center_tol = max(abs(c["dist_center"]) for c in table)
    return dict(N=N, dim=dim, budget=budget, table=table, asyml=asyml_detail,
                center_tol=center_tol, c3_ok=c3_ok)


def main():
    print("H_1364 R1 — WHORFIAN CP PLASTICITY: LATTICE-RESOLUTION LADDER")
    print("=" * 92)
    print("paradigm: re-run the H_1355 5 placements at a LATTICE-RESOLUTION LADDER N in")
    print(f"          {N_LADDER} (N_STIM + RBF density DIM + per-phase split budget all scale")
    print("          PROPORTIONALLY, anti-budget-starvation). Read ASYM-L coherence (peak-count)")
    print("          + CENTER_TOL(N)=max_rung|L-0.5| per N. RESOLUTION-BOUND => coherence recovers")
    print("          + CENTER_TOL shrinks as N grows; INTRINSIC => persists. ALL outcomes valid (c9).")
    print(f"seeds={SEEDS}  N_BASE={N_BASE} DIM_BASE={DIM_BASE} BUDGET_BASE={BUDGET_BASE}")
    print(f"COH_MAX_LANG={COH_MAX_LANG} COH_MIN_SHUF={COH_MIN_SHUF} LOC_TOL={LOC_TOL} CENTER={CENTER}")
    print("")

    results = [run_N(N) for N in N_LADDER]
    print("")

    # ── N=21 self-check: must reproduce H_1355 ASYM-L (L=0.375, 2/3 incoherent) ──────
    base = results[0]
    base_asyml = base["asyml"]
    print("=" * 92)
    print("  SELF-CHECK (N=21 reproduces H_1355 ASYM-L):")
    print(f"     ASYM-L landing L={base_asyml['mean_pR']:.3f} (H_1355: 0.375)  "
          f"peak-count {base_asyml['pcR']} (H_1355: [3,1,3])  "
          f"incoherent {base_asyml['n_incoh']}/3 (H_1355: 2/3)")
    reproduced = (abs(base_asyml['mean_pR'] - 0.375) < 1e-6 and base_asyml['pcR'] == [3, 1, 3])
    print(f"     -> reproduces H_1355: {'YES' if reproduced else 'NO (drift!)'}")
    print("")

    # ── c1 REPORT: coherence + CENTER_TOL vs N ──────────────────────────────────────
    print("  c1 — ASYM-L COHERENCE + CENTER_TOL vs N (mean of 3 seeds):")
    print(f"     {'N':>4} {'dim':>4} {'budget':>7} | {'ASYM-L pc(seeds)':>20} {'mean pc':>8} "
          f"{'incoh/3':>8} {'L_ASYM-L':>9} {'frac':>7} | {'CENTER_TOL':>11}")
    for r in results:
        a = r["asyml"]
        print(f"     {r['N']:>4} {r['dim']:>4} {r['budget']:>7} | {str(a['pcR']):>20} "
              f"{a['mean_pcR']:>8.2f} {a['n_incoh']:>6}/3 {a['mean_pR']:>9.3f} {a['mean_frac']:>+7.3f} "
              f"| {r['center_tol']:>11.3f}")
    print("")
    print("     full absolute-landing table per N (all 5 rungs):")
    for r in results:
        print(f"       N={r['N']}: " + "  ".join(
            f"{c['name']}={c['mean_pR']:.3f}(|{abs(c['dist_center']):.3f}|)" for c in r["table"]))
    print(f"     -> c1 CURVE MEASURED at {len(N_LADDER)} N rungs x 5 placements x 3 seeds: PASS")
    print("")

    # ── c3 EARNED (controls) ────────────────────────────────────────────────────────
    c3_all = all(r["c3_ok"] for r in results)
    print(f"  c3 — EARNED controls held at ALL N (no-retrain anchors, shuffle incoherent, "
          f"non-ASYM-L lang coherent): {'PASS' if c3_all else 'FAIL'}")
    for r in results:
        bad = [c["name"] for c in r["table"] if not c["c3"]]
        print(f"     N={r['N']}: {'PASS' if r['c3_ok'] else 'FAIL (rungs: %s)' % bad}")
    print("")

    # ── c2 DISCRIMINATE (pre-registered DIRECTION) ───────────────────────────────────
    print("  c2 — DISCRIMINATE (resolution-bound vs intrinsic, frozen DIRECTION rule):")
    pc_curve = [r["asyml"]["mean_pcR"] for r in results]
    incoh_curve = [r["asyml"]["n_incoh"] for r in results]
    tol_curve = [r["center_tol"] for r in results]
    print(f"     ASYM-L mean peak-count vs N: {[round(x,2) for x in pc_curve]}")
    print(f"     ASYM-L incoherent-seeds vs N: {incoh_curve} (out of 3)")
    print(f"     CENTER_TOL vs N:             {[round(x,3) for x in tol_curve]}")

    fine, base_i = -1, 0
    # (i) coherence recovers
    coh_recovers = (pc_curve[fine] <= COH_MAX_LANG) and (incoh_curve[fine] < incoh_curve[base_i])
    # (ii) CENTER_TOL shrinks: monotone non-increasing AND strictly smaller at finest
    tol_monotone = all(tol_curve[k + 1] <= tol_curve[k] + 1e-9 for k in range(len(tol_curve) - 1))
    tol_shrinks = tol_monotone and (tol_curve[fine] < tol_curve[base_i] - 1e-9)
    # intrinsic conditions
    coh_persists = (pc_curve[fine] > COH_MAX_LANG) or (incoh_curve[fine] >= incoh_curve[base_i])
    tol_no_shrink = tol_curve[fine] >= tol_curve[base_i] - 1e-9

    print(f"     (i)  ASYM-L coherence RECOVERS (pc<=2 at N=81 AND fewer incoherent seeds than N=21)? "
          f"{coh_recovers}  (pc@81={pc_curve[fine]:.2f}, incoh {incoh_curve[base_i]}->{incoh_curve[fine]})")
    print(f"     (ii) CENTER_TOL SHRINKS (monotone & strictly smaller at N=81)? {tol_shrinks}  "
          f"(monotone={tol_monotone}, {tol_curve[base_i]:.3f}->{tol_curve[fine]:.3f})")

    if coh_recovers and tol_shrinks:
        tag = "RESOLUTION-BOUND"
        verdict = (
            "RESOLUTION-BOUND — as the lattice resolution N grows, the ASYM-L incoherence "
            "RECOVERS (peak-count -> <=2, fewer incoherent seeds) AND the CENTER_TOL band "
            "SHRINKS. The H_1355 ASYM-L incoherence was a DISCRETIZATION ARTIFACT of the "
            "coarse N=21 lattice, not a deep limit of split-only re-growth; a finer continuum "
            "fixes it.")
    elif coh_persists or tol_no_shrink:
        tag = "INTRINSIC"
        verdict = (
            "INTRINSIC — the ASYM-L incoherence PERSISTS at the finest lattice (peak-count "
            "stays >2 and/or the same seeds stay incoherent) AND/OR the CENTER_TOL band does "
            "NOT shrink with N. The incoherence is INTRINSIC to split-only same-side leftward "
            "re-growth (the never-removed first-carving cells genuinely fragment the curve), "
            "independent of lattice resolution — an honest, deeper limit (c9).")
    else:
        tag = "MIXED"
        verdict = (
            "MIXED — neither clean recovery nor clean persistence. One of {coherence, "
            "CENTER_TOL} moves with resolution while the other does not (or non-monotone); "
            "reported VERBATIM with the per-N breakdown, NO forced single label (c9).")
    print(f"     => c2 VERDICT: {tag}")
    for line in verdict.split(". "):
        if line.strip():
            print(f"        {line.strip().rstrip('.')}.")
    print("")

    print("=" * 92)
    print("VERDICT: 📈 LATTICE-RESOLUTION LADDER COMPLETE — ASYM-L coherence + CENTER_TOL")
    print(f"  mapped across N={N_LADDER}, 5 placements, 3 seeds. c1 PASS (curve measured) · "
          f"c3 {'PASS' if c3_all else 'FAIL'} (EARNED controls) · c2 = {tag}.")
    print(f"  ASYM-L mean peak-count vs N = {[round(x,2) for x in pc_curve]}  "
          f"(incoherent-seeds {incoh_curve}).")
    print(f"  CENTER_TOL vs N = {[round(x,3) for x in tol_curve]}.")
    print(f"  N=21 self-check reproduces H_1355 ASYM-L: {'YES' if reproduced else 'NO'}.")
    print("  DIRECTIONAL mirror — engine-transfer UNVERIFIED. TOY synthetic, 3 seeds. NO")
    print("  human-cognition claim (a_scale_honest_scope). NO bar moved (c9/p7).")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
