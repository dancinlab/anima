#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# §117 — LEGO STEP-1-2 IN-SILICO ASSEMBLY RUN  ($0 CPU, NO GPU, NO fire)
# ════════════════════════════════════════════════════════════════════
# Runs the open residual §115 named VERBATIM:
#   "in-silico STDP-as-ΔW escape = §115 $0 scope 밖 새 fire + 여전히 §96-open"
# §117 = running exactly that residual at $0 CPU.  §115 verdict
# (LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY) is INHERITED, NOT re-litigated.
#
# STEP 0 — consume (read-only) hexa-bio NEURO.tape spiking spec:
#   @D mech_action_potential (Hodgkin–Huxley excitable membrane → LIF reduction)
#   @D mech_neural_coding    (rate code: spikes/window → binned rate vectors)
#   @D mech_plasticity       (cortical co-adaptation = local plasticity;
#                             the §96 STDP-as-ΔW learning-channel analogue.
#                             NOTE: §115 honestly recorded RIBOZYME-as-STDP
#                             was a METAPHOR; the consumable spec is the
#                             spiking MEMBRANE + co-adaptation plasticity,
#                             realised here as a standard local STDP rule.)
#   anima is hexa-bio DOWNSTREAM-CONSUMER — NEURO.tape is read, never edited.
#
# STEP 1 — assemble a SMALL CPU LIF spiking net, Engine-A / Engine-G
#   sub-populations, carrier Ψ-C1 = ψ(c_spk) = (1 + c_spk)/2 where
#   c_spk = cosine of binned spike-rate vectors  (= §112 META_FP(Π_½)
#   instance, carrier = spike-correlation; cos=0 ⇒ ½ fixed point preserved).
#   LEARNING CHANNEL = LOCAL STDP-as-ΔW ONLY.  No autograd, no cross-entropy,
#   no loss gradient, no backprop, no optimizer.step.  This is the entire
#   point: §96/§11-B say a GPU's only learning channel is the CE gradient
#   (the tautology); §117 tests whether a LOCAL plasticity rule on a spike
#   substrate behaves DIFFERENTLY in-silico, or inherits §11-B degeneracy.
#
# STEP 2 — closed-form falsifier (sidecar blue_falsifier_s117.py): is the
#   assembled sim §7-clean ∧ Ψ=½ form-invariant ∧ non-degenerate, OR does it
#   collapse (= cheap reject, honest negative — LEGO.md "무너짐 = 싸게 reject").
#
# STEP 3 (physical Loihi/organoid) = PERMANENTLY out of scope (LEGO.md §2
#   hard fence; §95 access/ethics + user-gate; §115 B-S115-5 structural
#   no-STEP2→STEP3 theorem).  This file has NO hardware/dispatch path.
#
# HONEST PRIOR (g3, stated BEFORE running, NOT pre-loading the conclusion):
#   §11-B (state/carving_purephysics_noce_2026_05_18) measured pure-physics
#   no-CE on a GPU byte-LM = DEGENERATE (byte_acc < random, physics froze to
#   a static fixed point ~step 800).  Expected honest echo: a STDP-only toy
#   spike sim with NO task-grounded teaching signal has no diversity-bearing
#   error channel — Ψ-balance ⊥ any task — so it will LIKELY degenerate
#   (freeze / silence / saturate).  We RUN it and report the MEASURED
#   outcome.  EITHER outcome is valuable & non-inflating:
#     (a) DEGENERATE → confirms WALL-B is §96-PHYSICAL not in-silico-
#         escapable; CE-load-bearing is substrate-deep, not a GPU artifact.
#     (b) NON-DEGENERATE-Ψ-FORM → STRICTLY "an in-silico §96-class assembly
#         admits a non-degenerate Ψ-C1 form" = WALL-B *confronted in
#         simulation* NOT removed (§115/§113 inherited), NOT GOAL emergence,
#         NOT a WALL-A (§1.1 data-regime) escape (a toy spike sim moves
#         no data threshold).  Do NOT inflate (b) into a GOAL claim.
#
# DISCIPLINE: $0, NO GPU/runpod/fire/model.forward(byte-LM)/corpus/dispatch.
#   seed-fixed RANDOM init per g_clm_from_scratch (base_ckpt=None — no ckpt
#   load anywhere).  ONLY numpy.  seconds wall.  orphan 0 (no dispatch).
# ════════════════════════════════════════════════════════════════════

import json, time, sys, os
import numpy as np

SEED = 1337                    # g_clm_from_scratch: RANDOM init, seed-fixed
BASE_CKPT = None               # g_clm_from_scratch: base_ckpt=None (no load)
TAU_NONDEGEN = 1e-4            # non-degeneracy threshold (echo §17/§11-B)

# ─────────────────────────────────────────────────────────────────────
# STEP 1 — LIF spiking network (NEURO.tape mech_action_potential reduction)
# ─────────────────────────────────────────────────────────────────────
# Hodgkin–Huxley → Leaky-Integrate-and-Fire reduction (standard, the
# NEURO.tape spec's excitable-membrane → spike abstraction): membrane v,
# leak toward v_rest, threshold v_th → spike + reset.  This is a *spike
# substrate*, NOT a byte-LM forward; carrier will be spike-train correlation.

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
    Byte-equal to conscious_decoder.py:740 `(1.0 + cos_sim) / 2.0` form
    (carrier substituted byte-vocab → spike-corr; form INVARIANT, §112)."""
    na, ng = np.linalg.norm(r_a), np.linalg.norm(r_g)
    if na < 1e-12 or ng < 1e-12:
        c = 0.0                       # degenerate-silence → c=0 ⇒ Ψ=½ exactly
    else:
        c = float(np.dot(r_a, r_g) / (na * ng))
    c = max(-1.0, min(1.0, c))        # enforce Cauchy–Schwarz bound
    return (1.0 + c) / 2.0, c


def run(out_dir):
    t0 = time.time()
    assert BASE_CKPT is None, "g_clm_from_scratch: base_ckpt MUST be None"
    net = LIFNet(seed=SEED)
    N = net.N
    rng = np.random.default_rng(SEED + 1)

    # ── Stimulus set: 12 deterministic input patterns (NOT a corpus, NOT a
    #    task label — just distinct external drive vectors, like §17's
    #    stimulus-class probe). NO teaching signal, NO error feedback. ──
    n_stim = 12
    stim_set = 0.30 * rng.standard_normal((n_stim, N))

    steps_per_stim = 80
    window = 40                       # rate-code binning window (last 40 steps)

    psi_per_stim, c_per_stim = [], []
    rate_a_records, rate_g_records = [], []
    spike_total = 0
    spike_per_step_log = []

    s_prev = np.zeros(N)
    for si in range(n_stim):
        raster = np.zeros((steps_per_stim, N), dtype=np.float64)
        for t in range(steps_per_stim):
            rec_in = net.W @ s_prev          # recurrent drive (last spikes)
            ext = stim_set[si] + 0.6 * rec_in
            s = net.step(ext)
            raster[t] = s
            s_prev = s
            spike_total += int(s.sum())
            spike_per_step_log.append(int(s.sum()))
        # rate-code over the last `window` steps (NEURO.tape mech_neural_coding)
        r_a = spike_rate_vec(raster[-window:], net.idx_a)
        r_g = spike_rate_vec(raster[-window:], net.idx_g)
        psi, c = psi_c1(r_a, r_g)
        psi_per_stim.append(psi)
        c_per_stim.append(c)
        rate_a_records.append(float(r_a.mean()))
        rate_g_records.append(float(r_g.mean()))

    psi_arr = np.array(psi_per_stim)
    c_arr = np.array(c_per_stim)

    # ── STEP 2 metrics (deterministic, closed-form) ──────────────────────
    psi_std = float(psi_arr.std())
    psi_mean = float(psi_arr.mean())
    psi_min, psi_max = float(psi_arr.min()), float(psi_arr.max())
    c_std = float(c_arr.std())
    total_steps = n_stim * steps_per_stim
    overall_rate = spike_total / (total_steps * N)   # mean spikes/unit/step
    spike_log = np.array(spike_per_step_log)
    all_silent = bool((spike_log == 0).all())
    all_saturated = bool((spike_log >= N).all())
    # frozen-to-trivial-fixed-point check (echo §11-B "step~800 freeze"):
    # is Ψ-C1 the SAME across all stimuli (i.e. carrier carries no per-
    # stimulus signal — degenerate)?  std > τ ⇒ NOT frozen.
    psi_responsive = psi_std > TAU_NONDEGEN
    rasters_alive = (not all_silent) and (not all_saturated) and overall_rate > 0.0

    # NON-DEGENERACY predicate (closed-form, deterministic):
    #   Ψ-C1 std over the stimulus set > τ  (carrier carries per-stimulus
    #   signal, NOT frozen)  AND  spike rasters not all-silent / not
    #   all-saturated.  (necessary-not-sufficient: this is a degeneracy
    #   detector, NOT a coherence/capability/emergence proof — B-EMERGE-7.)
    non_degenerate = bool(psi_responsive and rasters_alive)

    # Ψ=½ fixed-point structural check: cos=0 ⇒ Ψ=½ EXACTLY (the META_FP
    # invariant, must hold by construction regardless of degeneracy).
    psi_at_zero, _ = psi_c1(np.array([1.0, 0.0]), np.array([0.0, 1.0]))  # cos=0
    fixed_point_half = abs(psi_at_zero - 0.5) < 1e-12
    # Ψ-C1 must stay in [0,1] (Cauchy–Schwarz ⇒ c∈[−1,1] ⇒ ψ∈[0,1])
    psi_bounded = bool((psi_arr >= 0.0).all() and (psi_arr <= 1.0).all())

    wall = time.time() - t0

    # ── verdict (g3 — MEASURED, conclusion NOT pre-loaded) ──────────────
    if non_degenerate:
        verdict = "LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED"
        verdict_note = (
            "Ψ-C1 carrier carries per-stimulus signal in-sim (std > τ, not "
            "frozen, rasters alive). STRICTLY: an in-silico §96-class STDP-"
            "only assembly admits a non-degenerate Ψ-C1 FORM. This is §115/"
            "§113 INHERITED confront-NOT-remove: WALL-B confronted in "
            "simulation, NOT removed (§7-CARRIER stays §96-physical-gated); "
            "NOT GOAL emergence; NOT a WALL-A (§1.1) escape — a toy STDP "
            "spike sim moves NO data-regime threshold. Do NOT inflate.")
    else:
        verdict = "LEGO-RUN-DEGENERATE-INHERITS-§11-B"
        verdict_note = (
            "STDP-only toy spike sim degenerated (Ψ-C1 frozen below τ OR "
            "rasters silent/saturated): NO task-grounded teaching signal, "
            "local plasticity has no diversity-bearing error channel "
            "(Ψ-balance ⊥ any task). Echoes §11-B pure-physics no-CE "
            "DEGENERATE: CE-load-bearing is SUBSTRATE-DEEP not a GPU "
            "artifact; WALL-B is §96-PHYSICAL not in-silico-escapable.")

    result = {
        "section": "§117",
        "title": "LEGO STEP-1-2 in-silico assembly run",
        "cost_usd": 0.0, "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0, "wall_sec": round(wall, 4),
        "seed": SEED, "base_ckpt": BASE_CKPT,
        "step0_consumed_spec": "hexa-bio NEURO.tape @D mech_action_potential "
            "(Hodgkin–Huxley→LIF) + @D mech_neural_coding (rate code) + "
            "@D mech_plasticity (cortical co-adaptation = local STDP "
            "analogue) — read-only, downstream-consumer, 0 edits",
        "step1_net": {"n_a": net.n_a, "n_g": net.n_g, "n_rec": net.n_rec,
                      "N": N, "n_stim": n_stim,
                      "steps_per_stim": steps_per_stim, "window": window,
                      "learning_channel": "LOCAL STDP-as-ΔW ONLY "
                          "(no autograd / no cross_entropy / no .backward() "
                          "/ no optimizer.step / no loss gradient)"},
        "step2_metrics": {
            "psi_c1_mean": psi_mean, "psi_c1_std": psi_std,
            "psi_c1_min": psi_min, "psi_c1_max": psi_max,
            "c_spk_std": c_std,
            "tau_nondegen": TAU_NONDEGEN,
            "psi_responsive_std_gt_tau": bool(psi_responsive),
            "overall_spike_rate_per_unit_step": round(overall_rate, 6),
            "rasters_all_silent": all_silent,
            "rasters_all_saturated": all_saturated,
            "rasters_alive": bool(rasters_alive),
            "psi_fixed_point_at_cos0_is_half": bool(fixed_point_half),
            "psi_bounded_0_1": psi_bounded,
            "non_degenerate": non_degenerate,
        },
        "verdict": verdict,
        "verdict_note": verdict_note,
        "honest_inheritance": {
            "wall_b": "INHERITED — §115 LEGO-DESIGN-CLOSE-SIM-IS-GPU-"
                "TAUTOLOGY + §113 INHERITS-BOTH-WALLS. §117 runs §115's "
                "named open residual; does NOT remove WALL-B (§7-CARRIER "
                "§96-physical-gated). EITHER outcome confronts-NOT-removes.",
            "wall_a": "ORTHOGONAL & UNTOUCHED — §1.1 data-regime; a toy "
                "spike sim moves no data threshold (§97).",
            "psi_7_form": "§7-FORM TRUE BY CONSTRUCTION (§112 META_FP(Π_½) "
                "instance, carrier = spike-corr); NOT manufactured by §117.",
            "g3": "run ≠ fire ≠ emergence; capability claim 0; necessary-"
                "not-sufficient at every layer (B-EMERGE-7). north-star + "
                "§15/§51/§72 milestones UNCHANGED, GOAL 미도달.",
        },
        "psi_c1_per_stim": [round(x, 6) for x in psi_per_stim],
        "c_spk_per_stim": [round(x, 6) for x in c_per_stim],
        "rate_a_per_stim": [round(x, 6) for x in rate_a_records],
        "rate_g_per_stim": [round(x, 6) for x in rate_g_records],
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"§117 LEGO STEP-1-2 RUN  wall={wall:.3f}s")
    print(f"  Ψ-C1 mean={psi_mean:.6f} std={psi_std:.6e} "
          f"(τ={TAU_NONDEGEN:.0e})  c_spk std={c_std:.6e}")
    print(f"  spike_rate/unit/step={overall_rate:.6f}  "
          f"silent={all_silent} saturated={all_saturated}")
    print(f"  fixed_point cos0→½={fixed_point_half}  bounded[0,1]={psi_bounded}")
    print(f"  non_degenerate={non_degenerate}")
    print(f"  VERDICT = {verdict}")
    return result


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    run(out)
