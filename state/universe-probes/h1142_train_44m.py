#!/usr/bin/env python3
"""h1142_train_44m.py — train the ~44.68M ByteGPT rung for the H_1142 gate-tension
ladder, on the SAME English wiki corpus the gates probe against (so gate_g2's
corpus-absent test + gate_g5_l2's verbatim-sentence extraction are metric-faithful).

ARCH + TRAIN LOOP = h1129_midcap_broad_converged_recombination.py recipe VERBATIM
(ByteGPT, AdamW betas(0.9,0.95) wd0.1, cosine+warmup, best-ckpt-by-val-CE), only
the size config differs: d=512/L14/H8 = 44.53M (~44.68M target rung; 7B/303M/this
are all the SAME ByteGPT family so the frozen gate harness applies verbatim).

summer GPU $0, VRAM-capped (set_per_process_memory_fraction) — co-tenant untouched.
"""
from __future__ import annotations
import argparse, json, math, os, time
import torch, torch.nn as nn, torch.nn.functional as F


# ── ByteGPT arch — h1129/h1141 VERBATIM ──
class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=512, n_layer=14, n_head=8, block=512, p=0.0):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device, dtype=x.dtype), diagonal=1)
        for b in s.blocks:
            x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256).float(), targets.view(-1)) if targets is not None else None
        return logits, loss


def load_bytes(p):
    raw = open(p, "rb").read()
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8)

def get_batch(d, block, bs, dev):
    ix = torch.randint(0, d.numel() - block - 1, (bs,))
    x = torch.stack([d[i:i+block] for i in ix]).to(dev, non_blocking=True).long()
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev, non_blocking=True).long()
    return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--d", type=int, default=512)
    ap.add_argument("--n_layer", type=int, default=14)
    ap.add_argument("--n_head", type=int, default=8)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--bs", type=int, default=24)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--eval_every", type=int, default=500)
    ap.add_argument("--vram_frac", type=float, default=0.36)
    ap.add_argument("--ckpt", default="/tmp/h1142_44m_best.pt")
    a = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    if dev == "cuda":
        torch.cuda.set_per_process_memory_fraction(a.vram_frac, 0)
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)} VRAM-cap frac={a.vram_frac}", flush=True)

    data = load_bytes(a.corpus); n = data.numel(); ntr = int(n*0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB val={va.numel()/1e6:.2f}MB", flush=True)

    m = ByteGPT(d=a.d, n_layer=a.n_layer, n_head=a.n_head, block=a.block).to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] ByteGPT d={a.d} L={a.n_layer} H={a.n_head} block={a.block} PARAMS={nparam:,} ({nparam/1e6:.2f}M)", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)

    @torch.no_grad()
    def eval_ce(d, iters=40):
        m.eval(); tot = 0.0
        for _ in range(iters):
            x, y = get_batch(d, a.block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, l = m(x, y)
            else:
                _, l = m(x, y)
            tot += l.item()
        m.train(); return tot/iters

    best = 1e9; t0 = time.time()
    print(f"[train] {a.steps} steps bs={a.bs} accum={a.accum} (eff {a.bs*a.accum}) cosine warmup={a.warmup}", flush=True)
    m.train()
    for st in range(a.steps):
        if st < a.warmup:
            lr_t = a.lr * (st+1)/a.warmup
        else:
            prog = min(1.0, (st - a.warmup)/max(1, a.steps - a.warmup))
            lr_t = a.lr * 0.5 * (1 + math.cos(math.pi*prog))
        for g in opt.param_groups: g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(a.accum):
            x, y = get_batch(tr, a.block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, loss = m(x, y)
            else:
                _, loss = m(x, y)
            (loss/a.accum).backward(); acc_loss += loss.item()/a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if (st+1) % a.eval_every == 0 or st == a.steps-1:
            vce = eval_ce(va); dt = time.time()-t0
            print(f"  step {st+1:5d} train_ce={acc_loss:.4f} val_ce={vce:.4f} lr={lr_t:.2e} {dt/60:.1f}min", flush=True)
            if vce < best:
                best = vce
                torch.save({"model": m.state_dict(),
                            "config": {"vocab":256,"d":a.d,"n_layer":a.n_layer,"n_head":a.n_head,"block":a.block},
                            "val_ce": vce, "step": st+1, "nparam": nparam}, a.ckpt)
                print(f"    [ckpt] saved best val_ce={vce:.4f} -> {a.ckpt}", flush=True)
    print(f"[done] best val_ce={best:.4f} ckpt={a.ckpt}", flush=True)


if __name__ == "__main__":
    main()
