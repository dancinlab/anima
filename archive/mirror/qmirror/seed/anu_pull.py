#!/usr/bin/env python3
"""anu_pull.py — self-contained LIVE ANU quantum-entropy puller (H_923 M4).

Pulls REAL ANU vacuum-fluctuation bytes from the ANU Quantum Numbers API, keyed
via the `secret` CLI, and writes a .bin + a provenance.jsonl row (ts, tier,
n_bytes, sha256, request_id) — the same provenance shape the qmirror anu_legacy
path uses, so H_923's probe can consume a FRESH per-experiment quantum draw.

Why standalone: the canonical `pull_live.hexa` is coupled to ~/core/qmirror's
entropy module (absent on this host) and looks up non-matching key names. This
module wires the ACTUAL secret keys (flat.anu_key_paid / flat.anu_key_free) and
depends only on the Python stdlib + the `secret` CLI.

Tier chain (first available wins):
  T1.c paid   secret flat.anu_key_paid   -> api.quantumnumbers.anu.edu.au (x-api-key)
  T1.b free   secret flat.anu_key_free   -> api.quantumnumbers.anu.edu.au (x-api-key)
  T1.a legacy (keyless)                  -> qrng.anu.edu.au/API/jsonI.php  (rate-throttled)

Usage:
  anu_pull.py --bytes 1024 --out qrng_fresh.bin [--provenance provenance.jsonl]
Honest C3 (#123-A): ANU statistical quality == chacha20 PRNG (JSD 23x under NIST).
The value is PROVENANCE / audit / algorithmic-attack immunity / ontology — not
better randomness. NOT a phenomenal-consciousness claim.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

SECRET_BIN = os.environ.get("SECRET_BIN") or "secret"
API_KEYED = "https://api.quantumnumbers.anu.edu.au/"          # x-api-key, type=uint8
API_LEGACY = "https://qrng.anu.edu.au/API/jsonI.php"          # keyless, throttled
MAX_PER_REQ = 1024                                            # ANU per-request cap


def _secret_get(name: str) -> str:
    """Return the secret value for `name`, or "" if absent. Never logs the value."""
    try:
        v = subprocess.run([SECRET_BIN, "get", name], capture_output=True,
                           text=True, timeout=10)
        return v.stdout.strip() if v.returncode == 0 else ""
    except Exception:  # noqa: BLE001
        return ""


def _resolve_key() -> tuple[str, str]:
    """(tier, key). Prefer paid (100 req/s) > free (100 req/min) > legacy keyless."""
    for tier, name in (("anu_paid", "flat.anu_key_paid"),
                       ("anu_free", "flat.anu_key_free")):
        k = os.environ.get("NEXUS_QMIRROR_ANU_KEY", "") or _secret_get(name)
        if k:
            return tier, k
    return "anu_legacy", ""


def _http_json(url: str, headers: dict, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 (trusted ANU host)
        return json.loads(r.read().decode())


def _pull_chunk(n: int, tier: str, key: str) -> tuple[bytes, str]:
    """Pull n<=1024 bytes. Returns (bytes, request_id)."""
    if tier == "anu_legacy":
        url = f"{API_LEGACY}?length={n}&type=uint8"
        j = _http_json(url, {"User-Agent": "anima-qmirror/anu_pull"})
        if not j.get("success"):
            raise RuntimeError(f"ANU legacy fail: {j}")
        return bytes(int(x) for x in j["data"]), f"anu_legacy_{j.get('length', n)}"
    url = f"{API_KEYED}?length={n}&type=uint8"
    j = _http_json(url, {"x-api-key": key, "User-Agent": "anima-qmirror/anu_pull"})
    if not j.get("success"):
        raise RuntimeError(f"ANU keyed fail: {j}")
    return bytes(int(x) for x in j["data"]), f"{tier}_keyed"


def pull(n_bytes: int) -> tuple[bytes, str, str]:
    """Pull n_bytes of ANU entropy, chunked. Returns (bytes, tier, request_id)."""
    tier, key = _resolve_key()
    out = bytearray()
    rid = ""
    while len(out) < n_bytes:
        want = min(MAX_PER_REQ, n_bytes - len(out))
        chunk, rid = _pull_chunk(want, tier, key)
        if not chunk:
            raise RuntimeError("ANU returned empty chunk")
        out.extend(chunk)
    return bytes(out[:n_bytes]), tier, rid


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bytes", type=int, default=1024)
    ap.add_argument("--out", default="qrng_fresh.bin")
    ap.add_argument("--provenance", default="provenance.jsonl")
    ap.add_argument("--ts", default="", help="ISO ts (caller-supplied for determinism)")
    a = ap.parse_args()

    try:
        raw, tier, rid = pull(a.bytes)
    except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
        print(json.dumps({"ok": 0, "error": repr(e)}))
        return 1

    sha = hashlib.sha256(raw).hexdigest()
    with open(a.out, "wb") as f:
        f.write(raw)
    ts = a.ts or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = {"ts": ts, "qmirror_version": "anu_pull.py-1.0", "slot": "S1_qrng_seed_live",
           "module": "anu_pull", "tier": tier, "n_bytes": len(raw), "sha256": sha,
           "out": os.path.basename(a.out), "ok": 1, "request_id": rid,
           "qmirror_message": "ANU vacuum-fluctuation live pull (secret-keyed)"}
    with open(a.provenance, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps({"ok": 1, "tier": tier, "n_bytes": len(raw), "sha256": sha,
                      "request_id": rid, "out": a.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
