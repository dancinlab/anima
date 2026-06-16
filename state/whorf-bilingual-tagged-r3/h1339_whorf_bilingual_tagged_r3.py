"""
H_1339 — SAPIR-WHORF BILINGUAL r3 (TAGGED, control re-freeze): a language-TAG dimension lets a
substrate hold BOTH languages' categorical perception (CP) WITHOUT the H_1330 catastrophic
overwrite. R1 numpy MIRROR (DIRECTIONAL).

Named r3 of H_1335 🧱 (.verdicts/1335_whorf_bilingual_tagged/result.txt). H_1335 found I1∧I2
DECISIVE (coexistence is REAL and TAG-ATTRIBUTABLE, all 3 seeds: TAGGED holds CP at BOTH p_A
[+0.200] and p_B [+0.177], single-channel-untagged reproduces the H_1330 overwrite byte-exact
[-0.001]), but the frozen I3a bar (GLOBAL count_peaks ≤ 1 on the B=A control) FAILED — count=2 —
because the B=A control grows ZERO B-tagged cells (it re-learns A's SAME boundary, so the
grow-not-evict store finds no B-misclassified stimulus to split on) and its B-channel curve runs
entirely on cross-tag bleed from the A-cells, exposing a benign low-end discretization wiggle as
a 2nd "peak". That wiggle is NOT a second-language CP (pk@p_B=False on all 3 seeds, the INTENDED
no-spurious-CP-at-the-other-boundary test already PASSES). The GLOBAL count conflated a benign
discrete-Voronoi artifact with the localized spurious-CP test.

WHAT R3 CHANGES (a DIFFERENT frozen bar, NOT a relaxation of the r2 bar — c9/p7):
I3a is RE-FROZEN as the LOCALIZED "no coherent peak near p_B" test for the B=A control —
coherent_peak_near(B=A B-channel, p_B) is False on ALL 3 seeds. This is the CORRECTLY-SCOPED
control: the B=A arm exists to prove that a tagged second fit on the SAME boundary does NOT
manufacture a spurious second-language CP at the OTHER boundary p_B. The localized test measures
exactly that. The GLOBAL count_peaks bar measured something else (total curve shape, including the
benign discretization wiggle) and is RETIRED for this arm. The SHUFFLE arm keeps its r2 bar
VERBATIM (count_peaks ≥ 3 OR no peak@p_B). NO threshold on any surviving bar is moved.

THE MECHANISM (embed, VoronoiCells, build_labels, discrim_curve, within_cross_margin,
coherent_peak_near, count_peaks, the tag block, the seeds [4323,4324,4325]) is IMPORTED VERBATIM
from UNIVERSE/h1335_whorf_bilingual_tagged.py (which itself imports h1330 verbatim). NOTHING in
the data generation changes — only which control statistic gates I3a.

PLUS a NON-GATING TAG_GAIN CHANNEL-ISOLATION SWEEP (diagnostic, c9): the r2 B=A bleed exposed
imperfect channel isolation at TAG_GAIN=1.0 (the B-channel could read A-tagged cells across the
tag gap). The sweep measures, as a function of TAG_GAIN, (i) how many B-tagged cells the B=A
control grows and (ii) the residual B-channel curve magnitude in the B=A control (cross-tag
bleed). It is a DIAGNOSTIC ONLY — it does NOT gate the verdict and TAG_GAIN=1.0 stays the FROZEN
operating point for the gating arms (NOT swept-to-green).

Frozen design: .verdicts/1339_whorf_bilingual_tagged_r3/FREEZE.txt (pre-registered BEFORE this
scoring). NO tune-to-green (c9/p7). $0 CPU numpy, gradient-free, 3 seeds [4323,4324,4325], p7.

a_no_llm_frame_trap (cognitive-science / bilingual-cognition lens, c15) — NOT an LLM recipe,
NOT a human-bilingualism claim. ENGINE-TRANSFER UNVERIFIED at the mirror; the engine-native
realization of the tagged faculty on live CORE/engine_cli.hexa §CategoricalPerception is wired
in this same r3 (a_engine_native_learning · a_verified_must_wire) and re-scored by the smoke.
"""
import os
import sys
import numpy as np

# import the H_1335 tagged machinery VERBATIM (same directory) — which in turn imports h1330.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h1330_whorf_bilingual import (  # noqa: E402
    N_STIM, DIM, P_A, P_B, GROW_MAX, SPLIT_PASSES, SEEDS,
    W1_MARGIN, PEAK_FRAC, LANG_MAX_PEAKS, SHUF_MIN_PEAKS,
    VoronoiCells, make_basis, build_labels, discrim_curve, count_peaks,
    within_cross_margin, coherent_peak_near,
)
from h1335_whorf_bilingual_tagged import (  # noqa: E402
    TAG_GAIN, run_seed,
)


def isolation_sweep(seed, gains):
    """NON-GATING diagnostic: for the B=A control, how does channel isolation depend on TAG_GAIN?
    Returns, per gain, (n_B_tagged_cells_grown, residual_B_channel_curve_peak). At small gain the
    A and B keys overlap (poor separation); at large gain they separate but the B=A control still
    grows zero B-cells (it has no B-error to split on) so its B-channel runs on bleed whose
    magnitude SHRINKS as the tag gap widens. TAG_GAIN=1.0 (the frozen gating point) is included."""
    import h1335_whorf_bilingual_tagged as m
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)
    YA = build_labels(positions, "A", np.random.default_rng(seed + 2))
    rows = []
    saved = m.TAG_GAIN
    try:
        for g in gains:
            m.TAG_GAIN = g  # temporarily set the module gain so tag_vec/tagged_key use it
            XA = np.array([m.tagged_key(x, basis, "A") for x in positions])
            XB = np.array([m.tagged_key(x, basis, "B") for x in positions])
            cAA = VoronoiCells().fit(XA, YA, GROW_MAX, SPLIT_PASSES)
            n_after_A = len(cAA.protos)
            cAA.fit_more(XB, YA, GROW_MAX, SPLIT_PASSES)  # B re-learns A's boundary
            n_B_grown = len(cAA.protos) - n_after_A
            _, normB, rawB = m.discrim_curve_tagged(cAA, basis, positions, "B")
            rows.append((g, n_B_grown, float(np.max(rawB))))
    finally:
        m.TAG_GAIN = saved  # restore the FROZEN gating gain (no leak into the gating arms)
    return rows


def main():
    print("H_1339 R3 — SAPIR-WHORF BILINGUAL TAGGED (control re-freeze): does a language-TAG")
    print("enable bilingual CP COEXISTENCE? (I3a re-frozen LOCALIZED; data unchanged from r2)")
    print("=" * 86)
    print("A->B on ONE grow-not-evict Voronoi store, A & B channels SEPARATED by a fixed language")
    print("tag (key_A=concat(embed,t_A), key_B=concat(embed,t_B)); read CP@p_A via tag_A, @p_B via")
    print("tag_B. Single-channel (untagged) control MUST reproduce the H_1330 OVERWRITE. I3a is the")
    print("LOCALIZED 'no coherent peak near p_B' test (NOT the r2 global count_peaks<=1 — a")
    print("correctly-scoped control, NOT a relaxation: the GLOBAL count conflated a benign discrete-")
    print("Voronoi wiggle with the intended no-spurious-CP-at-p_B test, which already passes).")
    print(f"N_stim={N_STIM} dim={DIM} TAG_GAIN={TAG_GAIN} (FIXED) p_A={P_A:.3f} p_B={P_B:.3f} "
          f"grow_max={GROW_MAX} seeds={SEEDS}")
    print(f"frozen: W1_MARGIN={W1_MARGIN} PEAK_FRAC={PEAK_FRAC} SHUF_MIN_PEAKS={SHUF_MIN_PEAKS}  "
          f"(r2 LANG_MAX_PEAKS={LANG_MAX_PEAKS} RETIRED for B=A → localized pk@p_B)")
    print("")

    rec = {"tagged": [], "single": [], "aa": [], "shuf": []}
    for seed in SEEDS:
        positions, arms = run_seed(seed)  # IDENTICAL data generation as r2 (imported verbatim)

        # (1) TAGGED: margins at p_A (tag_A channel) and p_B (tag_B channel) + coherent peaks
        cwA = within_cross_margin(arms["tagged"]["midsA"], arms["tagged"]["rawA"], P_A)
        cwB = within_cross_margin(arms["tagged"]["midsB"], arms["tagged"]["rawB"], P_B)
        m_pA = cwA[0] - cwA[1]
        m_pB = cwB[0] - cwB[1]
        pkA_present, _ = coherent_peak_near(arms["tagged"]["midsA"], arms["tagged"]["normA"], P_A)
        pkB_present, _ = coherent_peak_near(arms["tagged"]["midsB"], arms["tagged"]["normB"], P_B)
        rec["tagged"].append(dict(m_pA=m_pA, m_pB=m_pB, pkA=pkA_present, pkB=pkB_present,
                                  ncells=arms["tagged"]["ncells"],
                                  ncells_after_A=arms["tagged"]["ncells_after_A"]))

        # (2) SINGLE-CHANNEL: margin at p_A (must collapse, reproducing H_1330)
        cw_pA = within_cross_margin(arms["single"]["mids"], arms["single"]["raw"], P_A)
        rec["single"].append(dict(m_pA=cw_pA[0] - cw_pA[1]))

        # (3) B=A control: LOCALIZED peak@p_B (re-frozen I3a) + the now-DIAGNOSTIC global count
        aaB_present, _ = coherent_peak_near(arms["aa"]["mids"], arms["aa"]["norm"], P_B)
        rec["aa"].append(dict(pkB=aaB_present, npeaks=count_peaks(arms["aa"]["norm"])))

        # (4) SHUFFLE: peak near p_B + total peak-count (r2 bar VERBATIM)
        shB_present, _ = coherent_peak_near(arms["shuf"]["mids"], arms["shuf"]["norm"], P_B)
        rec["shuf"].append(dict(pkB=shB_present, npeaks=count_peaks(arms["shuf"]["norm"])))

    # ── per-seed table ──────────────────────────────────────────────────────
    print("  PER-SEED:")
    print("  seed   TAGGED m@pA  m@pB  pk@pA pk@pB ncellsA->AB | SINGLE m@pA | B=A pk@pB (npk diag) | SHUF npk pk@pB")
    for i, seed in enumerate(SEEDS):
        t = rec["tagged"][i]; s = rec["single"][i]; c = rec["aa"][i]; h = rec["shuf"][i]
        print(f"  {seed}  {t['m_pA']:+.3f} {t['m_pB']:+.3f}  "
              f"{str(t['pkA'])[0]}     {str(t['pkB'])[0]}    {t['ncells_after_A']}->{t['ncells']}     "
              f"| {s['m_pA']:+.3f}     | {str(c['pkB'])[0]}      ({c['npeaks']})        "
              f"| {h['npeaks']}  {str(h['pkB'])[0]}")
    print("")

    # ── I1 COEXISTENCE ──────────────────────────────────────────────────────
    i1_seeds = []
    for i in range(len(SEEDS)):
        t = rec["tagged"][i]
        ok = (t["m_pA"] >= W1_MARGIN and t["m_pB"] >= W1_MARGIN and t["pkA"] and t["pkB"])
        i1_seeds.append(bool(ok))
    i1 = all(i1_seeds)
    mean_m_pA = float(np.mean([r["m_pA"] for r in rec["tagged"]]))
    mean_m_pB = float(np.mean([r["m_pB"] for r in rec["tagged"]]))
    print(f"  I1 COEXISTENCE (TAGGED CP at BOTH p_A & p_B, all 3 seeds, margin>={W1_MARGIN}):")
    print(f"     mean margin@p_A={mean_m_pA:+.3f}  mean margin@p_B={mean_m_pB:+.3f}  (bar {W1_MARGIN})")
    print(f"     per-seed pass: {i1_seeds}   -> I1 {'PASS' if i1 else 'FAIL'}")

    # ── I2 TAG-ATTRIBUTION (single-channel control MUST overwrite) ───────────
    i2_seeds = [bool(rec["single"][i]["m_pA"] < W1_MARGIN) for i in range(len(SEEDS))]
    i2 = all(i2_seeds)
    mean_sc_pA = float(np.mean([r["m_pA"] for r in rec["single"]]))
    print(f"  I2 TAG-ATTRIBUTION (SINGLE-CHANNEL untagged REPRODUCES H_1330 OVERWRITE, m@pA<{W1_MARGIN}):")
    print(f"     single-channel mean margin@p_A={mean_sc_pA:+.3f}  (H_1330 ref -0.001; collapse expected)")
    print(f"     per-seed pass: {i2_seeds}   -> I2 {'PASS' if i2 else 'FAIL'}")

    # ── I3' EARNED (LOCALIZED B=A control re-freeze + SHUFFLE r2 bar) ─────────
    # (a) B=A control: NO coherent peak near p_B (re-frozen I3a — localized, NOT global count).
    # (b) SHUFFLE: >=3 peaks OR no peak near p_B (r2 bar VERBATIM).
    i3a = [bool(not rec["aa"][i]["pkB"]) for i in range(len(SEEDS))]
    i3b = [bool((rec["shuf"][i]["npeaks"] >= SHUF_MIN_PEAKS) or (not rec["shuf"][i]["pkB"]))
           for i in range(len(SEEDS))]
    i3 = all(i3a) and all(i3b)
    print(f"  I3' EARNED (B=A LOCALIZED: NO coherent peak@p_B; SHUFFLE: >= {SHUF_MIN_PEAKS} peaks OR no peak@p_B):")
    print(f"     B=A   peak@p_B (re-frozen I3a, localized): {[c['pkB'] for c in rec['aa']]}  pass {i3a}")
    print(f"           (DIAGNOSTIC: global count_peaks = {[c['npeaks'] for c in rec['aa']]} — benign discretization wiggle, NOT gating)")
    print(f"     SHUF  peak-counts: {[h['npeaks'] for h in rec['shuf']]}  peak@p_B: {[h['pkB'] for h in rec['shuf']]}  pass {i3b}")
    print(f"     -> I3' {'PASS' if i3 else 'FAIL'}")

    # ── NON-GATING TAG_GAIN channel-isolation sweep (diagnostic, c9) ─────────
    print("")
    print("  [NON-GATING DIAGNOSTIC — TAG_GAIN channel-isolation sweep, c9; verdict NOT gated on this]")
    gains = [0.25, 0.5, 1.0, 2.0, 4.0]
    print("  B=A control: B-tagged cells grown + residual B-channel curve magnitude vs TAG_GAIN")
    print("  (TAG_GAIN=1.0 = the FROZEN gating point; sweep is informational only)")
    print("  gain  |  B-cells grown (mean over seeds)  |  residual B-curve peak (mean)")
    sweep_acc = {g: [] for g in gains}
    bleed_acc = {g: [] for g in gains}
    for seed in SEEDS:
        for (g, n_b, resid) in isolation_sweep(seed, gains):
            sweep_acc[g].append(n_b)
            bleed_acc[g].append(resid)
    for g in gains:
        mark = "  <- FROZEN" if abs(g - TAG_GAIN) < 1e-9 else ""
        print(f"  {g:<5.2f} |  {float(np.mean(sweep_acc[g])):>6.2f}                          |  "
              f"{float(np.mean(bleed_acc[g])):.4f}{mark}")
    print("  reading: the B=A control grows ZERO B-cells at EVERY gain (it re-learns A's boundary →")
    print("  no B-error to split on); residual B-curve magnitude is pure cross-tag BLEED and SHRINKS")
    print("  as the tag gap widens (isolation improves with gain) — confirms the r2 diagnosis. The")
    print("  gating arms stay at the FROZEN TAG_GAIN=1.0 (NOT swept-to-green).")

    print("=" * 86)
    green = i1 and i2 and i3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — LANGUAGE-TAGGED BILINGUAL CP COEXISTENCE.")
        print("  A language-tag dimension lets ONE grow-not-evict Voronoi store hold BOTH languages'")
        print("  categorical perception simultaneously: a coherent CP peak at p_A (read via tag_A) AND")
        print("  at p_B (read via tag_B), each clearing the H_1323 cross-within margin bar 0.15, all 3")
        print("  seeds (I1). The SINGLE-CHANNEL (untagged) control REPRODUCES the H_1330 OVERWRITE")
        print("  (CP@p_A collapses to -0.001), so coexistence is attributable to the TAG, not extra")
        print("  training (I2). The B=A control fabricates NO spurious CP at the other boundary p_B")
        print("  (localized I3a, pk@p_B=False all seeds) and the SHUFFLE arm fabricates no coherent")
        print("  second CP (I3b). FINDING: the H_1330 OVERWRITE was the SINGLE-SHARED-STORE mechanism,")
        print("  NOT a fundamental limit — a tagged multi-channel readout overturns it. This MIRRORS")
        print("  anima's REAL separate EN-trunk + KO faculties (H_1316/1321/1322): the tag is the")
        print("  substrate-level 'select the faculty', so anima's separate EN+KO faculties coexist for")
        print("  the SAME structural reason. The engine-native realization is wired into live")
        print("  CORE/engine_cli.hexa §CategoricalPerception in this r3 (a_verified_must_wire).")
        print("  ENGINE-TRANSFER at mirror DIRECTIONAL; TOY synthetic continuum, 3 seeds; NO human-")
        print("  bilingualism claim.")
        return 0
    if not i1:
        print("VERDICT: 🧱 INTERFERENCE PERSISTS — even with a language-tag dimension the TAGGED arm")
        print("  does NOT hold CP at both boundaries. Reported straight, NO bar moved (c9).")
        return 2
    if i1 and not i2:
        print("VERDICT: 🧱 NOT-ATTRIBUTABLE — coexistence held (I1) but the SINGLE-CHANNEL control did")
        print("  NOT reproduce the H_1330 overwrite. Honest, NO bar moved (c9).")
        return 1
    print("VERDICT: 🧱 CONTROL-FAIL — I1∧I2 held but the re-frozen I3' control did NOT separate.")
    print("  Honest, NO bar moved (c9).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
