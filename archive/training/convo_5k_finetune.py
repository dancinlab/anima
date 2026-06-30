#!/usr/bin/env python3
"""convo_5k.pt 추가 fine-tuning — chat-cap 회복 시도.

원본: conscious-lm/convo-ft/convo_5k.pt (R2, 18.523M, step=45000, 2026-03-28)
목표: ConsciousLMReconstructed (byte-level, dual engine_a/g + dual head_a/g)
       위에 5K-20K step 추가 FT, KO+EN persona dialogue corpus 로 chat-cap 회복.

Architecture (verified strict 108/108 PASS):
  vocab=256 (byte-level), block_size=256, d_model=384, n_head=4, n_layer=6
  ffn = engine_a (-) engine_g, head_a + head_g dual output
  total params: 18,523,392

Loss: 0.5 * CE(head_a, next_byte) + 0.5 * CE(head_g, next_byte)

Usage (local dry-run):
  /Users/ghost/.hx/bin/python3 training/convo_5k_finetune.py \\
      --dry-run --steps 10 --batch 4 --seq 64

Usage (H100 production — DO NOT FIRE without verbatim user keyword):
  python training/convo_5k_finetune.py \\
      --ckpt /workspace/convo_5k.pt \\
      --corpus /workspace/dialogue_corpus.txt \\
      --steps 10000 --batch 32 --seq 256 \\
      --lr 1e-5 --warmup 500 \\
      --out /workspace/convo_5k_ft_step{N}.pt

raw#15 additive — original convo_5k.pt 미수정. 새 ckpt out 으로 save.
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

# Reuse arch from forward_smoke.py
SMOKE_DIR = Path(__file__).resolve().parent.parent / "state" / "anima_clm_v2_mitosis_cells_recovery_2026_05_09"
if str(SMOKE_DIR) not in sys.path:
    sys.path.insert(0, str(SMOKE_DIR))
from forward_smoke import ConsciousLMReconstructed  # noqa: E402


# ----- corpus / dataset -----

class ByteSlidingDataset(Dataset):
    """Sliding-window byte-level dataset over a single concatenated corpus.

    Each sample: (input_ids[seq_len], target_ids[seq_len]) where target = shifted-by-1.
    """

    def __init__(self, corpus_bytes: bytes, seq_len: int, stride: int | None = None):
        self.data = corpus_bytes
        self.seq_len = seq_len
        self.stride = stride or seq_len  # non-overlapping by default
        # Number of windows
        self.n = max(0, (len(self.data) - seq_len - 1) // self.stride)

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        start = idx * self.stride
        chunk = self.data[start : start + self.seq_len + 1]
        x = torch.tensor(list(chunk[:-1]), dtype=torch.long)
        y = torch.tensor(list(chunk[1:]), dtype=torch.long)
        return x, y


def load_corpus(path: str | Path, max_bytes: int | None = None) -> bytes:
    p = Path(path)
    with p.open("rb") as f:
        data = f.read()
    if max_bytes is not None:
        data = data[:max_bytes]
    return data


# ----- training loop -----

def cosine_lr(step: int, warmup: int, total: int, lr_max: float, lr_min: float) -> float:
    if step < warmup:
        return lr_max * (step + 1) / max(1, warmup)
    pct = (step - warmup) / max(1, total - warmup)
    pct = min(1.0, max(0.0, pct))
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * pct))


def compute_loss(model, x, y, dual_weight=(0.5, 0.5)):
    la, lg, _tensions = model(x)
    # CE on each head; predict next byte from logit at position t given x[:t+1]
    # Note: our forward emits logits at every position; we use the full sequence.
    B, T, V = la.shape
    loss_a = F.cross_entropy(la.reshape(-1, V), y.reshape(-1))
    loss_g = F.cross_entropy(lg.reshape(-1, V), y.reshape(-1))
    wa, wg = dual_weight
    return wa * loss_a + wg * loss_g, loss_a.detach(), loss_g.detach()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default="/Users/ghost/.cache/huggingface/hub/models--dancinlab--clm-v2-byte-18m-convo-5k/snapshots/1af2bcaeaf70c1d0b1a19939a8ada79a28f8cd30/convo_5k.pt")
    p.add_argument("--corpus", default="/Users/ghost/core/anima/state/anima_dialogue_tier_a_iter2_2026_05_08.txt")
    p.add_argument("--out", default="/Users/ghost/core/anima/state/anima_convo_5k_ft_design_2026_05_10/dry_run_step_final.pt")
    p.add_argument("--log", default="/Users/ghost/core/anima/state/anima_convo_5k_ft_design_2026_05_10/dry_run.log")
    p.add_argument("--steps", type=int, default=10)
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--seq", type=int, default=64)
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--lr-min", type=float, default=1e-6)
    p.add_argument("--warmup", type=int, default=2)
    p.add_argument("--corpus-max-bytes", type=int, default=512 * 1024)  # 512KB for dry-run
    p.add_argument("--device", default="cpu")
    p.add_argument("--dry-run", action="store_true",
                   help="local Mac CPU smoke; tiny config + log writes only.")
    p.add_argument("--save-every", type=int, default=0,
                   help="save ckpt every N steps; 0=only at end.")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    torch.manual_seed(args.seed)

    Path(args.log).parent.mkdir(parents=True, exist_ok=True)

    log_lines = []

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line)
        log_lines.append(line)

    log(f"convo_5k_finetune start  device={args.device}  dry_run={args.dry_run}")
    log(f"args: {vars(args)}")

    # 1) Load ckpt + arch
    t0 = time.time()
    ckpt = torch.load(args.ckpt, map_location=args.device, weights_only=False)
    sd = ckpt.get("model_state", ckpt)
    base_step = ckpt.get("step", 0)
    log(f"ckpt loaded: keys={len(sd)} base_step={base_step} ({time.time()-t0:.2f}s)")

    model = ConsciousLMReconstructed(
        vocab_size=256, d_model=384, n_head=4,
        n_layer=6, block_size=256, dropout=0.0,
    ).to(args.device)
    miss, unexp = model.load_state_dict(sd, strict=False)
    log(f"load_state_dict: missing={len(miss)} unexpected={len(unexp)}")
    assert len(miss) == 0 and len(unexp) == 0, f"strict load failed: miss={miss} unexp={unexp}"

    n_params = sum(p.numel() for p in model.parameters())
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log(f"params: total={n_params:,} trainable={n_trainable:,}")
    assert n_trainable == n_params, "expected all params trainable for full FT"

    # 2) Corpus
    t0 = time.time()
    corpus_bytes = load_corpus(args.corpus, max_bytes=args.corpus_max_bytes if args.dry_run else None)
    log(f"corpus loaded: {len(corpus_bytes):,} bytes ({time.time()-t0:.2f}s)")
    ds = ByteSlidingDataset(corpus_bytes, seq_len=args.seq, stride=args.seq)
    dl = DataLoader(ds, batch_size=args.batch, shuffle=True, num_workers=0, drop_last=True)
    log(f"dataset: n_windows={len(ds)} batches_per_epoch={len(dl)}")

    # 3) Optimizer
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
            x = x.to(args.device)
            y = y.to(args.device)

            lr = cosine_lr(step, args.warmup, args.steps, args.lr, args.lr_min)
            for pg in optim.param_groups:
                pg["lr"] = lr

            optim.zero_grad(set_to_none=True)
            loss, la_, lg_ = compute_loss(model, x, y)
            loss.backward()

            # Grad norm sanity
            total_norm = 0.0
            for prm in model.parameters():
                if prm.grad is not None:
                    total_norm += prm.grad.detach().pow(2).sum().item()
            total_norm = math.sqrt(total_norm)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            optim.step()

            losses.append(loss.item())
            grad_norms.append(total_norm)
            log(f"step {step:5d}  loss={loss.item():.4f}  loss_a={la_.item():.4f}  loss_g={lg_.item():.4f}  "
                f"lr={lr:.2e}  grad_norm={total_norm:.3f}")

            step += 1
            if args.save_every and step % args.save_every == 0:
                save_path = args.out.replace("final", f"step_{step}")
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
        "dry_run": args.dry_run,
        "steps_done": step,
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
        "params_trainable": n_trainable,
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
    summary_path = args.log.replace(".log", "_summary.json")
    Path(summary_path).write_text(json.dumps(summary, indent=2))
    log(f"summary: {summary_path}")
    print("\n--- SUMMARY ---")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
