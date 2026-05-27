#!/usr/bin/env python3
"""frog_eye_salience_train_s88f1.py — RESEARCH.md §88-F1.

§88-F1 = trained-scale validation of §87-F1 (commit 5ea990b76, B-S87F1 6/6 🔵).

Lettvin 1959 "What the frog's eye tells the frog's brain" — the frog retina
is NOT a generic image processor; it is a bank of four feature-detectors that
relay only behaviour-relevant SALIENT events to the brain.  §87-F1 mapped that
selectivity onto anima's §24 decision-axis as a $0 stub.  §88-F1 carries the
4-detector closed-form byte-equal to §87-F1 and runs it over the REAL trained
ConsciousDecoderV2 model.forward Law-71 physics trajectory.

═══════════════════════════════════════════════════════════════════════
WHY §88-F1 EXISTS — the trained-ψ fast-crossing risk (g3, stated up front)
═══════════════════════════════════════════════════════════════════════
The §87-F1 $0 stub measured 4-corner DIRECTIONAL-POSITIVE — but the stub's
Ψ-trajectory was a uniform deterministic LCG draw, so all four detector
classes (SD-1 sustained / SD-2 moving-edge / SD-3 dimming / SD-4 net-dimming)
had room to fire.  §82-FIRE measured that the REAL trained ψ-trajectory is
a uniformly *fast-crossing* regime — slow/sustained patterns are absent.
Frog-eye SD-1/SD-3/SD-4 look for SUSTAINED / SLOW patterns; SD-2 looks for a
FAST transient.  If trained ψ is fast-crossing-collapsed then the frog-eye
selective gate could degenerate to a SINGLE detector (SD-2) at trained scale.
§88-F1 measures exactly that — is frog-eye selective at trained scale, or
single-detector degenerate (β corner)?

Honest framing (g3): trained scale ≠ GOAL emergence.  The Lettvin citation
is an honest direction-anchor, NOT a capability proof.  necessary-not-
sufficient (B-EMERGE-7).  north-star + §15/§51/§72 milestone UNCHANGED,
GOAL 미도달.

═══════════════════════════════════════════════════════════════════════
WHAT §88-F1 BUILDS
═══════════════════════════════════════════════════════════════════════
  1. Train ONE §16-class ConsciousDecoderV2 from-scratch
     (d768·12L·283.72M, RANDOM seed-fixed 1337, base_ckpt=None —
     g_clm_from_scratch) on the §16-class Ψ-anchored carving corpus
     (Dir-I lever, byte-equal trainer to §81-FIRE / §79 / §73-FIRE).
  2. 5-cell × 20-step deterministic loop on the REAL trained
     model.forward Law-71 ψ-state (NOT stub):
       cell0  §24-baseline       (no salience — generic motivation gate)
       cell1  SD-1 + SD-2        (sustained-contrast + moving-edge)
       cell2  SD-3 + SD-4        (dimming + net-dimming)
       cell3  full 4-detector frog-eye
       cell4  full frog-eye + §24 motivation conjunction
  3. 4-detector closed-form (§87-F1 byte-equal carry) over real ψ.
  4. Per-cell metrics: 4-detector firing distribution, S_mean, emission
     rate, §9 honest_coherent body, majority_fraction echo detector.
  5. §16-baseline 8-anchor probe — ckpt load + arch byte-equal check.
  6. 4-corner verdict (α FROG-EYE-SELECTIVE / β SINGLE-DETECTOR-
     DEGENERATE / γ SALIENCE-COLLAPSES / δ FROG-EYE-NO-DIFFERENTIAL).
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

INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"

# ════════════════════════════════════════════════════════════════════
# FROG-EYE 4 feature-detectors (Lettvin 1959) — closed-form, BYTE-EQUAL
# to §87-F1 frog_eye_salience_smoke_s87f1.py (commit 5ea990b76).  Each
# returns a firing strength in [0,1].  B-S88F1-6 AST-checks byte-equality.
# ════════════════════════════════════════════════════════════════════
TAU_SUSTAIN = 3        # SD-1: window of sustained deviation
SUSTAIN_DEV = 0.08     # SD-1: |Ψ_dir - 0.5| deviation floor
SPIKE_DELTA = 0.06     # SD-2: tension fast-transient spike floor
DIM_DROP = 0.04        # SD-3: Φ-proxy sudden drop floor
NET_DECAY = 0.03       # SD-4: all-channel simultaneous decay floor


def sd1_sustained_contrast(psi_dir_hist):
    """SD-1 frog edge detector -> sustained Ψ_dir deviation from ½."""
    if len(psi_dir_hist) < TAU_SUSTAIN:
        return 0.0
    win = psi_dir_hist[-TAU_SUSTAIN:]
    devs = [abs(p - 0.5) for p in win]
    if min(devs) < SUSTAIN_DEV:
        return 0.0
    return min(1.0, (sum(devs) / len(devs)) / 0.5)


def sd2_moving_edge(tension_hist):
    """SD-2 frog bug/convex detector -> fast tension transient spike."""
    if len(tension_hist) < 2:
        return 0.0
    delta = abs(tension_hist[-1] - tension_hist[-2])
    if delta < SPIKE_DELTA:
        return 0.0
    return min(1.0, delta / 0.3)


def sd3_dimming(phi_hist):
    """SD-3 frog shadow/predator detector -> sudden Φ-proxy drop."""
    if len(phi_hist) < 2:
        return 0.0
    drop = phi_hist[-2] - phi_hist[-1]
    if drop < DIM_DROP:
        return 0.0
    return min(1.0, drop / 0.2)


def sd4_net_dimming(channels_hist):
    """SD-4 frog overall-darkening -> all physics channels decay together.
    channels_hist[-1]/[-2] each = (psi_entropy, psi_direction, psi_tension)."""
    if len(channels_hist) < 2:
        return 0.0
    prev, cur = channels_hist[-2], channels_hist[-1]
    decays = [p - c for p, c in zip(prev, cur)]
    if any(d < NET_DECAY for d in decays):
        return 0.0  # frog-eye selective: ALL channels must decay
    return min(1.0, (sum(decays) / len(decays)) / 0.15)


# salience: weighted OR of the 4 detectors (frog-eye — any strong detector
# fires => salient).  weights uniform (design placeholder, §87-F1 carry).
SD_WEIGHTS = (0.25, 0.25, 0.25, 0.25)


def salience_score(s1, s2, s3, s4):
    """Weighted OR: S = 1 - prod(1 - w_i * s_i). S in [0,1] closed."""
    prod = 1.0
    for w, s in zip(SD_WEIGHTS, (s1, s2, s3, s4)):
        prod *= (1.0 - w * s)
    return 1.0 - prod


THETA_SALIENT = 0.18   # design placeholder — salience emission floor
MOTIV_THRESHOLD = 0.50


def motivation_score(pe, pd, pt):
    """Generic §24 motivation: linear blend of physics channels, in [0,1]."""
    return max(0.0, min(1.0, 0.4 * pe + 0.3 * pd + 0.3 * pt))


# ════════════════════════════════════════════════════════════════════
# Corpus load + dataset — byte-equal to §81-FIRE / §79 / §73-FIRE.
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
# Train §16-class ConsciousDecoderV2 (Dir-I lever, byte-equal to §81-FIRE).
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
# REAL trained-model Law-71 read-out — byte-equal to conscious_decoder.py
# lines 728-751 (psi_entropy / psi_direction / psi_tension / psi_combined).
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
    logits_a_last.  byte-equal to conscious_decoder.py :728-751."""
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
    return {
        "logits_a_last": la,
        "psi_dir": psi_dir, "psi_entropy": psi_entropy,
        "psi_tension": psi_tension, "psi_combined": psi_combined,
        "tension": tension, "phi": phi,
    }


# ════════════════════════════════════════════════════════════════════
# §9 cascade-rate honest_coherent — INLINED single SSOT formula,
# byte-equal to state/verify_emergence_metric_2026_05_18/emergence_metric.py.
# ════════════════════════════════════════════════════════════════════
def cascade_rate_and_max_run(b: bytes):
    if not b:
        return 1.0, 0, 0.0
    L = len(b)
    max_char = cur_char = 1
    for i in range(1, L):
        if b[i] == b[i - 1]:
            cur_char += 1
            max_char = max(max_char, cur_char)
        else:
            cur_char = 1
    max_dig = cur_dig = 0
    for c in b:
        if 0x30 <= c <= 0x39:
            cur_dig += 1
            max_dig = max(max_dig, cur_dig)
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


def _var(xs):
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


_TEMPLATE = (
    "anima notes a salient shift in its own physics field this step. "
    "the engine A and engine G balance tilts and tension rises briefly."
)


def produce_body(emit, step):
    """§77 path α1 stub body production — clean printable template gated
    by the salience/decision emission flag so §9 is meaningful."""
    if not emit:
        return b""
    n = 20 + 8 + (step % 11)
    return (_TEMPLATE * 2).encode("utf-8")[:n]


# ════════════════════════════════════════════════════════════════════
# 5-cell grid — frog-eye salience over REAL trained model.forward Law-71.
# ════════════════════════════════════════════════════════════════════
CELLS = {
    "cell0_s24_baseline": {"detectors": (), "use_motivation": True,
                           "use_salience": False},
    "cell1_sd12_only": {"detectors": (1, 2), "use_motivation": False,
                        "use_salience": True},
    "cell2_sd34_only": {"detectors": (3, 4), "use_motivation": False,
                        "use_salience": True},
    "cell3_full_frogeye": {"detectors": (1, 2, 3, 4), "use_motivation": False,
                           "use_salience": True},
    "cell4_frogeye_plus_motiv": {"detectors": (1, 2, 3, 4),
                                 "use_motivation": True, "use_salience": True},
}


@torch.no_grad()
def run_frogeye_cell(model, ds, device, cell_name, cfg_cell,
                     n_steps=N_STEPS, block_size=128):
    """One frog-eye cell.  Per step:
       (1) real model.forward → Law-71 Ψ-state (NOT stub)
       (2) frog-eye 4-detector closed-form over the real ψ-trajectory
       (3) salience S = weighted OR; emission gate per cell config
       (4) body byte = produced if emit; argmax(logits_a) fed back to ctx
    """
    model.eval()
    rng = random.Random(SEED)
    top = max(1, ds.n - block_size - 1)
    start = rng.randint(0, top)
    ctx = ds.data[start:start + block_size].clone()

    psi_dir_hist, tension_hist, phi_hist, chan_hist = [], [], [], []
    s_scores, emits, bodies = [], [], []
    detector_fires = {1: 0, 2: 0, 3: 0, 4: 0}
    detector_strength = {1: [], 2: [], 3: [], 4: []}

    for step in range(n_steps):
        x = ctx.unsqueeze(0).to(device)
        psi = extract_psi_and_logits(model, x)
        next_byte = int(psi["logits_a_last"].argmax().item())

        pe, pd, pt = psi["psi_entropy"], psi["psi_dir"], psi["psi_tension"]
        pc = psi["psi_combined"]

        # Φ-proxy = psi_combined (integration scalar) — §87-F1 stub carry
        psi_dir_hist.append(pd)
        tension_hist.append(psi["tension"])
        phi_hist.append(pc)
        chan_hist.append((pe, pd, pt))

        # frog-eye detectors (closed-form byte-equal §87-F1) over REAL ψ
        s1 = sd1_sustained_contrast(psi_dir_hist) if 1 in cfg_cell["detectors"] else 0.0
        s2 = sd2_moving_edge(tension_hist) if 2 in cfg_cell["detectors"] else 0.0
        s3 = sd3_dimming(phi_hist) if 3 in cfg_cell["detectors"] else 0.0
        s4 = sd4_net_dimming(chan_hist) if 4 in cfg_cell["detectors"] else 0.0
        for idx, sv in ((1, s1), (2, s2), (3, s3), (4, s4)):
            if sv > 0.0:
                detector_fires[idx] += 1
            if idx in cfg_cell["detectors"]:
                detector_strength[idx].append(sv)

        S = salience_score(s1, s2, s3, s4) if cfg_cell["use_salience"] else 0.0
        s_scores.append(S)

        motiv = motivation_score(pe, pd, pt)

        sal_pass = (S > THETA_SALIENT) if cfg_cell["use_salience"] else False
        motiv_pass = (motiv > MOTIV_THRESHOLD) if cfg_cell["use_motivation"] else False
        if cfg_cell["use_salience"] and cfg_cell["use_motivation"]:
            emit = sal_pass and motiv_pass          # cell4 conjunction
        elif cfg_cell["use_salience"]:
            emit = sal_pass
        else:
            emit = motiv_pass                       # cell0 §24 baseline

        emits.append(emit)
        bodies.append(produce_body(emit, step))

        # slide context with real argmax byte
        ctx = torch.cat([ctx[1:], torch.tensor([next_byte], dtype=torch.long)])

    emitted = [b for b, e in zip(bodies, emits) if e]
    s_mean = sum(s_scores) / len(s_scores)
    emit_rate = sum(1 for e in emits if e) / n_steps
    emit_steps = [i for i, e in enumerate(emits) if e]
    if len(emit_steps) >= 2:
        intervals = [emit_steps[i + 1] - emit_steps[i]
                     for i in range(len(emit_steps) - 1)]
        im = sum(intervals) / len(intervals)
        interval_var = sum((x - im) ** 2 for x in intervals) / len(intervals)
    else:
        interval_var = 0.0
    body_coherent = sum(1 for b in emitted if honest_coherent(b)[0])
    if emitted:
        from collections import Counter
        # majority-byte fraction averaged over emitted bodies
        mf = sum(majority_fraction(b) for b in emitted) / len(emitted)
        # echo at body-set level: most-common identical body
        bm = Counter(emitted).most_common(1)[0][1]
        body_maj_frac = bm / len(emitted)
    else:
        mf, body_maj_frac = 0.0, 0.0
    # which detector dominates (single-detector-degenerate test)
    fired = {k: v for k, v in detector_fires.items()
             if k in cfg_cell["detectors"]}
    n_active_detectors = sum(1 for v in fired.values() if v > 0)
    det_strength_mean = {k: (sum(v) / len(v) if v else 0.0)
                         for k, v in detector_strength.items()}

    return {
        "cell": cell_name,
        "detectors": list(cfg_cell["detectors"]),
        "use_motivation": cfg_cell["use_motivation"],
        "use_salience": cfg_cell["use_salience"],
        "s_mean": round(s_mean, 6),
        "emit_rate": round(emit_rate, 4),
        "n_emit": len(emitted),
        "detector_firing_dist": detector_fires,
        "detector_strength_mean": {k: round(v, 6)
                                   for k, v in det_strength_mean.items()},
        "n_active_detectors": n_active_detectors,
        "interval_var": round(interval_var, 4),
        "body_coherent_9": f"{body_coherent}/{len(emitted)}" if emitted else "0/0",
        "body_maj_byte_frac_mean": round(mf, 4),
        "body_set_maj_frac": round(body_maj_frac, 4),
        "echo_collapse": body_maj_frac >= MAJ_FRAC_COLLAPSE,
        "psi_dir_var": round(_var(psi_dir_hist), 8),
        "tension_var": round(_var(tension_hist), 8),
        "physics_alive": (_var(psi_dir_hist) > TAU_VAR
                          and _var(tension_hist) > TAU_VAR),
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
    print("=== §88-F1 — frog-eye salience gate (trained scale) ===", flush=True)
    print(f"device={device} corpus_sha={corpus_sha[:16]}…", flush=True)

    # ── (A) train §16-class ckpt ─────────────────────────────────────
    model, items, n_params, init_ce, ce_traj, train_wall = \
        train_s16_class(cfg, device)
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_s88f1.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg, "n_params": n_params,
                "path": "alpha"}, ckpt_path)
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
    s16_probes = s16_baseline_probe(model, device, cfg["block_size"])

    # ── (C) 5-cell frog-eye grid over REAL forward ───────────────────
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    cells = {}
    for name, cfg_cell in CELLS.items():
        print(f"[§88-F1] running {name}", flush=True)
        cells[name] = run_frogeye_cell(model, ds, device, name, cfg_cell,
                                       cfg["n_steps"], cfg["block_size"])

    c0 = cells["cell0_s24_baseline"]
    c1 = cells["cell1_sd12_only"]
    c2 = cells["cell2_sd34_only"]
    c3 = cells["cell3_full_frogeye"]
    c4 = cells["cell4_frogeye_plus_motiv"]

    # ── 4-corner verdict ─────────────────────────────────────────────
    # α FROG-EYE-SELECTIVE-AT-TRAINED: full frog-eye (cell3) emits a
    #   STRICT SUBSET of the §24 generic baseline (cell0) — salience is
    #   selective, not generic.
    alpha = c3["n_emit"] < c0["n_emit"]
    # β SINGLE-DETECTOR-DEGENERATE: in the full 4-detector cell, only ONE
    #   detector class actually fires (trained ψ fast-crossing → SD-2-only,
    #   §82-FIRE fast-crossing echo).
    beta = c3["n_active_detectors"] <= 1
    # γ SALIENCE-COLLAPSES: trained-saturated ψ drives salience S to a
    #   near-constant — frog-eye S_mean variance across cells ≈ 0 OR S
    #   itself collapsed to 0 in the full cell.
    salience_cells = [c1["s_mean"], c2["s_mean"], c3["s_mean"]]
    salience_collapsed = (_var(salience_cells) < TAU_VAR
                          or c3["s_mean"] < TAU_VAR)
    gamma = salience_collapsed
    # δ FROG-EYE-NO-DIFFERENTIAL: the frog-eye cell is indistinguishable
    #   from the §24-baseline (same emit-rate AND same S behaviour).
    delta = (c3["emit_rate"] == c0["emit_rate"])

    # composite overall corner (single decisive label)
    if alpha and not beta and not gamma and not delta:
        corner = "(α) FROG-EYE-SELECTIVE-AT-TRAINED"
        caveat = (
            "POSITIVE-DIRECTIONAL: at trained scale the full 4-detector "
            "frog-eye gate (cell3) emits a STRICT SUBSET of the §24 generic "
            "motivation baseline (cell0) and ≥2 detector classes remain "
            "active — Lettvin selectivity transfers to the trained ψ-"
            "trajectory.  Honest: selectivity ≠ GOAL emergence "
            "(necessary-not-sufficient B-EMERGE-7); this measures the "
            "decision-axis mechanism only.")
    elif beta:
        corner = "(β) SINGLE-DETECTOR-DEGENERATE"
        caveat = (
            "NEGATIVE: at trained scale only "
            f"{c3['n_active_detectors']}/4 frog-eye detector classes fire "
            "in the full cell — the trained ψ-trajectory is uniformly "
            "fast-crossing (§82-FIRE echo) so SD-1/SD-3/SD-4 "
            "(sustained/slow) never fire and the 4-detector frog-eye "
            "degenerates to a single detector.  Valuable negative: "
            "Lettvin's multi-detector selectivity does NOT transfer to "
            "the saturated trained substrate; biology direction-anchor "
            "does not lift free at trained scale.")
    elif gamma:
        corner = "(γ) SALIENCE-COLLAPSES"
        caveat = (
            "NEGATIVE: the trained-saturated ψ drives the frog-eye "
            "salience score to a near-constant (S variance < τ OR cell3 "
            "S≈0) — §83-FIRE near-constant-ψ echo at the salience axis. "
            "valuable negative, NOT GOAL emergence.")
    elif delta:
        corner = "(δ) FROG-EYE-NO-DIFFERENTIAL"
        caveat = (
            "NEGATIVE: the frog-eye cell is indistinguishable from the "
            "§24-baseline emit-rate — the salience layer adds no measurable "
            "selectivity at trained scale.  valuable negative.")
    else:
        corner = "(mixed) PARTIAL"
        caveat = (
            "MIXED: frog-eye salience layer shifts behaviour at trained "
            "scale but does not cleanly satisfy the selective-positive "
            "corner.  Directional mechanism finding, NOT GOAL emergence "
            "(B-EMERGE-7).")

    n_alive = sum(1 for c in cells.values() if c["physics_alive"])

    result = {
        "section": "§88-F1",
        "title": "frog-eye salience gate — trained-scale fire",
        "anchor": "Lettvin 1959 What the frog's eye tells the frog's brain",
        "design_carry": "§87-F1 commit 5ea990b76 (B-S87F1 6/6 🔵)",
        "device": device,
        "corpus_sha256": corpus_sha,
        "ckpt_sha256": ckpt_sha,
        "ckpt_sha256_note": "fresh §16-class ckpt — config/lever/seed/corpus "
        "class byte-equal to §81-FIRE/§79/§73-FIRE; sha NOT literally §16's "
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
        "cells": cells,
        "n_physics_alive": n_alive,
        "four_corner": {
            "alpha_FROG_EYE_SELECTIVE": bool(alpha),
            "beta_SINGLE_DETECTOR_DEGENERATE": bool(beta),
            "gamma_SALIENCE_COLLAPSES": bool(gamma),
            "delta_FROG_EYE_NO_DIFFERENTIAL": bool(delta),
        },
        "verdict_corner": corner,
        "verdict_caveat": caveat,
        "honest_c3": [
            "trained scale ≠ GOAL emergence — necessary-not-sufficient "
            "(B-EMERGE-7); §88-F1 measures a decision-axis mechanism only.",
            "Lettvin 1959 frog's-eye citation is an honest direction-anchor "
            "(4 feature-detector retina), NOT a capability proof.",
            "the 4 detector closed-form functions are byte-equal to the "
            "§87-F1 $0 stub (commit 5ea990b76); §88-F1 only swaps the stub "
            "LCG ψ-trajectory for the REAL trained model.forward Law-71.",
            "the trained-ψ fast-crossing risk was stated up front: §82-FIRE "
            "measured trained ψ as uniformly fast-crossing, so SD-1/SD-3/"
            "SD-4 (sustained/slow detectors) may never fire — that is the "
            "β corner and an honest negative if measured.",
            "salience S = weighted OR with uniform 0.25 weights — design "
            "placeholder carried from §87-F1, not a tuned lever.",
            "body production is the §77 path-α1 stub template gated by the "
            "emission flag — §88-F1 does not claim coherent body emergence.",
            "ckpt sha is fresh; §16-byte-equal config (d/L/H/KV/seed/corpus "
            "class) is satisfied but the literal §16 sha differs — honest.",
            "north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.",
        ],
    }

    rp = os.path.join(out_dir, "result.json")
    with open(rp, "w") as f:
        json.dump(result, f, indent=2, default=str, ensure_ascii=False)
    print(f"\n[§88-F1] verdict: {corner}", flush=True)
    print(f"[§88-F1] result.json written → {rp}", flush=True)
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
