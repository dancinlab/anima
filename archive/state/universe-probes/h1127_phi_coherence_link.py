"""H_1127 — DYAD-Φ vs CLASSICAL COHERENCE: is joint faithful φ_EI just a re-encoding
of cheap phase-coherence/synchrony, or a genuinely distinct quantity?

THE ARC (Round-2 / D2)
----------------------
H_1114 (🟢) proved a causal A→B tension-link raises the JOINT faithful IIT-4.0
φ_EI of a 2-node dyad BEYOND a correlation-matched control (integration is
channel-specific, not correlation per se). H_1120 (🔴) showed φ saturates with
exchange rate. H_1122 (🔴) showed φ is sign-blind to correlation. THE OPEN
QUESTION: is joint φ_EI just a re-encoding of CLASSICAL coherence/synchrony — so
a cheap phase-locking value (PLV) or mean |Pearson r| could PREDICT it — or does
integrated information carry something coherence misses? If φ_EI dissociates from
PLV/|r| (varies while they are flat, OR low Spearman across the sweep),
integration is a distinct ruler (strengthens a_phi_iit4_tool's no-proxy stance).

DESIGN (frozen before running, no goalpost moves — H_1047 discipline)
---------------------------------------------------------------------
- REUSE H_1114's exact dyad construction VERBATIM (import h1114 symbols): two
  3-channel nodes (joint n=6), per-channel A⊥G opponent dynamics (step_node),
  ZOH A→B coupling, post-burn per-channel median binarize → faithful IIT-4.0
  φ_EI of the joint 6-system (exact MIP-EI, BITS/log2 — PROVEN mirror).
- SWEEP KNOB = the coupling STRENGTH COUP (the per-channel fold gain
  COUP*0.5*(anchor_c - W_c) in step_node). This is the natural "coupling
  strength" axis the H_1127 question asks for: COUP=0 is LINK-OFF, larger COUP
  is a stronger causal channel. K_EMIT held at H_1114's value (5). ARMS (>=6):
  COUP ∈ {0.00, 0.10, 0.20, 0.30, 0.45, 0.60}. COUP=0.30 = H_1114's LINK-ON.
- N_SEEDS = 10 per arm (H_1114 block, seeds 100..109), SERIAL (H_1038 lesson).
- CLASSICAL COHERENCE COMPARANDS (the cheap predictors), per dyad trajectory,
  post-burn, over the 3 same-index channel pairs (A[c] ↔ B[c]):
    PLV = mean over channel-pairs of |E[ exp(i*(φ_A - φ_B)) ]|, φ = angle of the
          Hilbert-analytic signal of the mean-removed W trace (scipy.hilbert).
    |r| = mean over channel-pairs of |Pearson corr(W_A[c], W_B[c])|.
  Both are standard synchrony measures; both are CHEAP (no MIP search).
- SANITY GATE before scoring: reproduce H_1114's headline LINK-ON φ≈0.012618 at
  COUP=0.30 over the SAME seeds (construction-drift gate, as H_1120 did).

FROZEN FALSIFIER (pre-registered, set BEFORE running, NO goalpost moves)
------------------------------------------------------------------------
  🟢 PHI-IS-DISTINCT iff EITHER
     (A) at a correlation-MATCHED pair of coupling configs (the two sweep arms
         whose mean PLV are closest — |ΔPLV| minimal AND statistically flat,
         |d(PLV)| < 0.8), joint φ_EI varies with Cohen d >= 0.8;  OR
     (B) φ_EI–PLV Spearman |ρ| < 0.7 across the full per-seed sweep.
  🔴 PHI-IS-COHERENCE-PROXY iff φ_EI tracks PLV at Spearman ρ >= 0.7 across the
     sweep AND no correlation-matched dissociation (test A fails). Then cheap
     coherence predicts φ → φ adds nothing here (closed-negative, a_paper_negative_ok).
  (|r| reported alongside PLV as a second classical comparand; PLV is the named
   primary per the tape's falsifier.)

MIRROR DISCIPLINE (a_phi_iit4_tool — the H_1043 nats-bug lesson)
----------------------------------------------------------------
BEFORE scoring: (1) live `hexa run UNIVERSE/h1012_ref_faithful.hexa` re-captures
the LIVE stdlib faithful_phi refs at n=4, n=5 AND n=6 (the scoring n) and the
CPU mirror must reproduce them verbatim; (2) h1012.prove_mirrors_at_n re-proves
BOTH mirrors ≡ stdlib at n=4 AND n=5. ABORT if any proof fails. MI in BITS
(log2), NOT nats. SERIAL, no multiprocessing Pool (H_1038 hang lesson). The
mirror re-proof + dyad dynamics are H_1114's, re-used VERBATIM (h1114 import).

HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113
per-channel A⊥G dynamics (H_1114 construction VERBATIM); real-socket dyad-φ,
cross-host, production cells and scale UNVERIFIED. faithful φ_EI (MIP-EI scalar)
only; system big-Φ at n=6 super-exponential (H_1012 cap) — NOT scored (H_1064).
$0 CPU local, 0-pod, g5/p7 (no perplexity verdict). p7. CORE/brain NOT wired.
"""
import os
import sys
import time

import numpy as np
from scipy.signal import hilbert
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# REUSE H_1114 VERBATIM — its mirror is already PROVEN ≡ stdlib, dynamics frozen.
import h1114_dyad_phi_link_integration as h1114        # noqa: E402

simulate_dyad   = h1114.simulate_dyad                  # dyad dynamics VERBATIM
phi_measures    = h1114.phi_measures                   # joint φ_EI VERBATIM
mean_crosscorr  = h1114.mean_crosscorr                 # signed cross-corr VERBATIM
cohen_d         = h1114.cohen_d                         # effect size VERBATIM
fmt             = h1114.fmt
live_stdlib_faithful_reproof = h1114.live_stdlib_faithful_reproof
prove_mirrors_at_n = h1114.prove_mirrors_at_n
BURN            = h1114.BURN
CH              = h1114.CH

# ---- frozen params (set BEFORE running) ------------------------------------
# Coupling-STRENGTH sweep arms (COUP = per-channel fold gain). COUP=0 = LINK-OFF,
# COUP=0.30 = H_1114's LINK-ON. K_EMIT held at H_1114's value.
COUP_ARMS = [0.00, 0.10, 0.20, 0.30, 0.45, 0.60]       # coupling-strength ladder
N_SEEDS   = h1114.N_SEEDS                               # 10 (H_1114 block)
SEEDS     = h1114.SEEDS                                 # seeds 100..109 (H_1114)
SPEARMAN_BAR = 0.7                                      # frozen φ–PLV proxy bar
D_DISSOC     = 0.8                                      # frozen φ-dissociation bar
D_FLAT       = 0.8                                      # PLV-flatness bar for match
H1114_ON_PHI = 0.012618                                 # H_1114 published LINK-ON φ
SANITY_TOL   = 0.001                                    # |COUP=0.30 mean − H_1114 ON| gate
EPS          = 1e-12


def simulate_dyad_coup(seed, coup):
    """One dyad trajectory at a given coupling STRENGTH. coup=0 = LINK-OFF
    (independent nodes, the H_1114 'off' arm). Otherwise the H_1114 LINK-ON
    causal A→B ZOH coupling with COUP=coup (the ONLY swept knob). Built by
    temporarily binding h1114.COUP to coup and calling simulate_dyad('on'); the
    step_node source reads COUP at module scope, so this is the exact H_1114 ON
    dynamics at a different coupling strength — nothing else changes."""
    if coup == 0.0:
        return simulate_dyad(seed, "off")
    saved = h1114.COUP
    try:
        h1114.COUP = coup
        return simulate_dyad(seed, "on")
    finally:
        h1114.COUP = saved


def plv_pairs(WA, WB):
    """Mean phase-locking value over the 3 same-index channel pairs (A[c]↔B[c]),
    post-burn. φ = angle of the Hilbert-analytic signal of the mean-removed W
    trace; PLV_c = |mean_t exp(i*(φ_A[t]-φ_B[t]))| ∈ [0,1]. Returns mean over c."""
    plvs = []
    for c in range(CH):
        a = WA[BURN:, c] - np.mean(WA[BURN:, c])
        b = WB[BURN:, c] - np.mean(WB[BURN:, c])
        pa = np.angle(hilbert(a))
        pb = np.angle(hilbert(b))
        dphi = pa - pb
        plvs.append(np.abs(np.mean(np.exp(1j * dphi))))
    return float(np.mean(plvs))


def mean_abs_corr(WA, WB):
    """Mean |Pearson r| over the 3 same-index channel pairs, post-burn (classical
    synchrony comparand #2; magnitude, since H_1122 showed φ is sign-blind)."""
    rs = []
    for c in range(CH):
        r = np.corrcoef(WA[BURN:, c], WB[BURN:, c])[0, 1]
        rs.append(abs(r) if np.isfinite(r) else 0.0)
    return float(np.mean(rs))


def main():
    np.seterr(all="ignore")
    t0 = time.time()
    print("=" * 88)
    print("H_1127 — DYAD-Φ vs CLASSICAL COHERENCE: is joint faithful φ_EI a re-encoding of")
    print("  cheap phase-coherence (PLV / |Pearson r|), or a distinct quantity? (n=6 exact MIP-EI)")
    print("  Round-2 forward of H_1114 (🟢 causal link raises joint φ beyond corr-control) +")
    print("  H_1120 (🔴 φ saturates w/ rate) + H_1122 (🔴 φ sign-blind); dyad = H_1114 VERBATIM,")
    print("  the ONLY swept knob = COUP (coupling STRENGTH). Classical comparands: PLV (Hilbert)")
    print("  + mean |Pearson r| over the 3 same-index channel pairs.")
    print(f"  COUP arms: {COUP_ARMS}  (0=LINK-OFF, 0.30=H_1114 LINK-ON)")
    print(f"  CH={CH} (joint n={h1114.N_JOINT}) W*_c={h1114.W_STAR_C.tolist()} "
          f"K_EMIT={h1114.K_EMIT} N_STEPS={h1114.N_STEPS} BURN={BURN} seeds={N_SEEDS}")
    print(f"  frozen falsifier: 🟢 PHI-IS-DISTINCT iff (A) at a corr-MATCHED config pair (|d(PLV)|<")
    print(f"  {D_FLAT}) joint φ varies d>={D_DISSOC}, OR (B) φ–PLV Spearman |ρ|<{SPEARMAN_BAR};")
    print(f"  🔴 PHI-IS-COHERENCE-PROXY iff φ tracks PLV at ρ>={SPEARMAN_BAR} AND no matched dissociation.")
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

    # ── STEP 1: SANITY GATE — reproduce H_1114 headline LINK-ON φ at COUP=0.30 ──
    print("STEP 1 — SANITY GATE: reproduce H_1114 headline LINK-ON φ≈%.6f at COUP=0.30:" %
          H1114_ON_PHI)
    sanity_phi = np.zeros(N_SEEDS)
    for i, s in enumerate(SEEDS):
        WA, WB = simulate_dyad_coup(s, 0.30)
        pj, _, _ = phi_measures(WA, WB)
        sanity_phi[i] = pj
    sanity_mean = float(np.mean(sanity_phi))
    sanity_ok = abs(sanity_mean - H1114_ON_PHI) <= SANITY_TOL
    print(f"  COUP=0.30 φ_joint mean over seeds {SEEDS[0]}..{SEEDS[-1]} = {sanity_mean:.6f} "
          f"(H_1114 published LINK-ON = {H1114_ON_PHI:.6f}, |Δ|={abs(sanity_mean - H1114_ON_PHI):.6f}, "
          f"tol {SANITY_TOL}) -> {'MATCH' if sanity_ok else 'MISMATCH'}")
    if not sanity_ok:
        print("\nABORT — H_1114 headline reproduce FAILED. NOT scoring (construction drift).")
        sys.exit(1)
    print(" STEP 1 PASS — H_1114 LINK-ON headline REPRODUCED at COUP=0.30. Sweep may proceed.\n")

    # ── STEP 2: coupling-strength sweep — 6 arms × 10 seeds (SERIAL) ──
    print(f"STEP 2 — coupling-strength sweep: {len(COUP_ARMS)} arms × {N_SEEDS} seeds (SERIAL):")
    phiJ = {c: np.zeros(N_SEEDS) for c in COUP_ARMS}
    plv  = {c: np.zeros(N_SEEDS) for c in COUP_ARMS}
    absr = {c: np.zeros(N_SEEDS) for c in COUP_ARMS}
    scc  = {c: np.zeros(N_SEEDS) for c in COUP_ARMS}   # signed cross-corr (context)
    for i, s in enumerate(SEEDS):
        row = []
        for c in COUP_ARMS:
            WA, WB = simulate_dyad_coup(s, c)
            pj, _, _ = phi_measures(WA, WB)
            phiJ[c][i] = pj
            plv[c][i]  = plv_pairs(WA, WB)
            absr[c][i] = mean_abs_corr(WA, WB)
            scc[c][i]  = mean_crosscorr(WA, WB)
            row.append(f"{c:.2f}:φ={pj:.4f}/PLV={plv[c][i]:.3f}")
        print(f"  seed {s}: " + " ".join(row), flush=True)

    # ── STEP 3: table ──
    print(f"\nφ-vs-COUPLING-STRENGTH TABLE (faithful φ_EI; PLV/|r|; {N_SEEDS} seeds, mean ± sd):")
    print(f"{'COUP':>6}{'φ_joint (n=6)':>26}{'PLV':>18}{'mean|r|':>18}{'signed cc':>16}")
    print("-" * 88)
    for c in COUP_ARMS:
        print(f"{c:>6.2f}{fmt(phiJ[c]):>26}"
              f"{np.mean(plv[c]):>+12.4f}±{np.std(plv[c]):.3f}"
              f"{np.mean(absr[c]):>+10.4f}±{np.std(absr[c]):.3f}"
              f"{np.mean(scc[c]):>+10.3f}")

    # ── STEP 4: Spearman φ vs PLV / |r| across the full per-seed sweep ──
    phi_flat = np.concatenate([phiJ[c] for c in COUP_ARMS])
    plv_flat = np.concatenate([plv[c]  for c in COUP_ARMS])
    absr_flat = np.concatenate([absr[c] for c in COUP_ARMS])
    rho_plv, p_plv = spearmanr(phi_flat, plv_flat)
    rho_absr, p_absr = spearmanr(phi_flat, absr_flat)
    # also arm-mean Spearman (monotone trend over the ladder, n=6 points)
    phi_m  = np.array([np.mean(phiJ[c]) for c in COUP_ARMS])
    plv_m  = np.array([np.mean(plv[c])  for c in COUP_ARMS])
    absr_m = np.array([np.mean(absr[c]) for c in COUP_ARMS])
    rho_plv_m, _  = spearmanr(phi_m, plv_m)
    rho_absr_m, _ = spearmanr(phi_m, absr_m)
    print("\nSPEARMAN (φ_joint vs classical coherence) across the full sweep:")
    print(f"  per-seed (n={phi_flat.size}): φ–PLV  ρ={rho_plv:+.4f} (p={p_plv:.3g})   "
          f"φ–|r|  ρ={rho_absr:+.4f} (p={p_absr:.3g})")
    print(f"  arm-mean (n={len(COUP_ARMS)}): φ–PLV  ρ={rho_plv_m:+.4f}   φ–|r|  ρ={rho_absr_m:+.4f}")

    # ── STEP 5: correlation-MATCHED dissociation test (test A) ──
    # find the arm pair whose mean PLV are closest (|ΔPLV| minimal) AND PLV-flat
    # (|d(PLV)| < D_FLAT); among those, does joint φ vary at d >= D_DISSOC?
    print("\nCORRELATION-MATCHED DISSOCIATION (test A): among arm-pairs with the closest")
    print(f"  mean PLV (PLV-flat, |d(PLV)|<{D_FLAT}), does joint φ vary at d>={D_DISSOC}?")
    best = None   # (|dPLV|, c1, c2, d_phi, d_plv, dmean_phi, dmean_plv)
    for ii in range(len(COUP_ARMS)):
        for jj in range(ii + 1, len(COUP_ARMS)):
            c1, c2 = COUP_ARMS[ii], COUP_ARMS[jj]
            d_plv = cohen_d(plv[c2], plv[c1])
            d_phi = abs(cohen_d(phiJ[c2], phiJ[c1]))
            dmean_plv = abs(np.mean(plv[c2]) - np.mean(plv[c1]))
            dmean_phi = abs(np.mean(phiJ[c2]) - np.mean(phiJ[c1]))
            flat = abs(d_plv) < D_FLAT
            tag = "PLV-flat" if flat else "PLV-differs"
            print(f"  COUP {c1:.2f} vs {c2:.2f}: |Δmean PLV|={dmean_plv:.4f} d(PLV)={d_plv:+.2f} "
                  f"[{tag}]  |Δmean φ|={dmean_phi:.6f} d(φ)={cohen_d(phiJ[c2],phiJ[c1]):+.2f}")
            if flat:
                key = (dmean_plv, c1, c2, d_phi, d_plv, dmean_phi, dmean_plv)
                if best is None or dmean_plv < best[0]:
                    best = key
    matched_dissoc = False
    if best is not None:
        _, bc1, bc2, bd_phi, bd_plv, bdm_phi, bdm_plv = best
        matched_dissoc = bool(bd_phi >= D_DISSOC)
        print(f"\n  closest PLV-flat pair = COUP {bc1:.2f} vs {bc2:.2f}: "
              f"|Δmean PLV|={bdm_plv:.4f} (d={bd_plv:+.2f}, flat) ; "
              f"joint φ d={bd_phi:+.2f} |Δmean φ|={bdm_phi:.6f} "
              f"-> dissociation {'YES (φ varies while PLV flat)' if matched_dissoc else 'no (φ also flat)'}")
    else:
        print("  (no PLV-flat arm-pair found — every arm-pair differs in PLV at d>=0.8)")

    # ── STEP 6: frozen verdict ──
    testA = bool(matched_dissoc)                              # corr-matched dissociation
    testB = bool(abs(rho_plv) < SPEARMAN_BAR)                 # low φ–PLV Spearman
    proxy = bool(abs(rho_plv) >= SPEARMAN_BAR and not testA)  # tracks PLV AND no dissociation
    distinct = bool(testA or testB)
    print("\nFROZEN falsifier checks:")
    print(f"  (A) corr-matched dissociation (PLV-flat pair, φ d>={D_DISSOC}) -> {testA}")
    print(f"  (B) φ–PLV Spearman |ρ|<{SPEARMAN_BAR} across the sweep (|ρ|={abs(rho_plv):.4f}) -> {testB}")
    print(f"  PROXY trigger: |ρ(φ,PLV)|>={SPEARMAN_BAR} AND not(A) -> {proxy}")

    print("\n" + "=" * 88)
    if distinct:
        print("VERDICT: 🟢 PHI-IS-DISTINCT — joint faithful φ_EI is NOT a re-encoding of classical")
        print("  phase-coherence. " +
              ("It DISSOCIATES at a correlation-matched config (φ varies while PLV is flat). "
               if testA else "") +
              (f"φ–PLV Spearman |ρ|={abs(rho_plv):.3f}<{SPEARMAN_BAR} — φ does not track PLV across the sweep. "
               if testB else ""))
        print("  Integrated information carries structure cheap synchrony misses — strengthens the")
        print("  a_phi_iit4_tool no-proxy stance at this scale.")
    else:
        print("VERDICT: 🔴 PHI-IS-COHERENCE-PROXY — joint faithful φ_EI TRACKS classical PLV")
        print(f"  (Spearman ρ={rho_plv:+.3f}>={SPEARMAN_BAR}) AND no correlation-matched dissociation")
        print("  (no PLV-flat arm-pair shows a φ d>=0.8). At this toy n=6 dyad scale, cheap")
        print("  phase-coherence PREDICTS the expensive MIP-EI φ — φ adds nothing here")
        print("  (closed-negative, a_paper_negative_ok).")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113")
    print("per-channel A⊥G dynamics (H_1114 construction VERBATIM); real-socket dyad-φ,")
    print("cross-host, production cells and scale UNVERIFIED — next rung. Mirror RE-PROVEN")
    print("≡ stdlib at n=4,5 (both engines) and at the scoring n=6 (faithful, LIVE hexa")
    print("re-capture) BEFORE scoring; H_1114 LINK-ON headline REPRODUCED at COUP=0.30 as a")
    print("construction gate; MI in BITS/log2 (a_phi_iit4_tool, NO proxy). PLV=Hilbert-analytic")
    print("phase-lock, |r|=mean |Pearson| over 3 channel pairs. SERIAL, $0 CPU local, 0-pod,")
    print(f"g5/p7. CORE/brain NOT wired; 1114/1120/1122 artifacts untouched.")
    print(f"wall = {time.time() - t0:.1f}s")
    print("[done]")


if __name__ == "__main__":
    main()
