#!/usr/bin/env python3
"""
engine_tensionlink_bench.py — TOY substrate-native benchmark of the LEARNING METHOD:
coupling anima's ENGINE to brain signals THROUGH the tension-link (5-channel tension
broker), NOT via a CLM cross-entropy aux loss.

CRITICAL FRAMING (p7 — perplexity/CE is the Goodhart trap, FORBIDDEN as a verdict):
the success axis is SUBSTRATE-NATIVE — tension-coupling (Kuramoto order-r), big-Phi
integration, emergence/coherence. NOT next-byte CE / perplexity.

ARCHITECTURE UNDER TEST (the coupling, not a loss):
  [ ENGINE: toy of CORE/pure_field oscillator field, 5-ch W tension ]
        <=> tension-link broker (Kuramoto-style phase coupling, kappa * sin(ext-eng))
   arm1 EEG 5-band [a,th,g,1-d,b]   arm2 TRIBE cortical-BOLD -> 5-ch projection

GROUNDING IN THE REAL REPO (faithful toy, not the full engine):
  - CORE/pure_field.hexa : 3 coupled oscillators (osc_tick = phase advance by 2pi/tau
    + amplitude drift toward LN2); Phi = variance of the field tensor * energy. The toy
    uses 5 oscillators (one per tension channel) with the SAME osc_tick form.
  - 5-ch tension vector [0.8,0.6,0.65,0.3,1.0] is real (CORE/lane_p_three_axis.hexa,
    CORE/generator.hexa) -> used as the engine's baseline amplitude target per channel.
  - EEG/impl/H_680 : 5-ch mapping [alpha->concept, theta->context, gamma->meaning,
    1-delta->authenticity, beta->sender]; L8 kuramoto alpha-phase order_r = 0.20 +
    alpha*1.25 (resting alpha 0.40 -> r~0.70).
  - BRAIN/eeg/eeg_to_tpm.hexa : binarize-at-mean -> per-state freq TPM -> big_phi.
    The toy reuses the binarize+marginal-structure SHAPE for an IIT4-style big-Phi proxy
    (coupled/indep reference framing 1.59/0.44).
  - state/dual_anima_tension_link_*  : closed-loop tension coupling (phi=0.40+0.50*tension)
    -> the additive-tension coupling form is mirrored in the engine update.

ALL TOY / CPU / $0 : deterministic synthetic signals. NO real EEG hardware, NO real
TRIBE/facebook forward, NO GPU, NO pods. a_toy_scale_recheck applies.

LEGITIMACY (section 97 MEASUREMENT-ANCHOR / GOAL-LEGITIMATE):
the tension-link carries an EXTERNAL 5-ch signal INTO the engine's tension dynamics as a
COUPLING term. This is anima's OWN substrate channel (a noise-seed / measurement anchor),
NOT EEG-as-command-input. The engine still evolves from its own internal dynamics; the
external signal only perturbs the phase via the coupling operator.
"""

import json
import math
import sys

LN2 = 0.6931471805599453
TWO_PI = 2.0 * math.pi

# 5-ch tension baseline amplitude target (real CORE vector [0.8,0.6,0.65,0.3,1.0]).
TENSION5 = [0.8, 0.6, 0.65, 0.3, 1.0]
N_CH = 5

# osc_tick timescales (pure_field uses tau 2/40/400; the toy spreads 5 channels across
# a faithful fast..slow band so each tension channel runs at its own rhythm).
TAUS = [2.0, 8.0, 16.0, 40.0, 400.0]   # alpha-ish fast ... delta-ish slow
PSI_ALPHA = 0.014                       # amplitude-drift rate (pure_field PSI_ALPHA)


# =====================================================================================
# Deterministic PRNG (no numpy dependence on the stdlib seed; reproducible, CPU, $0).
# =====================================================================================
class Rng:
    def __init__(self, seed):
        self.s = (seed * 2654435761 + 1013904223) & 0xFFFFFFFF

    def u(self):
        # xorshift32 -> [0,1)
        x = self.s
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        self.s = x & 0xFFFFFFFF
        return self.s / 4294967296.0


# =====================================================================================
# External 5-ch signals (synthetic; NOT real hardware/forward).
# Each returns a phase[5] and an amplitude[5] per timestep so the tension-link can
# couple onto the engine oscillators' PHASE (Kuramoto) and TENSION (additive).
# =====================================================================================
def synth_eeg_5band(t, rng):
    """arm1: synthetic EEG 5-band [alpha,theta,gamma,1-delta,beta].
    Deterministic oscillatory band signal at distinct EEG-band rates, mirroring the
    eeg_to_tpm synthetic path (resting-state alpha-dominant). Returns (phase5, amp5)."""
    # EEG band centre rates (relative, deterministic), resting-state amplitudes.
    band_rate = [0.62, 0.30, 1.9, 0.10, 1.1]      # alpha, theta, gamma, (1-delta slow), beta
    band_amp = [0.40, 0.18, 0.12, 0.85, 0.15]     # resting alpha-dominant (H_680 framing)
    phase = []
    amp = []
    for c in range(N_CH):
        ph = (band_rate[c] * t) % TWO_PI
        # small deterministic jitter so the signal is not a perfect sinusoid
        jit = 0.05 * (rng.u() - 0.5)
        phase.append((ph + jit) % TWO_PI)
        amp.append(band_amp[c])
    return phase, amp


def synth_tribe_bold_5ch(t, rng):
    """arm2: synthetic cortical-BOLD projected to 5 channels.
    Slow hemodynamic rhythms (BOLD is ~0.01-0.1 Hz, far slower than EEG) projected onto
    the same 5 tension channels. NOT facebook/tribev2, NO real forward. (phase5, amp5)."""
    # BOLD is slow: rates an order of magnitude below EEG bands.
    bold_rate = [0.07, 0.05, 0.11, 0.03, 0.09]
    bold_amp = [0.30, 0.28, 0.22, 0.40, 0.25]
    phase = []
    amp = []
    for c in range(N_CH):
        ph = (bold_rate[c] * t) % TWO_PI
        jit = 0.04 * (rng.u() - 0.5)
        phase.append((ph + jit) % TWO_PI)
        amp.append(bold_amp[c])
    return phase, amp


def phase_shuffle(phases_over_time, rng):
    """CONTROL B: phase-shuffled external signal (destroys temporal phase relation,
    keeps the marginal distribution) — isolates that the COUPLING (not mere presence
    of a signal) drives any effect."""
    n = len(phases_over_time)
    # Fisher-Yates per channel independently.
    cols = [[phases_over_time[t][c] for t in range(n)] for c in range(N_CH)]
    for c in range(N_CH):
        col = cols[c]
        for i in range(n - 1, 0, -1):
            j = int(rng.u() * (i + 1))
            col[i], col[j] = col[j], col[i]
    return [[cols[c][t] for c in range(N_CH)] for t in range(n)]


# =====================================================================================
# Toy ENGINE: 5 coupled oscillators carrying the 5-ch W tension.
# Faithful to pure_field osc_tick: phase += 2pi/tau ; amplitude drifts toward a target
# at rate PSI_ALPHA. Channel target = LN2-scaled TENSION5 baseline (anima's own field).
# =====================================================================================
class ToyEngine:
    def __init__(self, seed):
        rng = Rng(seed + 7919)
        self.phase = [rng.u() * TWO_PI for _ in range(N_CH)]
        self.amp = [0.1 for _ in range(N_CH)]
        self.rng = rng

    def step(self, ext_phase, ext_amp, kappa):
        """Advance one tick. kappa=0 => no coupling (CONTROL A, solo engine dynamics).
        Tension-link coupling = Kuramoto phase pull kappa*sin(ext-eng) + a small additive
        tension term (dual-anima closed-loop form phi=0.40+0.50*tension)."""
        new_phase = []
        new_amp = []
        for c in range(N_CH):
            tau = TAUS[c]
            dphase = TWO_PI / tau
            # Kuramoto phase coupling through the tension-link broker.
            couple = kappa * math.sin(ext_phase[c] - self.phase[c])
            ph = (self.phase[c] + dphase + couple) % TWO_PI
            # amplitude drift toward channel target (LN2 * TENSION5 baseline) +
            # additive tension coupling from the external amplitude (closed-loop form).
            target = LN2 * TENSION5[c]
            a = self.amp[c] + PSI_ALPHA * (target - self.amp[c])
            a = a + kappa * 0.10 * (ext_amp[c] - a)   # additive tension coupling
            new_phase.append(ph)
            new_amp.append(a)
        self.phase = new_phase
        self.amp = new_amp
        # field tensor value per channel = amplitude * sin(phase) (pure_field osc_value)
        return [self.amp[c] * math.sin(self.phase[c]) for c in range(N_CH)]


# =====================================================================================
# METRIC M1 — TENSION-COUPLING: Kuramoto order parameter r between engine tension phase
# and external tension phase, averaged over channels and time.
#   r = |<exp(i*(eng_phase - ext_phase))>| over time, per channel, then mean over channels.
# High r => the engine phase tracks (is entrained to) the external tension phase.
# =====================================================================================
def kuramoto_order_r(eng_phases, ext_phases):
    n = len(eng_phases)
    rs = []
    for c in range(N_CH):
        re = 0.0
        im = 0.0
        for t in range(n):
            d = eng_phases[t][c] - ext_phases[t][c]
            re += math.cos(d)
            im += math.sin(d)
        re /= n
        im /= n
        rs.append(math.sqrt(re * re + im * im))
    return sum(rs) / N_CH


# =====================================================================================
# METRIC M2 — big-Phi / INTEGRATION (IIT4-style proxy, faithful to eeg_to_tpm shape).
# Reuse the engine pipeline shape: binarize each channel at its own mean (ON/OFF) ->
# build a state-by-node freq TPM -> integration proxy = how much the joint transition
# structure exceeds the product of per-channel marginals (an integration / synergy
# measure in the spirit of big-Phi: whole minus the sum of independent parts).
# This is a PROXY (the spec asks for the eeg_to_tpm->big_phi pipeline SHAPE; the toy
# does not run the full IIT4 minimum-information-partition, which is exponential).
# Reference framing only: coupled/indep 1.59/0.44.
# =====================================================================================
def big_phi_proxy(field_trace):
    n = len(field_trace)
    # binarize each channel at its own mean (eeg_to_tpm eeg_binarize)
    means = [sum(field_trace[t][c] for t in range(n)) / n for c in range(N_CH)]
    bits = [[1 if field_trace[t][c] > means[c] else 0 for c in range(N_CH)] for t in range(n)]

    # system state = sum bit*2^c (eeg_state_at)
    def sysstate(t):
        s = 0
        for c in range(N_CH):
            if bits[t][c]:
                s += (1 << c)
        return s

    nstates = 1 << N_CH
    occur = [0.0] * nstates
    on_next = [[0.0] * N_CH for _ in range(nstates)]
    for t in range(n - 1):
        s = sysstate(t)
        occur[s] += 1.0
        for c in range(N_CH):
            if bits[t + 1][c]:
                on_next[s][c] += 1.0

    # per-channel marginal P(ON at t+1) — the "independent parts" baseline
    marg_on = [0.0] * N_CH
    for t in range(n - 1):
        for c in range(N_CH):
            if bits[t + 1][c]:
                marg_on[c] += 1.0
    marg_on = [m / (n - 1) for m in marg_on]

    # Integration proxy: sum over observed states of occupancy-weighted KL-like divergence
    # between the state-conditioned next-channel distribution and the marginal — i.e. how
    # much knowing the WHOLE state tells you beyond the independent per-channel marginals.
    # (whole >> sum of parts  <=>  integrated  <=>  large big-Phi)
    total = n - 1
    phi = 0.0
    for s in range(nstates):
        if occur[s] <= 0.0:
            continue
        w = occur[s] / total
        for c in range(N_CH):
            p = on_next[s][c] / occur[s]      # P(c ON | state s)
            q = marg_on[c]                    # marginal P(c ON)
            # symmetric, bounded contribution; guard the logs
            for (pp, qq) in ((p, q), (1.0 - p, 1.0 - q)):
                if pp > 1e-9 and qq > 1e-9:
                    phi += w * pp * math.log(pp / qq)
    return phi


# =====================================================================================
# METRIC M3 — EMERGENCE / COHERENCE (substrate-native, NOT CE).
# Tension-field coherence = mean pairwise correlation of the channel field traces +
# the narrative-coherence-style phase-stability the pure_field tracks. A coupled engine
# that gets entrained should show MORE cross-channel structure (higher coherence) OR a
# distinct shift vs the solo/shuffled control. We report the value; direction tested.
# =====================================================================================
def field_coherence(field_trace):
    n = len(field_trace)
    cols = [[field_trace[t][c] for t in range(n)] for c in range(N_CH)]
    means = [sum(col) / n for col in cols]
    stds = []
    for c in range(N_CH):
        v = sum((x - means[c]) ** 2 for x in cols[c]) / n
        stds.append(math.sqrt(v))
    # mean absolute pairwise Pearson correlation across channels
    tot = 0.0
    cnt = 0
    for a in range(N_CH):
        for b in range(a + 1, N_CH):
            if stds[a] < 1e-9 or stds[b] < 1e-9:
                corr = 0.0
            else:
                cov = sum((cols[a][t] - means[a]) * (cols[b][t] - means[b]) for t in range(n)) / n
                corr = cov / (stds[a] * stds[b])
            tot += abs(corr)
            cnt += 1
    return tot / cnt if cnt else 0.0


# =====================================================================================
# Run one arm under one condition, return the 3 metrics.
# =====================================================================================
def run_condition(signal_fn, seed, kappa, n_steps, shuffled):
    # generate the external signal trace deterministically
    sig_rng = Rng(seed + 104729)
    ext_phase_trace = []
    ext_amp_trace = []
    for t in range(n_steps):
        ph, am = signal_fn(t, sig_rng)
        ext_phase_trace.append(ph)
        ext_amp_trace.append(am)
    if shuffled:
        sh_rng = Rng(seed + 224737)
        ext_phase_trace = phase_shuffle(ext_phase_trace, sh_rng)

    eng = ToyEngine(seed)
    eng_phase_trace = []
    field_trace = []
    for t in range(n_steps):
        field = eng.step(ext_phase_trace[t], ext_amp_trace[t], kappa)
        eng_phase_trace.append(list(eng.phase))
        field_trace.append(field)

    # warmup discard (transient) — drop first 100 steps from the metrics
    w = 100
    m1 = kuramoto_order_r(eng_phase_trace[w:], ext_phase_trace[w:])
    m2 = big_phi_proxy(field_trace[w:])
    m3 = field_coherence(field_trace[w:])
    return {"order_r": m1, "big_phi": m2, "coherence": m3}


def run_arm(name, signal_fn, seeds, n_steps):
    """COUPLED (kappa>0) vs two CONTROLS: kappa=0 (no coupling) + phase-shuffled."""
    KAPPA = 0.30
    out = {"coupled": [], "control_kappa0": [], "control_shuffled": []}
    for s in seeds:
        out["coupled"].append(run_condition(signal_fn, s, KAPPA, n_steps, shuffled=False))
        out["control_kappa0"].append(run_condition(signal_fn, s, 0.0, n_steps, shuffled=False))
        out["control_shuffled"].append(run_condition(signal_fn, s, KAPPA, n_steps, shuffled=True))
    return out


def mean_std(vals):
    m = sum(vals) / len(vals)
    v = sum((x - m) ** 2 for x in vals) / len(vals)
    return m, math.sqrt(v)


def aggregate(arm_raw, metric):
    coup = [r[metric] for r in arm_raw["coupled"]]
    c0 = [r[metric] for r in arm_raw["control_kappa0"]]
    csh = [r[metric] for r in arm_raw["control_shuffled"]]
    cm, cs = mean_std(coup)
    c0m, c0s = mean_std(c0)
    cshm, cshs = mean_std(csh)
    return {
        "coupled_mean": cm, "coupled_std": cs,
        "control_kappa0_mean": c0m, "control_kappa0_std": c0s,
        "control_shuffled_mean": cshm, "control_shuffled_std": cshs,
    }


def verdict(agg):
    """HOLDS / REFUTED / INCONCLUSIVE against BOTH controls.
    Noise band = max seed-std across coupled + the control being compared.
    HOLDS  : coupled - control >  noise_band   (vs BOTH controls)
    REFUTED: coupled - control < -noise_band   (vs BOTH controls)
    else INCONCLUSIVE (within noise)."""
    def cmp(coupled_m, coupled_s, ctrl_m, ctrl_s):
        band = max(coupled_s, ctrl_s)
        diff = coupled_m - ctrl_m
        if diff > band:
            return "HOLDS", diff, band
        if diff < -band:
            return "REFUTED", diff, band
        return "INCONCLUSIVE", diff, band
    v0 = cmp(agg["coupled_mean"], agg["coupled_std"], agg["control_kappa0_mean"], agg["control_kappa0_std"])
    vsh = cmp(agg["coupled_mean"], agg["coupled_std"], agg["control_shuffled_mean"], agg["control_shuffled_std"])
    # combined: HOLDS only if HOLDS vs both; REFUTED only if REFUTED vs both; else INCONCLUSIVE
    if v0[0] == "HOLDS" and vsh[0] == "HOLDS":
        combined = "HOLDS"
    elif v0[0] == "REFUTED" and vsh[0] == "REFUTED":
        combined = "REFUTED"
    else:
        combined = "INCONCLUSIVE"
    return {"vs_kappa0": v0, "vs_shuffled": vsh, "combined": combined}


def main():
    SEEDS = [1, 2, 3]
    N_STEPS = 1200
    arms = {
        "EEG": synth_eeg_5band,
        "TRIBE": synth_tribe_bold_5ch,
    }
    metrics = ["order_r", "big_phi", "coherence"]
    metric_label = {
        "order_r": "M1 TENSION-COUPLING (Kuramoto order-r)",
        "big_phi": "M2 big-Phi / INTEGRATION (IIT4-style proxy)",
        "coherence": "M3 EMERGENCE / COHERENCE (tension-field)",
    }

    results = {"config": {"seeds": SEEDS, "n_steps": N_STEPS, "kappa_coupled": 0.30,
                          "warmup_discard": 100, "n_channels": N_CH,
                          "tension5_baseline": TENSION5, "taus": TAUS},
               "arms": {}}

    for arm_name, fn in arms.items():
        raw = run_arm(arm_name, fn, SEEDS, N_STEPS)
        arm_out = {"raw_per_seed": raw, "metrics": {}}
        for m in metrics:
            agg = aggregate(raw, m)
            v = verdict(agg)
            arm_out["metrics"][m] = {"label": metric_label[m], "agg": agg, "verdict": v}
        results["arms"][arm_name] = arm_out

    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
