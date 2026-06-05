#!/usr/bin/env python3
"""Fetch a balanced 5-lang SUBSET (en/fr/de/es/ko shard0000) of the R2 webscale
corpus and CONCAT into ONE byte file for train_lane_p.py --corpus.

R2 bucket=phanes prefix=anima-7b/web/<lang>/shardNNNN.bytes (byte V=256).
Creds via `secret get r2.phanes.{account_id,access_key_id,secret_access_key,bucket}`.
READ-ONLY against R2 (anima-7b/ is DO-NOT-TOUCH; we only GET).
"""
import os, sys, subprocess, boto3
from botocore.config import Config

# R2 uses ISO-639-3 dir names: eng/fra/deu/spa/kor. ko (kor) INCLUDED, balanced.
LANGS = ["eng", "fra", "deu", "spa", "kor"]
SHARD = os.environ.get("SHARD", "shard0000")
OUT = sys.argv[1] if len(sys.argv) > 1 else "mid_corpus_5lang.bytes"
# cap per-lang bytes so the concat lands ~3-6 GB total balanced (override CAP_MB)
CAP_MB = int(os.environ.get("CAP_MB", "900"))
CAP = CAP_MB * 1024 * 1024


def sec(k):
    return subprocess.check_output(["secret", "get", f"r2.phanes.{k}"]).decode().strip()


def main():
    acct = sec("account_id"); ak = sec("access_key_id")
    sk = sec("secret_access_key"); bucket = sec("bucket")
    ep = f"https://{acct}.r2.cloudflarestorage.com"
    s3 = boto3.client("s3", endpoint_url=ep, aws_access_key_id=ak,
                      aws_secret_access_key=sk, region_name="auto",
                      config=Config(signature_version="s3v4"))
    total = 0
    per_lang = {}
    with open(OUT, "wb") as out:
        for lang in LANGS:
            key = f"anima-7b/web/{lang}/{SHARD}.bytes"
            candidates = [key, f"anima-7b/web/{lang}/{SHARD}",
                          f"anima-7b/{lang}/{SHARD}.bytes"]
            got = None
            for c in candidates:
                try:
                    s3.head_object(Bucket=bucket, Key=c)
                    got = c; break
                except Exception:
                    continue
            if got is None:
                pref = f"anima-7b/web/{lang}/"
                r = s3.list_objects_v2(Bucket=bucket, Prefix=pref, MaxKeys=5)
                contents = r.get("Contents", [])
                if not contents:
                    print(f"LANG {lang}: NO OBJECTS under {pref} (skipped)", flush=True)
                    per_lang[lang] = 0
                    continue
                got = contents[0]["Key"]
                print(f"LANG {lang}: shard0000 not found, using first listed {got}", flush=True)
            obj = s3.get_object(Bucket=bucket, Key=got)
            body = obj["Body"]
            wrote = 0
            while wrote < CAP:
                chunk = body.read(8 * 1024 * 1024)
                if not chunk:
                    break
                if wrote + len(chunk) > CAP:
                    chunk = chunk[:CAP - wrote]
                out.write(chunk)
                wrote += len(chunk)
            per_lang[lang] = wrote
            total += wrote
            print(f"LANG {lang}: key={got} wrote={wrote} ({wrote/1e9:.3f} GB)", flush=True)
    print(f"DONE out={OUT} total={total} ({total/1e9:.3f} GB) per_lang={per_lang}", flush=True)


if __name__ == "__main__":
    main()
