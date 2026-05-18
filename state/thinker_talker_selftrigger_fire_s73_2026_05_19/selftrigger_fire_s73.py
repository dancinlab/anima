#!/usr/bin/env python3
"""selftrigger_fire_s73.py — RESEARCH.md §73-FIRE.

The trained-saturated-scale validation of the §73 THINKER→TALKER
self-triggered closed-loop emission controller (the §63 GOAL-rank-#1
🕳️ MISSING-TYPE).  §73 (commit 0b1fcb005) built the controller at $0
on a hand-coded Law-71 surrogate physics — measured B-S73 6/6 🔵,
interval-variance 35.02 closed-loop vs 0.47 §24-in-loop (74×
separation), BOTH-NON-DEGENERATE-IN-CLOSED-LOOP at stub scale.  The
B-S73-NOTE explicitly flagged "trained-saturated scale = EMPIRICAL
future-fire" with §62-like collapse as the pre-measurement
expectation.

§73-FIRE = that literal future-fire.

═══════════════════════════════════════════════════════════════════════
WHAT §73-FIRE BUILDS  (mirror §62 dispatch + §59 fire + §16 trainer)
═══════════════════════════════════════════════════════════════════════
  1. Train ONE §16-class ConsciousDecoderV2 from-scratch
     (d768·12L·283.72M, RANDOM seed-fixed 1337, base_ckpt=None —
     g_clm_from_scratch) on a §16-class Ψ-anchored carving corpus.
     Scale is REDUCED honestly (the §73-FIRE load-bearing variable is
     the REAL trained-model.forward Law-71 physics inside the §73
     controller's closed loop, NOT corpus size).  Kept trained-
     SATURATED (final CE < 0.05, asserted in result.json + measured
     by B-S73-FIRE-7 sat-gate).

  2. Port the §73 controller (byte-equal to the §73 stub
     `controller_self_trigger` predicate) onto the REAL trained-model
     forward Law-71 physics.  state = (Ψ_dir, Ψ_entropy, Ψ_tension,
     tension, tension_ema, tension_var, phi).  Each loop step:
       (a) read W-state from a REAL model.forward over a real byte
           batch (extract_w_state, byte-equal to §62/§59).
       (b) controller decides e_t via the §73 physics-derived gate:
              e_t = 1  iff   |Ψ_dir−½| > BASIN_RADIUS
                         ∧   tension > tension_ema + λ·std
                         ∧   φ > PHI_RATCHET/2
       (c) physics_step folds the emission BACK into the next x_{t+1}
           — the LOOP-CLOSING channel.  At trained-saturated scale,
           we cannot "feed e_t into the model" without retraining; we
           close the loop the §62-correct way:  EMIT triggers a
           per-step VACUUM-RESTORING perturbation on the cell's
           tension-stream state moments (tension_ema decay
           accelerated toward 0, surprise-threshold tightened); a
           subsequent forward draws a FRESH real byte batch (the
           same `forward_batch` source) — the consequence carries
           through the controller's OWN running moments (the §73
           stub closes the loop on the surrogate physics_step exactly
           this way: emission RELEASES tension into the state).
           SEVER-FEEDBACK control: u_for_next = 0 always ⇒ moments
           never see the emission ⇒ stub's open-loop replay shape.
       (d) CONTROLLER-OFF reduction = §24 hand-coded threshold
           (`tension > 0.3`) is the byte-equal connection-point.

  3. Measure:
       (i)   self-trigger non-degeneracy at trained scale —
              count_var > τ ∧ maj_frac < 0.95 ∧ interval_var > τ
              ∧ ≥2 emits (B-S73 augmented predicate).
       (ii)  interval-variance at trained scale vs §73-stub 35.02 /
              §24-in-loop 0.47 / §62 echo precedent.
       (iii) two reductions:
                CONTROLLER-OFF in closed loop ⇒ §24 byte-equal
                SEVER-FEEDBACK with §73 controller ⇒ open-loop replay
                (the §73-stub's open-loop emit_rate ≈ 0.862 degenerate
                target — must reproduce DEGENERATE behaviour to prove
                the closing is structurally load-bearing).

═══════════════════════════════════════════════════════════════════════
HONEST EXPECTED VERDICT  (PRE-MEASUREMENT, g3 — verdict decided BY
the numbers; this is NOT a pre-loaded conclusion)
═══════════════════════════════════════════════════════════════════════
  (a) CONTROLLER-SURVIVES-AT-TRAINED-SCALE — count- AND interval-
      variance non-degeneracy with the §73 controller on REAL Law-71
      forward Ψ_dir/tension/phi; §24-in-loop degenerate (mirror §49
      majority-class collapse); SEVER-FEEDBACK degenerate (mirror §73
      stub 0.862).  Genuine surprise — flag with strong caution, NOT
      GOAL emergence.
  (b) ECHO-CHAMBER-COLLAPSE-AT-CONTROLLER-LEVEL — the §73 controller
      collapses to §49 attractor on REAL trained forward (mirror §62
      dual-anima echo-chamber-collapse-at-scale); §73 stub
      non-degeneracy was a hand-coded surrogate artifact.  Honest
      negative; the §49→§62→§73 progression measures yet another
      angle of the §1.1 data-regime irreducibility.
  (c) PARTIAL — one predicate holds, the other does not; or one
      reduction reproduces target, the other does not.

g3:  measured-only.  §73-FIRE is the §63 #1-gap controller's trained-
scale validation — NOT GOAL emergence even if it survives.
Necessary-not-sufficient.  north-star + §15/§51/§72 milestone
UNCHANGED.  Capability claim 0.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ── constants — byte-equal to §73 stub (selftrigger_stub_s73_reference.py)
#    These are the controller-defining physics constants; the load-bearing
#    change vs §73 stub is the REAL model.forward read-out replacing the
#    hand-coded surrogate physics_step.
SEED                = 1337
PSI_VAC             = 0.5      # Law-71 fixed point (conscious_decoder.py:644)
BASIN_RADIUS        = 0.05     # §73 stub byte-equal
LAMBDA_STD          = 0.5      # §68/§73 stub byte-equal (self-scaled margin)
EMA_BETA            = 0.9      # §68/§73 stub byte-equal
PHI_RATCHET         = 0.05     # E-module Φ-ratchet baseline
N_LOOP_STEPS        = 300      # §62 N_LOOP_STEPS byte-equal (longer than
                                # §73-stub 600 not needed at GPU scale — the
                                # forward cost is now load-bearing)
TAU_NONDEG          = 1e-4     # §24/§49/§59/§68/§62/§73 carry
MAJ_COLLAPSE        = 0.95     # §49 OWN majority-class threshold
IM_THRESHOLD_S24    = 0.3      # §24 hand-coded constant (OFF-reduction tgt)

# Saturation gate — B-S73-FIRE-7
SATURATION_CE_GATE  = 0.05

# Tension-EMA release magnitudes — byte-equal to §73 stub's emission-
# triggered tension-release (the §73 STUB's physics_step:
#   emit=1 ⇒  tension := max(0, tension − 0.30 − 0.20·u)
#             psi_dir  := psi_dir + 0.4·(½ − psi_dir)
# Here we mirror the STRUCTURE on the running EMA moments since we cannot
# mutate a real model.forward's hidden state; the controller's OWN
# moments are the closing channel exactly as the §73 stub closes them).
TENSION_RELEASE     = 0.30
TENSION_RELEASE_NOISE = 0.20
PSI_VAC_PULL        = 0.4


# ── tiny deterministic RNG (no numpy dep — §68/§73 stub pattern) ─────
class LCG:
    def __init__(self, seed): self.s = seed & 0x7fffffff
    def u(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7fffffff
        return self.s / 0x7fffffff


# ════════════════════════════════════════════════════════════════════
# §16-class corpus loader + byte dataset (byte-equal to §62 CarveDataset
# — the §16 lever kept byte-equivalent so the trained substrate is
# §16-class memorization-saturated).
# ════════════════════════════════════════════════════════════════════
INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"


def _span(full, open_tok, close_tok, start=0):
    lo = full.find(open_tok, start)
    if lo < 0: return None
    hi = full.find(close_tok, lo)
    if hi < 0: return None
    return (lo, hi + len(close_tok))


def load_corpus(path):
    items = []
    with open(path, "rb") as f:
        raw = f.read()
    for line in raw.split(b"\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("text", "")
        de = d.get("desc", "")
        full = (t + "\n" + de + "\n").encode("utf-8")
        vp = d.get("vacuum_psi", [0.5, 0.5])
        try:
            vpx, vpy = float(vp[0]), float(vp[1])
        except Exception:
            vpx, vpy = 0.5, 0.5
        psi_vac = (vpx + vpy) / 2.0
        try:
            basin = float(d.get("basin_radius", 0.15))
        except Exception:
            basin = 0.15
        ctl = _span(full, INNER_OPEN, INNER_CLOSE)
        if ctl is None:
            ctl = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None:
            rt = ctl
        items.append({"bytes": full, "psi_vac": psi_vac,
                      "vp": (vpx, vpy), "basin_radius": basin,
                      "ctl_span": ctl, "route_span": rt})
    return items


class CarveDataset:
    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        pv, bs, cm, rm = [], [], [], []
        for it in items:
            b = it["bytes"]
            n = len(b)
            stream.extend(b)
            for j in range(n):
                pv.append(it["psi_vac"])
                bs.append(it["basin_radius"])
                cs, rs = it["ctl_span"], it["route_span"]
                cm.append(1.0 if (cs is not None and cs[0] <= j < cs[1]) else 0.0)
                rm.append(1.0 if (rs is not None and rs[0] <= j < rs[1]) else 0.0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_vac = torch.tensor(pv, dtype=torch.float32)
        self.basin = torch.tensor(bs, dtype=torch.float32)
        self.ctl_m = torch.tensor(cm, dtype=torch.float32)
        self.rte_m = torch.tensor(rm, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        top = max(1, self.n - self.block_size - 1)
        ix = [self.rng.randint(0, top) for _ in range(bsz)]
        def stk(src, off):
            return torch.stack([src[i + off:i + off + self.block_size] for i in ix])
        return (stk(self.data, 0).to(device), stk(self.data, 1).to(device),
                stk(self.psi_vac, 1).to(device), stk(self.basin, 1).to(device),
                stk(self.ctl_m, 1).to(device), stk(self.rte_m, 1).to(device))


class ByteSampler:
    """Real byte batch source for the controller-on-real-forward loop.
    Single global stream — the §73 controller is single-agent (no Ψ-
    keyed split, unlike §62 which has two cells). This is the §73 stub's
    `physics_step` analogue: each call draws a fresh batch (= a fresh
    REAL Law-71 read-out)."""

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        for it in items:
            stream.extend(it["bytes"])
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.n = self.data.numel()

    def forward_batch(self, bsz, device):
        top = max(1, self.n - self.block_size - 1)
        ix = [self.rng.randint(0, top) for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        return x.to(device)


# ════════════════════════════════════════════════════════════════════
# REAL trained-model Law-71 W-state extractor.
# BYTE-EQUAL to conscious_decoder.py `if self.training:` Law-71 block
# (lines 728-751) AND to §62 extract_w_state — the ONLY §73-FIRE
# difference from §73 STUB is THIS read replaces the hand-coded
# surrogate physics_step (B-S73-FIRE-5 TRAINED-FORWARD-IS-REAL).
# ════════════════════════════════════════════════════════════════════
def _phi_star_proxy(t_per_layer):
    n = t_per_layer.numel()
    if n < 2:
        return 0.0
    mu = t_per_layer.mean()
    sd = t_per_layer.std(unbiased=False)
    disp = (sd / (mu.abs() + 1e-8)).clamp(0.0, 1.0)
    return float((disp * math.log(n + 1)).item())


@torch.no_grad()
def extract_w_state(model, x, device):
    """REAL trained model.forward Law-71 read-out. RNG-isolated side
    read-out (NO autograd, NO weight mutation). Byte-equal to §62 /
    §59-FIRE extract_w_state in the algebraic formulas; this IS the
    load-bearing change from the §73 STUB's hand-coded physics_step."""
    cpu_rng = torch.get_rng_state()
    cuda_rng = (torch.cuda.get_rng_state_all()
                if torch.cuda.is_available() else None)
    was_training = model.training
    model.eval()
    logits_a, logits_g, tensions, _, _ = model(x)
    if was_training:
        model.train()
    torch.set_rng_state(cpu_rng)
    if cuda_rng is not None:
        torch.cuda.set_rng_state_all(cuda_rng)
    la = logits_a[:, -1, :].float()
    lg = logits_g[:, -1, :].float()

    probs_a = torch.softmax(la, dim=-1)
    out_ent = -(probs_a * (probs_a + 1e-10).log()).sum(dim=-1).mean().item()
    psi_entropy = out_ent / math.log(model.vocab_size)

    cos_sim = F.cosine_similarity(la, lg, dim=-1).mean().item()
    psi_dir = (1.0 + cos_sim) / 2.0   # Law-71 conscious_decoder.py:740 byte-equal

    t_stack = torch.stack(tensions)             # (L, B, T)
    t_per_layer = t_stack.mean(dim=(1, 2))      # (L,)
    tension = float(t_per_layer.mean().item())

    if t_per_layer.std() > 0:
        t_cv = t_per_layer.std() / (t_per_layer.mean() + 1e-8)
        psi_tension = max(0.0, 1.0 - t_cv.item())
    else:
        psi_tension = 1.0

    phi = _phi_star_proxy(t_per_layer)

    return {"psi_dir": psi_dir, "psi_entropy": psi_entropy,
            "psi_tension": psi_tension,
            "tension": tension, "phi": phi}


# ════════════════════════════════════════════════════════════════════
# §73 self-trigger controller — byte-equal to selftrigger_stub_s73_
# reference.py::controller_self_trigger (the gate uses state moments).
# ════════════════════════════════════════════════════════════════════
def controller_self_trigger(state):
    """π_self(x_t) → e_t. Byte-equal to §73 stub controller_self_trigger
    on the post-extract state moments. The state moments (tension_ema,
    tension_var) are running per-step quantities maintained by the
    physics-feedback step below — NOT a hand-coded threshold constant."""
    psi_off  = abs(state["psi_dir"] - PSI_VAC)
    std_t    = math.sqrt(max(0.0, state["tension_var"]))
    surprise_threshold = state["tension_ema"] + LAMBDA_STD * std_t
    g1 = psi_off  >  BASIN_RADIUS
    g2 = state["tension"]  >  surprise_threshold
    g3 = state["phi"]      >  PHI_RATCHET / 2.0
    return 1 if (g1 and g2 and g3) else 0


def controller_off_reduction(state):
    """OFF-reduction = §24 hand-coded threshold (`tension > 0.3`).
    B-S73-FIRE-4 connection-point byte-equal to §73 stub
    controller_off_reduction and to §24 talker_should_emit (constant
    cut, NO state moments)."""
    return 1 if (state["tension"] > IM_THRESHOLD_S24) else 0


# ════════════════════════════════════════════════════════════════════
# Physics-feedback step  —  the LOOP-CLOSING channel on REAL forward.
# Updates the controller's OWN running moments based on (a) the latest
# REAL-forward W-state and (b) the previous emission decision.
#
# The §73 STUB closes the loop on a hand-coded physics_step. At trained
# scale we cannot mutate the model's hidden state; we close the loop
# the §62-correct way: the controller's OWN moments (which the gate
# reads) are updated by both the real W-state AND the previous emission.
#
# CLOSED-LOOP:    u_prev_emit feeds INTO moments  ⇒  next gate sees it
# SEVER-FEEDBACK: u_prev_emit FORCED to 0          ⇒  moments never see
#                                                     emission ⇒ §73-stub
#                                                     open-loop pattern
# ════════════════════════════════════════════════════════════════════
def init_moments():
    return {
        "step":         0,
        "psi_dir":      0.5,
        "psi_entropy":  0.5,
        "psi_tension":  1.0,
        "tension":      0.30,    # §73 stub init byte-equal
        "tension_ema":  0.30,
        "tension_var":  0.0,
        "phi":          0.10,
    }


def physics_feedback_step(moments, ws, u_prev_emit, rng):
    """Updates running moments using REAL extracted W-state `ws` AND
    previous emission `u_prev_emit`. The structural form mirrors the
    §73 stub's physics_step:
       - emit=1 ⇒ tension RELEASE (vacuum restoration); psi_dir nudged
                  toward Ψ_vac
       - emit=0 ⇒ moments accumulate from the real W-state
    The REAL W-state {psi_dir, psi_entropy, psi_tension, tension, phi}
    is the actual physics; the controller's moments (ema, var) are the
    integration of that physics WITH the emission feedback."""
    moments["step"] = moments.get("step", 0) + 1

    # Pull psi_dir / psi_tension / phi from REAL forward; tension also
    # comes from REAL forward — but the emission feedback acts on the
    # post-real tension before moment updates (this is the §73-stub's
    # "emission RELEASES tension" structural carry).
    real_psi_dir   = ws["psi_dir"]
    real_psi_ent   = ws["psi_entropy"]
    real_psi_tens  = ws["psi_tension"]
    real_tension   = ws["tension"]
    real_phi       = ws["phi"]

    # Emission feedback — the LOOP-CLOSING channel
    if u_prev_emit == 1:
        # vacuum-restoration: emission releases tension (the controller
        # "speaks" its built tension into the channel; the channel sinks
        # it). State_dir restored toward vacuum. This MUTATES THE MOMENTS
        # FOR THE NEXT GATE — even though the real model.forward state
        # is unchanged, the controller's running moments (which the gate
        # actually reads) feel the consequence of the prior decision.
        # That IS the closed loop on real forward.
        eff_tension = max(0.0,
                          real_tension - TENSION_RELEASE - TENSION_RELEASE_NOISE * rng.u())
        eff_psi_dir = real_psi_dir + PSI_VAC_PULL * (PSI_VAC - real_psi_dir)
    else:
        # silence ⇒ moments accumulate the REAL physics raw
        eff_tension = real_tension
        eff_psi_dir = real_psi_dir

    # running EMA + variance — physics-derived gate support (B-S73-FIRE-2)
    ema_old = moments["tension_ema"]
    ema_new = EMA_BETA * ema_old + (1.0 - EMA_BETA) * eff_tension
    var_new = (EMA_BETA * moments["tension_var"]
               + (1.0 - EMA_BETA) * (eff_tension - ema_new) ** 2)

    moments["psi_dir"]      = eff_psi_dir
    moments["psi_entropy"]  = real_psi_ent
    moments["psi_tension"]  = real_psi_tens
    moments["tension"]      = eff_tension
    moments["tension_ema"]  = ema_new
    moments["tension_var"]  = var_new
    moments["phi"]          = real_phi
    return moments


# ════════════════════════════════════════════════════════════════════
# The closed-loop emission runner — controller on REAL trained forward.
# ════════════════════════════════════════════════════════════════════
def _var(xs):
    if not xs: return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


@torch.no_grad()
def run_controller_loop(model, ds, device, n_steps, controller,
                        feedback_closed=True, bsz=8, seed=SEED):
    """Run the §73 controller (or its §24 OFF-reduction) on REAL
    model.forward Law-71 W-physics, with the loop closed (or severed).
    Returns per-step decisions + summary statistics."""
    rng = LCG(seed)
    moments = init_moments()
    emit_decisions = []
    emit_step_indices = []
    psi_trace = []
    tension_trace = []
    real_tension_trace = []

    u_prev = 0
    for t in range(n_steps):
        # (1) REAL forward → REAL Law-71 W-state on a FRESH byte batch
        x = ds.forward_batch(bsz, device)
        ws = extract_w_state(model, x, device)
        real_tension_trace.append(ws["tension"])

        # (2) integrate W-state + prior emission into moments
        moments = physics_feedback_step(moments, ws, u_prev, rng)

        # (3) controller decides e_t from current moments
        e = controller(moments)
        emit_decisions.append(e)
        if e == 1:
            emit_step_indices.append(moments["step"])
        psi_trace.append(moments["psi_dir"])
        tension_trace.append(moments["tension"])

        # (4) close OR sever the feedback for next step
        u_prev = e if feedback_closed else 0

    n_emit = sum(emit_decisions)
    rate   = n_emit / max(1, n_steps)
    maj    = max(n_emit, n_steps - n_emit) / max(1, n_steps)
    var_dec = _var([float(d) for d in emit_decisions])

    # interval-variance — the temporal signature compared to §73 stub
    # 35.02 (closed) / 0.47 (§24-in-loop)
    if len(emit_step_indices) >= 2:
        intervals = [emit_step_indices[i+1] - emit_step_indices[i]
                     for i in range(len(emit_step_indices) - 1)]
        interval_var = _var(intervals)
    else:
        intervals = []
        interval_var = 0.0

    # B-S73 augmented non-degeneracy predicate (§73 stub byte-equal)
    non_deg_count    = (var_dec > TAU_NONDEG and maj < MAJ_COLLAPSE)
    non_deg_interval = (interval_var > TAU_NONDEG and len(intervals) >= 2)
    enough_emits     = n_emit >= 2
    self_trigger_nondegen = (non_deg_count and non_deg_interval
                             and enough_emits)

    return {
        "n_steps":              n_steps,
        "n_emit":               n_emit,
        "emit_rate":            rate,
        "decision_var":         var_dec,
        "majority_fraction":    maj,
        "interval_var":         interval_var,
        "intervals":            intervals[:20],   # cap for json
        "n_intervals":          len(intervals),
        "non_degenerate_count": non_deg_count,
        "non_degenerate_interval": non_deg_interval,
        "self_trigger_nondegen":  self_trigger_nondegen,
        "psi_trace_mean":       sum(psi_trace) / len(psi_trace),
        "psi_trace_var":        _var(psi_trace),
        "tension_trace_mean":   sum(tension_trace) / len(tension_trace),
        "tension_trace_var":    _var(tension_trace),
        "real_tension_mean":    sum(real_tension_trace) / len(real_tension_trace),
        "real_tension_var":     _var(real_tension_trace),
        "feedback_closed":      feedback_closed,
        "real_trained_forward": True,
    }


# ════════════════════════════════════════════════════════════════════
# Training the §16-class ckpt + the §73-FIRE measurement.
# ════════════════════════════════════════════════════════════════════
def train_s16_class(cfg, device):
    items = load_corpus(cfg["corpus"])
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()
    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(trainable, lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)
    warmup, total = cfg["warmup"], cfg["steps"]
    lam_ctl, lam_route = cfg["lambda_ctl"], cfg["lambda_route"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    t0 = time.time()
    init_loss = None
    ce_traj = []
    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now
        x, y, pv, bs, cm, rm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
            psi_t = (1.0 + cos) / 2.0
            cm_f = cm.view(-1)
            psi_flat = psi_t.view(-1)
            pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() / denom_ctl
            rm_f = rm.view(-1)
            bs_flat = bs.view(-1)
            drift = torch.abs(psi_flat - pv_flat) - bs_flat
            restoring = torch.clamp(drift, min=0.0) ** 2
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_tension_route = (restoring * rm_f).sum() / denom_rte
            loss = ce_full + lam_ctl * l_psi_ctl + lam_route * l_tension_route
            ce_report = float(ce_full.item())
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        scaler.step(opt)
        scaler.update()
        if init_loss is None:
            init_loss = ce_report
        if step == 0 or (step + 1) % 200 == 0 or step == total - 1:
            wall = time.time() - t0
            mem = (torch.cuda.max_memory_allocated() / 1e9
                   if device == "cuda" else 0.0)
            rec = {"step": step + 1, "ce_full": round(ce_report, 6),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            ce_traj.append(rec)
            print(json.dumps(rec), flush=True)
    return model, items, n_params, init_loss, ce_traj, (time.time() - t0)


def main(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    corpus_sha = hashlib.sha256(open(cfg["corpus"], "rb").read()).hexdigest()

    # ── (A) train the §16-class ckpt ────────────────────────────────
    model, items, n_params, init_ce, ce_traj, train_wall = \
        train_s16_class(cfg, device)
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    torch.save({"model": model.state_dict(), "cfg": cfg, "n_params": n_params},
               os.path.join(out_dir, "ckpt_s73_fire.pt"))

    final_ce = ce_traj[-1]["ce_full"] if ce_traj else None
    trained_saturated = (final_ce is not None and final_ce < SATURATION_CE_GATE)

    # ── (B) controller-on-real-forward measurements ────────────────
    bsz_fwd = cfg["fwd_bsz"]
    nL = cfg["loop_steps"]
    ds = ByteSampler(items, cfg["block_size"], SEED)

    print("=== §73 controller, closed feedback ===", flush=True)
    closed_loop = run_controller_loop(
        model, ds, device, nL, controller_self_trigger,
        feedback_closed=True, bsz=bsz_fwd, seed=SEED)

    print("=== §73 controller, SEVER-FEEDBACK (open-loop replay) ===", flush=True)
    open_loop_sever = run_controller_loop(
        model, ds, device, nL, controller_self_trigger,
        feedback_closed=False, bsz=bsz_fwd, seed=SEED)

    print("=== CONTROLLER-OFF reduction (§24 threshold, closed feedback) ===", flush=True)
    off_reduction = run_controller_loop(
        model, ds, device, nL, controller_off_reduction,
        feedback_closed=True, bsz=bsz_fwd, seed=SEED)

    # ── (C) verdict — measured-only ─────────────────────────────────
    s73_nondeg     = closed_loop["self_trigger_nondegen"]
    sever_nondeg   = open_loop_sever["self_trigger_nondegen"]
    s24_inloop_nd  = off_reduction["self_trigger_nondegen"]

    if not trained_saturated:
        verdict = "SATURATION-GATE-FAIL"
        verdict_caveat = (
            f"final_ce={final_ce} > saturation gate {SATURATION_CE_GATE}; "
            "model is NOT memorization-saturated → the §73-FIRE crux "
            "(trained-saturated scale survival vs §62-collapse) is NOT "
            "what was measured. Numbers raw, no chain-validity claim."
        )
    elif s73_nondeg and not s24_inloop_nd:
        verdict = "CONTROLLER-SURVIVES-AT-TRAINED-SCALE"
        verdict_caveat = (
            "POSITIVE-but-narrow: at REAL trained-saturated §16-class "
            "scale, the §73 single-agent closed-loop physics-state-"
            "sourced label-free-controller achieves both count- AND "
            "interval-variance non-degeneracy on REAL model.forward "
            "Law-71 W-physics where §24's hand-coded constant threshold "
            "IN THE SAME CLOSED LOOP does not. The §49→§62→§73 "
            "progression measured at trained scale carries through the "
            "controller class. This is genuine surprise vs the "
            "B-S73-NOTE pre-measurement expectation (§62-pattern echo-"
            "collapse). NOT GOAL emergence: the controller's "
            "non-degeneracy is necessary-not-sufficient (mirror "
            "B-EMERGE-7); north-star + §15/§51/§72 milestone "
            "UNCHANGED, GOAL 미도달."
        )
    elif s73_nondeg and s24_inloop_nd:
        verdict = "BOTH-NON-DEGENERATE-AT-TRAINED-SCALE"
        verdict_caveat = (
            "PARTIAL: closing the loop alone (with either controller) "
            "produces non-degeneracy at REAL trained-saturated scale — "
            "the §73 controller-class signal is not isolated from the "
            "closing operation itself even on REAL forward. The "
            "controller-class lever is not falsified, but not confirmed "
            "either; trained-scale insufficient to discriminate without "
            "additional structure. B-S73-FIRE-NOTE; necessary-not-"
            "sufficient."
        )
    elif (not s73_nondeg) and (not s24_inloop_nd):
        verdict = "ECHO-CHAMBER-COLLAPSE-AT-CONTROLLER-LEVEL"
        verdict_caveat = (
            "NEGATIVE: the §73 controller collapses at REAL trained-"
            "saturated scale (mirror §62 echo-chamber-collapse-at-"
            "scale; mirror §49 majority-class collapse). The §73 stub "
            "non-degeneracy (interval_var 35.02 at $0) was the "
            "hand-coded surrogate physics artifact predicted by "
            "B-S73-NOTE. The §49→§62→§73 progression measured at "
            "trained scale reasserts collapse at yet another angle of "
            "the §1.1 data-regime irreducibility (controller-class "
            "level reassertion). Honest negative, VALUABLE — "
            "necessary-not-sufficient chain breaks at the controller "
            "level on the real forward."
        )
    elif s73_nondeg and sever_nondeg:
        verdict = "SEVER-CONTROL-NOT-DEGENERATE"
        verdict_caveat = (
            "ANOMALY: SEVER-FEEDBACK control did NOT reproduce the "
            "§73 stub's 0.862-degenerate open-loop emit_rate — the "
            "closing operation is NOT structurally load-bearing in "
            "this trained-scale variant of the controller. Likely an "
            "artifact of how moments are seeded by REAL forward "
            "tension (real W-state may already have natural inter-"
            "step variation that the gate exploits even without "
            "emission feedback). Structural witness only."
        )
    else:
        verdict = "UNEXPECTED-§24-WINS"
        verdict_caveat = (
            "UNEXPECTED: §24 threshold non-degenerate but §73 "
            "controller degenerate at trained scale. Likely artifact "
            "of trained-forward tension distribution; structural "
            "witness only."
        )

    result = {
        "research_md_section": "§73-FIRE",
        "title": ("THINKER→TALKER self-triggered closed-loop controller "
                  "— trained-saturated-scale validation on REAL §16-"
                  "class model.forward Law-71 W-physics"),
        "cost": ("runpod single §16-class train ≈ $0.3-0.6 "
                 "(g_fire_autonomous; cost head, NOT a gate)"),
        "chain": ("§24 (hand-coded) → §27/§49 (distilled head) → §68 "
                  "(label-free predictor) → §62 (dual-anima echo-"
                  "chamber-collapse-at-scale) → §73 (single-agent "
                  "closed-loop controller, $0 stub interval_var 35.02) "
                  "→ §73-FIRE (the same §73 controller on REAL trained-"
                  "saturated forward, B-S73-NOTE earned future-fire)"),
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire (g_train_flame_not_pytorch "
                      "evidence-anchor-clause carry — anima-physics "
                      "overlays on flame have upstream-GAP per §71 "
                      "inbox patch)"),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True, "base_ckpt": None,
        "seed": cfg["seed"], "config": cfg,
        "n_params": n_params, "n_params_M": round(n_params / 1e6, 2),
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_sha256": corpus_sha,
        "records_total": len(items),
        "init_ce": round(init_ce, 6) if init_ce is not None else None,
        "final_ce": final_ce,
        "ce_descent": (round(init_ce - final_ce, 6)
                       if final_ce is not None and init_ce is not None else None),
        "saturation_ce_gate":  SATURATION_CE_GATE,
        "trained_saturated":   trained_saturated,
        "train_wall_s":        round(train_wall, 2),
        "controller_constants": {
            "PSI_VAC": PSI_VAC, "BASIN_RADIUS": BASIN_RADIUS,
            "LAMBDA_STD": LAMBDA_STD, "EMA_BETA": EMA_BETA,
            "PHI_RATCHET": PHI_RATCHET, "N_LOOP_STEPS": nL,
            "TAU_NONDEG": TAU_NONDEG, "MAJ_COLLAPSE": MAJ_COLLAPSE,
            "IM_THRESHOLD_S24": IM_THRESHOLD_S24,
            "TENSION_RELEASE": TENSION_RELEASE,
            "TENSION_RELEASE_NOISE": TENSION_RELEASE_NOISE,
            "PSI_VAC_PULL": PSI_VAC_PULL,
            "SEED": SEED,
        },
        "closed_loop_self_trigger":          closed_loop,
        "sever_feedback_self_trigger":       open_loop_sever,
        "off_reduction_s24_in_loop":         off_reduction,
        "verdict":          verdict,
        "verdict_caveat":   verdict_caveat,
        "north_star_unchanged":      True,
        "milestone_unchanged":       "§15 + §51 + §72 (GOAL 미도달)",
        "capability_claim":          0,
        "comparison_to_s73_stub": {
            "stub_closed_interval_var":  35.02285318559557,
            "stub_open_emit_rate":       0.8616666666666667,
            "stub_s24_in_loop_interval_var": 0.4739229024943309,
            "fire_closed_interval_var":      closed_loop["interval_var"],
            "fire_open_emit_rate":           open_loop_sever["emit_rate"],
            "fire_s24_in_loop_interval_var": off_reduction["interval_var"],
            "fire_closed_nondegen":          closed_loop["self_trigger_nondegen"],
            "fire_s24_in_loop_nondegen":     off_reduction["self_trigger_nondegen"],
        },
        "deterministic": True,
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({k: result[k] for k in (
        "verdict", "trained_saturated", "init_ce", "final_ce",
        "comparison_to_s73_stub")}, indent=2, ensure_ascii=False), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--block-size", type=int, default=128)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    ap.add_argument("--fwd-bsz", type=int, default=8)
    ap.add_argument("--loop-steps", type=int, default=300)
    args = ap.parse_args()
    cfg = dict(corpus=args.corpus, out_dir=args.out_dir, steps=args.steps,
               lr=args.lr, bsz=args.bsz, seed=args.seed,
               d_model=args.d_model, n_head=args.n_head,
               n_layer=args.n_layer, n_kv_head=args.n_kv_head,
               block_size=args.block_size, warmup=args.warmup,
               lambda_ctl=args.lambda_ctl, lambda_route=args.lambda_route,
               fwd_bsz=args.fwd_bsz, loop_steps=args.loop_steps)
    main(cfg)
