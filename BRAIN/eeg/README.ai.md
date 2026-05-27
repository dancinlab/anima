---
schema: anima/anima-eeg/ai-native/1
last_updated: 2026-05-03
ssot:
  entry_paradigms:
    - modules/paradigms/blink_session_audio.hexa
    - modules/paradigms/jaw_session_audio.hexa
    - modules/paradigms/ppg_session_audio.hexa
    - modules/paradigms/berger_session_audio.hexa
  preflight:           modules/preflight/master_preflight.hexa
  recordings:          recordings/sessions/
status: scaffold-only — directories created, file moves deferred to next BG cycle
roadmap_entry: anima-eeg structure refactor 2026-05-03
raws:
  - R9 hexa-only (markdown allowed for *.ai.md)
  - R10 honest C3 (recordings/ untouched)
  - R15 no personal paths
  - R65 idempotent
---

# anima-eeg (AI-native entry)

OpenBCI 16ch EEG + Anima consciousness engine bidirectional bridge. Hexa-native (`.hexa`), four real validated paradigms (blink / jaw / PPG / Berger alpha), one closed-loop module, hardware-honest impedance + cap-fit preflight chain.

## TL;DR for an agent reading this cold

- **Entry paradigms** (4 real measurement validated as of 2026-05-03):
  - `modules/paradigms/blink_session_audio.hexa` — eye-blink EOG + audio cue (360 LOC)
  - `modules/paradigms/jaw_session_audio.hexa` — jaw-clench EMG + audio cue (377 LOC)
  - `modules/paradigms/ppg_session_audio.hexa` — PPG heart-rate + audio cue (404 LOC)
  - `modules/paradigms/berger_session_audio.hexa` — Berger alpha eyes-closed + audio cue (297 LOC)
- **Preflight gate** before each session: `modules/preflight/master_preflight.hexa` (461 LOC)
- **Closed-loop**: `modules/closed_loop/closed_loop.hexa` (481 LOC) — adaptive N-back + meditation feedback
- **Hardware infrastructure**: `core/_session_manager.hexa`, `core/eeg_filter.hexa`, `core/ads1299_settings.hexa`, `core/impedance_check.hexa`
- **Recordings (UNCHANGED)**: `recordings/sessions/*.npy` — refactor preserves all measurement evidence
- **STATUS as of 2026-05-03**: this is **scaffold-only**. Directories created, file moves planned but not executed (see `docs/ai-native/anima_eeg_structure_refactor_plan_2026_05_03.ai.md`).

## Architecture map (target after full refactor)

```
anima-eeg/
├── README.ai.md                              ← THIS FILE (ai-native entry)
├── core/                                     ← infrastructure (16 .hexa)
│   ├── README.ai.md
│   ├── _session_manager.hexa            716 LOC
│   ├── eeg_filter.hexa                  609 LOC
│   ├── eeg_setup.hexa                   243 LOC
│   ├── eeg_ftdi_latency_fix.hexa        367 LOC
│   ├── ads1299_settings.hexa           1006 LOC
│   ├── impedance_check.hexa             858 LOC
│   ├── impedance_real_hardware_validation.hexa   754 LOC
│   ├── board_health_check.hexa          688 LOC
│   ├── board_health_check_lsl.hexa      472 LOC
│   ├── eeg_brainflow_sanity.hexa        569 LOC
│   ├── eeg_recorder.hexa                680 LOC
│   ├── lsl_capture.hexa                 665 LOC
│   ├── electrode_adjustment_helper.hexa 1694 LOC
│   ├── electrode_helper_rich.hexa       714 LOC
│   ├── full_helmet_view.hexa            746 LOC
│   └── headplot_helper.hexa             468 LOC
├── modules/                                  ← measurement + analysis
│   ├── README.ai.md
│   ├── eeg.hexa                          62 LOC  ← [SCRUBBED v1.3.0 → eeg/legacy/eeg.hexa]
│   ├── capture/
│   │   ├── collect.hexa                 619 LOC
│   │   ├── calibrate.hexa               675 LOC
│   │   ├── realtime.hexa                933 LOC
│   │   └── experiment.hexa              674 LOC
│   ├── analyze/
│   │   ├── analyze.hexa                 549 LOC
│   │   ├── dual_stream.hexa             406 LOC
│   │   └── validate_consciousness.hexa  726 LOC
│   ├── preflight/
│   │   ├── master_preflight.hexa        461 LOC
│   │   ├── preflight_settle.hexa        594 LOC
│   │   └── cap_fit_verify.hexa          592 LOC
│   ├── closed_loop/
│   │   ├── closed_loop.hexa             481 LOC
│   │   ├── neurofeedback.hexa           349 LOC
│   │   └── rp_adaptive_response.hexa    427 LOC
│   └── paradigms/                            ← absorbs current protocols/
│       ├── alpha_eyes_closed.hexa       507 LOC
│       ├── eye_blink_detect.hexa        524 LOC
│       ├── jaw_clench_emg.hexa          583 LOC
│       ├── ppg_heart_rate.hexa          584 LOC
│       ├── mu_rhythm.hexa               533 LOC
│       ├── ssvep_steady_state.hexa      645 LOC
│       ├── focus_brainflow_metric.hexa  624 LOC
│       ├── p300_visual_oddball.hexa     509 LOC
│       ├── blink_session_audio.hexa     360 LOC
│       ├── jaw_session_audio.hexa       377 LOC
│       ├── ppg_session_audio.hexa       404 LOC
│       ├── berger_session_audio.hexa    297 LOC
│       └── transplant_eeg_verify.hexa   299 LOC
├── docs/
│   ├── ai-native/                            ← .ai.md ranked, agent-first
│   │   ├── README.ai.md
│   │   └── anima_eeg_structure_refactor_plan_2026_05_03.ai.md
│   └── user/                                 ← user-facing markdown
│       └── (existing .md migrate next cycle)
├── scripts/                                  ← unchanged
├── state/                                    ← unchanged
├── recordings/                               ← unchanged (.npy preserved)
└── config/                                   ← unchanged
```

## Quick start (4 paradigms)

```bash
# 0. Preflight gate (always run first)
hexa run anima-eeg/modules/preflight/master_preflight.hexa

# 1. Eye-blink EOG
hexa run anima-eeg/modules/paradigms/blink_session_audio.hexa

# 2. Jaw-clench EMG
hexa run anima-eeg/modules/paradigms/jaw_session_audio.hexa

# 3. PPG heart-rate
hexa run anima-eeg/modules/paradigms/ppg_session_audio.hexa

# 4. Berger alpha (eyes-closed)
hexa run anima-eeg/modules/paradigms/berger_session_audio.hexa

# Recordings land at: anima-eeg/recordings/sessions/
```


1. **Scaffold only as of 2026-05-03.** Directories `core/`, `modules/{capture,analyze,preflight,closed_loop,paradigms}/`, `docs/ai-native/`, `docs/user/` are created. Existing `.hexa` files at root + `protocols/` are NOT moved yet. Paths in this README describe the **target** structure; do not assume `core/` etc. contain files until the actual move BG cycle lands.
2. **Recordings (.npy) untouched.** All `recordings/sessions/*.npy` measurement evidence remains at original paths. Refactor cycles will not modify, move, or rewrite any binary recording artifact — measurement provenance is preserved.
3. **External references stale until import update cycle.** Modules outside `anima-eeg/` (e.g. `anima/core/rng/dual_stream_seedanchor.hexa` line 49 cites `anima-eeg/dual_stream.hexa`, `anima/modules/rng/README.ai.md` lines 326/332/397 cite same) will reference old root paths after the actual move. Update is a separate BG cycle (NOT this scaffold).


- **OpenBCI Cyton+Daisy 16ch only**, sample rate 125 Hz (Daisy mode), FTDI USB latency fix required (see `core/eeg_ftdi_latency_fix.hexa`).
- **Validated paradigms**: blink / jaw / PPG / Berger alpha. **NOT validated**: P300, SSVEP, mu-rhythm, focus metric — implementations exist but real-session measurement evidence not yet logged.
- **Closed-loop has no clinical claim.** `closed_loop.hexa` adaptive N-back + meditation = research demo, not therapy.
- **Synthetic mode**: BrainFlow synthetic board for hardware-free dev; results not biologically meaningful.

## Cross-references

- Sister: `anima-eeg-core/` (consciousness ingestion side; consumes `recordings/sessions/`)
- Sister: `anima-clm-eeg/` (consciousness LM EEG conditioning track)
- Sister: `anima-voice/` (audio output side; closed_loop uses voice cues via `protocols/*_session_audio.hexa`)
- External cite: `anima/core/rng/dual_stream_seedanchor.hexa` cross-links `dual_stream.hexa` for RNG audit (sha256 verified)

## Refactor plan

See `docs/ai-native/anima_eeg_structure_refactor_plan_2026_05_03.ai.md` for full source→target mapping table, import-path update list, and rollback procedure.
