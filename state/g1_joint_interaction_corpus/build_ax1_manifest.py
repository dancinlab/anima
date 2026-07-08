"""Build the AX1 content-pair window manifest for --interaction-lift (Fable §1 주력 축).

A = content word (freq-rank band), B = another content word, cell = a T-byte window where
both co-occur; the model's NLL over the continuation after the SECOND concept is the Y1
target. Unlike the PC-P controls, content-pairs are abundant -> not power-limited.

Emits {win, score_len, items:[{text, a, b}]} for `anima evaluate --interaction-lift`.
model-free build ($0, mini-OK). Frozen: band, K, window, seed.
"""
import sys, json, re
from collections import Counter

KO_GENERAL = ("/Users/mini/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-ko-general/"
              "snapshots/9f03495689d52fb50b5b7d8d673d77e38266afcc/anima-corpus-ko-general.txt")
T = 64
SCORE_LEN = 8
K = 24                 # top-K content words -> K×K grid
BAND = (100, 1000)     # freq-rank band (skip function words / rare)
MIN_WORD_BYTES = 6     # ~2 hangul syllables; skip particles
MAX_PER_CELL = 12
SEED = 7

WORD = re.compile(r"[가-힣]{2,}")


def content_vocab(text):
    c = Counter(WORD.findall(text))
    ranked = [w for w, _ in c.most_common() if len(w.encode()) >= MIN_WORD_BYTES]
    band = ranked[BAND[0]:BAND[1]]
    return band[:K]


def build(text, vocab):
    idx = {w: i for i, w in enumerate(vocab)}
    per_cell = {}
    # simple deterministic scan: sliding sentences by newline; find first two distinct vocab words
    for line in text.split("\n"):
        hits = [(m.start(), m.group()) for m in WORD.finditer(line) if m.group() in idx]
        if len(hits) < 2:
            continue
        (pa, wa), (pb, wb) = hits[0], hits[1]
        if wa == wb:
            continue
        a, b = idx[wa], idx[wb]
        key = (a, b)
        if len(per_cell.get(key, [])) >= MAX_PER_CELL:
            continue
        # window = T bytes ending after the SECOND concept + a little continuation
        end = pb + len(wb) + SCORE_LEN
        seg = line[max(0, end - T):end]
        if len(seg.encode()) < 8:
            continue
        per_cell.setdefault(key, []).append(seg)
    items = []
    for (a, b), segs in per_cell.items():
        for s in segs:
            items.append({"text": s, "a": a, "b": b})
    return items, per_cell


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else KO_GENERAL
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0     # 0 = all; >0 = smoke subset
    out = sys.argv[3] if len(sys.argv) > 3 else "state/g1_joint_interaction_corpus/ax1_manifest.json"
    with open(corpus, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    vocab = content_vocab(text)
    items, per_cell = build(text, vocab)
    if limit:
        items = items[:limit]
    json.dump({"win": T, "score_len": SCORE_LEN, "vocab": vocab, "items": items},
              open(out, "w"), ensure_ascii=False)
    print("vocab K=%d · cells filled=%d · windows=%d -> %s" %
          (len(vocab), len(per_cell), len(items), out))
