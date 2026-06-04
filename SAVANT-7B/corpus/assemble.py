#!/usr/bin/env python3
# Assemble the SAVANT 5-lang rung0 starter corpus from Gutenberg PD + Wikipedia.
# Strip Gutenberg boilerplate, dedup lines, balance languages, write one file.
import glob, os, re, hashlib

OUT = "savant_5lang_starter.txt"

def strip_gutenberg(text):
    # remove the *** START/END OF ... *** boilerplate blocks
    start = re.search(r"\*\*\*\s*START OF.*?\*\*\*", text, re.S)
    end = re.search(r"\*\*\*\s*END OF.*?\*\*\*", text, re.S)
    s = start.end() if start else 0
    e = end.start() if end else len(text)
    return text[s:e]

# per-language file groups (lang -> list of source files)
GROUPS = {
 "en": ["en_austen_1342.txt","en_doyle_1661.txt","en_melville_2701.txt","wiki_en.txt"],
 "fr": ["fr_dumas_17989.txt","fr_flaubert_14155.txt","fr_hugo_135.txt","fr_verne_800.txt","wiki_fr.txt"],
 "de": ["de_goethe_2229.txt","de_grimm_22555.txt","de_kafka_22367.txt","de_nietzsche_7205.txt","wiki_de.txt"],
 "es": ["es_cervantes_2000.txt","es_galdos_16109.txt","wiki_es.txt"],
 "ru": ["ru_pushkin_cyr.txt","wiki_ru.txt","ru_wiki_extracts.txt"],
}
# Gutenberg files get boilerplate stripped; wiki files do not.
WIKI = lambda f: f.startswith("wiki_") or f.endswith("_extracts.txt")

per_lang_lines = {}
for lang, files in GROUPS.items():
    lines = []
    seen = set()
    for f in files:
        if not os.path.exists(f):
            continue
        raw = open(f, "r", encoding="utf-8", errors="replace").read()
        if not WIKI(f):
            raw = strip_gutenberg(raw)
        for ln in raw.split("\n"):
            ln = ln.strip()
            if len(ln) < 12:        # drop near-empty / single-word lines
                continue
            h = hashlib.md5(ln.encode()).hexdigest()
            if h in seen:           # exact-line dedup within language
                continue
            seen.add(h); lines.append(ln)
    per_lang_lines[lang] = lines
    nb = sum(len(l.encode()) for l in lines)
    print(f"{lang}: {len(lines)} lines, {nb} bytes (pre-balance)")

# language balance: cap each language at the min-language line count * 3 so no
# single language dominates (en/fr have far more Gutenberg text than ru).
counts = {k: len(v) for k, v in per_lang_lines.items()}
# Fixed per-language cap: en/fr/de/es are Gutenberg-rich, ru is thin (Cyrillic is
# scarce in reachable PD/wiki sources — HONEST). Cap the rich langs so they don't
# swamp the corpus, but keep ALL of the thin Russian. rung1 full-dump recipe fixes ru.
cap = 2500
import random
random.seed(42)
final = []
for lang, lines in per_lang_lines.items():
    take = lines[:cap] if len(lines) > cap else lines
    final.extend((lang, l) for l in take)
random.shuffle(final)   # interleave languages
with open(OUT, "w", encoding="utf-8") as f:
    for lang, l in final:
        f.write(l + "\n")
nb = os.path.getsize(OUT)
sha = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"\nSTARTER {OUT}: {len(final)} lines, {nb} bytes, sha256={sha}")
# per-lang final balance
bal = {}
for lang, l in final: bal[lang] = bal.get(lang, 0) + 1
print("balance:", bal)
