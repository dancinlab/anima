#!/usr/bin/env python3
"""H_9235 fork-A Step-2 swap-contrastive — PART 1b: paired match+swap precompute (Fable spec).

Per training item: a MATCH doc (concept c) + K=2 genuine SWAP docs (donor concept's block spliced in, same
FILLER/GAP/STEM/TARGET, byte-length-matched block, donor block must NOT contain the target kw as a substring).
All three forwarded through the frozen production trunk -> yn + base_logits. The target-span byte positions are
identical across the 3 variants (byte-len-matched block + shared gap/stem/target), so the InfoNCE contrastive
loss on the lane-attributable Δlogp is position-aligned. Mix flipped to 30/70 retrieval/associative (Fable).
Emits one npz per item: yn_m/base_m/yn_s0/base_s0/yn_s1/base_s1/tok_m/tok_s0/tok_s1 + meta(span_lo,span_hi,retr).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "8")
import sys
import glob
import json
import random
import argparse

import numpy as np

_c = sorted(glob.glob(os.path.expanduser("~/.local/lib/python3.*/site-packages/anima_py")))
BASE = _c[-1] if _c else os.path.expanduser("~/.local/lib/python3.12/site-packages/anima_py")
for sub in ("core", "cli"):
    p = os.path.join(BASE, sub)
    if p not in sys.path:
        sys.path.insert(0, p)
sys.path.insert(0, os.path.expanduser("~/g1_gamma"))
import decode
import step2_precompute as SP

RNG = random.Random(20260710)


def _block(concept, shown):
    return "%s: %s %s %s %s %s. " % (concept, shown[0], shown[1], shown[2], shown[3], shown[4])


def _lenmatch(bD, bDp):
    d = len(bD.encode()) - len(bDp.encode())
    if d > 0:
        bDp = bDp[:-1] + (" " * d) + " "
    elif d < 0:
        bD = bD[:-1] + (" " * (-d)) + " "
    return bD, bDp


def _fwd(W, text):
    tok = np.array([b for b in text.encode("utf-8", "ignore")], dtype=np.float64)
    T = len(tok)
    yn, logits = decode.clm_forward_hidden_logits(W, tok, T)
    return yn.astype(np.float16), logits.astype(np.float16), tok.astype(np.int16)


def make_triple(concepts, names, c):
    kws = concepts[c]
    shown = RNG.sample(kws, 5)
    unshown = [k for k in kws if k not in shown]
    retrieval = RNG.random() < 0.3                       # Fable: flip to 30/70 retrieval/associative
    target = RNG.choice(shown) if retrieval else RNG.choice(unshown)
    filler = RNG.choice(SP._FILLERS)
    gap = SP._gap(RNG.randint(128, 224))
    for _ in range(20):
        stem = RNG.choice(SP._STEMS)
        if not any((k[:3] in stem) for k in kws):
            break
    bD = _block(c, shown)
    # 2 donors != c, whose block does NOT contain target as substring
    donors = []
    pool = [n for n in names if n != c]
    RNG.shuffle(pool)
    for dp in pool:
        dshown = RNG.sample(concepts[dp], 5)
        bDp = _block(dp, dshown)
        if target in bDp or c in bDp:
            continue
        donors.append((dp, bDp))
        if len(donors) == 2:
            break
    if len(donors) < 2:
        return None
    pre_tail = gap + stem
    # anti-copy for associative: target must not appear in match pre-region
    if not retrieval and (target in (filler + bD + pre_tail)):
        return None
    variants = []
    bD_m, _ = _lenmatch(bD, donors[0][1])              # normalize bD length vs first donor
    # length-match ALL blocks to the max block byte length
    blocks = [bD] + [d[1] for d in donors]
    maxlen = max(len(b.encode()) for b in blocks)
    blocks = [(b[:-1] + (" " * (maxlen - len(b.encode()))) + " ") if len(b.encode()) < maxlen else b for b in blocks]
    texts = [filler + b + pre_tail + target for b in blocks]
    # target span byte positions (identical across variants: blocks equal byte length)
    pre = filler + blocks[0] + pre_tail
    span_lo = len(pre.encode()); span_hi = span_lo + len(target.encode())
    return texts, span_lo, span_hi, retrieval, target, [c] + [d[0] for d in donors]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.expanduser("~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm"))
    ap.add_argument("--per", type=int, default=9, help="items per concept")
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/step2_paired"))
    ap.add_argument("--maxT", type=int, default=560)
    import evaluate as E
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    train, val = SP.build_concepts()
    names = list(train)
    print("train concepts=%d (val %d held out as donors too)" % (len(train), len(val)), flush=True)
    W = E._Mouth(a.ckpt).W
    man = {"train": names, "val": list(val), "items": []}
    n = 0
    for c in names:
        made = 0; tries = 0
        while made < a.per and tries < a.per * 4:
            tries += 1
            tr = make_triple(train, names, c)
            if tr is None:
                continue
            texts, span_lo, span_hi, retr, target, cs = tr
            if max(len(t.encode()) for t in texts) > a.maxT:
                continue
            ynm, bm, tm = _fwd(W, texts[0])
            yn0, b0, t0 = _fwd(W, texts[1])
            yn1, b1, t1 = _fwd(W, texts[2])
            fn = "it_%06d.npz" % n
            np.savez(os.path.join(a.out, fn), yn_m=ynm, base_m=bm, tok_m=tm,
                     yn_s0=yn0, base_s0=b0, tok_s0=t0, yn_s1=yn1, base_s1=b1, tok_s1=t1,
                     meta=np.array([span_lo, span_hi, int(retr)], dtype=np.int32))
            man["items"].append({"fn": fn, "concept": c, "target": target, "retrieval": bool(retr), "donors": cs[1:]})
            n += 1; made += 1
            if n % 50 == 0:
                print("  paired %d items" % n, flush=True)
    json.dump(man, open(os.path.join(a.out, "manifest.json"), "w"))
    print("DONE paired %d items -> %s" % (n, a.out), flush=True)


if __name__ == "__main__":
    main()
