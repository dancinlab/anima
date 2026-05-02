---
schema: anima-eeg-core/_hw/ai-native/1
last_updated: 2026-05-02
ssot:
  integration_test: anima-eeg-core/tool/modules/_hw/_integration_test.hexa
  audit_ledger:     state/anima_eeg_core_phase5_hw_integration_audit.jsonl
  impedance_ledger: state/anima_eeg_impedance_ledger.jsonl
status: live — Phase 5 hardware operations; 5 modules + 1 integration; mock fallback in selftest
roadmap_entry: 270
raws:
  - raw#9 hexa-only
  - raw#42 mac-local-USB-only
  - raw#65 idempotent
  - raw#71 falsifier ≥3 per module
  - raw#77 audit-jsonl emit
  - raw#91 honest triad
  - raw#137 80% Pareto
---

# anima-eeg-core hardware modules (AI-native)

Phase 5 hardware operations — board health probe, impedance check, electrode adjustment, head-plot rendering, and recording driver. All modules expose **mock** mode (selftest) and **real** mode (USB FTDI dongle, mac-local-only per raw#42).

## TL;DR for an agent reading this cold

- **6 files**: 5 hardware ops + 1 integration test.
- **Selftest = mock mode** — uses legacy backend's synthetic / mock path. No real hardware required. Phase 5 mac-zero-compute compliant.
- **Real mode** = USB FTDI dongle + Cyton (+ Daisy 8-or-16ch). raw#42 mac-local-USB-only.
- Run individual modules via `bin/eeg hw <op> --check` for real-HW verification (per-module live probes).
- Audit ledger: `state/anima_eeg_core_phase5_hw_integration_audit.jsonl` + per-impedance row in `state/anima_eeg_impedance_ledger.jsonl`.

## Architecture map

```
anima-eeg-core/tool/modules/_hw/
├── _integration_test.hexa     batch runner (Phase 5)
├── board_health.hexa          BrainFlow board probe + version check (312 LOC)
├── impedance.hexa             per-channel impedance check, append to ledger (297 LOC)
├── adjustment.hexa            electrode adjustment guidance (gain / referencing) (312 LOC)
├── headplot.hexa              topographic head-plot render → PNG (189 LOC)
└── recorder.hexa              session recorder → .npy v1.0 (314 LOC)
```

## API contract

```hexa
// board_health.hexa
fn probe_board(board: string) -> BoardHealth
// BoardHealth { connected: bool, sample_rate: int, channels: int, firmware: string, ... }

// impedance.hexa
fn check_impedance(channels: [int]) -> ImpedanceResult
// per-channel kΩ + verdict {GOOD: <5, OK: 5-10, POOR: 10-50, FAIL: >50}
// Appends row to state/anima_eeg_impedance_ledger.jsonl

// adjustment.hexa
fn suggest_adjustments(impedance: ImpedanceResult, target_metric: string) -> [Adjustment]
// → ordered remediation steps (re-gel, re-scrub, re-reference, swap electrode)

// headplot.hexa
fn render_topomap(metric_per_channel: [float], output_png: string) -> bool

// recorder.hexa
fn record_session(board: string, duration_s: int, output_npy: string) -> SessionMeta
```

## Invocation patterns

```bash
# Phase 5 batch (mock mode)
hexa run anima-eeg-core/tool/modules/_hw/_integration_test.hexa

# Real-HW probe
bin/eeg hw board_health --check
bin/eeg hw impedance --check --channels "1,2,3,4,5,6,7,8"

# Record real session
bin/eeg hw recorder --board cyton_daisy --duration 60 --output data/session.npy

# Render topomap
hexa run anima-eeg-core/tool/modules/_hw/headplot.hexa \
  --metric data/alpha_per_channel.json --output data/topomap.png
```

## Failure cascade

```
board_health.fail (USB dongle missing)
  → impedance / recorder fail-soft to mock mode if --selftest, else exit 1
       → adjustment suggests "check USB cable" as first remediation
            → headplot can still render from cached metric file
```

```
impedance.check_impedance → channel 7 = FAIL (>50 kΩ)
  → adjustment.suggest emits ["re-scrub channel 7", "re-gel", "swap electrode"]
       → ledger row pinned to state/anima_eeg_impedance_ledger.jsonl
            → operator iterates until impedance ≤ 10 kΩ
```

## raw#10 caveats

1. **Mac-local-USB-only.** raw#42 explicit. Linux / Windows hosts have no FTDI driver in this tree.
2. **Cyton + Daisy hardcoded** as primary board. Other BrainFlow boards (Ganglion / Synthetic / Muse) work via BrainFlow's BoardIds enum but are not selftest-covered.
3. **Impedance ledger append-only.** No row deletion. Use the latest row per channel (group-by channel, max timestamp) for "current" state.
4. **Adjustment suggestions are heuristic.** Empirical rules; not learnt. Operator judgment overrides.
5. **Headplot uses simple radial-basis interpolation** — not CSD / spherical spline. For publication-quality, use offline MNE / EEGLAB.
6. **Recorder emits .npy v1.0 only.** No streaming write. Long sessions (>30 min) buffer in RAM — OOM risk on small hosts.
7. **No SD card / external storage support.** Recorder writes to local fs only.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `_integration_test.hexa` | `2d177e3d9645bb440f3a2327626b4cfbd45192ca322e11d04d3bd16815ed2f10` | 169 |
| `adjustment.hexa` | `7427cf7e0f7719c15e7f30c244f4e21cdd68f1bdeac2b401d59f84a0c2e857a8` | 312 |
| `board_health.hexa` | `fa1c32daaefe1e2cab0e19281ae5be3ea41f9d874bc94eb287dceb247fe15d9f` | 312 |
| `headplot.hexa` | `4acc600a82adf557ee9330bd8fb43311a8f1d32001f47f38eaa41813096a0b7f` | 189 |
| `impedance.hexa` | `8f4b5e5bf63cd472a675262d7f33ff895448828ab3e757badcb5b26894e6a76b` | 297 |
| `recorder.hexa` | `b44833d55c694c8d55ef2148c521a4635e3c66f124bdf19fe5d3f3026056deb7` | 314 |

shas pinned 2026-05-02.
