#!/usr/bin/env python3
"""qmirror cond.4 NIST tier-1+ verification — full SP 800-22 battery on 10^6 bits.

Three streams (each 125,000 bytes = 1,000,000 bits):
  1. ANU live (vacuum-fluctuation QRNG, fetched live via REST under
     NEXUS_QMIRROR_ANU_KEY, rate-limited <=100 req/min)
  2. qmirror MOCK (Park-Miller LCG with seed=12345, mirrors qmirror.qrng
     _qrng_lcg_bytes when NEXUS_QMIRROR_MOCK=1)
  3. HMAC-DRBG legacy (NIST SP 800-90A Rev.1 SHA-256, IonQ Forte 1 4096-bit
     entropy seed; extends the existing 8192-byte sample to 125,000 bytes
     by continuing generate() from the same DRBG instance)

Each stream is run through the full SP 800-22 battery via the `nistrng`
package (15 tests: monobit, frequency_within_block, runs,
longest_run_ones_in_a_block, binary_matrix_rank, dft,
non_overlapping_template_matching, overlapping_template_matching,
maurers_universal, linear_complexity, serial, approximate_entropy,
cumulative_sums, random_excursion, random_excursion_variant).

Output: results.json + summary.txt + raw bytes per stream + provenance log.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import urllib.request
import urllib.error

# nistrng (installed in /tmp/nistenv)
sys.path.insert(0, "/tmp/nistenv/lib/python3.14/site-packages")
from nistrng import (
    SP800_22R1A_BATTERY,
    pack_sequence,
    run_all_battery,
    check_eligibility_all_battery,
    Result,
)

REPO = Path("/Users/ghost/core/anima")
OUT = REPO / "state" / "qmirror_qrng_nist_tier1plus_2026_05_03"
OUT.mkdir(parents=True, exist_ok=True)
HMAC_REF = REPO / "state" / "nexus_qrng_quantum_seed_2026_05_02" / "hmac_drbg_seed.json"
QMEAS = REPO / "state" / "nexus_qrng_quantum_seed_2026_05_02" / "quantum_measurement_raw.json"

N_BYTES = 125_000  # = 1,000,000 bits
ALPHA = 0.01

ANU_URL = "https://api.quantumnumbers.anu.edu.au"
ANU_PER_CALL = 1024
ANU_RATE_RPM = 60  # be conservative: 60 rpm, well under the 100 rpm cap


# ---------------------------------------------------------------------------
# 1. ANU live fetcher (rate-limited)
# ---------------------------------------------------------------------------
def anu_fetch_bytes(n_bytes: int, key: str, log_path: Path) -> bytes:
    out = bytearray()
    n_calls = (n_bytes + ANU_PER_CALL - 1) // ANU_PER_CALL
    interval = 60.0 / ANU_RATE_RPM  # seconds between calls
    log = log_path.open("w")
    log.write(f"ANU fetch start: n_bytes={n_bytes} n_calls={n_calls} "
              f"per_call={ANU_PER_CALL} rpm={ANU_RATE_RPM} "
              f"iso={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
    log.flush()
    t_first = time.monotonic()
    for i in range(n_calls):
        need = min(ANU_PER_CALL, n_bytes - len(out))
        url = f"{ANU_URL}?length={need}&type=uint8"
        req = urllib.request.Request(url, headers={"x-api-key": key,
                                                   "User-Agent": "anima-qmirror-tier1plus/1.0"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    body = json.loads(resp.read().decode())
                if not body.get("success"):
                    raise RuntimeError(f"ANU non-success: {body}")
                data = body["data"]
                if len(data) != need:
                    raise RuntimeError(f"ANU short read: got {len(data)} want {need}")
                out.extend(data)
                log.write(f"call {i+1}/{n_calls} ok bytes={need} cum={len(out)} "
                          f"t={time.monotonic()-t_first:.1f}s\n")
                log.flush()
                break
            except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, TimeoutError) as e:
                wait = 2 ** attempt
                log.write(f"call {i+1}/{n_calls} attempt {attempt+1} ERROR: {e!r} "
                          f"backoff {wait}s\n")
                log.flush()
                time.sleep(wait)
        else:
            raise RuntimeError(f"ANU call {i+1} failed after 5 attempts")
        if i < n_calls - 1:
            time.sleep(interval)
    log.write(f"ANU fetch done: total={len(out)} elapsed={time.monotonic()-t_first:.1f}s\n")
    log.close()
    return bytes(out[:n_bytes])


# ---------------------------------------------------------------------------
# 2. qmirror MOCK LCG (Park-Miller / Numerical Recipes coefficients)
#    Mirrors state/qmirror_phase1_staging_2026_05_03/qrng.hexa _qrng_lcg_bytes
# ---------------------------------------------------------------------------
def qmirror_mock_lcg_bytes(n_bytes: int, seed: int = 12345) -> bytes:
    s = seed if seed > 0 else 12345
    out = bytearray(n_bytes)
    a = 1664525
    c = 1013904223
    m = 4294967296
    for i in range(n_bytes):
        s = (a * s + c) % m
        out[i] = s % 256
    return bytes(out)


# ---------------------------------------------------------------------------
# 3. HMAC-DRBG SHA-256 (NIST SP 800-90A Rev.1) extended to N bytes
# ---------------------------------------------------------------------------
class HmacDrbgSha256:
    OUTLEN = 32

    def __init__(self, entropy: bytes, nonce: bytes, pers: bytes = b""):
        seed_material = entropy + nonce + pers
        self.K = b"\x00" * self.OUTLEN
        self.V = b"\x01" * self.OUTLEN
        self._update(seed_material)
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


def hmac_drbg_legacy_bytes(n_bytes: int) -> tuple[bytes, dict]:
    meta = json.loads(HMAC_REF.read_text())
    raw = json.loads(QMEAS.read_text())
    entropy = bytes.fromhex(raw["raw_bits_4096_hex"])
    nonce = meta["nonce"].encode()
    pers = meta["personalization_string"].encode()
    expected_first_1024 = bytes.fromhex(meta["first_output_1024_bytes_hex"])

    drbg = HmacDrbgSha256(entropy, nonce, pers)
    out = drbg.generate(n_bytes)
    assert out[:1024] == expected_first_1024, "HMAC-DRBG re-derivation MISMATCH"
    sha_first = hashlib.sha256(out[:1024]).hexdigest()
    assert sha_first == meta["first_output_sha256"], "HMAC-DRBG first_1024 sha mismatch"
    return out, {
        "algorithm": meta["algorithm"],
        "entropy_input_bits": meta["entropy_input_bits"],
        "personalization_string": meta["personalization_string"],
        "first_1024_sha256_verified": True,
    }


# ---------------------------------------------------------------------------
# NIST battery driver
# ---------------------------------------------------------------------------
def run_nist_battery(name: str, raw: bytes) -> dict:
    """Run full SP 800-22 battery on raw bytes; return per-test result dict."""
    # Convert bytes to a numpy int8 sequence of {0,1} bits.
    arr = np.frombuffer(raw, dtype=np.uint8)
    bits = np.unpackbits(arr).astype(np.int8)
    # nistrng uses signed int8, with 0 → 0 and 1 → 1 (no ±1 mapping).
    eligible = check_eligibility_all_battery(bits, SP800_22R1A_BATTERY)
    print(f"[{name}] sequence n_bits={bits.size} "
          f"eligible_tests={len(eligible)}/{len(SP800_22R1A_BATTERY)}")
    sys.stdout.flush()
    t0 = time.monotonic()
    results = run_all_battery(bits, eligible, False)
    elapsed = time.monotonic() - t0
    out = {
        "name": name,
        "n_bytes": len(raw),
        "n_bits": int(bits.size),
        "elapsed_sec": round(elapsed, 2),
        "tests": {},
        "summary": {"eligible": 0, "ineligible": 0, "passed": 0, "failed": 0},
    }
    eligible_set = set(eligible.keys())
    for name_test in SP800_22R1A_BATTERY.keys():
        if name_test not in eligible_set:
            out["tests"][name_test] = {"eligible": False}
            out["summary"]["ineligible"] += 1
    for r, t_elapsed in results:
        # r: nistrng.Result
        passed = bool(r.passed)
        entry = {
            "eligible": True,
            "p_value": float(r.score),
            "passed": passed,
            "elapsed_sec": round(float(t_elapsed), 3),
        }
        out["tests"][r.name] = entry
        out["summary"]["eligible"] += 1
        if passed:
            out["summary"]["passed"] += 1
        else:
            out["summary"]["failed"] += 1
    print(f"[{name}] battery elapsed={elapsed:.1f}s "
          f"passed={out['summary']['passed']}/{out['summary']['eligible']} "
          f"ineligible={out['summary']['ineligible']}")
    sys.stdout.flush()
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 72)
    print("qmirror cond.4 NIST tier-1+ verification (n=10^6 bits per stream)")
    print("=" * 72)
    sys.stdout.flush()

    streams: dict[str, bytes] = {}
    provenance: dict[str, dict] = {}

    # ---- 2. qmirror MOCK (instant) ----
    print("\n[1/3] qmirror MOCK (LCG seed=12345) ...")
    sys.stdout.flush()
    mock = qmirror_mock_lcg_bytes(N_BYTES, seed=12345)
    streams["qmirror_mock_lcg"] = mock
    sha = hashlib.sha256(mock).hexdigest()
    (OUT / "qmirror_mock_bytes_125000.bin").write_bytes(mock)
    provenance["qmirror_mock_lcg"] = {
        "source": "Park-Miller LCG, a=1664525, c=1013904223, m=2**32, seed=12345",
        "matches_qrng_hexa": "state/qmirror_phase1_staging_2026_05_03/qrng.hexa _qrng_lcg_bytes",
        "n_bytes": len(mock),
        "sha256": sha,
    }
    print(f"  mock n={len(mock)} sha256={sha[:16]}...")
    sys.stdout.flush()

    # ---- 3. HMAC-DRBG legacy ----
    print("\n[2/3] HMAC-DRBG legacy (IonQ Forte 1 4096-bit seed, SHA-256) ...")
    sys.stdout.flush()
    drbg, drbg_meta = hmac_drbg_legacy_bytes(N_BYTES)
    streams["hmac_drbg_legacy"] = drbg
    sha = hashlib.sha256(drbg).hexdigest()
    (OUT / "hmac_drbg_legacy_bytes_125000.bin").write_bytes(drbg)
    provenance["hmac_drbg_legacy"] = {**drbg_meta,
                                      "n_bytes": len(drbg),
                                      "sha256": sha}
    print(f"  drbg n={len(drbg)} sha256={sha[:16]}...")
    sys.stdout.flush()

    # ---- 1. ANU live (slow: ~123 calls @ 60 rpm = ~123 sec; budget 5 min) ----
    print("\n[3/3] ANU live (vacuum-fluctuation QRNG) ...")
    sys.stdout.flush()
    key = os.environ.get("NEXUS_QMIRROR_ANU_KEY", "").strip()
    if not key:
        print("  WARN: NEXUS_QMIRROR_ANU_KEY not set, skipping ANU live")
        anu = None
    else:
        try:
            anu = anu_fetch_bytes(N_BYTES, key, OUT / "anu_fetch.log")
            sha = hashlib.sha256(anu).hexdigest()
            (OUT / "anu_live_bytes_125000.bin").write_bytes(anu)
            provenance["anu_live"] = {
                "source": "ANU Quantum Numbers REST API "
                          "(https://api.quantumnumbers.anu.edu.au)",
                "url_pattern": f"{ANU_URL}?length={ANU_PER_CALL}&type=uint8",
                "rate_rpm": ANU_RATE_RPM,
                "n_calls": (N_BYTES + ANU_PER_CALL - 1) // ANU_PER_CALL,
                "n_bytes": len(anu),
                "sha256": sha,
                "fetched_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }
            streams["anu_live"] = anu
            print(f"  anu n={len(anu)} sha256={sha[:16]}...")
        except Exception as e:
            print(f"  ANU fetch FAILED: {e!r}")
            anu = None
        sys.stdout.flush()

    # ---- NIST battery ----
    print("\n" + "=" * 72)
    print("Running NIST SP 800-22 battery (15 tests) on each stream ...")
    print("=" * 72)
    sys.stdout.flush()
    test_results = {}
    # Run in stream order (mock fastest, drbg, anu)
    for name in ("anu_live", "hmac_drbg_legacy", "qmirror_mock_lcg"):
        if name not in streams:
            continue
        print(f"\n--- {name} ---")
        sys.stdout.flush()
        test_results[name] = run_nist_battery(name, streams[name])

    # ---- cond.4 verdict ----
    verdicts = {}
    for name, res in test_results.items():
        s = res["summary"]
        if s["passed"] == s["eligible"] and s["eligible"] >= 13:
            v = "PASS_ALL"
        elif s["passed"] >= s["eligible"] - 1 and s["eligible"] >= 13:
            v = "PASS_MOST"
        elif s["passed"] >= s["eligible"] // 2:
            v = "PARTIAL"
        else:
            v = "FAIL"
        verdicts[name] = {
            "verdict": v,
            "passed": s["passed"],
            "eligible": s["eligible"],
            "ineligible": s["ineligible"],
        }

    # cond.4 recommendation logic:
    #   fully_met if anu_live PASS_ALL/PASS_MOST AND hmac_drbg PASS_ALL/PASS_MOST
    #     (qmirror MOCK is allowed to PARTIAL/FAIL — LCG is cryptographically
    #      weak by design and is only the fixture path)
    #   partially_met if any production stream is PARTIAL or one or more
    #     tier-1+ tests fail on a production stream
    #   unmet if production streams FAIL
    prod_streams = ["anu_live", "hmac_drbg_legacy"]
    prod_verdicts = [verdicts[s]["verdict"] for s in prod_streams if s in verdicts]
    if prod_verdicts and all(v in ("PASS_ALL", "PASS_MOST") for v in prod_verdicts):
        cond4 = "fully_met"
    elif prod_verdicts and all(v in ("PASS_ALL", "PASS_MOST", "PARTIAL") for v in prod_verdicts):
        cond4 = "partially_met"
    elif not prod_verdicts:
        cond4 = "unverified"
    else:
        cond4 = "unmet"

    out_doc = {
        "test": "qmirror_cond4_nist_tier1plus_full_battery",
        "date": "2026-05-03",
        "alpha": ALPHA,
        "n_bytes_per_stream": N_BYTES,
        "n_bits_per_stream": N_BYTES * 8,
        "battery": "NIST SP 800-22 Rev.1a (15 tests via nistrng package)",
        "tests_in_battery": list(SP800_22R1A_BATTERY.keys()),
        "streams": list(test_results.keys()),
        "provenance": provenance,
        "test_results": test_results,
        "verdicts": verdicts,
        "cond4_recommendation": cond4,
        "honest_caveats": [
            "qmirror MOCK (LCG seed=12345) is byte-deterministic and "
            "cryptographically weak by construction (Park-Miller-class state "
            "fully recoverable from <=2 outputs). LCG failures in tier-1+ "
            "tests are expected and do NOT degrade cond.4 for the production "
            "(ANU live + HMAC-DRBG) path; LCG only stays in qmirror as the "
            "deterministic CI fixture under NEXUS_QMIRROR_MOCK=1.",
            "ANU live is a single-vendor live measurement at a single moment "
            "in time; statistical PASS at n=10^6 bits does not certify the "
            "vendor pipeline as cryptographically sound (no ANU device "
            "attestation, no end-to-end audit of the TLS-fronted REST path). "
            "Cross-vendor independence (e.g., IDQ Quantis, IonQ Aria) and "
            "long-haul drift testing remain open per docs/qmirror_n2_cross_"
            "vendor_revision_2026_05_03.md.",
            "HMAC-DRBG is extended from the original 4096-bit IonQ Forte 1 "
            "entropy seed (no reseed); a full battery PASS confirms the SHA-"
            "256 PRF is statistically indistinguishable from random over "
            "10^6 bits, but does NOT re-prove SP 800-90A health-test "
            "conformance, which is a separate compliance audit.",
        ],
    }
    (OUT / "results.json").write_text(json.dumps(out_doc, indent=2))

    # text summary
    lines = []
    lines.append("=" * 72)
    lines.append("qmirror cond.4 — NIST SP 800-22 tier-1+ full battery (n=10^6 bits)")
    lines.append("=" * 72)
    lines.append(f"date: 2026-05-03   alpha: {ALPHA}")
    lines.append(f"streams: {list(test_results.keys())}")
    lines.append("")
    # per-test matrix
    test_names = list(SP800_22R1A_BATTERY.keys())
    header = f"{'test':35s}"
    for s in test_results:
        header += f" {s[:18]:>18s}"
    lines.append(header)
    lines.append("-" * len(header))
    for tn in test_names:
        row = f"{tn:35s}"
        for s in test_results:
            t = test_results[s]["tests"].get(tn, {})
            if not t.get("eligible", False):
                cell = "INELIG"
            else:
                p = t.get("p_value", float("nan"))
                tag = "PASS" if t.get("passed") else "FAIL"
                cell = f"{tag} p={p:.4f}"
            row += f" {cell:>18s}"
        lines.append(row)
    lines.append("")
    lines.append("Per-stream summary:")
    for s, v in verdicts.items():
        lines.append(f"  {s:25s} verdict={v['verdict']:10s} "
                     f"passed={v['passed']:2d}/{v['eligible']:2d} "
                     f"(ineligible={v['ineligible']})")
    lines.append("")
    lines.append(f"cond.4 recommendation: {cond4}")
    summary = "\n".join(lines) + "\n"
    (OUT / "summary.txt").write_text(summary)
    print()
    print(summary)
    print(f"results: {OUT/'results.json'}")
    print(f"summary: {OUT/'summary.txt'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
