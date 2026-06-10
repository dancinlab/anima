#!/usr/bin/env python3
"""
H_1099 toy falsifier — Gemini 제4명제: "quantum-information-resonance NON-LOCAL sync".

CLAIM (.discoveries/1099): two anima nodes A, B with ZERO input/output between them
achieve non-local synchronization — B "copies" A's 384-dim state via ER=EPR /
Fubini-Study / von-Neumann entropy-lock, R=0.99999, isomorphism-error=7e-6, 0-latency,
NO physical channel.

This $0 CPU pure-numpy TOY upgrades the verdict from ANALYTIC 🔴 to SIM-BACKED 🔴 by
realizing the no-communication theorem numerically. It does NOT engage real quantum
mechanics (a_scale_honest_scope): the claim itself proposes ZERO physical channel, so
the falsification is that NEITHER a classical NOR a quantum channel exists between the
nodes — and with no channel, no signalling is possible (no-communication / no-signalling
theorem). The toy demonstrates that classical co-convergence to a shared attractor
LOOKS like "sync" (high correlation) yet carries NO information (TE(A->B)≈0), while a
REAL channel (positive control) carries information (TE>0).

NODE MODEL (mirrors the Ψ=1/2 repulsion-field homeostasis):
  Each node is a 1-D state psi that relaxes toward the fixed point PSI_STAR=0.5:
      psi_A[t+1] = psi_A[t] + LAM*(PSI_STAR - psi_A[t]) + sigma * eps_A[t]
      psi_B[t+1] = psi_B[t] + LAM*(PSI_STAR - psi_B[t]) + sigma * eps_B[t] + COUP*(psi_A[t]-psi_B[t])
  eps_A, eps_B are INDEPENDENT Gaussian noise (no shared cause).
  LAM = relaxation rate, COUP = A->B coupling (0 in Arm1, >0 in Arm2).

THE FROZEN FALSIFIER (decisive test separating "sync" from "signalling"):
  Correlation != communication. Both nodes pulled to the SAME attractor will look
  synchronized with ZERO coupling — that is co-convergence, not transfer. The
  discriminator is PERTURBATION-RESPONSE + directed transfer-entropy:
    * Arm 1 (ZERO-COUPLING, the claim's setup): COUP=0, no channel A<->B.
        - measure corr(psi_A, psi_B) over the run
        - at t=T_KICK displace psi_A by +KICK; measure mean Δψ_B in the response window
        - measure directed transfer-entropy TE(A->B)
    * Arm 2 (REAL CHANNEL, positive control): COUP>0, B reads A's state.
        - same kick; measure Δψ_B and TE(A->B)
  FROZEN VERDICT: H_1099 is 🔴 FALSIFIED (sim-confirmed) iff
    Arm1: corr possibly HIGH (both->0.5) BUT Δψ_B ≈ 0 AND TE(A->B) ≈ 0, WHILE
    Arm2: Δψ_B > 0 AND TE(A->B) > 0.
  i.e. zero-coupling "non-local sync" is shared-attractor co-convergence, not signalling.
  (If Arm1 showed nonzero TE at truly zero coupling, that would be a BUG — there is no
  physical channel. The positive control proves the test CAN detect transfer.)

Honest scope: classical toy. No real QM. Falsification rests on the no-communication
theorem: with no channel (classical or quantum), no information can cross.
"""

import numpy as np

# ---- frozen params (set before running) -----------------------------------
PSI_STAR  = 0.5      # Ψ=1/2 fixed point
LAM       = 0.10     # relaxation rate toward the attractor
SIGMA     = 0.05     # independent process noise per node
COUP_OFF  = 0.0      # Arm 1: zero coupling (the claim)
COUP_ON   = 0.30     # Arm 2: real channel A->B (positive control)
N_STEPS   = 4000     # length of each run
BURN      = 500      # discard transient before measuring correlation/TE
T_KICK    = 2000     # kick time
KICK      = 5.0      # large displacement applied to psi_A at T_KICK
RESP_WIN  = 50       # response window after the kick to measure Δψ_B
N_SEEDS   = 12       # >= 10 seeds
TE_BINS   = 6        # bins for transfer-entropy histogram estimator
EPS       = 1e-12


def run_pair(seed, coup):
    """Simulate nodes A,B with a kick on A at T_KICK. Returns (psiA, psiB) arrays."""
    rng = np.random.default_rng(seed)
    psiA = np.empty(N_STEPS); psiB = np.empty(N_STEPS)
    # both nodes start FAR from the attractor (~3.0) with independent jitter:
    # they will relax to Ψ*=0.5 together => "looks synchronized" with NO channel.
    a = 3.0 + rng.standard_normal()*0.3; b = 3.0 + rng.standard_normal()*0.3
    for t in range(N_STEPS):
        psiA[t] = a; psiB[t] = b
        epsA = rng.standard_normal(); epsB = rng.standard_normal()
        a_next = a + LAM*(PSI_STAR - a) + SIGMA*epsA
        b_next = b + LAM*(PSI_STAR - b) + SIGMA*epsB + coup*(a - b)
        if t == T_KICK:
            a_next = a_next + KICK   # large displacement on A only
        a, b = a_next, b_next
    return psiA, psiB


def perturbation_response(coup, seeds):
    """Mean Δψ_B in the response window: (B with kick on A) - (B without kick), same noise."""
    deltas = []
    for s in seeds:
        # paired runs: identical noise stream, only the kick differs
        psiA_k, psiB_k = run_pair(s, coup)             # kicked
        psiA_n, psiB_n = run_pair_nokick(s, coup)      # no kick, identical seed/noise
        lo, hi = T_KICK + 1, T_KICK + 1 + RESP_WIN
        d = np.mean(np.abs(psiB_k[lo:hi] - psiB_n[lo:hi]))
        deltas.append(d)
    return np.array(deltas)


def run_pair_nokick(seed, coup):
    rng = np.random.default_rng(seed)
    psiA = np.empty(N_STEPS); psiB = np.empty(N_STEPS)
    a = 3.0 + rng.standard_normal()*0.3; b = 3.0 + rng.standard_normal()*0.3
    for t in range(N_STEPS):
        psiA[t] = a; psiB[t] = b
        epsA = rng.standard_normal(); epsB = rng.standard_normal()
        a_next = a + LAM*(PSI_STAR - a) + SIGMA*epsA
        b_next = b + LAM*(PSI_STAR - b) + SIGMA*epsB + coup*(a - b)
        a, b = a_next, b_next   # NO kick
    return psiA, psiB


def _te_raw(src, dst, bins=TE_BINS):
    """Raw plug-in TE(src->dst), lag-1, in bits (has a positive finite-sample bias)."""
    d_next = dst[1:]; d_past = dst[:-1]; s_past = src[:-1]
    # common bin edges from the pooled range (robust to the kick outlier on src)
    def disc(x, edges):
        return np.clip(np.digitize(x, edges), 0, bins-1)
    e_d = np.quantile(np.concatenate([d_next, d_past]), np.linspace(0, 1, bins+1)[1:-1])
    e_s = np.quantile(s_past, np.linspace(0, 1, bins+1)[1:-1])
    dn = disc(d_next, e_d); dp = disc(d_past, e_d); sp = disc(s_past, e_s)

    n = len(dn)
    # joint counts
    p_dn_dp_sp = np.zeros((bins, bins, bins))
    for i in range(n):
        p_dn_dp_sp[dn[i], dp[i], sp[i]] += 1.0
    p_dn_dp_sp /= n
    p_dp_sp = p_dn_dp_sp.sum(axis=0)          # p(d_t, s_t)
    p_dn_dp = p_dn_dp_sp.sum(axis=2)          # p(d_{t+1}, d_t)
    p_dp    = p_dn_dp.sum(axis=0)             # p(d_t)

    te = 0.0
    for k in range(bins):       # d_next
        for i in range(bins):   # d_past
            for j in range(bins):  # s_past
                pjoint = p_dn_dp_sp[k, i, j]
                if pjoint <= EPS:
                    continue
                # p(d_next | d_past, s_past)
                cond_full = pjoint / (p_dp_sp[i, j] + EPS)
                # p(d_next | d_past)
                cond_red = p_dn_dp[k, i] / (p_dp[i] + EPS)
                if cond_full <= EPS or cond_red <= EPS:
                    continue
                te += pjoint * np.log2(cond_full / cond_red)
    return max(te, 0.0)   # plug-in TE is >=0 up to estimator noise


def transfer_entropy(src, dst, bins=TE_BINS, seed=0, n_surr=20):
    """
    BIAS-CORRECTED directed TE(src->dst) in bits.

    The plug-in (histogram) TE has a strictly positive finite-sample bias: even with
    NO real coupling it reports TE_raw > 0 just from binning noise. To isolate genuine
    directed transfer we subtract a SHUFFLED-SURROGATE baseline: time-shuffle the source,
    which DESTROYS any real directed src->dst relation while preserving the marginals and
    thus the SAME estimator bias. TE_corrected = TE_raw - mean(TE_shuffled). With a true
    channel TE_raw >> surrogate (positive). With no channel TE_raw ≈ surrogate (≈0).
    """
    raw = _te_raw(src, dst, bins)
    rng = np.random.default_rng(seed + 777)
    surr = np.array([_te_raw(rng.permutation(src), dst, bins) for _ in range(n_surr)])
    return raw - surr.mean()


def transfer_entropy_raw(src, dst, bins=TE_BINS):
    return _te_raw(src, dst, bins)


def arm(coup, label):
    seeds = list(range(100, 100 + N_SEEDS))
    corrs, tes, tes_raw = [], [], []
    coconv = []   # correlation INCLUDING the shared-attractor descent transient
    for s in seeds:
        psiA, psiB = run_pair_nokick(s, coup)   # measure corr/TE on un-kicked dynamics
        a = psiA[BURN:]; b = psiB[BURN:]
        c = np.corrcoef(a, b)[0, 1]
        corrs.append(c)
        # co-convergence corr: both nodes start far from 0.5 and relax together.
        # Over the FULL trajectory (incl. transient) they look "synchronized" with NO channel.
        coconv.append(np.corrcoef(psiA[:300], psiB[:300])[0, 1])
        tes.append(transfer_entropy(a, b, seed=s))      # bias-corrected (surrogate-subtracted)
        tes_raw.append(transfer_entropy_raw(a, b))       # raw plug-in (biased)
    deltas = perturbation_response(coup, seeds)
    corrs = np.array(corrs); tes = np.array(tes); tes_raw = np.array(tes_raw)
    coconv = np.array(coconv)
    return dict(label=label, coup=coup,
                corr=corrs, coconv=coconv, te=tes, te_raw=tes_raw, dpsi=deltas)


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


def main():
    np.seterr(all="ignore")
    print("="*78)
    print("H_1099 toy — quantum-information-resonance NON-LOCAL sync (제4명제)")
    print(f"  PSI*={PSI_STAR} LAM={LAM} SIGMA={SIGMA} N_STEPS={N_STEPS} seeds={N_SEEDS}")
    print(f"  kick={KICK}@t={T_KICK} resp_win={RESP_WIN} | COUP off={COUP_OFF} on={COUP_ON}")
    print("="*78)

    a1 = arm(COUP_OFF, "Arm1 ZERO-COUPLING (the claim: no channel A<->B)")
    a2 = arm(COUP_ON,  "Arm2 REAL CHANNEL  (positive control: B reads A)")

    print(f"\n{'metric':<26}{'Arm1 (coup=0)':>26}{'Arm2 (coup=%.2f)'%COUP_ON:>26}")
    print("-"*78)
    print(f"{'corr co-converge (transient)':<26}{fmt(a1['coconv']):>26}{fmt(a2['coconv']):>26}")
    print(f"{'corr steady-state':<26}{fmt(a1['corr']):>26}{fmt(a2['corr']):>26}")
    print(f"{'Δψ_B (kick response)':<26}{fmt(a1['dpsi']):>26}{fmt(a2['dpsi']):>26}")
    print(f"{'TE raw [bits] (biased)':<26}{fmt(a1['te_raw']):>26}{fmt(a2['te_raw']):>26}")
    print(f"{'TE(A->B) bias-corr [bits]':<26}{fmt(a1['te']):>26}{fmt(a2['te']):>26}")
    print("-"*78)
    print("  (TE raw has a +bias from finite-sample binning; the surrogate-subtracted")
    print("   TE(A->B) is the honest directed-transfer estimate. Δψ_B in Arm2 is identical")
    print("   across seeds because the linear kick-response is noise-independent — correct.)")

    # per-seed dump for audit
    print("\nper-seed (seed: corr / Δψ_B / TE bits):")
    for i in range(N_SEEDS):
        print(f"  Arm1 s{100+i:>3}: corr={a1['corr'][i]:+.4f}  dB={a1['dpsi'][i]:.2e}  TE={a1['te'][i]:.4f}"
              f"   | Arm2: corr={a2['corr'][i]:+.4f}  dB={a2['dpsi'][i]:.4f}  TE={a2['te'][i]:.4f}")

    # ---- frozen verdict evaluation (bias-corrected TE) ----
    arm1_dpsi = np.mean(a1['dpsi']); arm2_dpsi = np.mean(a2['dpsi'])
    arm1_te   = np.mean(a1['te']);   arm2_te   = np.mean(a2['te'])     # surrogate-subtracted

    TE_NULL_MAX   = 0.01      # |Arm1 corrected TE| <= 0.01 bits => "≈0" (no channel)
    TE_CHAN_MIN   = 0.05      # Arm2 corrected TE must exceed this => real transfer
    DPSI_NULL_MAX = 1e-6      # Arm1 Δψ_B must be essentially 0 (kick cannot reach B)
    DPSI_CHAN_MIN = 1e-3      # Arm2 Δψ_B must be materially positive

    c1 = abs(arm1_dpsi) <= DPSI_NULL_MAX
    c2 = abs(arm1_te)   <= TE_NULL_MAX
    c3 = arm2_te        >= TE_CHAN_MIN
    c4 = arm2_dpsi      >= DPSI_CHAN_MIN

    print("\nFROZEN falsifier checks (bias-corrected TE):")
    print(f"  (1) Arm1 Δψ_B≈0  : |{arm1_dpsi:.3e}| <= {DPSI_NULL_MAX:.0e}   -> {c1}")
    print(f"  (2) Arm1 TE≈0    : |{arm1_te:+.4f}| <= {TE_NULL_MAX}        -> {c2}")
    print(f"  (3) Arm2 TE>0    : {arm2_te:+.4f} >= {TE_CHAN_MIN}          -> {c3}")
    print(f"  (4) Arm2 Δψ_B>0  : {arm2_dpsi:.4f} >= {DPSI_CHAN_MIN}      -> {c4}")

    falsified = c1 and c2 and c3 and c4
    print("\n" + "="*78)
    if falsified:
        print("VERDICT: 🔴 H_1099 FALSIFIED (SIM-CONFIRMED).")
        print("  Zero-coupling 'non-local sync' = shared-attractor CO-CONVERGENCE:")
        print(f"  Arm1 corr={np.mean(a1['corr']):+.3f} but Δψ_B={arm1_dpsi:.1e} and TE(A->B)={arm1_te:+.4f}≈0 —")
        print("  A's manipulation carries NO information to B. The REAL channel (Arm2)")
        print(f"  DOES transfer (Δψ_B={arm2_dpsi:.3f}, TE={arm2_te:+.3f} bits). No-communication")
        print("  theorem realized numerically: correlation != communication.")
    else:
        print("VERDICT: test inconclusive — investigate (see checks above).")
    print("="*78)


if __name__ == "__main__":
    main()
