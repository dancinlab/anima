#!/usr/bin/env python3
"""qmirror cond.4 - clean NIST SP 800-22 tier-1+ reference implementation.

Replaces the prior nistrng-based runner which had three bugs at n=10^6:
  1. tier-1+ verdict logic mismatched test names (lowercase keys vs
     "Monobit"/"Frequency Within Block" results) -> all marked INELIGIBLE
  2. nistrng test_cumulative_sums.py uses Python int but accumulates
     numpy int8 -> overflow -> always returns score=1.0 (false PASS)
  3. nistrng test_approximate_entropy.py has 'min(2, max(3, ...))' bug
     and 'log(c_i/10.0)' typo -> always returns score=0.0 (false FAIL)

This script implements the 7 tier-1+ tests directly from
NIST SP 800-22 Rev.1a (April 2010), sections 2.1, 2.2, 2.3, 2.4, 2.6,
2.11, 2.12 (NIST_TIER1_PLUS = monobit, block_frequency, runs,
longest_run, dft, cumulative_sums, approximate_entropy).

Streams (each 125_000 bytes = 1_000_000 bits):
  - hmac_drbg_legacy : HMAC-DRBG SHA-256 seeded by IonQ Forte 1
                       4096-bit |+>^16 measurement (NIST SP 800-90A)
  - qmirror_mock_lcg : Park-Miller LCG seed=12345 (control / fixture)
  - anu_legacy_live  : ANU qrng.anu.edu.au/API/jsonI.php uint16 stream
                       (legacy unauthenticated endpoint, T1.b)

Falsifier F-QM-NIST-TIER1-1: a stream PASSES cond.4 iff
  >= 6/7 tier-1+ tests have p_value >= 0.01.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.special import erfc, gammaincc
from scipy.fft import fft

REPO = Path("/Users/ghost/core/anima")
OUT = REPO / "state" / "nexus_qmirror_nist_2026_05_03"
OUT.mkdir(parents=True, exist_ok=True)
HMAC_REF = REPO / "state" / "nexus_qrng_quantum_seed_2026_05_02" / "hmac_drbg_seed.json"
QMEAS = REPO / "state" / "nexus_qrng_quantum_seed_2026_05_02" / "quantum_measurement_raw.json"

N_BYTES = 125_000      # = 1_000_000 bits
ALPHA = 0.01
TIER1_PLUS = [
    "monobit",
    "block_frequency",
    "runs",
    "longest_run",
    "dft",
    "cumulative_sums",
    "approximate_entropy",
]
THRESHOLD = 6


# =========================================================================
# Sample generators
# =========================================================================
class HmacDrbgSha256:
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


def hmac_drbg_legacy(n_bytes: int) -> tuple[bytes, dict]:
    meta = json.loads(HMAC_REF.read_text())
    raw = json.loads(QMEAS.read_text())
    entropy = bytes.fromhex(raw["raw_bits_4096_hex"])
    nonce = meta["nonce"].encode()
    pers = meta["personalization_string"].encode()
    drbg = HmacDrbgSha256(entropy, nonce, pers)
    out = drbg.generate(n_bytes)
    expected = bytes.fromhex(meta["first_output_1024_bytes_hex"])
    assert out[:1024] == expected, "HMAC-DRBG re-derivation MISMATCH"
    return out, {
        "algorithm": meta["algorithm"],
        "entropy_input_bits": meta["entropy_input_bits"],
        "entropy_input_source": meta["entropy_input_source"],
        "personalization_string": meta["personalization_string"],
        "first_1024_sha256_verified": True,
    }


def qmirror_mock_lcg(n_bytes: int, seed: int = 12345) -> bytes:
    s = seed if seed > 0 else 12345
    out = bytearray(n_bytes)
    a, c, m = 1664525, 1013904223, 4294967296
    for i in range(n_bytes):
        s = (a * s + c) % m
        out[i] = s % 256
    return bytes(out)


# =========================================================================
# NIST SP 800-22 Rev.1a tier-1+ reference implementations
# (verified against the example computations in the spec where present)
# =========================================================================
def t_monobit(bits: np.ndarray) -> float:
    """SP 800-22 Rev.1a §2.1 Frequency (Monobit) test."""
    n = bits.size
    s = int(np.sum(bits == 1) - np.sum(bits == 0))
    s_obs = abs(s) / math.sqrt(n)
    return math.erfc(s_obs / math.sqrt(2))


def t_block_frequency(bits: np.ndarray, M: int = 128) -> float:
    """SP 800-22 Rev.1a §2.2 Frequency Within a Block.
    M=128 per spec recommendation."""
    n = bits.size
    N = n // M
    if N == 0:
        return 0.0
    chi2 = 0.0
    for i in range(N):
        block = bits[i * M:(i + 1) * M]
        pi_i = float(np.sum(block)) / M
        chi2 += (pi_i - 0.5) ** 2
    chi2 *= 4.0 * M
    return gammaincc(N / 2.0, chi2 / 2.0)


def t_runs(bits: np.ndarray) -> float:
    """SP 800-22 Rev.1a §2.3 Runs test."""
    n = bits.size
    pi = float(np.sum(bits)) / n
    if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
        # Pre-test fails -> p_value = 0 by spec
        return 0.0
    # V_n(obs) = number of positions where adjacent bits differ + 1
    diffs = int(np.sum(bits[:-1] != bits[1:]))
    Vn = diffs + 1
    num = abs(Vn - 2.0 * n * pi * (1.0 - pi))
    den = 2.0 * math.sqrt(2.0 * n) * pi * (1.0 - pi)
    return math.erfc(num / den)


# Longest-run-of-ones — table per SP 800-22 Rev.1a §2.4 (n>=750000 uses M=10000, K=6)
_LR_TABLE = {
    # M, K, N, V_thresholds (length), pi[K+1]
    8:    (8,    3, 16,    [1, 2, 3, 4],          [0.2148, 0.3672, 0.2305, 0.1875]),
    128:  (128,  5, 49,    [4, 5, 6, 7, 8, 9],
            [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]),
    10000:(10000,6, 75,    [10, 11, 12, 13, 14, 15, 16],
            [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]),
}


def t_longest_run(bits: np.ndarray) -> float:
    """SP 800-22 Rev.1a §2.4 Longest Run of Ones in a Block."""
    n = bits.size
    if n < 6272:
        M = 8
    elif n < 750_000:
        M = 128
    else:
        M = 10000
    M, K, N_target, v_lens, pi = _LR_TABLE[M]
    N = n // M
    if N == 0:
        return 0.0
    nu = [0] * (K + 1)
    for i in range(N):
        block = bits[i * M:(i + 1) * M]
        # find longest run of ones
        longest = 0
        cur = 0
        for b in block:
            if b == 1:
                cur += 1
                if cur > longest:
                    longest = cur
            else:
                cur = 0
        # bucket
        if longest <= v_lens[0]:
            nu[0] += 1
        elif longest >= v_lens[-1]:
            nu[K] += 1
        else:
            nu[longest - v_lens[0]] += 1
    chi2 = 0.0
    for i in range(K + 1):
        expected = N * pi[i]
        chi2 += (nu[i] - expected) ** 2 / expected
    return gammaincc(K / 2.0, chi2 / 2.0)


def t_dft(bits: np.ndarray) -> float:
    """SP 800-22 Rev.1a §2.6 Discrete Fourier Transform (Spectral) test."""
    n = bits.size
    X = 2.0 * bits.astype(np.float64) - 1.0  # 0,1 -> -1,+1
    S = fft(X)
    # modulus of first n/2
    M = np.abs(S[: n // 2])
    T = math.sqrt(math.log(1.0 / 0.05) * n)
    N0 = 0.95 * n / 2.0
    N1 = float(np.sum(M < T))
    d = (N1 - N0) / math.sqrt(n * 0.95 * 0.05 / 4.0)
    return math.erfc(abs(d) / math.sqrt(2))


def t_cumulative_sums(bits: np.ndarray) -> float:
    """SP 800-22 Rev.1a §2.13 Cumulative Sums (Cusum) test.
    Returns min of forward/backward p-values (conservative for tier-1+)."""
    n = bits.size
    X = 2 * bits.astype(np.int64) - 1  # int64: NO OVERFLOW (was the bug)
    fwd = np.cumsum(X)
    bwd = np.cumsum(X[::-1])
    z_fwd = int(np.max(np.abs(fwd)))
    z_bwd = int(np.max(np.abs(bwd)))
    p_vals = []
    for z in (z_fwd, z_bwd):
        # Sum 1: k from floor((-n/z+1)/4) to floor((n/z-1)/4)
        if z == 0:
            p_vals.append(1.0)
            continue
        sum1 = 0.0
        k_lo = int(math.floor(((-n / z) + 1.0) / 4.0))
        k_hi = int(math.floor(((n / z) - 1.0) / 4.0))
        sqrt_n = math.sqrt(n)
        for k in range(k_lo, k_hi + 1):
            a = ((4.0 * k + 1.0) * z) / sqrt_n
            b = ((4.0 * k - 1.0) * z) / sqrt_n
            # 1/2 erfc(-x/sqrt2) - 1/2 erfc(-y/sqrt2)
            from scipy.stats import norm
            sum1 += norm.cdf(a) - norm.cdf(b)
        # Sum 2: k from floor((-n/z-3)/4) to floor((n/z-1)/4)
        sum2 = 0.0
        k_lo = int(math.floor(((-n / z) - 3.0) / 4.0))
        k_hi = int(math.floor(((n / z) - 1.0) / 4.0))
        for k in range(k_lo, k_hi + 1):
            a = ((4.0 * k + 3.0) * z) / sqrt_n
            b = ((4.0 * k + 1.0) * z) / sqrt_n
            from scipy.stats import norm
            sum2 += norm.cdf(a) - norm.cdf(b)
        p = 1.0 - sum1 + sum2
        p_vals.append(max(0.0, min(1.0, p)))
    return min(p_vals)


def t_approximate_entropy(bits: np.ndarray, m: int = 10) -> float:
    """SP 800-22 Rev.1a §2.12 Approximate Entropy.
    Default m=10 per spec for n=10^6. Uses correct log(c_i) (NOT log(c_i/10))."""
    n = bits.size

    def phi(m: int) -> float:
        # Append first m-1 bits (wrap)
        seq = np.concatenate([bits, bits[: m - 1]])
        # Count m-bit patterns by bit-packing into ints
        counts = np.zeros(1 << m, dtype=np.int64)
        # Vectorised sliding window via bit-packing
        pat = 0
        # initial window
        for i in range(m):
            pat = (pat << 1) | int(seq[i])
        counts[pat] += 1
        mask = (1 << m) - 1
        for i in range(1, n):  # there are exactly n m-bit windows over the wrapped sequence
            pat = ((pat << 1) | int(seq[i + m - 1])) & mask
            counts[pat] += 1
        # C_i^m = counts / n
        c = counts.astype(np.float64) / n
        # phi^m = sum c_i * log(c_i) (over c_i > 0)
        nz = c[c > 0.0]
        return float(np.sum(nz * np.log(nz)))

    phi_m = phi(m)
    phi_m1 = phi(m + 1)
    ap_en = phi_m - phi_m1
    chi2 = 2.0 * n * (math.log(2) - ap_en)
    return float(gammaincc(2 ** (m - 1), chi2 / 2.0))


# =========================================================================
# Driver
# =========================================================================
def run_battery(name: str, raw: bytes, log) -> dict:
    arr = np.frombuffer(raw, dtype=np.uint8)
    bits = np.unpackbits(arr).astype(np.int8)
    n_bits = int(bits.size)
    log(f"\n--- {name} ---  n_bits={n_bits}")
    out = {"name": name, "n_bytes": len(raw), "n_bits": n_bits, "tests": {}}
    funcs = [
        ("monobit",            lambda: t_monobit(bits)),
        ("block_frequency",    lambda: t_block_frequency(bits, M=128)),
        ("runs",               lambda: t_runs(bits)),
        ("longest_run",        lambda: t_longest_run(bits)),
        ("dft",                lambda: t_dft(bits)),
        ("cumulative_sums",    lambda: t_cumulative_sums(bits)),
        ("approximate_entropy",lambda: t_approximate_entropy(bits, m=10)),
    ]
    n_pass = 0
    for tname, fn in funcs:
        t0 = time.monotonic()
        try:
            p = float(fn())
            elapsed = time.monotonic() - t0
            passed = bool(p >= ALPHA)
            n_pass += int(passed)
            out["tests"][tname] = {
                "p_value": p,
                "passed": passed,
                "elapsed_sec": round(elapsed, 2),
            }
            log(f"  {tname:24s} p={p:.6f} {'PASS' if passed else 'FAIL':4s} ({elapsed:.1f}s)")
        except Exception as e:
            elapsed = time.monotonic() - t0
            out["tests"][tname] = {
                "p_value": None,
                "passed": False,
                "error": repr(e),
                "elapsed_sec": round(elapsed, 2),
            }
            log(f"  {tname:24s} ERROR {e!r} ({elapsed:.1f}s)")
    out["pass_count"] = n_pass
    out["test_count"] = len(funcs)
    out["verdict"] = "PASS" if n_pass >= THRESHOLD else "FAIL"
    log(f"  -> {out['verdict']} ({n_pass}/{len(funcs)})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anu-bytes", type=str, default="",
                    help="optional path to ANU live byte file (e.g. /tmp/anu_pull_progress.bin)")
    ap.add_argument("--include-mock", action="store_true",
                    help="also test the deterministic LCG mock (control)")
    args = ap.parse_args()

    log_path = OUT / "tier1plus_clean.log"
    log_f = log_path.open("w")
    def log(msg):
        print(msg, flush=True)
        log_f.write(msg + "\n")
        log_f.flush()

    log("=" * 72)
    log("qmirror cond.4 NIST SP 800-22 tier-1+ (clean reference impl)")
    log(f"  N={N_BYTES} bytes ({N_BYTES * 8} bits)  alpha={ALPHA}  threshold={THRESHOLD}/7")
    log("=" * 72)

    samples: list[tuple[str, bytes, dict]] = []

    # HMAC-DRBG legacy (always available)
    log("\n[gen] HMAC-DRBG legacy (IonQ Forte 1 4096-bit quantum seed) ...")
    drbg, drbg_meta = hmac_drbg_legacy(N_BYTES)
    drbg_sha = hashlib.sha256(drbg).hexdigest()
    log(f"  n={len(drbg)} sha256={drbg_sha[:16]}...")
    (OUT / "sample_1mbit_hmac_drbg.bin").write_bytes(drbg)
    samples.append(("hmac_drbg_legacy", drbg, {**drbg_meta,
                                                "n_bytes": len(drbg),
                                                "sha256": drbg_sha,
                                                "anu_tier": "T1.a-fallback (HMAC-DRBG seeded by IonQ quantum bits)"}))

    # ANU live (if provided)
    anu_meta = None
    if args.anu_bytes and Path(args.anu_bytes).exists():
        anu_raw = Path(args.anu_bytes).read_bytes()
        if len(anu_raw) >= N_BYTES:
            anu = anu_raw[:N_BYTES]
            anu_sha = hashlib.sha256(anu).hexdigest()
            log(f"\n[gen] ANU legacy live (qrng.anu.edu.au) using {args.anu_bytes}")
            log(f"  n={len(anu)} sha256={anu_sha[:16]}...")
            (OUT / "sample_1mbit_anu_legacy.bin").write_bytes(anu)
            anu_meta = {
                "source": "ANU Quantum Numbers legacy REST API "
                          "(qrng.anu.edu.au/API/jsonI.php?length=1024&type=uint16)",
                "anu_tier": "T1.b (legacy unauthenticated endpoint, "
                            "deprecated but operational; vacuum-fluctuation QRNG)",
                "n_bytes": len(anu),
                "sha256": anu_sha,
                "fetched_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            samples.append(("anu_legacy_live", anu, anu_meta))
        else:
            log(f"\n[gen] ANU partial only ({len(anu_raw)}/{N_BYTES} bytes), "
                "running test on PARTIAL sample as best-effort")
            anu_sha = hashlib.sha256(anu_raw).hexdigest()
            (OUT / "sample_partial_anu_legacy.bin").write_bytes(anu_raw)
            anu_meta = {
                "source": "ANU Quantum Numbers legacy REST API "
                          "(qrng.anu.edu.au/API/jsonI.php?length=1024&type=uint16)",
                "anu_tier": "T1.b (legacy endpoint, PARTIAL pull only)",
                "n_bytes": len(anu_raw),
                "n_bits": len(anu_raw) * 8,
                "sha256": anu_sha,
                "partial": True,
                "fetched_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            samples.append(("anu_legacy_partial", anu_raw, anu_meta))
    else:
        log("\n[gen] ANU live SKIPPED (no anu_bytes provided / file missing)")

    # MOCK LCG (control)
    if args.include_mock:
        log("\n[gen] MOCK qmirror LCG (control, expected to FAIL) ...")
        mock = qmirror_mock_lcg(N_BYTES, seed=12345)
        mock_sha = hashlib.sha256(mock).hexdigest()
        log(f"  n={len(mock)} sha256={mock_sha[:16]}...")
        (OUT / "sample_1mbit_mock.bin").write_bytes(mock)
        samples.append(("qmirror_mock_lcg", mock, {
            "source": "Park-Miller LCG seed=12345",
            "anu_tier": "T0",
            "n_bytes": len(mock),
            "sha256": mock_sha,
        }))

    # Run battery
    log("\n" + "=" * 72)
    log("Running 7 tier-1+ tests on each stream")
    log("=" * 72)
    test_results = {}
    provenance = {}
    for name, raw, prov in samples:
        provenance[name] = prov
        test_results[name] = run_battery(name, raw, log)

    # Compose verdict
    prod_streams = [s for s in test_results
                    if s in ("anu_legacy_live", "hmac_drbg_legacy")]
    prod_passing = [s for s in prod_streams
                    if test_results[s]["verdict"] == "PASS"]

    if "anu_legacy_live" in test_results:
        anu_tier_used = "T1.b (legacy ANU endpoint, full 10^6 bit pull)"
    elif "anu_legacy_partial" in test_results:
        anu_tier_used = "T1.b (legacy ANU endpoint, PARTIAL pull)"
    else:
        anu_tier_used = "T1.a-fallback (HMAC-DRBG seeded by IonQ Forte 1; ANU unavailable)"

    cond4_verdict = "PASS" if prod_passing else "FAIL"

    out_doc = {
        "test": "qmirror_cond4_nist_tier1plus_clean",
        "date": "2026-05-03",
        "alpha": ALPHA,
        "n_bytes_per_stream": N_BYTES,
        "n_bits_per_stream": N_BYTES * 8,
        "battery": "NIST SP 800-22 Rev.1a §2.{1,2,3,4,6,11,12} (clean reference impl)",
        "tier1_plus_tests": TIER1_PLUS,
        "threshold": THRESHOLD,
        "streams": list(test_results.keys()),
        "provenance": provenance,
        "test_results": test_results,
        "production_streams_evaluated": prod_streams,
        "production_streams_passing": prod_passing,
        "anu_tier_used": anu_tier_used,
        "cond4_verdict": cond4_verdict,
        "honest_caveats_c3": [
            ("ANU pull tier: " + anu_tier_used + ". The legacy "
             "qrng.anu.edu.au/API/jsonI.php endpoint is deprecated by ANU "
             "(rate-limited to ~1 request/min, no API attestation, no SLA). "
             "It remains a real vacuum-fluctuation quantum source but does NOT "
             "constitute a hardened production T1 stream. The new T1.a "
             "api.quantumnumbers.anu.edu.au endpoint requires NEXUS_QMIRROR_ANU_KEY "
             "which is not present in this environment."),
            ("Sample size: 1,000,000 bits per stream is the NIST SP 800-22 "
             "MINIMUM (sometimes called 'tier-1+ minimum'); production "
             "certification typically requires N=10^9 bits (1 Gbit) and m "
             "independent sequences for the second-tier proportion-of-passing "
             "metric. A single-sequence p-value PASS at n=10^6 is necessary "
             "but not sufficient evidence of cryptographic-grade entropy."),
            ("Test selection rationale: this run covers ONLY the 7 tier-1+ "
             "tests (monobit, block_frequency, runs, longest_run, dft, "
             "cumulative_sums, approximate_entropy) per the cond.4 falsifier "
             "F-QM-NIST-TIER1-1. The remaining 8 SP 800-22 tests "
             "(binary_matrix_rank, non_overlapping_template, overlapping_template, "
             "maurers_universal, linear_complexity, serial, random_excursion, "
             "random_excursion_variant) are NOT included; tier-2+/full-battery "
             "PASS is a separate condition not adjudicated here. "
             "Note also: the prior nistrng-package run reported approximate_entropy "
             "p=0.0 and cumulative_sums p=1.0 due to two reproducible bugs in the "
             "library at n=10^6 (int8 cumsum overflow; min(2,max(3,…)) inversion + "
             "log(c_i/10.0) typo); this implementation is a direct rewrite from "
             "the spec equations to remove both."),
        ],
    }

    (OUT / "results_tier1plus.json").write_text(json.dumps(out_doc, indent=2))

    verdict_doc = {
        "test": "qmirror_cond4_nist_tier1plus",
        "falsifier": "F-QM-NIST-TIER1-1",
        "rule": ">=6/7 tier-1+ tests with p_value >= 0.01 on a production stream",
        "alpha": ALPHA,
        "threshold": THRESHOLD,
        "n_bits": N_BYTES * 8,
        "tier1_plus_tests": TIER1_PLUS,
        "anu_tier_used": anu_tier_used,
        "stream_pass_counts": {s: f"{r['pass_count']}/{r['test_count']}"
                                for s, r in test_results.items()},
        "stream_verdicts": {s: r["verdict"] for s, r in test_results.items()},
        "production_streams_evaluated": prod_streams,
        "production_streams_passing": prod_passing,
        "cond4_verdict": cond4_verdict,
        "cond4_reason": (
            f"{len(prod_passing)}/{len(prod_streams)} production streams "
            f"meet F-QM-NIST-TIER1-1 (>={THRESHOLD}/7 tier-1+ PASS at p>={ALPHA})"
        ),
    }
    (OUT / "verdict.json").write_text(json.dumps(verdict_doc, indent=2))

    log("\n" + "=" * 72)
    log("SUMMARY")
    log("=" * 72)
    for s, r in test_results.items():
        log(f"  {s:24s} {r['verdict']:4s} {r['pass_count']}/{r['test_count']}")
    log(f"\nANU tier used        : {anu_tier_used}")
    log(f"production streams   : {prod_streams}")
    log(f"  passing            : {prod_passing}")
    log(f"cond.4 verdict       : {cond4_verdict}")
    log(f"\nresults: {OUT/'results_tier1plus.json'}")
    log(f"verdict: {OUT/'verdict.json'}")
    log_f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
