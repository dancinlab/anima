"""
H_1341 — WHORFIAN CP PLASTICITY: SHIFT-SIZE LADDER (fraction-vs-shift curve)
R1 numpy MIRROR (DIRECTIONAL). The H_1333 load-bearing follow-on (a_scale_honest_scope ladder).

Frozen design: .verdicts/1341_whorf_cp_shift_ladder/FREEZE.txt (pre-registered BEFORE this
scoring). $0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335], p7. a_no_llm_frame_trap
(developmental / critical-period plasticity lens, c15) — NOT an LLM recipe, NOT a
human-cognition claim. ENGINE-TRANSFER UNVERIFIED (directional mirror).

THE QUESTION: H_1333 — a re-trained CP boundary relocates ~60% for a SINGLE shift
(p_A=1/3 -> p_A'=2/3). H_1338 re-diagnosed that residual as BUDGET/GEOMETRY (not never-evict).
H_1341 maps the move-fraction vs SHIFT-SIZE curve across >=3 shift magnitudes:
  - fraction TRACKS shift (range >= TRACK_TOL, smaller shift => larger fraction)  => GEOMETRY/BUDGET
  - fraction ~ CONSTANT  (range <  CONST_TOL)                                     => MEMORY
This is a CHARACTERIZATION ladder. ALL outcomes VALID (c9) — report the curve verbatim,
no GREEN/RED to manufacture.

Reuses the H_1333 CP machinery EXACTLY (UNIVERSE/h1333_whorf_developmental.py): the
VoronoiCells store (error-targeted SPLIT-only growth, phase-2 re-grow on the SAME store,
NO reset), RBF embed, soft-posterior discrimination readout, peak-count coherence. The ONLY
new code = sweeping the phase-2 target boundary p_A' across 3 shift rungs and assembling the
fraction-vs-shift curve.
"""
import numpy as np

from h1333_whorf_developmental import (
    N_STIM, DIM, P_A, GROW_MAX, SPLIT_PASSES, LOC_TOL,
    COH_MAX_LANG, COH_MIN_SHUF, SEEDS,
    embed, make_basis, VoronoiCells, discrim_curve, peak_loc, peak_count,
)

# ── frozen rungs / thresholds (from FREEZE) ─────────────────────────────────
# 3 shift rungs, all RIGHTWARD from the fixed anchor p_A=1/3, on the grid (spacing 0.05).
RUNGS = [
    ("SMALL", 0.467),   # SHIFT 0.133
    ("MID",   0.600),   # SHIFT 0.267
    ("LARGE", 0.667),   # SHIFT 0.333  -- the H_1333/H_1338 anchor rung
]
TRACK_TOL = 0.15        # frac range >= this AND monotone-dec in shift => GEOMETRY/BUDGET
CONST_TOL = 0.10        # frac range <  this => MEMORY (shift-independent)


def labels_cut(positions, cut):
    """category labels: cat 0 below the cut, cat 1 above (H_1333 build_labels verbatim form)."""
    return (positions > cut).astype(int)


def run_rung(seed, p_a2):
    """All 4 arms for ONE seed at ONE shift rung. Same stimulus world (basis fixed by seed),
    same fixed anchor p_A; only the phase-2 target p_a2 varies across rungs."""
    rng = np.random.default_rng(seed)
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([embed(x, basis) for x in positions])

    Y_A  = labels_cut(positions, P_A)
    Y_A2 = labels_cut(positions, p_a2)
    sh_rng = np.random.default_rng(seed + 4)
    Y_sh = rng_shuffle(positions, sh_rng)

    out = {}

    # (1) A-trained anchor (identical every rung; reproduces H_1323).
    cA = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cA, X, positions)
    out["A"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cA.protos))

    # (2) A->A' re-trained: phase-1 on p_A, phase-2 grow FURTHER on p_a2 (same store, no reset).
    cR = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    nc_p1 = len(cR.protos)
    cR.fit(X, Y_A2, GROW_MAX, SPLIT_PASSES, fresh=False)
    mids, norm, _ = discrim_curve(cR, X, positions)
    out["A2"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cR.protos),
                     ncells_p1=nc_p1)

    # (3) NO-RETRAIN control: grow on p_A only, read at the same protocol point, NO phase-2.
    cN = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cN, X, positions)
    out["noretrain"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cN.protos))

    # (4) SHUFFLE: incoherent labels -> EARNED control.
    cS = VoronoiCells().fit(X, Y_sh, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cS, X, positions)
    out["shuffle"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cS.protos))

    return out


def rng_shuffle(positions, rng):
    return rng.integers(0, 2, size=len(positions))


def main():
    print("H_1341 R1 — WHORFIAN CP PLASTICITY: SHIFT-SIZE LADDER (fraction-vs-shift curve)")
    print("=" * 84)
    print("paradigm: FIXED anchor p_A=1/3; RE-train SAME store on a MOVED cut p_A' at 3 shift")
    print("          magnitudes; map move-fraction vs shift. TRACKS shift=>geometry/budget;")
    print("          CONSTANT=>memory. CHARACTERIZATION ladder — ALL outcomes valid (c9).")
    print(f"N_stim={N_STIM} dim={DIM} p_A={P_A:.3f} grow_max={GROW_MAX}/phase seeds={SEEDS}")
    print(f"rungs (p_A'): " + "  ".join(f"{n}={p:.3f}(shift {p-P_A:.3f})" for n, p in RUNGS))
    print("")

    # per-rung aggregates
    curve = []   # (name, shift, mean_frac, fracs_per_seed, peaks_per_seed, ...)
    l2_ok_all = True

    for name, p_a2 in RUNGS:
        shift = p_a2 - P_A
        fracs, peaksR, peaksA, peaksN, pcA, pcR, pcN, pcS, ncp1, ncp2 = (
            [], [], [], [], [], [], [], [], [], [])
        print(f"  rung {name}  p_A'={p_a2:.3f}  shift={shift:.3f}:")
        for seed in SEEDS:
            o = run_rung(seed, p_a2)
            pA, pR, pN = o["A"]["peak"], o["A2"]["peak"], o["noretrain"]["peak"]
            frac = (pR - pA) / (p_a2 - P_A) if (p_a2 - P_A) != 0 else 0.0
            fracs.append(frac); peaksR.append(pR); peaksA.append(pA); peaksN.append(pN)
            pcA.append(o["A"]["pc"]); pcR.append(o["A2"]["pc"]); pcN.append(o["noretrain"]["pc"])
            pcS.append(o["shuffle"]["pc"]); ncp1.append(o["A2"]["ncells_p1"]); ncp2.append(o["A2"]["ncells"])
            print(f"    seed {seed}: A={pA:.3f} A->A'={pR:.3f} noR={pN:.3f}  frac={frac:+.3f}"
                  f"  | pc A={o['A']['pc']} A->A'={o['A2']['pc']} noR={o['noretrain']['pc']} "
                  f"shuf={o['shuffle']['pc']}  ncells p1->p2={o['A2']['ncells_p1']}->{o['A2']['ncells']}")
        mean_frac = float(np.mean(fracs))
        mean_pR   = float(np.mean(peaksR))
        # L2 EARNED at this rung
        l2a = all(abs(p - P_A) <= LOC_TOL for p in peaksN)               # no-retrain flat
        l2b_shuf = all(p >= COH_MIN_SHUF for p in pcS)                   # shuffle incoherent
        l2b_lang = all(p <= COH_MAX_LANG for p in pcA + pcR + pcN)       # lang arms coherent
        l2 = l2a and l2b_shuf and l2b_lang
        l2_ok_all = l2_ok_all and l2
        curve.append(dict(name=name, p_a2=p_a2, shift=shift, mean_frac=mean_frac,
                          fracs=fracs, mean_peakR=mean_pR, mean_peakA=float(np.mean(peaksA)),
                          l2a=l2a, l2b_shuf=l2b_shuf, l2b_lang=l2b_lang, l2=l2,
                          mean_pcS=float(np.mean(pcS))))
        print(f"    -> mean frac={mean_frac:+.3f}  mean peak A->A'={mean_pR:.3f}  "
              f"L2 noR-flat={'PASS' if l2a else 'FAIL'} shuf-incoh={'PASS' if l2b_shuf else 'FAIL'} "
              f"lang-coh={'PASS' if l2b_lang else 'FAIL'} -> L2 {'PASS' if l2 else 'FAIL'}")
        print("")

    # ── L1 CURVE ────────────────────────────────────────────────────────────
    print("=" * 84)
    print("  L1 — FRACTION-vs-SHIFT CURVE (mean of 3 seeds):")
    print(f"    {'rung':<7} {'shift':>7} {'p_A->p_A''':>12} {'mean peak A->A''':>16} {'mean frac':>10}")
    for c in curve:
        print(f"    {c['name']:<7} {c['shift']:>7.3f} {P_A:>5.3f}->{c['p_a2']:.3f}   "
              f"{c['mean_peakA']:>6.3f}->{c['mean_peakR']:.3f}      {c['mean_frac']:>+9.3f}")
    fracs_by_rung = [c["mean_frac"] for c in curve]      # SMALL, MID, LARGE order
    shifts = [c["shift"] for c in curve]
    frac_range = max(fracs_by_rung) - min(fracs_by_rung)
    # monotone in shift? (compare ordered by increasing shift)
    order = np.argsort(shifts)
    fr_ord = [fracs_by_rung[i] for i in order]
    mono_dec = all(fr_ord[i] >= fr_ord[i + 1] - 1e-9 for i in range(len(fr_ord) - 1))
    mono_inc = all(fr_ord[i] <= fr_ord[i + 1] + 1e-9 for i in range(len(fr_ord) - 1))
    trend = ("DECREASING-in-shift" if (mono_dec and not mono_inc) else
             "INCREASING-in-shift" if (mono_inc and not mono_dec) else
             "FLAT" if (mono_dec and mono_inc) else "NON-MONOTONE")
    print(f"    -> frac range (max-min) = {frac_range:.3f} ; trend vs shift = {trend}")
    print(f"    -> L1 CURVE MEASURED at 3 rungs, 3 seeds: PASS")
    print("")

    # ── L2 EARNED (summary across rungs) ─────────────────────────────────────
    print(f"  L2 — EARNED controls held at ALL rungs: {'PASS' if l2_ok_all else 'FAIL'}")
    for c in curve:
        print(f"     {c['name']:<7}: no-retrain-flat={'PASS' if c['l2a'] else 'FAIL'}  "
              f"shuffle-incoherent(pc={c['mean_pcS']:.1f})={'PASS' if c['l2b_shuf'] else 'FAIL'}  "
              f"lang-coherent={'PASS' if c['l2b_lang'] else 'FAIL'}")
    print("")

    # ── L3 INTERPRETATION (frozen rule) ──────────────────────────────────────
    print("  L3 — INTERPRETATION (geometry-vs-memory, frozen rule on frac range/trend):")
    print(f"     TRACK_TOL={TRACK_TOL}  CONST_TOL={CONST_TOL}  measured frac range={frac_range:.3f}  trend={trend}")
    # Also report the absolute-landing signature directly: if geometry/budget, the ABSOLUTE
    # post-retrain peak should be near-CONSTANT across rungs (lands at a fixed spot regardless
    # of how far it was asked to move). If memory, the absolute peak moves proportionally.
    peaks_abs = [c["mean_peakR"] for c in curve]
    peak_abs_range = max(peaks_abs) - min(peaks_abs)
    print(f"     diagnostic: ABSOLUTE post-retrain peak across rungs = "
          f"{[round(p,3) for p in peaks_abs]}  range={peak_abs_range:.3f}")

    if frac_range >= TRACK_TOL and (mono_dec and not mono_inc):
        verdict = ("GEOMETRY/BUDGET-LIMITED — the move-fraction TRACKS shift magnitude "
                   "(smaller shift => larger fraction, monotone-decreasing): the boundary "
                   "lands at a near-fixed ABSOLUTE position set by RBF resolution + fixed "
                   "split budget, so a bigger requested move leaves a bigger residual gap. "
                   "GENERALIZES the H_1338 budget/geometry finding across shift magnitude "
                   "(H_1338 found it at the LARGE rung only).")
        tag = "GEOMETRY/BUDGET"
    elif frac_range < CONST_TOL:
        verdict = ("MEMORY-LIMITED — the move-fraction is CONSTANT across shift sizes "
                   "(shift-independent proportional pull-back from the first carving, "
                   "scale-free). This is the never-evict growth-memory signature the H_1333 "
                   "card originally hypothesized (and that H_1338 rejected at the LARGE rung "
                   "— a constant fraction here would reopen it).")
        tag = "MEMORY"
    else:
        verdict = (f"MIXED / non-clean — frac range {frac_range:.3f} in [{CONST_TOL},{TRACK_TOL}) "
                   f"or trend {trend}; reported verbatim, no forced geometry/memory label (c9).")
        tag = "MIXED"
    print(f"     => L3 VERDICT: {tag}")
    for line in verdict.split(". "):
        if line.strip():
            print(f"        {line.strip().rstrip('.')}.")
    print("")

    print("=" * 84)
    print("VERDICT: 📈 CHARACTERIZATION LADDER COMPLETE — fraction-vs-shift curve mapped at 3")
    print(f"  rungs, 3 seeds. L1 PASS (curve measured) · L2 {'PASS' if l2_ok_all else 'FAIL'} "
          f"(EARNED controls) · L3 = {tag}.")
    print(f"  CURVE: " + " | ".join(f"{c['name']}(shift {c['shift']:.3f}) frac {c['mean_frac']:+.3f}"
                                     for c in curve))
    print(f"  frac range={frac_range:.3f} trend={trend} ; abs-peak range={peak_abs_range:.3f}.")
    print("  DIRECTIONAL mirror — engine-transfer UNVERIFIED. TOY synthetic, 3 seeds. NO")
    print("  human-cognition claim (a_scale_honest_scope). NO bar moved (c9/p7).")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
