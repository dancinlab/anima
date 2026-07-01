#!/usr/bin/env python3
"""clean_split.py — language-split a mixed (5lang) byte corpus into CLEAN ko / en
streams for the anima 4-cell register ({ko·en}x{general·SNS}, a_chat_registers).

The prior "en" cells were 5lang mixtures (de/es/fr/en/ko) — only ~20% en. This
splitter keeps ONLY confidently-ko or confidently-en lines and DROPS de/es/fr/
other (chat standard languages are ko·en only). Dedups exact-duplicate lines and
drops broken/too-short lines.

Detection = script + stopword fingerprint (torch-free, deterministic, no langdetect
dependency). ko = any Hangul. en = Latin script whose stopword fingerprint is en
AND en stopword hits strictly dominate the other Latin languages (avoids the
header/caption ambiguity that inflates en in a naive count).

Usage:
  python clean_split.py --in FILE [FILE ...] --ko OUT_KO.txt --en OUT_EN.txt
      [--min-len N] [--en-min-words N] [--report]
"""
import argparse
import re
import sys

HANGUL = re.compile(r'[가-힣ᄀ-ᇿ]')
KANA   = re.compile(r'[぀-ヿ]')
CJK    = re.compile(r'[一-鿿]')
CYR    = re.compile(r'[Ѐ-ӿ]')
LATIN  = re.compile(r'[A-Za-z]')

SW = {
 'en': set("the of and to in is are was were a an that for with as it this be on by not or "
           "from at he she they we you have has had will would can could".split()),
 'de': set("der die und zu das ist eine den von mit sich auf für nicht ein dem als auch ich "
           "du wir sie er es war haben werden".split()),
 'es': set("el la de que en los las un una con por para no se su del al es muy yo tu ella "
           "ellos somos estar tener".split()),
 'fr': set("le la et les des un une que dans pour pas qui sur est au avec ce il je tu nous "
           "vous elle ils sont avoir être".split()),
}


def latin_lang(line: str):
    """Return ('en'|'de'|'es'|'fr'|'latin-other', dominance) for a Latin line.
    dominance = en_hits - max(other-lang hits); >0 means en strictly dominates."""
    words = re.findall(r"[A-Za-z']+", line.lower())
    if not words:
        return 'latin-other', 0
    hits = {lg: sum(1 for w in words if w in sw) for lg, sw in SW.items()}
    best = max(hits, key=hits.get)
    if hits[best] == 0:
        return 'latin-other', 0
    other_max = max(v for k, v in hits.items() if k != best)
    return best, hits[best] - other_max


def classify(line: str, en_min_words: int):
    s = line.strip()
    if not s:
        return None
    if HANGUL.search(s):
        return 'ko'
    if KANA.search(s) or CJK.search(s) or CYR.search(s):
        return 'drop'          # ja/zh/cyr — not chat standard
    if LATIN.search(s):
        lg, dom = latin_lang(s)
        if lg == 'en' and dom >= 1 and len(re.findall(r"[A-Za-z']+", s)) >= en_min_words:
            return 'en'
        return 'drop'          # de/es/fr/latin-other → not a clean en line
    return 'drop'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infiles", nargs="+", required=True)
    ap.add_argument("--ko", required=True, help="output clean-ko path")
    ap.add_argument("--en", required=True, help="output clean-en path")
    ap.add_argument("--min-len", type=int, default=4,
                    help="drop lines shorter than this many chars (broken/noise)")
    ap.add_argument("--en-min-words", type=int, default=3,
                    help="a clean en line needs >= this many ascii words")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    seen_ko, seen_en = set(), set()
    ko_lines, en_lines = [], []
    stats = {'ko': 0, 'en': 0, 'drop': 0, 'dup': 0, 'short': 0}
    for path in a.infiles:
        with open(path, 'rb') as f:
            for raw in f:
                line = raw.decode('utf-8', 'replace')
                s = line.strip()
                if not s:
                    continue
                if len(s) < a.min_len:
                    stats['short'] += 1
                    continue
                c = classify(s, a.en_min_words)
                if c == 'ko':
                    h = hash(s)
                    if h in seen_ko:
                        stats['dup'] += 1; continue
                    seen_ko.add(h); ko_lines.append(s); stats['ko'] += 1
                elif c == 'en':
                    h = hash(s)
                    if h in seen_en:
                        stats['dup'] += 1; continue
                    seen_en.add(h); en_lines.append(s); stats['en'] += 1
                else:
                    stats['drop'] += 1

    with open(a.ko, 'w', encoding='utf-8') as f:
        f.write("\n".join(ko_lines) + ("\n" if ko_lines else ""))
    with open(a.en, 'w', encoding='utf-8') as f:
        f.write("\n".join(en_lines) + ("\n" if en_lines else ""))

    import os
    if a.report:
        print(f"  inputs: {a.infiles}")
        print(f"  ko: {stats['ko']} lines -> {a.ko} ({os.path.getsize(a.ko)} bytes)")
        print(f"  en: {stats['en']} lines -> {a.en} ({os.path.getsize(a.en)} bytes)")
        print(f"  dropped(non-ko/en): {stats['drop']}  dup: {stats['dup']}  "
              f"short(<{a.min_len}): {stats['short']}")


if __name__ == "__main__":
    main()
