"""
H_1340 — WHORFIAN CP RELOCATION CEILING: BUDGET / RBF-DENSITY SWEEP AT THE MOVED CUT.
R2 of H_1338 (the re-diagnosis follow-on). R1 numpy MIRROR (DIRECTIONAL).

Frozen design: .verdicts/1340_whorf_cp_budget_sweep/FREEZE.txt (pre-registered BEFORE this
scoring). $0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335] (SAME as H_1333/H_1338 so the
baseline rung reproduces the H_1338 anchor IN-RUN). p7. a_no_llm_frame_trap / a_break_the_wall
(developmental/critical-period plasticity + representational-RESOLUTION lens, c15) — NOT an
LLM recipe, NOT a human-cognition claim. ENGINE-TRANSFER UNVERIFIED (directional mirror, same
family as H_1333 R1 / H_1338 R1 / H_1323 R1).

THE QUESTION: H_1338 found that EVICTING stale phase-1 cells did NOT complete the H_1333
partial relocation (peak stayed 0.525, frac +0.60 even with cells 28→3) and DIAGNOSED the
residual as BUDGET / GEOMETRY (RBF resolution + a fixed per-phase split budget). DECISIVE
test of THAT diagnosis: SWEEP the phase-2 split budget AND the RBF grid density at the moved
boundary p_A'. If raising budget/density lets the relocated CP peak REACH p_A' (crossing
|peak−p_A'| ≤ LOC_TOL), the residual IS budget/geometry and the resolution ceiling is mapped.

THE SWEEP (everything else is H_1333/H_1338 verbatim — this file IMPORTS that machinery):
a LADDER of joint (DIM, GROW2) rungs applied ONLY to phase-2. Phase-1 is FIXED at the
H_1333/H_1338 baseline budget (GROW=24) on EVERY rung — so the never-evicted phase-1 packing
(the residual H_1338 identified) is IDENTICAL across rungs; the ONLY thing that changes is
how much budget/density the RE-TRAINING gets. N_STIM is FIXED at 81 (finer than H_1338's 21
so peak-location is not quantization-bound; constant across rungs = not a confound). NO
eviction (split-only never-evict store), since H_1338 already showed eviction is not the lever.

p1/p2/p3/p6: discrimination readout reads ONLY representational distance; NO injected boundary
location at test; labels enter ONLY during training. Budget/density are STRUCTURAL store knobs;
NO injected target peak. The baseline (R0) + monotonicity (B2) bars are the anti-Goodhart legs.
"""
import importlib.util
import os
import sys

import numpy as np

# ── import the H_1333 / H_1338 CP machinery VERBATIM (do NOT re-implement) ───────
_H1333 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h1333_whorf_developmental.py")
_spec = importlib.util.spec_from_file_location("h1333_whorf_developmental", _H1333)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
# reuse: h.embed, h.VoronoiCells, h.discrim_curve, h.peak_loc, h.peak_count

# ── frozen constants (inherited VERBATIM from H_1333 / H_1338 FREEZE) ────────────
P_A   = 1.0 / 3.0              # initial language A boundary (h.P_A)
P_A2  = 2.0 / 3.0             # RE-trained (moved) boundary p_A' (h.P_A2)
N_STIM = 81                   # stimulus count, FIXED across rungs (finer than H_1338's 21)
PHASE1_BUDGET = 24            # phase-1 split budget, FIXED on every rung (= H_1333/H_1338)
SEEDS = [4333, 4334, 4335]    # SAME as H_1333/H_1338 (R0 reproduces the H_1338 anchor in-run)

# frozen bar thresholds
LOC_TOL      = 0.12           # peak "reaches" p_A' iff |peak−p_A'| ≤ this (= H_1333/H_1338)
COH_MAX_LANG = 2              # a coherent CP arm: mean peak-count ≤ 2
TRACK_TOL    = 0.10           # B2: total frac span across the ladder ≥ this (a real climb)
B3_FRAC_LO   = 0.40           # B3: R0 reproduces H_1338 partial — frac in [LO, HI]
B3_FRAC_HI   = 0.75
MONO_SLACK   = 0.01           # B2: each rung ≥ previous − this (numeric slack)

# RUNG LADDER: (label, DIM=RBF density, GROW2=phase-2 split budget AND passes)
RUNGS = [
    ("R0_base", 16, 24),     # = H_1338 baseline budget/density — must reproduce ~0.525
    ("R1",      32, 96),
    ("R2",      48, 192),
    ("R3",      64, 384),
    ("R4_high", 96, 768),    # highest-resolution rung
]


def make_basis_dim(seed, dim):
    """H_1333 make_basis VERBATIM except DIM is a sweep parameter (RBF grid density).
    Same width draw rng (seed+7000) so a rung's basis is deterministic and seed-locked."""
    rb = np.random.default_rng(seed + 7000)
    centers = np.linspace(0.0, 1.0, dim)
    width = float(rb.uniform(0.10, 0.13))
    return {"centers": centers, "width": width}


def reloc_peak(dim, grow2, seed):
    """Phase-1 carve p_A at FIXED PHASE1_BUDGET, then phase-2 RE-grow on p_A' with the swept
    (dim, grow2) — split-only never-evict store (H_1333 verbatim, NO eviction). Returns the
    relocated CP peak, A-trained peak (same basis), peak-count, and cell budgets."""
    basis = make_basis_dim(seed, dim)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([h.embed(x, basis) for x in positions])
    Y_A = (positions > P_A).astype(int)
    Y_A2 = (positions > P_A2).astype(int)

    # A-trained baseline peak (phase-1 only, FIXED budget) — the move-fraction reference.
    cA = h.VoronoiCells().fit(X, Y_A, PHASE1_BUDGET, PHASE1_BUDGET, fresh=True)
    midsA, normA, _ = h.discrim_curve(cA, X, positions)
    peakA = h.peak_loc(midsA, normA)

    # Relocation: phase-1 FIXED budget on p_A, then phase-2 swept (dim already in basis) on p_A'.
    cR = h.VoronoiCells().fit(X, Y_A, PHASE1_BUDGET, PHASE1_BUDGET, fresh=True)
    nc_p1 = len(cR.protos)
    cR.fit(X, Y_A2, grow2, grow2, fresh=False)            # split-only, NO evict (never-evict)
    midsR, normR, _ = h.discrim_curve(cR, X, positions)
    peakR = h.peak_loc(midsR, normR)
    pcR = h.peak_count(normR)
    return dict(peakA=peakA, peakR=peakR, pcR=pcR, nc_p1=nc_p1, nc_p2=len(cR.protos))


def frac(peak_r, peak_a):
    return (peak_r - peak_a) / (P_A2 - P_A) if (P_A2 - P_A) != 0 else 0.0


def main():
    print("H_1340 R1 — WHORFIAN CP RELOCATION CEILING: BUDGET / RBF-DENSITY SWEEP")
    print("=" * 84)
    print("R2 of H_1338: does raising phase-2 split budget + RBF density let the RE-LOCATED CP")
    print("              peak REACH p_A'? (tests the H_1338 budget/geometry re-diagnosis)")
    print(f"N_stim={N_STIM} p_A={P_A:.3f} p_A'={P_A2:.3f} phase1_budget={PHASE1_BUDGET} "
          f"seeds={SEEDS}  (NO eviction — split-only never-evict store)")
    print("")

    # per-rung accumulation
    rung_peak = {}     # label -> mean relocated peak
    rung_frac = {}     # label -> mean move-fraction
    rung_pc = {}       # label -> mean peak-count
    rung_per = {}      # label -> {peaks:[], dists:[], fracs:[]}
    print("  per-rung relocated CP peak (phase-1 FIXED budget=24, phase-2 swept):")
    for label, dim, grow2 in RUNGS:
        peaks, dists, fracs, pcs, ncs = [], [], [], [], []
        for seed in SEEDS:
            r = reloc_peak(dim, grow2, seed)
            peaks.append(r["peakR"])
            dists.append(abs(r["peakR"] - P_A2))
            fracs.append(frac(r["peakR"], r["peakA"]))
            pcs.append(r["pcR"])
            ncs.append((seed, r["nc_p1"], r["nc_p2"]))
        rung_peak[label] = float(np.mean(peaks))
        rung_frac[label] = float(np.mean(fracs))
        rung_pc[label] = float(np.mean(pcs))
        rung_per[label] = dict(peaks=peaks, dists=dists, fracs=fracs)
        print(f"    {label:8s} DIM={dim:3d} GROW2={grow2:4d}: "
              f"peak mean={np.mean(peaks):.3f}  |peak-p_A'| mean={np.mean(dists):.3f}  "
              f"frac={np.mean(fracs):+.2f}  peak-count={np.mean(pcs):.1f}")
        print(f"             per-seed |peak-p_A'| = {[round(d, 3) for d in dists]}  "
              f"all≤{LOC_TOL}: {all(d <= LOC_TOL for d in dists)}   "
              f"cells(seed,p1,p2)={ncs}")
    print("")

    labels = [r[0] for r in RUNGS]

    # ── B1 RELOCATES: lowest rung where all 3 seeds reach p_A' (coherent) = mapped ceiling ──
    ceiling = None
    for label in labels:
        reaches = all(d <= LOC_TOL for d in rung_per[label]["dists"])
        coherent = rung_pc[label] <= COH_MAX_LANG
        if reaches and coherent:
            ceiling = label
            break
    b1 = ceiling is not None
    print(f"  B1 RELOCATES (some rung: all 3 seeds |peak-p_A'|≤{LOC_TOL} AND coherent "
          f"peak-count≤{COH_MAX_LANG}):")
    if b1:
        print(f"     MAPPED CEILING = {ceiling} (DIM/GROW2 of that rung) — peak reaches p_A' "
              f"there; per-seed |peak-p_A'|={[round(d,3) for d in rung_per[ceiling]['dists']]}, "
              f"peak-count={rung_pc[ceiling]:.1f}")
    else:
        hi = labels[-1]
        print(f"     NO rung reaches p_A' — highest rung {hi}: "
              f"|peak-p_A'|={[round(d,3) for d in rung_per[hi]['dists']]}, "
              f"frac={rung_frac[hi]:+.2f} (peak stuck short of p_A')")
    print(f"     -> B1 {'PASS' if b1 else 'FAIL'}")

    # ── B2 EARNED-MONOTONE: frac non-decreasing across ladder AND total span ≥ TRACK_TOL ───
    fr_seq = [rung_frac[l] for l in labels]
    mono = all(fr_seq[i] >= fr_seq[i - 1] - MONO_SLACK for i in range(1, len(fr_seq)))
    span = fr_seq[-1] - fr_seq[0]
    b2 = mono and span >= TRACK_TOL
    print(f"  B2 EARNED-MONOTONE (frac non-decreasing R0→R4 within slack {MONO_SLACK}; "
          f"span≥{TRACK_TOL}):")
    print(f"     frac ladder = {[round(f, 3) for f in fr_seq]}  -> monotone "
          f"{'PASS' if mono else 'FAIL'}")
    print(f"     span (R4−R0) = {span:+.3f}  -> climb {'PASS' if span >= TRACK_TOL else 'FAIL'}")
    print(f"     -> B2 {'PASS' if b2 else 'FAIL'}")

    # ── B3 BASELINE-REPRO: R0 reproduces the H_1338 partial (in-run anchor) ────────────────
    r0 = rung_per["R0_base"]
    b3_frac = all(B3_FRAC_LO <= f <= B3_FRAC_HI for f in r0["fracs"])
    b3_partial = all(d > LOC_TOL for d in r0["dists"])      # still partial (did NOT complete)
    b3 = b3_frac and b3_partial
    print(f"  B3 BASELINE-REPRO (R0 frac in [{B3_FRAC_LO},{B3_FRAC_HI}] AND |peak-p_A'|>{LOC_TOL} "
          f"all 3 seeds — reproduces H_1338 partial):")
    print(f"     R0 per-seed frac = {[round(f, 3) for f in r0['fracs']]}  -> partial-frac "
          f"{'PASS' if b3_frac else 'FAIL'}")
    print(f"     R0 per-seed |peak-p_A'| = {[round(d, 3) for d in r0['dists']]}  -> not-complete "
          f"{'PASS' if b3_partial else 'FAIL'}")
    print(f"     -> B3 {'PASS' if b3 else 'FAIL'}")

    print("=" * 84)
    green = b1 and b2 and b3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — the H_1338 RESIDUAL PULL *IS* a")
        print("  BUDGET / GEOMETRY (resolution) limit. Raising the phase-2 split budget + RBF")
        print(f"  grid density RELOCATES the CP peak the rest of the way to p_A'={P_A2:.3f}:")
        print(f"  the peak crosses into |peak-p_A'|≤{LOC_TOL} at the mapped ceiling rung "
              f"({ceiling}),")
        print(f"  monotonically with budget (frac {fr_seq[0]:+.2f}→{fr_seq[-1]:+.2f}, "
              f"span {span:+.3f}), while R0 reproduces the H_1338 partial in-run.")
        print("  The resolution ceiling is MAPPED (a_break_the_wall: the wall was insufficient")
        print("  resolution/investment, not a deep memory limit). NO eviction was used — the")
        print("  lever is budget/density, confirming H_1338's re-diagnosis. ENGINE-TRANSFER")
        print("  UNVERIFIED. TOY synthetic continuum, 3 seeds; NO human-cognition claim.")
        return 0
    # honest non-green branches (NO bar move, c9)
    if b2 and b3 and not b1:
        hi = labels[-1]
        print("VERDICT: 🧱 DEEPER LIMIT — raising budget + RBF density does NOT finish the move.")
        print(f"  Even the highest rung ({hi}) leaves the relocated peak short of p_A' "
              f"(|peak-p_A'|={rung_per[hi]['dists']}, frac {rung_frac[hi]:+.2f}). The H_1338")
        print("  budget/geometry diagnosis is itself INCOMPLETE — the residual is a deeper")
        print("  limit. Honest re-re-diagnosis, NO bar move (c9). ENGINE-TRANSFER UNVERIFIED.")
        return 3
    if not b3:
        print("VERDICT: 🧱 CONFOUNDED — R0 did NOT reproduce the H_1338 partial in-run; the")
        print("  ladder floor differs from H_1338, so the climb comparison is confounded.")
        print("  Honest, NO bar move (c9). Treat B1 cautiously.")
        return 2
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen EARNED bar failed (B2 monotonicity/span).")
    print("  The climb is not budget-driven / is a fluke. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
