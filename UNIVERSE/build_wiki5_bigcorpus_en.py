#!/usr/bin/env python3
"""build_wiki5_bigcorpus_en.py — EN-ONLY slice of build_wiki5_bigcorpus.py for the
7B G5-L2 recovery diagnostic. The full corpus concatenates en->zh->ru->ja->ko, so
the first `bytes_per_lang` bytes the L2 probe reads = the ENGLISH portion. We only
need that English slice, so build ONLY en (deterministic, byte-identical to the
en head of the training corpus). build_wiki5_bigcorpus.py logic VERBATIM, en only.

Usage: build_wiki5_bigcorpus_en.py <out_path> <bytes> <workdir>
"""
import hashlib, os, sys, json
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

REPO = "wikimedia/wikipedia"; DATE = "20231101"
SHARDS_EN = 41  # same as build_wiki5_bigcorpus.SHARDS["en"]


def _doc_key(text):
    t = " ".join(text.split()); head = t[:200]; tail = t[-200:]; bucket = len(t) // 256
    return hashlib.blake2b(f"{head}\x00{tail}\x00{bucket}".encode("utf-8", "replace"),
                           digest_size=16).digest()


def collect_en(target_bytes, workdir):
    seen = set(); out = []; got = 0; n_docs = 0; n_dup = 0
    for si in range(SHARDS_EN):
        if got >= target_bytes: break
        fn = f"{DATE}.en/train-{si:05d}-of-{SHARDS_EN:05d}.parquet"
        path = hf_hub_download(REPO, fn, repo_type="dataset",
                               cache_dir=os.path.join(workdir, "hfcache"),
                               token=os.environ.get("HF_TOKEN"))
        pf = pq.ParquetFile(path)
        for batch in pf.iter_batches(batch_size=2000, columns=["text"]):
            for text in batch.column("text").to_pylist():
                if not text: continue
                k = _doc_key(text)
                if k in seen: n_dup += 1; continue
                seen.add(k)
                b = (text.strip() + "\n\n").encode("utf-8", "replace")
                out.append(b); got += len(b); n_docs += 1
                if got >= target_bytes: break
            if got >= target_bytes: break
        try: os.remove(path)
        except OSError: pass
        print(f"  en shard {si}: got={got} docs={n_docs} dup={n_dup}", flush=True)
    return b"".join(out)[:target_bytes]


def main():
    out_path = sys.argv[1]; nbytes = int(sys.argv[2]); workdir = sys.argv[3]
    os.makedirs(workdir, exist_ok=True)
    data = collect_en(nbytes, workdir)
    with open(out_path, "wb") as f: f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    print(f"CORPUS_OUT {out_path} bytes={len(data)} sha256={sha}", flush=True)


if __name__ == "__main__": main()
