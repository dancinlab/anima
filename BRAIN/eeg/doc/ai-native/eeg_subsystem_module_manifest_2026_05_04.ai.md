---
date: 2026-05-04
package: hexa-brain
subsystem: eeg
status: LANDED
owner: hexa-brain repo
cycle: v1.1.0
ssot_artifact: eeg/*.hexa + eeg/protocols/*.hexa + eeg/protocol/*.hexa
---

# eeg subsystem module manifest — v1.1.0 (2026-05-04)

## §1 Purpose

The **eeg** subsystem is the scalp-EEG capture-to-analysis pipeline that
constitutes the production-ready surface of hexa-brain v1. It owns the
hardware handshake (OpenBCI Cyton+Daisy 16ch via BrainFlow), per-electrode
calibration, real-time + batch acquisition, DSP filtering, band-power +
topomap analysis, brain-likeness validation, and protocol orchestration
(closed-loop N-back, neurofeedback, paradigm-specific stimulus presentation).
This is the layer with **7 cycles of real-hardware evidence** including
Berger eyes-open/closed, jaw EMG artifact, blink EOG artifact, and
alpha-blocking sessions captured in `eeg/recordings/sessions/`.

In v1.1.0 the entire subsystem moved from repo root into `eeg/` to make room
for the new `core/` subsystem. All file paths below are relative to repo root
and prefixed with `eeg/`.

## §2 File inventory

### §2.1 `eeg/` top-level `.hexa` files (30 files, ~19,000 LoC total)

| File | Purpose |
|---|---|
| `eeg/__init__.hexa` | Module init / re-export shim |
| `eeg/_port_lock_detector.hexa` | Auto-recover from stuck `/dev/cu.usbserial-*` |
| `eeg/_session_manager.hexa` | Session lifecycle (start/stop/persist) |
| `eeg/ads1299_settings.hexa` | ADS1299 register config (gain, sample rate, channels) |
| `eeg/analyze.hexa` | Band-power + topomap analysis |
| `eeg/board_health_check_lsl.hexa` | LSL-side health probe |
| `eeg/board_health_check.hexa` | Cyton+Daisy alive probe |
| `eeg/calibrate.hexa` | Per-electrode impedance + adjust loop |
| `eeg/closed_loop.hexa` | Adaptive N-back + meditation closed-loop (WebSocket) |
| `eeg/collect.hexa` | Live BrainFlow acquisition to `.npy` |
| `eeg/dual_stream.hexa` | Phi + EEG dual-stream RNG-seeded capture |
| `eeg/eeg_brainflow_sanity.hexa` | BrainFlow board sanity check |
| `eeg/eeg_filter.hexa` | Band-pass / notch / common-mode filters |
| `eeg/eeg_ftdi_latency_fix.hexa` | FTDI USB latency timer override (256→1ms) |
| `eeg/eeg_recorder.hexa` | Background recorder + auto-organize |
| `eeg/eeg_setup.hexa` | Board init wrapper |
| `eeg/eeg.hexa` | Top-level CLI router (entry point for `hexa-brain eeg router`) |
| `eeg/electrode_adjustment_helper.hexa` | Interactive 16ch placement guide |
| `eeg/electrode_helper_rich.hexa` | Rich-TUI variant of adjustment helper |
| `eeg/experiment.hexa` | Standardized protocols (resting / alpha / anima) |
| `eeg/full_helmet_view.hexa` | Full-helmet ASCII visualization |
| `eeg/headplot_helper.hexa` | Head topomap ASCII renderer |
| `eeg/impedance_check.hexa` | z-command driver + thresholds |
| `eeg/impedance_real_hardware_validation.hexa` | Real-board impedance verify |
| `eeg/lsl_capture.hexa` | LSL stream capture |
| `eeg/neurofeedback.hexa` | Binaural beats + LED feedback (Φ/tension → params) |
| `eeg/realtime.hexa` | Live BrainState consumer thread |
| `eeg/rp_adaptive_response.hexa` | Adaptive response policy (RPC pacing) |
| `eeg/transplant_eeg_verify.hexa` | Cross-substrate transplant verifier |
| `eeg/validate_consciousness.hexa` | 6-metric brain-likeness QA (85.6% canonical) |

### §2.2 `eeg/protocols/` paradigm modules (33 files)

Paradigm-specific stimulus + measurement orchestration:

- **Audio-cued sessions**: `blink_session_audio.hexa`, `jaw_session_audio.hexa`,
  `ppg_session_audio.hexa`, `berger_session_audio.hexa`,
  `berger_session_audio_v3_8ch.hexa`, `jaw_clench_emg_v2_8ch.hexa`.
- **Detector cores**: `eye_blink_detect.hexa`, `jaw_clench_emg.hexa`,
  `ppg_heart_rate.hexa`, `ppg_hrv_extended.hexa`,
  `concentration_episodes.hexa`, `drowsy_microsleep_detect.hexa`.
- **Resting/alpha**: `alpha_eyes_closed.hexa`, `mu_rhythm.hexa`,
  `long_duration_resting.hexa`.
- **Evoked**: `p300_visual_oddball.hexa`, `ssvep_steady_state.hexa`,
  `focus_brainflow_metric.hexa`.
- **Closed-loop application**: `bci_control.hexa`, `emotion_sync.hexa`,
  `multi_eeg.hexa`, `sleep_protocol.hexa`.
- **Preflight gates**: `master_preflight.hexa`, `preflight_settle.hexa`,
  `cap_fit_verify.hexa`, `warmup_fs_check.hexa`, `dc_settle_trim.hexa`,
  `sample_rate_guard.hexa`, `cyton_only_250hz.hexa`.
- **Audit / wrapper**: `analyze_wrapper.hexa`,
  `background_quality_audit.hexa`, `package_num_audit.hexa`.
- **Init**: `__init__.hexa`.

### §2.3 `eeg/protocol/` (auditory only — 1 file)

- `eeg/protocol/p300_auditory_oddball.hexa` — auditory P300 evoked-potential paradigm.

### §2.4 `eeg/core/` (legacy quality layer — 2 files)

| File | Purpose |
|---|---|
| `eeg/core/quality_audit.hexa` | Per-recording quality audit (rail / DC / impedance flags) |
| `eeg/core/quality_ledger.hexa` | Append-only ledger of audit verdicts |

Note: this is **distinct** from the top-level `core/` subsystem (which holds
paradigms + metrics + filter pipeline). The `eeg/core/` subdir is the legacy
quality-layer sibling that was scaffolded inside anima-eeg pre-spinoff and
carried over. v1.2+ may consolidate into the top-level `core/` if appropriate.

### §2.5 `eeg/scripts/` and `eeg/tool/`

- `eeg/scripts/monthly_eeg_validate.hexa` — monthly batch brain-likeness validation
- `eeg/scripts/organize_recordings.hexa` — auto-organize recordings/ into bins
- `eeg/tool/` — 14 fusion + integrator + audit utilities (cardiac, sleep,
  eye-tracker, mobile EEG, wearable health, daily-life context, eye-blink
  detector, etc.) — see CHANGELOG v1.0.0 for the full list.

## §3 Public API surface

Verbs (via `bin/hexa-brain eeg <verb>` dispatcher):

| Verb | Backing file | Description |
|---|---|---|
| `eeg board-health` (alias `health`) | `eeg/board_health_check.hexa` | USB / FTDI / Cyton serial verify |
| `eeg calibrate` | `eeg/calibrate.hexa` | Impedance + adjust loop |
| `eeg collect` | `eeg/collect.hexa` | Live BrainFlow to .npy |
| `eeg analyze` | `eeg/analyze.hexa` | Band-power + topomap |
| `eeg experiment` | `eeg/experiment.hexa` | Standardized protocol set |
| `eeg closed-loop` (aliases `nback`, `meditation`) | `eeg/closed_loop.hexa` | N-back / meditation |
| `eeg validate` (alias `brain-likeness`) | `eeg/validate_consciousness.hexa` | 6-metric brain-likeness |
| `eeg realtime` | `eeg/realtime.hexa` | Live consumer thread |
| `eeg recorder` | `eeg/eeg_recorder.hexa` | Background recorder daemon |
| `eeg electrode-adjust` | `eeg/electrode_adjustment_helper.hexa` | Live electrode adjustment helper |
| `eeg impedance` | `eeg/impedance_check.hexa` | Standalone impedance check |
| `eeg lsl-capture` | `eeg/lsl_capture.hexa` | LSL stream capture |
| `eeg dual-stream` | `eeg/dual_stream.hexa` | Dual Phi+EEG stream |
| `eeg neurofeedback` | `eeg/neurofeedback.hexa` | Binaural beats + LED feedback |
| `eeg full-helmet-view` | `eeg/full_helmet_view.hexa` | 16-ch helmet visualization |
| `eeg router` (default) | `eeg/eeg.hexa` | Top-level eeg.hexa router |

Direct invocation (without dispatcher) for any of the 30 `eeg/*.hexa` files
plus 33 `eeg/protocols/*.hexa` is also supported via `hexa run <path>`. The
dispatcher also supports a fall-through: an unknown verb `eeg foo` will try
`eeg/foo.hexa` (with `-` → `_` conversion) and otherwise delegate to
`eeg/eeg.hexa`.

## §4 Dependencies

### §4.1 Hardware
- **OpenBCI Cyton+Daisy 16ch** at 125 Hz (Daisy mode); $0 marginal cost (owned).
- FTDI USB-serial bridge (Cyton uplink); requires latency-timer fix to 1ms.
- Optional PPG add-on (3-pin wiring documented in `eeg/doc/cyton_ppg_wiring_official_*`).

### §4.2 Software
- **BrainFlow Python** — wraps board protocol; called via `.venv-eeg/` Python
  bridge (see Honest C3 §7).
- **Hexa-lang runtime** (`hexa run`).
- **macOS / Linux** (Linux less-tested; Windows untested).
- **NumPy** (via BrainFlow venv) for `.npy` recording I/O.

## §5 Sibling subsystems

- **core** subsystem (`core_subsystem_module_manifest_2026_05_04.ai.md`) —
  paradigms + metrics + filter pipeline. Consumes recordings produced by this
  eeg subsystem; provides pure-hexa metric primitives (LZ76, permutation
  entropy, Hjorth) used by analyze.
- **cli** subsystem (`cli_dispatch_design_2026_05_04.ai.md`) — provides the
  `hexa-brain eeg <verb>` routing layer that fronts this manifest's surface.

## §6 Future evolution

| Version | Substrate | Status | Gating |
|---|---|---|---|
| **v1** | Scalp EEG (current) | Production-ready | DONE |
| **v2** | Intracranial EEG (ECoG / sEEG) | Spec phase | Clinical MoU + ethics board |
| **v3** | High-density arrays (Neuropixels / Utah / Neuralink-class) | Spec phase | Hardware acquisition |
| **v4** | Closed-loop BMI (motor decode + neurostim) | Spec phase | Decode + stim integration |
| **v5** | Chronic implant + wireless | Spec phase | Implant partner collab |

Per `.roadmap.hexa_brain` cond.2-cond.5. Each cond carries an `honest_c3` field
disclosing the absence of partnerships/hardware.


1. **BrainFlow Python wrap is non-pure-hexa**: the core hardware protocol talks
   to BrainFlow's Python SDK via the `.venv-eeg/` bridge. This is a conscious
   and would require re-implementing the OpenBCI serial protocol from scratch.
   under the `.own N` taxonomy in this repo. Anima-side `.own 9` (BrainFlow
   bridge) was the historical opt-out home; spinoff inherited the carve-out
   without re-paperwork.
3. **Sampling 125 Hz vs ZuCo 500 Hz asymmetry**: hexa-brain v1 captures at
   125 Hz (Cyton+Daisy hardware limit); cross-substrate research that compares
   to ZuCo (500 Hz invasive-style scalp) corpora must apply explicit upsampling
   or downsampling. This is documented in `eeg/doc/sample_rate_root_cause_consolidated_2026_05_03.md`.
4. **16ch min for binding evidence**: validate_consciousness.hexa's 85.6%
   brain-likeness benchmark is calibrated against 16ch Cyton+Daisy. Cyton-only
   8ch sessions exist (e.g. `eeg/protocols/cyton_only_250hz.hexa`) but do not produce
   comparable brain-likeness scores; downgrading to 8ch is **not** supported as
   a primary mode for v1 brain-likeness claims.
5. **hexa-resolver darwin-native bypass**: glob expansion on `/dev/cu.*` paths
   is handled by a darwin-native bypass marker in the hexa runtime to avoid
   resolver-induced path mangling. Linux equivalent uses `/dev/ttyUSB*` and may
   need its own bypass; not yet stress-tested on Linux.
6. **eeg/core/ vs core/ name collision**: `eeg/core/` (legacy quality layer)
   and the top-level `core/` (paradigms/metrics) share the name "core" but
   serve different purposes. Reading code that says "core/quality_audit"
   resolves to `eeg/core/quality_audit.hexa`; "tool/core/eeg_core" resolves to
   the new substrate-agnostic core. This is a documentation hazard; v1.2+ may
   rename `eeg/core/` to `eeg/quality/` to disambiguate.

## §8 Composability

- **Upstream**: hexa-lang runtime, BrainFlow Python (via venv bridge), OS
  USB-serial driver stack.
- **Downstream**:
  - anima's consciousness runtime (consumes `eeg/closed_loop.hexa` WebSocket
    events + `eeg/recordings/sessions/*.npy` capture artifacts).
  - core subsystem (consumes `eeg/recordings/sessions/*.npy` for paradigm +
    metric + artifact-detector evaluation).
  - hexa-lang ecosystem packages that need EEG I/O (none yet beyond anima).
