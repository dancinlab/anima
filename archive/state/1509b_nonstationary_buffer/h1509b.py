#!/usr/bin/env python3
"""H_1509b NON-STATIONARY ALLOSTERIC-BUFFER — R1 numpy mirror (DIRECTIONAL).

SOURCE: external proposal — Amoeba Protocol (@qingkong66) μ_t allosteric buffer.
FOLLOW-ON to H_1509 (🧱 WALL-HELD stationary, PR #2484). a_break_the_wall (b):
isolate the stationarity variable. HYPOTHESIS: in a NON-STATIONARY environment where
the regulated target m_t DRIFTS, the allosteric μ_t beats the best-swept FIXED gain
(it LOST in the stationary case, B−A=−0.0061). MECHANISM: a fixed gain pulls toward a
stale center and cannot track a moving setpoint; the buffer re-tightens resistance to
deviation as the target moves.

FROZEN BARS: state/verdicts/1509b_nonstationary_buffer/H_1509b_FREEZE.txt (MARGIN=0.05,
drift levels [0,0.01,0.02,0.03], NO tune-to-green). $0 CPU, deterministic, p7, c9.
"""
import math

# ── frozen parameters (pre-registered in FREEZE) ──────────────────────────────
T          = 200
DRIVE_AMP  = 0.30
DRIVE_PER  = 17
SHOCK_T    = 100
SHOCK_LEN  = 20
SHOCK_AMP  = 0.35
G_GRID     = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
G0         = 0.40
LAMBDA     = 1.0
SIGMA      = 0.12
MARGIN     = 0.05
SEEDS      = [1509, 1510, 1511]
DRIFTS     = [0.000, 0.010, 0.020, 0.030]   # 0.0 = H_1509 stationary baseline
M_LO, M_HI = 0.15, 0.85                     # target drift clamp


def _clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else (hi if x > hi else x)


def _lcg(state):
    state = (state * 1103515245 + 12345) & 2147483647
    return state, (state / 2147483647.0)


def _drive(t, phase):
    d = DRIVE_AMP * math.sin(2.0 * math.pi * (t + phase) / DRIVE_PER)
    if SHOCK_T <= t < SHOCK_T + SHOCK_LEN:
        d = d + SHOCK_AMP
    return d


def _mu(b, m, lam=LAMBDA, sigma=SIGMA):
    """buffer reads the deviation from the CURRENT (possibly moving) target m."""
    dev2 = (b - m) ** 2
    return 1.0 + lam * (1.0 - math.exp(-dev2 / (2.0 * sigma * sigma)))


def _target_walk(seed, drift_rate):
    """deterministic target sequence m_t: random-walk ±1 steps scaled by drift_rate.
    drift_rate=0 → m_t ≡ 0.5 EXACTLY (the H_1509 stationary environment)."""
    m = 0.5
    seq = []
    # target uses an INDEPENDENT LCG stream (seed-derived) so it's identical across arms
    st = (seed * 40503 + 12345) & 2147483647
    for _ in range(T):
        seq.append(m)
        st, r = _lcg(st)
        step = 1.0 if r >= 0.5 else -1.0
        m = _clamp(m + drift_rate * step, M_LO, M_HI)
    return seq


def run_arm(mode, g, seed, drift_rate, lam=LAMBDA):
    """Roll b_t for T ticks tracking the (drifting) target m_t.
    mode 'gain' : restoring = g·(m−b)        (fixed-gain lever, ARM A/C base)
    mode 'allo' : restoring = g·μ(b,m)·(m−b)  (ARM B; ablate via lam=0 == ARM C)
    Returns RMS tracking error sqrt(mean (b−m)²)."""
    mseq = _target_walk(seed, drift_rate)
    st = seed & 2147483647
    phase = (seed % DRIVE_PER)
    b = 0.5
    sq = 0.0
    for t in range(T):
        st, noise = _lcg(st)
        noise = (noise - 0.5) * 0.02
        d = _drive(t, phase) + noise
        m = mseq[t]
        if mode == "gain":
            mu = 1.0
        elif mode == "allo":
            mu = _mu(b, m, lam)
        else:
            raise ValueError(mode)
        restoring = g * mu * (m - b)
        b = _clamp(b + d + restoring)
        e = b - m
        sq += e * e
    return math.sqrt(sq / T)


def best_fixed_gain(seed, drift_rate):
    """ARM A: sweep the grid, return the LOWEST RMS (strongest fixed baseline)."""
    best = None
    bg = None
    for g in G_GRID:
        r = run_arm("gain", g, seed, drift_rate)
        if best is None or r < best:
            best, bg = r, g
    return bg, best


def main():
    print("H_1509b NON-STATIONARY ALLOSTERIC-BUFFER — R1 numpy mirror (DIRECTIONAL)")
    print("SOURCE: external proposal — Amoeba Protocol (μ_t allosteric buffer)")
    print(f"FROZEN MARGIN={MARGIN} λ={LAMBDA} σ={SIGMA} g0={G0} drifts={DRIFTS}")
    print("=" * 74)

    # per drift level: mean RMS_A (best fixed), RMS_B (allo), RMS_C (ablate)
    A = {}; B = {}; C = {}; A_each = {}; B_each = {}
    for d in DRIFTS:
        ra = {}; rb = {}; rc = {}
        for s in SEEDS:
            _, ba = best_fixed_gain(s, d)
            ra[s] = ba
            rb[s] = run_arm("allo", G0, s, d, lam=LAMBDA)
            rc[s] = run_arm("allo", G0, s, d, lam=0.0)
        A[d] = sum(ra.values()) / 3; B[d] = sum(rb.values()) / 3; C[d] = sum(rc.values()) / 3
        A_each[d] = ra; B_each[d] = rb

    # determinism
    chk1 = run_arm("allo", G0, SEEDS[0], 0.030, lam=LAMBDA)
    chk2 = run_arm("allo", G0, SEEDS[0], 0.030, lam=LAMBDA)
    det = "PASS" if chk1 == chk2 else "FAIL"

    print(f"\n{'drift':>7} {'RMS_A':>9} {'RMS_B':>9} {'RMS_C':>9} {'adv=A-B':>9} {'C-A':>8}")
    for d in DRIFTS:
        print(f"{d:>7.3f} {A[d]:>9.4f} {B[d]:>9.4f} {C[d]:>9.4f} "
              f"{A[d]-B[d]:>+9.4f} {C[d]-A[d]:>+8.4f}")
    print(f"\ndeterminism run1==run2: {det} ({chk1:.6f})")

    # ── frozen bars ──
    d_hi = 0.030; d_lo = 0.000
    # (A NONSTAT-WIN) at drift 0.030 allo beats best fixed by >=0.05, mean AND each seed
    a_mean = (A[d_hi] - B[d_hi]) >= MARGIN
    a_each = all((A_each[d_hi][s] - B_each[d_hi][s]) >= MARGIN for s in SEEDS)
    barA = a_mean and a_each
    # (B REGIME-DISSOCIATION) drift0 → A<=B (fixed wins/ties) AND drift0.030 → A-B>=0.05
    barB = (A[d_lo] <= B[d_lo]) and ((A[d_hi] - B[d_hi]) >= MARGIN)
    # (C DRIFT-MONOTONE) adv non-decreasing over positive drifts AND adv(hi)>adv(0)
    adv = {d: A[d] - B[d] for d in DRIFTS}
    barC = (adv[0.010] <= adv[0.020] <= adv[0.030]) and (adv[0.030] > adv[0.000])
    # (D EARNED ablate) ablated never beats best fixed by margin at any drift AND
    #   at 0.030 buffer beats ablate by >=0.05
    d_noWin = all((C[d] - A[d]) >= -0.02 for d in DRIFTS)
    d_buffer = (C[d_hi] - B[d_hi]) >= MARGIN
    barD = d_noWin and d_buffer

    print("\nFROZEN BAR EVALUATION (MARGIN=0.05, no tune-to-green):")
    print(f"  (A NONSTAT-WIN @0.030)  A−B={A[d_hi]-B[d_hi]:+.4f} >= {MARGIN} "
          f"mean={'PASS' if a_mean else 'FAIL'} each={'PASS' if a_each else 'FAIL'} "
          f"=> {'PASS' if barA else 'FAIL'}")
    print(f"  (B REGIME-DISSOC) drift0 A<=B {'PASS' if A[d_lo]<=B[d_lo] else 'FAIL'} "
          f"(A={A[d_lo]:.4f} B={B[d_lo]:.4f}) AND drift0.030 A−B>={MARGIN} "
          f"{'PASS' if (A[d_hi]-B[d_hi])>=MARGIN else 'FAIL'} => {'PASS' if barB else 'FAIL'}")
    print(f"  (C DRIFT-MONOTONE) adv {adv[0.0]:+.4f}→{adv[0.01]:+.4f}→{adv[0.02]:+.4f}"
          f"→{adv[0.03]:+.4f} => {'PASS' if barC else 'FAIL'}")
    print(f"  (D EARNED ablate) ablate-never-wins={'PASS' if d_noWin else 'FAIL'} AND "
          f"buffer>ablate@0.030 C−B={C[d_hi]-B[d_hi]:+.4f}>={MARGIN} "
          f"{'PASS' if d_buffer else 'FAIL'} => {'PASS' if barD else 'FAIL'}")

    green = barA and barB and barC and barD and det == "PASS"
    print("\n" + "=" * 74)
    if green:
        print("VERDICT: 🟢 WALL-BROKEN-IN-NONSTAT — the allosteric buffer BEATS the best")
        print("         swept fixed gain under target DRIFT (lost stationary, wins moving),")
        print("         the win is EARNED (C ablate loses), MONOTONE in drift, REGIME-flip.")
    else:
        print("VERDICT: 🧱 WALL-HOLDS (REGIME-INVARIANT) — the buffer ALSO fails to beat the")
        print("         best fixed gain under drift → the neuromodulation ceiling is regime-")
        print("         invariant (even STRONGER 🧱, c9). Failed bar(s):")
        for nm, ok in [("A", barA), ("B", barB), ("C", barC), ("D", barD)]:
            if not ok:
                print(f"           - bar {nm} FAILED")
    print("=" * 74)
    return green


if __name__ == "__main__":
    main()
