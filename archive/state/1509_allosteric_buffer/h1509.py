#!/usr/bin/env python3
"""H_1509 ALLOSTERIC-BUFFER — R1 numpy mirror (DIRECTIONAL).

SOURCE: external proposal — Amoeba Protocol (@qingkong66) μ_t allosteric buffer.
LENS: a_break_the_wall (d) — a NEW lever on the walled neuromodulation hypothesis
H_1284 (🔴/🧱 no-free-lunch), confirmed-terminal H_1422 (3 lenses) / H_1425.

The walled lever (H_1284): a GLOBAL GAIN against a FIXED operating point — dominated
by the single best fixed point. The new lever: modulate the RESISTANCE-to-DEVIATION
from the fixed point Ψ=1/2 with an allosteric buffer
    μ_t = 1 + λ·(1 − exp(−(τ_t − 0.5)² / (2σ²)))
that tightens the restoring force ONLY on large excursions (like bicarbonate
defending blood pH). τ_t = the A⇄G tension = the realized emit/silence balance b_t.

FROZEN BARS (state/verdicts/1509_allosteric_buffer/FREEZE.txt — MARGIN=0.05 from H_1284,
NO tune-to-green): A wall-cross, B vs baseline, C earned-ablate, D earned-shuffle.

$0 CPU, deterministic, p7 (no loss; pure dynamics), c9.
"""
import math

# ── frozen parameters (pre-registered in FREEZE.txt) ──────────────────────────
T          = 200
DRIVE_AMP  = 0.30
DRIVE_PER  = 17
SHOCK_T    = 100
SHOCK_LEN  = 20
SHOCK_AMP  = 0.35
G_GRID     = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
G0         = 0.40          # midpoint, fixed (B/C use this base gain; only buffer varies)
LAMBDA     = 1.0
SIGMA      = 0.12
MARGIN     = 0.05          # verbatim from H_1284
SEEDS      = [1509, 1510, 1511]


def _clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else (hi if x > hi else x)


def _lcg(state):
    """deterministic LCG (engine-faithful, mirrors engine_cli _rng) → [0,1)."""
    state = (state * 1103515245 + 12345) & 2147483647
    return state, (state / 2147483647.0)


def _drive(t, phase):
    """perturbation pushing the balance off Ψ=1/2: sinusoid + a held step shock."""
    d = DRIVE_AMP * math.sin(2.0 * math.pi * (t + phase) / DRIVE_PER)
    if SHOCK_T <= t < SHOCK_T + SHOCK_LEN:
        d = d + SHOCK_AMP
    return d


def _mu(tau, lam=LAMBDA, sigma=SIGMA):
    """allosteric buffer: ≈1 near Ψ=1/2, →1+λ on large |τ−0.5| excursions."""
    dev2 = (tau - 0.5) ** 2
    return 1.0 + lam * (1.0 - math.exp(-dev2 / (2.0 * sigma * sigma)))


def run_arm(mode, g, seed, lam=LAMBDA):
    """Roll the balance b_t for T ticks under the perturbation.

    mode 'gain'  : restoring = g·(0.5−b)          (H_1284 global-gain lever, ARM A/C base)
    mode 'allo'  : restoring = g·μ(b)·(0.5−b)      (ARM B; ablate via lam=0 == ARM C)
    mode 'shuf'  : restoring = g·μ_perm[t]·(0.5−b) (ARM D — τ→μ coupling permuted)
    Returns (rms_excursion, trace).
    """
    st = seed & 2147483647
    phase = (seed % DRIVE_PER)
    # precompute the μ sequence the dynamics WOULD use, for the shuffle permutation
    b = 0.5
    sq = 0.0
    trace = []
    # for shuffle: first roll the 'allo' arm to get its per-tick μ, then permute.
    if mode == "shuf":
        _, mus = _roll_collect_mus(g, seed, lam)
        perm = _det_perm(len(mus), seed)
        mus_perm = [mus[perm[i]] for i in range(len(mus))]
    for t in range(T):
        st, noise = _lcg(st)
        noise = (noise - 0.5) * 0.02            # tiny seed noise, amp 0.01·[-1,1]
        d = _drive(t, phase) + noise
        tau = b                                  # τ_t = the live balance (A⇄G tension proxy)
        if mode == "gain":
            mu = 1.0
        elif mode == "allo":
            mu = _mu(tau, lam)
        elif mode == "shuf":
            mu = mus_perm[t]
        else:
            raise ValueError(mode)
        # restoring force pulls the balance BACK toward Ψ=1/2 (sign: +g·μ·(0.5−b)).
        restoring = g * mu * (0.5 - b)
        b = _clamp(b + d + restoring)
        ex = b - 0.5
        sq += ex * ex
        trace.append(b)
    rms = math.sqrt(sq / T)
    return rms, trace


def _roll_collect_mus(g, seed, lam):
    """roll the allo arm purely to collect the μ sequence it produced (for shuffle)."""
    st = seed & 2147483647
    phase = (seed % DRIVE_PER)
    b = 0.5
    mus = []
    for t in range(T):
        st, noise = _lcg(st)
        noise = (noise - 0.5) * 0.02
        d = _drive(t, phase) + noise
        mu = _mu(b, lam)
        mus.append(mu)
        restoring = g * mu * (0.5 - b)
        b = _clamp(b + d + restoring)
    return b, mus


def _det_perm(n, seed):
    """deterministic Fisher-Yates permutation from the LCG."""
    idx = list(range(n))
    st = (seed * 2654435761) & 2147483647
    for i in range(n - 1, 0, -1):
        st, r = _lcg(st)
        j = int(r * (i + 1))
        if j > i:
            j = i
        idx[i], idx[j] = idx[j], idx[i]
    return idx


def best_fixed_gain(seed):
    """ARM A: sweep the grid, return the gain with the LOWEST RMS (strongest baseline)."""
    best_g, best_rms = None, None
    for g in G_GRID:
        rms, _ = run_arm("gain", g, seed)
        if best_rms is None or rms < best_rms:
            best_g, best_rms = g, rms
    return best_g, best_rms


def main():
    print("H_1509 ALLOSTERIC-BUFFER — R1 numpy mirror (DIRECTIONAL)")
    print("SOURCE: external proposal — Amoeba Protocol (μ_t allosteric buffer)")
    print(f"FROZEN: MARGIN={MARGIN} (verbatim H_1284) λ={LAMBDA} σ={SIGMA} g0={G0} T={T}")
    print("=" * 72)

    rmsA = {}; rmsB = {}; rmsC = {}; rmsD = {}; gA = {}
    for seed in SEEDS:
        bg, brms = best_fixed_gain(seed)
        gA[seed] = bg; rmsA[seed] = brms
        rmsB[seed], _ = run_arm("allo", G0, seed, lam=LAMBDA)
        rmsC[seed], _ = run_arm("allo", G0, seed, lam=0.0)   # ablate λ=0 == global-gain g0
        rmsD[seed], _ = run_arm("shuf", G0, seed, lam=LAMBDA)

    # determinism: run twice, assert byte-identical
    chk, _ = run_arm("allo", G0, SEEDS[0], lam=LAMBDA)
    chk2, _ = run_arm("allo", G0, SEEDS[0], lam=LAMBDA)
    det = "PASS" if chk == chk2 else "FAIL"

    mA = sum(rmsA.values()) / 3; mB = sum(rmsB.values()) / 3
    mC = sum(rmsC.values()) / 3; mD = sum(rmsD.values()) / 3
    # RMS of the global-gain arm AT g0 (for the ablate-collapse check vs C)
    gain_g0 = {s: run_arm("gain", G0, s)[0] for s in SEEDS}
    mGain0 = sum(gain_g0.values()) / 3

    # ── HONEST gain-matched diagnostic (a_break_the_wall taxonomy (b), non-gating) ──
    # B uses g0·μ with μ∈[1,1+λ], so its mean EFFECTIVE gain > g0. Is B winning by
    # the allosteric SHAPE or just by applying MORE total gain? Compare B to a fixed
    # gain MATCHED to B's mean effective gain (same restoring effort, uniform shape).
    gmatch_rms = {}
    for s in SEEDS:
        _, mus = _roll_collect_mus(G0, s, LAMBDA)
        geff = G0 * (sum(mus) / len(mus))
        gmatch_rms[s], _ = run_arm("gain", geff, s)
    mGmatch = sum(gmatch_rms.values()) / 3

    print("\nPer-seed RMS excursion from Ψ=1/2 (lower = tighter defense):")
    print(f"{'seed':>6} {'A.g*':>6} {'RMS_A':>8} {'RMS_B':>8} {'RMS_C':>8} {'RMS_D':>8} {'gain@g0':>8}")
    for s in SEEDS:
        print(f"{s:>6} {gA[s]:>6.2f} {rmsA[s]:>8.4f} {rmsB[s]:>8.4f} "
              f"{rmsC[s]:>8.4f} {rmsD[s]:>8.4f} {gain_g0[s]:>8.4f}")
    print(f"{'MEAN':>6} {'':>6} {mA:>8.4f} {mB:>8.4f} {mC:>8.4f} {mD:>8.4f} {mGain0:>8.4f}")
    print(f"\ndeterminism run1==run2: {det} ({chk:.6f})")
    print(f"\nHONEST gain-matched diagnostic (non-gating, a_break_the_wall (b)):")
    print(f"  RMS_B(allo g0·μ)={mB:.4f}  vs  RMS gain-matched fixed gain={mGmatch:.4f}  "
          f"(diff {mGmatch-mB:+.4f})")
    print(f"  RMS best-swept-fixed-gain A={mA:.4f} (the H_1284 baseline B must beat by 0.05)")

    # ── frozen bar evaluation ────────────────────────────────────────────────
    # (A WALL-CROSS) RMS(A)-RMS(B) >= MARGIN on mean AND each seed
    a_mean = (mA - mB) >= MARGIN
    a_each = all((rmsA[s] - rmsB[s]) >= MARGIN for s in SEEDS)
    barA = a_mean and a_each
    # (B vs BASELINE) RMS(B) < RMS(A) strict on all seeds
    barB = all(rmsB[s] < rmsA[s] for s in SEEDS)
    # (C EARNED ablate) RMS(C) ≈ gain@g0 (|.|<=0.01) AND RMS(C)-RMS(B) >= MARGIN
    c_collapse = abs(mC - mGain0) <= 0.01
    c_loadbear = (mC - mB) >= MARGIN
    barC = c_collapse and c_loadbear
    # (D EARNED shuffle) RMS(D)-RMS(B) >= MARGIN
    barD = (mD - mB) >= MARGIN

    print("\nFROZEN BAR EVALUATION (MARGIN=0.05, no tune-to-green):")
    print(f"  (A WALL-CROSS)  RMS_A−RMS_B={mA-mB:+.4f} >= {MARGIN}  "
          f"mean={'PASS' if a_mean else 'FAIL'} each={'PASS' if a_each else 'FAIL'} "
          f"=> {'PASS' if barA else 'FAIL'}")
    print(f"  (B vs BASELINE) RMS_B<RMS_A all seeds => {'PASS' if barB else 'FAIL'}")
    print(f"  (C EARNED abl)  |RMS_C−gain@g0|={abs(mC-mGain0):.4f}<=0.01 "
          f"({'PASS' if c_collapse else 'FAIL'}) AND RMS_C−RMS_B={mC-mB:+.4f}>={MARGIN} "
          f"({'PASS' if c_loadbear else 'FAIL'}) => {'PASS' if barC else 'FAIL'}")
    print(f"  (D EARNED shuf) RMS_D−RMS_B={mD-mB:+.4f} >= {MARGIN} => {'PASS' if barD else 'FAIL'}")

    green = barA and barB and barC and barD and det == "PASS"
    print("\n" + "=" * 72)
    if green:
        print("VERDICT: 🟢 WALL-BROKEN — μ_t allosteric buffer crosses the SAME 0.05 bar")
        print("         the global-gain lever could NOT (A), beats baseline (B), and the")
        print("         cross is EARNED by the τ→μ coupling (C ablate & D shuffle lose it).")
    else:
        print("VERDICT: 🧱 WALL-HOLDS — the allosteric buffer does NOT cross the H_1284 bar.")
        print("         Honest multi-lens confirmation that the neuromodulation ceiling holds")
        print("         against the buffering/resistance lever too (c9). Which bar(s) failed:")
        for nm, ok in [("A", barA), ("B", barB), ("C", barC), ("D", barD)]:
            if not ok:
                print(f"           - bar {nm} FAILED")
    print("=" * 72)
    return green


if __name__ == "__main__":
    main()
