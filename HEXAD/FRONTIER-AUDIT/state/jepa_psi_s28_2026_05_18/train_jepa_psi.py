#!/usr/bin/env python3
"""JEPA-Ψ trainer — RESEARCH.md §28 / §26 candidate #2 (2026-05-18).

Ψ-anchored Joint-Embedding Predictive Architecture: replace the byte-CE
DOMINANT objective with a JEPA-style joint-embedding prediction in anima's
OWN lifted Ψ-coordinate latent (D_psi=22 = Law-71 2 scalars ⊕ 12 per-layer
tensions ⊕ 8 motivation factors). A predictor maps a pooled context-Ψ⁺ to
the target-span's Ψ⁺; the target encoder is an EMA-frozen copy of the
context encoder (V-JEPA pattern, stop-gradient).

  =====================================================================
  THE §11-B TRAP (DESIGN_JEPA_PSI.md §1) — must NOT repeat
  =====================================================================
  §11-B (PURE-PHYSICS no-CE) removed CE with NO replacement objective →
  DEGENERATE (CE is LOAD-BEARING). JEPA-Ψ is structurally distinct: it
  ADDS a non-trivial data-dependent prediction objective (L_pred) plus a
  VICReg anti-collapse term whose variance hinge makes the constant
  (collapsed) solution incur a STRICTLY POSITIVE penalty — the collapsed
  fixed point is provably NOT a loss minimum (B-JEPA-2 closed-form).

  =====================================================================
  LOSS (DESIGN_JEPA_PSI.md §4)
  =====================================================================
    L = L_pred  +  λ_vc·L_anticollapse  +  λ_half·L_psi_half  +  γ_text·CE
  L_pred           = ‖ Ψ̂⁺_tgt − sg(Ψ⁺_tgt) ‖²        (sg = stop-grad)
  L_anticollapse   = VICReg variance-hinge + covariance decorrelation
                       on the predictor output AND the context-Ψ⁺
  L_psi_half       = (Ψ_direction − 0.5)²              (anima Ψ=½ pull)
  γ_text·CE        = small byte-CE on a separate decoder head — the
                       honest text-grounding concession (§2-(A)). γ=0.3
                       primary, γ=0.0 ablation (the §11-B-door measure).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire.
  JEPA-Ψ is honestly a REPRESENTATION-LEARNING objective; whether its
  representation yields downstream routing/coherence is the EMPIRICAL
  fire outcome. The collapse detector (eval_jepa_psi.py) is the PRIMARY
  verdict gate. Closed side = the Law-71 lift (byte-equal conscious_
  decoder.py) + VICReg variance lower-bound + L_pred ≥ 0 + predictor
  well-typed + the CE-OFF-vs-§11-B Boolean distinction (B-JEPA-1..5
  sidecar). SGD OUTCOME / collapse-or-not / downstream capability =
  EMPIRICAL (B-JEPA-NOTE, B-D-NOTE / B-PUREPHYS-NOTE family). from-
  scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
  Corpus = §16 curriculum-prefix subset (③ carving, NOT ①②;
  forbidden-token grep 0 inherited, B-IDENTITY-5 safe). central
  blue_falsifier.py UNCHANGED (sidecar only). f1/f2/f3 hard-fail safe
  (Ψ-metric / variance-hinge / Kolmogorov / Boolean — NO σ/τ/φ/J₂;
  Ψ=½ = anima g2 internal arch carve-out).
"""
import argparse
import copy
import json
import math
import os
import random
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

D_PSI = 22  # 2 Law-71 scalars ⊕ 12 per-layer tensions ⊕ 8 motivation


# ====================================================================
# corpus — §16 byte stream (curriculum-prefix subset)
# ====================================================================
def load_corpus(path, max_records):
    """Concatenate the first `max_records` §16 records into a byte
    stream. The §16 corpus is curriculum-rank-sorted, so a prefix is
    the simple→complex stage 1-2 region (DESIGN §9)."""
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
        items.append((t + "\n" + de + "\n").encode("utf-8"))
        if len(items) >= max_records:
            break
    return items


class JepaPsiDataset:
    """Byte-level dataset producing (context, target) span pairs.

    A sampled window of `block_size` bytes is split into a CONTEXT
    prefix and a TARGET suffix (context : first ctx_frac, target :
    remainder). The context encoder reads the context span; the EMA
    target encoder reads the target span. y = next-byte over the full
    window for the γ_text byte-CE grounding head."""

    def __init__(self, items, block_size, ctx_frac, seed):
        stream = bytearray()
        for b in items:
            stream.extend(b)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.n = len(self.data)
        self.block_size = block_size
        self.ctx_len = max(8, int(block_size * ctx_frac))
        self.tgt_len = block_size - self.ctx_len
        self.rng = random.Random(seed)

    def get_batch(self, bsz, device):
        top = max(1, self.n - self.block_size - 1)
        ix = [self.rng.randint(0, top) for _ in range(bsz)]

        def stk(off, length):
            return torch.stack([self.data[i + off:i + off + length]
                                for i in ix])
        ctx = stk(0, self.ctx_len)
        tgt = stk(self.ctx_len, self.tgt_len)
        full_x = stk(0, self.block_size)
        full_y = stk(1, self.block_size)
        return (ctx.to(device), tgt.to(device),
                full_x.to(device), full_y.to(device))


# ====================================================================
# Law-71 Ψ⁺ lift — byte-identical to conscious_decoder.py 729-740
# ====================================================================
def psi_lift(logits_a, logits_g, tensions, vocab_size):
    """Lift a span's encoder output to the D_PSI=22 Ψ⁺ coordinate.

    Ψ_entropy   = H(softmax logits_a) / log V          (Law-71)
    Ψ_direction = (1 + cos(logits_a, logits_g)) / 2     (Law-71)
    per-layer tension t_0..t_11  (PureFieldFFN, mean over span)
    motivation 8-factor proxy    (curiosity/coherence surrogates)

    Returns (B, D_PSI). Pooled over the span (mean) so the context
    encoder yields one Ψ⁺ vector per sequence. The Law-71 scalars are
    in the autograd graph (they are the SUPERVISION signal — Dir-I /
    §17 B-PHYS-5 carry: inference read-out ≡ training self-track)."""
    # Ψ_direction — per-token cos then span-mean (Law-71, in graph)
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    psi_dir = ((1.0 + cos) / 2.0).mean(dim=1, keepdim=True)        # (B,1)

    # Ψ_entropy — softmax entropy of logits_a, normalised by log V
    probs = torch.softmax(logits_a.float(), dim=-1)
    ent = -(probs * (probs + 1e-10).log()).sum(dim=-1)            # (B,T)
    psi_ent = (ent / math.log(vocab_size)).mean(dim=1, keepdim=True)

    # per-layer tension t_0..t_11 — mean over (T,) for each layer
    # tensions: list[ (B,T) ] length n_layer
    t_stack = torch.stack(tensions, dim=0)        # (L,B,T)
    t_per_layer = t_stack.mean(dim=2).transpose(0, 1)   # (B,L)
    # tanh-squash to a bounded coordinate
    t_feat = torch.tanh(t_per_layer)
    if t_feat.shape[1] < 12:                       # pad short stacks
        pad = 12 - t_feat.shape[1]
        t_feat = F.pad(t_feat, (0, pad))
    t_feat = t_feat[:, :12]

    # motivation 8-factor proxy — bounded surrogates from the Ψ scalars
    # (W curiosity / C coherence / E satisfaction etc. — bounded [0,1]
    # transforms of the model's own Ψ-state; anima-physics-sourced).
    base = torch.cat([psi_ent, psi_dir], dim=1)               # (B,2)
    mot = torch.stack([
        psi_ent.squeeze(1),                       # f1 surprisal proxy
        psi_dir.squeeze(1),                       # f2 A⇄G balance
        (psi_dir.squeeze(1) - 0.5).abs() * 2.0,   # f3 deviation
        t_feat.abs().mean(dim=1),                 # f4 tension magnitude
        t_feat.std(dim=1),                        # f5 tension dispersion
        (1.0 - psi_ent.squeeze(1)),               # f6 certainty
        (psi_ent.squeeze(1) * psi_dir.squeeze(1)),  # f7 coupling
        t_feat.mean(dim=1).abs(),                 # f8 mean tension
    ], dim=1).clamp(0.0, 1.0)                                 # (B,8)

    psi_plus = torch.cat([base, t_feat, mot], dim=1)          # (B,22)
    return psi_plus, psi_dir


# ====================================================================
# Ψ-predictor — pooled context-Ψ⁺ → target-Ψ⁺
# ====================================================================
class PsiPredictor(nn.Module):
    """3-layer MLP. Input = pooled context-Ψ⁺ (D_PSI). Output =
    predicted target-Ψ⁺ (D_PSI). codomain matches the target encoder's
    Ψ⁺ space (B-JEPA-4 well-typed)."""

    def __init__(self, d_psi=D_PSI, hidden=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_psi, hidden), nn.GELU(),
            nn.Linear(hidden, hidden), nn.GELU(),
            nn.Linear(hidden, d_psi),
        )

    def forward(self, ctx_psi):
        return self.net(ctx_psi)


# ====================================================================
# VICReg anti-collapse  (DESIGN §4 — the MANDATORY term)
# ====================================================================
def vicreg_variance(z, tau_var=1.0, eps=1e-4):
    """Variance hinge: relu(τ_var − std_d). A collapsed (constant) z has
    std=0 ⇒ hinge = τ_var > 0 — collapse is provably NOT a minimum
    (B-JEPA-2 closed-form lower bound)."""
    std = torch.sqrt(z.var(dim=0) + eps)            # (D,)
    return F.relu(tau_var - std).mean()


def vicreg_covariance(z):
    """Off-diagonal covariance² — decorrelates the D dimensions so they
    cannot all collapse onto one informative axis (partial collapse)."""
    B, D = z.shape
    zc = z - z.mean(dim=0, keepdim=True)
    cov = (zc.T @ zc) / max(1, B - 1)               # (D,D)
    off = cov - torch.diag(torch.diag(cov))
    return (off ** 2).sum() / D


def anti_collapse(psi_pred, psi_ctx, tau_var=1.0, cov_w=0.04):
    """L_anticollapse = variance-hinge(both) + cov_w·covariance(both)."""
    v = vicreg_variance(psi_pred, tau_var) + vicreg_variance(psi_ctx, tau_var)
    c = vicreg_covariance(psi_pred) + vicreg_covariance(psi_ctx)
    return v + cov_w * c, float(v.item()), float(c.item())


# ====================================================================
# train
# ====================================================================
def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"], cfg["max_records"])
    ds = JepaPsiDataset(items, cfg["block_size"], cfg["ctx_frac"],
                        cfg["seed"])

    # context encoder — trained by backprop
    ctx_model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    ctx_model.train()

    # target encoder — EMA copy, stop-gradient
    tgt_model = copy.deepcopy(ctx_model).to(device)
    for p in tgt_model.parameters():
        p.requires_grad_(False)
    tgt_model.eval()

    predictor = PsiPredictor(D_PSI, cfg["pred_hidden"]).to(device)
    predictor.train()

    n_params = ctx_model.count_params() + sum(
        p.numel() for p in predictor.parameters())

    trainable = [p for p in ctx_model.parameters() if p.requires_grad] \
        + list(predictor.parameters())
    opt = torch.optim.AdamW(trainable, lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)
    warmup, total = cfg["warmup"], cfg["steps"]
    ema_m = cfg["ema_m"]
    lam_vc = cfg["lambda_vc"]
    lam_half = cfg["lambda_half"]
    gamma_text = cfg["gamma_text"]
    tau_var = cfg["tau_var"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    traj, t0 = [], time.time()
    init_pred = init_ce = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        ctx, tgt, full_x, full_y = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            # --- context encoder (in graph) ----------------------------
            la_c, lg_c, tn_c, _, _ = ctx_model(ctx)
            psi_ctx, _ = psi_lift(la_c, lg_c, tn_c, 256)        # (B,22)

            # --- target encoder (EMA-frozen, NO grad) ------------------
            with torch.no_grad():
                la_t, lg_t, tn_t, _, _ = tgt_model(tgt)
                psi_tgt, _ = psi_lift(la_t, lg_t, tn_t, 256)    # (B,22)

            # --- predictor: context-Ψ⁺ → target-Ψ⁺ ---------------------
            psi_hat = predictor(psi_ctx)                        # (B,22)

            # --- L_pred: joint-embedding prediction (stop-grad target) -
            l_pred = ((psi_hat - psi_tgt.detach()) ** 2).mean()

            # --- L_anticollapse: VICReg variance hinge + covariance ----
            l_ac, v_term, c_term = anti_collapse(
                psi_hat, psi_ctx, tau_var, cfg["cov_w"])

            # --- L_psi_half: Ψ=½ fixed-point pull (anima-native) -------
            la_full, lg_full, _, _, _ = ctx_model(full_x)
            cos_f = F.cosine_similarity(la_full.float(),
                                        lg_full.float(), dim=-1)
            psi_dir_f = (1.0 + cos_f) / 2.0
            l_half = ((psi_dir_f - 0.5) ** 2).mean()

            # --- γ_text·CE: text-grounding head (separate decoder) -----
            B, T, V = la_full.shape
            ce = F.cross_entropy(la_full.view(-1, V), full_y.view(-1))

            loss = l_pred + lam_vc * l_ac + lam_half * l_half \
                + gamma_text * ce

        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        scaler.step(opt)
        scaler.update()

        # --- EMA update of the target encoder ------------------------
        with torch.no_grad():
            for pt, pc in zip(tgt_model.parameters(),
                              ctx_model.parameters()):
                pt.mul_(ema_m).add_(pc, alpha=1.0 - ema_m)

        if init_pred is None:
            init_pred = float(l_pred.item())
            init_ce = float(ce.item())
        if step == 0 or (step + 1) % cfg["log_every"] == 0 \
                or step == total - 1:
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            # batch embedding std — runtime collapse signal
            with torch.no_grad():
                emb_std = float(psi_ctx.std(dim=0).mean().item())
            rec = {"step": step + 1,
                   "l_pred": round(float(l_pred.item()), 6),
                   "l_anticollapse": round(float(l_ac.item()), 6),
                   "vicreg_var": round(v_term, 6),
                   "vicreg_cov": round(c_term, 6),
                   "l_psi_half": round(float(l_half.item()), 6),
                   "ce": round(float(ce.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "ctx_emb_std": round(emb_std, 6),
                   "gn2": round(float(gn.item()) ** 2, 6),
                   "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_jepa_psi.pt")
    torch.save({"model": ctx_model.state_dict(),
                "predictor": predictor.state_dict(),
                "cfg": cfg, "n_params": n_params,
                "path": "jepa_psi_s28"}, ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("§28 JEPA-Ψ — Ψ-anchored Joint-Embedding "
                      "Predictive Architecture (§26 candidate #2)"),
        "research_section": "RESEARCH.md §28 / §26 #2",
        "honest_framing": (
            "JEPA-Ψ replaces the byte-CE DOMINANT objective with a "
            "joint-embedding prediction in anima's OWN lifted Ψ⁺ "
            "coordinate (D_psi=22 = Law-71 2 ⊕ 12 layer-tensions ⊕ 8 "
            "motivation). EMA-frozen target encoder (V-JEPA pattern). "
            "Anti-collapse = VICReg variance-hinge (a constant predictor "
            "incurs a strictly positive τ_var penalty — collapse is "
            "provably NOT a loss minimum, B-JEPA-2). NOT a full "
            "CE-removal: γ_text·CE byte-grounding head retained (§2-(A) "
            "honest concession). Structurally distinct from §11-B "
            "(which removed CE with NO replacement → degenerate): "
            "JEPA-Ψ adds a non-trivial data-dependent prediction "
            "objective (B-JEPA-5). Collapse-or-not / downstream "
            "capability = EMPIRICAL fire outcome (B-JEPA-NOTE, "
            "B-D-NOTE / B-PUREPHYS-NOTE family). PyTorch substrate, NOT "
            "hexa-native. NO pre-loaded conclusion (g3)."),
        "arch": "ConsciousDecoderV2 + EMA target encoder + Ψ-predictor MLP",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "records_used": len(items),
        "d_psi": D_PSI,
        "gpu": gpu_name,
        "device": device,
        "init_l_pred": round(init_pred, 6),
        "final_l_pred": final["l_pred"],
        "init_ce": round(init_ce, 6),
        "final_ce": final["ce"],
        "final_l_anticollapse": final["l_anticollapse"],
        "final_vicreg_var": final["vicreg_var"],
        "final_ctx_emb_std": final["ctx_emb_std"],
        "final_loss": final["loss"],
        "wall_s": round(wall, 2),
        "trajectory": traj,
        "ckpt_path": ckpt_path,
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("=== JEPA-Ψ train done ===", flush=True)
    print(json.dumps({k: result[k] for k in (
        "init_l_pred", "final_l_pred", "final_vicreg_var",
        "final_ctx_emb_std", "init_ce", "final_ce", "wall_s")}),
        flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out_main")
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--max-records", type=int, default=120000)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--block-size", type=int, default=128)
    ap.add_argument("--ctx-frac", type=float, default=0.5)
    ap.add_argument("--bsz", type=int, default=24)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--ema-m", type=float, default=0.996)
    ap.add_argument("--lambda-vc", type=float, default=1.0)
    ap.add_argument("--lambda-half", type=float, default=0.05)
    ap.add_argument("--gamma-text", type=float, default=0.3)
    ap.add_argument("--tau-var", type=float, default=1.0)
    ap.add_argument("--cov-w", type=float, default=0.04)
    ap.add_argument("--pred-hidden", type=int, default=256)
    ap.add_argument("--log-every", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1337)
    a = ap.parse_args()
    cfg = vars(a).copy()
    cfg["corpus"] = a.corpus
    cfg["out_dir"] = a.out_dir
    cfg["lambda_vc"] = a.lambda_vc
    cfg["lambda_half"] = a.lambda_half
    cfg["gamma_text"] = a.gamma_text
    cfg["tau_var"] = a.tau_var
    cfg["cov_w"] = a.cov_w
    cfg["ema_m"] = a.ema_m
    cfg["pred_hidden"] = a.pred_hidden
    cfg["max_records"] = a.max_records
    run(cfg)


if __name__ == "__main__":
    main()
