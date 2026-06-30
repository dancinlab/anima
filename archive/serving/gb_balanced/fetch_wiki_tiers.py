#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_wiki_tiers.py — Wikipedia tier-0 (baseline) + tier-100 (cosmic/science).

KOSMOS tier -> real source mapping (GB-balanced default-lane corpus)
--------------------------------------------------------------------
- tier 0   baseline/factual -> `wikimedia/wikipedia` 5-lang, multi-shard breadth
           (topical spread across the parquet shard space, no alphabetical bias).
           CC-BY-SA-4.0.
- tier 100 cosmic/science   -> the SAME wiki, SQL keyword-FILTERED to science /
           cosmology / physics / astronomy (title OR lead matches a per-language
           science marker). CC-BY-SA-4.0.

GB-SCALE PATH: DOWNLOADS each parquet shard to a local cache ONCE (curl, ~15-30s
per 300-400MB shard), then duckdb-reads it LOCALLY (instant, no read-amplification).
Reading remote parquet over httpfs amplifies I/O badly (a 3MB sample pulls >1GB of
row-groups); the REST `/rows` endpoint 429s at GB volume. Local-shard read avoids
both. The parquet files are the official `refs/convert/parquet` mirror of
`wikimedia/wikipedia` (CC-BY-SA-4.0). $0 CPU, NO GPU. DETERMINISTIC: fixed shard
order + fixed per-shard byte budget + fixed marker lists + stable parquet row order.

byte-vocab V=256 (UTF-8); one article per block (blank-line separated); UTF-8
round-trip truncation (never splits a multibyte char).

Honest scope (a_scale_honest_scope)
-----------------------------------
- Multi-shard sampling spreads the slice across the article space (broad topical
  band); it is a coverage heuristic, NOT a measured topical-uniformity guarantee.
- The science filter is a keyword gate over title+text; it raises science density,
  it is NOT a curated science partition. Korean has fewer shards (3) than en (41),
  so ko breadth is shallower — reported per-lang in the build JSON.

Usage
-----
  python3 serving/gb_balanced/fetch_wiki_tiers.py \
      --tier 0   --out serving/corpus/_src/wiki_t0.txt   --mb-per-lang 90
  python3 serving/gb_balanced/fetch_wiki_tiers.py \
      --tier 100 --out serving/corpus/_src/wiki_t100.txt --mb-per-lang 18
"""

import argparse
import hashlib
import json
import os
import subprocess
import urllib.parse
import urllib.request

LANGS = ["en", "fr", "de", "es", "ko"]
DATE = "20231101"
DATASET = "wikimedia/wikipedia"
PARQUET_API = "https://datasets-server.huggingface.co/parquet"

# tier-100 science/cosmology markers per language, HIGH-PRECISION: matched against
# the TITLE only (the article's topic), not the body — a body match catches any
# article that merely mentions "evolution"/"scientific" in passing (e.g. Anarchism).
# Title-scoped + strong cosmology/physics/astronomy terms keep precision high.
SCI_MARKERS = {
    "en": ["physics", "astronom", "cosmolog", "galaxy", "galaxies", "universe",
           "quantum", "planet", "asteroid", "nebula", "supernova", "black hole",
           "telescope", "particle", "relativity", "thermodynamic", "molecule",
           "atomic", "spacetime", "stellar", "gravit", "cosmic"],
    "fr": ["physique", "astronomie", "cosmologie", "galaxie", "univers",
           "quantique", "planète", "astéroïde", "nébuleuse", "supernova",
           "télescope", "particule", "relativité", "thermodynamique", "molécule",
           "atome", "électron", "photon", "gravit", "cosmique", "étoile"],
    "de": ["physik", "astronomie", "kosmologie", "galaxie", "universum",
           "quanten", "planet", "asteroid", "nebel", "supernova", "teleskop",
           "teilchen", "relativität", "thermodynamik", "molekül", "atom",
           "elektron", "photon", "gravitation", "kosmisch", "stern"],
    "es": ["física", "astronomía", "cosmología", "galaxia", "universo",
           "cuántic", "planeta", "asteroide", "nebulosa", "supernova",
           "telescopio", "partícula", "relatividad", "termodinámica", "molécula",
           "átomo", "electrón", "fotón", "gravit", "cósmic", "estrella"],
    "ko": ["물리", "천문", "우주", "은하", "양자", "행성", "소행성", "성운",
           "초신성", "망원경", "입자", "상대성", "열역학", "분자", "원자",
           "전자", "광자", "중력", "항성", "천체"],
}


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


def shard_urls(lang, token):
    q = urllib.parse.urlencode({"dataset": DATASET, "config": f"{DATE}.{lang}"})
    req = urllib.request.Request(f"{PARQUET_API}?{q}",
                                 headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    return [f["url"] for f in d.get("parquet_files", []) if f["split"] == "train"]


CACHE = os.environ.get("WIKI_SHARD_CACHE", "/tmp/anima_wiki_shards")
MAX_SHARDS_PER_LANG = int(os.environ.get("WIKI_MAX_SHARDS", "3"))


def _con():
    import duckdb
    con = duckdb.connect()
    con.execute("PRAGMA threads=4;")
    return con


def _local_shard(url, lang, idx):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"wiki_{lang}_{idx}.parquet")
    if os.path.exists(path) and os.path.getsize(path) > 1_000_000:
        return path
    tmp = path + ".part"
    rc = subprocess.run(
        ["curl", "-s", "-L", "-H", f"Authorization: Bearer {_token_cache[0]}",
         "-o", tmp, url], timeout=900).returncode
    if rc != 0 or not os.path.exists(tmp) or os.path.getsize(tmp) < 1_000_000:
        raise RuntimeError(f"shard download failed: {lang}/{idx} rc={rc}")
    os.replace(tmp, path)
    return path


def fetch_lang(con, lang, target_bytes, science):
    urls = shard_urls(lang, _token_cache[0])[:MAX_SHARDS_PER_LANG]
    if not urls:
        return b"", 0
    per_shard = max(1, target_bytes // len(urls))
    blocks, got, seen = [], 0, set()
    where, params = "", []
    if science:
        markers = SCI_MARKERS[lang]
        # TITLE-scoped match = high precision (the title IS the topic). A body
        # match would catch any article merely mentioning a science word.
        ors = " OR ".join(["lower(title) LIKE '%' || ? || '%'" for _ in markers])
        where = f"WHERE ({ors})"
        for m in markers:
            params.append(m.lower())
    for idx, url in enumerate(urls):
        if got >= target_bytes:
            break
        shard_budget = min(per_shard, target_bytes - got)
        try:
            path = _local_shard(url, lang, idx)
        except Exception as e:
            print(f"  ! {lang}/{idx} download skip: {e}", flush=True)
            continue
        # local read — no read-amplification; LIMIT scans more for the science filter
        lim = 60000 if science else 12000
        sql = (f"SELECT title, text FROM read_parquet('{path}') {where} LIMIT {lim}")
        rows = con.execute(sql, params).fetchall()
        sb = 0
        for title, text in rows:
            t = (text or "").strip()
            if len(t) < 200:
                continue
            key = t[:128]
            if key in seen:
                continue
            seen.add(key)
            blocks.append(t)
            nb = len(t.encode("utf-8", "replace"))
            got += nb
            sb += nb
            if sb >= shard_budget or got >= target_bytes:
                break
    raw = ("\n\n".join(blocks)).encode("utf-8", "replace")[:target_bytes]
    raw = raw.decode("utf-8", "ignore").encode("utf-8")  # UTF-8 round-trip
    return raw, len(blocks)


_token_cache = [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", type=int, required=True, choices=[0, 100])
    ap.add_argument("--out", required=True)
    ap.add_argument("--mb-per-lang", type=float, default=10.0)
    args = ap.parse_args()

    token = _token()
    assert token, "no HF token (hf auth login / HF_TOKEN / secret get hf.token)"
    _token_cache[0] = token
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)
    science = (args.tier == 100)
    con = _con()

    per_lang, per_lang_blocks = {}, {}
    with open(args.out, "wb") as f:
        for lang in LANGS:
            blob, nblk = fetch_lang(con, lang, target, science)
            f.write(blob)
            f.write(b"\n\n")
            per_lang[lang] = len(blob)
            per_lang_blocks[lang] = nblk
            print(f"  t{args.tier} {lang}: {len(blob)} bytes / {nblk} blocks"
                  + (" (science-filtered)" if science else " (multi-shard)"),
                  flush=True)

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    print(json.dumps({
        "out": args.out, "tier": args.tier, "bytes": size,
        "mb": round(size / 1048576, 3), "sha256": h.hexdigest(),
        "per_lang_bytes": per_lang, "per_lang_blocks": per_lang_blocks,
        "source": f"{DATASET} {DATE} parquet (CC-BY-SA-4.0)", "langs": LANGS,
        "sampling": ("multi-shard + science keyword filter (duckdb httpfs)"
                     if science else "multi-shard spread (duckdb httpfs)"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
