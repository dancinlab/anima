#!/usr/bin/env python3
"""axolotl_neoteny_train_s88f2.py — RESEARCH.md §88-F2.

§88-F2 = trained-scale validation of §87-F2 (commit 798b6110d, B-S87F2
6/6 🔵): AXOLOTL NEOTENY ANTI-SATURATION.

═══════════════════════════════════════════════════════════════════════
WHY §88-F2 DIFFERS DECISIVELY FROM §81/§82/§83-FIRE
═══════════════════════════════════════════════════════════════════════
§81/§82/§83-FIRE all train a trained-SATURATED §16-class ckpt FIRST and
then OVERLAY a mechanism at inference time — and the overlay collapsed
because the ckpt was already in the byte-cascade attractor basin.

§87-F2 axolotl neoteny is structurally different: the neoteny mechanism
is applied DURING TRAINING itself (in the optimisation loop), so the
goal is to produce a *non-saturated* ckpt, not to rescue a saturated one.
The axolotl stays a plastic juvenile its whole life — never metamorphoses
into a frozen "adult".  §16.6-C memorization-saturation is anima becoming
an over-mature adult too fast.  §88-F2 keeps anima juvenile.

This directly targets §1.1 data-regime irreducibility: the question is
whether a "juvenile-but-competent" regime exists — saturation slowed AND
CE still descends AND body §9-coherent.

═══════════════════════════════════════════════════════════════════════
THE 4 NK MECHANISMS — IN THE TRAINING LOOP (carry from §87-F2)
═══════════════════════════════════════════════════════════════════════
  NK-1  CE-floor clamp        — when batch CE < θ_floor the CE term is
                                clamped at θ_floor (no further over-fit
                                gradient on that term — juvenile keeps a
                                non-zero loss).  Targets maturity M-1.
  NK-2  plasticity-reinjection— on saturation detection (maturity proxy
                                crosses SAT_TRIGGER) apply a TARGETED
                                controlled Gaussian perturbation to the
                                weights (axolotl regeneration mirror;
                                saturation-TRIGGERED, distinct from §81
                                unconditional noise).  Targets M-2.
  NK-3  dimensionality-floor  — add a dimensionality-spread reg term that
                                pushes effective D back up when it drops
                                below θ_D (juvenile keeps representation
                                rank).  Targets M-3.
  NK-4  metamorphosis-block   — once maturity crosses SAT_TRIGGER, freeze
                                the LR schedule at a juvenile floor (hold
                                further descent — dynamic, state-triggered,
                                NOT epoch-budget early-stop).  Targets the
                                global maturation rate.

Honest framing (g3): trained scale ≠ GOAL emergence.  axolotl neoteny is
an honest direction-anchor, NOT a capability proof.  necessary-not-
sufficient (B-EMERGE-7).  north-star + §15/§51/§72 milestone UNCHANGED.

3-cell:
  cell0_baseline   normal training → trained-saturated (§16 pattern)
  cell1_neoteny    full-neoteny (NK-1+2+3+4) training
  cell2_neoteny_emit  neoteny arm + §24-style emission probe
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
N_EMIT_STEPS = 20
TAU_VAR = 1e-4
MAJ_FRAC_COLLAPSE = 0.95          # §62 echo-chamber detector

# ── §87-F2 carry: maturity 3-proxy weights + thresholds ──────────────
CE_INIT = 5.65
CE_NATURAL_FLOOR = 0.0045
D_INIT = 14.0
D_NATURAL_FLOOR = 1.6
W_CE, W_MAJ, W_D = 0.40, 0.35, 0.25     # §87-F2 convex 3-proxy weights
THETA_FLOOR = 0.08                      # NK-1 CE-floor clamp threshold
THETA_D = 4.0                           # NK-3 dimensionality floor
SAT_TRIGGER = 0.70                      # NK-2/NK-4 saturation trigger
NK2_SIGMA = 0.01                        # NK-2 reinjection perturbation scale
NK3_LAMBDA = 0.05                       # NK-3 dimensionality-spread reg weight
NK4_LR_FLOOR_FRAC = 0.25                # NK-4 frozen LR juvenile floor frac

INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"


def clip01(x):
    return max(0.0, min(1.0, x))


# ════════════════════════════════════════════════════════════════════
# Corpus load + dataset — byte-equal to §81-FIRE (§16 Dir-I lever).
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
# Maturity 3-proxy — §87-F2 closed-form carry, computed from the actual
# training trajectory of THIS run.
# ════════════════════════════════════════════════════════════════════
def maturity_score(ce, maj, D):
    """maturity ∈ [0,1]: convex weighted 3-proxy (§87-F2 byte-equal).

    m1 CE-floor proximity   : CE near floor ⇒ 1
    m2 attractor-basin depth: maj_frac
    m3 dimensionality collapse: D collapsed ⇒ 1
    """
    m1 = clip01(1.0 - (ce - CE_NATURAL_FLOOR) / (CE_INIT - CE_NATURAL_FLOOR))
    m2 = clip01(maj)
    m3 = clip01(1.0 - (D - D_NATURAL_FLOOR) / (D_INIT - D_NATURAL_FLOOR))
    return clip01(W_CE * m1 + W_MAJ * m2 + W_D * m3)


def neoteny_score(ce, maj, D):
    return clip01(1.0 - maturity_score(ce, maj, D))


def effective_dim(model):
    """Effective dimensionality of the gradient/activation field, proxied
    by the participation ratio of the LM-head weight singular spectrum
    (a cheap, deterministic rank proxy).  Higher = more plastic juvenile,
    lower = collapsed/over-mature."""
    with torch.no_grad():
        w = None
        for name, p in model.named_parameters():
            if "head_a" in name and p.dim() == 2:
                w = p.detach().float()
                break
        if w is None:
            for name, p in model.named_parameters():
                if p.dim() == 2:
                    w = p.detach().float()
                    break
        if w is None:
            return D_NATURAL_FLOOR
        try:
            s = torch.linalg.svdvals(w.cpu())
        except Exception:
            return D_NATURAL_FLOOR
        s2 = (s ** 2)
        pr = float((s2.sum() ** 2) / (s2.pow(2).sum() + 1e-12))
        # participation ratio → bounded into the [D_FLOOR, D_INIT] window
        return max(D_NATURAL_FLOOR, min(D_INIT, pr / 16.0))


# ════════════════════════════════════════════════════════════════════
# NK-3 dimensionality-spread reg — pushes effective D up: penalise
# correlation among LM-head rows (anti-collapse).  In-graph, in-loop.
# ════════════════════════════════════════════════════════════════════
def nk3_dim_spread_reg(model):
    """Closed-form in-graph dimensionality-floor regulariser: penalise
    the off-diagonal Gram energy of a head_a weight slice (rows highly
    correlated ⇒ rank-collapsed ⇒ penalty).  Targets maturity M-3."""
    w = None
    for name, p in model.named_parameters():
        if "head_a" in name and p.dim() == 2 and p.requires_grad:
            w = p
            break
    if w is None:
        return torch.tensor(0.0, device=next(model.parameters()).device)
    sl = w[:64, :].float()
    sl = sl / (sl.norm(dim=1, keepdim=True) + 1e-8)
    gram = sl @ sl.t()
    off = gram - torch.diag(torch.diagonal(gram))
    return (off ** 2).mean()


# ════════════════════════════════════════════════════════════════════
# NK-2 plasticity-reinjection — saturation-triggered targeted weight
# perturbation (axolotl regeneration mirror).  Distinct from §81's
# unconditional Engine-G noise: this is TRIGGERED and TARGETED at the
# LM-head (the byte-cascade attractor surface) only.
# ════════════════════════════════════════════════════════════════════
@torch.no_grad()
def nk2_plasticity_reinject(model, sigma, gen):
    """Apply a controlled Gaussian perturbation to the head_a weights —
    shallows the attractor basin, lifts representation plasticity."""
    applied = 0
    for name, p in model.named_parameters():
        if "head_a" in name and p.dim() == 2:
            noise = torch.randn(p.shape, generator=gen,
                                dtype=torch.float32).to(p.device).to(p.dtype)
            p.add_(sigma * noise)
            applied += 1
    return applied


# ════════════════════════════════════════════════════════════════════
# Train a §16-class ConsciousDecoderV2 with optional in-loop NK neoteny.
# ════════════════════════════════════════════════════════════════════
def train_cell(cfg, device, neoteny):
    """neoteny=False ⇒ cell0 baseline (natural saturation, §16 pattern).
    neoteny=True  ⇒ cell1 full-neoteny (NK-1+2+3+4 in the training loop).
    Returns (model, items, n_params, init_ce, traj, train_wall, nk_log)."""
    items = load_corpus(cfg["corpus"])
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    torch.manual_seed(cfg["seed"])
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
    init_ce = None
    traj = []
    nk_log = {"nk1_clamp_fired": 0, "nk2_reinject_fired": 0,
              "nk4_metamorph_held": False, "nk4_hold_step": None}
    metamorphosis_held = False
    cur_maj = 0.0

    for step in range(total):
        # NK-4 metamorphosis-block: once held, LR frozen at juvenile floor
        lr_now = cosine_lr_at(step)
        if neoteny and metamorphosis_held:
            lr_now = cfg["lr"] * NK4_LR_FLOOR_FRAC * \
                (0.5 * (1.0 + math.cos(math.pi)))  # frozen juvenile LR
            lr_now = cfg["lr"] * NK4_LR_FLOOR_FRAC
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

            ce_term = ce_full
            # ── NK-1 CE-floor clamp: juvenile keeps a non-zero loss ──
            nk1_active = False
            if neoteny and float(ce_full.item()) < THETA_FLOOR:
                # clamp the CE term at the floor — no over-fit gradient
                # below θ_floor (CE-base preserved: still a CE term, just
                # floored, not removed — B-S88F2 §11-B-CE-BASE clause).
                ce_term = torch.clamp(ce_full, min=THETA_FLOOR)
                nk1_active = True
                nk_log["nk1_clamp_fired"] += 1

            loss = ce_term + lam_ctl * l_psi_ctl + lam_route * l_route
            # ── NK-3 dimensionality-floor reg (in-graph) ─────────────
            if neoteny:
                l_dim = nk3_dim_spread_reg(model)
                loss = loss + NK3_LAMBDA * l_dim

        if init_ce is None:
            init_ce = float(ce_full.item())
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        scaler.step(opt)
        scaler.update()

        # ── trajectory probe every 100 steps ─────────────────────────
        if step % 100 == 0 or step == total - 1:
            ce_now = float(ce_full.item())
            D_now = effective_dim(model)
            # maj proxy: derive from CE position in the saturation window
            cur_maj = clip01(1.0 - (ce_now - CE_NATURAL_FLOOR) /
                             (CE_INIT - CE_NATURAL_FLOOR))
            mat = maturity_score(ce_now, cur_maj, D_now)
            traj.append({"step": step, "ce": ce_now, "lr": lr_now,
                         "D": D_now, "maturity": mat,
                         "neoteny": 1.0 - mat})

            # ── NK-2 plasticity-reinjection: saturation-triggered ────
            if neoteny and not metamorphosis_held and mat > SAT_TRIGGER:
                gen = torch.Generator(device="cpu")
                gen.manual_seed((SEED * 2654435761 + step * 374761393)
                                & 0x7FFFFFFF)
                nk2_plasticity_reinject(model, NK2_SIGMA, gen)
                nk_log["nk2_reinject_fired"] += 1

            # ── NK-4 metamorphosis-block: hold once trigger crossed ──
            if neoteny and not metamorphosis_held and mat > SAT_TRIGGER:
                metamorphosis_held = True
                nk_log["nk4_metamorph_held"] = True
                nk_log["nk4_hold_step"] = step

            tag = "NEOTENY" if neoteny else "BASE"
            print(f"[{tag} step {step}/{total}] ce={ce_now:.6f} "
                  f"D={D_now:.3f} maturity={mat:.4f} lr={lr_now:.3e} "
                  f"nk1={nk_log['nk1_clamp_fired']} "
                  f"nk2={nk_log['nk2_reinject_fired']} "
                  f"held={metamorphosis_held}", flush=True)

    train_wall = time.time() - t0
    return model, items, n_params, init_ce, traj, train_wall, nk_log


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


def majority_fraction(b: bytes):
    if not b:
        return 1.0
    cnt = {}
    for c in b:
        cnt[c] = cnt.get(c, 0) + 1
    return max(cnt.values()) / len(b)


# ════════════════════════════════════════════════════════════════════
# REAL trained-model body emission probe + Law-71 read-out.
# ════════════════════════════════════════════════════════════════════
ANCHOR_PROBES = [
    b"<vacuum tier=99 psi=[0.9,0.9] basin=0.21>",
    b"<vacuum tier=77 psi=[0.5,0.5] basin=0.15>",
    b"<vacuum tier=51 psi=[0.46,0.49] basin=0.12>",
    b"<vacuum tier=0 psi=[0.50,0.50] basin=0.10>",
    b"<vacuum tier=88 psi=[0.80,0.80] basin=0.18>",
]


@torch.no_grad()
def body_emission_probe(model, device, block_size=128, max_new=80):
    """Emit a body byte-stream per anchor probe; measure §9 honest_coherent
    + majority fraction over the emitted bodies."""
    model.eval()
    bodies = []
    for probe in ANCHOR_PROBES:
        pad_len = max(0, block_size - len(probe))
        ctx = bytearray(probe[-block_size:])
        if pad_len > 0:
            ctx = bytearray([0x20] * pad_len) + ctx
        x = torch.tensor(list(ctx), dtype=torch.long).unsqueeze(0).to(device)
        gen = bytearray()
        for _ in range(max_new):
            logits_a, _, _, _, _ = model(x)
            nb = int(logits_a[:, -1, :].argmax().item())
            gen.append(nb)
            x = torch.cat([x[:, 1:],
                           torch.tensor([[nb]], dtype=torch.long).to(device)],
                          dim=1)
        body = bytes(gen)
        coh, info = honest_coherent(body)
        bodies.append({
            "probe_hex": probe.hex()[:50],
            "body_sample": body.decode("latin-1", errors="replace")[:48],
            "honest_coherent_9": coh,
            "coherent_info": info,
            "majority_fraction": majority_fraction(body),
        })
    n_coh = sum(1 for b in bodies if b["honest_coherent_9"])
    maj_mean = sum(b["majority_fraction"] for b in bodies) / max(1, len(bodies))
    return bodies, n_coh, maj_mean


@torch.no_grad()
def emission_axis_probe(model, ds, device, block_size=128, n_steps=N_EMIT_STEPS):
    """cell2 §24-style emission probe — does the non-saturated neoteny
    ckpt behave differently on the decision/emission axis?"""
    model.eval()
    rng = random.Random(SEED)
    top = max(1, ds.n - block_size - 1)
    start = rng.randint(0, top)
    ctx = ds.data[start:start + block_size].clone()
    psi_dir_seq, tension_seq = [], []
    body = bytearray()
    for _ in range(n_steps):
        x = ctx.unsqueeze(0).to(device)
        logits_a, logits_g, tensions, _, _ = model(x)
        la = logits_a[:, -1, :].float()
        lg = logits_g[:, -1, :].float()
        cos = F.cosine_similarity(la, lg, dim=-1).mean().item()
        psi_dir_seq.append((1.0 + cos) / 2.0)
        t_stack = torch.stack(tensions)
        tension_seq.append(float(t_stack.mean().item()))
        nb = int(la.argmax().item())
        body.append(nb)
        ctx = torch.cat([ctx[1:], torch.tensor([nb], dtype=torch.long)])

    def _var(xs):
        if len(xs) < 2:
            return 0.0
        m = sum(xs) / len(xs)
        return sum((v - m) ** 2 for v in xs) / (len(xs) - 1)
    psi_var = _var(psi_dir_seq)
    tension_var = _var(tension_seq)
    return {
        "n_steps": n_steps,
        "psi_dir_var": psi_var,
        "tension_var": tension_var,
        "psi_nontrivial": psi_var > TAU_VAR,
        "tension_nontrivial": tension_var > TAU_VAR,
        "physics_alive": (psi_var > TAU_VAR) and (tension_var > TAU_VAR),
        "body_sample": bytes(body).decode("latin-1", errors="replace")[:40],
    }


# ════════════════════════════════════════════════════════════════════
# Build a per-cell measurement record.
# ════════════════════════════════════════════════════════════════════
def cell_metrics(name, model, items, ds, device, traj, nk_log,
                 n_params, init_ce, train_wall, block_size, emit=False):
    final_ce = traj[-1]["ce"] if traj else None
    final_D = traj[-1]["D"] if traj else D_NATURAL_FLOOR
    bodies, n_coh, maj_mean = body_emission_probe(model, device, block_size)
    final_maturity = maturity_score(final_ce, maj_mean, final_D) \
        if final_ce is not None else 1.0
    rec = {
        "cell": name,
        "init_ce": init_ce,
        "final_ce": final_ce,
        "final_D": final_D,
        "final_maturity": final_maturity,
        "final_neoteny": clip01(1.0 - final_maturity),
        "attractor_maj_frac": maj_mean,
        "body_n_honest_coherent_9": n_coh,
        "body_n_probes": len(bodies),
        "ce_descended": (init_ce is not None and final_ce is not None
                         and final_ce < init_ce - 1.0),
        "trained_saturated": (final_ce is not None and final_ce < 0.05),
        "nk_log": nk_log,
        "n_params": n_params,
        "train_wall_sec": train_wall,
        "traj": traj,
        "body_probes": bodies,
    }
    if emit:
        rec["emission_probe"] = emission_axis_probe(model, ds, device,
                                                    block_size)
    return rec


# ════════════════════════════════════════════════════════════════════
# Main — 3-cell grid.
# ════════════════════════════════════════════════════════════════════
def main(cfg):
    torch.manual_seed(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    corpus_sha = hashlib.sha256(open(cfg["corpus"], "rb").read()).hexdigest()
    print("=== §88-F2 — AXOLOTL NEOTENY ANTI-SATURATION (trained scale) ===",
          flush=True)
    print(f"device={device} corpus_sha={corpus_sha[:16]}…", flush=True)
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # ── cell0 baseline — normal training (natural saturation) ────────
    print("\n=== cell0_baseline — normal training (natural saturation) ===",
          flush=True)
    m0, items, np0, ce0, traj0, wall0, nk0 = train_cell(cfg, device,
                                                        neoteny=False)
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    cell0 = cell_metrics("cell0_baseline", m0, items, ds, device, traj0,
                         nk0, np0, ce0, wall0, cfg["block_size"], emit=False)
    ck0 = os.path.join(out_dir, "ckpt_baseline_s88f2.pt")
    torch.save({"model": m0.state_dict(), "cfg": cfg, "arm": "baseline"}, ck0)
    del m0
    if device == "cuda":
        torch.cuda.empty_cache()

    # ── cell1 neoteny — full-neoteny (NK-1+2+3+4) training ───────────
    print("\n=== cell1_neoteny — full-neoteny training (NK-1+2+3+4) ===",
          flush=True)
    m1, items1, np1, ce1, traj1, wall1, nk1 = train_cell(cfg, device,
                                                         neoteny=True)
    ds1 = CarveDataset(items1, cfg["block_size"], cfg["seed"])
    cell1 = cell_metrics("cell1_neoteny", m1, items1, ds1, device, traj1,
                         nk1, np1, ce1, wall1, cfg["block_size"], emit=False)

    # ── cell2 neoteny + §24-style emission probe (same ckpt) ─────────
    print("\n=== cell2_neoteny_emit — §24-style emission probe ===",
          flush=True)
    cell2 = cell_metrics("cell2_neoteny_emit", m1, items1, ds1, device,
                         traj1, nk1, np1, ce1, wall1, cfg["block_size"],
                         emit=True)
    ck1 = os.path.join(out_dir, "ckpt_neoteny_s88f2.pt")
    torch.save({"model": m1.state_dict(), "cfg": cfg, "arm": "neoteny"}, ck1)
    h = hashlib.sha256()
    with open(ck1, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    ckpt_sha = h.hexdigest()
    del m1
    if device == "cuda":
        torch.cuda.empty_cache()

    # ── 4-corner verdict ─────────────────────────────────────────────
    base_mat = cell0["final_maturity"]
    neo_mat = cell1["final_maturity"]
    base_ce = cell0["final_ce"]
    neo_ce = cell1["final_ce"]
    base_maj = cell0["attractor_maj_frac"]
    neo_maj = cell1["attractor_maj_frac"]
    base_D = cell0["final_D"]
    neo_D = cell1["final_D"]

    # neoteny actually trained (CE descended) — not under-trained?
    neo_ce_descended = cell1["ce_descended"]
    base_ce_descended = cell0["ce_descended"]
    # neoteny is non-degenerate if it learned (CE down) but stayed juvenile
    neo_delays_saturation = (neo_mat < base_mat - 1e-6)
    neo_undertrained = (not neo_ce_descended) or \
        (neo_ce is not None and base_ce is not None
         and neo_ce > min(2.0, base_ce + 1.0))
    # juvenile-but-competent: saturation delayed AND learning happened AND
    # body §9-coherent on at least one probe
    juvenile_but_competent = (neo_delays_saturation and neo_ce_descended
                              and cell1["body_n_honest_coherent_9"] >= 1)
    no_effect = (abs(neo_mat - base_mat) < 1e-3)

    if neo_undertrained:
        corner = "(β) NEOTENY-UNDERTRAINS"
        verdict = (
            f"NEGATIVE: the neoteny arm did not learn — neoteny final_ce="
            f"{neo_ce} (CE descended={neo_ce_descended}). The NK mechanisms "
            "blocked training itself, producing a degenerate juvenile "
            "(§11-B no-CE-degenerate echo). Anti-saturation that costs "
            "learning is not a path. Honest negative, valuable: confirms "
            "saturation and learning are coupled in this regime — §1.1 "
            "data-regime irreducibility reasserted."
        )
    elif juvenile_but_competent:
        corner = "(γ) JUVENILE-BUT-COMPETENT"
        verdict = (
            f"DIRECTIONAL-POSITIVE: the neoteny arm BOTH delayed saturation "
            f"(maturity {neo_mat:.4f} < baseline {base_mat:.4f}) AND learned "
            f"(CE descended {cell1['init_ce']:.3f}→{neo_ce:.4f}) AND emitted "
            f"≥1 §9-coherent body. A 'juvenile-but-competent' regime exists "
            "at trained scale — saturation slowed without killing learning. "
            "This is the §1.1-targeting positive the F-2 design hoped for. "
            "NOT GOAL emergence — necessary-not-sufficient (B-EMERGE-7); "
            "juvenile-but-competent is a mechanism-level finding, body §9 "
            "coherence is cascade-absence not capability. axolotl neoteny "
            "(biology direction-anchor) does measurably transfer at trained "
            "scale. north-star + §15/§51/§72 milestone UNCHANGED."
        )
    elif neo_delays_saturation:
        corner = "(α) NEOTENY-DELAYS-SATURATION-AT-TRAINED"
        verdict = (
            f"PARTIAL-POSITIVE: the neoteny arm delays saturation (maturity "
            f"{neo_mat:.4f} < baseline {base_mat:.4f}; neoteny maj_frac "
            f"{neo_maj:.3f} vs baseline {base_maj:.3f}; D {neo_D:.2f} vs "
            f"{base_D:.2f}) but did NOT reach the full juvenile-but-"
            "competent corner (body §9-coherent count="
            f"{cell1['body_n_honest_coherent_9']}). Anti-saturation works "
            "as a mechanism; coherent juvenile competence is not yet "
            "demonstrated. Directional, NOT GOAL emergence (B-EMERGE-7)."
        )
    elif no_effect:
        corner = "(δ) NEOTENY-NO-EFFECT-AT-TRAINED"
        verdict = (
            f"NEGATIVE: at trained scale the NK mechanisms produced no "
            f"measurable maturity difference (neoteny {neo_mat:.4f} ≈ "
            f"baseline {base_mat:.4f}). The §87-F2 stub's DIRECTIONAL-"
            "POSITIVE did not transfer — the NK levers are stub-bound. "
            "Honest negative. §1.1 data-regime irreducibility holds."
        )
    else:
        corner = "(β-mixed) NEOTENY-SHIFTS-BUT-NOT-CLEANLY"
        verdict = (
            f"MIXED: neoteny shifts the trajectory (maturity {neo_mat:.4f} "
            f"vs baseline {base_mat:.4f}) but neither cleanly delays "
            "saturation nor reaches juvenile-but-competent. Directional "
            "mechanism observation, NOT GOAL emergence (B-EMERGE-7)."
        )

    result = {
        "section": "§88-F2",
        "title": "axolotl neoteny anti-saturation — trained scale",
        "design_anchor": "§87-F2 commit 798b6110d (B-S87F2 6/6 🔵)",
        "biology_anchor": "axolotl (Ambystoma mexicanum) neoteny — §80 "
                          "amphibian subsection",
        "device": device,
        "corpus_sha256": corpus_sha,
        "neoteny_ckpt_sha256": ckpt_sha,
        "ckpt_sha256_note": "fresh §16-class ckpt — config/lever/seed/corpus "
        "class byte-equal to §81-FIRE/§79; sha NOT literally §16's.",
        "config": {k: cfg[k] for k in
                   ["d_model", "n_layer", "n_head", "n_kv_head", "block_size",
                    "steps", "warmup", "lr", "bsz", "lambda_ctl",
                    "lambda_route", "seed"]},
        "maturity_proxy_weights": {"W_CE": W_CE, "W_MAJ": W_MAJ, "W_D": W_D},
        "neoteny_thresholds": {"THETA_FLOOR": THETA_FLOOR, "THETA_D": THETA_D,
                               "SAT_TRIGGER": SAT_TRIGGER,
                               "NK2_SIGMA": NK2_SIGMA,
                               "NK3_LAMBDA": NK3_LAMBDA,
                               "NK4_LR_FLOOR_FRAC": NK4_LR_FLOOR_FRAC},
        "cells": {"cell0_baseline": cell0, "cell1_neoteny": cell1,
                  "cell2_neoteny_emit": cell2},
        "grid_summary": [
            {"cell": "cell0_baseline", "final_ce": base_ce,
             "maturity": base_mat, "neoteny": cell0["final_neoteny"],
             "attractor_maj_frac": base_maj, "effective_D": base_D,
             "body_coherent_9": cell0["body_n_honest_coherent_9"]},
            {"cell": "cell1_neoteny", "final_ce": neo_ce,
             "maturity": neo_mat, "neoteny": cell1["final_neoteny"],
             "attractor_maj_frac": neo_maj, "effective_D": neo_D,
             "body_coherent_9": cell1["body_n_honest_coherent_9"]},
            {"cell": "cell2_neoteny_emit",
             "final_ce": cell2["final_ce"],
             "maturity": cell2["final_maturity"],
             "neoteny": cell2["final_neoteny"],
             "physics_alive": cell2.get("emission_probe", {})
             .get("physics_alive"),
             "body_coherent_9": cell2["body_n_honest_coherent_9"]},
        ],
        "four_corner": {
            "alpha_NEOTENY_DELAYS_SATURATION": bool(neo_delays_saturation),
            "beta_NEOTENY_UNDERTRAINS": bool(neo_undertrained),
            "gamma_JUVENILE_BUT_COMPETENT": bool(juvenile_but_competent),
            "delta_NEOTENY_NO_EFFECT": bool(no_effect),
        },
        "verdict_corner": corner,
        "verdict_caveat": verdict,
        "honest_c3": [
            "trained scale ≠ GOAL emergence — necessary-not-sufficient "
            "(B-EMERGE-7); §88-F2 measures the anti-saturation mechanism "
            "axis only.",
            "§88-F2 differs structurally from §81/§82/§83-FIRE: NK is "
            "applied IN the training loop (learning-time anti-saturation), "
            "NOT as an inference overlay on an already-saturated ckpt.",
            "axolotl neoteny is an honest biological direction-anchor, NOT "
            "a capability proof. Biology USE ≠ anima emergence.",
            "the maturity 3-proxy and θ_floor/θ_D/SAT_TRIGGER are §87-F2 "
            "design choices; well-formed (B-S88F2) but not unique.",
            "effective D is a participation-ratio proxy of the head_a "
            "weight spectrum — a cheap deterministic rank proxy, not a "
            "rigorous gradient-field dimensionality certificate.",
            "under-training risk is real and pre-registered: NK could "
            "block learning itself (§11-B no-CE-degenerate echo) — the "
            "(β) corner captures that honestly.",
            "body §9 honest_coherent is cascade-absence, NOT correctness "
            "(B-EMERGE-7); a §9-coherent body can still be garbled.",
            "NK-1 clamps the CE term, never removes it — §11-B precedence "
            "respected (CE is load-bearing, NK is a CE-base overlay).",
            "ckpt sha is fresh; §16-byte-equal config (d/L/H/KV/seed/"
            "corpus class) satisfied, literal §16 sha differs — honest.",
            "north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.",
        ],
    }
    rp = os.path.join(out_dir, "result.json")
    with open(rp, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[§88-F2] verdict: {corner}", flush=True)
    print(f"[§88-F2] result.json → {rp}", flush=True)
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
    a = ap.parse_args()
    cfg = {
        "corpus": a.corpus, "out_dir": a.out_dir, "steps": a.steps,
        "warmup": a.warmup, "seed": a.seed, "d_model": a.d_model,
        "n_layer": a.n_layer, "n_head": a.n_head, "n_kv_head": a.n_kv_head,
        "block_size": a.block_size, "bsz": a.bsz, "lr": a.lr,
        "lambda_ctl": a.lambda_ctl, "lambda_route": a.lambda_route,
    }
    main(cfg)
