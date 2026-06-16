"""
H_1355 — WHORFIAN CP PLASTICITY: LEFTWARD + ASYMMETRIC LANDING
R1 numpy MIRROR (DIRECTIONAL). The H_1341 load-bearing follow-on.

Frozen design: .verdicts/1355_cp_leftward/FREEZE.txt (pre-registered BEFORE this scoring).
$0 CPU numpy, gradient-free, 3 seeds [4333,4334,4335], p7. a_no_llm_frame_trap
(developmental / critical-period plasticity lens, c15) — NOT an LLM recipe, NOT a
human-cognition claim. ENGINE-TRANSFER UNVERIFIED (directional mirror).

THE QUESTION: H_1341 found the post-retrain CP peak ALWAYS lands at the SAME absolute spot
(~0.525) for RIGHTWARD shifts from the FIXED anchor p_A=1/3, regardless of requested shift
size — read as GEOMETRY/BUDGET. But p_A=1/3 is LEFT of center and ALL rungs shifted RIGHTWARD
(toward/past 0.5), so 0.525 ~= 0.5 = continuum CENTER. Two unresolved explanations:
  (H-center)   0.525 is a CONTINUUM-CENTER ATTRACTOR (symmetric lattice artifact) — peak
               pulled to ~0.5 regardless of the requested cut.
  (H-geometry) 0.525 is a GENUINE GEOMETRY-FIXED landing of the budget mechanism, which would
               MOVE if the anchor/target geometry is made asymmetric.

H_1355 DISCRIMINATES by adding LEFTWARD (p_A' < p_A) and ASYMMETRIC (anchor off-center, both
cuts on the SAME side) rungs and reading the ABSOLUTE landing spot per placement.
CHARACTERIZATION ladder — ALL outcomes VALID (c9); report the table verbatim, no GREEN/RED.

Reuses the H_1333 CP machinery EXACTLY (h1333_whorf_developmental.py copied verbatim into
this dir): VoronoiCells split-only re-growth, RBF embed, soft-posterior discrimination
readout, peak-count coherence. The ONLY new code = sweeping (p_A anchor, p_A' target)
placement across the 5 leftward/asymmetric rungs and assembling the absolute-landing table.
"""
import numpy as np

from h1333_whorf_developmental import (
    N_STIM, DIM, GROW_MAX, SPLIT_PASSES, LOC_TOL,
    COH_MAX_LANG, COH_MIN_SHUF, SEEDS,
    embed, make_basis, VoronoiCells, discrim_curve, peak_loc, peak_count,
)

# ── frozen rungs / thresholds (from FREEZE) ─────────────────────────────────
# Each rung = a (p_A anchor, p_A' target) PLACEMENT, all on the grid (spacing 0.05),
# no edge clipping. RIGHT-REF reproduces the H_1341 LARGE rung (the 0.525 anchor).
RUNGS = [
    ("RIGHT-REF",  0.333, 0.667),   # rightward, anchor left  (H_1341 LARGE — reproduces 0.525)
    ("LEFTWARD-1", 0.667, 0.333),   # leftward,  anchor right (mirror of RIGHT-REF)
    ("LEFTWARD-2", 0.800, 0.500),   # leftward,  anchor far right -> center
    ("ASYM-R",     0.600, 0.800),   # rightward, BOTH cuts right of center (away from center)
    ("ASYM-L",     0.400, 0.200),   # leftward,  BOTH cuts left  of center (away from center)
]
CENTER     = 0.50
CENTER_TOL = 0.08


def labels_cut(positions, cut):
    """category labels: cat 0 below the cut, cat 1 above (H_1333 build_labels verbatim form)."""
    return (positions > cut).astype(int)


def run_rung(seed, p_a1, p_a2):
    """All 4 arms for ONE seed at ONE placement rung. Same stimulus world (basis fixed by
    seed); the anchor p_a1 and target p_a2 BOTH vary across rungs (vs H_1341 fixed anchor)."""
    rng = np.random.default_rng(seed)
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([embed(x, basis) for x in positions])

    Y_A  = labels_cut(positions, p_a1)
    Y_A2 = labels_cut(positions, p_a2)
    sh_rng = np.random.default_rng(seed + 4)
    Y_sh = sh_rng.integers(0, 2, size=len(positions))

    out = {}

    # (1) A-trained anchor: grow on labels(p_a1) only.
    cA = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cA, X, positions)
    out["A"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cA.protos))

    # (2) A->A' re-trained: phase-1 on p_a1, phase-2 grow FURTHER on p_a2 (same store, no reset).
    cR = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    nc_p1 = len(cR.protos)
    cR.fit(X, Y_A2, GROW_MAX, SPLIT_PASSES, fresh=False)
    mids, norm, _ = discrim_curve(cR, X, positions)
    out["A2"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cR.protos),
                     ncells_p1=nc_p1)

    # (3) NO-RETRAIN control: grow on p_a1 only, NO phase-2 -> peak must hold p_a1.
    cN = VoronoiCells().fit(X, Y_A, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cN, X, positions)
    out["noretrain"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cN.protos))

    # (4) SHUFFLE: incoherent labels -> EARNED control.
    cS = VoronoiCells().fit(X, Y_sh, GROW_MAX, SPLIT_PASSES, fresh=True)
    mids, norm, _ = discrim_curve(cS, X, positions)
    out["shuffle"] = dict(peak=peak_loc(mids, norm), pc=peak_count(norm), ncells=len(cS.protos))

    return out


def main():
    print("H_1355 R1 — WHORFIAN CP PLASTICITY: LEFTWARD + ASYMMETRIC LANDING")
    print("=" * 88)
    print("paradigm: RE-train SAME store from anchor p_A to a MOVED cut p_A' across 5 placement")
    print("          rungs (LEFTWARD p_A'<p_A + ASYMMETRIC off-center). Read the ABSOLUTE landing")
    print("          spot. CENTER-ATTRACTOR => all land ~0.5; GEOMETRY-FIXED => tracks placement.")
    print("          CHARACTERIZATION ladder — ALL outcomes valid (c9).")
    print(f"N_stim={N_STIM} dim={DIM} grow_max={GROW_MAX}/phase seeds={SEEDS}")
    print(f"center={CENTER} center_tol={CENTER_TOL}")
    print("rungs (p_A->p_A'): " + "  ".join(
        f"{n}={a:.3f}->{b:.3f}" for n, a, b in RUNGS))
    print("")

    table = []   # per-rung aggregate
    c3_ok_all = True

    for name, p_a1, p_a2 in RUNGS:
        shift = p_a2 - p_a1
        peaksR, peaksA, peaksN, pcA, pcR, pcN, pcS = [], [], [], [], [], [], []
        nc1, nc2 = [], []
        print(f"  rung {name:<11}  p_A={p_a1:.3f} -> p_A'={p_a2:.3f}  (shift {shift:+.3f}):")
        for seed in SEEDS:
            o = run_rung(seed, p_a1, p_a2)
            pA, pR, pN = o["A"]["peak"], o["A2"]["peak"], o["noretrain"]["peak"]
            peaksA.append(pA); peaksR.append(pR); peaksN.append(pN)
            pcA.append(o["A"]["pc"]); pcR.append(o["A2"]["pc"]); pcN.append(o["noretrain"]["pc"])
            pcS.append(o["shuffle"]["pc"]); nc1.append(o["A2"]["ncells_p1"]); nc2.append(o["A2"]["ncells"])
            frac = (pR - pA) / (p_a2 - p_a1) if (p_a2 - p_a1) != 0 else 0.0
            print(f"    seed {seed}: A={pA:.3f} A->A'={pR:.3f} noR={pN:.3f}  frac={frac:+.3f}"
                  f"  | pc A={o['A']['pc']} A->A'={o['A2']['pc']} noR={o['noretrain']['pc']} "
                  f"shuf={o['shuffle']['pc']}  ncells {o['A2']['ncells_p1']}->{o['A2']['ncells']}")
        mean_pR = float(np.mean(peaksR)); mean_pA = float(np.mean(peaksA)); mean_pN = float(np.mean(peaksN))
        mean_frac = float(np.mean([(r - a) / (p_a2 - p_a1) for r, a in zip(peaksR, peaksA)]))
        # c3 EARNED at this rung
        c3a = all(abs(p - p_a1) <= LOC_TOL for p in peaksN)               # no-retrain holds anchor
        c3b_shuf = all(p >= COH_MIN_SHUF for p in pcS)                    # shuffle incoherent
        c3b_lang = all(p <= COH_MAX_LANG for p in pcA + pcR + pcN)        # lang arms coherent
        c3 = c3a and c3b_shuf and c3b_lang
        c3_ok_all = c3_ok_all and c3
        dist_from_center = mean_pR - CENTER
        table.append(dict(name=name, p_a1=p_a1, p_a2=p_a2, shift=shift,
                          mean_pR=mean_pR, mean_pA=mean_pA, mean_pN=mean_pN, mean_frac=mean_frac,
                          dist_center=dist_from_center,
                          c3a=c3a, c3b_shuf=c3b_shuf, c3b_lang=c3b_lang, c3=c3,
                          mean_pcS=float(np.mean(pcS))))
        print(f"    -> mean ABS landing A->A'={mean_pR:.3f}  (|L-0.5|={abs(dist_from_center):.3f})  "
              f"anchor A={mean_pA:.3f} noR={mean_pN:.3f}  frac={mean_frac:+.3f}")
        print(f"       c3: noR-holds-anchor={'PASS' if c3a else 'FAIL'} "
              f"shuf-incoh={'PASS' if c3b_shuf else 'FAIL'} lang-coh={'PASS' if c3b_lang else 'FAIL'} "
              f"-> c3 {'PASS' if c3 else 'FAIL'}")
        print("")

    # ── c1 REPORT: absolute-landing table ───────────────────────────────────
    print("=" * 88)
    print("  c1 — ABSOLUTE-LANDING TABLE (mean of 3 seeds):")
    print(f"    {'rung':<11} {'p_A->p_A''':>14} {'shift':>7} {'ABS land L':>11} {'|L-0.5|':>8} {'frac':>8}")
    for c in table:
        print(f"    {c['name']:<11} {c['p_a1']:>5.3f}->{c['p_a2']:.3f}   {c['shift']:>+7.3f} "
              f"{c['mean_pR']:>11.3f} {abs(c['dist_center']):>8.3f} {c['mean_frac']:>+8.3f}")
    print(f"    -> c1 TABLE MEASURED at 5 placement rungs, 3 seeds: PASS")
    print("")

    # ── c3 EARNED (summary) ─────────────────────────────────────────────────
    print(f"  c3 — EARNED controls held at ALL rungs: {'PASS' if c3_ok_all else 'FAIL'}")
    for c in table:
        print(f"     {c['name']:<11}: noR-holds-anchor={'PASS' if c['c3a'] else 'FAIL'}  "
              f"shuffle-incoherent(pc={c['mean_pcS']:.1f})={'PASS' if c['c3b_shuf'] else 'FAIL'}  "
              f"lang-coherent={'PASS' if c['c3b_lang'] else 'FAIL'}")
    print("")

    # ── c2 DISCRIMINATE (frozen rule) ───────────────────────────────────────
    print("  c2 — DISCRIMINATE (center-attractor vs geometry-fixed, frozen rule):")
    dists = {c["name"]: c["dist_center"] for c in table}
    max_abs_dist = max(abs(c["dist_center"]) for c in table)
    print(f"     CENTER={CENTER}  CENTER_TOL={CENTER_TOL}")
    print(f"     signed |L-center| per rung: " +
          "  ".join(f"{c['name']}={c['dist_center']:+.3f}" for c in table))
    print(f"     max |L-0.5| across rungs = {max_abs_dist:.3f}")

    # CENTER-ATTRACTOR: every rung within CENTER_TOL of 0.5.
    center_pin = max_abs_dist <= CENTER_TOL

    # GEOMETRY-FIXED: asymmetric away-from-center rungs land off-center in requested direction,
    # AND leftward rungs land left of the RIGHT-REF landing (signed landing tracks direction).
    asym_r = dists["ASYM-R"] >  CENTER_TOL                 # toward 0.800 (right)
    asym_l = dists["ASYM-L"] < -CENTER_TOL                 # toward 0.200 (left)
    left_tracks = (table_by(table, "LEFTWARD-1")["mean_pR"] < table_by(table, "RIGHT-REF")["mean_pR"]
                   and table_by(table, "LEFTWARD-2")["mean_pR"] < table_by(table, "RIGHT-REF")["mean_pR"])
    geometry_fixed = asym_r and asym_l and left_tracks

    print(f"     center-pinned (all |L-0.5|<=tol)? {center_pin}")
    print(f"     asym-R off-center-right (L>{CENTER+CENTER_TOL:.2f})? {asym_r} "
          f"(L={table_by(table,'ASYM-R')['mean_pR']:.3f})   "
          f"asym-L off-center-left (L<{CENTER-CENTER_TOL:.2f})? {asym_l} "
          f"(L={table_by(table,'ASYM-L')['mean_pR']:.3f})")
    print(f"     leftward rungs land left of RIGHT-REF? {left_tracks} "
          f"(LEFT-1={table_by(table,'LEFTWARD-1')['mean_pR']:.3f} "
          f"LEFT-2={table_by(table,'LEFTWARD-2')['mean_pR']:.3f} "
          f"RIGHT-REF={table_by(table,'RIGHT-REF')['mean_pR']:.3f})")

    if center_pin:
        tag = "CENTER-ATTRACTOR"
        verdict = (
            "CENTER-ATTRACTOR — the post-retrain peak lands within CENTER_TOL of the continuum "
            "center (0.5) at EVERY placement, including LEFTWARD and away-from-center ASYMMETRIC "
            "shifts. The fixed ~0.525 landing of H_1341 is a SYMMETRIC-LATTICE artifact (the "
            "discrimination readout is richest near the N=21 RBF-lattice center), NOT a "
            "geometry-fixed budget landing. This RE-DIAGNOSES the H_1341 'geometry/budget' "
            "reading as a continuum-center bias (honest correction of the parent, c9).")
    elif geometry_fixed:
        tag = "GEOMETRY-FIXED"
        verdict = (
            "GEOMETRY-FIXED — the absolute landing TRACKS the placement: asymmetric "
            "away-from-center rungs land off-center toward their requested cut and leftward "
            "shifts land left of the rightward reference. The fixed ~0.525 of H_1341 was a "
            "genuine geometry/budget landing for that specific placement, not a center pin; the "
            "H_1341 budget/geometry reading STANDS and GENERALIZES to leftward/asymmetric moves.")
    else:
        tag = "MIXED"
        verdict = (
            "MIXED — neither pure center-pin nor clean geometry-tracking. Some rungs sit near "
            "center while others track placement; reported VERBATIM with the per-rung breakdown "
            "(a center-bias MODULATED by geometry is itself the finding, c9). NO forced single "
            "label.")
    print(f"     => c2 VERDICT: {tag}")
    for line in verdict.split(". "):
        if line.strip():
            print(f"        {line.strip().rstrip('.')}.")
    print("")

    print("=" * 88)
    print("VERDICT: 📈 CHARACTERIZATION LADDER COMPLETE — absolute-landing table mapped at 5")
    print(f"  placement rungs (leftward + asymmetric), 3 seeds. c1 PASS (table measured) · "
          f"c3 {'PASS' if c3_ok_all else 'FAIL'} (EARNED controls) · c2 = {tag}.")
    print("  LANDINGS: " + " | ".join(
        f"{c['name']}({c['p_a1']:.2f}->{c['p_a2']:.2f}) L={c['mean_pR']:.3f}" for c in table))
    print(f"  max |L-0.5|={max_abs_dist:.3f}.")
    print("  DIRECTIONAL mirror — engine-transfer UNVERIFIED. TOY synthetic, 3 seeds. NO")
    print("  human-cognition claim (a_scale_honest_scope). NO bar moved (c9/p7).")
    return 0


def table_by(table, name):
    for c in table:
        if c["name"] == name:
            return c
    raise KeyError(name)


if __name__ == "__main__":
    import sys
    sys.exit(main())
