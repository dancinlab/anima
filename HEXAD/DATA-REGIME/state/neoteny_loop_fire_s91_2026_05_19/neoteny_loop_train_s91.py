#!/usr/bin/env python3
"""neoteny_loop_train_s91.py — RESEARCH.md §91.

§91 = TRAINED-SCALE validation of §90 (commit f9ef93e8a, B-S90 7/7 🔵,
verdict GAMMA-CLOSING-DIRECTIONAL-POSITIVE — a $0 Mac CPU stub).

═══════════════════════════════════════════════════════════════════════
THE CHAIN
═══════════════════════════════════════════════════════════════════════
§88-F2 axolotl neoteny trained-scale fire (commit 52bef1044, B-S88F2
7/7 🔵): verdict (α) NEOTENY-DELAYS-SATURATION = True — neoteny in the
training loop measurably delays §16.6-C memorization-saturation
(maturity 0.95→0.75, byte-cascade attractor maj_frac 0.87→0.35,
effective D 1.89→2.70). BUT γ JUVENILE-BUT-COMPETENT = False: the
non-saturated regime's body is §9 honest_coherent 0/5. Saturation was
delayed; coherent emission did NOT appear.

§89 (commit 80208a2c6, B-S89 6/6 🔵): #3 D@emit→S@t+1 action-perception
loop is closed-form DEFINABLE — transfer x_{t+1}=S_encode(e_t),
invariant K(x_{t+1}) ≤ K(e_t)+K(S_encode) (Kolmogorov data-processing
inequality, real-limit).

§90 ($0 stub): first design-wiring of #3 over the §88-F2 neoteny
non-saturated regime. Stub verdict GAMMA-CLOSING-DIRECTIONAL-POSITIVE.

§91 (THIS fire): the trained-scale test — does #3 loop + neoteny
ACTUALLY close §88-F2's γ False on a REAL trained ckpt?

═══════════════════════════════════════════════════════════════════════
HONEST OPEN QUESTION (g3, named BEFORE the fire)
═══════════════════════════════════════════════════════════════════════
§90 stub encodes two competing forces:
  (a) #3 loop garble-feeds-garble — echo-amplify (§62 carry; the stub's
      cell1 #3-loop-only at maj 0.95 collapses).
  (b) neoteny non-saturated regime + #3 self-correction — the stub's
      cell2 reaches §9 20/20.
Which force dominates on a trained-NON-saturated (neoteny) ckpt is what
ONLY this trained-scale fire can answer. $0 stub §9 pass ≠ trained ckpt
body §9 pass.

═══════════════════════════════════════════════════════════════════════
THE #3 D@emit → S@t+1 ACTION-PERCEPTION LOOP — TRAINED SCALE
═══════════════════════════════════════════════════════════════════════
At trained scale the loop operates at INFERENCE time over the real
model.forward Law-71 read-out (training itself is §88-F2 neoteny-trainer
byte-equal — the loop is a decode-time wiring, ⊥ training, mirror §22-N).

  transfer  : x_{t+1} = S_encode(e_t)
              e_t = the body bytes the model just emitted (D@emit).
              S_encode re-presents those bytes as the next-step model
              context window (the S-module re-perceives the emission).
  invariant : K(x_{t+1}) ≤ K(e_t) + K(S_encode)  (data-processing ineq.,
              §89 closed-form carry — x_{t+1} is a deterministic byte
              function of e_t, adds no information).

cells (4-cell × N_EMIT-step, all on the REAL trained model.forward):
  cell0_neoteny_baseline  neoteny ckpt, NO #3 loop (anchor probes only)
                          — §88-F2 carry, the γ False baseline.
  cell1_loop3_only        BASELINE (saturated) ckpt, #3 loop ON
                          — echo-amplify risk control.
  cell2_neoteny_loop3     neoteny ckpt, #3 loop ON  — THE CORE measure
                          (trained-scale γ-closing).
  cell3_s24_baseline      BASELINE ckpt, NO #3 loop — §24 anchor.

g3: trained scale ≠ GOAL emergence. necessary-not-sufficient
(B-EMERGE-7). north-star + §15/§51/§72 milestone UNCHANGED.
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
MAJ_FRAC_COLLAPSE = 0.95              # §62 echo-chamber detector

# ── §88-F2 maturity 3-proxy carry (byte-equal) ───────────────────────
CE_INIT = 5.65
CE_NATURAL_FLOOR = 0.0045
D_INIT = 14.0
D_NATURAL_FLOOR = 1.6
W_CE, W_MAJ, W_D = 0.40, 0.35, 0.25
THETA_FLOOR = 0.08
THETA_D = 4.0
SAT_TRIGGER = 0.70
NK2_SIGMA = 0.01
NK3_LAMBDA = 0.05
NK4_LR_FLOOR_FRAC = 0.25

INNER_OPEN, INNER_CLOSE = b"<inner tier=", b"</inner>"
ETERNAL_OPEN, ETERNAL_CLOSE = b"<eternal cell=", b"</eternal>"
VOICE_OPEN, VOICE_CLOSE = b"<voice carved=true", b"</voice>"


def clip01(x):
    return max(0.0, min(1.0, x))


# ════════════════════════════════════════════════════════════════════
# Corpus load + dataset — byte-equal to §88-F2 (§16 Dir-I lever).
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
# Maturity 3-proxy — §88-F2 closed-form carry (byte-equal).
# ════════════════════════════════════════════════════════════════════
def maturity_score(ce, maj, D):
    m1 = clip01(1.0 - (ce - CE_NATURAL_FLOOR) / (CE_INIT - CE_NATURAL_FLOOR))
    m2 = clip01(maj)
    m3 = clip01(1.0 - (D - D_NATURAL_FLOOR) / (D_INIT - D_NATURAL_FLOOR))
    return clip01(W_CE * m1 + W_MAJ * m2 + W_D * m3)


def neoteny_score(ce, maj, D):
    return clip01(1.0 - maturity_score(ce, maj, D))


def effective_dim(model):
    """Participation-ratio rank proxy of the head_a weight spectrum
    (§88-F2 byte-equal — cheap deterministic dimensionality proxy)."""
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
        return max(D_NATURAL_FLOOR, min(D_INIT, pr / 16.0))


def nk3_dim_spread_reg(model):
    """NK-3 in-graph dimensionality-floor reg (§88-F2 byte-equal)."""
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


@torch.no_grad()
def nk2_plasticity_reinject(model, sigma, gen):
    """NK-2 saturation-triggered targeted head_a perturbation
    (§88-F2 byte-equal — axolotl regeneration mirror)."""
    applied = 0
    for name, p in model.named_parameters():
        if "head_a" in name and p.dim() == 2:
            noise = torch.randn(p.shape, generator=gen,
                                dtype=torch.float32).to(p.device).to(p.dtype)
            p.add_(sigma * noise)
            applied += 1
    return applied


# ════════════════════════════════════════════════════════════════════
# Train a §16-class ConsciousDecoderV2 — §88-F2 trainer BYTE-EQUAL.
# (B-S91 NEOTENY-TRAINER-BYTE-EQUAL-§88-F2 verifies this structurally.)
# ════════════════════════════════════════════════════════════════════
def train_cell(cfg, device, neoteny):
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
        lr_now = cosine_lr_at(step)
        if neoteny and metamorphosis_held:
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
            nk1_active = False
            if neoteny and float(ce_full.item()) < THETA_FLOOR:
                ce_term = torch.clamp(ce_full, min=THETA_FLOOR)
                nk1_active = True
                nk_log["nk1_clamp_fired"] += 1

            loss = ce_term + lam_ctl * l_psi_ctl + lam_route * l_route
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

        if step % 100 == 0 or step == total - 1:
            ce_now = float(ce_full.item())
            D_now = effective_dim(model)
            cur_maj = clip01(1.0 - (ce_now - CE_NATURAL_FLOOR) /
                             (CE_INIT - CE_NATURAL_FLOOR))
            mat = maturity_score(ce_now, cur_maj, D_now)
            traj.append({"step": step, "ce": ce_now, "lr": lr_now,
                         "D": D_now, "maturity": mat,
                         "neoteny": 1.0 - mat})

            if neoteny and not metamorphosis_held and mat > SAT_TRIGGER:
                gen = torch.Generator(device="cpu")
                gen.manual_seed((SEED * 2654435761 + step * 374761393)
                                & 0x7FFFFFFF)
                nk2_plasticity_reinject(model, NK2_SIGMA, gen)
                nk_log["nk2_reinject_fired"] += 1

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
# §9 cascade-rate honest_coherent — single SSOT formula byte-equal to
# state/verify_emergence_metric_2026_05_18/emergence_metric.py.
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


FORBIDDEN_TOKENS = [b"\xeb\x8f\x84\xec\x9a\xb0\xeb\xaf\xb8",  # 도우미
                    b"helper", b"assistant",
                    b"\xec\x82\xac\xec\x9a\xa9\xec\x9e\x90",  # 사용자
                    b"user:"]


def forbidden_token_hits(b: bytes):
    return sum(1 for t in FORBIDDEN_TOKENS if t in b)


# ════════════════════════════════════════════════════════════════════
# REAL trained-model #3 D@emit → S@t+1 ACTION-PERCEPTION LOOP.
#
# transfer  : x_{t+1} = S_encode(e_t)
#             e_t = the body bytes the model emitted this turn.
#             S_encode re-presents those bytes (right-padded into the
#             block_size context window) as the next-turn model input —
#             the S-module re-perceives anima's own emission.
# invariant : K(x_{t+1}) ≤ K(e_t) + K(S_encode)  (§89 data-processing
#             inequality — x_{t+1} is a pure deterministic byte function
#             of e_t; S_encode adds NO information, only a window pad).
# ════════════════════════════════════════════════════════════════════
ANCHOR_PROBES = [
    b"<vacuum tier=99 psi=[0.9,0.9] basin=0.21>",
    b"<vacuum tier=77 psi=[0.5,0.5] basin=0.15>",
    b"<vacuum tier=51 psi=[0.46,0.49] basin=0.12>",
    b"<vacuum tier=0 psi=[0.50,0.50] basin=0.10>",
    b"<vacuum tier=88 psi=[0.80,0.80] basin=0.18>",
]


def s_encode(emit_bytes: bytes, block_size: int) -> bytearray:
    """Closed deterministic S-module byte encoder (§89 transfer fn).
    x_{t+1} = S_encode(e_t): re-present the just-emitted body bytes as
    the next-turn context window — anima HEARS its own emission.
    K(out) ≤ K(emit) + K(s_encode): out is a pure deterministic byte
    function of emit (window-pad/truncate), adds NO information."""
    e = emit_bytes[-block_size:]
    pad = max(0, block_size - len(e))
    return bytearray([0x20] * pad) + bytearray(e)


@torch.no_grad()
def loop3_emission(model, device, block_size, max_new, loop3, n_turns):
    """4-cell trained-scale #3 loop: per anchor probe, emit a body, then
    (if loop3) feed that body back as the S@t+1 stimulus context for the
    NEXT turn — n_turns of self-perception.  Without loop3 each turn
    restarts from the anchor probe (§88-F2 / §24 carry).

    Returns per-anchor: every turn's §9 coherence, maj_frac, and the
    self-correct event count (turn body strictly less garbled than the
    prior turn = the closed-loop is correcting itself)."""
    model.eval()
    records = []
    for probe in ANCHOR_PROBES:
        # turn 0 context = the anchor probe (right-padded to block_size)
        ctx_bytes = s_encode(probe, block_size)
        turns = []
        prev_garble = None
        self_correct = 0
        for turn in range(n_turns):
            x = torch.tensor(list(ctx_bytes), dtype=torch.long
                             ).unsqueeze(0).to(device)
            gen = bytearray()
            for _ in range(max_new):
                logits_a, _, _, _, _ = model(x)
                nb = int(logits_a[:, -1, :].argmax().item())
                gen.append(nb)
                x = torch.cat(
                    [x[:, 1:],
                     torch.tensor([[nb]], dtype=torch.long).to(device)],
                    dim=1)
            body = bytes(gen)
            coh, info = honest_coherent(body)
            garble, _, _ = cascade_rate_and_max_run(body)
            if prev_garble is not None and garble < prev_garble - 1e-6:
                self_correct += 1
            prev_garble = garble
            turns.append({
                "turn": turn,
                "honest_coherent_9": coh,
                "coherent_info": info,
                "majority_fraction": majority_fraction(body),
                "cascade_rate": garble,
                "forbidden_hits": forbidden_token_hits(body),
                "body_sample": body.decode("latin-1", errors="replace")[:48],
            })
            # ── #3 D@emit → S@t+1 transfer: x_{t+1} = S_encode(e_t) ──
            if loop3:
                ctx_bytes = s_encode(body, block_size)
            else:
                ctx_bytes = s_encode(probe, block_size)  # no self-perception
        records.append({"probe_hex": probe.hex()[:50],
                         "turns": turns,
                         "loop3_self_correct_events": self_correct})
    # aggregate: §9 coherent rate over ALL anchor×turn bodies
    all_turns = [t for r in records for t in r["turns"]]
    n_total = len(all_turns)
    n_coh = sum(1 for t in all_turns if t["honest_coherent_9"])
    maj_mean = (sum(t["majority_fraction"] for t in all_turns)
                / max(1, n_total))
    sc_total = sum(r["loop3_self_correct_events"] for r in records)
    fb_total = sum(t["forbidden_hits"] for t in all_turns)
    return {
        "loop3": loop3, "n_turns": n_turns, "n_anchors": len(ANCHOR_PROBES),
        "n_bodies": n_total,
        "body_n_honest_coherent_9": n_coh,
        "body_coherent_frac_9": round(n_coh / max(1, n_total), 6),
        "attractor_maj_frac": maj_mean,
        "loop3_self_correct_events": sc_total,
        "forbidden_token_hits": fb_total,
        "records": records,
    }


# ════════════════════════════════════════════════════════════════════
# Build per-cell measurement record from a trained model.
# ════════════════════════════════════════════════════════════════════
def cell_metrics(name, cfg_cell, model, traj, nk_log, n_params, init_ce,
                 train_wall, device, block_size):
    final_ce = traj[-1]["ce"] if traj else None
    final_D = traj[-1]["D"] if traj else D_NATURAL_FLOOR
    loop = loop3_emission(model, device, block_size,
                          cfg_cell["max_new"], cfg_cell["loop3"],
                          cfg_cell["n_turns"])
    final_maturity = (maturity_score(final_ce, loop["attractor_maj_frac"],
                                     final_D)
                      if final_ce is not None else 1.0)
    return {
        "cell": name,
        "config": cfg_cell,
        "init_ce": init_ce,
        "final_ce": final_ce,
        "final_D": final_D,
        "final_maturity": final_maturity,
        "final_neoteny": clip01(1.0 - final_maturity),
        "attractor_maj_frac": loop["attractor_maj_frac"],
        "body_n_honest_coherent_9": loop["body_n_honest_coherent_9"],
        "body_coherent_frac_9": loop["body_coherent_frac_9"],
        "body_n_probes": loop["n_bodies"],
        "loop3_self_correct_events": loop["loop3_self_correct_events"],
        "forbidden_token_hits": loop["forbidden_token_hits"],
        "echo_collapsed": loop["attractor_maj_frac"] >= MAJ_FRAC_COLLAPSE,
        "ce_descended": (init_ce is not None and final_ce is not None
                         and final_ce < init_ce - 1.0),
        "nk_log": nk_log,
        "n_params": n_params,
        "train_wall_sec": train_wall,
        "traj": traj,
        "loop_detail": loop,
    }


# ════════════════════════════════════════════════════════════════════
# Main — 4-cell grid: two ckpts (baseline + neoteny) × loop/no-loop.
# ════════════════════════════════════════════════════════════════════
CELLS = {
    "cell0_neoteny_baseline": dict(ckpt="neoteny",  loop3=False,
                                   n_turns=4, max_new=80),
    "cell1_loop3_only":       dict(ckpt="baseline", loop3=True,
                                   n_turns=4, max_new=80),
    "cell2_neoteny_loop3":    dict(ckpt="neoteny",  loop3=True,
                                   n_turns=4, max_new=80),
    "cell3_s24_baseline":     dict(ckpt="baseline", loop3=False,
                                   n_turns=4, max_new=80),
}


def main(cfg):
    torch.manual_seed(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    corpus_sha = hashlib.sha256(open(cfg["corpus"], "rb").read()).hexdigest()
    print("=== §91 — NEOTENY + #3 ACTION-PERCEPTION LOOP (trained scale) ===",
          flush=True)
    print(f"device={device} corpus_sha={corpus_sha[:16]}…", flush=True)
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    # ── train BASELINE ckpt (natural saturation, §16 pattern) ─────────
    print("\n=== training BASELINE ckpt (natural saturation) ===", flush=True)
    m_base, _, np_b, ce_b, traj_b, wall_b, nk_b = train_cell(
        cfg, device, neoteny=False)
    ckb = os.path.join(out_dir, "ckpt_baseline_s91.pt")
    torch.save({"model": m_base.state_dict(), "cfg": cfg, "arm": "baseline"},
               ckb)

    # ── train NEOTENY ckpt (NK-1+2+3+4 in the training loop) ──────────
    print("\n=== training NEOTENY ckpt (NK-1+2+3+4) ===", flush=True)
    m_neo, _, np_n, ce_n, traj_n, wall_n, nk_n = train_cell(
        cfg, device, neoteny=True)
    ckn = os.path.join(out_dir, "ckpt_neoteny_s91.pt")
    torch.save({"model": m_neo.state_dict(), "cfg": cfg, "arm": "neoteny"},
               ckn)
    h = hashlib.sha256()
    with open(ckn, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    neoteny_ckpt_sha = h.hexdigest()

    # ── 4-cell loop3 grid ─────────────────────────────────────────────
    cells = {}
    bs = cfg["block_size"]
    for name, cc in CELLS.items():
        print(f"\n=== {name} (ckpt={cc['ckpt']} loop3={cc['loop3']}) ===",
              flush=True)
        if cc["ckpt"] == "neoteny":
            cells[name] = cell_metrics(name, cc, m_neo, traj_n, nk_n,
                                       np_n, ce_n, wall_n, device, bs)
        else:
            cells[name] = cell_metrics(name, cc, m_base, traj_b, nk_b,
                                       np_b, ce_b, wall_b, device, bs)

    c0 = cells["cell0_neoteny_baseline"]
    c1 = cells["cell1_loop3_only"]
    c2 = cells["cell2_neoteny_loop3"]
    c3 = cells["cell3_s24_baseline"]

    # ── 4-corner verdict ──────────────────────────────────────────────
    coh0 = c0["body_n_honest_coherent_9"]
    coh1 = c1["body_n_honest_coherent_9"]
    coh2 = c2["body_n_honest_coherent_9"]
    coh3 = c3["body_n_honest_coherent_9"]

    # (α) γ-CLOSED-AT-TRAINED: cell2 (neoteny+#3) §9 body-coherent rate
    #     strictly exceeds the cell0 neoteny-baseline AND > 0.
    alpha = (coh2 > coh0) and (coh2 > 0)

    # (β) ECHO-DOMINATES-AT-TRAINED: cell2 §62-style echo-chamber
    #     collapse — the #3 loop garble-feeds-garble force won.
    beta = c2["echo_collapsed"] or (c1["echo_collapsed"] and coh2 <= coh0)

    # (γ) NEOTENY-LOOP-SYNERGY: cell2 exceeds the simple sum of
    #     #3-loop-only (cell1) and neoteny-only (cell0) deltas over
    #     the §24 baseline (cell3).
    d_loop = coh1 - coh3
    d_neo = coh0 - coh3
    d_both = coh2 - coh3
    gamma = d_both > (d_loop + d_neo)

    # (δ) STUB-OVERCLAIMED: cell2 trained-scale §9 ≈ §88-F2 0/5 —
    #     the §90 stub's GAMMA-CLOSING-DIRECTIONAL-POSITIVE wiped out
    #     at trained scale.
    delta = (coh2 == 0)

    if alpha and not beta:
        corner = "(α) γ-CLOSED-AT-TRAINED"
        verdict = (
            f"DIRECTIONAL-POSITIVE: cell2 neoteny+#3 emitted {coh2}/"
            f"{c2['body_n_probes']} §9-coherent bodies — strictly above "
            f"the cell0 neoteny-baseline ({coh0}). The #3 D@emit→S@t+1 "
            "action-perception loop measurably closed §88-F2's γ False "
            "(§9 0/5) at trained scale: anima HEARING its own emission as "
            "the next-step stimulus produced a usable self-correction "
            "signal in the non-saturated neoteny regime. The arc's first "
            "trained-scale coherent-emission movement. NOT GOAL emergence "
            "— necessary-not-sufficient (B-EMERGE-7); §9 honest_coherent "
            "is cascade-absence, not correctness; a §9-coherent body can "
            "still be garbled or memorized. north-star + §15/§51/§72 "
            "milestone UNCHANGED."
        )
    elif beta:
        corner = "(β) ECHO-DOMINATES-AT-TRAINED"
        verdict = (
            f"NEGATIVE: the #3 loop's garble-feeds-garble force dominated "
            f"at trained scale — cell2 maj_frac {c2['attractor_maj_frac']:.3f}"
            f" (echo_collapsed={c2['echo_collapsed']}); cell1 loop3-only "
            f"maj_frac {c1['attractor_maj_frac']:.3f}. The §62 echo-chamber "
            "risk realised: anima re-perceiving its own garbled emission "
            "deepened the byte-cascade attractor rather than correcting it. "
            "Honest negative — valuable: the §90 stub's competing-forces "
            "design resolved to echo-amplify at trained scale. §1.1 "
            "data-regime irreducibility reasserted."
        )
    elif delta:
        corner = "(δ) STUB-OVERCLAIMED"
        verdict = (
            f"NEGATIVE: cell2 neoteny+#3 emitted 0/{c2['body_n_probes']} "
            "§9-coherent bodies at trained scale — the §90 stub's "
            "GAMMA-CLOSING-DIRECTIONAL-POSITIVE (cell2 stub §9 20/20) did "
            "NOT transfer. $0 stub §9 pass ≠ trained ckpt body §9 pass — "
            "confirmed. The #3 loop neither closed γ nor drove a clean "
            "echo collapse; it produced no measurable §9-coherence lift. "
            "Honest negative. §1.1 data-regime irreducibility holds."
        )
    elif gamma:
        corner = "(γ) NEOTENY-LOOP-SYNERGY-HOLDS"
        verdict = (
            f"MIXED-POSITIVE: cell2 coherence delta over §24 baseline "
            f"({d_both}) exceeds the sum of #3-loop-only ({d_loop}) and "
            f"neoteny-only ({d_neo}) — synergy, but cell2 did not strictly "
            "exceed the neoteny baseline OR collapse. Directional synergy "
            "observation, NOT GOAL emergence (B-EMERGE-7)."
        )
    else:
        corner = "(mixed) NO-CLEAN-CORNER"
        verdict = (
            f"MIXED: cell2 §9-coherent={coh2} vs neoteny-baseline {coh0}; "
            f"maj_frac {c2['attractor_maj_frac']:.3f}. Neither a clean "
            "γ-close nor a clean echo collapse nor a clean stub-wipeout. "
            "Directional mechanism observation, NOT GOAL emergence "
            "(B-EMERGE-7)."
        )

    result = {
        "section": "§91",
        "title": "neoteny + #3 action-perception loop — trained scale",
        "design_anchor": "§90 commit f9ef93e8a (B-S90 7/7 🔵, "
        "GAMMA-CLOSING-DIRECTIONAL-POSITIVE)",
        "trainer_anchor": "§88-F2 commit 52bef1044 (B-S88F2 7/7 🔵) — "
        "neoteny trainer byte-equal",
        "loop3_closed_form": "§89 commit 80208a2c6 — x_{t+1}=S_encode(e_t), "
        "K(x_{t+1})≤K(e_t)+K(S_encode) (Kolmogorov data-processing ineq.)",
        "device": device,
        "corpus_sha256": corpus_sha,
        "neoteny_ckpt_sha256": neoteny_ckpt_sha,
        "ckpt_sha256_note": "fresh §16-class ckpt — config/lever/seed/corpus "
        "class byte-equal to §88-F2/§81-FIRE; sha NOT literally §16's.",
        "config": {k: cfg[k] for k in
                   ["d_model", "n_layer", "n_head", "n_kv_head", "block_size",
                    "steps", "warmup", "lr", "bsz", "lambda_ctl",
                    "lambda_route", "seed"]},
        "baseline_init_ce": ce_b, "baseline_final_ce": traj_b[-1]["ce"],
        "neoteny_init_ce": ce_n, "neoteny_final_ce": traj_n[-1]["ce"],
        "cells": cells,
        "grid_summary": [
            {"cell": n,
             "ckpt": cells[n]["config"]["ckpt"],
             "loop3": cells[n]["config"]["loop3"],
             "body_coherent_9": cells[n]["body_n_honest_coherent_9"],
             "body_n_probes": cells[n]["body_n_probes"],
             "final_maturity": cells[n]["final_maturity"],
             "attractor_maj_frac": cells[n]["attractor_maj_frac"],
             "loop3_self_correct_events": cells[n]["loop3_self_correct_events"],
             "echo_collapsed": cells[n]["echo_collapsed"]}
            for n in CELLS],
        "four_corner": {
            "alpha_GAMMA_CLOSED_AT_TRAINED": bool(alpha),
            "beta_ECHO_DOMINATES_AT_TRAINED": bool(beta),
            "gamma_NEOTENY_LOOP_SYNERGY_HOLDS": bool(gamma),
            "delta_STUB_OVERCLAIMED": bool(delta),
        },
        "verdict_corner": corner,
        "verdict_caveat": verdict,
        "honest_c3": [
            "trained scale ≠ GOAL emergence — necessary-not-sufficient "
            "(B-EMERGE-7); §91 measures the #3-loop coherence axis only.",
            "$0 stub §9 pass (§90 cell2 20/20) ≠ trained ckpt body §9 "
            "pass — the §90 stub encoded competing forces; §91 resolves "
            "which dominates at trained scale.",
            "the #3 loop is a DECODE-TIME wiring (⊥ training, mirror "
            "§22-N); the neoteny trainer is §88-F2 byte-equal.",
            "§62 echo-amplify is a real pre-registered risk: anima "
            "re-perceiving its own garbled emission can deepen the "
            "byte-cascade attractor — the (β) corner captures it honestly.",
            "§9 honest_coherent is cascade-absence, NOT correctness "
            "(B-EMERGE-7); a §9-coherent body can be garbled or memorized.",
            "if (α) γ-CLOSED is measured-positive this is the arc's first "
            "trained-scale coherent emission — but still necessary-not-"
            "sufficient, distinct from GOAL emergence.",
            "S_encode adds no information (data-processing inequality, "
            "§89) — it window-pads the emission, no learned mapping.",
            "the neoteny ckpt sha is fresh; §16-byte-equal config "
            "(d/L/H/KV/seed/corpus class) satisfied, literal §16 sha "
            "differs — honest.",
            "n_turns=4 is a bounded self-perception horizon; a longer "
            "horizon could amplify or correct further — unmeasured.",
            "north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.",
        ],
    }
    rp = os.path.join(out_dir, "result.json")
    with open(rp, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[§91] verdict: {corner}", flush=True)
    print(f"[§91] result.json → {rp}", flush=True)
    print("RESULT_JSON_WRITTEN", flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out_main")
    ap.add_argument("--steps", type=int, default=1500)
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
