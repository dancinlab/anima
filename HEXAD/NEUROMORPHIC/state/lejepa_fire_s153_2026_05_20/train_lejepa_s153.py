#!/usr/bin/env python3
"""§153 LEJEPA — anima byte-LM non-CE SSL with LeJEPA (arxiv 2511.08544).

WHY: §96-Q2 hypothesis ("`§11-B (CE load-bearing on GPU) is GPU tautology`")
needs a fourth distinct non-CE algorithmic data point. Prior three:

  §125 NONCE-FF   (Hinton goodness contrast, negative samples)
                  → S11B_LIKE_DEGENERATE
  §126 PCN-C4     (top-down prediction error, MSE on logits)
                  → PARTIAL_AMBIGUOUS
  §139 EqProp-C2  (2-phase free/nudge local update, MSE on logits)
                  → result.json byte_acc 0.1185 PARTIAL-class

§153 LeJEPA differs from all three:
  - vs §125: NO negative samples / NO goodness contrast.
  - vs §126: NO per-block top-down target / NO MSE-on-logits supervision.
  - vs §139: NO two-phase free/nudge / NO activation-difference local rule.

The LeJEPA objective:

    L_LeJEPA = (1 - lam) * L_pred  +  lam * L_SIGReg

where:
  - L_pred    = ||z_a - z_b||^2 with z_v = encoder(view_v), SYMMETRIC (both
                with grad — NO stop-gradient, NO teacher EMA, NO sharpening)
  - L_SIGReg  = (1/|A|) sum_a EP({a^T z_n}) is the Sketched Isotropic
                Gaussian Regularization (Balestriero+LeCun): |A| sphere
                directions a in S^(d-1) (resampled each step); EP is the
                Epps-Pulley characteristic-function test that the projected
                samples are standard-normal distributed
                  EP({s_n}) = N * integral |phi_hat_S(t) - phi_N(t)|^2
                              * w(t) dt
                with phi_hat_S(t) = (1/N) sum exp(i*t*s_n),
                     phi_N(t)     = exp(-t^2/2),
                     w(t)         = exp(-t^2/2).
                We discretize the integral as a finite sum over K=8 test
                frequencies t_k in linspace(0.5, 3.0, K).
  - lam = 0.05 (paper default — the single hyperparameter).

KEY INVARIANTS:
  - B-S153-1  SIGReg pressure-rejects exact collapse (CLOSED, design 9).
  - B-S153-2  Symmetric prediction = NO-STOP-GRAD (CLOSED, design 9).
  - B-S153-3  NO-CE invariant: F.cross_entropy / nn.CrossEntropyLoss /
              F.nll_loss / F.binary_cross_entropy / log_softmax.gather
              never appear in this source. (CLOSED, source-grep verifiable.)
  - B-S153-4  Sphere-direction sampling is anima-deterministic (CLOSED,
              torch.Generator with seed=1337+step).
  - B-S153-5  Epps-Pulley statistic non-negative (CLOSED, integral of
              non-negative * positive-weight).
  - B-S153-6  Single encoder (one ConsciousDecoderV2 instance, no
              teacher/student/EMA). (CLOSED, source.)
  - B-S153-7  Verdict bucket byte-equal to §125/§126/§139 (eval-side).
  - B-S153-8  Corpus byte-identical (dispatch-side sha ASSERT).

HONEST CARVE-OUT (B-S153-NOTE):
The L_LeJEPA objective trains the ENCODER (residual stream up to ln_f); it
does NOT train head_a / head_g (they have no gradient because L_pred and
L_SIGReg never touch them). At §96-Q2 eval, byte_acc is measured via the
UNTRAINED head_a (initialization-random linear projection). A low byte_acc
under §153 has TWO interpretations: (a) embedding is degenerate, or (b)
embedding carries signal but random head_a can't read it. See DESIGN.md
§6 C3 #3. Necessary-not-sufficient (B-EMERGE-7) carries.
"""
import os
import sys
import json
import math
import random
import argparse
import time

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


def load_corpus_bytes(path):
    out = bytearray()
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
            if isinstance(txt, str):
                out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str):
                        out.extend(t.encode("utf-8", errors="replace"))
    return bytes(out)


class LeJEPASampler:
    """Sample (ctx_a, ctx_b) — two overlapping byte-windows of the SAME
    starting record-region; offset delta in [16, 64] guarantees non-trivial
    view difference (>= 12.5% of block_size=128) yet same semantic anchor.
    """
    def __init__(self, corpus_bytes, block_size, seed=1337,
                 delta_min=16, delta_max=64):
        self.corpus = corpus_bytes
        self.T = block_size
        self.dmin = delta_min
        self.dmax = delta_max
        self.rng = random.Random(seed)

    def sample_batch(self, bsz, device):
        N = len(self.corpus)
        T = self.T
        ctxs_a, ctxs_b = [], []
        for _ in range(bsz):
            delta = self.rng.randint(self.dmin, self.dmax)
            s = self.rng.randint(0, N - T - delta - 1)
            ctxs_a.append(list(self.corpus[s : s + T]))
            ctxs_b.append(list(self.corpus[s + delta : s + delta + T]))
        x_a = torch.tensor(ctxs_a, dtype=torch.long, device=device)
        x_b = torch.tensor(ctxs_b, dtype=torch.long, device=device)
        return x_a, x_b


def encode_view(model, x):
    """Run ConsciousDecoderV2 forward up to ln_f, return final-position
    embedding z in R^(B x d_model). We do NOT touch head_a / head_g —
    they have no gradient in §153 (NO-CE structural invariant B-S153-3).
    """
    x = model.drop(model.tok_emb(x))
    for block in model.blocks:
        x, _t, _kv, _aux = block(
            x, consciousness_signal=None, consciousness_states=None,
            use_cache=False, past_kv=None, position_offset=0,
        )
    x = model.ln_f(x)
    z = x[:, -1, :]
    return z


# Epps-Pulley test frequencies (standard defaults, K=8).
EP_FREQS = torch.tensor([0.5, 0.857, 1.214, 1.571, 1.929, 2.286, 2.643, 3.0],
                        dtype=torch.float32)


def sigreg_loss(z, n_sketch, step_seed, device):
    """L_SIGReg over batch embeddings z in R^(B x d_emb).

    Algorithm:
      1. Sample |A|=n_sketch directions a in S^(d_emb - 1) uniformly
         (deterministic seed = step_seed, anima-substrate-controlled).
      2. Project: s = z @ A^T, standardize per direction.
      3. For each direction compute Epps-Pulley statistic
         EP = mean_k w_k * |phi_hat(t_k) - exp(-t_k^2/2)|^2
         with K=8 frequencies.
      4. Return L_SIGReg = (1/|A|) sum_a EP_a.
    """
    B, d_emb = z.shape
    g = torch.Generator(device=device)
    g.manual_seed(step_seed)
    A = torch.randn(n_sketch, d_emb, generator=g, device=device,
                    dtype=z.dtype)
    A = F.normalize(A, dim=-1)
    s = z @ A.t()                                            # (B, |A|)
    s_mean = s.mean(dim=0, keepdim=True)
    s_std = s.std(dim=0, keepdim=True).clamp(min=1e-6)
    s_norm = (s - s_mean) / s_std                            # (B, |A|)
    freqs = EP_FREQS.to(device=device, dtype=z.dtype)        # (K,)
    ts = freqs.view(1, 1, -1)
    # phi_hat(t) = (1/B) sum exp(i*t*s_n)
    phi_re = torch.cos(s_norm.unsqueeze(-1) * ts).mean(dim=0)  # (|A|, K)
    phi_im = torch.sin(s_norm.unsqueeze(-1) * ts).mean(dim=0)  # (|A|, K)
    phi_gauss_re = torch.exp(-0.5 * freqs * freqs)            # (K,)
    diff_re = phi_re - phi_gauss_re.unsqueeze(0)
    diff_im = phi_im
    sq = diff_re * diff_re + diff_im * diff_im                # (|A|, K)
    w = phi_gauss_re                                          # (K,)
    ep = (sq * w.unsqueeze(0)).mean(dim=-1)                   # (|A|,)
    return ep.mean()


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = ("cuda" if torch.cuda.is_available() and not cfg.get("cpu_only")
              else "cpu")
    print(f"[§153-LeJEPA] device={device} d_model={cfg['d_model']} "
          f"n_layer={cfg['n_layer']} steps={cfg['steps']}", flush=True)

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()

    # ONE optimizer over encoder params (head_a / head_g EXCLUDED).
    encoder_params = (
        list(model.tok_emb.parameters())
        + list(model.drop.parameters())
        + [p for b in model.blocks for p in b.parameters()]
        + list(model.ln_f.parameters())
    )
    opt = torch.optim.AdamW(
        encoder_params, lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=0.01,
    )

    corpus_bytes = load_corpus_bytes(cfg["corpus"])
    print(f"[§153-LeJEPA] corpus bytes: {len(corpus_bytes):,}", flush=True)
    sampler = LeJEPASampler(corpus_bytes, cfg["block_size"], seed=cfg["seed"])

    lam = cfg["lambda_sigreg"]
    n_sketch = cfg["n_sketch"]
    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = cfg["log_every"]

    for step in range(steps):
        x_a, x_b = sampler.sample_batch(cfg["bsz"], device)

        # BOTH views with grad — NO stop-gradient (B-S153-2).
        z_a = encode_view(model, x_a)
        z_b = encode_view(model, x_b)

        # L_pred — symmetric pairwise embedding match.
        L_pred = ((z_a - z_b) ** 2).sum(dim=-1).mean()

        # L_SIGReg — apply to BOTH views (concatenate, 2B samples).
        z_both = torch.cat([z_a, z_b], dim=0)
        step_seed = int(cfg["seed"] + step)
        L_sigreg = sigreg_loss(z_both, n_sketch=n_sketch,
                               step_seed=step_seed, device=device)

        # B-S153-5 sanity (EP >= 0 strict; allow small fp slack).
        assert L_sigreg.item() >= -1e-4, (
            f"B-S153-5 violated: L_SIGReg={L_sigreg.item()} < 0 sharply"
        )

        L_total = (1.0 - lam) * L_pred + lam * L_sigreg

        opt.zero_grad(set_to_none=True)
        L_total.backward()
        torch.nn.utils.clip_grad_norm_(encoder_params, max_norm=1.0)
        opt.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            elapsed = time.time() - t0
            with torch.no_grad():
                z_mean = z_both.mean(dim=0)
                z_std = z_both.std(dim=0)
                z_std_mean = float(z_std.mean())
                z_mean_norm = float(z_mean.norm())
            entry = dict(
                step=step + 1,
                L_total=float(L_total.detach()),
                L_pred=float(L_pred.detach()),
                L_sigreg=float(L_sigreg.detach()),
                z_std_mean=z_std_mean,
                z_mean_norm=z_mean_norm,
                elapsed_s=elapsed,
            )
            log.append(entry)
            print(f"[§153-LeJEPA] step={step+1:6d}  "
                  f"L_total={entry['L_total']:.6f}  "
                  f"L_pred={entry['L_pred']:.6f}  "
                  f"L_sigreg={entry['L_sigreg']:.6f}  "
                  f"z_std={z_std_mean:.4f}  z_mean_norm={z_mean_norm:.4f}  "
                  f"t={elapsed:.1f}s", flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_lejepa_s153.pt")
    torch.save({
        "model": model.state_dict(), "cfg": cfg, "log": log,
    }, ckpt_path)

    result = dict(
        battery="§153 LEJEPA (Balestriero+LeCun 2025) training",
        cfg=cfg, device=device,
        n_params=sum(p.numel() for p in model.parameters()),
        n_encoder_params_optimized=sum(p.numel() for p in encoder_params),
        train_wall_s=time.time() - t0,
        init_log=log[0] if log else None,
        final_log=log[-1] if log else None,
        n_encoder_optimizer=1,
        head_optimizer=False,
        algorithm=("LeJEPA (arxiv 2511.08544): JEPA + SIGReg, single encoder, "
                   "no stop-grad, no teacher, lambda=0.05, |A|=256, K=8"),
        non_ce_supervision=("symmetric pairwise embedding match + "
                            "characteristic-function isotropic-Gaussian "
                            "regularization (NO CE / NO NLL / NO MSE-on-logits)"),
        sibling_arc_s125_s126_s139=(
            "§125 S11B_LIKE_DEGENERATE / §126 PARTIAL_AMBIGUOUS / §139 "
            "PARTIAL_AMBIGUOUS-like. §153 fourth distinct non-CE algorithm."
        ),
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[§153-LeJEPA] DONE wall={result['train_wall_s']:.1f}s "
          f"ckpt={ckpt_path}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--lambda-sigreg", type=float, default=0.05,
                    help="paper default; single trade-off hyperparameter")
    ap.add_argument("--n-sketch", type=int, default=256,
                    help="|A| sphere directions per step (paper: 256-2048)")
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--cpu-only", action="store_true")
    args = ap.parse_args()
    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, seed=args.seed,
                   lambda_sigreg=args.lambda_sigreg,
                   n_sketch=args.n_sketch,
                   log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   cpu_only=args.cpu_only)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=8, steps=args.steps,
                   seed=args.seed, lambda_sigreg=args.lambda_sigreg,
                   n_sketch=64,
                   log_every=max(1, args.steps // 10),
                   corpus=args.corpus, out_dir=args.out_dir, cpu_only=True)
    run(cfg)


if __name__ == "__main__":
    main()
