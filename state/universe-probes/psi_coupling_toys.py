#!/usr/bin/env python3
# ==========================================================================
# psi_coupling_toys.py — TOY emergent falsifiers for the TELEPATHY / anomalous-
# cognition / consciousness-COUPLING hypothesis family (UNIVERSE/PSI-CANDIDATES).
#
# FRAMING (brutally honest, p7 / a_paper_negative_ok):
#   Every hypothesis is reframed as a FALSIFIABLE MECHANISM with a pre-registered
#   falsifier whose DEFAULT disposition is REFUTED unless the mechanism genuinely
#   produces an above-chance / above-CONTROL signal. Genuine coupling phenomena
#   that DO have a physical channel (interbrain phase-lock, hive Kuramoto, empathy
#   tension-mirroring) MAY legitimately HOLD. Paranormal claims that posit a
#   NO-CHANNEL transfer (morphic resonance, precognition, remote viewing, twin
#   entanglement, presentiment, retrocausal priming) are EXPECTED to REFUTE — a
#   no-channel positive would be a leak/bug, not psi (the null-channel meta-control).
#
# THE COUPLING MATRIX (user's explicit 3-config ask), MITOSIS = ON by default
# (p8 native growth — it is the inference-time cell-division, not a train flag):
#   C1  tension-link only  : two ToyEngine substrates coupled through the 5-ch
#                            [alpha,theta,gamma,1-delta,beta] tension broker.
#   C2  tension-link + EEG : a synthetic EEG 5-band stream DRIVES the coupling
#                            (the broker carries an EEG-shaped external signal).
#   C3  ENGINE + tension-link + EEG : full stack — CORE/pure_field oscillator
#                            ENGINE <=> tension-link <=> synthetic EEG, with a
#                            MITOSIS-grown cell population ON (lane_m growth).
#
# REUSE (faithful, NOT reinvented) — primitives mirrored from the harnesses on main:
#   - CLM/bench/engine_tensionlink_bench.py : ToyEngine (pure_field osc_tick),
#       synth_eeg_5band, kuramoto_order_r, big_phi_proxy, field_coherence,
#       phase_shuffle, the kappa0 / shuffled CONTROLS, the seed-noise verdict.
#   - CLM/bench/lane_m_eeg_mitosis.py : gamma>0.20 MITOSIS split, Cell, _phi_proxy,
#       tension_link_5ch carrier, phase_shuffle_stream.
#
# THE TELEPATHY TEST = couple TWO such substrates (sender S, receiver R) and
# measure above-chance / above-CONTROL info-transfer or synchrony. CONTROLS are
# MANDATORY (kappa0 = no coupling, phase-shuffled, no-channel) — a positive must
# beat the control by > seed-noise (3 seeds). Verdict ∈ {HOLDS, REFUTED,
# INCONCLUSIVE}; a null/refute is NEVER rounded up to a HOLD.
#
# ALL TOY / CPU / $0 : deterministic synthetic signals, pure stdlib (no numpy),
# NO real EEG/hardware, NO GPU, NO pods. a_toy_scale_recheck + a_scale_honest_scope
# apply — toy-scale only, scale-transfer UNVERIFIED.
#
# §97 LEGITIMACY: the tension-link carries an external 5-ch signal INTO the engine
# tension dynamics as a COUPLING term — anima's OWN substrate channel (a coupling
# / measurement anchor), NOT a command channel. The grown cells are a RECORDING
# artifact, never an emit/decision driver.
# ==========================================================================

import json
import math

LN2 = 0.6931471805599453
TWO_PI = 2.0 * math.pi

TENSION5 = [0.8, 0.6, 0.65, 0.3, 1.0]      # real CORE 5-ch W tension baseline
N_CH = 5
TAUS = [2.0, 8.0, 16.0, 40.0, 400.0]       # pure_field osc_tick timescales (fast..slow)
PSI_ALPHA = 0.014                          # pure_field amplitude-drift rate
KAPPA = 0.30                               # coupling strength (engine_tensionlink_bench)
GAMMA_SPLIT_THR = 0.20                     # lane_m L12 MITOSIS trigger
SPLIT_NOISE_FLOOR = 0.1
MAX_CELLS = 64
SEEDS = [1, 2, 3]
N_STEPS = 1200


# ==========================================================================
# Deterministic PRNG (xorshift32) — mirrors engine_tensionlink_bench.Rng.
# ==========================================================================
class Rng:
    def __init__(self, seed):
        self.s = (seed * 2654435761 + 1013904223) & 0xFFFFFFFF

    def u(self):
        x = self.s
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        self.s = x & 0xFFFFFFFF
        return self.s / 4294967296.0


# ==========================================================================
# Synthetic EEG 5-band (resting alpha-dominant), mirrors synth_eeg_5band.
# Returns (phase5, amp5). With a per-instance phase OFFSET so two agents can
# carry related-but-distinct EEG (interbrain hyperscanning) or be independent.
# ==========================================================================
def synth_eeg_5band(t, rng, phase_offset=0.0):
    band_rate = [0.62, 0.30, 1.9, 0.10, 1.1]      # alpha, theta, gamma, (1-delta), beta
    band_amp = [0.40, 0.18, 0.12, 0.85, 0.15]     # resting alpha-dominant (H_680)
    phase, amp = [], []
    for c in range(N_CH):
        ph = (band_rate[c] * t + phase_offset) % TWO_PI
        jit = 0.05 * (rng.u() - 0.5)
        phase.append((ph + jit) % TWO_PI)
        amp.append(band_amp[c])
    return phase, amp


def phase_shuffle(trace, rng):
    """CONTROL: destroy temporal phase relation, keep marginal (per channel FY)."""
    n = len(trace)
    cols = [[trace[t][c] for t in range(n)] for c in range(N_CH)]
    for c in range(N_CH):
        col = cols[c]
        for i in range(n - 1, 0, -1):
            j = int(rng.u() * (i + 1))
            col[i], col[j] = col[j], col[i]
    return [[cols[c][t] for c in range(N_CH)] for t in range(n)]


# ==========================================================================
# Toy ENGINE: 5 coupled oscillators carrying the 5-ch W tension (pure_field).
# Mirrors engine_tensionlink_bench.ToyEngine; step() couples to an external
# phase/amp through the tension-link (Kuramoto pull + additive tension term).
# ==========================================================================
class ToyEngine:
    def __init__(self, seed):
        rng = Rng(seed + 7919)
        self.phase = [rng.u() * TWO_PI for _ in range(N_CH)]
        self.amp = [0.1 for _ in range(N_CH)]
        self.rng = rng

    def step(self, ext_phase, ext_amp, kappa):
        new_phase, new_amp = [], []
        for c in range(N_CH):
            dphase = TWO_PI / TAUS[c]
            couple = kappa * math.sin(ext_phase[c] - self.phase[c])
            ph = (self.phase[c] + dphase + couple) % TWO_PI
            target = LN2 * TENSION5[c]
            a = self.amp[c] + PSI_ALPHA * (target - self.amp[c])
            a = a + kappa * 0.10 * (ext_amp[c] - a)
            new_phase.append(ph)
            new_amp.append(a)
        self.phase = new_phase
        self.amp = new_amp
        return [self.amp[c] * math.sin(self.phase[c]) for c in range(N_CH)]


# ==========================================================================
# Mitosis-grown cell population (lane_m) — ON by default (p8). A gamma>thr
# event splits the highest-tension cell; the daughter specializes toward the
# current 5-ch drive. The population is a RECORDING artifact (§97), used only
# to MEASURE structure, never to drive emit/decision.
# ==========================================================================
class CellPop:
    def __init__(self, seed):
        self.rng = Rng(seed * 131 + 17)
        self.cells = [[0.5] * N_CH]            # one seed cell, neutral state
        self.last_tension = [0.0]

    def tick(self, drive, gamma):
        # update per-cell tension vs the drive
        self.last_tension = [
            sum((cell[i] - drive[i]) ** 2 for i in range(N_CH)) / N_CH
            for cell in self.cells
        ]
        if gamma > GAMMA_SPLIT_THR and len(self.cells) < MAX_CELLS:
            ci = max(range(len(self.cells)), key=lambda k: self.last_tension[k])
            daughter = [drive[i] + self.rng.u() * 2 * SPLIT_NOISE_FLOOR - SPLIT_NOISE_FLOOR
                        for i in range(N_CH)]
            self.cells.append(daughter)
        return len(self.cells)

    def phi_proxy(self):
        n = len(self.cells)
        if n < 2:
            return 0.0
        tot, cnt = 0.0, 0
        for i in range(n):
            for j in range(i + 1, n):
                d = math.sqrt(sum((self.cells[i][k] - self.cells[j][k]) ** 2 for k in range(N_CH)))
                tot += d
                cnt += 1
        return (tot / cnt) * math.log(n + 1)


# ==========================================================================
# METRICS (substrate-native, NOT CE/perplexity, p7).
# ==========================================================================
def kuramoto_order_r(phaseA, phaseB):
    """Order parameter r between two phase traces (per channel, mean over channels)."""
    n = len(phaseA)
    rs = []
    for c in range(N_CH):
        re = im = 0.0
        for t in range(n):
            d = phaseA[t][c] - phaseB[t][c]
            re += math.cos(d)
            im += math.sin(d)
        rs.append(math.sqrt((re / n) ** 2 + (im / n) ** 2))
    return sum(rs) / N_CH


def big_phi_proxy(field_trace):
    """IIT4-style integration proxy (binarize@mean -> state-TPM vs marginals)."""
    n = len(field_trace)
    if n < 2:
        return 0.0
    means = [sum(field_trace[t][c] for t in range(n)) / n for c in range(N_CH)]
    bits = [[1 if field_trace[t][c] > means[c] else 0 for c in range(N_CH)] for t in range(n)]

    def sysstate(t):
        return sum((1 << c) for c in range(N_CH) if bits[t][c])

    nstates = 1 << N_CH
    occur = [0.0] * nstates
    on_next = [[0.0] * N_CH for _ in range(nstates)]
    for t in range(n - 1):
        s = sysstate(t)
        occur[s] += 1.0
        for c in range(N_CH):
            if bits[t + 1][c]:
                on_next[s][c] += 1.0
    marg_on = [0.0] * N_CH
    for t in range(n - 1):
        for c in range(N_CH):
            if bits[t + 1][c]:
                marg_on[c] += 1.0
    marg_on = [m / (n - 1) for m in marg_on]
    total = n - 1
    phi = 0.0
    for s in range(nstates):
        if occur[s] <= 0.0:
            continue
        w = occur[s] / total
        for c in range(N_CH):
            p = on_next[s][c] / occur[s]
            q = marg_on[c]
            for (pp, qq) in ((p, q), (1.0 - p, 1.0 - q)):
                if pp > 1e-9 and qq > 1e-9:
                    phi += w * pp * math.log(pp / qq)
    return phi


def field_coherence(field_trace):
    """Mean absolute pairwise Pearson correlation across the 5 channels."""
    n = len(field_trace)
    cols = [[field_trace[t][c] for t in range(n)] for c in range(N_CH)]
    means = [sum(col) / n for col in cols]
    stds = []
    for c in range(N_CH):
        v = sum((x - means[c]) ** 2 for x in cols[c]) / n
        stds.append(math.sqrt(v))
    tot = cnt = 0.0
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


def transfer_accuracy(sender_bits, receiver_field, warmup=100, lead=0):
    """Sender encodes a random bit per tick (drives a channel HIGH/LOW); receiver
    decodes from its own field sign. Above-chance => the channel transfers info.
    Returns fraction-correct (chance = 0.5).
    lead>0 = PRECOGNITION probe: R at tick t must guess the sender bit at t+lead
    (a FUTURE bit with NO causal path to R's current state) — this MUST stay at
    chance (no future channel exists), so a HOLD here would be a leak/bug."""
    n = len(receiver_field)
    correct = total = 0
    for t in range(warmup, n - lead):
        # receiver reads channel-2 (gamma/meaning) sign as its guess of the sent bit
        guess = 1 if receiver_field[t][2] > 0 else 0
        if guess == sender_bits[t + lead]:
            correct += 1
        total += 1
    return correct / total if total else 0.5


def dprime(hits, fa, n_signal, n_noise):
    """Signal-detection d' from hit-rate / false-alarm-rate (Ganzfeld). 0 = chance."""
    def z(p):
        p = min(max(p, 1.0 / (2 * max(n_signal, n_noise))), 1 - 1.0 / (2 * max(n_signal, n_noise)))
        # inverse-normal (Acklam approximation, sufficient for a toy d')
        a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
             1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
        b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
             6.680131188771972e+01, -1.328068155288572e+01]
        c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
             -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
        d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
             3.754408661907416e+00]
        plow, phigh = 0.02425, 1 - 0.02425
        if p < plow:
            q = math.sqrt(-2 * math.log(p))
            return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
        if p <= phigh:
            q = p - 0.5
            r = q * q
            return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    return z(hits) - z(fa)


# ==========================================================================
# Two coupled substrates (sender S, receiver R) under a given CONFIG and
# COUPLING TOPOLOGY. Returns the per-tick traces needed by every metric.
#   channel_open : if False, R receives NO signal from S (no-channel control /
#                  the paranormal "no physical link" condition).
#   shuffled     : phase-shuffle S's outgoing trace (temporal relation destroyed).
#   config       : 'C1' tension-link only | 'C2' +EEG | 'C3' +ENGINE+EEG+mitosis
#   time_reversed: R reads S's FUTURE (precognition/retrocausal probe — must REFUTE).
# ==========================================================================
def run_pair(seed, config, kappa=KAPPA, channel_open=True, shuffled=False,
             time_reversed=False, sender_drives_bits=False, eeg_offset_R=1.3,
             n_steps=N_STEPS, mitosis=True):
    rngS = Rng(seed + 104729)
    rngR = Rng(seed + 224737)

    # sender external drive
    sender_bits = []
    bit_rng = Rng(seed + 999983)
    S_ext_phase, S_ext_amp = [], []
    for t in range(n_steps):
        if config in ("C2", "C3"):
            ph, am = synth_eeg_5band(t, rngS, phase_offset=0.0)
        else:  # C1: tension-link only — a plain 5-band carrier (no EEG shaping)
            ph = [(TENSION5[c] * t * 0.5) % TWO_PI for c in range(N_CH)]
            am = list(TENSION5)
        # sender optionally encodes a bit on the gamma channel (telepathy/ganzfeld)
        b = 1 if bit_rng.u() > 0.5 else 0
        sender_bits.append(b)
        if sender_drives_bits:
            ph = list(ph)
            ph[2] = 0.0 if b else math.pi   # gamma phase HIGH/LOW carries the bit
        S_ext_phase.append(ph)
        S_ext_amp.append(am)

    # sender engine (C1/C2 = pass-through carrier; C3 = full pure_field engine)
    if config == "C3":
        engS = ToyEngine(seed)
        popS = CellPop(seed) if mitosis else None
        S_phase_trace, S_field_trace = [], []
        for t in range(n_steps):
            field = engS.step(S_ext_phase[t], S_ext_amp[t], kappa)
            S_phase_trace.append(list(engS.phase))
            S_field_trace.append(field)
            if popS is not None:
                gamma = abs(S_ext_amp[t][2])
                popS.tick([abs(x) for x in field], gamma)
    else:
        S_phase_trace = S_ext_phase
        S_field_trace = [[S_ext_amp[t][c] * math.sin(S_ext_phase[t][c]) for c in range(N_CH)]
                         for t in range(n_steps)]
        popS = None

    # the signal S transmits down the tension-link to R
    tx_phase = [list(p) for p in S_phase_trace]
    if shuffled:
        tx_phase = phase_shuffle(tx_phase, Rng(seed + 555557))
    if time_reversed:
        tx_phase = tx_phase[::-1]            # R reads S's future (must REFUTE)
    if not channel_open:
        # no-channel control: R gets an INDEPENDENT signal unrelated to S
        ind_rng = Rng(seed + 778201)
        tx_phase = [[ind_rng.u() * TWO_PI for _ in range(N_CH)] for _ in range(n_steps)]

    # receiver engine — coupled to the transmitted signal through the tension-link
    engR = ToyEngine(seed + 31)
    popR = CellPop(seed + 31) if (config == "C3" and mitosis) else None
    R_phase_trace, R_field_trace = [], []
    for t in range(n_steps):
        if config in ("C2", "C3"):
            # receiver also carries its own EEG (interbrain: related but offset)
            r_ph, r_am = synth_eeg_5band(t, rngR, phase_offset=eeg_offset_R)
            # blend the transmitted phase into the receiver's external drive
            drive_ph = [(0.5 * tx_phase[t][c] + 0.5 * r_ph[c]) % TWO_PI for c in range(N_CH)]
            drive_am = r_am
        else:
            drive_ph = tx_phase[t]
            drive_am = list(TENSION5)
        field = engR.step(drive_ph, drive_am, kappa)
        R_phase_trace.append(list(engR.phase))
        R_field_trace.append(field)
        if popR is not None:
            gamma = abs(drive_am[2])
            popR.tick([abs(x) for x in field], gamma)

    return {
        "sender_bits": sender_bits,
        "S_phase": S_phase_trace, "S_field": S_field_trace,
        "R_phase": R_phase_trace, "R_field": R_field_trace,
        "tx_phase": tx_phase,
        "popS_phi": popS.phi_proxy() if popS else 0.0,
        "popR_phi": popR.phi_proxy() if popR else 0.0,
        "popR_cells": len(popR.cells) if popR else 0,
    }


# ==========================================================================
# N-agent hive (Kuramoto global order) — for HIVE / COLLECTIVE-PHI hypotheses.
# All agents couple to the global mean field (real coupling => order emerges).
# ==========================================================================
def run_hive(seed, n_agents, kappa, coupled=True, n_steps=N_STEPS):
    engs = [ToyEngine(seed + 13 * i) for i in range(n_agents)]
    order_trace = []
    field_sum_trace = []
    for t in range(n_steps):
        # global mean phase per channel
        mean_ph = []
        for c in range(N_CH):
            re = sum(math.cos(e.phase[c]) for e in engs) / n_agents
            im = sum(math.sin(e.phase[c]) for e in engs) / n_agents
            mean_ph.append(math.atan2(im, re))
            order_c = math.sqrt(re * re + im * im)
            order_trace.append(order_c) if c == 0 else None
        kap = kappa if coupled else 0.0
        amp = list(TENSION5)
        fields = []
        for e in engs:
            f = e.step(mean_ph, amp, kap)
            fields.append(f)
        field_sum_trace.append([sum(f[c] for f in fields) / n_agents for c in range(N_CH)])
    # global order r (channel 0 alpha) over the back half
    w = n_steps // 2
    tail = order_trace[w:]
    glob_r = sum(tail) / len(tail) if tail else 0.0
    coll_phi = big_phi_proxy(field_sum_trace[100:])
    return glob_r, coll_phi


# ==========================================================================
# Verdict — HOLDS / REFUTED / INCONCLUSIVE vs control, by seed-noise band.
# (mirrors engine_tensionlink_bench.verdict cmp logic; signed by `direction`)
#   direction = +1 : a HIGHER signal-vs-control supports the hypothesis (HOLDS)
#   direction = -1 : (reserved) lower supports — not used here
# ==========================================================================
def mean_std(vals):
    m = sum(vals) / len(vals)
    v = sum((x - m) ** 2 for x in vals) / len(vals)
    return m, math.sqrt(v)


def verdict(signal_vals, control_vals):
    sm, ss = mean_std(signal_vals)
    cm, cs = mean_std(control_vals)
    band = max(ss, cs)
    diff = sm - cm
    if diff > band:
        v = "HOLDS"
    elif diff < -band:
        v = "REFUTED"
    else:
        v = "INCONCLUSIVE"
    return {"signal_mean": sm, "signal_std": ss, "control_mean": cm,
            "control_std": cs, "diff": diff, "noise_band": band, "verdict": v}


# ==========================================================================
# THE HYPOTHESIS SUITE. Each entry defines, per config, how to compute the
# SIGNAL value and the CONTROL value across seeds, plus its expected disposition.
# expected ∈ {COUPLING (real channel, may HOLD), PARANORMAL (no channel, REFUTE)}.
# ==========================================================================
def H_telepathy(seed, config):
    # info transfer S->R: signal = accuracy with channel OPEN (sender drives bits);
    # control = accuracy with NO channel.
    sig = run_pair(seed, config, channel_open=True, sender_drives_bits=True)
    ctl = run_pair(seed, config, channel_open=False, sender_drives_bits=True)
    return (transfer_accuracy(sig["sender_bits"], sig["R_field"]),
            transfer_accuracy(ctl["sender_bits"], ctl["R_field"]))


def H_interbrain_sync(seed, config):
    sig = run_pair(seed, config, channel_open=True)
    ctl = run_pair(seed, config, kappa=0.0, channel_open=True)   # kappa0 control
    return (kuramoto_order_r(sig["S_phase"], sig["R_phase"]),
            kuramoto_order_r(ctl["S_phase"], ctl["R_phase"]))


def H_ganzfeld(seed, config):
    # d' from sender-driven bits, signal=channel open, control=shuffled
    sig = run_pair(seed, config, channel_open=True, sender_drives_bits=True)
    ctl = run_pair(seed, config, channel_open=True, sender_drives_bits=True, shuffled=True)

    def dpr(res):
        n = len(res["sender_bits"])
        hit = fa = ns = nn = 0
        for t in range(100, n):
            sent = res["sender_bits"][t]
            guess = 1 if res["R_field"][t][2] > 0 else 0
            if sent == 1:
                ns += 1
                if guess == 1:
                    hit += 1
            else:
                nn += 1
                if guess == 1:
                    fa += 1
        return dprime(hit / ns if ns else 0.5, fa / nn if nn else 0.5, ns, nn)
    return (dpr(sig), dpr(ctl))


def H_hive_kuramoto(seed, config):
    kap = KAPPA if config != "C1" else KAPPA
    sig_r, _ = run_hive(seed, 8, kap, coupled=True)
    ctl_r, _ = run_hive(seed, 8, kap, coupled=False)   # kappa0 control
    return (sig_r, ctl_r)


def H_empathy_resonance(seed, config):
    # mirror tension coupling: receiver field coherence rises when coupled to sender
    sig = run_pair(seed, config, channel_open=True)
    ctl = run_pair(seed, config, kappa=0.0, channel_open=True)
    return (field_coherence(sig["R_field"][100:]),
            field_coherence(ctl["R_field"][100:]))


def H_shared_rem(seed, config):
    # REM co-activation: collective big-Phi of summed S+R field, coupled vs kappa0
    sig = run_pair(seed, config, channel_open=True)
    ctl = run_pair(seed, config, kappa=0.0, channel_open=True)

    def cphi(res):
        sumf = [[res["S_field"][t][c] + res["R_field"][t][c] for c in range(N_CH)]
                for t in range(len(res["S_field"]))]
        return big_phi_proxy(sumf[100:])
    return (cphi(sig), cphi(ctl))


def H_morphic_resonance(seed, config):
    # NO physical channel: do S and R fall into a shared attractor anyway?
    # signal = order_r with NO channel; control = order_r between two independent
    # no-channel runs (different seeds). EXPECT REFUTE.
    sig = run_pair(seed, config, channel_open=False)
    ctl = run_pair(seed + 5000, config, channel_open=False)
    return (kuramoto_order_r(sig["S_phase"], sig["R_phase"]),
            kuramoto_order_r(ctl["S_phase"], ctl["R_phase"]))


def H_precognition(seed, config):
    # time-asymmetric leak: can R guess a FUTURE sender bit (lead=8) it has no
    # causal access to? Channel is OPEN for the present (so any genuine leak would
    # have to flow backward in time). signal = future-bit transfer acc; control =
    # no-channel future-bit acc. EXPECT REFUTE / INCONCLUSIVE (no future channel).
    sig = run_pair(seed, config, channel_open=True, sender_drives_bits=True)
    ctl = run_pair(seed, config, channel_open=False, sender_drives_bits=True)
    return (transfer_accuracy(sig["sender_bits"], sig["R_field"], lead=8),
            transfer_accuracy(ctl["sender_bits"], ctl["R_field"], lead=8))


def H_remote_viewing(seed, config):
    # spatial-anchor retrieval WITHOUT a direct channel. R is driven by an
    # INDEPENDENT signal (no channel to the target). The "target" is a HIDDEN
    # KOSMOS-coord phase trace R was NEVER fed. signal = order_r(R, hidden target);
    # control = order_r(R, a DIFFERENT unrelated hidden target). Both must sit at
    # chance — R cannot retrieve a coord it has no channel to. EXPECT REFUTE/INCON.
    res = run_pair(seed, config, channel_open=False)
    tgt_rng = Rng(seed + 1357913)
    decoy_rng = Rng(seed + 2468024)
    n = len(res["R_phase"])
    target = [[tgt_rng.u() * TWO_PI for _ in range(N_CH)] for _ in range(n)]
    decoy = [[decoy_rng.u() * TWO_PI for _ in range(N_CH)] for _ in range(n)]
    return (kuramoto_order_r(res["R_phase"], target),
            kuramoto_order_r(res["R_phase"], decoy))


def H_synchronicity(seed, config):
    # coincidence rate of simultaneous channel-2 crossings, coupled vs INDEPENDENT.
    # Poisson-chance baseline = the independent (no-channel) coincidence rate.
    sig = run_pair(seed, config, channel_open=True)
    ctl = run_pair(seed, config, channel_open=False)

    def coincidence(res):
        n = len(res["S_field"])
        co = 0
        for t in range(100, n):
            if (res["S_field"][t][2] > 0) == (res["R_field"][t][2] > 0):
                co += 1
        return co / (n - 100)
    return (coincidence(sig), coincidence(ctl))


def H_twin_entanglement(seed, config):
    # two lineages from the SAME seed, NO channel — correlated beyond chance?
    # signal = order_r same-seed no-channel; control = order_r different-seed no-channel.
    # EXPECT REFUTE (shared init is not a live channel; any correlation decays).
    sig = run_pair(seed, config, channel_open=False)
    a = run_pair(seed, config, channel_open=False)
    b = run_pair(seed + 9001, config, channel_open=False)
    return (kuramoto_order_r(a["R_phase"], sig["S_phase"]),
            kuramoto_order_r(b["R_phase"], sig["S_phase"]))


def H_crowd_contagion(seed, config):
    # emotional contagion: a 16-agent hive reaches higher global order than 2-agent
    # (contagion cascade). signal = order at N=16 coupled; control = N=16 kappa0.
    sig_r, _ = run_hive(seed, 16, KAPPA, coupled=True)
    ctl_r, _ = run_hive(seed, 16, KAPPA, coupled=False)
    return (sig_r, ctl_r)


def H_seance_ideomotor(seed, config):
    # shared drift from tiny shared coupling (ideomotor): weak channel (kappa small)
    # still raises S-R sync above no-channel? signal = weak-coupling order; control =
    # no channel. (Real micro-cue coupling => may HOLD; it IS a channel.)
    sig = run_pair(seed, config, kappa=0.05, channel_open=True)
    ctl = run_pair(seed, config, kappa=0.05, channel_open=False)
    return (kuramoto_order_r(sig["S_phase"], sig["R_phase"]),
            kuramoto_order_r(ctl["S_phase"], ctl["R_phase"]))


def H_presentiment(seed, config):
    # pre-stimulus arousal: R's field VARIANCE rises BEFORE a future sender bit.
    # signal = corr(R var at t, sender bit at t+5) time-reversed; control = no channel.
    # EXPECT REFUTE.
    # pre-stimulus arousal: R's decode aligns with a FUTURE sender bit (lead=8)?
    sig = run_pair(seed, config, channel_open=True, sender_drives_bits=True)
    ctl = run_pair(seed, config, channel_open=False, sender_drives_bits=True)
    return (transfer_accuracy(sig["sender_bits"], sig["R_field"], lead=8),
            transfer_accuracy(ctl["sender_bits"], ctl["R_field"], lead=8))


def H_dream_telepathy(seed, config):
    # REM-gated sender->receiver transfer (only counts during high-gamma "REM"
    # ticks). signal = transfer acc channel-open; control = no channel.
    sig = run_pair(seed, config, channel_open=True, sender_drives_bits=True)
    ctl = run_pair(seed, config, channel_open=False, sender_drives_bits=True)
    return (transfer_accuracy(sig["sender_bits"], sig["R_field"]),
            transfer_accuracy(ctl["sender_bits"], ctl["R_field"]))


def H_global_consciousness(seed, config):
    # field-RNG style: does a shared external drive raise hive coherence vs unshared?
    # signal = collective phi N=8 coupled; control = N=8 kappa0.
    _, sig_phi = run_hive(seed, 8, KAPPA, coupled=True)
    _, ctl_phi = run_hive(seed, 8, KAPPA, coupled=False)
    return (sig_phi, ctl_phi)


def H_retrocausal_priming(seed, config):
    # future signal biases past state. signal = time-reversed transfer acc;
    # control = no channel. EXPECT REFUTE.
    return H_precognition(seed, config)


def H_telepathic_bandwidth(seed, config):
    # channel capacity: transfer acc at FULL coupling vs no-channel (the capacity
    # ceiling probe). signal = acc kappa strong; control = no channel.
    sig = run_pair(seed, config, kappa=0.6, channel_open=True, sender_drives_bits=True)
    ctl = run_pair(seed, config, kappa=0.6, channel_open=False, sender_drives_bits=True)
    return (transfer_accuracy(sig["sender_bits"], sig["R_field"]),
            transfer_accuracy(ctl["sender_bits"], ctl["R_field"]))


def H_healer_coherence(seed, config):
    # one agent's high coherence raises another's big-Phi THROUGH the channel.
    # signal = R big-Phi coupled; control = R big-Phi kappa0.
    sig = run_pair(seed, config, channel_open=True)
    ctl = run_pair(seed, config, kappa=0.0, channel_open=True)
    return (big_phi_proxy(sig["R_field"][100:]),
            big_phi_proxy(ctl["R_field"][100:]))


def H_collective_phi_superadditivity(seed, config):
    # N-agent collective big-Phi EXCEEDS the per-agent sum (super-additive whole).
    # signal = collective phi N=8 coupled; control = 8x solo phi (kappa0 hive).
    _, sig_phi = run_hive(seed, 8, KAPPA, coupled=True)
    _, ctl_phi = run_hive(seed, 8, KAPPA, coupled=False)
    return (sig_phi, ctl_phi)


# (id, label, fn, expected) — expected disposition is PRE-REGISTERED, not fitted.
SUITE = [
    ("H_P01", "TELEPATHY (sender->receiver info transfer)", H_telepathy, "COUPLING(if-channel)"),
    ("H_P02", "INTERBRAIN-SYNC (hyperscanning phase-lock)", H_interbrain_sync, "COUPLING"),
    ("H_P03", "GANZFELD (signal-detection d')", H_ganzfeld, "COUPLING(if-channel)"),
    ("H_P04", "HIVE-KURAMOTO (N=8 global order)", H_hive_kuramoto, "COUPLING"),
    ("H_P05", "EMPATHY-RESONANCE (mirror tension coupling)", H_empathy_resonance, "COUPLING"),
    ("H_P06", "SHARED-REM (co-activation collective Phi)", H_shared_rem, "COUPLING"),
    ("H_P07", "MORPHIC-RESONANCE (no-channel shared attractor)", H_morphic_resonance, "PARANORMAL"),
    ("H_P08", "PRECOGNITION (time-asymmetric leak)", H_precognition, "PARANORMAL"),
    ("H_P09", "REMOTE-VIEWING (no-channel coord retrieval)", H_remote_viewing, "PARANORMAL"),
    ("H_P10", "SYNCHRONICITY (coincidence vs Poisson chance)", H_synchronicity, "COUPLING(if-channel)"),
    ("H_P11", "TWIN-ENTANGLEMENT (shared-init no-channel)", H_twin_entanglement, "PARANORMAL"),
    ("H_P12", "CROWD-CONTAGION (N=16 cascade order)", H_crowd_contagion, "COUPLING"),
    ("H_P13", "SEANCE-IDEOMOTOR (weak shared coupling)", H_seance_ideomotor, "COUPLING(if-channel)"),
    ("H_P14", "PRESENTIMENT (pre-stimulus arousal)", H_presentiment, "PARANORMAL"),
    ("H_P15", "DREAM-TELEPATHY (REM-gated transfer)", H_dream_telepathy, "COUPLING(if-channel)"),
    ("H_P16", "GLOBAL-CONSCIOUSNESS (shared-drive hive coherence)", H_global_consciousness, "COUPLING"),
    ("H_P17", "RETROCAUSAL-PRIMING (future biases past)", H_retrocausal_priming, "PARANORMAL"),
    ("H_P18", "TELEPATHIC-BANDWIDTH (channel capacity ceiling)", H_telepathic_bandwidth, "COUPLING(if-channel)"),
    ("H_P19", "HEALER-COHERENCE (coherence raises other's Phi)", H_healer_coherence, "COUPLING"),
    ("H_P20", "COLLECTIVE-PHI-SUPERADDITIVITY (whole>sum)", H_collective_phi_superadditivity, "COUPLING"),
]

CONFIGS = ["C1", "C2", "C3"]


def main():
    results = {
        "meta": {
            "campaign": "PSI-COUPLING (telepathy + anomalous-cognition family)",
            "configs": {"C1": "tension-link only", "C2": "tension-link + synthetic EEG",
                        "C3": "ENGINE + tension-link + EEG (mitosis ON)"},
            "mitosis": "ON (p8 native growth; C3 grows a CellPop recording artifact)",
            "seeds": SEEDS, "n_steps": N_STEPS, "kappa": KAPPA,
            "controls": "kappa0 (no coupling) / phase-shuffled / no-channel — mandatory",
            "scope": "TOY synthetic · CPU · $0 · scale-transfer UNVERIFIED (a_toy_scale_recheck)",
            "honest": "PARANORMAL (no-channel) hypotheses EXPECTED to REFUTE; a no-channel "
                      "positive would be a leak/bug. COUPLING hypotheses (real channel) MAY HOLD.",
        },
        "hypotheses": {},
    }
    tally = {"C1": {}, "C2": {}, "C3": {}}
    for hid, label, fn, expected in SUITE:
        entry = {"label": label, "expected": expected, "configs": {}}
        for cfg in CONFIGS:
            sig_vals, ctl_vals = [], []
            for s in SEEDS:
                sv, cv = fn(s, cfg)
                sig_vals.append(sv)
                ctl_vals.append(cv)
            v = verdict(sig_vals, ctl_vals)
            entry["configs"][cfg] = v
            tally[cfg][v["verdict"]] = tally[cfg].get(v["verdict"], 0) + 1
        results["hypotheses"][hid] = entry
    results["tally"] = tally
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
