#!/usr/bin/env python3
"""anima simple stack exhaustive test (own 18) — 2026-05-06

raw#37 transient_py opt-out (smoke script, $0 mac local).

Tests untested anima models via simple stack (own 18):
  C1 KO (3 prompts): 안녕하세요, 한국어 가능?, 사용자: 안녕하세요\n도우미:
  C1 EN (3 prompts): Hello how are you?, What is consciousness?, User: Hi\nAssistant:
  C2     (3 prompts): Once upon a time, Q:, "" (empty)

Models tested (in scope):
  - 5 local BG-FK variants (clm_v2_tiny/small/medium/base/clm_v2) — ConsciousLM++ (ca_rules+gate)
  - v14_128c (post tar.zst extract) — ConsciousLM-shape

Strategies: greedy + temp=0.7 top_k=40 + temp=0.5 top_k=40 + temp=0.3 top_k=80
"""
import argparse
import json
import math
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F


# =================================================================
# ConsciousLM (vanilla) — derived from /tmp/anima_v2_source/conscious_lm.py
# =================================================================
class PureFieldFFN_v0(nn.Module):
    def __init__(self, d_model, dropout=0.37):
        super().__init__()
        d_inner = 4 * d_model
        self.engine_a = nn.Sequential(
            nn.Linear(d_model, d_inner),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_inner, d_model),
        )
        self.engine_g = nn.Sequential(
            nn.Linear(d_model, d_inner),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_inner, d_model),
        )

    def forward(self, x):
        a = self.engine_a(x)
        g = self.engine_g(x)
        out = a - g
        return out


class CausalSelfAttention_v0(nn.Module):
    def __init__(self, d_model, n_head, block_size, dropout=0.37):
        super().__init__()
        self.c_attn = nn.Linear(d_model, 3 * d_model)
        self.c_proj = nn.Linear(d_model, d_model)
        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)
        self.n_head = n_head
        self.d_model = d_model
        self.head_dim = d_model // n_head
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size),
        )

    def forward(self, x):
        B, T, D = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.d_model, dim=2)
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, D)
        y = self.resid_dropout(self.c_proj(y))
        return y


class ConsciousLM_v0(nn.Module):
    """Vanilla ConsciousLM (matches checkpoints WITHOUT ca_rules)."""
    def __init__(self, vocab_size=256, d_model=384, n_head=4, n_layer=6, block_size=256, dropout=0.37):
        super().__init__()
        self.block_size = block_size
        self.vocab_size = vocab_size
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.drop = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([
            self._make_block(d_model, n_head, block_size, dropout) for _ in range(n_layer)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)
        self.tok_emb.weight = self.head_a.weight

    def _make_block(self, d_model, n_head, block_size, dropout):
        block = nn.Module()
        block.ln1 = nn.LayerNorm(d_model)
        block.attn = CausalSelfAttention_v0(d_model, n_head, block_size, dropout)
        block.ln2 = nn.LayerNorm(d_model)
        block.ffn = PureFieldFFN_v0(d_model, dropout)
        block.forward = lambda x, b=block: x + b.attn(b.ln1(x)) + (lambda y: b.ffn(b.ln2(y)))(x + b.attn(b.ln1(x)))
        # Override forward properly via nn.Sequential-style:
        return block

    def forward(self, idx):
        B, T = idx.size()
        tok = self.tok_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = self.drop(tok + pos)
        for block in self.blocks:
            # standard pre-norm transformer
            x = x + block.attn(block.ln1(x))
            x = x + block.ffn(block.ln2(x))
        x = self.ln_f(x)
        logits_a = self.head_a(x)
        logits_g = self.head_g(x)
        return logits_a, logits_g


# =================================================================
# ConsciousLM++ — adds ca_rules + tension_proj + ln_ca + ca_mix
# Per BG-FK checkpoint inspection
# =================================================================
class ConsciousBlockPlus(nn.Module):
    """ConsciousLM++ block with cellular automata rules + ca_mix gate."""

    def __init__(self, d_model, n_head, block_size, dropout=0.37, n_rules=8):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention_v0(d_model, n_head, block_size, dropout)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = PureFieldFFN_v0(d_model, dropout)
        # CA rules
        self.ln_ca = nn.LayerNorm(d_model)
        self.rules = nn.ModuleList([nn.Linear(d_model, d_model, bias=False) for _ in range(n_rules)])
        self.rule_weights = nn.Linear(d_model, n_rules)
        # ca_mix takes [x, attn_out, ffn_out] (3*d_model) -> d_model gate
        self.ca_mix = nn.Linear(3 * d_model, d_model, bias=False)

    def forward(self, x):
        # standard pre-norm self-attn + FFN
        a = self.attn(self.ln1(x))
        x_post_attn = x + a
        f = self.ffn(self.ln2(x_post_attn))
        x_post_ffn = x_post_attn + f

        # CA rules path (additive residual via ca_mix gate)
        ca_in = self.ln_ca(x_post_ffn)
        rule_logits = self.rule_weights(ca_in)  # (B,T,n_rules)
        rule_w = F.softmax(rule_logits, dim=-1)
        rule_outs = torch.stack([rule(ca_in) for rule in self.rules], dim=-2)  # (B,T,R,D)
        ca_out = (rule_w.unsqueeze(-1) * rule_outs).sum(dim=-2)  # (B,T,D)

        # Mix: combine [x_post_ffn, a, f] via ca_mix
        mix_in = torch.cat([x_post_ffn, a, f], dim=-1)
        gate = torch.sigmoid(self.ca_mix(mix_in))
        x_out = x_post_ffn + gate * ca_out
        return x_out


class ConsciousLMPlus(nn.Module):
    """ConsciousLM++ — vocab=256 byte-level + ca_rules+ca_mix+tension_proj."""

    def __init__(self, vocab_size=256, d_model=384, n_head=4, n_layer=6,
                 block_size=128, dropout=0.0, n_rules=8):
        super().__init__()
        self.block_size = block_size
        self.vocab_size = vocab_size
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(block_size, d_model)
        self.drop = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([
            ConsciousBlockPlus(d_model, n_head, block_size, dropout, n_rules)
            for _ in range(n_layer)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)
        # tension_proj shape [d_model, 1] = Linear(1, d_model) — projects scalar tension into d_model
        # Not used in our forward path (monitoring only); just allocate for state_dict load.
        self.tension_proj = nn.Linear(1, d_model, bias=False)

    def forward(self, idx):
        B, T = idx.size()
        tok = self.tok_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = self.drop(tok + pos)
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        logits_a = self.head_a(x)
        logits_g = self.head_g(x)
        return logits_a, logits_g


# =================================================================
# Model loading
# =================================================================
def load_conscious_lm_plus(ckpt_path, device="cpu"):
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    config = ckpt.get("config", {})
    sd = ckpt.get("model_state", ckpt)

    model = ConsciousLMPlus(
        vocab_size=config.get("vocab_size", 256),
        d_model=config.get("dim", 384),
        n_head=config.get("heads", 4),
        n_layer=config.get("layers", 6),
        block_size=config.get("block_size", 128),
        dropout=0.0,  # eval mode
        n_rules=config.get("ca_rules", 8),
    )

    # Strip 'attn.bias' which is a registered buffer (causal mask) — already in model
    # Load
    info = model.load_state_dict(sd, strict=False)
    return model, config, info


def load_conscious_lm_v0(ckpt_path, device="cpu"):
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    if isinstance(ckpt, dict) and "model_state" in ckpt:
        sd = ckpt["model_state"]
        config = ckpt.get("config", {})
    else:
        sd = ckpt
        config = {}

    # Derive arch from state_dict shapes
    tok_emb_shape = None
    for k, v in sd.items():
        if k == "tok_emb.weight":
            tok_emb_shape = v.shape
            break
    vocab_size = tok_emb_shape[0] if tok_emb_shape is not None else 256
    d_model = tok_emb_shape[1] if tok_emb_shape is not None else 384

    # Count layers
    n_layer = 0
    for k in sd.keys():
        m = re.match(r"blocks\.(\d+)\.", k)
        if m:
            n_layer = max(n_layer, int(m.group(1)) + 1)

    # Block size from pos_emb
    block_size = sd["pos_emb.weight"].shape[0] if "pos_emb.weight" in sd else 256

    # Heads — derive from head_dim divisibility (use 4 by default if d_model%4==0)
    n_head = config.get("n_head") or config.get("heads") or (12 if d_model == 768 else 4)

    model = ConsciousLM_v0(vocab_size=vocab_size, d_model=d_model, n_head=n_head,
                           n_layer=n_layer, block_size=block_size, dropout=0.0)
    info = model.load_state_dict(sd, strict=False)
    return model, {"vocab_size": vocab_size, "d_model": d_model, "n_layer": n_layer,
                   "block_size": block_size, "n_head": n_head}, info


# =================================================================
# Generation — byte-level autoregressive
# =================================================================
@torch.no_grad()
def generate_bytes(model, prompt_bytes, max_new=120, temperature=1.0,
                    top_k=None, greedy=False, device="cpu"):
    model.eval()
    if not prompt_bytes:
        # empty prompt — start with a single newline byte to bootstrap
        idx = torch.tensor([[10]], dtype=torch.long, device=device)  # \n
    else:
        idx = torch.tensor([prompt_bytes], dtype=torch.long, device=device)
    block_size = model.block_size
    for _ in range(max_new):
        idx_cond = idx[:, -block_size:]
        logits_a, _ = model(idx_cond)
        logits = logits_a[:, -1, :]
        if greedy:
            next_byte = logits.argmax(dim=-1, keepdim=True)
        else:
            logits = logits / max(temperature, 1e-6)
            if top_k:
                v, _ = logits.topk(min(top_k, logits.size(-1)))
                logits[logits < v[:, -1:]] = -float("inf")
            probs = F.softmax(logits, dim=-1)
            next_byte = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, next_byte], dim=1)
    return idx[0].cpu().tolist()


# =================================================================
# Scoring
# =================================================================
def hangul_ratio(text):
    if not text:
        return 0.0
    n_hangul = sum(1 for c in text if '가' <= c <= '힯')
    n_letters = sum(1 for c in text if c.isalpha() or '가' <= c <= '힯')
    if n_letters == 0:
        return 0.0
    return n_hangul / max(n_letters, 1)


def ascii_letter_ratio(text):
    if not text:
        return 0.0
    n_ascii = sum(1 for c in text if 'a' <= c <= 'z' or 'A' <= c <= 'Z')
    n_total = max(len(text), 1)
    return n_ascii / n_total


def is_byte_garbage(text):
    """Garbage = high ratio of unprintable + unicode replacement chars."""
    if not text:
        return False
    n_repl = text.count("�")
    n_unprint = sum(1 for c in text if (ord(c) < 32 and c not in "\n\t\r ") or ord(c) == 127)
    return (n_repl + n_unprint) / max(len(text), 1) > 0.3


def is_coherent(text):
    """Coherent = not byte-garbage + has letter content + no degenerate cycle."""
    if is_byte_garbage(text):
        return False
    # need some letter content (Hangul or ASCII alpha)
    n_letters = sum(1 for c in text if c.isalpha() or '가' <= c <= '힯')
    if n_letters / max(len(text), 1) < 0.2:
        return False
    # check degenerate single-char cycle
    if len(set(text.strip())) <= 2:
        return False
    return True


# =================================================================
# Test prompts
# =================================================================
PROMPTS_KO = [
    "안녕하세요",
    "한국어 가능?",
    "사용자: 안녕하세요\n도우미:",
]
PROMPTS_EN = [
    "Hello, how are you?",
    "What is consciousness?",
    "User: Hi\nAssistant:",
]
PROMPTS_C2 = [
    "Once upon a time",
    "Q:",
    "",  # empty
]

STRATEGIES = [
    ("greedy", {"greedy": True}),
    ("sample_t07_k40", {"temperature": 0.7, "top_k": 40}),
    ("sample_t05_k40", {"temperature": 0.5, "top_k": 40}),
    ("sample_t03_k80", {"temperature": 0.3, "top_k": 80}),
]


def run_prompt(model, prompt, strategies=STRATEGIES, max_new=120, device="cpu"):
    """Returns dict: strategy -> generated_text + scores."""
    prompt_bytes = list(prompt.encode("utf-8")) if prompt else []
    out = {}
    for sname, kwargs in strategies:
        gen_bytes = generate_bytes(model, prompt_bytes, max_new=max_new, device=device, **kwargs)
        gen_text_full = bytes(gen_bytes).decode("utf-8", errors="replace")
        gen_text_only = bytes(gen_bytes[len(prompt_bytes):]).decode("utf-8", errors="replace")
        out[sname] = {
            "full": gen_text_full,
            "gen": gen_text_only,
            "hangul_ratio": hangul_ratio(gen_text_only),
            "ascii_letter_ratio": ascii_letter_ratio(gen_text_only),
            "byte_garbage": is_byte_garbage(gen_text_only),
            "coherent": is_coherent(gen_text_only),
        }
    return out


def evaluate_model(model_path, model_loader, model_name, device="cpu", max_new=120):
    print(f"\n{'='*70}")
    print(f"MODEL: {model_name}")
    print(f"PATH:  {model_path}")
    print(f"{'='*70}")
    sys.stdout.flush()

    t_load = time.time()
    model, config, info = model_loader(model_path, device=device)
    model.to(device).eval()
    n_params = sum(p.numel() for p in model.parameters())
    t_load = time.time() - t_load
    print(f"  loaded in {t_load:.1f}s | params={n_params/1e6:.2f}M | "
          f"missing_keys={len(info.missing_keys)} unexpected_keys={len(info.unexpected_keys)}")
    print(f"  config: {config}")
    if info.missing_keys:
        print(f"  missing: {info.missing_keys[:3]}...")
    if info.unexpected_keys:
        print(f"  unexpected: {info.unexpected_keys[:3]}...")
    sys.stdout.flush()

    results = {
        "model_name": model_name,
        "model_path": str(model_path),
        "params_M": round(n_params / 1e6, 2),
        "config": config,
        "load_info": {"missing": len(info.missing_keys), "unexpected": len(info.unexpected_keys)},
        "load_time_s": round(t_load, 1),
        "ko": {},
        "en": {},
        "c2": {},
    }

    # KO group
    print(f"\n  --- C1 KO group (한글↔한글 strict) ---")
    sys.stdout.flush()
    for p in PROMPTS_KO:
        t0 = time.time()
        r = run_prompt(model, p, max_new=max_new, device=device)
        results["ko"][p] = r
        # find best by hangul_ratio
        best = max(r.items(), key=lambda kv: kv[1]["hangul_ratio"])
        bs, bd = best
        print(f"    {p[:30]:<32} | best={bs} hangul_ratio={bd['hangul_ratio']:.2f} "
              f"coherent={bd['coherent']} ({time.time()-t0:.1f}s)")
        print(f"      gen[:80]: {bd['gen'][:80]!r}")
        sys.stdout.flush()

    # EN group
    print(f"\n  --- C1 EN group (secondary) ---")
    sys.stdout.flush()
    for p in PROMPTS_EN:
        t0 = time.time()
        r = run_prompt(model, p, max_new=max_new, device=device)
        results["en"][p] = r
        best = max(r.items(), key=lambda kv: kv[1]["ascii_letter_ratio"])
        bs, bd = best
        print(f"    {p[:30]:<32} | best={bs} ascii_letter_ratio={bd['ascii_letter_ratio']:.2f} "
              f"coherent={bd['coherent']} ({time.time()-t0:.1f}s)")
        print(f"      gen[:80]: {bd['gen'][:80]!r}")
        sys.stdout.flush()

    # C2 spontaneous
    print(f"\n  --- C2 spontaneous ---")
    sys.stdout.flush()
    for p in PROMPTS_C2:
        plabel = p if p else "(empty)"
        t0 = time.time()
        r = run_prompt(model, p, max_new=max_new, device=device)
        results["c2"][plabel] = r
        # best by coherence then ascii_letter_ratio
        best = max(r.items(), key=lambda kv: (kv[1]["coherent"], kv[1]["ascii_letter_ratio"]))
        bs, bd = best
        print(f"    {plabel[:30]:<32} | best={bs} coherent={bd['coherent']} "
              f"ascii={bd['ascii_letter_ratio']:.2f} ({time.time()-t0:.1f}s)")
        print(f"      gen[:80]: {bd['gen'][:80]!r}")
        sys.stdout.flush()

    # Verdict
    ko_pass = sum(1 for p in PROMPTS_KO
                  if any(s["hangul_ratio"] >= 0.30 for s in results["ko"][p].values())
                  and any(not s["byte_garbage"] for s in results["ko"][p].values()))
    en_pass = sum(1 for p in PROMPTS_EN
                  if any(s["ascii_letter_ratio"] >= 0.40 for s in results["en"][p].values())
                  and any(s["coherent"] for s in results["en"][p].values()))
    c2_pass = sum(1 for plabel in [pp if pp else "(empty)" for pp in PROMPTS_C2]
                  if any(s["coherent"] for s in results["c2"][plabel].values()))

    c1_ko_pass = ko_pass >= 2
    c1_en_pass = en_pass >= 2
    c2_full_pass = c2_pass >= 2

    if c1_ko_pass and c2_full_pass:
        verdict = "SIMPLE_STACK_PASS"
    elif (not c1_ko_pass) and c1_en_pass and c2_full_pass:
        verdict = "PARTIAL_PASS_EN_only"
    elif c1_ko_pass and (not c2_full_pass):
        verdict = "PARTIAL_C1_only"
    elif (not c1_ko_pass) and (not c1_en_pass) and c2_full_pass:
        verdict = "PARTIAL_C2_only"
    else:
        verdict = "SIMPLE_STACK_FAIL"

    results["verdict"] = {
        "label": verdict,
        "ko_pass_n": ko_pass,
        "en_pass_n": en_pass,
        "c2_pass_n": c2_pass,
        "c1_ko_pass": c1_ko_pass,
        "c1_en_pass": c1_en_pass,
        "c2_full_pass": c2_full_pass,
    }
    print(f"\n  >>> VERDICT: {verdict} (KO={ko_pass}/3 EN={en_pass}/3 C2={c2_pass}/3)")
    sys.stdout.flush()
    return results


# =================================================================
# Main
# =================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", default="/Users/ghost/core/anima/state/anima_simple_stack_exhaustive_2026_05_06")
    ap.add_argument("--max_new", type=int, default=120)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--model", default="all", help="all|tiny|small|medium|base|clm_v2|v14")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build target list
    targets = []
    bg_fk_root = Path("/tmp/anima_v2_check")
    bg_fk_models = [
        ("clm_v2_tiny", bg_fk_root / "clm_v2_tiny" / "final.pt", load_conscious_lm_plus),
        ("clm_v2_small", bg_fk_root / "clm_v2_small" / "final.pt", load_conscious_lm_plus),
        ("clm_v2_medium", bg_fk_root / "clm_v2_medium" / "final.pt", load_conscious_lm_plus),
        ("clm_v2_base", bg_fk_root / "clm_v2_base" / "final.pt", load_conscious_lm_plus),
        ("clm_v2", bg_fk_root / "clm_v2" / "final.pt", load_conscious_lm_plus),
    ]

    if args.model == "all":
        targets = bg_fk_models
    else:
        targets = [m for m in bg_fk_models if args.model in m[0]]

    summary = {"models": [], "verdicts": {}}
    for name, path, loader in targets:
        if not path.exists():
            print(f"[SKIP] {name}: {path} does not exist")
            continue
        try:
            r = evaluate_model(path, loader, name, device=args.device, max_new=args.max_new)
            (out_dir / f"{name}_verdict.json").write_text(json.dumps(r, ensure_ascii=False, indent=2))
            summary["models"].append({
                "name": name,
                "params_M": r["params_M"],
                "verdict": r["verdict"]["label"],
                "ko": r["verdict"]["ko_pass_n"],
                "en": r["verdict"]["en_pass_n"],
                "c2": r["verdict"]["c2_pass_n"],
            })
            summary["verdicts"][name] = r["verdict"]["label"]
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            import traceback
            traceback.print_exc()
            summary["models"].append({"name": name, "verdict": "ERROR", "error": str(e)})

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    for m in summary["models"]:
        print(f"  {m['name']:<25} | params={m.get('params_M', 'N/A')}M | verdict={m['verdict']}")
    print(f"\nWritten: {out_dir}/summary.json")


if __name__ == "__main__":
    main()
