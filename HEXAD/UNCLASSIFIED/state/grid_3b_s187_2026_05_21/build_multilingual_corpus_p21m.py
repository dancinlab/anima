#!/usr/bin/env python3
"""Build a multilingual (en + ko + zh + ru + ja) wiki corpus jsonl for P21M.

Forked from build_korean_corpus_p21k.py. Per-language ≥20% native-script
filter (Hangul / CJK Han / Hiragana+Katakana+Han / Cyrillic / Latin),
streams ~10 MB per language, concats into single jsonl.

Per-language fallback sources to weather HF dataset outages.
"""
import argparse
import json
import os
import sys
import traceback


SOURCES = {
    "en": [
        ("Salesforce/wikitext", "wikitext-2-raw-v1", "train"),
        ("wikimedia/wikipedia", "20231101.en", "train"),
    ],
    "ko": [
        ("wikimedia/wikipedia", "20231101.ko", "train"),
        ("lcw99/wikipedia-korean-20221001", None, "train"),
        ("graelo/wikipedia", "20230601.ko", "train"),
        ("heegyu/kowiki-sentences", None, "train"),
    ],
    "zh": [
        ("wikimedia/wikipedia", "20231101.zh", "train"),
        ("graelo/wikipedia", "20230601.zh", "train"),
    ],
    "ru": [
        ("wikimedia/wikipedia", "20231101.ru", "train"),
        ("graelo/wikipedia", "20230601.ru", "train"),
    ],
    "ja": [
        ("wikimedia/wikipedia", "20231101.ja", "train"),
        ("graelo/wikipedia", "20230601.ja", "train"),
    ],
}


def native_ratio(text, lang):
    if not text:
        return 0.0
    n = 0
    L = len(text)
    if lang == "en":
        # at least latin-ish letters
        for c in text:
            if ("a" <= c <= "z") or ("A" <= c <= "Z"):
                n += 1
    elif lang == "ko":
        for c in text:
            if "가" <= c <= "힣":
                n += 1
    elif lang == "zh":
        # CJK Unified Ideographs
        for c in text:
            cp = ord(c)
            if 0x4E00 <= cp <= 0x9FFF:
                n += 1
    elif lang == "ja":
        # Hiragana 3040-309F + Katakana 30A0-30FF (excluding pure Han, since
        # zh corpus also has Han; require kana presence to be Japanese)
        for c in text:
            cp = ord(c)
            if (0x3040 <= cp <= 0x309F) or (0x30A0 <= cp <= 0x30FF):
                n += 1
    elif lang == "ru":
        # Cyrillic
        for c in text:
            cp = ord(c)
            if 0x0400 <= cp <= 0x04FF:
                n += 1
    return n / L


def try_load(name, config, split):
    from datasets import load_dataset
    try:
        if config is None:
            ds = load_dataset(name, split=split, streaming=True)
        else:
            ds = load_dataset(name, config, split=split, streaming=True)
        print(f"[p21m-build] loaded {name}/{config} streaming OK", flush=True)
        return ds
    except Exception as e:
        print(f"[p21m-build] failed {name}/{config}: {type(e).__name__}: {str(e)[:200]}",
              flush=True)
        return None


def extract_text(row):
    for key in ("text", "content", "story", "sentence"):
        v = row.get(key)
        if isinstance(v, str) and v.strip():
            return v
    t, b = row.get("title", ""), row.get("body", "")
    if t or b:
        return (str(t) + "\n" + str(b)).strip()
    return ""


def build_lang(lang, out_path, target_mb):
    sources = SOURCES[lang]
    ds = None
    used_source = None
    for name, config, split in sources:
        ds = try_load(name, config, split)
        if ds is not None:
            used_source = f"{name}/{config or '-'}"
            break
    if ds is None:
        print(f"[p21m-build] FATAL: all {lang} sources failed", flush=True)
        return None

    target_bytes = target_mb * 1024 * 1024
    # JA needs kana; threshold lower (kana sparser than Han in mixed text)
    threshold = 0.05 if lang == "ja" else 0.20
    if lang == "en":
        threshold = 0.50  # latin letters are dense; tighter
    written = 0
    n_recs = 0
    n_filtered = 0
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        try:
            for row in ds:
                text = extract_text(row)
                if not text or not text.strip():
                    continue
                stripped = text.strip()
                if stripped.startswith("=") and stripped.endswith("="):
                    continue
                if len(stripped) > 40:
                    r = native_ratio(stripped, lang)
                    if r < threshold:
                        n_filtered += 1
                        continue
                f.write(json.dumps({"text": text, "lang": lang},
                                   ensure_ascii=False) + "\n")
                written += len(text.encode("utf-8", errors="replace"))
                n_recs += 1
                if written >= target_bytes:
                    break
        except Exception as e:
            print(f"[p21m-build] {lang} iter error after {n_recs}: {type(e).__name__}: {str(e)[:200]}",
                  flush=True)
            traceback.print_exc()
    print(f"[p21m-build] DONE lang={lang} source={used_source} "
          f"records={n_recs:,} bytes={written:,} ({written/1024/1024:.1f} MB) "
          f"filtered={n_filtered:,}",
          flush=True)
    return {
        "lang": lang, "source": used_source,
        "records": n_recs, "bytes": written, "filtered": n_filtered,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True,
                    help="output jsonl path (concatenated all langs)")
    ap.add_argument("--target-mb-per-lang", type=int, default=10)
    ap.add_argument("--langs", default="en,ko,zh,ru,ja")
    ap.add_argument("--per-lang-dir", default=None,
                    help="if set, also write per-lang jsonl into this dir")
    args = ap.parse_args()

    langs = [l.strip() for l in args.langs.split(",") if l.strip()]
    print(f"[p21m-build] langs={langs} target_mb/lang={args.target_mb_per_lang}",
          flush=True)

    per_dir = args.per_lang_dir or (os.path.dirname(args.out) or ".")
    os.makedirs(per_dir, exist_ok=True)

    summaries = []
    per_lang_paths = []
    for lang in langs:
        p = os.path.join(per_dir, f"wiki_{lang}.jsonl")
        s = build_lang(lang, p, args.target_mb_per_lang)
        if s is not None:
            summaries.append(s)
            per_lang_paths.append(p)
        else:
            print(f"[p21m-build] WARN lang={lang} produced nothing — skipping",
                  flush=True)

    # concat into out
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    total_bytes = 0
    total_recs = 0
    with open(args.out, "w", encoding="utf-8") as fout:
        for p in per_lang_paths:
            with open(p, "r", encoding="utf-8") as fin:
                for line in fin:
                    fout.write(line)
                    total_bytes += len(line.encode("utf-8", errors="replace"))
                    total_recs += 1
    print(f"[p21m-build] CONCAT DONE: {total_recs:,} records, "
          f"{total_bytes/1024/1024:.1f} MB → {args.out}", flush=True)

    with open(args.out + ".source.json", "w") as f:
        json.dump({"langs": langs, "per_lang": summaries,
                   "total_records": total_recs,
                   "total_bytes": total_bytes}, f, indent=2)


if __name__ == "__main__":
    main()
