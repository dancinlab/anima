#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_wiki_backbone_5lang.py — clean en/fr/de/es/ko wiki backbone (REST, $0 CPU).

Why not reuse `clm-backbone-5lang-sample`?
------------------------------------------
That HF dataset is ko/en/zh/ru/ja (mC4), NOT the en/fr/de/es/ko set the persona
corpus targets — and its ko C4 slice contains NSFW/spam web text unsuitable as a
persona-corpus backbone. So this builder pulls a CLEAN, ON-AXIS backbone in the
SAME 5 languages as the persona/SNS surface, from wikimedia/wikipedia
(CC-BY-SA-4.0), via the HF datasets-server REST `/rows` endpoint (no `datasets`
lib, no GPU, deterministic by fixed page offsets).

Honest scope
------------
- Source: wikimedia/wikipedia 20231101.<lang> (CC-BY-SA-4.0, attributable).
- Balanced per-language byte budget (--mb-per-lang). Deterministic page walk
  (fixed offsets) → re-running with the same args reproduces the same sha256
  modulo upstream dataset revision (the dataset is pinned by date 20231101).
- Plain newline corpus, byte-vocab V=256 (UTF-8). One article block per line
  region; articles separated by a blank line.

Usage
-----
  python3 serving/build_wiki_backbone_5lang.py \
      --out serving/corpus/wiki_backbone_5lang.txt --mb-per-lang 1.0
"""

import argparse
import hashlib
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request

LANGS = ["en", "fr", "de", "es", "ko"]
DATE = "20231101"
DATASET = "wikimedia/wikipedia"
ROWS_URL = "https://datasets-server.huggingface.co/rows"
PAGE = 100  # datasets-server max length per request


def _token():
    try:
        return subprocess.run(["hf", "auth", "token"], capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except Exception:
        return os.environ.get("HF_TOKEN", "")


def fetch_lang(lang, target_bytes, token, offset0=0):
    """Walk wikipedia rows deterministically from offset0 until target_bytes."""
    cfg = f"{DATE}.{lang}"
    got = 0
    offset = offset0
    blocks = []
    seen = set()
    while got < target_bytes:
        q = urllib.parse.urlencode({
            "dataset": DATASET, "config": cfg, "split": "train",
            "offset": offset, "length": PAGE,
        })
        req = urllib.request.Request(f"{ROWS_URL}?{q}",
                                     headers={"Authorization": f"Bearer {token}"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = json.load(r)
                break
            except Exception as e:
                if attempt == 4:
                    raise
                time.sleep(2 * (attempt + 1))
        rows = data.get("rows", [])
        if not rows:
            break
        for item in rows:
            t = (item["row"].get("text") or "").strip()
            if not t or len(t) < 200:
                continue
            key = t[:128]
            if key in seen:
                continue
            seen.add(key)
            blocks.append(t)
            got += len(t.encode("utf-8", "replace"))
            if got >= target_bytes:
                break
        offset += PAGE
    raw = ("\n\n".join(blocks)).encode("utf-8", "replace")[:target_bytes]
    # truncate on a valid UTF-8 char boundary (avoid splitting a multibyte char)
    raw = raw.decode("utf-8", "ignore").encode("utf-8")
    return raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="serving/corpus/wiki_backbone_5lang.txt")
    ap.add_argument("--mb-per-lang", type=float, default=1.0)
    args = ap.parse_args()

    token = _token()
    assert token, "no HF token (hf auth login)"
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)

    per_lang = {}
    with open(args.out, "wb") as f:
        for lang in LANGS:
            blob = fetch_lang(lang, target, token)
            f.write(blob)
            f.write(b"\n\n")
            per_lang[lang] = len(blob)
            print(f"  {lang}: {len(blob)} bytes", flush=True)

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    print(json.dumps({
        "out": args.out, "bytes": size, "mb": round(size / 1048576, 3),
        "sha256": h.hexdigest(), "per_lang_bytes": per_lang,
        "source": f"{DATASET} {DATE} (CC-BY-SA-4.0)", "langs": LANGS,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
