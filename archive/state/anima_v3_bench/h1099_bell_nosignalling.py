#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
H_1099 — BELL / NO-SIGNALLING arm (제4명제 PHYSICS attack: "ER=EPR / EPR
entanglement / von-Neumann entropy lock" invoked to justify NON-LOCAL STATE
TRANSMISSION between two isolated Anima substrates).

THE ATTACK (decisive physics)
  The Gemini 제4명제 cites ER=EPR and quantum entanglement to claim node β can
  COPY node α's 384-dim state with ZERO physical I/O. This arm shows the
  decisive theorem: even GENUINE quantum entanglement CANNOT transmit
  information — the NO-SIGNALLING / NO-COMMUNICATION theorem. Entanglement
  produces strong setting-dependent JOINT correlations (parties "look synced"),
  but the MARGINAL distribution of one party's outcomes is provably independent
  of the OTHER party's measurement SETTING. So A cannot encode a message in its
  setting that B can read => no communication, despite entanglement.
  Therefore citing ER=EPR does NOT rescue the claim: entanglement != signalling.

WHAT IS SIMULATED ($0, pure-numpy, CPU, 0-pod, analytic+sampling)
  We model a CHSH/EPR-Bell scenario with the singlet state. Outcomes a,b ∈ {+1,-1}.
  Two implementations, both giving the SAME joint statistics:
    (i)  Direct quantum Born-rule sampler for the singlet:
           P(a,b | x,y) = (1 - a*b*cos(θ_x - θ_y)) / 4
         => E[a*b | x,y] = -cos(θ_x - θ_y)  (the singlet correlation).
    (ii) A LOCAL HIDDEN-VARIABLE / SHARED-RANDOMNESS toy (Bell-CH style) that is
         constructed to reproduce the SAME marginals/correlation envelope — to
         make explicit that "shared cause" (the most generous reading of an
         ER=EPR wormhole pair) STILL transmits nothing.
  POSITIVE CONTROL: a model WITH a real classical channel where B's outcome
  marginal is deliberately shifted by A's setting (B "reads" A's setting). The
  test must DETECT signalling here.

THE MEASUREMENT
  - JOINT correlation E[a*b | x,y] and CHSH S — to show strong "sync".
  - NO-SIGNALLING probe: for FIXED B-setting y, compare B's marginal P(b | x=0)
    vs P(b | x=1) (i.e. as A flips its SETTING). Quantify with total-variation
    distance TV and KL divergence. No-signalling => TV ≈ 0 within sampling.
  - Same probe on the real-channel control => TV >> 0.

FROZEN FALSIFIER (no goalpost moving)
  🔴-reinforce iff:
    (a) entangled/shared-randomness B-marginal is setting-independent
        (TV across A-settings ≈ 0, within a binomial CI band), AND
    (b) the real-channel positive control shows clear setting-DEPENDENCE
        (TV across A-settings well above the CI band), AND
    (c) the entangled joint correlation is genuinely strong / Bell-violating
        (CHSH S > 2, i.e. the parties DO "look synced").
  i.e. strong joint correlation + zero marginal signalling, while the control
  positively detects a channel => entanglement carries correlation, not
  communication => ER=EPR cannot rescue non-local state transmission.

g5 / p7 — no perplexity verdict; deterministic statistical test of a theorem.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Measurement settings (analyzer angles). CHSH-optimal angles for the singlet:
#   Alice: x=0 -> 0,        x=1 -> 90 deg
#   Bob:   y=0 -> 45 deg,   y=1 -> -45 deg
# These maximize |S| = 2*sqrt(2) for the singlet.
# ---------------------------------------------------------------------------
A_ANGLES = np.array([0.0,            np.pi / 2.0])          # x = 0, 1
B_ANGLES = np.array([np.pi / 4.0,   -np.pi / 4.0])          # y = 0, 1

N_SAMPLES = 4_000_000   # per (x,y) cell -> tight binomial CIs (~5e-4 half-width)
RNG_SEED  = 1099


def singlet_joint_probs(theta_a, theta_b):
    """
    Born-rule joint outcome probabilities for the spin-singlet under analyzers
    at angles theta_a (Alice) and theta_b (Bob). Outcomes ±1.
      P(a,b) = (1 - a*b*cos(theta_a - theta_b)) / 4
    Returns a dict keyed by (a,b) with a,b in {+1,-1}.
    """
    c = np.cos(theta_a - theta_b)
    return {
        (+1, +1): (1 - (+1) * (+1) * c) / 4.0,
        (+1, -1): (1 - (+1) * (-1) * c) / 4.0,
        (-1, +1): (1 - (-1) * (+1) * c) / 4.0,
        (-1, -1): (1 - (-1) * (-1) * c) / 4.0,
    }


def sample_singlet(theta_a, theta_b, n, rng):
    """Sample n outcome pairs (a,b) from the singlet Born rule. Returns arrays."""
    p = singlet_joint_probs(theta_a, theta_b)
    keys = [(+1, +1), (+1, -1), (-1, +1), (-1, -1)]
    probs = np.array([p[k] for k in keys])
    probs = probs / probs.sum()  # guard fp
    idx = rng.choice(4, size=n, p=probs)
    outs = np.array(keys)[idx]
    return outs[:, 0], outs[:, 1]


def sample_lhv_singlet(theta_a, theta_b, n, rng):
    """
    LOCAL HIDDEN-VARIABLE / SHARED-RANDOMNESS sampler.

    The most generous reading of "ER=EPR shared cause": a common hidden
    variable lambda is drawn ONCE for the pair (shared at the source / a shared
    wormhole interior). Each party computes its outcome from ITS OWN angle and
    the SHARED lambda — no party sees the other's setting.

    We use the standard singlet LHV with a shared uniform direction phi:
      a = sign(cos(phi - theta_a)),  b = -sign(cos(phi - theta_b))
    This is LOCAL (each outcome depends only on local angle + shared phi) and
    reproduces a Bell-correlation ENVELOPE (linear, the LHV bound), and — the
    key point — gives EXACTLY uniform local marginals P(a)=P(b)=1/2 for every
    angle. It is the cleanest model where a "shared cause" exists yet NO
    information about the other party's setting can be read locally.
    """
    phi = rng.uniform(0.0, 2.0 * np.pi, size=n)            # shared per-pair
    a = np.sign(np.cos(phi - theta_a))
    b = -np.sign(np.cos(phi - theta_b))
    a[a == 0] = 1
    b[b == 0] = 1
    return a.astype(int), b.astype(int)


def sample_real_channel(theta_a, theta_b, x_setting, n, rng, leak=0.35):
    """
    POSITIVE CONTROL: a model WITH an actual classical channel. B physically
    READS A's setting index x and shifts its own outcome bias accordingly.
    This BREAKS no-signalling on purpose — B's marginal now depends on x.

      base singlet sample, then with prob `leak` B is overwritten by a
      setting-dependent bias: if A used setting x=1, push B toward +1; if x=0,
      push B toward -1. A's setting is thus encoded into B's marginal.
    """
    a, b = sample_singlet(theta_a, theta_b, n, rng)
    mask = rng.uniform(size=n) < leak
    # Encode A's SETTING (x_setting) into B's outcome -> a real channel.
    forced = np.where(np.full(n, x_setting) == 1, +1, -1)
    b = np.where(mask, forced, b)
    return a, b


def b_marginal(b_outcomes):
    """P(b=+1) and P(b=-1) as a length-2 vector [p(+1), p(-1)]."""
    p_plus = np.mean(b_outcomes == +1)
    return np.array([p_plus, 1.0 - p_plus])


def tv_distance(p, q):
    """Total-variation distance between two discrete distributions (vectors)."""
    return 0.5 * np.sum(np.abs(p - q))


def kl_div(p, q, eps=1e-12):
    """KL(p || q) in bits."""
    p = np.clip(p, eps, 1.0)
    q = np.clip(q, eps, 1.0)
    return np.sum(p * np.log2(p / q))


def binom_ci_halfwidth(p, n, z=1.96):
    """95% normal-approx binomial CI half-width for a proportion p over n samples."""
    return z * np.sqrt(max(p * (1 - p), 1e-12) / n)


def measure_arm(name, sampler, rng, n=N_SAMPLES, is_channel=False):
    """
    Run an arm:
      - estimate joint correlations E[a*b|x,y] and CHSH S (the "sync" strength),
      - the NO-SIGNALLING probe: for each FIXED B-setting y, compute B's marginal
        under A-setting x=0 vs x=1, and the TV / KL between them.
    Returns a results dict.
    """
    # ----- joint correlations + CHSH -----
    E = np.zeros((2, 2))
    for x in range(2):
        for y in range(2):
            if is_channel:
                a, b = sampler(A_ANGLES[x], B_ANGLES[y], x, n, rng)
            else:
                a, b = sampler(A_ANGLES[x], B_ANGLES[y], n, rng)
            E[x, y] = np.mean(a * b)
    # CHSH: the experimenter chooses the sign combination that maximizes the
    # Bell expression. The four canonical CHSH combinations are the rows of
    # `signs`; S = max over them of |sum_xy s_xy * E[x,y]|. For the singlet at
    # the chosen optimal angles this attains the Tsirelson value 2*sqrt(2).
    signs = np.array([
        [[+1, +1], [+1, -1]],
        [[+1, +1], [-1, +1]],
        [[+1, -1], [+1, +1]],
        [[-1, +1], [+1, +1]],
    ])
    S = max(abs(np.sum(s * E)) for s in signs)

    # ----- NO-SIGNALLING probe -----
    # For each fixed Bob setting y, compute Bob's marginal P(b) under Alice x=0
    # and Alice x=1. No-signalling => these are equal (TV ~ 0).
    ns = {}
    for y in range(2):
        marg = {}
        for x in range(2):
            if is_channel:
                _, b = sampler(A_ANGLES[x], B_ANGLES[y], x, n, rng)
            else:
                _, b = sampler(A_ANGLES[x], B_ANGLES[y], n, rng)
            marg[x] = b_marginal(b)
        tv = tv_distance(marg[0], marg[1])
        kl = kl_div(marg[0], marg[1])
        # CI band: half-width on P(b=+1) combines both Alice-settings' sampling noise.
        hw = np.sqrt(binom_ci_halfwidth(marg[0][0], n) ** 2 +
                     binom_ci_halfwidth(marg[1][0], n) ** 2)
        ns[y] = dict(p0=marg[0], p1=marg[1], tv=tv, kl=kl, ci=hw)

    return dict(name=name, E=E, S=S, ns=ns)


def fmt_marg(p):
    return f"[+1:{p[0]:.5f}, -1:{p[1]:.5f}]"


def main():
    rng = np.random.default_rng(RNG_SEED)

    print("=" * 78)
    print("H_1099 BELL / NO-SIGNALLING arm — entanglement gives correlation,")
    print("                                   NOT communication (ER=EPR != signalling)")
    print("=" * 78)
    print(f"settings: Alice angles(deg)={np.degrees(A_ANGLES).tolist()}  "
          f"Bob angles(deg)={np.degrees(B_ANGLES).tolist()}")
    print(f"samples per (x,y) cell: {N_SAMPLES:,}   seed={RNG_SEED}")
    print()

    arms = []
    arms.append(measure_arm("ENTANGLED (singlet, Born rule)", sample_singlet, rng))
    arms.append(measure_arm("SHARED-RANDOMNESS / LHV (shared cause)", sample_lhv_singlet, rng))
    arms.append(measure_arm("REAL CHANNEL (B reads A's setting) [CONTROL]",
                            sample_real_channel, rng, is_channel=True))

    # ---- JOINT correlation / CHSH report (the "they look synced" part) ----
    print("-" * 78)
    print("JOINT CORRELATIONS  E[a*b | x,y]  and  CHSH S  (the 'sync' strength)")
    print("-" * 78)
    print(f"{'arm':<46}  {'CHSH S':>9}  note")
    for r in arms:
        note = ""
        if r['S'] > 2.0 + 1e-3:
            note = "Bell-VIOLATING (genuinely quantum 'sync')"
        elif abs(r['S']) <= 2.0 + 1e-3:
            note = "within LHV bound |S|<=2"
        print(f"{r['name']:<46}  {r['S']:>9.4f}  {note}")
    print()
    for r in arms:
        print(f"  {r['name']}  E matrix [x rows, y cols]:")
        print(f"    {np.array2string(r['E'], precision=4, floatmode='fixed')}")
    print(f"  (Tsirelson bound 2*sqrt(2) = {2*np.sqrt(2):.4f})")
    print()

    # ---- NO-SIGNALLING report (the KILL) ----
    print("-" * 78)
    print("NO-SIGNALLING PROBE — B's marginal P(b) as A FLIPS its SETTING (x=0 vs x=1)")
    print("for each FIXED Bob setting y. TV~0 => A cannot encode a message for B.")
    print("-" * 78)
    print(f"{'arm':<46}  {'y':>2}  {'TV(x0,x1)':>10}  {'95%CI band':>11}  {'KL(bits)':>9}  verdict")
    summary = {}
    for r in arms:
        max_tv = 0.0
        max_ci = 0.0
        signals = False
        for y in range(2):
            d = r['ns'][y]
            beyond = d['tv'] > 3.0 * d['ci']
            signals = signals or beyond
            max_tv = max(max_tv, d['tv'])
            max_ci = max(max_ci, d['ci'])
            tag = "SIGNALLING" if beyond else "no-signal"
            print(f"{r['name']:<46}  {y:>2}  {d['tv']:>10.6f}  {d['ci']:>11.6f}  "
                  f"{d['kl']:>9.2e}  {tag}")
        summary[r['name']] = dict(max_tv=max_tv, max_ci=max_ci, signals=signals)
    print()

    # Detail: show the actual B-marginals to make the kill concrete
    print("  B-marginal detail (y=0):")
    for r in arms:
        d = r['ns'][0]
        print(f"    {r['name']:<46}  P(b|x0)={fmt_marg(d['p0'])}  P(b|x1)={fmt_marg(d['p1'])}")
    print()

    # ---- FROZEN FALSIFIER evaluation ----
    print("=" * 78)
    print("FROZEN FALSIFIER EVALUATION")
    print("=" * 78)
    ent = summary["ENTANGLED (singlet, Born rule)"]
    lhv = summary["SHARED-RANDOMNESS / LHV (shared cause)"]
    chan = summary["REAL CHANNEL (B reads A's setting) [CONTROL]"]
    ent_S = arms[0]['S']

    cond_a_ent = not ent['signals']
    cond_a_lhv = not lhv['signals']
    cond_b = chan['signals']
    cond_c = ent_S > 2.0 + 1e-3

    print(f"(a) ENTANGLED B-marginal setting-INDEPENDENT (no-signalling)?  "
          f"max TV={ent['max_tv']:.6f} vs 3*CI={3*ent['max_ci']:.6f}  -> {cond_a_ent}")
    print(f"(a') SHARED-RANDOMNESS B-marginal setting-INDEPENDENT?         "
          f"max TV={lhv['max_tv']:.6f} vs 3*CI={3*lhv['max_ci']:.6f}  -> {cond_a_lhv}")
    print(f"(b) REAL-CHANNEL control DOES signal (TV >> CI)?               "
          f"max TV={chan['max_tv']:.6f} vs 3*CI={3*chan['max_ci']:.6f}  -> {cond_b}")
    print(f"(c) ENTANGLED joint correlation strong (CHSH S>2)?            "
          f"S={ent_S:.4f}  -> {cond_c}")
    print()

    reinforced = cond_a_ent and cond_a_lhv and cond_b and cond_c
    if reinforced:
        print("RESULT: 🔴 H_1099 REINFORCED (Bell/no-signalling arm).")
        print("  Strong setting-dependent JOINT correlation (CHSH up to Tsirelson)")
        print("  COEXISTS with ZERO marginal signalling — B's outcome distribution")
        print("  is provably independent of A's measurement SETTING. The positive")
        print("  control (real classical channel) IS detected, so the test has teeth.")
        print("  => Entanglement (ER=EPR) yields CORRELATION, not COMMUNICATION.")
        print("  => Citing ER=EPR / EPR entanglement / von-Neumann entropy lock does")
        print("     NOT rescue non-local STATE TRANSMISSION: NO-SIGNALLING THEOREM.")
    else:
        print("RESULT: falsifier NOT satisfied — re-examine.")
    print()
    print("g5 / p7 — deterministic statistical test of the no-signalling theorem; "
          "no perplexity/loss used as a verdict.")


if __name__ == "__main__":
    main()
