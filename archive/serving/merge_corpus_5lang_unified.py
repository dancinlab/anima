#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_corpus_5lang_unified.py — unify wiki backbone + persona/SNS (5-lang, $0 CPU).

Merges two 5-language byte corpora into ONE unified corpus so a single model is
multilingual across ALL surfaces (wiki + SNS + persona):

  [ wiki_backbone_5lang.txt ]  (en/fr/de/es/ko encyclopedic, CC-BY-SA)
  [ persona_sns_corpus_5lang.txt ] (en/fr/de/es/ko persona×SNS, authored-synthetic)
        └── deterministic block-interleave ──▶ persona_sns_corpus_5lang_unified.txt

Ratio: ~50% wiki / ~50% persona-SNS by bytes (documented in the card). Blocks
(wiki articles ↔ persona dialogues, each a blank-line-separated unit) are
interleaved by a deterministic round-robin weighted to hold the byte ratio, so
the surfaces are mixed rather than concatenated in two halves.

Honest scope
------------
- wiki = real CC-BY-SA wikipedia (provenance carried). persona = authored-
  synthetic templated multilingual COVERAGE (NOT native-collected). The card
  states both licenses + the per-language byte split (no silent under-coverage).
- DETERMINISTIC: same inputs → same sha256.

Usage
-----
  python3 serving/merge_corpus_5lang_unified.py \
      --wiki serving/corpus/wiki_backbone_5lang.txt \
      --persona serving/corpus/persona_sns_corpus_5lang.txt \
      --out serving/corpus/persona_sns_corpus_5lang_unified.txt
"""

import argparse
import hashlib
import json
import os


def read_blocks(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [b for b in text.split("\n\n") if b.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default="serving/corpus/wiki_backbone_5lang.txt")
    ap.add_argument("--persona", default="serving/corpus/persona_sns_corpus_5lang.txt")
    ap.add_argument("--out", default="serving/corpus/persona_sns_corpus_5lang_unified.txt")
    args = ap.parse_args()

    wiki = read_blocks(args.wiki)
    persona = read_blocks(args.persona)
    wiki_b = sum(len(b.encode("utf-8")) for b in wiki)
    persona_b = sum(len(b.encode("utf-8")) for b in persona)

    # Deterministic byte-weighted round-robin interleave to hold ~50/50.
    # Advance whichever stream is currently under-represented by bytes.
    out_blocks = []
    wi = pi = 0
    acc_w = acc_p = 0
    while wi < len(wiki) or pi < len(persona):
        take_wiki = (acc_w <= acc_p and wi < len(wiki)) or pi >= len(persona)
        if take_wiki:
            b = wiki[wi]; wi += 1; acc_w += len(b.encode("utf-8"))
        else:
            b = persona[pi]; pi += 1; acc_p += len(b.encode("utf-8"))
        out_blocks.append(b)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n\n".join(out_blocks) + "\n\n")

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    total = wiki_b + persona_b
    print(json.dumps({
        "out": args.out, "bytes": size, "mb": round(size / 1048576, 3),
        "sha256": h.hexdigest(),
        "wiki_blocks": len(wiki), "persona_blocks": len(persona),
        "wiki_bytes": wiki_b, "persona_bytes": persona_b,
        "wiki_pct": round(100 * wiki_b / total, 2),
        "persona_pct": round(100 * persona_b / total, 2),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
