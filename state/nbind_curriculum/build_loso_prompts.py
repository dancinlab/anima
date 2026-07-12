#!/usr/bin/env python3
"""build_loso_prompts.py — Probe A (LOSO-NEG) prompt set for the γ earn-seal (Fable GAMMA_NEWANGLE).

Tests whether a STEM-INVARIANT negation feature exists in the BASE 303M substrate: mine wild NSMC
sentences carrying each negation STEM (안/않/못/아니) = neg class, + affirmative (no-negation) = plain
class. A LOSO linear probe on the frozen dump then asks: does neg-vs-plain classify a HELD-OUT stem
(못, 아니) it never trained on? If yes -> the invariant exists (γ measure-side may be addressable);
if no -> earned terminal (substrate has no stem-invariant NEG to abstract over).

Output prompts.json = {"items":[{"id":"<stem|plain>_<i>", "prompt": <wild sentence, right-aligned>}]}.
Balanced per stem. Byte-confound note (Fable): 안(EC95 88)/않(EC95 8A) share 2/3 UTF-8 bytes, so the
INFORMATIVE held-out folds are 못 and 아니. Surface-matched non-NEG control class = sentences with an
adverb (매우/정말/아주 …) but NO negation — same "modifier present" surface, different function.
"""
import json
import os
import re
import sys

NSMC_TEST = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt"
CACHE = os.path.expanduser("~/g1_natem/nsmc_ratings_test.txt")
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "loso_prompts.json"
N_PER = 60          # per class (stem neg / plain / adv-control)
WIN = 24            # right-align window (matches --win 24); keep prompt tail informative

STEM_RE = {
    "an":  re.compile(r"(^|\s)안\s+[가-힣]"),
    "anh": re.compile(r"지\s*않"),
    "mot": re.compile(r"(^|\s)못\s+[가-힣]"),
    "ani": re.compile(r"아니(다|라|야|에|었)"),
}
ANY_NEG = re.compile(r"지\s*않|(^|\s)안\s+[가-힣]|(^|\s)못\s+[가-힣]|아니(다|라|야|에|었)|없")
ADV_RE = re.compile(r"(매우|정말|아주|너무|진짜|완전)\s")


def load():
    p = CACHE
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        import urllib.request
        urllib.request.urlretrieve(NSMC_TEST, p)
    rows = []
    with open(p, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3 and 6 <= len(pp[1]) <= 60:
                rows.append(pp[1])
    return rows


def tail(s):
    return s[-(WIN):] if len(s) > WIN else s


def main():
    rows = load()
    items = []
    seen = set()

    def add(cid, s):
        s = s.strip()
        if s and s not in seen:
            seen.add(s)
            items.append({"id": cid, "prompt": tail(s)})

    # neg classes (one per stem)
    for stem, rx in STEM_RE.items():
        n = 0
        for s in rows:
            if n >= N_PER:
                break
            if rx.search(s):
                add("%s_%d" % (stem, n), s)
                n += 1
    # plain (no negation, no 없)
    n = 0
    for s in rows:
        if n >= N_PER:
            break
        if not ANY_NEG.search(s) and not ADV_RE.search(s):
            add("plain_%d" % n, s)
            n += 1
    # adv-control (modifier present, NO negation) — surface-matched non-NEG
    n = 0
    for s in rows:
        if n >= N_PER:
            break
        if ADV_RE.search(s) and not ANY_NEG.search(s):
            add("adv_%d" % n, s)
            n += 1

    json.dump({"items": items}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    from collections import Counter
    c = Counter(it["id"].rsplit("_", 1)[0] for it in items)
    print("LOSO prompts: %d total | %s -> %s" % (len(items), dict(c), OUT))


if __name__ == "__main__":
    main()
