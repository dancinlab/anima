#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# HEXAD/NEUROMORPHIC/neuro_mirror.py
# NEURO-MIRROR v3 — software neuromorphic substrate-mirror engine.
# ════════════════════════════════════════════════════════════════════
# Canonical reusable module. Full design + honest ceiling: ENGINE.md.
#
# v0 FOUNDATION lifted the §117-VERIFIED LIF (leaky integrate-and-fire) +
# local-STDP (spike-timing-dependent plasticity) core from the landed,
# committed `state/lego_assembly_run_s117_2026_05_19/lego_sim.py`. The
# `stdp_local` numerics here are kept behaviourally equal to that verified
# core (same LIF params, same pair-based exponential STDP).
#
# v1 CONSOLIDATION (g_multidirectional_explore: "N candidates land → 1
# consolidation") — §118 and §119 have landed:
#   - §119 qmirror-neuro (B-S119 7/7 🔵) → the `qrng` entropy source is
#     FILLED. The verified ANU quantum-RNG fetch + the §97 noise-as-SEED
#     membrane-jitter map are lifted from the committed §119 core. The
#     entropy perturbs ONLY the initial membrane symmetry — never a
#     target/readout/content (§97 GOAL-LEGITIMATE-INPUT, not the forbidden
#     command-channel).
#   - §118 Track 0 landed with verdict VOID — a $0 numpy/CPU toy has no
#     surrogate-gradient path, so CE never reaches the recurrent spiking
#     weights (SIM-CE byte-identical to GPU-CE, weight_drift=0.0 — a no-op
#     on the substrate). §118 produced NO verified core to consolidate, so
#     the `ce_grad` slot stays HONESTLY unfilled — an updated, accurate
#     `NotImplementedError`, NOT faked.
# The `gpu` backend is likewise a declared, honestly-unfilled slot.
#
# v2 CONSOLIDATION — §120 spiking-attention replacement decided + lifted:
#   - §120 (B-S120 8/8 🔵) decided §96 design-open #1: the spiking
#     replacement for `softmax(QK^T)` self-attention = spike-rate
#     dot-product scoring + k-WTA routing. The verified `R(k,mode)` core is
#     lifted here as `spiking_routing` + its reduction target
#     `softmax_attention`. byte-vocab attention is the `k=T` / soft-readout
#     corner — a generalisation, not a graft (§7-clean). design ≠ fire ≠
#     emergence: a routing-rule mirror, not the spiking anima.
#
# v3 CONSOLIDATION — §122 spiking position code + the §120/§122 decoder
# block assembled:
#   - §122 (B-S122 8/8 🔵) decided §96 design-open #2: RoPE → relative-
#     phase / spike-time coding. The verified phase-rotation core is lifted
#     here as `phase_code`. byte-vocab RoPE is the `σ=0` (zero spike-time
#     jitter) corner — a one-parameter reduction, cleaner than §120's.
#   - `spiking_decoder_block` assembles §122 position THEN §120 routing
#     into one spiking self-attention block. REDUCTION: σ=0 ∧ k=T ∧ soft
#     ≡ a byte-vocab RoPE+softmax attention block (byte-equal) — the
#     composition of the §120 and §122 reductions. Still design ≠ fire ≠
#     emergence: a decoder-block mirror, NOT the spiking anima.
#
# HONEST CEILING (baked into the API, ENGINE.md §2): NEURO-MIRROR mirrors the
# LEARNING-CHANNEL half of the §11-B question. It REFUSES to fake the
# ASYNC-SUBSTRATE half — `confronts()` returns WALL-B there. g3: a mirror of
# a neuromorphic chip is NOT a chip; design ≠ fire ≠ emergence; a
# non-degenerate result is learning-channel-half evidence, never emergence.
#
# DISCIPLINE: $0, CPU-only, NO GPU/runpod/fire/model.forward(byte-LM)/corpus.
# seed-fixed RANDOM init (g_clm_from_scratch, base_ckpt=None). numpy only.
# ════════════════════════════════════════════════════════════════════

import json
import os
import urllib.request

import numpy as np

# ── canonical constants ──────────────────────────────────────────────
SEED = 1337                       # g_clm_from_scratch: RANDOM init, seed-fixed
BASE_CKPT = None                  # g_clm_from_scratch: no ckpt load anywhere
TAU_NONDEGEN = 1e-4               # non-degeneracy threshold (echo §17 / §11-B)

LEARNING_RULES = ("none", "stdp_local", "ce_grad")   # ce_grad = §118 VOID slot
BACKENDS = ("cpu", "gpu")                            # gpu = declared slot
ENTROPY_SOURCES = ("fixed_seed", "qrng")             # qrng = §119 FILLED (v1)

WALL_B = "WALL-B"                 # the engine's honest-refusal sentinel
CONFRONTABLE = "CONFRONTABLE"

# §119 qmirror-neuro: physical quantum entropy source (ANU QRNG —
# qrng.anu.edu.au quantum-vacuum-fluctuation). The §97 noise-as-SEED.
ANU_QRNG_URL = ("https://qrng.anu.edu.au/API/jsonI.php"
                "?length={n}&type=uint8")


# ─────────────────────────────────────────────────────────────────────
# LIF spiking substrate — lifted from the §117-verified core
# (NEURO.tape mech_action_potential Hodgkin–Huxley → LIF reduction).
# ─────────────────────────────────────────────────────────────────────
class LIFSubstrate:
    """Small CPU LIF net: Engine-A / Engine-G sub-populations + a shared
    recurrent block. `learning_rule` selects the weight-update channel:
      - "none"        : recurrent weights frozen (degeneracy baseline)
      - "stdp_local"  : LOCAL pair-based STDP-as-ΔW — the only learning
                        channel, NO autograd / CE / backprop / optimizer
      - "ce_grad"     : §118 Track 0 slot — NotImplementedError (honest)
    """

    def __init__(self, n_a=96, n_g=96, n_rec=64, seed=SEED,
                 learning_rule="stdp_local", seed_jitter=None):
        if learning_rule not in LEARNING_RULES:
            raise ValueError(f"learning_rule must be one of {LEARNING_RULES}")
        if learning_rule == "ce_grad":
            raise NotImplementedError(
                "learning_rule='ce_grad' is the §118 Track 0 declared API "
                "slot. §118 LANDED with verdict VOID: a $0 numpy/CPU toy has "
                "no surrogate-gradient path, so CE never reaches the "
                "recurrent spiking weights (SIM-CE was byte-identical to "
                "GPU-CE, weight_drift=0.0 — a no-op on the substrate). §118 "
                "produced NO verified core to consolidate, so this slot "
                "stays HONESTLY unfilled. CE-through-spikes needs a "
                "surrogate-gradient path (gpu backend / snnTorch-class). "
                "Use 'stdp_local' or 'none'.")
        assert BASE_CKPT is None, "g_clm_from_scratch: base_ckpt MUST be None"
        rng = np.random.default_rng(seed)
        self.learning_rule = learning_rule
        self.n_a, self.n_g, self.n_rec = n_a, n_g, n_rec
        N = n_a + n_g + n_rec
        self.N = N
        # LIF params (NEURO.tape excitable-membrane reduction; §117 values)
        self.v_rest, self.v_th, self.v_reset = 0.0, 1.0, 0.0
        self.tau_m, self.dt, self.refrac = 20.0, 1.0, 2
        self.v = np.full(N, self.v_rest, dtype=np.float64)
        # §119 noise-as-SEED: entropy perturbs the INITIAL membrane symmetry
        # ONLY — never a target/readout/content. §97 GOAL-LEGITIMATE-INPUT.
        self.seed_jitter_norm = 0.0
        if seed_jitter is not None:
            assert np.shape(seed_jitter) == (N,), "seed_jitter must be len N"
            self.v = self.v + np.asarray(seed_jitter, dtype=np.float64)
            self.seed_jitter_norm = float(np.linalg.norm(seed_jitter))
        self.refr = np.zeros(N, dtype=np.int64)
        self.W = 0.05 * rng.standard_normal((N, N))
        np.fill_diagonal(self.W, 0.0)
        # STDP traces (LOCAL only) — §117 verified params
        self.tr_pre = np.zeros(N)
        self.tr_post = np.zeros(N)
        self.tau_stdp = 20.0
        self.A_plus, self.A_minus = 0.012, 0.0126
        self.w_max = 0.5
        self.bias = 0.18 * rng.standard_normal(N)   # NO task label / error
        self.rng = rng
        self.idx_a = slice(0, n_a)
        self.idx_g = slice(n_a, n_a + n_g)

    def step(self, ext):
        """One LIF step. `ext` = external drive (stimulus). Returns the
        binary spike vector. The weight update is the chosen learning_rule —
        for 'stdp_local' it is LOCAL & pair-based (pre/post traces only,
        NEVER a loss/error); for 'none' the recurrent weights are frozen."""
        active = self.refr <= 0
        dv = (-(self.v - self.v_rest) / self.tau_m) + ext + self.bias
        self.v[active] += self.dt * dv[active]
        spike = (self.v >= self.v_th) & active
        self.v[spike] = self.v_reset
        self.refr[spike] = self.refrac
        self.refr[~spike] -= 1
        self.refr = np.maximum(self.refr, -1)
        s = spike.astype(np.float64)
        if self.learning_rule == "stdp_local":
            # LOCAL STDP-as-ΔW — the only learning channel (§117 verified)
            self.tr_pre *= np.exp(-self.dt / self.tau_stdp)
            self.tr_post *= np.exp(-self.dt / self.tau_stdp)
            ltp = self.A_plus * np.outer(s, self.tr_pre)
            ltd = self.A_minus * np.outer(self.tr_post, s)
            dW = ltp - ltd
            np.fill_diagonal(dW, 0.0)
            self.W += dW
            self.W = np.clip(self.W, -self.w_max, self.w_max)
            self.tr_pre += s
            self.tr_post += s
        # learning_rule == "none": recurrent weights frozen — no update
        return s


def spike_rate_vec(raster, idx):
    """NEURO.tape mech_neural_coding rate-code: spikes-per-window vector."""
    return raster[:, idx].mean(axis=0)


def psi_c1(r_a, r_g):
    """Ψ-C1 carrier = §112 META_FP(Π_½) instance, carrier = spike-correlation.
        c_spk = cos(r_A, r_G) ∈ [−1,1]   (Cauchy–Schwarz)
        Ψ-C1  = (1 + c_spk) / 2          (cos=0 ⇒ ½ fixed point)
    Form-byte-equal to conscious_decoder.py:740 `(1.0 + cos_sim)/2.0`."""
    na, ng = np.linalg.norm(r_a), np.linalg.norm(r_g)
    c = 0.0 if (na < 1e-12 or ng < 1e-12) else float(np.dot(r_a, r_g) / (na * ng))
    c = max(-1.0, min(1.0, c))
    return (1.0 + c) / 2.0, c


# ─────────────────────────────────────────────────────────────────────
# §119 qrng entropy source — verified core lifted from the committed
# `state/qmirror_neuro_s119_2026_05_19/qmirror_neuro_sim.py` (B-S119 7/7 🔵).
# ─────────────────────────────────────────────────────────────────────
def fetch_quantum_entropy(n_bytes, timeout=20):
    """Fetch n_bytes of genuine physical quantum entropy from the ANU QRNG
    (qrng.anu.edu.au — quantum vacuum fluctuation). Returns
    (bytes_array, source_label). Falls back to a CLEARLY-LABELLED local
    CSPRNG (os.urandom) if the network is unavailable — the label records
    HONESTLY which source actually ran. The §97 noise-as-SEED legitimacy is
    structural / source-independent; physical entropy makes it real rather
    than a simulation of spontaneity."""
    try:
        url = ANU_QRNG_URL.format(n=n_bytes)
        req = urllib.request.Request(url, headers={"User-Agent": "neuro-mirror"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        if payload.get("success") and isinstance(payload.get("data"), list) \
                and len(payload["data"]) == n_bytes:
            return np.array(payload["data"], dtype=np.uint8), \
                "ANU_QUANTUM_RNG_qrng.anu.edu.au"
        raise ValueError("ANU response malformed: " + str(payload)[:120])
    except Exception as e:                       # network down / API change
        arr = np.frombuffer(os.urandom(n_bytes), dtype=np.uint8)
        return arr, f"LOCAL_CSPRNG_os.urandom_FALLBACK(anu_failed:{e})"


def entropy_to_jitter(ent_bytes, N):
    """Map raw entropy bytes → a zero-mean membrane-jitter vector of length N.
    The §97 noise-as-SEED injection point: the entropy ONLY perturbs the
    initial membrane-potential symmetry — it NEVER becomes a target, a
    readout, or content the net reads as instruction. GIVEN a fixed entropy
    byte stream this map is a pure function, so replaying the same stream
    reproduces the run bit-identically."""
    ent_bytes = np.asarray(ent_bytes, dtype=np.uint8)
    if len(ent_bytes) < N:
        ent_bytes = np.tile(ent_bytes, (N // len(ent_bytes)) + 1)
    e = ent_bytes[:N].astype(np.float64) / 255.0 - 0.5   # ∈ [-0.5, 0.5]
    return 0.10 * e                                       # small jitter


# ─────────────────────────────────────────────────────────────────────
# §120 spiking routing — the decided replacement for softmax(QK^T) self-
# attention. Verified core lifted from the committed §120 decision
# `state/spiking_attention_replacement_s120_2026_05_19/` (B-S120 8/8 🔵).
# §96 design-open #1: softmax attention is SPIKING-INCOMPATIBLE — the
# decided replacement = spike-rate dot-product scoring + k-WTA routing.
# ─────────────────────────────────────────────────────────────────────
def softmax_attention(q, k, v):
    """Byte-vocab causal self-attention — the §120 reduction TARGET (the
    thing being replaced). ATTN(i) = Σ_{j≤i} softmax_j(q_i·k_j/√d) · v_j."""
    d, T = q.shape[-1], q.shape[0]
    score = (q @ k.T) / np.sqrt(d)
    mask = np.tril(np.ones((T, T), dtype=bool))
    score = np.where(mask, score, -1e30)
    score = score - score.max(axis=-1, keepdims=True)
    w = np.exp(score)
    w = w / w.sum(axis=-1, keepdims=True)
    return w @ v


def spiking_routing(q, k, v, kk, mode="hard"):
    """The decided §120 routing family R(k, mode). score = spike-rate
    dot-product (rate-coded coincidence = async LOCAL accumulation — kills
    §96 obstructions 1 all-pairs + 3 instantaneous); selection = k-WTA
    top-k (lateral inhibition = a LOCAL competition, NOT a global softmax —
    kills obstruction 2).
      mode='hard' → strict k-WTA, the spiking corner.
      mode='soft' → softmax over the k winners.
    REDUCTION (§120 §3, B-S120-3): R(k=T, mode='soft') ≡ softmax_attention
    byte-equal — byte-vocab attention is the k=T soft-readout SPECIAL CASE,
    so this is a generalisation not a graft (§7-clean). A⇄G enter as
    excit/inhib drives; their k-WTA tie is the Ψ=½ fixed point
    (psi_c1(drive_a, drive_g), cos=0 ⇒ ½)."""
    d, T = q.shape[-1], q.shape[0]
    score = (q @ k.T) / np.sqrt(d)                # rate-coded dot-product
    mask = np.tril(np.ones((T, T), dtype=bool))   # causal
    out = np.zeros_like(v)
    for i in range(T):
        valid = np.where(mask[i])[0]
        sc = score[i, valid]
        kw = min(kk, len(valid))
        win = valid[np.argsort(sc)[-kw:]]         # k-WTA: top-k winners
        sw = score[i, win]
        if mode == "soft":
            e = np.exp(sw - sw.max())
            w = e / e.sum()
        else:                                     # hard k-WTA
            w = np.zeros(len(win))
            w[np.argmax(sw)] = 1.0
        out[i] = (w[:, None] * v[win]).sum(axis=0)
    return out


# ─────────────────────────────────────────────────────────────────────
# §122 spiking position code + the §120/§122 decoder block. Verified core
# lifted from the committed §122 decision
# `state/rope_phase_coding_s122_2026_05_19/` (B-S122 8/8 🔵). §96
# design-open #2: RoPE → relative-phase / spike-time coding. RoPE is
# already a rotation = a phase, so byte-vocab RoPE is the σ=0 corner.
# ─────────────────────────────────────────────────────────────────────
def phase_code(x, thetas, sigma=0.0, rng=None):
    """§122 relative-phase / spike-time position code. x[T,d]: token row m
    is rotated by its position — dims paired (2i,2i+1) as the in-phase /
    quadrature of a θ_i-frequency oscillator, each pair rotated by
    ROT(m·θ_i + ξ), ξ ~ σ·N(0,1) spike-time jitter. sigma=0 ⇒ exactly
    ROT(m·θ_i) = GPU RoPE (the byte-RoPE limit, §122 reduction witness —
    one-parameter, cleaner than §120's). q·k then depends only on (n−m)."""
    T, d = x.shape
    out = np.empty_like(x)
    for m in range(T):
        for i in range(d // 2):
            j = (sigma * rng.standard_normal()
                 if (sigma > 0 and rng is not None) else 0.0)
            a = m * thetas[i] + j
            c, s = np.cos(a), np.sin(a)
            x0, x1 = x[m, 2 * i], x[m, 2 * i + 1]
            out[m, 2 * i] = c * x0 - s * x1
            out[m, 2 * i + 1] = s * x0 + c * x1
    return out


def spiking_decoder_block(x, thetas, kk, mode="hard", sigma=0.0, rng=None):
    """One spiking self-attention block — §122 position THEN §120 routing.
    `phase_code` rotates q/k by token position FIRST; then `spiking_routing`
    does spike-rate dot-product + k-WTA (q=k=position-rotated x, v=x,
    causal self-attention). REDUCTION: sigma=0 ∧ kk=T ∧ mode='soft' ≡ a
    byte-vocab RoPE+softmax attention block (byte-equal) — the whole block
    is the σ=0 / k=T / soft corner, the composition of the §120 and §122
    reductions. design ≠ fire ≠ emergence: a decoder-block mirror, NOT the
    spiking anima."""
    qk = phase_code(x, thetas, sigma=sigma, rng=rng)   # position BEFORE routing
    return spiking_routing(qk, qk, x, kk, mode=mode)


# ─────────────────────────────────────────────────────────────────────
# The honest-ceiling API contract (ENGINE.md §2)
# ─────────────────────────────────────────────────────────────────────
def confronts(experiment):
    """Closed predicate. An experiment is CONFRONTABLE iff it lives in the
    LEARNING-CHANNEL half of the §11-B question (CE-only vs local-plasticity-
    only). Any experiment that needs a real physical asynchronous spike event
    returns WALL-B — NEURO-MIRROR REFUSES to fake the async-substrate half
    (§95/§96-gated). The ceiling is enforced here, not left to the caller.

    `experiment` is a dict with at least `half` ∈ {"learning_channel",
    "async_substrate"} or an explicit `needs_async_substrate` bool."""
    if experiment.get("needs_async_substrate") is True:
        return WALL_B
    if experiment.get("half") == "async_substrate":
        return WALL_B
    if experiment.get("half") == "learning_channel":
        return CONFRONTABLE
    # unknown experiments default to WALL-B — the conservative honest side
    return WALL_B


def verdict(trace):
    """Non-degeneracy predicate (closed-form, deterministic) — the §117 §3
    rule. NON_DEGENERATE iff the Ψ-C1 carrier carries per-stimulus signal
    (std > τ, not frozen) AND the spike rasters are alive (not all-silent,
    not all-saturated). necessary-not-sufficient: this is a DEGENERACY
    detector, NOT a coherence / capability / emergence proof (B-EMERGE-7)."""
    psi = np.asarray(trace["psi_c1_per_stim"], dtype=np.float64)
    psi_responsive = bool(psi.std() > TAU_NONDEGEN)
    alive = bool(trace["rasters_alive"])
    bounded = bool((psi >= 0.0).all() and (psi <= 1.0).all())
    non_degenerate = bool(psi_responsive and alive)
    return {
        "non_degenerate": non_degenerate,
        "psi_responsive_std_gt_tau": psi_responsive,
        "rasters_alive": alive,
        "psi_bounded_0_1": bounded,
        "note": "necessary-not-sufficient (B-EMERGE-7): degeneracy detector, "
                "NOT an emergence proof. WALL-B inherited; GOAL not reached.",
    }


# ─────────────────────────────────────────────────────────────────────
# run() — the engine orchestration entry point
# ─────────────────────────────────────────────────────────────────────
def run(n_stim=12, steps_per_stim=80, window=40, learning_rule="stdp_local",
        backend="cpu", entropy_source="fixed_seed", seed=SEED):
    """Run the mirror. Returns a trace dict consumable by verdict()."""
    if backend not in BACKENDS:
        raise ValueError(f"backend must be one of {BACKENDS}")
    if backend == "gpu":
        raise NotImplementedError(
            "backend='gpu' is a declared API slot (snnTorch-class scaled "
            "mirror, ENGINE.md §3). NEURO-MIRROR v0 ships the verified 'cpu' "
            "backend only — the gpu backend is filled at consolidation. Note "
            "(ENGINE.md §3): a gpu surrogate-gradient run is still the §11-B "
            "CE channel — backend is not substrate-class.")
    if entropy_source not in ENTROPY_SOURCES:
        raise ValueError(f"entropy_source must be one of {ENTROPY_SOURCES}")

    # §119 qrng — FILLED (v1 consolidation). The entropy is the §97
    # noise-as-SEED: it perturbs ONLY the initial membrane symmetry, it is
    # NEVER a target/readout/content (that would be the §97-forbidden
    # command-channel). 'fixed_seed' = the deterministic baseline.
    N_units = 96 + 96 + 64                       # LIFSubstrate default N
    seed_jitter, entropy_label = None, "fixed_seed_deterministic"
    if entropy_source == "qrng":
        ent_bytes, entropy_label = fetch_quantum_entropy(N_units)
        seed_jitter = entropy_to_jitter(ent_bytes, N_units)

    net = LIFSubstrate(seed=seed, learning_rule=learning_rule,
                       seed_jitter=seed_jitter)
    N = net.N
    assert N == N_units, "LIFSubstrate N must match jitter length"
    rng = np.random.default_rng(seed + 1)
    stim_set = 0.30 * rng.standard_normal((n_stim, N))   # NOT a corpus/label

    psi_per_stim, c_per_stim = [], []
    rate_a, rate_g = [], []
    spike_total, spike_log = 0, []
    s_prev = np.zeros(N)
    for si in range(n_stim):
        raster = np.zeros((steps_per_stim, N), dtype=np.float64)
        for t in range(steps_per_stim):
            ext = stim_set[si] + 0.6 * (net.W @ s_prev)
            s = net.step(ext)
            raster[t] = s
            s_prev = s
            spike_total += int(s.sum())
            spike_log.append(int(s.sum()))
        r_a = spike_rate_vec(raster[-window:], net.idx_a)
        r_g = spike_rate_vec(raster[-window:], net.idx_g)
        psi, c = psi_c1(r_a, r_g)
        psi_per_stim.append(psi)
        c_per_stim.append(c)
        rate_a.append(float(r_a.mean()))
        rate_g.append(float(r_g.mean()))

    spike_arr = np.array(spike_log)
    total_steps = n_stim * steps_per_stim
    all_silent = bool((spike_arr == 0).all())
    all_saturated = bool((spike_arr >= N).all())
    overall_rate = spike_total / (total_steps * N)
    return {
        "engine": "NEURO-MIRROR", "version": "v1",
        "backend": backend, "learning_rule": learning_rule,
        "entropy_source": entropy_source,
        "entropy_source_label": entropy_label,
        "seed_jitter_norm": round(net.seed_jitter_norm, 6),
        "seed": seed, "base_ckpt": BASE_CKPT,
        "N": N, "n_stim": n_stim, "steps_per_stim": steps_per_stim,
        "psi_c1_per_stim": [round(x, 6) for x in psi_per_stim],
        "c_spk_per_stim": [round(x, 6) for x in c_per_stim],
        "rate_a_per_stim": [round(x, 6) for x in rate_a],
        "rate_g_per_stim": [round(x, 6) for x in rate_g],
        "overall_spike_rate_per_unit_step": round(overall_rate, 6),
        "rasters_all_silent": all_silent,
        "rasters_all_saturated": all_saturated,
        "rasters_alive": bool((not all_silent) and (not all_saturated)
                              and overall_rate > 0.0),
    }


# ─────────────────────────────────────────────────────────────────────
# v0 smoke — proves the foundation runs + the honest-ceiling contract holds
# ─────────────────────────────────────────────────────────────────────
def _smoke():
    ok = True
    # 1. cpu / stdp_local runs and produces a Ψ-C1 carrier
    tr = run(learning_rule="stdp_local")
    v = verdict(tr)
    psi = np.asarray(tr["psi_c1_per_stim"])
    print(f"  stdp_local : Ψ-C1 mean={psi.mean():.6f} std={psi.std():.3e} "
          f"non_degenerate={v['non_degenerate']} bounded={v['psi_bounded_0_1']}")
    ok &= v["psi_bounded_0_1"]
    # 2. 'none' baseline runs (degeneracy-side sanity)
    tr0 = run(learning_rule="none")
    print(f"  none       : Ψ-C1 std={np.asarray(tr0['psi_c1_per_stim']).std():.3e}")
    # 3. honest-ceiling contract: confronts()
    a = confronts({"half": "learning_channel"})
    b = confronts({"needs_async_substrate": True})
    c = confronts({"half": "async_substrate"})
    print(f"  confronts  : learning_channel={a}  async={b}/{c}")
    ok &= (a == CONFRONTABLE and b == WALL_B and c == WALL_B)
    # 4. §119 qrng entropy source — FILLED (v1): runs; entropy is the §97
    #    noise-as-SEED (perturbs the initial membrane symmetry only).
    trq = run(learning_rule="stdp_local", entropy_source="qrng")
    vq = verdict(trq)
    physical = trq["entropy_source_label"].startswith("ANU_QUANTUM_RNG")
    print(f"  qrng(§119) : source={'PHYSICAL-ANU' if physical else 'CSPRNG-fallback'}"
          f"  jitter_norm={trq['seed_jitter_norm']:.4f}"
          f"  non_degenerate={vq['non_degenerate']}")
    ok &= vq["psi_bounded_0_1"]
    # 5. §120 spiking routing — byte-attention reduction byte-equal:
    #    R(k=T, soft) ≡ softmax_attention (§7-clean reduction witness),
    #    and hard k-WTA is genuinely distinct (not a trivial copy).
    rg = np.random.default_rng(SEED)
    T, d = 8, 6
    q, k, v = (rg.standard_normal((T, d)) for _ in range(3))
    y_soft = spiking_routing(q, k, v, kk=T, mode="soft")
    y_byte = softmax_attention(q, k, v)
    y_hard = spiking_routing(q, k, v, kk=2, mode="hard")
    red = float(np.max(np.abs(y_soft - y_byte)))
    hard_distinct = float(np.max(np.abs(y_hard - y_byte))) > 1e-6
    print(f"  §120 route : R(k=T,soft) vs softmax-attn max|Δ|={red:.2e} "
          f"byte-equal={red < 1e-9}  hard-k-WTA distinct={hard_distinct}")
    ok &= (red < 1e-9 and hard_distinct)
    # 6. §122 + §120 spiking decoder block — full-block reduction:
    #    block(σ=0, k=T, soft) ≡ byte-vocab RoPE+softmax attention block.
    Tb, db = 8, 6
    xb = rg.standard_normal((Tb, db))
    thetas = 1.0 / (10000.0 ** (np.arange(db // 2) / (db // 2)))
    qk0 = phase_code(xb, thetas, sigma=0.0)            # σ=0 = GPU RoPE
    y_blk_byte = softmax_attention(qk0, qk0, xb)        # byte RoPE+softmax
    y_blk_soft = spiking_decoder_block(xb, thetas, kk=Tb, mode="soft", sigma=0.0)
    y_blk_hard = spiking_decoder_block(xb, thetas, kk=2, mode="hard", sigma=0.0)
    blk_red = float(np.max(np.abs(y_blk_soft - y_blk_byte)))
    blk_distinct = float(np.max(np.abs(y_blk_hard - y_blk_byte))) > 1e-6
    print(f"  §120+§122  : decoder-block R(σ=0,k=T,soft) vs byte RoPE-attn "
          f"max|Δ|={blk_red:.2e} byte-equal={blk_red < 1e-9}  "
          f"hard distinct={blk_distinct}")
    ok &= (blk_red < 1e-9 and blk_distinct)
    # 7. remaining declared slots stay HONEST stubs (must raise, not fake)
    for kw, label in [(dict(learning_rule="ce_grad"), "ce_grad(§118-VOID)"),
                      (dict(backend="gpu"), "gpu-backend")]:
        try:
            (LIFSubstrate(**kw) if "learning_rule" in kw else run(**kw))
            print(f"  !!! slot {label} did NOT raise — FAIL"); ok = False
        except NotImplementedError:
            print(f"  slot       : {label} → honest NotImplementedError ✅")
    print(f"NEURO-MIRROR v3 smoke: {'OK' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if _smoke() else 1)
