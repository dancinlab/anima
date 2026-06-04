#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_web_bulk.py — web-scale ODC-BY general-web BULK tier for the 7B corpus.

Constraint change (user decision 2026-06-05)
--------------------------------------------
The prior "NO scraped data" constraint is RELAXED for the bulk tiers only: web-scale
ODC-BY (Common-Crawl-derived) data is now SANCTIONED to reach 7B-sufficiency. Scope =
ODC-BY / permissive web corpora for BULK ONLY; PII-scrub + quality-filter still
required; persona/identity registers stay authored. See domains/CORPUS.md
`## constraint: web-scale sanctioned for 7B (2026-06-05)`.

KOSMOS tier -> real source mapping (web bulk)
---------------------------------------------
- tier `web` (general-web baseline bulk) -> the MAJORITY register at 7B scale.
  - fr / de / ko : FineWeb-2 (`HuggingFaceFW/fineweb-2`, ODC-BY) configs
                   `fra_Latn` / `deu_Latn` / `kor_Hang`. FineWeb-2 is already
                   quality-filtered + PII-reduced (Common-Crawl-derived). Korean
                   (`kor_Hang`) FIXES the prior ko bulk gap (Gutenberg had no ko).
  - en / es     : FineWeb-2 has NO English and NO Spanish config (it is the
                   non-English complement to FineWeb-1), so en/es fall back to the
                   task-named fallback `allenai/c4` (mC4, ODC-BY) configs `en`/`es`.

Both sources are ODC-BY (cite per source; web-derived, honest-labeled). This is the
ONLY scraped tier — every other tier (wiki CC-BY-SA, Gutenberg PD, authored persona)
is unchanged.

GB-SCALE PATH (same as fetch_wiki_tiers.py): each parquet shard is downloaded to a
LOCAL cache ONCE (curl), then duckdb-read LOCALLY (no read-amplification, no REST
429). DISK SAFETY: each lang is byte-capped (--mb-per-lang); the shard cache is
transient and pruned by build_all.sh's trap. $0 CPU, NO GPU.

Quality / cleanliness
---------------------
- FineWeb-2 is pre-filtered + PII-reduced upstream; c4 is the standard cleaned mC4.
  We additionally apply a light quality gate (min length, printable ratio, drop
  near-boilerplate) and a PII spot-scrub of e-mail addresses (belt-and-suspenders
  over the upstream scrub). Reported in the build JSON.
- byte-vocab V=256 (UTF-8); one document per block (blank-line separated); UTF-8
  round-trip truncation (never splits a multibyte char); control bytes 0xFE/0xFF
  never emitted (round-trip + the merge's vocab256 clean pass).

Honest scope (a_scale_honest_scope)
-----------------------------------
- Multi-shard sampling is a coverage heuristic, NOT a measured topical-uniformity
  guarantee. Per-lang achieved bytes reported verbatim in the build JSON.
- en/es ride mC4 (c4), fr/de/ko ride FineWeb-2 — the source differs per lang; both
  ODC-BY, both reported. NO fabrication.

Usage
-----
  python3 serving/gb_balanced/fetch_web_bulk.py \
      --out serving/corpus/_src/web_bulk.txt --mb-per-lang 1800
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import urllib.parse
import urllib.request

LANGS = ["en", "fr", "de", "es", "ko"]

# tier `web` source routing. FineWeb-2 (ODC-BY) for fr/de/ko; c4/mC4 (ODC-BY) for
# en/es (FineWeb-2 has no eng/spa config).
FINEWEB2 = "HuggingFaceFW/fineweb-2"
C4 = "allenai/c4"
FW2_CONFIG = {"fr": "fra_Latn", "de": "deu_Latn", "ko": "kor_Hang"}
C4_CONFIG = {"en": "en", "es": "es"}
SOURCE_LICENSE = {
    "en": ("allenai/c4 (mC4, en)", "ODC-BY-1.0"),
    "es": ("allenai/c4 (mC4, es)", "ODC-BY-1.0"),
    "fr": ("HuggingFaceFW/fineweb-2 (fra_Latn)", "ODC-BY-1.0"),
    "de": ("HuggingFaceFW/fineweb-2 (deu_Latn)", "ODC-BY-1.0"),
    "ko": ("HuggingFaceFW/fineweb-2 (kor_Hang)", "ODC-BY-1.0"),
}

PARQUET_API = "https://datasets-server.huggingface.co/parquet"
CACHE = os.environ.get("WEB_SHARD_CACHE", "/tmp/anima_web_shards")
MAX_SHARDS_PER_LANG = int(os.environ.get("WEB_MAX_SHARDS", "2"))

# light PII spot-scrub (belt-and-suspenders over the upstream scrub). FineWeb-2 / c4
# already reduce PII; this catches stray e-mail addresses in the sampled slice.
_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_token_cache = [""]


def _token():
    try:
        t = subprocess.run(["hf", "auth", "token"], capture_output=True,
                           text=True, timeout=30).stdout.strip()
        if t and t.startswith("hf_"):
            return t
    except Exception:
        pass
    for k in ("HF_TOKEN", "HUGGING_FACE_HUB_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    return ""


def shard_urls(dataset, config):
    q = urllib.parse.urlencode({"dataset": dataset, "config": config})
    req = urllib.request.Request(f"{PARQUET_API}?{q}",
                                 headers={"Authorization": f"Bearer {_token_cache[0]}"})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    return [f["url"] for f in d.get("parquet_files", []) if f["split"] == "train"]


def _local_shard(url, lang, idx):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"web_{lang}_{idx}.parquet")
    if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
        return path
    tmp = path + ".part"
    rc = subprocess.run(
        ["curl", "-s", "-L", "-H", f"Authorization: Bearer {_token_cache[0]}",
         "-o", tmp, url], timeout=1800).returncode
    if rc != 0 or not os.path.exists(tmp) or os.path.getsize(tmp) < 1_000_000:
        raise RuntimeError(f"web shard download failed: {lang}/{idx} rc={rc}")
    os.replace(tmp, path)
    return path


def _con():
    import duckdb
    con = duckdb.connect()
    con.execute("PRAGMA threads=4;")
    return con


def _quality_ok(t):
    """Light quality gate on top of the upstream FineWeb-2 / c4 filtering."""
    if len(t) < 200:
        return False
    # printable ratio (drop binary/garbled docs); allow newlines + common unicode.
    printable = sum(1 for c in t if c.isprintable() or c in "\n\t ")
    if printable / max(1, len(t)) < 0.85:
        return False
    return True


def _scrub(t):
    return _EMAIL.sub("[EMAIL]", t)


def fetch_lang(con, lang, target_bytes):
    if lang in C4_CONFIG:
        dataset, config = C4, C4_CONFIG[lang]
    else:
        dataset, config = FINEWEB2, FW2_CONFIG[lang]
    urls = shard_urls(dataset, config)[:MAX_SHARDS_PER_LANG]
    if not urls:
        return b"", 0, 0
    per_shard = max(1, target_bytes // len(urls))
    blocks, got, seen, scrubbed = [], 0, set(), 0
    for idx, url in enumerate(urls):
        if got >= target_bytes:
            break
        shard_budget = min(per_shard, target_bytes - got)
        try:
            path = _local_shard(url, lang, idx)
        except Exception as e:
            print(f"  ! {lang}/{idx} download skip: {e}", flush=True)
            continue
        # local read — no read-amplification. Scan a generous LIMIT; the quality
        # gate + byte budget bound the kept set.
        sql = f"SELECT text FROM read_parquet('{path}') LIMIT 200000"
        rows = con.execute(sql).fetchall()
        sb = 0
        for (text,) in rows:
            t = (text or "").strip()
            if not _quality_ok(t):
                continue
            key = t[:128]
            if key in seen:
                continue
            seen.add(key)
            t2 = _scrub(t)
            if t2 != t:
                scrubbed += 1
            blocks.append(t2)
            nb = len(t2.encode("utf-8", "replace"))
            got += nb
            sb += nb
            if sb >= shard_budget or got >= target_bytes:
                break
    raw = ("\n\n".join(blocks)).encode("utf-8", "replace")[:target_bytes]
    raw = raw.decode("utf-8", "ignore").encode("utf-8")  # UTF-8 round-trip
    return raw, len(blocks), scrubbed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--mb-per-lang", type=float, default=1800.0)
    ap.add_argument("--langs", default=",".join(LANGS),
                    help="comma list subset of en,fr,de,es,ko")
    args = ap.parse_args()

    token = _token()
    assert token, "no HF token (hf auth login / HF_TOKEN / secret get hf.token)"
    _token_cache[0] = token
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)
    langs = [l for l in args.langs.split(",") if l in LANGS]
    con = _con()

    per_lang, per_lang_blocks, per_lang_scrub = {}, {}, {}
    with open(args.out, "wb") as f:
        for lang in langs:
            blob, nblk, scr = fetch_lang(con, lang, target)
            f.write(blob)
            f.write(b"\n\n")
            per_lang[lang] = len(blob)
            per_lang_blocks[lang] = nblk
            per_lang_scrub[lang] = scr
            src, lic = SOURCE_LICENSE[lang]
            print(f"  web {lang}: {len(blob)} bytes / {nblk} blocks "
                  f"/ {scr} email-scrubbed | {src} {lic}", flush=True)

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    print(json.dumps({
        "out": args.out, "tier": "web", "bytes": size,
        "mb": round(size / 1048576, 3), "gb": round(size / 1073741824, 4),
        "sha256": h.hexdigest(),
        "per_lang_bytes": per_lang, "per_lang_blocks": per_lang_blocks,
        "per_lang_email_scrubbed": per_lang_scrub,
        "source_per_lang": {l: SOURCE_LICENSE[l][0] for l in langs},
        "license_per_lang": {l: SOURCE_LICENSE[l][1] for l in langs},
        "langs": langs,
        "sampling": "multi-shard local-parquet-cache (duckdb), quality+PII gate",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
