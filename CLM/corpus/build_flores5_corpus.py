#!/usr/bin/env python3
"""Build a BIGGER real multilingual byte corpus from FLORES-200 (5 langs).

Concatenates FLORES-200 dev + devtest raw UTF-8 sentence files for the SAME 5
languages as the landed 402KB Lane P corpus (en/zh/ru/ja/ko) into one byte
stream. FLORES-200 is real, parallel, ungated multilingual evaluation text
(fbaipublicfiles, NLLB). The result is >> 402KB and lets the train/val split
test memorization-vs-generalization on a larger real corpus.

Usage: build_flores5_corpus.py <flores200_extract_dir> <out_path>
  where <flores200_extract_dir> contains dev/ and devtest/ subdirs of *.devtest
  files named like eng_Latn.dev, zho_Hans.devtest, etc.
"""
import hashlib, os, sys

# FLORES-200 lang codes for the 5 Lane P languages.
LANGS = ["eng_Latn", "zho_Hans", "rus_Cyrl", "jpn_Jpan", "kor_Hang"]


def main():
    root, out = sys.argv[1], sys.argv[2]
    chunks = []
    manifest = []
    for split in ("dev", "devtest"):
        d = os.path.join(root, split)
        if not os.path.isdir(d):
            continue
        for lang in LANGS:
            # files are <lang>.dev / <lang>.devtest
            fn = os.path.join(d, f"{lang}.{split}")
            if not os.path.exists(fn):
                # some releases name dev files <lang>.dev under a flat dir
                alt = os.path.join(root, f"{lang}.{split}")
                fn = alt if os.path.exists(alt) else fn
            if not os.path.exists(fn):
                print(f"MISS {fn}", flush=True)
                continue
            with open(fn, "rb") as f:
                b = f.read()
            chunks.append(b)
            manifest.append((split, lang, len(b)))
            print(f"ADD {split}/{lang} {len(b)} bytes", flush=True)
    data = b"".join(chunks)
    with open(out, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    print(f"CORPUS_OUT {out} bytes={len(data)} sha256={sha}", flush=True)
    for (split, lang, n) in manifest:
        print(f"  {split:8s} {lang:10s} {n}", flush=True)


if __name__ == "__main__":
    main()
