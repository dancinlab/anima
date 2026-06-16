"""
H_1338 — WHORFIAN CP RELOCATION: IS THE RESIDUAL PULL THE NEVER-EVICT GROWTH-MEMORY?
R2 of H_1333 (the load-bearing follow-on). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1338_whorf_cp_eviction/FREEZE.txt (pre-registered BEFORE this
scoring). $0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335] (SAME as H_1333 so the
never-evict arm reproduces the H_1333 anchor IN-RUN). p7. a_no_llm_frame_trap
(developmental/critical-period plasticity + memory-protection-vs-overwrite lens, c15) —
NOT an LLM recipe, NOT a human-cognition claim. ENGINE-TRANSFER UNVERIFIED (directional
mirror, same family as H_1333 R1 / H_1323 R1 / H_1290 / H_1293 R1).

THE QUESTION: H_1333 found a Whorfian CP boundary is GRADED-plastic — re-training the SAME
split-only store on a MOVED boundary relocates the CP peak ~60% (0.325->0.525), NOT fully.
The residual pull was DIAGNOSED (only hypothesized) as the split-only store's NEVER-EVICTED
first-boundary cells (28 cells after phase-2). DECISIVE test: if REMOVING the stale
old-boundary cells COMPLETES the move (->~100%), the residual pull IS the never-evict
property (dual to H_1288 growth-memory); if it STAYS partial, the limit is budget/geometry.

THE ONE NEW MECHANISM (everything else is H_1333 verbatim): an EVICTION/DECAY store that,
during the phase-2 (A->A') re-growth, removes every existing prototype whose BOUND label
conflicts with the re-trained (p_A') label of the stimulus it currently OWNS (a
stale-conflicting cell). The never-evict A->A' arm is the H_1333 arm verbatim (split-only),
so the ONLY difference between never-evict and eviction is whether stale-conflicting cells
are removed in phase-2 — isolating any completion as the EVICTION (V2).

p1/p2/p3/p6: discrimination readout reads ONLY representational distance in the learned
prototype space; NO injected boundary location at test; labels enter ONLY during training.
Eviction keys on a cell's OWN bound label vs the re-trained label of the stimulus it owns;
NO injected target peak. The no-retrain + shuffle arms are the anti-Goodhart discriminators.
"""
import numpy as np

# ── frozen constants (inherited VERBATIM from H_1333 FREEZE) ─────────────────
N_STIM   = 21
DIM      = 16
P_A      = 1.0 / 3.0          # initial language A boundary
P_A2     = 2.0 / 3.0          # RE-trained (moved) boundary p_A'
SHIFT    = abs(P_A2 - P_A)    # 0.333
PAIR_STEP = 1
GROW_MAX = 24                 # max prototype splits PER PHASE (FIXED, H_1333 verbatim)
SPLIT_PASSES = 24             # error-targeted split iterations per phase (H_1333 verbatim)
SEEDS    = [4333, 4334, 4335]

# frozen bar thresholds
LOC_TOL      = 0.12           # peak within tol of a boundary (= H_1333 / H_1323 W2_PEAK_TOL)
COH_MAX_LANG = 2              # a coherent CP arm: peak-count <= 2
COH_MIN_SHUF = 3              # an incoherent shuffle arm: peak-count >= 3
# V1/V2 bars
EVICT_FRAC_MIN  = 0.85        # eviction COMPLETES: move-fraction >= this (V1b)
NEVEREV_FRAC_LO = 0.40        # never-evict reproduces partial (V2a) — brackets H_1333 ~0.60
NEVEREV_FRAC_HI = 0.75


# ── H_1323/H_1333 machinery, reused VERBATIM, + the ONE eviction option ──────
def embed(x, rng_basis):
    """RBF population code of scalar position x in [0,1] over DIM evenly-spaced centers
    (H_1323/H_1333 verbatim). Boundary-AGNOSTIC."""
    centers = rng_basis["centers"]
    width = rng_basis["width"]
    v = np.exp(-((x - centers) ** 2) / (2.0 * width ** 2))
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def make_basis(seed):
    rb = np.random.default_rng(seed + 7000)
    centers = np.linspace(0.0, 1.0, DIM)
    width = float(rb.uniform(0.10, 0.13))
    return {"centers": centers, "width": width}


class VoronoiCells:
    """Immune/Voronoi prototype store, error-targeted SPLIT-only growth (p8 mirror,
    H_1333 verbatim). H_1338 adds ONE option to fit(): evict=True. When evict=True, during
    THIS fit() call, BEFORE each split, every prototype whose BOUND label conflicts with the
    label Y of the stimulus it currently OWNS is removed (a stale-conflicting cell). The last
    surviving prototype is never removed. evict=False (default) == H_1333 split-only behavior
    EXACTLY. Eviction is used ONLY in the eviction arm's phase-2 re-train; every other call
    (phase-1, A-trained, no-retrain, shuffle) uses evict=False == H_1333 verbatim."""

    def __init__(self):
        self.protos = []
        self.labels = []

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def _evict_stale_conflicting(self, X, Y):
        """Remove every prototype whose bound label disagrees with the label Y of the
        stimulus it currently owns (under the re-trained boundary). Keeps >=1 cell.
        Returns # evicted. Structural store op — keyed on cell's OWN label vs owned-stimulus
        re-trained label; NO injected target peak (p2/p3/p6)."""
        M = len(X)
        owners = np.array([self._owner(X[m])[0] for m in range(M)])
        # for each prototype, does the re-trained label of ANY stimulus it owns conflict
        # with its bound label? (a prototype that still says 0 but now owns a 1-stimulus)
        kill = []
        for c in range(len(self.protos)):
            owned = np.where(owners == c)[0]
            if len(owned) == 0:
                continue
            lab_c = self.labels[c]
            # conflict if the re-trained label of any owned stimulus != this cell's label
            if np.any(Y[owned] != lab_c):
                kill.append(c)
        if not kill:
            return 0
        keep = [c for c in range(len(self.protos)) if c not in kill]
        if len(keep) == 0:                       # never empty the store: keep the 1st kill cell
            keep = [kill[0]]
        self.protos = [self.protos[c] for c in keep]
        self.labels = [self.labels[c] for c in keep]
        return len(self.protos) and (len(kill) - (0 if len(keep) > 0 else 0)) or 0

    def fit(self, X, Y, grow_max, passes, fresh=True, evict=False):
        """Error-targeted SPLIT-only growth (H_1333 verbatim). fresh=True seeds a new store
        (phase 1); fresh=False grows the EXISTING store further on NEW labels WITHOUT reset
        (phase-2 re-training). evict=True (H_1338, used ONLY in eviction-arm phase-2) removes
        stale-conflicting cells before each split. Budget grow_max applies to splits IN THIS
        call. The split criterion is the SAME as H_1333; only seeding/eviction differ."""
        M = len(X)
        if fresh:
            c0 = X.mean(axis=0)
            n = np.linalg.norm(c0)
            c0 = c0 / n if n > 0 else c0
            self.protos = [c0]
            seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
            self.labels = [int(Y[seed_stim])]
        # else: keep existing self.protos / self.labels (phase-2 re-train on the same store).
        splits = 0
        for _ in range(passes):
            if evict:
                self._evict_stale_conflicting(X, Y)   # remove stale cells before this split
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
        """Soft category-posterior P(cat=1) = softmin-weighted vote of nearby prototypes'
        bound labels (H_1333 verbatim)."""
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        beta = 18.0
        w = np.exp(-beta * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


def build_labels(positions, kind, rng):
    """category labels over the continuum (H_1333 verbatim).
       'A' -> cut at P_A; 'A2' -> cut at P_A2; 'shuffle' -> random per-stimulus label."""
    if kind == "A":
        return (positions > P_A).astype(int)
    if kind == "A2":
        return (positions > P_A2).astype(int)
    if kind == "shuffle":
        return rng.integers(0, 2, size=len(positions))
    raise ValueError(kind)


def discrim_curve(cells, X, positions):
    """discrimination(midpoint) = |Δ soft-posterior| over adjacent pairs (H_1333 verbatim)."""
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
    """COHERENCE metric (H_1333 EARNED bar): # midpoints reaching >=0.5 * arm's own peak."""
    c = np.array(curve)
    if c.max() <= 0:
        return 0
    return int((c >= 0.5 * c.max()).sum())


def run_seed(seed):
    """Run all arms for one seed. Same stimulus world across arms (basis fixed by seed)."""
    rng = np.random.default_rng(seed)
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([embed(x, basis) for x in positions])

    Y_A = build_labels(positions, "A", None)
    Y_A2 = build_labels(positions, "A2", None)
    sh_rng = np.random.default_rng(seed + 4)
    Y_sh = build_labels(positions, "shuffle", sh_rng)

    out = {}

    # (0) A-trained: grow on labels(p_A) only -> reproduce H_1323 (shared baseline peak p_A).
    cA = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cA, X, positions)
    out["A"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cA.protos))

    # (1) NEVER-EVICT A->A' (= H_1333 verbatim): phase-1 on p_A, phase-2 grow further on p_A'.
    cNE = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    nc_p1 = len(cNE.protos)
    cNE.fit(X, Y_A2, GROW_MAX, SPLIT_PASSES, fresh=False, evict=False)   # split-only, NO evict
    mids, norm, _ = discrim_curve(cNE, X, positions)
    out["neverevict"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm),
                             ncells=len(cNE.protos), ncells_p1=nc_p1)

    # (2) EVICTION-STORE A->A': phase-1 IDENTICAL to (1); phase-2 grows on p_A' WITH eviction
    #     of stale-conflicting cells. ONLY difference vs (1) is evict=True in phase-2.
    cEV = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    nc_p1_ev = len(cEV.protos)
    cEV.fit(X, Y_A2, GROW_MAX, SPLIT_PASSES, fresh=False, evict=True)    # EVICT stale cells
    mids, norm, _ = discrim_curve(cEV, X, positions)
    out["eviction"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm),
                           ncells=len(cEV.protos), ncells_p1=nc_p1_ev)

    # (3) NO-RETRAIN control, BOTH stores: grow on p_A only, no phase-2 -> must stay at p_A.
    cN = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cN, X, positions)
    out["noretrain_ne"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm),
                               ncells=len(cN.protos))
    # eviction store with NO phase-2 re-train = a pure split-only p_A store (evict only fires
    # in phase-2 which is absent) -> identical no-retrain peak; run separately for V3 totality.
    cNev = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cNev, X, positions)
    out["noretrain_ev"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm),
                               ncells=len(cNev.protos))

    # (4) SHUFFLE: incoherent labels -> EARNED control (must be incoherent).
    cS = VoronoiCells().fit(X, Y_sh, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cS, X, positions)
    out["shuffle"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cS.protos))

    return positions, out


def main():
    print("H_1338 R1 — WHORFIAN CP RESIDUAL: NEVER-EVICT GROWTH-MEMORY OR BUDGET/GEOMETRY?")
    print("=" * 84)
    print("R2 of H_1333: does EVICTING stale old-boundary cells COMPLETE the CP relocation?")
    print("paradigm: train A (cut p_A), re-train SAME store on moved p_A'; compare NEVER-EVICT")
    print("          (= H_1333 split-only) vs EVICTION (remove stale-conflicting cells) move.")
    print(f"N_stim={N_STIM} dim={DIM} p_A={P_A:.3f} p_A'={P_A2:.3f} shift={SHIFT:.3f} "
          f"grow_max={GROW_MAX}/phase seeds={SEEDS}")
    print("")

    keys = ["A", "neverevict", "eviction", "noretrain_ne", "noretrain_ev", "shuffle"]
    per = {k: [] for k in keys}     # peak loc per seed
    pc = {k: [] for k in keys}      # peak-count per seed
    fr = {"neverevict": [], "eviction": []}   # move-fraction per seed
    nc_info = []

    def frac(peak_r, peak_a):
        return (peak_r - peak_a) / (P_A2 - P_A) if (P_A2 - P_A) != 0 else 0.0

    print("  per-seed CP peak location:")
    for seed in SEEDS:
        positions, out = run_seed(seed)
        for k in keys:
            per[k].append(out[k]["peak"])
            pc[k].append(out[k]["pc"])
        f_ne = frac(out["neverevict"]["peak"], out["A"]["peak"])
        f_ev = frac(out["eviction"]["peak"], out["A"]["peak"])
        fr["neverevict"].append(f_ne)
        fr["eviction"].append(f_ev)
        nc_info.append((seed, out["neverevict"]["ncells_p1"], out["neverevict"]["ncells"],
                        out["eviction"]["ncells"]))
        print(f"    seed {seed}:  A={out['A']['peak']:.3f}  "
              f"never-evict={out['neverevict']['peak']:.3f}(frac{f_ne:+.2f})  "
              f"eviction={out['eviction']['peak']:.3f}(frac{f_ev:+.2f})  "
              f"no-retr={out['noretrain_ne']['peak']:.3f}  shuf={out['shuffle']['peak']:.3f}")
        print(f"               peak-count: A={out['A']['pc']} "
              f"never-evict={out['neverevict']['pc']} eviction={out['eviction']['pc']} "
              f"no-retr={out['noretrain_ne']['pc']} shuf={out['shuffle']['pc']}")
    print("")

    mean = {k: float(np.mean(per[k])) for k in keys}
    mpc = {k: float(np.mean(pc[k])) for k in keys}
    mfr = {k: float(np.mean(fr[k])) for k in fr}
    print("  mean CP peak (over 3 seeds):")
    print(f"    A-trained:          {mean['A']:.3f}   (p_A ={P_A:.3f})")
    print(f"    NEVER-EVICT A->A':  {mean['neverevict']:.3f}   (p_A'={P_A2:.3f})   "
          f"move-fraction {mfr['neverevict']:+.2f}")
    print(f"    EVICTION   A->A':   {mean['eviction']:.3f}   (p_A'={P_A2:.3f})   "
          f"move-fraction {mfr['eviction']:+.2f}")
    print(f"    no-retrain (NE):    {mean['noretrain_ne']:.3f}   (p_A ={P_A:.3f})")
    print(f"    no-retrain (EV):    {mean['noretrain_ev']:.3f}   (p_A ={P_A:.3f})")
    print(f"    shuffle:            {mean['shuffle']:.3f}")
    print(f"  mean peak-count: A={mpc['A']:.1f} never-evict={mpc['neverevict']:.1f} "
          f"eviction={mpc['eviction']:.1f} no-retr={mpc['noretrain_ne']:.1f} "
          f"shuffle={mpc['shuffle']:.1f}")
    print(f"  cell budget (seed, p1, never-evict-p2, eviction-p2): {nc_info}")
    print("")

    # ── V1 COMPLETES (eviction relocates fully) ────────────────────────────────
    v1a = all(abs(p - P_A2) <= LOC_TOL for p in per["eviction"])         # reaches p_A'
    v1b = all(f >= EVICT_FRAC_MIN for f in fr["eviction"])              # frac >= 0.85
    v1_coh = mpc["eviction"] <= COH_MAX_LANG                             # stays coherent
    v1 = v1a and v1b and v1_coh
    print(f"  V1 COMPLETES (eviction: all 3 seeds |peak-p_A'|<={LOC_TOL} AND frac>="
          f"{EVICT_FRAC_MIN}; coherent peak-count<={COH_MAX_LANG}):")
    print(f"     eviction per-seed |peak-p_A'| = {[round(abs(p-P_A2),3) for p in per['eviction']]}"
          f"  -> reaches-new {'PASS' if v1a else 'FAIL'}")
    print(f"     eviction per-seed move-fraction = {[round(f,3) for f in fr['eviction']]}"
          f"  -> full-move {'PASS' if v1b else 'FAIL'}")
    print(f"     eviction mean peak-count = {mpc['eviction']:.1f}  -> coherent "
          f"{'PASS' if v1_coh else 'FAIL'}")
    print(f"     -> V1 {'PASS' if v1 else 'FAIL'}")

    # ── V2 CONTRAST (never-evict reproduces H_1333 partial in-run) ──────────────
    v2a = all(NEVEREV_FRAC_LO <= f <= NEVEREV_FRAC_HI for f in fr["neverevict"])  # partial
    v2b = all(abs(p - P_A2) > LOC_TOL for p in per["neverevict"])       # did NOT complete
    v2 = v2a and v2b
    print(f"  V2 CONTRAST (never-evict in-run partial: all 3 seeds frac in "
          f"[{NEVEREV_FRAC_LO},{NEVEREV_FRAC_HI}] AND |peak-p_A'|>{LOC_TOL}):")
    print(f"     never-evict per-seed move-fraction = {[round(f,3) for f in fr['neverevict']]}"
          f"  -> partial {'PASS' if v2a else 'FAIL'}")
    print(f"     never-evict per-seed |peak-p_A'| = "
          f"{[round(abs(p-P_A2),3) for p in per['neverevict']]}  -> not-complete "
          f"{'PASS' if v2b else 'FAIL'}")
    print(f"     -> V2 {'PASS' if v2 else 'FAIL'}")

    # ── V3 EARNED (no-retrain stays at p_A both stores; shuffle incoherent) ─────
    v3_nr = (all(abs(p - P_A) <= LOC_TOL for p in per["noretrain_ne"])
             and all(abs(p - P_A) <= LOC_TOL for p in per["noretrain_ev"]))
    v3_shuf = mpc["shuffle"] >= COH_MIN_SHUF
    v3 = v3_nr and v3_shuf
    print(f"  V3 EARNED (no-retrain both stores |peak-p_A|<={LOC_TOL}; shuffle incoherent "
          f"peak-count>={COH_MIN_SHUF}):")
    print(f"     no-retrain NE |peak-p_A| = {[round(abs(p-P_A),3) for p in per['noretrain_ne']]}"
          f"  EV = {[round(abs(p-P_A),3) for p in per['noretrain_ev']]}  -> "
          f"{'PASS' if v3_nr else 'FAIL'}")
    print(f"     shuffle peak-count = {mpc['shuffle']:.1f}  -> {'PASS' if v3_shuf else 'FAIL'}")
    print(f"     -> V3 {'PASS' if v3 else 'FAIL'}")

    print("=" * 84)
    green = v1 and v2 and v3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — the H_1333 RESIDUAL PULL *IS* the")
        print("  NEVER-EVICT growth-memory property. In the SAME run, evicting the stale")
        print(f"  old-boundary cells COMPLETES the CP move (eviction {mean['A']:.3f}->"
              f"{mean['eviction']:.3f}, frac {mfr['eviction']:+.2f})")
        print(f"  while the never-evict store stays partial ({mean['A']:.3f}->"
              f"{mean['neverevict']:.3f}, frac {mfr['neverevict']:+.2f}, reproducing H_1333).")
        print("  No-retrain held at p_A (both stores), shuffle incoherent. CLEAN TIE: H_1288")
        print("  growth-memory = protect-old-memory = partial-plasticity; eviction =")
        print("  full-plasticity — the two are DUAL. ENGINE-TRANSFER UNVERIFIED — R3 follow-on.")
        print("  TOY synthetic continuum, 3 seeds; NO human-cognition claim (a_scale_honest_scope).")
        return 0
    # honest non-green branches (NO bar move, c9)
    if v2 and v3 and not v1:
        print("VERDICT: 🧱 RE-DIAGNOSIS — eviction does NOT complete the move. Removing the")
        print(f"  stale old-boundary cells leaves the eviction move at frac {mfr['eviction']:+.2f}")
        print(f"  (mean {mean['A']:.3f}->{mean['eviction']:.3f}), still short of p_A'={P_A2:.3f},")
        print("  while never-evict reproduced the H_1333 partial. So the H_1333 residual pull is")
        print("  NOT (only) never-evicted old cells — the limit is BUDGET / GEOMETRY. An honest,")
        print("  important re-diagnosis of H_1333's residual. NO bar move (c9). ENGINE-TRANSFER")
        print("  UNVERIFIED. TOY synthetic, 3 seeds.")
        return 3
    if not v2:
        print("VERDICT: 🧱 CONFOUNDED — the never-evict arm did NOT reproduce the H_1333 ~0.60")
        print(f"  partial in-run (frac {mfr['neverevict']:+.2f}); the eviction comparison is")
        print("  confounded by a run difference. Honest, NO bar move (c9). Treat V1 cautiously.")
        return 2
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen EARNED bar failed (V3: no-retrain drift or")
    print("  shuffle coherent). Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
