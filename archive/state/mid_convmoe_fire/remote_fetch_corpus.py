#!/usr/bin/env python3
"""remote_fetch_corpus.py — fetch a BALANCED 5-lang byte SUBSET from R2 (phanes
anima-7b/web/<lang>/shard0000.bytes) via byte-range GETs, CONCAT to ONE bytes
file the trainer consumes as --corpus. READ-ONLY on anima-7b/ (range GET only).

Balanced subset: PER_LANG_MB from the START of each shard0000, langs eng/fra/deu/
spa/kor (incl ko). Byte V=256, no tokenizer. Deterministic (fixed range offsets).
"""
import os, sys, boto3, hashlib, json

PER_LANG_MB = int(os.environ.get("PER_LANG_MB", "800"))   # 800MB x5 = ~4.0 GB
LANGS = [("eng","en"),("fra","fr"),("deu","de"),("spa","es"),("kor","ko")]
OUT = os.environ.get("CORPUS_OUT", "/workspace/mid_corpus_5lang.bytes")

acc=os.environ["R2_ACCOUNT_ID"]; ak=os.environ["R2_ACCESS_KEY_ID"]
sk=os.environ["R2_SECRET_ACCESS_KEY"]; bk=os.environ["R2_BUCKET"]
ep=f"https://{acc}.r2.cloudflarestorage.com"
s3=boto3.client("s3", endpoint_url=ep, aws_access_key_id=ak,
                aws_secret_access_key=sk, region_name="auto")

nbytes = PER_LANG_MB * 1024 * 1024
h = hashlib.sha256()
meta = {"per_lang_mb": PER_LANG_MB, "langs": [], "out": OUT}
total = 0
with open(OUT, "wb") as fout:
    for d3, d2 in LANGS:
        key = f"anima-7b/web/{d3}/shard0000.bytes"
        rng = f"bytes=0-{nbytes-1}"
        print(f"FETCH {key} {rng}", flush=True)
        r = s3.get_object(Bucket=bk, Key=key, Range=rng)
        body = r["Body"].read()
        fout.write(body)
        h.update(body)
        total += len(body)
        meta["langs"].append({"lang": d2, "shard": key, "bytes": len(body)})
        print(f"  wrote {len(body)} bytes ({d2})", flush=True)
meta["total_bytes"] = total
meta["sha256"] = h.hexdigest()
print("CORPUS_DONE " + json.dumps(meta), flush=True)
with open(OUT + ".meta.json", "w") as f:
    json.dump(meta, f, indent=2)
