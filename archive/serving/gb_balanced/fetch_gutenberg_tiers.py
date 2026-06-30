#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_gutenberg_tiers.py — Project Gutenberg (PD) tier-77 art + tier-91 consciousness.

KOSMOS tier -> real source mapping
----------------------------------
- tier 77 art           -> Gutenberg literature / poetry / fiction (PUBLIC DOMAIN).
- tier 91 consciousness -> Gutenberg philosophy / meditation / contemplative /
                           ethics / mysticism (PUBLIC DOMAIN). The 31 e7_31 carving
                           anchors DEFINE this register (authored seed slice
                           elsewhere); HERE it is FILLED with REAL PD contemplative
                           text — NOT the 31 anchors repeated.

Sources (read DIRECTLY from HF parquet shards via duckdb httpfs — no per-row REST
rate limit, $0 CPU, NO GPU):
- English  : `sedthh/gutenberg_english` (has `METADATA` JSON with `subjects`) ->
             tier classified by subject keyword (poetry/fiction -> art; philosophy/
             ethics/religion/meditation/mysticism -> consciousness).
- fr/de/es : `manu/project_gutenberg` (id+text only; classified by the PG header
             title line). Residual literary books labeled "mixed literature".
- ko       : NO Gutenberg Korean split exists -> HONEST GAP (ko art/consciousness
             fall back to wiki). Reported, never fabricated.

Each book is stripped of the PG boilerplate, then sliced into deterministic EXCERPT
windows (diverse text, NOT whole-book repeats -> anti-memorization). V=256, UTF-8
round-trip.

Honest scope (a_scale_honest_scope): fr/de/es Gutenberg is FAR thinner than en;
ko = 0. Reported per-lang verbatim.

Usage
-----
  python3 serving/gb_balanced/fetch_gutenberg_tiers.py \
      --tier art           --out serving/corpus/_src/gut_art.txt --mb-per-lang 22
  python3 serving/gb_balanced/fetch_gutenberg_tiers.py \
      --tier consciousness --out serving/corpus/_src/gut_con.txt --mb-per-lang 14
"""

import argparse
import hashlib
import json
import os
import subprocess
import urllib.parse
import urllib.request

PARQUET_API = "https://datasets-server.huggingface.co/parquet"
EN_DS = "sedthh/gutenberg_english"
MULTI_DS = "manu/project_gutenberg"
MULTI_LANGS = ["fr", "de", "es"]
ALL_LANGS = ["en", "fr", "de", "es", "ko"]

ART_SUBJ = ["poetry", "fiction", "drama", "tragedy", "comedy", "novel",
            "short stories", "romance", "literature", "tales", "verse",
            "sonnet", "epic", "ballad", "fable", "fairy"]
CON_SUBJ = ["philosophy", "ethics", "metaphysic", "meditation", "mysticism",
            "consciousness", "spiritual", "religion", "buddhis", "taois",
            "hindu", "stoic", "contemplat", "theosophy", "transcendental",
            "soul", "mind and body", "wisdom", "psychology", "occult",
            "theology", "faith", "prayer", "immortality", "conduct of life",
            "self-realization", "yoga", "vedanta", "moral", "virtue"]

ART_TITLE = {
    "fr": ["poésie", "poèmes", "roman", "contes", "théâtre", "fables",
           "nouvelles", "récit", "drame", "comédie"],
    "de": ["gedichte", "lyrik", "roman", "märchen", "novelle", "drama",
           "erzählung", "dichtung", "sagen"],
    "es": ["poesía", "poemas", "novela", "cuentos", "teatro", "fábulas",
           "drama", "comedia", "versos"],
}
CON_TITLE = {
    "fr": ["philosophie", "méditations", "éthique", "morale", "âme",
           "sagesse", "métaphysique", "religion", "mystique"],
    "de": ["philosophie", "ethik", "betrachtungen", "seele", "weisheit",
           "metaphysik", "religion", "moral", "mystik"],
    "es": ["filosofía", "meditaciones", "ética", "moral", "alma",
           "sabiduría", "metafísica", "religión", "mística"],
}

EXCERPT = 2800
STRIDE = 9000
MAX_EXCERPTS_PER_BOOK = 6
_token_cache = [""]
CACHE = os.environ.get("GUT_SHARD_CACHE", "/tmp/anima_gut_shards")
MAX_SHARDS = int(os.environ.get("GUT_MAX_SHARDS", "4"))


def _local_shard(url, tag, idx):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"gut_{tag}_{idx}.parquet")
    if os.path.exists(path) and os.path.getsize(path) > 100_000:
        return path
    tmp = path + ".part"
    rc = subprocess.run(
        ["curl", "-s", "-L", "-H", f"Authorization: Bearer {_token_cache[0]}",
         "-o", tmp, url], timeout=900).returncode
    if rc != 0 or not os.path.exists(tmp) or os.path.getsize(tmp) < 100_000:
        raise RuntimeError(f"gut shard download failed: {tag}/{idx} rc={rc}")
    os.replace(tmp, path)
    return path


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


def shard_urls(dataset, splits):
    q = urllib.parse.urlencode({"dataset": dataset})
    req = urllib.request.Request(f"{PARQUET_API}?{q}",
                                 headers={"Authorization": f"Bearer {_token_cache[0]}"})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    return [f["url"] for f in d.get("parquet_files", []) if f["split"] in splits]


def _con():
    import duckdb
    con = duckdb.connect()
    con.execute("PRAGMA threads=4;")
    return con


def _strip_pg(text):
    lo = text
    up = text.upper()
    s = up.find("*** START")
    if s != -1:
        nl = lo.find("\n", s)
        if nl != -1:
            lo = lo[nl + 1:]; up = lo.upper()
    e = up.find("*** END")
    if e != -1:
        lo = lo[:e]
    return lo.strip()


def _excerpts(body):
    out = []
    b = body.encode("utf-8", "replace")
    pos = 0
    while pos < len(b) and len(out) < MAX_EXCERPTS_PER_BOOK:
        chunk = b[pos:pos + EXCERPT].decode("utf-8", "ignore").strip()
        if len(chunk) > 600:
            out.append(chunk)
        pos += STRIDE
    return out


def fetch_en(con, target_bytes, tier):
    urls = shard_urls(EN_DS, {"train"})[:MAX_SHARDS]
    kws = CON_SUBJ if tier == "consciousness" else ART_SUBJ
    # art: literary AND not primarily philosophy/religion
    ors = " OR ".join(["lower(METADATA) LIKE '%' || ? || '%'" for _ in kws])
    if tier == "art":
        nots = " AND ".join(["lower(METADATA) NOT LIKE '%' || ? || '%'" for _ in CON_SUBJ])
        where = f"WHERE ({ors}) AND ({nots})"
        params = [k.lower() for k in kws] + [k.lower() for k in CON_SUBJ]
    else:
        where = f"WHERE ({ors})"
        params = [k.lower() for k in kws]
    got, blocks, seen = 0, [], set()
    per_shard = max(1, target_bytes // max(1, len(urls)))
    for idx, url in enumerate(urls):
        if got >= target_bytes:
            break
        try:
            path = _local_shard(url, f"en_{tier}", idx)
        except Exception as e:
            print(f"  ! en/{idx} download skip: {e}", flush=True)
            continue
        # consciousness books are RARE -> scan far more rows to find them.
        lim = 12000 if tier == "consciousness" else 1500
        sql = f"SELECT TEXT FROM read_parquet('{path}') {where} LIMIT {lim}"
        rows = con.execute(sql, params).fetchall()
        sb = 0
        for (text,) in rows:
            body = _strip_pg(text or "")
            for ex in _excerpts(body):
                key = ex[:96]
                if key in seen:
                    continue
                seen.add(key); blocks.append(ex)
                nb = len(ex.encode("utf-8", "replace"))
                got += nb; sb += nb
                if got >= target_bytes:
                    break
            if sb >= per_shard or got >= target_bytes:
                break
    return blocks, got


def fetch_multi(con, lang, target_bytes, tier):
    urls = shard_urls(MULTI_DS, {lang})[:MAX_SHARDS]
    titles = CON_TITLE[lang] if tier == "consciousness" else ART_TITLE[lang]
    got, blocks, seen = 0, [], set()
    matched, fallback = 0, 0
    # pass 1: title-classified; pass 2 (art only): relaxed literary residual
    passes = ["classified"] + (["relaxed"] if tier == "art" else [])
    for pkind in passes:
        if got >= target_bytes:
            break
        if pkind == "classified":
            ors = " OR ".join(["lower(substr(text,1,400)) LIKE '%' || ? || '%'"
                               for _ in titles])
            where = f"WHERE ({ors})"
            params = [t.lower() for t in titles]
        else:
            where = ""
            params = []
        for idx, url in enumerate(urls):
            if got >= target_bytes:
                break
            try:
                path = _local_shard(url, lang, idx)
            except Exception as e:
                print(f"  ! {lang}/{idx} download skip: {e}", flush=True)
                continue
            sql = f"SELECT text FROM read_parquet('{path}') {where} LIMIT 3000"
            rows = con.execute(sql, params).fetchall() if params \
                else con.execute(sql).fetchall()
            for (text,) in rows:
                body = _strip_pg(text or "")
                added = False
                for ex in _excerpts(body):
                    key = ex[:96]
                    if key in seen:
                        continue
                    seen.add(key); blocks.append(ex)
                    got += len(ex.encode("utf-8", "replace")); added = True
                    if got >= target_bytes:
                        break
                if added:
                    matched += (pkind == "classified")
                    fallback += (pkind == "relaxed")
                if got >= target_bytes:
                    break
    return blocks, got, matched, fallback


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", required=True, choices=["art", "consciousness"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--mb-per-lang", type=float, default=12.0)
    args = ap.parse_args()

    token = _token()
    assert token, "no HF token"
    _token_cache[0] = token
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)
    con = _con()

    per_lang, per_lang_blocks, notes = {}, {}, {}
    with open(args.out, "wb") as f:
        blocks, got = fetch_en(con, target, args.tier)
        blob = ("\n\n".join(blocks)).encode("utf-8", "replace")[:target]
        blob = blob.decode("utf-8", "ignore").encode("utf-8")
        f.write(blob); f.write(b"\n\n")
        per_lang["en"] = len(blob); per_lang_blocks["en"] = len(blocks)
        notes["en"] = "sedthh/gutenberg_english subject-classified (parquet)"
        print(f"  {args.tier} en: {len(blob)} bytes / {len(blocks)} excerpts (subject-classified)", flush=True)

        for lang in MULTI_LANGS:
            blocks, got, mb, fb = fetch_multi(con, lang, target, args.tier)
            blob = ("\n\n".join(blocks)).encode("utf-8", "replace")[:target]
            blob = blob.decode("utf-8", "ignore").encode("utf-8")
            f.write(blob); f.write(b"\n\n")
            per_lang[lang] = len(blob); per_lang_blocks[lang] = len(blocks)
            notes[lang] = (f"manu/project_gutenberg title-classified={mb} books"
                           + (f" + mixed-literature residual={fb}" if fb else ""))
            print(f"  {args.tier} {lang}: {len(blob)} bytes / {len(blocks)} excerpts "
                  f"(title={mb}, residual={fb})", flush=True)

        per_lang["ko"] = 0; per_lang_blocks["ko"] = 0
        notes["ko"] = "NO Gutenberg Korean split (gap; ko art/consciousness fall back to wiki)"
        print(f"  {args.tier} ko: 0 bytes (HONEST GAP — no Gutenberg ko)", flush=True)

    h = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    size = os.path.getsize(args.out)
    print(json.dumps({
        "out": args.out, "tier": args.tier, "bytes": size,
        "mb": round(size / 1048576, 3), "sha256": h.hexdigest(),
        "per_lang_bytes": per_lang, "per_lang_blocks": per_lang_blocks,
        "per_lang_notes": notes,
        "source": "Gutenberg PUBLIC-DOMAIN parquet (sedthh/gutenberg_english en; manu/project_gutenberg fr/de/es)",
        "langs": ALL_LANGS, "excerpt_window": EXCERPT, "stride": STRIDE,
        "honest_gap": "ko has no Gutenberg split; fr/de/es far thinner than en",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
