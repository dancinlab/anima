"""H_1053 — pre-fetch TRUE quantum random bytes from the ANU Quantum Numbers API and CACHE
them to a committed file, so the H_1053 run is reproducible from the SAME physical draw and
re-runs do not re-hit the rate-limited API.

Endpoint: https://api.quantumnumbers.anu.edu.au/ (header x-api-key). type=hex16, size=10 packs
20480 bytes/call. The key is read INLINE from the macOS keychain via `secret get` (never printed).

Writes:
  UNIVERSE/state/h1053_qrng_bytes.bin       — the raw true-quantum byte stream
  UNIVERSE/state/h1053_qrng_bytes.prov.json — provenance (endpoint, UTC ts, bytes, key class, sha256)

NO PRNG anywhere. If the API is unreachable / no key -> the script HALTS with the exact blocker
(it does NOT fabricate bytes).
"""
import sys, os, json, time, hashlib, subprocess, datetime
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "state")
os.makedirs(STATE, exist_ok=True)
BIN = os.path.join(STATE, "h1053_qrng_bytes.bin")
PROV = os.path.join(STATE, "h1053_qrng_bytes.prov.json")

ENDPOINT = "https://api.quantumnumbers.anu.edu.au/"
TARGET_BYTES = int(os.environ.get("H1053_TARGET_BYTES", str(3_000_000)))  # >= 2.69MB budget
PER_CALL = 20480  # length=1024, type=hex16, size=10 -> 1024*10 bytes


def get_key():
    """Return (key, key_class). Tries paid then free keychain entries; never prints the value."""
    for name, cls in (("flat.anu_key_paid", "paid"), ("flat.anu_key_free", "free")):
        try:
            k = subprocess.check_output(["secret", "get", name], stderr=subprocess.DEVNULL).decode().strip()
            if k:
                return k, cls
        except Exception:
            continue
    return None, None


def fetch_block(key):
    url = f"{ENDPOINT}?length=1024&type=hex16&size=10"
    req = urllib.request.Request(url, headers={"x-api-key": key})
    with urllib.request.urlopen(req, timeout=30) as resp:
        j = json.loads(resp.read().decode())
    if not j.get("success"):
        raise RuntimeError(f"ANU API returned success=false: {j.get('message','?')}")
    data = j["data"]  # list of hex strings, 20 hex chars (10 bytes) each
    return b"".join(bytes.fromhex(h) for h in data)


def main():
    key, key_class = get_key()
    if not key:
        print("HALT — no ANU API key in keychain (tried flat.anu_key_paid, flat.anu_key_free).")
        print("  H_1053 needs an ANU QRNG key (no silent PRNG fallback). Blocker reported.")
        raise SystemExit(2)

    ts_start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"H_1053 QRNG fetch — endpoint={ENDPOINT}  key_class={key_class}  target>={TARGET_BYTES} bytes")
    buf = bytearray()
    calls = 0
    backoff = 2.0
    t0 = time.time()
    while len(buf) < TARGET_BYTES:
        try:
            blk = fetch_block(key)
            buf.extend(blk)
            calls += 1
            backoff = 2.0
            if calls % 10 == 0 or len(buf) >= TARGET_BYTES:
                print(f"  call {calls}: {len(buf):,}/{TARGET_BYTES:,} bytes  ({time.time()-t0:.1f}s)", flush=True)
            time.sleep(0.6)  # be polite to the rate limiter
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            print(f"  transient error (call {calls+1}): {e}; backoff {backoff:.1f}s", flush=True)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60.0)
            if backoff >= 60.0 and len(buf) == 0:
                print("HALT — ANU API unreachable and no bytes fetched. Blocker:", e)
                raise SystemExit(3)
    ts_end = datetime.datetime.now(datetime.timezone.utc).isoformat()

    raw = bytes(buf[:TARGET_BYTES])
    with open(BIN, "wb") as f:
        f.write(raw)
    sha = hashlib.sha256(raw).hexdigest()
    prov = dict(endpoint=ENDPOINT, type="hex16", size=10, length_per_call=1024,
                bytes_per_call=PER_CALL, total_bytes=len(raw), api_calls=calls,
                key_class=key_class, ts_start_utc=ts_start, ts_end_utc=ts_end,
                sha256=sha, source="ANU Quantum Numbers (vacuum-fluctuation QRNG)",
                note="TRUE physical quantum random bytes; NO PRNG. Cached for reproducibility.")
    with open(PROV, "w") as f:
        json.dump(prov, f, indent=2)
    print(f"WROTE {len(raw):,} bytes -> {BIN}")
    print(f"  sha256={sha}")
    print(f"  provenance -> {PROV}")


if __name__ == "__main__":
    main()
