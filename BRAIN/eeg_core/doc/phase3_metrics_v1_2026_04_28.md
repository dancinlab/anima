# anima-eeg-core Phase 3 — `_metrics/` v1 (2026-04-28)

Phase 3 lands the first 4 of 10 planned `_metrics/` kernels:
`lz76`, `gamma_theta`, `permutation_entropy`, `hjorth`.


**DECISION: WRAP all 4** — thin wrappers around frozen `anima-clm-eeg/tool/`
verifiers (commit `ef3efeb09` frozen). Re-implementation deferred until
Phase 5 port (own4 root-cause-only would surface a real reason to port,

| Module | Backend (legacy, frozen) | LoC (wrapper) | LoC (legacy) |
|---|---|---|---|
| `lz76.hexa` | `clm_eeg_lz76_real.hexa` | ~210 | 1055 |
| `gamma_theta.hexa` | `clm_eeg_gamma_theta_ratio.hexa` | ~210 | 718 |
| `permutation_entropy.hexa` | `clm_eeg_pe_real.hexa` | ~210 | 562 |
| `hjorth.hexa` | `clm_eeg_hjorth_real.hexa` | ~220 | 534 |

The Phase 2 `_gates/` modules (`pe_saturation.hexa`, `hjorth_band.hexa`)
are **NOT replaced** by the metric modules — gates emit only PASS/FAIL
binary verdicts; metrics surface the underlying numeric descriptors and

## Module API — kv-block convention (Phase 1 reconcile)

All 4 modules expose a hermetic `_metric_<name>_kv(npy_path, sidecar_kv)`
function returning a kv-block:

```
schema=anima-eeg-core/_metrics/<name>/1
metric=<name>
npy_path=<path or empty for selftest>
sidecar_kv=<csv kv pairs>
value_x1000=<int>          # canonical numeric (LZ b(n), ratio, PE, complexity)
verdict=<PASS|FAIL|FALSIFIED|PARTIAL>
backend=<legacy_path>
backend_rc=<int>
raw71_falsifier_count=3
raw71_triggered_count=<int>
raw71_triggered_ids=<csv>
raw91_evidence=<...>
raw91_limit=<...>
raw95_enforce_layer=in_module
```

Per-module extras (e.g. `c_n` for LZ76, `occipital_ratio_x1000` for
gamma_theta) are emitted alongside `value_x1000`.

### Adapter shim — legacy stdout parser

The wrappers exec their legacy backend via `exec_with_status` and parse
the pretty-printed stdout (lines like `  PE mean overall x1000 = 999`)
using a back-scan parser that captures the trailing digit run on the
marker line. This handles labels with embedded digits (`lz76`, `log10`)
without regex.

## Raw#71 Falsifiers (preregistered, frozen 2026-04-28)

Each module preregisters ≥3 falsifiers. Verdict `FALSIFIED` iff any
trigger fires.

| Module | F_*01 | F_*02 | F_*03 |
|---|---|---|---|
| lz76 | c_n ≤ 1 | norm_x1000 < 100 | norm_x1000 > 1500 |
| gamma_theta | ratio < 1.0 | ratio > 10 | occipital < frontal |
| permutation_entropy | pe < 0.10 | pe > 0.99 | sentinel (helper-fail) |
| hjorth | cpx < 0.8 | cpx > 2.5 | mobility ≤ 0 |

## Selftest Results

| Module | Mode | Computed | Falsifiers | Verdict |
|---|---|---|---|---|
| lz76 | random (256-bit) | c_n=39, b(n)_x1000=1218 | 0 | PASS |
| gamma_theta | synthetic_3 | ratio=2.973, occ=3.728, fro=2.865 | 0 | PASS |
| permutation_entropy | white | pe=0.999 | F_PE_02 (>0.99 saturation) | FALSIFIED ✓ intentional |
| hjorth | white | cpx=1.225, mob=1.414 | 0 | PASS |

PE selftest **correctly** triggers F_PE_02 — white noise saturates PE
near 1.0 by Bandt-Pompe construction. The integration test treats
`FALSIFIED` as a contract-PASS (kv-block honored) since the falsifier
fired *as designed*.


In `anima-eeg-core/tool/eeg_core.hexa`, the `metric` verb now routes:

| Verb / Noun | Backend | Status |
|---|---|---|
| `metric lz76` | `_metrics/lz76.hexa` | landed |
| `metric pe` | `_metrics/permutation_entropy.hexa` | landed |
| `metric hjorth` | `_metrics/hjorth.hexa` | landed |
| `metric gamma_theta` | `_metrics/gamma_theta.hexa` | landed |
| `metric gamma-theta` | `_metrics/gamma_theta.hexa` | landed (alias) |
| `metric berger` | legacy `clm_eeg_berger_sanity.hexa` | legacy (Phase 4) |
| `metric all` | composite | pending (Phase 4) |

Dispatcher selftest: `eeg_core selftest` → 4/4 PASS.
Dispatcher list summary: landed=20 legacy=29 pending=2 total=51.

## Integration Test

`anima-eeg-core/tool/modules/_metrics/_integration_test.hexa` runs all
4 modules in selftest mode + verifies kv-contract (schema, verdict,
value_x1000 emitted) + appends a JSONL audit row per module to
`state/anima_eeg_core_phase3_metrics_integration_audit.jsonl`.

**Verdict: PHASE3_METRICS_INTEGRATION_PASS** (4/4 contract PASS;
selftest verdicts: PASS/PASS/FALSIFIED-intentional/PASS).

real-data .npy compute on Mac. Real-data verification is delegated to
the host run (e.g. `bin/eeg metric lz76 --input <npy>` invoked
manually after worktree merge to host).

## RAW Compliance

| RAW | Compliance |
|---|---|
| #9 hexa-only | All 4 modules + integration test pure hexa |
| #10 honest C3 | Wrap-vs-port decision documented; selftest classifies synthetic |
| #12 silent-error-ban | Helper-fail → sentinel `-2147483647` → verdict=FAIL |
| #18 self-host fixpoint | Reuse legacy frozen verifiers via wrapper shim |
| #42 mac-zero-compute | Heavy compute delegated to legacy backend's host venv |
| #65 idempotent | All modules re-runnable; backend is deterministic |
| #71 falsifier ≥3 | 3 falsifiers preregistered per module |
| #82 darwin | `.venv-eeg/bin/python` resolver-bypass declared |
| #91 honest triad | `raw91_evidence` + `raw91_limit` emitted in kv-block |
| #95 triad-universal | `raw95_enforce_layer=in_module` emitted in kv-block |
| #137 80% Pareto | Phase 3 first batch covers 4/10 of planned metrics |

## Out-of-scope (Phase 4+)

- 6 remaining metric modules: `dmn_coherence`, `frontal_asymmetry`,
  `spectral_entropy`, `change_points`, `berger_alpha_metric` (gate→metric
  promotion), `composite_metric_all`.
- Phase 4 will land `pipeline standard` (gate→metric→audit composite).
- Phase 5 may port (re-implement) any metric whose legacy backend
  exhibits drift vs. own3 SSOT — not yet observed.
