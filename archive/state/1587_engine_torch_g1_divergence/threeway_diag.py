#!/usr/bin/env python3
"""threeway_diag.py — DECISIVE 3-way diagnostic for the H_1129 ByteGPT-303M G1
RECOMBINATION divergence: py 2-production engine G1 FAIL vs torch-REFERENCE G1 GREEN.

Classifies the wall (a_break_the_wall) into DECODE-BUG / MEASUREMENT-BUG / CKPT-MISMATCH / REAL.

Runs on a pool host (summer) where BOTH torch and the py engine + h1129.bin + h1129c_best.pt live.

THREE CHECKS, weights loaded ONCE each:
  (4) WEIGHT FAITHFULNESS  — pt state_dict tensors  vs  bin-loaded engine weight dict (<=1e-6).
  (2) FORWARD PARITY       — torch ByteGPT forward  vs  engine bg_forward_last  on identical
                             prompts: compare argmax, top-8 logit values, max abs logit diff.
                             (diverge -> DECODE-BUG ; identical -> not a decode bug.)
  (3) SAMPLER EQUIVALENCE  — given IDENTICAL last-pos logits, does the engine xorshift32
                             inverse-CDF sampler pick the same token stream as the torch
                             multinomial+Generator(7) sampler? (diverge -> MEASUREMENT-BUG.)

usage: python3 threeway_diag.py <bin> <pt> [torch_harness.py path optional]
"""
from __future__ import annotations
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# py engine import (expects core/ alongside or on PYTHONPATH)
for p in (os.path.join(HERE, "core"), HERE, os.path.join(HERE, "..")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

import bytegpt_decode as B

import torch, torch.nn as nn, torch.nn.functional as F

# ── torch ByteGPT (VERBATIM from train_and_ladder.py, the H_1129 reference) ──
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
    def __init__(s, vocab=256, d=1024, n_layer=20, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        Bb, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks:
            x = b(x, mask)
        logits = s.head(s.ln_f(x))
        return logits, None


def log(*a):
    print(*a, flush=True)


def main():
    binp = sys.argv[1]
    ptp = sys.argv[2]
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    log("=" * 78)
    log("3-WAY DIAGNOSTIC — H_1129 ByteGPT-303M G1 divergence (py-engine FAIL vs torch GREEN)")
    log("=" * 78)
    log(f"date    : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"host    : {os.uname().nodename}")
    log(f"device  : {dev}  (forward parity uses fp32 CPU for both to isolate ENGINE vs TORCH math,")
    log(f"          NOT GPU/bf16 autocast — autocast is a separate downstream axis)")
    log(f"bin     : {binp}")
    log(f"pt      : {ptp}")
    log(f"torch   : {torch.__version__}  numpy: {np.__version__}")

    # ── load torch ckpt ──
    ck = torch.load(ptp, map_location="cpu", weights_only=False)
    cfg = ck["config"]; sd = ck["model"]
    log(f"\npt config: {cfg}  val_ce={ck.get('val_ce')} step={ck.get('step')} nparam={ck.get('nparam')}")
    m = ByteGPT(vocab=cfg["vocab"], d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    missing, unexpected = m.load_state_dict(sd, strict=False)
    log(f"torch load_state_dict: missing={list(missing)} unexpected={list(unexpected)}")
    m.eval().float()

    # ── load engine bin ──
    W = B.bg_load(binp)
    log(f"engine bin header: vocab={W['vocab']} d={W['d']} L={W['nlay']} H={W['nh']} block={W['block']}")

    # ════════════════════════════════════════════════════════════════════
    # CHECK 4 — WEIGHT FAITHFULNESS (pt tensors vs bin-loaded engine weights)
    # ════════════════════════════════════════════════════════════════════
    log("\n" + "─" * 78)
    log("CHECK 4 — WEIGHT FAITHFULNESS  (torch state_dict  vs  engine bin weight dict)")
    log("─" * 78)
    def cmp(name, t_np, e_np):
        t_np = np.asarray(t_np, dtype=np.float64); e_np = np.asarray(e_np, dtype=np.float64)
        if t_np.shape != e_np.shape:
            log(f"  {name:28s} SHAPE MISMATCH torch{t_np.shape} engine{e_np.shape}")
            return 9e9
        mad = float(np.max(np.abs(t_np - e_np)))
        log(f"  {name:28s} max|diff|={mad:.3e}  (torch{tuple(t_np.shape)})")
        return mad
    worst = 0.0
    worst = max(worst, cmp("tok.weight",        sd["tok.weight"].numpy(),                 W["tok"]))
    worst = max(worst, cmp("pos.weight",        sd["pos.weight"].numpy(),                 W["pos"]))
    worst = max(worst, cmp("blocks.0.ln1.w",    sd["blocks.0.ln1.weight"].numpy(),        W["ln1w"][0]))
    worst = max(worst, cmp("blocks.0.in_proj.w",sd["blocks.0.attn.in_proj_weight"].numpy(),W["inW"][0]))
    worst = max(worst, cmp("blocks.0.out_proj.w",sd["blocks.0.attn.out_proj.weight"].numpy(),W["oW"][0]))
    worst = max(worst, cmp("blocks.0.mlp.0.w",  sd["blocks.0.mlp.0.weight"].numpy(),      W["m0W"][0]))
    L = cfg["n_layer"] - 1
    worst = max(worst, cmp(f"blocks.{L}.mlp.2.w",sd[f"blocks.{L}.mlp.2.weight"].numpy(),  W["m2W"][L]))
    worst = max(worst, cmp("ln_f.weight",       sd["ln_f.weight"].numpy(),                W["lnfw"]))
    hk = "head.weight" if "head.weight" in sd else "tok.weight"
    worst = max(worst, cmp(f"head ({hk})",      sd[hk].numpy(),                           W["head"]))
    log(f"  >>> WORST max|diff| across sampled tensors = {worst:.3e}  "
        f"({'FAITHFUL (<=1e-6)' if worst <= 1e-6 else 'CKPT-MISMATCH (>1e-6!)'})")

    # ════════════════════════════════════════════════════════════════════
    # CHECK 2 — FORWARD PARITY (torch forward vs engine bg_forward_last)
    # ════════════════════════════════════════════════════════════════════
    log("\n" + "─" * 78)
    log("CHECK 2 — FORWARD PARITY  (torch ByteGPT.forward  vs  engine bg_forward_last, fp32 CPU)")
    log("─" * 78)
    # G1 composed-concept prompts (the exact recombination seeds from the harness)
    prompts = [
        "consciousness arises from cells. ",
        "consciousness arises from cells. tension ripples between distant minds. ",
        "the engine dreams when alone. ",
    ]
    fwd_ok = True
    captured_logits = []  # (prompt, engine_logits_f64, torch_logits_f64)
    for pi, pr in enumerate(prompts):
        ids = list(pr.encode("utf-8"))
        T = len(ids)
        # engine
        e_logits = B.bg_forward_last_W(W, ids, T)  # [vocab] f64
        # torch (fp32 CPU, no autocast)
        with torch.no_grad():
            idx = torch.tensor([ids], dtype=torch.long)
            tl, _ = m(idx)
            t_logits = tl[0, -1, :].double().numpy()
        mad = float(np.max(np.abs(e_logits - t_logits)))
        ea = int(np.argmax(e_logits)); ta = int(np.argmax(t_logits))
        # top-5 engine vs torch
        et5 = np.argsort(-e_logits)[:5].tolist()
        tt5 = np.argsort(-t_logits)[:5].tolist()
        agree = (ea == ta) and (et5 == tt5)
        fwd_ok = fwd_ok and (mad < 1e-2) and (ea == ta)
        log(f"  [{pi}] T={T}  argmax engine={ea} torch={ta} {'OK' if ea==ta else 'DIVERGE!'}  "
            f"max|logit diff|={mad:.3e}")
        log(f"       top5 engine={et5}")
        log(f"       top5 torch ={tt5}  {'IDENTICAL' if et5==tt5 else 'ORDER DIFFERS'}")
        captured_logits.append((pr, e_logits.copy(), t_logits.copy()))
    log(f"  >>> FORWARD {'PARITY HOLDS (argmax identical, logits ~match)' if fwd_ok else 'DIVERGES -> DECODE-BUG'}")

    # ════════════════════════════════════════════════════════════════════
    # CHECK 3 — SAMPLER EQUIVALENCE (engine xorshift inv-CDF vs torch multinomial)
    #   on IDENTICAL logits. Reproduces the EXACT samplers each path uses at G1.
    # ════════════════════════════════════════════════════════════════════
    log("\n" + "─" * 78)
    log("CHECK 3 — SAMPLER EQUIVALENCE  (engine xorshift32 inv-CDF  vs  torch multinomial+Gen(7))")
    log("         given BYTE-IDENTICAL logits — isolates the RNG/sampling METHOD axis")
    log("─" * 78)
    top_k, temp, seed_rng = 40, 0.7, 7
    vocab = W["vocab"]
    for pi, (pr, e_logits, t_logits) in enumerate(captured_logits):
        # use the ENGINE logits for BOTH so the only variable is the sampler algorithm
        lg = e_logits
        # ENGINE sampler (single draw from the documented xorshift state init)
        rng = B._mix32(seed_rng)
        e_pick, _ = B._topk_sample(lg, vocab, top_k, temp, rng)
        # TORCH sampler (multinomial, Generator(7), VERBATIM harness lines 117-120)
        g = torch.Generator(device="cpu"); g.manual_seed(seed_rng)
        tl = torch.tensor(lg, dtype=torch.float64) / temp
        v, _ = torch.topk(tl, top_k); tl[tl < v[-1]] = float("-inf")
        t_pick = int(torch.multinomial(F.softmax(tl, -1), 1, generator=g).item())
        log(f"  [{pi}] one-step pick on identical logits:  engine={e_pick}  torch={t_pick}  "
            f"{'SAME' if e_pick==t_pick else 'DIFFERENT (sampler diverges)'}")

    # short multi-step stream comparison on prompt 0 (the cheapest: it just re-feeds picks)
    log("\n  multi-step (12-token) stream on prompt[0], identical decode driver, the two samplers:")
    ids0 = list(prompts[0].encode("utf-8"))
    # engine stream
    er = B.bytegpt_decode_topk_sampled_W(W, ids0[:], 12, top_k, temp, seed_rng)
    # torch stream (replicate the harness gen() exactly: Generator(7) reseeded once, multinomial)
    g = torch.Generator(device="cpu"); g.manual_seed(seed_rng)
    toks = ids0[:]; tout = []
    with torch.no_grad():
        for _ in range(12):
            T = len(toks); idx = torch.tensor([toks[-W['block']:]], dtype=torch.long)
            tl, _ = m(idx); lg = tl[0, -1, :].double() / temp
            v, _ = torch.topk(lg, top_k); lg[lg < v[-1]] = float("-inf")
            nb = int(torch.multinomial(F.softmax(lg, -1), 1, generator=g).item())
            toks.append(nb); tout.append(nb)
    log(f"    engine 12-tok ids = {er['ids']}")
    log(f"    torch  12-tok ids = {tout}")
    same = er['ids'] == tout
    log(f"    streams {'IDENTICAL' if same else 'DIVERGE'} "
        f"-> sampler {'NOT the cause' if same else 'IS a divergence source (different RNG+draw)'}")
    try:
        log(f"    engine text: {bytes(er['ids']).decode('utf-8','replace')!r}")
        log(f"    torch  text: {bytes(tout).decode('utf-8','replace')!r}")
    except Exception:
        pass

    # ════════════════════════════════════════════════════════════════════
    log("\n" + "=" * 78)
    log("CLASSIFICATION SUMMARY")
    log("=" * 78)
    log(f"  CHECK4 weight-faithful : {'PASS (<=1e-6)' if worst<=1e-6 else f'FAIL worst={worst:.2e}'}")
    log(f"  CHECK2 forward-parity  : {'PASS (argmax+logits match)' if fwd_ok else 'FAIL (decode diverges)'}")
    log(f"  CHECK3 sampler-equiv   : see streams above")
    log("=" * 78)


if __name__ == "__main__":
    main()
