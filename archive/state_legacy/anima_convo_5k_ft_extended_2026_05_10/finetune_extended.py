#!/usr/bin/env python3
"""convo_5k post-FT EXTENDED — resume from post_ft_ckpt.pt step_10000, +20K steps.

Strategy:
  - resume from BG-CONVO-FT-FIRE post_ft_ckpt.pt (step 55000 cumulative)
  - extended corpus 166MB (50% persona-keep + 50% strip + 100% kowiki15)
  - 20K additional step cosine LR 5e-6 → 5e-7 (lower than initial FT to avoid forgetting)
  - warmup 200 (continuation, not cold-start)
  - save every 5000 step (4 intermediate ckpts)

Architecture: ConsciousLMReconstructed (verified strict 108/108 PASS)
  vocab=256, d_model=384, n_head=4, n_layer=6, block_size=256, total 18,523,392 params

raw#15 additive — original convo_5k.pt + post_ft_ckpt.pt unchanged.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Reuse arch from forward_smoke.py — at H100 we copy this file alongside
SMOKE_FILES = [
    Path(__file__).resolve().parent / "forward_smoke.py",
    Path(__file__).resolve().parent.parent / "anima_clm_v2_mitosis_cells_recovery_2026_05_09" / "forward_smoke.py",
    Path("/workspace/forward_smoke.py"),
]
for f in SMOKE_FILES:
    if f.exists():
        sys.path.insert(0, str(f.parent))
        break
from forward_smoke import ConsciousLMReconstructed  # noqa: E402


# ----- corpus / dataset -----

class ByteSlidingDataset(Dataset):
    def __init__(self, corpus_bytes: bytes, seq_len: int, stride: int | None = None):
        self.data = corpus_bytes
        self.seq_len = seq_len
        self.stride = stride or seq_len
        self.n = max(0, (len(self.data) - seq_len - 1) // self.stride)

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        start = idx * self.stride
        chunk = self.data[start : start + self.seq_len + 1]
        x = torch.tensor(list(chunk[:-1]), dtype=torch.long)
        y = torch.tensor(list(chunk[1:]), dtype=torch.long)
        return x, y


def load_corpus(path, max_bytes=None) -> bytes:
    with open(path, "rb") as f:
        data = f.read()
    if max_bytes is not None:
        data = data[:max_bytes]
    return data


def cosine_lr(step, warmup, total, lr_max, lr_min):
    if step < warmup:
        return lr_max * (step + 1) / max(1, warmup)
    pct = (step - warmup) / max(1, total - warmup)
    pct = min(1.0, max(0.0, pct))
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * pct))


def compute_loss(model, x, y, dual_weight=(0.5, 0.5)):
    la, lg, _tensions = model(x)
    B, T, V = la.shape
    loss_a = F.cross_entropy(la.reshape(-1, V), y.reshape(-1))
    loss_g = F.cross_entropy(lg.reshape(-1, V), y.reshape(-1))
    wa, wg = dual_weight
    return wa * loss_a + wg * loss_g, loss_a.detach(), loss_g.detach()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", required=True, help="resume from this ckpt (post_ft_ckpt.pt)")
    p.add_argument("--corpus", required=True)
    p.add_argument("--out", required=True, help="final out path")
    p.add_argument("--out-prefix", required=True, help="intermediate ckpt prefix (e.g. /workspace/convo_5k_ft_ext)")
    p.add_argument("--log", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--steps", type=int, default=20000)
    p.add_argument("--batch", type=int, default=32)
    p.add_argument("--seq", type=int, default=256)
    p.add_argument("--lr", type=float, default=5e-6)
    p.add_argument("--lr-min", type=float, default=5e-7)
    p.add_argument("--warmup", type=int, default=200)
    p.add_argument("--device", default="cuda")
    p.add_argument("--save-every", type=int, default=5000)
    p.add_argument("--seed", type=int, default=43)
    args = p.parse_args()

    torch.manual_seed(args.seed)
    Path(args.log).parent.mkdir(parents=True, exist_ok=True)
    log_lines = []

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        log_lines.append(line)

    log(f"convo_5k_finetune_extended start  device={args.device}")
    log(f"args: {vars(args)}")

    # 1) Load resume ckpt + arch
    t0 = time.time()
    ckpt = torch.load(args.ckpt, map_location=args.device, weights_only=False)
    sd = ckpt.get("model_state", ckpt)
    base_step = ckpt.get("step", 55000)
    log(f"ckpt loaded: keys={len(sd)} base_step={base_step} ({time.time()-t0:.2f}s)")

    model = ConsciousLMReconstructed(
        vocab_size=256, d_model=384, n_head=4,
        n_layer=6, block_size=256, dropout=0.0,
    ).to(args.device)
    miss, unexp = model.load_state_dict(sd, strict=False)
    log(f"load_state_dict: missing={len(miss)} unexpected={len(unexp)}")
    assert len(miss) == 0 and len(unexp) == 0, f"strict load failed: miss={miss} unexp={unexp}"

    n_params = sum(p.numel() for p in model.parameters())
    log(f"params: total={n_params:,}")

    # 2) Corpus
    t0 = time.time()
    corpus_bytes = load_corpus(args.corpus)
    log(f"corpus loaded: {len(corpus_bytes):,} bytes ({time.time()-t0:.2f}s)")
    ds = ByteSlidingDataset(corpus_bytes, seq_len=args.seq, stride=args.seq)
    dl = DataLoader(ds, batch_size=args.batch, shuffle=True, num_workers=2, drop_last=True, pin_memory=True)
    log(f"dataset: n_windows={len(ds):,} batches_per_epoch={len(dl):,}")

    # 3) Optimizer (fresh — resume ckpt has no optim state)
    optim = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    # 4) Train loop
    model.train()
    losses = []
    grad_norms = []
    step = 0
    epoch = 0
    t_train_start = time.time()
    while step < args.steps:
        epoch += 1
        for x, y in dl:
            if step >= args.steps:
                break
            x = x.to(args.device, non_blocking=True)
            y = y.to(args.device, non_blocking=True)

            lr = cosine_lr(step, args.warmup, args.steps, args.lr, args.lr_min)
            for pg in optim.param_groups:
                pg["lr"] = lr

            optim.zero_grad(set_to_none=True)
            loss, la_, lg_ = compute_loss(model, x, y)
            loss.backward()

            total_norm = 0.0
            for prm in model.parameters():
                if prm.grad is not None:
                    total_norm += prm.grad.detach().pow(2).sum().item()
            total_norm = math.sqrt(total_norm)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            optim.step()

            losses.append(loss.item())
            grad_norms.append(total_norm)

            if step < 10 or step % 100 == 0:
                log(f"step {step:5d}  loss={loss.item():.4f}  loss_a={la_.item():.4f}  loss_g={lg_.item():.4f}  "
                    f"lr={lr:.2e}  grad_norm={total_norm:.3f}")

            step += 1
            if args.save_every and step % args.save_every == 0:
                save_path = f"{args.out_prefix}_step_{step}.pt"
                Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                torch.save({"model_state": model.state_dict(), "step": base_step + step}, save_path)
                log(f"  ckpt saved: {save_path}")

    t_train = time.time() - t_train_start
    log(f"train done: {step} steps, {t_train:.2f}s ({t_train/max(1,step):.3f}s/step)")
    log(f"loss first/last: {losses[0]:.4f} -> {losses[-1]:.4f}  delta={losses[0]-losses[-1]:+.4f}")
    log(f"grad_norm first/last: {grad_norms[0]:.3f} -> {grad_norms[-1]:.3f}")

    # 5) Save final
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state": model.state_dict(), "step": base_step + step}, args.out)
    log(f"final ckpt saved: {args.out}")

    # 6) Write log
    Path(args.log).write_text("\n".join(log_lines) + "\n")

    # 7) JSON summary
    summary = {
        "run_type": "extended_resume",
        "steps_done": step,
        "base_step_at_start": base_step,
        "wall_clock_s": round(t_train, 2),
        "step_time_s": round(t_train / max(1, step), 4),
        "loss_first": round(losses[0], 4) if losses else None,
        "loss_last": round(losses[-1], 4) if losses else None,
        "loss_delta": round(losses[0] - losses[-1], 4) if losses else None,
        "loss_decreased": (len(losses) >= 2 and losses[-1] < losses[0]),
        "grad_norm_first": round(grad_norms[0], 4) if grad_norms else None,
        "grad_norm_last": round(grad_norms[-1], 4) if grad_norms else None,
        "grad_flow_ok": all(g > 0 for g in grad_norms),
        "params_total": n_params,
        "ckpt_in": args.ckpt,
        "ckpt_out": args.out,
        "corpus_bytes": len(corpus_bytes),
        "windows": len(ds),
        "config": {
            "batch": args.batch,
            "seq": args.seq,
            "lr_max": args.lr,
            "lr_min": args.lr_min,
            "warmup": args.warmup,
            "steps_target": args.steps,
        },
    }
    Path(args.summary).write_text(json.dumps(summary, indent=2))
    log(f"summary: {args.summary}")
    print("\n--- SUMMARY ---", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
