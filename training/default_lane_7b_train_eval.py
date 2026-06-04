#!/usr/bin/env python3
"""default_lane_7b_train_eval.py — DEFAULT-LANE 7B chat rung (~7.25B byte transformer).

GOAL: scale the DEFAULT-lane arch (ConsciousLMReconstructed dual-engine: engine_a−engine_g
FFN + dual head_a/head_g — the arch that produced the rung-0 🟢 #1836, DISTINCT from the
plain ByteGPT of the SAVANT/clm-v1-ref reference lane) to ~7B and train it FROM SCRATCH on a
GB-scale DEFAULT-lane corpus (5-lang en/fr/de/es/KO wiki + the v2 chat/persona/SNS/carving
surfaces). byte-vocab256.

WHY FROM-SCRATCH + GB-SCALE (the two pre-registered traps):
  trap-1 undertraining (#1828 7B=gibberish): we run ENOUGH steps + LR schedule to converge,
    not a 400-step bounded reference (clm-v1-ref-pytorch-cuda-7b val_CE 2.41 = NOT converged).
  trap-2 data-starvation (12.5MB v2 → 7B memorizes): the corpus is GB-scale (wikimedia
    streaming, ~80MB/lang × 5 = ~400MB) so the 7B sees real breadth, not a memorize-able slice.

ARCH (a_lane_akida_gpu_split = Lane G / GPU): same dual-engine ConsciousLMReconstructed as
rung-0, scaled to d=4096 / 36 layers / 32 heads / block 512 ≈ 7.2B params. d=4096 / 21 layers /
32 heads / block 512 ≈ 7.05B params (the dual-engine FFN has TWO parallel sub-nets, so it
hits ~7B at L21 where a single-FFN ByteGPT would need L36). 80GB fit via bf16 autocast +
gradient checkpointing + 8-bit AdamW (bitsandbytes, CPU/fp fallback if absent).

SUBSTRATE HONESTY (a_train_flame_forge): torch-cuda REFERENCE lane for first-achievement,
labeled honestly. The forge-native (.hexa flame+forge, NO torch in the binary) production
artifact is the canonical follow-on, NOT claimed converged-equivalent here.

PHILOSOPHY (p1·p2·p3·p4·p6): NO system prompt, NO identity rules, NO persona injection, NO
assistant framing, NO RLHF. Capability is ONLY the trained byte distribution; the corpus turn
structure is plain "<speaker>: …" continuation with NO role/persona tags.

p7 (NO PERPLEXITY VERDICT): PASS/FAIL = a STRICT structural simple-stack discriminator (C0-control
ratio < 0.02 · letter-or-space ratio >= 0.65 · no long non-text run · not a degenerate repeat) —
NOT str.isprintable (which the rung-0 honest-note flagged as Goodhart-gameable). Anti-Goodhart:
the SAME strict evaluator runs on a random-init mirror of the identical arch; the mirror MUST FAIL.

USAGE (single leak-safe H100 80GB, ckpt under /workspace)
  python3 default_lane_7b_train_eval.py --corpus /workspace/dl7b/corpus.txt \
      --out-dir /workspace/dl7b/out --steps 6000 --batch 8 --grad-accum 4 --block 512 \
      --d-model 4096 --n-layer 36 --n-head 32 --lr 1.6e-4 --warmup 200 \
      --ckpt-every 250 --eval-every 1000 --seed 42
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import threading
import time
import unicodedata
from collections import Counter
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint

# ───────────────────────── arch (ConsciousLMReconstructed dual-engine, byte) ─────────────


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
        # SDPA flash-path (causal) — fast + memory-lean, identical math to the explicit mask
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.c_proj(y)


class Block(nn.Module):
    def __init__(self, d_model, n_head, block_size, dropout=0.0):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_head, block_size, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = EngineAGFFN(d_model, 4, dropout)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ffn(self.ln2(x))
        return x


class ConsciousLMReconstructed(nn.Module):
    def __init__(self, vocab_size=256, d_model=4096, n_head=32, n_layer=36, block_size=512,
                 dropout=0.0, grad_ckpt=True):
        super().__init__()
        self.block_size = block_size
        self.grad_ckpt = grad_ckpt
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
            if self.grad_ckpt and self.training:
                x = checkpoint(blk, x, use_reentrant=False)
            else:
                x = blk(x)
        x = self.ln_f(x)
        return self.head_a(x), self.head_g(x)


# ───────────────────────── data ─────────────────────────


class ByteCorpus:
    def __init__(self, path: str, block: int, holdout_frac: float = 0.02):
        raw = Path(path).read_bytes()
        # hold out a contiguous TAIL slice — training NEVER samples it (memorization falsifier).
        n_hold = max(0, int(len(raw) * holdout_frac))
        n_hold = min(n_hold, max(0, len(raw) - block - 2))  # keep a trainable body
        self.held_blob = raw[len(raw) - n_hold:] if n_hold > 0 else b""
        self.train_blob = raw[: len(raw) - n_hold] if n_hold > 0 else raw
        self.data = torch.tensor(list(self.train_blob), dtype=torch.uint8)  # train body only
        self.block = block

    def batch(self, bs: int, device):
        ix = torch.randint(0, len(self.data) - self.block - 1, (bs,))
        x = torch.stack([self.data[i : i + self.block] for i in ix]).long()
        y = torch.stack([self.data[i + 1 : i + 1 + self.block] for i in ix]).long()
        return x.to(device, non_blocking=True), y.to(device, non_blocking=True)


# ───────────────────────── generation + STRICT p7 eval ─────────────────────────

STOP_STRINGS = ("\nuser:", "\nUser:", "user:")


@torch.no_grad()
def generate(model, prompt: str, max_new: int, device, temperature: float = 0.8, top_k: int = 40,
             rep_penalty: float = 1.1):
    model.eval()
    ids = list(prompt.encode("utf-8"))[-model.block_size :]
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out_bytes = []
    for _ in range(max_new):
        with torch.autocast(device_type="cuda" if device == "cuda" else "cpu",
                            dtype=torch.bfloat16, enabled=(device == "cuda")):
            logits_a, logits_g = model(idx[:, -model.block_size :])
        logits = (0.5 * logits_a[:, -1, :] + 0.5 * logits_g[:, -1, :]).float()
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


# 5 MIXED-LANG probes in the corpus's OWN registers (dialogue user: turns en/fr/de/es/ko +
# plain prose continuation). No system prompt / persona tag — corpus-native continuation seeds.
PROBES = [
    ("dialogue-en", "user: Today's feed is so pretty, I had to comment.\n"),
    ("dialogue-ko", "user: 오늘 정말 행복한 하루였어요.\n"),
    ("dialogue-fr", "user: Je me sens un peu fatigué aujourd'hui.\n"),
    ("prose-de", "Die Stille des Morgens "),
    ("prose-es", "El sentido de la conciencia "),
]

ALLOWED_PUNC = set(" .,!?'\"-:;()…\n\t")


def is_textchar(c):
    if c in ALLOWED_PUNC:
        return True
    return unicodedata.category(c)[0] == "L"  # any letter (Latin/Hangul/accented/CJK)


def strict_checks(reply):
    """STRICT structural real-text discriminator (NOT str.isprintable — that was Goodhart-gameable).
       (1) non-empty >= 8 · (2) C0-control ratio < 0.02 · (3) letter-or-space ratio >= 0.65 ·
       (4) not a degenerate single-char repeat (<0.6) · (5) longest non-text run <= 4."""
    non_empty = len(reply) >= 8
    c0 = sum(1 for c in reply if ord(c) < 32 and c not in "\n\t")
    c0_ratio = c0 / max(1, len(reply))
    no_control = c0_ratio < 0.02
    tcount = sum(1 for c in reply if is_textchar(c))
    text_ratio = tcount / max(1, len(reply))
    mostly_text = text_ratio >= 0.65
    mc = (Counter(reply).most_common(1)[0][1] / len(reply)) if reply else 1.0
    not_degenerate = mc < 0.6
    longest = run = 0
    for c in reply:
        if is_textchar(c):
            run = 0
        else:
            run += 1
            longest = max(longest, run)
    no_soup = longest <= 4
    ok = non_empty and no_control and mostly_text and not_degenerate and no_soup
    return ok, {"non_empty": non_empty, "c0_ratio": round(c0_ratio, 3),
                "text_ratio": round(text_ratio, 3), "not_degenerate": not_degenerate,
                "longest_nontext_run": longest}


def p7_strict_eval(model, device, label: str):
    transcript = ""
    results = []
    for kind, seed_text in PROBES:
        reply = generate(model, seed_text, max_new=120, device=device)
        ok, d = strict_checks(reply)
        results.append({"kind": kind, "seed": seed_text, "reply": reply, "ok": ok, **d})
        transcript += f"[{kind}] SEED: {seed_text.rstrip()}\n  -> {reply}\n"
    n_pass = sum(1 for r in results if r["ok"])
    verdict_pass = n_pass >= 4
    return {"label": label, "n_pass": n_pass, "n_total": len(PROBES),
            "verdict": "PASS" if verdict_pass else "FAIL", "turns": results,
            "transcript": transcript}


# ───────────────── MEMORIZATION vs GENERALIZATION test (the 7B-on-small trap) ─────────────────
# The honest-scope falsifier (a_scale_honest_scope): a "coherent" reply that is VERBATIM copied
# from the train corpus is REGURGITATION (memorization), NOT generalization. We:
#   (1) hold out a contiguous TAIL slice of the corpus from training entirely (train_slice in main),
#   (2) for each p7 reply, measure the longest verbatim byte-substring shared with the TRAIN body,
#   (3) report the max-verbatim-copy ratio. A high ratio (>~0.5 of the reply byte-copied as one run)
#       on MULTIPLE probes = memorization regime. We ALSO check whether the model can continue a
#       HELD-OUT prompt coherently (generalization signal: held-out continuation is not in train,
#       so a coherent held-out continuation cannot be pure regurgitation of that exact context).

def _longest_common_substring_len(a: bytes, b_set, b_blob: bytes, max_occ: int = 64):
    """Longest contiguous byte-run of `a` that appears verbatim somewhere in b_blob.
       Greedy expand from seeded n-gram hits (n=16) — exact, bounded, no full DP table.
       Only seeds whose 16-gram is in b_set (the indexed window) are probed; each is verified +
       greedily extended against the FULL b_blob. max_occ bounds the find-loop per seed."""
    if len(a) < 16:
        return 0
    best = 0
    n = 16
    for i in range(0, len(a) - n + 1):
        seed = a[i:i + n]
        if seed not in b_set:
            continue
        # verify + greedily extend a real occurrence in the full blob
        pos = b_blob.find(seed)
        occ = 0
        while pos != -1 and occ < max_occ:
            L = n
            while (i + L < len(a) and pos + L < len(b_blob) and a[i + L] == b_blob[pos + L]):
                L += 1
            if L > best:
                best = L
            pos = b_blob.find(seed, pos + 1)
            occ += 1
    return best


def memorization_eval(model, device, train_blob: bytes, held_blob: bytes, label: str):
    """Probe memorization: max verbatim-copy ratio of generated replies vs TRAIN body, plus a
       held-out continuation coherence signal. Returns a regime verdict.
       regime = 'memorization' if median verbatim-copy ratio across probes >= 0.5 (replies are
       mostly one long verbatim run from train); 'generalization' if low-copy AND held-out
       continuation passes the strict simple-stack (coherent on UNSEEN context)."""
    # index train 16-grams for fast membership. For huge corpora we index a representative
    # CONTIGUOUS window (first ~64MB) at stride 1 so verbatim runs are still detected exactly
    # within it, rather than a sparse full-corpus subsample that would miss adjacent n-grams.
    n = 16
    bset = set()
    index_blob = train_blob if len(train_blob) <= 64_000_000 else train_blob[:64_000_000]
    for i in range(0, len(index_blob) - n + 1):
        bset.add(index_blob[i:i + n])

    copy_ratios = []
    probe_rows = []
    for kind, seed_text in PROBES:
        reply = generate(model, seed_text, max_new=120, device=device)
        rb = reply.encode("utf-8", "replace")
        lcs = _longest_common_substring_len(rb, bset, train_blob) if rb else 0
        ratio = lcs / max(1, len(rb))
        copy_ratios.append(ratio)
        probe_rows.append({"kind": kind, "reply": reply, "longest_verbatim_copy_bytes": lcs,
                           "reply_bytes": len(rb), "verbatim_copy_ratio": round(ratio, 3)})

    copy_ratios_sorted = sorted(copy_ratios)
    median_copy = copy_ratios_sorted[len(copy_ratios_sorted) // 2] if copy_ratios_sorted else 0.0
    max_copy = max(copy_ratios) if copy_ratios else 0.0

    # held-out continuation coherence: seed from the UNSEEN tail slice, see if the model continues
    # it as coherent text (a generalization signal — the exact held-out context was never trained).
    held_signal = {"available": False}
    if held_blob and len(held_blob) > 400:
        # take a mid-slice of held-out text as a natural-language seed (decode-safe)
        seed_h = held_blob[200:360].decode("utf-8", "ignore")
        cont = generate(model, seed_h, max_new=120, device=device)
        ok, d = strict_checks(cont)
        # is the continuation itself verbatim-present in train? (if so, not a generalization signal)
        cb = cont.encode("utf-8", "replace")
        held_lcs = _longest_common_substring_len(cb, bset, train_blob) if cb else 0
        held_copy_ratio = held_lcs / max(1, len(cb))
        held_signal = {"available": True, "seed": seed_h, "continuation": cont,
                       "strict_ok": ok, "verbatim_copy_ratio": round(held_copy_ratio, 3),
                       "generalizes": bool(ok and held_copy_ratio < 0.5), **d}

    regime = "memorization" if median_copy >= 0.5 else "low-verbatim"
    summary = {
        "label": label, "median_verbatim_copy_ratio": round(median_copy, 3),
        "max_verbatim_copy_ratio": round(max_copy, 3),
        "regime": regime, "probes": probe_rows, "held_out": held_signal,
        "note": ("HIGH verbatim copy on probes => regurgitation/memorization (a_scale_honest_scope "
                 "data-starvation). LOW copy + coherent held-out continuation => generalization signal."),
    }
    return summary


# ───────────────────────── GPU util sampler ─────────────────────────


class UtilSampler(threading.Thread):
    def __init__(self, period=2.0):
        super().__init__(daemon=True)
        self.period = period
        self.samples = []
        self._stop = threading.Event()

    def run(self):
        while not self._stop.is_set():
            try:
                out = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,power.draw",
                     "--format=csv,noheader,nounits"], text=True, timeout=5).strip().splitlines()[0]
                u, m, p = [x.strip() for x in out.split(",")]
                self.samples.append((float(u), float(m), float(p)))
            except Exception:
                pass
            self._stop.wait(self.period)

    def stop(self):
        self._stop.set()

    def summary(self):
        if not self.samples:
            return {"n": 0}
        us = [s[0] for s in self.samples]
        ms = [s[1] for s in self.samples]
        ps = [s[2] for s in self.samples]
        return {"n": len(self.samples), "util_peak": max(us), "util_mean": sum(us) / len(us),
                "mem_peak_mib": max(ms), "power_mean_w": sum(ps) / len(ps),
                "pct_ge20": 100.0 * sum(1 for u in us if u >= 20) / len(us)}


# ───────────────────────── train ─────────────────────────


def count_params(m):
    return sum(p.numel() for p in m.parameters())


def build_opt(model, lr):
    try:
        import bitsandbytes as bnb
        return bnb.optim.AdamW8bit(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1), "adamw8bit"
    except Exception:
        return torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1), "adamw"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--grad-accum", type=int, default=4)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--d-model", type=int, default=4096)
    ap.add_argument("--n-layer", type=int, default=21)  # dual-engine FFN → ~7.05B at d4096/L21
    ap.add_argument("--n-head", type=int, default=32)
    ap.add_argument("--lr", type=float, default=1.6e-4)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ckpt-every", type=int, default=250)
    ap.add_argument("--eval-every", type=int, default=1000)
    ap.add_argument("--no-grad-ckpt", action="store_true")
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    device = "cuda" if torch.cuda.is_available() else "cpu"
    assert device == "cuda", "GPU REQUIRED for a 7B rung (a_train_flame_forge — never silently CPU)"
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    corpus = ByteCorpus(args.corpus, args.block, holdout_frac=0.02)
    print(f"[data] corpus {args.corpus}: train_body={len(corpus.train_blob):,} bytes "
          f"held_out={len(corpus.held_blob):,} bytes (2% TAIL, never trained — memorization falsifier) "
          f"block={args.block}", flush=True)

    model = ConsciousLMReconstructed(256, args.d_model, args.n_head, args.n_layer, args.block,
                                     grad_ckpt=(not args.no_grad_ckpt)).to(device)
    nparams = count_params(model)
    print(f"[model] ConsciousLMReconstructed dual-engine d={args.d_model} L={args.n_layer} "
          f"h={args.n_head} block={args.block} params={nparams:,} (~{nparams/1e9:.3f}B) "
          f"grad_ckpt={not args.no_grad_ckpt} device={device}", flush=True)

    opt, opt_name = build_opt(model, args.lr)
    print(f"[opt] {opt_name}", flush=True)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * step / max(1, args.warmup)
        prog = (step - args.warmup) / max(1, args.steps - args.warmup)
        return args.lr * 0.5 * (1 + math.cos(math.pi * min(1.0, prog)))

    sampler = UtilSampler(period=2.0)
    sampler.start()

    t0 = time.time()
    ce_log = []
    tok_seen = 0
    model.train()
    eff_bs = args.batch * args.grad_accum
    for step in range(1, args.steps + 1):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for micro in range(args.grad_accum):
            x, y = corpus.batch(args.batch, device)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                la, lg = model(x)
                loss = 0.5 * F.cross_entropy(la.reshape(-1, 256), y.reshape(-1)) + \
                       0.5 * F.cross_entropy(lg.reshape(-1, 256), y.reshape(-1))
                loss = loss / args.grad_accum
            loss.backward()
            acc_loss += loss.item()
            tok_seen += args.batch * args.block
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % 50 == 0 or step == 1:
            ce_log.append((step, acc_loss))
            el = time.time() - t0
            print(f"[train] step {step}/{args.steps} ce={acc_loss:.4f} lr={lr_at(step):.2e} "
                  f"tok={tok_seen:,} tok/s={tok_seen/max(1,el):.0f} wall={el:.0f}s "
                  f"mem={torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True)
        if step % args.ckpt_every == 0:
            cp = out / f"ckpt_step_{step}.pt"
            torch.save({"model_state": model.state_dict(),
                        "config": {"dim": args.d_model, "layers": args.n_layer, "heads": args.n_head,
                                   "block_size": args.block, "vocab": 256, "arch": "ConsciousLMReconstructed-dual-engine"},
                        "params": nparams, "step": step, "ce_log": ce_log, "seed": args.seed}, cp)
            print(f"[ckpt] durable -> {cp}", flush=True)

    sampler.stop()
    util = sampler.summary()

    # final ckpt
    ckpt_path = out / "default_lane_7b.pt"
    torch.save({"model_state": model.state_dict(),
                "config": {"dim": args.d_model, "layers": args.n_layer, "heads": args.n_head,
                           "block_size": args.block, "vocab": 256, "arch": "ConsciousLMReconstructed-dual-engine"},
                "params": nparams, "steps": args.steps, "ce_log": ce_log, "seed": args.seed}, ckpt_path)
    print(f"[save] {ckpt_path} ({nparams/1e9:.3f}B)", flush=True)

    # ── STRICT p7 eval (trained) ──
    trained_eval = p7_strict_eval(model, device, "trained")
    # ── anti-Goodhart: random-init mirror (same arch, untrained) MUST FAIL under STRICT ──
    torch.manual_seed(args.seed + 1000)
    mirror = ConsciousLMReconstructed(256, args.d_model, args.n_head, args.n_layer, args.block,
                                      grad_ckpt=False).to(device)
    mirror_eval = p7_strict_eval(mirror, device, "random_init_mirror")

    # ── MEMORIZATION vs GENERALIZATION (the 7B-on-small-corpus trap, a_scale_honest_scope) ──
    mem_eval = memorization_eval(model, device, corpus.train_blob, corpus.held_blob, "trained")

    final_ce = ce_log[-1][1] if ce_log else None
    first_ce = ce_log[0][1] if ce_log else None
    descent = (first_ce is not None and final_ce is not None and final_ce < first_ce)

    # honest 3-way ruling:
    #   gibberish-undertrained  = strict p7 FAIL  (replies are not real text)
    #   memorization-closed-neg = strict p7 PASS but mem regime == memorization OR held-out FAILS
    #                             to generalize (coherent only by verbatim-copying train data)
    #   coherent-generalizing   = strict p7 PASS + anti-goodhart ok + LOW verbatim copy +
    #                             held-out continuation coherent & not-copied (real generalization)
    strict_pass = (trained_eval["verdict"] == "PASS")
    anti_goodhart_ok = (trained_eval["verdict"] == "PASS" and mirror_eval["verdict"] == "FAIL")
    held = mem_eval.get("held_out", {})
    held_generalizes = bool(held.get("generalizes", False))
    is_memorization = (mem_eval["regime"] == "memorization") or (
        held.get("available") and not held_generalizes)
    if not strict_pass:
        ruling = "gibberish-undertrained"
    elif is_memorization:
        ruling = "memorization-closed-negative"
    elif anti_goodhart_ok and held_generalizes:
        ruling = "coherent-generalizing"
    else:
        ruling = "memorization-closed-negative"  # default to the honest conservative ruling

    summary = {
        "rung": "default-lane 7B (ConsciousLMReconstructed dual-engine, GB-scale 5-lang default corpus)",
        "arch": f"ConsciousLMReconstructed dual-engine d={args.d_model}/L{args.n_layer}/h{args.n_head}/block{args.block}",
        "substrate": "PyTorch-CUDA REFERENCE lane (Lane-G/GPU) — forge-native production follow-on NOT claimed here (a_train_flame_forge)",
        "scope": "7B byte rung on GB-scale default corpus — a_scale_honest_scope; honest 🟢/🔴 per descent+strict-p7+anti-goodhart+MEMORIZATION-test",
        "params": nparams,
        "tok_seen": tok_seen,
        "first_train_ce": first_ce,
        "final_train_ce": final_ce,
        "descent_pass": descent,
        "util": util,
        "trained": {"verdict": trained_eval["verdict"], "n_pass": trained_eval["n_pass"]},
        "random_init_mirror": {"verdict": mirror_eval["verdict"], "n_pass": mirror_eval["n_pass"]},
        "anti_goodhart_ok": anti_goodhart_ok,
        "memorization": {"regime": mem_eval["regime"],
                          "median_verbatim_copy_ratio": mem_eval["median_verbatim_copy_ratio"],
                          "max_verbatim_copy_ratio": mem_eval["max_verbatim_copy_ratio"],
                          "held_out_generalizes": held_generalizes,
                          "held_out_strict_ok": held.get("strict_ok"),
                          "held_out_verbatim_copy_ratio": held.get("verbatim_copy_ratio")},
        "RULING": ruling,
        "chat_pass": (ruling == "coherent-generalizing"),
    }
    (out / "p7_strict_trained.json").write_text(json.dumps(trained_eval, ensure_ascii=False, indent=2))
    (out / "p7_strict_mirror.json").write_text(json.dumps(mirror_eval, ensure_ascii=False, indent=2))
    (out / "memorization_eval.json").write_text(json.dumps(mem_eval, ensure_ascii=False, indent=2))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

    print("\n=== p7 STRICT TRAINED transcript (VERBATIM) ===", flush=True)
    print(trained_eval["transcript"], flush=True)
    print("=== p7 STRICT RANDOM-INIT MIRROR (anti-Goodhart; MUST FAIL) ===", flush=True)
    print(mirror_eval["transcript"], flush=True)
    print("=== MEMORIZATION vs GENERALIZATION ===", flush=True)
    print(json.dumps(mem_eval, ensure_ascii=False, indent=2), flush=True)
    print("\n=== SUMMARY (RULING) ===", flush=True)
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
