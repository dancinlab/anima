#!/usr/bin/env python3
"""Single attempt R2 download with python urllib + long socket timeout.

Streams bytes in 1MB chunks; reports progress to stderr; flushes to disk.
"""
import os
import sys
import time
import urllib.request
import socket

ACCOUNT_ID = sys.argv[1]
EMAIL = sys.argv[2]
KEY = sys.argv[3]
OUT = sys.argv[4]
TARGET = int(sys.argv[5])

url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/r2/buckets/anima-models/objects/conscious-lm/cells64/final.pt"

req = urllib.request.Request(
    url,
    headers={
        "X-Auth-Email": EMAIL,
        "X-Auth-Key": KEY,
    },
)

socket.setdefaulttimeout(120.0)  # 2 min socket idle timeout

t0 = time.time()
with urllib.request.urlopen(req, timeout=120.0) as resp, open(OUT, "wb") as f:
    print(f"[start] http={resp.status} headers-cl={resp.headers.get('Content-Length')}", file=sys.stderr)
    chunk = 1 << 20  # 1 MB
    written = 0
    last_report = 0
    while True:
        try:
            buf = resp.read(chunk)
        except (TimeoutError, socket.timeout) as e:
            print(f"[timeout] at {written} bytes: {e}", file=sys.stderr)
            break
        except Exception as e:
            print(f"[error] at {written} bytes: {type(e).__name__}: {e}", file=sys.stderr)
            break
        if not buf:
            break
        f.write(buf)
        written += len(buf)
        if written - last_report >= 10 * (1 << 20):
            elapsed = time.time() - t0
            mb = written / (1 << 20)
            rate = mb / elapsed if elapsed > 0 else 0
            print(f"[progress] {written:,} / {TARGET:,} bytes ({100.0*written/TARGET:.1f}%) {rate:.2f} MB/s", file=sys.stderr)
            last_report = written
elapsed = time.time() - t0
print(f"[done] wrote {written:,} bytes in {elapsed:.1f}s ({(written/(1<<20))/elapsed:.2f} MB/s)", file=sys.stderr)
print(f"[match] {'PASS' if written == TARGET else 'FAIL'} (target {TARGET:,})", file=sys.stderr)
