---
schema: anima/ready/modules/eeg/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:        ready/anima/modules/eeg/eeg.hexa
  collect:      ready/anima/modules/eeg/collect.hexa
  experiment:   ready/anima/modules/eeg/experiment.hexa
  realtime:     ready/anima/modules/eeg/realtime.hexa
  closed_loop:  ready/anima/modules/eeg/closed_loop.hexa
  validate:     ready/anima/modules/eeg/validate_consciousness.hexa
  config:       anima/config/eeg_config.json   # SSOT brain_like_target=0.856
status: stub-tier (Phase 4b 18-file group); compare with anima-eeg-core/tool/modules/_* (live)
roadmap_entry: 270
related:
  - anima-eeg-core/tool/modules/_paradigms (live paradigm runners)
  - anima-eeg-core/tool/modules/_core      (filter / loader / audit pipeline)
---

# anima eeg modules (AI-native)

EEG consciousness validation surface. 18 stub files covering collection (BrainFlow ingest), real-time analysis, closed-loop neurofeedback, dual-stream Φ-α correlation, multi-protocol experiments, and consciousness validation against anima/config/eeg_config.json target metrics.

## TL;DR for an agent reading this cold

- **18 files**, all stub-tier (12-59 LOC range). Phase 4b 7/9 group with closed-loop + dual-stream upgraded to wrapper-complete (project_anima_eeg_phase4_cycle9_10).
- Live EEG runtime is in **anima-eeg-core/tool/modules/_*/** (separate dir; 7 sub-groups: paradigms / core / gates / artifact / integrations / hw / metrics). This `ready/` tree is the namespace anchor.
- 5 functional sub-groups: **collection** (3) / **analysis** (3) / **realtime** (4) / **protocols** (5) / **bridges** (2).
- Brain-likeness target: **85.6 %** (`brain_like_pct=0.856`), pinned in `anima/config/eeg_config.json` SSOT (validate.hexa BRAIN_LIKE_TARGET=0.856 cross-link verified).

## Architecture map

```
ready/anima/modules/eeg/
├── eeg.hexa                       namespace + EegMetrics + EegSession
├── collection/
│   ├── collect.hexa               BrainFlow ingest → .npy v1.0
│   ├── eeg_recorder.hexa
│   └── calibrate.hexa
├── analysis/
│   ├── analyze.hexa
│   ├── validate_consciousness.hexa  brain_like_pct check vs config target
│   └── experiment.hexa
├── realtime/
│   ├── realtime.hexa
│   ├── neurofeedback.hexa
│   ├── dual_stream.hexa            Φ ↔ α-band correlation (pearson_r)
│   └── closed_loop.hexa            BCI control loop
├── protocols/
│   ├── emotion_sync.hexa
│   ├── multi_eeg.hexa
│   ├── sleep_protocol.hexa
│   ├── bci_control.hexa
│   └── __init__.hexa
└── bridges/
    └── transplant_eeg_verify.hexa
```

## API contract

```hexa
struct EegMetrics {
    lempel_ziv:     float,
    hurst:          float,
    psd_slope:      float,
    autocorr_decay: float,
    critical_exp:   float,
    brain_like_pct: float    // target 0.856 per config SSOT
}

struct EegSession {
    board:       string,    // "cyton_daisy" | "synthetic"
    channels:    int,       // 16 for cyton-daisy
    sample_rate: int,       // 250 Hz typical
    steps:       int,
    metrics:     EegMetrics
}

pure fn metrics_default() -> EegMetrics
// Per stage:
fn collect(board: string, duration_s: int) -> EegSession
fn analyze(npy_path: string) -> EegMetrics
fn validate(metrics: EegMetrics) -> bool   // metrics.brain_like_pct >= 0.856 - tolerance
```

## Invocation patterns

```bash
# Synthetic 60s collect (no HW)
hexa run ready/anima/modules/eeg/collect.hexa --board cyton_daisy --duration 60

# Run experiment (resting / alpha / anima 4-phase / meditation protocols)
hexa run ready/anima/modules/eeg/experiment.hexa --protocol resting

# Live real-data (anima-eeg-core path; this tree is stub)
hexa run anima-eeg-core/tool/modules/_paradigms/resting_baseline.hexa --live
```

## Failure cascade

```
collect.fail (BrainFlow disconnect)
  → analyze receives empty .npy
      → validate emits brain_like_pct=0.0 → FAIL gate
```

```
realtime.fail (closed-loop dropout)
  → dual_stream Φ-α pearson undefined (n<min_samples)
      → closed_loop falls open (no neurofeedback signal)
```

## raw#10 caveats

1. **Stub vs live duality.** This `ready/anima/modules/eeg/` tree is the namespace; the live runtime is `anima-eeg-core/tool/modules/_*/`. Don't confuse — wrapper-complete files (closed_loop / dual_stream / experiment / collect / calibrate / realtime) here are 25-30 LOC stubs, the real implementations are 800+ LOC and live in anima-eeg-core.
2. **brain_like_pct=85.6** is the SSOT target (4-way alignment: validate.hexa + eeg.hexa + README + config.json — verified 2026-04-26). If you change the target, sync all 4 anchors.
3. **R33 α-coherence channel pair frozen = O1↔O2** (occipital, Berger 1929). See anima-clm-eeg/docs/eeg_arrival_impact_5fold.md §4.
4. **No Welch implementation here.** PSD/coherence is computed in `anima-eeg-core/tool/modules/_metrics/alpha_coherence.hexa` (real impl). The `ready/` tree references metric names but does not implement them.
5. **Protocols stub-only.** `protocols/multi_eeg.hexa` and `scripts/organize_recordings` are the 2 remaining stubs in the Phase 4 9/9 path (project_phase4_silent_land_audit_correction).
6. **No selftest.** Adding a `eeg_main.hexa` aggregator that walks all 18 stubs is recommended raw#10 debt.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `eeg.hexa` | `4b7ddff4f9e227bfa15f58259c5a8312edbb418db5d1bf55ff419a5d1e3319ab` | 59 |
| `__init__.hexa` | `888876a14ee63411f72f7dea08290f81590c1ef491133af15c60ca44feec4a50` | 19 |
| `analyze.hexa` | `3c629afa9e33bd35b2db5895cf4bfe4ae02c914ddaec3924f6ed800bce5a0549` | 32 |
| `calibrate.hexa` | `a2a60efb4119aab62195f8b9989a7c46c706fecc266d77b679bef1b3aba4c45b` | 23 |
| `closed_loop.hexa` | `22f1ebc2df75ac61adbe3e914b8a8405c43d9c4d455acdba67e57c518dfc91c9` | 29 |
| `collect.hexa` | `9b9893a7580ec46786b4a35163a65728d33980c0087d8753327784c8e1a2355d` | 25 |
| `dual_stream.hexa` | `d304a9862a40236b6b1743657024395f011637371584fb140bbe466340288dfe` | 25 |
| `eeg_recorder.hexa` | `acf2d15df677369fe2034ed8aff1a9771add93316782e9bb03430fcae870cb96` | 34 |
| `experiment.hexa` | `0ae2130288a8cd1349b8db710a5109e8c5506ac42bb88dfb6fed3a31f028ecab` | 30 |
| `neurofeedback.hexa` | `3bc12f4c4f47e7cef3413150bb771425fedc551b649e8330a8fdbe083abc9f01` | 30 |
| `realtime.hexa` | `de94f17ff1b8cd5c8940c839c0ba6ed73a62e3c79658e7eee23a782d76860d8f` | 29 |
| `transplant_eeg_verify.hexa` | `3cfa7ee3878b07c3dc751ae9a3f0fd0ba12495b2cc11553983217dc4dc5f4a08` | 20 |
| `validate_consciousness.hexa` | `8af03c2ba925192a080d4e75a6221377e37f676806c53d2c9905e295cee344fb` | 23 |
| `protocols/__init__.hexa` | `1be0f133044f96ba048f0e2ca6b2b012c45f2f82d4edccacffab4b89ca8b3b7a` | 12 |
| `protocols/bci_control.hexa` | `c2ce8c7770e123671eb61aa111ea2987ee5f59ceae2d1a444b0de536d1ca78b5` | 27 |
| `protocols/emotion_sync.hexa` | `d098dd4a42192fb718bff3304d5ec4bcdc00df75706ce8e740508bcc39bf8755` | 26 |
| `protocols/multi_eeg.hexa` | `8b732de7cd357fced041e9469f9d9ad0fe0d5f7fa2e9e913bef7c24b6bb3d0e7` | 26 |
| `protocols/sleep_protocol.hexa` | `ead77923d0f4a84d7dd647d5780e3678cb180f56009118fc16789c0164dde557` | 28 |

shas pinned 2026-05-02.
