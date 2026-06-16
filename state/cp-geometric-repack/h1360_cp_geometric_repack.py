"""
H_1360 — WHORFIAN CP RELOCATION: GEOMETRIC RE-PACK (move the cells, not their weight/count).
R2 follow-on of H_1352 (the soft-decay DEEPER-LIMIT) and H_1340 (the budget-sweep DEEPER-LIMIT).
R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1360_cp_geometric_repack/FREEZE.txt (pre-registered BEFORE this scoring).
$0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335] (SAME as H_1333/H_1338/H_1340/H_1352 so the
NO-REPACK arm reproduces the H_1340 R0_base anchor IN-RUN). p7. a_no_llm_frame_trap /
a_break_the_wall (developmental/critical-period plasticity + memory-protection-vs-overwrite
lens, c15) -- NOT an LLM recipe, NOT a human-cognition claim. ENGINE-TRANSFER UNVERIFIED
(directional mirror, same family as H_1333/H_1338/H_1340/H_1352 R1).

THE QUESTION: TWO orthogonal levers are exhausted as WALLS. H_1340 (budget+RBF density) buys
DISTANCE toward p_A' but DESTROYS coherence (peak-count 4.3->7.0). H_1352 (soft-decay, quiet the
VOTE) relocates EVEN BETTER (frac +0.88) but coherence collapses HARDER (15.7). Both follow-ons
exposed the SAME decisive cause: the phase-1 prototypes are NEVER PHYSICALLY RELOCATED -- they
SIT at the old cut and inject secondary peaks. Budget drowns them, decay quiets their vote, but
NEITHER moves the cells. The H_1352 card named the ONLY untried lever: "the old cells must MOVE
or be re-positioned (GEOMETRIC re-pack)." H_1360 tests EXACTLY that -- the THIRD lever.

THE ONE NEW MECHANISM = a GEOMETRIC RE-PACK. Everything else is H_1333/H_1340/H_1352 verbatim
(this file IMPORTS that machinery). During phase-2 (A->A') re-training, after every phase-2
split each residual phase-1 cell's SOURCE POSITION drifts a FROZEN fraction REPACK_ETA of the
remaining distance toward p_A', and the cell is RE-EMBEDDED at the drifted position with its
label RE-READ from the new boundary. We move the CELLS in feature space -- not their weight
(H_1352 decay) or their count (H_1340 budget). Budget is held at the H_1340 R0_base LOW value
(DIM=16/GROW2=24), SAME as H_1352 -- NO inflation; the ONLY change is the geometric drift.

p1/p2/p3/p6: discrimination readout reads ONLY representational distance; NO injected boundary
location at test; the re-pack keys on a cell's BIRTH PHASE + its own source position (a
structural store property, NO injected target peak / persona / RLHF); labels enter ONLY during
training (re-read from the SAME p_A' that trains phase-2 cells). The no-retrain + shuffle arms
are the anti-Goodhart discriminators; the no-repack arm (must STAY partial+incoherent in-run)
isolates the geometric drift as the lever.
"""
import importlib.util
import os
import sys

import numpy as np

# ── import the H_1333 / H_1340 / H_1352 CP machinery VERBATIM (do NOT re-implement) ──
_HERE = os.path.dirname(os.path.abspath(__file__))
_H1333 = os.path.abspath(os.path.join(_HERE, "..", "universe-probes", "h1333_whorf_developmental.py"))
_spec = importlib.util.spec_from_file_location("h1333_whorf_developmental", _H1333)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
# reuse: h.embed, h.VoronoiCells, h.discrim_curve, h.peak_loc, h.peak_count

# ── frozen constants (inherited VERBATIM from H_1333 / H_1340 / H_1352 FREEZE) ───────
P_A    = 1.0 / 3.0            # initial language A boundary (h.P_A)
P_A2   = 2.0 / 3.0           # RE-trained (moved) boundary p_A' (h.P_A2)
N_STIM = 81                  # = H_1340/H_1352 (finer than H_1338's 21; constant = not a confound)
DIM    = 16                  # LOW = H_1340 R0_base / H_1352 RBF density (NOT inflated)
PHASE1_BUDGET = 24           # phase-1 split budget, FIXED (= H_1333/H_1338/H_1340/H_1352)
GROW2  = 24                  # phase-2 budget LOW = H_1340 R0_base / H_1352 (NO budget inflation)
SEEDS  = [4333, 4334, 4335]  # SAME as H_1333/H_1338/H_1340/H_1352 (no-repack arm reproduces anchor)

# frozen geometric-re-pack schedule (PRE-REGISTERED; gate scored ONLY at REPACK_ETA=0.15)
REPACK_ETA   = 0.15          # phase-1 source position moves this fraction toward p_A' per split
REPACK_LADDER = [0.10, 0.15, 0.25]   # NON-GATING diagnostic (knife-edge check), gate=0.15 only

# frozen bar thresholds (from FREEZE)
LOC_TOL       = 0.12         # |peak - boundary| reach tolerance (= H_1333/H_1340/H_1352)
COH_MAX       = 2            # c2 / c4a: coherent CP arm has peak-count <= this
SHUF_MIN_PC   = 3            # c3b: shuffle control must be incoherent (peak-count >= this)
H1340_BEST_DIST = 0.081      # c4b: best (closest) H_1340 rung |peak-p_A'| (R4_high, from card)
H1340_MIN_PC    = 4.3        # ref: lowest H_1340 rung peak-count (R0_base; all rungs >= this)
H1352_PC        = 15.7       # ref: H_1352 soft-decay peak-count (the lever c4 must beat)


def make_basis_dim(seed, dim):
    """H_1333 make_basis VERBATIM except DIM is a parameter. Same width draw (seed+7000).
    Identical to H_1352.make_basis_dim so the NO-REPACK anchor is byte-comparable."""
    rb = np.random.default_rng(seed + 7000)
    centers = np.linspace(0.0, 1.0, dim)
    width = float(rb.uniform(0.10, 0.13))
    return {"centers": centers, "width": width}


class RepackCells(h.VoronoiCells):
    """H_1333 VoronoiCells + a GEOMETRIC RE-PACK of residual phase-1 cells during phase-2.

    We track each cell's SOURCE continuum position (pos_i) and its BIRTH PHASE. The base phase-1
    fit() is reused VERBATIM (split-only never-evict growth) -- we only record the source
    positions of the cells it creates. Phase-2 is re-implemented HERE (same split criterion as
    H_1333) so that, after each phase-2 split, every phase-1 cell's source position is DRIFTED a
    fraction REPACK_ETA toward p_A', and the cell is RE-EMBEDDED + its label RE-READ from p_A'.

    With eta=0.0 (or n_p2=0) the store is BYTE-IDENTICAL to H_1333/H_1340 R0_base (the NO-REPACK
    anchor) -- the drift simply never fires.
    """

    def __init__(self, eta=0.0, basis=None, p_new=P_A2):
        super().__init__()
        self.eta = eta
        self.basis = basis
        self.p_new = p_new
        self.pos = []          # source continuum position per cell (parallel to self.protos)
        self.n_phase1 = 0      # how many cells exist after phase-1 (cells [0:n_phase1) re-pack)

    # -- phase-1: reuse base fit() VERBATIM, then record source positions of created cells. --
    def fit_phase1(self, X, Y, positions):
        super().fit(X, Y, PHASE1_BUDGET, PHASE1_BUDGET, fresh=True)
        # recover the source continuum position of every proto by matching its embedding to X.
        # protos are exact copies of X rows (split-only stores X[s].copy()) plus a seed mean.
        self.pos = []
        for p in self.protos:
            d = [float(np.linalg.norm(p - X[m])) for m in range(len(X))]
            self.pos.append(float(positions[int(np.argmin(d))]))
        self.n_phase1 = len(self.protos)
        return self

    def _repack_phase1(self):
        """Drift every phase-1 cell's source position one REPACK_ETA step toward p_new, clamp at
        p_new (no overshoot), re-embed at the drifted position, re-read its label from p_new.
        Phase-2 cells (index >= n_phase1) are untouched -- they are already at the new locus."""
        if self.eta <= 0.0:
            return
        for i in range(self.n_phase1):
            new_pos = self.pos[i] + self.eta * (self.p_new - self.pos[i])
            # clamp so a cell crossing p_new does not overshoot past the boundary
            if (self.p_new - self.pos[i]) >= 0:
                new_pos = min(new_pos, self.p_new)
            else:
                new_pos = max(new_pos, self.p_new)
            self.pos[i] = float(new_pos)
            self.protos[i] = h.embed(new_pos, self.basis)
            self.labels[i] = int(new_pos > self.p_new)

    def fit_phase2(self, X, Y2, positions, grow2):
        """Phase-2 re-growth on labels Y2 (the moved boundary), with a geometric re-pack of the
        residual phase-1 cells after EACH split. Same split criterion as H_1333.fit (error-
        targeted, split the worst-owned mismatched stimulus). New cells are phase-2 (no drift)."""
        M = len(X)
        splits = 0
        for _ in range(grow2):
            if splits >= grow2:
                break
            owners = np.array([self._owner(X[m])[0] for m in range(M)])
            cell_lab = np.array(self.labels)[owners]
            mism = np.where(cell_lab != Y2)[0]
            if len(mism) == 0:
                # no remaining error -- still re-pack so the residual keeps migrating each step
                self._repack_phase1()
                break
            md = [float(np.linalg.norm(X[m] - self.protos[owners[m]])) for m in mism]
            s = int(mism[int(np.argmin(md))])
            self.protos.append(X[s].copy())
            self.labels.append(int(Y2[s]))
            self.pos.append(float(positions[s]))   # phase-2 cell, will not be drifted
            splits += 1
            self._repack_phase1()                  # MOVE the residual phase-1 cells one step
        return self


def reloc(seed, eta, kind="A2"):
    """Phase-1 carve p_A (FIXED budget), then phase-2 re-grow on labels(kind) with geometric
    re-pack eta. kind='A2' = moved boundary; kind='shuffle' = incoherent control. Returns the
    relocated peak, A-trained peak (same basis), peak-count, cell budgets."""
    basis = make_basis_dim(seed, DIM)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([h.embed(x, basis) for x in positions])
    Y_A = (positions > P_A).astype(int)
    if kind == "A2":
        Y_2 = (positions > P_A2).astype(int)
    elif kind == "shuffle":
        sh = np.random.default_rng(seed + 4)
        Y_2 = sh.integers(0, 2, size=len(positions))
    else:
        raise ValueError(kind)

    # A-trained baseline peak (phase-1 only) -- the move-fraction reference (eta irrelevant,
    # no phase-2 so no drift fires).
    cA = RepackCells(eta=eta, basis=basis).fit_phase1(X, Y_A, positions)
    midsA, normA, _ = h.discrim_curve(cA, X, positions)
    peakA = h.peak_loc(midsA, normA)

    # Relocation: phase-1 FIXED budget on p_A, then phase-2 LOW budget on labels(kind) + re-pack.
    cR = RepackCells(eta=eta, basis=basis).fit_phase1(X, Y_A, positions)
    nc_p1 = len(cR.protos)
    cR.fit_phase2(X, Y_2, positions, GROW2)
    midsR, normR, _ = h.discrim_curve(cR, X, positions)
    peakR = h.peak_loc(midsR, normR)
    pcR = h.peak_count(normR)
    return dict(peakA=peakA, peakR=peakR, pcR=pcR, nc_p1=nc_p1, nc_p2=len(cR.protos))


def noretrain(seed):
    """NO-RETRAIN control: grow on p_A only, no phase-2, no re-pack -> must hold p_A."""
    basis = make_basis_dim(seed, DIM)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([h.embed(x, basis) for x in positions])
    Y_A = (positions > P_A).astype(int)
    cN = RepackCells(eta=0.0, basis=basis).fit_phase1(X, Y_A, positions)
    midsN, normN, _ = h.discrim_curve(cN, X, positions)
    return h.peak_loc(midsN, normN)


def frac(peak_r, peak_a):
    return (peak_r - peak_a) / (P_A2 - P_A) if (P_A2 - P_A) != 0 else 0.0


def main():
    print("H_1360 R1 -- WHORFIAN CP RELOCATION: GEOMETRIC RE-PACK (move the cells)")
    print("=" * 86)
    print("R2 of H_1340/H_1352: at FIXED LOW budget (DIM=16/GROW2=24), does physically DRIFTING")
    print("              the residual phase-1 cells toward p_A' recover a COHERENT relocation?")
    print(f"N_stim={N_STIM} DIM={DIM} p_A={P_A:.3f} p_A'={P_A2:.3f} phase1={PHASE1_BUDGET} "
          f"phase2={GROW2} eta={REPACK_ETA} seeds={SEEDS}  (split-only never-evict + geo re-pack)")
    print("")

    # ── per-seed arms at the FROZEN eta=0.15 ────────────────────────────────────────
    nr_peaks, nr_dists, nr_fracs, nr_pcs = [], [], [], []   # NO-REPACK (eta=0.0 anchor)
    rp_peaks, rp_dists, rp_fracs, rp_pcs = [], [], [], []   # RE-PACK (eta=0.15)
    noR_dists = []                                          # NO-RETRAIN
    sh_pcs = []                                             # SHUFFLE + re-pack
    print("  per-seed (NO-REPACK eta=0.0 / RE-PACK eta=0.15 / NO-RETRAIN / SHUFFLE+repack):")
    for seed in SEEDS:
        nr = reloc(seed, eta=0.0, kind="A2")               # == H_1340 R0_base / H_1352 anchor
        rp = reloc(seed, eta=REPACK_ETA, kind="A2")
        noRp = noretrain(seed)
        sh = reloc(seed, eta=REPACK_ETA, kind="shuffle")

        nr_peaks.append(nr["peakR"]); nr_dists.append(abs(nr["peakR"] - P_A2))
        nr_fracs.append(frac(nr["peakR"], nr["peakA"])); nr_pcs.append(nr["pcR"])
        rp_peaks.append(rp["peakR"]); rp_dists.append(abs(rp["peakR"] - P_A2))
        rp_fracs.append(frac(rp["peakR"], rp["peakA"])); rp_pcs.append(rp["pcR"])
        noR_dists.append(abs(noRp - P_A))
        sh_pcs.append(sh["pcR"])
        print(f"    seed {seed}: NO-REPACK peak={nr['peakR']:.3f} pc={nr['pcR']} | "
              f"RE-PACK peak={rp['peakR']:.3f} pc={rp['pcR']} | "
              f"no-retrain peak={noRp:.3f} | shuffle pc={sh['pcR']}  "
              f"cells(p1,p2)={rp['nc_p1']},{rp['nc_p2']}")
    print("")

    nr_peak_m = float(np.mean(nr_peaks)); nr_dist_m = float(np.mean(nr_dists))
    nr_frac_m = float(np.mean(nr_fracs)); nr_pc_m = float(np.mean(nr_pcs))
    rp_peak_m = float(np.mean(rp_peaks)); rp_dist_m = float(np.mean(rp_dists))
    rp_frac_m = float(np.mean(rp_fracs)); rp_pc_m = float(np.mean(rp_pcs))
    noR_dist_m = float(np.mean(noR_dists)); sh_pc_m = float(np.mean(sh_pcs))
    print(f"  NO-REPACK  (anchor): peak {nr_peak_m:.3f} |peak-p_A'| {nr_dist_m:.3f} "
          f"frac {nr_frac_m:+.2f} peak-count {nr_pc_m:.1f}")
    print(f"  RE-PACK    (e=0.15): peak {rp_peak_m:.3f} |peak-p_A'| {rp_dist_m:.3f} "
          f"frac {rp_frac_m:+.2f} peak-count {rp_pc_m:.1f}")
    print(f"  NO-RETRAIN: mean |peak-p_A| {noR_dist_m:.3f}  |  SHUFFLE+repack: peak-count {sh_pc_m:.1f}")
    print("")

    # ── NON-GATING diagnostic: re-pack-ladder (knife-edge check; gate scored ONLY at 0.15) ──
    print("  [NON-GATING diagnostic] RE-PACK-LADDER (gate is scored ONLY at eta=0.15):")
    for e in REPACK_LADDER:
        ds, ps = [], []
        for seed in SEEDS:
            r = reloc(seed, eta=e, kind="A2")
            ds.append(abs(r["peakR"] - P_A2)); ps.append(r["pcR"])
        tag = "  <-- FROZEN GATE" if abs(e - REPACK_ETA) < 1e-9 else ""
        print(f"     eta={e:.2f}: |peak-p_A'| mean={np.mean(ds):.3f}  "
              f"peak-count mean={np.mean(ps):.1f}{tag}")
    print("")

    # ── BARS ────────────────────────────────────────────────────────────────────────
    c1 = all(d <= LOC_TOL for d in rp_dists)                            # RELOCATES (all seeds)
    c2 = rp_pc_m <= COH_MAX                                             # COHERENT
    c3a = all(d <= LOC_TOL for d in noR_dists)                          # no-retrain holds p_A
    c3b = sh_pc_m >= SHUF_MIN_PC                                        # shuffle collapses
    c3 = c3a and c3b
    c4a = rp_pc_m <= COH_MAX                                            # coherent where 1340/1352 not
    c4b = rp_dist_m <= H1340_BEST_DIST                                  # >= best H_1340 closeness
    c4 = c4a and c4b

    print(f"  c1 RELOCATES (re-pack |peak-p_A'|<={LOC_TOL} all 3 seeds):")
    print(f"     per-seed = {[round(d,3) for d in rp_dists]}  -> c1 {'PASS' if c1 else 'FAIL'}")
    print(f"  c2 COHERENT (re-pack mean peak-count<={COH_MAX}; H_1340 4.3->7.0, H_1352 15.7):")
    print(f"     per-seed pc = {rp_pcs}, mean {rp_pc_m:.1f}  -> c2 {'PASS' if c2 else 'FAIL'}")
    print(f"  c3 EARNED (3a no-retrain holds p_A |peak-p_A|<={LOC_TOL}; 3b shuffle pc>={SHUF_MIN_PC}):")
    print(f"     3a no-retrain |peak-p_A| = {[round(d,3) for d in noR_dists]} -> "
          f"{'PASS' if c3a else 'FAIL'}")
    print(f"     3b shuffle peak-count = {sh_pcs}, mean {sh_pc_m:.1f} -> {'PASS' if c3b else 'FAIL'}")
    print(f"     -> c3 {'PASS' if c3 else 'FAIL'}")
    print(f"  c4 vs-PRIOR (4a pc<={COH_MAX} < H_1340 {H1340_MIN_PC}/H_1352 {H1352_PC}; "
          f"4b |peak-p_A'|<={H1340_BEST_DIST} best-H1340):")
    print(f"     4a re-pack peak-count mean {rp_pc_m:.1f} -> {'PASS' if c4a else 'FAIL'}")
    print(f"     4b re-pack |peak-p_A'| mean {rp_dist_m:.3f} -> {'PASS' if c4b else 'FAIL'}")
    print(f"     -> c4 {'PASS' if c4 else 'FAIL'}")
    print("")

    # ── anchor sanity (NOT a gate): NO-REPACK arm must reproduce the H_1340/H_1352 partial ──
    anchor_ok = (0.40 <= nr_frac_m <= 0.75) and nr_dist_m > LOC_TOL
    print(f"  [anchor sanity] NO-REPACK reproduces H_1340/H_1352 partial (frac {nr_frac_m:+.2f} in "
          f"[0.40,0.75] AND |peak-p_A'| {nr_dist_m:.3f}>{LOC_TOL}): {'OK' if anchor_ok else 'DRIFT'}")
    print("=" * 86)

    green = c1 and c2 and c3 and c4
    if green:
        print("VERDICT: GREEN (MIRROR, DIRECTIONAL) -- GEOMETRIC RE-PACK RECOVERS A COHERENT FULL")
        print(f"  RELOCATION. At FIXED LOW budget (DIM={DIM}/GROW2={GROW2}, eta={REPACK_ETA}),")
        print(f"  physically MOVING the residual phase-1 cells toward p_A'={P_A2:.3f} lands the CP")
        print(f"  peak AT p_A' (|peak-p_A'|={rp_dist_m:.3f}<={LOC_TOL}) AND restores coherence "
              f"(peak-count {rp_pc_m:.1f}<={COH_MAX}) --")
        print(f"  the gate H_1340 (budget, pc>=4.3) AND H_1352 (decay, pc=15.7) BOTH FAILED.")
        print("  Carving relocation is MOVE-THE-CELLS: the residual was a GEOMETRIC-PLACEMENT")
        print("  problem all along, NOT a weight (decay) or count (budget) problem. NO-RETRAIN")
        print("  held p_A, SHUFFLE collapsed (moving cells does not fabricate a peak from noise).")
        print("  a_break_the_wall: the H_1340/H_1352 walls were the WRONG MECHANISM, not a true")
        print("  ceiling. ENGINE-TRANSFER UNVERIFIED. TOY synthetic, 3 seeds, one frozen eta.")
        return 0
    # honest non-green branches (NO bar move, c9)
    if c1 and c3 and not c2:
        print("VERDICT: TERMINAL 🧱 -- THREE LEVERS EXHAUSTED. Geometric re-pack RELOCATES the")
        print(f"  peak but coherence is STILL NOT recovered (peak-count {rp_pc_m:.1f}>{COH_MAX}).")
        print("  Budget (count, H_1340), decay (weight, H_1352), AND geometry (re-pack, H_1360)")
        print("  ALL fail the coherence gate -> CP relocation is INTRINSICALLY partial-or-")
        print("  incoherent under this RBF geometry. THREE orthogonal levers exhausted. Honest,")
        print("  NO bar move (c9). ENGINE-TRANSFER UNVERIFIED.")
        return 3
    if not c1:
        print("VERDICT: INTRINSICALLY-PARTIAL -- even moving the cells leaves the peak short of")
        print(f"  p_A' (|peak-p_A'| mean {rp_dist_m:.3f}>{LOC_TOL}). The geometric drift is not")
        print("  even the distance lever; relocation may be intrinsically partial under this RBF")
        print("  geometry. Honest closed-negative, NO bar move (c9). ENGINE-TRANSFER UNVERIFIED.")
        return 2
    print("VERDICT: CONFOUNDED -- a frozen EARNED control failed (no-retrain drift or shuffle")
    print("  fabrication). Treat c1/c2 cautiously. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
