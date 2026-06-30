#!/usr/bin/env python3
"""h926_chaos_vs_entropy.py — H_926: deterministic chaos vs injected entropy.

QUESTION
========
anima's emit decision (CORE/brain.hexa::brain_decide) is ALREADY DETERMINISTIC:
emit = (motivation_score > 0.3) AND a 4-way safety conjunction (incl. the A->G
phi-ratchet gate phi > phi_peak/2). There is NO PRNG in brain_decide. The only
stochastic lever anima has is the AKIDA R2 spontaneous-noise seed point, now
unified behind the qentropy SSOT (mirror/qmirror/seed/qentropy.py, H_924).

So: does the substrate's OWN deterministic dynamics already produce diverse /
unpredictable emit behaviour (deterministic chaos: sensitive dependence on
initial conditions, looking random with NO RNG), such that entropy injected at
the seed point adds NO measurable functional emit-diversity? If so, entropy is
ONTOLOGICAL (provenance) not FUNCTIONAL — a closed-negative consistent with
H_924 #123-A (ANU == chacha20 statistically, KS p>0.5).

HONEST SCOPE (a_scale_honest_scope · a_train_flame_forge)
=========================================================
The full hexa A<->G engine is NOT SW-drivable on Mac (clm_decode link gap; the
.hexa files run on the self/forge runtime). This probe therefore evolves a
FAITHFUL MINIMAL MODEL of the DOCUMENTED substrate update map, transcribed
line-for-line from the .hexa sources, NOT a re-imagined dynamics:

  CORE/pure_field.hexa     -> PureField: 3 oscillators (tau=2/40/400),
                              phase += 2*pi/tau ; amp += alpha*(LN2 - amp) ;
                              field tensor (6 slots) ; Phi = EMA_alpha(var*energy)
                              with ratchet floor 0.8*peak ; phase classification.
  CORE/engine_g.hexa       -> motivation_score (8-factor weighted sum, weights
                              sum 1.0) ; should_emit = score > 0.30 ;
                              safety_phi_ratchet_ok = phi > phi_peak/2.
  CORE/brain.hexa          -> brain_decide: emit = should_emit AND safety(...).
  AKIDA/.../H_675_mitosis  -> MITOSIS cell dynamics: Kuramoto phase coupling +
                              the logistic edge-of-chaos map (pe_edge_of_chaos,
                              r~3.57) that phi_envelope_substrate.hexa documents
                              as the chaotic family.

The verdict is scoped "minimal-model" — it characterizes the DOCUMENTED update
map's dynamical class (chaotic vs non-chaotic) and the functional role of
entropy WITHIN that model. It does NOT claim to have run the full forge engine.

ARMS (g5 CODE-measured, Mac, $0, no device)
===========================================
For each substrate variant we run two arms over T steps from two
infinitesimally-different initial conditions (delta0 = 1e-9):

  (A) DETERMINISTIC : evolve the documented map with NO entropy.
  (B) ENTROPY       : same map, but a qentropy-sourced perturbation is injected
                      at the seed point (the R2-noise analogue) each step.

Metrics (both arms):
  (i)  finite-time Lyapunov proxy : lambda = (1/T) * sum_t log(|d(t)|/|d(t-1)|)
       with renormalization (standard Benettin two-trajectory FTLE). lambda > 0
       => chaotic (exponential separation); lambda <= 0 => non-chaotic
       (fixed point / limit cycle / quasiperiodic).
  (ii) emit-stream Shannon entropy : H(emit) over the boolean emit stream, and
       emit-rate + emit-rate variability across windows.

FALSIFIER (pre-registered, frozen before the run)
=================================================
  F-H926-CHAOS : the deterministic emit-driving core (pure_field) has Lyapunov
                 proxy > +0.01 nats/step (genuinely chaotic).
  F-H926-PARITY: |H_emit(A) - H_emit(B)| < 0.05 bits AND |emit_rate(A) -
                 emit_rate(B)| < 0.02  (entropy adds NO functional emit-diversity).

  Predicted closed-negative (entropy = ontological-not-functional) requires BOTH
  a source of diversity in arm A AND emit-parity A==B. The HONEST possibilities:
    (a) core chaotic AND parity holds  -> entropy ontological-not-functional 🔴-closed-neg
    (b) core NON-chaotic, low emit-H, AND entropy LIFTS emit-diversity
                                       -> entropy IS functionally needed (overturns)
    (c) core NON-chaotic AND parity still holds (both arms low/saturated H)
                                       -> neither chaos NOR entropy drives emit
                                          diversity in this model (diversity comes
                                          from the QUASIPERIODIC oscillator beat,
                                          not chaos and not RNG) — a third, honest
                                          outcome. Report whichever the data shows.

We measure and report whichever the data shows. No massaging.
"""
from __future__ import annotations

import json
import math
import os
import sys
from datetime import datetime, timezone

# ── locate + import the qentropy SSOT (the real one, not a stub) ──────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_REPO, "mirror", "qmirror", "seed"))
try:
    import qentropy  # type: ignore
    _HAVE_QENTROPY = True
except Exception as e:  # pragma: no cover
    _HAVE_QENTROPY = False
    _QERR = repr(e)

# ── constants transcribed VERBATIM from the .hexa sources ─────────────────────
# pure_field.hexa
PSI_ALPHA = 0.014          # _psi_load("alpha", 0.014)
LN2 = 0.6931471805599453
TAU_FAST, TAU_MEDIUM, TAU_SLOW = 2, 40, 400
FIELD_DIM = 6
RATCHET_FLOOR_RATIO = 0.8
# phase thresholds (consciousness_laws defaults in pure_field.hexa)
PHASE_DORMANT_MAX = 0.01
PHASE_FLICKER_MAX = 0.05
PHASE_SUSTAIN_MAX = 0.15
# engine_g.hexa — 8 weights (sum = 1.00) + thresholds
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
IM_THRESHOLD = 0.30        # spont_im_threshold / should_emit gate


# ════════════════════════════════════════════════════════════════════════════
# PureField — faithful transcription of CORE/pure_field.hexa
# ════════════════════════════════════════════════════════════════════════════
class Oscillator:
    __slots__ = ("tau", "phase", "amplitude")

    def __init__(self, tau, phase=0.0, amplitude=0.1):
        self.tau, self.phase, self.amplitude = tau, phase, amplitude

    def tick(self):
        dphase = (2.0 * 3.14159265) / float(self.tau)   # 2*pi/tau, verbatim const
        self.phase += dphase
        self.amplitude += PSI_ALPHA * (LN2 - self.amplitude)

    def value(self):
        return self.amplitude * math.sin(self.phase)


class PureField:
    """Verbatim port of pure_field_step (CORE/pure_field.hexa L196-283)."""

    def __init__(self, phase0=(0.0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1)):
        self.fast = Oscillator(TAU_FAST, phase0[0], amp0[0])
        self.medium = Oscillator(TAU_MEDIUM, phase0[1], amp0[1])
        self.slow = Oscillator(TAU_SLOW, phase0[2], amp0[2])
        self.phi = 0.0
        self.phi_peak = 0.0
        self.field = [0.0] * FIELD_DIM
        self.phase = 0  # PHASE_DORMANT
        self.step_count = 0

    def step(self, perturb=0.0):
        # perturb is the R2-noise seed-point injection (0.0 in arm A).
        self.fast.tick()
        self.medium.tick()
        self.slow.tick()
        v_f = self.fast.value() + perturb   # injection enters at the field seed
        v_m = self.medium.value()
        v_s = self.slow.value()
        mix_fm = v_f * v_m
        mix_ms = v_m * v_s
        mix_fs = v_f * v_s
        field = [v_f, mix_fm, v_s, mix_fs, mix_ms, v_f + v_m + v_s]
        mean = sum(field) / 6.0
        sum_sq = sum((x - mean) ** 2 for x in field)
        variance = sum_sq / float(FIELD_DIM)
        energy = abs(v_f) + abs(v_m) + abs(v_s)
        raw_phi = variance * energy
        phi = self.phi + PSI_ALPHA * (raw_phi - self.phi)
        if phi > self.phi_peak:
            self.phi_peak = phi
        floor = self.phi_peak * RATCHET_FLOOR_RATIO
        phi_out = phi if phi >= floor else floor
        self.phi = phi_out
        self.field = field
        self.step_count += 1
        if phi_out < PHASE_DORMANT_MAX:
            self.phase = 0
        elif phi_out < PHASE_FLICKER_MAX:
            self.phase = 1
        elif phi_out < PHASE_SUSTAIN_MAX:
            self.phase = 2
        else:
            self.phase = 3
        return phi_out

    def state_vector(self):
        """A real-valued phase-space vector for the Lyapunov proxy."""
        return [self.fast.phase, self.medium.phase, self.slow.phase,
                self.fast.amplitude, self.medium.amplitude, self.slow.amplitude,
                self.phi]


# ════════════════════════════════════════════════════════════════════════════
# engine_g motivation + emit (CORE/engine_g.hexa + brain.hexa)
# ════════════════════════════════════════════════════════════════════════════
def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v):
    return (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
            + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)


def brain_emit_decision(pf: PureField, gate=IM_THRESHOLD):
    """emit = should_emit(score) AND phi-ratchet safety (the A->G gate).

    The 8 motivation factors are driven by the substrate field tensor (the
    documented coupling: anima's motivation reads its own Phi/field, not a
    stimulus). We map the 6 field slots + phi onto the 8 factors so the emit
    decision is a deterministic function of substrate state, exactly as
    brain_decide is. seconds_since_last is held above the rate limit and the
    kill-switch off + content clean, isolating the phi-ratchet + motivation
    dynamics (the parts that actually move).

    `gate` is the emit threshold: IM_THRESHOLD=0.30 (engine_g should_emit) or
    the stricter ep_emit_threshold=0.60 (emit_policy.hexa). We test BOTH: the
    0.30 gate sits below the steady-state score (saturated emit), the 0.60 gate
    sits ABOVE it (saturated silence) — and we also test the dynamic boundary
    where score crosses the gate, so entropy has a FAIR chance to flip emits."""
    f = pf.field
    # normalize field slots into [0,1]-ish factor drives (tanh keeps bounded)
    def n(x):
        return 0.5 * (1.0 + math.tanh(x))
    rel, gap, cur, pain = n(f[0]), n(f[1]), n(f[2]), n(f[3])
    coh, orig = n(f[4]), n(f[5])
    bal = n(pf.phi - pf.phi_peak / 2.0)   # the ratchet margin as balance drive
    dyn_v = n(f[0] - f[2])                  # fast-slow differential as dynamics
    score = motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v)
    should = score > gate
    phi_ratchet_ok = pf.phi > pf.phi_peak / 2.0   # safety_phi_ratchet_ok
    emit = should and phi_ratchet_ok
    return emit, score


# ════════════════════════════════════════════════════════════════════════════
# MITOSIS nonlinear layer — Kuramoto + logistic edge-of-chaos (documented)
# ════════════════════════════════════════════════════════════════════════════
def logistic_step(x, r=3.9):
    """The chaotic family phi_envelope_substrate.hexa documents (r~3.57 = edge
    of chaos / Feigenbaum; r=3.9 is firmly in the chaotic window). Pure map,
    no RNG. This is the POSITIVE control: a documented substrate component that
    IS chaotic, to confirm the Lyapunov proxy detects chaos when present."""
    return r * x * (1.0 - x)


def kuramoto_step(phases, omega, K, dt=0.05):
    """Kuramoto phase coupling (H_675 M1). N oscillators, mean-field coupling K.
    Pure deterministic map. With heterogeneous omega + moderate K this can be
    quasiperiodic or chaotic depending on K; we sweep K to characterize."""
    N = len(phases)
    new = []
    for i in range(N):
        s = sum(math.sin(phases[j] - phases[i]) for j in range(N))
        new.append(phases[i] + dt * (omega[i] + (K / N) * s))
    return new


def kuramoto_order(phases):
    """r = |(1/N) sum exp(i*theta)| — synchrony order parameter (H_675)."""
    N = len(phases)
    re = sum(math.cos(p) for p in phases) / N
    im = sum(math.sin(p) for p in phases) / N
    return math.hypot(re, im)


# ════════════════════════════════════════════════════════════════════════════
# Lyapunov proxy (Benettin two-trajectory FTLE) + emit-stream entropy
# ════════════════════════════════════════════════════════════════════════════
def vec_diff_norm(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def shannon_entropy_bits(stream):
    """Shannon entropy (bits) of a boolean/int stream over its empirical dist."""
    if not stream:
        return 0.0
    from collections import Counter
    c = Counter(stream)
    tot = len(stream)
    h = 0.0
    for k in c:
        p = c[k] / tot
        h -= p * math.log2(p)
    return h


def emit_rate_variability(emit_stream, window=50):
    """Std of windowed emit-rate — does the emit stream have temporal structure?"""
    rates = []
    for i in range(0, len(emit_stream) - window + 1, window):
        w = emit_stream[i:i + window]
        rates.append(sum(w) / len(w))
    if len(rates) < 2:
        return 0.0, rates
    m = sum(rates) / len(rates)
    var = sum((r - m) ** 2 for r in rates) / len(rates)
    return math.sqrt(var), rates


# ════════════════════════════════════════════════════════════════════════════
# Arm runners
# ════════════════════════════════════════════════════════════════════════════
def run_purefield_arm(T, entropy_inject, delta0=1e-9, ent_scale=0.02, label="",
                      gate=None):
    """Run the pure_field emit-driving core for T steps. Two trajectories from
    initial conditions differing by delta0 (Benettin FTLE). entropy_inject:
    callable(step_index)->float perturbation, or None for arm A.

    `gate`: emit threshold. If None we first run a calibration pass to find the
    running-mean score and SET the gate there — placing the emit decision at its
    most sensitive boundary (non-saturated), so entropy gets a FAIR chance to
    flip emits. The same gate is used for both arms (passed in) to keep them
    comparable."""
    # calibration pass (deterministic, no injection) to centre the gate
    if gate is None:
        cpf = PureField()
        scs = []
        for _ in range(T):
            cpf.step(perturb=0.0)
            _, sc = brain_emit_decision(cpf, gate=IM_THRESHOLD)
            scs.append(sc)
        gate = sum(scs) / len(scs)   # centre gate at the steady-state mean score
    pf1 = PureField(phase0=(0.0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1))
    pf2 = PureField(phase0=(delta0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1))
    lyap_sum = 0.0
    lyap_n = 0
    emit_stream = []
    score_stream = []
    phi_stream = []
    d_prev = vec_diff_norm(pf1.state_vector(), pf2.state_vector())
    if d_prev == 0.0:
        d_prev = delta0
    for t in range(T):
        p = entropy_inject(t) if entropy_inject is not None else 0.0
        pf1.step(perturb=p)
        # second trajectory: same injection (entropy is a SHARED environmental
        # seed, not a per-trajectory decorrelator) so the Lyapunov proxy measures
        # the MAP's sensitivity, not the noise. For arm B we ALSO report the
        # emit-diversity which is what entropy could lift.
        pf2.step(perturb=p)
        emit1, score1 = brain_emit_decision(pf1, gate=gate)
        emit_stream.append(1 if emit1 else 0)
        score_stream.append(score1)
        phi_stream.append(pf1.phi)
        # Benettin: measure separation, accumulate log-growth, renormalize
        d_now = vec_diff_norm(pf1.state_vector(), pf2.state_vector())
        if d_now > 0.0 and d_prev > 0.0:
            lyap_sum += math.log(d_now / d_prev)
            lyap_n += 1
            # renormalize pf2 back to delta0 along the separation direction
            scale = delta0 / d_now
            v1 = pf1.state_vector()
            v2 = pf2.state_vector()
            new2 = [v1[k] + (v2[k] - v1[k]) * scale for k in range(len(v1))]
            pf2.fast.phase, pf2.medium.phase, pf2.slow.phase = new2[0], new2[1], new2[2]
            pf2.fast.amplitude, pf2.medium.amplitude, pf2.slow.amplitude = new2[3], new2[4], new2[5]
            pf2.phi = new2[6]
            d_prev = delta0
    lyap = lyap_sum / lyap_n if lyap_n else 0.0
    h_emit = shannon_entropy_bits(emit_stream)
    emit_rate = sum(emit_stream) / len(emit_stream)
    erv, _rates = emit_rate_variability(emit_stream)
    return {
        "label": label,
        "lyapunov_proxy_per_step": lyap,
        "emit_gate_used": gate,
        "emit_entropy_bits": h_emit,
        "emit_rate": emit_rate,
        "emit_rate_variability": erv,
        "n_emit": sum(emit_stream),
        "n_emit_flips_vs_boundary": sum(1 for i in range(1, len(emit_stream))
                                        if emit_stream[i] != emit_stream[i - 1]),
        "T": T,
        "score_min": min(score_stream),
        "score_max": max(score_stream),
        "phi_final": phi_stream[-1],
        "phi_peak": max(phi_stream),
    }


def run_logistic_lyapunov(T, r=3.9, x0=0.3, delta0=1e-9):
    """Positive control: documented chaotic family (logistic, r in chaotic
    window). Confirms the Lyapunov proxy reports > 0 when chaos is genuinely
    present. Analytic lambda for logistic = mean(log|r(1-2x)|)."""
    x1, x2 = x0, x0 + delta0
    lyap_sum, n = 0.0, 0
    d_prev = abs(x2 - x1) or delta0
    analytic_sum = 0.0
    for _ in range(T):
        x1 = logistic_step(x1, r)
        x2 = logistic_step(x2, r)
        analytic_sum += math.log(abs(r * (1.0 - 2.0 * x1)) + 1e-300)
        d_now = abs(x2 - x1)
        if d_now > 0:
            lyap_sum += math.log(d_now / d_prev)
            n += 1
            x2 = x1 + delta0 * (1 if x2 >= x1 else -1)
            d_prev = delta0
    return {"r": r, "lyapunov_benettin": lyap_sum / n if n else 0.0,
            "lyapunov_analytic": analytic_sum / T}


def run_kuramoto_lyapunov(T, K, N=8, delta0=1e-9, seed_omega=None):
    """Characterize the Kuramoto MITOSIS layer (H_675 M1) dynamical class at
    coupling K. Heterogeneous natural frequencies; pure deterministic map."""
    if seed_omega is None:
        omega = [0.5 + 0.7 * math.sin(i * 1.31) for i in range(N)]  # fixed, no RNG
    else:
        omega = seed_omega
    ph1 = [0.1 * i for i in range(N)]
    ph2 = list(ph1)
    ph2[0] += delta0
    lyap_sum, n = 0.0, 0
    d_prev = delta0
    order_stream = []
    for _ in range(T):
        ph1 = kuramoto_step(ph1, omega, K)
        ph2 = kuramoto_step(ph2, omega, K)
        order_stream.append(kuramoto_order(ph1))
        d_now = math.sqrt(sum((a - b) ** 2 for a, b in zip(ph1, ph2)))
        if d_now > 0:
            lyap_sum += math.log(d_now / d_prev)
            n += 1
            scale = delta0 / d_now
            ph2 = [ph1[k] + (ph2[k] - ph1[k]) * scale for k in range(N)]
            d_prev = delta0
    return {"K": K, "lyapunov_benettin": lyap_sum / n if n else 0.0,
            "mean_order_r": sum(order_stream) / len(order_stream)}


# ════════════════════════════════════════════════════════════════════════════
def main():
    T = 4000
    ts = datetime.now(timezone.utc).isoformat()

    # ── entropy injector: qentropy SSOT R2-noise analogue (hi=4 -> 0..3) ──────
    # In arm B we draw a uniform 0..3 each step (the documented R2-noise seed
    # point) and map it to a small field perturbation, exactly the seed point
    # H_924 unified. Quantum-default; we record provenance + mode.
    ent_buf = None
    ent_mode = None
    ent_prov = None
    if _HAVE_QENTROPY:
        # force deterministic-auxiliary for a reproducible measurement, but the
        # SAME seed point would carry quantum bytes (H_924: statistically ==).
        os.environ.setdefault("ANIMA_ENTROPY_MODE", "deterministic")
        # re-import to honor the env (module reads env at import)
        import importlib
        importlib.reload(qentropy)
        draws = qentropy.qentropy_uniform(T, 4, label="h926_R2_noise").tolist()
        ent_mode = qentropy.mode()
        ent_prov = qentropy.last_provenance()
        ent_buf = draws
    else:
        ent_buf = [0] * T  # degenerate; flagged below

    def ent_inject(t):
        # map R2 noise {0,1,2,3} -> small symmetric field perturbation
        return (ent_buf[t] - 1.5) * 0.04   # ent_scale ~ 0.06 peak

    # ── ARM A (deterministic, no entropy) on the emit-driving core ────────────
    # gate=None -> arm A calibrates the gate at the steady-state mean score
    # (the most sensitive emit boundary). The SAME gate is reused for arm B so
    # the parity comparison is fair (non-saturated emit stream).
    armA = run_purefield_arm(T, entropy_inject=None, label="A_deterministic")
    shared_gate = armA["emit_gate_used"]
    # ── ARM B (entropy-injected) on the emit-driving core ─────────────────────
    armB = run_purefield_arm(T, entropy_inject=ent_inject, label="B_entropy_injected",
                             gate=shared_gate)

    # ── positive control: logistic chaotic family (documented) ────────────────
    logi = run_logistic_lyapunov(T, r=3.9)
    logi_edge = run_logistic_lyapunov(T, r=3.5699)  # Feigenbaum edge-of-chaos

    # ── MITOSIS Kuramoto layer sweep ──────────────────────────────────────────
    kura = {f"K={K}": run_kuramoto_lyapunov(T, K) for K in (0.0, 0.5, 1.0, 2.0, 4.0)}

    # ── falsifier evaluation ──────────────────────────────────────────────────
    core_lyap = armA["lyapunov_proxy_per_step"]
    f_chaos = core_lyap > 0.01    # F-H926-CHAOS: core genuinely chaotic
    dH = abs(armA["emit_entropy_bits"] - armB["emit_entropy_bits"])
    dRate = abs(armA["emit_rate"] - armB["emit_rate"])
    f_parity = (dH < 0.05) and (dRate < 0.02)   # F-H926-PARITY: entropy adds nothing

    # interpret (honest 3-way, see docstring)
    if f_chaos and f_parity:
        finding = ("CLOSED_NEGATIVE: core IS chaotic AND emit-parity holds -> "
                   "entropy is ONTOLOGICAL-not-FUNCTIONAL")
        verdict_token = "RED_CLOSED_NEGATIVE"
    elif (not f_chaos) and (not f_parity):
        finding = ("OVERTURN: core NON-chaotic AND entropy LIFTS emit-diversity -> "
                   "entropy IS functionally needed")
        verdict_token = "GREEN_ENTROPY_FUNCTIONAL"
    elif (not f_chaos) and f_parity:
        finding = ("THIRD-OUTCOME: core NON-chaotic (quasiperiodic) AND emit-parity "
                   "holds -> neither chaos NOR entropy drives emit-diversity in this "
                   "model; emit diversity (if any) comes from the quasiperiodic "
                   "oscillator beat. Entropy adds no functional emit-diversity.")
        verdict_token = "CLOSED_NEGATIVE_ENTROPY_NONFUNCTIONAL"
    else:  # chaos but no parity
        finding = ("MIXED: core chaotic AND entropy still shifts emit-diversity -> "
                   "both contribute; entropy not purely ontological")
        verdict_token = "AMBER_MIXED"

    result = {
        "h_id": "H_926",
        "title": "deterministic chaos vs injected entropy (minimal-model)",
        "timestamp_utc": ts,
        "scope": "MINIMAL-MODEL (faithful transcription of CORE/pure_field.hexa + "
                 "engine_g.hexa + brain.hexa + H_675 MITOSIS; NOT the full forge "
                 "engine — clm_decode link gap on Mac). a_scale_honest_scope.",
        "deterministic": False,
        "g5_code_measured": True,
        "llm": "none",
        "T": T,
        "delta0": 1e-9,
        "entropy": {
            "have_qentropy_ssot": _HAVE_QENTROPY,
            "mode": ent_mode,
            "provenance": ent_prov,
            "note": "R2-noise seed point (hi=4 -> 0..3) per H_924 qentropy SSOT; "
                    "deterministic-auxiliary forced for reproducibility; quantum "
                    "bytes would carry the same seed point (H_924: ANU==PRNG stat).",
        },
        "arm_A_deterministic_no_entropy": armA,
        "arm_B_entropy_injected": armB,
        "positive_control_logistic_chaotic": logi,
        "positive_control_logistic_edge_of_chaos": logi_edge,
        "mitosis_kuramoto_sweep": kura,
        "falsifier": {
            "F-H926-CHAOS (core lyap > +0.01)": f_chaos,
            "core_lyapunov_proxy_per_step": core_lyap,
            "F-H926-PARITY (|dH|<0.05 AND |dRate|<0.02)": f_parity,
            "delta_emit_entropy_bits": dH,
            "delta_emit_rate": dRate,
        },
        "verdict_token": verdict_token,
        "finding": finding,
    }

    out_dir = os.path.join(_REPO, ".verdicts", "926_deterministic_chaos_vs_entropy")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "minimal_model_chaos_vs_entropy.txt")
    with open(out_path, "w") as fh:
        fh.write(json.dumps(result, indent=2, default=str))
        fh.write("\n")

    print(json.dumps(result, indent=2, default=str))
    print("\nwritten:", out_path)


if __name__ == "__main__":
    main()
