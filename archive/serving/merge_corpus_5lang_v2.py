#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_corpus_5lang_v2.py — v2 UNIFIED corpus = wiki(broadened) + persona + enrichment.

Builds the v2 unified corpus ON TOP of v1 by block-interleaving THREE 5-lang
surfaces (v1 left intact):

  [ wiki_backbone_5lang_v2.txt ]   topical-breadth wiki (v2 #2, CC-BY-SA real)
  [ persona_sns_corpus_5lang.txt ] v1 persona × SNS (authored-synthetic, unchanged)
  [ corpus_enrichment_5lang.txt ]  v2 register enrichment (#1 carving · #3 act ·
                                    #4 codeswitch · #5 emotion · #7 genre)
        └── deterministic byte-weighted round-robin ──▶
            persona_sns_corpus_5lang_v2.txt

Target byte mix (documented in CORPUS_CARD_v2):
  ~40% wiki / ~40% persona / ~20% enrichment (held by byte-weighted round-robin).

Honest scope (a_scale_honest_scope)
-----------------------------------
- wiki = real CC-BY-SA wikipedia (provenance carried, now topically broadened).
- persona + enrichment = authored-synthetic multilingual COVERAGE (NOT native).
  The card states each license + the per-language AND per-register byte split.
- DETERMINISTIC: same inputs → same sha256.

Usage
-----
  python3 serving/merge_corpus_5lang_v2.py \
      --wiki serving/corpus/wiki_backbone_5lang_v2.txt \
      --persona serving/corpus/persona_sns_corpus_5lang.txt \
      --enrichment serving/corpus/corpus_enrichment_5lang.txt \
      --out serving/corpus/persona_sns_corpus_5lang_v2.txt
"""

import argparse
import hashlib
import json
import os


def read_blocks(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return [b for b in text.split("\n\n") if b.strip()]


def _bytes(b):
    return len(b.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default="serving/corpus/wiki_backbone_5lang_v2.txt")
    ap.add_argument("--persona",
                    default="serving/corpus/persona_sns_corpus_5lang.txt")
    ap.add_argument("--enrichment",
                    default="serving/corpus/corpus_enrichment_5lang.txt")
    ap.add_argument("--out",
                    default="serving/corpus/persona_sns_corpus_5lang_v2.txt")
    args = ap.parse_args()

    streams = {
        "wiki": read_blocks(args.wiki),
        "persona": read_blocks(args.persona),
        "enrichment": read_blocks(args.enrichment),
    }
    stream_bytes = {k: sum(_bytes(b) for b in v) for k, v in streams.items()}

    # Deterministic byte-weighted round-robin: advance whichever stream is most
    # under-represented by accumulated bytes, so the byte mix tracks the input
    # proportions (no fixed-ratio forcing — the inputs' relative sizes set the mix).
    cursors = {k: 0 for k in streams}
    acc = {k: 0 for k in streams}
    out_blocks = []
    remaining = sum(len(v) for v in streams.values())
    while remaining > 0:
        # pick the stream with blocks left and the smallest accumulated bytes
        cand = [k for k in streams if cursors[k] < len(streams[k])]
        pick = min(cand, key=lambda k: acc[k])
        b = streams[pick][cursors[pick]]
        cursors[pick] += 1
        acc[pick] += _bytes(b)
        out_blocks.append(b)
        remaining -= 1

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n\n".join(out_blocks) + "\n\n")

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    total = sum(stream_bytes.values())
    print(json.dumps({
        "out": args.out, "bytes": size, "mb": round(size / 1048576, 3),
        "sha256": h.hexdigest(),
        "blocks": {k: len(v) for k, v in streams.items()},
        "stream_bytes": stream_bytes,
        "pct": {k: round(100 * stream_bytes[k] / total, 2) for k in stream_bytes},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
