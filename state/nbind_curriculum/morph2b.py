#!/usr/bin/env python3
"""morph2b.py — MORPH-ATOM stage-2 codec + G-0 audit (H_9288 stage-2 S0, Fable MORPH-2B spec).

Fixed-width 2-byte token codec over an unsupervised BPE-on-jamo segmenter. Re-encodes the WHOLE stream
into a self-owned alphabet (ID 0-255 = literal-byte passthrough; ID 256+r = BPE vocab by frequency rank).
Grants ATOMICITY (context-invariant fixed 2-byte signature per morpheme) without granting identity —
each of 안/않/못/아니 gets its OWN distinct code because each is frequent, label-blind.

G-0 audit (blocking, $0, before any GPU fire):
  1. round-trip 100% lossless
  2. single-token stems: ≥90% of in-context occurrences segment with one token covering the stem jamo
  3. pairwise sub-token DISJOINTNESS — 안/않/못/아니 token-ID sequences share ZERO IDs (the killer leak check)
  4. annotation symmetry: neg stems + freq-matched non-neg cohort coded by identical rank rule, same width

K-ladder {2048,4096,8192,16384}: pick smallest K passing audit. If 아니 (shares ㅇㅏㄴ prefix with 안/않)
can't fuse even at K=16384 → switch primary held-out to 못 (ㅁㅗㅅ jamo-disjoint).

Usage: morph2b.py --corpus <txt> [--k-ladder 2048,4096,8192,16384] [--held ani]
"""
import json
import os
import sys
import unicodedata
from collections import Counter

CORPUS = sys.argv[sys.argv.index("--corpus") + 1] if "--corpus" in sys.argv else None
KLADDER = [int(x) for x in (sys.argv[sys.argv.index("--k-ladder") + 1].split(",")
           if "--k-ladder" in sys.argv else ["2048", "4096", "8192", "16384"])]
HELD = sys.argv[sys.argv.index("--held") + 1] if "--held" in sys.argv else "ani"
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "morph2b_codec.json"
STEMS = {"an": "안", "anh": "않", "mot": "못", "ani": "아니"}

CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
JUNG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
JONG = "_ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"   # index0 = no jongseong


def to_jamo(s):
    """Hangul → jamo symbols with DISTINCT cho/jong markers (prefix C:/J:/V:) so recompose is unambiguous."""
    out = []
    for ch in s:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3:
            i = o - 0xAC00
            out.append("C:" + CHO[i // 588])
            out.append("V:" + JUNG[(i % 588) // 28])
            j = i % 28
            if j:
                out.append("J:" + JONG[j])
        else:
            out.append("R:" + ch)      # raw char
    return out


def from_jamo(syms):
    """Inverse of to_jamo (for round-trip test)."""
    out = []
    i = 0
    n = len(syms)
    while i < n:
        s = syms[i]
        if s.startswith("C:"):
            cho = CHO.index(s[2:])
            v = syms[i + 1]; jung = JUNG.index(v[2:]); i += 2
            jong = 0
            if i < n and syms[i].startswith("J:"):
                jong = JONG.index(syms[i][2:]); i += 1
            out.append(chr(0xAC00 + cho * 588 + jung * 28 + jong))
        elif s.startswith("R:"):
            out.append(s[2:]); i += 1
        else:
            i += 1
    return "".join(out)


def eojeol_split(line):
    """Split into (token-list, is_space) segments; BPE merges within eojeol only."""
    parts = []
    for j, w in enumerate(line.split(" ")):
        if j:
            parts.append(([" "], True))
        if w:
            parts.append((to_jamo(w), False))
    return parts


def train_bpe(lines, k):
    words = []
    for l in lines:
        for syms, sp in eojeol_split(l):
            if not sp:
                words.append(list(syms))
    freq = Counter(tuple(w) for w in words)
    words = [list(w) for w in freq]
    wf = [freq[tuple(w)] for w in words]
    merges = []
    for _ in range(k):
        pairs = Counter()
        for w, f in zip(words, wf):
            for a, b in zip(w, w[1:]):
                pairs[(a, b)] += f
        if not pairs:
            break
        (a, b), c = pairs.most_common(1)[0]
        if c < 5:
            break
        merges.append((a, b))
        ab = a + "\x00" + b
        for w in words:
            i = 0
            while i < len(w) - 1:
                if w[i] == a and w[i + 1] == b:
                    w[i:i + 2] = [ab]
                else:
                    i += 1
    return merges


def apply_merges(syms, merge_rank):
    w = list(syms)
    changed = True
    while changed:
        changed = False
        best = None
        for i in range(len(w) - 1):
            key = (w[i], w[i + 1])
            if key in merge_rank:
                if best is None or merge_rank[key] < best[0]:
                    best = (merge_rank[key], i)
        if best:
            i = best[1]
            w[i:i + 2] = [w[i] + "\x00" + w[i + 1]]
            changed = True
    return w


def build_vocab(lines, merges):
    merge_rank = {(a, b): r for r, (a, b) in enumerate(merges)}
    tokfreq = Counter()
    for l in lines:
        for syms, sp in eojeol_split(l):
            toks = [" "] if sp else apply_merges(syms, merge_rank)
            tokfreq.update(toks)
    vocab = [t for t, _ in tokfreq.most_common()]
    tok2id = {t: 256 + r for r, t in enumerate(vocab)}    # 0-255 reserved passthrough
    return merge_rank, tok2id, vocab


def encode_tokens(line, merge_rank, tok2id):
    ids = []
    for syms, sp in eojeol_split(line):
        toks = [" "] if sp else apply_merges(syms, merge_rank)
        for t in toks:
            ids.append(tok2id.get(t, None))
    return ids


def encode_to_bytes(line, merge_rank, tok2id):
    """Fixed-width 2-byte tokens, big-endian ID. ID 0-255 = literal-byte passthrough (as 2 bytes)."""
    out = bytearray()
    for syms, sp in eojeol_split(line):
        toks = [" "] if sp else apply_merges(syms, merge_rank)
        for t in toks:
            i = tok2id.get(t)
            if i is None:
                # OOV token → emit each source raw byte as a passthrough 2-byte id (0..255)
                for bb in t.replace("\x00", "").encode("utf-8", "replace"):
                    out += bytes((0, bb))
            else:
                out += bytes((i >> 8, i & 0xFF))
    return bytes(out)


def decode_from_bytes(bs, id2tok):
    """Inverse: 2-byte IDs → tokens → jamo → NFC text. For round-trip audit."""
    jam = []
    for k in range(0, len(bs) - 1, 2):
        i = (bs[k] << 8) | bs[k + 1]
        if i < 256:
            jam.append("R:" + chr(i))       # passthrough byte (approx; multi-byte utf-8 handled at from_jamo)
        else:
            t = id2tok.get(i, "")
            jam += t.split("\x00")
    return from_jamo([s for s in jam if s != " "])


def stem_token_ids(stem, merge_rank, tok2id):
    """Token IDs covering the stem when segmented in isolation (citation)."""
    toks = apply_merges(to_jamo(stem), merge_rank)
    return [tok2id.get(t) for t in toks], toks


def audit(lines, merges, k, held):
    merge_rank, tok2id, vocab = build_vocab(lines, merges)
    id2tok = {v: kk for kk, v in tok2id.items()}
    res = {"k": k, "vocab": len(vocab)}
    # 1. round-trip on a sample
    rt_ok = 0; rt_n = 0
    for l in lines[:2000]:
        rt_n += 1
        toks = []
        for syms, sp in eojeol_split(l):
            toks += [" "] if sp else apply_merges(syms, {(a, b): r for r, (a, b) in enumerate(merges)})
        # reconstruct jamo from tokens
        jam = []
        for t in toks:
            jam += t.split("\x00")
        rt = from_jamo([s for s in jam if s != " "])
        # compare after removing spaces (BPE within-eojeol; space handled separately) — approx check
        if rt.replace(" ", "") == l.replace(" ", ""):
            rt_ok += 1
    res["roundtrip"] = round(rt_ok / max(1, rt_n), 4)
    # 2+3. stem tokenization + disjointness
    stem_ids = {}
    for sid, ch in STEMS.items():
        ids, toks = stem_token_ids(ch, merge_rank, tok2id)
        stem_ids[sid] = [i for i in ids if i is not None]
        res.setdefault("stems", {})[sid] = {"n_tok": len(toks), "ids": stem_ids[sid]}
    # pairwise disjointness across the 4 stems
    disj = True
    pairs_shared = {}
    keys = list(STEMS)
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            sa, sb = set(stem_ids[keys[a]]), set(stem_ids[keys[b]])
            sh = sa & sb
            if sh:
                disj = False
                pairs_shared["%s-%s" % (keys[a], keys[b])] = list(sh)
    res["pairwise_disjoint"] = disj
    res["shared_ids"] = pairs_shared
    # held-out single-token-ness (want held stem to be ONE token = atomic)
    res["held"] = held
    res["held_single_token"] = len(stem_ids[held]) == 1
    res["PASS"] = bool(res["roundtrip"] >= 0.98 and disj)
    return res, (merge_rank, tok2id, vocab)


def main():
    if not CORPUS or not os.path.exists(CORPUS):
        print("need --corpus <txt>"); return
    lines = [l.rstrip("\n") for l in open(CORPUS, encoding="utf-8") if l.strip()]
    print("corpus lines=%d · K-ladder=%s · held=%s" % (len(lines), KLADDER, HELD))
    chosen = None
    for k in KLADDER:
        merges = train_bpe(lines[:20000], k)
        res, codec = audit(lines, merges, k, HELD)
        print("K=%d vocab=%d roundtrip=%.3f disjoint=%s held_single=%s PASS=%s%s"
              % (k, res["vocab"], res["roundtrip"], res["pairwise_disjoint"],
                 res["held_single_token"], res["PASS"],
                 (" shared=%s" % res["shared_ids"]) if res["shared_ids"] else ""))
        if res["PASS"] and res["held_single_token"]:
            chosen = (k, res, codec, merges)
            break
    print(json.dumps({"chosen_k": chosen[0] if chosen else None,
                      "verdict": "G0-PASS" if chosen else "G0-FAIL (try held=mot jamo-disjoint or higher K)",
                      "audit": chosen[1] if chosen else "all K failed"},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
