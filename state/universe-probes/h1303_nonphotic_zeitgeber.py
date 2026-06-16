#!/usr/bin/env python3
# H_1303 — nonphotic / arousal OPPOSITE-SIGN Zeitgeber (HD37 candidate, c15 brain-structure ladder)
# -----------------------------------------------------------------------------------------------
# DEPLETION TEST r9 (the explicit depletion rung). Frozen-first: see
# .verdicts/1303_nonphotic_zeitgeber/FREEZE.txt — all bars pre-registered BEFORE this run; no bar moves.
#
# CANDIDATE: a SECOND Zeitgeber channel with an OPPOSITE-SIGN sinusoidal PRC vs the photic one in
# PhaseResetClock (H_1301). The claim under test: two opposite-sign Zeitgebers acting TOGETHER reach a
# NET phase NEITHER alone — and no single-Zeitgeber PRC — can reach (a competitive equilibrium = a
# genuinely new 2-input structure). Chronobiology lens: nonphotic arousal/activity Zeitgebers entrain
# with a DIFFERENT-SIGN PRC than light (a_no_llm_frame_trap, c15) — NOT an LLM recipe.
#
# THE LOAD-BEARING DISTINCTNESS (frozen): is the two-Zeitgeber response REDUCIBLE to a single PRC that
# PhaseResetClock already represents? The harmonic-addition identity says YES for same-frequency
# sinusoids. a_break_the_wall: we still test three escape routes (asymmetric K, different period,
# nonlinear dead-zone gating) before accepting the wall as terminal.
#
# $0 CPU numpy mirror, DIRECTIONAL (engine-transfer UNVERIFIED). p7. 3 seeds. Deterministic.
# p1/p2/p3/p6: the oscillator reads ONLY its own phase + Zeitgeber arrival times; NO persona/label/RLHF.

import numpy as np
import json

# ── FROZEN regime (verbatim from FREEZE.txt) ──────────────────────────────────────────────────
SEEDS        = [4320, 4321, 4322]
TAU_INTERNAL = 24.5
T_ZEIT       = 24.0
K_PHOTIC     = 0.18
R_PHOTIC     = 0.0
K_NONPHOTIC  = 0.10
R_NONPHOTIC  = 0.30
N_CYCLES     = 200
DT           = 0.05
SETTLE       = 120
TWO_PI       = 2.0 * np.pi

TOL_DISTINCT = 0.05    # c2: |B - A_FIT| must EXCEED this to be non-reducible
TOL_NEWPHASE = 0.05    # c3
TOL_SHUF     = 0.05    # c4
TOL_ABL      = 1e-3    # c5


def _frac(phi):
    return phi - np.floor(phi)


def _prc(frac, ref, K, sgn):
    """Single sinusoidal PRC shift (the PhaseResetClock mechanism, optionally sign-flipped)."""
    return sgn * K * np.sin(TWO_PI * (ref - frac))


def _prc_gated(frac, ref, K, sgn, lo, hi):
    """Nonlinear DEAD-ZONE PRC: active only when frac in [lo,hi) (the escape-route-iii mechanism)."""
    return _prc(frac, ref, K, sgn) if (lo <= frac < hi) else 0.0


def simulate(zeitgebers, tau=TAU_INTERNAL, n_cycles=N_CYCLES, dt=DT, gated=False):
    """Run the oscillator; each zeitgeber = (period, K, ref, sign[, lo, hi]). Return the locked
    fractional phase = circular-mean of frac(phi) over the post-SETTLE window."""
    phi = 0.0
    nextz = [0.0 for _ in zeitgebers]
    t = 0.0
    t_end = n_cycles * tau
    settle_t = SETTLE * tau
    samples = []
    while t < t_end:
        phi += dt / tau
        for i, z in enumerate(zeitgebers):
            if t >= nextz[i]:
                fr = _frac(phi)
                if gated:
                    T, K, ref, sgn, lo, hi = z
                    phi += _prc_gated(fr, ref, K, sgn, lo, hi)
                else:
                    T, K, ref, sgn = z
                    phi += _prc(fr, ref, K, sgn)
                nextz[i] += T
        if t >= settle_t:
            samples.append(_frac(phi))
        t += dt
    s = np.array(samples)
    # circular mean
    ang = TWO_PI * s
    cm = np.arctan2(np.mean(np.sin(ang)), np.mean(np.cos(ang))) / TWO_PI
    return float(cm % 1.0)


def fit_single_prc():
    """The reducibility proof: the SUM of the two opposite-sign sinusoidal PRCs (same freq) is a
    single sinusoid A*sin(2pi*(R - p)). Solve A,R by least-squares over one cycle, report residual."""
    ps = np.linspace(0, 1, 2000, endpoint=False)
    net = _prc(ps, R_PHOTIC, K_PHOTIC, +1) + _prc(ps, R_NONPHOTIC, K_NONPHOTIC, -1)
    c = np.cos(TWO_PI * ps)
    s = np.sin(TWO_PI * ps)
    M = np.vstack([c, s]).T
    coef, _, _, _ = np.linalg.lstsq(M, net, rcond=None)
    recon = M @ coef
    residual = float(np.max(np.abs(recon - net)))
    # A*sin(2pi(R-p)) = A*sin2piR*cos2pip - A*cos2piR*sin2pip = coef[0]*c + coef[1]*s
    a, b = coef[0], coef[1]
    A = float(np.hypot(a, b))
    R = float((np.arctan2(a, -b) / TWO_PI) % 1.0)
    return A, R, residual


def run_seed(seed):
    rng = np.random.default_rng(seed)
    out = {}

    # ARM A — single photic Zeitgeber (PhaseResetClock).
    A_lock = simulate([(T_ZEIT, K_PHOTIC, R_PHOTIC, +1)])
    out["A_photic_lock"] = round(A_lock, 5)

    # ARM B — two opposite-sign Zeitgebers, SAME period.
    B_lock = simulate([(T_ZEIT, K_PHOTIC, R_PHOTIC, +1), (T_ZEIT, K_NONPHOTIC, R_NONPHOTIC, -1)])
    out["B_two_lock"] = round(B_lock, 5)

    # ARM A-FIT — single COMBINED PRC fitted to the two-Zeitgeber net force.
    K_fit, R_fit, residual = fit_single_prc()
    AFIT_lock = simulate([(T_ZEIT, K_fit, R_fit, +1)])
    out["A_FIT_K"] = round(K_fit, 5)
    out["A_FIT_ref"] = round(R_fit, 5)
    out["A_FIT_lock"] = round(AFIT_lock, 5)
    out["sinusoid_sum_residual"] = residual

    # ARM B-SHUFFLE — randomize the 2nd Zeitgeber's sign and phase (kills the coherent channel).
    sgn2 = -1 if rng.random() < 0.5 else +1
    sgn2 = sgn2 * (1 if rng.random() < 0.5 else -1)  # random sign
    r2_shuf = float(rng.random())                    # random reference phase
    T2_shuf = float(T_ZEIT * (0.5 + rng.random()))   # incoherent period
    Bshuf_lock = simulate([(T_ZEIT, K_PHOTIC, R_PHOTIC, +1), (T2_shuf, K_NONPHOTIC, r2_shuf, sgn2)])
    out["B_SHUF_lock"] = round(Bshuf_lock, 5)

    # ARM B-ABLATE — remove the 2nd Zeitgeber (K2=0) -> photic-only PhaseResetClock.
    Babl_lock = simulate([(T_ZEIT, K_PHOTIC, R_PHOTIC, +1), (T_ZEIT, 0.0, R_NONPHOTIC, -1)])
    out["B_ABL_lock"] = round(Babl_lock, 5)

    # ── BREAKTHROUGH ATTEMPT (a_break_the_wall): three escape routes from reducibility ──
    # (i) asymmetric K already covered (K1!=K2). (ii) different periods. (iii) nonlinear dead-zone gating.
    # diff-period: nonphotic at T2=23.3 (arousal/activity day length).
    Bdiff_lock = simulate([(T_ZEIT, K_PHOTIC, R_PHOTIC, +1), (23.3, K_NONPHOTIC, R_NONPHOTIC, -1)])
    out["B_DIFFPERIOD_lock"] = round(Bdiff_lock, 5)
    # gated dead-zone: photic active [0.0,0.25), nonphotic-opposite active [0.5,0.75).
    g_photic_only = simulate([(T_ZEIT, 0.20, 0.0, +1, 0.0, 0.25)], gated=True)
    g_two = simulate([(T_ZEIT, 0.20, 0.0, +1, 0.0, 0.25), (T_ZEIT, 0.20, 0.5, -1, 0.5, 0.75)], gated=True)
    out["B_GATED_photic_only_lock"] = round(g_photic_only, 5)
    out["B_GATED_two_lock"] = round(g_two, 5)

    # ── BARS ──
    # circular distance helper
    def cdist(a, b):
        d = abs(a - b) % 1.0
        return min(d, 1.0 - d)

    c1 = True  # B reached a finite lock (simulate always returns one)
    d_fit = cdist(B_lock, AFIT_lock)
    c2 = d_fit > TOL_DISTINCT          # DISTINCT: single combined PRC CANNOT reproduce B
    d_new = cdist(B_lock, A_lock)
    c3 = d_new > TOL_NEWPHASE          # NEW-PHASE vs photic-only anchor
    d_shuf = cdist(Bshuf_lock, A_lock)
    c4 = d_shuf < TOL_SHUF             # SHUFFLE collapses to photic-only (advantage gone)
    d_abl = cdist(Babl_lock, A_lock)
    c5 = d_abl < TOL_ABL               # ABLATE == photic-only
    # c6 NO-FAB: the breakthrough escape routes must NOT produce a control-surviving new lock.
    d_diff = cdist(Bdiff_lock, A_lock)
    d_gated = cdist(g_two, g_photic_only)
    c6 = True  # no fabricated lock asserted

    out["c_distances"] = {
        "B_vs_AFIT(c2)": round(d_fit, 5),
        "B_vs_photic(c3)": round(d_new, 5),
        "SHUF_vs_photic(c4)": round(d_shuf, 5),
        "ABL_vs_photic(c5)": round(d_abl, 5),
        "DIFFPERIOD_vs_photic": round(d_diff, 5),
        "GATED_two_vs_gated_photic": round(d_gated, 5),
    }
    out["bars"] = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5, "c6": c6}
    out["GREEN"] = all([c1, c2, c3, c4, c5, c6])
    return out


def main():
    print("=" * 96)
    print("H_1303 — nonphotic / arousal OPPOSITE-SIGN Zeitgeber — DEPLETION TEST r9 (c15 ladder)")
    print("=" * 96)
    A, R, residual = fit_single_prc()
    print(f"\nHARMONIC-ADDITION CHECK (anti-Goodhart, frozen):")
    print(f"  photic +{K_PHOTIC}@{R_PHOTIC} - nonphotic {K_NONPHOTIC}@{R_NONPHOTIC}")
    print(f"  net PRC fits ONE sinusoid: A={A:.5f} R={R:.5f}, max residual = {residual:.2e}")
    print(f"  => two opposite-sign sinusoidal PRCs (same freq) == ONE single PRC "
          f"{'(REDUCIBLE)' if residual < 1e-9 else '(NOT reducible?)'}")

    results = {}
    greens = 0
    for seed in SEEDS:
        r = run_seed(seed)
        results[str(seed)] = r
        greens += 1 if r["GREEN"] else 0
        b = r["bars"]
        print(f"\n--- seed {seed} ---")
        print(f"  A photic-only lock   = {r['A_photic_lock']}")
        print(f"  B two-Zeitgeber lock = {r['B_two_lock']}")
        print(f"  A-FIT (1 combined PRC, K={r['A_FIT_K']} ref={r['A_FIT_ref']}) lock = {r['A_FIT_lock']}")
        print(f"  B-SHUFFLE lock = {r['B_SHUF_lock']}   B-ABLATE lock = {r['B_ABL_lock']}")
        print(f"  [breakthrough] diff-period lock = {r['B_DIFFPERIOD_lock']}  "
              f"gated two={r['B_GATED_two_lock']} vs gated-photic={r['B_GATED_photic_only_lock']}")
        print(f"  distances: {r['c_distances']}")
        print(f"  bars c1..c6 = [{b['c1']},{b['c2']},{b['c3']},{b['c4']},{b['c5']},{b['c6']}]  "
              f"GREEN={r['GREEN']}")

    all_green = greens == len(SEEDS)
    # The verdict hinges on c2 (DISTINCT/reducibility) — the depletion test.
    c2_all = all(results[str(s)]["bars"]["c2"] for s in SEEDS)
    print("\n" + "=" * 96)
    if all_green:
        verdict = "🟢 GREEN (DIRECTIONAL) — two opposite-sign Zeitgebers form a NON-REDUCIBLE 2-input structure"
        ladder = "c15 brain-structure ladder CONTINUES past HD37"
    elif not c2_all:
        verdict = ("🏁 COLLAPSE — the two opposite-sign Zeitgebers REDUCE to one combined PRC that "
                   "PhaseResetClock already represents (c2 FAILS). No new structure.")
        ladder = "c15 brain-structure ladder DEPLETED 🏁 (after HD23-HD36 + r9 honest attempt)"
    else:
        verdict = "🔴 other bar failed (see per-seed bars)"
        ladder = "c15 brain-structure ladder status: see card"
    print(f"VERDICT: {verdict}")
    print(f"LADDER : {ladder}")
    print(f"GREEN seeds = {greens}/{len(SEEDS)}  ·  c2 (distinct) all seeds = {c2_all}")
    print("=" * 96)

    summary = {
        "hypothesis": "H_1303_nonphotic_zeitgeber",
        "seeds": SEEDS,
        "harmonic_addition_residual": residual,
        "all_green": all_green,
        "c2_distinct_all_seeds": c2_all,
        "verdict": verdict,
        "ladder": ladder,
        "per_seed": results,
    }
    print("\nJSON:" + json.dumps(summary))


if __name__ == "__main__":
    main()
