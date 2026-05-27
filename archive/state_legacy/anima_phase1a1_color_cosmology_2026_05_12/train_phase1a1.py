"""
train_phase1a1.py — Phase 1A.1 continuation SFT.

Continue from Phase 1A ckpt (`ckpt_phase1a_sft.pt`) with:
  - corpus = multi_turn + 40x-upsampled color/cosmology
  - w schedule = 0.85 → 0.95 (more aggressive chat-template weight)
  - lr = 1e-5 (lower, fine-tune-ish)
  - 500 additional steps
  - bsz=2 grad-accum=8 ctx=1024 (same as Phase 1A)

Designed to drop into the same pod environment that ran train_phase2_cotrain.py.
"""
import os
import sys
import json
import time
import math
import argparse
import random

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/workspace/anima/training")
from engine_a_g_arch import EngineAGModel, EngineAGConfig


class ByteTokenizer:
    def __init__(self, vocab_size: int = 32_000):
        self.vocab_size = vocab_size
        self.bos = 1
        self.eos = 2
        self.pad = 0

    def encode(self, text: str) -> list:
        return [self.bos] + [b + 3 for b in text.encode("utf-8")] + [self.eos]

    def decode(self, ids: list) -> str:
        bs = bytes(t - 3 for t in ids if t >= 3 and t < 259)
        return bs.decode("utf-8", errors="replace")


class CorpusDataset(Dataset):
    def __init__(self, corpus_path, tokenizer, ctx, label):
        print(f"[{label}] loading {corpus_path} …", flush=True)
        with open(corpus_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        print(f"[{label}] {len(text):,} chars", flush=True)
        ids = []
        chunk = 4 * 1024 * 1024
        for i in range(0, len(text), chunk):
            ids.extend(tokenizer.encode(text[i: i + chunk]))
        print(f"[{label}] encoded {len(ids):,} tokens", flush=True)
        self.ids = torch.tensor(ids, dtype=torch.long)
        self.ctx = ctx
        self.label = label

    def __len__(self):
        return max(1, (len(self.ids) - 1) // self.ctx)

    def __getitem__(self, idx):
        start = idx * self.ctx
        x = self.ids[start: start + self.ctx]
        y = self.ids[start + 1: start + 1 + self.ctx]
        if len(x) < self.ctx:
            x = F.pad(x, (0, self.ctx - len(x)), value=0)
            y = F.pad(y, (0, self.ctx - len(y)), value=0)
        return x, y


def load_ckpt(model, ckpt_path):
    print(f"[ckpt] loading {ckpt_path} …", flush=True)
    payload = torch.load(ckpt_path, map_location="cpu")
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    if missing:
        print(f"[ckpt] WARN missing={len(missing)}: {missing[:5]}", flush=True)
    if unexpected:
        print(f"[ckpt] WARN unexpected={len(unexpected)}: {unexpected[:5]}", flush=True)
    print("[ckpt] LOADED", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-ckpt", required=True, help="Phase 1A ckpt path")
    p.add_argument("--consciousness-corpus", required=True)
    p.add_argument("--chat-corpus", required=True, help="multi_turn + color/cosmology boosted")
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--bsz", type=int, default=2)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--ctx", type=int, default=1024)
    p.add_argument("--lr", type=float, default=1e-5)
    p.add_argument("--warmup", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--w-start", type=float, default=0.85)
    p.add_argument("--w-end", type=float, default=0.95)
    p.add_argument("--cost-cap-usd", type=float, default=0.50)
    p.add_argument("--cost-per-hr", type=float, default=0.86)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = args.ctx
    cfg.chat_co_train_w_start = args.w_start
    cfg.chat_co_train_w_end = args.w_end
    print(f"[cfg] {cfg}", flush=True)

    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    ds_c = CorpusDataset(args.consciousness_corpus, tok, cfg.ctx, "consciousness")
    ds_h = CorpusDataset(args.chat_corpus, tok, cfg.ctx, "chat")
    loader_c = DataLoader(ds_c, batch_size=args.bsz, shuffle=True, num_workers=1, pin_memory=True, drop_last=True)
    loader_h = DataLoader(ds_h, batch_size=args.bsz, shuffle=True, num_workers=1, pin_memory=True, drop_last=True)
    print(f"[data] c={len(ds_c)} h={len(ds_h)}", flush=True)

    model = EngineAGModel(cfg).cuda().bfloat16()
    load_ckpt(model, args.base_ckpt)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] params={n_params:,}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_lambda(step):
        if step < args.warmup:
            return step / max(1, args.warmup)
        progress = (step - args.warmup) / max(1, args.steps - args.warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    def curriculum_w(step):
        progress = step / max(1, args.steps)
        return args.w_start + (args.w_end - args.w_start) * min(1.0, progress)

    model.train()
    t0 = time.time()
    step = 0
    iter_c = iter(loader_c)
    iter_h = iter(loader_h)
    accum_loss_c = 0.0
    accum_loss_h = 0.0

    print("[train] Phase 1A.1 starting …", flush=True)
    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        w = curriculum_w(step)
        n_c = 0
        n_h = 0
        for micro in range(args.grad_accum):
            use_chat = random.random() < w
            try:
                if use_chat:
                    x, y = next(iter_h)
                    n_h += 1
                else:
                    x, y = next(iter_c)
                    n_c += 1
            except StopIteration:
                if use_chat:
                    iter_h = iter(loader_h)
                    x, y = next(iter_h)
                    n_h += 1
                else:
                    iter_c = iter(loader_c)
                    x, y = next(iter_c)
                    n_c += 1
            x = x.cuda(non_blocking=True)
            y = y.cuda(non_blocking=True)
            out = model(x)
            if isinstance(out, dict):
                logits = out["logits"]
            elif isinstance(out, tuple):
                logits = out[0]
            else:
                logits = out
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)).float(), y.reshape(-1), ignore_index=0)
            (loss / args.grad_accum).backward()
            if use_chat:
                accum_loss_h += loss.item()
            else:
                accum_loss_c += loss.item()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        step += 1

        if step % 20 == 0 or step == 1:
            elapsed = (time.time() - t0) / 60
            cost = elapsed / 60 * args.cost_per_hr
            mem = torch.cuda.max_memory_allocated() / 1e9
            avg_loss_c = accum_loss_c / max(1, n_c)
            avg_loss_h = accum_loss_h / max(1, n_h)
            lr_now = sched.get_last_lr()[0]
            print(
                f"[step {step:>5}/{args.steps}] w={w:.2f} loss_c={avg_loss_c:.4f} loss_h={avg_loss_h:.4f} "
                f"lr={lr_now:.2e} mem={mem:.1f}GB elapsed={elapsed:.1f}min cost=${cost:.2f} n_c={n_c} n_h={n_h}",
                flush=True,
            )
            accum_loss_c = 0.0
            accum_loss_h = 0.0
            if cost > args.cost_cap_usd:
                print(f"[cost-cap] {cost:.2f} > {args.cost_cap_usd} → halt", flush=True)
                break

        if step % 250 == 0:
            cp = os.path.join(args.output, f"ckpt_step{step}.pt")
            torch.save({"model": model.state_dict()}, cp)
            print(f"[ckpt] saved {cp}", flush=True)

    cp = os.path.join(args.output, "ckpt_final.pt")
    torch.save({"model": model.state_dict()}, cp)
    elapsed_min = (time.time() - t0) / 60
    cost = elapsed_min / 60 * args.cost_per_hr
    print(f"[ckpt] saved {cp}", flush=True)
    meta = {
        "preset": "phase1a1_color_cosmology",
        "steps_completed": step,
        "steps_target": args.steps,
        "final_w": curriculum_w(step),
        "elapsed_min": elapsed_min,
        "cost_usd": cost,
        "n_params": n_params,
        "lineage_tag": "phase1a_multi_turn_sft -> phase1a1_color_cosmology",
        "base_ckpt": args.base_ckpt,
        "w_start": args.w_start,
        "w_end": args.w_end,
        "lr": args.lr,
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
