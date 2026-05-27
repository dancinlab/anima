#!/usr/bin/env python3
"""physics_metacognition_train_s83_fire.py — RESEARCH.md §83-FIRE.

The trained-saturated-scale validation of the §83 physics-only metacognition
7-cell × 20-step closed-form rule grid (commit 5138cffb0, B-S83 7/7 🔵).
§83 (stub) measured the 7-cell × 20-step grid on a HAND-CODED LCG-driven
ψ-state surrogate; §83-FIRE re-runs the SAME 7 cells on the REAL §16-class
trained-saturated `model.forward` Law-71 ψ-state.

§83 stub measured:
  cell0 dhdl_distillation       dec_var=0.160 maj_frac=0.80 plast=0.850 emit=4
  cell1 s24_baseline (§24)      dec_var=0.128 maj_frac=0.85 plast=0.625 emit=17
  cell2 R1 phi+tension          dec_var=0.040 maj_frac=0.80 plast=0.825 emit=4
  cell3 R2 criticality_band     dec_var=0.132 maj_frac=0.50 plast=0.600 emit=10
  cell4 R3 motivation+critical  dec_var=0.250 maj_frac=0.50 plast=0.750 emit=10   ← winner
  cell5 R4 slow_dwell           dec_var=0.137 maj_frac=0.70 plast=0.675 emit=3
  cell6 R5 composite            dec_var=0.078 maj_frac=0.60 plast=0.675 emit=1

4-corner verdict at stub:
  (α) PHYSICS-RULE-NON-DEGENERATE = TRUE  (R3 won)
  (β) ALL-RULES-COLLAPSE         = FALSE
  (γ) R5 COMPOSITE-OUTPERFORMS    = FALSE (over-restricts)
  (δ) SUBSTRATE-PLASTICITY-CONF   = TRUE  (R1+R3 ≥ 0.75)

§73-FIRE precedent: §73 stub controller (B-S73 6/6 🔵) → §73-FIRE trained-scale
re-run on REAL model.forward Law-71 (B-S73-FIRE 7/7 🔵) measured
CONTROLLER-SURVIVES-AT-TRAINED-SCALE (interval_var 38.07 vs §24 0.00). §75-FIRE
followed with the 4-cell ladder.

§83-FIRE is the literal future-fire the §83 closed-form rule grid earned:
the 7 closed-form rules' behaviour on REAL trained-saturated ψ-state, NOT
hand-coded surrogate ψ. The structural difference vs §83 stub: ψ_state from
`model.forward` Law-71 (conscious_decoder.py:728-751 byte-equal) over a REAL
byte batch (ByteSampler.forward_batch). No learned parameters in any rule.

═══════════════════════════════════════════════════════════════════════
WHAT §83-FIRE BUILDS
═══════════════════════════════════════════════════════════════════════

  1. Train ONE §16-class ConsciousDecoderV2 (d=768/12L/283.72M, from-scratch
     RANDOM seed-fixed 1337, base_ckpt=None, g_clm_from_scratch). Saturation
     regime (init CE ~5.66 → final CE < 0.05, B-S83-FIRE-7 sat gate).
     Trainer/corpus/config BYTE-EQUAL to §73-FIRE (B-S83-FIRE-2
     connection-point).

  2. Run ALL 7 §83 cells on REAL `model.forward` Law-71 ψ-state (NOT
     LCG-driven hand-coded ψ_state). Each cell shares IDENTICAL
     load_corpus, ByteSampler.forward_batch, extract_psi_state, run_cell_loop,
     LCG seed=1337. The ONLY per-cell variable is the closed-form decision
     rule (no learned parameter, AST-verified B-S83-FIRE-1).

  3. Run substrate-plasticity test on REAL ψ-state. For each cell, run the
     same N steps with the same model+corpus, but permute ψ field assignments
     (Levin "use different field as readout substrate" mirror): swap
     phi↔tension, then swap psi_dir↔motivation. Compute decision agreement
     rate between base and permuted runs. ≥0.75 = substrate-invariant.

  4. Compare 7-cell × 20-step trained-scale metrics to §83 stub. Track
     §49 distillation null-control (cell0): is the learned-head's predicted
     §49 majority-collapse REPRODUCED at trained-scale?

═══════════════════════════════════════════════════════════════════════
HONEST PRE-MEASUREMENT VERDICT BUCKETS (g3, decided BY numbers)
═══════════════════════════════════════════════════════════════════════

  (α) PHYSICS-RULE-NON-DEGENERATE-AT-TRAINED  — ≥1 R-rule (cells 2-6)
      decision_var > τ_var=0.05 AND maj_frac < 0.95 at trained-scale.

  (β) ALL-RULES-COLLAPSE-AT-TRAINED  — every R-rule maj_frac ≥ 0.95 at
      trained-scale (§49 + §62 collapse mirror).

  (γ) COMPOSITE-R5-VS-R3-AT-TRAINED  — R5 decision_var ≥ R3 decision_var
      (composite conjunction outperforms best single rule).

  (δ) SUBSTRATE-PLASTICITY-CONFIRMED-AT-TRAINED  — ≥1 R-rule has
      substrate_plasticity_agreement ≥ 0.75 under REAL ψ field permutation
      at trained-scale (Levin biology mirror).

g3: capability claim 0. north-star + §15/§51/§72 milestone UNCHANGED. §83-FIRE
= measurement of closed-form-rule readout discrimination at trained-saturated
scale, NOT GOAL emergence. Closed-form rule survival ≠ capability emergence —
substrate-plasticity = readout substrate property NOT decision-substance
property. Levin biology (Xenopus tadpole ectopic-eye visual learning) ≠
silicon substrate (anchor only, NOT transfer claim).
Necessary-not-sufficient (mirror B-EMERGE-7 / B-S73-FIRE-NOTE / B-S75-NOTE /
B-S83-NOTE).
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

# ── constants — byte-equal to §83 stub ────────────────────────────────
SEED                = 1337
PSI_VAC             = 0.5      # Law-71 fixed point
SATURATION_CE_GATE  = 0.05     # §73-FIRE / §75-FIRE byte-equal saturation gate
TAU_VAR             = 0.05     # §83 stub 4-corner α threshold
MAJ_COLLAPSE        = 0.95     # §83 stub 4-corner β threshold
PLAST_THRESHOLD     = 0.75     # §83 stub 4-corner δ threshold (Levin mirror)

# action enum — byte-equal to §83 stub
EMIT_VOICE     = "EMIT_VOICE"
CONTINUE_THINK = "CONTINUE_THINK"
REMAIN_SILENT  = "REMAIN_SILENT"
ACTIONS = (EMIT_VOICE, CONTINUE_THINK, REMAIN_SILENT)

# ── deterministic LCG — byte-equal to §83 stub ────────────────────────
class LCG:
    def __init__(self, seed=1337): self.s = seed & 0xFFFFFFFF
    def next_u32(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s
    def uniform(self): return self.next_u32() / 4294967296.0

# ════════════════════════════════════════════════════════════════════
# 7 CELLS — closed-form decision rules. BYTE-EQUAL PORT of §83 stub
# cell0_dhdl_distillation, cell1_s24_baseline, rule_R1..R5.
# ════════════════════════════════════════════════════════════════════

# cell0 — §27/§49 DH-DL learned-head DISTILLATION NULL-CONTROL.
# Closed-form deterministic mirror = §24 threshold the head distills to:
# (psi_dir > 0.55 AND tension > 0.5) → EMIT else SILENT. Encodes the
# expected §49 majority-collapse baseline at trained-scale.
def cell0_dhdl_distillation(psi):
    if psi["psi_dir"] > 0.55 and psi["tension"] > 0.5:
        return EMIT_VOICE
    return REMAIN_SILENT

# cell1 — §24 hand-coded scalar threshold baseline.
def cell1_s24_baseline(psi):
    if psi["motivation"] > 0.6:
        return EMIT_VOICE
    return REMAIN_SILENT

# cell2 — R1 phi+tension closed-form rule.
def rule_R1_phi_tension(psi, tau_phi=0.35, tau_t=0.45):
    if psi["phi"] > tau_phi and psi["tension"] > tau_t:
        return EMIT_VOICE
    if psi["phi"] > 0.5 * tau_phi:
        return CONTINUE_THINK
    return REMAIN_SILENT

# cell3 — R2 criticality_band closed-form rule.
def rule_R2_criticality_band(psi, lo=0.4, hi=0.6):
    if lo <= psi["psi_dir"] <= hi:
        return EMIT_VOICE
    if abs(psi["psi_dir"] - 0.5) < 0.15:
        return CONTINUE_THINK
    return REMAIN_SILENT

# cell4 — R3 motivation+critical closed-form rule (§83 stub winner).
def rule_R3_motivation_critical(psi, tau_m=0.5):
    in_band = 0.4 <= psi["psi_dir"] <= 0.6
    if in_band and psi["motivation"] > tau_m:
        return EMIT_VOICE
    if in_band:
        return CONTINUE_THINK
    return REMAIN_SILENT

# cell5 — R4 slow_dwell closed-form rule. Has 5-step window state.
# _DwellTracker + _dwell + rule_R4_slow_dwell body BYTE-EQUAL to §83 stub
# (B-S83-FIRE-8 connection-point requires AST-unparse equality).
class _DwellTracker:
    def __init__(self): self.hist = []
    def update(self, psi_dir):
        self.hist.append(psi_dir)
        if len(self.hist) > 5: self.hist.pop(0)
        if len(self.hist) < 3: return False
        rng = max(self.hist) - min(self.hist)
        return rng < 0.08  # slow-dwell detected
    def reset(self): self.hist = []
_dwell = _DwellTracker()

def rule_R4_slow_dwell(psi):
    slow = _dwell.update(psi["psi_dir"])
    if slow and psi["tension"] > 0.3:
        return EMIT_VOICE
    if slow:
        return CONTINUE_THINK
    return REMAIN_SILENT

# cell6 — R5 composite conjunction.
def rule_R5_composite(psi):
    r1 = rule_R1_phi_tension(psi) == EMIT_VOICE
    r2 = rule_R2_criticality_band(psi) == EMIT_VOICE
    r3 = rule_R3_motivation_critical(psi) == EMIT_VOICE
    if r1 and r2 and r3:
        return EMIT_VOICE
    if r1 or r2 or r3:
        return CONTINUE_THINK
    return REMAIN_SILENT

# Cell registry — byte-equal to §83 stub CELLS.
CELLS = [
    ("cell0_dhdl_distillation",    cell0_dhdl_distillation,    False),
    ("cell1_s24_baseline",         cell1_s24_baseline,         False),
    ("cell2_R1_phi_tension",       rule_R1_phi_tension,        False),
    ("cell3_R2_criticality_band",  rule_R2_criticality_band,   False),
    ("cell4_R3_motivation_critical", rule_R3_motivation_critical, False),
    ("cell5_R4_slow_dwell",        rule_R4_slow_dwell,         True),   # stateful
    ("cell6_R5_composite",         rule_R5_composite,          False),
]

# ════════════════════════════════════════════════════════════════════
# §16-class corpus loader + byte dataset — byte-equal to §73-FIRE
# (B-S83-FIRE-2 trainer-byte-equal connection-point).
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
    """REAL byte batch source for the cell-on-real-forward loop.
    Byte-equal to §73-FIRE / §75-FIRE ByteSampler."""
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
# REAL trained-model Law-71 ψ-state extractor.  ψ_dir + tension are
# byte-equal to §73-FIRE / §75-FIRE extract_w_state (conscious_decoder.py
# Law-71 byte-equal). phi/motivation are §83-stub-mirror physics fields
# extracted as derived statistics over the same forward.  No learned
# parameter, no autograd, no weight mutation, RNG-isolated.
# ════════════════════════════════════════════════════════════════════
def _phi_star_proxy(t_per_layer):
    n = t_per_layer.numel()
    if n < 2: return 0.0
    mu = t_per_layer.mean()
    sd = t_per_layer.std(unbiased=False)
    disp = (sd / (mu.abs() + 1e-8)).clamp(0.0, 1.0)
    return float((disp * math.log(n + 1)).item())

@torch.no_grad()
def extract_psi_state(model, x, device):
    """REAL trained model.forward Law-71 ψ-state read-out for §83-FIRE.

    Returns a dict with exactly the 4 fields §83 rules consume:
      psi_dir   ∈ [0,1] Law-71 (1+cos(logits_a, logits_g))/2
      tension   ∈ [0,1] mean of model.tensions per layer (clamped)
      phi       ∈ [0,1] _phi_star_proxy normalized (clamped)
      motivation ∈ [0,1] (1 - psi_entropy) — high curiosity = high motivation
                          (anima W.curiosity proxy; bounded, deterministic)

    No autograd, RNG-isolated, byte-equal to §73-FIRE / §75-FIRE
    extract_w_state for psi_dir / tension. Mapping of phi / motivation
    are §83-stub-mirror real ψ-state derivations.
    """
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
    psi_entropy = out_ent / math.log(model.vocab_size)  # ∈ [0,1]
    cos_sim = F.cosine_similarity(la, lg, dim=-1).mean().item()
    psi_dir = (1.0 + cos_sim) / 2.0   # Law-71 byte-equal
    t_stack = torch.stack(tensions)
    t_per_layer = t_stack.mean(dim=(1, 2))
    tension_raw = float(t_per_layer.mean().item())
    tension = max(0.0, min(1.0, tension_raw))
    phi_raw = _phi_star_proxy(t_per_layer)
    phi = max(0.0, min(1.0, phi_raw))
    motivation = max(0.0, min(1.0, 1.0 - psi_entropy))
    return {"psi_dir": psi_dir, "tension": tension,
            "phi": phi, "motivation": motivation,
            "_raw_tension": tension_raw, "_raw_phi": phi_raw,
            "_psi_entropy": psi_entropy}

@torch.no_grad()
def run_cell_loop(model, ds, device, n_steps, cell_fn,
                  permute_map=None, bsz=8, seed=SEED):
    """Run one §83 cell on REAL trained-model forward Law-71 ψ-state.

    permute_map=None → identity (base run).
    permute_map = {field: source_field} → Levin substrate-plasticity test
    (rule reads psi[field] but value comes from psi_state[source_field]).
    """
    rng_byte = random.Random(seed)
    # Reset stateful R4 tracker per cell run for determinism.
    _dwell.reset()

    stream = []
    psi_dir_trace = []
    tension_trace = []
    raw_psi_trace = []
    for step in range(n_steps):
        x = ds.forward_batch(bsz, device)
        psi_state = extract_psi_state(model, x, device)
        if permute_map is None:
            psi_for_rule = {k: psi_state[k] for k in
                            ("psi_dir", "tension", "phi", "motivation")}
        else:
            psi_for_rule = {k: psi_state[permute_map.get(k, k)] for k in
                            ("psi_dir", "tension", "phi", "motivation")}
        action = cell_fn(psi_for_rule)
        stream.append(action)
        psi_dir_trace.append(psi_for_rule["psi_dir"])
        tension_trace.append(psi_for_rule["tension"])
        raw_psi_trace.append({k: psi_state[k] for k in
                              ("psi_dir", "tension", "phi", "motivation",
                               "_psi_entropy")})
    return {"stream": stream,
            "psi_dir_trace": psi_dir_trace,
            "tension_trace": tension_trace,
            "raw_psi_trace": raw_psi_trace}

# ════════════════════════════════════════════════════════════════════
# Metrics — byte-equal to §83 stub honest_coherent / maj_frac / variance.
# ════════════════════════════════════════════════════════════════════
def honest_coherent(decision_stream):
    if len(decision_stream) < 5:
        return False
    return len(set(decision_stream[-5:])) >= 2

def maj_frac(stream):
    if not stream: return 0.0
    from collections import Counter
    c = Counter(stream)
    return max(c.values()) / len(stream)

def variance(stream):
    if len(stream) < 2: return 0.0
    enc = {EMIT_VOICE: 1.0, CONTINUE_THINK: 0.5, REMAIN_SILENT: 0.0}
    xs = [enc[a] for a in stream]
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)

def emit_count(stream):
    return sum(1 for a in stream if a == EMIT_VOICE)

def substrate_plasticity_real(model, ds, device, cell_fn, n_step, bsz, seed):
    """Levin substrate-plasticity mirror at TRAINED-SCALE on REAL ψ-state.
    Permute ψ field assignments and check decision agreement rate vs base.

    base    : identity (psi_dir, tension, phi, motivation) → rule.
    perm1   : swap phi↔tension (rule reads psi_dir, but psi[tension] = real phi,
              psi[phi] = real tension).
    perm2   : swap psi_dir↔motivation.

    Returns mean agreement over two permutations.
    """
    base_out = run_cell_loop(model, ds, device, n_step, cell_fn,
                             permute_map=None, bsz=bsz, seed=seed)["stream"]
    perm1 = {"psi_dir": "psi_dir", "tension": "phi",
             "phi": "tension", "motivation": "motivation"}
    p1_out = run_cell_loop(model, ds, device, n_step, cell_fn,
                           permute_map=perm1, bsz=bsz, seed=seed)["stream"]
    perm2 = {"psi_dir": "motivation", "tension": "tension",
             "phi": "phi", "motivation": "psi_dir"}
    p2_out = run_cell_loop(model, ds, device, n_step, cell_fn,
                           permute_map=perm2, bsz=bsz, seed=seed)["stream"]
    agree1 = sum(1 for a, b in zip(base_out, p1_out) if a == b) / max(1, len(base_out))
    agree2 = sum(1 for a, b in zip(base_out, p2_out) if a == b) / max(1, len(base_out))
    return (agree1 + agree2) / 2.0, base_out

# ════════════════════════════════════════════════════════════════════
# Training — byte-equal to §73-FIRE / §75-FIRE train_s16_class.
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
               os.path.join(out_dir, "ckpt_s83_fire.pt"))
    final_ce = ce_traj[-1]["ce_full"] if ce_traj else None
    trained_saturated = (final_ce is not None and final_ce < SATURATION_CE_GATE)

    # ── (B) 7-cell × 20-step grid on REAL forward ───────────────────
    bsz_fwd = cfg["fwd_bsz"]
    nL      = cfg["loop_steps"]
    ds = ByteSampler(items, cfg["block_size"], SEED)

    grid = []
    for cell_name, cell_fn, _stateful in CELLS:
        print(f"=== CELL {cell_name} on REAL forward (n={nL}) ===", flush=True)
        base = run_cell_loop(model, ds, device, nL, cell_fn,
                             permute_map=None, bsz=bsz_fwd, seed=SEED)
        stream = base["stream"]
        plast, _ = substrate_plasticity_real(model, ds, device, cell_fn,
                                             nL, bsz_fwd, SEED)
        psi_dir_mean = (sum(base["psi_dir_trace"]) / max(1, len(base["psi_dir_trace"])))
        record = {
            "cell": cell_name,
            "decision_var": round(variance(stream), 6),
            "honest_coherent_body": honest_coherent(stream),
            "maj_frac": round(maj_frac(stream), 4),
            "substrate_plasticity_agreement": round(plast, 4),
            "emit_count": emit_count(stream),
            "n_steps": nL,
            "stream_head": stream[:8],
            "stream_tail": stream[-8:],
            "psi_dir_mean_real": round(psi_dir_mean, 6),
            "tension_mean_real": round(
                sum(base["tension_trace"]) / max(1, len(base["tension_trace"])), 6),
        }
        grid.append(record)
        print(json.dumps({k: record[k] for k in
                          ("cell", "decision_var", "maj_frac",
                           "substrate_plasticity_agreement",
                           "emit_count")}, indent=2), flush=True)

    # ── (C) 4-corner verdict on TRAINED-SCALE numbers ───────────────
    rule_cells = [r for r in grid if r["cell"].startswith(
        ("cell2", "cell3", "cell4", "cell5", "cell6"))]
    r5 = next(r for r in grid if r["cell"].startswith("cell6"))
    singles = [r for r in grid if r["cell"].startswith(
        ("cell2", "cell3", "cell4", "cell5"))]
    alpha_non_degen = any(r["decision_var"] > TAU_VAR
                          and r["maj_frac"] < MAJ_COLLAPSE for r in rule_cells)
    beta_all_collapse = all(r["maj_frac"] >= MAJ_COLLAPSE for r in rule_cells)
    gamma_R5_outperforms = (r5["decision_var"] >=
                            max(s["decision_var"] for s in singles))
    delta_plasticity = any(r["substrate_plasticity_agreement"] >= PLAST_THRESHOLD
                           for r in rule_cells)

    verdict_4corner = {
        "alpha_physics_rule_non_degenerate_at_trained": bool(alpha_non_degen),
        "beta_all_rules_collapse_at_trained": bool(beta_all_collapse),
        "gamma_R5_composite_outperforms_at_trained": bool(gamma_R5_outperforms),
        "delta_substrate_plasticity_confirmed_at_trained": bool(delta_plasticity),
    }

    if not trained_saturated:
        verdict = "SATURATION-GATE-FAIL"
        verdict_caveat = (
            f"final_ce={final_ce} > saturation gate {SATURATION_CE_GATE}; "
            "model is NOT memorization-saturated → §83-FIRE crux (trained-"
            "scale closed-form rule discrimination) is NOT what was measured. "
            "Numbers raw, no chain-validity claim.")
    else:
        # Comparison vs §49 distillation null-control (cell 0)
        cell0 = grid[0]
        cell0_collapsed = cell0["maj_frac"] >= MAJ_COLLAPSE
        any_rule_better_than_cell0 = any(
            r["maj_frac"] < cell0["maj_frac"] and r["decision_var"] > cell0["decision_var"]
            for r in rule_cells)
        if alpha_non_degen and any_rule_better_than_cell0:
            verdict = "PHYSICS-RULES-SURVIVE-AT-TRAINED-SCALE"
            verdict_caveat = (
                "Closed-form physics-rule readout maintains non-degeneracy at "
                "trained-saturated scale, AND ≥1 rule strictly outperforms the "
                "§27/§49 distillation null-control on both dec_var and "
                "maj_frac. The §83 stub finding (R-rule discriminates at "
                "hand-coded ψ) transfers to REAL trained-saturated ψ-state. "
                "g3: closed-form rule survival ≠ capability emergence — "
                "this is *measurement-substrate property*, not GOAL emergence. "
                "Necessary-not-sufficient (mirror B-EMERGE-7 / B-S73-FIRE-NOTE / "
                "B-S83-NOTE).")
        elif beta_all_collapse:
            verdict = "ALL-RULES-COLLAPSE-AT-TRAINED-SCALE"
            verdict_caveat = (
                "Every R-rule maj_frac ≥ 0.95 at trained-saturated scale — "
                "REAL Law-71 ψ-state from trained-saturated forward collapses "
                "the closed-form rules just as the §27/§49 distillation null-"
                "control predicts. The §83 stub winner (R3) does NOT transfer; "
                "trained-saturated forward ψ-state is structurally narrower "
                "than the §83 stub hand-coded surrogate. g3 valuable "
                "negative on the closed-form-readout hypothesis.")
        elif cell0_collapsed and alpha_non_degen:
            verdict = "RULES-BREAK-FREE-OF-DISTILLATION-BUT-NO-WINNER"
            verdict_caveat = (
                "§49 distillation null-control (cell0) collapses at trained-"
                "scale as predicted, AND ≥1 R-rule reaches non-degeneracy. "
                "However, no rule strictly dominates cell0 on BOTH dec_var "
                "AND maj_frac. Mechanism partial: closed-form readout "
                "structurally avoids the distillation trap at trained-scale, "
                "but the discrimination is weaker than the stub indicated. "
                "g3: necessary-not-sufficient.")
        else:
            verdict = "MIXED-OR-PARTIAL-AT-TRAINED-SCALE"
            verdict_caveat = (
                f"Mixed: α={alpha_non_degen}, β={beta_all_collapse}, "
                f"γ={gamma_R5_outperforms}, δ={delta_plasticity}; "
                "cell0 maj_frac={cell0_mf}. Closed-form rules show neither "
                "uniform collapse nor uniform survival at trained-scale. "
                "See grid for per-cell decomposition. Verdict (c) mixed.").format(
                    cell0_mf=cell0["maj_frac"])

    stub_s83 = {
        "cell0_dhdl_distillation":       {"dec_var": 0.160, "maj_frac": 0.80, "plast": 0.850, "emit": 4},
        "cell1_s24_baseline":            {"dec_var": 0.128, "maj_frac": 0.85, "plast": 0.625, "emit": 17},
        "cell2_R1_phi_tension":          {"dec_var": 0.040, "maj_frac": 0.80, "plast": 0.825, "emit": 4},
        "cell3_R2_criticality_band":     {"dec_var": 0.132, "maj_frac": 0.50, "plast": 0.600, "emit": 10},
        "cell4_R3_motivation_critical":  {"dec_var": 0.250, "maj_frac": 0.50, "plast": 0.750, "emit": 10},
        "cell5_R4_slow_dwell":           {"dec_var": 0.137, "maj_frac": 0.70, "plast": 0.675, "emit": 3},
        "cell6_R5_composite":            {"dec_var": 0.078, "maj_frac": 0.60, "plast": 0.675, "emit": 1},
    }
    fire_s73 = {
        "closed_loop_interval_var": 38.07,
        "off_reduction_interval_var": 0.0,
    }

    result = {
        "research_md_section": "§83-FIRE",
        "title": ("Physics-only metacognition via closed-form rule decision-"
                  "heads — trained-saturated-scale 7-cell × 20-step grid on "
                  "REAL §16-class model.forward Law-71 ψ-state + Levin "
                  "substrate-plasticity test"),
        "cost": ("runpod single §16-class train ≈ $0.3-0.5 "
                 "(g_fire_autonomous; cost head, NOT a gate)"),
        "chain": ("§24 (hand-coded) → §27/§49 (distilled head collapse) → "
                  "§62 (dual-anima echo-chamber-collapse-at-scale) → "
                  "§73-FIRE (controller survives at trained scale, "
                  "B-S73-FIRE 7/7 🔵) → §75-FIRE (4-cell ladder; A-only "
                  "state-derivation suffices) → §83 ($0 stub closed-form "
                  "rule grid, B-S83 7/7 🔵, R3 winner at stub) → §83-FIRE "
                  "(the same 7 closed-form rules on REAL trained-saturated "
                  "ψ-state, B-S83-NOTE earned future-fire)"),
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire (g_train_flame_not_pytorch "
                      "evidence-anchor-clause carry — anima-physics "
                      "overlays on flame have upstream-GAP per §71 inbox "
                      "patch)"),
        "biology_anchor": ("Blackiston-Levin Xenopus tadpole ectopic-eye "
                          "visual learning (substrate-plasticity readout, "
                          "anchor only, NOT silicon-transfer claim); "
                          "prr:f1hv-bf1f spontaneous metacognition emergence "
                          "in RNN; cell-reports-physical-science Levin "
                          "field-mediated bioelectric prepatterning."),
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
        "rule_constants": {
            "TAU_VAR": TAU_VAR, "MAJ_COLLAPSE": MAJ_COLLAPSE,
            "PLAST_THRESHOLD": PLAST_THRESHOLD,
            "N_LOOP_STEPS": nL, "SEED": SEED,
            "PSI_VAC": PSI_VAC,
        },
        "grid":                  grid,
        "verdict_4corner":       verdict_4corner,
        "verdict":               verdict,
        "verdict_caveat":        verdict_caveat,
        "comparison_to_s83_stub": stub_s83,
        "comparison_to_s73_fire": fire_s73,
        "north_star_unchanged":      True,
        "milestone_unchanged":       "§15 + §51 + §72 (GOAL 미도달)",
        "capability_claim":          0,
        "deterministic":             True,
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({k: result[k] for k in (
        "verdict", "trained_saturated", "init_ce", "final_ce",
        "verdict_4corner")}, indent=2, ensure_ascii=False), flush=True)
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
    ap.add_argument("--loop-steps", type=int, default=20)
    args = ap.parse_args()
    cfg = dict(corpus=args.corpus, out_dir=args.out_dir, steps=args.steps,
               lr=args.lr, bsz=args.bsz, seed=args.seed,
               d_model=args.d_model, n_head=args.n_head,
               n_layer=args.n_layer, n_kv_head=args.n_kv_head,
               block_size=args.block_size, warmup=args.warmup,
               lambda_ctl=args.lambda_ctl, lambda_route=args.lambda_route,
               fwd_bsz=args.fwd_bsz, loop_steps=args.loop_steps)
    main(cfg)
