#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_wiki_backbone_5lang_scaleup.py — SCALE-UP-grade 8-band wiki sampler.

Same DETERMINISTIC 8-band offset-spread method as build_wiki_backbone_5lang_v2.py
(real CC-BY-SA wikimedia/wikipedia 20231101, en/fr/de/es/ko, byte-vocab256,
HF datasets-server REST /rows, $0 CPU, NO GPU), but HARDENED for a large
(~20 MB/lang) sustained pull:

  - 429-aware EXPONENTIAL backoff with jitter + Retry-After honor (the v2 sampler's
    fixed 2*(attempt+1) backoff trips on a 100 MB sustained pull -> HTTP 429 storm).
  - a small inter-page courtesy sleep to stay under the datasets-server rate limit.
  - PER-LANGUAGE on-disk checkpoint (<out>.<lang>.part): a 429 storm mid-run is
    RESUMABLE -- re-run continues each language from its last completed byte count,
    so the pull is robust without re-fetching finished languages.

Determinism: same fixed 8 band offsets + pinned 20231101 revision -> the same
slice (modulo upstream revision), independent of where a resume picked up, because
each band walks its fixed cursor sequence; the merge truncates to target_bytes on
a UTF-8 boundary. (0.4.0 storm-backoff compliant.)

Usage
-----
  python3 serving/build_wiki_backbone_5lang_scaleup.py \
      --out serving/corpus/wiki_backbone_5lang_v3.txt --mb-per-lang 20.0
"""

import argparse
import hashlib
import json
import os
import random
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request

LANGS = ["en", "fr", "de", "es", "ko"]
DATE = "20231101"
DATASET = "wikimedia/wikipedia"
ROWS_URL = "https://datasets-server.huggingface.co/rows"
PAGE = 100

LANG_ROWS = {
    "en": 6_400_000,
    "fr": 2_500_000,
    "de": 2_800_000,
    "es": 1_800_000,
    "ko": 640_000,
}
N_BANDS = 8
PAGE_SLEEP = 0.35   # courtesy delay between pages (stay under the rate limit)


def _token():
    try:
        return subprocess.run(["hf", "auth", "token"], capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except Exception:
        return os.environ.get("HF_TOKEN", "")


def _fetch_page(cfg, offset, token):
    q = urllib.parse.urlencode({
        "dataset": DATASET, "config": cfg, "split": "train",
        "offset": offset, "length": PAGE,
    })
    req = urllib.request.Request(f"{ROWS_URL}?{q}",
                                 headers={"Authorization": f"Bearer {token}"})
    # 429-aware exponential backoff with jitter (max ~10 tries -> ~5 min worst case)
    for attempt in range(10):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if (ra and ra.isdigit()) else min(
                    60.0, (2.0 ** attempt)) + random.uniform(0, 3)
                time.sleep(wait)
                continue
            if attempt == 9:
                raise
            time.sleep(min(30.0, 2.0 ** attempt) + random.uniform(0, 2))
        except Exception:
            if attempt == 9:
                raise
            time.sleep(min(30.0, 2.0 ** attempt) + random.uniform(0, 2))
    return {"rows": []}


def fetch_lang(lang, target_bytes, token, part_path):
    """8-band spread-sample until target_bytes, checkpointing to part_path.

    Resumable: if part_path already holds >= target_bytes (UTF-8), reuse it."""
    if os.path.exists(part_path):
        cur = os.path.getsize(part_path)
        if cur >= target_bytes:
            with open(part_path, "rb") as f:
                raw = f.read()[:target_bytes]
            raw = raw.decode("utf-8", "ignore").encode("utf-8")
            return raw, raw.count(b"\n\n") + 1
    cfg = f"{DATE}.{lang}"
    n_rows = LANG_ROWS[lang]
    band_starts = [(n_rows // N_BANDS) * i for i in range(N_BANDS)]
    cursors = list(band_starts)
    band_span = n_rows // N_BANDS
    band_end = [band_starts[i] + band_span for i in range(N_BANDS)]

    got = 0
    blocks = []
    seen = set()
    exhausted = [False] * N_BANDS
    while got < target_bytes and not all(exhausted):
        for bi in range(N_BANDS):
            if got >= target_bytes:
                break
            if exhausted[bi] or cursors[bi] >= band_end[bi]:
                exhausted[bi] = True
                continue
            data = _fetch_page(cfg, cursors[bi], token)
            time.sleep(PAGE_SLEEP)
            rows = data.get("rows", [])
            cursors[bi] += PAGE
            if not rows:
                exhausted[bi] = True
                continue
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
    raw = ("\n\n".join(blocks)).encode("utf-8", "replace")[:target_bytes]
    raw = raw.decode("utf-8", "ignore").encode("utf-8")
    with open(part_path, "wb") as f:   # checkpoint the completed language
        f.write(raw)
    return raw, len(blocks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="serving/corpus/wiki_backbone_5lang_v3.txt")
    ap.add_argument("--mb-per-lang", type=float, default=20.0)
    args = ap.parse_args()

    random.seed(20260604)
    token = _token()
    assert token, "no HF token (hf auth login)"
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)

    per_lang = {}
    per_lang_blocks = {}
    with open(args.out, "wb") as f:
        for lang in LANGS:
            part = f"{args.out}.{lang}.part"
            blob, nblk = fetch_lang(lang, target, token, part)
            f.write(blob)
            f.write(b"\n\n")
            per_lang[lang] = len(blob)
            per_lang_blocks[lang] = nblk
            print(f"  {lang}: {len(blob)} bytes / {nblk} blocks (8-band spread)",
                  flush=True)

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    print(json.dumps({
        "out": args.out, "bytes": size, "mb": round(size / 1048576, 3),
        "sha256": h.hexdigest(), "per_lang_bytes": per_lang,
        "per_lang_blocks": per_lang_blocks,
        "source": f"{DATASET} {DATE} (CC-BY-SA-4.0)", "langs": LANGS,
        "sampling": f"{N_BANDS}-band offset-spread (scale-up, 429-hardened)",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
