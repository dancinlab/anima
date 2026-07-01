"""
H_1325 — SAPIR-WHORF / LINGUISTIC RELATIVITY r2 — anti-Goodhart W3 RE-CLOSE.
R2 numpy MIRROR (DIRECTIONAL). Re-closes the H_1323 (🟠 PARTIAL, PR #2228) W3 leg
with a CORRECTLY-SPECIFIED control (peak COUNT, not peak HEIGHT).

Frozen design: .verdicts/1325_sapir_whorf_r2/H_1325_FREEZE.txt (pre-registered BEFORE
this scoring). NO tune-to-green (c9/p7). $0 CPU numpy, gradient-free, 3 seeds
[4323,4324,4325] (SAME as H_1323 so W1/W2 reproduce), p7.

THE MECHANISM (VoronoiCells, embed, build_labels, discrim_curve, the W1/W2 bars) is
REUSED VERBATIM from UNIVERSE/h1323_sapir_whorf.py — W1 and W2 PASSED there and are NOT
touched here. The ONLY change is the anti-Goodhart W3 leg:

WHY r2 (c16/a_break_the_wall = the control was the WRONG METHOD, not a wall):
  H_1323 W3 prominence sub-clause (shuffle single-peak height vs median < 0.5× language)
  FAILED because the shuffle arm is MULTI-PEAK (random per-stimulus labels → 8 scattered
  sharp spikes; the non-gating diagnostic measured 8.0 peaks vs 1.0 per language). A
  single one of those spikes is naturally as tall as a language's one coherent peak, so
  "single-peak height" is the WRONG observable. The honest anti-Goodhart question is
  COHERENCE: does the shuffle have ONE coherent CP peak (like a language) or MANY
  scattered ones (incoherent)? That is a PEAK-COUNT question, with a threshold from the
  STRUCTURE (1 boundary → ≤1 dominant peak; no boundary → ≥several), NOT from the data.

a_no_llm_frame_trap (cognitive-science / categorical-perception lens, c15) — NOT an LLM
recipe, NOT a human-cognition claim. ENGINE-TRANSFER UNVERIFIED until Part B (engine-
native re-score on the live CORE/engine_cli.hexa immune/Voronoi lane).
"""
import numpy as np

# ── frozen constants (REUSED VERBATIM from H_1323) ──────────────────────────
N_STIM   = 21
DIM      = 16
P_A      = 1.0 / 3.0
P_B      = 2.0 / 3.0
PAIR_STEP = 1
GROW_MAX = 24
SPLIT_PASSES = 24
SEEDS    = [4323, 4324, 4325]

# W1/W2 frozen bar thresholds (UNCHANGED from H_1323)
W1_MARGIN      = 0.15
W2_PEAK_TOL    = 0.12
W2_PEAK_SEP    = 0.20

# W3' frozen bar thresholds (NEW — peak-count coherence metric, from FREEZE)
PEAK_FRAC      = 0.50         # local-maximum height floor (fraction of arm's own peak)
LANG_MAX_PEAKS = 1            # a single boundary → AT MOST one coherent peak
SHUF_MIN_PEAKS = 3            # no coherent boundary → at least 3 scattered spikes
W3_LOC_STD     = 0.15         # retained (already PASSED H_1323) corroboration


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
    REUSED VERBATIM from H_1323."""

    def __init__(self):
        self.protos = []
        self.labels = []

    def _owner(self, key):
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        i = int(np.argmin(d))
        return i, d[i]

    def fit(self, X, Y, grow_max, passes):
        M = len(X)
        c0 = X.mean(axis=0)
        n = np.linalg.norm(c0)
        c0 = c0 / n if n > 0 else c0
        self.protos = [c0]
        seed_stim = int(np.argmin([float(np.linalg.norm(X[m] - c0)) for m in range(M)]))
        self.labels = [int(Y[seed_stim])]
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
        d = np.array([float(np.linalg.norm(p - key)) for p in self.protos])
        beta = 18.0
        w = np.exp(-beta * (d - d.min()))
        s = w.sum()
        w = w / s if s > 0 else w
        lab = np.array(self.labels, dtype=np.float64)
        return float((w * lab).sum())


def build_labels(positions, kind, rng):
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


def run_seed(seed):
    rng = np.random.default_rng(seed)
    basis = make_basis(seed)
    positions = np.linspace(0.0, 1.0, N_STIM)
    X = np.array([embed(x, basis) for x in positions])
    arms = {}
    for kind in ["none", "A", "B", "shuffle"]:
        lr = np.random.default_rng(seed + {"none": 1, "A": 2, "B": 3, "shuffle": 4}[kind])
        Y = build_labels(positions, kind, lr)
        cells = VoronoiCells().fit(X, Y, GROW_MAX, SPLIT_PASSES)
        mids, norm, raw = discrim_curve(cells, X, positions)
        arms[kind] = dict(mids=mids, norm=norm, raw=raw, ncells=len(cells.protos))
    return positions, arms


def peak_loc(mids, curve):
    return float(mids[int(np.argmax(curve))])


def within_cross_margin(mids, raw, boundary):
    near = np.abs(mids - boundary) <= 0.12
    far = np.abs(mids - boundary) >= 0.25
    cross = raw[near].mean() if near.any() else 0.0
    within = raw[far].mean() if far.any() else 0.0
    return cross, within


def count_peaks(curve, frac=PEAK_FRAC):
    """W3' COHERENCE METRIC (FROZEN): number of LOCAL MAXIMA of the normalized curve
    whose height >= frac of the arm's own peak. A "local maximum" is a bin strictly
    greater than BOTH immediate neighbors; endpoints count if they strictly exceed
    their single neighbor. A coherent language carving (1 boundary) → 1 peak; an
    incoherent shuffle (no boundary) → many scattered peaks. Strict-local-maximum so a
    monotone shoulder does NOT over-count (the diagnostic-to-gating promotion)."""
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
        left_ok = (t == 0) or (c[t] > c[t - 1])
        right_ok = (t == n - 1) or (c[t] > c[t + 1])
        # an interior bin must strictly exceed BOTH neighbors; an endpoint its one neighbor
        if t == 0:
            is_max = c[t] > c[t + 1]
        elif t == n - 1:
            is_max = c[t] > c[t - 1]
        else:
            is_max = left_ok and right_ok
        if is_max:
            cnt += 1
    return cnt


def main():
    print("H_1325 R2 — SAPIR-WHORF / LINGUISTIC RELATIVITY — anti-Goodhart W3 RE-CLOSE")
    print("=" * 82)
    print("re-closes H_1323 (🟠) W3 with peak-COUNT coherence (not peak-HEIGHT prominence)")
    print(f"N_stim={N_STIM} dim={DIM} p_A={P_A:.3f} p_B={P_B:.3f} grow_max={GROW_MAX} seeds={SEEDS}")
    print(f"W3' frozen: PEAK_FRAC={PEAK_FRAC} LANG_MAX_PEAKS={LANG_MAX_PEAKS} SHUF_MIN_PEAKS={SHUF_MIN_PEAKS}")
    print("")

    acc = {k: [] for k in ["none", "A", "B", "shuffle"]}
    peak_locs = {k: [] for k in ["none", "A", "B", "shuffle"]}
    peak_cnts = {k: [] for k in ["none", "A", "B", "shuffle"]}
    mids_ref = None
    cross_within = {"A": [], "B": []}
    base_at_peak = {"A": [], "B": []}

    for seed in SEEDS:
        positions, arms = run_seed(seed)
        mids_ref = arms["A"]["mids"]
        for k in acc:
            acc[k].append(arms[k]["norm"])
            peak_locs[k].append(peak_loc(arms[k]["mids"], arms[k]["norm"]))
            peak_cnts[k].append(count_peaks(arms[k]["norm"]))
        for lang, p in [("A", P_A), ("B", P_B)]:
            cr, wi = within_cross_margin(arms[lang]["mids"], arms[lang]["raw"], p)
            cross_within[lang].append(cr - wi)
            pk_i = int(np.argmax(arms[lang]["norm"]))
            base_at_peak[lang].append(arms[lang]["raw"][pk_i] - arms["none"]["raw"][pk_i])

    mean_curve = {k: np.mean(np.array(acc[k]), axis=0) for k in acc}
    pl_mean = {k: float(np.mean(peak_locs[k])) for k in peak_locs}
    pl_std = {k: float(np.std(peak_locs[k])) for k in peak_locs}
    pc_mean = {k: float(np.mean(peak_cnts[k])) for k in peak_cnts}

    print("  CP peak location (mean argmax ± std over seeds):")
    print(f"    PRE-LANG: {pl_mean['none']:.3f} ± {pl_std['none']:.3f}")
    print(f"    L_A:      {pl_mean['A']:.3f} ± {pl_std['A']:.3f}    (p_A={P_A:.3f})")
    print(f"    L_B:      {pl_mean['B']:.3f} ± {pl_std['B']:.3f}    (p_B={P_B:.3f})")
    print(f"    SHUFFLE:  {pl_mean['shuffle']:.3f} ± {pl_std['shuffle']:.3f}")
    print("")

    # ── W1 CP PRESENT (UNCHANGED) ──────────────────────────────────────────
    cw_A = float(np.mean(cross_within["A"]))
    cw_B = float(np.mean(cross_within["B"]))
    bvp_A = float(np.mean(base_at_peak["A"]))
    bvp_B = float(np.mean(base_at_peak["B"]))
    w1 = (cw_A >= W1_MARGIN and cw_B >= W1_MARGIN and
          bvp_A >= W1_MARGIN and bvp_B >= W1_MARGIN)
    print(f"  W1 CP PRESENT (cross-within>=%.2f & lang-vs-baseline@peak>=%.2f):" % (W1_MARGIN, W1_MARGIN))
    print(f"     L_A cross-within={cw_A:+.3f}  vs-baseline={bvp_A:+.3f}")
    print(f"     L_B cross-within={cw_B:+.3f}  vs-baseline={bvp_B:+.3f}   -> {'PASS' if w1 else 'FAIL'}")

    # ── W2 WHORFIAN DISSOCIATION (UNCHANGED) ───────────────────────────────
    locA_ok = abs(pl_mean["A"] - P_A) <= W2_PEAK_TOL
    locB_ok = abs(pl_mean["B"] - P_B) <= W2_PEAK_TOL
    sep = abs(pl_mean["A"] - pl_mean["B"])
    w2 = locA_ok and locB_ok and sep >= W2_PEAK_SEP
    print(f"  W2 WHORFIAN DISSOC (|locA-p_A|<=%.2f & |locB-p_B|<=%.2f & |locA-locB|>=%.2f):"
          % (W2_PEAK_TOL, W2_PEAK_TOL, W2_PEAK_SEP))
    print(f"     |locA-p_A|={abs(pl_mean['A']-P_A):.3f}  |locB-p_B|={abs(pl_mean['B']-P_B):.3f}"
          f"  sep={sep:.3f}   -> {'PASS' if w2 else 'FAIL'}")

    # ── W3' EARNED (anti-Goodhart, RE-CLOSED with peak COUNT) ───────────────
    pcA = pc_mean["A"]
    pcB = pc_mean["B"]
    pcSh = pc_mean["shuffle"]
    pcNone = pc_mean["none"]
    w3a = (pcA <= LANG_MAX_PEAKS) and (pcB <= LANG_MAX_PEAKS)
    w3b = pcSh >= SHUF_MIN_PEAKS
    w3_locstd = pl_std["shuffle"] >= W3_LOC_STD     # retained corroboration (non-gating)
    w3 = w3a and w3b
    print(f"  W3' COHERENCE peak-count (LANG<=%d coherent & SHUFFLE>=%d incoherent):"
          % (LANG_MAX_PEAKS, SHUF_MIN_PEAKS))
    print(f"     peak-count: L_A={pcA:.1f}  L_B={pcB:.1f}  PRE-LANG={pcNone:.1f}  SHUFFLE={pcSh:.1f}")
    print(f"       (a) languages coherent (<=%d): {'PASS' if w3a else 'FAIL'}"
          % LANG_MAX_PEAKS)
    print(f"       (b) shuffle incoherent (>=%d): {'PASS' if w3b else 'FAIL'}   -> W3' {'PASS' if w3 else 'FAIL'}"
          % SHUF_MIN_PEAKS)
    print(f"     [retained corroboration] shuffle loc-std={pl_std['shuffle']:.3f}"
          f" >= {W3_LOC_STD}: {'PASS' if w3_locstd else 'FAIL'} (non-gating)")

    print("=" * 82)
    green = w1 and w2 and w3
    if green:
        print("VERDICT: 🟢 GREEN (MIRROR, DIRECTIONAL) — LINGUISTIC RELATIVITY ANTI-GOODHART-CLOSED.")
        print("  W1 (CP present) ✅, W2 (Whorfian dissociation — peak tracks the language) ✅,")
        print("  W3' (coherence): the languages each have ONE coherent CP peak while the SHUFFLE")
        print("  arm is an INCOHERENT scatter of many spikes (NOT a single coherent CP peak) ✅.")
        print("  The mis-specified single-peak-height control (H_1323 W3) is REPLACED by the")
        print("  correctly-specified peak-COUNT coherence control (frozen anew, NOT a relaxation).")
        print("  ENGINE-TRANSFER UNVERIFIED until Part B (live CORE/engine_cli.hexa immune lane).")
        print("  TOY synthetic continuum, 3 seeds; NO human-cognition claim (a_scale_honest_scope).")
        return 0
    if w1 and w2 and not w3:
        print("VERDICT: 🟠 W3' UNRESOLVED — W1∧W2 HOLD (relativity decisive) but the peak-count")
        print("  coherence control did NOT separate shuffle from coherent CP (or a language split).")
        print("  HONEST (c9): the relativity result rests on W1+W2 alone, W3 unresolved. NO further")
        print("  re-specification — one honest new control, verdict accepted. ENGINE-TRANSFER UNVERIFIED.")
        return 4
    if w1 and not w2:
        print("VERDICT: 🔵 UNIVERSALIST (Whorf REFUTED) — CP present, location language-INDEPENDENT.")
        return 2
    if not w1:
        print("VERDICT: 🧱 NO CP — the substrate does NOT categorically perceive (W1 fails).")
        return 3
    print("VERDICT: 🧱 CLOSED-NEGATIVE — a frozen bar failed. Honest, NO bar move (c9).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
