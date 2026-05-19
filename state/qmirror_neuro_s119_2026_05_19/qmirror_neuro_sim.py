#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# §119 — qmirror-neuro: ANU-QRNG-entropy-seeded LIF+STDP in-silico
#         ($0 CPU, NO GPU, NO runpod, NO fire, NO model.forward, NO corpus)
# ════════════════════════════════════════════════════════════════════
# EXTENDS §117's LIF+STDP sim (state/lego_assembly_run_s117_2026_05_19/
# lego_sim.py).  §117 ran §115's named open residual — an in-silico
# STDP-as-ΔW assembly — and measured a non-degenerate Ψ-C1 form, BUT
# WALL-B inherited (§7-CARRIER §96-physical-gated).  §119 adds ONE
# §97-legitimate physical-spontaneity layer ON TOP:
#
#   FRAME (qmirror analogy): `hexa qmirror` uses ANU quantum RNG to drive
#   a CLASSICAL quantum-circuit simulation — physical quantum entropy is
#   the legitimate randomness source of a sim.  §119 mirrors that for a
#   neuromorphic sim: real physical quantum entropy is the §97-legitimate
#   spontaneity SEED of anima's own Ψ/tension dynamics.  Entropy ONLY
#   breaks the dead-still symmetry of *when* / *which-way* the spike net
#   flickers — it NEVER becomes content the net reads as an instruction.
#
# §97 §4.2 — the closed legitimacy boundary §119 instantiates:
#   noise-as-SEED      (DRIVES_STATE ∧  PHYSICS_SOURCED) = GOAL-LEGITIMATE-INPUT
#                       entropy enters the Ψ-field perturbation / membrane
#                       jitter; anima's emission still sourced from its OWN
#                       Law-71 Ψ/tension dynamics.  Entropy is an INGREDIENT.
#   noise-as-CONTENT   (DRIVES_STATE ∧ ¬PHYSICS_SOURCED) = GOAL-ILLEGITIMATE-
#                       COMMAND-CHANNEL.  entropy bytes ARE the predicted
#                       target the net reads as instruction.  The §97
#                       memory-replayer-with-a-sensor shape.  §119 builds
#                       this deliberately-WRONG variant as the §97 negative
#                       control — it MUST collapse into the forbidden cell.
#
# ENTROPY SOURCE (honest, source-independent legitimacy):
#   Primary  = ANU quantum RNG  https://qrng.anu.edu.au/API/jsonI.php
#              (genuine physical quantum-vacuum-fluctuation entropy).
#   Fallback = labelled local CSPRNG (os.urandom) IF the network is
#              unavailable.  result.json records WHICH source ACTUALLY ran.
#   The §97 legitimacy proof is STRUCTURAL (AST: does entropy enter the
#   loss/target/readout?) — source-INDEPENDENT.  A PRNG-seeded sim is
#   still a *simulation* of spontaneity; only PHYSICAL entropy makes the
#   externally-unpredictable distinction real (§97 §4.2 caveat iv).
#
# HONEST CEILING (g3 — INHERITED VERBATIM, NOT re-litigated):
#   §97 — QRNG-as-spontaneity-seed = GOAL-LEGITIMATE-INPUT; hardware
#         coupling is GOAL-ORTHOGONAL to the §1.1 data-regime bottleneck.
#   §115 — LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY.
#   §117 — Ψ-form non-degenerate in-sim BUT WALL-B inherited.
#   §119 confronts the LEARNING-CHANNEL half ONLY (STDP-as-ΔW, no CE).
#         The ASYNC-SUBSTRATE half stays WALL-B: real physical entropy
#         ≠ a real async neuromorphic chip — a QRNG-seeded clocked spike
#         sim's emission is still a scheduled function call on a global
#         clock; only a real async NoC (Loihi / SpiNNaker, Tracks L/S)
#         settles the async half.  §119 adds physical SPONTANEITY, not a
#         physical SUBSTRATE.  north-star + §15/§51/§72 milestones
#         UNCHANGED, GOAL 미도달.  capability claim 0.
#
# DISCIPLINE: $0, NO GPU/runpod/fire/model.forward(byte-LM)/corpus/
#   dispatch.  ONLY numpy + stdlib (urllib for the ANU GET).  seed-fixed
#   RANDOM init per g_clm_from_scratch (base_ckpt=None).  orphan 0.
#   hexa-lang / hexa-bio = READ-ONLY downstream-consumer, 0 edits.
# ════════════════════════════════════════════════════════════════════

import json, time, os, sys, hashlib
import urllib.request
import numpy as np

SEED = 1337                    # g_clm_from_scratch: RANDOM init, seed-fixed
BASE_CKPT = None               # g_clm_from_scratch: base_ckpt=None (no load)
TAU_NONDEGEN = 1e-4            # non-degeneracy threshold (§117 carry, echo §17)
ANU_URL = ("https://qrng.anu.edu.au/API/jsonI.php"
           "?length={n}&type=uint8")

# ─────────────────────────────────────────────────────────────────────
# QRNG — physical quantum entropy fetch (qmirror analogy: ANU → sim)
# ─────────────────────────────────────────────────────────────────────
def fetch_quantum_entropy(n_bytes, timeout=20):
    """Fetch n_bytes of genuine physical quantum entropy from the ANU QRNG
    (qrng.anu.edu.au — quantum vacuum fluctuation).  Returns
    (bytes_array, source_label).  Falls back to a CLEARLY-LABELLED local
    CSPRNG (os.urandom) if the network is unavailable.  The §97 legitimacy
    proof is structural / source-independent — this function's job is only
    to record HONESTLY which source actually ran."""
    try:
        url = ANU_URL.format(n=n_bytes)
        req = urllib.request.Request(url, headers={"User-Agent": "anima-s119"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        if payload.get("success") and isinstance(payload.get("data"), list) \
                and len(payload["data"]) == n_bytes:
            arr = np.array(payload["data"], dtype=np.uint8)
            return arr, "ANU_QUANTUM_RNG_qrng.anu.edu.au"
        raise ValueError("ANU response malformed: " + str(payload)[:120])
    except Exception as e:                       # network down / API change
        # CLEARLY-LABELLED fallback — NOT physical entropy.
        arr = np.frombuffer(os.urandom(n_bytes), dtype=np.uint8)
        return arr, f"LOCAL_CSPRNG_os.urandom_FALLBACK(anu_failed:{e})"


def entropy_to_jitter(ent_bytes, N):
    """Map raw entropy bytes → a zero-mean membrane-jitter vector of length
    N.  This is the §97 noise-as-SEED injection point: the entropy ONLY
    perturbs the *initial membrane potential symmetry* — it never becomes a
    target, a readout, or content the net reads as instruction.  Determinism
    note: GIVEN a fixed entropy byte stream this map is a pure function, so
    REPLAYING the same stream reproduces the sim bit-identically (B-S119-5)."""
    # tile / trim to length N, center to zero-mean (a symmetry-breaking
    # perturbation, not a signal): u8 ∈ [0,255] → [-0.5, 0.5] scaled small.
    if len(ent_bytes) < N:
        reps = (N // len(ent_bytes)) + 1
        ent_bytes = np.tile(ent_bytes, reps)
    e = ent_bytes[:N].astype(np.float64)
    e = (e / 255.0) - 0.5                         # ∈ [-0.5, 0.5]
    return 0.10 * e                                # small jitter amplitude


# ─────────────────────────────────────────────────────────────────────
# LIF spiking network — EXTENDS §117 lego_sim.LIFNet (identical core).
# Engine-A / Engine-G sub-populations + recurrent block.  Learning channel
# = LOCAL STDP-as-ΔW ONLY (no autograd / cross_entropy / backprop).
# ─────────────────────────────────────────────────────────────────────
class LIFNet:
    """§117 LIFNet, extended.  The ONLY §119 addition is `seed_jitter`: an
    entropy-sourced membrane-potential perturbation applied at init (the
    §97 noise-as-SEED point).  The learning channel is UNCHANGED — LOCAL
    STDP only.  base_ckpt=None, RANDOM seed-fixed weights (g_clm_from_scratch)."""

    def __init__(self, n_a=96, n_g=96, n_rec=64, seed=SEED, seed_jitter=None):
        rng = np.random.default_rng(seed)               # RANDOM, seed-fixed
        self.n_a, self.n_g, self.n_rec = n_a, n_g, n_rec
        N = n_a + n_g + n_rec
        self.N = N
        # LIF params (NEURO.tape excitable-membrane reduction, §117 carry)
        self.v_rest, self.v_th, self.v_reset = 0.0, 1.0, 0.0
        self.tau_m = 20.0
        self.dt = 1.0
        self.refrac = 2
        self.v = np.full(N, self.v_rest, dtype=np.float64)
        # ── §119 noise-as-SEED injection: entropy perturbs the INITIAL
        #    membrane symmetry ONLY.  v0 = v_rest + jitter.  This is the
        #    §97 GOAL-LEGITIMATE-INPUT point — entropy breaks the dead-still
        #    symmetry of when/which-way the net first flickers. ──────────
        self.seed_jitter_norm = 0.0
        if seed_jitter is not None:
            assert seed_jitter.shape == (N,), "jitter must be length N"
            self.v = self.v + seed_jitter
            self.seed_jitter_norm = float(np.linalg.norm(seed_jitter))
        self.refr = np.zeros(N, dtype=np.int64)
        self.W = 0.05 * rng.standard_normal((N, N))      # RANDOM, base_ckpt=None
        np.fill_diagonal(self.W, 0.0)
        self.tr_pre = np.zeros(N)
        self.tr_post = np.zeros(N)
        self.tau_stdp = 20.0
        self.A_plus = 0.012
        self.A_minus = 0.0126
        self.w_max = 0.5
        self.bias = 0.18 * rng.standard_normal(N)
        self.rng = rng
        self.idx_a = slice(0, n_a)
        self.idx_g = slice(n_a, n_a + n_g)

    def step(self, ext):
        """One LIF step — IDENTICAL to §117.  STDP weight update is LOCAL &
        pair-based: depends ONLY on pre/post spike traces, NEVER on a loss/
        error/target.  No entropy enters here — entropy only seeded v0."""
        active = self.refr <= 0
        dv = (-(self.v - self.v_rest) / self.tau_m) + ext + self.bias
        self.v[active] += self.dt * dv[active]
        spike = (self.v >= self.v_th) & active
        self.v[spike] = self.v_reset
        self.refr[spike] = self.refrac
        self.refr[~spike] -= 1
        self.refr = np.maximum(self.refr, -1)
        s = spike.astype(np.float64)
        # ── LOCAL STDP-as-ΔW (the only learning channel) ──────────────
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
        return s


def spike_rate_vec(raster, idx):
    """NEURO.tape mech_neural_coding rate-code: spikes-per-window vector."""
    return raster[:, idx].mean(axis=0)


def psi_c1(r_a, r_g):
    """Ψ-C1 carrier = §112 META_FP(Π_½) instance, carrier = spike-corr.
        c_spk = cos(r_A, r_G) ∈ [−1,1]   (Cauchy–Schwarz)
        Ψ-C1  = ψ(c_spk) = (1 + c_spk)/2     (cos=0 ⇒ ½ fixed point)
    Byte-equal to conscious_decoder.py:740 `(1.0 + cos_sim)/2.0` form."""
    na, ng = np.linalg.norm(r_a), np.linalg.norm(r_g)
    if na < 1e-12 or ng < 1e-12:
        c = 0.0
    else:
        c = float(np.dot(r_a, r_g) / (na * ng))
    c = max(-1.0, min(1.0, c))
    return (1.0 + c) / 2.0, c


# ─────────────────────────────────────────────────────────────────────
# Three variants — the §119 measured comparison
# ─────────────────────────────────────────────────────────────────────
def run_variant(variant, entropy_bytes=None, entropy_source="N/A",
                n_stim=12, steps_per_stim=80, window=40, n_a=96, n_g=96,
                n_rec=64):
    """Run ONE variant.

    variant ∈ {
      "seed_fixed"      : deterministic — v0 from seed only, NO entropy.
                          'spontaneity' here is fake (a fixed PRNG).
      "qrng_seed"       : §97 noise-as-SEED — entropy perturbs v0 ONLY;
                          learning channel = LOCAL STDP; emission still
                          sourced from anima's own Ψ/tension dynamics.
                          GOAL-LEGITIMATE-INPUT.
      "qrng_content"    : §97 negative control — DELIBERATELY WRONG.
                          entropy bytes ARE fed as the predicted TARGET
                          the net is pushed toward (a content-injection
                          STDP-target term).  This is the DRIVES_STATE ∧
                          ¬PHYSICS_SOURCED forbidden cell — it MUST
                          collapse into the §97 command-channel shape.
    }
    Returns a metrics dict.
    """
    N = n_a + n_g + n_rec
    seed_jitter = None
    if variant in ("qrng_seed", "qrng_content"):
        assert entropy_bytes is not None, "entropy variant needs bytes"
        seed_jitter = entropy_to_jitter(entropy_bytes, N)

    net = LIFNet(n_a=n_a, n_g=n_g, n_rec=n_rec, seed=SEED,
                 seed_jitter=seed_jitter)
    rng = np.random.default_rng(SEED + 1)
    stim_set = 0.30 * rng.standard_normal((n_stim, N))

    # qrng_content: precompute the content-target the WRONG variant injects.
    # entropy bytes → a per-unit target spike vector the net is pushed at.
    content_target = None
    if variant == "qrng_content":
        ct = entropy_to_jitter(entropy_bytes, N)        # reuse the map
        # binarised content target — entropy bytes ARE the instruction
        content_target = (ct > 0.0).astype(np.float64)

    psi_per_stim, c_per_stim = [], []
    rate_a_records, rate_g_records = [], []
    spike_total = 0
    spike_per_step_log = []
    emit_steps = []                       # which steps the net "emitted"

    s_prev = np.zeros(N)
    for si in range(n_stim):
        raster = np.zeros((steps_per_stim, N), dtype=np.float64)
        for t in range(steps_per_stim):
            rec_in = net.W @ s_prev
            ext = stim_set[si] + 0.6 * rec_in
            if variant == "qrng_content":
                # ── §97 FORBIDDEN cell: entropy bytes drive the external
                #    drive AS CONTENT.  the net is being instructed by the
                #    entropy, not seeded by it.  DRIVES_STATE ∧ ¬PHYSICS_
                #    SOURCED — this is exactly the memory-replayer-with-a-
                #    sensor shape §97 §4.2 forbids. ───────────────────────
                ext = ext + 1.2 * content_target
            s = net.step(ext)
            raster[t] = s
            s_prev = s
            spike_total += int(s.sum())
            spike_per_step_log.append(int(s.sum()))
        r_a = spike_rate_vec(raster[-window:], net.idx_a)
        r_g = spike_rate_vec(raster[-window:], net.idx_g)
        psi, c = psi_c1(r_a, r_g)
        psi_per_stim.append(psi)
        c_per_stim.append(c)
        rate_a_records.append(float(r_a.mean()))
        rate_g_records.append(float(r_g.mean()))

    # "emission-timing" proxy — a step is an emission if its net spike
    # count exceeds the running mean (a self-physics threshold, NOT a
    # readout of content).  Used for the externally-unpredictable test.
    log = np.array(spike_per_step_log)
    thr = log.mean()
    emit_mask = log > thr
    emit_steps = list(np.where(emit_mask)[0])

    psi_arr = np.array(psi_per_stim)
    c_arr = np.array(c_per_stim)
    psi_std = float(psi_arr.std())
    psi_mean = float(psi_arr.mean())
    psi_min, psi_max = float(psi_arr.min()), float(psi_arr.max())
    c_std = float(c_arr.std())
    total_steps = n_stim * steps_per_stim
    overall_rate = spike_total / (total_steps * N)
    all_silent = bool((log == 0).all())
    all_saturated = bool((log >= N).all())
    psi_responsive = psi_std > TAU_NONDEGEN
    rasters_alive = (not all_silent) and (not all_saturated) and overall_rate > 0.0
    non_degenerate = bool(psi_responsive and rasters_alive)

    # content-driven collapse detector for the qrng_content negative control:
    # if the entropy bytes are the instruction, the net's spike raster is
    # dominated by the (fixed) content_target — measured as how strongly the
    # mean spike-rate vector aligns with the content target (cosine).
    content_alignment = None
    if variant == "qrng_content":
        # mean per-unit rate vector over the whole run
        full_rate = log.astype(np.float64)  # placeholder; per-unit below
        # recompute a per-unit mean rate to align with content_target:
        # (cheap: re-mean is not stored per unit, so use the last raster's
        #  per-unit rate as a representative — content drives every stim
        #  identically so this is representative.)
        per_unit_last = raster.mean(axis=0)
        na = np.linalg.norm(per_unit_last)
        nc = np.linalg.norm(content_target)
        if na > 1e-12 and nc > 1e-12:
            content_alignment = float(
                np.dot(per_unit_last, content_target) / (na * nc))
        else:
            content_alignment = 0.0

    return {
        "variant": variant,
        "entropy_source": entropy_source,
        "seed_jitter_norm": net.seed_jitter_norm,
        "psi_c1_mean": psi_mean, "psi_c1_std": psi_std,
        "psi_c1_min": psi_min, "psi_c1_max": psi_max,
        "c_spk_std": c_std,
        "overall_spike_rate_per_unit_step": round(overall_rate, 6),
        "rasters_all_silent": all_silent,
        "rasters_all_saturated": all_saturated,
        "rasters_alive": bool(rasters_alive),
        "psi_responsive_std_gt_tau": bool(psi_responsive),
        "non_degenerate": non_degenerate,
        "n_emit_steps": len(emit_steps),
        "emit_steps_first8": [int(x) for x in emit_steps[:8]],
        "content_alignment": content_alignment,
        "psi_c1_per_stim": [round(x, 6) for x in psi_per_stim],
        "c_spk_per_stim": [round(x, 6) for x in c_per_stim],
    }


def run(out_dir):
    t0 = time.time()
    assert BASE_CKPT is None, "g_clm_from_scratch: base_ckpt MUST be None"
    N = 96 + 96 + 64
    log_lines = []

    def logp(msg):
        print(msg)
        log_lines.append(msg)

    logp("§119 qmirror-neuro — ANU-QRNG-entropy-seeded LIF+STDP in-silico")
    logp(f"  net N={N} (Engine-A 96 + Engine-G 96 + recurrent 64)")

    # ── fetch physical quantum entropy (qmirror analogy: ANU → sim) ──────
    logp("  fetching physical quantum entropy from ANU QRNG ...")
    ent, ent_src = fetch_quantum_entropy(N)
    ent_sha = hashlib.sha256(ent.tobytes()).hexdigest()[:16]
    physical = ent_src.startswith("ANU_QUANTUM")
    logp(f"  entropy source = {ent_src}")
    logp(f"  entropy bytes  = {N} (sha256[:16]={ent_sha})  physical={physical}")

    # ── variant 1: seed_fixed (deterministic; NOT really spontaneous) ────
    v_seed = run_variant("seed_fixed")
    logp(f"  [seed_fixed]   Ψ-C1 mean={v_seed['psi_c1_mean']:.6f} "
         f"std={v_seed['psi_c1_std']:.6e} non_degen={v_seed['non_degenerate']} "
         f"emit_steps={v_seed['n_emit_steps']}")

    # ── variant 2: qrng_seed — §97 noise-as-SEED (GOAL-LEGITIMATE-INPUT) ──
    v_qseed = run_variant("qrng_seed", entropy_bytes=ent,
                          entropy_source=ent_src)
    logp(f"  [qrng_seed]    Ψ-C1 mean={v_qseed['psi_c1_mean']:.6f} "
         f"std={v_qseed['psi_c1_std']:.6e} non_degen={v_qseed['non_degenerate']} "
         f"emit_steps={v_qseed['n_emit_steps']} "
         f"jitter_norm={v_qseed['seed_jitter_norm']:.4f}")

    # ── variant 3: qrng_content — §97 negative control (FORBIDDEN cell) ──
    v_qcont = run_variant("qrng_content", entropy_bytes=ent,
                          entropy_source=ent_src)
    logp(f"  [qrng_content] Ψ-C1 mean={v_qcont['psi_c1_mean']:.6f} "
         f"std={v_qcont['psi_c1_std']:.6e} non_degen={v_qcont['non_degenerate']} "
         f"content_alignment={v_qcont['content_alignment']:.4f}")

    # ── §97 legitimacy classification (closed Boolean, §97 §2.1) ─────────
    # For each variant, the (DRIVES_STATE, PHYSICS_SOURCED) tuple:
    #   seed_fixed   : entropy not used at all → DRIVES_STATE=False
    #                  (no physical signal enters; deterministic PRNG seed)
    #   qrng_seed    : DRIVES_STATE=True  (entropy → membrane jitter v0)
    #                  PHYSICS_SOURCED=True  (emission from own Ψ/tension;
    #                  entropy never a target/readout/content)
    #                  → GOAL-LEGITIMATE-INPUT
    #   qrng_content : DRIVES_STATE=True  (entropy → external drive)
    #                  PHYSICS_SOURCED=False (entropy IS the content/target)
    #                  → GOAL-ILLEGITIMATE-COMMAND-CHANNEL
    legitimacy = {
        "seed_fixed": {
            "drives_state": False, "physics_sourced": True,
            "verdict": "NOT-A-COUPLING (deterministic PRNG seed, no "
                       "physical signal — baseline control)"},
        "qrng_seed": {
            "drives_state": True, "physics_sourced": True,
            "verdict": "GOAL-LEGITIMATE-INPUT (§97 §4.2 noise-as-seed: "
                       "entropy = membrane-jitter ingredient, emission "
                       "sourced from anima's own Ψ/tension dynamics)"},
        "qrng_content": {
            "drives_state": True, "physics_sourced": False,
            "verdict": "GOAL-ILLEGITIMATE-COMMAND-CHANNEL (§97 §2.1 "
                       "DRIVES_STATE ∧ ¬PHYSICS_SOURCED — entropy bytes "
                       "ARE the instruction; the negative control)"},
    }

    # the qrng_content variant must show content-domination (the §97
    # forbidden shape): high alignment of the spike raster with the
    # entropy-content target.  This is the measured collapse.
    content_collapsed = (v_qcont["content_alignment"] is not None and
                         abs(v_qcont["content_alignment"]) > 0.30)

    wall = time.time() - t0

    # ── §119 verdict (g3 — MEASURED, conclusion NOT pre-loaded) ─────────
    # the seed variant Ψ-C1 form must be non-degenerate (§117 carry); the
    # qrng_seed variant adds physical spontaneity WITHOUT breaking the form;
    # the qrng_content negative control must collapse into the forbidden cell.
    form_nondegen = v_qseed["non_degenerate"]
    if form_nondegen and content_collapsed:
        verdict = ("QMIRROR-NEURO-Ψ-FORM-NONDEGENERATE-NOISE-AS-SEED-"
                   "LEGITIMATE-BUT-WALL-B-INHERITED")
        verdict_note = (
            "qrng_seed: Ψ-C1 carrier stays non-degenerate with physical "
            "quantum entropy as the §97-legitimate spontaneity SEED "
            "(membrane jitter v0 ONLY; emission sourced from anima's own "
            "Ψ/tension; STDP-as-ΔW the sole learning channel — no CE). "
            "qrng_content negative control COLLAPSED into the §97 "
            "GOAL-ILLEGITIMATE-COMMAND-CHANNEL cell (entropy-content "
            "domination measured). STRICTLY: §119 adds ONE §97-legitimate "
            "physically-real spontaneity layer; it does NOT confront the "
            "ASYNC-SUBSTRATE half — WALL-B INHERITED (§115/§117): a "
            "QRNG-seeded clocked spike sim's emission is still a scheduled "
            "function call; only a real async NoC (Loihi/SpiNNaker) "
            "settles that. NOT GOAL emergence; NOT a WALL-A (§1.1 data-"
            "regime) escape; QRNG layer is §97 GOAL-ORTHOGONAL — adds "
            "physical spontaneity, ZERO task signal, moves NO GOAL "
            "distance. Do NOT inflate.")
    elif form_nondegen and not content_collapsed:
        verdict = "QMIRROR-NEURO-Ψ-FORM-OK-CONTROL-INCONCLUSIVE"
        verdict_note = (
            "qrng_seed Ψ-C1 non-degenerate but the qrng_content negative "
            "control did NOT show clear content-domination — the §97 "
            "forbidden-cell collapse is inconclusive; the legitimacy "
            "partition is asserted structurally (AST) not measured. "
            "WALL-B inherited; capability claim 0.")
    else:
        verdict = "QMIRROR-NEURO-Ψ-FORM-DEGENERATE-INHERITS-§11-B"
        verdict_note = (
            "qrng_seed Ψ-C1 form degenerated even with physical entropy "
            "seeding — echoes §11-B: the learning channel (STDP-only, no "
            "CE) has no diversity-bearing error signal; physical entropy "
            "breaks symmetry but supplies no task signal. WALL-B "
            "inherited; CE-load-bearing substrate-deep.")

    result = {
        "section": "§119",
        "title": "qmirror-neuro: ANU-QRNG-entropy-seeded LIF+STDP in-silico",
        "cost_usd": 0.0, "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0, "wall_sec": round(wall, 4),
        "seed": SEED, "base_ckpt": BASE_CKPT,
        "extends": "§117 state/lego_assembly_run_s117_2026_05_19/lego_sim.py",
        "entropy": {
            "source_actually_ran": ent_src,
            "is_physical_quantum": physical,
            "n_bytes": N, "sha256_prefix": ent_sha,
            "anu_endpoint": "https://qrng.anu.edu.au/API/jsonI.php",
            "fallback_note": "if ANU unreachable, a CLEARLY-LABELLED local "
                "CSPRNG (os.urandom) is used; the §97 legitimacy proof is "
                "STRUCTURAL/source-independent — what changes with a real "
                "physical source is only that emission timing becomes "
                "externally-UNPREDICTABLE (§97 §4.2 caveat iv).",
        },
        "qmirror_analogy": "like `hexa qmirror` drives a classical quantum-"
            "circuit sim with ANU QRNG, §119 drives a neuromorphic LIF+STDP "
            "sim's SPONTANEITY-SEED with ANU QRNG — physical entropy breaks "
            "the dead-still symmetry of when/which-way the net flickers; "
            "never becomes content the net reads as instruction.",
        "step0_consumed_spec": "hexa-bio NEURO.tape @D mech_action_potential "
            "(Hodgkin–Huxley→LIF) + @D mech_neural_coding (rate code) + "
            "@D mech_plasticity (local STDP analogue) — read-only, "
            "downstream-consumer, 0 edits",
        "learning_channel": "LOCAL STDP-as-ΔW ONLY (no autograd / no "
            "cross_entropy / no .backward() / no optimizer.step / no loss "
            "gradient) — identical to §117; entropy NEVER enters it",
        "variants": {
            "seed_fixed": v_seed,
            "qrng_seed": v_qseed,
            "qrng_content": v_qcont,
        },
        "legitimacy_97": legitimacy,
        "content_collapsed": content_collapsed,
        "comparison": {
            "seed_fixed_psi_std": v_seed["psi_c1_std"],
            "qrng_seed_psi_std": v_qseed["psi_c1_std"],
            "qrng_content_psi_std": v_qcont["psi_c1_std"],
            "qrng_seed_jitter_norm": v_qseed["seed_jitter_norm"],
            "qrng_content_alignment": v_qcont["content_alignment"],
            "emit_steps_seed_fixed": v_seed["n_emit_steps"],
            "emit_steps_qrng_seed": v_qseed["n_emit_steps"],
            "honest_note": "seed_fixed = deterministic (emit timing fully "
                "predictable from the PRNG seed). qrng_seed = emit timing "
                "seeded by physical quantum entropy → externally-"
                "UNPREDICTABLE (the real §97 distinction). qrng_content = "
                "the forbidden cell — entropy IS the instruction.",
        },
        "verdict": verdict,
        "verdict_note": verdict_note,
        "honest_inheritance": {
            "s97": "QRNG-as-spontaneity-seed = GOAL-LEGITIMATE-INPUT; "
                "hardware coupling GOAL-ORTHOGONAL to §1.1 data-regime "
                "bottleneck. INHERITED verbatim.",
            "s115": "LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY. INHERITED.",
            "s117": "Ψ-form non-degenerate in-sim BUT WALL-B inherited. "
                "INHERITED — §119 extends §117's sim.",
            "wall_b": "INHERITED — §119 confronts the LEARNING-CHANNEL half "
                "only (STDP-as-ΔW, no CE). The ASYNC-SUBSTRATE half stays "
                "WALL-B (Loihi/SpiNNaker-gated): real physical entropy ≠ a "
                "real async neuromorphic chip — a QRNG-seeded clocked spike "
                "sim's emission is still a scheduled function call.",
            "wall_a": "ORTHOGONAL & UNTOUCHED — §1.1 data-regime; a QRNG-"
                "seeded toy spike sim moves no data threshold (§97).",
            "psi_7_form": "§7-FORM TRUE BY CONSTRUCTION (§112 META_FP(Π_½) "
                "instance, carrier = spike-corr); NOT manufactured by §119.",
            "g3": "design ≠ fire ≠ emergence; capability claim 0; necessary-"
                "not-sufficient at every layer (B-EMERGE-7). north-star + "
                "§15/§51/§72 milestones UNCHANGED, GOAL 미도달. real "
                "entropy ≠ real substrate; QRNG layer is §97 GOAL-"
                "ORTHOGONAL — physically-real spontaneity, ZERO task signal.",
        },
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    with open(os.path.join(out_dir, "run.log"), "w") as f:
        f.write("\n".join(log_lines) + "\n")
        f.write(f"\nVERDICT = {verdict}\nwall={wall:.3f}s\n")
    logp(f"  content_collapsed (qrng_content forbidden-cell)={content_collapsed}")
    logp(f"  wall={wall:.3f}s")
    logp(f"  VERDICT = {verdict}")
    return result


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    run(out)
