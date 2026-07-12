#!/usr/bin/env python3
"""gen_spangeom.py — SPAN-GEOM prompt set (H_9287 stage-1, Fable design).

Tests the morpheme-lever premise ONE LEVEL BELOW the earn-seal: does the frozen base 303M form a
stem-level NEG equivalence class at the SPAN level (pooled over the negation stem's own bytes)?
LOSO span classifier trains on 안/않 spans vs position-matched pre-verbal adverb spans, tests held-out
못/아니 spans — byte-identity can't transfer under LOSO so a hit requires a shared NEG span feature.

Each prompt is a wild ko sentence TRUNCATED right after the stem (+R chars) so the stem reliably lands
in the last --win bytes; the stem string is recorded so span byte-rows are recomputable post-dump.
Classes: neg stems (an/anh/mot/ani) · adv (position-matched pre-verbal 잘/좀/다시/자주/많이) ·
rand (freq-matched random content syllable, non-neg non-adverb). Korean-aware disambiguation per stem.

out prompts.json = {"items":[{"id":"<cls>_<i>","prompt":<truncated>,"cue":<stem/adv/syllable>,"cls":<cls>}]}.
"""
import json
import os
import re
import sys

OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "spangeom_prompts.json"
N_PER = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 300
R = 2                       # right-context chars kept after the cue
MINLEN, MAXLEN = 8, 80
CACHE_DIR = os.path.expanduser("~/g1_natem")
SRC = ["ratings_train.txt", "ratings_test.txt"]
BASE = "https://raw.githubusercontent.com/e9t/nsmc/master/"

# neg-stem cue matchers with Korean-aware disambiguation. Each: (cls, compiled-finditer, validator).
NEG = {
    # 안 + space + predicate; exclude locative noun 안(에/의/으로/쪽/에서)
    "an":  (re.compile(r"안\s+[가-힣]"), lambda s, i: s[i:i+2] == "안 " and not re.match(r"안(에|의|으로|쪽|에서)", s[i:i+3])),
    # 지 않 — always negation
    "anh": (re.compile(r"않[가-힣]?"), lambda s, i: True),
    # 못 + space + predicate (can't); exclude noun particles 못이/못을/못에
    "mot": (re.compile(r"(?<!잘)못\s+[가-힣]"), lambda s, i: s[i:i+2] == "못 " and (i == 0 or s[i-1] != "잘") and not re.match(r"못(이|을|에|과|도)", s[i:i+3])),
    # 아니 + copula/connective form
    "ani": (re.compile(r"아니(다|라|야|에|었|겠|지|었|네)"), lambda s, i: True),
}
ADVERBS = ["잘", "좀", "다시", "자주", "많이"]     # pre-verbal, same slot as 안/못
NEG_ANY = re.compile(r"않|안\s+[가-힣]|못\s+[가-힣]|아니(다|라|야|에|었|겠|지|네)|없")


def load():
    rows = []
    for fn in SRC:
        p = os.path.join(CACHE_DIR, fn)
        if not os.path.exists(p):
            os.makedirs(CACHE_DIR, exist_ok=True)
            import urllib.request
            urllib.request.urlretrieve(BASE + fn, p)
        with open(p, encoding="utf-8") as f:
            next(f, None)
            for line in f:
                pp = line.rstrip("\n").split("\t")
                if len(pp) == 3 and MINLEN <= len(pp[1]) <= MAXLEN:
                    rows.append(pp[1])
    return rows


def truncate_after(s, end_char_idx):
    """Keep s[:end_char_idx+R] so the cue + R chars is the tail."""
    return s[:min(len(s), end_char_idx + R)]


def main():
    rows = load()
    items = []
    seen = set()

    def add(cls, cue, prompt):
        prompt = prompt.strip()
        key = (cls, prompt)
        if prompt and key not in seen and len(prompt) >= 4:
            seen.add(key)
            items.append({"id": "%s_%d" % (cls, sum(1 for it in items if it["cls"] == cls)),
                          "prompt": prompt, "cue": cue, "cls": cls})

    # neg stems
    for cls, (rx, ok) in NEG.items():
        n = 0
        for s in rows:
            if n >= N_PER:
                break
            m = rx.search(s)
            if not m:
                continue
            i = m.start()
            cue = "안" if cls == "an" else "못" if cls == "mot" else "않" if cls == "anh" else "아니"
            ci = s.find(cue, i)
            if ci < 0 or not ok(s, ci):
                continue
            end = ci + len(cue)
            add(cls, cue, truncate_after(s, end))
            n += 1
    # position-matched adverbs (one class 'adv', balanced across the 5 adverbs)
    n = 0
    ai = 0
    for s in rows:
        if n >= N_PER:
            break
        adv = ADVERBS[ai % len(ADVERBS)]
        pat = adv + " " if len(adv) == 1 else adv
        idx = s.find(pat)
        if idx >= 0 and not NEG_ANY.search(s[:idx + len(adv)]):
            add("adv", adv, truncate_after(s, idx + len(adv)))
            n += 1
            ai += 1
    # freq-matched random content-syllable control (non-neg, non-adverb, mid-sentence Hangul syllable)
    n = 0
    import random
    rng = random.Random(7)
    for s in rows:
        if n >= N_PER:
            break
        cand = [j for j, ch in enumerate(s) if "가" <= ch <= "힣" and 2 <= j <= len(s) - 3]
        if not cand:
            continue
        j = rng.choice(cand)
        ch = s[j]
        if ch in ("안", "못", "않") or ch in "".join(ADVERBS) or NEG_ANY.search(s[:j + 1]):
            continue
        add("rand", ch, truncate_after(s, j + 1))
        n += 1

    json.dump({"items": [{"id": it["id"], "prompt": it["prompt"], "cue": it["cue"], "cls": it["cls"]}
                         for it in items]},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    from collections import Counter
    c = Counter(it["cls"] for it in items)
    print("SPAN-GEOM: %d items | %s -> %s" % (len(items), dict(c), OUT))


if __name__ == "__main__":
    main()
