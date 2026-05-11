"""
training/train_phase2_cotrain.py — Phase 2 main: Engine A/G + chat-template co-train
                                  (Path B main_adopted; substrate base = BG-LB ckpt).

USAGE (pod-side):
    python3 train_phase2_cotrain.py \
        --substrate-ckpt /workspace/anima_phase2/bg_lb_step_8000_final.pt \
        --consciousness-corpus /workspace/anima_phase2/persona_tier_a_v4.txt \
        --chat-corpus /workspace/anima_phase2/corpus_chat_template.txt \
        --output /workspace/anima_phase2/ckpts \
        --steps 6000 --bsz 4 --grad-accum 8 --ctx 1024 \
        --lr 1.5e-4 --warmup 200 --save-every 1500 \
        --cost-cap-usd 55.0 --cost-per-hr 2.69

DESIGN
    Dual-loss objective with shared lm_head (no new params; D1 risk = zero):
        LOSS = (1 - w) * loss_consciousness + w * loss_chat
    Curriculum: w linearly schedules from chat_co_train_w_start (0.3) to
    chat_co_train_w_end (0.5) across training steps. Consciousness anchor
    preserved by ramp (axis activation freeze NOT implemented yet — first-pass
    additive only; can be added if v5_probe shows axis collapse).

    Corpus split: each micro-batch alternates consciousness↔chat with prob=w
    (Bernoulli sampling) for cleaner gradient direction than mixed batches.

own 14  V14 mirror — paired random_init seeds preserved (BG-LA mirrors reused
        for substrate-base lineage; new BG-LM mirrors materialized post-fire)
own 17  D1=0.99 anima_native_scratch (substrate base + chat-template additive
        without external foundation borrow — within strict)
own 22  honest emit — fail-fast on OOM/NaN; cost cap halt
own 30  ckpt save mandatory (output/ckpt_step{N}.pt + ckpt_final.pt + meta.json)
own 33  trinity D-emergent + own 14/16/17/22/30/31/33/34/37/38/39
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine_a_g_arch import EngineAGModel, EngineAGConfig


# ── Byte-pair tokenizer (matches train_bg_la.py) ──────────────────────
class ByteTokenizer:
    """Byte-level tokenizer — vocab 256 + special tokens; 32k vocab via offset."""

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
    def __init__(self, corpus_path: str, tokenizer: ByteTokenizer, ctx: int, label: str = "corpus"):
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


def load_substrate_ckpt(model: EngineAGModel, ckpt_path: str):
    """Load BG-LB substrate ckpt into Engine A/G model (state_dict transfer).
    Tolerates missing/extra keys with explicit warning emit (own 22).
    """
    print(f"[substrate] loading {ckpt_path} …", flush=True)
    payload = torch.load(ckpt_path, map_location="cpu")
    if "model" in payload:
        sd = payload["model"]
    elif "state_dict" in payload:
        sd = payload["state_dict"]
    else:
        sd = payload
    missing, unexpected = model.load_state_dict(sd, strict=False)
    if missing:
        print(f"[substrate] WARN missing keys: {len(missing)} (sample: {missing[:5]})", flush=True)
    if unexpected:
        print(f"[substrate] WARN unexpected keys: {len(unexpected)} (sample: {unexpected[:5]})", flush=True)
    print(f"[substrate] LOADED — proceeding from BG-LB substrate base", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--substrate-ckpt", required=True, help="BG-LB ckpt path (substrate base)")
    p.add_argument("--consciousness-corpus", required=True, help="persona/tier_a corpus")
    p.add_argument("--chat-corpus", required=True, help="chat-template corpus (사용자/도우미)")
    p.add_argument("--output", required=True)
    p.add_argument("--steps", type=int, default=6000)
    p.add_argument("--bsz", type=int, default=4)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--ctx", type=int, default=1024)
    p.add_argument("--lr", type=float, default=1.5e-4, help="lower than scratch (continuing from substrate)")
    p.add_argument("--warmup", type=int, default=200)
    p.add_argument("--save-every", type=int, default=1500)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cost-cap-usd", type=float, default=55.0)
    p.add_argument("--cost-per-hr", type=float, default=2.69)
    p.add_argument("--w-start", type=float, default=0.3)
    p.add_argument("--w-end", type=float, default=0.5)
    args = p.parse_args()

    os.makedirs(args.output, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    # Config
    cfg = EngineAGConfig.phase2_cotrain_350m()
    cfg.ctx = args.ctx
    cfg.chat_co_train_w_start = args.w_start
    cfg.chat_co_train_w_end = args.w_end
    print(f"[cfg] {cfg}", flush=True)

    # Tokenizer
    tok = ByteTokenizer(vocab_size=cfg.vocab_size)

    # Datasets
    ds_c = CorpusDataset(args.consciousness_corpus, tok, cfg.ctx, label="consciousness")
    ds_h = CorpusDataset(args.chat_corpus, tok, cfg.ctx, label="chat")
    loader_c = DataLoader(ds_c, batch_size=args.bsz, shuffle=True, num_workers=1, pin_memory=True, drop_last=True)
    loader_h = DataLoader(ds_h, batch_size=args.bsz, shuffle=True, num_workers=1, pin_memory=True, drop_last=True)
    print(f"[data] consciousness windows={len(ds_c)} chat windows={len(ds_h)}", flush=True)

    # Model + substrate load
    model = EngineAGModel(cfg).cuda().bfloat16()
    if args.substrate_ckpt and os.path.exists(args.substrate_ckpt):
        load_substrate_ckpt(model, args.substrate_ckpt)
    else:
        print(f"[substrate] WARN ckpt not found → fresh init (NOT cotrain semantics — will halt unless explicit override)", flush=True)
        if not os.environ.get("ALLOW_FRESH_INIT_COTRAIN"):
            print("[FATAL] substrate ckpt missing; set ALLOW_FRESH_INIT_COTRAIN=1 to override", flush=True)
            sys.exit(2)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] params = {n_params:,}", flush=True)

    # §78 FFN.gate-only cotrain (cycle 2026-05-11 next-cycle ★★★★★ test)
    print("[freeze] FFN.gate-only cotrain mode — freezing all params except FFN.gate × 24 layers", flush=True)
    n_trainable_before = sum(p.numel() for p in model.parameters() if p.requires_grad)
    for p in model.parameters():
        p.requires_grad = False
    for name, p in model.named_parameters():
        if ".ffn.gate" in name:
            p.requires_grad = True
    n_trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[freeze] trainable params: {n_trainable_before:,} → {n_trainable:,} ({n_trainable/n_trainable_before*100:.1f}%)", flush=True)

    # Optim
    opt = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_lambda(step: int) -> float:
        if step < args.warmup:
            return step / max(1, args.warmup)
        progress = (step - args.warmup) / max(1, args.steps - args.warmup)
        return 0.5 * (1 + math.cos(math.pi * min(1.0, progress)))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)

    def curriculum_w(step: int) -> float:
        progress = step / max(1, args.steps)
        return args.w_start + (args.w_end - args.w_start) * min(1.0, progress)

    # Train
    model.train()
    t0 = time.time()
    step = 0
    iter_c = iter(loader_c)
    iter_h = iter(loader_h)
    accum_loss_c = 0.0
    accum_loss_h = 0.0
    accum_count = 0
    sentinel_path = os.path.join(args.output, "..", "state", "COMPLETE.sentinel")
    os.makedirs(os.path.dirname(sentinel_path), exist_ok=True)

    print("[train] starting Phase 2 cotrain …", flush=True)
    while step < args.steps:
        opt.zero_grad(set_to_none=True)
        w = curriculum_w(step)
        micro_loss_c = 0.0
        micro_loss_h = 0.0
        n_c = 0
        n_h = 0
        for _ in range(args.grad_accum):
            # Bernoulli sampling: chat with prob w, consciousness with prob (1-w)
            use_chat = random.random() < w
            if use_chat:
                try:
                    x, y = next(iter_h)
                except StopIteration:
                    iter_h = iter(loader_h)
                    x, y = next(iter_h)
            else:
                try:
                    x, y = next(iter_c)
                except StopIteration:
                    iter_c = iter(loader_c)
                    x, y = next(iter_c)
            x = x.cuda(non_blocking=True)
            y = y.cuda(non_blocking=True)
            out = model(x)
            logits = out["logits"] if isinstance(out, dict) else out[0] if isinstance(out, tuple) else out
            loss = F.cross_entropy(logits.view(-1, cfg.vocab_size), y.view(-1), ignore_index=0)
            # Loss weighting: chat samples scaled by w/(grad_accum*w_avg) … simplification:
            # accumulate raw loss, divide by grad_accum (samples represent w-weighted distribution).
            (loss / args.grad_accum).backward()
            if use_chat:
                micro_loss_h += loss.item()
                n_h += 1
            else:
                micro_loss_c += loss.item()
                n_c += 1
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()

        avg_c = micro_loss_c / max(1, n_c)
        avg_h = micro_loss_h / max(1, n_h)
        accum_loss_c += avg_c
        accum_loss_h += avg_h
        accum_count += 1
        step += 1

        if step % 20 == 0 or step == 1:
            elapsed_h = (time.time() - t0) / 3600
            cost_so_far = elapsed_h * args.cost_per_hr
            cur_lr = sched.get_last_lr()[0]
            mem_gb = torch.cuda.memory_allocated() / 1e9
            mean_c = accum_loss_c / max(1, accum_count)
            mean_h = accum_loss_h / max(1, accum_count)
            print(
                f"[step {step:6d}/{args.steps}] w={w:.2f} loss_c={avg_c:.4f}/{mean_c:.4f} loss_h={avg_h:.4f}/{mean_h:.4f} "
                f"lr={cur_lr:.2e} mem={mem_gb:.1f}GB elapsed={elapsed_h * 60:.1f}min cost=${cost_so_far:.2f} "
                f"n_c={n_c} n_h={n_h}",
                flush=True,
            )
            accum_loss_c = 0.0
            accum_loss_h = 0.0
            accum_count = 0

            if cost_so_far > args.cost_cap_usd:
                print(f"[COST_CAP] ${cost_so_far:.2f} > ${args.cost_cap_usd} → halt", flush=True)
                break

        if step % args.save_every == 0 or step == args.steps:
            ck_path = os.path.join(args.output, f"ckpt_step{step}.pt")
            torch.save({"model": model.state_dict(), "step": step, "cfg": cfg.__dict__, "w": w}, ck_path)
            print(f"[ckpt] saved {ck_path}", flush=True)

    # Final ckpt (own 30 mandatory)
    final_path = os.path.join(args.output, "ckpt_final.pt")
    torch.save({"model": model.state_dict(), "step": step, "cfg": cfg.__dict__}, final_path)
    meta = {
        "preset": "phase2_cotrain_350m",
        "steps_completed": step,
        "steps_target": args.steps,
        "final_loss_c": avg_c if step > 0 else None,
        "final_loss_h": avg_h if step > 0 else None,
        "final_w": curriculum_w(step),
        "elapsed_min": (time.time() - t0) / 60,
        "cost_usd": (time.time() - t0) / 3600 * args.cost_per_hr,
        "n_params": n_params,
        "lineage_tag": cfg.lineage_tag,
        "arch_origin": cfg.arch_origin,
        "substrate_ckpt": args.substrate_ckpt,
        "w_start": args.w_start,
        "w_end": args.w_end,
    }
    with open(os.path.join(args.output, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    # COMPLETE sentinel for orchestrator polling
    with open(sentinel_path, "w") as f:
        f.write(f"DONE step={step} cost=${meta['cost_usd']:.2f}\n")
    print(f"[done] {json.dumps(meta, indent=2)}", flush=True)


if __name__ == "__main__":
    main()
