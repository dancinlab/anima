"""
H_1352 — WHORFIAN CP RELOCATION: SOFT-DECAY RE-PACK (coherence-preserving).
R2 follow-on of H_1340 (the budget-sweep DEEPER-LIMIT). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1352_cp_soft_decay/FREEZE.txt (pre-registered BEFORE this scoring).
$0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335] (SAME as H_1333/H_1338/H_1340 so the
NO-DECAY arm reproduces the H_1338/H_1340 anchor IN-RUN). p7. a_no_llm_frame_trap /
a_break_the_wall (developmental/critical-period plasticity + memory-protection-vs-overwrite
lens, c15) -- NOT an LLM recipe, NOT a human-cognition claim. ENGINE-TRANSFER UNVERIFIED
(directional mirror, same family as H_1333 R1 / H_1338 R1 / H_1340 R1 / H_1323 R1).

THE QUESTION: H_1340 found that raising the phase-2 split budget + RBF density buys
peak-DISTANCE toward p_A' MONOTONICALLY but DESTROYS coherence (peak-count 4.3->7.0, never
<=2) -- pure budget can NOT deliver a COHERENT full relocation. H_1340's verdict named the
next mechanism: "a clean full relocation needs a DIFFERENT mechanism (soft DECAY /
coherence-preserving re-pack), not more resolution." H_1352 tests EXACTLY that.

THE ONE NEW MECHANISM = a SOFT-DECAY store. Everything else is H_1333/H_1338/H_1340 verbatim
(this file IMPORTS that machinery). During phase-2 (A->A') re-training, residual phase-1 cells
are DOWN-WEIGHTED -- their vote weight d_i decays by DECAY_GAMMA per subsequent phase-2 split,
phase-2 cells stay at 1.0 -- instead of full-weight (never-evict, H_1333/H_1338), hard-removed
(eviction, H_1338, no help), or budget-drowned (H_1340, kills coherence). Budget is held at
the H_1340 R0_base LOW value (DIM=16/GROW2=24) -- NO inflation; the ONLY change is decay.

p1/p2/p3/p6: discrimination readout reads ONLY representational distance x structural decay
weight; NO injected boundary location at test; decay keys on a cell's BIRTH PHASE only (a
structural store property, NO injected target peak / persona / RLHF); labels enter ONLY during
training. The no-retrain + shuffle arms are the anti-Goodhart discriminators; the no-decay arm
(must STAY partial in-run) isolates decay as the lever.
"""
import importlib.util
import os
import sys

import numpy as np

# ── import the H_1333 / H_1338 / H_1340 CP machinery VERBATIM (do NOT re-implement) ──
_HERE = os.path.dirname(os.path.abspath(__file__))
_H1333 = os.path.abspath(os.path.join(_HERE, "..", "universe-probes", "h1333_whorf_developmental.py"))
_spec = importlib.util.spec_from_file_location("h1333_whorf_developmental", _H1333)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
# reuse: h.embed, h.VoronoiCells, h.discrim_curve, h.peak_loc, h.peak_count

# ── frozen constants (inherited VERBATIM from H_1333 / H_1338 / H_1340 FREEZE) ───────
P_A   = 1.0 / 3.0             # initial language A boundary (h.P_A)
P_A2  = 2.0 / 3.0            # RE-trained (moved) boundary p_A' (h.P_A2)
N_STIM = 81                  # = H_1340 (finer than H_1338's 21; constant = not a confound)
DIM    = 16                  # LOW = H_1340 R0_base RBF density (NOT inflated)
PHASE1_BUDGET = 24           # phase-1 split budget, FIXED (= H_1333/H_1338/H_1340)
GROW2  = 24                  # phase-2 budget LOW = H_1340 R0_base (NO budget inflation)
SEEDS  = [4333, 4334, 4335]  # SAME as H_1333/H_1338/H_1340 (no-decay arm reproduces anchor)

# frozen soft-decay schedule (PRE-REGISTERED; gate is scored ONLY at DECAY_GAMMA=0.80)
DECAY_GAMMA   = 0.80         # phase-1 cell vote weight x= this per subsequent phase-2 split
DECAY_LADDER  = [0.70, 0.80, 0.90]   # NON-GATING diagnostic (knife-edge check), gate=0.80 only

# frozen bar thresholds (from FREEZE)
LOC_TOL       = 0.12         # |peak - boundary| reach tolerance (= H_1333/H_1338/H_1340)
COH_MAX       = 2            # c2 / c4b: coherent CP arm has peak-count <= this
SHUF_MIN_PC   = 3            # c3b: shuffle control must be incoherent (peak-count >= this)
H1340_BEST_DIST = 0.081      # c4a: best (closest) H_1340 rung |peak-p_A'| (R4_high, from card)
H1340_MIN_PC    = 4.3        # c4b ref: lowest H_1340 rung peak-count (R0_base; all rungs >= this)


def make_basis_dim(seed, dim):
    """H_1333 make_basis VERBATIM except DIM is a parameter. Same width draw (seed+7000)."""
    rb = np.random.default_rng(seed + 7000)
    centers = np.linspace(0.0, 1.0, dim)
    width = float(rb.uniform(0.10, 0.13))
    return {"centers": centers, "width": width}


class SoftDecayCells(h.VoronoiCells):
    """H_1333 VoronoiCells + a per-cell decay weight d_i that multiplies into the softmin vote.
    The base fit() is reused VERBATIM (split-only never-evict growth). We add a decay-schedule
    hook: after a fit() call we know how many cells existed before; decay only fires on a
    phase-2 re-grow and only on cells born in phase-1.

    decay_birth[i] = number of phase-2 splits already present when cell i was born; for a
    phase-1 cell that is 0. We then assign d_i = DECAY_GAMMA ** (n_phase2_splits - decay_birth[i])
    for phase-1 cells, and 1.0 for phase-2 cells. Equivalently each phase-1 cell is multiplied
    by DECAY_GAMMA once per phase-2 split that occurred AFTER it.
    """

    def __init__(self, gamma=1.0):
        super().__init__()
        self.gamma = gamma
        self.n_phase1 = 0           # how many cells exist after phase-1 (set by caller)
        self.weights = None         # filled lazily for the posterior

    def freeze_phase1(self):
        """Mark the current cell count as the phase-1 boundary (cells [0:n_phase1) decay)."""
        self.n_phase1 = len(self.protos)

    def _decay_weights(self):
        """d_i: phase-1 cells decay by gamma per phase-2 split that happened after phase-1;
        all phase-2 cells stay 1.0. n_phase2_splits = total cells - n_phase1."""
        n = len(self.protos)
        n_p2 = max(0, n - self.n_phase1)
        w = np.ones(n, dtype=np.float64)
        if n_p2 > 0 and self.gamma < 1.0:
            # every phase-1 cell saw all n_p2 phase-2 splits born after it -> gamma**n_p2
            for i in range(self.n_phase1):
                w[i] = self.gamma ** n_p2
        return w

    def posterior(self, key):
        """Soft category-posterior with decay-weighted softmin vote (H_1333 posterior VERBATIM
        except each weight is x= d_i). beta=18.0 (H_1333). With gamma=1.0 this is EXACTLY the
        H_1333 posterior (so the NO-DECAY arm == H_1340 R0_base byte-for-byte)."""
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        beta = 18.0
        w = np.exp(-beta * (d - d.min()))
        dw = self._decay_weights()
        w = w * dw
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


def reloc(seed, gamma, kind="A2"):
    """Phase-1 carve p_A (FIXED budget), then phase-2 re-grow on labels(kind) with soft-decay
    gamma. kind='A2' = moved boundary; kind='shuffle' = incoherent control. Returns the
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

    # A-trained baseline peak (phase-1 only) -- the move-fraction reference (gamma irrelevant,
    # no phase-2 splits so all weights are 1.0).
    cA = SoftDecayCells(gamma=gamma).fit(X, Y_A, PHASE1_BUDGET, PHASE1_BUDGET, fresh=True)
    cA.freeze_phase1()
    midsA, normA, _ = h.discrim_curve(cA, X, positions)
    peakA = h.peak_loc(midsA, normA)

    # Relocation: phase-1 FIXED budget on p_A, freeze, then phase-2 LOW budget on labels(kind).
    cR = SoftDecayCells(gamma=gamma).fit(X, Y_A, PHASE1_BUDGET, PHASE1_BUDGET, fresh=True)
    cR.freeze_phase1()
    nc_p1 = len(cR.protos)
    cR.fit(X, Y_2, GROW2, GROW2, fresh=False)              # split-only never-evict + soft-decay
    midsR, normR, _ = h.discrim_curve(cR, X, positions)
    peakR = h.peak_loc(midsR, normR)
    pcR = h.peak_count(normR)
    return dict(peakA=peakA, peakR=peakR, pcR=pcR, nc_p1=nc_p1, nc_p2=len(cR.protos))


def noretrain(seed):
    """NO-RETRAIN control: grow on p_A only, no phase-2, no decay -> must hold p_A."""
    basis = make_basis_dim(seed, DIM)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([h.embed(x, basis) for x in positions])
    Y_A = (positions > P_A).astype(int)
    cN = SoftDecayCells(gamma=1.0).fit(X, Y_A, PHASE1_BUDGET, PHASE1_BUDGET, fresh=True)
    cN.freeze_phase1()
    midsN, normN, _ = h.discrim_curve(cN, X, positions)
    return h.peak_loc(midsN, normN)


def frac(peak_r, peak_a):
    return (peak_r - peak_a) / (P_A2 - P_A) if (P_A2 - P_A) != 0 else 0.0


def main():
    print("H_1352 R1 -- WHORFIAN CP RELOCATION: SOFT-DECAY RE-PACK (coherence-preserving)")
    print("=" * 86)
    print("R2 of H_1340: at FIXED LOW budget (DIM=16/GROW2=24), does soft-decaying the residual")
    print("              phase-1 cells recover a COHERENT full relocation (peak AT p_A', pc~1)?")
    print(f"N_stim={N_STIM} DIM={DIM} p_A={P_A:.3f} p_A'={P_A2:.3f} phase1={PHASE1_BUDGET} "
          f"phase2={GROW2} gamma={DECAY_GAMMA} seeds={SEEDS}  (split-only never-evict + decay)")
    print("")

    # ── per-seed arms at the FROZEN gamma=0.80 ──────────────────────────────────────
    nd_peaks, nd_dists, nd_fracs, nd_pcs = [], [], [], []   # NO-DECAY (gamma=1.0)
    sd_peaks, sd_dists, sd_fracs, sd_pcs = [], [], [], []   # SOFT-DECAY (gamma=0.80)
    nr_dists = []                                            # NO-RETRAIN
    sh_pcs = []                                              # SHUFFLE + decay
    print("  per-seed (NO-DECAY gamma=1.0 / SOFT-DECAY gamma=0.80 / NO-RETRAIN / SHUFFLE+decay):")
    for seed in SEEDS:
        nd = reloc(seed, gamma=1.0, kind="A2")              # == H_1340 R0_base anchor
        sd = reloc(seed, gamma=DECAY_GAMMA, kind="A2")
        nrp = noretrain(seed)
        sh = reloc(seed, gamma=DECAY_GAMMA, kind="shuffle")

        nd_peaks.append(nd["peakR"]); nd_dists.append(abs(nd["peakR"] - P_A2))
        nd_fracs.append(frac(nd["peakR"], nd["peakA"])); nd_pcs.append(nd["pcR"])
        sd_peaks.append(sd["peakR"]); sd_dists.append(abs(sd["peakR"] - P_A2))
        sd_fracs.append(frac(sd["peakR"], sd["peakA"])); sd_pcs.append(sd["pcR"])
        nr_dists.append(abs(nrp - P_A))
        sh_pcs.append(sh["pcR"])
        print(f"    seed {seed}: NO-DECAY peak={nd['peakR']:.3f} pc={nd['pcR']} | "
              f"SOFT-DECAY peak={sd['peakR']:.3f} pc={sd['pcR']} | "
              f"no-retrain peak={nrp:.3f} | shuffle pc={sh['pcR']}  "
              f"cells(p1,p2)={sd['nc_p1']},{sd['nc_p2']}")
    print("")

    nd_peak_m = float(np.mean(nd_peaks)); nd_dist_m = float(np.mean(nd_dists))
    nd_frac_m = float(np.mean(nd_fracs)); nd_pc_m = float(np.mean(nd_pcs))
    sd_peak_m = float(np.mean(sd_peaks)); sd_dist_m = float(np.mean(sd_dists))
    sd_frac_m = float(np.mean(sd_fracs)); sd_pc_m = float(np.mean(sd_pcs))
    nr_dist_m = float(np.mean(nr_dists)); sh_pc_m = float(np.mean(sh_pcs))
    print(f"  NO-DECAY   (anchor): peak {nd_peak_m:.3f} |peak-p_A'| {nd_dist_m:.3f} "
          f"frac {nd_frac_m:+.2f} peak-count {nd_pc_m:.1f}")
    print(f"  SOFT-DECAY (g=0.80): peak {sd_peak_m:.3f} |peak-p_A'| {sd_dist_m:.3f} "
          f"frac {sd_frac_m:+.2f} peak-count {sd_pc_m:.1f}")
    print(f"  NO-RETRAIN: mean |peak-p_A| {nr_dist_m:.3f}  |  SHUFFLE+decay: peak-count {sh_pc_m:.1f}")
    print("")

    # ── NON-GATING diagnostic: decay-ladder (knife-edge check; gate scored ONLY at 0.80) ──
    print("  [NON-GATING diagnostic] DECAY-LADDER (gate is scored ONLY at gamma=0.80):")
    for g in DECAY_LADDER:
        ds, ps = [], []
        for seed in SEEDS:
            r = reloc(seed, gamma=g, kind="A2")
            ds.append(abs(r["peakR"] - P_A2)); ps.append(r["pcR"])
        tag = "  <-- FROZEN GATE" if abs(g - DECAY_GAMMA) < 1e-9 else ""
        print(f"     gamma={g:.2f}: |peak-p_A'| mean={np.mean(ds):.3f}  "
              f"peak-count mean={np.mean(ps):.1f}{tag}")
    print("")

    # ── BARS ────────────────────────────────────────────────────────────────────────
    c1 = all(d <= LOC_TOL for d in sd_dists)                            # RELOCATES (all seeds)
    c2 = sd_pc_m <= COH_MAX                                             # COHERENT
    c3a = all(d <= LOC_TOL for d in nr_dists)                           # no-retrain holds p_A
    c3b = sh_pc_m >= SHUF_MIN_PC                                        # shuffle collapses
    c3 = c3a and c3b
    c4a = sd_dist_m <= H1340_BEST_DIST                                  # >= best H_1340 closeness
    c4b = sd_pc_m <= COH_MAX                                            # coherent where 1340 wasn't
    c4 = c4a and c4b

    print(f"  c1 RELOCATES (soft-decay |peak-p_A'|<={LOC_TOL} all 3 seeds):")
    print(f"     per-seed = {[round(d,3) for d in sd_dists]}  -> c1 {'PASS' if c1 else 'FAIL'}")
    print(f"  c2 COHERENT (soft-decay mean peak-count<={COH_MAX}; H_1340 was 4.3->7.0):")
    print(f"     per-seed pc = {sd_pcs}, mean {sd_pc_m:.1f}  -> c2 {'PASS' if c2 else 'FAIL'}")
    print(f"  c3 EARNED (3a no-retrain holds p_A |peak-p_A|<={LOC_TOL}; 3b shuffle pc>={SHUF_MIN_PC}):")
    print(f"     3a no-retrain |peak-p_A| = {[round(d,3) for d in nr_dists]} -> "
          f"{'PASS' if c3a else 'FAIL'}")
    print(f"     3b shuffle peak-count = {sh_pcs}, mean {sh_pc_m:.1f} -> {'PASS' if c3b else 'FAIL'}")
    print(f"     -> c3 {'PASS' if c3 else 'FAIL'}")
    print(f"  c4 vs-BUDGET (4a |peak-p_A'|<={H1340_BEST_DIST} best-H1340; 4b pc<={COH_MAX} < "
          f"H_1340 min {H1340_MIN_PC}):")
    print(f"     4a soft-decay |peak-p_A'| mean {sd_dist_m:.3f} -> {'PASS' if c4a else 'FAIL'}")
    print(f"     4b soft-decay peak-count mean {sd_pc_m:.1f} -> {'PASS' if c4b else 'FAIL'}")
    print(f"     -> c4 {'PASS' if c4 else 'FAIL'}")
    print("")

    # ── anchor sanity (NOT a gate): NO-DECAY arm must reproduce the H_1340/H_1338 partial ──
    anchor_ok = (0.40 <= nd_frac_m <= 0.75) and nd_dist_m > LOC_TOL
    print(f"  [anchor sanity] NO-DECAY reproduces H_1340/H_1338 partial (frac {nd_frac_m:+.2f} in "
          f"[0.40,0.75] AND |peak-p_A'| {nd_dist_m:.3f}>{LOC_TOL}): {'OK' if anchor_ok else 'DRIFT'}")
    print("=" * 86)

    green = c1 and c2 and c3 and c4
    if green:
        print("VERDICT: GREEN (MIRROR, DIRECTIONAL) -- SOFT-DECAY RECOVERS A COHERENT FULL")
        print(f"  RELOCATION. At FIXED LOW budget (DIM={DIM}/GROW2={GROW2}, gamma={DECAY_GAMMA}),")
        print(f"  down-weighting residual phase-1 cells lands the CP peak AT p_A'={P_A2:.3f}")
        print(f"  (|peak-p_A'|={sd_dist_m:.3f}<={LOC_TOL}) AND restores coherence "
              f"(peak-count {sd_pc_m:.1f}<={COH_MAX}) --")
        print(f"  the gate H_1340 NEVER met (its peak-count was 4.3->7.0). Soft-decay BEATS")
        print("  high-budget on BOTH axes at a fraction of the budget: the relocation residual")
        print("  was a COHERENCE/re-pack problem, NOT a resolution one. NO-RETRAIN held p_A,")
        print("  SHUFFLE collapsed (decay does not fabricate a peak). a_break_the_wall: the")
        print("  H_1340 wall was the WRONG MECHANISM (budget), not a true ceiling. ENGINE-")
        print("  TRANSFER UNVERIFIED. TOY synthetic, 3 seeds, single shift, one frozen gamma.")
        return 0
    # honest non-green branches (NO bar move, c9)
    if c1 and c3 and not c2:
        print("VERDICT: DEEPER LIMIT -- soft-decay RELOCATES the peak but coherence is NOT")
        print(f"  recovered (peak-count {sd_pc_m:.1f}>{COH_MAX}). Relocation COHERENCE is a")
        print("  deeper limit than budget OR decay. Honest, NO bar move (c9).")
        return 3
    if not c1:
        print("VERDICT: INTRINSICALLY-PARTIAL -- even soft-decay leaves the peak short of p_A'")
        print(f"  (|peak-p_A'| mean {sd_dist_m:.3f}>{LOC_TOL}). Under this RBF geometry the")
        print("  relocation may be intrinsically partial; soft-decay is not the lever. Honest")
        print("  closed-negative, NO bar move (c9). ENGINE-TRANSFER UNVERIFIED.")
        return 2
    print("VERDICT: CONFOUNDED -- a frozen EARNED control failed (no-retrain drift or shuffle")
    print("  fabrication). Treat c1/c2 cautiously. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
