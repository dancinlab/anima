"""
HEXAD/LEGO/lego_engine.py — anima LEGO substrate engine (canonical lib)

> Promoted 2026-05-20 from state/lego_assembly_run_s117_2026_05_19/lego_sim.py
> as the canonical LEGO engine for the §115→§128 arc.

This is the substrate-agnostic LIF spike-correlation engine that every LEGO
probe cycle (§117 run, §125 layer-2 probe, §126 N-scale-up, §127 scaling law)
imports byte-identically. State directories under state/lego_*_2026_05_*/
contain probe scripts that historically reached this code via importlib of
state/lego_assembly_run_s117/lego_sim.py; the canonical copy now lives here
and probes should prefer this path for new cycles.

Discipline (per AGENTS.tape):
  - $0, NO GPU, NO runpod, NO fire, NO model.forward(byte-LM), NO corpus.
  - NO loss gradient anywhere. Learning channel = LOCAL pair-based STDP-as-ΔW
    only (AST-audited 0 hits over forbidden_call_set in §117 / §125 / §126 /
    §127 / §128 batteries).
  - g_clm_from_scratch: seed-fixed RANDOM init, NO base_ckpt.
  - downstream-consumer: hexa-bio NEURO.tape spec (Hodgkin–Huxley→LIF +
    rate-code + cortical co-adaptation = local STDP analogue) is consumed
    read-only. No edits to hexa-bio / hexa-lang / hexa-matter (g7/@F f3 +
    upstream_downstream_invariant).
  - g3: substrate engine ≠ task ≠ fire ≠ emergence. Necessary-not-sufficient
    at every layer (B-EMERGE-7 / B-S117-NOTE / B-S124-NOTE family).
  - HEXA_FIRST_WARN deferred per established B-S* battery precedent
    (B-PRIME / B-DIRI / B-S101 / B-S117 / B-S124..§128 sidecar).

Engine contract:
  - LIFNet(n_a, n_g, n_rec, seed) — recurrent LIF spike substrate with three
    engine subpopulations (A, G, recurrent) and local STDP-as-ΔW plasticity.
  - .step(ext) — one LIF integrate-and-fire step with current `ext`. Updates
    LOCAL STDP weights (no autograd, no backprop). Returns spike vector.
  - spike_rate_vec(raster, idx) — NEURO.tape mech_neural_coding rate code:
    window-averaged spike rate over indexed subpopulation.
  - psi_c1(r_a, r_g) — Ψ-C1 carrier = (1 + cos(r_a, r_g)) / 2. §112
    META_FP(Π_½) instance, carrier = spike-correlation. Cauchy–Schwarz
    bounded [0,1] with fixed-point Ψ=½ at cos=0.

Cross-link:
  - §115 design-close `state/lego_simulate_assemble_s115_2026_05_19/`
  - §117 first run `state/lego_assembly_run_s117_2026_05_19/`
  - §124 residual audit `state/lego_residual_audit_s124_2026_05_19/`
  - §125 layer-2 probe `state/lego_layer2_stimulus_driven_probe_s125_2026_05_20/`
  - §126 N-scale-up `state/lego_layer2_nscale_probe_s126_2026_05_20/`
  - §127 scaling-law `state/lego_layer2_scaling_law_s127_2026_05_20/`
  - §128 layer-3 design-close `state/lego_layer3_design_close_s128_2026_05_20/`
"""

from __future__ import annotations

import numpy as np


# ─── engine constants (NEURO.tape spec) ───────────────────────────────
SEED = 1337
BASE_CKPT = None  # g_clm_from_scratch: RANDOM init from seed only
V_REST = 0.0
V_THRESHOLD = 1.0
V_RESET = 0.0
TAU_MEMBRANE = 20.0
TAU_STDP = 20.0
REFRAC_STEPS = 2
W_INIT_SCALE = 0.05


class LIFNet:
    """Recurrent LIF spike substrate (Engine A · Engine G · recurrent pool).

    Faithful promotion of §117 lego_sim.LIFNet. Learning = LOCAL STDP-as-ΔW
    only (pre/post eligibility traces). NO loss gradient, NO autograd.

    Parameters
    ----------
    n_a    : Engine A subpopulation size (excitatory readout side)
    n_g    : Engine G subpopulation size (inhibitory readout side)
    n_rec  : recurrent pool size
    seed   : RNG seed (g_clm_from_scratch — RANDOM init only)
    """

    def __init__(self, n_a: int = 96, n_g: int = 96, n_rec: int = 64,
                 seed: int = SEED):
        self.n_a = n_a
        self.n_g = n_g
        self.n_rec = n_rec
        self.N = n_a + n_g + n_rec
        self.rng = np.random.default_rng(seed)

        # NEURO.tape mech_action_potential (Hodgkin–Huxley → LIF reduction):
        # membrane potential, leak toward v_rest, threshold-and-reset.
        self.v = self.rng.normal(0.0, 0.1, size=self.N).astype(np.float32)
        self.refr = np.zeros(self.N, dtype=np.int32)
        self.v_rest = V_REST
        self.v_th = V_THRESHOLD
        self.v_reset = V_RESET
        self.tau_m = TAU_MEMBRANE
        self.refrac = REFRAC_STEPS

        # NEURO.tape mech_plasticity (cortical co-adaptation = LOCAL STDP):
        # eligibility traces for pre and post spikes only.
        self.tau_stdp = TAU_STDP
        self.trace_pre = np.zeros(self.N, dtype=np.float32)
        self.trace_post = np.zeros(self.N, dtype=np.float32)
        self.a_plus = 0.01     # LTP gain
        self.a_minus = 0.012   # LTD gain (slightly stronger for stability)
        self.w_max = 1.0
        self.w_min = -1.0

        # Recurrent weight matrix (engine-A / engine-G / recurrent connections).
        self.W = (self.rng.normal(0.0, W_INIT_SCALE,
                                    size=(self.N, self.N)).astype(np.float32))
        np.fill_diagonal(self.W, 0.0)  # no self-connections

    def step(self, ext: np.ndarray) -> np.ndarray:
        """One LIF integrate-and-fire step.

        Parameters
        ----------
        ext  : (N,) array — external + recurrent input current for this step.

        Returns
        -------
        spike  : (N,) boolean array — neurons that fired this step.

        Learning channel: LOCAL pair-based STDP only (NO autograd, NO loss).
        Pre-spike trace ↑ on spike, exponentially decays. Post-spike trace
        likewise. Δw_{ij} ∝ +trace_pre[i]·spike[j] (LTP) − a_minus·trace_post[j]·spike[i] (LTD).
        Weights clipped to [w_min, w_max].
        """
        active = (self.refr <= 0)
        # Leak toward v_rest
        self.v[active] += (self.v_rest - self.v[active]) / self.tau_m
        # Inject input
        self.v[active] += ext[active]

        # Threshold-and-reset
        spike = (self.v >= self.v_th) & active
        self.v[spike] = self.v_reset
        self.refr[spike] = self.refrac
        self.refr[~spike] -= 1

        # STDP traces (pre/post eligibility) — exponential decay + spike kick
        self.trace_pre *= np.exp(-1.0 / self.tau_stdp)
        self.trace_post *= np.exp(-1.0 / self.tau_stdp)
        spike_f = spike.astype(np.float32)
        self.trace_pre += spike_f
        self.trace_post += spike_f

        # LOCAL STDP-as-ΔW (NO loss gradient anywhere)
        # LTP: post-spike[j] pairs with pre-trace[i] → strengthen W[j,i]
        # LTD: pre-spike[i] pairs with post-trace[j] → weaken W[j,i]
        ltp = self.a_plus * np.outer(spike_f, self.trace_pre)
        ltd = self.a_minus * np.outer(self.trace_post, spike_f)
        self.W += ltp - ltd
        np.fill_diagonal(self.W, 0.0)
        np.clip(self.W, self.w_min, self.w_max, out=self.W)

        return spike


def spike_rate_vec(raster: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """NEURO.tape mech_neural_coding rate-code: window-averaged spikes/unit.

    Parameters
    ----------
    raster  : (window_steps, N_total) boolean array — spike history over window.
    idx     : (k,) integer array — indices of the subpopulation to average.

    Returns
    -------
    (k,) float array — mean spike rate per indexed unit over the window.
    """
    return raster[:, idx].mean(axis=0)


def psi_c1(r_a: np.ndarray, r_g: np.ndarray) -> tuple[float, float]:
    """Ψ-C1 carrier = §112 META_FP(Π_½) instance, carrier = spike-correlation.

        c_spk = cos(r_a, r_g) ∈ [−1, 1]   (Cauchy–Schwarz, inner-product space)
        Ψ-C1  = ψ(c_spk) = (1 + c_spk) / 2  (cos=0 ⇒ ½ fixed point)

    Byte-equal in *form* to conscious_decoder.py:740 `(1.0 + cos_sim) / 2.0`,
    with carrier substituted from byte-vocab → spike-correlation. The form is
    invariant (§112); only the carrier relocates.

    Returns
    -------
    (psi, c)  : tuple of (Ψ-C1 value, raw cos similarity)
    """
    na, ng = np.linalg.norm(r_a), np.linalg.norm(r_g)
    if na < 1e-12 or ng < 1e-12:
        c = 0.0  # degenerate-silence → c=0 ⇒ Ψ=½ exactly
    else:
        c = float(np.dot(r_a, r_g) / (na * ng))
    c = max(-1.0, min(1.0, c))  # enforce Cauchy–Schwarz bound
    return (1.0 + c) / 2.0, c


def make_stimuli(d: int, n_stim: int, seed: int) -> list[np.ndarray]:
    """Deterministic binary-pattern stimulus set (half-active).

    Promoted from §125/§126/§127 probe code (identical across probes).
    Each pattern has exactly d//2 indices set to 1.0 in a length-d vector.
    """
    rng = np.random.default_rng(seed)
    pats = []
    for _ in range(n_stim):
        v = np.zeros(d, dtype=np.float32)
        idx = rng.choice(d, d // 2, replace=False)
        v[idx] = 1.0
        pats.append(v)
    return pats


def variance_decomposition(values: np.ndarray) -> dict:
    """ANOVA decomposition for layer-2 stimulus-driven liveness measurement.

    Parameters
    ----------
    values  : (n_stim, n_samples_per_stim) float array — pooled Ψ-C1 samples.

    Returns
    -------
    dict with η² (correlation ratio), Gaussian MI (bits), SS_between/within/total.

    Identity (B-S125-3 / B-S126-3 / B-S127-2):  SS_total = SS_between + SS_within
    Bound (B-S125-1 / B-S126-1):  η² ∈ [0, 1]  (sum-of-squares)
    Gaussian MI:  I = -½ log(1 - η²)  ≥ 0  (sympy strict monotone on (0,1))
    """
    import math
    n_stim, n_samples = values.shape
    grand_mean = values.mean()
    stim_means = values.mean(axis=1)
    ss_between = n_samples * float(((stim_means - grand_mean) ** 2).sum())
    ss_within = float(((values - stim_means[:, None]) ** 2).sum())
    ss_total = ss_between + ss_within
    eta_sq = ss_between / ss_total if ss_total > 0 else 0.0
    mi_nats = -0.5 * math.log(max(1.0 - eta_sq, 1e-12))
    mi_bits = mi_nats / math.log(2.0)
    return {
        "n_stim": int(n_stim),
        "n_samples_per_stim": int(n_samples),
        "grand_mean": float(grand_mean),
        "ss_between": float(ss_between),
        "ss_within": float(ss_within),
        "ss_total": float(ss_total),
        "eta_squared": float(eta_sq),
        "gaussian_mi_nats": float(mi_nats),
        "gaussian_mi_bits": float(mi_bits),
    }


__all__ = [
    "SEED", "BASE_CKPT", "LIFNet",
    "spike_rate_vec", "psi_c1",
    "make_stimuli", "variance_decomposition",
]
