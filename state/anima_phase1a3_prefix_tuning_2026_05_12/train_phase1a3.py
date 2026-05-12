"""
train_phase1a3.py — Phase 1A.3 prefix-tuning on Phase 1A.1 base.

Strategy (Li & Liang 2021 — Prefix-Tuning: Optimizing Continuous Prompts for Generation):
  - load Phase 1A.1 ckpt (base model with markdown attractor over anima_fact)
  - FREEZE all base model parameters (requires_grad=False)
  - introduce learnable `prefix = nn.Parameter(n_prefix × d_model)` only
  - forward: prepend prefix embeddings to the token-embedding sequence
    → base model layers receive `[prefix_emb (n_prefix), input_embeds (T)]`
    → causal mask extends naturally; lm_head logits for the prefix positions are discarded
  - loss computed only over the input-token positions (the real corpus)
  - optimizer only sees the prefix params (base weights frozen)

Rationale: full SFT (Phase 1A.1 lr 2e-6, Phase 1A.2 lr 1e-6) failed to break the byte-vocab
markdown attractor (`| --- | --- |`) over "의식" → next-byte distribution. Prefix-tuning
acts as a CONTROL PLANE — base attractor is unchanged, but the prefix shifts the response
distribution for prompts that contain "anima 는 의식 lane 안에 있는 entity" by conditioning
the entire causal context on a learnable continuous prompt.

Hyperparams:
  - n_prefix = 20
  - lr = 1e-3 (prefix-tuning literature: 1e-3 to 1e-2; much larger than full SFT 5e-6)
  - steps = 500
  - bsz = 2 × grad_accum 8, ctx 1024 - 20 = 1004 for real tokens
"""
import os
import sys
import json
import time
import math
import argparse
import random
from typing import Optional

import torch
import torch.nn as nn
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


class PrefixTunedEngineAG(nn.Module):
    """Wraps EngineAGModel with a learnable prefix prepended at the embedding level.

    All base model weights are frozen. Only `self.prefix` is trainable.

    forward(input_ids, labels=None):
        prefix_emb = self.prefix.expand(B, -1, -1)          # (B, n_prefix, D)
        tok_emb    = base.tok_emb(input_ids)                 # (B, T, D)
        x          = concat([prefix_emb, tok_emb], dim=1)    # (B, n_prefix + T, D)
        ... layers (with causal mask extended automatically) ...
        logits     = base.lm_head(base.norm_f(x))            # (B, n_prefix + T, V)
        # discard prefix logits, keep only the T positions corresponding to input_ids
        logits     = logits[:, n_prefix:, :]                 # (B, T, V)
        if labels is not None: standard shifted cross-entropy
    """

    def __init__(self, base: EngineAGModel, n_prefix: int = 20, init_std: float = 0.02):
        super().__init__()
        self.base = base
        self.n_prefix = n_prefix
        D = base.cfg.d_model
        # Initialize prefix from a random subset of token embeddings (Li & Liang reparam trick light)
        # — using random gaussian × init_std for simplicity, matches paper "from scratch" variant
        prefix = torch.randn(n_prefix, D) * init_std
        self.prefix = nn.Parameter(prefix)
        # Freeze base
        for p in self.base.parameters():
            p.requires_grad = False

    def trainable_parameters(self):
        return [self.prefix]

    def forward(
        self,
        input_ids: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ):
        B, T = input_ids.shape
        base = self.base
        # Embed input tokens (with frozen embeddings).
        tok_emb = base.tok_emb(input_ids)                      # (B, T, D)
        # Expand prefix to match dtype/device of tok_emb (bf16).
        prefix_emb = self.prefix.unsqueeze(0).expand(B, -1, -1).to(dtype=tok_emb.dtype, device=tok_emb.device)
        x = torch.cat([prefix_emb, tok_emb], dim=1)            # (B, n_prefix + T, D)
        # Engine G cells run over the extended sequence — its cell-pool logic uses x.mean(dim=1)
        # which naturally averages over the (prefix + tokens) extended seq.
        cells = base.engine_g.fresh_cells(B, x.device, x.dtype)
        for li, layer in enumerate(base.layers):
            t = base.engine_g.tension(x, cells)                # (B,)
            x, _ = layer(x, tension=t)
            if (li + 1) % base.cfg.g_refresh_every == 0 and li + 1 < base.cfg.n_layers:
                cells = base.engine_g.step(cells, x.mean(dim=1))
                x = x + base.engine_g.project_back(cells).unsqueeze(1)
        x = base.norm_f(x)
        logits_full = base.lm_head(x)                          # (B, n_prefix + T, V)
        # Discard prefix positions — we predict only real tokens
        logits = logits_full[:, self.n_prefix:, :]             # (B, T, V)
        loss = None
        if labels is not None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = F.cross_entropy(
                shift_logits.reshape(-1, shift_logits.size(-1)).float(),
                shift_labels.reshape(-1),
                ignore_index=0,
            )
        return {"logits": logits, "loss": loss}


def load_base_ckpt(model, ckpt_path):
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
    p.add_argument("--n-prefix", type=int, default=20)
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--bsz", type=int, default=2)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--ctx", type=int, default=1024)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--warmup", type=int, default=50)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cost-cap-usd", type=float, default=0.13)
    p.add_argument("--cost-per-hr", type=float, default=0.27)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    cfg = EngineAGConfig.phase2_cotrain_350m()
    # Real-token ctx leaves room for prefix on the prepend side; loader uses (ctx - n_prefix).
    real_ctx = args.ctx - args.n_prefix
    cfg.ctx = args.ctx
    print(f"[cfg] {cfg}", flush=True)
    print(f"[cfg] real_ctx (loader window) = {real_ctx}, n_prefix = {args.n_prefix}", flush=True)

    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    ds_h = CorpusDataset(args.chat_corpus, tok, real_ctx, "anima_fact")
    loader_h = DataLoader(ds_h, batch_size=args.bsz, shuffle=True, num_workers=1, pin_memory=True, drop_last=True)
    print(f"[data] anima_fact windows={len(ds_h)}", flush=True)

    base = EngineAGModel(cfg).cuda().bfloat16()
    load_base_ckpt(base, args.base_ckpt)
    model = PrefixTunedEngineAG(base, n_prefix=args.n_prefix).cuda()
    # Ensure prefix tensor lives in bf16 on cuda (Parameter default float32; cast).
    model.prefix.data = model.prefix.data.to(dtype=torch.bfloat16, device="cuda")

    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    n_frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    print(f"[model] trainable={n_trainable:,} frozen={n_frozen:,} ratio={n_trainable/(n_trainable+n_frozen):.2e}", flush=True)

    opt = torch.optim.AdamW(model.trainable_parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_lambda(step):
        if step < args.warmup:
            return step / max(1, args.warmup)
        progress = (step - args.warmup) / max(1, args.steps - args.warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    # Base model in eval to keep frozen RMSNorm running stats stable (no BN here, but consistent).
    model.base.eval()
    t0 = time.time()
    step = 0
    iter_h = iter(loader_h)
    accum_loss = 0.0
    accum_count = 0

    print(f"[train] Phase 1A.3 prefix-tuning starting (lr={args.lr}, {args.steps} steps, n_prefix={args.n_prefix}) …", flush=True)
    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        for _ in range(args.grad_accum):
            try:
                x, y = next(iter_h)
            except StopIteration:
                iter_h = iter(loader_h)
                x, y = next(iter_h)
            x = x.cuda(non_blocking=True)
            y = y.cuda(non_blocking=True)
            out = model(x)
            logits = out["logits"]
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)).float(), y.reshape(-1), ignore_index=0)
            (loss / args.grad_accum).backward()
            accum_loss += loss.item()
            accum_count += 1

        torch.nn.utils.clip_grad_norm_(model.trainable_parameters(), 1.0)
        opt.step()
        sched.step()
        step += 1

        if step % 20 == 0 or step == 1:
            elapsed = (time.time() - t0) / 60
            cost = elapsed / 60 * args.cost_per_hr
            mem = torch.cuda.max_memory_allocated() / 1e9
            avg_loss = accum_loss / max(1, accum_count)
            lr_now = sched.get_last_lr()[0]
            prefix_norm = float(model.prefix.detach().float().norm().item())
            print(
                f"[step {step:>4}/{args.steps}] loss={avg_loss:.4f} lr={lr_now:.2e} "
                f"prefix_norm={prefix_norm:.4f} mem={mem:.1f}GB elapsed={elapsed:.1f}min cost=${cost:.3f}",
                flush=True,
            )
            accum_loss = 0.0
            accum_count = 0
            if cost > args.cost_cap_usd:
                print(f"[cost-cap] {cost:.3f} > {args.cost_cap_usd} → halt", flush=True)
                break

        if step % 100 == 0:
            cp = os.path.join(args.output, f"prefix_step{step}.pt")
            torch.save({"prefix": model.prefix.detach().cpu(), "n_prefix": args.n_prefix}, cp)
            print(f"[ckpt] saved {cp}", flush=True)

    cp = os.path.join(args.output, "prefix_final.pt")
    torch.save({"prefix": model.prefix.detach().cpu(), "n_prefix": args.n_prefix}, cp)
    elapsed_min = (time.time() - t0) / 60
    cost = elapsed_min / 60 * args.cost_per_hr
    print(f"[ckpt] saved {cp}", flush=True)
    meta = {
        "preset": "phase1a3_prefix_tuning",
        "method": "prefix-tuning (Li & Liang 2021)",
        "n_prefix": args.n_prefix,
        "trainable_params": n_trainable,
        "frozen_params": n_frozen,
        "trainable_ratio": n_trainable / (n_trainable + n_frozen),
        "steps_completed": step,
        "steps_target": args.steps,
        "elapsed_min": elapsed_min,
        "cost_usd": cost,
        "lineage_tag": "phase1a_multi_turn_sft -> phase1a1_color_cosmology_v2 -> phase1a3_prefix_tuning",
        "base_ckpt": args.base_ckpt,
        "lr": args.lr,
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
