---
schema: anima/modules/rng/ai-native/1
last_updated: 2026-05-02
ssot:
  interface: anima/core/rng/source.hexa
  registry:  anima/core/rng/registry.hexa
  router:    anima/core/rng/router.hexa
  config:    anima/config/rng_sources.json   # untracked per .gitignore:81 policy
upstream_dependency:
  hexa_lang_stdlib: stdlib/qrng_anu.hexa     # http_client → ANU REST
  upstream_doc:     /Users/ghost/core/hexa-lang/stdlib/qrng_anu.ai.md
markers:
  abstraction_landed: state/markers/anima_rng_abstraction_t1_anu_complete.marker
  primary_landed:     state/markers/anima_rng_anu_primary_landed.marker
roadmap_entry: 251
status: ANU primary, ESP32 wrapped, T2/T3/T4 stubs
---

# anima RNG abstraction (AI-native)

Pluggable quantum/classical entropy source layer. Consumers ask for N bytes from a named source (or trust the router fallback chain). New sources plug in as one `.hexa` module + one config block.

## TL;DR for an agent reading this cold

- Default chain: **ANU → ESP32 → urandom**. ANU is real quantum (vacuum-fluctuation @ qrng.anu.edu.au), free, no auth, but rate-limited to ~1 req/min.
- To collect bytes: call `rng_source_collect("<name>", n_bytes, opts)` from `anima/core/rng/router.hexa`. The router walks the chain.
- To force a single source: `ANIMA_RNG_SOURCE=esp32` env (no fallback).
- To override chain: `ANIMA_RNG_FALLBACK_CHAIN=ibm_q,idq_quantis,urandom`.
- For deterministic CI: `ANIMA_QRNG_MOCK=1` (ANU returns LCG fixture).
- For real ANU API call: `ANIMA_QRNG_LIVE=1` + caller honors 60s pacing.
- **Do not modify** `anima-physics/{esp32/qrng_bridge,verify_7cond_hw,hw_engine_bridge}.hexa` — these are wrapped, not migrated. Migrating consumer sites to the router is a separate, opt-in cycle.

## Architecture map

```
caller
  └── anima/core/rng/router.hexa            (priority + fallback)
       └── anima/core/rng/registry.hexa     (name → module)
            ├── anima/modules/rng/urandom.hexa        T0  IMPLEMENTED  (kernel CSPRNG, NOT quantum)
            ├── anima/modules/rng/esp32.hexa          T0  WRAPPED      (preserves anima-physics/esp32/qrng_bridge.hexa)
            ├── anima/modules/rng/anu.hexa            T1  IMPLEMENTED  ← PRIMARY
            │    └── stdlib/qrng_anu (hexa-lang upstream)
            ├── anima/modules/rng/ibm_q.hexa          T2  STUB
            ├── anima/modules/rng/idq_quantis.hexa    T3  STUB
            └── anima/modules/rng/kaist_optical.hexa  T4  STUB
```

## Public API contract

```hexa
struct RngSourceMeta {
    name:           str
    tier:           int    // 0..4, see tier table
    throughput_bps: int
    cost_usd:       int
    lead_days:      int
    is_quantum:     int    // 0/1
    is_local:       int    // 0/1
    is_free:        int    // 0/1
    status:         str    // "IMPLEMENTED" | "WRAPPED" | "STUB"
    vendor:         str
}

struct RngCollectResult {
    ok:         int        // 0 on any failure (parse / network / rate-limit / stub)
    n_bytes:    int
    bytes_:     [int]      // 0..255 each; len == n_bytes when ok==1
    sha256_hex: str        // hex digest of bytes_
    message:    str        // human-readable diagnostic
}

// Per-module: anima/modules/rng/<name>.hexa exports
fn rng_source_meta_<name>() -> RngSourceMeta
fn rng_source_collect_<name>(n_bytes: int, seed: int) -> RngCollectResult
```

Caller-visible aggregator: `anima/core/rng/rng_main.hexa` runs all module selftests + interface contract checks (14 categories, byte-identical 2-run).

## Tier table (canonical)

| Tier | Source | Throughput | Cost | Lead | Quantum | Local | Status | Vendor / wire |
|------|--------|-----------|------|------|---------|-------|--------|---------------|
| 0 | `urandom` | 1 Gbps | $0 | 0 | ✗ | ✓ | IMPLEMENTED | POSIX kernel CSPRNG (always-available fallback) |
| 0 | `esp32` | 256 kbps | $4 | 0 | ✓ | ✓ | WRAPPED | ESP32-S3 USB-CDC (mock-LCG layer; serial HW path needs hexa-lang serial stdlib) |
| **1** | **`anu`** | **1 kbps** | **$0** | **0** | **✓** | **✗** | **IMPLEMENTED + PRIMARY** | qrng.anu.edu.au public REST (vacuum fluctuation) |
| 2 | `ibm_q` | 100 bps | free-tier | 7-14d | ✓ | ✗ | STUB | qiskit-ibm-runtime SDK + `IBM_QUANTUM_TOKEN` |
| 3 | `idq_quantis` | 240 Mbps (PCIe-240M) | $1k-10k | 28-56d | ✓ | ✓ | STUB | libQuantis SDK + PCIe device + udev |
| 4 | `kaist_optical` | 1 Gbps | free/sponsored | 30-90d | ✓ | ✓ | STUB | KAIST research collab + IRB + custom FPGA + optical fibre |

Throughput for ANU is sustained free-tier (≤8 kbit per chunk × 1 chunk/min); HW rate is 5.7 Gbps but internet-throttled.

## Invocation patterns

### Mock / CI default (no network)

```hexa
// anima/modules/rng/anu.hexa: ANIMA_QRNG_MOCK=1 → deterministic LCG fixture, same shape
let r = rng_source_collect_anu(64, /*seed*/ 1)
// r.ok == 1, r.bytes_ length 64, deterministic across runs
```

### Live ANU (real quantum)

```bash
# explicit live (1 req/min rate-limited; chunks > 1024 bytes paced 60s apart)
ANIMA_QRNG_LIVE=1 hexa.real <driver>.hexa
```

```hexa
let r = rng_source_collect_anu(8, 1)
// r.bytes_ from real vacuum-fluctuation measurement
```

### Force-single-source (no fallback)

```bash
ANIMA_RNG_SOURCE=esp32 hexa.real <driver>.hexa
# router returns ESP32 result or hard-fails (no cascade)
```

### Custom fallback chain

```bash
ANIMA_RNG_FALLBACK_CHAIN=anu,idq_quantis,urandom hexa.real <driver>.hexa
```

## Failure cascade (default chain)

```
anu.collect()
  ├── ok=1 → return                                      (best case: real quantum)
  └── ok=0 (network/rate-limit/parse fail)
       └── esp32.collect()
            ├── ok=1 → return                             (mock-LCG layer; entropy is NOT quantum)
            └── ok=0
                 └── urandom.collect()
                      └── ok=1 → return                   (kernel CSPRNG; NOT quantum)
```

**Critical for callers**: when `ok=1`, inspect `meta.is_quantum`. The fallback chain silently degrades quantum → non-quantum. Security-critical consumers must hard-fail when `is_quantum == 0`.

## Adding a new RNG source (T2/T3/T4 wire-up template)

1. Create `anima/modules/rng/<name>.hexa` with the two exported fns and three structs (mirror `anu.hexa`).
2. Implement `rng_source_collect_<name>(n_bytes, seed)`:
   - Validate inputs.
   - Vendor-specific call (SDK / device / network).
   - Return `rng_result_ok(bytes_, sha256, msg)` or `rng_result_fail(reason)`.
3. Register in `anima/core/rng/registry.hexa` (add dispatch case).
4. Add config block to `anima/config/rng_sources.json` with full meta (use existing entries as template).
5. Add module selftest (mock + opt-in live) and an aggregator test in `anima/core/rng/rng_main.hexa`.
6. Update this README's tier table row from STUB to IMPLEMENTED.
7. Land marker: `state/markers/anima_rng_<name>_landed.marker`.

Per-Tier wiring hint:

- **T2 IBM Q** (`ibm_q.hexa`): `qiskit-ibm-runtime` Python via `exec("python3 -c ...")` facade; or stdlib python bridge if landed. Bell-state circuit shots → bitstream pack. Auth via `IBM_QUANTUM_TOKEN`.
- **T3 IDQ Quantis** (`idq_quantis.hexa`): purchase device, install libQuantis SDK, expose `/dev/quantis0` via udev rule, `exec("…libQuantis_GetData…")` or FFI when hexa-lang FFI stdlib lands.
- **T4 KAIST optical** (`kaist_optical.hexa`): research collab + IRB clearance gates; custom FPGA firmware + optical fibre. Treat as **research**, not production, until clearance documented in marker.

## Rate-limit and pacing (ANU)

ANU public API enforces ~1 request/min unsigned. The anima module honors this:

- `ANU_CHUNK_MAX = 1024` bytes per request.
- `ANU_PAUSE_MS = 60000` between chunks.
- For 4096 bytes → 4 chunks → ≥3 min wallclock.
- Don't call ANU in tight loops for high-throughput needs — switch to T3 IDQ or T0 urandom.

## raw#10 caveats (read before relying)

1. **Fallback silently degrades quantum-ness.** Check `meta.is_quantum`.
2. **`anu` requires network.** Air-gapped → set `ANIMA_RNG_SOURCE=esp32`.
3. **`esp32` is mock-LCG today**, not real HW serial. Real-HW serial path lands when hexa-lang serial stdlib lands; until then, treat as deterministic pseudo-random regardless of `is_quantum=1` flag.
4. **NIST SP 800-90B health tests not implemented.** Informational only — do not certify.
5. **`anima/config/rng_sources.json` is untracked** (`.gitignore:81` policy alongside `consciousness_laws.json`). The marker pins its sha256 for verification.
6. **`verify_7cond_hw.hexa` and `hw_engine_bridge.hexa` use inline LCG**, not this abstraction. They were preserved unchanged. Migration to router is opt-in.
7. **`exec("printenv X")` env-visibility quirk** in hexa-lang main entry observed 2026-05-02 — `anu.hexa` `main()` live-probe gate may not fire under `ANIMA_QRNG_LIVE=1` env in some shell contexts. Direct call `qrng_anu_uint8_live(N)` works (verified). Affects diagnostic/selftest CLI only, not library callers.

## Verified end-to-end (2026-05-02)

- ANU REST raw smoke: `success:true` 8 bytes returned.
- hexa-lang stdlib selftest: `qrng_anu` 20/20, `http_client` 5/5.
- hexa-lang stdlib live API smoke: `qrng_anu_uint8_live(8)` PASS (b0=33, b3=175).
- anima abstraction selftest: 14 categories all PASS.
- Post-swap mock selftest: PASS.
- Post-swap live smoke via 1-shot driver: PASS — bytes `[44,38,14,157,148,53,203,250]`.
- Preserved files sha unchanged: `qrng_bridge.hexa`, `verify_7cond_hw.hexa`, `hw_engine_bridge.hexa`.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `anima/core/rng/source.hexa` | `5c4174a1e74bf6baab71012c5805faaa6e8a277d5243024060039105c1cd1e2e` | 143 |
| `anima/core/rng/registry.hexa` | `0a2096fc93979b079f2398e1779bb38ca91093815ff00fb75b8535c060741cae` | 339 |
| `anima/core/rng/router.hexa` | `0eaa6d0a8b7187deda3666882b8677c70795ced68a1b2f6bbd985cf80d9aae8e` | 319 |
| `anima/core/rng/rng_main.hexa` | `e6f431fd2469d637cb012104283de571e69d1fb399958875f637c7cb4fd7bbc1` | 204 |
| `anima/modules/rng/urandom.hexa` | `254e1c6ff473cd38d6b568adea6883c417a845029b18e2c43acfbfc807130469` | 156 |
| `anima/modules/rng/esp32.hexa` | `69694ce45ecf827aee41b5eeacd3f9b31b0d5d276b08f29d1c5b8f3c0e037e68` | 175 |
| `anima/modules/rng/anu.hexa` | `2b76df170440b42b4adb956f4981bb8442736916833e10adb30d939cb6ae834d` | 255 |
| `anima/modules/rng/ibm_q.hexa` | `9cbbf07be455e21167a3a9218ba9321c384ac68fb46960d4c5a2818fb2ae2ae7` | 104 |
| `anima/modules/rng/idq_quantis.hexa` | `fc5e97039f8d77580c5add11c37288e83923140f5e6bf79fe384e1048aaea720` | 104 |
| `anima/modules/rng/kaist_optical.hexa` | `3f37c753a0a5f70c2ca79f9f68c38527711e08fa6ec25fc8d4f18de4e1b51f1d` | 102 |
| `anima/config/rng_sources.json` | `1b0fb6ff7391f42f81d6bd7673fc436636a71574afe9cbd95f62b478be72aba4` | 99 |

shas at land time. After any edit, re-pin via `shasum -a 256` and update this table + the marker.
