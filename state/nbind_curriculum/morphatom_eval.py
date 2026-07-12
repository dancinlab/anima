#!/usr/bin/env python3
"""morphatom_eval.py — MORPH-ATOM stage-2 codec-aware forced-choice scorer (H_9288 S1).

Same engine-native forward as cli/evaluate.py interaction-lift (clm._fwd_logits, evaluate.py:1265-1277)
but scores CODEC-encoded label continuations for the codec arms (M/C2/C3). For each eval item:
  NLL(seed+gold) vs NLL(seed+counterfactual)  → correct if NLL(gold) < NLL(cf); D-acc = mean(correct).
Byte-level NLL over the label's own token bytes (V=256). Raw arm (C1) uses utf-8 (clm._seed_to_tok path).

Usage: morphatom_eval.py <ckpt.clm> --panel <eval_fX.json> --codec <codec.json|none> [--win 96] [--out f.json]
  --codec none  → RAW utf-8 arm (C1).  --codec codec.json → MORPH-2B encode (M/C2/C3).
Imports anima_py's clm forward (installed on pod) + morph2b (shipped alongside).
"""
import json
import math
import os
import sys
import numpy as np

# anima_py engine-native forward (installed on the pod). decode.py does bare `import slw`/`import clml`,
# so its OWN dir must be on sys.path (the same resolution cli/evaluate.py sets up for `import decode`).
try:
    import anima_py.core.decode as _d
    sys.path.insert(0, os.path.dirname(_d.__file__))
    from anima_py.core import decode as clm
except Exception:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import decode as clm       # fallback: core/decode.py on path

import morph2b as MB

CKPT = sys.argv[1]
PANEL = sys.argv[sys.argv.index("--panel") + 1]
CODEC = sys.argv[sys.argv.index("--codec") + 1] if "--codec" in sys.argv else "none"
WIN = int(sys.argv[sys.argv.index("--win") + 1]) if "--win" in sys.argv else 96
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None


def load_codec():
    """Rebuild encoder from codec.json (needs merges+tok2id — regenerate from corpus if absent)."""
    d = json.load(open(CODEC, encoding="utf-8"))
    if "merges" in d and "tok2id" in d:
        merge_rank = {tuple(k.split("\t")): r for r, k in enumerate(d["merges"])}
        tok2id = {k: v for k, v in d["tok2id"].items()}
        return merge_rank, tok2id, d.get("shared_collapse")
    # codec.json from gen_morphatom_s1 only stored ids; retrain deterministically from --corpus
    corpus = d.get("corpus") or os.path.join(os.path.dirname(CODEC), "morph_corpus.txt")
    lines = [l.rstrip("\n") for l in open(corpus, encoding="utf-8") if l.strip()][:d.get("cpt_lines", 120000)]
    merges = MB.train_bpe(lines[:20000], d["k"])
    merge_rank, tok2id, _ = MB.build_vocab(lines, merges)
    return merge_rank, tok2id, d.get("shared_collapse")


def tok_from_bytes(bs, T):
    """Right-align raw bytes into a length-T float tok window, left-pad 32.0 (matches _seed_to_tok)."""
    tok = np.full(T, 32.0)
    n = min(len(bs), T)
    for p in range(n):
        tok[T - n + p] = float(bs[-n + p])
    return tok


def nll_tail(W, tok, T, n_score):
    logits = clm._fwd_logits(W, tok, T)
    lo = max(0, T - 1 - n_score)
    s = 0.0; c = 0
    for i in range(lo, T - 1):
        row = logits[i]; m = float(np.max(row))
        lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
        s += lse - float(row[int(tok[i + 1])]); c += 1
    return s / max(1, c)


def main():
    W = clm.clm_load_weights(CKPT)
    if not W.get("ok"):
        print("ERROR ckpt not decodable"); return 1
    panel = json.load(open(PANEL, encoding="utf-8"))["items"]
    use_codec = CODEC != "none"
    if use_codec:
        merge_rank, tok2id, shared = load_codec()
        allstem = set()
        cj = json.load(open(CODEC, encoding="utf-8"))
        for v in cj.get("stem_ids", {}).values(): allstem |= set(v)
        min_stem = min(allstem) if allstem else None

        def enc(t):
            b = bytearray(MB.encode_to_bytes(t, merge_rank, tok2id))
            if shared and min_stem is not None:      # C3: collapse stem ids
                for k in range(0, len(b) - 1, 2):
                    i = (b[k] << 8) | b[k + 1]
                    if i in allstem: b[k], b[k + 1] = min_stem >> 8, min_stem & 0xFF
            return bytes(b)
    else:
        enc = lambda t: t.encode("utf-8", "surrogateescape")

    correct = 0; n = 0; margins = []
    n_score = 4 if use_codec else 3       # codec label ≈2 tokens×2B; raw "긍정."≈3B tail
    for it in panel:
        seed, gold, cf = it["seed"], it["gold"], it["counterfactual"]
        tg = tok_from_bytes(enc(seed + gold), WIN)
        tc = tok_from_bytes(enc(seed + cf), WIN)
        ng = nll_tail(W, tg, WIN, n_score)
        nc = nll_tail(W, tc, WIN, n_score)
        margins.append(nc - ng)
        correct += int(ng < nc); n += 1
    dacc = correct / max(1, n)
    res = {"ckpt": os.path.basename(CKPT), "codec": os.path.basename(CODEC) if use_codec else "raw",
           "panel": os.path.basename(PANEL), "n": n, "d_acc": round(dacc, 4),
           "mean_margin": round(float(np.mean(margins)), 4)}
    print(json.dumps(res, ensure_ascii=False))
    if OUT:
        json.dump({**res, "margins": [round(m, 4) for m in margins]}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
