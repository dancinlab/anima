#!/usr/bin/env python3
"""NAT-ATOM (H_9290) — minimal codec-natural CPT corpus (no drill, no gen_nbind dep).

Trains the MORPH-2B codec on the natural corpus and writes the codec-encoded natural stream
(sentinel-delimited, same format as cpt_M.bytes in the MORPH-ATOM run) + codec.json. This is the
M-nat CPT input: natural Korean text only, NO XOR drill, NO handed equivalence — the frontier cell
that H_9290 measured (answer: codec atomicity does NOT rescue natural grounding).

Usage: gen_codec_natural.py --corpus morph_corpus.txt --k 2048 --cpt-lines 120000 --out-dir .
"""
import json, os, sys
import morph2b as MB

CORPUS = sys.argv[sys.argv.index("--corpus") + 1] if "--corpus" in sys.argv else "morph_corpus.txt"
K = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 2048
CPT_LINES = int(sys.argv[sys.argv.index("--cpt-lines") + 1]) if "--cpt-lines" in sys.argv else 120000
OUTDIR = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else "."

lines = [l.rstrip("\n") for l in open(CORPUS, encoding="utf-8") if l.strip()][:CPT_LINES]
merges = MB.train_bpe(lines[:20000], K)
merge_rank, tok2id, vocab = MB.build_vocab(lines, merges)
json.dump({"k": K, "vocab_size": len(vocab),
           "merges": ["\t".join(m) for m in merges], "tok2id": tok2id, "shared_collapse": False},
          open(os.path.join(OUTDIR, "codec.json"), "w", encoding="utf-8"), ensure_ascii=False)
enc = lambda t: MB.encode_to_bytes(t, merge_rank, tok2id)
with open(os.path.join(OUTDIR, "cpt_M.bytes"), "wb") as f:
    for l in lines:
        f.write(enc(l) + b"\x00\x0a")     # 2-byte sentinel line delimiter (matches MORPH-ATOM format)
print("GEN_DONE: %d lines · vocab %d · cpt_M.bytes %d bytes" %
      (len(lines), len(vocab), os.path.getsize(os.path.join(OUTDIR, "cpt_M.bytes"))))
