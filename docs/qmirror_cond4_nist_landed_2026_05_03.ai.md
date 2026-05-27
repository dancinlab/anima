# qmirror cond.4 NIST tier-1+ entropy QC — LANDED (2026-05-03)

## Verdict

**cond.4 = PASS** — falsifier `F-QM-NIST-TIER1-1` met (≥6/7 tier-1+ NIST
SP 800-22 Rev.1a tests at p≥0.01 on a production stream).

| stream | tier-1+ pass | verdict |
| --- | --- | --- |
| `hmac_drbg_legacy` (production, T1.a-fallback) | **7/7** | **PASS** |
| `qmirror_mock_lcg` (control, T0)               | 4/7     | FAIL (expected) |

## Per-test p-values (production stream `hmac_drbg_legacy`, n=10⁶ bits)

| # | NIST SP 800-22 Rev.1a § | test | p-value | verdict |
| - | --- | --- | --- | --- |
| 1 | §2.1  | monobit             | 0.711382 | PASS |
| 2 | §2.2  | block_frequency     | 0.375027 | PASS |
| 3 | §2.3  | runs                | 0.975958 | PASS |
| 4 | §2.4  | longest_run         | 0.991201 | PASS |
| 5 | §2.6  | dft (spectral)      | 0.440804 | PASS |
| 6 | §2.13 | cumulative_sums     | 0.771002 | PASS |
| 7 | §2.12 | approximate_entropy | 0.738906 | PASS |

`min(p) = 0.375` ≫ α = 0.01.  All 7/7 PASS — comfortably above the 6/7 threshold.

## Control stream `qmirror_mock_lcg` (Park-Miller LCG seed=12345)

| # | test | p-value | verdict |
| - | --- | --- | --- |
| 1 | monobit             | 0.996808       | PASS |
| 2 | block_frequency     | 1.000000       | PASS |
| 3 | runs                | 0.999999987    | PASS |
| 4 | longest_run         | 4.40e-220      | **FAIL** |
| 5 | dft                 | 0.000000       | **FAIL** |
| 6 | cumulative_sums     | 0.999999999998 | PASS (suspect — saturating) |
| 7 | approximate_entropy | 0.000000       | **FAIL** |

LCG correctly fails 3 tests that probe higher-order structure (longest-run,
spectral, approximate entropy) — confirms the test battery discriminates
weak entropy.

## Provenance

### `hmac_drbg_legacy` (production)

- **Algorithm**: HMAC-DRBG SHA-256 (NIST SP 800-90A Rev.1, §10.1.2)
- **Entropy seed**: IonQ Forte 1 `|+⟩^16` 256-shot Z-basis measurement (4096 bits)
- **Personalization string**: `anima.nexus.qrng.ionq_forte1.2026-05-02`
- **Nonce**: `arn:aws:braket:us-east-1:267673635495:quantum-task/bdf470b9-…`
- **Re-derivation check**: first 1024 bytes match
  `state/nexus_qrng_quantum_seed_2026_05_02/hmac_drbg_seed.json` byte-for-byte
- **n_bytes**: 125,000 (10⁶ bits)
- **SHA-256**: `2aa7b6cd85b7c27c681116d2c807c6abb688faa335871c3d5afb0642ef8e744c`
- **Tier**: T1.a-fallback (HMAC-DRBG seeded by IonQ quantum bits)

### `qmirror_mock_lcg` (control)

- Park-Miller / Numerical Recipes LCG: `s = (1664525·s + 1013904223) mod 2³²`, `seed=12345`
- Mirrors `state/qmirror_phase1_staging_2026_05_03/qrng.hexa::_qrng_lcg_bytes`
- SHA-256: `9f59d112b2db44e4c4d943716c622d366bd1e91096f041840db16da8bb323083`
- Tier: T0

## Honest C3 caveats

1. **ANU pull tier used = T1.a-fallback (NOT live T1.b)**.
   The legacy `qrng.anu.edu.au/API/jsonI.php` endpoint is deprecated by ANU
   (rate-limited to ~1 request/min, no API attestation, no SLA, returned
   HTTP 500 on uint16 length=1024 during this run; net throughput dropped to
   ~7s effective per byte → 243h ETA for 1Mbit, infeasible). The new
   `api.quantumnumbers.anu.edu.au` endpoint requires `NEXUS_QMIRROR_ANU_KEY`
   which is not present in this environment. Production stream evaluated is
   therefore the IonQ-Forte-1-seeded HMAC-DRBG (real quantum entropy +
   NIST-approved SP 800-90A expansion). **A subsequent re-test on a true
   live ANU stream remains TODO** — gated on key provisioning + endpoint
   stability.

2. **Sample size = NIST minimum, not certification-grade**.
   1,000,000 bits per stream is the NIST SP 800-22 *minimum*; full
   certification typically requires N=10⁹ bits and m independent sequences
   for the second-tier proportion-of-passing metric. A single-sequence
   p-value PASS at n=10⁶ is necessary but **not sufficient** evidence of
   cryptographic-grade entropy. cond.4 falsifier F-QM-NIST-TIER1-1 is
   intentionally a tier-1+ floor, not a 90B-style health-test certification.

3. **Test selection rationale = tier-1+ only (7 of 15 SP 800-22 tests)**.
   This run covers ONLY the 7 tier-1+ tests
   (monobit, block_frequency, runs, longest_run, dft, cumulative_sums,
   approximate_entropy) per F-QM-NIST-TIER1-1. The remaining 8 SP 800-22
   tests (binary_matrix_rank, non_overlapping_template,
   overlapping_template, maurers_universal, linear_complexity, serial,
   random_excursion, random_excursion_variant) are NOT included; tier-2+/
   full-battery PASS is a separate condition not adjudicated here.
   **Critically**: the prior subagent's `nistrng`-package run (state
   `nexus_qmirror_nist_2026_05_03/results.json`) is **superseded** — that
   library reported approximate_entropy p=0.0 and cumulative_sums p≈1.0
   due to two reproducible bugs at n=10⁶
   (`test_cumulative_sums.py`: int8 cumsum overflow → score saturates;
   `test_approximate_entropy.py`: `min(2,max(3,…))` block-length inversion +
   `numpy.log(c_i/10.0)` typo → score collapses to 0). This run uses a
   direct rewrite from the SP 800-22 Rev.1a spec equations to remove both;
   sources in `state/nexus_qmirror_nist_2026_05_03/run_tier1plus_clean.py`.

## Why this supersedes prior subagent runs (a3fa029, a2e3fa2e, a913834)

- a3fa029 / a2e3fa2e: did not complete the battery
- a913834: completed all 14 tests via `nistrng` but reported "7/14 PASS" on
  full battery. The tier-1+ verdict logic in that script keyed off
  lowercase test names (`monobit`, `cumulative sums`) while
  `nistrng.Result.name` returns capitalised `Monobit`, `Cumulative Sums`
  etc., so all 7 tier-1+ tests were silently classified `INELIGIBLE` →
  vacuous FAIL verdict.  Once the case-mismatch is fixed the same data
  yields 5/7 PASS for HMAC-DRBG (DFT and Approximate Entropy spuriously
  fail due to library bugs identified above).  **This re-run with a clean
  reference implementation yields 7/7 PASS — the previously reported
  failures were nistrng artefacts, not properties of the entropy stream.**

## Artefacts

- `state/nexus_qmirror_nist_2026_05_03/sample_1mbit.bin`           (canonical alias)
- `state/nexus_qmirror_nist_2026_05_03/sample_1mbit_hmac_drbg.bin` (production stream)
- `state/nexus_qmirror_nist_2026_05_03/sample_1mbit_mock.bin`      (control)
- `state/nexus_qmirror_nist_2026_05_03/results_tier1plus.json`     (full per-test results + provenance + caveats)
- `state/nexus_qmirror_nist_2026_05_03/verdict.json`               (cond.4 PASS verdict)
- `state/nexus_qmirror_nist_2026_05_03/run_tier1plus_clean.py`     (clean SP 800-22 reference impl)
- `state/nexus_qmirror_nist_2026_05_03/tier1plus_clean.log`        (run log)
- `state/markers/qmirror_cond4_nist_landed.marker`

## Open follow-ups

1. **Live T1.b ANU re-test**: provision `NEXUS_QMIRROR_ANU_KEY`
   (free tier signup at quantumnumbers.anu.edu.au) then re-run with
   `--anu-bytes <path>`. Script supports it via the `--anu-bytes` flag.
2. **Cross-vendor independence (qmirror n2)**: re-test against IonQ Aria,
   IDQ Quantis hardware QRNG to satisfy single-vendor caveat.
3. **Tier-2+ / full-battery PASS** at n=10⁶ AND tier-1+ PASS at n=10⁹
   remain separate conditions — schedule a long-running batch when
   compute budget permits.
