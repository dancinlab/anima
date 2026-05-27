#!/usr/bin/env python3
"""Build a Korean-wiki clean corpus jsonl for P21K Korean-generalization train.

Forked from build_diverse_corpus_p21g.py. Multi-source Korean fallback:
  1. wikimedia/wikipedia ko (full Korean Wikipedia dump) — primary
  2. lcw99/wikipedia-korean-20221001 — fallback (community Korean wiki snapshot)
  3. graelo/wikipedia 20230601.ko — fallback
  4. heegyu/kowiki-sentences — fallback (sentence-level Korean wiki)
  5. nlpai-lab/openassistant-guanaco-ko — last-resort small Korean chat fallback

Writes jsonl with {"text": "..."} format. Drops empty / section-header rows.
"""
import argparse
import json
import os
import sys
import traceback


PRIMARY_SOURCES = [
    # (dataset_name, dataset_config, split)
    ("wikimedia/wikipedia", "20231101.ko", "train"),
    ("lcw99/wikipedia-korean-20221001", None, "train"),
    ("graelo/wikipedia", "20230601.ko", "train"),
    ("heegyu/kowiki-sentences", None, "train"),
    ("nlpai-lab/openassistant-guanaco-ko", None, "train"),
]


def try_load(name, config, split):
    """Try load_dataset; return iterator of dicts or None."""
    from datasets import load_dataset
    try:
        if config is None:
            ds = load_dataset(name, split=split, streaming=True)
        else:
            ds = load_dataset(name, config, split=split, streaming=True)
        print(f"[p21k-build] loaded {name}/{config} streaming OK", flush=True)
        return ds
    except Exception as e:
        print(f"[p21k-build] failed {name}/{config}: {type(e).__name__}: {str(e)[:200]}",
              flush=True)
        return None


def extract_text(row):
    # wikipedia-style: {"id":..., "title":..., "text":...}
    # heegyu/kowiki-sentences: {"text":...}
    # guanaco-ko: {"text":"### Human: ...### Assistant: ..."}
    for key in ("text", "content", "story", "sentence"):
        v = row.get(key)
        if isinstance(v, str) and v.strip():
            return v
    # fallback: title + text join
    t, b = row.get("title", ""), row.get("body", "")
    if t or b:
        return (str(t) + "\n" + str(b)).strip()
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--target-mb", type=int, default=60)
    args = ap.parse_args()

    print(f"[p21k-build] target {args.target_mb} MB → {args.out}", flush=True)

    ds = None
    used_source = None
    for name, config, split in PRIMARY_SOURCES:
        ds = try_load(name, config, split)
        if ds is not None:
            used_source = f"{name}/{config or '-'}"
            break

    if ds is None:
        print(f"[p21k-build] FATAL: all dataset sources failed", flush=True)
        sys.exit(1)

    target_bytes = args.target_mb * 1024 * 1024
    written = 0
    n_recs = 0
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        try:
            for row in ds:
                text = extract_text(row)
                if not text or not text.strip():
                    continue
                stripped = text.strip()
                # skip wikitext section-headers " = Title = "
                if stripped.startswith("=") and stripped.endswith("="):
                    continue
                # crude Korean-character ratio filter (>= 20% Hangul)
                if len(stripped) > 40:
                    n_ko = sum(1 for c in stripped if "가" <= c <= "힣")
                    if n_ko / len(stripped) < 0.20:
                        continue
                f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")
                written += len(text.encode("utf-8", errors="replace"))
                n_recs += 1
                if written >= target_bytes:
                    break
        except Exception as e:
            print(f"[p21k-build] iterator error after {n_recs} recs: {type(e).__name__}: {str(e)[:200]}",
                  flush=True)
            traceback.print_exc()

    print(f"[p21k-build] DONE source={used_source} wrote {n_recs:,} records, "
          f"{written:,} UTF-8 bytes ({written/1024/1024:.1f} MB)", flush=True)
    with open(args.out + ".source.json", "w") as f:
        json.dump({"source": used_source, "n_records": n_recs,
                   "bytes": written}, f, indent=2)


if __name__ == "__main__":
    main()
