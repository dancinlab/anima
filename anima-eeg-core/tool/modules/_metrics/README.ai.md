---
schema: anima-eeg-core/_metrics/ai-native/1
last_updated: 2026-05-02
ssot:
  integration_test: anima-eeg-core/tool/modules/_metrics/_integration_test.hexa
  audit_ledger:     state/anima_eeg_core_phase3_metrics_integration_audit.jsonl
status: live — Phase 3 EEG metric suite; 14 modules; selftest synthetic short-window
roadmap_entry: 270
raws:
  - raw#9 hexa-only
  - raw#42 mac-zero-compute
  - raw#65 idempotent
  - raw#71 falsifier ≥3 per module
  - raw#77 audit-jsonl emit
  - raw#91 honest triad
  - raw#137 80% Pareto
---

# anima-eeg-core metrics modules (AI-native)

Phase 3 EEG metric suite — Lempel-Ziv complexity, Hjorth (activity/mobility/complexity), permutation entropy, gamma/theta ratio, frontal asymmetry, α-band coherence, α-phase PLV, DMN coherence, change points, spectral entropy, plus a high-throughput chunked + native LZ76 path.

## TL;DR for an agent reading this cold

- **14 files**: 13 metric modules + 1 integration test. ~150-860 LOC each.
- Integration test exercises **4 core metrics** (lz76 / gamma_theta / permutation_entropy / hjorth) for kv-block contract; remaining 9 are individually selftested.
- Three LZ76 variants: `lz76.hexa` (283 LOC, basic) / `lz76_chunked.hexa` (638 LOC, sliding window) / `lz76_native.hexa` (856 LOC, hexa-native, fastest, replaces py harness per project_omega_rules_compliance Phase 5).
- Audit ledger: `state/anima_eeg_core_phase3_metrics_integration_audit.jsonl` + per-metric ledgers (`state/clm_eeg_*_audit/`).
- raw#42 mac-zero-compute: selftest uses synthetic short-window inputs; real-data via `bin/eeg metric <name> --input <npy>` on host.

## Architecture map

```
anima-eeg-core/tool/modules/_metrics/
├── _integration_test.hexa         Phase 3 batch (4-metric kv-block contract)
│
├── COMPLEXITY (3 LZ76 variants)
│   ├── lz76.hexa                  (283 LOC, basic)
│   ├── lz76_chunked.hexa          (638 LOC, sliding window)
│   └── lz76_native.hexa           (856 LOC, hexa-native, fastest)
│
├── ENTROPY (2)
│   ├── permutation_entropy.hexa   (254 LOC, m+τ)
│   └── spectral_entropy.hexa      (389 LOC)
│
├── HJORTH + ASYMMETRY (2)
│   ├── hjorth.hexa                (258 LOC, activity/mobility/complexity)
│   └── frontal_asymmetry.hexa     (389 LOC, F3-F4 α-asymmetry)
│
├── BAND POWER (1)
│   └── gamma_theta.hexa           (258 LOC, ratio)
│
├── COHERENCE / PLV (4)
│   ├── alpha_coherence.hexa       (467 LOC, Welch)
│   ├── alpha_phase_plv.hexa       (387 LOC, Hilbert PLV)
│   ├── dmn_coherence.hexa         (393 LOC, RSN topology)
│   └── plv_preserving.hexa        (439 LOC, surrogate-preserving)
│
└── CHANGE DETECTION (1)
    └── change_points.hexa         (418 LOC, online + offline)
```

## API contract

```hexa
// Per metric module (uniform contract):
fn compute_<metric>(npy_path: string, fs: int, args: <MetricArgs>) -> MetricResult
// MetricResult { value: float | [float], evidence: {...}, falsifiers_passed: [int] }
fn run_selftest() -> (ok: bool, summary: string)

// _integration_test.hexa runs lz76 / gamma_theta / permutation_entropy / hjorth
//   in selftest mode and verifies the kv-block contract:
//     __METRIC_LZ76__               PASS lz=N c_norm=...
//     __METRIC_GAMMA_THETA__        PASS ratio=...
//     __METRIC_PERMUTATION_ENTROPY__ PASS pe=... m=4 tau=1
//     __METRIC_HJORTH__             PASS activity=... mobility=... complexity=...
```

## Invocation patterns

```bash
# Phase 3 batch (4-metric integration)
hexa run anima-eeg-core/tool/modules/_metrics/_integration_test.hexa

# Real-data per metric
bin/eeg metric lz76_native --input data/recorded.npy --fs 250
bin/eeg metric alpha_coherence --input data/recorded.npy --pair "O1,O2"
bin/eeg metric permutation_entropy --input data/recorded.npy --m 4 --tau 1

# Selftest single metric
hexa run anima-eeg-core/tool/modules/_metrics/lz76_native.hexa --selftest
```

## Failure cascade

```
_core/composite_gate FAIL upstream
  → metric runners can still execute, but raw#10 honest:
       outputs are uninterpretable; audit row emits gate_passed=false flag
            → downstream consumer must check gate_passed before trusting metric
```

```
lz76_native NaN propagation (input contains NaN samples)
  → compute returns lz=-1, falsifier F1 (NaN-in) fails
       → integration test detects, batch FAIL, ledger row captures sha
```

## raw#10 caveats

1. **3 LZ76 variants** — `lz76_native.hexa` is canonical (project_omega_rules_compliance Phase 5: 390 LOC python harness ported to 390 LOC hexa-native, 6-digit equivalence). Use `lz76.hexa` for portability, `lz76_chunked.hexa` for streaming, `lz76_native.hexa` for production.
2. **α-band hardcoded 8-12 Hz.** Older studies use 8-13. Override via `--band 8,13` per module.
3. **Permutation entropy m=4, τ=1 default.** m+τ tuning matters — tested for fs=250 only.
4. **Coherence uses Welch NFFT=512** (4-bin α resolution). 8-12 Hz band-mean from 4 bins is a known accuracy floor (see project_eeg_config_r33_update raw#10).
5. **Hilbert PLV requires bandpass first.** Run `_core/filter_pipeline.hexa --band 8,12` upstream.
6. **Frontal asymmetry F3-F4 hardcode.** Other electrode pairs need source edit.
7. **DMN coherence assumes 8-channel minimum** (Cyton 8ch). Cyton-Daisy 16-ch preferred for spatial decomposition.
8. **Change points online mode is causal-only.** Offline mode allows look-ahead — toggle via `--offline`.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `_integration_test.hexa` | `60b37b07df3b0717fbbb5cefe13938118563d1c1fb8ee849d719a34d4a2dc052` | 167 |
| `alpha_coherence.hexa` | `cef22e51cbef9b5bc6f5561ecb40dcfd2731371efaff51662a000d1cd195324d` | 467 |
| `alpha_phase_plv.hexa` | `918cd37a3e3f9035270ffc267a61c5f9ae39bdc41e85dd87cda6f33db32dc56f` | 387 |
| `change_points.hexa` | `397f68376ac95f5fc38d776f07bded8a1ba150d6b37ad9d79c0b12d2a95f80f6` | 418 |
| `dmn_coherence.hexa` | `d82e7bda8b3d56c17d09221db069a50cc73d6c24dbbe23c8fe0872d47572e321` | 393 |
| `frontal_asymmetry.hexa` | `b23f48060227cdb3d6d7c8ab3984d647f77284371da61b1c5545cff5212522a2` | 389 |
| `gamma_theta.hexa` | `e5e6792d78f710404b0c9d956df9171b413adaff0fa494c576e1e0d771c2dbb8` | 258 |
| `hjorth.hexa` | `c375630f8f7c2565b1d0a78102da2332f0c6752bda82a0c3c414f28b7ef3d2e8` | 258 |
| `lz76_chunked.hexa` | `d5aa759193eb4a1c4dfb4874ae48331d6e6b88117c01106db7667812e833c6e3` | 638 |
| `lz76_native.hexa` | `3ede29de5e6a66ecbf9822b6f4dd6c5d762ef80b47204384dc9b54bd255acf70` | 856 |
| `lz76.hexa` | `fc1cf50c384890223fea95b3800d60ce7836c5047e64791be40fe72f705121d0` | 283 |
| `permutation_entropy.hexa` | `f65e3380ef3af02df08280b9a2883d871c5f4a0cfc282fe8d4dba04aa1c566e5` | 254 |
| `plv_preserving.hexa` | `d4e43cd6f340b19e2a95d147aaa8f839ba9d2fc7214f79cd23ebb860fcb2235f` | 439 |
| `spectral_entropy.hexa` | `5e4c75b8bfb9fc5c7765d6c5f9ce3e85bb0537ce4bd10108905a533691f875b4` | 389 |

shas pinned 2026-05-02.
