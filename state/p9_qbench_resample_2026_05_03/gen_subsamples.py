#!/usr/bin/env python3
"""F-QBENCH-1 sub-sample generator: 500 classical PRNG + 500 qmirror QRNG seeds.

Mac-side, $0. raw#9: Python helper for data prep is allowed.

Each "seed" → one 500-index sub-sample drawn without replacement from [0, N_full).
Two sources:
  A) classical_prng : torch.Generator(device='cpu').manual_seed(42 + i),
     then torch.randperm(N_full)[:500] — exactly the construction A' would have
     used had they parametrized the sub-sample seed.
  B) qmirror_qrng   : HMAC-DRBG (NIST SP 800-90A Rev.1, SHA-256) instantiated
     from the IonQ Forte 1 4096-bit quantum entropy bank
     (state/nexus_qrng_quantum_seed_2026_05_02). For each i, derive a fresh
     32-byte sub-key by personalising the DRBG with f"qbench:{i:04d}" and
     consume enough bytes to drive a Fisher–Yates partial shuffle.

This approximates the "qmirror production stream" per
state/nexus_qmirror_nist_2026_05_03/verdict.json (cond4 PASS = HMAC-DRBG seeded
by IonQ Forte 1; ANU vacuum-fluctuation source unavailable in cycle).
"""
import hashlib
import hmac
import json
import sys
import time
from pathlib import Path

import torch

REPO = Path("/Users/ghost/core/anima")
OUT_DIR = REPO / "state" / "p9_qbench_resample_2026_05_03"
QSEED_DIR = REPO / "state" / "nexus_qrng_quantum_seed_2026_05_02"

N_FULL = 10042       # hellaswag eval-docs total
N_SUB = 500          # each sub-sample size
N_SEEDS_PER_SOURCE = 500
CLASSICAL_BASE = 42  # matches A' canonical seed


# -- HMAC-DRBG (NIST SP 800-90A Rev.1, SHA-256) -------------------------------
class HmacDrbgSha256:
    """Mirrors state/qmirror_qrng_regression_2026_05_03/extend_hmac_drbg.py"""
    OUTLEN = 32

    def __init__(self, entropy: bytes, nonce: bytes, pers: bytes = b""):
        self.K = b"\x00" * self.OUTLEN
        self.V = b"\x01" * self.OUTLEN
        self._update(entropy + nonce + pers)
        self.reseed_counter = 1

    def _hmac(self, key, data):
        return hmac.new(key, data, hashlib.sha256).digest()

    def _update(self, provided_data: bytes):
        self.K = self._hmac(self.K, self.V + b"\x00" + provided_data)
        self.V = self._hmac(self.K, self.V)
        if provided_data:
            self.K = self._hmac(self.K, self.V + b"\x01" + provided_data)
            self.V = self._hmac(self.K, self.V)

    def generate(self, n_bytes: int, additional_input: bytes = b"") -> bytes:
        if additional_input:
            self._update(additional_input)
        out = b""
        while len(out) < n_bytes:
            self.V = self._hmac(self.K, self.V)
            out += self.V
        self._update(additional_input)
        self.reseed_counter += 1
        return out[:n_bytes]


def fisher_yates_partial_from_bytes(byte_stream: bytes, n_full: int, k: int) -> list[int]:
    """Draw k distinct indices from [0, n_full) using Fisher–Yates partial
    shuffle. Each step needs an unbiased uniform integer in [i, n_full) which
    we get via rejection sampling on (n_full - i)-byte chunks (more than enough
    entropy: n_full < 2^14)."""
    arr = list(range(n_full))
    pos = 0  # byte cursor

    def draw_int(lo: int, hi: int) -> int:
        """Unbiased uniform in [lo, hi). hi-lo <= 65536 here."""
        nonlocal pos
        rng = hi - lo
        # Use 4 bytes per draw (32-bit) → bias rejection with 2^32 // rng * rng
        BYTES_PER_DRAW = 4
        max_unbiased = (2 ** (8 * BYTES_PER_DRAW) // rng) * rng
        while True:
            if pos + BYTES_PER_DRAW > len(byte_stream):
                raise RuntimeError(f"byte_stream exhausted at pos={pos}, "
                                   f"need {BYTES_PER_DRAW} more for draw [{lo},{hi})")
            r = int.from_bytes(byte_stream[pos:pos + BYTES_PER_DRAW], "big")
            pos += BYTES_PER_DRAW
            if r < max_unbiased:
                return lo + (r % rng)

    for i in range(k):
        j = draw_int(i, n_full)
        arr[i], arr[j] = arr[j], arr[i]
    return arr[:k]


def gen_classical_seeds():
    """500 sub-samples driven by torch.Generator (CPU, manual_seed)."""
    out = []
    for i in range(N_SEEDS_PER_SOURCE):
        seed = CLASSICAL_BASE + i
        g = torch.Generator(device="cpu").manual_seed(seed)
        perm = torch.randperm(N_FULL, generator=g).tolist()
        idx = sorted(perm[:N_SUB])
        out.append({
            "source": "classical_prng",
            "seed": seed,
            "indices": idx,
            "sha256": hashlib.sha256(",".join(map(str, idx)).encode()).hexdigest(),
        })
    return out


def gen_qmirror_seeds():
    """500 sub-samples driven by IonQ-seeded HMAC-DRBG (qmirror production
    stream per nexus_qmirror_nist_2026_05_03 cond4 PASS verdict)."""
    meta = json.loads((QSEED_DIR / "hmac_drbg_seed.json").read_text())
    raw = json.loads((QSEED_DIR / "quantum_measurement_raw.json").read_text())
    entropy = bytes.fromhex(raw["raw_bits_4096_hex"])
    nonce = meta["nonce"].encode()
    pers_root = meta["personalization_string"].encode()

    # Fisher–Yates over [0, N_FULL) needs ≤ 4·N_SUB = 2000 bytes, but rejection
    # may double that. Budget 8 KiB per sub-sample = 4 MiB for 500 sub-samples
    # → well within HMAC-DRBG reseed interval (NIST allows 2^48 bits between
    # reseeds; we use ≪ 2^25).
    budget_bytes = 8192
    out = []
    for i in range(N_SEEDS_PER_SOURCE):
        # Per-sub-sample personalization → distinct DRBG instance per i
        pers = pers_root + f".qbench.subsample.{i:04d}".encode()
        drbg = HmacDrbgSha256(entropy, nonce, pers)
        stream = drbg.generate(budget_bytes)
        idx = sorted(fisher_yates_partial_from_bytes(stream, N_FULL, N_SUB))
        out.append({
            "source": "qmirror_qrng",
            "seed_pers": pers.decode(),
            "drbg_first_32_hex": stream[:32].hex(),
            "indices": idx,
            "sha256": hashlib.sha256(",".join(map(str, idx)).encode()).hexdigest(),
        })
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print("[1/2] generating classical_prng sub-samples …", flush=True)
    cls = gen_classical_seeds()
    print(f"      {len(cls)} sub-samples in {time.time()-t0:.1f}s", flush=True)

    t1 = time.time()
    print("[2/2] generating qmirror_qrng sub-samples …", flush=True)
    qm = gen_qmirror_seeds()
    print(f"      {len(qm)} sub-samples in {time.time()-t1:.1f}s", flush=True)

    out_path = OUT_DIR / "subsamples.jsonl"
    with out_path.open("w") as f:
        for rec in cls + qm:
            f.write(json.dumps(rec) + "\n")
    print(f"[done] wrote {out_path} ({len(cls)+len(qm)} records)", flush=True)

    # Sanity: every sub-sample is 500 distinct ints in [0, N_FULL)
    bad = 0
    for rec in cls + qm:
        idx = rec["indices"]
        if len(idx) != N_SUB or len(set(idx)) != N_SUB or min(idx) < 0 or max(idx) >= N_FULL:
            bad += 1
    print(f"[validate] {bad} malformed sub-samples (expect 0)", flush=True)
    if bad:
        sys.exit(1)

    # Write meta
    meta = {
        "schema": "anima/p9_qbench_resample/subsample_meta/1",
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n_full": N_FULL,
        "n_sub": N_SUB,
        "n_seeds_per_source": N_SEEDS_PER_SOURCE,
        "task": "hellaswag",
        "classical_base_seed": CLASSICAL_BASE,
        "qmirror_source": {
            "drbg": "HMAC-DRBG SHA-256 (NIST SP 800-90A Rev.1)",
            "entropy_input_bits": 4096,
            "entropy_input_source": "IonQ Forte 1 |+>^16 256-shot Z-basis measurement",
            "entropy_provenance": str(QSEED_DIR / "quantum_measurement_raw.json"),
            "production_stream_verdict": "state/nexus_qmirror_nist_2026_05_03/verdict.json (cond4 PASS, T1.a-fallback)",
        },
        "subsample_path": str(out_path),
    }
    (OUT_DIR / "subsample_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"[done] wrote {OUT_DIR / 'subsample_meta.json'}", flush=True)


if __name__ == "__main__":
    main()
