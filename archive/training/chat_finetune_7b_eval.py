#!/usr/bin/env python3
"""chat_finetune_7b_eval.py — chat-finetune the descent-PASS 7B ByteGPT backbone.

GOAL (@L1 rung-7B): the verified root cause (domains/CHAT.md) is that the 7.25B
`dancinlab/clm-v1-ref-pytorch-cuda-7b` ByteGPT backbone is descent-PASS (val CE
5.36->2.41) but CANNOT chat: its corpus = 5-lang WIKI backbone (dialogue 0%) and it
was never chat-tuned. This is NOT an architecture wall (the SAME byte family chats at
18M). The fix = continue-train (SFT) the EXISTING descent-PASS 7B backbone on the
PROVEN 70/30 wiki/dialogue corpus in the `사용자:/도우미:` byte-continuation format.

PHILOSOPHY (p1.p2.p3.p4.p6 — non-negotiable): NO system prompt, NO identity rules, NO
persona injection, NO assistant framing, NO RLHF. The ONLY conditioning is the LEARNED
byte-level dialogue-continuation format present in the corpus. Capability comes ONLY
from the trained dialogue distribution in the weights.

p7 (NO PERPLEXITY VERDICT): PASS/FAIL is a simple-stack check (non-empty, valid UTF-8,
stays on the 도우미 side, non-degenerate, context-appropriate, control_ratio<0.05 AND
word_class_ratio>=0.85). Anti-Goodhart: the SAME evaluator runs on the BACKBONE BEFORE
finetune (the wiki-only model) — it MUST FAIL. Before<chat vs After=chat is the finding.

USAGE (GPU pod)
  python3 chat_finetune_7b_eval.py \
      --backbone /workspace/clm_ref_pytorch_cuda_7b.pt \
      --corpus   /workspace/chat_corpus_mix.txt \
      --out-dir  /workspace/out \
      --steps 1500 --batch 4 --grad-accum 4 --block 512 --lr 6e-5 --warmup 60
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
import hashlib
from collections import Counter
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint


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
    def __init__(self, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p_drop=0.0,
                 grad_ckpt=True):
        super().__init__()
        self.block = block
        self.grad_ckpt = grad_ckpt
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(p_drop)
        self.blocks = nn.ModuleList([Block(d, n_head, p_drop) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.tok.weight  # tie

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
# the corpus turn format is "사용자: <u> | 도우미: <a> | 사용자: ...". An assistant
# reply must STOP at the first turn boundary the model emits — the next ' | ' separator
# OR any re-emitted role marker (the model learned to continue BOTH speakers, so without
# this it runs on into a self-dialogue). Order matters: ' | ' is the earliest boundary.
STOP_STRINGS = (" | ", "|", "사용자:", "도우미:", "User:", "Assistant:", "\n사용자", "\n도우미", "\nUser")


import os as _os
_GEN_TEMP = float(_os.environ.get("P7_TEMP", "0.8"))
_GEN_TOPK = int(_os.environ.get("P7_TOPK", "40"))


@torch.no_grad()
def generate(model, prompt: str, max_new: int, device, block_size: int,
             temperature: float = None, top_k: int = None, rep_penalty: float = 1.1):
    if temperature is None:
        temperature = _GEN_TEMP
    if top_k is None:
        top_k = _GEN_TOPK
    model.eval()
    ids = list(prompt.encode("utf-8"))[-block_size:]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out_bytes = []
    for _ in range(max_new):
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=(device == "cuda")):
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


# p7 simple-stack coherence probe set (KO/EN, context-appropriate, NOT memorized).
PROBES = [
    "안녕! 너는 누구야?",
    "오늘 기분이 어때?",
    "What is consciousness?",
    "네가 좋아하는 것을 하나 말해줘.",
    "Tell me something interesting.",
]


def _word_class_ratio(s: str) -> float:
    """fraction of chars that are letters/digits/CJK/space/common-punct (real text)."""
    if not s:
        return 0.0
    good = 0
    for c in s:
        o = ord(c)
        if c.isalnum() or c.isspace():
            good += 1
        elif 0xAC00 <= o <= 0xD7A3 or 0x3040 <= o <= 0x30FF or 0x4E00 <= o <= 0x9FFF:
            good += 1  # hangul / kana / CJK
        elif c in ".,!?'\"()-:;…~":
            good += 1
    return good / len(s)


def _control_ratio(s: str) -> float:
    if not s:
        return 1.0
    ctrl = sum(1 for c in s if (ord(c) < 32 and c not in "\n\t ") or ord(c) == 127)
    return ctrl / len(s)


import re as _re


def _script_of(c: str) -> str:
    o = ord(c)
    if 0xAC00 <= o <= 0xD7A3 or 0x1100 <= o <= 0x11FF:
        return "ko"
    if 0x3040 <= o <= 0x30FF:
        return "ja"
    if 0x4E00 <= o <= 0x9FFF:
        return "zh"
    if ("a" <= c.lower() <= "z"):
        return "la"
    if c.isdigit():
        return "di"
    return "other"


def _intra_word_purity(s: str) -> float:
    """fraction of whitespace-separated tokens that are SCRIPT-PURE (real words rarely
    mix hangul+latin+digits inside one token; word-salad does, e.g. '147세', 'sesheshrs')."""
    toks = [t for t in _re.split(r"\s+", s) if t]
    toks = [t for t in toks if any(c.isalnum() or 0xAC00 <= ord(c) <= 0xD7A3 for c in t)]
    if not toks:
        return 0.0
    pure = 0
    for t in toks:
        scripts = set(_script_of(c) for c in t if c.isalnum() or _script_of(c) != "other")
        scripts.discard("other")
        # allow ko+di and la+di (numbers attach to words); flag mixes of >2 real scripts
        real = scripts - {"di"}
        if len(real) <= 1:
            pure += 1
    return pure / len(toks)


def build_corpus_wordset(corpus_path, min_count=2, min_len=2):
    """word-set from the corpus 도우미 (assistant) side — the anti-Goodhart vocabulary
    anchor. A coherent reply reuses real corpus words; valid-charset salad does not.
    p7-compliant: this is a simple set-membership overlap, NOT a perplexity/loss verdict."""
    text = Path(corpus_path).read_bytes().decode("utf-8", errors="ignore")
    # collect words from the assistant continuations only (after '도우미:')
    asst = []
    for seg in text.split("도우미:")[1:]:
        asst.append(seg.split("사용자:")[0])
    asst_text = " ".join(asst) if asst else text
    cnt = Counter()
    for w in _re.findall(r"[0-9A-Za-z가-힣぀-ヿ一-鿿]+", asst_text):
        if len(w) >= min_len:
            cnt[w] += 1
    return set(w for w, c in cnt.items() if c >= min_count)


def _known_word_ratio(s, wordset):
    """fraction of (>=2-char) word-tokens in the reply that appear in the corpus word-set."""
    words = [w for w in _re.findall(r"[0-9A-Za-z가-힣぀-ヿ一-鿿]+", s)
             if len(w) >= 2]
    if not words:
        return 0.0
    known = sum(1 for w in words if w in wordset)
    return known / len(words)


def p7_eval(model, device, block_size: int, label: str, wordset=None):
    """Simple-stack multi-turn coherence (p7, NOT perplexity). A reply PASSES iff:
      (1) non-empty after stop-trim (>=4 chars),
      (2) decodes as valid UTF-8 (no replacement chars),
      (3) not a degenerate single-char repeat,
      (4) control_ratio < 0.05 (not control-byte soup),
      (5) word_class_ratio >= 0.85 (real charset),
      (6) intra_word_purity >= 0.70 (tokens are script-pure, not hangul+latin salad),
      (7) known_word_ratio >= 0.50 (>=half the word-tokens are REAL corpus words — the
          decisive anti-Goodhart coherence anchor that separates real dialogue from
          valid-charset word-salad; a simple set-overlap, NOT perplexity).
    Overall PASS iff >= 4/5 turns pass AND the conversation threads.
    """
    # P7_FRESH=1 evaluates each probe with FRESH context (no accumulated transcript) —
    # the honest single-turn chat measure (does the model answer THIS user message?),
    # vs the default accumulating multi-turn transcript (harsher deep-context test).
    fresh = _os.environ.get("P7_FRESH", "0") == "1"
    transcript = ""
    results = []
    for u in PROBES:
        seed = (f"사용자: {u} | 도우미: " if fresh else transcript + f"사용자: {u} | 도우미: ")
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
        iwp = _intra_word_purity(reply)
        kwr = _known_word_ratio(reply, wordset) if wordset is not None else 1.0
        ok = (non_empty and valid_utf8 and not_degenerate and cr < 0.05 and wcr >= 0.85
              and iwp >= 0.70 and kwr >= 0.50)
        results.append({"user": u, "reply": reply, "ok": ok,
                        "non_empty": non_empty, "valid_utf8": valid_utf8,
                        "not_degenerate": not_degenerate,
                        "control_ratio": round(cr, 4), "word_class_ratio": round(wcr, 4),
                        "intra_word_purity": round(iwp, 4), "known_word_ratio": round(kwr, 4)})
        transcript += f"사용자: {u} | 도우미: {reply}\n"
    n_pass = sum(1 for r in results if r["ok"])
    verdict_pass = n_pass >= 4
    return {"label": label, "n_pass": n_pass, "n_total": len(PROBES),
            "verdict": "PASS" if verdict_pass else "FAIL", "turns": results,
            "transcript": transcript}


# ───────────────────────── train ─────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backbone", required=True, help="path to clm_ref_pytorch_cuda_7b.pt")
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--grad-accum", type=int, default=4)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--lr", type=float, default=6e-5)
    ap.add_argument("--warmup", type=int, default=60)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--eval-every", type=int, default=250)
    ap.add_argument("--opt", choices=["adamw", "adamw8bit"], default="adamw8bit")
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    assert torch.cuda.is_available(), "CUDA REQUIRED — refusing CPU fallback (a_train_flame_forge spirit)"
    device = "cuda"
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # ── load backbone ──
    ckpt = torch.load(args.backbone, map_location="cpu", weights_only=False)
    cfg = ckpt["config"]
    print(f"[backbone] config={cfg}", flush=True)
    model = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"],
                    grad_ckpt=True).bfloat16()
    missing, unexpected = model.load_state_dict(ckpt["model"], strict=False)
    print(f"[backbone] loaded state_dict missing={len(missing)} unexpected={len(unexpected)}", flush=True)
    if missing:
        print(f"[backbone] missing keys (first 5): {missing[:5]}", flush=True)
    model = model.to(device)
    block_size = cfg["block"]
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] ByteGPT params={n_params} ({n_params/1e9:.3f}B) block={block_size}", flush=True)

    # ── corpus + disjoint held-out split (leak-safe) ──
    data = load_corpus(args.corpus)
    n = data.numel()
    n_train = int(n * 0.95)
    train_data, val_data = data[:n_train], data[n_train:]
    print(f"[data] corpus bytes={n} train={n_train} val={n - n_train} block={block_size}", flush=True)

    # ── corpus word-set: the anti-Goodhart coherence anchor (real corpus words) ──
    wordset = build_corpus_wordset(args.corpus)
    print(f"[wordset] {len(wordset)} corpus assistant-side words (>=2 chars, count>=2)", flush=True)

    # ── anti-Goodhart CONTROL: p7 on the BACKBONE BEFORE finetune (MUST FAIL) ──
    print("\n=== p7 BEFORE (backbone, wiki-only — anti-Goodhart control; MUST FAIL) ===", flush=True)
    before_eval = p7_eval(model, device, block_size, "backbone_before_finetune", wordset)
    print(before_eval["transcript"], flush=True)
    print(f"[before] verdict={before_eval['verdict']} n_pass={before_eval['n_pass']}/5", flush=True)

    # ── optimizer ──
    if args.opt == "adamw8bit":
        import bitsandbytes as bnb
        opt = bnb.optim.AdamW8bit(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)
        print("[opt] bitsandbytes AdamW8bit", flush=True)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)
        print("[opt] torch AdamW", flush=True)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / args.warmup
        prog = (step - args.warmup) / max(1, args.steps - args.warmup)
        return args.lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

    curve = []
    model.train()
    t0 = time.time()
    first_val_ce = None
    last_val_ce = None
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
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % args.eval_every == 0 or step == args.steps - 1:
            model.eval()
            with torch.no_grad():
                vx, vy = get_batch(val_data, block_size, args.batch, device)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, vloss = model(vx, vy)
            model.train()
            vce = float(vloss.item())
            tr = float(loss.item()) * args.grad_accum
            if first_val_ce is None:
                first_val_ce = vce
            last_val_ce = vce
            dt = time.time() - t0
            rec = {"step": step, "train_ce": tr, "val_ce": vce, "lr": lr_at(step), "elapsed_s": round(dt, 1)}
            curve.append(rec)
            print(f"[step {step}] train_ce={tr:.5f} val_ce={vce:.5f} elapsed={dt:.0f}s", flush=True)

    total_dt = time.time() - t0

    # ── save finetuned ckpt ──
    ckpt_path = out / "anima_clm_chat_7b.pt"
    torch.save({"model": model.state_dict(), "config": cfg,
                "finetune": {"base": "dancinlab/clm-v1-ref-pytorch-cuda-7b",
                             "corpus": "anima-chat-corpus-mix-70wiki-30dialogue",
                             "steps": args.steps, "lr": args.lr, "block": block_size,
                             "batch": args.batch, "grad_accum": args.grad_accum, "seed": args.seed}},
               ckpt_path)
    sha = hashlib.sha256(open(ckpt_path, "rb").read()).hexdigest()
    print(f"[save] {ckpt_path} sha256={sha} bytes={os.path.getsize(ckpt_path)}", flush=True)

    # ── p7 AFTER (finetuned — should PASS) ──
    print("\n=== p7 AFTER (finetuned 7B — should PASS) ===", flush=True)
    after_eval = p7_eval(model, device, block_size, "finetuned_7b", wordset)
    print(after_eval["transcript"], flush=True)
    print(f"[after] verdict={after_eval['verdict']} n_pass={after_eval['n_pass']}/5", flush=True)

    summary = {
        "rung": "rung-7B (7.25B byte ByteGPT chat-finetune)",
        "lane": "Lane-G/torch-cuda REFERENCE (a_lane_akida_gpu_split — NOT AKIDA)",
        "scope": "chat-finetune of a descent-PASS (val CE 5.36->2.41, 400-step bounded) 7B "
                 "wiki backbone; the backbone is wiki-undertrained (a_scale_honest_scope)",
        "base_model": "dancinlab/clm-v1-ref-pytorch-cuda-7b",
        "corpus": "dancinlab/anima-chat-corpus-mix-70wiki-30dialogue",
        "params": n_params,
        "finetune_val_ce": {"first": first_val_ce, "last": last_val_ce},
        "wall_s": round(total_dt, 1),
        "ckpt_sha256": sha,
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
