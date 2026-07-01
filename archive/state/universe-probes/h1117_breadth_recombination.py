#!/usr/bin/env python3
"""h1117_breadth_recombination.py — IS TRAINING BREADTH the lever for emergent
concept-recombination? Controlled experiment (the constructive successor to 1116's
closed-negative, which found the 7B couldn't recombine — bottleneck = narrow ~5MB
training, NOT model size).

CONTROLLED DESIGN (isolates breadth, holds arch+size+steps+format+TOTAL-BYTES fixed):
  · SAME small ByteGPT (d384/6L/6head/block256), SAME steps, from scratch.
  · NARROW corpus  = dialogue × 3  (15 MB, all consciousness-dialogue — one topic family).
  · BROAD  corpus  = dialogue + diverse 5-lang wiki  (15 MB, same dialogue base + ADDED
    multi-topic breadth instead of repeated dialogue). Same total bytes, same chat
    format (사용자:/도우미: present in both), the ONLY difference = topical breadth.
  · Run the 1116 emergence-recombination metric on BOTH.

FROZEN FALSIFIER (pre-registered): 🟢 BREADTH-IS-LEVER iff the BROAD model's composed
concept coverage > the NARROW model's AND broad composed_distinct >= 2 (recombination
emerges with breadth where narrow degenerates). 🔴 if broad <= narrow (breadth is NOT
sufficient at this scale → size/other bound). p7 deterministic (seed 7); g5/p7.
Lane-G torch REFERENCE; summer GPU $0.
"""
from __future__ import annotations
import argparse, json, math, re as _re, os
from collections import Counter
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
    def __init__(s, vocab=256, d=384, n_layer=6, n_head=6, block=256, p=0.0):
        super().__init__()
        s.block = block; s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256), targets.view(-1)) if targets is not None else None
        return logits, loss


def load(p): return torch.frombuffer(bytearray(open(p, "rb").read()), dtype=torch.uint8).long()
def batch(d, block, bs, dev):
    ix = torch.randint(0, d.numel()-block-1, (bs,))
    x = torch.stack([d[i:i+block] for i in ix]).to(dev)
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev)
    return x, y

def train(corpus, steps, dev, block=256, bs=32, lr=3e-4, seed=7):
    torch.manual_seed(seed)
    data = load(corpus); n = data.numel(); ntr = int(n*0.95); tr = data[:ntr]
    m = ByteGPT(block=block).to(dev); opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    m.train()
    for st in range(steps):
        lr_t = lr * (st+1)/200 if st < 200 else lr*0.5*(1+math.cos(math.pi*min(1.0,(st-200)/max(1,steps-200))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(tr, block, bs, dev)
        _, loss = m(x, y); opt.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == steps-1: print(f"    step {st} ce={loss.item():.4f}", flush=True)
    return m

@torch.no_grad()
def gen(m, seed, mx, dev, block, top_k=40, temp=0.9):
    m.eval(); idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    for _ in range(mx):
        logits, _ = m(idx[:, -block:]); logits = logits[:, -1, :].float()/temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, -1), 1).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if any(s in bytes(out).decode("utf-8", "ignore") for s in stops): break
    t = bytes(out).decode("utf-8", "ignore")
    for s in stops:
        i = t.find(s);  t = t[:i] if i >= 0 else t
    return t.strip()

def words(s): return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
def bigrams(s): w = words(s); return set(zip(w, w[1:]))

CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]
def metric(m, dev, block, label):
    def cov(t):
        wl = set(words(t)); return [i for i,(_,kw) in enumerate(CONCEPTS) if wl & kw]
    singles = [gen(m, f"사용자: {c}? | 도우미: ", 80, dev, block) for c,_ in CONCEPTS]
    sd = [len(cov(o)) for o in singles]; mx = max(sd)
    comp = gen(m, "사용자: "+" ".join(c for c,_ in CONCEPTS)+" — combine these. | 도우미: ", 120, dev, block)
    cc = cov(comp)
    sbg = set();
    for o in singles: sbg |= bigrams(o)
    novel = [(x,y) for (x,y) in (bigrams(comp)-bigrams(" ".join(c for c,_ in CONCEPTS))-sbg) if len(x)>=3 and len(y)>=3]
    print(f"  [{label}] singles_max_distinct={mx} composed_distinct={len(cc)} novel_bigrams={len(novel)}", flush=True)
    print(f"  [{label}] composed >> {comp[:150]}", flush=True)
    return {"label": label, "max_single": mx, "composed_distinct": len(cc), "novel": len(novel),
            "composed_text": comp, "singles": singles}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narrow", required=True); ap.add_argument("--broad", required=True)
    ap.add_argument("--steps", type=int, default=4000)
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[dev] {dev}", flush=True)
    print("[train NARROW]", flush=True); mn = train(a.narrow, a.steps, dev)
    rn = metric(mn, dev, 256, "NARROW")
    print("[train BROAD]", flush=True);  mb = train(a.broad, a.steps, dev)
    rb = metric(mb, dev, 256, "BROAD")
    breadth_lever = (rb["composed_distinct"] > rn["composed_distinct"] and rb["composed_distinct"] >= 2)
    print("\n=== H_1117 BREADTH-IS-LEVER? ===", flush=True)
    print(f"  NARROW composed_distinct={rn['composed_distinct']} (singles_max {rn['max_single']}, novel {rn['novel']})", flush=True)
    print(f"  BROAD  composed_distinct={rb['composed_distinct']} (singles_max {rb['max_single']}, novel {rb['novel']})", flush=True)
    print(f"  F-BREADTH-LEVER = {'1 🟢 BREADTH-IS-LEVER (broad recombines where narrow does not)' if breadth_lever else '0 🔴 NOT (breadth alone insufficient at this scale)'}", flush=True)
    json.dump({"narrow": {k:v for k,v in rn.items() if k!='singles'}, "broad": {k:v for k,v in rb.items() if k!='singles'},
               "breadth_lever": breadth_lever}, open("h1117_result.json","w"), ensure_ascii=False, indent=2)

if __name__ == "__main__": main()
