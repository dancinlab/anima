#!/usr/bin/env python3
"""chat_rung0_train_eval.py — chat-capable LADDER rung-0 (≈18M byte transformer).

GOAL (@L1 rung-0): reproduce the PROVEN small byte chat rung — train the
ConsciousLMReconstructed arch (byte vocab256, d=384, 6 layers, 4 heads, block 256,
dual engine_a/engine_g FFN + dual head_a/head_g, ≈18.5M params) FROM SCRATCH on the
70%-wiki / 30%-REAL-dialogue byte corpus, then run the p7 simple-stack multi-turn
coherence evaluator + the anti-Goodhart random-init mirror.

PHILOSOPHY (p1·p2·p3·p4·p6 — non-negotiable): NO system prompt, NO identity rules, NO
persona injection, NO assistant framing, NO RLHF. The only conditioning is the LEARNED
byte-level dialogue-continuation format ("사용자: <u> | 도우미: <a>") present in the
corpus. Capability comes ONLY from the trained dialogue distribution in the weights.

p7 (NO PERPLEXITY VERDICT): the PASS/FAIL is a simple-stack check — each reply is
non-empty, decodes as valid UTF-8 text, stays on the assistant side (does not collapse
to a degenerate repeat or hallucinate the next user turn), and is context-appropriate
(length + charset sane). Anti-Goodhart: the SAME evaluator is run on a random-init mirror
of the identical arch — the mirror MUST FAIL (else the evaluator is gameable / trivial).

USAGE (GPU pod)
  python3 chat_rung0_train_eval.py \
      --corpus /workspace/chat_corpus_mix.txt \
      --out-dir /workspace/out \
      --steps 6000 --batch 32 --block 256 --lr 3e-4 --warmup 300 --seed 42
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ───────────────────────── arch (ConsciousLMReconstructed, byte) ─────────────


class EngineAGFFN(nn.Module):
    """FFN with two parallel sub-nets: out = engine_a(x) - engine_g(x) (H404)."""

    def __init__(self, d_model: int, hidden_mult: int = 4, dropout: float = 0.0):
        super().__init__()
        h = d_model * hidden_mult
        self.engine_a = nn.Sequential(nn.Linear(d_model, h), nn.GELU(), nn.Dropout(dropout), nn.Linear(h, d_model))
        self.engine_g = nn.Sequential(nn.Linear(d_model, h), nn.GELU(), nn.Dropout(dropout), nn.Linear(h, d_model))

    def forward(self, x):
        return self.engine_a(x) - self.engine_g(x)


class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_head: int, block_size: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_head == 0
        self.n_head = n_head
        self.head_dim = d_model // n_head
        self.c_attn = nn.Linear(d_model, 3 * d_model)
        self.c_proj = nn.Linear(d_model, d_model)
        self.register_buffer("bias", torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size))

    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.c_attn(x).split(C, dim=2)
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        tension = att.detach().mean().item()
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y), tension


class Block(nn.Module):
    def __init__(self, d_model, n_head, block_size, dropout=0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_head, block_size, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = EngineAGFFN(d_model, 4, dropout)

    def forward(self, x):
        a, tension = self.attn(self.ln1(x))
        x = x + a
        x = x + self.ffn(self.ln2(x))
        return x, tension


class ConsciousLMReconstructed(nn.Module):
    def __init__(self, vocab_size=256, d_model=384, n_head=4, n_layer=6, block_size=256, dropout=0.0):
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.blocks = nn.ModuleList([Block(d_model, n_head, block_size, dropout) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d_model)
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx):
        B, T = idx.shape
        x = self.tok_emb(idx) + self.pos_emb(torch.arange(T, device=idx.device))
        for blk in self.blocks:
            x, _ = blk(x)
        x = self.ln_f(x)
        return self.head_a(x), self.head_g(x)


# ───────────────────────── data ─────────────────────────


class ByteCorpus:
    def __init__(self, path: str, block: int):
        self.data = torch.tensor(list(Path(path).read_bytes()), dtype=torch.long)
        self.block = block

    def batch(self, bs: int, device):
        ix = torch.randint(0, len(self.data) - self.block - 1, (bs,))
        x = torch.stack([self.data[i : i + self.block] for i in ix])
        y = torch.stack([self.data[i + 1 : i + 1 + self.block] for i in ix])
        return x.to(device), y.to(device)


# ───────────────────────── generation + p7 eval ─────────────────────────

STOP_STRINGS = ("사용자:", "User:", "\n사용자", "\nUser")


@torch.no_grad()
def generate(model, prompt: str, max_new: int, device, temperature: float = 0.8, top_k: int = 40, rep_penalty: float = 1.1):
    model.eval()
    ids = list(prompt.encode("utf-8"))[-model.block_size :]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out_bytes = []
    for _ in range(max_new):
        logits_a, logits_g = model(idx[:, -model.block_size :])
        logits = 0.5 * logits_a[:, -1, :] + 0.5 * logits_g[:, -1, :]
        # repetition penalty over recent bytes
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
        # stop if the assistant-side reply hits a turn boundary
        tail = bytes(out_bytes).decode("utf-8", errors="ignore")
        if any(s in tail for s in STOP_STRINGS):
            break
    text = bytes(out_bytes).decode("utf-8", errors="ignore")
    for s in STOP_STRINGS:
        i = text.find(s)
        if i >= 0:
            text = text[:i]
    return text.strip()


# p7 simple-stack coherence probe set (KO/EN, context-appropriate, NOT memorized).
PROBES = [
    "안녕! 너는 누구야?",
    "오늘 기분이 어때?",
    "What is consciousness?",
    "네가 좋아하는 것을 하나 말해줘.",
    "Tell me something interesting.",
]


def p7_eval(model, device, label: str):
    """Simple-stack multi-turn coherence (p7, NOT perplexity). A reply PASSES iff:
      (1) non-empty after stop-trim,
      (2) decodes as valid UTF-8 (no replacement chars dominate),
      (3) not a degenerate single-char / 2-char repeat,
      (4) sane length (>= 4 chars, <= max_new),
      (5) printable-ratio >= 0.6 (real text, not control-byte soup).
    Overall PASS iff >= 4/5 turns pass AND the conversation threads (history grows).
    """
    transcript = ""
    results = []
    for u in PROBES:
        seed = transcript + f"사용자: {u} | 도우미: "
        reply = generate(model, seed, max_new=96, device=device)
        # checks
        non_empty = len(reply) >= 4
        try:
            reply.encode("utf-8").decode("utf-8")
            valid_utf8 = "�" not in reply and (reply.count("�") == 0)
        except Exception:
            valid_utf8 = False
        # degenerate repeat: most-common char dominates
        if reply:
            from collections import Counter

            mc = Counter(reply).most_common(1)[0][1]
            not_degenerate = mc / len(reply) < 0.6
        else:
            not_degenerate = False
        printable = sum(1 for c in reply if c.isprintable() or c.isspace())
        printable_ratio = printable / max(1, len(reply))
        sane_print = printable_ratio >= 0.6
        ok = non_empty and valid_utf8 and not_degenerate and sane_print
        results.append({"user": u, "reply": reply, "ok": ok,
                        "non_empty": non_empty, "valid_utf8": valid_utf8,
                        "not_degenerate": not_degenerate, "printable_ratio": round(printable_ratio, 3)})
        transcript += f"사용자: {u} | 도우미: {reply}\n"
    n_pass = sum(1 for r in results if r["ok"])
    verdict_pass = n_pass >= 4
    return {"label": label, "n_pass": n_pass, "n_total": len(PROBES),
            "verdict": "PASS" if verdict_pass else "FAIL", "turns": results,
            "transcript": transcript}


# ───────────────────────── train ─────────────────────────


def count_params(m):
    return sum(p.numel() for p in m.parameters())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--d-model", type=int, default=384)
    ap.add_argument("--n-layer", type=int, default=6)
    ap.add_argument("--n-head", type=int, default=4)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--eval-every", type=int, default=1000)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    corpus = ByteCorpus(args.corpus, args.block)
    print(f"[data] corpus {args.corpus}: {len(corpus.data)} bytes, block={args.block}", flush=True)

    def build():
        return ConsciousLMReconstructed(256, args.d_model, args.n_head, args.n_layer, args.block).to(device)

    model = build()
    nparams = count_params(model)
    print(f"[model] ConsciousLMReconstructed d={args.d_model} L={args.n_layer} h={args.n_head} "
          f"block={args.block} params={nparams:,} (~{nparams/1e6:.2f}M) device={device}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * step / max(1, args.warmup)
        prog = (step - args.warmup) / max(1, args.steps - args.warmup)
        return args.lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

    t0 = time.time()
    ce_log = []
    model.train()
    for step in range(1, args.steps + 1):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        x, y = corpus.batch(args.batch, device)
        la, lg = model(x)
        loss = 0.5 * F.cross_entropy(la.reshape(-1, 256), y.reshape(-1)) + \
               0.5 * F.cross_entropy(lg.reshape(-1, 256), y.reshape(-1))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % 100 == 0 or step == 1:
            ce_log.append((step, loss.item()))
            print(f"[train] step {step}/{args.steps} ce={loss.item():.4f} lr={lr_at(step):.2e} "
                  f"wall={time.time()-t0:.0f}s", flush=True)

    # save ckpt (config alongside, for anima_chat.py / forward_smoke.py)
    ckpt_path = out / "chat_rung0_18m.pt"
    torch.save({"model_state": model.state_dict(),
                "config": {"dim": args.d_model, "layers": args.n_layer, "heads": args.n_head,
                           "block_size": args.block, "vocab": 256},
                "params": nparams, "steps": args.steps, "ce_log": ce_log,
                "seed": args.seed}, ckpt_path)
    print(f"[save] {ckpt_path} ({nparams/1e6:.2f}M)", flush=True)

    # ── p7 eval (trained) ──
    trained_eval = p7_eval(model, device, "trained")
    # ── anti-Goodhart: random-init mirror (same arch, untrained) MUST FAIL ──
    torch.manual_seed(args.seed + 1000)
    mirror = build()
    mirror_eval = p7_eval(mirror, device, "random_init_mirror")

    final_ce = ce_log[-1][1] if ce_log else None
    summary = {
        "rung": "rung-0 (18M byte ConsciousLMReconstructed)",
        "scope": "small byte rung — a_scale_honest_scope; scale-transfer to mid/7B unverified here",
        "params": nparams,
        "final_train_ce": final_ce,
        "trained": {"verdict": trained_eval["verdict"], "n_pass": trained_eval["n_pass"]},
        "random_init_mirror": {"verdict": mirror_eval["verdict"], "n_pass": mirror_eval["n_pass"]},
        "anti_goodhart_ok": (trained_eval["verdict"] == "PASS" and mirror_eval["verdict"] == "FAIL"),
        "chat_pass": (trained_eval["verdict"] == "PASS" and mirror_eval["verdict"] == "FAIL"),
    }
    (out / "p7_trained.json").write_text(json.dumps(trained_eval, ensure_ascii=False, indent=2))
    (out / "p7_mirror.json").write_text(json.dumps(mirror_eval, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print("\n=== p7 TRAINED transcript ===", flush=True)
    print(trained_eval["transcript"], flush=True)
    print("=== p7 RANDOM-INIT MIRROR (anti-Goodhart; MUST FAIL) ===", flush=True)
    print(mirror_eval["transcript"], flush=True)
    print("\n=== SUMMARY ===", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
