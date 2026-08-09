#!/usr/bin/env python3
"""
qrng_pool_fetch.py — pre-fetch a block of REAL ANU QRNG bytes into an on-disk
entropy pool for the LIVE anima engine (H_1289 R2).
==============================================================================
FLEET lane quantum-entropy r2 · slug 1289_quantum_entropy.

R1 (H_1289 R1, numpy MIRROR) proved REAL ANU QRNG is a substrate-faithful
entropy source (NIST-lite >= PRNG) that gives genuine NON-REPRODUCIBILITY
(PRNG run1==run2 byte-identical; QRNG run1!=run2). R2 wires that REAL quantum
entropy into the LIVE engine the HONEST engineering way: NOT a per-tick network
fetch (latency + a network dependency in the substrate loop = bad design), but
a PRE-FETCHED on-disk entropy pool the engine draws from.

This tool fetches a block of REAL ANU QRNG vacuum-fluctuation bytes into a small
git-ignored pool file (default state/qrng_pool.bin). The live engine
(CORE/engine_cli.hexa qrng_pool_draw / vadapt_field_step_entropic) draws from
that pool as its OPT-IN entropy source; when the pool is exhausted the engine
falls back to its existing deterministic PRNG with an HONEST pool-exhausted flag
(pseudo, clearly labeled — NOT claimed quantum).

REAL-ONLY (anima ethos a_eeg_consciousness_record / c9): REAL quantum bytes
ONLY. If the ANU API is unreachable / returns success=false / short reads, this
tool reports the failure HONESTLY and EXITS NON-ZERO — it NEVER fabricates
quantum bytes and NEVER writes PRNG bytes into the pool and calls them quantum.

CREDENTIALS (c7): the paid key is read at call time from `secret get anu_key_paid`
(or the ANU_KEY environment variable for a managed runtime), passed ONLY through
curl's standard input as the x-api-key HTTP header, NEVER placed in process arguments,
echoed, logged, or written to any file. The fetch shells out to
`curl` (the ANU API Gateway WAF currently 403s the python-urllib TLS/UA
fingerprint but serves curl cleanly — observed 2026-06-15; curl is the robust
REAL path here, NOT a fallback to fake data).

USAGE:
    python3 tool/qrng_pool_fetch.py [--bytes N] [--out PATH]

Writes a raw .bin of N REAL quantum uint8 bytes. Logs ONLY the byte count drawn
(never the key, never the bytes). Modest request budget (default 512 bytes, ANU
caps a single request at 1024; chunked above that).
"""
import os, sys, json, subprocess, argparse

ANU_ENDPOINT = "https://api.quantumnumbers.anu.edu.au"
ANU_MAX_PER_REQ = 1024          # ANU caps length per request at 1024


class QRNGError(RuntimeError):
    pass


def _curl_fetch_chunk(n, key):
    """Fetch n (<=1024) REAL quantum uint8 bytes via curl. Raise QRNGError on any
    failure. The key is passed through curl's config on stdin, never process argv.
    Returns a list[int] of length n."""
    url = f"{ANU_ENDPOINT}?length={n}&type=uint8"
    # -s silent, -S show errors, -m hard timeout; -w appends the HTTP code so we can
    # gate on it. The secret header enters through stdin to avoid `ps` exposure.
    proc = subprocess.run(
        ["curl", "-sS", "-m", "30", "-w", "\n%{http_code}",
         "--config", "-", url],
        input=f'header = "x-api-key: {key}"\n', capture_output=True, text=True,
    )
    out = proc.stdout
    if "\n" in out:
        body, _, code = out.rpartition("\n")
        code = code.strip()
    else:
        body, code = out, "000"
    if proc.returncode != 0 and code in ("000", ""):
        err = (proc.stderr or "curl transport error")[:160]
        raise QRNGError(f"curl transport failed (code={code}): {err}")
    if code != "200":
        raise QRNGError(f"ANU HTTP {code} (body redacted to be safe)")
    try:
        b = json.loads(body)
    except json.JSONDecodeError as e:
        raise QRNGError(f"ANU response not JSON: {str(e)[:80]}")
    if not b.get("success", False):
        raise QRNGError("ANU success=false (api msg redacted)")
    data = b.get("data", [])
    if len(data) != n:
        raise QRNGError(f"ANU short read {len(data)}!={n}")
    return [int(x) & 0xFF for x in data]


def fetch_real_qrng(total, key):
    """Fetch `total` REAL quantum bytes (chunked at ANU_MAX_PER_REQ). REAL-ONLY:
    raises QRNGError on ANY failure (no fabricated bytes, no PRNG fallback here)."""
    if not key:
        raise QRNGError("ANU key unavailable — store it with `secret set anu_key_paid` (c7).")
    out = []
    remaining = total
    while remaining > 0:
        chunk = min(remaining, ANU_MAX_PER_REQ)
        out.extend(_curl_fetch_chunk(chunk, key))
        remaining -= chunk
    return bytes(out)


def main():
    ap = argparse.ArgumentParser(description="Pre-fetch REAL ANU QRNG bytes into the engine entropy pool.")
    ap.add_argument("--bytes", type=int, default=512, help="number of REAL quantum bytes to fetch (default 512)")
    ap.add_argument("--out", type=str, default="state/qrng_pool.bin", help="pool output path (git-ignored)")
    args = ap.parse_args()
    if args.bytes < 1:
        print("FATAL: --bytes must be at least 1", file=sys.stderr)
        return 2

    key = os.environ.get("ANU_KEY", "").strip()
    if not key:
        try:
            key = subprocess.run(
                ["secret", "get", "anu_key_paid"], capture_output=True, text=True,
                timeout=10, check=True,
            ).stdout.strip()
        except (FileNotFoundError, subprocess.SubprocessError):
            key = ""
    if not key:
        print("FATAL: ANU key unavailable. Run: secret set anu_key_paid", file=sys.stderr)
        print("REAL-ONLY: no PRNG-as-quantum fallback in the pool. STOP.", file=sys.stderr)
        return 2

    print(f"[qrng_pool_fetch] fetching {args.bytes} REAL ANU QRNG bytes -> {args.out} (key NEVER logged, c7) ...")
    try:
        qbytes = fetch_real_qrng(args.bytes, key)
    except QRNGError as e:
        print(f"FATAL: REAL ANU QRNG fetch FAILED: {e}", file=sys.stderr)
        print("REAL-ONLY (c9): NO fabricated quantum, NO PRNG written to the pool. Pool NOT updated. STOP.", file=sys.stderr)
        return 3

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    pool_tmp = args.out + f".tmp.{os.getpid()}"
    manifest_path = args.out + ".manifest.json"
    manifest_tmp = manifest_path + f".tmp.{os.getpid()}"
    # Provenance manifest (NO bytes, NO key).
    manifest = {
        "source": "ANU QRNG (api.quantumnumbers.anu.edu.au, vacuum-fluctuation uint8)",
        "real": True, "bytes": len(qbytes), "pool": args.out,
        "note": "REAL quantum entropy pool for CORE/engine_cli.hexa qrng_pool_draw (H_1289 R2). Key NEVER stored (c7).",
    }
    try:
        with open(pool_tmp, "wb") as f:
            f.write(qbytes)
            f.flush()
            os.fsync(f.fileno())
        with open(manifest_tmp, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(pool_tmp, args.out)
        os.replace(manifest_tmp, manifest_path)
    finally:
        for tmp in (pool_tmp, manifest_tmp):
            if os.path.exists(tmp):
                os.unlink(tmp)
    print(f"[qrng_pool_fetch] OK — wrote {len(qbytes)} REAL quantum bytes to {args.out} (success=true).")
    print(f"[qrng_pool_fetch] manifest -> {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
