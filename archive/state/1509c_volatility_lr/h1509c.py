#!/usr/bin/env python3
"""H_1509c VOLATILITY-GATED LEARNING RATE — R1 numpy mirror (DIRECTIONAL).

SOURCE: anima-internal ESCAPE from the Amoeba-Protocol thread (μ_t buffer, H_1509/H_1509b).
Mechanism-family ESCAPE per the peeled meta-law (H_1509c_ABSTRACT_census.txt):
  "a tuned FIXED gain dominates state-contingent adaptation WHEN task statistics are
   stationary/learnable — adaptation pays ONLY when the disturbance is UNPREDICTABLE
   (changepoints/volatility)."
The escape: reposition neuromodulation from a TRACKING-GAIN to a LEARNING-RATE modulator
on a CHANGEPOINT task whose statistics JUMP (Yu&Dayan 2005; Behrens et al. 2007).

FROZEN BARS: state/verdicts/1509c_volatility_lr/H_1509c_FREEZE.txt (MARGIN=0.05, hazards
[0,0.02,0.05,0.10], NO tune-to-green). $0 CPU, deterministic, p7, c9.
"""
import math

# ── frozen parameters (pre-registered in FREEZE) ──────────────────────────────
T          = 300
NOISE_HALF = 0.10                 # observation noise ε ~ uniform[-0.10,+0.10]
JUMP_LO, JUMP_HI = 0.15, 0.85     # hidden mean jump target range
A_GRID     = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.70, 0.90]
A_LO, A_HI = 0.05, 0.90           # gate endpoints (= grid endpoints, NOT tuned)
S_SCALE    = 0.30                 # surprise scale (frozen)
MARGIN     = 0.05
SEEDS      = [1509, 1510, 1511]
HAZARDS    = [0.00, 0.02, 0.05, 0.10]


def _clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else (hi if x > hi else x)


def _lcg(state):
    state = (state * 1103515245 + 12345) & 2147483647
    return state, (state / 2147483647.0)


def _gen_world(seed, hazard):
    """Deterministic hidden-mean + observation stream. The hidden mean h_t JUMPS with
    probability `hazard` each tick (changepoint), else holds; o_t = h_t + noise.
    hazard=0 → a single fixed mean (stationary learnable task). Returns (hs, os)."""
    st = (seed * 2246822519 + 3266489917) & 2147483647
    h = 0.5
    hs = []
    os = []
    for _ in range(T):
        st, r_jump = _lcg(st)
        if r_jump < hazard:
            st, r_new = _lcg(st)
            h = JUMP_LO + (JUMP_HI - JUMP_LO) * r_new
        hs.append(h)
        st, r_noise = _lcg(st)
        noise = (r_noise * 2.0 - 1.0) * NOISE_HALF
        os.append(_clamp(h + noise))
    return hs, os


def run_arm(mode, alpha, seed, hazard):
    """Delta-rule estimator x_{t+1}=x_t+α_t·(o_t−x_t) tracking the jumping hidden mean.
    mode 'fixed' : α_t = alpha (FIXED-rate arm A / ablate-base)
    mode 'gated' : α_t = α_lo+(α_hi−α_lo)·u_t, u_t = clamp(|o−x|/S,0,1) surprise (arm B)
    mode 'ablate': α_t = (α_lo+α_hi)/2 fixed (arm C)
    Returns RMS estimation error sqrt(mean (x−h)²). Same world stream per (seed,hazard)."""
    hs, os = _gen_world(seed, hazard)
    x = 0.5
    sq = 0.0
    amid = 0.5 * (A_LO + A_HI)
    for t in range(T):
        o = os[t]
        err = o - x
        if mode == "fixed":
            a = alpha
        elif mode == "gated":
            u = _clamp(abs(err) / S_SCALE, 0.0, 1.0)   # surprise from OWN pred-error
            a = A_LO + (A_HI - A_LO) * u
        elif mode == "ablate":
            a = amid
        else:
            raise ValueError(mode)
        x = _clamp(x + a * err)
        d = x - hs[t]
        sq += d * d
    return math.sqrt(sq / T)


def best_fixed_rate(seed, hazard):
    """ARM A: sweep the α grid, return the LOWEST RMS (strongest fixed baseline)."""
    best = None; ba = None
    for a in A_GRID:
        r = run_arm("fixed", a, seed, hazard)
        if best is None or r < best:
            best, ba = r, a
    return ba, best


def main():
    print("H_1509c VOLATILITY-GATED LEARNING RATE — R1 numpy mirror (DIRECTIONAL)")
    print("ESCAPE (anima-internal) from Amoeba-thread; meta-law: adaptation pays iff VOLATILE")
    print(f"FROZEN MARGIN={MARGIN} α_lo={A_LO} α_hi={A_HI} S={S_SCALE} hazards={HAZARDS}")
    print("=" * 76)

    A = {}; B = {}; C = {}; A_each = {}; B_each = {}; bestA_alpha = {}
    for H in HAZARDS:
        ra = {}; rb = {}; rc = {}
        for s in SEEDS:
            ba, va = best_fixed_rate(s, H)
            ra[s] = va; bestA_alpha[(H, s)] = ba
            rb[s] = run_arm("gated", 0.0, s, H)
            rc[s] = run_arm("ablate", 0.0, s, H)
        A[H] = sum(ra.values()) / 3; B[H] = sum(rb.values()) / 3; C[H] = sum(rc.values()) / 3
        A_each[H] = ra; B_each[H] = rb

    chk1 = run_arm("gated", 0.0, SEEDS[0], 0.10)
    chk2 = run_arm("gated", 0.0, SEEDS[0], 0.10)
    det = "PASS" if chk1 == chk2 else "FAIL"

    print(f"\n{'hazard':>7} {'A.best_a':>9} {'RMS_A':>9} {'RMS_B':>9} {'RMS_C':>9} {'adv=A-B':>9}")
    for H in HAZARDS:
        a_alpha = bestA_alpha[(H, SEEDS[0])]
        print(f"{H:>7.2f} {a_alpha:>9.2f} {A[H]:>9.4f} {B[H]:>9.4f} {C[H]:>9.4f} {A[H]-B[H]:>+9.4f}")
    print(f"\ndeterminism run1==run2: {det} ({chk1:.6f})")

    # ── frozen bars ──
    H_hi = 0.10; H_lo = 0.00
    a_mean = (A[H_hi] - B[H_hi]) >= MARGIN
    a_each = all((A_each[H_hi][s] - B_each[H_hi][s]) >= MARGIN for s in SEEDS)
    barA = a_mean and a_each
    barB = (A[H_lo] <= B[H_lo]) and ((A[H_hi] - B[H_hi]) >= MARGIN)
    adv = {H: A[H] - B[H] for H in HAZARDS}
    barC = (adv[0.02] <= adv[0.05] <= adv[0.10]) and (adv[0.10] > adv[0.00])
    d_noWin = all((C[H] - A[H]) >= -0.02 for H in HAZARDS)
    d_gate = (C[H_hi] - B[H_hi]) >= MARGIN
    barD = d_noWin and d_gate

    print("\nFROZEN BAR EVALUATION (MARGIN=0.05, no tune-to-green):")
    print(f"  (A ESCAPE-WIN @H=0.10) A−B={A[H_hi]-B[H_hi]:+.4f} >= {MARGIN} "
          f"mean={'PASS' if a_mean else 'FAIL'} each={'PASS' if a_each else 'FAIL'} "
          f"=> {'PASS' if barA else 'FAIL'}")
    print(f"  (B DOUBLE-DISSOC) H=0 A<=B {'PASS' if A[H_lo]<=B[H_lo] else 'FAIL'} "
          f"(A={A[H_lo]:.4f} B={B[H_lo]:.4f}) AND H=0.10 A−B>={MARGIN} "
          f"{'PASS' if (A[H_hi]-B[H_hi])>=MARGIN else 'FAIL'} => {'PASS' if barB else 'FAIL'}")
    print(f"  (C VOLATILITY-MONOTONE) adv {adv[0.0]:+.4f}→{adv[0.02]:+.4f}→{adv[0.05]:+.4f}"
          f"→{adv[0.10]:+.4f} => {'PASS' if barC else 'FAIL'}")
    print(f"  (D EARNED ablate) ablate-never-wins={'PASS' if d_noWin else 'FAIL'} AND "
          f"gate>ablate@0.10 C−B={C[H_hi]-B[H_hi]:+.4f}>={MARGIN} "
          f"{'PASS' if d_gate else 'FAIL'} => {'PASS' if barD else 'FAIL'}")

    green = barA and barB and barC and barD and det == "PASS"
    print("\n" + "=" * 76)
    if green:
        print("VERDICT: 🟢 WALL-BROKEN (ORTHOGONAL-FAMILY ESCAPE) — the uncertainty-gated")
        print("         learning rate BEATS the best fixed rate on a VOLATILE changepoint task")
        print("         (loses on the stationary task), MONOTONE in volatility, EARNED by the")
        print("         gate. The meta-law's escape clause is CONFIRMED: adaptation pays iff volatile.")
    else:
        print("VERDICT: 🧱 MULTI-FAMILY WALL — the orthogonal learning-rate family ALSO fails")
        print("         to beat the best fixed rate → the neuromodulation ceiling holds across")
        print("         BOTH the tracking-gain AND learning-rate families (meta-law incomplete). c9.")
        for nm, ok in [("A", barA), ("B", barB), ("C", barC), ("D", barD)]:
            if not ok:
                print(f"           - bar {nm} FAILED")
    print("=" * 76)
    return green


if __name__ == "__main__":
    main()
