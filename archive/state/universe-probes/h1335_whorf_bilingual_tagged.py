"""
H_1335 — SAPIR-WHORF BILINGUAL r2 (TAGGED): does a LANGUAGE-TAG dimension let a substrate
hold BOTH languages' categorical perception (CP) WITHOUT the H_1330 catastrophic overwrite?
R1 numpy MIRROR (DIRECTIONAL).

Named r2 of H_1330 🧱 OVERWRITE (.verdicts/1330_whorf_bilingual/H_1330.txt). H_1330 found:
on a SINGLE shared store with one-bound-label-per-cell, language B catastrophically OVERWRITES
language A's CP — because B labels [p_A,p_B] as 0 where A labeled it 1 (a DIRECT CONTRADICTION
on SHARED stimuli) and a single bound-label-per-cell readout cannot express two contradictory
answers for the same stimulus. The H_1330 verdict named this r2: a language-TAGGED readout
(distinct label-channel per language) mirroring anima's ACTUAL separate EN-trunk + KO faculties.

THE MECHANISM (embed, VoronoiCells, build_labels, discrim_curve, within_cross_margin,
coherent_peak_near, count_peaks, the W1/W2 thresholds, the seeds) is IMPORTED VERBATIM from
UNIVERSE/h1330_whorf_bilingual.py. The ONLY new thing is a LANGUAGE-TAG DIMENSION: a small
fixed orthonormal tag block appended to the DIM=16 RBF key, marking "read under language A"
vs "...under language B". key_A(x)=concat(embed(x),t_A), key_B(x)=concat(embed(x),t_B); t_A
and t_B live on DISJOINT appended coordinates so for the SAME continuum position the two
tagged keys are SEPARATED by a fixed tag distance — the [p_A,p_B] contradiction is no longer
on a SHARED key. At test, language A's curve is read with key_A() and language B's with
key_B() (= select the faculty by tag, read its carving). This is the substrate realization
of anima's separate-faculty design — NOT a hack to manufacture green (TAG_GAIN is FIXED, not
swept; the untagged single-channel control MUST reproduce the H_1330 overwrite or coexistence
is not attributable to the tag).

Frozen design: .verdicts/1335_whorf_bilingual_tagged/FREEZE.txt (pre-registered BEFORE this
scoring). NO tune-to-green (c9/p7). $0 CPU numpy, gradient-free, 3 seeds [4323,4324,4325]
(SAME as H_1323/H_1325/H_1330 so the A-only baseline + single-channel overwrite reproduce), p7.

a_no_llm_frame_trap (cognitive-science / bilingual-cognition lens, c15) — NOT an LLM recipe,
NOT a human-bilingualism claim. ENGINE-TRANSFER UNVERIFIED (DIRECTIONAL mirror).
"""
import os
import sys
import numpy as np

# import the H_1330 machinery VERBATIM (same directory)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h1330_whorf_bilingual import (  # noqa: E402
    N_STIM, DIM, P_A, P_B, GROW_MAX, SPLIT_PASSES, SEEDS,
    W1_MARGIN, W2_PEAK_TOL, W2_PEAK_SEP, PEAK_FRAC, LANG_MAX_PEAKS, SHUF_MIN_PEAKS,
    embed, make_basis, VoronoiCells, build_labels, discrim_curve, count_peaks,
    within_cross_margin, coherent_peak_near,
)

# ── frozen NEW constant (the ONLY addition) ─────────────────────────────────
TAG_GAIN = 1.0   # FIXED (FREEZE) — tag magnitude comparable to the unit RBF key, NOT swept.
TAG_DIM  = 2     # two disjoint appended coords: t_A on +0, t_B on +1.


def tag_vec(lang):
    """The language-tag block appended to embed(x). t_A and t_B live on DISJOINT coords so
    key_A(x) and key_B(x) for the SAME x are separated by sqrt(2)*TAG_GAIN — the substrate
    realization of 'select the faculty by tag'. FIXED, not learned, not swept."""
    t = np.zeros(TAG_DIM, dtype=np.float64)
    if lang == "A":
        t[0] = TAG_GAIN
    elif lang == "B":
        t[1] = TAG_GAIN
    else:
        raise ValueError(lang)
    return t


def tagged_key(x, basis, lang):
    """concat(embed(x), tag_vec(lang)) — the tagged key in the EXTENDED store space."""
    return np.concatenate([embed(x, basis), tag_vec(lang)])


def discrim_curve_tagged(cells, basis, positions, lang):
    """discrim_curve but querying with the TAGGED key for `lang` (select the faculty by tag,
    then read its carving). Identical |Δ soft posterior| over adjacent pairs as H_1330."""
    Xtag = np.array([tagged_key(x, basis, lang) for x in positions])
    return discrim_curve(cells, Xtag, positions)


def run_seed(seed):
    """Build the 4 frozen arms on ONE substrate per arm."""
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)

    # untagged RBF keys (for the single-channel H_1330 control — byte-identical to H_1330)
    X_plain = np.array([embed(x, basis) for x in positions])
    # tagged keys
    XA = np.array([tagged_key(x, basis, "A") for x in positions])
    XB = np.array([tagged_key(x, basis, "B") for x in positions])

    YA  = build_labels(positions, "A", np.random.default_rng(seed + 2))
    YB  = build_labels(positions, "B", np.random.default_rng(seed + 3))
    Ysh = build_labels(positions, "shuffle", np.random.default_rng(seed + 4))

    arms = {}

    # (1) A->B TAGGED: A-fit on tagged-A keys, B-fit on tagged-B keys (grow-not-evict).
    cTag = VoronoiCells().fit(XA, YA, GROW_MAX, SPLIT_PASSES)
    nA = len(cTag.protos)
    cTag.fit_more(XB, YB, GROW_MAX, SPLIT_PASSES)
    nAB = len(cTag.protos)
    midsA, normA, rawA = discrim_curve_tagged(cTag, basis, positions, "A")  # read p_A via tag_A
    midsB, normB, rawB = discrim_curve_tagged(cTag, basis, positions, "B")  # read p_B via tag_B
    arms["tagged"] = dict(midsA=midsA, normA=normA, rawA=rawA,
                          midsB=midsB, normB=normB, rawB=rawB,
                          ncells=nAB, ncells_after_A=nA)

    # (2) SINGLE-CHANNEL control (untagged = EXACT H_1330 AB_seq) — must reproduce OVERWRITE.
    cSc = VoronoiCells().fit(X_plain, YA, GROW_MAX, SPLIT_PASSES)
    cSc.fit_more(X_plain, YB, GROW_MAX, SPLIT_PASSES)
    mids, norm, raw = discrim_curve(cSc, X_plain, positions)
    arms["single"] = dict(mids=mids, norm=norm, raw=raw, ncells=len(cSc.protos))

    # (3) B=A control (TAGGED A->A: B uses A's boundary but tag_B) — one peak, no double-artifact.
    cAA = VoronoiCells().fit(XA, YA, GROW_MAX, SPLIT_PASSES)
    cAA.fit_more(XB, YA, GROW_MAX, SPLIT_PASSES)   # B-channel re-learns A's boundary
    # readout on the B channel (where a spurious second CP would appear if the tag fabricated one)
    midsB, normB, rawB = discrim_curve_tagged(cAA, basis, positions, "B")
    arms["aa"] = dict(mids=midsB, norm=normB, raw=rawB, ncells=len(cAA.protos))

    # (4) SHUFFLE (TAGGED A->B with B labels shuffled) — tagged-B channel must not fabricate CP.
    cSh = VoronoiCells().fit(XA, YA, GROW_MAX, SPLIT_PASSES)
    cSh.fit_more(XB, Ysh, GROW_MAX, SPLIT_PASSES)
    midsB, normB, rawB = discrim_curve_tagged(cSh, basis, positions, "B")
    arms["shuf"] = dict(mids=midsB, norm=normB, raw=rawB, ncells=len(cSh.protos))

    return positions, arms


def main():
    print("H_1335 R2 — SAPIR-WHORF BILINGUAL TAGGED: does a language-TAG enable CP COEXISTENCE?")
    print("=" * 84)
    print("A->B on ONE grow-not-evict Voronoi store, A-channel & B-channel SEPARATED by a fixed")
    print("language-tag dimension (key_A=concat(embed,t_A), key_B=concat(embed,t_B)); read CP at")
    print("p_A via tag_A and p_B via tag_B. The single-channel (untagged) control MUST reproduce")
    print("the H_1330 OVERWRITE => the tag, not extra training, is what enables coexistence.")
    print(f"N_stim={N_STIM} dim={DIM} TAG_GAIN={TAG_GAIN} (FIXED) p_A={P_A:.3f} p_B={P_B:.3f} "
          f"grow_max={GROW_MAX} seeds={SEEDS}")
    print(f"frozen: W1_MARGIN={W1_MARGIN} PEAK_FRAC={PEAK_FRAC} W2_PEAK_TOL={W2_PEAK_TOL} "
          f"LANG_MAX_PEAKS={LANG_MAX_PEAKS} SHUF_MIN_PEAKS={SHUF_MIN_PEAKS}")
    print("")

    rec = {"tagged": [], "single": [], "aa": [], "shuf": []}
    for seed in SEEDS:
        positions, arms = run_seed(seed)

        # (1) TAGGED: margins at p_A (tag_A channel) and p_B (tag_B channel) + coherent peaks
        cwA = within_cross_margin(arms["tagged"]["midsA"], arms["tagged"]["rawA"], P_A)
        cwB = within_cross_margin(arms["tagged"]["midsB"], arms["tagged"]["rawB"], P_B)
        m_pA = cwA[0] - cwA[1]
        m_pB = cwB[0] - cwB[1]
        pkA_present, pkA_loc = coherent_peak_near(arms["tagged"]["midsA"], arms["tagged"]["normA"], P_A)
        pkB_present, pkB_loc = coherent_peak_near(arms["tagged"]["midsB"], arms["tagged"]["normB"], P_B)
        rec["tagged"].append(dict(m_pA=m_pA, m_pB=m_pB, pkA=pkA_present, pkB=pkB_present,
                                  pkA_loc=pkA_loc, pkB_loc=pkB_loc,
                                  ncells=arms["tagged"]["ncells"],
                                  ncells_after_A=arms["tagged"]["ncells_after_A"]))

        # (2) SINGLE-CHANNEL: margin at p_A (must collapse, reproducing H_1330)
        cw_pA = within_cross_margin(arms["single"]["mids"], arms["single"]["raw"], P_A)
        cw_pB = within_cross_margin(arms["single"]["mids"], arms["single"]["raw"], P_B)
        rec["single"].append(dict(m_pA=cw_pA[0] - cw_pA[1], m_pB=cw_pB[0] - cw_pB[1]))

        # (3) B=A control: peak-count + peak near p_B (on the B channel)
        aaB_present, _ = coherent_peak_near(arms["aa"]["mids"], arms["aa"]["norm"], P_B)
        rec["aa"].append(dict(pkB=aaB_present, npeaks=count_peaks(arms["aa"]["norm"])))

        # (4) SHUFFLE: peak near p_B + total peak-count (on the B channel)
        shB_present, _ = coherent_peak_near(arms["shuf"]["mids"], arms["shuf"]["norm"], P_B)
        rec["shuf"].append(dict(pkB=shB_present, npeaks=count_peaks(arms["shuf"]["norm"])))

    # ── per-seed table ──────────────────────────────────────────────────────
    print("  PER-SEED:")
    print("  seed   TAGGED m@pA  m@pB  pk@pA pk@pB ncellsA->AB | SINGLE m@pA m@pB | B=A npk pk@pB | SHUF npk pk@pB")
    for i, seed in enumerate(SEEDS):
        t = rec["tagged"][i]; s = rec["single"][i]; c = rec["aa"][i]; h = rec["shuf"][i]
        print(f"  {seed}  {t['m_pA']:+.3f} {t['m_pB']:+.3f}  "
              f"{str(t['pkA'])[0]}     {str(t['pkB'])[0]}    {t['ncells_after_A']}->{t['ncells']}     "
              f"| {s['m_pA']:+.3f} {s['m_pB']:+.3f} | {c['npeaks']}  {str(c['pkB'])[0]}    "
              f"| {h['npeaks']}  {str(h['pkB'])[0]}")
    print("")

    # ── I1 COEXISTENCE ──────────────────────────────────────────────────────
    i1_seeds = []
    for i in range(len(SEEDS)):
        t = rec["tagged"][i]
        ok = (t["m_pA"] >= W1_MARGIN and t["m_pB"] >= W1_MARGIN and t["pkA"] and t["pkB"])
        i1_seeds.append(ok)
    i1 = all(i1_seeds)
    mean_m_pA = float(np.mean([r["m_pA"] for r in rec["tagged"]]))
    mean_m_pB = float(np.mean([r["m_pB"] for r in rec["tagged"]]))
    print(f"  I1 COEXISTENCE (TAGGED CP at BOTH p_A & p_B, all 3 seeds, margin>={W1_MARGIN}):")
    print(f"     mean margin@p_A={mean_m_pA:+.3f}  mean margin@p_B={mean_m_pB:+.3f}  (bar {W1_MARGIN})")
    print(f"     per-seed pass: {i1_seeds}   -> I1 {'PASS' if i1 else 'FAIL'}")

    # ── I2 TAG-ATTRIBUTION (single-channel control MUST overwrite) ───────────
    i2_seeds = [rec["single"][i]["m_pA"] < W1_MARGIN for i in range(len(SEEDS))]
    i2 = all(i2_seeds)
    mean_sc_pA = float(np.mean([r["m_pA"] for r in rec["single"]]))
    print(f"  I2 TAG-ATTRIBUTION (SINGLE-CHANNEL untagged REPRODUCES H_1330 OVERWRITE, m@pA<{W1_MARGIN}):")
    print(f"     single-channel mean margin@p_A={mean_sc_pA:+.3f}  (H_1330 ref -0.001; collapse expected)")
    print(f"     per-seed pass: {i2_seeds}   -> I2 {'PASS' if i2 else 'FAIL'}")

    # ── I3 EARNED ───────────────────────────────────────────────────────────
    # (a) B=A control: <=1 peak AND no peak near p_B ; (b) SHUFFLE: >=3 peaks OR no peak near p_B
    i3a = [(rec["aa"][i]["npeaks"] <= LANG_MAX_PEAKS) and (not rec["aa"][i]["pkB"]) for i in range(len(SEEDS))]
    i3b = [(rec["shuf"][i]["npeaks"] >= SHUF_MIN_PEAKS) or (not rec["shuf"][i]["pkB"]) for i in range(len(SEEDS))]
    i3 = all(i3a) and all(i3b)
    print(f"  I3 EARNED (B=A one peak<= {LANG_MAX_PEAKS} & no peak@p_B; SHUFFLE >= {SHUF_MIN_PEAKS} peaks OR no peak@p_B):")
    print(f"     B=A   peak-counts: {[c['npeaks'] for c in rec['aa']]}  peak@p_B: {[c['pkB'] for c in rec['aa']]}  pass {i3a}")
    print(f"     SHUF  peak-counts: {[h['npeaks'] for h in rec['shuf']]}  peak@p_B: {[h['pkB'] for h in rec['shuf']]}  pass {i3b}")
    print(f"     -> I3 {'PASS' if i3 else 'FAIL'}")

    print("=" * 84)
    green = i1 and i2 and i3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — LANGUAGE-TAGGED BILINGUAL CP COEXISTENCE.")
        print("  A language-tag dimension lets ONE grow-not-evict Voronoi store hold BOTH languages'")
        print("  categorical perception simultaneously: a coherent CP peak at p_A (read via tag_A)")
        print("  AND at p_B (read via tag_B), each clearing the H_1323 cross-within margin bar 0.15.")
        print("  The SINGLE-CHANNEL (untagged) control REPRODUCES the H_1330 OVERWRITE (CP@p_A")
        print("  collapses), so coexistence is attributable to the TAG, not extra training. The B=A")
        print("  control yields ONE peak (no double-artifact) and the SHUFFLE arm fabricates no")
        print("  coherent second CP (earned). FINDING: the H_1330 OVERWRITE was the SINGLE-SHARED-")
        print("  STORE mechanism, NOT a fundamental limit — a tagged multi-channel readout overturns")
        print("  it. This MIRRORS anima's REAL separate EN-trunk + KO faculties (H_1316/1321/1322):")
        print("  the tag is the substrate-level 'select the faculty', so anima's separate faculties")
        print("  coexist for the SAME structural reason. ENGINE-TRANSFER UNVERIFIED (DIRECTIONAL")
        print("  mirror). TOY synthetic continuum, 3 seeds; NO human-bilingualism claim.")
        return 0
    if not i1:
        print("VERDICT: 🧱 INTERFERENCE PERSISTS — even with a language-tag dimension the TAGGED arm")
        print("  does NOT hold CP at both boundaries (a margin@boundary fell below the 0.15 bar on")
        print("  some seed). Tagging this size does not prevent the interference — a deeper wall.")
        print("  Reported straight, NO bar moved (c9). ENGINE-TRANSFER UNVERIFIED.")
        return 2
    if i1 and not i2:
        print("VERDICT: 🧱 NOT-ATTRIBUTABLE — coexistence held (I1) but the SINGLE-CHANNEL control did")
        print("  NOT reproduce the H_1330 overwrite, so coexistence is not attributable to the tag")
        print("  (some extra-training artifact). Not cleanly the tag. Honest, NO bar moved (c9).")
        return 1
    if i1 and i2 and not i3:
        print("VERDICT: 🧱 CONTROL-FAIL — coexistence held & attributable (I1∧I2) but an anti-Goodhart")
        print("  control (I3 B=A double-artifact / SHUFFLE) did NOT separate. Not cleanly earned.")
        print("  Honest, NO bar moved (c9).")
        return 1
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
