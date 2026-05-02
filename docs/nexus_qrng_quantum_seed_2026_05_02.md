# nexus QRNG — IonQ-seeded HMAC-DRBG (2026-05-02)

**Mission ID:** B1 EXEC — Hybrid IonQ-seeded HMAC-DRBG QRNG nexus refresh
**Origin:** #122 권고 1 (nexus QRNG narrative anchor)
**Operator:** anima ghost agent
**Date:** 2026-05-02
**Status:** PASS — research artifact landed; nexus integration spec only (sister-repo PR pending)

## Why

The nexus runtime PRNG today is `algorithmic urandom` — cryptographically secure but classically derived. This refresh replaces the seed-source narrative with a quantum measurement on **IonQ Forte 1** (trapped-ion QPU, Maryland) feeding a NIST SP 800-90A HMAC-DRBG. The DRBG's output is the seed nexus consumes.

## What ran

| Item | Value |
|---|---|
| Device | `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1` |
| Circuit | OpenQASM 3.0 — H^16 \|0⟩ + Z-basis measurement |
| Shots | 256 |
| Bits collected | 4096 (16 qubits × 256 shots) |
| Task ARN | `arn:aws:braket:us-east-1:267673635495:quantum-task/bdf470b9-27bd-443b-8fce-d79291c15949` |
| Queue wait | 219 s observed |
| Completed | 2026-05-02T14:04:38Z |

## Cost

| Line | USD |
|---|---|
| Task fee | $0.30 |
| Shot fee (256 × $0.08) | $20.48 |
| **Total** | **$20.78** |

Within the $0-25 mission cap.

## Entropy assessment (NIST SP 800-90B simplified MCV)

| Metric | Value |
|---|---|
| Bit balance | 2037 zeros / 2059 ones (ideal 2048/2048) |
| `p_max` per bit | 0.502686 |
| `H_min` per bit | 0.992272 bits |
| **Bit-level total min-entropy** | **≈ 4064 bits (99.23 % of raw 4096)** |
| `H_min` per 16-bit symbol | 8.000 bits (256 distinct symbols, all `1/256`) |

The bit-level estimate is the operationally relevant figure for the DRBG seeding.

## HMAC-DRBG mix (NIST SP 800-90A Rev.1, §10.1.2)

| Field | Value |
|---|---|
| Algorithm | HMAC_DRBG-SHA256 |
| Entropy input | 512 bytes (4096 bits) raw quantum |
| Nonce | task ARN (anti-replay) |
| Personalization | `anima.nexus.qrng.ionq_forte1.2026-05-02` |
| First output | 1024 bytes |
| First-32-byte sample | `06be17ff389d4225ca48d911d9d9948979c6884ecef94594dbf1370ddb59e418` |
| SHA-256 of full output | `ddf057ba61916c3183fe245345c6f5108e3ffb88fa573e33474f32740f0da81b` |

## Artifacts

```
state/nexus_qrng_quantum_seed_2026_05_02/
  ├─ quantum_measurement_raw.json   # raw 4096-bit hex + per-shot bitstrings
  ├─ nist_min_entropy.json          # MCV estimator output (bit + 16-bit symbol)
  ├─ hmac_drbg_seed.json            # 1024-byte DRBG output, hex + SHA-256
  ├─ provenance_ledger.json         # full chain-of-custody
  └─ nexus_integration_spec.json    # how nexus repo should consume this
docs/nexus_qrng_quantum_seed_2026_05_02.md  # this file
```

## nexus integration (spec only)

- **Seed file path (nexus repo):** `state/qrng/seed.bin` (JSON wrapper, `first_output_1024_bytes_hex` field)
- **Refresh cadence default:** 1×/week ($83/month)
- **Modes:** `hybrid_default` (XOR with urandom, fallback if stale > 30d), `quantum_only` (hard-fail on miss), `classical_only` (disable hook)
- **Refresh shell snippet:** see `nexus_integration_spec.json::refresh_shell_snippet`

Actual nexus PRNG hook is **sister-repo work** — out of scope for this PR.

## Honest C3 (3 disclosures)

1. **Batch quantum, per-sample classical.** 256 shots are individually quantum-random, but every downstream `random()` draw the nexus PRNG serves is HMAC-DRBG-expanded from the seed — *not* per-sample fresh quantum.
2. **MCV simplified, not certified.** NIST SP 800-90B certification requires the full IID/non-IID test battery (`sp800_90b_entropyassessment`) over ≥1M samples. This artifact runs *only* the single-pass MCV step. Treat the 99.23 % figure as a sanity check, not a certified bound.
3. **nexus integration deferred.** The actual nexus PRNG hook (replacing the urandom call site) is sister-repo work tracked separately. This PR delivers spec + reference seed file only.

## Reproduction

```bash
# 1. AWS Braket creds
export AWS_ACCESS_KEY_ID=$(secret get aws_braket.access_key_id)
export AWS_SECRET_ACCESS_KEY=$(secret get aws_braket.secret_access_key)
export AWS_DEFAULT_REGION=us-east-1

# 2. Submit (off-repo .py at /tmp/b1_nexus_qrng/process.py per HEXA-only policy)
aws braket create-quantum-task \
  --action file:///tmp/b1_nexus_qrng/action.json \
  --device-arn "arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1" \
  --output-s3-bucket "amazon-braket-us-east-1-267673635495" \
  --output-s3-key-prefix "nexus_qrng_$(date -u +%Y_%m_%d)" \
  --shots 256 \
  --device-parameters file:///tmp/b1_nexus_qrng/device_params.json

# 3. Poll → COMPLETED → s3 cp results.json → python3 process.py → copy artifacts
```
