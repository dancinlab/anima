"""Phase 1B SimPO training on top of Phase 1A SFT checkpoint.

WHY SimPO over DPO?
- SimPO needs NO reference model → 2× memory savings, simpler pipeline.
- EngineAG is custom arch — TRL DPOTrainer expects HF model + tokenizer +
  __call__ returning HF ModelOutput. Wrapping all of that is brittle.
  Direct SimPO loss is ~30 lines.

SimPO loss (Park et al. 2024 https://arxiv.org/abs/2405.14734):

    π_θ(y|x) = exp(Σ_t log p_θ(y_t | x, y_<t))   (sequence likelihood)
    avg_logp(y|x) = (1/|y|) · log π_θ(y|x)       (length-normalized)

    L_SimPO = -log σ( β · ( avg_logp(y_w|x) - avg_logp(y_l|x) ) - γ )

  where:
    β  = reward scaling (default 2.0; we use 2.5)
    γ  = target reward margin (default 0.5; we use 1.4 for stronger separation)
    y_w = chosen (winner), y_l = rejected (loser)

Why length-normalize? rejected samples in our data are sometimes longer
(verbose hallucinations). Without length-norm, longer sequences accumulate
more log-prob magnitude even if average per-token p is poor → DPO/SimPO
trains to game length, not semantics.

USAGE (pod-side after upload):
    python3 train_phase1b_simpo.py \
        --phase1a-ckpt /workspace/anima/ckpts/ckpt_phase1a_sft.pt \
        --pref-pairs /workspace/anima/data/preference_pairs.jsonl \
        --output /workspace/anima/output \
        --steps 600 --bsz 4 --grad-accum 4 \
        --lr 5e-6 --beta 2.5 --gamma 1.4 \
        --cost-cap-usd 10.0 --cost-per-hr 2.99
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
    """Matches train_phase2_cotrain.py — byte-level + special tokens (bos=1, eos=2, pad=0)."""

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
    """JSONL of {prompt, chosen, rejected}.

    Returns pre-tokenized tensors:
        prompt_ids       (L_p,)
        chosen_full_ids  (L_p + L_c + 1 for eos,)  with chosen_mask: 1 over chosen+eos region
        rejected_full_ids (L_p + L_r + 1,)         with rejected_mask: 1 over rejected+eos
    """

    def __init__(self, path: str, tokenizer: ByteTokenizer, max_len: int = 256):
        self.tok = tokenizer
        self.items = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                p_ids = tokenizer.encode(rec["prompt"])  # has bos at front
                # drop trailing eos from prompt (we want to continue, not stop)
                if p_ids and p_ids[-1] == tokenizer.eos:
                    p_ids = p_ids[:-1]
                c_ids = tokenizer.encode_no_special(rec["chosen"]) + [tokenizer.eos]
                r_ids = tokenizer.encode_no_special(rec["rejected"]) + [tokenizer.eos]
                full_c = p_ids + c_ids
                full_r = p_ids + r_ids
                if len(full_c) > max_len or len(full_r) > max_len:
                    # truncate from the prompt-side head if too long (rare for our data)
                    over_c = max(0, len(full_c) - max_len)
                    over_r = max(0, len(full_r) - max_len)
                    over = max(over_c, over_r)
                    p_ids = p_ids[over:]
                    full_c = p_ids + c_ids
                    full_r = p_ids + r_ids
                self.items.append({
                    "prompt_len": len(p_ids),
                    "full_c": full_c,
                    "full_r": full_r,
                    "chosen_len": len(c_ids),
                    "rejected_len": len(r_ids),
                })
        print(f"[data] loaded {len(self.items)} pairs from {path}", flush=True)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, idx):
        return self.items[idx]


def collate(batch, pad_id: int = 0):
    """Pad chosen/rejected to max length in batch, return tensors + masks."""
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
        # response region = positions [Pl, Lc) and [Pl, Lr)
        c_resp_mask[i, Pl:Lc] = 1.0
        r_resp_mask[i, Pl:Lr] = 1.0
    return c_ids, c_resp_mask, r_ids, r_resp_mask


def seq_avg_logp(model, input_ids: torch.Tensor, resp_mask: torch.Tensor, vocab_size: int) -> torch.Tensor:
    """Length-normalized log-prob of response region.

    For autoregressive LM: log p(y_t | y_<t) is supervised at position (t-1)'s
    logits predicting label y_t. Standard left-shift:
        shift_logits = logits[:, :-1, :]
        shift_labels = input_ids[:, 1:]
        shift_mask   = resp_mask[:, 1:]
    """
    out = model(input_ids)
    logits = out["logits"] if isinstance(out, dict) else out[0]
    shift_logits = logits[:, :-1, :].contiguous()
    shift_labels = input_ids[:, 1:].contiguous()
    shift_mask = resp_mask[:, 1:].contiguous().to(shift_logits.dtype)
    # gather log-prob at label positions
    logp = F.log_softmax(shift_logits.float(), dim=-1)
    tok_logp = logp.gather(-1, shift_labels.unsqueeze(-1)).squeeze(-1)  # (B, T-1)
    # masked sum / length
    num = (tok_logp * shift_mask).sum(dim=-1)  # (B,)
    den = shift_mask.sum(dim=-1).clamp(min=1.0)
    return num / den


def simpo_loss(logp_w: torch.Tensor, logp_l: torch.Tensor, beta: float, gamma: float):
    """L = -log σ( β (logp_w - logp_l) - γ )."""
    diff = beta * (logp_w - logp_l) - gamma
    loss = -F.logsigmoid(diff).mean()
    acc = (logp_w > logp_l).float().mean()  # chosen > rejected rate
    margin = (logp_w - logp_l).mean()
    return loss, acc, margin


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--phase1a-ckpt", required=True)
    p.add_argument("--pref-pairs", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=600)
    p.add_argument("--bsz", type=int, default=4)
    p.add_argument("--grad-accum", type=int, default=4)
    p.add_argument("--lr", type=float, default=5e-6)
    p.add_argument("--beta", type=float, default=2.5)
    p.add_argument("--gamma", type=float, default=1.4)
    p.add_argument("--max-len", type=int, default=256)
    p.add_argument("--warmup", type=int, default=30)
    p.add_argument("--save-every", type=int, default=300)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cost-cap-usd", type=float, default=10.0)
    p.add_argument("--cost-per-hr", type=float, default=2.99)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    cfg = EngineAGConfig.phase2_cotrain_350m()
    tok = ByteTokenizer(vocab_size=cfg.vocab_size)
    print(f"[cfg] {cfg}", flush=True)

    # Data
    ds = PreferenceDataset(args.pref_pairs, tok, max_len=args.max_len)

    def _collate(b):
        return collate(b, pad_id=0)

    loader = DataLoader(
        ds, batch_size=args.bsz, shuffle=True, num_workers=1,
        collate_fn=_collate, pin_memory=True, drop_last=True,
    )

    # Model + Phase 1A load
    model = EngineAGModel(cfg).cuda().bfloat16()
    print(f"[ckpt] loading Phase 1A → {args.phase1a_ckpt}", flush=True)
    payload = torch.load(args.phase1a_ckpt, map_location="cpu", weights_only=False)
    sd = payload.get("model") or payload.get("state_dict") or payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    if missing:
        print(f"[ckpt] WARN missing keys: {len(missing)} sample={missing[:3]}", flush=True)
    if unexpected:
        print(f"[ckpt] WARN unexpected keys: {len(unexpected)} sample={unexpected[:3]}", flush=True)
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
    accum_loss = 0.0
    accum_acc = 0.0
    accum_margin = 0.0
    accum_count = 0

    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        micro_loss = 0.0
        micro_acc = 0.0
        micro_margin = 0.0
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

            logp_w = seq_avg_logp(model, c_ids, c_mask, cfg.vocab_size)
            logp_l = seq_avg_logp(model, r_ids, r_mask, cfg.vocab_size)
            loss, acc, margin = simpo_loss(logp_w, logp_l, args.beta, args.gamma)
            (loss / args.grad_accum).backward()
            micro_loss += loss.item()
            micro_acc += acc.item()
            micro_margin += margin.item()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        step += 1

        avg_loss = micro_loss / args.grad_accum
        avg_acc = micro_acc / args.grad_accum
        avg_margin = micro_margin / args.grad_accum
        accum_loss += avg_loss
        accum_acc += avg_acc
        accum_margin += avg_margin
        accum_count += 1

        if step % 10 == 0 or step == 1:
            elapsed_h = (time.time() - t0) / 3600
            cost = elapsed_h * args.cost_per_hr
            cur_lr = sched.get_last_lr()[0]
            mem = torch.cuda.memory_allocated() / 1e9
            ml = accum_loss / max(1, accum_count)
            ma = accum_acc / max(1, accum_count)
            mm = accum_margin / max(1, accum_count)
            print(
                f"[step {step:4d}/{args.steps}] loss={avg_loss:.4f}/{ml:.4f} "
                f"acc={avg_acc:.3f}/{ma:.3f} margin={avg_margin:.3f}/{mm:.3f} "
                f"lr={cur_lr:.2e} mem={mem:.1f}GB elapsed={elapsed_h*60:.1f}min cost=${cost:.2f}",
                flush=True,
            )
            accum_loss = 0.0
            accum_acc = 0.0
            accum_margin = 0.0
            accum_count = 0
            if cost > args.cost_cap_usd:
                print(f"[COST_CAP] ${cost:.2f} > ${args.cost_cap_usd} → halt", flush=True)
                break

        if step % args.save_every == 0:
            ck = os.path.join(args.output, f"ckpt_step{step}.pt")
            torch.save({"model": model.state_dict(), "step": step, "cfg": cfg.__dict__}, ck)
            print(f"[ckpt] saved {ck}", flush=True)

    # Final
    final_path = os.path.join(args.output, "ckpt_phase1b_simpo.pt")
    torch.save({"model": model.state_dict(), "step": step, "cfg": cfg.__dict__}, final_path)
    meta = {
        "preset": "phase1b_simpo",
        "steps_completed": step,
        "steps_target": args.steps,
        "elapsed_min": (time.time() - t0) / 60,
        "cost_usd": (time.time() - t0) / 3600 * args.cost_per_hr,
        "beta": args.beta,
        "gamma": args.gamma,
        "lr": args.lr,
        "n_pairs": len(ds),
        "n_params": n_params,
        "phase1a_ckpt": args.phase1a_ckpt,
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
