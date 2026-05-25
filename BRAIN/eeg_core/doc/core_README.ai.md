---
schema: anima-eeg-core/_core/ai-native/1
last_updated: 2026-05-02
ssot:
  integration_test:   anima-eeg-core/tool/modules/_core/_integration_test.hexa
  npy_loader:         anima-eeg-core/tool/modules/_core/npy_loader.hexa
  filter_pipeline:    anima-eeg-core/tool/modules/_core/filter_pipeline.hexa
  falsifier_runner:   anima-eeg-core/tool/modules/_core/falsifier_runner.hexa
  jsonl_audit:        anima-eeg-core/tool/modules/_core/jsonl_audit.hexa
  chflags_lock:       anima-eeg-core/tool/modules/_core/chflags_lock.hexa
  eeg_export:         anima-eeg-core/tool/modules/_core/eeg_export.hexa
  pipeline_suggester: anima-eeg-core/tool/modules/_core/pipeline_suggester.hexa
  adapter:            anima-eeg-core/tool/modules/_core/_adapter.hexa
roadmap_entry: 270
---

# anima-eeg-core core modules (AI-native)

Phase 1 anima-eeg-core foundation — npy ingest, notch+bandpass filtering, falsifier runner against bound specs, jsonl audit ledger, chflags-lock immutability, eeg export, pipeline suggester, and a venv adapter. The substrate that paradigm + gate + metric + artifact + integration modules are layered on.

## TL;DR for an agent reading this cold

- **9 files**: 6 core utilities + 1 adapter + 1 export + 1 integration test. 200-560 LOC each (substantive).
- **Mini-pipeline** order: `npy_loader → filter_pipeline → (re-load filtered) → falsifier_runner → jsonl_audit → chflags_lock`.
- `_adapter.hexa` (473 LOC) is the venv-eeg / BrainFlow adapter — wraps the `.venv-eeg/bin/python` host call.
- `pipeline_suggester.hexa` (564 LOC) — recommends filter + gate chain based on input characteristics.

## Architecture map

```
anima-eeg-core/tool/modules/_core/
├── _integration_test.hexa     mini-pipeline runner (Phase 1)
├── _adapter.hexa              venv-eeg / BrainFlow Python adapter (473 LOC)
├── npy_loader.hexa            .npy v1.0 reader + sha256 emit (290 LOC)
├── filter_pipeline.hexa       notch (60 Hz) + bandpass (0.5-45 Hz) (322 LOC)
├── falsifier_runner.hexa      eval metrics against bound specs (245 LOC)
├── jsonl_audit.hexa           structured audit row emit (276 LOC)
├── chflags_lock.hexa          macOS chflags uchg lock/unlock (244 LOC)
├── eeg_export.hexa            .npy → CSV / EDF / BIDS export (393 LOC)
└── pipeline_suggester.hexa    recommend filter+gate chain (564 LOC)
```

## API contract

```hexa
// npy_loader.hexa
fn load_npy(path: string) -> (data: [[float]], sha256: string, shape: (int, int))

// filter_pipeline.hexa
fn notch(data: [[float]], fs: int, freq_hz: int) -> [[float]]
fn bandpass(data: [[float]], fs: int, low: float, high: float) -> [[float]]
fn apply_chain(data: [[float]], fs: int, chain: [FilterStep]) -> [[float]]

// falsifier_runner.hexa
fn eval_against_spec(metrics: Metrics, spec_path: string) -> FalsifierResult
// → {passed: bool, falsifiers_failed: [string], evidence: [...]}

// jsonl_audit.hexa
fn emit_row(ledger_path: string, row: AuditRow) -> bool

// chflags_lock.hexa
fn lock(path: string) -> bool       // macOS: chflags uchg
fn unlock(path: string) -> bool     // macOS: chflags nouchg

// eeg_export.hexa
fn export_csv(npy_path: string, out_path: string) -> bool
fn export_edf(npy_path: string, out_path: string, channel_names: [string]) -> bool

// pipeline_suggester.hexa
fn suggest_chain(input_meta: InputMeta) -> SuggestedPipeline
// → recommended {notch, bandpass, gates[], metrics[]}
```

## Invocation patterns

```bash
# Mini-pipeline integration test
hexa run anima-eeg-core/tool/modules/_core/_integration_test.hexa

# Standalone npy load + sha
hexa run anima-eeg-core/tool/modules/_core/npy_loader.hexa --input data/raw.npy

# Filter chain
hexa run anima-eeg-core/tool/modules/_core/filter_pipeline.hexa \
  --input raw.npy --fs 250 --notch 60 --band 0.5,45 --output filtered.npy

# Lock audit ledger
hexa run anima-eeg-core/tool/modules/_core/chflags_lock.hexa --lock state/audit.jsonl
```

## Failure cascade

```
npy_loader.fail (header magic mismatch)
  → filter_pipeline never invoked
       → integration_test exits 1, audit row emits status=LOAD_FAIL
```

```
filter_pipeline.fail (NaN propagation from upstream board glitch)
  → falsifier_runner sees all-NaN metrics → all falsifiers fail
       → jsonl_audit logs ALL_FALSIFIERS_FAIL, integration exits 1
```

```
chflags_lock.fail (non-macOS host)
    Linux hosts get noop with WARN log
```


2. **`.venv-eeg/bin/python` SDK dependency.** `_adapter.hexa` shells out to a venv Python with BrainFlow installed. If venv missing, BrainFlow paths fail (mock fallback in selftest).
3. **Transient `/tmp/anima_eeg_core_phase1_integration/` not persisted.** Re-run regenerates. Don't expect ledger continuity across host reboots — emit to `state/` for permanent rows.
4. **NPY loader v1.0 only.** v2.0 / v3.0 npy headers (long magic, fortran order=True) not supported.
5. **Pipeline suggester is heuristic.** 564 LOC of empirical rules — not learnt; outputs are advisory, always cross-check with falsifier_runner output.
6. **Notch filter assumes 60 Hz mains.** EU 50 Hz hosts must pass `--notch 50`. No auto-detection.
7. **Audit ledger sha-pinning is row-level.** No prev-row chain hash → tampering is detectable per-row but not as ledger.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `_adapter.hexa` | `d9b2b0daacd8f6139c32204586d8280b035f016a21ceb879ee5639928aa28811` | 473 |
| `_integration_test.hexa` | `74f443af64c2533c10b060fd177cb1396e0af54229a8d47ff5a910b2794ccbe4` | 201 |
| `chflags_lock.hexa` | `6772142f0cc04059160094fd7d0fb9d474d3ac440c7c42013f06c8b4774f84de` | 244 |
| `eeg_export.hexa` | `49c28f072bc9568db23e5096868329fa22799eb9ee1ab6bfd64e53565c82f735` | 393 |
| `falsifier_runner.hexa` | `4a2359027797c8c424206b024f2c57fd8481ee0d3e7ccdeb2dee574c593cf8c9` | 245 |
| `filter_pipeline.hexa` | `fe75313caf103965d2b38f769fc7c6c638e50e04804d55d09af499d7905bf410` | 322 |
| `jsonl_audit.hexa` | `875ba003ab822cd078de9ffdeadafb9fe85fc488915a161e5bd93ca6da8a1a26` | 276 |
| `npy_loader.hexa` | `d79a77a2fe0a63a028fddb637a871d2c0672b5a2f2b74e04b754208b3fa11f69` | 290 |
| `pipeline_suggester.hexa` | `e81e71674e1e40efd09c6dc6be8b94f26832e5503f5c9ca6f3b90f1048b1a90f` | 564 |

shas pinned 2026-05-02.
