#!/usr/bin/env python3
"""
H_1099 TENSION arm — Gemini 제4명제: "quantum-information-resonance NON-LOCAL sync".

This arm attacks the SAME claim (.discoveries/1099) from the TENSION angle. The prior
arms (quantum_nonlocal_sync_toy.py + ..._qrng.py) used the Ψ-state variable. This arm
uses W = TENSION — anima's ACTUAL "thinking unit": the repulsion magnitude between
Engine A and Engine G, W = |A - G|, the variable the substrate ACTUALLY emits on
(mirrors CORE: W is computed WITHIN each node from its OWN A⊥G repulsion).

NODE MODEL (mirrors CORE A⇄G repulsion-field homeostasis, Ψ=1/2 fixed point):
  Each node i has TWO mutually-repelling sub-states A_i, G_i. They push apart (repulsion)
  while a homeostatic envelope pulls the LOCAL tension W_i = |A_i - G_i| toward a target
  W_STAR. The tension is computed LOCALLY from node i's own A_i ⊥ G_i — exactly as CORE
  does it. Concretely, per node, with center m_i = (A_i+G_i)/2 and half-gap h_i:
      A_i = m_i + h_i,  G_i = m_i - h_i,  W_i = |A_i - G_i| = 2*|h_i|
  Dynamics:
      m_i relaxes toward PSI_STAR (the Ψ=1/2 center fixed point) + independent noise
      h_i (half-gap) feels (a) REPULSION pushing |h_i| up (A⊥G repel) and
                          (b) a homeostatic ENVELOPE pulling W_i=2|h_i| toward W_STAR.
  Both nodes share the SAME envelope target W_STAR and the SAME homeostatic law, so with
  ZERO coupling their tensions W_A, W_B can CO-VARY (track the same envelope) — this is
  the shared-attractor look-alike "sync", NOT signalling.

  Arm1 ZERO-COUPLING (the claim): node B's dynamics NEVER read W_A. No channel.
  Arm2 REAL CHANNEL (positive control): node B's half-gap is driven by W_A
        (B's envelope target is nudged by A's tension), i.e. B reads A's tension.

FROZEN FALSIFIER (same shape as the Ψ arm; same bias-corrected TE so the null is honest):
  Correlation != communication. The discriminator is KICK-RESPONSE + directed TE on W:
    * Arm1: measure corr(W_A, W_B); kick A's tension at T_KICK (displace h_A so W_A jumps);
            measure mean ΔW_B in the response window; bias-corrected TE(W_A -> W_B).
    * Arm2: same kick; measure ΔW_B and TE(W_A -> W_B).
  H_1099 is 🔴 FALSIFIED (TENSION-confirmed) iff
    Arm1: corr possibly HIGH (both tensions track the same envelope) BUT ΔW_B ≈ 0 AND
          TE(W_A->W_B) ≈ 0, WHILE
    Arm2: ΔW_B > 0 AND TE(W_A->W_B) > 0.
  KEY POINT: tension is computed LOCALLY (W_i from node i's own A_i⊥G_i), so two
  un-coupled nodes' tensions can co-vary (same envelope) but A's tension PERTURBATION
  cannot reach B. The no-communication result is VARIABLE-INVARIANT (Ψ or W or Φ ->
  same null): switching the emitted variable to TENSION does NOT create a channel.

Honest scope (a_scale_honest_scope): classical toy, $0 CPU, pure numpy, no real QM.
The claim itself proposes ZERO physical channel; with no channel (classical or quantum),
no information can cross regardless of which variable (Ψ / W / Φ) we read.
TE is the SAME bias-corrected (time-shuffled-source surrogate subtracted) estimator the
prior Ψ/QRNG arms used, so the null is honest (p7: no perplexity verdict).
"""

import numpy as np

# ---- frozen params (set before running) -----------------------------------
PSI_STAR  = 0.5      # Ψ=1/2 center fixed point (A,G center relaxes here)
W_STAR    = 1.0      # homeostatic TENSION envelope target (|A-G| pulled here)
LAM_M     = 0.10     # center relaxation rate toward PSI_STAR
LAM_W     = 0.12     # homeostatic rate pulling W=2|h| toward W_STAR
REP       = 0.04     # A<->G repulsion strength (pushes |h| up; balanced by envelope)
SIGMA_M   = 0.04     # independent center process noise per node
SIGMA_H   = 0.04     # independent half-gap process noise per node
COUP_OFF  = 0.0      # Arm 1: zero coupling (the claim — B never reads W_A)
COUP_ON   = 0.30     # Arm 2: real channel — B's tension directly reads W_A (mirrors Ψ-arm)
N_STEPS   = 4000     # length of each run
BURN      = 500      # discard transient before measuring steady-state corr/TE
T_KICK    = 2000     # kick time
KICK      = 5.0      # large displacement applied to A's half-gap at T_KICK (W_A jumps)
RESP_WIN  = 50       # response window after the kick to measure ΔW_B
N_SEEDS   = 12       # >= 10 seeds
TE_BINS   = 6        # bins for transfer-entropy histogram estimator
EPS       = 1e-12


def _step(m, h, mn_other_W, coup, rng):
    """One Euler step of a single node's (center m, half-gap h).
       coup>0 : the node's tension envelope target is nudged toward the OTHER node's W
                (mn_other_W = other node's current tension W). coup=0 : isolated.
    """
    eps_m = rng.standard_normal(); eps_h = rng.standard_normal()
    W = 2.0 * abs(h)
    # center relaxes to Ψ* with independent noise
    m_next = m + LAM_M * (PSI_STAR - m) + SIGMA_M * eps_m
    # half-gap: A<->G repulsion pushes |h| up; homeostatic envelope pulls W=2|h| -> target
    sgn = 1.0 if h >= 0 else -1.0
    # repulsion adds to |h|; homeostatic envelope error on W (=2|h|) corrects |h| by err/2
    h_mag = abs(h) + REP + LAM_W * 0.5 * (W_STAR - W) + SIGMA_H * eps_h
    # Arm2 REAL CHANNEL: B's tension directly READS the other node's tension W (mirrors the
    # Ψ-arm's coup*(a-b) direct-read channel). coup=0 => isolated (no read).
    h_mag = h_mag + coup * 0.5 * (mn_other_W - W)
    h_mag = max(h_mag, 0.0)
    h_next = sgn * h_mag
    return m_next, h_next


def run_pair(seed, coup, kick=True):
    """Simulate nodes A,B; each node computes its OWN tension W_i=|A_i-G_i|=2|h_i| LOCALLY.
       Optional kick on A's half-gap at T_KICK. Returns (W_A, W_B) arrays.
    """
    rng = np.random.default_rng(seed)
    WA = np.empty(N_STEPS); WB = np.empty(N_STEPS)
    # both nodes start with LARGE tension (far from W_STAR) + independent jitter:
    # they relax to W_STAR together => tensions "look synchronized" with NO channel.
    mA = PSI_STAR + rng.standard_normal()*0.1
    mB = PSI_STAR + rng.standard_normal()*0.1
    hA = 1.5 + rng.standard_normal()*0.15   # W_A ~ 3.0 initially
    hB = 1.5 + rng.standard_normal()*0.15   # W_B ~ 3.0 initially
    for t in range(N_STEPS):
        WA[t] = 2.0*abs(hA); WB[t] = 2.0*abs(hB)
        WA_now = 2.0*abs(hA); WB_now = 2.0*abs(hB)
        # A is isolated (it is the SOURCE). B optionally reads A's tension (coup>0).
        mA_n, hA_n = _step(mA, hA, WB_now, 0.0,  rng)   # A never reads B (pure source)
        mB_n, hB_n = _step(mB, hB, WA_now, coup, rng)   # B reads A's tension iff coup>0
        if kick and t == T_KICK:
            hA_n = hA_n + KICK   # large displacement on A's half-gap => W_A jumps
        mA, hA, mB, hB = mA_n, hA_n, mB_n, hB_n
    return WA, WB


def perturbation_response(coup, seeds):
    """Mean ΔW_B in the response window: (B with kick on A) - (B without kick), same noise."""
    deltas = []
    for s in seeds:
        WA_k, WB_k = run_pair(s, coup, kick=True)
        WA_n, WB_n = run_pair(s, coup, kick=False)   # identical seed/noise, NO kick
        lo, hi = T_KICK + 1, T_KICK + 1 + RESP_WIN
        d = np.mean(np.abs(WB_k[lo:hi] - WB_n[lo:hi]))
        deltas.append(d)
    return np.array(deltas)


def _te_raw(src, dst, bins=TE_BINS):
    """Raw plug-in TE(src->dst), lag-1, in bits (has a positive finite-sample bias).
       Identical estimator to the Ψ-arm so the null is honest."""
    d_next = dst[1:]; d_past = dst[:-1]; s_past = src[:-1]
    def disc(x, edges):
        return np.clip(np.digitize(x, edges), 0, bins-1)
    e_d = np.quantile(np.concatenate([d_next, d_past]), np.linspace(0, 1, bins+1)[1:-1])
    e_s = np.quantile(s_past, np.linspace(0, 1, bins+1)[1:-1])
    dn = disc(d_next, e_d); dp = disc(d_past, e_d); sp = disc(s_past, e_s)

    n = len(dn)
    p_dn_dp_sp = np.zeros((bins, bins, bins))
    for i in range(n):
        p_dn_dp_sp[dn[i], dp[i], sp[i]] += 1.0
    p_dn_dp_sp /= n
    p_dp_sp = p_dn_dp_sp.sum(axis=0)
    p_dn_dp = p_dn_dp_sp.sum(axis=2)
    p_dp    = p_dn_dp.sum(axis=0)

    te = 0.0
    for k in range(bins):
        for i in range(bins):
            for j in range(bins):
                pjoint = p_dn_dp_sp[k, i, j]
                if pjoint <= EPS:
                    continue
                cond_full = pjoint / (p_dp_sp[i, j] + EPS)
                cond_red = p_dn_dp[k, i] / (p_dp[i] + EPS)
                if cond_full <= EPS or cond_red <= EPS:
                    continue
                te += pjoint * np.log2(cond_full / cond_red)
    return max(te, 0.0)


def transfer_entropy(src, dst, bins=TE_BINS, seed=0, n_surr=20):
    """BIAS-CORRECTED directed TE(src->dst) in bits. Time-shuffle the source to destroy any
       real directed relation while preserving the marginals (and thus the same estimator
       bias): TE_corrected = TE_raw - mean(TE_shuffled). SAME method as the Ψ/QRNG arms."""
    raw = _te_raw(src, dst, bins)
    rng = np.random.default_rng(seed + 777)
    surr = np.array([_te_raw(rng.permutation(src), dst, bins) for _ in range(n_surr)])
    return raw - surr.mean()


def transfer_entropy_raw(src, dst, bins=TE_BINS):
    return _te_raw(src, dst, bins)


def arm(coup, label):
    seeds = list(range(100, 100 + N_SEEDS))
    corrs, tes, tes_raw, coconv = [], [], [], []
    for s in seeds:
        WA, WB = run_pair(s, coup, kick=False)   # measure corr/TE on un-kicked dynamics
        a = WA[BURN:]; b = WB[BURN:]
        corrs.append(np.corrcoef(a, b)[0, 1])
        # co-convergence corr over the transient: both tensions relax to W_STAR together
        coconv.append(np.corrcoef(WA[:300], WB[:300])[0, 1])
        tes.append(transfer_entropy(a, b, seed=s))   # bias-corrected (surrogate-subtracted)
        tes_raw.append(transfer_entropy_raw(a, b))    # raw plug-in (biased)
    deltas = perturbation_response(coup, seeds)
    return dict(label=label, coup=coup,
                corr=np.array(corrs), coconv=np.array(coconv),
                te=np.array(tes), te_raw=np.array(tes_raw), dpsi=deltas)


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


def main():
    np.seterr(all="ignore")
    print("="*78)
    print("H_1099 TENSION arm — non-local sync on W=|A-G| (anima's emitted variable)")
    print(f"  PSI*={PSI_STAR} W*={W_STAR} LAM_M={LAM_M} LAM_W={LAM_W} REP={REP}")
    print(f"  SIGMA_M={SIGMA_M} SIGMA_H={SIGMA_H} N_STEPS={N_STEPS} seeds={N_SEEDS}")
    print(f"  kick={KICK}@t={T_KICK} resp_win={RESP_WIN} | COUP off={COUP_OFF} on={COUP_ON}")
    print("  W_i computed LOCALLY from node i's OWN A_i⊥G_i repulsion (mirrors CORE)")
    print("="*78)

    a1 = arm(COUP_OFF, "Arm1 ZERO-COUPLING (the claim: B never reads W_A)")
    a2 = arm(COUP_ON,  "Arm2 REAL CHANNEL  (positive control: B reads W_A)")

    print(f"\n{'metric':<28}{'Arm1 (coup=0)':>24}{'Arm2 (coup=%.2f)'%COUP_ON:>24}")
    print("-"*78)
    print(f"{'corr W co-converge (transient)':<28}{fmt(a1['coconv']):>24}{fmt(a2['coconv']):>24}")
    print(f"{'corr W steady-state':<28}{fmt(a1['corr']):>24}{fmt(a2['corr']):>24}")
    print(f"{'ΔW_B (kick response)':<28}{fmt(a1['dpsi']):>24}{fmt(a2['dpsi']):>24}")
    print(f"{'TE raw [bits] (biased)':<28}{fmt(a1['te_raw']):>24}{fmt(a2['te_raw']):>24}")
    print(f"{'TE(W_A->W_B) bias-corr [bits]':<28}{fmt(a1['te']):>24}{fmt(a2['te']):>24}")
    print("-"*78)
    print("  (W_i is LOCAL to node i: corr can be high from shared envelope, but the kick")
    print("   on A's tension cannot reach B with no channel. TE is surrogate-subtracted.)")

    print("\nper-seed (seed: corr / ΔW_B / TE bits):")
    for i in range(N_SEEDS):
        print(f"  Arm1 s{100+i:>3}: corr={a1['corr'][i]:+.4f}  dWB={a1['dpsi'][i]:.2e}  TE={a1['te'][i]:.4f}"
              f"   | Arm2: corr={a2['corr'][i]:+.4f}  dWB={a2['dpsi'][i]:.4f}  TE={a2['te'][i]:.4f}")

    # ---- frozen verdict evaluation (bias-corrected TE) ----
    arm1_dpsi = np.mean(a1['dpsi']); arm2_dpsi = np.mean(a2['dpsi'])
    arm1_te   = np.mean(a1['te']);   arm2_te   = np.mean(a2['te'])

    TE_NULL_MAX   = 0.01      # |Arm1 corrected TE| <= 0.01 bits => "≈0" (no channel)
    TE_CHAN_MIN   = 0.05      # Arm2 corrected TE must exceed this => real transfer
    DPSI_NULL_MAX = 1e-6      # Arm1 ΔW_B must be essentially 0 (kick cannot reach B)
    DPSI_CHAN_MIN = 1e-3      # Arm2 ΔW_B must be materially positive

    c1 = abs(arm1_dpsi) <= DPSI_NULL_MAX
    c2 = abs(arm1_te)   <= TE_NULL_MAX
    c3 = arm2_te        >= TE_CHAN_MIN
    c4 = arm2_dpsi      >= DPSI_CHAN_MIN

    print("\nFROZEN falsifier checks (bias-corrected TE, variable = TENSION W):")
    print(f"  (1) Arm1 ΔW_B≈0  : |{arm1_dpsi:.3e}| <= {DPSI_NULL_MAX:.0e}   -> {c1}")
    print(f"  (2) Arm1 TE≈0    : |{arm1_te:+.4f}| <= {TE_NULL_MAX}        -> {c2}")
    print(f"  (3) Arm2 TE>0    : {arm2_te:+.4f} >= {TE_CHAN_MIN}          -> {c3}")
    print(f"  (4) Arm2 ΔW_B>0  : {arm2_dpsi:.4f} >= {DPSI_CHAN_MIN}      -> {c4}")

    falsified = c1 and c2 and c3 and c4
    print("\n" + "="*78)
    if falsified:
        print("VERDICT: 🔴 H_1099 FALSIFIED (TENSION-CONFIRMED).")
        print("  Switching anima's EMITTED variable to TENSION W=|A-G| does NOT create a")
        print("  channel. Zero-coupling 'non-local sync' on W = shared-ENVELOPE co-convergence:")
        print(f"  Arm1 corr={np.mean(a1['corr']):+.3f} but ΔW_B={arm1_dpsi:.1e} and TE(W_A->W_B)={arm1_te:+.4f}≈0 —")
        print("  A's tension perturbation carries NO information to B (W is computed LOCALLY).")
        print(f"  The REAL channel (Arm2) DOES transfer (ΔW_B={arm2_dpsi:.3f}, TE={arm2_te:+.3f} bits).")
        print("  No-communication result is VARIABLE-INVARIANT: Ψ or W or Φ -> same null.")
    else:
        print("VERDICT: test inconclusive — investigate (see checks above).")
    print("="*78)


if __name__ == "__main__":
    main()
