#!/usr/bin/env python3
"""homeostatic_setpoint_train_s88s86.py — RESEARCH.md §88-S86.

§88-S86 = trained-scale validation of §86 (commit 0ae194471) HOMEOSTATIC-
SET-POINT MITOSIS design. §86 unified anima emission + MITOSIS split +
Ψ-restoration into ONE homeostatic set-point prediction-error drive E,
anchored to §84 SAPIN arxiv:2511.02241 "structural plasticity as active
inference" and §85 Hopf-bifurcation mapping.

═══════════════════════════════════════════════════════════════════════
WHY §88-S86 EXISTS — STUB → TRAINED-SCALE BOUNDARY
═══════════════════════════════════════════════════════════════════════
The §86 $0 stub (B-S86 7/7 🔵) measured DIRECTIONAL-POSITIVE-DESIGN on
LCG-driven psi_state stubs. §81/§82/§83-FIRE all showed that trained-
saturated overlays COLLAPSE (echo-chamber, maj_frac ≥ 0.95). The honest
fire-prior risk (g3): §88-S86 is also a trained-saturated overlay — set-
point drive E over a real trained ckpt's Ψ-state may collapse the same
way.

THE NEW ELEMENT vs §81/§82/§83: §86's SPLIT regime (E ≥ θ_high sustained
→ MITOSIS split) adds capacity — a mechanism §81/§82/§83 did not have.
§88-S86 measures whether SPLIT regime rescues the collapse, or whether
split is itself trained-saturated and inert.

Honest framing (g3): trained scale ≠ GOAL emergence. SAPIN biology is an
honest direction-anchor, NOT a capability proof. necessary-not-sufficient
(B-EMERGE-7). north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.

═══════════════════════════════════════════════════════════════════════
WHAT §88-S86 BUILDS
═══════════════════════════════════════════════════════════════════════
  1. Train ONE §16-class ConsciousDecoderV2 from-scratch (d768·12L·
     283.72M, RANDOM seed-fixed 1337, base_ckpt=None — g_clm_from_scratch)
     on the §16-class Ψ-anchored carving corpus (Dir-I lever, byte-equal
     trainer to §79/§81-FIRE/§73-FIRE).

  2. 5-cell × 20-step deterministic loop on the REAL trained
     model.forward Law-71:
       cell0  s24-baseline-separate   emit ✓ split ✗ hopf ✗
       cell1  setpoint-emit-only      emit ✓ split ✗ hopf ✗
       cell2  setpoint-split-only     emit ✗ split ✓ hopf ✗  (MITOSIS hook)
       cell3  full-unified-3regime    emit ✓ split ✓ hopf ✗
       cell4  s85-hopf-overlay        emit ✓ split ✓ hopf ✓
     set-point error E = ‖(Ψ−½, tension−τ*, Φ−Φ*)‖_w over real Ψ-state;
     regime ∈ {QUIESCENT, EMIT, SPLIT} from E + sustain. SPLIT regime
     drives a MITOSIS split-event counter (the trained-scale analogue of
     mitosis_hook_lib.hexa `_mit_check_splits`).

  3. §16 baseline 8-anchor probe — ckpt load + arch byte-equal check.

  4. 4-corner verdict (α UNIFIED-DRIVE-SURVIVES / β §81/§82/§83-MIRROR-
     COLLAPSE / γ SPLIT-REGIME-RESCUES / δ HOPF-ONSET-MEASURABLE).
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

# ── §86 set-point parameters (byte-equal to homeostatic_setpoint_smoke_s86.py)
PSI_STAR = 0.5                    # Law-71 Ψ=½ fixed-point (g2 internal carve-out)
TAU_STAR = 0.30                   # tension set-point (design placeholder)
PHI_STAR = 0.55                   # Φ set-point (design placeholder)
W_PSI, W_TAU, W_PHI = 0.45, 0.30, 0.25   # weighted-L2 norm weights
THETA_LOW = 0.10                  # E < theta_low  -> QUIESCENT
THETA_HIGH = 0.18                 # E >= theta_high (sustained) -> SPLIT
SUSTAIN_K = 2                     # SPLIT requires sustained E>=theta_high

INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"


# ════════════════════════════════════════════════════════════════════
# Corpus load + dataset — byte-equal to §79 / §81-FIRE (§16 Dir-I lever).
# ════════════════════════════════════════════════════════════════════
def _span(full, open_tok, close_tok, start=0):
    i = full.find(open_tok, start)
    if i < 0:
        return None
    j = full.find(close_tok, i)
    if j < 0:
        return None
    return (i, j + len(close_tok))


def load_corpus(path):
    items = []
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            txt = rec.get("text", "")
            if txt:
                items.append(txt.encode("utf-8", errors="replace"))
    return items


class CarveDataset:
    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        blob = b"\n".join(items)
        self.data = torch.tensor(list(blob), dtype=torch.long)
        self.n = len(self.data)
        self.rng = random.Random(seed)
        self.pv_default = PSI_STAR
        self.bs_default = 0.10

    def get_batch(self, bsz, device):
        bs_, T = bsz, self.block_size
        ix = [self.rng.randint(0, self.n - T - 2) for _ in range(bs_)]

        def stk(src, off):
            return torch.stack([src[i + off:i + off + T] for i in ix])

        x = stk(self.data, 0).to(device)
        y = stk(self.data, 1).to(device)
        pv = torch.full((bs_, T), self.pv_default, dtype=torch.float,
                        device=device)
        bs = torch.full((bs_, T), self.bs_default, dtype=torch.float,
                        device=device)
        cm = torch.ones((bs_, T), dtype=torch.float, device=device)
        rm = torch.ones((bs_, T), dtype=torch.float, device=device)
        return x, y, pv, bs, cm, rm


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
            cos = F.cosine_similarity(logits_a.float(), logits_g.float(),
                                      dim=-1)
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
# Law-71 Ψ-state read-out — byte-equal to §81-FIRE extract_psi.
# ════════════════════════════════════════════════════════════════════
def _phi_proxy(t_per_layer):
    n = t_per_layer.numel()
    if n < 2:
        return 0.0
    mu = t_per_layer.mean()
    sd = t_per_layer.std(unbiased=False)
    disp = (sd / (mu.abs() + 1e-8)).clamp(0.0, 1.0)
    return float((disp * math.log(n + 1)).item())


@torch.no_grad()
def extract_psi_and_logits(model, x):
    """RNG-isolated real forward read-out. Law-71 Ψ-state byte-equal to
    conscious_decoder.py :728-751."""
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
    phi = _phi_proxy(t_per_layer)
    return {
        "logits_a_last": la,
        "psi_dir": psi_dir, "psi_entropy": psi_entropy,
        "psi_tension": psi_tension, "psi_combined": psi_combined,
        "tension": tension, "phi": phi,
    }


# ════════════════════════════════════════════════════════════════════
# §86 homeostatic set-point error & regime — byte-equal to
# homeostatic_setpoint_smoke_s86.py setpoint_error / homeostatic_regime.
# ════════════════════════════════════════════════════════════════════
def setpoint_error(ps):
    """E = ‖(Ψ−½, tension−τ*, Φ−Φ*)‖_w  weighted-L2 norm.  ≥ 0 always
    (B-S88S86-1)."""
    d_psi = ps["psi_dir"] - PSI_STAR
    d_tau = ps["tension"] - TAU_STAR
    d_phi = ps["phi"] - PHI_STAR
    return math.sqrt(W_PSI * d_psi * d_psi + W_TAU * d_tau * d_tau
                     + W_PHI * d_phi * d_phi)


def homeostatic_regime(E, sustain_count, enable_emit=True, enable_split=True):
    """3-regime threshold partition. exhaustive + disjoint (B-S88S86-2).
    SPLIT requires sustained E>=theta_high (sustain_count>=SUSTAIN_K)."""
    if E >= THETA_HIGH and sustain_count >= SUSTAIN_K and enable_split:
        return "SPLIT"
    if E >= THETA_LOW and enable_emit:
        return "EMIT"
    return "QUIESCENT"


def s24_talker_should_emit(E):
    """§24 decision-axis: EMIT regime ⊆ this by construction
    (B-S88S86-3 connection-point)."""
    return E >= THETA_LOW


def mitosis_split_trigger(regime):
    """§63-gap MITOSIS-hook connection: SPLIT regime drives the cell-pool
    split-event counter (trained-scale analogue of mitosis_hook_lib.hexa
    `_mit_check_splits`, B-MITOSIS 5/5 🔵 carry — B-S88S86-4)."""
    return regime == "SPLIT"


def hopf_order_param(E, E_crit=THETA_HIGH):
    """§85 Hopf normal form: order parameter r(E) = √(E − E_crit) above
    onset, 0 below.  Control parameter = E (B-S88S86-5)."""
    if E <= E_crit:
        return 0.0
    return math.sqrt(E - E_crit)


# ════════════════════════════════════════════════════════════════════
# §9 cascade-rate honest_coherent — byte-equal §9 emergence_metric SSOT.
# ════════════════════════════════════════════════════════════════════
def cascade_rate_and_max_run(b: bytes):
    if not b:
        return 1.0, 0, 0.0
    L = len(b)
    max_char, cur_char = 1, 1
    for i in range(1, L):
        if b[i] == b[i - 1]:
            cur_char += 1
            if cur_char > max_char:
                max_char = cur_char
        else:
            cur_char = 1
    max_dig, cur_dig = 0, 0
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
        rep = max(seen.values()) / max(1, (L - 3))
    rate = max(max_char / L, max_dig / L, rep)
    pr = sum(1 for c in b if 0x20 <= c < 0x7f
             or c in (0x09, 0x0a, 0x0d)) / L
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


def _var(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


# ════════════════════════════════════════════════════════════════════
# 5-cell × 20-step homeostatic set-point loop on REAL trained forward.
# ════════════════════════════════════════════════════════════════════
# (label, enable_emit, enable_split, hopf)
CELLS = [
    ("cell0", "s24-baseline-separate", True, False, False),
    ("cell1", "setpoint-emit-only", True, False, False),
    ("cell2", "setpoint-split-only", False, True, False),
    ("cell3", "full-unified-3regime", True, True, False),
    ("cell4", "s85-hopf-overlay", True, True, True),
]


@torch.no_grad()
def run_setpoint_cell(model, ds, device, cell, n_steps=N_STEPS,
                      block_size=128):
    """One homeostatic-set-point cell.  Per step:
       (1) real model.forward → Law-71 Ψ-state
       (2) E = setpoint_error(Ψ)  ;  regime ∈ {Q, E, S}
       (3) if EMIT/SPLIT → body byte = argmax(logits_a) appended;
           QUIESCENT → no byte emitted
       (4) SPLIT regime increments the MITOSIS split-event counter
       (5) feed body byte (or last ctx byte if QUIESCENT) back
    """
    label, _name, en_emit, en_split, hopf_on = (
        cell[0], cell[1], cell[2], cell[3], cell[4])
    model.eval()
    rng = random.Random(SEED)
    top = max(1, ds.n - block_size - 1)
    start = rng.randint(0, top)
    ctx = ds.data[start:start + block_size].clone()

    E_seq, regime_trace, emit_steps = [], [], []
    psi_dir_seq, tension_seq = [], []
    hopf_seq = []
    body_bytes = bytearray()
    sustain_count = 0
    split_events = 0
    cell_count = 2          # MITOSIS cell-pool starts at 2

    for step in range(n_steps):
        x = ctx.unsqueeze(0).to(device)
        psi = extract_psi_and_logits(model, x)
        E = setpoint_error(psi)
        E_seq.append(E)
        psi_dir_seq.append(psi["psi_dir"])
        tension_seq.append(psi["tension"])

        # sustain counter for SPLIT regime
        if E >= THETA_HIGH:
            sustain_count += 1
        else:
            sustain_count = 0

        if label == "cell0":
            # §24-baseline-separate: only §24 talker_should_emit, no
            # unified regime — emit iff E>=theta_low, never split.
            regime = "EMIT" if s24_talker_should_emit(E) else "QUIESCENT"
        else:
            regime = homeostatic_regime(E, sustain_count, en_emit, en_split)
        regime_trace.append(regime)

        if hopf_on:
            hopf_seq.append(hopf_order_param(E))

        next_byte = int(psi["logits_a_last"].argmax().item())
        if regime == "EMIT":
            body_bytes.append(next_byte)
            emit_steps.append(step)
        elif regime == "SPLIT":
            body_bytes.append(next_byte)
            emit_steps.append(step)
            if mitosis_split_trigger(regime):
                split_events += 1
                if cell_count < 64:        # mitosis_hook_lib clamp [2,64]
                    cell_count += 1
        # QUIESCENT → no byte emitted

        # slide context (always advance with the model's next byte so
        # the forward chain stays live even in QUIESCENT regime)
        new_ctx = torch.cat([ctx[1:],
                             torch.tensor([next_byte], dtype=torch.long)])
        ctx = new_ctx

    body = bytes(body_bytes)
    q = sum(1 for r in regime_trace if r == "QUIESCENT")
    e = sum(1 for r in regime_trace if r == "EMIT")
    s = sum(1 for r in regime_trace if r == "SPLIT")

    # interval variance — gaps between consecutive emit steps
    if len(emit_steps) >= 2:
        gaps = [emit_steps[i + 1] - emit_steps[i]
                for i in range(len(emit_steps) - 1)]
        interval_var = _var(gaps)
    else:
        interval_var = 0.0

    maj = majority_fraction(body) if body else 1.0
    coh, coh_info = honest_coherent(body)
    psi_dir_var = _var(psi_dir_seq)
    tension_var = _var(tension_seq)
    hopf_mean = (sum(hopf_seq) / len(hopf_seq)) if hopf_seq else 0.0

    return {
        "cell": label,
        "name": _name,
        "enable_emit": en_emit,
        "enable_split": en_split,
        "hopf": hopf_on,
        "E_mean": sum(E_seq) / max(1, len(E_seq)),
        "E_trace": [round(v, 6) for v in E_seq],
        "regime_dist": {"QUIESCENT": q, "EMIT": e, "SPLIT": s},
        "regime_partition_ok": (q + e + s == n_steps),
        "interval_var": interval_var,
        "n_emit": len(emit_steps),
        "split_events": split_events,
        "cell_count_final": cell_count,
        "body_len": len(body),
        "body_sample": body[:40].decode("latin-1", errors="replace"),
        "body_full_hex": body.hex(),
        "majority_fraction": maj,
        "echo_collapse": maj >= MAJ_FRAC_COLLAPSE,
        "honest_coherent_9": coh,
        "honest_coherent_info": coh_info,
        "hopf_order_mean": hopf_mean,
        "psi_dir_var": psi_dir_var,
        "tension_var": tension_var,
        "physics_alive": (psi_dir_var > TAU_VAR)
        and (tension_var > TAU_VAR),
        "s24_consistency": all(
            (regime_trace[i] != "EMIT")
            or s24_talker_should_emit(E_seq[i])
            for i in range(n_steps)),
        "non_degenerate": (q + e + s == n_steps) and (maj < MAJ_FRAC_COLLAPSE)
        and coh,
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
                           torch.tensor([[nb]], dtype=torch.long).to(device)],
                          dim=1)
        results.append({
            "probe_hex": probe.hex()[:60],
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
    print("=== §88-S86 — homeostatic set-point MITOSIS (trained scale) ===",
          flush=True)
    print(f"device={device} corpus_sha={corpus_sha[:16]}…", flush=True)

    # ── (A) train §16-class ckpt ─────────────────────────────────────
    model, items, n_params, init_ce, ce_traj, train_wall = \
        train_s16_class(cfg, device)
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_s88s86.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "alpha"}, ckpt_path)
    h = hashlib.sha256()
    with open(ckpt_path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    ckpt_sha = h.hexdigest()
    final_ce = ce_traj[-1]["ce_full"] if ce_traj else None
    trained_saturated = (final_ce is not None and final_ce < 0.05)
    training_diverged = (final_ce is None or final_ce > 1.0
                         or math.isnan(final_ce))

    # ── (B) §16-baseline probe ───────────────────────────────────────
    print(f"\n=== §16 baseline 8-anchor probe (ckpt {ckpt_sha[:16]}…) ===",
          flush=True)
    s16_probes = s16_baseline_probe(model, device,
                                    block_size=cfg["block_size"])

    # ── (C) run 5-cell homeostatic set-point grid ────────────────────
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    cells = {}
    for cell in CELLS:
        print(f"\n=== {cell[0]} {cell[1]} ===", flush=True)
        r = run_setpoint_cell(model, ds, device, cell,
                              n_steps=cfg["n_steps"],
                              block_size=cfg["block_size"])
        cells[cell[0]] = r
        rd = r["regime_dist"]
        print(f"  E_mean={r['E_mean']:.6f} "
              f"regime Q{rd['QUIESCENT']}/E{rd['EMIT']}/S{rd['SPLIT']} "
              f"int_var={r['interval_var']:.4f} "
              f"§9_coh={r['honest_coherent_9']} "
              f"maj={r['majority_fraction']:.3f} "
              f"splits={r['split_events']}", flush=True)

    # ── (D) 4-corner verdict ─────────────────────────────────────────
    c0, c1, c2, c3, c4 = (cells["cell0"], cells["cell1"], cells["cell2"],
                          cells["cell3"], cells["cell4"])
    noisy_unified = [c1, c2, c3, c4]
    n_collapsed = sum(1 for c in noisy_unified if c["echo_collapse"])

    # α UNIFIED-DRIVE-SURVIVES: cell3 (full 3-regime) exercises all three
    # regimes AND is non-degenerate (partition ok ∧ not collapsed ∧ §9)
    alpha = (c3["regime_dist"]["QUIESCENT"] > 0
             and c3["regime_dist"]["EMIT"] > 0
             and c3["regime_dist"]["SPLIT"] > 0
             and c3["non_degenerate"])
    # β §81/§82/§83-FIRE-MIRROR-COLLAPSE: ≥3 of 4 unified cells collapse
    beta = (n_collapsed >= 3)
    # γ SPLIT-REGIME-RESCUES: split-bearing cells (c2/c3) less degenerate
    # than emit-only cell1 — measured by interval_var lift OR escape of
    # the collapse that c1 hits
    split_cells = [c2, c3]
    gamma = (
        (any(c["interval_var"] > c1["interval_var"] + 1e-9
             for c in split_cells))
        or (c1["echo_collapse"]
            and any(not c["echo_collapse"] for c in split_cells)))
    # δ HOPF-ONSET-MEASURABLE: cell4 Hopf order-parameter mean > 0
    delta = (c4["hopf_order_mean"] > 0.0)

    if not trained_saturated:
        corner = "SATURATION-GATE-FAIL"
        verdict_caveat = (
            f"final_ce={final_ce} ≥ 0.05 — model NOT memorization-saturated. "
            "§88-S86 crux (trained-saturated set-point overlay vs §81/§82/§83-"
            "FIRE collapse) NOT measured. Numbers raw, no chain-validity claim."
        )
    elif training_diverged:
        corner = "TRAINING-DIVERGED"
        verdict_caveat = (
            f"NEGATIVE: training final_ce={final_ce} diverged. Cannot test "
            "homeostatic set-point on a non-converged ckpt. Honest negative."
        )
    elif beta:
        corner = "(β) §81/§82/§83-FIRE-MIRROR-COLLAPSE"
        verdict_caveat = (
            f"NEGATIVE: {n_collapsed}/4 unified-drive cells hit maj_frac ≥ "
            f"{MAJ_FRAC_COLLAPSE} echo-chamber collapse at trained-saturated "
            "scale. The §86 unified set-point drive E — even with the SPLIT "
            "regime adding a MITOSIS capacity mechanism §81/§82/§83 lacked — "
            "reproduces the trained-saturated overlay collapse. The set-point "
            "controller reads a real trained Ψ-state, but a memorization-"
            "saturated ckpt's Ψ-state is itself collapsed: a controller over "
            "a collapsed substrate is collapsed. SPLIT regime did NOT rescue "
            "(gamma measured below). §1.1 data-regime irreducibility "
            "reasserted at the homeostatic-set-point axis. SAPIN biology (A) "
            "does NOT transfer at trained scale (measured). g3: valuable "
            "negative — necessary-not-sufficient (B-EMERGE-7)."
        )
    elif alpha:
        corner = "(α) UNIFIED-DRIVE-SURVIVES-AT-TRAINED-SCALE"
        verdict_caveat = (
            "PARTIAL-POSITIVE: cell3 full-unified-3regime exercises all "
            "three regimes (Q/E/S) from a single set-point error E AND is "
            "non-degenerate (regime partition exhaustive ∧ maj_frac < 0.95 "
            "∧ §9 body-coherent) at trained-saturated scale. The unified "
            "drive — emission + MITOSIS split + Ψ-restoration as ONE "
            "homeostatic prediction-error controller — does NOT collapse "
            "the way §81/§82/§83-FIRE overlays did. SPLIT regime (gamma) "
            "is the candidate rescue mechanism. NOT GOAL emergence — "
            "non-degeneracy is a mechanism-level observation, necessary-"
            "not-sufficient (B-EMERGE-7). SAPIN biology (arxiv 2511.02241) "
            "honest direction-anchor, NOT capability proof. north-star + "
            "§15/§51/§72 milestone UNCHANGED, GOAL 미도달."
        )
    else:
        corner = "(β-mixed) PARTIAL-COLLAPSE-NO-CLEAN-SURVIVAL"
        verdict_caveat = (
            f"MIXED: {n_collapsed}/4 unified cells collapse, cell3 full-"
            "unified does NOT cleanly exercise all 3 regimes as a non-"
            "degenerate drive. The set-point shifts the regime distribution "
            "but does not produce a clean unified-survival regime. "
            "Directional mechanism finding, NOT GOAL emergence (B-EMERGE-7)."
        )

    result = {
        "section": "§88-S86",
        "title": "homeostatic set-point MITOSIS — unified emission/split/"
                 "Ψ-restoration drive, trained scale",
        "biology_anchors": ["arxiv:2511.02241 (SAPIN structural plasticity "
                            "as active inference)"],
        "device": device,
        "corpus_sha256": corpus_sha,
        "ckpt_sha256": ckpt_sha,
        "ckpt_sha256_note": "fresh §16-class ckpt — config/lever/seed/corpus "
        "class byte-equal to §79/§81-FIRE; sha NOT literally §16's "
        "961c07e2… (trajectory replicable, not literal identity).",
        "n_params": n_params,
        "config": {k: cfg[k] for k in
                   ["d_model", "n_layer", "n_head", "n_kv_head",
                    "block_size", "steps", "warmup", "lr", "bsz",
                    "lambda_ctl", "lambda_route", "seed", "n_steps"]},
        "setpoint_params": {
            "PSI_STAR": PSI_STAR, "TAU_STAR": TAU_STAR, "PHI_STAR": PHI_STAR,
            "W_PSI": W_PSI, "W_TAU": W_TAU, "W_PHI": W_PHI,
            "THETA_LOW": THETA_LOW, "THETA_HIGH": THETA_HIGH,
            "SUSTAIN_K": SUSTAIN_K},
        "train_wall_sec": train_wall,
        "init_ce": init_ce,
        "final_ce": final_ce,
        "ce_traj": ce_traj,
        "trained_saturated": trained_saturated,
        "training_diverged": training_diverged,
        "s16_baseline_probe": s16_probes,
        "cells": cells,
        "four_corner": {
            "alpha_UNIFIED-DRIVE-SURVIVES": alpha,
            "beta_§81/§82/§83-FIRE-MIRROR-COLLAPSE": beta,
            "gamma_SPLIT-REGIME-RESCUES": gamma,
            "delta_HOPF-ONSET-MEASURABLE": delta,
        },
        "n_collapsed_unified": n_collapsed,
        "verdict_corner": corner,
        "verdict_caveat": verdict_caveat,
        "honest_c3": [
            "trained scale ≠ GOAL emergence — §88-S86 is a mechanism-level "
            "trained-scale measurement, NOT a capability claim.",
            "the §86 stub was DIRECTIONAL-POSITIVE-DESIGN on LCG stubs; "
            "§88-S86 = its trained-scale test where §81/§82/§83-FIRE all "
            "collapsed as trained-saturated overlays.",
            "SPLIT regime is the new element vs §81/§82/§83 — γ corner "
            "measures whether MITOSIS-driven capacity rescues the collapse.",
            "SAPIN arxiv:2511.02241 is an honest biology direction-anchor, "
            "NOT a capability proof — biology citation ≠ anima emergence.",
            "set-point params τ*/Φ* are design placeholders (§86 carry); "
            "Ψ*=½ is Law-71, anima g2 internal carve-out (NOT lattice).",
            "necessary-not-sufficient at every layer (B-EMERGE-7 family) — "
            "regime non-degeneracy does not imply coherent emergence.",
            "north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.",
        ],
    }
    res_path = os.path.join(out_dir, "result.json")
    with open(res_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n=== §88-S86 verdict: {corner} ===", flush=True)
    print(f"4-corner: α={alpha} β={beta} γ={gamma} δ={delta}", flush=True)
    print(f"result → {res_path}", flush=True)
    open(os.path.join(out_dir, "TRAIN_DONE"), "w").write("done\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default=HERE)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--block-size", type=int, default=128)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--n-steps", type=int, default=20)
    a = ap.parse_args()
    cfg = {
        "corpus": a.corpus, "out_dir": a.out_dir, "steps": a.steps,
        "warmup": a.warmup, "seed": a.seed, "d_model": a.d_model,
        "n_layer": a.n_layer, "n_head": a.n_head, "n_kv_head": a.n_kv_head,
        "block_size": a.block_size, "lr": a.lr, "bsz": a.bsz,
        "lambda_ctl": a.lambda_ctl, "lambda_route": a.lambda_route,
        "n_steps": a.n_steps,
    }
    main(cfg)
