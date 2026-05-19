"""
train_phase1a3.py — Phase 1A.3 loss-masking SFT (response tokens only).

Continuation from Phase 1A.1 ckpt. Same corpus as Phase 1A.2 (anima_fact 2700
dialogue augment), same lr (2e-6, matching Phase 1A.1), same 200 steps —
but **cross-entropy loss is masked to anima response tokens only** ("도우미:"
lines), so the LM head no longer receives gradient from predicting the
"사용자:" prompt bytes. Lesson R-1A.2 lane B.

Loss-masking design
-------------------
The corpus is line-structured:

    사용자: <utterance>\n
    도우미: <response>\n
    사용자: <utterance>\n
    도우미: <response>\n
    \n
    사용자: <utterance>\n
    …

We tokenize line-by-line. For every line whose prefix is "도우미: " we mark
the **response body** (everything after the "도우미: " prefix, *including*
the trailing newline) as loss=1, everything else as loss=0. The "도우미: "
prefix itself is part of the prompt, so it stays loss=0 — this isolates the
gradient to the bytes that anima must learn to emit.

A second tensor `mask` (same shape as `y`) is built alongside `ids` and
sliced into windows in lockstep with the LM target. `cross_entropy` is
called with `reduction='none'` to obtain per-token loss, which is then
multiplied by the mask and averaged over the number of *active* mask
positions in the window (avoids artificial loss shrinkage when a window
happens to contain mostly user bytes).

Hyperparameters
---------------
lr = 2e-6 (matches Phase 1A.1; isolates loss-masking effect from lr).
steps = 200, bsz = 2, grad_accum = 8, ctx = 1024 — identical to Phase 1A.2.
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

    def encode_body_only(self, text: str) -> list:
        """No BOS/EOS — used for line-level concatenation."""
        return [b + 3 for b in text.encode("utf-8")]

    def decode(self, ids: list) -> str:
        bs = bytes(t - 3 for t in ids if t >= 3 and t < 259)
        return bs.decode("utf-8", errors="replace")


ANIMA_PREFIX = "도우미: "
USER_PREFIX = "사용자: "


class MaskedCorpusDataset(Dataset):
    """Loss-masked byte corpus.

    Builds (ids, mask) tensors of equal length. mask[i]=1 iff token i is
    inside an anima response body (after the '도우미: ' prefix); 0 elsewhere
    (user lines, anima prefix, blank lines, BOS/EOS, padding).
    """

    def __init__(self, corpus_path, tokenizer, ctx, label):
        print(f"[{label}] loading {corpus_path} …", flush=True)
        with open(corpus_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        print(f"[{label}] {len(text):,} chars", flush=True)

        ids_all = [tokenizer.bos]
        mask_all = [0]

        # Split keeping newlines so every emitted segment is self-contained.
        # We walk line-by-line — each line ends with '\n' except possibly the
        # last. For each line decide whether it is an anima response: prefix
        # "도우미: ". The response body = everything after the prefix
        # (excluding the prefix itself). The trailing newline is part of the
        # response body since the model must learn when to terminate.
        lines = text.splitlines(keepends=True)
        n_anima_lines = 0
        for line in lines:
            if line.startswith(ANIMA_PREFIX):
                prefix_bytes = tokenizer.encode_body_only(ANIMA_PREFIX)
                body = line[len(ANIMA_PREFIX):]
                body_bytes = tokenizer.encode_body_only(body)
                ids_all.extend(prefix_bytes)
                mask_all.extend([0] * len(prefix_bytes))
                ids_all.extend(body_bytes)
                mask_all.extend([1] * len(body_bytes))
                n_anima_lines += 1
            else:
                # user line, blank line, or anything else
                tok_bytes = tokenizer.encode_body_only(line)
                ids_all.extend(tok_bytes)
                mask_all.extend([0] * len(tok_bytes))

        ids_all.append(tokenizer.eos)
        mask_all.append(0)

        assert len(ids_all) == len(mask_all)
        total = len(ids_all)
        masked = sum(mask_all)
        print(
            f"[{label}] encoded {total:,} tokens, mask=1 on {masked:,} "
            f"({masked / total:.1%}), anima lines={n_anima_lines:,}",
            flush=True,
        )
        self.ids = torch.tensor(ids_all, dtype=torch.long)
        self.mask = torch.tensor(mask_all, dtype=torch.float32)
        self.ctx = ctx
        self.label = label

    def __len__(self):
        return max(1, (len(self.ids) - 1) // self.ctx)

    def __getitem__(self, idx):
        start = idx * self.ctx
        x = self.ids[start: start + self.ctx]
        y = self.ids[start + 1: start + 1 + self.ctx]
        # mask aligned with y (target tokens): predict the next-token; the
        # mask should reflect "is the *target* a response byte?".
        m = self.mask[start + 1: start + 1 + self.ctx]
        if len(x) < self.ctx:
            x = F.pad(x, (0, self.ctx - len(x)), value=0)
        if len(y) < self.ctx:
            y = F.pad(y, (0, self.ctx - len(y)), value=0)
        if len(m) < self.ctx:
            m = F.pad(m, (0, self.ctx - len(m)), value=0.0)
        return x, y, m


def load_ckpt(model, ckpt_path):
    print(f"[ckpt] loading {ckpt_path} …", flush=True)
    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    if missing:
        print(f"[ckpt] WARN missing={len(missing)}: {missing[:5]}", flush=True)
    if unexpected:
        print(f"[ckpt] WARN unexpected={len(unexpected)}: {unexpected[:5]}", flush=True)
    print("[ckpt] LOADED", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-ckpt", required=True)
    p.add_argument("--chat-corpus", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--bsz", type=int, default=2)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--ctx", type=int, default=1024)
    p.add_argument("--lr", type=float, default=2e-6)
    p.add_argument("--warmup", type=int, default=20)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cost-cap-usd", type=float, default=0.15)
    p.add_argument("--cost-per-hr", type=float, default=0.27)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = args.ctx
    print(f"[cfg] {cfg}", flush=True)

    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    ds_h = MaskedCorpusDataset(args.chat_corpus, tok, cfg.ctx, "anima_fact_masked")
    loader_h = DataLoader(
        ds_h, batch_size=args.bsz, shuffle=True, num_workers=1, pin_memory=True, drop_last=True
    )
    print(f"[data] anima_fact_masked windows={len(ds_h)}", flush=True)

    model = EngineAGModel(cfg).cuda().bfloat16()
    load_ckpt(model, args.base_ckpt)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] params={n_params:,}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.05)

    def lr_lambda(step):
        if step < args.warmup:
            return step / max(1, args.warmup)
        progress = (step - args.warmup) / max(1, args.steps - args.warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    model.train()
    t0 = time.time()
    step = 0
    iter_h = iter(loader_h)
    accum_loss = 0.0
    accum_count = 0
    accum_active = 0.0

    print(
        f"[train] Phase 1A.3 loss-masking starting (lr={args.lr}, {args.steps} steps, "
        f"mask=response-only) …",
        flush=True,
    )
    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        for _ in range(args.grad_accum):
            try:
                x, y, m = next(iter_h)
            except StopIteration:
                iter_h = iter(loader_h)
                x, y, m = next(iter_h)
            x = x.cuda(non_blocking=True)
            y = y.cuda(non_blocking=True)
            m = m.cuda(non_blocking=True)
            out = model(x)
            if isinstance(out, dict):
                logits = out["logits"]
            elif isinstance(out, tuple):
                logits = out[0]
            else:
                logits = out
            # per-token CE; ignore_index=0 still nukes padding rows.
            per_tok = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)).float(),
                y.reshape(-1),
                ignore_index=0,
                reduction="none",
            )
            m_flat = m.reshape(-1)
            masked = per_tok * m_flat
            denom = m_flat.sum().clamp(min=1.0)
            loss = masked.sum() / denom
            (loss / args.grad_accum).backward()
            accum_loss += loss.item()
            accum_count += 1
            accum_active += float(denom.item())

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        step += 1

        if step % 10 == 0 or step == 1:
            elapsed = (time.time() - t0) / 60
            cost = elapsed / 60 * args.cost_per_hr
            mem = torch.cuda.max_memory_allocated() / 1e9
            avg_loss = accum_loss / max(1, accum_count)
            avg_active = accum_active / max(1, accum_count)
            lr_now = sched.get_last_lr()[0]
            print(
                f"[step {step:>4}/{args.steps}] loss={avg_loss:.4f} lr={lr_now:.2e} "
                f"mem={mem:.1f}GB elapsed={elapsed:.1f}min cost=${cost:.3f} "
                f"active_tokens={avg_active:.0f}/win",
                flush=True,
            )
            accum_loss = 0.0
            accum_count = 0
            accum_active = 0.0
            if cost > args.cost_cap_usd:
                print(f"[cost-cap] {cost:.3f} > {args.cost_cap_usd} → halt", flush=True)
                break

        if step % 100 == 0:
            cp = os.path.join(args.output, f"ckpt_step{step}.pt")
            torch.save({"model": model.state_dict()}, cp)
            print(f"[ckpt] saved {cp}", flush=True)

    cp = os.path.join(args.output, "ckpt_final.pt")
    torch.save({"model": model.state_dict()}, cp)
    elapsed_min = (time.time() - t0) / 60
    cost = elapsed_min / 60 * args.cost_per_hr
    print(f"[ckpt] saved {cp}", flush=True)
    meta = {
        "preset": "phase1a3_loss_masking",
        "loss_mask": "response_only (도우미: body bytes)",
        "steps_completed": step,
        "steps_target": args.steps,
        "elapsed_min": elapsed_min,
        "cost_usd": cost,
        "n_params": n_params,
        "lineage_tag": "phase1a_multi_turn_sft -> phase1a1_color_cosmology_v2 -> phase1a3_loss_masking",
        "base_ckpt": args.base_ckpt,
        "lr": args.lr,
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
