#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_wiki_backbone_5lang_v2.py — topically-BROADENED en/fr/de/es/ko wiki backbone.

v2 enrichment #2 — wiki topical breadth (fix the alphabetical-prefix bias).
------------------------------------------------------------------------
v1 (`build_wiki_backbone_5lang.py`) walks `wikimedia/wikipedia` rows from a SINGLE
fixed offset 0 forward — the dataset is roughly alphabetical by title, so v1's
slice is dominated by A-prefix / early-alphabet articles (a narrow topical band).

v2 fixes this by sampling from SEVERAL spread-out offsets across the article space
(deterministic, fixed offset list) and round-robining one page from each offset
band, so each language's slice spans the whole alphabet → broader topical coverage
(science / history / art / geography rather than just A-prefix). Still:

- DETERMINISTIC: fixed offset bands → same sha modulo the pinned 20231101 revision.
- CLEAN, ON-AXIS: `wikimedia/wikipedia` 20231101.<lang> (CC-BY-SA-4.0), same source.
- byte-vocab V=256 (UTF-8), one article per block (blank-line separated).
- $0 CPU, HF datasets-server REST `/rows` (no `datasets` lib, no GPU).

Honest scope (a_scale_honest_scope)
-----------------------------------
- The offset bands are a coverage HEURISTIC over the title-ordered dump; they
  broaden the topical band but do not guarantee uniform topical balance (the dump
  ordering is not a clean topical partition). Honest: this REDUCES alphabetical
  bias measurably (slice now spans the full offset range), it does not claim a
  measured topical-uniformity guarantee.

Usage
-----
  python3 serving/build_wiki_backbone_5lang_v2.py \
      --out serving/corpus/wiki_backbone_5lang_v2.txt --mb-per-lang 1.0
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

# Per-language approximate train-split row counts (wikimedia/wikipedia 20231101).
# Used only to space the deterministic offset bands across the article space.
# Conservative LOWER bounds so every band offset is valid for the split.
LANG_ROWS = {
    "en": 6_400_000,
    "fr": 2_500_000,
    "de": 2_800_000,
    "es": 1_800_000,
    "ko": 640_000,
}
N_BANDS = 8  # spread sampling across 8 evenly-spaced offset bands per language


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
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
    return {"rows": []}


def fetch_lang(lang, target_bytes, token):
    """Spread-sample wikipedia rows across N_BANDS offset bands until target_bytes.

    Round-robins one page from each band, advancing each band's cursor, so the
    accumulated slice spans the full offset range (alphabet) rather than a single
    A-prefix prefix walk."""
    cfg = f"{DATE}.{lang}"
    n_rows = LANG_ROWS[lang]
    # Evenly-spaced band start offsets across the article space.
    band_starts = [(n_rows // N_BANDS) * i for i in range(N_BANDS)]
    cursors = list(band_starts)
    # per-band ceiling so a band cannot bleed into the next band's range
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
    # truncate on a valid UTF-8 boundary (don't split a multibyte char)
    raw = raw.decode("utf-8", "ignore").encode("utf-8")
    return raw, len(blocks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="serving/corpus/wiki_backbone_5lang_v2.txt")
    ap.add_argument("--mb-per-lang", type=float, default=1.0)
    args = ap.parse_args()

    token = _token()
    assert token, "no HF token (hf auth login)"
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)

    per_lang = {}
    per_lang_blocks = {}
    with open(args.out, "wb") as f:
        for lang in LANGS:
            blob, nblk = fetch_lang(lang, target, token)
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
        "sampling": f"{N_BANDS}-band offset-spread (topical breadth, v2 #2)",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
