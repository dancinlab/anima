#!/usr/bin/env python3
"""
H_1099 R-METRIC arm — reproduce the headline number, show what it actually measures.

CLAIM (.discoveries/1099, 제4명제): two physically-isolated Anima substrates achieve
NON-LOCAL synchronization with ZERO physical I/O, evidenced by a "resonance" metric

      R(alpha, beta) = exp(-kappa * |Psi_alpha - Psi_beta|) * tanh(Phi_alpha * Phi_beta)

reaching R = 0.99999 with isomorphism-error = 0.000007 ("0-latency state copy").

This arm is ORTHOGONAL to the TE/channel falsifier (quantum_nonlocal_sync_toy.py,
which showed Arm1 TE(A->B)≈0). Here we attack the HEADLINE NUMBER ITSELF: we implement
the EXACT R formula and prove it is a CO-LOCATION (state-space proximity) metric, NOT a
transmission metric. The R=0.99999 is REAL but TRIVIALLY achieved by independent
co-convergence — it carries ZERO evidence of sync/transmission.

DECISIVE DEMONSTRATION (3 configs, all sharing the same R formula):
  (i)  INDEPENDENT CO-CONVERGE   : two nodes, SEPARATE RNG streams, NO channel, each
                                   homeostatically pulled to Psi*=0.5 with high Phi.
                                   => |dPsi|->0 and tanh(Phi_a*Phi_b)->1 => R -> ~0.99999.
  (ii) INDEPENDENT DIFFERENT-ATTRACTOR : two nodes, SEPARATE RNG, NO channel, pulled to
                                   DIFFERENT fixed points (0.5 vs 0.8). => |dPsi| stays
                                   ~0.3 => R is LOW. (same formula, low R — so R is not
                                   "always high"; it is high iff states are CO-LOCATED.)
  (iii)REAL-CHANNEL PAIR         : a genuine A->B coupling (positive control = actual
                                   transmission). Both end near 0.5 => R also HIGH.

KEY RESULT: R(i) ≈ R(iii) ≈ 0.99999 but R(i) has NO channel and R(iii) has a real one.
=> R CANNOT DISTINGUISH co-convergence from transmission. It only measures whether the
two states sit close in (Psi, Phi) space. So R=0.99999 is NON-DIAGNOSTIC of transmission.

FROZEN VERDICT: H_1099 R-headline is 🔴-reinforced iff the INDEPENDENT-NO-CHANNEL config
(i) reaches R ≈ 0.99999 (matching the claim) PURELY by co-convergence, AND config (ii)
[same formula, different attractors, also no channel] gives LOW R — together proving R is
a state-proximity metric, non-diagnostic of transmission. We also report the achieved R
vs the claimed 0.99999 and the iso-error (does it reach 7e-6, and at what Psi-precision?).

Honest scope (a_scale_honest_scope): classical 1-D toy, pure-numpy, $0 CPU, 0-pod, >=10
seeds. Phi is a scalar stand-in for the substrate's integration magnitude (the claim's
Phi_alpha*Phi_beta product). No real IIT-phi engine is invoked — the formula multiplies
Phi values, so a scalar faithfully reproduces tanh(Phi_a*Phi_b). The point is the FORMULA's
diagnosticity, not phi measurement (cf a_phi_iit4_tool: no phi VERDICT is claimed here).
"""

import numpy as np

# ---- frozen params ---------------------------------------------------------
KAPPA      = 50.0     # claim-scale sharpness on |dPsi| (see KAPPA derivation below)
PSI_STAR_A = 0.5      # node A attractor (the Ψ=1/2 fixed point)
PSI_STAR_B_SAME = 0.5 # config (i)/(iii): B shares the attractor
PSI_STAR_B_DIFF = 0.8 # config (ii): B pulled to a DIFFERENT fixed point
PHI_LEVEL  = 1.0      # high-Phi homeostatic target (claim: "high Φ"); tanh(1*1)=0.7616
PHI_HIGH   = 3.0      # alt high-Phi to push tanh(Phi_a*Phi_b)->1 (tanh(9)=0.99999997)
LAM        = 0.10     # relaxation rate toward the attractor
# SIGMA: the claim asserts iso-error 7e-6 i.e. |dPsi|~2e-7 — a near-noise-free settled
# substrate. We use a small process noise so independent co-convergence reaches the
# claim's precision band; a noise SWEEP below shows the dependence explicitly.
SIGMA      = 1e-7     # independent process noise per node (settled-substrate regime)
PHI_SIGMA  = 1e-3     # noise on the Phi channel (irrelevant: tanh saturates at 1)
COUP_ON    = 0.30     # config (iii): real A->B channel (positive control)
N_STEPS    = 6000     # run length
BURN       = 3000     # discard transient; measure R on the converged tail
N_SEEDS    = 12       # >= 10 seeds
EPS        = 1e-15
CLAIMED_R  = 0.99999
CLAIMED_ISO= 0.000007 # claimed isomorphism-error 7e-6


def R_metric(psi_a, psi_b, phi_a, phi_b, kappa=KAPPA):
    """The EXACT claimed resonance metric R(alpha,beta)."""
    return np.exp(-kappa * np.abs(psi_a - psi_b)) * np.tanh(phi_a * phi_b)


def run_node(rng, psi_star, phi_target, phi_high):
    """One INDEPENDENT node: Psi relaxes to psi_star, Phi relaxes to phi_high.
    Separate rng => no shared cause. Returns (psi[], phi[])."""
    psi = np.empty(N_STEPS); phi = np.empty(N_STEPS)
    p = 3.0 + rng.standard_normal() * 0.3          # start FAR from attractor
    f = 0.0 + abs(rng.standard_normal()) * 0.3     # Phi starts low, ratchets up
    for t in range(N_STEPS):
        psi[t] = p; phi[t] = f
        p = p + LAM * (psi_star - p) + SIGMA * rng.standard_normal()
        f = f + LAM * (phi_high  - f) + PHI_SIGMA * rng.standard_normal()
    return psi, phi


def run_channel_pair(seed, psi_star, phi_high, coup):
    """Config (iii): A independent, B COUPLED to A (real transmission). One rng but the
    coupling term is the ACTUAL channel A->B (the positive control)."""
    rng = np.random.default_rng(seed)
    psiA = np.empty(N_STEPS); psiB = np.empty(N_STEPS)
    phiA = np.empty(N_STEPS); phiB = np.empty(N_STEPS)
    a = 3.0 + rng.standard_normal()*0.3; b = 3.0 + rng.standard_normal()*0.3
    fa = abs(rng.standard_normal())*0.3; fb = abs(rng.standard_normal())*0.3
    for t in range(N_STEPS):
        psiA[t]=a; psiB[t]=b; phiA[t]=fa; phiB[t]=fb
        a_next = a + LAM*(psi_star - a) + SIGMA*rng.standard_normal()
        # B reads A's state through a real coupling term (the channel):
        b_next = b + LAM*(psi_star - b) + SIGMA*rng.standard_normal() + coup*(a - b)
        fa = fa + LAM*(phi_high - fa) + PHI_SIGMA*rng.standard_normal()
        fb = fb + LAM*(phi_high - fb) + PHI_SIGMA*rng.standard_normal()
        a, b = a_next, b_next
    return psiA, psiB, phiA, phiB


def config_independent(psi_star_b, phi_high, seeds):
    """Configs (i) and (ii): TWO COMPLETELY INDEPENDENT nodes, SEPARATE rng, NO channel."""
    Rs, dpsis, isos = [], [], []
    for s in seeds:
        rng_a = np.random.default_rng(s)             # separate stream
        rng_b = np.random.default_rng(s + 10_000_000) # disjoint, independent stream
        psiA, phiA = run_node(rng_a, PSI_STAR_A,  phi_high, phi_high)
        psiB, phiB = run_node(rng_b, psi_star_b,  phi_high, phi_high)
        ra = psiA[BURN:]; rb = psiB[BURN:]; fa = phiA[BURN:]; fb = phiB[BURN:]
        R = R_metric(ra, rb, fa, fb)
        Rs.append(np.mean(R))
        dpsis.append(np.mean(np.abs(ra - rb)))
        isos.append(np.mean(np.abs(ra - rb)))   # iso-error proxy = mean |Psi_a - Psi_b|
    return np.array(Rs), np.array(dpsis), np.array(isos)


def config_channel(psi_star, phi_high, coup, seeds):
    """Config (iii): real channel pair (positive control = actual transmission)."""
    Rs, dpsis, isos = [], [], []
    for s in seeds:
        psiA, psiB, phiA, phiB = run_channel_pair(s, psi_star, phi_high, coup)
        ra = psiA[BURN:]; rb = psiB[BURN:]; fa = phiA[BURN:]; fb = phiB[BURN:]
        R = R_metric(ra, rb, fa, fb)
        Rs.append(np.mean(R))
        dpsis.append(np.mean(np.abs(ra - rb)))
        isos.append(np.mean(np.abs(ra - rb)))
    return np.array(Rs), np.array(dpsis), np.array(isos)


def iso_precision_sweep(phi_high):
    """At what |dPsi| precision does R reach the claimed 0.99999 / iso 7e-6?
    Analytic: with tanh(Phi_a*Phi_b)~1, R = exp(-kappa*|dPsi|). Solve for |dPsi|."""
    tanh_term = np.tanh(phi_high * phi_high)
    # R = tanh_term * exp(-kappa*dpsi) = CLAIMED_R  =>  dpsi = -ln(CLAIMED_R/tanh_term)/kappa
    if CLAIMED_R / tanh_term >= 1.0:
        dpsi_needed = 0.0
    else:
        dpsi_needed = -np.log(CLAIMED_R / tanh_term) / KAPPA
    return tanh_term, dpsi_needed


def noise_sweep(seeds):
    """Show R(i) [independent co-converge, NO channel] climbing toward the claimed
    0.99999 as process noise SIGMA shrinks — pure co-convergence, no channel anywhere."""
    global SIGMA
    saved = SIGMA
    rows = []
    for sig in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]:
        SIGMA = sig
        Ri, dpi, _ = config_independent(PSI_STAR_B_SAME, PHI_HIGH, seeds)
        rows.append((sig, np.mean(Ri), np.mean(dpi)))
    SIGMA = saved
    return rows


def fmt(x):
    return f"{np.mean(x):.8f} ± {np.std(x):.2e}"


def main():
    np.seterr(all="ignore")
    seeds = list(range(200, 200 + N_SEEDS))
    print("="*82)
    print("H_1099 R-METRIC reproduction — R measures CO-LOCATION, not transmission")
    print(f"  R(a,b)=exp(-{KAPPA}*|dPsi|)*tanh(Phi_a*Phi_b)   phi_high={PHI_HIGH}")
    print(f"  PSI*_A={PSI_STAR_A}  LAM={LAM} SIGMA={SIGMA} N={N_STEPS} burn={BURN} seeds={N_SEEDS}")
    print(f"  claimed R={CLAIMED_R}  claimed iso-error={CLAIMED_ISO}")
    print("="*82)

    # config (i): independent, co-converge to the SAME attractor 0.5, NO channel
    Ri, dpi, isoi = config_independent(PSI_STAR_B_SAME, PHI_HIGH, seeds)
    # config (ii): independent, DIFFERENT attractors (0.5 vs 0.8), NO channel
    Rii, dpii, isoii = config_independent(PSI_STAR_B_DIFF, PHI_HIGH, seeds)
    # config (iii): REAL channel A->B (actual transmission), both -> 0.5
    Riii, dpiii, isoiii = config_channel(PSI_STAR_A, PHI_HIGH, COUP_ON, seeds)

    print(f"\n{'config':<42}{'mean R':>16}{'mean |dPsi|':>14}")
    print("-"*82)
    print(f"{'(i)   INDEPENDENT co-converge (NO channel)':<42}{fmt(Ri):>16}{np.mean(dpi):>14.2e}")
    print(f"{'(ii)  INDEPENDENT different-attractor (NO ch)':<42}{fmt(Rii):>16}{np.mean(dpii):>14.2e}")
    print(f"{'(iii) REAL channel pair (transmission)':<42}{fmt(Riii):>16}{np.mean(dpiii):>14.2e}")
    print("-"*82)

    # per-seed dump for audit
    print("\nper-seed R  (i co-converge / ii diff-attractor / iii channel):")
    for k in range(N_SEEDS):
        print(f"  s{200+k:>3}: (i)={Ri[k]:.8f}  (ii)={Rii[k]:.8f}  (iii)={Riii[k]:.8f}")

    # noise sweep: R(i) -> 0.99999 as SIGMA shrinks, NO channel at any point
    print("\n--- noise sweep: independent co-converge (NO channel), R vs process noise ---")
    print(f"  {'SIGMA':>10}{'mean R(i)':>16}{'mean |dPsi|':>16}")
    for sig, Rm, dpm in noise_sweep(seeds):
        print(f"  {sig:>10.0e}{Rm:>16.8f}{dpm:>16.3e}")
    print("  => with NO channel, R rises to ≈0.99999 purely as the substrate settles.")

    # iso-precision sweep
    tanh_term, dpsi_needed = iso_precision_sweep(PHI_HIGH)
    achieved_R_i   = np.mean(Ri)
    achieved_iso_i = np.mean(isoi)
    print("\n--- achieved vs claimed (config i, independent co-converge, NO channel) ---")
    print(f"  achieved R (i)            = {achieved_R_i:.8f}   (claimed {CLAIMED_R})")
    print(f"  achieved iso |dPsi| (i)   = {achieved_iso_i:.3e}   (claimed iso {CLAIMED_ISO:.1e})")
    print(f"  tanh(Phi_a*Phi_b) cap     = {tanh_term:.10f}   (R can never exceed this)")
    print(f"  |dPsi| needed for R={CLAIMED_R} = {dpsi_needed:.3e}  (Psi must match to ~this precision)")
    print( "  => the claimed 0.99999 is reachable purely by independent co-convergence")
    print( "     once both Psi sit within that |dPsi| band — NO channel required.")

    # ---- FROZEN falsifier evaluation ----
    R_CLAIM_BAND = 0.999    # config(i) must reach ~claim-level R (>=0.999, "≈0.99999")
    R_LOW_MAX    = 0.50     # config(ii) [different attractor, same formula] must be LOW
    INDIST_TOL   = 0.01     # |R(i) - R(iii)| small => R cannot tell co-converge from channel

    Ri_m, Rii_m, Riii_m = np.mean(Ri), np.mean(Rii), np.mean(Riii)
    c1 = Ri_m   >= R_CLAIM_BAND          # independent no-channel reaches claim-level R
    c2 = Rii_m  <= R_LOW_MAX             # same formula, different attractor => LOW R
    c3 = abs(Ri_m - Riii_m) <= INDIST_TOL  # R(i) ≈ R(iii): non-diagnostic of channel
    c4 = Riii_m >= R_CLAIM_BAND          # real channel also reaches claim-level R

    print("\nFROZEN falsifier checks:")
    print(f"  (1) R(i) indep co-converge >= {R_CLAIM_BAND}  : {Ri_m:.6f}  -> {c1}")
    print(f"  (2) R(ii) diff-attractor   <= {R_LOW_MAX}   : {Rii_m:.6f}  -> {c2}")
    print(f"  (3) |R(i)-R(iii)| <= {INDIST_TOL} (indistinct): {abs(Ri_m-Riii_m):.6f}  -> {c3}")
    print(f"  (4) R(iii) real channel    >= {R_CLAIM_BAND}  : {Riii_m:.6f}  -> {c4}")

    reinforced = c1 and c2 and c3 and c4
    print("\n" + "="*82)
    if reinforced:
        print("VERDICT: 🔴 H_1099 R-headline FALSIFIED-reinforced (SIM).")
        print(f"  Two COMPLETELY INDEPENDENT nodes (separate RNG, NO channel) reach")
        print(f"  R = {Ri_m:.6f} ≈ {CLAIMED_R} PURELY by co-convergence to Psi*=0.5.")
        print(f"  The SAME formula gives LOW R = {Rii_m:.4f} when the two nodes converge to")
        print(f"  DIFFERENT attractors — so R is HIGH iff the states are CO-LOCATED, not iff")
        print(f"  they communicate. R(i no-channel)={Ri_m:.6f} ≈ R(iii real-channel)={Riii_m:.6f}")
        print(f"  (|Δ|={abs(Ri_m-Riii_m):.2e}): R CANNOT distinguish co-convergence from")
        print(f"  transmission. The headline 0.99999 is a REAL number but a CO-LOCATION")
        print(f"  metric — NON-DIAGNOSTIC of sync/transmission.")
    else:
        print("VERDICT: inconclusive — investigate checks above.")
    print("="*82)


if __name__ == "__main__":
    main()
