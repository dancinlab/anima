#!/usr/bin/env python3
"""h1118_broad_7b_recombination.py — the EMPTY 2x2 cell: 7B capacity × BROAD data.

1116 (7B × narrow dialogue) → 0 concepts. 1117 (11M × broad) → 0 concepts. The
untested cell is BIG capacity × BROAD breadth. The base model clm-v1-ref-pytorch-
cuda-7b is exactly that: a 7.25B ByteGPT trained on the 5-lang WIKI backbone
(diverse topics) — NOT chat-tuned, so we probe it with PLAIN concept-continuation
prompts (no 사용자:/도우미:), and measure concept-recombination the same way.

If the broad base-7B recombines composed concepts (composed_distinct >= 2 AND >
1116's 0), the conjunction hypothesis (capacity × breadth) gains support. HONEST
caveat: the base 7B is descent-PASS but UNDERTRAINED (400 bounded steps) — broad
but not converged; a 🔴 could be undertraining rather than a breadth refutation.
Lane-G torch REFERENCE; summer CPU bf16 $0; g5/p7 deterministic.
"""
from __future__ import annotations
import argparse, json, re as _re
import torch, torch.nn as nn, torch.nn.functional as F


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
def gen(m, seed, mx, dev, block, top_k=40, temp=0.9):
    m.eval(); idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    for _ in range(mx):
        logits = m(idx[:, -block:]); logits = logits[:, -1, :].float()/temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, -1), 1).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if "\n\n" in bytes(out).decode("utf-8", "ignore"): break
    return bytes(out).decode("utf-8", "ignore").strip()

def words(s): return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
def bigrams(s): w = words(s); return set(zip(w, w[1:]))
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ckpt", required=True); a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = ck["config"]
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).bfloat16()
    m.load_state_dict(ck["model"], strict=False); m = m.to(dev); block = cfg["block"]
    print(f"[base-7B broad] {sum(p.numel() for p in m.parameters())} params on {dev}", flush=True)
    def cov(t):
        wl = set(words(t)); return [i for i,(_,kw) in enumerate(CONCEPTS) if wl & kw]
    # PLAIN (non-chat) continuation prompts — base 7B is wiki-continuation, not chat.
    singles = [gen(m, c + ". ", 80, dev, block) for c,_ in CONCEPTS]
    sd = [len(cov(o)) for o in singles]; mx = max(sd)
    for i,o in enumerate(singles): print(f"  [single {i}] cov={cov(o)} :: {o[:100]}", flush=True)
    comp = gen(m, ". ".join(c for c,_ in CONCEPTS) + ". ", 130, dev, block)
    cc = cov(comp)
    sbg = set()
    for o in singles: sbg |= bigrams(o)
    novel = [(x,y) for (x,y) in (bigrams(comp)-bigrams(". ".join(c for c,_ in CONCEPTS))-sbg) if len(x)>=3 and len(y)>=3]
    print(f"\n  [COMPOSED] cov={cc} ({len(cc)} distinct) novel_bigrams={len(novel)}", flush=True)
    print(f"  >> {comp}", flush=True)
    emergent = (len(cc) >= 2 and len(cc) > 0)   # vs 1116 narrow-7B composed_distinct=0
    print("\n=== H_1118 EMPTY-CELL (7B × BROAD wiki) ===", flush=True)
    print(f"  composed_distinct={len(cc)} (singles_max={mx}, novel={len(novel)}); vs 1116 narrow-7B=0", flush=True)
    print(f"  F-CONJUNCTION = {'1 🟢 broad-7B RECOMBINES (capacity×breadth conjunction supported)' if emergent else '0 🔴 broad-7B also fails (undertrained base, or conjunction needs converged-broad)'}", flush=True)
    json.dump({"composed_distinct": len(cc), "singles_max": mx, "novel": len(novel),
               "composed_text": comp, "singles": singles, "emergent": emergent},
              open("h1118_result.json","w"), ensure_ascii=False, indent=2)

if __name__ == "__main__": main()
