#!/usr/bin/env python
"""Prep the 5-lang c4 backbone corpus for the Lane-G-ref 7B fire.

Downloads dancinlab/clm-backbone-5lang-sample (the SAME corpus the 85.6M PUBLIC
and 3.149B reference rungs used) and flattens it to a single byte stream at
/root/laneg_ref_7b/corpus.txt (UTF-8). Prints the resulting byte count + sha.
"""
import os, hashlib
from huggingface_hub import snapshot_download

OUT = "/root/laneg_ref_7b/corpus.txt"
p = snapshot_download(repo_id="dancinlab/clm-backbone-5lang-sample", repo_type="dataset")
print("SNAPDIR", p, flush=True)

texts = []
for root, _, fs in os.walk(p):
    for f in sorted(fs):
        fp = os.path.join(root, f)
        low = f.lower()
        if low.endswith((".txt",)):
            with open(fp, "r", encoding="utf-8", errors="replace") as h:
                texts.append(h.read())
        elif low.endswith((".json", ".jsonl")):
            import json
            with open(fp, "r", encoding="utf-8", errors="replace") as h:
                if low.endswith(".jsonl"):
                    for line in h:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            o = json.loads(line)
                        except Exception:
                            texts.append(line)
                            continue
                        if isinstance(o, dict):
                            v = o.get("text") or o.get("content") or o.get("raw") or ""
                            if v:
                                texts.append(v if isinstance(v, str) else str(v))
                        elif isinstance(o, str):
                            texts.append(o)
                else:
                    try:
                        o = json.load(h)
                    except Exception:
                        h.seek(0)
                        texts.append(h.read())
                        continue
                    if isinstance(o, list):
                        for it in o:
                            if isinstance(it, dict):
                                v = it.get("text") or it.get("content") or it.get("raw") or ""
                                if v:
                                    texts.append(v if isinstance(v, str) else str(v))
                            elif isinstance(it, str):
                                texts.append(it)
        elif low.endswith((".parquet",)):
            try:
                import pyarrow.parquet as pq
                tbl = pq.read_table(fp)
                cols = tbl.column_names
                tcol = "text" if "text" in cols else ("content" if "content" in cols else cols[0])
                for v in tbl.column(tcol).to_pylist():
                    if v:
                        texts.append(v if isinstance(v, str) else str(v))
            except Exception as e:
                print("parquet skip", fp, e, flush=True)

blob = "\n".join(texts)
data = blob.encode("utf-8", errors="replace")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "wb") as h:
    h.write(data)
sha = hashlib.sha256(data).hexdigest()
print(f"CORPUS_BYTES={len(data)}", flush=True)
print(f"CORPUS_SHA256={sha}", flush=True)
print(f"CORPUS_PATH={OUT}", flush=True)
print(f"N_TEXTS={len(texts)}", flush=True)
