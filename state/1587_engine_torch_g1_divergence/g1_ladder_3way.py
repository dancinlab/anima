#!/usr/bin/env python3
"""g1_ladder_3way.py — run the FULL G1 recombination ladder THREE ways on h1129, with
the IDENTICAL frozen metric (coverage / max_single / clears) from the H_1129 harness,
to pin down WHERE the py-engine G1 FAIL vs torch-REF G1 GREEN divergence lives:

  (A) torch GPU bf16 autocast   — the EXACT condition the original H_1129 'GREEN' was measured under
  (B) torch fp32 CPU            — same torch model+metric+multinomial sampler, but fp32/CPU
  (C) engine fp32 CPU           — the py 2-production engine (bytegpt_decode) + its xorshift sampler

All three use: temp=0.7, top_k=40, seed_rng=7, single@80 / composed@120, CONCEPTS verbatim,
coverage() verbatim, clears = distinct>=2 AND distinct>max_single AND kwr>=0.50.

A==GREEN, C==FAIL already known. The point: does B (torch, same metric, fp32/CPU, multinomial)
match A (GREEN) or C (FAIL)?
  - B==GREEN, C==FAIL  -> the divergence is the SAMPLER METHOD (engine xorshift vs torch multinomial),
                         NOT precision/device. The metric is faithful; only the RNG differs. MEASUREMENT-BUG.
  - B==FAIL like C     -> the original GREEN needed GPU/bf16 (precision/seed-luck), engine fp32 reproduces
                         torch-fp32; the GREEN is precision/seed-fragile (also a measurement caveat, not a model property).
"""
from __future__ import annotations
import sys, os, re, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "core"), HERE):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bytegpt_decode as B
import torch, torch.nn as nn, torch.nn.functional as F

class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))
class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(0.0)
        s.blocks = nn.ModuleList([Block(d, n_head, 0.0) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx):
        Bb, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None, :, :]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))

CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]
def words(s): return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
KNOWN = set()
for _c, _kw in CONCEPTS:
    KNOWN |= {w for w in words(_c)}; KNOWN |= _kw
for _p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
    try:
        with open(_p, errors="ignore") as _f:
            for _w in _f:
                _w = _w.strip().lower()
                if _w.isalpha(): KNOWN.add(_w)
        break
    except OSError: continue
KNOWN |= {"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t"}
def kwr(text):
    wl = words(text)
    return sum(1 for w in wl if w in KNOWN)/len(wl) if wl else 0.0
def coverage(text):
    wl = set(words(text))
    return [i for i,(_,kw) in enumerate(CONCEPTS) if wl & kw]

STOPS = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
def _trim(t):
    for st in STOPS:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()

@torch.no_grad()
def gen_torch(m, seed, mx, dev, block, use_amp, top_k=40, temp=0.7, seed_rng=7):
    m.eval(); g = torch.Generator(device=dev); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out=[]
    for _ in range(mx):
        ctx = idx[:, -block:]
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits = m(ctx)
        else:
            logits = m(ctx)
        logits = logits[:, -1, :].float()/temp
        if top_k:
            v,_ = torch.topk(logits, top_k); logits[logits < v[:,[-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits,-1),1,generator=g).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]],device=dev)],1)
        if any(st in bytes(out).decode("utf-8","ignore") for st in STOPS): break
    return _trim(bytes(out).decode("utf-8","ignore"))

def gen_engine(W, seed, mx, top_k=40, temp=0.7, seed_rng=7):
    ids = list(seed.encode("utf-8"))
    r = B.bytegpt_decode_topk_sampled_W(W, ids, mx, top_k, temp, seed_rng)
    # engine has no stop-trim in the W entry; apply the SAME trim for metric parity
    return _trim(r["text"])

def ladder(genfn, label):
    print(f"\n##### LADDER [{label}] #####", flush=True)
    sd = []
    for i,(c,_) in enumerate(CONCEPTS):
        o = genfn(f"{c}. ", 80); cov = coverage(o); sd.append(len(cov))
        print(f"  single[{i}] cov={cov} kwr={kwr(o):.2f} :: {o[:90]!r}", flush=True)
    ms = max(sd) if sd else 0
    print(f"  max_single_distinct = {ms}", flush=True)
    best = 0; clears_any = False
    for k in (2,3,4,5):
        seedp = ". ".join(c for c,_ in CONCEPTS[:k]) + ". "
        o = genfn(seedp, 120); cc = coverage(o); kk = kwr(o); coh = kk>=0.50
        clears = (len(cc)>=2 and len(cc)>ms and coh)
        clears_any = clears_any or clears; best = max(best, len(cc))
        print(f"  k={k} composed_distinct={len(cc)} cov={cc} kwr={kk:.2f} coherent={coh} clears={clears}", flush=True)
        print(f"       >> {o[:130]!r}", flush=True)
    verdict = "GREEN (recombines)" if clears_any else "FAIL (no recombination lift)"
    print(f"  ==> [{label}] G1 = {verdict}  (max_single={ms} best_composed={best})", flush=True)
    return clears_any, ms, best

def main():
    binp, ptp = sys.argv[1], sys.argv[2]
    print("="*78); print("G1 LADDER 3-WAY — A(torch GPU bf16) / B(torch fp32 CPU) / C(engine fp32 CPU)")
    print("="*78)
    print(f"date {time.strftime('%Y-%m-%d %H:%M:%S')} host {os.uname().nodename} torch {torch.__version__}")
    ck = torch.load(ptp, map_location="cpu", weights_only=False); cfg = ck["config"]
    print(f"pt cfg {cfg} val_ce {ck.get('val_ce'):.4f} step {ck.get('step')}")
    W = B.bg_load(binp)

    has_cuda = torch.cuda.is_available()
    # ---- A: torch GPU bf16 (original GREEN condition) ----
    if has_cuda:
        mg = ByteGPT(**cfg).cuda(); mg.load_state_dict(ck["model"]); mg.eval()
        a_green,_,_ = ladder(lambda s,mx: gen_torch(mg,s,mx,"cuda",cfg["block"],True), "A torch GPU bf16 (orig GREEN cond)")
        del mg; torch.cuda.empty_cache()
    else:
        print("\n[A] CUDA unavailable — skipping GPU bf16 arm"); a_green=None
    # ---- B: torch fp32 CPU ----
    mc = ByteGPT(**cfg); mc.load_state_dict(ck["model"]); mc.eval().float()
    b_green,_,_ = ladder(lambda s,mx: gen_torch(mc,s,mx,"cpu",cfg["block"],False), "B torch fp32 CPU")
    # ---- C: engine fp32 CPU ----
    c_green,_,_ = ladder(lambda s,mx: gen_engine(W,s,mx), "C engine fp32 CPU (py 2-production)")

    print("\n"+"="*78); print("3-WAY G1 VERDICT")
    print("="*78)
    print(f"  A torch GPU bf16 : {'GREEN' if a_green else ('FAIL' if a_green is not None else 'SKIP')}")
    print(f"  B torch fp32 CPU : {'GREEN' if b_green else 'FAIL'}")
    print(f"  C engine fp32 CPU: {'GREEN' if c_green else 'FAIL'}")
    print("  INTERPRETATION:")
    if (a_green or b_green) and not c_green:
        print("    torch GREEN, engine FAIL with byte-identical forward -> divergence is SAMPLER/METHOD")
        print("    (engine xorshift inv-CDF vs torch multinomial+Gen(7)) = MEASUREMENT-BUG, not a model property.")
    if b_green is not None and a_green is not None and (a_green != b_green):
        print("    A!=B -> the original GREEN is precision/device(bf16/GPU)-dependent (seed-fragile measurement).")
    if (not a_green) and (not b_green) and (not c_green):
        print("    ALL FAIL -> the recorded torch GREEN used a different ckpt/condition than h1129c_best.pt.")
if __name__ == "__main__": main()
