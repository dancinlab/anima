# Boundary: `qrng` (provider) vs `qmirror.qrng` (consumer drop-in)

> **Status**: API-surface dual-home, ZERO code overlap (audited 2026-05-04).
> **Risk class**: low — naming collision but disjoint scope.
> **Action**: this doc + cross-link in both READMEs; future qmirror v3+ may
> declare qrng as a runtime dependency to formally unify the entropy pipeline.

---

## TL;DR

| Repository | Surface | Role | LoC |
|------------|---------|------|-----|
| `qrng` (this) | `modules/{anu,curby,nist_beacon,hardware_qrng,mock_qrng}.hexa` + `modules/{registry,router,source,qrng_main}.hexa` | **Provider registry**: 5 backends + abstraction (interface contract / dispatch table / fallback chain / aggregator) | 1593 |
| `qmirror` | `modules/qrng.hexa` (single file) | **Consumer drop-in**: HMAC-DRBG amplifier API exposed as `qmirror qrng` subcommand | 193 |

They share:
- The `QrngBytes { ok, n_bytes, bytes_, sha256_hex, nist_pass, message }` **struct shape** (by convention; not a code import).
- The `QrngSourceMeta { name, tier, throughput_bps, cost_usd, lead_days, is_quantum, is_local, is_free, status, vendor }` **struct shape**.
- The `__QRNG_*__ PASS|FAIL` **sentinel naming convention** for selftest output.

They do NOT share:
- Module source code (verified: `diff -r` against any module pair → empty intersection).
- Runtime invocation paths (qmirror's `qrng.hexa` is invoked via `qmirror qrng <bits>`; this package's modules are invoked via `qrng collect/selftest/...` or directly via `hexa run modules/<backend>.hexa`).
- `_python_bridge` (this package has NONE — pure-hexa raw#9 STRICT; qmirror has 6 `_python_bridge/*.py` files for Aer / pyphi / IIT bridges, but `qmirror/modules/qrng.hexa` itself is also pure-hexa).

---

## Why the dual-home is intentional

`qmirror` was extracted first (2026-05-03 → v2.0.0) with `qmirror.qrng` as a
small, self-contained HMAC-DRBG amplifier so qmirror users could pull
"quantum-grade" entropy without taking a hard dependency on a separate
provider package. The 4-tier ANU fallback chain (paid → keyed → trial →
legacy → mock) was inlined into `qmirror/modules/qrng.hexa` for closure
condition cond.7 (ANU 4-tier QRNG fallback).

When the **phase 2 audit** (anima cycle, `2026-05-04`) re-examined the nexus
module landscape, `nexus/modules/qrng/` (5-source provider registry, 1047 LoC)
ranked #7 of 9 candidates with score 7/10 — broadly reusable but more
elaborate than qmirror's slim drop-in. Folding it into qmirror would have
inflated qmirror's module count and forced a v3.0.0 SemVer bump for unrelated
consumers (anima-physics / anima-eeg / sim-universe). Keeping it standalone:

1. **Preserves qmirror v2.x SemVer stability** — qmirror does not need to
   absorb the 5-source registry to remain functional; its inline 4-tier ANU
   path keeps working unchanged.
2. **Lets non-qmirror consumers use qrng directly** — `anima-physics/esp32`,
   `anima-eeg`, `sim-universe/modules/godel_q` can pull entropy without
   pulling the entire qmirror substrate (which carries Aer / pyphi / Cirq).
3. **Opens the v3.0.0 path** — when qmirror v3 ships, it can `[dependencies]
   qrng = "^1.0.0"` and replace its inline `qmirror/modules/qrng.hexa` with a
   shellout to the standalone, eliminating the duplication entirely.

---

## Falsifier: when does dual-home break?

The dual-home is **safe** as long as:

- **F-DUAL-1** (struct compatibility): the `QrngBytes` and `QrngSourceMeta`
  field sets in qmirror and qrng remain identical (same field names, types,
  ordering). Validated by both packages declaring them locally — no shared
  import means no transitive break, but a divergence would silently break
  consumers that interchange them. **Mitigation**: both repos snapshot the
  struct definitions in their respective `modules/source.hexa` (qrng) and
  `modules/qrng.hexa` (qmirror) docstrings; PR review on either side flags a
  shape change.

- **F-DUAL-2** (sentinel uniqueness): qmirror emits `__QMIRROR_QRNG__ PASS`;
  qrng emits `__QRNG_MOCK_QRNG__`, `__QRNG_ANU__`, etc. **Different
  prefixes** (`__QMIRROR_*` vs `__QRNG_*`) — no collision possible.
  Mitigation: documented sentinel namespace per package.

- **F-DUAL-3** (env var collision): qmirror uses `NEXUS_QMIRROR_*` (legacy)
  + `QMIRROR_*` (forward) prefixes. qrng uses `NEXUS_QRNG_*` (legacy) +
  `QRNG_*` (forward) prefixes plus `ANIMA_QRNG_MOCK` (anima consumer alias).
  Distinct namespaces; no collision. Mitigation: documented env var
  namespace per package; CI greps for cross-namespace leakage.

If any of F-DUAL-1/2/3 fails in a future cycle, the boundary becomes a real
break and qmirror v3.0.0 must take qrng as a hard dependency to consolidate
the surface.

---

## Migration path: qmirror v3.0.0 → qrng dependency

When qmirror cuts v3:

1. Add `[dependencies] qrng = "^1.0.0"` to `qmirror/hexa.toml`.
2. Replace `qmirror/modules/qrng.hexa` body with a shellout to
   `qrng collect --bytes <N>` + HMAC-DRBG amplifier wrapper preserved.
3. Bump qmirror to `3.0.0` (consumers that import `qmirror/modules/qrng.hexa`
   directly need to update their code path; pure CLI consumers
   `qmirror qrng <bits>` are unaffected).
4. Deprecate the inline 4-tier ANU implementation; migrate to
   `qrng collect --source=anu`.

This consolidation is **NOT scheduled** for the current cycle — qrng v1.0.0
ships standalone first, and qmirror v3 dependency wire-up is deferred until
non-qmirror consumers (anima-physics / anima-eeg / sim-universe) stabilize on
the qrng API.

---

## Provenance

- Audit doc: `anima/state/nexus_module_extraction_audit_phase2_2026_05_04/audit.json#qrng`
- Sister extractions: qmirror v2.0.0 (2026-05-03), sim-universe v1.0.0 (2026-05-03), hexa-bio v1.0.0, honesty-monitor v1.0.0, anima-agent v1.0.0
- Phase 1 audit destination decision: `extract_standalone_qrng_repo_with_caveats` (verdict, score 7)

---

*This document is the authoritative source for the qrng/qmirror.qrng boundary.
Cross-linked from `qrng/README.md` "Boundary" section and (planned) from
`qmirror/README.md` v2.1+ when qmirror documents its qrng-future-dep.*
