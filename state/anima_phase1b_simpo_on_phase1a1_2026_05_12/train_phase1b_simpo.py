"""Phase 1B SimPO on Phase 1A.1 — substrate-mismatch-corrected retry.

Differences from prior B' SimPO attempt:
  1. Base ckpt: Phase 1A.1 (NOT B')
  2. Prompt format: V5.8-exact 2-line ack (NOT abbreviated '네, 기억할게요.')
  3. Hyperparams (conservative — prior B' over-sharpened to margin 3.5):
       beta  = 0.05   (was 2.5)   ← 50x weaker reward separation
       gamma = 0.3    (was 1.4)   ← gentler target margin
       lr    = 5e-6   (same)
       steps = 500    (was 600)   ← shorter, less ossification risk
  4. SFT-anchor (chat-co-train weight 0.9→1.0) — preserve language modeling
     ability on chosen sequences via auxiliary CE loss term.

L_total = L_SimPO + w * L_ce_chosen
  where w ramps 0.9 → 1.0 over training (favor SFT signal early to prevent
  distribution collapse; lift SimPO gradient at end to align preferences).

USAGE (pod-side):
    python3 train_phase1b_simpo.py \\
        --base-ckpt /workspace/anima/ckpts/ckpt_phase1a1_sft.pt \\
        --pref-pairs /workspace/anima/data/preference_pairs.jsonl \\
        --output /workspace/anima/output \\
        --steps 500 --bsz 4 --grad-accum 4 \\
        --lr 5e-6 --beta 0.05 --gamma 0.3 \\
        --w-start 0.9 --w-end 1.0 \\
        --cost-cap-usd 0.50 --cost-per-hr 0.86
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

    def encode_no_special(self, text: str) -> list:
        return [b + 3 for b in text.encode("utf-8")]


class PreferenceDataset(Dataset):
    def __init__(self, path: str, tokenizer: ByteTokenizer, max_len: int = 256):
        self.tok = tokenizer
        self.items = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                p_ids = tokenizer.encode(rec["prompt"])
                if p_ids and p_ids[-1] == tokenizer.eos:
                    p_ids = p_ids[:-1]
                c_ids = tokenizer.encode_no_special(rec["chosen"]) + [tokenizer.eos]
                r_ids = tokenizer.encode_no_special(rec["rejected"]) + [tokenizer.eos]
                full_c = p_ids + c_ids
                full_r = p_ids + r_ids
                if len(full_c) > max_len or len(full_r) > max_len:
                    over = max(len(full_c) - max_len, len(full_r) - max_len, 0)
                    p_ids = p_ids[over:]
                    full_c = p_ids + c_ids
                    full_r = p_ids + r_ids
                self.items.append({
                    "prompt_len": len(p_ids),
                    "full_c": full_c,
                    "full_r": full_r,
                })
        print(f"[data] loaded {len(self.items)} pairs from {path}", flush=True)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


def collate(batch, pad_id: int = 0):
    max_c = max(len(b["full_c"]) for b in batch)
    max_r = max(len(b["full_r"]) for b in batch)
    B = len(batch)
    c_ids = torch.full((B, max_c), pad_id, dtype=torch.long)
    r_ids = torch.full((B, max_r), pad_id, dtype=torch.long)
    c_resp_mask = torch.zeros((B, max_c), dtype=torch.float)
    r_resp_mask = torch.zeros((B, max_r), dtype=torch.float)
    for i, b in enumerate(batch):
        Lc, Lr = len(b["full_c"]), len(b["full_r"])
        Pl = b["prompt_len"]
        c_ids[i, :Lc] = torch.tensor(b["full_c"], dtype=torch.long)
        r_ids[i, :Lr] = torch.tensor(b["full_r"], dtype=torch.long)
        c_resp_mask[i, Pl:Lc] = 1.0
        r_resp_mask[i, Pl:Lr] = 1.0
    return c_ids, c_resp_mask, r_ids, r_resp_mask


def forward_logits(model, input_ids):
    out = model(input_ids)
    if isinstance(out, dict):
        return out["logits"]
    if isinstance(out, tuple):
        return out[0]
    return out


def seq_avg_logp(logits, input_ids, resp_mask):
    """Length-normalized log-prob of response region (computed from precomputed logits)."""
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = input_ids[:, 1:].contiguous()
    shift_mask = resp_mask[:, 1:].contiguous().to(shift_logits.dtype)
    logp = F.log_softmax(shift_logits.float(), dim=-1)
    tok_logp = logp.gather(-1, shift_labels.unsqueeze(-1)).squeeze(-1)
    num = (tok_logp * shift_mask).sum(dim=-1)
    den = shift_mask.sum(dim=-1).clamp(min=1.0)
    return num / den


def ce_loss_response(logits, input_ids, resp_mask):
    """Standard CE over response tokens — preserves SFT signal."""
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = input_ids[:, 1:].contiguous()
    shift_mask = resp_mask[:, 1:].contiguous().to(shift_logits.dtype)
    flat_logits = shift_logits.reshape(-1, shift_logits.size(-1)).float()
    flat_labels = shift_labels.reshape(-1)
    ce = F.cross_entropy(flat_logits, flat_labels, reduction="none")  # (B*T-1,)
    ce = ce.reshape(shift_labels.shape)
    masked = (ce * shift_mask).sum() / shift_mask.sum().clamp(min=1.0)
    return masked


def simpo_loss(logp_w, logp_l, beta, gamma):
    diff = beta * (logp_w - logp_l) - gamma
    loss = -F.logsigmoid(diff).mean()
    acc = (logp_w > logp_l).float().mean()
    margin = (logp_w - logp_l).mean()
    return loss, acc, margin


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base-ckpt", required=True)
    p.add_argument("--pref-pairs", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--bsz", type=int, default=4)
    p.add_argument("--grad-accum", type=int, default=4)
    p.add_argument("--lr", type=float, default=5e-6)
    p.add_argument("--beta", type=float, default=0.05)
    p.add_argument("--gamma", type=float, default=0.3)
    p.add_argument("--w-start", type=float, default=0.9, help="SFT chosen-CE weight start")
    p.add_argument("--w-end", type=float, default=1.0, help="SFT chosen-CE weight end")
    p.add_argument("--max-len", type=int, default=192)
    p.add_argument("--warmup", type=int, default=25)
    p.add_argument("--save-every", type=int, default=250)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cost-cap-usd", type=float, default=0.50)
    p.add_argument("--cost-per-hr", type=float, default=0.86)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    cfg = EngineAGConfig.phase2_cotrain_350m()
    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    print(f"[cfg] {cfg}", flush=True)
    print(f"[hp] beta={args.beta} gamma={args.gamma} lr={args.lr} steps={args.steps} "
          f"w={args.w_start}->{args.w_end}", flush=True)

    ds = PreferenceDataset(args.pref_pairs, tok, max_len=args.max_len)

    def _collate(b):
        return collate(b, pad_id=0)

    loader = DataLoader(
        ds, batch_size=args.bsz, shuffle=True, num_workers=1,
        collate_fn=_collate, pin_memory=True, drop_last=True,
    )

    model = EngineAGModel(cfg).cuda().bfloat16()
    print(f"[ckpt] loading Phase 1A.1 → {args.base_ckpt}", flush=True)
    payload = torch.load(args.base_ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    if missing:
        print(f"[ckpt] WARN missing={len(missing)} sample={missing[:3]}", flush=True)
    if unexpected:
        print(f"[ckpt] WARN unexpected={len(unexpected)} sample={unexpected[:3]}", flush=True)
    print("[ckpt] LOADED", flush=True)

    n_params = sum(pp.numel() for pp in model.parameters())
    print(f"[model] params={n_params:,}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_lambda(step):
        if step < args.warmup:
            return step / max(1, args.warmup)
        progress = (step - args.warmup) / max(1, args.steps - args.warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    model.train()
    t0 = time.time()
    step = 0
    iter_loader = iter(loader)
    accum_loss = accum_simpo = accum_ce = accum_acc = accum_margin = 0.0
    accum_count = 0

    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        for _ in range(args.grad_accum):
            try:
                c_ids, c_mask, r_ids, r_mask = next(iter_loader)
            except StopIteration:
                iter_loader = iter(loader)
                c_ids, c_mask, r_ids, r_mask = next(iter_loader)
            c_ids = c_ids.cuda(non_blocking=True)
            c_mask = c_mask.cuda(non_blocking=True)
            r_ids = r_ids.cuda(non_blocking=True)
            r_mask = r_mask.cuda(non_blocking=True)

            logits_c = forward_logits(model, c_ids)
            logits_r = forward_logits(model, r_ids)
            logp_w = seq_avg_logp(logits_c, c_ids, c_mask)
            logp_l = seq_avg_logp(logits_r, r_ids, r_mask)
            loss_simpo, acc, margin = simpo_loss(logp_w, logp_l, args.beta, args.gamma)
            loss_ce = ce_loss_response(logits_c, c_ids, c_mask)

            progress = step / max(1, args.steps - 1)
            w_ce = args.w_start + (args.w_end - args.w_start) * progress
            loss_total = loss_simpo + w_ce * loss_ce

            (loss_total / args.grad_accum).backward()
            accum_loss += loss_total.item()
            accum_simpo += loss_simpo.item()
            accum_ce += loss_ce.item()
            accum_acc += acc.item()
            accum_margin += margin.item()
            accum_count += 1

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        step += 1

        if step % 10 == 0 or step == 1:
            elapsed_h = (time.time() - t0) / 3600
            cost = elapsed_h * args.cost_per_hr
            cur_lr = sched.get_last_lr()[0]
            mem = torch.cuda.memory_allocated() / 1e9
            n = max(1, accum_count)
            print(
                f"[step {step:4d}/{args.steps}] "
                f"total={accum_loss/n:.4f} simpo={accum_simpo/n:.4f} ce={accum_ce/n:.4f} "
                f"acc={accum_acc/n:.3f} margin={accum_margin/n:.3f} "
                f"lr={cur_lr:.2e} mem={mem:.1f}GB elapsed={elapsed_h*60:.1f}min cost=${cost:.3f}",
                flush=True,
            )
            accum_loss = accum_simpo = accum_ce = accum_acc = accum_margin = 0.0
            accum_count = 0
            if cost > args.cost_cap_usd:
                print(f"[COST_CAP] ${cost:.3f} > ${args.cost_cap_usd} → halt", flush=True)
                break

        if step % args.save_every == 0:
            ck = os.path.join(args.output, f"ckpt_step{step}.pt")
            torch.save({"model": model.state_dict(), "step": step}, ck)
            print(f"[ckpt] saved {ck}", flush=True)

    final_path = os.path.join(args.output, "ckpt_phase1b_simpo_on_phase1a1.pt")
    torch.save({"model": model.state_dict(), "step": step}, final_path)
    meta = {
        "preset": "phase1b_simpo_on_phase1a1",
        "steps_completed": step,
        "steps_target": args.steps,
        "elapsed_min": (time.time() - t0) / 60,
        "cost_usd": (time.time() - t0) / 3600 * args.cost_per_hr,
        "beta": args.beta,
        "gamma": args.gamma,
        "lr": args.lr,
        "w_start": args.w_start,
        "w_end": args.w_end,
        "n_pairs": len(ds),
        "n_params": n_params,
        "base_ckpt": args.base_ckpt,
        "lineage_tag": "phase1a1_color_cosmology -> phase1b_simpo (substrate-mismatch corrected)",
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
