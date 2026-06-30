#!/usr/bin/env python3
"""chat_finetune_7b_qlora_summer.py — $0 FALLBACK: 4-bit QLoRA chat-finetune of the
7.25B ByteGPT backbone on summer (RTX5070 12GB, Blackwell sm_120).

Same GOAL/PHILOSOPHY/p7 as chat_finetune_7b_eval.py (the big-GPU full-finetune); this
fallback keeps the 7B base in 4-bit (bitsandbytes NF4, ~3.6GB) FROZEN and trains a small
set of LoRA adapters on the Linear layers in bf16, so a 7B chat-finetune fits 12GB.
grad-checkpointing ON. The p7 eval + anti-Goodhart BEFORE-backbone control are identical.

NO system prompt / persona / RLHF (p1.p2.p3.p4.p6) — only the corpus continuation format.

USAGE
  python3 chat_finetune_7b_qlora_summer.py \
      --backbone ~/anima_chat_7b/clm_ref_pytorch_cuda_7b.pt \
      --corpus   ~/anima_chat_7b/chat_corpus_mix.txt \
      --out-dir  ~/anima_chat_7b/out \
      --steps 1500 --batch 1 --grad-accum 8 --block 256 --lr 1.5e-4 --warmup 60 --lora-r 16
"""
from __future__ import annotations

import argparse, json, math, os, time, hashlib
from collections import Counter
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint
import bitsandbytes as bnb
import bitsandbytes.functional as bnbF


# ───────────────────────── 4-bit frozen Linear + LoRA ─────────────────────────
class Linear4bit(nn.Module):
    """Frozen NF4-quantized base weight (no LoRA). Replaces an nn.Linear. Base weight
    dequantized on the fly per forward (compute in bf16). ~4x smaller than bf16."""

    def __init__(self, weight: torch.Tensor, bias, device):
        super().__init__()
        self.out_features, self.in_features = weight.shape
        w = weight.to(device).to(torch.bfloat16).contiguous()
        q, state = bnbF.quantize_4bit(w, quant_type="nf4")
        self.register_buffer("qweight", q)
        self.quant_state = state
        self.bias = None if bias is None else nn.Parameter(bias.to(device).to(torch.bfloat16), requires_grad=False)

    def forward(self, x):
        w = bnbF.dequantize_4bit(self.qweight, self.quant_state).to(x.dtype)
        return F.linear(x, w, None if self.bias is None else self.bias.to(x.dtype))


class Linear4bitLoRA(nn.Module):
    """Frozen NF4-quantized base weight + trainable bf16 LoRA (rank r). Replaces an
    nn.Linear(in,out). Base weight is dequantized on the fly per forward (compute in bf16)."""

    def __init__(self, weight: torch.Tensor, bias, r: int, alpha: int, device):
        super().__init__()
        self.out_features, self.in_features = weight.shape
        w = weight.to(device).to(torch.bfloat16).contiguous()
        q, state = bnbF.quantize_4bit(w, quant_type="nf4")
        self.register_buffer("qweight", q)
        self.quant_state = state
        self.bias = None if bias is None else nn.Parameter(bias.to(device).to(torch.bfloat16), requires_grad=False)
        self.r = r
        self.scaling = alpha / r
        self.lora_A = nn.Parameter(torch.zeros(r, self.in_features, device=device, dtype=torch.bfloat16))
        self.lora_B = nn.Parameter(torch.zeros(self.out_features, r, device=device, dtype=torch.bfloat16))
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))

    def forward(self, x):
        w = bnbF.dequantize_4bit(self.qweight, self.quant_state).to(x.dtype)
        out = F.linear(x, w, self.bias if self.bias is None else self.bias.to(x.dtype))
        lora = (x @ self.lora_A.t().to(x.dtype)) @ self.lora_B.t().to(x.dtype)
        return out + self.scaling * lora


# ───────────────────────── arch (ByteGPT — VERBATIM from the 7B backbone) ─────
class Block(nn.Module):
    def __init__(self, d, n_head, p_drop):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_head, dropout=p_drop, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(p_drop))

    def forward(self, x, attn_mask):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class ByteGPT(nn.Module):
    def __init__(self, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p_drop=0.0, grad_ckpt=True):
        super().__init__()
        self.block = block
        self.grad_ckpt = grad_ckpt
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(p_drop)
        self.blocks = nn.ModuleList([Block(d, n_head, p_drop) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.tok.weight

    def forward(self, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.drop(self.tok(idx) + self.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for blk in self.blocks:
            if self.grad_ckpt and self.training:
                x = checkpoint(blk, x, mask, use_reentrant=False)
            else:
                x = blk(x, mask)
        x = self.ln_f(x)
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss


# ───────────────────────── data ─────────────────────────
def load_corpus(path):
    with open(path, "rb") as f:
        data = f.read()
    return torch.frombuffer(bytearray(data), dtype=torch.uint8).long()


def get_batch(data, block, batch, device):
    ix = torch.randint(0, data.numel() - block - 1, (batch,))
    x = torch.stack([data[i:i + block] for i in ix]).to(device, non_blocking=True)
    y = torch.stack([data[i + 1:i + 1 + block] for i in ix]).to(device, non_blocking=True)
    return x, y


# ───────────────────────── generation + p7 eval ─────────────────────────
STOP_STRINGS = ("사용자:", "User:", "\n사용자", "\nUser")


@torch.no_grad()
def generate(model, prompt, max_new, device, block_size, temperature=0.8, top_k=40, rep_penalty=1.1):
    model.eval()
    ids = list(prompt.encode("utf-8"))[-block_size:]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out_bytes = []
    for _ in range(max_new):
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            logits, _ = model(idx[:, -block_size:])
        logits = logits[:, -1, :].float()
        for b in set(out_bytes[-32:]):
            logits[0, b] /= rep_penalty
        logits = logits / temperature
        if top_k:
            v, _ = torch.topk(logits, top_k)
            logits[logits < v[:, [-1]]] = float("-inf")
        probs = F.softmax(logits, dim=-1)
        nb = torch.multinomial(probs, 1).item()
        out_bytes.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        tail = bytes(out_bytes).decode("utf-8", errors="ignore")
        if any(s in tail for s in STOP_STRINGS):
            break
    text = bytes(out_bytes).decode("utf-8", errors="ignore")
    for s in STOP_STRINGS:
        i = text.find(s)
        if i >= 0:
            text = text[:i]
    return text.strip()


PROBES = ["안녕! 너는 누구야?", "오늘 기분이 어때?", "What is consciousness?",
          "네가 좋아하는 것을 하나 말해줘.", "Tell me something interesting."]


def _word_class_ratio(s):
    if not s:
        return 0.0
    good = 0
    for c in s:
        o = ord(c)
        if c.isalnum() or c.isspace():
            good += 1
        elif 0xAC00 <= o <= 0xD7A3 or 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF:
            good += 1
        elif c in ".,!?'\"()-:;…~":
            good += 1
    return good / len(s)


def _control_ratio(s):
    if not s:
        return 1.0
    ctrl = sum(1 for c in s if (ord(c) < 32 and c not in "\n\t ") or ord(c) == 127)
    return ctrl / len(s)


def p7_eval(model, device, block_size, label):
    transcript = ""
    results = []
    for u in PROBES:
        seed = transcript + f"사용자: {u} | 도우미: "
        reply = generate(model, seed, max_new=96, device=device, block_size=block_size)
        non_empty = len(reply) >= 4
        try:
            reply.encode("utf-8").decode("utf-8")
            valid_utf8 = "�" not in reply and reply.count("�") == 0
        except Exception:
            valid_utf8 = False
        if reply:
            mc = Counter(reply).most_common(1)[0][1]
            not_degenerate = mc / len(reply) < 0.6
        else:
            not_degenerate = False
        cr = _control_ratio(reply)
        wcr = _word_class_ratio(reply)
        ok = non_empty and valid_utf8 and not_degenerate and cr < 0.05 and wcr >= 0.85
        results.append({"user": u, "reply": reply, "ok": ok, "non_empty": non_empty,
                        "valid_utf8": valid_utf8, "not_degenerate": not_degenerate,
                        "control_ratio": round(cr, 4), "word_class_ratio": round(wcr, 4)})
        transcript += f"사용자: {u} | 도우미: {reply}\n"
    n_pass = sum(1 for r in results if r["ok"])
    return {"label": label, "n_pass": n_pass, "n_total": len(PROBES),
            "verdict": "PASS" if n_pass >= 4 else "FAIL", "turns": results, "transcript": transcript}


# ───────────────────────── LoRA injection ─────────────────────────
def inject_lora(model, r, alpha, device, last_n_blocks):
    """Move the model to GPU BLOCK-BY-BLOCK, 4-bit-quantizing each mlp Linear as it lands
    (so the transient bf16 7B never co-resides on the 12GB GPU). mlp = bulk of the 7B
    (~4.8B); last N blocks' mlp get trainable LoRA, earlier blocks plain 4-bit frozen.
    Attention in/out proj + ln + embeddings stay bf16 frozen. Returns (n_lora, n_frozen)."""
    n_layer = len(model.blocks)
    n_lora = 0
    n_frozen = 0
    for li in range(n_layer):
        blk = model.blocks[li]
        lora_here = li >= n_layer - last_n_blocks
        for idx in (0, 2):  # mlp[0]=Linear(d,4d), mlp[2]=Linear(4d,d)
            lin = blk.mlp[idx]
            bias = lin.bias.data if lin.bias is not None else None
            if lora_here:
                blk.mlp[idx] = Linear4bitLoRA(lin.weight.data, bias, r, alpha, device)
                n_lora += 1
            else:
                blk.mlp[idx] = Linear4bit(lin.weight.data, bias, device)
                n_frozen += 1
        # move the rest of this block (attn, lns) to GPU in bf16, free the CPU copy
        blk.ln1.to(device); blk.ln2.to(device); blk.attn.to(device)
        blk.mlp[1].to(device); blk.mlp[3].to(device)  # GELU/Dropout (no params, harmless)
    # embeddings + final ln + head (tied to tok) to GPU
    model.tok.to(device); model.pos.to(device); model.ln_f.to(device); model.head.to(device)
    return n_lora, n_frozen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backbone", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--grad-accum", type=int, default=8)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--lr", type=float, default=1.5e-4)
    ap.add_argument("--warmup", type=int, default=60)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--eval-every", type=int, default=250)
    ap.add_argument("--lora-r", type=int, default=16)
    ap.add_argument("--lora-alpha", type=int, default=32)
    ap.add_argument("--last-n-blocks", type=int, default=12)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    assert torch.cuda.is_available(), "CUDA REQUIRED"
    device = "cuda"
    torch.backends.cuda.matmul.allow_tf32 = True
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    ckpt = torch.load(args.backbone, map_location="cpu", weights_only=False)
    cfg = ckpt["config"]
    print(f"[backbone] config={cfg}", flush=True)
    # build on CPU in bf16, load weights, then move/quantize to GPU
    model = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"], grad_ckpt=True)
    model = model.bfloat16()
    missing, unexpected = model.load_state_dict(ckpt["model"], strict=False)
    print(f"[backbone] missing={len(missing)} unexpected={len(unexpected)}", flush=True)
    block_size = cfg["block"]

    # inject LoRA on last-N mlp + 4-bit-quantize those bases; move whole model to GPU bf16.
    # NOTE: to fit 12GB the non-LoRA Linears would also need 4-bit; here we rely on
    # gradient-checkpointing + small block + the fact that bf16 7B (~14.5GB) is близко —
    # if OOM, raise --last-n-blocks coverage of 4-bit and shrink block further.
    # build on CPU (host RAM ~30GB); inject moves to GPU block-by-block + 4-bit-quantizes
    # mlp so the transient bf16 7B never co-resides on the 12GB GPU.
    n_lora, n_frozen4 = inject_lora(model, args.lora_r, args.lora_alpha, device, args.last_n_blocks)
    print(f"[lora] {n_lora} Linear4bitLoRA (last {args.last_n_blocks} blocks) + "
          f"{n_frozen4} Linear4bit frozen mlp", flush=True)
    # freeze everything except lora params
    for n, p in model.named_parameters():
        p.requires_grad_("lora_" in n)
    torch.cuda.empty_cache()
    n_train = sum(p.numel() for p in model.parameters() if p.requires_grad)
    n_total = sum(p.numel() for p in model.parameters())
    print(f"[model] total={n_total} trainable(lora)={n_train} block={block_size}", flush=True)
    print(f"[mem] alloc={torch.cuda.memory_allocated()/1e9:.2f}GB", flush=True)

    data = load_corpus(args.corpus)
    n = data.numel(); ntr = int(n * 0.95)
    train_data, val_data = data[:ntr], data[ntr:]
    print(f"[data] bytes={n} train={ntr} val={n-ntr}", flush=True)

    print("\n=== p7 BEFORE (backbone — anti-Goodhart control; MUST FAIL) ===", flush=True)
    before_eval = p7_eval(model, device, block_size, "backbone_before_finetune")
    print(before_eval["transcript"], flush=True)
    print(f"[before] {before_eval['verdict']} {before_eval['n_pass']}/5", flush=True)

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / args.warmup
        prog = (step - args.warmup) / max(1, args.steps - args.warmup)
        return args.lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

    curve = []; model.train(); t0 = time.time(); first_ce = None; last_ce = None
    for step in range(args.steps):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        opt.zero_grad(set_to_none=True)
        for _ in range(args.grad_accum):
            x, y = get_batch(train_data, block_size, args.batch, device)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                _, loss = model(x, y)
                loss = loss / args.grad_accum
            loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        opt.step()
        if step % args.eval_every == 0 or step == args.steps - 1:
            model.eval()
            with torch.no_grad():
                vx, vy = get_batch(val_data, block_size, args.batch, device)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, vloss = model(vx, vy)
            model.train()
            vce = float(vloss.item()); tr = float(loss.item()) * args.grad_accum
            if first_ce is None: first_ce = vce
            last_ce = vce
            dt = time.time() - t0
            curve.append({"step": step, "train_ce": tr, "val_ce": vce, "elapsed_s": round(dt, 1)})
            print(f"[step {step}] train_ce={tr:.5f} val_ce={vce:.5f} elapsed={dt:.0f}s "
                  f"mem={torch.cuda.max_memory_allocated()/1e9:.2f}GB", flush=True)

    total_dt = time.time() - t0
    ckpt_path = out / "anima_clm_chat_7b_qlora.pt"
    torch.save({"lora_state": {k: v for k, v in model.state_dict().items() if "lora_" in k},
                "config": cfg,
                "finetune": {"base": "dancinlab/clm-v1-ref-pytorch-cuda-7b", "mode": "qlora-4bit",
                             "lora_r": args.lora_r, "lora_alpha": args.lora_alpha,
                             "last_n_blocks": args.last_n_blocks, "steps": args.steps,
                             "lr": args.lr, "block": block_size}}, ckpt_path)
    sha = hashlib.sha256(open(ckpt_path, "rb").read()).hexdigest()
    print(f"[save] {ckpt_path} sha256={sha} bytes={os.path.getsize(ckpt_path)}", flush=True)

    print("\n=== p7 AFTER (qlora-finetuned 7B — should PASS) ===", flush=True)
    after_eval = p7_eval(model, device, block_size, "finetuned_7b_qlora")
    print(after_eval["transcript"], flush=True)
    print(f"[after] {after_eval['verdict']} {after_eval['n_pass']}/5", flush=True)

    summary = {
        "rung": "rung-7B (7.25B byte ByteGPT chat-finetune, 4-bit QLoRA $0 summer fallback)",
        "lane": "Lane-G/torch-cuda REFERENCE (a_lane_akida_gpu_split — NOT AKIDA)",
        "scope": "4-bit QLoRA chat-finetune of a descent-PASS (val CE 5.36->2.41, 400-step) "
                 "7B wiki backbone on RTX5070 12GB; backbone wiki-undertrained (a_scale_honest_scope)",
        "base_model": "dancinlab/clm-v1-ref-pytorch-cuda-7b",
        "corpus": "dancinlab/anima-chat-corpus-mix-70wiki-30dialogue",
        "params_total": n_total, "params_trainable_lora": n_train,
        "finetune_val_ce": {"first": first_ce, "last": last_ce},
        "wall_s": round(total_dt, 1), "ckpt_sha256": sha,
        "before_backbone": {"verdict": before_eval["verdict"], "n_pass": before_eval["n_pass"]},
        "after_finetune": {"verdict": after_eval["verdict"], "n_pass": after_eval["n_pass"]},
        "anti_goodhart_ok": (after_eval["verdict"] == "PASS" and before_eval["verdict"] == "FAIL"),
        "chat_pass": (after_eval["verdict"] == "PASS" and before_eval["verdict"] == "FAIL"),
    }
    (out / "p7_before.json").write_text(json.dumps(before_eval, ensure_ascii=False, indent=2))
    (out / "p7_after.json").write_text(json.dumps(after_eval, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    (out / "train_curve.json").write_text(json.dumps(curve, ensure_ascii=False, indent=2))
    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
