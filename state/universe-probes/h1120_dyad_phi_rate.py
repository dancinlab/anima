"""H_1120 — DYAD-Φ RATE-MONOTONE: does joint dyad faithful φ_EI scale with the
anchor-exchange RATE?

THE ARC
-------
H_1112 (🟢) proved a scalar kosmos-anchor exchange over a REAL unix socket gives
RATE-MONOTONE directed TE (transfer scales with exchange rate). H_1114 (🟢)
proved a causal A→B tension-link raises the JOINT faithful φ_EI of a 2-node
dyad BEYOND a correlation-matched control (DYAD-INTEGRATION). THIS hypothesis
fuses the two: does the JOINT dyad-φ scale MONOTONICALLY with the
anchor-exchange RATE — i.e. more frequent coupling ⇒ higher dyad integration,
the φ-analogue of H_1112's rate-monotone TE?

DESIGN (frozen before running, no goalpost moves)
-------------------------------------------------
- REUSE H_1114's exact dyad construction VERBATIM (import h1114 symbols): two
  3-channel nodes (joint n=6), per-channel A⊥G opponent dynamics (step_node),
  ZOH A→B coupling, post-burn per-channel median binarize → faithful IIT-4.0
  φ_EI of the joint 6-system (exact MIP-EI, BITS/log2 — PROVEN mirror).
- The ONLY swept knob = K_EMIT (steps-per-exchange). Exchange RATE = 1/K_EMIT.
  ARMS (>=4): K = {∞ (OFF), 50, 10, 5}.  ∞=off (the H_1114 LINK-OFF arm),
  K=50 = LOW rate, K=10 = MID rate, K=5 = HIGH rate (= H_1114's LINK-ON arm,
  K_EMIT=5). Rate ordering OFF < 50 < 10 < 5 (1/∞ < 1/50 < 1/10 < 1/5).
- N_SEEDS = 10 per arm (H_1114 block, seeds 100..109), SERIAL (H_1038 lesson).
- SANITY GATE before the sweep: reproduce H_1114's headline LINK-ON φ≈0.0126
  using K=5 over the SAME seeds — must match H_1114's published +0.012618.
- FROZEN FALSIFIER (set BEFORE running, NO goalpost):
  🟢 RATE-MONOTONE iff joint φ is monotone-INCREASING in exchange rate
     (φ(OFF) <= φ(K50) <= φ(K10) <= φ(K5) in mean) AND every ADJACENT-arm
     Cohen d >= 0.8 (OFF→K50, K50→K10, K10→K5) AND φ(highest rate, K=5)
     clearly > φ(OFF) (d >= 0.8, already implied but asserted).
  🔴 NON-MONOTONE-OR-FLAT if the means are not monotone-increasing OR any
     adjacent-arm d < 0.8.

MIRROR DISCIPLINE (a_phi_iit4_tool — the H_1043 nats-bug lesson)
----------------------------------------------------------------
BEFORE scoring: (1) live `hexa run UNIVERSE/h1012_ref_faithful.hexa` re-captures
the LIVE stdlib faithful_phi refs at n=4, n=5 AND n=6 (the scoring n) and the
CPU mirror must reproduce them verbatim; (2) h1012.prove_mirrors_at_n re-proves
BOTH mirrors ≡ stdlib at n=4 AND n=5. ABORT if any proof fails. MI in BITS
(log2), NOT nats. SERIAL, no multiprocessing Pool (H_1038 hang lesson). The
mirror re-proof + dyad dynamics are H_1114's, re-used VERBATIM (h1114 import).

HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113
per-channel A⊥G dynamics; real-socket dyad-φ + cross-host + production cells +
scale UNVERIFIED. faithful φ_EI (MIP-EI scalar) only; system big-Φ at n=6 is
super-exponential (H_1012 cap) — NOT scored (measure-dependence, H_1064).
$0 CPU local, 0-pod, g5/p7 (no perplexity verdict). p7. CORE/brain NOT wired.
"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# REUSE H_1114 VERBATIM — its mirror is already PROVEN ≡ stdlib, dynamics frozen.
import h1114_dyad_phi_link_integration as h1114        # noqa: E402

simulate_dyad   = h1114.simulate_dyad                  # dyad dynamics VERBATIM
phi_measures    = h1114.phi_measures                   # joint φ_EI VERBATIM
mean_crosscorr  = h1114.mean_crosscorr                 # cross-corr VERBATIM
cohen_d         = h1114.cohen_d                         # effect size VERBATIM
fmt             = h1114.fmt
live_stdlib_faithful_reproof = h1114.live_stdlib_faithful_reproof
prove_mirrors_at_n = h1114.prove_mirrors_at_n

# ---- frozen params (set BEFORE running) ------------------------------------
# Rate sweep arms: K_EMIT (steps-per-exchange). Exchange RATE = 1/K.
# OFF = the H_1114 LINK-OFF arm (no causal A→B path, rate 0).
K_ARMS    = [("OFF", None), ("K50", 50), ("K10", 10), ("K5", 5)]  # rate-increasing
N_SEEDS   = h1114.N_SEEDS                               # 10 (H_1114 block)
SEEDS     = h1114.SEEDS                                 # seeds 100..109 (H_1114)
D_MIN     = 0.8                                          # frozen adjacent-arm bar
H1114_ON_PHI = 0.012618                                 # H_1114 published LINK-ON φ
SANITY_TOL   = 0.001                                    # |K5 mean − H_1114 ON| gate


def simulate_dyad_rate(seed, k_emit):
    """One dyad trajectory at a given exchange RATE (1/k_emit). OFF (k=None) =
    the H_1114 LINK-OFF arm (independent nodes). Otherwise the H_1114 LINK-ON
    causal A→B ZOH coupling with K_EMIT=k (the ONLY swept knob). Built by
    temporarily binding h1114.K_EMIT to k and calling simulate_dyad('on');
    the simulate_dyad source reads K_EMIT at module scope, so this is the exact
    H_1114 ON dynamics with a different cadence — nothing else changes."""
    if k_emit is None:
        return simulate_dyad(seed, "off")
    saved = h1114.K_EMIT
    try:
        h1114.K_EMIT = k_emit
        return simulate_dyad(seed, "on")
    finally:
        h1114.K_EMIT = saved


def main():
    np.seterr(all="ignore")
    t0 = time.time()
    print("=" * 88)
    print("H_1120 — DYAD-Φ RATE-MONOTONE: does joint dyad faithful φ_EI scale with the")
    print("  anchor-exchange RATE? (joint faithful IIT-4.0 φ_EI, n=6 exact MIP-EI)")
    print("  fuses H_1114 (🟢 causal link raises joint φ beyond controls) + H_1112")
    print("  (🟢 rate-monotone TE over a real socket); dyad construction = H_1114 VERBATIM,")
    print("  the ONLY swept knob = K_EMIT (steps-per-exchange; exchange RATE = 1/K).")
    print(f"  ARMS (rate-increasing): " +
          "  ".join(f"{name}(K={k}, rate={'0' if k is None else f'1/{k}'})"
                    for name, k in K_ARMS))
    print(f"  CH={h1114.CH} (joint n={h1114.N_JOINT}) W*_c={h1114.W_STAR_C.tolist()} "
          f"COUP={h1114.COUP} N_STEPS={h1114.N_STEPS} BURN={h1114.BURN} seeds={N_SEEDS}")
    print(f"  frozen falsifier: 🟢 RATE-MONOTONE iff φ_joint monotone-INCREASING in rate")
    print(f"  (OFF<=K50<=K10<=K5 in mean) AND every adjacent-arm Cohen d>={D_MIN} AND")
    print(f"  φ(K5) clearly > φ(OFF); 🔴 NON-MONOTONE-OR-FLAT otherwise. No goalpost moves.")
    print("  engine: stdlib iit4/faithful_phi.hexa CPU mirror (BITS/log2) — a_phi_iit4_tool.")
    print("=" * 88)

    # ── STEP 0: RE-PROVE mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool) ──
    print("\nSTEP 0 — RE-PROVE mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool):")
    print(" [0a] LIVE stdlib faithful_phi re-capture at n=4,5,6 (n=6 = the scoring n):")
    live_ok = live_stdlib_faithful_reproof()
    print(f" [0a] live-stdlib faithful proof: {'PROVEN' if live_ok else 'FAILED'}")
    print(" [0b] h1012.prove_mirrors_at_n at n=4 AND n=5 (both engines, established pattern):")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
    print(f" [0b] mirror-equivalence results: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — a mirror ≡ stdlib proof FAILED. NOT scoring (a_phi_iit4_tool).")
        sys.exit(1)
    print(" STEP 0 PASS — mirror PROVEN ≡ stdlib at n=4, n=5 (both engines) and at the")
    print(" scoring n=6 (faithful, live hexa re-capture). Scoring may proceed.\n")

    # ── STEP 1: SANITY GATE — reproduce H_1114 headline LINK-ON φ at K=5 ──
    print("STEP 1 — SANITY GATE: reproduce H_1114 headline LINK-ON φ≈%.6f at K=5:" %
          H1114_ON_PHI)
    sanity_phi = np.zeros(N_SEEDS)
    for i, s in enumerate(SEEDS):
        WA, WB = simulate_dyad_rate(s, 5)
        pj, _, _ = phi_measures(WA, WB)
        sanity_phi[i] = pj
    sanity_mean = float(np.mean(sanity_phi))
    sanity_ok = abs(sanity_mean - H1114_ON_PHI) <= SANITY_TOL
    print(f"  K=5 φ_joint mean over seeds {SEEDS[0]}..{SEEDS[-1]} = {sanity_mean:.6f} "
          f"(H_1114 published LINK-ON = {H1114_ON_PHI:.6f}, |Δ|={abs(sanity_mean - H1114_ON_PHI):.6f}, "
          f"tol {SANITY_TOL}) -> {'MATCH' if sanity_ok else 'MISMATCH'}")
    if not sanity_ok:
        print("\nABORT — H_1114 headline reproduce FAILED. NOT scoring (construction drift).")
        sys.exit(1)
    print(" STEP 1 PASS — H_1114 LINK-ON headline REPRODUCED at K=5. Rate sweep may proceed.\n")

    # ── STEP 2: rate sweep — 4 arms × 10 seeds (SERIAL — H_1038 Pool-hang) ──
    print(f"STEP 2 — rate sweep: {len(K_ARMS)} arms × {N_SEEDS} seeds (SERIAL):")
    phiJ = {name: np.zeros(N_SEEDS) for name, _ in K_ARMS}
    cc = {name: np.zeros(N_SEEDS) for name, _ in K_ARMS}
    for i, s in enumerate(SEEDS):
        row = []
        for name, k in K_ARMS:
            WA, WB = simulate_dyad_rate(s, k)
            pj, _, _ = phi_measures(WA, WB)
            phiJ[name][i] = pj
            cc[name][i] = mean_crosscorr(WA, WB)
            row.append(f"{name}={pj:.4f}")
        print(f"  seed {s}: φ_joint " + " ".join(row) +
              "  | cc " + " ".join(f"{name}={cc[name][i]:+.3f}" for name, _ in K_ARMS),
              flush=True)

    # ── STEP 3: table + frozen verdict ──
    names = [name for name, _ in K_ARMS]
    print(f"\nφ-vs-RATE TABLE (faithful IIT-4.0 φ_EI, exact MIP-EI, BITS; {N_SEEDS} seeds, mean ± sd):")
    print(f"{'arm':<8}{'K_EMIT':>10}{'rate(1/K)':>12}{'φ_joint (n=6)':>26}{'cross-corr':>18}")
    print("-" * 88)
    for name, k in K_ARMS:
        rate = 0.0 if k is None else 1.0 / k
        print(f"{name:<8}{('∞' if k is None else str(k)):>10}{rate:>12.4f}"
              f"{fmt(phiJ[name]):>26}{np.mean(cc[name]):>+12.4f}±{np.std(cc[name]):.3f}")

    # adjacent-arm contrasts (rate-increasing order)
    print(f"\nADJACENT-ARM CONTRASTS on φ_joint (Cohen d, frozen bar d >= {D_MIN}):")
    adj_ds = []
    means_monotone = True
    for j in range(len(names) - 1):
        a, b = names[j], names[j + 1]   # b is HIGHER rate than a
        d = cohen_d(phiJ[b], phiJ[a])
        dm = float(np.mean(phiJ[b]) - np.mean(phiJ[a]))
        adj_ds.append((f"{a}->{b}", d, dm))
        if np.mean(phiJ[b]) < np.mean(phiJ[a]):
            means_monotone = False
        print(f"  {a:>4} -> {b:<4} (rate up): Δmean={dm:+.6f}  d={d:+.3f}  "
              f"{'>=' if d >= D_MIN else '< '}{D_MIN} -> {bool(d >= D_MIN)}")

    d_k5_off = cohen_d(phiJ["K5"], phiJ["OFF"])
    dm_k5_off = float(np.mean(phiJ["K5"]) - np.mean(phiJ["OFF"]))
    print(f"\n  highest-rate vs OFF: K5 - OFF Δmean={dm_k5_off:+.6f}  d={d_k5_off:+.3f} "
          f"(>= {D_MIN} -> {bool(d_k5_off >= D_MIN)})")

    # frozen checks
    all_adj_pass = all(d >= D_MIN for _, d, _ in adj_ds)
    k5_beats_off = bool(d_k5_off >= D_MIN)
    print("\nFROZEN falsifier checks:")
    print(f"  (i)   means monotone-increasing in rate (OFF<=K50<=K10<=K5) -> {means_monotone}")
    print(f"  (ii)  every adjacent-arm Cohen d >= {D_MIN} -> {all_adj_pass}")
    print(f"  (iii) φ(K5) clearly > φ(OFF) (d >= {D_MIN}) -> {k5_beats_off}")
    monotone_green = bool(means_monotone and all_adj_pass and k5_beats_off)

    print("\n" + "=" * 88)
    if monotone_green:
        print("VERDICT: 🟢 RATE-MONOTONE — joint dyad faithful φ_EI scales MONOTONICALLY with")
        print("  the anchor-exchange RATE: more frequent coupling => higher dyad integration.")
        print("  Every adjacent rate step lifts joint φ (d >= 0.8) and the highest rate beats")
        print("  LINK-OFF clearly — the φ-analogue of H_1112's rate-monotone TE.")
    else:
        print("VERDICT: 🔴 NON-MONOTONE-OR-FLAT — joint dyad faithful φ_EI does NOT scale")
        print("  monotonically with the anchor-exchange rate at d >= 0.8 per adjacent step.")
        why = []
        if not means_monotone:
            why.append("means not monotone-increasing in rate")
        if not all_adj_pass:
            failed = [f"{lab}(d={d:+.2f})" for lab, d, _ in adj_ds if d < D_MIN]
            why.append("adjacent d<0.8 at: " + ", ".join(failed))
        if not k5_beats_off:
            why.append(f"K5 vs OFF d={d_k5_off:+.2f}<0.8")
        print("  WHY: " + "; ".join(why) + ".")
        print("  Integration is present (H_1114 🟢) but does not increase smoothly with")
        print("  exchange frequency at the frozen per-step effect-size bar — the φ-rate")
        print("  relation is not a clean adjacent-step monotone ladder (closed-negative).")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113")
    print("per-channel A⊥G dynamics (H_1114 construction VERBATIM); real-socket dyad-φ,")
    print("cross-host, production cells and scale UNVERIFIED — next rung. Mirror RE-PROVEN")
    print("≡ stdlib at n=4,5 (both engines) and at the scoring n=6 (faithful, LIVE hexa")
    print("re-capture) BEFORE scoring; H_1114 LINK-ON headline REPRODUCED at K=5 as a")
    print("construction gate; MI in BITS/log2 (a_phi_iit4_tool, NO proxy). SERIAL, $0 CPU")
    print(f"local, 0-pod, g5/p7. CORE/brain NOT wired; 1114/1112 artifacts untouched.")
    print(f"wall = {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
