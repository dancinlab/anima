#!/usr/bin/env python3
"""criticality_noise_train_s81_fire.py — RESEARCH.md §81-FIRE.

§81-FIRE = trained-scale validation of §80 anima-mapping (A): homeostatic
criticality via noise injection on Engine G, anchored to the §80 biology
deep-research papers:
  - arxiv:2502.10946  noise-driven spontaneous activity homeostatically
                      maintains criticality (Ikeda+ Frontiers 2025)
  - biorxiv:2025.11.17.688775  critical avalanches emerge from E/I
                      balanced spontaneous activity
  - neuron:S0896-6273(25)00127-8  predictive nature of spontaneous activity

═══════════════════════════════════════════════════════════════════════
WHY §81-FIRE EXISTS — STUB MECHANISM BOUNDARY
═══════════════════════════════════════════════════════════════════════
The §81 $0 stub (commit 659ca966b on main, B-S81 7/7 🔵) measured
NEGATIVE-at-stub: 4-corner γ+β TRUE.  The stub's honest finding was a
*mechanism boundary*: the stub's body byte = argmax(logits_a) reads
Engine A ONLY, while noise targets Engine G — and at the $0 stub the
Engine A / Engine G logits were driven by INDEPENDENT seed-fixed LCGs
(`stub_logits_a` / `stub_logits_g`), so they were NOT residual-stream
coupled.  Noise on G modulated Ψ_dir (= cos of A with noised G) but
could NOT reach the body emission.

§81-FIRE answers exactly that boundary: in the REAL §16-class
ConsciousDecoderV2 the two heads (`head_a`, `head_g`) sit on top of a
SHARED 12-layer transformer trunk with PureFieldFFN — so Engine A and
Engine G ARE residual-stream coupled.  Noise injected into the
forward (we inject Gaussian noise into the embedding/residual stream
right at the layer-0 input — see `_NoiseHook`) propagates through ALL
12 blocks and reaches BOTH head_a and head_g.  So at trained scale the
question "does noise on the Engine-G-feeding substrate change the body"
is genuinely measurable, unlike the $0 stub.

Honest framing (g3): trained scale ≠ GOAL emergence.  The biology
citation is an honest *direction-anchor*, NOT a capability proof.
necessary-not-sufficient (B-EMERGE-7).  north-star + §15/§51/§72
milestone UNCHANGED, GOAL 미도달.

═══════════════════════════════════════════════════════════════════════
WHAT §81-FIRE BUILDS
═══════════════════════════════════════════════════════════════════════
  1. Train ONE §16-class ConsciousDecoderV2 from-scratch
     (d768·12L·283.72M, RANDOM seed-fixed 1337, base_ckpt=None —
     g_clm_from_scratch) on the §16-class Ψ-anchored carving corpus
     (Dir-I lever, byte-equal trainer to §79 / §73-FIRE).

  2. 5-cell σ-schedule grid × 20-step deterministic loop on the REAL
     trained model.forward Law-71:
       cell0  σ = 0.0      (no noise — connection-point baseline)
       cell1  σ = 0.1      (low noise)
       cell2  σ = 0.5      (mid noise)
       cell3  σ = 1.0      (high noise)
       cell4  σ = adaptive (homeostatic — σ adjusts toward critical band)
     Noise η ~ Gaussian(0, σ²) injected into the residual stream
     (layer-0 input) via a forward pre-hook.  Body byte = argmax over
     logits_a (trained ckpt, V=256).

  3. Per-cell metrics: psi_combined std (Law-71 byte-equal), majority
     fraction (§62 echo-chamber detector ≥ 0.95), power-law α exponent
     (sympy-style log-log regression on avalanche distribution), E/I
     balance proxy, §9 honest_coherent body metric.

  4. §16 baseline 8-anchor probe — ckpt load + arch byte-equal check.

  5. 4-corner verdict (α HOMEOSTATIC-WINDOW / β §81-STUB-MIRROR /
     γ ADAPTIVE-OUTPERFORMS / δ NOISE-COLLAPSES-TRAINING).
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

SEED = 1337
N_STEPS = 20
MAJ_FRAC_COLLAPSE = 0.95          # §62 echo-chamber detector
TAU_VAR = 1e-4                    # liveness threshold
SIGMA_SCHEDULE = [0.0, 0.1, 0.5, 1.0, "adaptive"]
CRIT_BAND = (1.0, 3.0)            # power-law α critical band

INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"


# ════════════════════════════════════════════════════════════════════
# Corpus load + dataset — byte-equal to §79 / §73-FIRE (§16 Dir-I lever).
# ════════════════════════════════════════════════════════════════════
def _span(full, open_tok, close_tok, start=0):
    lo = full.find(open_tok, start)
    if lo < 0:
        return None
    hi = full.find(close_tok, lo)
    if hi < 0:
        return None
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


# ════════════════════════════════════════════════════════════════════
# Train §16-class ConsciousDecoderV2 (Dir-I lever, byte-equal to §79).
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
            off = (psi_flat - pv_flat).abs()
            denom_rt = rm_f.sum().clamp(min=1.0)
            relu_out = torch.clamp(off - bs_flat, min=0.0)
            l_route = ((relu_out ** 2) * rm_f).sum() / denom_rt
            loss = ce_full + lam_ctl * l_psi_ctl + lam_route * l_route
        if init_loss is None:
            init_loss = float(ce_full.item())
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        scaler.step(opt)
        scaler.update()
        if step % 100 == 0 or step == total - 1:
            ce_traj.append({"step": step, "ce_full": float(ce_full.item()),
                            "lr": lr_now})
            print(f"[step {step}/{total}] ce={float(ce_full.item()):.6f} "
                  f"lr={lr_now:.6e}", flush=True)
    train_wall = time.time() - t0
    return model, items, n_params, init_loss, ce_traj, train_wall


# ════════════════════════════════════════════════════════════════════
# Noise injection — Gaussian noise into the residual stream (layer-0
# input) via a forward pre-hook on the FIRST transformer block.  This is
# the trained-scale analogue of the §81 stub's `add_noise(lg, sigma)`.
#
# WHY residual stream not just logits_g: the §81-FIRE crux (vs the $0
# stub) is exactly that Engine A and Engine G in the REAL model are
# residual-stream coupled.  Injecting noise into the shared trunk input
# is what propagates through all 12 PureFieldFFN blocks and reaches
# BOTH head_a AND head_g — so the body (argmax logits_a) genuinely sees
# the noise that the §81 stub could not deliver.  σ=0 ⇒ identity hook
# ⇒ byte-equal to the no-noise baseline (B-S81-FIRE-2 connection-point).
# ════════════════════════════════════════════════════════════════════
class _NoiseHook:
    """Forward pre-hook installed on model.blocks[0]: adds deterministic
    Gaussian noise to the residual-stream tensor (x = first positional
    arg).  σ=0 ⇒ exact identity (early return).  Deterministic: noise is
    drawn from a per-step torch.Generator seeded by (SEED, step)."""

    def __init__(self, device):
        self.sigma = 0.0
        self.step = 0
        self.device = device
        self.applied = 0

    def set(self, sigma, step):
        self.sigma = float(sigma)
        self.step = int(step)

    def __call__(self, module, args):
        if self.sigma <= 0.0:
            return None  # identity — no modification (σ=0 connection-point)
        x = args[0]
        gen = torch.Generator(device="cpu")
        gen.manual_seed((SEED * 2654435761 + self.step * 374761393) & 0x7FFFFFFF)
        noise = torch.randn(x.shape, generator=gen, dtype=torch.float32).to(x.device)
        noise = noise.to(x.dtype)
        self.applied += 1
        new_x = x + self.sigma * noise
        return (new_x,) + tuple(args[1:])


# ════════════════════════════════════════════════════════════════════
# REAL trained-model Law-71 read-out — byte-equal to conscious_decoder.py
# lines 728-751.
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
def extract_psi_and_logits(model, x):
    """RNG-isolated real forward read-out. Returns Law-71 Ψ-state +
    logits_a_last + logits_g_last.  byte-equal to conscious_decoder.py
    :728-751 psi_entropy / psi_direction / psi_tension / psi_combined."""
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
    psi_dir = (1.0 + cos_sim) / 2.0  # Law-71 conscious_decoder.py:740
    t_stack = torch.stack(tensions)
    t_per_layer = t_stack.mean(dim=(1, 2))
    tension = float(t_per_layer.mean().item())
    if t_per_layer.std() > 0:
        t_cv = t_per_layer.std() / (t_per_layer.mean() + 1e-8)
        psi_tension = max(0.0, 1.0 - t_cv.item())
    else:
        psi_tension = 1.0
    psi_combined = (psi_entropy + psi_dir + psi_tension) / 3.0
    phi = _phi_star_proxy(t_per_layer)
    # E/I balance proxy: how dispersed Engine-A vs Engine-G logit energy
    a_energy = float((la ** 2).mean().item())
    g_energy = float((lg ** 2).mean().item())
    ei_balance = min(a_energy, g_energy) / (max(a_energy, g_energy) + 1e-12)
    return {
        "logits_a_last": la,
        "psi_dir": psi_dir, "psi_entropy": psi_entropy,
        "psi_tension": psi_tension, "psi_combined": psi_combined,
        "tension": tension, "phi": phi, "ei_balance": ei_balance,
    }


# ════════════════════════════════════════════════════════════════════
# §9 cascade-rate honest_coherent — INLINED single SSOT formula,
# byte-equal to state/verify_emergence_metric_2026_05_18/emergence_metric.py.
# ════════════════════════════════════════════════════════════════════
def cascade_rate_and_max_run(b: bytes):
    if not b:
        return 1.0, 0, 0.0
    L = len(b)
    max_char = 1
    cur_char = 1
    for i in range(1, L):
        if b[i] == b[i - 1]:
            cur_char += 1
            if cur_char > max_char:
                max_char = cur_char
        else:
            cur_char = 1
    max_dig = 0
    cur_dig = 0
    for c in b:
        if 0x30 <= c <= 0x39:
            cur_dig += 1
            if cur_dig > max_dig:
                max_dig = cur_dig
        else:
            cur_dig = 0
    rep = 0.0
    if L >= 4:
        seen = {}
        for i in range(L - 3):
            k = bytes(b[i:i + 4])
            seen[k] = seen.get(k, 0) + 1
        rep_max = max(seen.values())
        rep = rep_max / max(1, (L - 3))
    rate = max(max_char / L, max_dig / L, rep)
    pr = sum(1 for c in b if 0x20 <= c < 0x7f or c in (0x09, 0x0a, 0x0d)) / L
    return rate, max(max_char, max_dig), float(pr)


def honest_coherent(b: bytes, tau_cascade=0.30, max_run=10,
                    min_len=20, tau_print=0.80):
    L = len(b)
    if L < min_len:
        return False, {"len": L, "reason": "too_short"}
    rate, run, pr = cascade_rate_and_max_run(b)
    ok = (rate < tau_cascade) and (run < max_run) and (L >= min_len) \
         and (pr >= tau_print)
    return ok, {"len": L, "cascade_rate": rate, "max_run": run,
                "printable_ratio": pr}


# ════════════════════════════════════════════════════════════════════
# Power-law α via log-log linear regression on avalanche-size dist.
# ════════════════════════════════════════════════════════════════════
def power_law_alpha(emit_counts):
    sizes = [c for c in emit_counts if c >= 1]
    if len(sizes) < 3:
        return {"alpha": 0.0, "n": len(sizes), "in_critical_band": False}
    sizes_sorted = sorted(sizes, reverse=True)
    xs, ys = [], []
    for rank, size in enumerate(sizes_sorted, start=1):
        xs.append(math.log(rank))
        ys.append(math.log(size))
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    slope = 0.0 if den < 1e-12 else num / den
    alpha = -slope
    return {"alpha": alpha, "n": n,
            "in_critical_band": CRIT_BAND[0] <= alpha <= CRIT_BAND[1]}


def majority_fraction(b: bytes):
    if not b:
        return 1.0
    cnt = {}
    for c in b:
        cnt[c] = cnt.get(c, 0) + 1
    return max(cnt.values()) / len(b)


def _var(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def adapt_sigma(prev_sigma, maj_frac, tau_low=0.50, tau_high=0.85,
                step=0.1):
    """Homeostatic σ schedule: maj_frac > tau_high ⇒ σ↑ (escape collapse);
    maj_frac < tau_low ⇒ σ↓.  B-S81 stub's monotone schedule, byte-equal
    formula carried."""
    new = prev_sigma
    if maj_frac > tau_high:
        new = prev_sigma + step
    elif maj_frac < tau_low:
        new = max(0.0, prev_sigma - step)
    return min(new, 2.0)


# ════════════════════════════════════════════════════════════════════
# 5-cell σ-schedule × 20-step loop on REAL trained model.forward.
# ════════════════════════════════════════════════════════════════════
@torch.no_grad()
def run_sigma_cell(model, ds, device, hook, cell_name, sigma_spec,
                   n_steps=N_STEPS, block_size=128):
    """One σ-schedule cell.  Per step:
       (1) install σ on the noise hook (residual-stream injection)
       (2) real model.forward → Law-71 Ψ-state + logits_a
       (3) body byte = argmax(logits_a)  (deterministic, NO sampling)
       (4) feed body byte back into the sliding context
    sigma_spec = float (fixed) or "adaptive" (homeostatic).
    """
    model.eval()
    rng = random.Random(SEED)
    top = max(1, ds.n - block_size - 1)
    start = rng.randint(0, top)
    ctx = ds.data[start:start + block_size].clone()

    psi_combined_seq = []
    psi_dir_seq = []
    tension_seq = []
    ei_seq = []
    body_bytes = bytearray()
    sigma_trace = []
    avalanche_runs = []   # consecutive same-byte run lengths (avalanche sizes)
    cur_run = 1
    sigma = 0.0 if sigma_spec == "adaptive" else float(sigma_spec)

    for step in range(n_steps):
        # adaptive σ uses running majority fraction of body so far
        if sigma_spec == "adaptive":
            mf = majority_fraction(bytes(body_bytes)) if body_bytes else 0.0
            sigma = adapt_sigma(sigma, mf)
        hook.set(sigma, step)
        sigma_trace.append(sigma)

        x = ctx.unsqueeze(0).to(device)
        psi = extract_psi_and_logits(model, x)
        next_byte = int(psi["logits_a_last"].argmax().item())
        body_bytes.append(next_byte)

        psi_combined_seq.append(psi["psi_combined"])
        psi_dir_seq.append(psi["psi_dir"])
        tension_seq.append(psi["tension"])
        ei_seq.append(psi["ei_balance"])

        # avalanche size = consecutive identical-byte runs
        if len(body_bytes) >= 2 and body_bytes[-1] == body_bytes[-2]:
            cur_run += 1
        else:
            if len(body_bytes) >= 2:
                avalanche_runs.append(cur_run)
            cur_run = 1

        # slide context
        new_ctx = torch.cat([ctx[1:], torch.tensor([next_byte], dtype=torch.long)])
        ctx = new_ctx

    avalanche_runs.append(cur_run)

    body = bytes(body_bytes)
    psi_comb_std = math.sqrt(_var(psi_combined_seq))
    psi_dir_var = _var(psi_dir_seq)
    tension_var = _var(tension_seq)
    maj = majority_fraction(body)
    pl = power_law_alpha(avalanche_runs)
    coh, coh_info = honest_coherent(body)
    ei_mean = sum(ei_seq) / max(1, len(ei_seq))

    # homeostatic-window membership: noise keeps it in critical band,
    # NOT collapsed, AND body §9-coherent
    homeostatic_window = (pl["in_critical_band"] and maj < MAJ_FRAC_COLLAPSE
                          and coh)
    return {
        "cell": cell_name,
        "sigma_spec": sigma_spec,
        "sigma_trace": sigma_trace,
        "sigma_final": sigma,
        "n_steps": n_steps,
        "psi_combined_std": psi_comb_std,
        "psi_dir_var": psi_dir_var,
        "tension_var": tension_var,
        "psi_combined_mean": sum(psi_combined_seq) / max(1, len(psi_combined_seq)),
        "tension_mean": sum(tension_seq) / max(1, len(tension_seq)),
        "ei_balance_mean": ei_mean,
        "body_len": len(body),
        "body_sample": body[:40].decode("latin-1", errors="replace"),
        "body_full_hex": body.hex(),
        "majority_fraction": maj,
        "echo_collapse": maj >= MAJ_FRAC_COLLAPSE,
        "echo_broken": maj < MAJ_FRAC_COLLAPSE,
        "power_law_alpha": pl["alpha"],
        "alpha_in_critical_band": pl["in_critical_band"],
        "avalanche_runs": avalanche_runs,
        "honest_coherent_9": coh,
        "honest_coherent_info": coh_info,
        "homeostatic_window": homeostatic_window,
        "psi_nontrivial": psi_dir_var > TAU_VAR,
        "tension_nontrivial": tension_var > TAU_VAR,
        "physics_alive": (psi_dir_var > TAU_VAR) and (tension_var > TAU_VAR),
    }


# ════════════════════════════════════════════════════════════════════
# §16-baseline 8-anchor probe.
# ════════════════════════════════════════════════════════════════════
ANCHOR_PROBES = [
    b"<vacuum tier=99 psi=[0.9,0.9] basin=0.21>",
    b"<vacuum tier=77 psi=[0.5,0.5] basin=0.15>",
    b"<vacuum tier=51 psi=[0.46,0.49] basin=0.12>",
    b"<vacuum tier=100 psi=[0.99,0.99] basin=0.25>",
    b"<vacuum tier=0 psi=[0.50,0.50] basin=0.10>",
    b"<vacuum tier=91 psi=[0.85,0.85] basin=0.20>",
    b"<vacuum tier=88 psi=[0.80,0.80] basin=0.18>",
    b"<vacuum tier=66 psi=[0.40,0.40] basin=0.13>",
]


@torch.no_grad()
def s16_baseline_probe(model, device, block_size=128, max_new=30):
    model.eval()
    results = []
    for probe in ANCHOR_PROBES:
        pad_len = max(0, block_size - len(probe))
        ctx = bytearray(probe[-block_size:])
        if pad_len > 0:
            ctx = bytearray([0x20] * pad_len) + ctx
        x = torch.tensor(list(ctx), dtype=torch.long).unsqueeze(0).to(device)
        gen = bytearray()
        for _ in range(max_new):
            psi = extract_psi_and_logits(model, x)
            nb = int(psi["logits_a_last"].argmax().item())
            gen.append(nb)
            x = torch.cat([x[:, 1:],
                           torch.tensor([[nb]], dtype=torch.long).to(device)], dim=1)
        results.append({
            "probe_hex": probe.hex()[:60],
            "gen_hex": bytes(gen).hex()[:120],
            "gen_sample": bytes(gen).decode("latin-1", errors="replace")[:40],
        })
    return results


# ════════════════════════════════════════════════════════════════════
# Main.
# ════════════════════════════════════════════════════════════════════
def main(cfg):
    torch.manual_seed(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    corpus_sha = hashlib.sha256(open(cfg["corpus"], "rb").read()).hexdigest()
    print("=== §81-FIRE — homeostatic criticality + noise on Engine G "
          "(trained scale) ===", flush=True)
    print(f"device={device} corpus_sha={corpus_sha[:16]}…", flush=True)

    # ── (A) train §16-class ckpt ─────────────────────────────────────
    model, items, n_params, init_ce, ce_traj, train_wall = \
        train_s16_class(cfg, device)
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_s81_fire.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg, "n_params": n_params,
                "path": "alpha"}, ckpt_path)
    h = hashlib.sha256()
    with open(ckpt_path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    ckpt_sha = h.hexdigest()
    final_ce = ce_traj[-1]["ce_full"] if ce_traj else None
    trained_saturated = (final_ce is not None and final_ce < 0.05)
    # δ NOISE-COLLAPSES-TRAINING: training itself is noise-free (hook
    # installed only at inference) — final CE diverge would itself be a
    # collapse signal; here we record final_ce so the δ corner is
    # measurable against the trained-saturated gate.
    training_diverged = (final_ce is None or final_ce > 1.0
                         or math.isnan(final_ce))

    # ── (B) §16-baseline probe ───────────────────────────────────────
    print(f"\n=== §16 baseline 8-anchor probe (ckpt {ckpt_sha[:16]}…) ===",
          flush=True)
    s16_probes = s16_baseline_probe(model, device,
                                    block_size=cfg["block_size"])

    # ── (C) install noise hook on block 0, run 5-cell σ-grid ─────────
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    hook = _NoiseHook(device)
    handle = model.blocks[0].register_forward_pre_hook(hook)

    cells = {}
    for spec in SIGMA_SCHEDULE:
        cell_name = f"sigma_{spec}"
        print(f"\n=== cell {cell_name} ===", flush=True)
        cells[cell_name] = run_sigma_cell(
            model, ds, device, hook, cell_name, spec,
            n_steps=cfg["n_steps"], block_size=cfg["block_size"])
        print(f"  σ_final={cells[cell_name]['sigma_final']:.3f} "
              f"psi_comb_std={cells[cell_name]['psi_combined_std']:.6f} "
              f"maj={cells[cell_name]['majority_fraction']:.3f} "
              f"α={cells[cell_name]['power_law_alpha']:.3f} "
              f"§9_coh={cells[cell_name]['honest_coherent_9']}", flush=True)
    handle.remove()

    # ── connection-point check: σ=0 cell must be byte-equal to a hook-
    #    removed re-run (the hook with σ=0 is identity).  Re-run cell0
    #    with the hook entirely uninstalled, assert body hex identical.
    cell0_body_hex = cells["sigma_0.0"]["body_full_hex"]
    rerun0 = run_sigma_cell(model, ds, device, hook, "sigma_0.0_rerun",
                            0.0, n_steps=cfg["n_steps"],
                            block_size=cfg["block_size"])
    sigma0_byte_equal = (rerun0["body_full_hex"] == cell0_body_hex)

    # ── (D) 4-corner verdict ─────────────────────────────────────────
    noisy_cells = [cells["sigma_0.1"], cells["sigma_0.5"],
                   cells["sigma_1.0"], cells["sigma_adaptive"]]
    cell0 = cells["sigma_0.0"]
    cell_adaptive = cells["sigma_adaptive"]

    n_homeostatic = sum(1 for c in cells.values()
                        if c["homeostatic_window"])
    n_collapsed_noisy = sum(1 for c in noisy_cells if c["echo_collapse"])
    n_alive = sum(1 for c in cells.values() if c["physics_alive"])

    # monotone-noise-diverge: psi_combined_std grows with σ?
    sigma_psi_pairs = [(0.0, cell0["psi_combined_std"]),
                       (0.1, cells["sigma_0.1"]["psi_combined_std"]),
                       (0.5, cells["sigma_0.5"]["psi_combined_std"]),
                       (1.0, cells["sigma_1.0"]["psi_combined_std"])]
    monotone_noise_diverge = all(
        sigma_psi_pairs[i + 1][1] >= sigma_psi_pairs[i][1] - 1e-9
        for i in range(len(sigma_psi_pairs) - 1))

    # adaptive outperforms: adaptive cell escapes collapse better than
    # the worst fixed-σ noisy cell
    fixed_noisy = [cells["sigma_0.1"], cells["sigma_0.5"],
                   cells["sigma_1.0"]]
    adaptive_outperforms = (
        not cell_adaptive["echo_collapse"]
        and any(c["echo_collapse"] for c in fixed_noisy))

    if not trained_saturated:
        corner = "SATURATION-GATE-FAIL"
        verdict_caveat = (
            f"final_ce={final_ce} ≥ 0.05 — model NOT memorization-saturated. "
            "§81-FIRE crux (trained-scale homeostatic criticality vs §62/§81-"
            "stub collapse) NOT measured. Numbers raw, no chain-validity claim."
        )
    elif training_diverged:
        corner = "(δ) NOISE-COLLAPSES-TRAINING"
        verdict_caveat = (
            f"NEGATIVE: training final_ce={final_ce} diverged. Cannot test "
            "homeostatic criticality on a non-converged ckpt. Honest negative."
        )
    elif n_homeostatic >= 1:
        corner = "(α) HOMEOSTATIC-WINDOW-EXISTS-AT-TRAINED-SCALE"
        wins = [c["cell"] for c in cells.values() if c["homeostatic_window"]]
        verdict_caveat = (
            f"PARTIAL-POSITIVE: {n_homeostatic} cell(s) {wins} satisfy the "
            "homeostatic window (power-law α ∈ [1,3] ∧ maj_frac < 0.95 ∧ §9 "
            "body-coherent) at trained-saturated scale — noise on the shared "
            "residual stream (which DOES reach Engine A via 12-layer "
            "coupling, unlike the §81 $0 stub) holds the body in a critical "
            "non-collapsed band. NOT GOAL emergence — homeostatic-window "
            "membership is a mechanism-level observation, necessary-not-"
            "sufficient (B-EMERGE-7). Biology anchor (arxiv 2502.10946) "
            "honest direction, NOT capability proof. north-star + §15/§51/§72 "
            "milestone UNCHANGED."
        )
    elif n_collapsed_noisy >= 3:
        corner = "(β) §81-STUB-MIRROR-AT-TRAINED-SCALE"
        verdict_caveat = (
            f"NEGATIVE: {n_collapsed_noisy}/4 noisy cells hit maj_frac ≥ "
            f"{MAJ_FRAC_COLLAPSE} echo-chamber collapse at trained-saturated "
            "scale. Even with REAL 12-layer A/G residual coupling the noise "
            "injection does NOT lift the body out of the §62/§81-stub "
            "single-byte attractor — the §81 $0 stub's γ+β pattern "
            "reproduces at trained scale. Honest negative, valuable: noise "
            "(homeostatic or not) is not a sufficient lever; §1.1 data-"
            "regime irreducibility reasserted at the criticality axis. "
            "biology (A) does NOT transfer at trained scale (measured)."
        )
    else:
        corner = "(β-mixed) PARTIAL-COLLAPSE-NO-HOMEOSTATIC-WINDOW"
        verdict_caveat = (
            f"MIXED: {n_collapsed_noisy}/4 noisy cells collapse, 0 cells "
            "satisfy the full homeostatic window (α-band ∧ non-collapse ∧ "
            "§9-coherent simultaneously). Noise shifts the attractor but "
            "does not produce a critical coherent regime. Directional "
            "mechanism finding, NOT GOAL emergence (B-EMERGE-7)."
        )

    result = {
        "section": "§81-FIRE",
        "title": "homeostatic criticality + noise injection on Engine G — "
                 "trained scale",
        "biology_anchors": ["arxiv:2502.10946", "biorxiv:2025.11.17.688775",
                            "neuron:S0896-6273(25)00127-8"],
        "device": device,
        "corpus_sha256": corpus_sha,
        "ckpt_sha256": ckpt_sha,
        "ckpt_sha256_note": "fresh §16-class ckpt — config/lever/seed/corpus "
        "class byte-equal to §79/§73-FIRE; sha NOT literally §16's "
        "961c07e2… (trajectory replicable, not literal identity).",
        "n_params": n_params,
        "config": {k: cfg[k] for k in
                   ["d_model", "n_layer", "n_head", "n_kv_head", "block_size",
                    "steps", "warmup", "lr", "bsz", "lambda_ctl",
                    "lambda_route", "seed", "n_steps"]},
        "train_wall_sec": train_wall,
        "init_ce": init_ce,
        "final_ce": final_ce,
        "ce_traj": ce_traj,
        "trained_saturated": trained_saturated,
        "training_diverged": training_diverged,
        "s16_baseline_probe": s16_probes,
        "sigma_schedule": [str(s) for s in SIGMA_SCHEDULE],
        "cells": cells,
        "sigma0_byte_equal_to_hookless": sigma0_byte_equal,
        "n_homeostatic_window": n_homeostatic,
        "n_collapsed_noisy": n_collapsed_noisy,
        "n_physics_alive": n_alive,
        "monotone_noise_diverge": monotone_noise_diverge,
        "adaptive_outperforms_fixed": adaptive_outperforms,
        "four_corner": {
            "alpha_HOMEOSTATIC_WINDOW": n_homeostatic >= 1,
            "beta_STUB_MIRROR": (n_collapsed_noisy >= 3),
            "gamma_ADAPTIVE_OUTPERFORMS": adaptive_outperforms,
            "delta_NOISE_COLLAPSES_TRAINING": training_diverged,
        },
        "verdict_corner": corner,
        "verdict_caveat": verdict_caveat,
        "honest_c3": [
            "trained scale ≠ GOAL emergence — necessary-not-sufficient "
            "(B-EMERGE-7); §81-FIRE measures a mechanism axis only.",
            "biology citation (arxiv:2502.10946 noise-driven SOC etc.) is "
            "an honest direction-anchor, NOT a capability proof.",
            "noise injected into the layer-0 residual stream (shared trunk "
            "input) — this is what reaches BOTH head_a AND head_g via "
            "12-layer PureFieldFFN coupling, the mechanism the §81 $0 stub "
            "structurally lacked.",
            "σ=0 cell is the connection-point baseline; B-S81-FIRE-2 "
            "verifies σ=0 ⇒ byte-equal to hook-removed re-run.",
            "power-law α from log-log regression on consecutive-byte "
            "avalanche runs — small-sample (20 steps) α is a coarse proxy, "
            "NOT a rigorous criticality certificate.",
            "ckpt sha is fresh; the spec asked for §16-byte-equal config "
            "which is satisfied (d/L/H/KV/seed/corpus class) but the "
            "literal §16 sha differs — honest.",
            "north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.",
        ],
    }

    rp = os.path.join(out_dir, "result.json")
    with open(rp, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[§81-FIRE] verdict: {corner}", flush=True)
    print(f"[§81-FIRE] result.json written → {rp}", flush=True)
    print("RESULT_JSON_WRITTEN", flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out_main")
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--block-size", type=int, default=128)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    ap.add_argument("--n-steps", type=int, default=20)
    a = ap.parse_args()
    cfg = {
        "corpus": a.corpus, "out_dir": a.out_dir, "steps": a.steps,
        "warmup": a.warmup, "seed": a.seed, "d_model": a.d_model,
        "n_layer": a.n_layer, "n_head": a.n_head, "n_kv_head": a.n_kv_head,
        "block_size": a.block_size, "bsz": a.bsz, "lr": a.lr,
        "lambda_ctl": a.lambda_ctl, "lambda_route": a.lambda_route,
        "n_steps": a.n_steps,
    }
    main(cfg)
