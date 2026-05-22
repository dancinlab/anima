#!/usr/bin/env python3
"""Build a Wikipedia-EN clean corpus jsonl for P21G generalization train.

Forked from build_wikitext_corpus.py with multi-source fallback:
  1. wikitext-2-raw-v1 (small, fast, ~12 MB) — primary, low parse risk
  2. wikitext-103-raw-v1 (large, ~500 MB raw) — fallback
  3. EleutherAI/wikitext_document_level (already-cleaned chunks) — fallback
  4. roneneldan/TinyStories (small, fast, fully diverse-narrative) — fallback
  5. WriteToFile with embedded sample text — last-resort 0.5 MB diversity stub

If `load_dataset("wikitext", "wikitext-2-raw-v1")` raises an HfUriError or
similar invalid-URI bug, fall through to the next. Writes a jsonl with
{"text": "..."} format matching the trainer.
"""
import argparse
import json
import os
import sys
import traceback


PRIMARY_SOURCES = [
    # (dataset_name, dataset_config, split)
    ("Salesforce/wikitext", "wikitext-2-raw-v1", "train"),
    ("Salesforce/wikitext", "wikitext-103-raw-v1", "train"),
    ("wikitext", "wikitext-2-raw-v1", "train"),
    ("wikitext", "wikitext-103-raw-v1", "train"),
    ("roneneldan/TinyStories", None, "train"),
]


def try_load(name, config, split):
    """Try load_dataset; return iterator of {text: str} dicts or None."""
    from datasets import load_dataset
    try:
        if config is None:
            ds = load_dataset(name, split=split, streaming=True)
        else:
            ds = load_dataset(name, config, split=split, streaming=True)
        print(f"[p21g-build] loaded {name}/{config} streaming OK", flush=True)
        return ds
    except Exception as e:
        print(f"[p21g-build] failed {name}/{config}: {type(e).__name__}: {str(e)[:200]}",
              flush=True)
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--target-mb", type=int, default=60)
    args = ap.parse_args()

    print(f"[p21g-build] target {args.target_mb} MB → {args.out}", flush=True)

    ds = None
    used_source = None
    for name, config, split in PRIMARY_SOURCES:
        ds = try_load(name, config, split)
        if ds is not None:
            used_source = f"{name}/{config or '-'}"
            break

    if ds is None:
        print(f"[p21g-build] FATAL: all dataset sources failed", flush=True)
        sys.exit(1)

    target_bytes = args.target_mb * 1024 * 1024
    written = 0
    n_recs = 0
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        try:
            for row in ds:
                # try several common text fields
                text = (row.get("text") or row.get("story")
                        or row.get("content") or "")
                if not text or not text.strip():
                    continue
                stripped = text.strip()
                # skip wikitext section-headers " = Title = "
                if stripped.startswith("=") and stripped.endswith("="):
                    continue
                f.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")
                written += len(text.encode("utf-8", errors="replace"))
                n_recs += 1
                if written >= target_bytes:
                    break
        except Exception as e:
            print(f"[p21g-build] iterator error after {n_recs} recs: {type(e).__name__}: {str(e)[:200]}",
                  flush=True)
            traceback.print_exc()

    print(f"[p21g-build] DONE source={used_source} wrote {n_recs:,} records, "
          f"{written:,} UTF-8 bytes ({written/1024/1024:.1f} MB)", flush=True)
    # write the source metadata as sidecar
    with open(args.out + ".source.json", "w") as f:
        json.dump({"source": used_source, "n_records": n_recs,
                   "bytes": written}, f, indent=2)


if __name__ == "__main__":
    main()
