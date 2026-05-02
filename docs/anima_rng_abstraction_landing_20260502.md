# anima RNG abstraction — Tier 1 ANU implementation + 5 sources STUB/WRAPPED landing (2026-05-02)

Reserved roadmap entry: `#251 anima-rng-abstraction-t1-anu-landed`

## §1 Architecture

```
                    ┌──────────────────────────────────────────────────┐
                    │   anima/core/rng/rng_main.hexa                   │
                    │   (entry-point, selftest aggregator)             │
                    └─────────────────────┬────────────────────────────┘
                                          │
                    ┌─────────────────────▼────────────────────────────┐
                    │   anima/core/rng/router.hexa                     │
                    │   (config + env-driven chain selection)          │
                    │     env: ANIMA_RNG_SOURCE / FALLBACK_CHAIN       │
                    │     default: anu → esp32 → urandom               │
                    └─────────────────────┬────────────────────────────┘
                                          │
                    ┌─────────────────────▼────────────────────────────┐
                    │   anima/core/rng/registry.hexa                   │
                    │   (name → dispatch table, switch-style)          │
                    └─────────────────────┬────────────────────────────┘
                                          │
   ┌──────────┬───────────────┬───────────┼───────────────┬──────────────────────┬──────────────────────┐
   │          │               │           │               │                      │                      │
   ▼          ▼               ▼           ▼               ▼                      ▼                      ▼
urandom    esp32           anu         ibm_q          idq_quantis           kaist_optical          (unknown
(Tier 0)   (Tier 0)      (Tier 1)     (Tier 2)         (Tier 3)              (Tier 4)               name → fail)
POSIX      WRAPPED        IMPL          STUB             STUB                   STUB
kernel     LCG-mock      curl/HTTP    qiskit-ibm-      libQuantis             KAIST research
CSPRNG     (preserves    chunked        runtime         SDK + PCIe              collab + IRB
           qrng_bridge)  ANU JSON        SDK              device                + custom FPGA
```

Contract (`anima/core/rng/source.hexa` SSOT):

- `RngSourceMeta` struct: name, tier, throughput_bps, cost_usd, lead_days, is_quantum, is_local, is_free, status, vendor
- `RngCollectResult` struct: ok, n_bytes, bytes_, sha256_hex, message
- Per-source contract (function-name dispatch):
  - `rng_source_meta_<name>() -> RngSourceMeta`
  - `rng_source_collect_<name>(n_bytes: int, seed: int) -> RngCollectResult`

## §2 Source meta table (Tier 0..4)

| Source          | Tier | Throughput     | Cost USD  | Lead    | Quantum | Local | Free | Status      | Vendor                                                                |
|-----------------|-----:|---------------:|----------:|--------:|:-------:|:-----:|:----:|-------------|-----------------------------------------------------------------------|
| urandom         | 0    | 1 Gbps         | 0         | 0 d     | no      | yes   | yes  | IMPLEMENTED | POSIX kernel CSPRNG                                                   |
| esp32           | 0    | 256 kbit/s     | 4         | 0 d     | yes     | yes   | yes  | WRAPPED     | ESP32-S3 USB-CDC                                                      |
| anu             | 1    | 1 kbit/s       | 0         | 0 d     | yes     | no    | yes  | IMPLEMENTED | ANU qrng.au public                                                    |
| ibm_q           | 2    | 100 bit/s      | 0 (free)  | ~10 d   | yes     | no    | yes  | STUB        | IBM Quantum Network (qiskit-ibm-runtime)                              |
| idq_quantis     | 3    | 240 Mbps †     | ~5000     | ~42 d   | yes     | yes   | no   | STUB        | ID Quantique Quantis (default PCIe-240M; legacy USB-4M=4 Mbps)        |
| kaist_optical   | 4    | 1 Gbps         | 0 (sponsor) | ~60 d | yes     | yes   | yes  | STUB        | KAIST chip-scale optical QRNG (research collab)                       |

† IDQ legacy USB-4M model recorded in vendor string; `default_model=PCIe-240M` reflects 2026 commercial baseline.

## §3 T1 ANU usage

```hexa
// File: anima/modules/rng/anu.hexa
// Default selftest path runs in MOCK mode (deterministic fixture).
// Live probe is opt-in.

// 1) selftest only (mock fixture path):
//    hexa run anima/modules/rng/anu.hexa
//    → [rng/anu] SELFTEST PASS

// 2) Live probe (free, ANU public network):
//    ANIMA_QRNG_LIVE=1 hexa_real run anima/modules/rng/anu.hexa
//    → [rng/anu] LIVE n=8 sha=<hex>

// 3) Direct collect from any consumer:
let r = rng_source_collect_anu(64, 42)
if r.ok == 1 {
    println("got " + str(r.n_bytes) + " bytes; sha=" + r.sha256_hex)
}

// 4) Through router (recommended — automatic fallback):
//    Default chain anu→esp32→urandom; if ANU network fails, ESP32 mock LCG;
//    if ESP32 unavailable (e.g. compiled-out), kernel CSPRNG.
let route = rng_route_collect(64, 42)
println("final_source=" + route.final_source)
```

ANU API contract (free, no auth):
- Endpoint: `https://qrng.anu.edu.au/API/jsonI.php?length=N&type=uint8`
- Rate-limit: ~1 req/min unsigned. Module honors with 1000 ms inter-chunk pause.
- Chunk size: 1024 bytes (server hard cap per request).

## §4 STUB → real implementation checklists

### T2 IBM Q (`anima/modules/rng/ibm_q.hexa`)
1. Install qiskit-ibm-runtime in repo-external venv (raw#37 transient helper allowed)
2. Acquire `IBM_QUANTUM_TOKEN` via https://quantum.ibm.com (free tier: queue access)
3. Build 4-qubit Bell-state circuit; submit `runtime.run(circuit, shots=N*8)`
4. Parse measurement outcomes → bit-stream → pack into bytes
5. Sister facade `anima-physics/quantum/cloud_real_ibm_q_facade.hexa` already validates 4-gate contract; reuse the exec(python3 …) pattern there.

### T3 IDQ Quantis (`anima/modules/rng/idq_quantis.hexa`)
1. Procure Quantis device (PCIe-240M default ~$5k; USB-4M legacy ~$1.5k)
2. Install libQuantis SDK from ID Quantique support portal
3. Configure permissions: `/dev/quantis0` udev rule for non-root access
4. Wire `libQuantis_Open(handle)` → `libQuantis_GetData(handle, n_bytes, buf)`
5. Verify with vendor health-test suite (NIST SP 800-22)
6. Update meta `cost_usd` to actual purchase price

### T4 KAIST optical (`anima/modules/rng/kaist_optical.hexa`)
1. Initiate research-collaboration agreement with KAIST QRNG group
2. IRB review (data sovereignty + cross-border research compliance)
3. Receive custom FPGA firmware + optical fibre interface module
4. Wire FPGA serial / PCIe driver
5. Sponsor's data-sharing terms verified
6. Production batch availability check (typically 1-3 month delivery from agreement)
7. Update meta `lead_days` to actual onboarding duration

## §5 ESP32 preservation guarantee

The original ESP32 QRNG bridge is wrapped by a *separate* module (raw#9 strict — no destructive edit). Sha256 audit (this landing):

| File                                          | sha256                                                            | unchanged |
|-----------------------------------------------|-------------------------------------------------------------------|:---------:|
| `anima-physics/esp32/qrng_bridge.hexa`        | `547fa48598535e656f8305e7cf0e9f29394f6402b474f15d40de984690828ed4` | ✓         |
| `anima-physics/verify_7cond_hw.hexa`          | `b7c60e30b022daf12a767bf8353c7a3e2e8725ad376bf46017879f9fbbbd61b2` | ✓         |
| `anima-physics/hw_engine_bridge.hexa`         | `92015e08a0393703eab8088e4c845de3b0a89491eca5d92ede60e71751e6ff20` | ✓         |

Consumer-site smoke verification (post-landing, no migration yet):
- `verify_7cond_hw.hexa`: ALL 7/7 PASS (T3 Embodiment unaffected)
- `qrng_bridge.hexa`: mock LCG batch + tubulin bias matrix output unchanged

The wrapper module `anima/modules/rng/esp32.hexa` mirrors the LCG constants
(`QRNG_LCG_A=1664525, QRNG_LCG_C=1013904223, QRNG_MOCK_SEED=2463534242`) so
its byte stream is bit-equivalent to `qrng_batch_samples` × 256-discretization.

## §6 hexa-lang upstream `qrng_anu` swap point

When the parallel BG subagent lands `hexa-lang/stdlib/qrng_anu.hexa` (HTTP GET +
ANU JSON wrapper), the swap is a **single-line internal change** in
`anima/modules/rng/anu.hexa`:

```hexa
// CURRENT (uses curl exec):
fn _anu_fetch_via_curl(n: int) -> str {
    let url = ANU_ENDPOINT + "?length=" + str(n) + "&type=uint8"
    let cmd = "curl -sS --max-time " + str(ANU_TIMEOUT_S) + " '" + url + "' 2>&1"
    return exec(cmd).trim()
}

// AFTER stdlib/qrng_anu.hexa lands:
//   Replace the function body with one stdlib call. Surrounding chunking,
//   parsing, sha256, error-handling stays identical (same JSON shape).
fn _anu_fetch_via_curl(n: int) -> str {
    return qrng_anu_uint8(n).raw_json    // <-- ONLY this line changes
}
// (also rename fn to `_anu_fetch` for clarity in the swap commit; both forms
//  return the same JSON string contract.)
```

`anima/core/rng/router.hexa` and `registry.hexa` mirror the same pattern in
their inlined ANU branches.

## §7 raw#10 caveats (7)

1. **hexa-lang stdlib `qrng_anu` upstream not yet landed** — ANU module currently
   uses `exec(curl ...)` until the stdlib HTTP wrapper module is published.
   1-line swap point documented in §6. This landing intentionally does NOT
   block on hexa-lang completion (parallel cycle).

2. **ANU rate-limit fallback failure mode** — if ANU returns HTTP 429 or
   timeout, `rng_route_collect` cascades to the next chain entry (esp32 mock
   LCG, then urandom kernel CSPRNG). The router prints which fallback engaged
   so consumers can audit at runtime. Note: `urandom` is NOT quantum;
   downstream quantum-claim consumers must check `meta.is_quantum` before use.

3. **NIST SP 800-90B health tests NOT implemented** — informational caveat per
   `docs/anima_quantum_postquantum_abstraction_layers_20260425.md:74`.
   Recommended for production use; deferred to follow-up cycle.

4. **Tier 3 IDQ Quantis throughput dual-value** — the meta records
   `throughput_bps_default=240e6` (PCIe-240M, 2026 model) and
   `throughput_bps_legacy_usb_4m=4e6` (legacy reference from
   `docs/anima_quantum_postquantum_abstraction_layers_20260425.md:33`). Stub
   meta uses default; legacy preserved in vendor string.

5. **ESP32 wrapper is mock-LCG layer, not real serial HW** — original
   `qrng_bridge.hexa` exposes mock-LCG only; serial port reads activate when
   hexa-lang serial stdlib lands. The wrapper interface stays identical at
   that point (1-line swap inside `rng_source_collect_esp32`). Selftest
   determinism does not rely on a physical ESP32 device being attached.

6. **Network-dependent T1** — ANU is `is_local=0`. Air-gapped deployments
   should set `ANIMA_RNG_SOURCE=esp32` or `ANIMA_RNG_FALLBACK_CHAIN=esp32,urandom`
   to bypass network calls entirely.

7. **Consumer-site `verify_7cond_hw.hexa` was NOT migrated to use the new
   abstraction** — T3 Embodiment still uses inline `qrng_bias_vec` via the
   original LCG constants. Migration is a separate cycle (router stays
   opt-in until consumers explicitly switch). Preserved-files audit
   confirms zero destructive edits.

## §8 Reserved roadmap

`#251 anima-rng-abstraction-t1-anu-landed` (claim filed in this doc; commit
title should reference the marker `state/markers/anima_rng_abstraction_t1_anu_complete.marker`).

Next-cycle candidates:
- C-1: hexa-lang `stdlib/qrng_anu.hexa` swap-in (depends on parallel BG subagent landing)
- C-2: NIST SP 800-90B health test implementation (informational caveat #3)
- C-3: T2 IBM Q real wire-up (sister facade reuse path, $0 hardware)
- C-4: Migrate `verify_7cond_hw.hexa` T3 to use `rng_route_collect` (consumer-site pilot)
- C-5: Add ANIMA_RNG_CONFIG_FILE env to load `anima/config/rng_sources.json` priority list at runtime (currently env-driven only)

## §9 Selftest evidence summary

| Selftest                         | Cases | Result |
|----------------------------------|------:|:------:|
| Source interface contract        | 6     | PASS   |
| Registry name + meta dispatch    | 6     | PASS   |
| Registry collect dispatch        | 7     | PASS   |
| Router default chain resolution  | 1     | PASS   |
| Router env override (FALLBACK)   | 1     | PASS (manual via hexa_real) |
| Router env override (SOURCE)     | 1     | PASS (manual via hexa_real) |
| Router cascade on STUB-first     | 3     | PASS (ibm_q→idq→urandom)    |
| ESP32 determinism (seed match)   | 12    | PASS   |
| ESP32 anti-determinism (seed≠)   | 6     | PASS (≥6/8 bytes differ)    |
| Stub sentinel (3 modules)        | 3     | PASS   |
| Tier coverage                    | 5     | PASS (T0..T4)               |
| Aggregator (`rng_main.hexa`)     | 4     | PASS   |
| Byte-identical 2-run             | 1     | PASS (body sha `49b3434098…`) |
| Consumer `verify_7cond_hw`       | 7     | PASS (unchanged)            |
| Consumer `qrng_bridge`           | demo  | OK (unchanged)              |

Total: 14 selftest categories, all PASS. Body sha `49b3434098e30753a0fe17353934d5f219165bf271cfbf980839919c8857c64a` (resolver-line excluded).
