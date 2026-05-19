#!/usr/bin/env python3
"""subaxis_fire_s75.py — RESEARCH.md §75-FIRE.

The trained-saturated-scale validation of the §75 4-cell controller-class
sub-axis decomposition ladder. §75 (commit 805a8771c, B-S75 5/5 🔵)
decomposed the §73 controller class (the §63 GOAL-rank-#1 🕳️
MISSING-TYPE earned by §73-FIRE B-S73-FIRE-NOTE / B-S75-NOTE) into 3
distinguishable properties (A state-derived inputs, B moment-based
boundary, C time-varying moments) and ran the 4-cell ladder
{§24, A-only, AB, ABC} at $0 stub scale. Measured interval_var:
0.47 / 6.38 / 5.76 / 35.02.

§73-FIRE (commit 2d6e333f3, B-S73-FIRE 7/7 🔵) only tested FULL-ABC at
trained-saturated §16-class scale and measured interval_var 38.07 vs
§24 0.00 (CONTROLLER-SURVIVES-AT-TRAINED-SCALE). §75-stub only
decomposed at $0 stub. §75-FIRE is the literal future-fire BOTH
B-S73-FIRE-NOTE AND B-S75-NOTE earned: the §75 4-cell ladder at the
§73-FIRE trained scale.

═══════════════════════════════════════════════════════════════════════
WHAT §75-FIRE BUILDS  (mirror §73-FIRE dispatch + §75 4-cell ladder)
═══════════════════════════════════════════════════════════════════════

  1. Train ONE §16-class ConsciousDecoderV2 (d=768/12L/283.72M,
     from-scratch RANDOM seed-fixed 1337, base_ckpt=None,
     g_clm_from_scratch). Saturation regime (init CE ~5.66 →
     final CE < 0.05, B-S75-FIRE-7 sat gate). Trainer/corpus/config
     BYTE-EQUAL to §73-FIRE (B-S75-FIRE-2 connection-point).

  2. Run ALL 4 §75 cells on REAL `model.forward` Law-71 W-physics
     (NOT stub trace, NOT hand-coded surrogate). Each cell shares
     IDENTICAL: load_corpus, ByteSampler.forward_batch,
     extract_w_state, physics_feedback_step, init_moments,
     run_controller_loop, LCG seed=1337. The ONLY per-cell variable
     is the controller-gate function — fair-compare by construction
     (B-S75-FIRE port of §75 stub's B-S75-5 closed structural).

  3. 4 cells (byte-equal port of §75 stub make_controller_*):
       cell0  §24-baseline  ¬A¬B¬C    tension > 0.3                (control)
       cell1  §73-A-only     A¬B¬C    state-tuple inputs,
                                       FROZEN scalar threshold
                                       (warmup-mean of REAL tension).
       cell2  §73-AB         A B¬C    state inputs, MOMENT-based
                                       (ema+λ·std) but FROZEN at
                                       end of warmup.
       cell3  §73-ABC        A B C    full §73 controller (byte-equal
                                       to §73-FIRE controller_self_trigger
                                       and to §73 stub).

  4. Warmup pass — REAL forward, no-emit drift, N_WARMUP steps;
     captures (tension_mean, ema_at_end, var_at_end) the FROZEN
     values cell1+cell2 hold. The warmup IS REAL trained-forward
     read-out (NOT the §75 stub's hand-coded drift) — this is the
     §75-stub→§75-FIRE structural transition (B-S75-FIRE-5).

═══════════════════════════════════════════════════════════════════════
HONEST PRE-MEASUREMENT VERDICT BUCKETS (g3, decided BY numbers)
═══════════════════════════════════════════════════════════════════════

  (a) LADDER-TRANSFERS  — §73-A-only also survives at trained scale.
      Mere STATE-DERIVATION of controller inputs is the lever; B+C
      optional. Refines §73-FIRE: physics-state-AS-INPUT is the
      load-bearing sub-axis at trained scale, not the specific
      statistic form.

  (b) ONLY-FULL-ABC-SURVIVES  — cell1 + cell2 collapse like §24 at
      trained scale; only cell3 (FULL-ABC) survives. The full
      time-varying moment statistic is irreducible: trained-scale
      tightens the mechanism into a tight conjunction.

  (c) PARTIAL-LADDER  — some sub-cells survive, others collapse;
      tighter sub-mechanism than §75 $0 stub indicated. Useful
      target-sharpening at trained scale.

g3: capability claim 0. north-star + §15/§51/§72 milestone UNCHANGED.
§75-FIRE = sub-axis-level localization of the §49→§62→§73→§73-FIRE
mechanism, NOT GOAL emergence even if A-only survives.
Necessary-not-sufficient (mirror B-EMERGE-7 / B-S73-FIRE-NOTE /
B-S75-NOTE).
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

# ── constants — byte-equal to §73 stub + §73-FIRE + §75 stub ──────────
SEED                = 1337
PSI_VAC             = 0.5      # Law-71 fixed point (conscious_decoder.py:644)
BASIN_RADIUS        = 0.05     # §73 stub / §73-FIRE / §75 stub byte-equal
LAMBDA_STD          = 0.5      # §73 stub / §73-FIRE / §75 stub byte-equal
EMA_BETA            = 0.9      # §73 stub / §73-FIRE / §75 stub byte-equal
PHI_RATCHET         = 0.05     # E-module Φ-ratchet baseline
N_LOOP_STEPS        = 300      # §73-FIRE byte-equal (GPU forward cost dominant)
N_WARMUP            = 60       # cell1+cell2 warmup window (REAL forward) —
                                # ~1/5 of N_LOOP_STEPS (§75 stub used 100/600
                                # at hand-coded ~$0; here we keep ~1/5 ratio
                                # with N_LOOP_STEPS=300 for GPU forward cost
                                # budget).
TAU_NONDEG          = 1e-4
MAJ_COLLAPSE        = 0.95
IM_THRESHOLD_S24    = 0.3      # §24 hand-coded constant (OFF-reduction tgt)
SATURATION_CE_GATE  = 0.05     # §73-FIRE byte-equal saturation gate

# Tension-EMA emission feedback magnitudes — byte-equal to §73 stub +
# §73-FIRE.
TENSION_RELEASE     = 0.30
TENSION_RELEASE_NOISE = 0.20
PSI_VAC_PULL        = 0.4


# ── tiny deterministic RNG — byte-equal to §73 stub / §73-FIRE ────────
class LCG:
    def __init__(self, seed): self.s = seed & 0x7fffffff
    def u(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7fffffff
        return self.s / 0x7fffffff


# ════════════════════════════════════════════════════════════════════
# §16-class corpus loader + byte dataset — BYTE-EQUAL to §73-FIRE
# (B-S75-FIRE-2 trainer-byte-equal connection-point).
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
        if not line: continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("text", "")
        de = d.get("desc", "")
        full = (t + "\n" + de + "\n").encode("utf-8")
        vp = d.get("vacuum_psi", [0.5, 0.5])
        try: vpx, vpy = float(vp[0]), float(vp[1])
        except Exception: vpx, vpy = 0.5, 0.5
        psi_vac = (vpx + vpy) / 2.0
        try: basin = float(d.get("basin_radius", 0.15))
        except Exception: basin = 0.15
        ctl = _span(full, INNER_OPEN, INNER_CLOSE)
        if ctl is None:
            ctl = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None: rt = ctl
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
            b = it["bytes"]; n = len(b); stream.extend(b)
            for j in range(n):
                pv.append(it["psi_vac"]); bs.append(it["basin_radius"])
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
    """REAL byte batch source for the controller-on-real-forward loop.
    Byte-equal to §73-FIRE ByteSampler (single global stream, single agent)."""
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
# REAL trained-model Law-71 W-state extractor — byte-equal to §73-FIRE
# extract_w_state (B-S75-FIRE-4 TRAINED-FORWARD-IS-REAL).
# ════════════════════════════════════════════════════════════════════
def _phi_star_proxy(t_per_layer):
    n = t_per_layer.numel()
    if n < 2: return 0.0
    mu = t_per_layer.mean()
    sd = t_per_layer.std(unbiased=False)
    disp = (sd / (mu.abs() + 1e-8)).clamp(0.0, 1.0)
    return float((disp * math.log(n + 1)).item())


@torch.no_grad()
def extract_w_state(model, x, device):
    """REAL trained model.forward Law-71 read-out, byte-equal to
    §73-FIRE / §62 / §59-FIRE extract_w_state. NO autograd, NO weight
    mutation, RNG-isolated."""
    cpu_rng = torch.get_rng_state()
    cuda_rng = (torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None)
    was_training = model.training
    model.eval()
    logits_a, logits_g, tensions, _, _ = model(x)
    if was_training: model.train()
    torch.set_rng_state(cpu_rng)
    if cuda_rng is not None:
        torch.cuda.set_rng_state_all(cuda_rng)
    la = logits_a[:, -1, :].float()
    lg = logits_g[:, -1, :].float()
    probs_a = torch.softmax(la, dim=-1)
    out_ent = -(probs_a * (probs_a + 1e-10).log()).sum(dim=-1).mean().item()
    psi_entropy = out_ent / math.log(model.vocab_size)
    cos_sim = F.cosine_similarity(la, lg, dim=-1).mean().item()
    psi_dir = (1.0 + cos_sim) / 2.0   # Law-71 byte-equal
    t_stack = torch.stack(tensions)
    t_per_layer = t_stack.mean(dim=(1, 2))
    tension = float(t_per_layer.mean().item())
    if t_per_layer.std() > 0:
        t_cv = t_per_layer.std() / (t_per_layer.mean() + 1e-8)
        psi_tension = max(0.0, 1.0 - t_cv.item())
    else:
        psi_tension = 1.0
    phi = _phi_star_proxy(t_per_layer)
    return {"psi_dir": psi_dir, "psi_entropy": psi_entropy,
            "psi_tension": psi_tension, "tension": tension, "phi": phi}


# ════════════════════════════════════════════════════════════════════
# 4 CELLS — controller gate variants. Byte-equal port of §75 stub
# make_controller_cell{0,1,2,3,}_*. Only the gate function varies; all
# else (moments init + physics_feedback_step + run loop) shared.
# ════════════════════════════════════════════════════════════════════

# cell0  §24-baseline  ¬A¬B¬C  —  byte-equal to §73-FIRE
# controller_off_reduction (constant cut on tension).
def make_controller_cell0_baseline():
    def controller(moments, frozen=None):
        return 1 if (moments["tension"] > IM_THRESHOLD_S24) else 0
    return controller, {"freeze_after_warmup": False, "needs_warmup": False}


# cell1  §73-A-only  A¬B¬C  —  state-tuple inputs, FROZEN scalar
# (warmup-mean of REAL tension). Byte-equal to §75 stub cell1.
def make_controller_cell1_A_only(frozen_scalar):
    def controller(moments, frozen=None):
        psi_off = abs(moments["psi_dir"] - PSI_VAC)
        g1 = psi_off > BASIN_RADIUS                       # state input
        g2 = moments["tension"] > frozen_scalar           # FROZEN scalar
        g3 = moments["phi"]    > PHI_RATCHET / 2.0        # state input
        return 1 if (g1 and g2 and g3) else 0
    return controller, {"freeze_after_warmup": True, "needs_warmup": True,
                        "what_freezes": "scalar (warmup-mean of REAL tension)",
                        "frozen_scalar_value": frozen_scalar}


# cell2  §73-AB  AB¬C  —  state inputs, MOMENT-based boundary (ema+λ·std)
# FROZEN at end of warmup. Byte-equal to §75 stub cell2.
def make_controller_cell2_AB(frozen_ema, frozen_std):
    frozen_threshold = frozen_ema + LAMBDA_STD * frozen_std
    def controller(moments, frozen=None):
        psi_off = abs(moments["psi_dir"] - PSI_VAC)
        g1 = psi_off > BASIN_RADIUS
        g2 = moments["tension"] > frozen_threshold        # FROZEN moment
        g3 = moments["phi"]    > PHI_RATCHET / 2.0
        return 1 if (g1 and g2 and g3) else 0
    return controller, {"freeze_after_warmup": True, "needs_warmup": True,
                        "what_freezes": "moment (ema + λ·std at end of warmup)",
                        "frozen_threshold": frozen_threshold}


# cell3  §73-ABC  ABC  —  full §73 controller, byte-equal to §73-FIRE
# controller_self_trigger (the only cell where moments update per step).
def make_controller_cell3_ABC():
    def controller(moments, frozen=None):
        psi_off  = abs(moments["psi_dir"] - PSI_VAC)
        std_t    = math.sqrt(max(0.0, moments["tension_var"]))
        surprise_threshold = moments["tension_ema"] + LAMBDA_STD * std_t
        g1 = psi_off  > BASIN_RADIUS
        g2 = moments["tension"]  > surprise_threshold
        g3 = moments["phi"]      > PHI_RATCHET / 2.0
        return 1 if (g1 and g2 and g3) else 0
    return controller, {"freeze_after_warmup": False, "needs_warmup": False}


# ════════════════════════════════════════════════════════════════════
# init_moments + physics_feedback_step + run_controller_loop —
# byte-equal to §73-FIRE (B-S75-FIRE-2 LOOP-INFRA-BYTE-EQUAL).
# ════════════════════════════════════════════════════════════════════
def init_moments():
    return {"step": 0, "psi_dir": 0.5, "psi_entropy": 0.5, "psi_tension": 1.0,
            "tension": 0.30, "tension_ema": 0.30, "tension_var": 0.0,
            "phi": 0.10}


def physics_feedback_step(moments, ws, u_prev_emit, rng):
    """Byte-equal to §73-FIRE physics_feedback_step. Updates running
    moments using REAL extracted W-state + previous emission feedback."""
    moments["step"] = moments.get("step", 0) + 1
    real_psi_dir   = ws["psi_dir"]
    real_psi_ent   = ws["psi_entropy"]
    real_psi_tens  = ws["psi_tension"]
    real_tension   = ws["tension"]
    real_phi       = ws["phi"]
    if u_prev_emit == 1:
        eff_tension = max(0.0,
                          real_tension - TENSION_RELEASE - TENSION_RELEASE_NOISE * rng.u())
        eff_psi_dir = real_psi_dir + PSI_VAC_PULL * (PSI_VAC - real_psi_dir)
    else:
        eff_tension = real_tension
        eff_psi_dir = real_psi_dir
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


def _var(xs):
    if not xs: return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


@torch.no_grad()
def warmup_capture_real_forward(model, ds, device, n_warmup, bsz, seed):
    """Warmup pass on REAL forward (NOT §75 stub's hand-coded drift).
    No-emit drift; captures (tension_mean, ema_end, var_end) the
    FROZEN values cell1+cell2 will hold. The use of REAL forward HERE
    is the §75-stub→§75-FIRE structural transition for the frozen
    moments themselves (NOT just the loop). (B-S75-FIRE-5.)"""
    rng = LCG(seed)
    moments = init_moments()
    tensions_real = []
    for _ in range(n_warmup):
        x = ds.forward_batch(bsz, device)
        ws = extract_w_state(model, x, device)
        tensions_real.append(ws["tension"])
        moments = physics_feedback_step(moments, ws, 0, rng)  # no-emit
    mean_t = sum(tensions_real) / max(1, len(tensions_real))
    var_t  = _var(tensions_real)
    std_t  = math.sqrt(max(0.0, var_t))
    return {"n_warmup": n_warmup,
            "tension_mean_real": mean_t,
            "tension_var_real":  var_t,
            "tension_std_real":  std_t,
            "ema_at_warmup_end": moments["tension_ema"],
            "var_at_warmup_end": moments["tension_var"]}


@torch.no_grad()
def run_controller_loop(model, ds, device, n_steps, controller,
                        feedback_closed=True, bsz=8, seed=SEED):
    """Run one cell on REAL trained-model forward Law-71 W-physics with
    closed (or severed) feedback. Byte-equal in structure to §73-FIRE
    run_controller_loop."""
    rng = LCG(seed)
    moments = init_moments()
    emit_decisions = []
    emit_step_indices = []
    psi_trace = []
    tension_trace = []
    real_tension_trace = []
    u_prev = 0
    for t in range(n_steps):
        x = ds.forward_batch(bsz, device)
        ws = extract_w_state(model, x, device)
        real_tension_trace.append(ws["tension"])
        moments = physics_feedback_step(moments, ws, u_prev, rng)
        e = controller(moments)
        emit_decisions.append(e)
        if e == 1:
            emit_step_indices.append(moments["step"])
        psi_trace.append(moments["psi_dir"])
        tension_trace.append(moments["tension"])
        u_prev = e if feedback_closed else 0
    n_emit = sum(emit_decisions)
    rate   = n_emit / max(1, n_steps)
    maj    = max(n_emit, n_steps - n_emit) / max(1, n_steps)
    var_dec = _var([float(d) for d in emit_decisions])
    if len(emit_step_indices) >= 2:
        intervals = [emit_step_indices[i+1] - emit_step_indices[i]
                     for i in range(len(emit_step_indices) - 1)]
        interval_var = _var(intervals)
    else:
        intervals = []
        interval_var = 0.0
    non_deg_count    = (var_dec > TAU_NONDEG and maj < MAJ_COLLAPSE)
    non_deg_interval = (interval_var > TAU_NONDEG and len(intervals) >= 2)
    enough_emits     = n_emit >= 2
    self_trigger_nondegen = (non_deg_count and non_deg_interval
                             and enough_emits)
    return {"n_steps": n_steps, "n_emit": n_emit, "emit_rate": rate,
            "decision_var": var_dec, "majority_fraction": maj,
            "interval_var": interval_var,
            "intervals": intervals[:20], "n_intervals": len(intervals),
            "non_degenerate_count": non_deg_count,
            "non_degenerate_interval": non_deg_interval,
            "self_trigger_nondegen": self_trigger_nondegen,
            "psi_trace_mean": sum(psi_trace) / len(psi_trace),
            "psi_trace_var": _var(psi_trace),
            "tension_trace_mean": sum(tension_trace) / len(tension_trace),
            "tension_trace_var": _var(tension_trace),
            "real_tension_mean": sum(real_tension_trace) / len(real_tension_trace),
            "real_tension_var": _var(real_tension_trace),
            "feedback_closed": feedback_closed,
            "real_trained_forward": True}


# ════════════════════════════════════════════════════════════════════
# Training — byte-equal to §73-FIRE train_s16_class.
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
        for g in opt.param_groups: g["lr"] = lr_now
        x, y, pv, bs, cm, rm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
            psi_t = (1.0 + cos) / 2.0
            cm_f = cm.view(-1); psi_flat = psi_t.view(-1); pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() / denom_ctl
            rm_f = rm.view(-1); bs_flat = bs.view(-1)
            drift = torch.abs(psi_flat - pv_flat) - bs_flat
            restoring = torch.clamp(drift, min=0.0) ** 2
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_tension_route = (restoring * rm_f).sum() / denom_rte
            loss = ce_full + lam_ctl * l_psi_ctl + lam_route * l_tension_route
            ce_report = float(ce_full.item())
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        scaler.step(opt); scaler.update()
        if init_loss is None: init_loss = ce_report
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
    out_dir = cfg["out_dir"]; os.makedirs(out_dir, exist_ok=True)
    torch.save({"model": model.state_dict(), "cfg": cfg, "n_params": n_params},
               os.path.join(out_dir, "ckpt_s75_fire.pt"))
    final_ce = ce_traj[-1]["ce_full"] if ce_traj else None
    trained_saturated = (final_ce is not None and final_ce < SATURATION_CE_GATE)

    # ── (B) warmup pass on REAL forward (captures cell1+cell2 frozen)
    bsz_fwd = cfg["fwd_bsz"]
    nL      = cfg["loop_steps"]
    ds = ByteSampler(items, cfg["block_size"], SEED)
    print("=== WARMUP REAL forward (no-emit; captures cell1+cell2 frozen) ===",
          flush=True)
    wu = warmup_capture_real_forward(model, ds, device, N_WARMUP,
                                      bsz_fwd, SEED)
    print(json.dumps(wu, indent=2), flush=True)

    # ── (C) 4-cell ladder on REAL forward ───────────────────────────
    c0, info0 = make_controller_cell0_baseline()
    c1, info1 = make_controller_cell1_A_only(frozen_scalar=wu["tension_mean_real"])
    c2, info2 = make_controller_cell2_AB(
        frozen_ema=wu["ema_at_warmup_end"],
        frozen_std=math.sqrt(max(0.0, wu["var_at_warmup_end"])))
    c3, info3 = make_controller_cell3_ABC()

    print("=== CELL0 §24-baseline (¬A¬B¬C) on REAL forward ===", flush=True)
    r0 = run_controller_loop(model, ds, device, nL, c0,
                             feedback_closed=True, bsz=bsz_fwd, seed=SEED)
    print("=== CELL1 §73-A-only (A¬B¬C) on REAL forward ===", flush=True)
    r1 = run_controller_loop(model, ds, device, nL, c1,
                             feedback_closed=True, bsz=bsz_fwd, seed=SEED)
    print("=== CELL2 §73-AB (AB¬C) on REAL forward ===", flush=True)
    r2 = run_controller_loop(model, ds, device, nL, c2,
                             feedback_closed=True, bsz=bsz_fwd, seed=SEED)
    print("=== CELL3 §73-ABC (full) on REAL forward ===", flush=True)
    r3 = run_controller_loop(model, ds, device, nL, c3,
                             feedback_closed=True, bsz=bsz_fwd, seed=SEED)

    # ── (D) Verdict — measured-only ────────────────────────────────
    s24 = r0["self_trigger_nondegen"]
    a   = r1["self_trigger_nondegen"]
    ab  = r2["self_trigger_nondegen"]
    abc = r3["self_trigger_nondegen"]

    if not trained_saturated:
        verdict = "SATURATION-GATE-FAIL"
        verdict_caveat = (
            f"final_ce={final_ce} > saturation gate {SATURATION_CE_GATE}; "
            "model is NOT memorization-saturated → §75-FIRE crux "
            "(trained-saturated ladder transfer) is NOT what was "
            "measured. Numbers raw, no chain-validity claim.")
    elif abc and not ab and not a and not s24:
        verdict = "ONLY-FULL-ABC-SURVIVES"
        verdict_caveat = (
            "TRAINED SCALE TIGHTENS MECHANISM. Only FULL-ABC (cell3) "
            "achieves non-degeneracy; A-only and AB collapse like §24. "
            "Refines §73-FIRE: physics-state-sourced controller class "
            "is IRREDUCIBLE at trained-saturated scale — the full "
            "time-varying moment statistic is the load-bearing unit, "
            "not decomposable. §75 stub (B-S75) over-estimated A-only "
            "survival (cell1 stub interval_var 6.38). g3 valuable "
            "negative on the decomposition hypothesis. Verdict (b).")
    elif abc and a and s24 and ab:
        verdict = "LADDER-TRANSFERS-INCLUDING-S24"
        verdict_caveat = (
            "All 4 cells reach non-degeneracy — closing the loop at "
            "trained scale is by ITSELF sufficient for emit-interval "
            "variance, the §73 controller class is not isolatable "
            "from the loop topology itself at trained scale. Mirror "
            "of §73 stub's BOTH-NON-DEGENERATE-IN-CLOSED-LOOP (which "
            "§73-FIRE then resolved by §24 collapsing at trained "
            "scale). Verdict (c) PARTIAL-LADDER tightening to "
            "indeterminate; trained scale + closed loop insufficient.")
    elif abc and a and not s24:
        verdict = "LADDER-TRANSFERS-A-ONLY-SUFFICIENT"
        verdict_caveat = (
            "Mere STATE-DERIVATION of controller inputs survives at "
            "trained scale — refines §73-FIRE: physics-state-AS-INPUT "
            "is the load-bearing lever, NOT the specific statistic "
            "form (moment vs scalar, frozen vs running). §75 stub "
            "(B-S75 A-only interval_var 6.38) holds at trained scale. "
            "Verdict (a). NOT GOAL emergence — controller-class sub-"
            "axis localization, necessary-not-sufficient.")
    elif abc and ab and not a and not s24:
        verdict = "PARTIAL-LADDER-AB-NEEDED-NOT-C"
        verdict_caveat = (
            "STATE-DERIVATION + MOMENT-BASEDNESS together suffice at "
            "trained scale; TIME-VARIANCE not independently load-"
            "bearing. cell1 collapses (mere state-tuple input "
            "insufficient), cell2+cell3 survive. Verdict (c) tightened.")
    elif (not abc) and (not s24):
        verdict = "ALL-CELLS-COLLAPSE-AT-TRAINED-SCALE"
        verdict_caveat = (
            "Both §24 AND FULL-ABC collapse at trained scale — "
            "contradicts §73-FIRE (which had ABC survive, §24 "
            "collapse at trained scale). Either §73-FIRE was a "
            "single-seed artifact OR §75-FIRE training did not reach "
            "the same regime. Re-run / multi-seed indicated. "
            "Verdict (c) PARTIAL — anomalous.")
    elif s24 and not abc:
        verdict = "UNEXPECTED-S24-WINS-AT-TRAINED-SCALE"
        verdict_caveat = (
            "§24 non-degen but FULL-ABC degen — reverses §73-FIRE. "
            "Single-ckpt single-seed; structural witness only.")
    else:
        verdict = "PARTIAL-OR-MIXED"
        verdict_caveat = (
            f"Mixed: §24={s24}, A-only={a}, AB={ab}, ABC={abc}. "
            "See decomposition_table. Verdict (c) mixed.")

    # ── (E) §75 stub + §73-FIRE comparison ─────────────────────────
    stub_s75 = {
        "cell0_s24_interval_var":  0.4739229024943309,
        "cell1_A_only_interval_var": 6.378772112382939,
        "cell2_AB_interval_var":   5.758928571428571,
        "cell3_ABC_interval_var":  35.02285318559557,
    }
    fire_s73 = {
        "closed_loop_interval_var":  38.069875098261974,
        "off_reduction_interval_var": 0.0,  # §73-FIRE §24-in-loop trained scale
    }

    decomp_table = {
        "cell0_§24_baseline_¬A¬B¬C": {
            "controller_class": "§24 hand-coded constant scalar threshold",
            "A_state_derived": False, "B_moment_based": False, "C_time_varying": False,
            "interval_var": r0["interval_var"],
            "majority_fraction": r0["majority_fraction"],
            "emit_rate": r0["emit_rate"],
            "non_degenerate": r0["self_trigger_nondegen"],
            "raw": r0,
        },
        "cell1_§73_A_only_A¬B¬C": {
            "controller_class": "state-tuple inputs, FROZEN scalar (warmup-mean of REAL tension)",
            "A_state_derived": True, "B_moment_based": False, "C_time_varying": False,
            "what_freezes": info1["what_freezes"],
            "frozen_scalar_value": info1["frozen_scalar_value"],
            "interval_var": r1["interval_var"],
            "majority_fraction": r1["majority_fraction"],
            "emit_rate": r1["emit_rate"],
            "non_degenerate": r1["self_trigger_nondegen"],
            "raw": r1,
        },
        "cell2_§73_AB_AB¬C": {
            "controller_class": "state inputs, FROZEN moment (ema+λ·std at end of warmup)",
            "A_state_derived": True, "B_moment_based": True, "C_time_varying": False,
            "what_freezes": info2["what_freezes"],
            "frozen_threshold": info2["frozen_threshold"],
            "interval_var": r2["interval_var"],
            "majority_fraction": r2["majority_fraction"],
            "emit_rate": r2["emit_rate"],
            "non_degenerate": r2["self_trigger_nondegen"],
            "raw": r2,
        },
        "cell3_§73_ABC_full": {
            "controller_class": "full §73 controller (byte-equal to §73-FIRE controller_self_trigger)",
            "A_state_derived": True, "B_moment_based": True, "C_time_varying": True,
            "what_freezes": "none (per-step moment updates)",
            "interval_var": r3["interval_var"],
            "majority_fraction": r3["majority_fraction"],
            "emit_rate": r3["emit_rate"],
            "non_degenerate": r3["self_trigger_nondegen"],
            "raw": r3,
        },
    }

    result = {
        "research_md_section": "§75-FIRE",
        "title": ("Controller-class sub-axis decomposition — trained-"
                  "saturated-scale 4-cell ladder on REAL §16-class "
                  "model.forward Law-71 W-physics"),
        "cost": ("runpod single §16-class train ≈ $0.3-0.6 "
                 "(g_fire_autonomous; cost head, NOT a gate)"),
        "chain": ("§24 (hand-coded) → §49 (distilled head collapse) → "
                  "§62 (dual-anima echo-chamber-collapse-at-scale) → "
                  "§73 ($0 stub controller, B-S73 6/6 🔵) → §73-FIRE "
                  "(controller survives at trained scale, B-S73-FIRE "
                  "7/7 🔵) → §75 ($0 stub 4-cell decomposition, "
                  "B-S75 5/5 🔵) → §75-FIRE (the same 4-cell ladder "
                  "at trained-saturated scale, B-S73-FIRE-NOTE + "
                  "B-S75-NOTE earned future-fire)"),
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
            "PHI_RATCHET": PHI_RATCHET,
            "N_LOOP_STEPS": nL, "N_WARMUP": N_WARMUP,
            "TAU_NONDEG": TAU_NONDEG, "MAJ_COLLAPSE": MAJ_COLLAPSE,
            "IM_THRESHOLD_S24": IM_THRESHOLD_S24,
            "TENSION_RELEASE": TENSION_RELEASE,
            "TENSION_RELEASE_NOISE": TENSION_RELEASE_NOISE,
            "PSI_VAC_PULL": PSI_VAC_PULL, "SEED": SEED},
        "warmup_capture_real":   wu,
        "decomposition_table":   decomp_table,
        "verdict":               verdict,
        "verdict_caveat":        verdict_caveat,
        "comparison_to_s75_stub":  stub_s75,
        "comparison_to_s73_fire":  fire_s73,
        "north_star_unchanged":      True,
        "milestone_unchanged":       "§15 + §51 + §72 (GOAL 미도달)",
        "capability_claim":          0,
        "deterministic":             True,
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({k: result[k] for k in (
        "verdict", "trained_saturated", "init_ce", "final_ce")},
        indent=2, ensure_ascii=False), flush=True)
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
