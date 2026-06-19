#!/usr/bin/env python3
"""Build a LARGE real multilingual byte corpus from wikimedia/wikipedia for the
Lane P ~3B rung — a configurable scale-up of build_wiki5_bigcorpus.py.

WHY: the gen2 d768 run used 150MB (5 langs x 30MB) — fine for a 7.5M-param model
at ~1 epoch, but FAR too small for a 3.07B-param model (Chinchilla-optimal ~20
tokens/param = ~60GB). Clean-license wikipedia cannot reach 60GB, so this builds
the LARGEST practical clean multilingual corpus and the trainer STATES the exact
token/param ratio honestly (a_scale_honest_scope) — an undertrained 3B is an
HONEST negative, not a hidden failure.

Source: wikimedia/wikipedia (HF Hub) parquet shards via huggingface_hub +
pyarrow (NO `datasets`/pandas/numpy — broken by NumPy 2.x on the host). Real
article prose only. Per-lang near-duplicate docs dropped (exact + shingled-hash).
NO synthetic padding.

Usage:
  build_wiki_3b_corpus.py <out_path> <bytes_per_lang> <workdir> [langs_csv]
    langs_csv defaults to a 12-lang mix; pass e.g. "en,zh,ru,ja,ko,de,fr,es"
"""
import hashlib, os, sys, json
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download, list_repo_files

REPO = "wikimedia/wikipedia"
DATE = "20231101"
# A broad clean-license mix. Bytes-per-lang is the same target for all; small
# langs may fall short of target (we read all their shards) — reported honestly.
DEFAULT_LANGS = ["en", "zh", "ru", "ja", "ko", "de", "fr", "es", "it", "pt", "nl", "pl"]


def _doc_key(text):
    t = " ".join(text.split())
    head = t[:200]
    tail = t[-200:]
    bucket = len(t) // 256
    return hashlib.blake2b(f"{head}\x00{tail}\x00{bucket}".encode("utf-8", "replace"),
                           digest_size=16).digest()


def _shard_files(lang):
    """List all train parquet shards for a lang config from the HF repo tree."""
    prefix = f"{DATE}.{lang}/"
    try:
        files = [f for f in list_repo_files(REPO, repo_type="dataset")
                 if f.startswith(prefix) and f.endswith(".parquet")]
    except Exception as e:
        print(f"  WARN list_repo_files({lang}) failed: {e}", flush=True)
        files = []
    files.sort()
    return files


def collect_lang(lang, target_bytes, workdir, manifest):
    seen = set()
    out = []
    got = 0
    n_docs = 0
    n_dup = 0
    files = _shard_files(lang)
    if not files:
        print(f"LANG {lang} NO SHARDS (skipped)", flush=True)
        manifest.append({"lang": lang, "bytes": 0, "docs": 0, "dups_dropped": 0,
                         "shards_available": 0})
        return b""
    for fn in files:
        if got >= target_bytes:
            break
        path = hf_hub_download(REPO, fn, repo_type="dataset",
                               cache_dir=os.path.join(workdir, "hfcache"))
        pf = pq.ParquetFile(path)
        for batch in pf.iter_batches(batch_size=2000, columns=["text"]):
            texts = batch.column("text").to_pylist()
            for text in texts:
                if not text:
                    continue
                k = _doc_key(text)
                if k in seen:
                    n_dup += 1
                    continue
                seen.add(k)
                b = (text.strip() + "\n\n").encode("utf-8", "replace")
                out.append(b)
                got += len(b)
                n_docs += 1
                if got >= target_bytes:
                    break
            if got >= target_bytes:
                break
        try:
            os.remove(path)
        except OSError:
            pass
        print(f"  {lang} shard {os.path.basename(fn)}: got={got} docs={n_docs} dup={n_dup}", flush=True)
    blob = b"".join(out)[:target_bytes]
    manifest.append({"lang": lang, "bytes": len(blob), "docs": n_docs,
                     "dups_dropped": n_dup, "shards_available": len(files),
                     "hit_target": len(blob) >= target_bytes})
    print(f"LANG {lang} bytes={len(blob)} docs={n_docs} dup={n_dup} "
          f"shards={len(files)} hit_target={len(blob) >= target_bytes}", flush=True)
    return blob


def main():
    out_path = sys.argv[1]
    bytes_per_lang = int(sys.argv[2])
    workdir = sys.argv[3]
    langs = (sys.argv[4].split(",") if len(sys.argv) > 4 else DEFAULT_LANGS)
    os.makedirs(workdir, exist_ok=True)
    manifest = []
    blobs = []
    for lang in langs:
        print(f"=== collecting {lang} target={bytes_per_lang} ===", flush=True)
        blobs.append(collect_lang(lang, bytes_per_lang, workdir, manifest))
    data = b"".join(blobs)
    with open(out_path, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    card = {
        "source": f"{REPO} {DATE}",
        "langs": langs,
        "total_bytes": len(data),
        "total_GB": round(len(data) / 1e9, 4),
        "sha256": sha,
        "bytes_per_lang_target": bytes_per_lang,
        "per_lang": manifest,
        "dedup": "exact + shingled head/tail/length-bucket blake2b key",
        "encoding": "utf-8 (replace), article text col, doc-joined \\n\\n",
        "synthetic_padding": False,
        "purpose": "Lane P ~3B byte-LM training corpus (clean-license wikipedia only)",
    }
    with open(out_path + ".card.json", "w") as f:
        json.dump(card, f, indent=2, ensure_ascii=False)
    print(f"CORPUS_OUT {out_path} bytes={len(data)} ({len(data)/1e9:.4f}GB) sha256={sha}", flush=True)
    print("CARD " + json.dumps(card, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
