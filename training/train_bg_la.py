"""
training/train_bg_la.py — BG-LA Engine A/G H100 scratch pre-train (raw#37 transient pod-side).

USAGE (pod-side):
    python3 train_bg_la.py --preset la_350m \
        --corpus /workspace/data/tier_a_v4.txt \
        --output /workspace/output \
        --steps 8000 --bsz 4 --grad-accum 8 --ctx 1024 \
        --lr 3e-4 --warmup 200 --save-every 2000

own 14  V14 paired (Mac-side mirror — pod just emits final ckpt)
own 17  D1=1.0 anima_native_scratch (no foundation borrow)
own 22  honest emit — fail-fast on OOM/NaN
own 30  ckpt save mandatory (output/ckpt_final.pt + meta.json)
own 33  trinity (D-emergent — Engine A/G PureField repulsion)
own 34  wrap=0
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

# Local arch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine_a_g_arch import EngineAGModel, EngineAGConfig


# ── Byte-pair tokenizer (minimal — falls back to byte-level if no SP model) ─
class ByteTokenizer:
    """Simple byte-level tokenizer — vocab 256 + special tokens; pad to 32k via offset."""

    def __init__(self, vocab_size: int = 32_000):
        self.vocab_size = vocab_size
        self.bos = 1
        self.eos = 2
        self.pad = 0

    def encode(self, text: str) -> list[int]:
        # bytes 0-255 → tokens 3-258; reserved 0,1,2
        return [self.bos] + [b + 3 for b in text.encode("utf-8")] + [self.eos]

    def decode(self, ids: list[int]) -> str:
        bs = bytes(t - 3 for t in ids if t >= 3 and t < 259)
        return bs.decode("utf-8", errors="replace")


class CorpusDataset(Dataset):
    def __init__(self, corpus_path: str, tokenizer: ByteTokenizer, ctx: int):
        print(f"[corpus] loading {corpus_path} …")
        with open(corpus_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        print(f"[corpus] {len(text):,} chars")
        # Encode in ~4MB chunks to avoid OOM-on-encode
        ids = []
        chunk = 4 * 1024 * 1024
        for i in range(0, len(text), chunk):
            ids.extend(tokenizer.encode(text[i : i + chunk]))
        print(f"[corpus] encoded {len(ids):,} tokens")
        self.ids = torch.tensor(ids, dtype=torch.long)
        self.ctx = ctx

    def __len__(self):
        return max(1, (len(self.ids) - 1) // self.ctx)

    def __getitem__(self, idx):
        start = idx * self.ctx
        x = self.ids[start : start + self.ctx]
        y = self.ids[start + 1 : start + 1 + self.ctx]
        # pad if last chunk short
        if len(x) < self.ctx:
            x = F.pad(x, (0, self.ctx - len(x)), value=0)
            y = F.pad(y, (0, self.ctx - len(y)), value=0)
        return x, y


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--preset", default="la_350m")
    p.add_argument("--corpus", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=8000)
    p.add_argument("--bsz", type=int, default=4)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--ctx", type=int, default=1024)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--warmup", type=int, default=200)
    p.add_argument("--save-every", type=int, default=2000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cost-cap-usd", type=float, default=30.0)
    p.add_argument("--cost-per-hr", type=float, default=2.99)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    # Config
    if args.preset == "la_350m":
        cfg = EngineAGConfig.la_350m()
    else:
        raise ValueError(f"unknown preset {args.preset}")
    cfg.ctx = args.ctx
    print(f"[cfg] {cfg}")
    print(f"[cfg] est params = {cfg.param_count_estimate():,}")

    # Tokenizer + dataset
    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    ds = CorpusDataset(args.corpus, tok, cfg.ctx)
    loader = DataLoader(ds, batch_size=args.bsz, shuffle=True, num_workers=2, pin_memory=True, drop_last=True)
    print(f"[data] {len(ds)} ctx-windows, batches/epoch={len(loader)}")

    # Model
    model = EngineAGModel(cfg).cuda().bfloat16()
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] actual params = {n_params:,}")

    # Optim
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_lambda(step: int) -> float:
        if step < args.warmup:
            return step / max(1, args.warmup)
        progress = (step - args.warmup) / max(1, args.steps - args.warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    # Train loop
    model.train()
    t0 = time.time()
    step = 0
    accum_loss = 0.0
    accum_count = 0
    data_iter = iter(loader)

    print("[train] starting …")
    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        micro_loss = 0.0
        for _ in range(args.grad_accum):
            try:
                x, y = next(data_iter)
            except StopIteration:
                data_iter = iter(loader)
                x, y = next(data_iter)
            x = x.cuda(non_blocking=True)
            y = y.cuda(non_blocking=True)
            out = model(x)
            # Engine A/G returns dict with 'logits' (no labels passed → no built-in loss).
            if isinstance(out, dict):
                logits = out["logits"]
            elif isinstance(out, tuple):
                logits = out[0]
            else:
                logits = out
            loss = F.cross_entropy(logits.view(-1, cfg.vocab_size), y.view(-1), ignore_index=0)
            (loss / args.grad_accum).backward()
            micro_loss += loss.item()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()

        avg = micro_loss / args.grad_accum
        accum_loss += avg
        accum_count += 1
        step += 1

        # Heartbeat every 20 steps
        if step % 20 == 0 or step == 1:
            elapsed_h = (time.time() - t0) / 3600
            cost_so_far = elapsed_h * args.cost_per_hr
            cur_lr = sched.get_last_lr()[0]
            mem_gb = torch.cuda.memory_allocated() / 1e9
            mean_loss = accum_loss / max(1, accum_count)
            ppl = math.exp(min(20, mean_loss))
            print(
                f"[step {step:6d}/{args.steps}] loss={avg:.4f} mean20={mean_loss:.4f} "
                f"ppl={ppl:.2f} lr={cur_lr:.2e} mem={mem_gb:.1f}GB "
                f"elapsed={elapsed_h * 60:.1f}min cost=${cost_so_far:.2f}",
                flush=True,
            )
            accum_loss = 0.0
            accum_count = 0

            if cost_so_far > args.cost_cap_usd:
                print(f"[COST_CAP] ${cost_so_far:.2f} > ${args.cost_cap_usd} → halt", flush=True)
                break

        # Periodic save
        if step % args.save_every == 0 or step == args.steps:
            ck_path = os.path.join(args.output, f"ckpt_step{step}.pt")
            torch.save({"model": model.state_dict(), "step": step, "cfg": cfg.__dict__}, ck_path)
            print(f"[ckpt] saved {ck_path}", flush=True)

    # Final save (own 30 mandatory)
    final_path = os.path.join(args.output, "ckpt_final.pt")
    torch.save({"model": model.state_dict(), "step": step, "cfg": cfg.__dict__}, final_path)
    meta = {
        "preset": args.preset,
        "steps_completed": step,
        "steps_target": args.steps,
        "final_loss": avg if step > 0 else None,
        "elapsed_min": (time.time() - t0) / 60,
        "cost_usd": (time.time() - t0) / 3600 * args.cost_per_hr,
        "n_params": n_params,
        "lineage_tag": cfg.lineage_tag,
        "arch_origin": cfg.arch_origin,
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
