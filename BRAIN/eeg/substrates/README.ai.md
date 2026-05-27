---
schema: hexa-brain/eeg/substrates/ai-native/1
last_updated: 2026-05-12
parent: eeg/README.ai.md
status: Phase 1 dispatch landed (commit `76494ad3`) — `eeg/collect.hexa` + `eeg/eeg_recorder.hexa` accept `--substrate <brainflow|synth|replay>` + `--legacy-inline`; default brainflow byte-identical. synth/replay run in pointer mode (`verdict=DEFERRED`). Phase 2 full BoardShim delegation deferred (HW regression required).
raws:
  - R9 hexa-only
  - R10 honest C3
  - R11 snake_case
  - R15 SSOT
  - R65 idempotent
  - R68 byte-identical selftests
  - R71 falsifier-bound
---

# hexa-brain/eeg/substrates (AI-native entry)

Substrate-agnostic interface (Sprint 1 Part E-1). **Phase 1 dispatch landed** (commit `76494ad3`, 2026-05-12) on top of the original foundation (commit `77484267`). One protocol surface, multiple backend modules. Lifecycle / open / close / read are uniform across `synth`, `brainflow`, `replay` so closed-loop and capture code can swap backends without forking.

## TL;DR for an agent reading this cold

- **Protocol declaration**: `substrate.hexa` — 11-method contract (`api_open_session`, `api_read_chunk`, `api_stim`, ...). Schema `hexa-brain/eeg/substrate/1`. Contract version pinned at `v0`.
- **Pure-data preset**: `channel_set.hexa` — `CYTON_DAISY_16` (10-20 labels, 2D ASCII coords from `eeg/headplot_helper.hexa:111-131`). `coords_3d: null` explicit stub (no 3D head-mesh source yet).
- **3 active backends**:
  - `synth_substrate.hexa` — deterministic LCG seed=1 (mirrors `eeg/closed_loop.hexa:72-74` constants A/C/M byte-identically). 16-ch × N float32. No BrainFlow dep.
  - `brainflow_substrate.hexa` — thin shim. Lifecycle (open/close/reinit/start/stop) delegates to `eeg/_session_manager.hexa`. New read-side (`api_read_chunk`, `api_get_eeg_indices`, `api_get_sample_rate`) built directly on `BoardShim`.
  - `replay_substrate.hexa` — disk `.npy` playback. Numpy-optional (handwritten parser fallback). Sidecar `.meta.json` for `sample_rate`.
- **Registry**: `registry.yaml` — per-backend `dep_id`, `coupling`, `tier`, `read_only`, `status`. Two declared-not-implemented entries: `nes` (AGPL-3.0, Part C-1) and `cl1` (CC-BY-NC-4.0, Part C-2).
- **Falsifiers**: `F_SUB_PROTO_01..03` (substrate.hexa), `F_SUB_01` (synth — shape/determinism/idempotent/stim-raises), `F_SUB_02` (brainflow — shim/stim-raises/idempotent), `F_SUB_03` (replay — shape/roundtrip/eof/close+stim/missing-path), `F_CS_01..03` (channel_set).

## Landing record

| # | Item | Status |
| --- | --- | --- |
| 1 | `eeg/collect.hexa` `--substrate` dispatch flag | ✅ Phase 1 (`76494ad3`) — default brainflow byte-identical (12/12 PASS); synth/replay = pointer mode (`verdict=DEFERRED`) |
| 2 | `eeg/eeg_recorder.hexa` `--substrate` dispatch flag | ✅ Phase 1 (`76494ad3`) — same surgery |
| 3 | `eeg/dual_stream.hexa:211` Phase-5 comment → replay_substrate pointer | ✅ Phase 1 (`76494ad3`) — comment updated; real `compare_streams_from_files` wrapper deferred (subprocess blocker) |
| 4 | Full inline BoardShim → `brainflow_substrate.api_open_session` delegation | ⏸ Phase 2 deferred — needs OpenBCI Cyton+Daisy + `.venv-eeg` regression |
| 5 | Nested `hexa run <substrate>.hexa` subprocess wiring (real delegation, not pointer) | ⏸ blocked by hexa-interp sandbox (`pwd=/tmp/resource-tcp-*` cwd isolation). Fix: shim exports `HEXA_PROJECT_ROOT`, or shim path-translation, or python3 direct invocation |
| 6 | `bin/hexa-brain` top-level `substrate` verb | ⏸ deferred — modules currently reachable via `hexa run eeg/substrates/<name>.hexa --selftest` |
| 7 | NES adapter (Part C-1) | ⏸ `status: declared-not-implemented` in `registry.yaml`. Needs user NES probe |
| 8 | CL1 adapter (Part C-2) | ⏸ same — CC-BY-NC-4.0 loose-coupling required |
| 9 | Contract version `v0` → `v1` semver-freeze | ⏸ gated on items 4 + 5 + 6 closure |


1. **`EXPECTED_DATA_ROWS=32` invariant only holds for `brainflow` substrate.**
   - `brainflow` returns 32 rows (timestamp + 16 EEG + aux) per BrainFlow native shape.
   - `synth` and `replay` return **16 rows** (EEG-only, no timestamp/aux row).
   - Code that assumes 32-row layout must be updated when migrating to `--substrate=synth|replay`. The `api_get_eeg_indices()` helper exists exactly to abstract this — callers should slice by `eeg_indices` instead of hard-coding row 0..31.
   - Open question for reviewer: should the spec dict declare expected `data_rows` and let downstream code branch? See "Open questions" in `design/substrate_abstraction.md`.
2. **`coords_3d: null` is a deliberate stub.** No 3D head-mesh anatomy is encoded anywhere in hexa-brain yet. The CYTON_DAISY_16 layout is 2D ASCII at character-grid resolution (col,row in an 80×20 plot), tuned for terminal viz NOT anatomy.
3. **`api_stim` is NotImplementedError on all three active substrates.** Scalp EEG is read-only by definition. Synth has no stim hardware. Replay is read-only playback. The CL1 (Cortical Labs) substrate in Part C-2 is the slot where `api_stim` will become a first-class implementation.
4. **Synthetic EEG is not biologically meaningful.** `synth_substrate` emits LCG-driven uniform noise in [-50µV, +50µV). No alpha/beta/gamma structure, no inter-channel correlation, no artifacts. Suitable for protocol shape testing and round-trip determinism — not for any analysis whose output is interpreted as physiology.
5. **`brainflow_substrate` selftest is DEGRADED tier.** Without a real Cyton+Daisy board (and without the BrainFlow synthetic board's runtime) it can only assert lifecycle shape + delegated method existence. F_SUB_02 PASSes via a fallback shim — green marker does NOT imply hardware is connected.
6. **License-posture binding to firewall (Part A) is operational.** `registry.yaml` declares `dep_id` and `coupling` fields. `bin/check_licenses.sh` (commit `77484267` Part A) is now shipped and runs as `hexa-brain license-check`; latest scan is 205 files / 0 violations / 3/3 falsifiers (F_LF_01..03) green. `registry.yaml` consumption by the check script is the next-step item — current scan walks `eeg/`/`eeg_core/`/`core/`/`tool/` directly by grep pattern.

## Quick start

```bash
# Per-substrate selftest (direct, recommended)
hexa run eeg/substrates/synth_substrate.hexa --selftest         # F_SUB_01 — 7/7 PASS
hexa run eeg/substrates/brainflow_substrate.hexa --selftest     # F_SUB_02
hexa run eeg/substrates/replay_substrate.hexa --selftest        # F_SUB_03 — 8/8 PASS

# Protocol declaration
hexa run eeg/substrates/substrate.hexa --selftest               # F_SUB_PROTO_01..03 — 6/6 PASS
hexa run eeg/substrates/substrate.hexa --inspect

# Channel-set preset
hexa run eeg/substrates/channel_set.hexa --selftest

# Package load marker
hexa run eeg/substrates/__init__.hexa --selftest

# Substrate-aware collect/recorder dispatch (Phase 1, pointer mode)
hexa run eeg/collect.hexa --selftest                            # default brainflow — 12/12 PASS (regression gate)
hexa run eeg/collect.hexa --selftest --substrate synth          # pointer — verdict=DEFERRED, exit 0
hexa run eeg/collect.hexa --selftest --substrate replay         # pointer — verdict=DEFERRED, exit 0
hexa run eeg/collect.hexa --selftest --legacy-inline            # alias for --substrate brainflow
hexa run eeg/eeg_recorder.hexa --selftest --substrate synth     # pointer (also useful when .venv-eeg absent)

# Regression gate (must stay byte-identical)
hexa run eeg/_session_manager.hexa --selftest                   # F_SM_01..03

# License firewall (Part A — shipped 77484267)
bin/hexa-brain license-check --selftest                         # F_LF_01..03 — 3/3 PASS
bin/check_licenses.sh                                            # full scan — 205 files / 0 violations
```

## Cross-references

- Protocol contract: `eeg/substrates/substrate.hexa` — canonical declaration
- Design rationale: `design/substrate_abstraction.md` — protocol + license posture + §8 E-1 follow-up landing record
- Phase 1 dispatch wiring: `eeg/collect.hexa` (`--substrate` flag at L728-792), `eeg/eeg_recorder.hexa` (same), `eeg/dual_stream.hexa:211` (forward-look comment)
- Part A firewall: `vendor/external_deps.yaml` + `vendor/license_policy.yaml` + `bin/check_licenses.sh` — **shipped** (commit `77484267`); `LICENSE_FIREWALL.md` + `design/license_firewall.md`
- Sister: `eeg/protocols/` — paradigm modules (orthogonal concern, see `eeg/protocols/__init__.hexa`)
- Session record: `SESSION_LOG_2026_05_12.md` §10 — Phase 1 landing detail
