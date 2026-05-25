---
schema: anima/modules/rng/ai-native/1
last_updated: 2026-05-03
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
  hexa_wrapper_8src:  state/markers/anima_rng_curby_nist_beacon_landed.marker
  hexa_wrapper_9src:  state/markers/anima_rng_drand_landed.marker
roadmap_entry: 251
status: 9-source land — ANU+CURBy+NIST_Beacon+drand implemented, ESP32 wrapped, urandom T0, T2/T3/T4 stubs (3-jurisdiction quantum-anchor: AU + US + EU)
---

# anima RNG abstraction (AI-native)

Pluggable quantum/classical entropy source layer. Consumers ask for N bytes from a named source (or trust the router fallback chain). New sources plug in as one `.hexa` module + one config block.

## TL;DR for an agent reading this cold

- 9 sources: **urandom (T0), esp32 (T0), anu (T1), curby (T1), nist_beacon (T1), drand (T1), ibm_q (T2), idq_quantis (T3), kaist_optical (T4)**.
- **3-jurisdiction quantum-anchor diversity** (2026-05-03 complete): AU = `anu` (qrng.anu.edu.au, vacuum fluctuation, ~60s pacing), US = `curby` (CU Boulder Bell-test, 60s) + `nist_beacon` (US gov't, 60s), EU = `drand` (League of Entropy, **3s cadence — fastest**).
- Default chain: **ANU → ESP32 → urandom**. ANU is real quantum (vacuum-fluctuation @ qrng.anu.edu.au), free, no auth, but rate-limited to ~1 req/min.
- New seed-anchor sources (2026-05-03): **CURBy** (NIST + CU Boulder, Bell-test verified, Twine/IPLD anchored, 256 bits/60s), **NIST Beacon 2.0** (US sovereignty mirror, ECDSA P384 signed, 512 bits/60s, mixed entropy NOT pure quantum), and **drand quicknet** (League of Entropy 15-org collective, BLS12-381 G1 signed, 256 bits/3s, mixed entropy NOT pure quantum).
- To collect bytes: call `rng_source_collect("<name>", n_bytes, opts)` from `anima/core/rng/router.hexa`. The router walks the chain.
- To force a single source: `ANIMA_RNG_SOURCE=esp32` env (no fallback).
- To override chain: `ANIMA_RNG_FALLBACK_CHAIN=ibm_q,idq_quantis,urandom`.
- For deterministic CI: `ANIMA_QRNG_MOCK=1` (ANU LCG fixture) or `NEXUS_QRNG_MOCK=1` (CURBy/NIST Beacon/drand JSON fixtures under `fixtures/`).
- For real ANU API call: `ANIMA_QRNG_LIVE=1` + caller honors 60s pacing.
- For real CURBy / NIST Beacon / drand: `NEXUS_QRNG_LIVE=1` (no rate-limit issues; drand is 3s/pulse, others ≤1 pulse/min).
- **Dual-stream pattern (planned)**: urandom = workhorse (Gbps); CURBy + NIST Beacon = 60s seed anchor reseed of CSPRNG state. Provides honest sovereignty + Bell-test certification trail without bulk quantum throughput requirement.
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
            ├── anima/modules/rng/curby.hexa          T1  IMPLEMENTED  (NIST+CU Boulder, Bell-test, Twine anchor)
            ├── anima/modules/rng/nist_beacon.hexa    T1  IMPLEMENTED  (NIST Beacon 2.0, ECDSA-signed, mixed entropy)
            ├── anima/modules/rng/drand.hexa          T1  IMPLEMENTED  (League of Entropy, BLS12-381 G1 signed, 3s cadence)
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

| Tier | Source | Throughput | Cost | Lead | Quantum | Local | Status | Vendor / wire | Use case |
|------|--------|-----------|------|------|---------|-------|--------|---------------|----------|
| 0 | `urandom` | 1 Gbps | $0 | 0 | ✗ | ✓ | IMPLEMENTED | POSIX kernel CSPRNG | Workhorse / always-available fallback |
| 0 | `esp32` | 256 kbps | $4 | 0 | ✓ (claim, mock today) | ✓ | WRAPPED | ESP32-S3 USB-CDC (mock-LCG layer; serial HW path needs hexa-lang serial stdlib) | Local hw-anchor (post-bridge) |
| **1** | **`anu`** | **1 kbps** | **$0** | **0** | **✓** | **✗** | **IMPLEMENTED + PRIMARY** | qrng.anu.edu.au public REST (vacuum fluctuation) | AU-jurisdiction quantum primary |
| 1 | `curby` | 4.3 bps | $0 | 0 | ✓ (Bell-test verified) | ✗ | IMPLEMENTED | random.colorado.edu Twine/IPLD chain (NIST + CU Boulder) | Periodic seed anchor (60s reseed); Bell-cert trail |
| 1 | `nist_beacon` | 8.5 bps | $0 | 0 | ✗ (mixed HSM+QRNG, vendor-classified) | ✗ | IMPLEMENTED | beacon.nist.gov/beacon/2.0/pulse/last (ECDSA P-384 signed) | US-jurisdiction sovereignty mirror |
| 1 | `drand` | ~85 bps | $0 | 0 | ✗ (mixed 15-org collective; LavaRand contributes photonic noise but not pure-quantum) | ✗ | IMPLEMENTED | api.drand.sh/<chain>/public/latest (BLS12-381 G1 sig, RFC9380, unchained scheme) | EU-jurisdiction anchor; **3s cadence — fastest free pulse** |
| 2 | `ibm_q` | 100 bps | free-tier | 7-14d | ✓ | ✗ | STUB | qiskit-ibm-runtime SDK + `IBM_QUANTUM_TOKEN` | High-cert quantum (lab) |
| 3 | `idq_quantis` | 240 Mbps (PCIe-240M) | $1k-10k | 28-56d | ✓ | ✓ | STUB | libQuantis SDK + PCIe device + udev | Bulk local quantum (paid) |
| 4 | `kaist_optical` | 1 Gbps | free/sponsored | 30-90d | ✓ | ✓ | STUB | KAIST research collab + IRB + custom FPGA + optical fibre | Research-grade (pending IRB) |

Throughput for ANU is sustained free-tier (≤8 kbit per chunk × 1 chunk/min). CURBy: live-verified 256-bit pulse / 60 s (32 bytes) → seed-anchor only. NIST Beacon: 512-bit pulse / 60 s (64 bytes) → seed-anchor only. drand quicknet: 256-bit pulse / 3 s (32 bytes) → fast seed-anchor; ~85 bps sustained, but 100k samples (~800 MB) still infeasible (~1.2 years).

### Cadence comparison (T1 free public anchors, 2026-05-03)

| Source | Bits / pulse | Period | Sustained bps | Jurisdiction |
|--------|--------------|--------|---------------|--------------|
| anu | up to 8192 | ~60 s (rate-limit) | ~136 bps | AU |
| curby | 256 | 60 s | 4.3 bps | US |
| nist_beacon | 512 | 60 s | 8.5 bps | US |
| **drand** | **256** | **3 s** | **~85 bps** | **EU** |

### Free-tier QRNG market reality (2026-05-03)

No free public QRNG can sustain bulk randomness at >>1 kbps. Bootstrapping 100k samples (~800 MB) is not feasible from any of {ANU, CURBy, NIST Beacon, drand, hotbits, qrandom.io} on a free account — even drand's 3-s cadence at ~85 bps takes ~1.2 years for 800 MB. Honest path: **urandom = workhorse, CURBy + NIST Beacon + drand = reseed anchors of CSPRNG state** (60-s for CURBy/NIST, 3-s available from drand), ANU as on-demand quantum primary, paid IDQ Quantis when bulk quantum is mandatory. Do not advertise CSPRNG-with-quantum-seed downstream as "pure quantum" — flags `is_quantum=0` for `nist_beacon` and `drand` are intentional (raw#10 honest C3).

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
| `anima/modules/rng/curby.hexa` | `e85e80626e31ad3e1548cd1eb098410abe78155360351a8d6b6397ad3e9607fb` | 305 |
| `anima/modules/rng/nist_beacon.hexa` | `768d574c0bee52177c11acf358c6649a34cdb4fd94e01eba101923e7c0695775` | 304 |
| `anima/modules/rng/drand.hexa` | `ebfb9dfa34d07185c8d2da68b4619d6c5db9ac174269fb491e7655e0d47562dd` | 322 |
| `anima/modules/rng/ibm_q.hexa` | `9cbbf07be455e21167a3a9218ba9321c384ac68fb46960d4c5a2818fb2ae2ae7` | 104 |
| `anima/modules/rng/idq_quantis.hexa` | `fc5e97039f8d77580c5add11c37288e83923140f5e6bf79fe384e1048aaea720` | 104 |
| `anima/modules/rng/kaist_optical.hexa` | `3f37c753a0a5f70c2ca79f9f68c38527711e08fa6ec25fc8d4f18de4e1b51f1d` | 102 |
| `anima/modules/rng/fixtures/curby_pulse_sample.json` | `2cf6d523597700e26519ffb8c44ea8a737aa374f3f37a1206da2f8fd68c014d7` | 24 |
| `anima/modules/rng/fixtures/nist_beacon_pulse_sample.json` | `9a24edcd45d7255b0ea3c7ecb25820ec7091448edc7a10ca550019fb6f7f51bc` | 14 |
| `anima/modules/rng/fixtures/drand_pulse_sample.json` | `b2938f49c09cc74978f3fe7eb38f50be19d3cf519652a0b655837d966b1238c5` | 12 |
| `anima/config/rng_sources.json` | `1b0fb6ff7391f42f81d6bd7673fc436636a71574afe9cbd95f62b478be72aba4` | 99 |

shas at land time. After any edit, re-pin via `shasum -a 256` and update this table + the marker.

## CURBy + NIST Beacon land notes (2026-05-03)

### Endpoint discoveries
- CURBy `/api/randomness/latest` → 404 (rejected). Real path: `/api/chains/<chain_cid>/pulses?limit=1`. Pulse shape is Twine/IPLD: `data.content.payload.{round, randomness, signature}`. `randomness` is **256 bits = 32 bytes**, not the 512 bits the original spec assumed. Vendor refers to this as "Bell-test verified randomness".
- Default chain CID pinned in `curby.hexa` (`CURBY_CHAIN_CID`); override via `NEXUS_CURBY_CHAIN_CID` env. Chain rotates rarely; a stale CID will return empty pulses, triggering ok=0 and router fallback.
- NIST Beacon `/beacon/2.0/pulse/last` works as documented. Pretty-printed JSON (`"key" : value` with space) — parser handles both compact and spaced forms.
- NIST Beacon `outputValue` is 128 hex chars = **512 bits = 64 bytes**. `signatureValue` is 1024 hex chars = ECDSA P-384 over SHA-384.

### Falsifier evidence (live, 2026-05-03)
- F_CURBY_01 (mock fixture deterministic): SELFTEST PASS via `_curby_parse_pulse` on fixture JSON; round=1234567, randomness 64-char hex, twine_anchor present.
- F_CURBY_02 (live pulse 64-char hex): `LIVE n=8 sha=22f2d0c2…` — round=6078444 returned, all-hex chars validated.
- F_CURBY_03 (twine_anchor non-empty): live anchor `bafyriqcphlosq22le7gehvxzf67dd22…` (CID-encoded chain pointer).
- F_NIST_01 (mock fixture deterministic): SELFTEST PASS via `_nist_parse_pulse` on fixture; pulseIndex=9876543, outputValue 128-char hex.
- F_NIST_02 (live pulse 128-char hex): `LIVE n=8 sha=286ae355…` — pulseIndex=1770913, all-hex validated.
- F_NIST_03 (signature non-empty): live signatureValue len=1024 (ECDSA P384).

### Honesty caveats (raw#10 C3)
- `curby.is_quantum = 1` is justified by Bell-inequality violation in CU Boulder's measurement chain (vendor-published). We pass through this claim rather than re-certifying.
- `nist_beacon.is_quantum = 0` is **deliberate**. NIST Beacon mixes HSM-CSPRNG + multiple entropy sources including QRNG, but it is not pure-quantum and the vendor does not assert quantum-only. Honest classification beats false advertising.
- Both sources are **seed-anchor scale** (≤64 bytes / 60 s). Do not use as bulk RNG. Router callers requesting `n_bytes > 64` (NIST) / `> 32` (CURBy) get a hard fail — accumulation across pulses is the caller's responsibility.

### Selftest commands
```bash
# Mock (deterministic, no network)
hexa.real anima/modules/rng/curby.hexa
hexa.real anima/modules/rng/nist_beacon.hexa

# Live
NEXUS_QRNG_LIVE=1 hexa.real anima/modules/rng/curby.hexa
NEXUS_QRNG_LIVE=1 hexa.real anima/modules/rng/nist_beacon.hexa
```

### Next-cycle plan (post drand land 2026-05-03)
1. ~~**drand quicknet wrapper**~~ — **LANDED** (this cycle, 322 LoC). 3-jurisdiction quantum-anchor diversity (AU + US + EU) complete.
2. **`nexus/config/qrng_sources.json` update** — add curby + nist_beacon + drand entries (separate cycle to avoid cross-repo write).
3. **`anima/core/rng/dual_stream.hexa`** — formalize urandom-workhorse + CURBy/NIST/drand-anchor seed integration (60-s/3-s reseed of HKDF-extracted CSPRNG state). Provides "honest pure quantum" trail without bulk requirement. (BG in progress.)
4. **`anima/core/rng/registry.hexa` dispatch update** — register `curby`, `nist_beacon`, `drand` cases; required before router can route to them. (BG in progress.)
5. **BLS signature verification** — drand pulses currently treated as "vendor-signed claim" — pairing check on BLS12-381 G1 (RFC9380) deferred until hexa-lang signature stdlib lands. Until then, F_DRAND_03 only enforces signature presence + length, not cryptographic validity.

## drand quicknet land notes (2026-05-03)

### Endpoint discoveries
- v1 endpoint `https://api.drand.sh/<chain_hash>/public/latest` returns full schema: `{round, randomness, signature, previous_signature?}`. Quicknet (unchained scheme) **omits** `previous_signature` (or returns empty) — the parser tolerates both.
- v2 endpoint `https://api.drand.sh/v2/beacons/quicknet/rounds/latest` returns reduced schema `{round, signature}` only — **no `randomness` field**. We use the v1 path with explicit chain hash for full compatibility.
- Chain hash for quicknet: `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971` (BLS unchained-g1-rfc9380, 3-s period). Override via `NEXUS_DRAND_CHAIN` env.
- `randomness` is exactly **64 hex chars = 32 bytes (256 bits)**. `signature` is exactly **96 hex chars = 48 bytes (BLS12-381 G1 RFC9380)**. Both lengths verified live 2026-05-03.
- Cloudflare mirror (`https://drand.cloudflare.com/<chain>/public/latest`) returns identical schema, can be used as redundant endpoint.

### Falsifier evidence (live, 2026-05-03)
- F_DRAND_01 (mock fixture deterministic): SELFTEST PASS via `_drand_parse_pulse` on fixture; round=28000000, randomness 64-hex, signature 96-hex BLS12-381 G1.
- F_DRAND_02 (live randomness exact length 64): observed `round=28327242`, `randomness_len=64`, `signature_len=96`, `previous_signature_len=0` (unchained scheme as expected).
- F_DRAND_03 (signature non-empty + 96 hex chars BLS12-381 G1): live `signature` len=96 — verified. `LIVE n=8 sha=2bde962b7cc18152ddca6da833fd1c31dc5324e9400e8752d7f4a917a9649dfa`.

### Honesty caveats (raw#10 C3)
- `drand.is_quantum = 0` is **deliberate**. The 15-org League of Entropy collective combines entropy from many sources; Cloudflare contributes LavaRand (photonic noise from lava-lamp wall + camera sensor, has quantum-mechanical character) but the collective output is mixed and not certified pure-quantum. Honest classification beats "quantum-washing".
- **BLS signature verification not implemented.** F_DRAND_03 only checks signature *presence* + *length* (96 hex / 48 bytes BLS12-381 G1). Full pairing-based verification on BLS12-381 (per RFC9380) requires a BLS verify primitive — deferred to next cycle when hexa-lang signature stdlib lands.
- **3-second cadence does not solve bulk bootstrap.** ~85 bps sustained × 100k samples (~800 MB) ≈ 1.2 years. drand is a fast *seed-anchor*, not bulk RNG. Use as 3-s reseed of CSPRNG state, never as 100k-sample workhorse.

### Selftest commands
```bash
# Mock (deterministic, no network)
hexa.real anima/modules/rng/drand.hexa

# Live
NEXUS_QRNG_LIVE=1 hexa.real anima/modules/rng/drand.hexa

# Specific round
NEXUS_DRAND_CHAIN=<hex> hexa.real <driver-using-drand_fetch_round.hexa>
```

## dual_stream_seedanchor module (2026-05-03)

`anima/core/rng/dual_stream_seedanchor.hexa` (753 LoC) implements the
**honest pattern** identified in the free-tier QRNG market reality
section above: `/dev/urandom` workhorse for bulk entropy + CURBy
(primary) / NIST Beacon (redundant fallback) as periodic seed anchor
(60 s default cadence, configurable).

### Purpose
Consciousness-metric null distributions, surrogate / bootstrap tests,
and any anima downstream that wants a "quantum-anchored" entropy story
without pretending to have bulk quantum throughput. Per reseed event we
extract ~256 bits from the anchor pulse, expand via SHA-256 KDF into
PCG32 state + increment, then emit bulk bytes XOR-mixed with
`/dev/urandom`.

### NOT a replacement for `anima-eeg/dual_stream.hexa`
That file is the **EEG ↔ Anima Phi correlation harness** with raw#68
byte-identical guarantee (DEFAULT_ANIMA_SEED=2, DEFAULT_EEG_SEED=7
inline LCG). It has a totally different purpose (cross-modal alignment +
Pearson r) and **MUST remain byte-identical**. The seedanchor module is
distinct (different file, different directory, different semantic).
Cross-link only — sha256 of `anima-eeg/dual_stream.hexa` verified
unchanged at land:
`469f194af56d11af960e79bb0a11a12deeb7e107` (sha1; shasum default).

### API
```hexa
let s0 = dual_stream_seedanchor_init(60000)        // reseed cadence ms
let r  = dual_stream_seedanchor_step(s0, 1024)     // emit 1024 bulk bytes
// r.state carries forward; r.bytes_ are the bytes; r.ok=1 on success
let prov = dual_stream_seedanchor_provenance(r.state)
// prov.path = "anima/state/dual_stream_seedanchor_ledger.jsonl"
// prov.last_chain_sha256 / total_reseeds / total_bytes_emitted
```

### Provenance ledger
Each reseed appends a JSONL line at
`anima/state/dual_stream_seedanchor_ledger.jsonl` with fields:
`ts_ms`, `source` (`curby` | `nist_beacon` | `degraded:...`),
`pulse_id`, `pulse_sha256`, `chain_sha256`, `accumulated_bytes`,
`reseed_n`, `is_mock`. Chain hash:
`chain_n = sha256(chain_{n-1} || "|" || pulse_sha_n)` — externally
verifiable with `shasum -a 256`. Verified end-to-end at 2026-05-03 land.

### Falsifiers
- **F_DSS_01** (mock determinism): `NEXUS_QRNG_MOCK=1` + same `s0` produces byte-identical `bytes_` across runs. SELFTEST PASS.
- **F_DSS_02** (cadence reseed): elapsed > `reseed_interval_ms` (or first call) triggers reseed; `total_reseeds` increments. SELFTEST PASS.
- **F_DSS_03** (chain append-only): each ledger entry's `chain_sha256` = `sha256(prev_chain || "|" || pulse_sha256)`. Verified externally with `shasum -a 256` (PASS).

### Live land evidence (2026-05-03)
```
NEXUS_QRNG_MOCK=1 hexa.real anima/core/rng/dual_stream_seedanchor.hexa
[rng/dual_stream_seedanchor] SELFTEST PASS

NEXUS_QRNG_LIVE=1 hexa.real anima/core/rng/dual_stream_seedanchor.hexa
[rng/dual_stream_seedanchor] SELFTEST PASS
[rng/dual_stream_seedanchor] LIVE n=64 src=curby pulse_id=6078471
[rng/dual_stream_seedanchor] LIVE chain_sha=f5c00079aa029d93
```

### Honesty caveats (raw#10 C3)
1. **KDF is not RFC 5869 HMAC-HKDF**. We use
   `sha256(salt || ikm || prev_state)` for extract and
   `sha256(prk || ":" || i)` for expand instead of HMAC-SHA-256
   ipad/opad. Strength relies on SHA-256 PRF assumption + salt
   unpredictability; future cycle should port real HMAC-SHA-256 (no
   native HMAC in hexa-lang stage0; ~50 LoC of byte-plumbing per call).
2. **CSPRNG core is PCG32, not ChaCha20**. PCG32 state is recoverable
   from sufficient output (Bouillaguet et al. 2020). Mitigation: bulk
   bytes XOR-mixed with fresh `/dev/urandom`, so output is at least as
   strong as urandom even if PCG state leaks. **NOT** for cryptographic
   key generation; OK for null distributions / surrogate tests / bootstrap.
3. **Per-anchor entropy budget = 32-64 bytes / 60 s** (CURBy 256-bit /
   NIST 512-bit). Bulk throughput = `/dev/urandom`; the anchor is a
   pulse-rate sovereignty / certification trail, not bandwidth.

### Selftest commands
```bash
# Mock (deterministic, no network)
NEXUS_QRNG_MOCK=1 hexa.real anima/core/rng/dual_stream_seedanchor.hexa

# Live (real CURBy/NIST fetch + 1 reseed cycle)
NEXUS_QRNG_LIVE=1 hexa.real anima/core/rng/dual_stream_seedanchor.hexa
```

### Next-cycle suggestions
1. **Cross-link with `anima-eeg/dual_stream.hexa`** — README cross-reference
   only; raw#68 byte-identical guarantee on the EEG harness must remain.
2. **CURBy + NIST dual-anchor mode** — fetch *both* per reseed and
   sha256-cross-verify before installing into PCG state (currently
   primary/fallback only).
3. **Real HMAC-SHA-256 + RFC 5869 HKDF port** — replace SHA-256-based KDF.
4. **ChaCha20 stream cipher port** — replace PCG32 if cryptographic
   strength is needed downstream.
