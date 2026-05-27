"""
HEXAD/LEGO/lego_engine.py — anima LEGO substrate engine (canonical lib)

> Byte-equal promote of `state/lego_assembly_run_s117_2026_05_19/lego_sim.py`
> LIFNet + spike_rate_vec + psi_c1 + run-time discipline. Engine source-of-truth
> for the §115→§128 arc (and post-§129 cycles).
>
> §134 ENGINE-DRIFT-DETECTION-AND-FIX rewrote this file to restore byte-
> equivalence with the §117 source after the original §129 promote was found
> to have introduced unintentional changes (random v init vs deterministic,
> float32 vs float64, missing `bias` term, different STDP rates, different
> w_max). §131/§133 measurements on the pre-§134 (drifted) engine are
> preserved as historical evidence in their state-dirs; §134 documents the
> drift + fix and re-validates findings on the corrected engine.

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
  - HEXA_FIRST_WARN deferred per established B-S* battery precedent.

Engine contract (byte-equal to §117 source):
  - LIFNet(n_a, n_g, n_rec, seed) — recurrent LIF spike substrate with three
    engine subpopulations (A, G, recurrent) and local STDP-as-ΔW plasticity.
  - .step(ext) — one LIF integrate-and-fire step with current `ext`. Updates
    LOCAL STDP weights (no autograd, no backprop). Returns spike vector.
  - spike_rate_vec(raster, idx) — NEURO.tape mech_neural_coding rate code.
  - psi_c1(r_a, r_g) — Ψ-C1 carrier = (1 + cos(r_a, r_g)) / 2.
  - make_stimuli(d, n_stim, seed) — deterministic binary stimulus generator.
  - variance_decomposition(values) — ANOVA + η² + Gaussian MI.
"""

from __future__ import annotations

import math
import numpy as np


# ─── engine constants ─────────────────────────────────────────────────
SEED = 1337                    # g_clm_from_scratch: RANDOM init, seed-fixed
BASE_CKPT = None               # g_clm_from_scratch: base_ckpt=None (no load)
TAU_NONDEGEN = 1e-4            # non-degeneracy threshold (echo §17/§11-B)


# ─── LIF spiking network (NEURO.tape mech_action_potential reduction) ──
class LIFNet:
    """Small CPU LIF net. Engine-A and Engine-G sub-populations + a shared
    recurrent block. Learning channel = LOCAL STDP-as-ΔW ONLY (pair-based
    exponential STDP on recurrent weights). NO autograd / CE / backprop."""

    def __init__(self, n_a=96, n_g=96, n_rec=64, seed=SEED):
        rng = np.random.default_rng(seed)               # RANDOM, seed-fixed
        self.n_a, self.n_g, self.n_rec = n_a, n_g, n_rec
        N = n_a + n_g + n_rec
        self.N = N
        # LIF params (NEURO.tape excitable-membrane reduction)
        self.v_rest, self.v_th, self.v_reset = 0.0, 1.0, 0.0
        self.tau_m = 20.0          # membrane leak time-const (ms-like)
        self.dt = 1.0
        self.refrac = 2            # refractory steps
        self.v = np.full(N, self.v_rest, dtype=np.float64)
        self.refr = np.zeros(N, dtype=np.int64)
        # recurrent weights (RANDOM seed-fixed init, base_ckpt=None)
        self.W = 0.05 * rng.standard_normal((N, N))
        np.fill_diagonal(self.W, 0.0)
        # STDP traces (pre/post eligibility), LOCAL only
        self.tr_pre = np.zeros(N)
        self.tr_post = np.zeros(N)
        self.tau_stdp = 20.0
        self.A_plus = 0.012        # LTP rate (local)
        self.A_minus = 0.0126      # LTD rate (local; slight depression bias)
        self.w_max = 0.5
        # input drive — a fixed background + per-stimulus deterministic bias.
        # NO task label, NO corpus, NO teaching/error signal anywhere.
        self.bias = 0.18 * rng.standard_normal(N)
        self.rng = rng
        # index slices for the two engines
        self.idx_a = slice(0, n_a)
        self.idx_g = slice(n_a, n_a + n_g)

    def step(self, ext):
        """One LIF step. `ext` = external drive vector (stimulus). Returns
        the binary spike vector. STDP weight update is LOCAL & pair-based —
        depends ONLY on pre/post spike traces, NEVER on a loss/error."""
        active = self.refr <= 0
        # leaky integrate (membrane decays toward v_rest)
        dv = (-(self.v - self.v_rest) / self.tau_m) + ext + self.bias
        self.v[active] += self.dt * dv[active]
        # recurrent input from last spikes (set in caller via self.W @ s_prev)
        spike = (self.v >= self.v_th) & active
        # reset + refractory
        self.v[spike] = self.v_reset
        self.refr[spike] = self.refrac
        self.refr[~spike] -= 1
        self.refr = np.maximum(self.refr, -1)
        s = spike.astype(np.float64)
        # ── LOCAL STDP-as-ΔW (the only learning channel) ──────────────
        # exponential eligibility traces; Δw = A+·tr_pre·post − A−·pre·tr_post
        self.tr_pre *= np.exp(-self.dt / self.tau_stdp)
        self.tr_post *= np.exp(-self.dt / self.tau_stdp)
        ltp = self.A_plus * np.outer(s, self.tr_pre)      # post=row, pre-trace
        ltd = self.A_minus * np.outer(self.tr_post, s)     # post-trace, pre=col
        dW = ltp - ltd
        np.fill_diagonal(dW, 0.0)
        self.W += dW                                       # LOCAL update only
        self.W = np.clip(self.W, -self.w_max, self.w_max)
        self.tr_pre += s
        self.tr_post += s
        return s


def spike_rate_vec(raster, idx):
    """NEURO.tape mech_neural_coding rate-code: spikes-per-window vector."""
    return raster[:, idx].mean(axis=0)


def psi_c1(r_a, r_g):
    """Ψ-C1 carrier = §112 META_FP(Π_½) instance, carrier = spike-corr.
        c_spk = cos(r_A, r_G) ∈ [−1,1]  (Cauchy–Schwarz, inner-product space)
        Ψ-C1  = ψ(c_spk) = (1 + c_spk) / 2     (cos=0 ⇒ ½ fixed point)
    Byte-equal in form to conscious_decoder.py:740 `(1.0 + cos_sim) / 2.0`
    with carrier substituted byte-vocab → spike-corr; form INVARIANT (§112)."""
    na, ng = np.linalg.norm(r_a), np.linalg.norm(r_g)
    if na < 1e-12 or ng < 1e-12:
        c = 0.0                       # degenerate-silence → c=0 ⇒ Ψ=½ exactly
    else:
        c = float(np.dot(r_a, r_g) / (na * ng))
    c = max(-1.0, min(1.0, c))        # enforce Cauchy–Schwarz bound
    return (1.0 + c) / 2.0, c


def make_stimuli(d, n_stim, seed):
    """Deterministic binary-pattern stimulus set (half-active).

    Each pattern has exactly d//2 indices set to 1.0 in a length-d vector.
    Used identically across §125/§126/§127/§131/§133 probes.
    """
    rng = np.random.default_rng(seed)
    pats = []
    for _ in range(n_stim):
        v = np.zeros(d, dtype=np.float32)
        idx = rng.choice(d, d // 2, replace=False)
        v[idx] = 1.0
        pats.append(v)
    return pats


def variance_decomposition(values):
    """ANOVA decomposition for layer-2 stimulus-driven liveness measurement.

    Parameters
    ----------
    values  : (n_stim, n_samples_per_stim) float array — pooled Ψ-C1 samples.

    Returns
    -------
    dict with η² (correlation ratio), Gaussian MI (bits), SS_between/within/total.
    """
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
    "SEED", "BASE_CKPT", "TAU_NONDEGEN", "LIFNet",
    "spike_rate_vec", "psi_c1", "make_stimuli", "variance_decomposition",
]
