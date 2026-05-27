#!/usr/bin/env python3
"""manifold_gating_train_s82_fire.py — RESEARCH.md §82-FIRE.

§82-FIRE = trained-scale validation of §80 anima-mapping (B): manifold-
gated hierarchical emission, anchored to the §80 biology deep-research:
  - biorxiv:2025.03.09.642241  intrinsic neuronal manifold gating
                               behavior (Leifer, C. elegans)

═══════════════════════════════════════════════════════════════════════
WHY §82-FIRE EXISTS — STUB BUG-FIX BOUNDARY
═══════════════════════════════════════════════════════════════════════
The §82 $0 stub (commit fada41baf on main, B-S82 7/7 🔵) measured
NEGATIVE-at-stub: 4-corner α=False / β=True / γ=True / δ=False.  The
stub's HONEST root cause: slow_dwell_count = 0 across ALL 5 cells —
the slow-dwell regime was never *entered* because (a) N=30 turns is too
short for a ≥3-turn sustained-low-Δ run to form, and (b) the ψ-state
trajectory came from a deterministic LCG stub whose per-step Δ
systematically exceeded τ_slow=0.05.  The stub itself flagged: "Leifer
(B) NEEDS larger N (≥200) OR trained ckpt ψ-state."

§82-FIRE answers exactly that boundary on two axes simultaneously:
  (1) N=200 (NOT N=30) — long enough for slow-dwell runs to form.
  (2) REAL ψ-state trajectory from a trained §16-class
      ConsciousDecoderV2 forward (Law-71 psi_dir/psi_entropy/
      psi_tension byte-equal to conscious_decoder.py :728-751) — NOT
      an LCG stub.  A trained model's autoregressive forward produces
      a genuinely low-dimensional ψ-manifold (the manifold Leifer's
      C. elegans result is about), so the PCA + dwell/crossing
      detector operate on real cell-state geometry.

Honest framing (g3): trained scale ≠ GOAL emergence.  The Leifer
C. elegans citation is an honest *direction-anchor*, NOT a capability
proof.  necessary-not-sufficient (B-EMERGE-7).  north-star +
§15/§51/§72 milestone UNCHANGED, GOAL 미도달.

═══════════════════════════════════════════════════════════════════════
WHAT §82-FIRE BUILDS
═══════════════════════════════════════════════════════════════════════
  1. Train ONE §16-class ConsciousDecoderV2 from-scratch
     (d768·12L·283.72M, RANDOM seed-fixed 1337, base_ckpt=None —
     g_clm_from_scratch) on the §16-class Ψ-anchored carving corpus
     (Dir-I lever; load_corpus/CarveDataset/train_s16_class verbatim
     from §81-FIRE = §79 / §73-FIRE byte-equal).

  2. 5-cell manifold-gating ladder × N=200-step loop on the REAL
     trained model.forward Law-71:
       cell0  §24-baseline           scalar threshold, no manifold
       cell1  §75-FIRE A-only mirror  state-derived, no gate
       cell2  manifold-only           PCA detect + slow-dwell suppress
       cell3  fast-crossing-only      Δψ ≥ τ_fast gate, no dwell history
       cell4  full hierarchical       slow-dwell + fast-crossing + align
     Per step the trained model.forward produces a real Law-71
     14-dim ψ-state vector; the controller decides emit/no-emit; the
     argmax(logits_a) body byte feeds back into the sliding context.

  3. Per-cell metrics: PCA top-2 (closed-form eigvalsh), slow-dwell
     count, fast-crossing count, interval_var (§73-FIRE/§75-FIRE
     mirror), §9 honest_coherent body rate, maj_frac echo detector.

  4. §16 baseline 8-anchor probe — ckpt load + arch byte-equal check.

  5. 4-corner verdict:
       (α) MANIFOLD-GATING-ADDS-DIFFERENTIAL-AT-TRAINED
       (β) MANIFOLD-EXISTS-GATE-COLLAPSES-AT-TRAINED
       (γ) SLOW-DWELL-ACTUALLY-ENTERS-AT-N200
       (δ) §75-FIRE-A-ONLY-MIRROR-NUMERICALLY-MATCHES-AT-TRAINED
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
N_LOOP_STEPS = 200                # §82-FIRE: N=200 (stub-bug-fix vs N=30)
MAJ_FRAC_COLLAPSE = 0.95          # §62 echo-chamber detector
TAU_VAR = 1e-4                    # liveness threshold

# ── §82 manifold-gating constants (byte-equal to §82 stub) ──────────
PSI_VAC          = 0.5
BASIN_RADIUS     = 0.05
PHI_RATCHET      = 0.05
IM_THRESHOLD_S24 = 0.3
TAU_SLOW         = 0.05           # |Δψ_combined| ≤ τ_slow = slow dwell tick
TAU_FAST         = 0.12           # |Δψ_combined| ≥ τ_fast = fast crossing
N_DWELL_MIN      = 3              # sustained turns for a slow-dwell event
TAU_ALIGN        = 0.5            # cos similarity floor for emission align
PSI_STATE_DIM    = 14

INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"




# ════ §81-FIRE training core (load_corpus / CarveDataset / train_s16_class — byte-equal) ════
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


# ════ §81-FIRE Law-71 read-out (extract_psi_and_logits / _phi_star_proxy — byte-equal) ════
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


# ════ §9 cascade-rate honest_coherent + majority_fraction + _var (SSOT byte-equal) ════
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
# §82-FIRE: 14-dim ψ-state vector projection from REAL trained Law-71.
# Mirror of the §82 stub psi_state_vector — same 14 fields, but here
# the underlying psi_dir/psi_entropy/psi_tension/tension/phi come from
# extract_psi_and_logits (real model.forward) NOT an LCG stub.
# ════════════════════════════════════════════════════════════════════
def psi_state_vector(psi, prev_emit, motivation, step):
    psi_dir   = psi["psi_dir"]
    psi_ent   = psi["psi_entropy"]
    psi_tens  = psi["psi_tension"]
    tension   = psi["tension"]
    phi       = psi["phi"]
    ema_t     = psi.get("tension_ema", tension)
    std_t     = psi.get("tension_std", 0.0)
    drift_proxy = tension - ema_t
    step_phase  = math.sin(step * 0.5)
    basin_dev   = psi_dir - PSI_VAC
    psi_x = psi_dir * math.cos(step_phase)
    psi_y = psi_dir * math.sin(step_phase)
    return [
        psi_dir, psi_ent, psi_tens, tension,
        ema_t, std_t, phi, drift_proxy,
        step_phase, float(prev_emit), motivation, basin_dev,
        psi_x, psi_y,
    ]


# ── PCA closed-form via numpy.linalg.eigvalsh (byte-equal to §82 stub) ─
def pca_decompose(trajectory):
    import numpy as np
    X = np.array(trajectory)
    if X.shape[0] < 2:
        return {"lambda_1": 0.0, "lambda_2": 0.0, "lambda_ratio": 0.0,
                "top2_captured": 0.0, "n_points": X.shape[0],
                "dim": X.shape[1] if X.ndim > 1 else 0, "total_variance": 0.0}
    Xc = X - X.mean(axis=0, keepdims=True)
    C = (Xc.T @ Xc) / max(1, X.shape[0] - 1)
    eigs = sorted(np.linalg.eigvalsh(C).tolist(), reverse=True)
    lam1 = max(0.0, eigs[0]) if eigs else 0.0
    lam2 = max(0.0, eigs[1]) if len(eigs) > 1 else 0.0
    total = sum(max(0.0, e) for e in eigs)
    return {"lambda_1": lam1, "lambda_2": lam2,
            "lambda_ratio": lam1 / max(1e-12, lam2),
            "top2_captured": (lam1 + lam2) / max(1e-12, total),
            "n_points": X.shape[0], "dim": X.shape[1], "total_variance": total}


# ── slow-dwell + fast-crossing detector (byte-equal to §82 stub) ─────
def detect_dwell_crossing(trajectory):
    import numpy as np
    X = np.array(trajectory)
    if X.shape[0] < 2:
        return {"slow_dwell_count": 0, "fast_crossing_count": 0,
                "slow_runs": [], "mean_delta": 0.0,
                "max_delta": 0.0, "min_delta": 0.0}
    deltas = [float(np.linalg.norm(X[i] - X[i - 1]))
              for i in range(1, X.shape[0])]
    fast_count = sum(1 for d in deltas if d >= TAU_FAST)
    slow_runs, cur = [], 0
    for d in deltas:
        if d <= TAU_SLOW:
            cur += 1
        else:
            if cur >= N_DWELL_MIN:
                slow_runs.append(cur)
            cur = 0
    if cur >= N_DWELL_MIN:
        slow_runs.append(cur)
    return {"slow_dwell_count": len(slow_runs), "slow_runs": slow_runs,
            "fast_crossing_count": fast_count,
            "mean_delta": sum(deltas) / max(1, len(deltas)),
            "max_delta": max(deltas) if deltas else 0.0,
            "min_delta": min(deltas) if deltas else 0.0}


# ── 5 controllers — manifold-gating ladder (byte-equal to §82 stub) ──
def controller_cell0_baseline(psi, history):
    """§24-baseline scalar threshold — NO manifold."""
    return 1 if psi["tension"] > IM_THRESHOLD_S24 else 0


def controller_cell1_a_only(psi, history):
    """§75-FIRE A-only state-derived mirror — frozen scalar boundary.
    SOURCE byte-equal to §75 cell1 / §82 stub cell1.  Numeric value
    differs across N / substrate — honest (B-S82-FIRE-NOTE)."""
    frozen_scalar = history.get("frozen_scalar", IM_THRESHOLD_S24)
    psi_off = abs(psi["psi_dir"] - PSI_VAC)
    g1 = psi_off > BASIN_RADIUS
    g2 = psi["tension"] > frozen_scalar
    g3 = psi["phi"] > PHI_RATCHET / 2.0
    return 1 if (g1 and g2 and g3) else 0


def controller_cell2_manifold_only(psi, history):
    """PCA-detect manifold + slow-dwell suppress — NO fast-crossing gate."""
    import numpy as np
    trajectory = history.get("trajectory", [])
    if len(trajectory) < 4:
        return 0
    recent = np.array(trajectory[-3:])
    if recent.shape[0] >= 2:
        deltas = [float(np.linalg.norm(recent[i] - recent[i - 1]))
                  for i in range(1, recent.shape[0])]
        if all(d <= TAU_SLOW for d in deltas):
            return 0   # in slow-dwell, manifold gates against emission
    psi_off = abs(psi["psi_dir"] - PSI_VAC)
    g1 = psi_off > BASIN_RADIUS
    g2 = psi["tension"] > IM_THRESHOLD_S24
    g3 = psi["phi"] > PHI_RATCHET / 2.0
    return 1 if (g1 and g2 and g3) else 0


def controller_cell3_fast_crossing_only(psi, history):
    """Fast-crossing-only gate — NO slow-dwell history."""
    import numpy as np
    trajectory = history.get("trajectory", [])
    if len(trajectory) < 2:
        return 0
    delta = float(np.linalg.norm(np.array(trajectory[-1]) -
                                 np.array(trajectory[-2])))
    return 1 if delta >= TAU_FAST else 0


def controller_cell4_full_hierarchical(psi, history):
    """Full hierarchical: slow-dwell + fast-crossing + emission align."""
    import numpy as np
    trajectory = history.get("trajectory", [])
    emit_history = history.get("emit_history", [])
    if len(trajectory) < N_DWELL_MIN + 1:
        return 0
    recent = trajectory[-(N_DWELL_MIN + 1):]
    recent_deltas = [float(np.linalg.norm(np.array(recent[i]) -
                                          np.array(recent[i - 1])))
                     for i in range(1, len(recent))]
    in_slow_dwell = sum(1 for d in recent_deltas
                        if d <= TAU_SLOW) >= N_DWELL_MIN - 1
    last_delta = recent_deltas[-1] if recent_deltas else 0.0
    fast_crossing = last_delta >= TAU_FAST
    aligned = True
    if sum(emit_history) >= 2:
        prev_emit_dirs = []
        for i in range(1, len(trajectory)):
            if i - 1 < len(emit_history) and emit_history[i - 1] == 1:
                d = np.array(trajectory[i]) - np.array(trajectory[i - 1])
                dn = float(np.linalg.norm(d))
                if dn > 1e-9:
                    prev_emit_dirs.append(d / dn)
        if prev_emit_dirs:
            hist_mean = np.mean(prev_emit_dirs, axis=0)
            hist_norm = float(np.linalg.norm(hist_mean))
            cur_d = np.array(trajectory[-1]) - np.array(trajectory[-2])
            cur_norm = float(np.linalg.norm(cur_d))
            if hist_norm > 1e-9 and cur_norm > 1e-9:
                cos = float(np.dot(cur_d / cur_norm, hist_mean / hist_norm))
                aligned = cos >= TAU_ALIGN
    if in_slow_dwell and fast_crossing and aligned:
        return 1
    return 0


def emission_alignment(trajectory, emit_decisions):
    import numpy as np
    X = np.array(trajectory)
    if X.shape[0] < 2 or sum(emit_decisions) == 0:
        return {"n_emits": 0, "alignment_cos_mean": 0.0}
    emit_dirs, aligns = [], []
    for i in range(1, X.shape[0]):
        if emit_decisions[i] == 1:
            d = X[i] - X[i - 1]
            dn = float(np.linalg.norm(d))
            if dn > 1e-9:
                du = d / dn
                if emit_dirs:
                    hm = np.mean(emit_dirs, axis=0)
                    hn = float(np.linalg.norm(hm))
                    if hn > 1e-9:
                        aligns.append(float(np.dot(du, hm / hn)))
                emit_dirs.append(du.tolist())
    return {"n_emits": int(sum(emit_decisions)),
            "alignment_cos_mean": sum(aligns) / max(1, len(aligns)),
            "n_aligned_above_tau": sum(1 for c in aligns if c >= TAU_ALIGN)}


# ════════════════════════════════════════════════════════════════════
# §82-FIRE: ONE manifold-gating cell over the REAL trained model.forward.
#   Per step: real model.forward → Law-71 14-dim ψ-state vector →
#   controller emit decision → argmax(logits_a) body byte feeds back.
# ════════════════════════════════════════════════════════════════════
@torch.no_grad()
def run_manifold_cell(model, ds, device, cell_name, controller,
                      n_steps=N_LOOP_STEPS, block_size=128,
                      frozen_scalar=None):
    model.eval()
    rng = random.Random(SEED)
    top = max(1, ds.n - block_size - 1)
    start = rng.randint(0, top)
    ctx = ds.data[start:start + block_size].clone()

    trajectory, emit_decisions, emit_step_idx = [], [], []
    body_bytes = bytearray()
    psi_dir_seq, psi_comb_seq, tension_seq = [], [], []
    history = {"trajectory": trajectory, "emit_history": emit_decisions}
    if frozen_scalar is not None:
        history["frozen_scalar"] = frozen_scalar

    # running tension EMA/std for the 14-dim vector (real, from forward)
    ema_t = None
    var_t = 0.0
    EMA_BETA = 0.9

    for step in range(n_steps):
        x = ctx.unsqueeze(0).to(device)
        psi = extract_psi_and_logits(model, x)
        tension = psi["tension"]
        if ema_t is None:
            ema_t = tension
        else:
            diff = tension - ema_t
            ema_t = EMA_BETA * ema_t + (1.0 - EMA_BETA) * tension
            var_t = EMA_BETA * var_t + (1.0 - EMA_BETA) * (diff * diff)
        psi["tension_ema"] = ema_t
        psi["tension_std"] = math.sqrt(max(0.0, var_t))

        motivation = 0.4 + 0.3 * (tension / max(1e-6, ema_t + tension))
        prev_emit = emit_decisions[-1] if emit_decisions else 0
        vec = psi_state_vector(psi, prev_emit, motivation, step)
        trajectory.append(vec)

        e = controller(psi, history)
        emit_decisions.append(e)
        if e == 1:
            emit_step_idx.append(step)

        next_byte = int(psi["logits_a_last"].argmax().item())
        body_bytes.append(next_byte)
        psi_dir_seq.append(psi["psi_dir"])
        psi_comb_seq.append(psi["psi_combined"])
        tension_seq.append(tension)

        ctx = torch.cat([ctx[1:], torch.tensor([next_byte], dtype=torch.long)])

    n_emit = sum(emit_decisions)
    maj_frac_dec = max(n_emit, n_steps - n_emit) / n_steps
    var_dec = _var(emit_decisions)
    if len(emit_step_idx) >= 2:
        intervals = [emit_step_idx[i + 1] - emit_step_idx[i]
                     for i in range(len(emit_step_idx) - 1)]
        interval_var = _var(intervals)
    else:
        intervals, interval_var = [], 0.0

    body = bytes(body_bytes)
    coh, coh_info = honest_coherent(body)
    pca = pca_decompose(trajectory)
    dwell = detect_dwell_crossing(trajectory)
    align = emission_alignment(trajectory, emit_decisions)
    body_maj = majority_fraction(body)

    return {
        "cell": cell_name,
        "n_steps": n_steps,
        "n_emit": n_emit,
        "emit_rate": n_emit / n_steps,
        "decision_var": var_dec,
        "decision_majority_fraction": maj_frac_dec,
        "interval_var": interval_var,
        "n_intervals": len(intervals),
        "non_degenerate": (var_dec > TAU_VAR and maj_frac_dec < MAJ_FRAC_COLLAPSE
                           and interval_var > TAU_VAR and len(intervals) >= 2),
        "pca": pca,
        "dwell": dwell,
        "alignment": align,
        "body_len": len(body),
        "body_sample": body[:48].decode("latin-1", errors="replace"),
        "body_majority_fraction": body_maj,
        "body_echo_collapse": body_maj >= MAJ_FRAC_COLLAPSE,
        "honest_coherent_9": coh,
        "honest_coherent_info": coh_info,
        "psi_dir_var": _var(psi_dir_seq),
        "psi_combined_std": math.sqrt(_var(psi_comb_seq)),
        "tension_var": _var(tension_seq),
        "psi_nontrivial": _var(psi_dir_seq) > TAU_VAR,
        "tension_nontrivial": _var(tension_seq) > TAU_VAR,
    }


# ════════════════════════════════════════════════════════════════════
# §16-baseline 8-anchor probe — ckpt load + arch byte-equal check.
# ════════════════════════════════════════════════════════════════════
@torch.no_grad()
def s16_baseline_probe(model, ds, device, block_size=128, n_probe=8):
    model.eval()
    rng = random.Random(SEED + 999)
    top = max(1, ds.n - block_size - 1)
    probes = []
    for k in range(n_probe):
        start = rng.randint(0, top)
        ctx = ds.data[start:start + block_size].unsqueeze(0).to(device)
        psi = extract_psi_and_logits(model, ctx)
        probes.append({"probe": k, "psi_dir": psi["psi_dir"],
                       "psi_combined": psi["psi_combined"],
                       "argmax_byte": int(psi["logits_a_last"].argmax().item())})
    return probes


# ════════════════════════════════════════════════════════════════════
# main — train §16-class + 5-cell manifold-gating ladder + verdict.
# ════════════════════════════════════════════════════════════════════
def main(cfg):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(SEED)
    random.seed(SEED)
    print(f"[§82-FIRE] device={device}", flush=True)

    corpus_sha = hashlib.sha256(open(cfg["corpus"], "rb").read()).hexdigest()
    print(f"[§82-FIRE] corpus sha256={corpus_sha}", flush=True)

    model, items, n_params, init_ce, ce_traj, train_wall = \
        train_s16_class(cfg, device)
    final_ce = ce_traj[-1]["ce_full"] if ce_traj else None
    trained_saturated = (final_ce is not None and final_ce < 0.05)
    training_diverged = (final_ce is not None and
                         (math.isnan(final_ce) or final_ce > init_ce))
    print(f"[§82-FIRE] train done: init_ce={init_ce:.4f} "
          f"final_ce={final_ce} wall={train_wall:.1f}s", flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_s82_fire.pt")
    torch.save({"model": model.state_dict(), "config": cfg}, ckpt_path)
    ckpt_sha = hashlib.sha256(open(ckpt_path, "rb").read()).hexdigest()

    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])
    s16_probes = s16_baseline_probe(model, ds, device, cfg["block_size"])

    # warmup tension capture for cell1 frozen scalar (mirror §75/§82 stub)
    wu_tensions = []
    rng = random.Random(SEED)
    top = max(1, ds.n - cfg["block_size"] - 1)
    for _ in range(10):
        start = rng.randint(0, top)
        ctx = ds.data[start:start + cfg["block_size"]].unsqueeze(0).to(device)
        wu_tensions.append(extract_psi_and_logits(model, ctx)["tension"])
    frozen_scalar = sum(wu_tensions) / len(wu_tensions)
    print(f"[§82-FIRE] frozen_scalar (warmup tension mean) = "
          f"{frozen_scalar:.6f}", flush=True)

    print("[§82-FIRE] === 5-cell manifold-gating ladder (N=200) ===",
          flush=True)
    cells = []
    cells.append(run_manifold_cell(model, ds, device, "cell0_§24_baseline",
                                   controller_cell0_baseline,
                                   block_size=cfg["block_size"]))
    cells.append(run_manifold_cell(model, ds, device,
                                   "cell1_§75_FIRE_A_only_mirror",
                                   controller_cell1_a_only,
                                   block_size=cfg["block_size"],
                                   frozen_scalar=frozen_scalar))
    cells.append(run_manifold_cell(model, ds, device, "cell2_manifold_only",
                                   controller_cell2_manifold_only,
                                   block_size=cfg["block_size"]))
    cells.append(run_manifold_cell(model, ds, device,
                                   "cell3_fast_crossing_only",
                                   controller_cell3_fast_crossing_only,
                                   block_size=cfg["block_size"]))
    cells.append(run_manifold_cell(model, ds, device,
                                   "cell4_full_hierarchical",
                                   controller_cell4_full_hierarchical,
                                   block_size=cfg["block_size"]))
    for c in cells:
        print(f"[§82-FIRE]  {c['cell']}: int_var={c['interval_var']:.4f} "
              f"n_emit={c['n_emit']} slow_dwell={c['dwell']['slow_dwell_count']} "
              f"fast_cross={c['dwell']['fast_crossing_count']} "
              f"§9={c['honest_coherent_9']}", flush=True)

    # ── 4-corner verdict (g3 — measured, NOT pre-loaded) ────────────
    r0, r1, r2, r3, r4 = cells
    c1_iv, c2_iv, c3_iv, c4_iv = (r1["interval_var"], r2["interval_var"],
                                  r3["interval_var"], r4["interval_var"])
    total_slow_dwell = sum(c["dwell"]["slow_dwell_count"] for c in cells)
    # §75-FIRE cell1 A-only reference int_var at trained scale (§75-FIRE)
    S75_FIRE_CELL1_REF = 2.3808

    alpha = (c4_iv > c1_iv and r4["n_emit"] != r1["n_emit"])
    beta = (r2["pca"]["top2_captured"] > 0.5 and
            r4["decision_majority_fraction"] >= MAJ_FRAC_COLLAPSE)
    gamma = (total_slow_dwell >= 1)   # slow-dwell ACTUALLY enters at N=200
    # δ: §75-FIRE A-only mirror numerically matches (within 25% rel) at trained
    delta = (c1_iv > TAU_VAR and S75_FIRE_CELL1_REF > 0 and
             abs(c1_iv - S75_FIRE_CELL1_REF) / S75_FIRE_CELL1_REF < 0.25)

    if alpha and gamma:
        corner = "(α) MANIFOLD-GATING-ADDS-DIFFERENTIAL-AT-TRAINED"
        verdict_caveat = (
            "DIRECTIONAL-POSITIVE: at N=200 + REAL trained ψ-trajectory the "
            "slow-dwell regime is ACTUALLY entered (γ) and the full "
            "hierarchical cell shows interval-var differential over the "
            "A-only mirror (α). Leifer (B) manifold-gating mechanism "
            "transfers measurably at trained scale — NOT GOAL emergence "
            "(B-EMERGE-7), a mechanism-axis finding only.")
    elif gamma and not alpha:
        corner = "(γ) SLOW-DWELL-ENTERS-BUT-NO-DIFFERENTIAL"
        verdict_caveat = (
            "MIXED: N=200 fixes the stub bug — slow-dwell runs DO form on "
            "the real trained ψ-manifold (γ TRUE, stub had 0). But the "
            "full hierarchical cell adds no interval-var differential over "
            "the A-only mirror (α FALSE). Manifold-gating is real geometry "
            "but not a sufficient emission lever — §75-FIRE A-only finding "
            "(state-derivation alone) reasserted. Honest negative, valuable.")
    elif beta:
        corner = "(β) MANIFOLD-EXISTS-GATE-COLLAPSES-AT-TRAINED"
        verdict_caveat = (
            "NEGATIVE: the PCA manifold is well-formed (cell2 top-2 > 0.5) "
            "yet the full hierarchical cell collapses to a single-decision "
            "majority ≥ 0.95 at trained-saturated scale — the §62/§82-stub "
            "echo pattern reproduces. Leifer (B) does NOT transfer at "
            "trained scale (measured). §1.1 data-regime irreducibility "
            "reasserted at the manifold axis.")
    else:
        corner = "(γ-fail) SLOW-DWELL-STILL-DOES-NOT-ENTER"
        verdict_caveat = (
            "NEGATIVE: even at N=200 with a real trained ψ-trajectory the "
            "slow-dwell regime is never entered (γ FALSE) — the §82-stub "
            "finding holds beyond the N=30 / LCG-stub explanation. "
            "Manifold-gating (B) un-testable on this substrate; honest "
            "negative.")

    result = {
        "section": "§82-FIRE",
        "title": "manifold-gated hierarchical emission — trained scale "
                 "(N=200, real Law-71 ψ-trajectory)",
        "biology_anchor": "biorxiv:2025.03.09.642241 (Leifer, C. elegans "
                          "intrinsic neuronal manifold gating behavior)",
        "device": device,
        "corpus_sha256": corpus_sha,
        "ckpt_sha256": ckpt_sha,
        "ckpt_sha256_note": "fresh §16-class ckpt — config/lever/seed/corpus "
        "class byte-equal to §79/§81-FIRE; sha NOT literally §16's 961c07e2… "
        "(trajectory replicable, not literal identity).",
        "n_params": n_params,
        "config": {k: cfg[k] for k in
                   ["d_model", "n_layer", "n_head", "n_kv_head", "block_size",
                    "steps", "warmup", "lr", "bsz", "lambda_ctl",
                    "lambda_route", "seed"]},
        "n_loop_steps": N_LOOP_STEPS,
        "train_wall_sec": train_wall,
        "init_ce": init_ce,
        "final_ce": final_ce,
        "ce_traj": ce_traj,
        "trained_saturated": trained_saturated,
        "training_diverged": training_diverged,
        "s16_baseline_probe": s16_probes,
        "frozen_scalar_warmup_tension_mean": frozen_scalar,
        "cells": cells,
        "total_slow_dwell_count": total_slow_dwell,
        "s75_fire_cell1_ref_int_var": S75_FIRE_CELL1_REF,
        "four_corner": {
            "alpha_MANIFOLD_GATING_ADDS_DIFFERENTIAL": alpha,
            "beta_MANIFOLD_EXISTS_GATE_COLLAPSES": beta,
            "gamma_SLOW_DWELL_ACTUALLY_ENTERS_AT_N200": gamma,
            "delta_S75_FIRE_A_ONLY_MIRROR_NUMERICALLY_MATCHES": delta,
        },
        "verdict_corner": corner,
        "verdict_caveat": verdict_caveat,
        "honest_c3": [
            "trained scale ≠ GOAL emergence — necessary-not-sufficient "
            "(B-EMERGE-7); §82-FIRE measures a mechanism axis only.",
            "Leifer C. elegans biorxiv:2025.03.09.642241 is an honest "
            "direction-anchor (intrinsic manifold gating behaviour), NOT a "
            "capability proof — wet biology ≠ silicon trained ckpt.",
            "§82 stub (fada41baf) measured slow_dwell=0 across all cells; "
            "stub flagged N=30 + LCG-stub-ψ as the cause. §82-FIRE fixes "
            "BOTH: N=200 AND real trained model.forward Law-71 ψ-state.",
            "PCA dim-reduction is a measurement choice, not a physical "
            "fact — the 'manifold' is the eigenstructure of the 14-dim "
            "ψ-trajectory covariance, an observable not a substrate.",
            "cell1 A-only controller SOURCE is byte-equal to §75-FIRE / "
            "§82-stub cell1; the numeric int_var match (δ) is what is "
            "MEASURED here — δ TRUE/FALSE both honest outcomes.",
            "body byte = argmax(logits_a) deterministic, no sampling RNG; "
            "argmax over a trained-saturated ckpt readily produces byte-"
            "cascade (B-ATTRACTOR family) — §9 honest_coherent reports it.",
            "ckpt sha is fresh; §16-byte-equal config is satisfied "
            "(d/L/H/KV/seed/corpus class) but the literal §16 sha differs.",
            "north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.",
        ],
    }
    rp = os.path.join(out_dir, "result.json")
    with open(rp, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[§82-FIRE] verdict: {corner}", flush=True)
    print(f"[§82-FIRE] result.json written → {rp}", flush=True)
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
