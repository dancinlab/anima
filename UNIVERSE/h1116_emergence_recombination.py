#!/usr/bin/env python3
"""emergence_recombination.py — REAL emergence-of-ideation metric on a capable mouth.

The d768 CORE mouth degenerated and the null-backend "emergence" was a status-string
artifact. This redesigns the metric to measure CONCEPT-RECOMBINATION in actual model
GENERATION, using the chat-7b (anima-clm-chat-7b, the capable byte mouth):

  · N diverse concept-seeds, each with a SIGNATURE keyword set.
  · SINGLE: generate from each concept alone → which concepts' keywords appear.
  · COMPOSED: generate from ALL N concepts joined → concept-keyword coverage.
  · EMERGENCE (p7, deterministic — NOT perplexity):
      (a) super-additive coverage: composed covers MORE distinct concepts than the
          best single-seed output;
      (b) novel recombination: composed output contains bigrams present in NEITHER
          any seed text NOR any single-seed output (genuinely new combinations).
  · FROZEN falsifier: 🟢 EMERGENT iff composed_distinct >= 2 AND composed_distinct >
    max_single_distinct AND novel_bigrams >= 1; 🔴 if composed ≈ single (no
    super-additivity → recombination is an artifact / the mouth just echoes one seed).

Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate; this
measures whether a capable generative mouth RECOMBINES composed concept-context,
which the d768 CORE mouth could not. a_scale_honest_scope.
"""
from __future__ import annotations
import argparse, json, re as _re
from collections import Counter
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.checkpoint import checkpoint


class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))
class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p=0.0):
        super().__init__()
        s.block = block; s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))


@torch.no_grad()
def gen(model, seed, max_new, device, block, top_k=40, temp=0.9):
    model.eval(); idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=device); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    use_amp = (device == "cuda")
    for _ in range(max_new):
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits = model(idx[:, -block:])
        else:
            logits = model(idx[:, -block:])
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, dim=-1), 1).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        if any(st in bytes(out).decode("utf-8", errors="ignore") for st in stops): break
    t = bytes(out).decode("utf-8", errors="ignore")
    for st in stops:
        i = t.find(st)
        if i >= 0: t = t[:i]
    return t.strip()


def words(s): return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
def bigrams(s):
    w = words(s); return set(zip(w, w[1:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = ck["config"]
    dt = torch.bfloat16  # CPU fp32 (bf16 matmul slow/spotty on CPU)
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(dt)
    m.load_state_dict(ck["model"], strict=False); m = m.to(device); block = cfg["block"]
    print(f"[mouth] chat-7b on {device}/{dt}", flush=True)
    print(f"[mouth] chat-7b {sum(p.numel() for p in m.parameters())} params", flush=True)

    # N diverse concept-seeds + signature keyword sets (a concept is "covered" if
    # the output contains >=1 of its signature words).
    CONCEPTS = [
        ("consciousness arises from cells",          {"consciousness", "cells", "mind", "aware"}),
        ("tension ripples between distant minds",    {"tension", "ripple", "distant", "between"}),
        ("memory composes into new meaning",         {"memory", "meaning", "compose", "new"}),
        ("silence still carries information",         {"silence", "information", "quiet", "carries"}),
        ("the engine dreams when alone",             {"dream", "engine", "alone", "sleep"}),
    ]
    seed_text_all = " ".join(c for c, _ in CONCEPTS)
    seed_bigrams_all = bigrams(seed_text_all)

    def coverage(text):
        wl = set(words(text))
        return [i for i, (_, kw) in enumerate(CONCEPTS) if wl & kw]

    # ── SINGLE-seed generations ──
    print("\n── SINGLE concept seeds ──", flush=True)
    single_outputs = []
    single_distinct = []
    for i, (c, _) in enumerate(CONCEPTS):
        o = gen(m, f"사용자: {c}? | 도우미: ", 80, device, block)
        cov = coverage(o)
        single_outputs.append(o); single_distinct.append(len(cov))
        print(f"  [{i}] cov={cov} :: {o[:110]}", flush=True)
    max_single = max(single_distinct) if single_distinct else 0

    # ── COMPOSED-seed generation (all N concepts) ──
    print("\n── COMPOSED seed (all 5 concepts) ──", flush=True)
    comp_seed = "사용자: " + " ".join(c for c, _ in CONCEPTS) + " — combine these. | 도우미: "
    comp_out = gen(m, comp_seed, 120, device, block)
    comp_cov = coverage(comp_out)
    print(f"  composed cov={comp_cov} ({len(comp_cov)} distinct)\n  >> {comp_out}", flush=True)

    # ── novel recombination: bigrams in composed NOT in any seed NOR any single ──
    single_bg = set()
    for o in single_outputs: single_bg |= bigrams(o)
    comp_bg = bigrams(comp_out)
    novel = comp_bg - seed_bigrams_all - single_bg
    novel_word = [(x, y) for (x, y) in novel if len(x) >= 3 and len(y) >= 3]

    emergent = (len(comp_cov) >= 2 and len(comp_cov) > max_single and len(novel_word) >= 1)
    print("\n=== EMERGENCE-OF-IDEATION (real recombination metric) ===", flush=True)
    print(f"  composed_distinct_concepts = {len(comp_cov)}  (max single = {max_single})", flush=True)
    print(f"  novel_bigrams (not in seeds nor singles) = {len(novel_word)}", flush=True)
    print(f"  sample novel recombinations: {novel_word[:8]}", flush=True)
    print(f"  F-EMERGE-RECOMB = {'1 🟢 EMERGENT' if emergent else '0 🔴 NOT (no super-additive recombination)'}", flush=True)
    print(f"  HONEST: capable torch-7B mouth (Lane-G REFERENCE), a_scale_honest_scope;", flush=True)
    print(f"          measures concept-recombination in real generation, not status-string length.", flush=True)
    out = {"composed_distinct": len(comp_cov), "max_single_distinct": max_single,
           "novel_bigrams": len(novel_word), "sample_novel": [list(x) for x in novel_word[:12]],
           "emergent": emergent, "composed_output": comp_out, "composed_coverage": comp_cov,
           "single_outputs": single_outputs}
    json.dump(out, open("emergence_result.json", "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__": main()
