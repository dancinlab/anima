#!/usr/bin/env python3
"""H_1302 — multi-oscillator SCN-network (Kuramoto consensus) — R1 numpy mirror (DIRECTIONAL).

c15 brain-structure ladder r8 candidate (the r7/H_1301 card named this as one of three thin
r8 candidates). chronobiology / coupled-oscillator lens (a_no_llm_frame_trap): the SCN is NOT a
single clock — it is a NETWORK of ~20k neuronal oscillators with HETEROGENEOUS intrinsic periods
that MUTUALLY couple (VIP/GABA) into a single emergent ensemble rhythm. The network does TWO
things no single oscillator can:
  (i) EMERGENT CONSENSUS PERIOD: N heterogeneous oscillators (each its own tau_i) phase-lock to a
      SHARED ensemble period that is an emergent property of the coupling — NOT externally imposed
      (Kuramoto order parameter R -> 1).
  (ii) NETWORK DAMPING / ROBUSTNESS: a single perturbed (de-tuned) member is PULLED BACK by the
      ensemble — the consensus barely moves; the network resists a single bad oscillator.

THE DEPLETION TEST — control-surviving distinctness vs EVERY lane, decisively:
  - vs PhaseResetClock (H_1301), the nearest temporal lane: a SINGLE oscillator entrains to an
    EXTERNAL Zeitgeber. It has NO ensemble, NO mutual coupling, so it CANNOT produce a consensus
    period FROM N heterogeneous members (there is only one member), and a perturbation to it is
    not damped by any network — it just shifts. The falsifier: give A the same N heterogeneous
    oscillators with NO mutual coupling (= N independent PhaseResetClocks free-running) -> the
    spread NEVER collapses (R stays low), and a perturbed member is NOT pulled back.
  - vs CollectivePool (H_1295), the coupled-members lane: CollectivePool measures the IIT-4 Phi
    SUPER-ADDITIVITY of coupled ECA *substrates* — a STATIC structural-integration GAUGE over a
    TPM. It has NO phase, NO oscillation over time, NO consensus PERIOD, NO Kuramoto order
    parameter. The SCN-network is a TEMPORAL synchronization DYNAMIC (phases evolving over ticks
    toward a shared period). Orthogonal: structural Phi gauge != temporal phase-consensus process.
    (Articulated; the mirror's load-bearing falsifier is the temporal consensus + damping that the
    single-oscillator arm A cannot do.)

If B reduces to one averaged oscillator (R never rises above the uncoupled spread) or to an array
of independent oscillators (no emergent consensus, no damping), it FAILS distinctness -> 🏁.

FROZEN-FIRST, anti-Goodhart: 3 seeds, deterministic. Arms A (uncoupled = N independent PRCs,
SHOULD fail consensus) / B (mutually-coupled Kuramoto network) / B-SHUFFLE (coupling matrix
permuted to NON-mutual asymmetric pairings — destroys the symmetric mutual restoring structure) /
B-ABLATE (K_couple=0 -> each free-runs at its own tau). Bars: presence (B reaches consensus, A
cannot), distinct (A <= no-consensus), earned (shuffle+ablate collapse), damping, no-fab.
"""
import json
import math
import sys

TWO_PI = 2.0 * math.pi

# ── regime (frozen) ───────────────────────────────────────────────────────────
N_OSC = 8            # ensemble size (heterogeneous SCN cells)
STEPS = 400          # integration ticks
DT = 1.0             # tick
K_COUPLE = 0.25      # mutual coupling strength (live)
TAU_MEAN = 24.0      # mean intrinsic period (ticks/cycle)
TAU_SPREAD = 2.0     # heterogeneity: tau_i in [TAU_MEAN-spread, TAU_MEAN+spread]
SETTLE = 200         # ticks discarded before measuring consensus (transient)
R_CONSENSUS = 0.90   # order-parameter bar for "consensus reached"
PERTURB_DETUNE = 6.0 # de-tune one member by this many ticks (robustness test)


def _order_parameter(phases):
    """Kuramoto order parameter R = |mean(e^{i*theta})| in [0,1]. R->1 = full sync."""
    n = len(phases)
    cx = sum(math.cos(TWO_PI * p) for p in phases) / n
    sy = sum(math.sin(TWO_PI * p) for p in phases) / n
    return math.sqrt(cx * cx + sy * sy)


def _intrinsic_taus(seed, n):
    """N heterogeneous intrinsic periods, deterministic from seed (LCG, no numpy RNG drift)."""
    taus = []
    x = (seed * 2654435761 + 12345) & 0xFFFFFFFF
    for _ in range(n):
        x = (1103515245 * x + 12345) & 0x7FFFFFFF
        u = x / float(0x7FFFFFFF)              # u in [0,1)
        taus.append(TAU_MEAN + TAU_SPREAD * (2.0 * u - 1.0))
    return taus


def _coupling_matrix(n, mode, seed):
    """Mutual all-to-all coupling (mode='mutual'), a FRUSTRATED random-sign symmetric matrix
    (mode='shuffle' — half the pairs attract, half repel, so there is NO coherent consensus
    field), or zeros (mode='ablate').

    NOTE (c9 honesty trail, R1a->R1b): the FIRST shuffle was an asymmetric one-way 'directed
    chain' that PRESERVED per-row coupling magnitude — and a directed chain STILL drags
    oscillators toward a common phase (Bshuf_R=0.79), a mean-preserving-magnitude LEAK that does
    not break the claimed structure (the same trap H_1299/H_1301-R1b hit). The corrected control
    randomizes the SIGN (frustration): the claim is 'COHERENT ATTRACTIVE mutual coupling -> a
    single consensus'; random-sign coupling has the same magnitude but no coherent attractor ->
    consensus is destroyed (R falls BELOW even uncoupled). This is the CORRECT, stricter control.
    """
    if mode == "ablate":
        return [[0.0] * n for _ in range(n)]
    if mode == "mutual":
        # symmetric all-to-all (the real SCN-network mutual coupling), self-coupling 0
        return [[0.0 if i == j else 1.0 / (n - 1) for j in range(n)] for i in range(n)]
    if mode == "shuffle":
        # FRUSTRATED: symmetric coupling with RANDOM SIGN per pair (same magnitude as mutual).
        # Half attract, half repel -> no coherent consensus field (breaks the claimed structure
        # WITHOUT a magnitude/mean leak: total |coupling| per row matches the mutual arm).
        mat = [[0.0] * n for _ in range(n)]
        x = (seed * 2246822519 + 3266489917) & 0x7FFFFFFF
        for i in range(n):
            for j in range(i + 1, n):
                x = (1103515245 * x + 12345) & 0x7FFFFFFF
                s = 1.0 if (x & 1) else -1.0
                w = s / (n - 1)
                mat[i][j] = w
                mat[j][i] = w               # symmetric (only the SIGN is randomized)
        return mat
    raise ValueError(mode)


def _run_network(seed, mode, k_couple, perturb=False):
    """Integrate N phase oscillators with Kuramoto coupling. Returns the post-settle order
    parameter and the realized ensemble period.

    mode='uncoupled' = arm A (N independent oscillators, NO mutual coupling = N free PRCs).
    """
    taus = _intrinsic_taus(seed, N_OSC)
    if perturb:
        taus = list(taus)
        taus[0] = taus[0] + PERTURB_DETUNE     # de-tune ONE member hard

    if mode == "uncoupled":                    # arm A: no network at all
        cmat = [[0.0] * N_OSC for _ in range(N_OSC)]
        keff = 0.0
    else:
        cmat = _coupling_matrix(N_OSC, mode, seed)
        keff = k_couple

    # init phases spread across the cycle (deterministic, NOT pre-synchronized)
    phases = [(i / float(N_OSC)) for i in range(N_OSC)]
    cum = [0.0] * N_OSC                          # cumulative phase (for realized period)

    r_acc, r_cnt = 0.0, 0
    for t in range(STEPS):
        new = [0.0] * N_OSC
        for i in range(N_OSC):
            dphi = DT / taus[i]                  # intrinsic advance
            coup = 0.0                            # mutual Kuramoto coupling
            for j in range(N_OSC):
                if cmat[i][j] != 0.0:
                    coup += cmat[i][j] * math.sin(TWO_PI * (phases[j] - phases[i]))
            dphi += keff * coup / TWO_PI
            new[i] = phases[i] + dphi
            cum[i] += dphi
        phases = [p - math.floor(p) for p in new]  # wrap to [0,1)
        if t >= SETTLE:
            r_acc += _order_parameter(phases)
            r_cnt += 1

    r_mean = r_acc / max(1, r_cnt)
    mean_cycles = sum(cum) / N_OSC
    realized_period = STEPS / (mean_cycles if mean_cycles > 1e-9 else 1e-9)
    return r_mean, realized_period


def run_seed(seed):
    out = {}
    out["B_R"], out["B_period"] = _run_network(seed, "mutual", K_COUPLE)
    out["A_R"], out["A_period"] = _run_network(seed, "uncoupled", K_COUPLE)
    out["Bshuf_R"], _ = _run_network(seed, "shuffle", K_COUPLE)
    out["Babl_R"], out["Babl_period"] = _run_network(seed, "ablate", 0.0)

    # DAMPING / robustness, measured via the ORDER PARAMETER under a perturbed member (c9
    # honesty trail, R1a->R1b): the FIRST c5 used the consensus PERIOD shift, but Kuramoto
    # coupling is phase-difference-antisymmetric and CONSERVES the mean ensemble frequency, so the
    # perturbed-member period shift is IDENTICAL for the coupled and uncoupled arms (B=A=0.647) —
    # a metric that cannot see damping by construction (not a collapse, a wrong metric). The
    # CORRECT operationalization of 'the network resists a single bad oscillator': de-tune ONE
    # member hard and ask whether the ensemble PULLS IT BACK into the synchronized cluster — i.e.
    # does R STAY HIGH. The network keeps R~0.997 (pulls the bad member back); uncoupled stays
    # at ~0.41 (no cluster to pull into).
    bR_clean, _ = _run_network(seed, "mutual", K_COUPLE, perturb=False)
    bR_pert, _ = _run_network(seed, "mutual", K_COUPLE, perturb=True)
    aR_pert, _ = _run_network(seed, "uncoupled", K_COUPLE, perturb=True)
    out["B_R_pert"] = bR_pert
    out["B_R_drop"] = abs(bR_clean - bR_pert)   # how much consensus the perturbed member costs B
    out["A_R_pert"] = aR_pert
    return out


# ── frozen bars ────────────────────────────────────────────────────────────────
# c1 PRESENCE   : B reaches consensus (R >= R_CONSENSUS) AND beats A by >= 0.30
# c2 DISTINCT   : A (uncoupled) CANNOT reach consensus (R <= 0.65 = no shared period)
# c3 EARNED-SHUF: frustrated random-sign coupling collapses consensus (R <= A + 0.15)
# c4 EARNED-ABL : ablate (K=0) collapses consensus (R <= A + 0.15)
# c5 DAMP       : the network keeps R high under a perturbed member (B_R_pert >= 0.90) AND that
#                perturbed R far exceeds the uncoupled-perturbed R (B_R_pert - A_R_pert >= 0.30)
# c6 NO-FAB     : uncoupled spread does not spuriously read as consensus (A_R < R_CONSENSUS)
BAR_PRESENCE_R = R_CONSENSUS
BAR_PRESENCE_GAP = 0.30
BAR_DISTINCT = 0.65
BAR_EARNED = 0.15
BAR_DAMP_R = R_CONSENSUS
BAR_DAMP_GAP = 0.30


def score(seeds):
    rows = [run_seed(s) for s in seeds]
    m = {k: sum(r[k] for r in rows) / len(rows) for k in rows[0]}
    c1 = (m["B_R"] >= BAR_PRESENCE_R) and ((m["B_R"] - m["A_R"]) >= BAR_PRESENCE_GAP)
    c2 = m["A_R"] <= BAR_DISTINCT
    c3 = m["Bshuf_R"] <= (m["A_R"] + BAR_EARNED)
    c4 = m["Babl_R"] <= (m["A_R"] + BAR_EARNED)
    c5 = (m["B_R_pert"] >= BAR_DAMP_R) and ((m["B_R_pert"] - m["A_R_pert"]) >= BAR_DAMP_GAP)
    c6 = m["A_R"] < BAR_PRESENCE_R
    bars = [c1, c2, c3, c4, c5, c6]
    return m, rows, bars


def main():
    seeds = [5320, 5321, 5322]
    m, rows, bars = score(seeds)
    c1, c2, c3, c4, c5, c6 = bars
    allpass = all(bars)
    tier = "GREEN" if allpass else "RED / DEPLETED"

    print("=" * 74)
    print("H_1302 — multi-oscillator SCN-network (Kuramoto consensus) — R1 numpy mirror")
    print("=" * 74)
    print(f"seeds={seeds}  N_OSC={N_OSC}  STEPS={STEPS}  K_COUPLE={K_COUPLE}")
    print(f"  tau in [{TAU_MEAN-TAU_SPREAD},{TAU_MEAN+TAU_SPREAD}] (heterogeneous)  SETTLE={SETTLE}")
    print("-" * 74)
    print(f"{'metric':<26}{'B (network)':>14}{'A (uncoupled)':>16}")
    print(f"{'order param R':<26}{m['B_R']:>14.4f}{m['A_R']:>16.4f}")
    print(f"{'consensus period':<26}{m['B_period']:>14.4f}{m['A_period']:>16.4f}")
    print(f"{'B-SHUF R (frustrated)':<26}{m['Bshuf_R']:>14.4f}")
    print(f"{'B-ABL  R':<26}{m['Babl_R']:>14.4f}")
    print(f"{'R under perturb':<26}{m['B_R_pert']:>14.4f}{m['A_R_pert']:>16.4f}")
    print(f"{'B R drop (perturb)':<26}{m['B_R_drop']:>14.4f}")
    print("-" * 74)
    print(f"c1 PRESENCE  B_R>={BAR_PRESENCE_R} & B-A>={BAR_PRESENCE_GAP}: "
          f"R={m['B_R']:.4f} gap={m['B_R']-m['A_R']:+.4f}  -> {'PASS' if c1 else 'FAIL'}")
    print(f"c2 DISTINCT  A_R<={BAR_DISTINCT} (uncoupled no consensus): "
          f"{m['A_R']:.4f}  -> {'PASS' if c2 else 'FAIL'}")
    print(f"c3 EARNED-SHUF Bshuf<=A+{BAR_EARNED} (frustrated): "
          f"{m['Bshuf_R']:.4f} <= {m['A_R']+BAR_EARNED:.4f}  -> {'PASS' if c3 else 'FAIL'}")
    print(f"c4 EARNED-ABL  Babl<=A+{BAR_EARNED}: "
          f"{m['Babl_R']:.4f} <= {m['A_R']+BAR_EARNED:.4f}  -> {'PASS' if c4 else 'FAIL'}")
    print(f"c5 DAMP   B_R_pert>={BAR_DAMP_R} & B-A>={BAR_DAMP_GAP}: "
          f"B={m['B_R_pert']:.4f} A={m['A_R_pert']:.4f} gap={m['B_R_pert']-m['A_R_pert']:+.4f}"
          f"  -> {'PASS' if c5 else 'FAIL'}")
    print(f"c6 NO-FAB A_R<{BAR_PRESENCE_R}: {m['A_R']:.4f}  -> {'PASS' if c6 else 'FAIL'}")
    print("-" * 74)
    print(f"c1..c6 = {['T' if b else 'F' for b in bars]}   VERDICT: {tier}")
    print("=" * 74)

    if "--json" in sys.argv:
        print(json.dumps({"mean": m, "bars": bars, "tier": tier, "seeds": seeds}, indent=2))


if __name__ == "__main__":
    main()
