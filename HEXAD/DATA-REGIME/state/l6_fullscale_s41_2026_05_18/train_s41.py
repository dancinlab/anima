#!/usr/bin/env python3
"""RESEARCH.md §41 — L6 fullscale trainer: ConsciousDecoderV2 byte-LM on
the §41 <relate> relation corpus.

Substrate: §16-size byte-LM, from-scratch (g_clm_from_scratch
base_ckpt=NONE seed-fixed 1337). Default config d=768 / n_layer=12 /
283.72 M params (the §16 footprint) — same model class the entire
13-way arc used. Pure CE next-byte loss (B-S41-NOTE: no Dir-I lever,
no §16 curriculum, no §22 trie — the question is solely 'does the
SAME held-out-pair generalization §37 demonstrated at 3.7 k params
SURVIVE at 283.72 M params on the SAME byte-text task').

Why default 3000 steps (cost / honesty):
  §16 fire = 8000 steps on 603 MB / 777 k records (~$0.5-0.8 A100,
  wall 30 min). §41 corpus = 22.8 MB / 103 k records (~6 epochs at
  batch 32 / 3000 steps). 3000 steps for a 75 000× larger model on
  100× more relation records is sufficient for any held-out signal
  to emerge or fail to emerge; CE descent on §16 saturated < 5000
  steps (final CE 0.004 dropped from 5.64 init in first ~2000), so
  3000 steps is honest scope ($0.20-0.40 A100, ~10-15 min wall).

g3 honest scope:
  - this trainer measures whether L6_RELATIONS_GENERALIZE survives
    the scale transition. It does NOT add new GOAL machinery.
  - if held-out-pair acc on byte-LM ~ §37 0.9938 → relations generalize
    is a TASK PROPERTY (the relation function is genuinely learnable
    at any scale). If held-out-pair acc collapses → SMALL-MODEL GIFT
    (tiny RelationMLP could not memorize so was forced to generalize;
    big byte-LM prefers memorization, §16.6-C / B-D-NOTE).
  - either verdict is valuable: §37 generalize at 3.7 k params is a
    measured fact, the question §41 answers is what it SCALES INTO.
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# Re-use the §16 ConsciousDecoderV2 verbatim — same model class the
# entire arc uses (anima-self lever, not external substrate).
sys.path.insert(0, str(HERE.parent / "carving_dataregime_s16_2026_05_18"))
from conscious_decoder import ConsciousDecoderV2  # noqa: E402


def load_corpus(path: Path) -> bytes:
    """Read the <relate> corpus as a single byte-stream (next-byte CE)."""
    with open(path, "rb") as f:
        return f.read()


def get_batch(corpus: bytes, block_size: int, batch_size: int,
              rng: torch.Generator, device: str) -> tuple:
    n = len(corpus)
    idx = torch.randint(0, n - block_size - 1, (batch_size,),
                        generator=rng).tolist()
    x = torch.tensor(
        [list(corpus[k:k + block_size]) for k in idx],
        dtype=torch.long, device=device)
    y = torch.tensor(
        [list(corpus[k + 1:k + block_size + 1]) for k in idx],
        dtype=torch.long, device=device)
    return x, y


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(HERE / "relation_corpus_train_s41.jsonl"))
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--block-size", type=int, default=512)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--out", default=str(HERE / "ckpt_s41.pt"))
    ap.add_argument("--result", default=str(HERE / "result.json"))
    ap.add_argument("--log-every", type=int, default=50)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float32 if device == "cpu" else torch.float32

    corpus = load_corpus(Path(args.corpus))
    corpus_sha = hashlib.sha256(corpus).hexdigest()
    print(f"[§41] corpus bytes={len(corpus):,} sha256={corpus_sha[:16]}…")

    # from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE)
    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=args.d_model,
        n_head=args.n_head,
        n_kv_head=args.n_kv_head,
        n_layer=args.n_layer,
        block_size=args.block_size,
        dropout=0.1,
    ).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[§41] model params={n_params:,} ({n_params/1e6:.2f} M) "
          f"device={device}")

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr,
                            betas=(0.9, 0.95), weight_decay=0.1)

    # cosine schedule (mirror §16 / Dir-I; warmup 100 steps)
    def lr_at(step: int) -> float:
        if step < 100:
            return args.lr * step / 100
        prog = (step - 100) / max(1, args.steps - 100)
        return args.lr * 0.5 * (1 + math.cos(math.pi * prog))

    rng = torch.Generator(device="cpu").manual_seed(args.seed)
    t_start = time.time()
    train_log = []
    init_ce_value = None
    final_ce_value = None
    for step in range(args.steps):
        for pg in opt.param_groups:
            pg["lr"] = lr_at(step)

        x, y = get_batch(corpus, args.block_size, args.batch_size, rng, device)
        # ConsciousDecoderV2 returns (logits_a, logits_g, tensions, kv, aux)
        logits_a, _, _, _, _ = model(x)
        loss = F.cross_entropy(logits_a.reshape(-1, 256), y.reshape(-1))

        if step == 0:
            init_ce_value = float(loss)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % args.log_every == 0 or step == args.steps - 1:
            ce = float(loss)
            elapsed = time.time() - t_start
            print(f"[§41] step={step:5d}  ce={ce:.4f}  "
                  f"lr={lr_at(step):.5g}  wall={elapsed:.1f}s")
            train_log.append({"step": step, "ce": ce,
                              "lr": lr_at(step), "wall_s": elapsed})
            final_ce_value = ce

    wall = time.time() - t_start

    # save ckpt
    torch.save({
        "model": model.state_dict(),
        "config": {
            "vocab_size": 256, "d_model": args.d_model,
            "n_head": args.n_head, "n_kv_head": args.n_kv_head,
            "n_layer": args.n_layer, "block_size": args.block_size,
            "dropout": 0.1,
        },
        "n_params": n_params,
        "step": args.steps - 1,
        "init_ce": init_ce_value,
        "final_ce": final_ce_value,
        "wall_s": wall,
        "seed": args.seed,
        "corpus_sha256": corpus_sha,
    }, args.out)
    ckpt_sha = hashlib.sha256(Path(args.out).read_bytes()).hexdigest()
    print(f"[§41] ckpt saved {args.out}  sha256={ckpt_sha[:16]}…  "
          f"size={Path(args.out).stat().st_size:,} B")

    # write a partial result.json (eval fills final fields)
    result = {
        "research_section": "§41",
        "title": "L6 anchor-interaction full-scale fire — relations generalize at §16-scale byte-LM?",
        "config": vars(args),
        "n_params": n_params,
        "corpus_sha256": corpus_sha,
        "corpus_bytes": len(corpus),
        "device": device,
        "init_ce": init_ce_value,
        "final_ce": final_ce_value,
        "wall_s": wall,
        "ckpt_sha256": ckpt_sha,
        "ckpt_size_bytes": Path(args.out).stat().st_size,
        "train_log": train_log,
        "phase": "train_complete_pending_eval",
    }
    Path(args.result).write_text(json.dumps(result, indent=2,
                                            ensure_ascii=False))
    print(f"[§41] partial result.json written; eval step next")
    return 0


if __name__ == "__main__":
    sys.exit(main())
