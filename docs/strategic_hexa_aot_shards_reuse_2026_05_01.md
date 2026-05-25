# Strategic Hexa AOT Shards Reuse — N-51 W3 Investigation

> **ts**: 2026-05-02
> **agent**: N-51 W3
> **scope**: inventory `.hxc_aot/hxc_a25..a34` shards on Mac/ubu1/ubu2 + identify creative reuse for N-51 EXEC E blocked Comp 1 / Comp 3 / Comp 4
> **race-isolated dir**: `state/strategic_hexa_aot_shards_reuse_2026_05_01/*.json`
> **constraint compliance**: alpha pod untouched, sibling N-* dirs untouched, shards read-only, $0 spent
> **honest C3**: result is **NO_REUSE**, documented precisely below

---

## §1 Verdict (top-line)

**NO_REUSE.** All 16 AOT shards on Mac (and byte-identical mirrors on ubu1/ubu2) are deterministic byte-stream compression encoders/decoders. The blocked Comp 1/3/4 require numerical tensor operations (4096-d matmul, random projection, L1 gating, Z-score aggregation) that are categorically absent from every shard's capability surface.

The pilot wrap of the most-promising candidate (`hxc_a25 classify` -> Comp 3 L1 proxy) measured Pearson corr = **-0.313** between the proxy signal and the true L1 score — uncorrelated noise, confirming infeasibility.

**Final-answer sentence**: "AOT shards reuse 로 N-51 blocked components 0/3 해소 — 모든 shard 가 byte-stream 압축기라서 4096-d float 텐서 연산을 요구하는 Comp 1/3/4 와 의미적으로 직교하기 때문."

---

## §2 Phase 1 — Inventory

### 2.1 Shard population

Mac `.hxc_aot/` contains **16 shards** (not 10 — actual count includes backups + composite chains). All Mach-O 64-bit arm64 executables. Sources in `/Users/ghost/core/hexa-lang/self/stdlib/hxc_a*.hexa`. The `.hxc_aot_src/` path mentioned in the mission brief does not exist — sources live in `hexa-lang/self/stdlib/`.

| Shard | Size (B) | Role | Schema |
|---|---:|---|---|
| hxc_a18 | 320512 | LZ + PPM order-4 | encode/decode |
| hxc_a23 | 336528 | sparse PPM (small-file dispatch) | encode/decode |
| hxc_a24 | 318688 | v2 bounded compressor | encode/decode |
| hxc_a25 | 306064 | type-aware classifier + dispatcher | classify / dispatch / encode / decode |
| hxc_a25_new | 272664 | legacy a25 build | (same) |
| hxc_a29 | 386048 | deflate-style | encode/decode (--v2/--v3) |
| hxc_a30 | 302416 | BWT + MTF | encode/decode |
| hxc_a30_v1 | 302032 | earlier BWT+MTF | (same) |
| hxc_a33 | 286032 | cross-repo shared-dict | encode/decode/session-roundtrip |
| hxc_a33_pass5 | 286144 | a33 with hash-chain audit | (same) |
| hxc_a33_v1_backup | 286032 | a33 rollback safety | (same) |
| hxc_a34 | 302016 | sub-byte arithmetic coding | encode/decode |
| hxc_a34_v1_backup | 268376 | a34 rollback safety | (same) |
| hxc_a35 | 307568 | source-level pre-transform (column reorder + delta-varint + dict) | encode/decode |
| hxc_composite_chain | 309520 | linear chain a18->a29->a34 | encode/decode (--emit-ledger) |
| hxc_composite_chain_v_c | 311296 | alternate chain ordering | (same) |

### 2.2 ubu1/ubu2 mirrors

`ssh ubu1 ls -la /Users/ghost/core/anima/.hxc_aot/` and same for ubu2 returned byte-identical listings (same sizes, same mtimes Apr/May 2026). No machine-specific shard hides on cluster nodes.

### 2.3 General compiler status

`which hxc` -> not found. `which hexa` -> `/Users/ghost/.hx/bin/hexa` (interpreter only, NOT the missing native compiler). Confirms the EXEC E ledger statement: only single-program AOT shards exist; no general hexa->native compiler is available.

---

## §3 Phase 2 — Mapping blocked components to shards

| Component | Spec LOC | Needs | Exact fit | Wrappable | Chainable | Verdict |
|---|---:|---|:---:|:---:|:---:|:---:|
| Comp 1 emit | 120 | matmul HUB->D_MODEL, tanh-gelu, LCG random control, clamp ±0.014, JSONL emit | no | no | no | **none** |
| Comp 3 readback | 150 | parse 4096-d hidden, LCG random projection ->16, L1 gate count, phi_star, L2 norm, mind_step | no | no (pilot corr -0.31) | no | **none** |
| Comp 4 orchestrator | 100 | 5-seed aggregation, Z-score, verdict tree | no | no | no | **none** |

The shards are byte-stream compressors. The blocked components are numerical kernels. The two domains do not overlap.

---

## §4 Phase 3 — Wrapper feasibility

The most-promising candidate (`hxc_a25 classify`) emits per-input byte-class statistics (`json_per100`, `text_per100`, `multi_per100`, `newline_per100`, `rule_density_per100`). This is the only per-input numerical signal any shard produces — every other shard emits compressed bytes only.

For Comp 3, the only conceivable wrap path was: serialize each 4096-d hidden vector as a JSONL line, run `hxc_a25 classify`, and use `rule_density_per100` as a degraded L1-gate-count proxy. Phase 4 measured this empirically.

For Comp 1 and Comp 4 there is **no candidate at all**: shards do not generate float arrays, do not aggregate cross-run statistics, do not compute Z-scores. Any "wrapper" would be a clean Python rewrite of the blocked component with a no-op shard call attached, which adds LOC instead of saving it.

| Component | Wrapper LOC vs spec LOC | Viable |
|---|---|:---:|
| Comp 1 emit | infinite (must reimplement 100% in Python; shard contributes nothing) | no |
| Comp 3 readback | ~80 LOC scaffold + ~140 LOC re-implementation = ~220 vs spec 150 | no |
| Comp 4 orchestrator | ~95 LOC pure Python port; shard adds 0 | no |

---

## §5 Phase 4 — Pilot wrap result

**Pair**: `hxc_a25 classify` -> Comp 3 L1 proxy
**Path**: `/tmp/n51_W3/wrap_pilot/comp3_classify_wrapper.py` (md5 b08f5f10716bbebea878f342585fdd75)
**Selftest**: PASS (script exits 0; selftest condition is "measure correlation, log result")
**Selftest log**: `/tmp/n51_W3/wrap_pilot/selftest.log` (md5 083c9d9412b1ecb9fe0e44068830eed3)

| seed | true L1 | proxy rule_density | phi_max_abs |
|---:|---:|---:|---:|
| 0 | 11/16 | 10 | 1.1199 |
| 1 |  8/16 |  6 | 1.1285 |
| 2 | 13/16 |  5 | 0.9834 |
| 3 | 11/16 |  9 | 0.9567 |
| 4 |  5/16 |  9 | 1.3029 |
| 5 |  8/16 |  9 | 1.1321 |

**Pearson corr(true_L1, proxy_rule_density) = -0.313**

Interpretation: indistinguishable from zero on n=6. The proxy carries no usable information about gate-band membership of the projected phi vector. Increasing n would not lift the signal — `hxc_a25`'s byte-class statistics are dominated by JSON syntax overhead (key names, commas, brackets), not by the float values' projection-band properties.

---

## §6 Top 3 honest C3

1. **Negative result is structural, not measurement-budget-limited.** Even with 1000 fixtures the corr would not improve because a25 reads JSON syntax tokens, not the encoded float semantics. The wrap path is dead at the design level, not at the sample-size level.

2. **Mac and ubu1 + ubu2 carry byte-identical shard sets.** There is no machine-specific shard hiding elsewhere on the cluster. The 16 shards on Mac are the complete population — no extra shards accessible to W3 without spawning paid pods.

3. **The hexa-lang upstream blocker (roadmap 64-69) is the binding constraint.** Shard reuse could only have helped if a shard happened to coincide with one of the three numerical kernels Comp 1/3/4 need. None do. Restoring the general `hxc` native compiler (or a per-task PYTHON-PROXY exemption) remains the only unblock path.

---

## §7 Cross-references

- N-51 protocol: `docs/strategic_alm_tension_field_test_2026_05_01.md`
- EXEC E blocker ledger: `docs/strategic_alm_tension_field_exec_E_results_2026_05_01.md`
- Hexa toolchain blocker anchor: memory `reference_hexa_roadmap_64_69.md`
- Phase ledgers (race-isolated): `state/strategic_hexa_aot_shards_reuse_2026_05_01/phase{1..5}*.json`
- Pilot wrap artifacts (off-repo per HEXA-FIRST): `/tmp/n51_W3/wrap_pilot/`
