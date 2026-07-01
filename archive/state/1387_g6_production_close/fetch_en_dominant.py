#!/usr/bin/env python3
"""fetch_en_dominant.py — H_1129 SCRIPT-CONTROL corpus: english-dominant + ASCII-filter.
Fetch a large english shard + small fr/de/es (NO kor — the dominant-script collapse driver),
then ASCII-filter (drop bytes >=128) so the model sees a single-script (Latin/English) stream.
This is the H_1129 4th ingredient (script-control) that turned 303M FALS 0->1 for ByteGPT."""
import os, boto3, hashlib, json
EN_MB = int(os.environ.get("EN_MB", "1600"))     # english-dominant bulk
OTH_MB = int(os.environ.get("OTH_MB", "200"))    # small latin others (fr/de/es)
OUT = os.environ.get("CORPUS_OUT", "/workspace/corpus_en_dom.bytes")
acc=os.environ["R2_ACCOUNT_ID"]; ak=os.environ["R2_ACCESS_KEY_ID"]
sk=os.environ["R2_SECRET_ACCESS_KEY"]; bk=os.environ["R2_BUCKET"]
s3=boto3.client("s3", endpoint_url=f"https://{acc}.r2.cloudflarestorage.com",
                aws_access_key_id=ak, aws_secret_access_key=sk, region_name="auto")
def fetch(d3, mb):
    key=f"anima-7b/web/{d3}/shard0000.bytes"; n=mb*1024*1024
    r=s3.get_object(Bucket=bk, Key=key, Range=f"bytes=0-{n-1}")
    return r["Body"].read()
plan=[("eng",EN_MB),("fra",OTH_MB),("deu",OTH_MB),("spa",OTH_MB)]
h=hashlib.sha256(); total=0; total_raw=0; meta={"langs":[],"ascii_filter":True,"out":OUT}
with open(OUT,"wb") as f:
    for d3,mb in plan:
        body=fetch(d3,mb); total_raw+=len(body)
        # ASCII-filter: keep bytes < 128 (single-script Latin/English), drop multibyte non-Latin
        filt=bytes(b for b in body if b < 128)
        f.write(filt); h.update(filt); total+=len(filt)
        meta["langs"].append({"lang":d3,"raw":len(body),"ascii_kept":len(filt)})
        print(f"  {d3}: raw {len(body)} -> ascii {len(filt)}", flush=True)
meta["total_bytes"]=total; meta["total_raw"]=total_raw; meta["sha256"]=h.hexdigest()
print("CORPUS_DONE "+json.dumps(meta), flush=True)
with open(OUT+".meta.json","w") as mf: json.dump(meta,mf,indent=2)
