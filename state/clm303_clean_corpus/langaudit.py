#!/usr/bin/env python3
"""Script/charset-based per-line language classifier + per-file composition.
ko = has Hangul; ja = Hiragana/Katakana (no Hangul); zh = CJK ideographs only;
cyr = Cyrillic; latin-* = Latin script disambiguated by stopword fingerprint
(en/de/es/fr) for the lines that are pure Latin (the 'is en really en' question)."""
import sys, re, unicodedata
from collections import Counter

HANGUL = re.compile(r'[가-힣ᄀ-ᇿ㄰-㆏]')
KANA   = re.compile(r'[぀-ヿ]')
CJK    = re.compile(r'[一-鿿]')
CYR    = re.compile(r'[Ѐ-ӿ]')
LATIN  = re.compile(r'[A-Za-zÀ-ɏ]')

# tiny stopword fingerprints to split Latin into en/de/es/fr
SW = {
 'en': set("the of and to in is are was a an that for with as it this be on by not or from".split()),
 'de': set("der die und zu in das ist eine den von mit sich auf für nicht ein dem als auch".split()),
 'es': set("el la de que y en los las un una con por para no se su lel del al es".split()),
 'fr': set("le la de et les des un une que dans pour pas qui sur est au avec ne se ce il".split()),
}

def latin_lang(line):
    words = re.findall(r"[A-Za-zÀ-ɏ']+", line.lower())
    if not words: return 'latin-other'
    best, bestc = 'latin-other', 0
    for lg, sw in SW.items():
        c = sum(1 for w in words if w in sw)
        if c > bestc: best, bestc = lg, c
    # require at least 1 stopword hit to claim a language, else latin-other
    return best if bestc >= 1 else 'latin-other'

def classify(line):
    s = line.strip()
    if not s: return None
    if HANGUL.search(s): return 'ko'
    if KANA.search(s):   return 'ja'
    if CYR.search(s):    return 'cyr'
    if CJK.search(s):    return 'zh'
    if LATIN.search(s):  return latin_lang(s)
    return 'other'

def audit(path, maxlines=0):
    cnt = Counter(); bytes_by = Counter(); n=0
    with open(path, 'rb') as f:
        for raw in f:
            try: line = raw.decode('utf-8','replace')
            except: continue
            lg = classify(line)
            if lg is None: continue
            cnt[lg]+=1; bytes_by[lg]+=len(raw); n+=1
            if maxlines and n>=maxlines: break
    return cnt, bytes_by, n

if __name__=='__main__':
    for path in sys.argv[1:]:
        cnt, bb, n = audit(path)
        tot_b = sum(bb.values()) or 1
        print(f"\n=== {path}  (non-blank lines={n}) ===")
        print(f"  {'lang':<12s}{'lines':>8s}{'line%':>8s}{'bytes':>12s}{'byte%':>8s}")
        for lg,_ in cnt.most_common():
            print(f"  {lg:<12s}{cnt[lg]:>8d}{100*cnt[lg]/n:>7.1f}%{bb[lg]:>12d}{100*bb[lg]/tot_b:>7.1f}%")
