#!/usr/bin/env python3
"""Build a BIG real multilingual byte corpus from wikimedia/wikipedia (5 langs).

Lane P data-gate fix (F-CLM-LANEP-GEN2): the 1.65MB FLORES corpus was small
enough that a 7.479M-param byte LM MEMORIZED it (train_ce 0.61 vs val_ce 1.82,
rel_gap 1.96). This builds a >=100MB real multilingual UTF-8 byte corpus from
wikimedia/wikipedia 20231101 for the SAME 5 langs (en/zh/ru/ja/ko), large enough
that ~1 epoch cannot be memorized.

Source: wikimedia/wikipedia (HF Hub) parquet shards, read DIRECTLY via
huggingface_hub.hf_hub_download + pyarrow (NO `datasets`/pandas/numpy — that
stack is broken by NumPy 2.x on the host). Real article prose only. Per-lang
near-duplicate docs are dropped (exact + shingled-hash). Streams equal target
bytes per language, concatenated to one UTF-8 stream.

Usage: build_wiki5_bigcorpus.py <out_path> <bytes_per_lang> <workdir>
"""
import hashlib, os, sys, json
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

REPO = "wikimedia/wikipedia"
DATE = "20231101"
LANGS = ["en", "zh", "ru", "ja", "ko"]
# enough shards per lang to comfortably exceed the per-lang byte target;
# we stop reading as soon as the target is hit, so over-listing is free.
SHARDS = {"en": 41, "zh": 6, "ru": 21, "ja": 15, "ko": 3}


def _doc_key(text):
    """Near-dup key: normalized first 200 + last 200 chars + length bucket."""
    t = " ".join(text.split())
    head = t[:200]
    tail = t[-200:]
    bucket = len(t) // 256
    return hashlib.blake2b(f"{head}\x00{tail}\x00{bucket}".encode("utf-8", "replace"),
                           digest_size=16).digest()


def collect_lang(lang, target_bytes, workdir, manifest):
    seen = set()
    out = []
    got = 0
    n_docs = 0
    n_dup = 0
    nshard = SHARDS[lang]
    for si in range(nshard):
        if got >= target_bytes:
            break
        fn = f"{DATE}.{lang}/train-{si:05d}-of-{nshard:05d}.parquet"
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
        # free the parquet shard from disk cache to bound disk use
        try:
            os.remove(path)
        except OSError:
            pass
        print(f"  {lang} shard {si}: got={got} docs={n_docs} dup={n_dup}", flush=True)
    blob = b"".join(out)[:target_bytes]
    manifest.append({"lang": lang, "bytes": len(blob), "docs": n_docs,
                     "dups_dropped": n_dup})
    print(f"LANG {lang} bytes={len(blob)} docs={n_docs} dup={n_dup}", flush=True)
    return blob


def main():
    out_path = sys.argv[1]
    bytes_per_lang = int(sys.argv[2])
    workdir = sys.argv[3]
    os.makedirs(workdir, exist_ok=True)
    manifest = []
    blobs = []
    for lang in LANGS:
        print(f"=== collecting {lang} target={bytes_per_lang} ===", flush=True)
        blobs.append(collect_lang(lang, bytes_per_lang, workdir, manifest))
    data = b"".join(blobs)
    with open(out_path, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    card = {
        "source": f"{REPO} {DATE}",
        "langs": LANGS,
        "total_bytes": len(data),
        "sha256": sha,
        "bytes_per_lang_target": bytes_per_lang,
        "per_lang": manifest,
        "dedup": "exact + shingled head/tail/length-bucket blake2b key",
        "encoding": "utf-8 (replace), article text col, doc-joined \\n\\n",
    }
    with open(out_path + ".card.json", "w") as f:
        json.dump(card, f, indent=2, ensure_ascii=False)
    print(f"CORPUS_OUT {out_path} bytes={len(data)} sha256={sha}", flush=True)
    print("CARD " + json.dumps(card, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
