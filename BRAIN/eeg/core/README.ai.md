---
schema: anima/anima-eeg/core/ai-native/1
last_updated: 2026-05-03
parent: anima-eeg/README.ai.md
status: scaffold-only — directory created, files NOT yet moved
raws:
  - R9 hexa-only
  - R10 honest C3
  - R65 idempotent
---

# anima-eeg/core (AI-native)

Hardware infrastructure: OpenBCI Cyton+Daisy boot, ADS1299 register config, FTDI latency fix, impedance check, electrode adjustment helpers, recorders, raw filters.

## TL;DR

- **Not measurement, not analysis** — this layer talks to hardware, manages sessions, owns the data acquisition pipeline up to (but not including) paradigm-specific stimulus presentation.
- **16 .hexa files**, ~10,000 LOC total when populated.
- **Currently empty (scaffold)** — actual moves land in next BG cycle. Files still live at `anima-eeg/*.hexa` until then.

## Target contents (after move)

```
core/
├── _session_manager.hexa                  716 LOC  — session lifecycle (start/stop/persist)
├── eeg_filter.hexa                        609 LOC  — band-pass, notch, common-mode
├── eeg_setup.hexa                         243 LOC  — board init wrapper
├── eeg_ftdi_latency_fix.hexa              367 LOC  — FTDI USB latency timer override
├── ads1299_settings.hexa                 1006 LOC  — register config (gain, sample rate, channels)
├── impedance_check.hexa                   858 LOC  — z-command driver + thresholds
├── impedance_real_hardware_validation.hexa 754 LOC  — real-board impedance verify
├── board_health_check.hexa                688 LOC  — Cyton+Daisy alive probe
├── board_health_check_lsl.hexa            472 LOC  — LSL-side health probe
├── eeg_brainflow_sanity.hexa              569 LOC  — BrainFlow board sanity
├── eeg_recorder.hexa                      680 LOC  — background recorder + auto-organize
├── lsl_capture.hexa                       665 LOC  — LSL stream capture
├── electrode_adjustment_helper.hexa      1694 LOC  — interactive electrode placement guide
├── electrode_helper_rich.hexa             714 LOC  — Rich-TUI variant
├── full_helmet_view.hexa                  746 LOC  — full-helmet ASCII viz
└── headplot_helper.hexa                   468 LOC  — head topomap ASCII
```


1. Files are **NOT here yet** as of 2026-05-03. They reside at `anima-eeg/*.hexa`. See refactor plan.
2. Move will preserve git history (`git mv`); diffs against prior commits remain attributable.
3. After move, internal cross-imports inside these 16 files (e.g. `eeg_recorder` calls into `_session_manager`) must resolve through hexa-lang stage1 module path resolver. If stage1 resolver hard-codes `anima-eeg/<file>.hexa`, the move will break resolution — verify before mv lands.
