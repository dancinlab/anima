#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# §118 — TRACK 0 IN-SILICO  ($0 CPU, NO GPU/runpod/fire/dispatch)
# ════════════════════════════════════════════════════════════════════
# Executes the $0-simulatable subset of HEXAD/NEUROMORPHIC/TRACK0_INSILICO.md:
# the §96 §4.5 distinguishing cells, in a tiny CPU LIF/numpy rig.
#
# THE ONE HONEST MOVE (TRACK0_INSILICO.md §0):  §115 pre-registered the
# blanket verdict LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY.  Track 0 makes it
# PRECISE by splitting §11-B-as-GPU-artifact into two halves:
#   (i)  LEARNING-CHANNEL half  — is "physics-only = degenerate" a property
#        of the CE-only *channel* or of the *model*?  SIMULATABLE: run a cell
#        with NO CE / NO backprop, only event-local plasticity (STDP) — the
#        silicon is irrelevant, the available *learning channel* is what
#        changes.  Track 0 CONFRONTS this half.
#   (ii) ASYNC-SUBSTRATE half   — a spontaneous emission as a PHYSICAL spike
#        event vs a scheduled function call on a global clock.  NOT
#        simulatable on a clocked GPU/CPU sim.  Track 0 does NOT touch this;
#        stays Loihi/SpiNNaker-gated (Tracks L/S/P).  §117 INHERITED.
#
# 4-CELL RIG (§96 §4.5 / TRACK0_INSILICO.md §2, simulatable subset on CPU):
#   GPU-CE         — toy CE-gradient weight update (sanity: expect NON-DEGEN)
#   GPU-noCE       — no learning channel at all   (expect DEGENERATE; §11-B)
#   SIM-noCE-STDP  — event-local STDP as the SOLE update, no CE / no backprop
#                    — THE DECISIVE CELL (the learning-channel-half confront)
#   SIM-CE         — CE readout positive control  (VOID guard: must be
#                    non-degenerate, else the rig is broken)
#
# §3 PRE-REGISTERED CLOSED PREDICATE (verbatim from TRACK0_INSILICO.md §3 /
#   §96 §4.5):
#     NON_DEGENERATE(cell) := byte_acc > 1/256
#                           ∧ physics_not_frozen   (Ψ/tension/Φ std > τ)
#                           ∧ honest_§9_coherent ≥ 1/5   (§9 SSOT import)
#
# §3 3-OUTCOME VERDICT PARTITION (stated BEFORE the run — no result-fitting):
#   SIM-CONFRONTS-LEARNING-CHANNEL                 if
#     NON_DEGENERATE(SIM-noCE-STDP)=True ∧ GPU-noCE DEGENERATE ∧ SIM-CE non-degen
#   SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF   if
#     NON_DEGENERATE(SIM-noCE-STDP)=False  (GPU-noCE/SIM-CE as expected)
#   VOID                                           if
#     SIM-CE (guard) degenerate — rig broken, no verdict
#
# HEADLINE (TRACK0_INSILICO.md §4 — load-bearing, NOT a positive):
#   §96 design-open #1 — softmax(QK^T) self-attention is SPIKING-INCOMPATIBLE,
#   it must be REPLACED not ported.  This rig confronts the LEARNING-CHANNEL
#   half ONLY.  The full spiking-anima instantiation stays gated on the
#   attention-replacement design-open; the async-substrate half stays WALL-B
#   (Loihi/SpiNNaker-gated, §117 INHERITED).  A toy non-degeneracy = substrate
#   LIVENESS, NOT capability, NOT GOAL.  Do NOT inflate.
#
# DISCIPLINE: $0, NO GPU/runpod/fire/model.forward(byte-LM)/corpus/dispatch.
#   ≤256 units, seed-fixed RANDOM init per g_clm_from_scratch (base_ckpt=None).
#   ONLY numpy.  seconds wall.  orphan 0.  pure CPU.
# ════════════════════════════════════════════════════════════════════

import json, time, os, sys
# single-thread BLAS — must be set BEFORE numpy import. This tiny CPU rig's
# matmuls are sub-millisecond; multi-thread BLAS over-subscription on a
# 240-unit W@s product otherwise thrashes (~25s for 960 matmuls observed).
# Pure environment fix — does NOT change any numerical result (deterministic).
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

# ── §9 honest-coherence metric — SSOT IMPORT (NOT re-implemented) ─────
_S9_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "verify_emergence_metric_2026_05_18"))
sys.path.insert(0, _S9_DIR)
from emergence_metric import honest_coherent  # §9 SSOT — RESEARCH.md §9

SEED = 1337                    # g_clm_from_scratch: RANDOM init, seed-fixed
BASE_CKPT = None               # g_clm_from_scratch: base_ckpt=None (no load)
TAU_FROZEN = 1e-4              # physics-not-frozen threshold (echo §17/§11-B)
CHANCE = 1.0 / 256.0           # byte_acc chance floor (256-symbol alphabet)

# ─────────────────────────────────────────────────────────────────────
# Shared substrate — a tiny LIF spiking net (NEURO.tape mech_action_potential
# reduction: Hodgkin–Huxley excitable membrane → Leaky-Integrate-and-Fire).
# Engine-A / Engine-G sub-populations + a recurrent block.  ≤256 units.
# Each CELL differs ONLY in its WEIGHT-UPDATE CHANNEL — that is the whole
# experiment (the §96 §4.5 controlled comparison).
# ─────────────────────────────────────────────────────────────────────

# tiny deterministic "task": a stimulus→symbol map over a 256-symbol
# alphabet.  NOT a corpus, NOT a byte-LM forward.  Each of the 12 distinct
# stimulus patterns has one ground-truth target symbol — the canonical
# "which stimulus is driving me" classification.  This is genuinely
# learnable from the per-stimulus LIF rate vector by a 256-way head IFF
# a teaching/error signal is available (the CE channel); with no learning
# channel ('none') or an error-free local rule ('stdp') it is not directly
# fit — which is exactly the §96 §4.5 contrast.  Target spacing 37 keeps
# the 12 targets spread across the 256-symbol alphabet (NOT lattice-derived
# — an arbitrary coprime spacing for symbol separation, f1/f2 safe).
def task_target(stim_idx):    # ground-truth symbol for a stimulus pattern
    return (stim_idx * 37 + 11) % 256


class LIFCell:
    """One §96 §4.5 cell.  Shared LIF spike substrate; the `channel`
    argument selects the WEIGHT-UPDATE rule — the only thing that varies:
        'ce'    — toy CE-gradient update  (a teaching/error signal)
        'none'  — NO update at all        (frozen weights)
        'stdp'  — event-local STDP ONLY   (no CE, no backprop, no error)
    """

    def __init__(self, channel, n_a=88, n_g=88, n_rec=64, seed=SEED):
        assert channel in ("ce", "none", "stdp")
        assert BASE_CKPT is None, "g_clm_from_scratch: base_ckpt MUST be None"
        self.channel = channel
        rng = np.random.default_rng(seed)            # RANDOM, seed-fixed
        self.n_a, self.n_g, self.n_rec = n_a, n_g, n_rec
        N = n_a + n_g + n_rec
        self.N = N                                   # ≤ 256 units
        # LIF params (NEURO.tape excitable-membrane reduction)
        self.v_rest, self.v_th, self.v_reset = 0.0, 1.0, 0.0
        self.tau_m = 20.0
        self.dt = 1.0
        self.refrac = 2
        self.v = np.full(N, self.v_rest, dtype=np.float64)
        self.refr = np.zeros(N, dtype=np.int64)
        # recurrent weights — RANDOM seed-fixed init, base_ckpt=None
        self.W = 0.05 * rng.standard_normal((N, N))
        np.fill_diagonal(self.W, 0.0)
        self.W0 = self.W.copy()                      # frozen reference
        self.bias = 0.18 * rng.standard_normal(N)
        # STDP traces (event-local eligibility) — used by 'stdp' channel only
        self.tr_pre = np.zeros(N)
        self.tr_post = np.zeros(N)
        self.tau_stdp = 20.0
        self.A_plus = 0.012
        self.A_minus = 0.0126
        self.w_max = 0.5
        # CE-channel readout head (used by 'ce' channel only): maps the
        # recurrent-pop rate vector → 256 logits.  toy linear head.
        self.head = 0.10 * rng.standard_normal((256, n_rec))
        self.head0 = self.head.copy()      # frozen reference (head drift)
        self.head_lr = 0.05
        self.rng = rng
        self.idx_a = slice(0, n_a)
        self.idx_g = slice(n_a, n_a + n_g)
        self.idx_r = slice(n_a + n_g, N)

    # ── LIF membrane step (shared by all cells) ──────────────────────
    def _lif_step(self, ext):
        active = self.refr <= 0
        dv = (-(self.v - self.v_rest) / self.tau_m) + ext + self.bias
        self.v[active] += self.dt * dv[active]
        spike = (self.v >= self.v_th) & active
        self.v[spike] = self.v_reset
        self.refr[spike] = self.refrac
        self.refr[~spike] -= 1
        self.refr = np.maximum(self.refr, -1)
        return spike.astype(np.float64)

    # ── event-local STDP — the SOLE update for the 'stdp' channel.
    #    Δw = A+·tr_pre·post − A−·pre·tr_post.  Depends ONLY on pre/post
    #    spike traces — NEVER on a loss/error/target.  No autograd, no
    #    cross_entropy, no .backward(), no optimizer.step.  This is the
    #    decisive learning-channel-half confront (§96 §4.5).
    def _stdp_update(self, s):
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

    # ── toy CE-gradient update — used ONLY by the 'ce' channel.  This IS
    #    a teaching/error signal (the GPU tautology's one channel).  It is
    #    a hand-rolled local softmax-CE gradient on a 256-way linear head
    #    — NOT autograd, NOT torch, NOT .backward() — but it IS a
    #    CE-error-driven update, which is exactly the channel §96 §4.5
    #    contrasts against STDP.  byte-LM forward is NOT used (toy head).
    def _ce_update(self, rate_r, tgt):
        z = self.head @ rate_r                       # 256 logits
        z = z - z.max()
        p = np.exp(z); p = p / p.sum()
        onehot = np.zeros(256); onehot[tgt] = 1.0
        # dL/dz = p - onehot   (softmax-CE gradient — an ERROR signal)
        gz = p - onehot
        self.head -= self.head_lr * np.outer(gz, rate_r)
        return int(np.argmax(z))                     # predicted symbol

    def predict(self, rate_r):
        """next-symbol prediction from the recurrent-pop rate vector."""
        z = self.head @ rate_r
        return int(np.argmax(z))


def _psi_c1(r_a, r_g):
    """Ψ-C1 = §112 META_FP(Π_½) instance, carrier = spike-correlation.
        c_spk = cos(r_A, r_G) ∈ [−1,1]   (Cauchy–Schwarz)
        Ψ-C1  = (1 + c_spk) / 2          (cos=0 ⇒ ½ fixed point)
    Byte-equal to conscious_decoder.py:740 `(1.0 + cos_sim)/2.0` form
    (carrier substituted byte-vocab → spike-corr; form INVARIANT, §112)."""
    na, ng = np.linalg.norm(r_a), np.linalg.norm(r_g)
    if na < 1e-12 or ng < 1e-12:
        c = 0.0
    else:
        c = float(np.dot(r_a, r_g) / (na * ng))
    c = max(-1.0, min(1.0, c))
    return (1.0 + c) / 2.0, c


def run_cell(channel, label):
    """Run one §96 §4.5 cell; return its measured numbers.  Per-cell ONLY
    the weight-update channel differs (shared LIF substrate + seed)."""
    cell = LIFCell(channel=channel, seed=SEED)
    N = cell.N
    rng = np.random.default_rng(SEED + 1)
    # 12 deterministic stimulus patterns — distinct external drive vectors
    # (like §17's stimulus-class probe).  NOT a corpus.
    n_stim = 12
    stim_set = 0.30 * rng.standard_normal((n_stim, N))
    steps_per_stim = 80
    window = 40                    # rate-code window (NEURO.tape coding)

    psi_traj, tension_traj, phi_traj = [], [], []
    correct, total_pred = 0, 0
    gen_symbols = []               # the cell's emitted symbol stream
    spike_total = 0
    spike_per_step = []
    s_prev = np.zeros(N)
    # n_epochs passes over the 12-stimulus set.  The CE channel needs
    # repeated (rate, target) supervision to converge — this is the
    # ordinary training-epoch budget, identical for every cell (the only
    # thing that varies is whether the channel USES the supervision).
    n_epochs = 8
    rate_cache = {}                # last per-stimulus rate vector

    for ep in range(n_epochs):
        for si in range(n_stim):
            raster = np.zeros((steps_per_stim, N))
            # each stimulus = an independent probe: reset the recurrent
            # spike state + membrane so the per-stimulus rate vector is
            # reproducible across epochs (the CE head then trains on a
            # STABLE conditioning vector — otherwise drift across epochs
            # makes the scored final-epoch rate vector mismatch what was
            # learned).  Mirrors §17's stimulus-class probe discipline.
            s_prev = np.zeros(N)
            cell.v[:] = cell.v_rest
            cell.refr[:] = 0
            for t in range(steps_per_stim):
                rec_in = cell.W @ s_prev
                ext = stim_set[si] + 0.6 * rec_in
                s = cell._lif_step(ext)
                raster[t] = s
                s_prev = s
                spike_total += int(s.sum())
                spike_per_step.append(int(s.sum()))
                # ── weight-update channel — THE experiment ───────────
                if channel == "stdp":
                    cell._stdp_update(s)             # event-local ONLY
                # 'none' : no update at all (frozen W, frozen head)

            # per-stimulus rate vector (NEURO.tape mech_neural_coding,
            # last `window` steps) — the conditioning signal
            rate_r = raster[-window:, cell.idx_r].mean(axis=0)
            rate_cache[si] = rate_r
            tgt = task_target(si)
            # ── prediction + (CE channel only) error update ──────────
            #   predict BEFORE any update — the emitted symbol is the
            #   cell's current readout of this stimulus.
            pred = cell.predict(rate_r)
            if channel == "ce":
                cell._ce_update(rate_r, tgt)         # CE-error update
            # emitted stream for §9: ONE symbol per (epoch, stimulus) =
            # 8×12 = 96 symbols.  This is the cell's STIMULUS-DISCRIMINATION
            # stream — what symbol it assigns to each stimulus across
            # learning.  A cell that learns distinct per-stimulus answers
            # produces a VARIED stream; a cell collapsed onto one symbol
            # (no learning, or a degenerate substrate) produces a
            # near-constant stream = the §9 cascade signature.  This is the
            # natural "emission" for a discrimination rig (a 12-class head
            # has no autoregressive byte generation; emitting one symbol
            # per stimulus is the honest analogue, NOT 80 repeats of one
            # classification — that would be a cascade by construction).
            gen_symbols.append(pred)
            # score only the final epoch (post-learning) for byte_acc
            if ep == n_epochs - 1:
                if pred == tgt:
                    correct += 1
                total_pred += 1
                # per-stimulus physics readout — final epoch
                r_a = raster[-window:, cell.idx_a].mean(axis=0)
                r_g = raster[-window:, cell.idx_g].mean(axis=0)
                r_all = raster[-window:].mean(axis=0)
                psi, _c = _psi_c1(r_a, r_g)
                # tension = LIF leak/relaxation proxy (§96 §6: leak −v/τ_m
                # IS the restoring force) — mean squared rate magnitude
                tension = float((r_all ** 2).mean())
                # Φ proxy = spike-train correlation dispersion (§96 §6
                # NATIVE-MEASUREMENT: Φ from real spike rasters)
                sub = raster[-window:, ::8]
                if sub.shape[1] >= 2 and sub.std() > 1e-9:
                    cc = np.corrcoef(sub.T)
                    iu = np.triu_indices_from(cc, k=1)
                    phi = float(np.nanstd(cc[iu]))
                else:
                    phi = 0.0
                psi_traj.append(psi)
                tension_traj.append(tension)
                phi_traj.append(phi)

    # ── post-training readout sweep — 2 extra passes over the 12 stimuli
    #   purely to extend the emitted stream to ≥100 symbols for clean §9
    #   5-window scoring.  NO weight update here (CE head + W frozen for
    #   this readout) — it only reads what the cell already learned.
    for _rep in range(2):
        for si in range(n_stim):
            s_prev = np.zeros(N)
            cell.v[:] = cell.v_rest
            cell.refr[:] = 0
            raster = np.zeros((steps_per_stim, N))
            for t in range(steps_per_stim):
                ext = stim_set[si] + 0.6 * (cell.W @ s_prev)
                s = cell._lif_step(ext)
                raster[t] = s
                s_prev = s
                # STDP keeps running during readout for the 'stdp' cell —
                # event-local plasticity has no train/eval split (it is
                # always-on by construction; this is honest, not a leak).
                if channel == "stdp":
                    cell._stdp_update(s)
            rate_r = raster[-window:, cell.idx_r].mean(axis=0)
            gen_symbols.append(cell.predict(rate_r))

    psi_arr = np.array(psi_traj)
    tension_arr = np.array(tension_traj)
    phi_arr = np.array(phi_traj)

    # ── byte_acc — fraction of correct next-symbol predictions ───────
    byte_acc = correct / total_pred if total_pred else 0.0

    # ── physics_not_frozen — Ψ AND tension AND Φ trajectory std > τ ──
    #   (a frozen static fixed point = no per-stimulus variation = the
    #   §11-B "step~800 freeze" signature).  ALL THREE must vary.
    psi_std = float(psi_arr.std())
    tension_std = float(tension_arr.std())
    phi_std = float(phi_arr.std())
    physics_not_frozen = bool(psi_std > TAU_FROZEN and
                              tension_std > TAU_FROZEN and
                              phi_std > TAU_FROZEN)

    # ── honest_§9_coherent — §9 SSOT metric on the emitted symbol stream.
    #   The cell's gen_symbols are mapped to a printable string (mod into
    #   the ASCII printable range) and the §9 cascade-rate gate is applied.
    #   §9 is NECESSARY-not-sufficient (B-EMERGE-7) — a degeneracy/cascade
    #   detector, NOT a coherence proof.  We score 5 windows (≥1/5 gate).
    gen_str_full = "".join(chr(33 + (sym % 94)) for sym in gen_symbols)
    n_windows = 5
    wlen = max(20, len(gen_str_full) // n_windows)
    coherent_count = 0
    window_details = []
    for w in range(n_windows):
        seg = gen_str_full[w * wlen:(w + 1) * wlen]
        ok, det = honest_coherent(seg)
        if ok:
            coherent_count += 1
        window_details.append({"window": w, "honest_coherent": bool(ok),
                                "len": len(seg),
                                "cascade_rate": det["cascade_rate"],
                                "max_run": det["max_run"]})
    s9_coherent_ratio = coherent_count / n_windows
    s9_pass = s9_coherent_ratio >= (1.0 / 5.0)

    # ── §3 PRE-REGISTERED CLOSED PREDICATE — verbatim ────────────────
    #   NON_DEGENERATE := byte_acc > 1/256 ∧ physics_not_frozen
    #                     ∧ honest_§9_coherent ≥ 1/5
    byte_acc_pass = byte_acc > CHANCE
    non_degenerate = bool(byte_acc_pass and physics_not_frozen and s9_pass)

    total_steps = n_stim * steps_per_stim
    overall_rate = spike_total / (total_steps * N)
    # weight_drift = recurrent-W movement (STDP channel updates W);
    # head_drift   = readout-head movement (CE channel updates the HEAD,
    # NOT W).  BOTH are recorded so each channel's learning is visible:
    # a CE cell has head_drift>0 / weight_drift=0; a STDP cell has
    # weight_drift>0 / head_drift=0; a 'none' cell has both 0.  Reading
    # weight_drift alone would falsely look like "CE did nothing" — the
    # CE channel learns the readout head, which is its whole job here.
    w_drift = float(np.abs(cell.W - cell.W0).mean())
    head_drift = float(np.abs(cell.head - cell.head0).mean())

    return {
        "cell": label, "channel": channel,
        "N": N, "n_a": cell.n_a, "n_g": cell.n_g, "n_rec": cell.n_rec,
        "n_stim": n_stim, "steps_per_stim": steps_per_stim,
        "byte_acc": round(byte_acc, 6),
        "byte_acc_chance": round(CHANCE, 6),
        "byte_acc_pass_gt_chance": bool(byte_acc_pass),
        "psi_c1_mean": round(float(psi_arr.mean()), 6),
        "psi_c1_std": psi_std,
        "tension_std": tension_std,
        "phi_std": phi_std,
        "physics_not_frozen": physics_not_frozen,
        "s9_coherent_count": coherent_count,
        "s9_coherent_ratio": s9_coherent_ratio,
        "s9_pass_ge_1_5": bool(s9_pass),
        "s9_window_details": window_details,
        "non_degenerate": non_degenerate,
        "weight_drift_mean_abs": round(w_drift, 8),
        "head_drift_mean_abs": round(head_drift, 8),
        "overall_spike_rate_per_unit_step": round(overall_rate, 6),
    }


def run(out_dir):
    t0 = time.time()
    # ── 4 cells — only the weight-update channel varies ──────────────
    cells = {
        "GPU-CE":        run_cell("ce",   "GPU-CE"),
        "GPU-noCE":      run_cell("none", "GPU-noCE"),
        "SIM-noCE-STDP": run_cell("stdp", "SIM-noCE-STDP"),
        "SIM-CE":        run_cell("ce",   "SIM-CE"),
    }
    wall = time.time() - t0

    nd = {k: v["non_degenerate"] for k, v in cells.items()}

    # ── §3 3-OUTCOME VERDICT PARTITION (pre-registered, verbatim) ─────
    sim_stdp_nd = nd["SIM-noCE-STDP"]
    gpu_noce_degen = not nd["GPU-noCE"]
    sim_ce_nd = nd["SIM-CE"]              # VOID guard
    gpu_ce_nd = nd["GPU-CE"]             # sanity control

    if not sim_ce_nd:
        verdict = "VOID"
        verdict_note = (
            "SIM-CE positive-control guard is DEGENERATE — the rig itself "
            "is broken, NO verdict on the learning-channel question. (§3 "
            "VOID branch.)")
    elif sim_stdp_nd and gpu_noce_degen and sim_ce_nd:
        verdict = "SIM-CONFRONTS-LEARNING-CHANNEL"
        verdict_note = (
            "NON_DEGENERATE(SIM-noCE-STDP)=True AND GPU-noCE DEGENERATE AND "
            "SIM-CE guard non-degenerate: the §11-B blocker, at the "
            "learning-channel level, was the CE-ONLY channel — an "
            "event-local-plasticity (STDP) channel escapes degeneracy even "
            "in a clocked sim.  PARTIALLY REFINES §115's blanket "
            "SIM-IS-GPU-TAUTOLOGY (splits it: learning-half confrontable, "
            "async-half NOT).  STRICTLY: this is the LEARNING-CHANNEL HALF "
            "only — the async-substrate half stays WALL-B (Loihi/SpiNNaker-"
            "gated, §117 INHERITED), and §96 design-open #1 (softmax "
            "attention SPIKING-INCOMPATIBLE → must be REPLACED) BLOCKS the "
            "full spiking-anima instantiation.  NOT GOAL emergence; NOT a "
            "WALL-A (§1.1 data-regime) escape; toy non-degeneracy = "
            "substrate LIVENESS, NOT capability (B-EMERGE-7).")
    else:
        verdict = "SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF"
        verdict_note = (
            "NON_DEGENERATE(SIM-noCE-STDP)=False: consistent with §11-B "
            "being substrate-independent OR an attention-replacement / sim "
            "artifact — CANNOT disambiguate without async hardware.  This "
            "is §115's predicted outcome, now SCOPED to the learning-"
            "channel half only.  WALL-B (§96-physical) + §96 design-open "
            "#1 (attention replacement) remain; GOAL not reached.")

    headline = (
        "§96 design-open #1 — softmax(QK^T) self-attention is "
        "SPIKING-INCOMPATIBLE (§96 Q1): it must be REPLACED, not ported "
        "(phase-resonance / spike-rate dot-product + k-WTA — undecided). "
        "This 4-cell rig confronts the §11-B LEARNING-CHANNEL HALF ONLY. "
        "The full spiking-anima instantiation stays GATED on the "
        "attention-replacement design-open (TRACK0_INSILICO.md §4 / Phase "
        "2 = blocking design-open). The async-substrate half stays WALL-B "
        "(Loihi/SpiNNaker-gated, §117 INHERITED). Toy non-degeneracy = "
        "substrate LIVENESS, NOT capability, NOT GOAL.")

    result = {
        "section": "§118", "title": "Track 0 in-silico — §96 §4.5 cells",
        "cost_usd": 0.0, "gpu": False, "runpod": False, "fire": False,
        "model_forward_byte_lm": False, "corpus": False, "dispatch": False,
        "orphan": 0, "wall_sec": round(wall, 4),
        "seed": SEED, "base_ckpt": BASE_CKPT,
        "tau_frozen": TAU_FROZEN, "byte_acc_chance": CHANCE,
        "predicate": "NON_DEGENERATE(cell) := byte_acc > 1/256 "
                     "AND physics_not_frozen (Psi/tension/Phi std > tau) "
                     "AND honest_§9_coherent >= 1/5",
        "s9_metric_source": "state/verify_emergence_metric_2026_05_18/"
                            "emergence_metric.py :: honest_coherent (SSOT "
                            "import, NOT re-implemented)",
        "cells": cells,
        "non_degenerate_by_cell": nd,
        "verdict": verdict,
        "verdict_note": verdict_note,
        "headline": headline,
        "honest_inheritance": {
            "wall_b": "INHERITED — §117 LEGO-RUN-...-WALL-B-INHERITED + "
                "§115 LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY + §95 Loihi-"
                "sole-VIABLE. Track 0 confronts the LEARNING-CHANNEL half "
                "ONLY; the async-substrate half is structurally "
                "unreachable in a clocked CPU/GPU sim.",
            "wall_a": "ORTHOGONAL & UNTOUCHED — §1.1 data-regime; a toy "
                "spike sim moves no data threshold (§97).",
            "attention_blocker": "§96 design-open #1 — softmax(QK^T) "
                "self-attention SPIKING-INCOMPATIBLE; must be REPLACED. "
                "The full spiking-anima instantiation is BLOCKED on this "
                "design-open — Track 0 confronts the learning channel, "
                "NOT the full anima.",
            "psi_7_form": "§7-FORM TRUE BY CONSTRUCTION (§112 META_FP(Π_½) "
                "instance, carrier = spike-correlation); NOT manufactured "
                "by §118.",
            "g3": "design ≠ fire ≠ emergence; capability claim 0; "
                "necessary-not-sufficient at every layer (B-EMERGE-7). "
                "north-star + §15/§51/§72 milestones UNCHANGED, GOAL "
                "미도달.",
        },
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"§118 TRACK 0 IN-SILICO  wall={wall:.3f}s")
    for k, v in cells.items():
        print(f"  {k:14s} ch={v['channel']:5s} "
              f"byte_acc={v['byte_acc']:.4f}(>{CHANCE:.4f}={v['byte_acc_pass_gt_chance']}) "
              f"phys_not_frozen={v['physics_not_frozen']} "
              f"§9={v['s9_coherent_count']}/5 "
              f"→ NON_DEGEN={v['non_degenerate']}")
    print(f"  VERDICT = {verdict}")
    return result


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    run(out)
