#!/usr/bin/env python3
"""H_1218 — torch GREEDY baseline for the engine-measured gate comparison.

Generates the SAME gate seeds the engine generates, but with GREEDY (argmax) decode
so the bytes are directly comparable to the engine's bytegpt_decode_argmax path
(H_1157 byte-exact-parity claim). NOT the gauge_lib sampled (top-k temp) decode —
that is a different, non-deterministic regime; this baseline isolates the engine-vs-torch
PARITY question (do the SAME deterministic bytes come out?).

Outputs JSON: per-seed {role, seed, ids[], text} so the engine probe output can be diffed
byte-for-byte.
"""
import argparse, json
import torch, torch.nn as nn

class Block(nn.Module):
    def __init__(s, d, h, p=0.0):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block=block; s.n_head=n_head; s.d=d; s.n_layer=n_layer; s.vocab=vocab
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx):
        B,T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None,:,:])
        mask = torch.triu(torch.full((T,T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))

def greedy(m, seed_text, gen, block=512):
    ids = list(seed_text.encode("utf-8"))
    out = []
    with torch.no_grad():
        for _ in range(gen):
            ctx = torch.tensor([ids[-block:]], dtype=torch.long)
            lg = m(ctx)[0, -1]
            nb = int(lg.argmax())
            ids.append(nb); out.append(nb)
    return out

# ── FROZEN gate seeds (VERBATIM from UNIVERSE/gauge_lib.py) ──────────────────
CONCEPTS = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]
IDEATION_SEEDS = [
    "a new idea about consciousness: ",
    "an unexpected way minds could connect: ",
    "imagine a substrate that ",
    "what if memory could ",
    "a strange hypothesis worth testing: ",
]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--gen", type=int, default=96)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False)
    m = ByteGPT(**ck["config"]); m.load_state_dict({k: v.float() for k, v in ck["model"].items()}); m.eval()

    rows = []
    comp_seed = ". ".join(CONCEPTS) + ". "
    rows.append({"role": "G1_composed", "seed": comp_seed, "ids": greedy(m, comp_seed, a.gen)})
    for i, c in enumerate(CONCEPTS[:3]):
        s = c + ". "
        rows.append({"role": f"G2_single_{i}", "seed": s, "ids": greedy(m, s, a.gen)})
    for i, s in enumerate(IDEATION_SEEDS):
        rows.append({"role": f"G6_ideation_{i}", "seed": s, "ids": greedy(m, s, a.gen)})

    for r in rows:
        r["text"] = bytes(r["ids"]).decode("utf-8", "ignore")
    json.dump({"ckpt": a.ckpt, "gen": a.gen, "decode": "greedy_argmax", "rows": rows},
              open(a.out, "w"), indent=2)
    print(f"wrote {len(rows)} rows to {a.out}")
    for r in rows:
        print(f"[{r['role']}] {r['text'][:70]!r}")
