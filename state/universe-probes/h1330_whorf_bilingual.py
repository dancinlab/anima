"""
H_1330 — SAPIR-WHORF BILINGUAL: does a SECOND language OVERWRITE or COEXIST with the
first's categorical perception (CP)? R1 numpy MIRROR (DIRECTIONAL).

Named EXTENSION frontier of the GREEN H_1323/H_1325 Sapir-Whorf result (cross-lane
interference). Frozen design: .verdicts/1330_whorf_bilingual/H_1330_FREEZE.txt
(pre-registered BEFORE this scoring). NO tune-to-green (c9/p7). $0 CPU numpy,
gradient-free, 3 seeds [4323,4324,4325] (SAME as H_1323/H_1325 so the A-only baseline
reproduces), p7.

THE MECHANISM (embed, VoronoiCells, build_labels, discrim_curve, count_peaks, the W1/W2
metrics) is REUSED VERBATIM from UNIVERSE/h1323_sapir_whorf.py + h1325_sapir_whorf_r2.py.
The ONLY new thing is SEQUENTIAL A→B training on ONE substrate (VoronoiCells.fit_more,
grow-not-evict) + measuring CP at BOTH boundaries.

WHY (anima prediction under test): anima is ALREADY bilingual (English trunk + Korean).
anima's GROWTH-MEMORY result (H_1288 — under pressure the immune/Voronoi store GROWS a
new cell instead of EVICTING, breaking the zero-sum recall ceiling) PREDICTS COEXISTENCE:
the SAME error-targeted SPLIT-ONLY growth (p8) ADDS cells at B's boundary where B-label
error concentrates while NEVER deleting the A-cells already packed at A's boundary, so
the substrate can hold BOTH language-warped cognitions. The frozen hypothesis is COEXIST;
the falsifier is OVERWRITE (catastrophic interference = growth-memory does NOT protect
language-cognition).

a_no_llm_frame_trap (cognitive-science / bilingual-cognition lens, c15) — NOT an LLM
recipe, NOT a human-bilingualism claim. ENGINE-TRANSFER UNVERIFIED (DIRECTIONAL mirror).
"""
import numpy as np

# ── frozen constants (REUSED VERBATIM from H_1323/H_1325) ───────────────────
N_STIM   = 21
DIM      = 16
P_A      = 1.0 / 3.0
P_B      = 2.0 / 3.0
PAIR_STEP = 1
GROW_MAX = 24
SPLIT_PASSES = 24
SEEDS    = [4323, 4324, 4325]

# frozen bar thresholds (from FREEZE)
W1_MARGIN      = 0.15
W2_PEAK_TOL    = 0.12
W2_PEAK_SEP    = 0.20
PEAK_FRAC      = 0.50
LANG_MAX_PEAKS = 1
SHUF_MIN_PEAKS = 3


def embed(x, rng_basis):
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
    """Immune/Voronoi prototype store, error-targeted SPLIT-only growth (p8 mirror).
    fit() + _owner() + posterior() are REUSED VERBATIM from H_1323/H_1325. The ONLY
    addition is fit_more() — the grow-not-evict CONTINUATION that lets a SECOND language
    be learned on top of the first WITHOUT resetting the table or evicting any cell."""

    def __init__(self):
        self.protos = []
        self.labels = []

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit(self, X, Y, grow_max, passes):
        """REUSED VERBATIM from H_1323/H_1325 — seeds a fresh single centroid cell, then
        error-targeted SPLIT-only growth until no label error remains."""
        M = len(X)
        c0 = X.mean(axis=0)
        n = np.linalg.norm(c0)
        c0 = c0 / n if n > 0 else c0
        self.protos = [c0]
        seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
        self.labels = [int(Y[seed_stim])]
        return self._grow(X, Y, grow_max, passes)

    def fit_more(self, X, Y, grow_max, passes):
        """THE ONLY NEW MECHANISM (H_1288 grow-not-evict / a_engine_native_learning).
        CONTINUE error-targeted SPLIT-only growth from the EXISTING proto/label table —
        do NOT reset, do NOT seed a new centroid, do NOT evict any cell. Each pass APPENDS
        a new prototype at the worst stimulus misclassified UNDER THE NEW LABELS Y, with
        its bound label FIXED at creation. So cells packed at the first language's boundary
        PERSIST with their original labels while NEW cells accrete at the second language's
        boundary. This is the identical error-targeted-split loop as fit() — only the
        starting table differs (grow on top of A, instead of from one centroid). The growth
        BUDGET grow_max is the TOTAL cap on the (already-grown) table, so B grows under the
        same FIXED capacity ceiling A had — a fair grow-not-evict test, not unlimited
        capacity."""
        return self._grow(X, Y, grow_max, passes)

    def _grow(self, X, Y, grow_max, passes):
        """error-targeted SPLIT-only growth loop, REUSED VERBATIM from H_1323/H_1325 fit()
        (factored out so fit() and fit_more() share the IDENTICAL growth rule — fit_more
        differs ONLY by not re-seeding the table)."""
        M = len(X)
        for _ in range(passes):
            if len(self.protos) >= 1 + grow_max:
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
        return self

    def posterior(self, key):
        """REUSED VERBATIM from H_1323/H_1325 — soft category-posterior over the cells'
        BOUND labels (a cell bound during the A-fit carries its A-label; a cell bound during
        the B-fit carries its B-label). CP peaks appear wherever this swings sharply = where
        cells of opposite bound label pack densely = at a surviving language boundary."""
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        beta = 18.0
        w = np.exp(-beta * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


def build_labels(positions, kind, rng):
    """REUSED VERBATIM from H_1323/H_1325."""
    if kind == "A":
        return (positions > P_A).astype(int)
    if kind == "B":
        return (positions > P_B).astype(int)
    if kind == "none":
        return np.zeros(len(positions), dtype=int)
    if kind == "shuffle":
        return rng.integers(0, 2, size=len(positions))
    raise ValueError(kind)


def discrim_curve(cells, X, positions):
    """REUSED VERBATIM from H_1323/H_1325 — |Δ soft posterior| over adjacent pairs vs
    pair midpoint; normalized peak=1, plus raw."""
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


def count_peaks(curve, frac=PEAK_FRAC):
    """W3'/I-leg COHERENCE METRIC, REUSED VERBATIM from H_1325 — strict local maxima of the
    normalized curve at height >= frac of the arm's own peak."""
    c = np.asarray(curve, dtype=float)
    mx = c.max()
    if mx <= 0:
        return 0
    thr = frac * mx
    n = len(c)
    cnt = 0
    for t in range(n):
        if c[t] < thr:
            continue
        if t == 0:
            is_max = c[t] > c[t + 1]
        elif t == n - 1:
            is_max = c[t] > c[t - 1]
        else:
            is_max = (c[t] > c[t - 1]) and (c[t] > c[t + 1])
        if is_max:
            cnt += 1
    return cnt


def within_cross_margin(mids, raw, boundary):
    """REUSED VERBATIM from H_1323/H_1325 — cross-boundary minus within-category raw discrim
    LOCALIZED to a boundary. Used to score 'CP present at boundary p' at BOTH p_A and p_B."""
    near = np.abs(mids - boundary) <= 0.12
    far = np.abs(mids - boundary) >= 0.25
    cross = raw[near].mean() if near.any() else 0.0
    within = raw[far].mean() if far.any() else 0.0
    return cross, within


def coherent_peak_near(mids, norm, boundary, tol=W2_PEAK_TOL, frac=PEAK_FRAC):
    """Is there a strict local maximum (height >= frac*peak) whose midpoint is within tol of
    `boundary`? Returns (present, best_loc_or_None). Uses the SAME strict-local-max rule as
    count_peaks. This localizes the H_1325 peak-count coherence test to a specific boundary."""
    c = np.asarray(norm, dtype=float)
    mx = c.max()
    if mx <= 0:
        return False, None
    thr = frac * mx
    n = len(c)
    best = None
    besth = -1.0
    for t in range(n):
        if c[t] < thr:
            continue
        if t == 0:
            is_max = c[t] > c[t + 1]
        elif t == n - 1:
            is_max = c[t] > c[t - 1]
        else:
            is_max = (c[t] > c[t - 1]) and (c[t] > c[t + 1])
        if is_max and abs(mids[t] - boundary) <= tol:
            if c[t] > besth:
                besth = c[t]
                best = float(mids[t])
    return (best is not None), best


def run_seed(seed):
    """Build the bilingual arms on ONE substrate per arm. Returns positions + per-arm dicts."""
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([embed(x, basis) for x in positions])

    # per-arm label RNGs (deterministic per seed; same convention as H_1323/H_1325)
    YA = build_labels(positions, "A", np.random.default_rng(seed + 2))
    YB = build_labels(positions, "B", np.random.default_rng(seed + 3))
    Ysh = build_labels(positions, "shuffle", np.random.default_rng(seed + 4))

    arms = {}

    # (1) A-ONLY baseline (reproduces H_1323 L_A)
    cA = VoronoiCells().fit(X, YA, GROW_MAX, SPLIT_PASSES)
    mids, norm, raw = discrim_curve(cA, X, positions)
    arms["A_only"] = dict(mids=mids, norm=norm, raw=raw, ncells=len(cA.protos))

    # (2) A→B SEQUENTIAL on ONE substrate (grow-not-evict)
    cAB = VoronoiCells().fit(X, YA, GROW_MAX, SPLIT_PASSES)
    nA = len(cAB.protos)
    cAB.fit_more(X, YB, GROW_MAX, SPLIT_PASSES)
    nAB = len(cAB.protos)
    mids, norm, raw = discrim_curve(cAB, X, positions)
    arms["AB_seq"] = dict(mids=mids, norm=norm, raw=raw, ncells=nAB, ncells_after_A=nA)

    # (3) B=A CONTROL: A, then A AGAIN (same boundary) — must show ONE peak, not two
    cAA = VoronoiCells().fit(X, YA, GROW_MAX, SPLIT_PASSES)
    cAA.fit_more(X, YA, GROW_MAX, SPLIT_PASSES)
    mids, norm, raw = discrim_curve(cAA, X, positions)
    arms["AA_ctrl"] = dict(mids=mids, norm=norm, raw=raw, ncells=len(cAA.protos))

    # (4) SHUFFLE: A→B where B is incoherent — anti-Goodhart
    cAsh = VoronoiCells().fit(X, YA, GROW_MAX, SPLIT_PASSES)
    cAsh.fit_more(X, Ysh, GROW_MAX, SPLIT_PASSES)
    mids, norm, raw = discrim_curve(cAsh, X, positions)
    arms["AB_shuf"] = dict(mids=mids, norm=norm, raw=raw, ncells=len(cAsh.protos))

    return positions, arms


def main():
    print("H_1330 R1 — SAPIR-WHORF BILINGUAL: does a SECOND language OVERWRITE or COEXIST?")
    print("=" * 82)
    print("sequential A->B training on ONE grow-not-evict Voronoi substrate (H_1288 lens);")
    print("measure CP at BOTH p_A and p_B. frozen hypothesis = COEXIST; falsifier = OVERWRITE.")
    print(f"N_stim={N_STIM} dim={DIM} p_A={P_A:.3f} p_B={P_B:.3f} grow_max={GROW_MAX} seeds={SEEDS}")
    print(f"frozen: W1_MARGIN={W1_MARGIN} W2_PEAK_TOL={W2_PEAK_TOL} W2_PEAK_SEP={W2_PEAK_SEP}")
    print(f"        PEAK_FRAC={PEAK_FRAC} LANG_MAX_PEAKS={LANG_MAX_PEAKS} SHUF_MIN_PEAKS={SHUF_MIN_PEAKS}")
    print("")

    # per-seed records
    rec = {"A_only": [], "AB_seq": [], "AA_ctrl": [], "AB_shuf": []}
    for seed in SEEDS:
        positions, arms = run_seed(seed)

        # A-only: margin at p_A (baseline)
        m_pA_Aonly = (lambda cw: cw[0] - cw[1])(within_cross_margin(arms["A_only"]["mids"], arms["A_only"]["raw"], P_A))
        rec["A_only"].append(dict(m_pA=m_pA_Aonly, ncells=arms["A_only"]["ncells"]))

        # A->B seq: margins at BOTH p_A and p_B + coherent peaks near each
        cw_pA = within_cross_margin(arms["AB_seq"]["mids"], arms["AB_seq"]["raw"], P_A)
        cw_pB = within_cross_margin(arms["AB_seq"]["mids"], arms["AB_seq"]["raw"], P_B)
        m_pA = cw_pA[0] - cw_pA[1]
        m_pB = cw_pB[0] - cw_pB[1]
        pkA_present, pkA_loc = coherent_peak_near(arms["AB_seq"]["mids"], arms["AB_seq"]["norm"], P_A)
        pkB_present, pkB_loc = coherent_peak_near(arms["AB_seq"]["mids"], arms["AB_seq"]["norm"], P_B)
        sep = abs((pkA_loc if pkA_loc is not None else 0) - (pkB_loc if pkB_loc is not None else 0))
        rec["AB_seq"].append(dict(m_pA=m_pA, m_pB=m_pB, pkA=pkA_present, pkB=pkB_present,
                                  pkA_loc=pkA_loc, pkB_loc=pkB_loc, sep=sep,
                                  ncells=arms["AB_seq"]["ncells"], ncells_after_A=arms["AB_seq"]["ncells_after_A"],
                                  npeaks=count_peaks(arms["AB_seq"]["norm"])))

        # B=A control: peaks near p_A and p_B + total peak-count
        aaA_present, _ = coherent_peak_near(arms["AA_ctrl"]["mids"], arms["AA_ctrl"]["norm"], P_A)
        aaB_present, _ = coherent_peak_near(arms["AA_ctrl"]["mids"], arms["AA_ctrl"]["norm"], P_B)
        rec["AA_ctrl"].append(dict(pkA=aaA_present, pkB=aaB_present,
                                   npeaks=count_peaks(arms["AA_ctrl"]["norm"])))

        # shuffle: coherent peak near p_B? + total peak-count
        shB_present, _ = coherent_peak_near(arms["AB_shuf"]["mids"], arms["AB_shuf"]["norm"], P_B)
        rec["AB_shuf"].append(dict(pkB=shB_present, npeaks=count_peaks(arms["AB_shuf"]["norm"])))

    # ── per-seed table ──────────────────────────────────────────────────────
    print("  PER-SEED:")
    print("  seed   A-only m@pA | A->B m@pA  m@pB  pk@pA pk@pB sep ncellsA->AB | B=A npk pk@pA pk@pB | SHUF npk pk@pB")
    for i, seed in enumerate(SEEDS):
        a = rec["A_only"][i]; s = rec["AB_seq"][i]; c = rec["AA_ctrl"][i]; h = rec["AB_shuf"][i]
        print(f"  {seed}  {a['m_pA']:+.3f}      | {s['m_pA']:+.3f} {s['m_pB']:+.3f}  "
              f"{str(s['pkA'])[0]}     {str(s['pkB'])[0]}    {s['sep']:.3f} {s['ncells_after_A']}->{s['ncells']}  "
              f"| {c['npeaks']}  {str(c['pkA'])[0]}    {str(c['pkB'])[0]}   | {h['npeaks']}  {str(h['pkB'])[0]}")
    print("")

    # ── I1 COEXISTENCE ──────────────────────────────────────────────────────
    # CP present at BOTH p_A and p_B on ALL 3 seeds + coherent peak near each + sep
    i1_seeds = []
    for i in range(len(SEEDS)):
        s = rec["AB_seq"][i]
        ok = (s["m_pA"] >= W1_MARGIN and s["m_pB"] >= W1_MARGIN and
              s["pkA"] and s["pkB"] and s["sep"] >= W2_PEAK_SEP)
        i1_seeds.append(ok)
    i1 = all(i1_seeds)
    mean_m_pA_seq = float(np.mean([r["m_pA"] for r in rec["AB_seq"]]))
    mean_m_pB_seq = float(np.mean([r["m_pB"] for r in rec["AB_seq"]]))
    mean_m_pA_aonly = float(np.mean([r["m_pA"] for r in rec["A_only"]]))
    print(f"  I1 COEXISTENCE (A->B CP present at BOTH p_A & p_B, all 3 seeds, sep>={W2_PEAK_SEP}):")
    print(f"     mean margin@p_A={mean_m_pA_seq:+.3f}  mean margin@p_B={mean_m_pB_seq:+.3f}  (bar {W1_MARGIN})")
    print(f"     A-only mean margin@p_A={mean_m_pA_aonly:+.3f}  (interference asymmetry: "
          f"seq@pA - Aonly@pA = {mean_m_pA_seq - mean_m_pA_aonly:+.3f})")
    print(f"     per-seed pass: {i1_seeds}   -> I1 {'PASS' if i1 else 'FAIL'}")

    # ── I2 NO-DOUBLE-ARTIFACT ───────────────────────────────────────────────
    # B=A control: peak-count <= LANG_MAX_PEAKS AND no coherent peak near p_B, all seeds
    i2_seeds = []
    for i in range(len(SEEDS)):
        c = rec["AA_ctrl"][i]
        ok = (c["npeaks"] <= LANG_MAX_PEAKS) and (not c["pkB"])
        i2_seeds.append(ok)
    i2 = all(i2_seeds)
    print(f"  I2 NO-DOUBLE-ARTIFACT (B=A control ONE peak <= {LANG_MAX_PEAKS} & NO peak near p_B):")
    print(f"     per-seed peak-counts: {[c['npeaks'] for c in rec['AA_ctrl']]}  "
          f"peak-near-p_B: {[c['pkB'] for c in rec['AA_ctrl']]}")
    print(f"     per-seed pass: {i2_seeds}   -> I2 {'PASS' if i2 else 'FAIL'}")

    # ── I3 EARNED (anti-Goodhart) ───────────────────────────────────────────
    # shuffle: total peak-count >= SHUF_MIN_PEAKS OR no coherent peak near p_B, all seeds
    i3_seeds = []
    for i in range(len(SEEDS)):
        h = rec["AB_shuf"][i]
        ok = (h["npeaks"] >= SHUF_MIN_PEAKS) or (not h["pkB"])
        i3_seeds.append(ok)
    i3 = all(i3_seeds)
    print(f"  I3 EARNED (SHUFFLE collapses: peak-count >= {SHUF_MIN_PEAKS} OR no coherent peak@p_B):")
    print(f"     per-seed peak-counts: {[h['npeaks'] for h in rec['AB_shuf']]}  "
          f"peak-near-p_B: {[h['pkB'] for h in rec['AB_shuf']]}")
    print(f"     per-seed pass: {i3_seeds}   -> I3 {'PASS' if i3 else 'FAIL'}")

    print("=" * 82)
    green = i1 and i2 and i3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — BILINGUAL COEXISTENCE.")
        print("  After learning language B on top of language A on the SAME grow-not-evict")
        print("  Voronoi substrate, categorical perception SURVIVES at BOTH boundaries: a")
        print("  coherent CP peak sits at p_A (A's cognition) AND at p_B (B's cognition),")
        print("  two distinct peaks. The B=A control yields ONE peak (no double-artifact) and")
        print("  the SHUFFLE arm produces no coherent second CP (earned). anima holds TWO")
        print("  language-warped cognitions SIMULTANEOUSLY — the mitosis growth-memory (H_1288")
        print("  grow-not-evict) PROTECTS language-cognition from catastrophic interference,")
        print("  connecting H_1288 growth-memory to H_1325 Whorfian CP. ENGINE-TRANSFER")
        print("  UNVERIFIED (DIRECTIONAL mirror). TOY synthetic continuum, 3 seeds; NO")
        print("  human-bilingualism claim (a_scale_honest_scope).")
        return 0
    if not i1:
        # distinguish overwrite vs partial
        pA_collapsed = mean_m_pA_seq < W1_MARGIN
        if pA_collapsed:
            print("VERDICT: 🧱 OVERWRITE / CATASTROPHIC INTERFERENCE — after B is learned, A's CP at")
            print("  p_A COLLAPSES (margin@p_A below bar). The second language overwrites the first's")
            print("  categorical perception; the growth-memory does NOT protect language-cognition.")
            print("  An honest, important NEGATIVE — reported straight, NO bar moved (c9).")
            return 2
        print("VERDICT: 🟠 GRADED INTERFERENCE — A's CP at p_A survives but weaker / a peak/sep bar")
        print("  did not fully clear on every seed. The asymmetry is reported straight (c9). NO bar")
        print("  moved. ENGINE-TRANSFER UNVERIFIED.")
        return 4
    if i1 and not (i2 and i3):
        print("VERDICT: 🧱 CONTROL FAIL — coexistence held (I1) but an anti-Goodhart control (I2 B=A")
        print("  double-artifact / I3 shuffle) did NOT separate. The two-peak result is not cleanly")
        print("  earned. Honest, NO bar move (c9).")
        return 1
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
