# anima ↔ nexus QRNG dependency wire spec — 2026-05-03

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)

`raw#9` hexa-only · `raw#10` honest C3 · `raw#15` no-personal-paths · `raw#65` idempotent · `raw#68` byte-identical

**Status:** SPEC ONLY — no code changes in this cycle.
**Scope:** design the cross-repo dependency wire so anima's 7 RNG sources call into nexus QRNG provider modules, while honoring byte-identical reproducibility and the consumer/provider perspective split already encoded in the two `.roadmap.qrng` files.

**Sister files (read-only this cycle):**
- `anima/anima/modules/rng/{anu,curby,esp32,ibm_q,idq_quantis,kaist_optical,nist_beacon,urandom}.hexa`
- `anima/anima/core/rng/{router,registry,source,rng_main}.hexa`
- `anima/anima/config/rng_sources.json`
- `nexus/modules/qrng/{anu,hardware_qrng,mock_qrng}.hexa`
- `nexus/core/qrng/{router,registry,source,qrng_main}.hexa`
- `hexa-lang/stdlib/qrng_anu.hexa`
- `hexa-lang/self/module_loader.hexa`
- `anima/.roadmap.qrng` (consumer) · `nexus/.roadmap.qrng` (provider)
- `anima/anima-eeg/dual_stream.hexa` (raw#68 byte-identical reference)

---

## 1. Current dependency graph (audit)

```
                    ┌────────────────────────────────────────────────────┐
                    │  hexa-lang/stdlib/qrng_anu.hexa                    │
                    │  (qrng_anu_uint8_live, parse_response, chunked)    │
                    └────────────▲───────────────────────────────────────┘
                                 │ use "stdlib/qrng_anu"
                                 │
   anima/anima/modules/rng/      │
   ┌──────────────────┐          │
   │ anu.hexa         │──────────┘
   │ curby.hexa       │ inline curl + JSON parser (no use)
   │ esp32.hexa       │ inline LCG mirror of anima-physics/esp32/qrng_bridge
   │ urandom.hexa     │ inline dd if=/dev/urandom
   │ nist_beacon.hexa │ (BG-in-flight) inline curl + parser
   │ ibm_q.hexa       │ STUB (no inline impl)
   │ idq_quantis.hexa │ STUB
   │ kaist_optical    │ STUB
   └────────▲─────────┘
            │ called by
   anima/anima/core/rng/router.hexa  (default chain: anu → esp32 → urandom)
            │
            └─ inline _route_collect duplicates per-source logic
               (registry.hexa is the SSOT but router carries its own copy
                because hexa-lang stage0 had no `use` at the time of land)

   nexus/modules/qrng/             nexus/core/qrng/router.hexa
   ┌──────────────────┐            (default chain: anu → hardware_qrng → mock_qrng)
   │ anu.hexa         │            current state: stub-equivalent —
   │ hardware_qrng    │ STUB         _route_collect("anu") returns
   │ mock_qrng        │              "live deferred to wrapper module"
   │ curby (in-flight)│
   │ nist_beacon (in-flight)
   └──────────────────┘
                                    NO incoming wire from anima today.
```

**Observations**
- Only `anima/modules/rng/anu.hexa` uses an external module (`stdlib/qrng_anu`); the other six are self-contained.
- `anima/core/rng/router.hexa` re-inlines per-source bytes paths instead of dispatching through `registry.hexa` (technical debt; not blocker for this spec).
- `nexus/modules/qrng/anu.hexa` is a smaller, slightly newer copy of the anima module — same parser, same mock fixture, same env gating. It is effectively a parallel implementation, not a provider used by anima.
- Roadmap perspective is already correct: `nexus/.roadmap.qrng` = `provider`, `anima/.roadmap.qrng` = `consumer`. Code wire has not caught up.

---

## 2. Target dependency graph (provider/consumer split)

```
   ┌────────────────────────────────────────────────────────────────┐
   │  nexus/core/qrng/router.hexa     ← single provider entry point │
   │  qrng_route_collect(n, seed)     fallback chain config-driven  │
   └────────▲───────────────────────────────────────────────────────┘
            │ use "nexus/modules/qrng/{anu,curby,nist_beacon,hardware_qrng,mock_qrng}"
            │
   nexus/modules/qrng/* (production implementations, IMPLEMENTED_real)
            ▲
            │ thin cross-repo call (one of three mechanisms in §3)
            │
   anima/anima/modules/rng/* (consumer wrappers, ≤ 30 lines each)
   - delegate to nexus router for live bytes
   - keep anima's struct surface (RngCollectResult / RngSourceMeta)
   - keep mock fixture path on ANIMA_QRNG_MOCK=1 for byte-identical CI
            ▲
            │
   anima/anima/core/rng/router.hexa  ← consumer-side fallback chain
   chain: anu → curby → nist_beacon → esp32 → urandom
   (all "remote quantum" sources go through nexus; esp32 + urandom stay local)
```

**Two-router pattern (anima router ON TOP of nexus router):** anima retains its own router because the consumer chain mixes nexus-provided remote sources with anima-local sources (esp32, urandom) that nexus does not own. Nexus's chain is `anu → hardware_qrng → mock_qrng` — narrower scope.

---

## 3. Cross-repo import mechanism — 3 options + ranked recommendation

The hexa-lang module loader (`hexa-lang/self/module_loader.hexa`) resolves `use "..."` paths in this order:

1. caller-relative (`<caller_dir>/<path>.hexa`)
2. `g_target_dir`-relative (top-level script's dir)
3. stdlib prefix `stdlib/...` → `$HEXA_STDLIB_ROOT/<rest>.hexa` if set, else `$HEXA_LANG/self/stdlib/<rest>.hexa`
4. project-root fallback (`$HEXA_LANG/<imp>` and bare `<imp>`)

Three feasible mechanisms emerge:

### Option A — promote nexus modules to hexa-lang stdlib (`stdlib/qrng/*`)

- Move/symlink `nexus/modules/qrng/*.hexa` under `hexa-lang/self/stdlib/qrng/`.
- anima writes `use "stdlib/qrng/anu"` (same pattern as today's `stdlib/qrng_anu`).
- Resolution path 3 already supports this with **zero env config**.
- **Cost:** crosses repo boundaries (nexus code lives in hexa-lang). Conflicts with provider/consumer perspective: nexus is the provider, not hexa-lang.
- **Verdict:** clean wire but wrong ownership semantics.

### Option B — `HEXA_STDLIB_ROOT` env override pointing at nexus

- Set `HEXA_STDLIB_ROOT=$ROOT/core/nexus/modules` for anima processes.
- anima writes `use "stdlib/qrng/anu"`; loader resolves to `core/nexus/modules/qrng/anu.hexa`.
- **Cost:** one env var per process; conflicts with hexa-lang's actual stdlib if anima also uses any (e.g. `stdlib/json_object`) — `HEXA_STDLIB_ROOT` is a single-root override, so anima would lose access to hexa-lang stdlib once set.
- **Verdict:** breaks transitive deps; not viable.

### Option C — caller-relative cross-repo path via `$HEXA_LANG`-rooted import — **recommended**

- anima writes `use "../nexus/modules/qrng/anu"` (caller-relative path 1) **OR** rely on resolution path 4 (project-root): `use "nexus/modules/qrng/anu"` and run with `HEXA_LANG=$ROOT/core` so loader walks `$HEXA_LANG/nexus/modules/qrng/anu.hexa`.
- **Cost:** anima callers must set `HEXA_LANG=$ROOT/core` (already conventional in dev for hexa-lang stdlib resolution); no new env var.
- **Benefit:** ownership stays nexus-owned; anima is an explicit consumer; no coupling to hexa-lang stdlib.
- **Caveat:** **NOT verified** that the loader resolves a sibling-repo path through `HEXA_LANG=core`-rooted lookup in the current build — `ml_resolve_project_root` checks `HEXA_LANG`-relative + bare `<imp>`, so this works only if `HEXA_LANG` is set to the repo-parent (typically `$ROOT/core`). In `raw#15` no-personal-paths terms, `HEXA_LANG=$ROOT/core` is the canonical form (where `$ROOT` is the user's chosen base).

### Recommendation: **Option C**, with fallback rule

```
use "nexus/modules/qrng/anu"   # primary form, requires HEXA_LANG=<root>/core
```

Stage 1 of migration MUST land a verifying selftest (`anima/anima/modules/rng/_xrepo_smoke.hexa`) that fails with explicit message if `use "nexus/..."` fails to resolve, instead of silently falling back. This converts "raw#10 honest C3" caveat (3) into a runtime gate.

---

## 4. Migration plan — 4 stages

Each stage is bounded by anima cycle scope and assumes other BGs leave the wire alone between stages.

### Stage 1 — nexus provider implementations land (PROVIDER-side)

- in-flight BG: nexus `modules/qrng/{curby,nist_beacon}` IMPLEMENTED_real.
- post-condition: `nexus/core/qrng/router.hexa::_route_collect` actually dispatches to module bytes paths (not stub messages).
- **add:** `qrng_route_collect_typed` returning a struct compatible with anima's `RngCollectResult` (fields: `ok`, `n_bytes`, `bytes_`, `sha256_hex`, `message`).
- **add:** `_xrepo_smoke.hexa` selftest verifying `use "nexus/modules/qrng/anu"` resolves under `HEXA_LANG=core`.
- **cost estimate:** 0.5 cycle if BG already covers IMPLEMENTED_real swaps; +0.2 cycle for typed result + smoke test.

### Stage 2 — anima wrappers thinned to nexus delegators (CONSUMER-side)

- rewrite `anima/anima/modules/rng/{anu,curby,nist_beacon}.hexa` to ≤ 30 LOC each:
  - import: `use "nexus/modules/qrng/<name>"`
  - `rng_source_collect_<name>(n, seed)` body: call nexus collect, copy bytes/sha into anima's `RngCollectResult`.
  - keep `rng_source_meta_<name>` local (anima's tier/cost surface).
  - keep `_selftest_<name>` local (mock fixture path runs without network).
- `esp32.hexa`, `urandom.hexa`, `ibm_q.hexa`, `idq_quantis.hexa`, `kaist_optical.hexa` — **untouched** (local hardware or stub).
- **cost estimate:** 1 cycle (3 wrappers + selftest sweep + verify byte-identical).

### Stage 3 — deprecate inline duplicates in `anima/anima/core/rng/router.hexa`

- replace router's inline `_route_collect("anu", ...)` body with delegation to the wrapper module (or directly to nexus).
- preserve current chain order; legacy inline code moves to `_legacy_route_collect_inline` retained for 1 cycle as audit fallback.
- **cost estimate:** 0.5 cycle.

### Stage 4 — roadmap cross-link reinforcement

- `anima/.roadmap.qrng::cross_link.provider_evidence` add code-path evidence: `nexus/modules/qrng/<name>` files actually invoked at runtime, not just doc references.
- `nexus/.roadmap.qrng::consumers` already lists `anima`; add explicit `consumer_call_sites` array enumerating the anima wrapper files.
- `anima/.roadmap.qrng::qrng.blk.1` resolution path becomes "Stage 2 PASS" (no longer abstract).
- **cost estimate:** 0.2 cycle.

**Total:** ~2.4 cycles end-to-end if no rework.

---

## 5. Byte-identical preservation verification path

`raw#68` byte-identical applies primarily to `anima/anima-eeg/dual_stream.hexa` (DEFAULT_ANIMA_SEED=2, DEFAULT_EEG_SEED=7, inline LCG). dual_stream does **not** import any rng module today and **must not** acquire one in this migration — its inline LCG is intentional and the `compare_streams` golden output depends on it.

For the 7 rng sources themselves:

- **Mock paths** (ANIMA_QRNG_MOCK=1): both anima and nexus implement the same LCG (`s = (1664525*s + 1013904223) % 4294967296; b = s % 256`) seeded by the caller. After Stage 2, the wrapper calls into nexus's LCG; bytes must remain byte-identical for any (n, seed) pair.
  - **Verifier:** add `state/qrng_byte_identical_2026_05_03/golden_<source>_seed42_n64.hex` capturing pre-migration bytes for every source. Stage 2 selftest re-runs and `diff`s against goldens. PASS = byte-identical preserved across the cross-repo wire.
- **Live paths** (ANIMA_QRNG_LIVE=1): non-deterministic by design (real ANU vacuum noise, real CURBy Bell pulse). Byte-identical not applicable; instead verify `sha256_hex` field is computed identically by anima wrapper post-delegation (anima's `_<name>_sha256_of_bytes` is the SSOT for the hash format — must NOT be moved to nexus or shape changes).

---

## 6. Fallback chain alignment decision — **dual chain (anima retains its own)**

Two chains exist:

| router | chain | scope |
|---|---|---|
| `anima/anima/core/rng/router.hexa` | `anu → esp32 → urandom` | mixes remote-quantum + local-hw + kernel |
| `nexus/core/qrng/router.hexa` | `anu → hardware_qrng → mock_qrng` | remote-quantum + commercial-hw + deterministic safety net |

**Decision: dual chain — anima keeps its top-level router; nexus chain is invoked only for the remote-quantum head segment.**

**Sufficient condition:** anima's chain references nexus modules for `anu`, `curby`, `nist_beacon` (Stage 2 wire), but `esp32`, `urandom`, `ibm_q`, `idq_quantis`, `kaist_optical` stay anima-only. Nexus has no business resolving anima-local hardware (esp32 is `anima-physics/esp32/qrng_bridge.hexa`) or anima-installation kernel (`/dev/urandom`).

**Recommended Stage 2 anima default chain:** `anu → curby → nist_beacon → esp32 → urandom` (5 entries; quantum-first, local-fallback-last, kernel-last-resort).

Update `anima/anima/config/rng_sources.json::default_priority` accordingly.

---

## 7. Honest C3 caveats (raw#10)

1. **Cross-repo `use "nexus/..."` resolution UNVERIFIED.** Module loader code path 4 (`ml_resolve_project_root`) tries `$HEXA_LANG/<imp>`; this only works if `HEXA_LANG` is set to the repo-parent dir (typically `core/`). I have not run a test confirming the loader actually walks up to find `nexus/modules/qrng/anu.hexa` from anima context. Stage 1 smoke test is the gate.
2. **Byte-identical at the cross-repo seam is mock-only.** Live paths are non-deterministic by physics; only mock fixtures preserve byte-identical. If a downstream test relies on live bytes determinism (none today), the wire will appear to break it.
3. **dual_stream.hexa inline LCG is intentional (raw#68).** It MUST NOT be wired through nexus at any stage. Byte-identical reproducibility there is a feature, not a candidate for refactor; the inline LCG is the SSOT for the synthetic stream and any swap to a "real" RNG (even a deterministic mock) would change the golden.

---

## 8. Next-cycle recommendation — **Stage 1 first, ranked #1 by 완성도 lens**

Priority order:

| rank | stage | rationale |
|---|---|---|
| **#1** | **Stage 1** (nexus provider IMPLEMENTED_real + xrepo smoke selftest) | provider must be real before anima delegates; smoke test is the only way to falsify caveat (1) — without it, Stage 2 builds on assumed-working wire. Highest 완성도 risk reduction per cycle cost. |
| #2 | Stage 2 (anima wrappers) | depends on Stage 1; biggest visible payoff (anima → nexus dependency wire actually live in code). |
| #3 | Stage 4 (roadmap cross-link) | parallelizable with Stage 2 once code-path evidence exists. |
| #4 | Stage 3 (router inline cleanup) | tech debt, not user-visible; defer. |

**1순위 추천 사유:** Stage 1 PASS converts the architectural decision into a falsifiable runtime gate. Without smoke test, anima could land Stage 2 wrappers that silently fall back to local execution because `use "nexus/..."` quietly fails to resolve and the loader's "" return path collapses to caller-relative not-found, manifesting as a confusing chain-fail at runtime rather than a build-time error. Stage 1 smoke test catches this in <1s.
