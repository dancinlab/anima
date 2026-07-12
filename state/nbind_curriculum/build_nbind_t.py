#!/usr/bin/env python3
"""build_nbind_t.py — C track (NBIND-T wild-natural transfer · NATEM STAGE-3 · H_9270 slot).

Reconstructs the FROZEN track-A training grid (gen_nbind.build, seed 4302) -> pol[p], plist,
held[p] — then mines the NSMC **test** split for natural (predicate x negation) surfaces of the
SAME trained predicates and emits two xbind manifests:
  W-T (phrase-wild): natural predicate surface slotted into the trained frame  이 영화 <surf> =>
  W-R (sentence-wild): the full natural review clause (truncated so p+n sits in the final 64 bytes)
gold_word = label_word[ pol(p) ^ flip(n) ]  — pol from the FROZEN training grid, NEVER the NSMC review label.
Balanced 4-cell {pol}x{flip} -> additive ceiling 0.5 by construction. V-F 32-byte shingle scan vs the
training corpus (=0 hits) + echo-guard. Held-out split = (p, flip-class) in the Latin-square held cells.

Run ON the track-A pod (has gen_nbind.py + nbind_train.txt). Output = nbind_t_{wt,wr}_manifest.json
consumed by `anima-py evaluate <clm> --xbind <manifest> --arm main`.
"""
import json
import os
import re
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
sys.path.insert(0, HERE)
import gen_nbind as G

SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 4302
OUTDIR = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else HERE
TRAIN_CORPUS = os.path.join(OUTDIR, "nbind_train.txt")
NSMC_TEST_URL = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt"
NSMC_TEST_CACHE = os.path.expanduser("~/g1_natem/nsmc_ratings_test.txt")
N_PER_CELL = 50
WIN = 64

RE_JIAN = re.compile(r"지\s*않")
RE_AN = re.compile(r"(^|\s)안\s+[가-힣]")
RE_JEON = re.compile(r"전혀")
RE_MOT = re.compile(r"(^|\s)못\s+[가-힣]")


def classify_flip(clause):
    """Return 1 (negated) / 0 (affirmative). Wild surface rule (Fable spec)."""
    neg = bool(RE_JIAN.search(clause) or RE_AN.search(clause) or RE_JEON.search(clause) or RE_MOT.search(clause))
    return 1 if neg else 0


def nsmc_test():
    p = NSMC_TEST_CACHE
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        import urllib.request
        urllib.request.urlretrieve(NSMC_TEST_URL, p)
    rows = []
    with open(p, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3 and pp[2] in ("0", "1"):
                rows.append(pp[1])
    return rows


def load_shingles(path, k=32):
    s = set()
    if not os.path.exists(path):
        return s
    raw = open(path, encoding="utf-8", errors="ignore").read().encode("utf-8")
    for i in range(0, max(0, len(raw) - k), 4):
        s.add(raw[i:i + k])
    return s


def main():
    rows_tr = G.load_nsmc(None)
    B = G.build(rows_tr, SEED)
    pol, plist, held = B["pol"], B["plist"], B["held"]
    predset = set(plist)
    held_flip = {p: {G.FLIP[fid] for fid in held[p]} for p in plist}
    shingles = load_shingles(TRAIN_CORPUS, 32)

    reviews = nsmc_test()
    rng = random.Random(SEED + 7)
    rng.shuffle(reviews)

    def blank():
        return {(0, 0): [], (0, 1): [], (1, 0): [], (1, 1): []}
    wt_pool, wr_pool = blank(), blank()

    for rv in reviews:
        for p in predset:
            if p not in rv:
                continue
            m = re.search(re.escape(p) + r"[가-힣]*", rv)
            if not m:
                continue
            end = m.end()
            clause = rv[max(0, end - 40):end].strip()
            if not clause:
                continue
            flip = classify_flip(clause)
            bit = pol[p] ^ flip
            gold_word = "긍정" if bit else "부정"
            toks = clause.split()
            surf_wt = " ".join(toks[-2:]) if len(toks) >= 2 else clause
            seed_wt = "이 영화 " + surf_wt + " => "
            seed_wr = "이 영화 " + rv[max(0, end - (WIN - 12)):end].strip() + " => "
            if gold_word in seed_wt or gold_word in seed_wr:
                continue
            wbytes = surf_wt.encode("utf-8")
            leak = any(wbytes[i:i + 32] in shingles for i in range(0, max(1, len(wbytes) - 32), 4))
            if leak:
                continue
            cell = (pol[p], flip)
            it = {"p": p, "form": ("wildneg" if flip else "wildpos"),
                  "a": p, "b": ("wildneg" if flip else "wildpos"),
                  "pol": pol[p], "flip": flip, "xor": bit,
                  "surf": surf_wt, "seed": seed_wt,
                  "gold": ("긍정." if bit else "부정."),
                  "counterfactual": ("부정." if bit else "긍정."),
                  "gold_word": gold_word,
                  "heldout": (flip in held_flip[p])}
            wt_pool[cell].append(it)
            wr = dict(it)
            wr["seed"] = seed_wr
            wr_pool[cell].append(wr)

    def split_balance(pool):
        held_items, seen_items = [], []
        for _cell, items in pool.items():
            rng.shuffle(items)
            held_items += [x for x in items if x["heldout"]][:N_PER_CELL]
            seen_items += [x for x in items if not x["heldout"]][:N_PER_CELL]
        return held_items, seen_items

    def emit(pool, tag):
        held_items, seen_items = split_balance(pool)
        percell = {c: sum(1 for x in held_items if (x["pol"], x["flip"]) == c)
                   for c in [(0, 0), (0, 1), (1, 0), (1, 1)]}
        man = {"format": "nbind-eval-v1",
               "note": "NBIND-T %s wild-natural transfer (NSMC test · gold=frozen training-grid pol). "
                       "balanced 4-cell -> additive ceiling 0.5." % tag,
               "gen": 8, "win": WIN,
               "heldout": held_items, "seen": seen_items}
        path = os.path.join(OUTDIR, "nbind_t_%s_manifest.json" % tag)
        json.dump(man, open(path, "w", encoding="utf-8"), ensure_ascii=False)
        mincell = min(percell.values()) if percell else 0
        verdict = "POWER-INVALID(<25/cell)" if mincell < 25 else "OK"
        print("[%s] heldout=%d seen=%d per-cell=%s -> %s -> %s"
              % (tag, len(held_items), len(seen_items), percell, verdict, path))
        return mincell

    print("frozen grid: |plist|=%d pol-balance=%d/%d" % (len(plist), sum(pol.values()), len(plist)))
    m_wt = emit(wt_pool, "wt")
    m_wr = emit(wr_pool, "wr")
    print("C-BUILD-DONE wt_mincell=%d wr_mincell=%d" % (m_wt, m_wr))


if __name__ == "__main__":
    main()
