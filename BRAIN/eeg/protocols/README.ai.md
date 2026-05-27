---
schema: hexa-brain/eeg/protocols/ai-native/1
last_updated: 2026-05-12
parent: eeg/README.ai.md
status: scaffold — load marker + 4-protocol manifest (FULL + WRAPPER mix)
raws:
  - R9 hexa-only
  - R10 honest C3
  - R11 snake_case
  - R65 idempotent
---

# hexa-brain/eeg/protocols (AI-native entry)

Paradigm modules: stimulus / scoring / aggregation for established EEG paradigms (Berger alpha, blink/jaw EMG, PPG, SSVEP, P300, n-back, ...). Orthogonal to **substrate** — protocols *consume* sample streams from any substrate.

## Manifest

| Protocol | Type | Notes |
|---|---|---|
| `bci_control` | WRAPPER | realtime EEG threshold control |
| `multi_eeg` | WRAPPER | multi-board hivemind sync |
| `sleep_protocol` | FULL | band-power threshold rules |
| `emotion_sync` | FULL | FAA = ln(R/F4) - ln(L/F3) |

Plus ~30 paradigm-specific modules (alpha_eyes_closed, jaw_clench_emg, ppg_heart_rate, berger_session_audio, ...). See `eeg/protocols/__init__.hexa` for the load-marker count.

## substrates/ sibling

Substrates declare *where* samples come from (`brainflow` board / `synth` LCG / `replay` .npy file / future `nes` virtual brain / future `cl1` living neurons). Protocols declare *what to do with* those samples. The two concerns are split into separate packages to avoid the conceptual mixing called out in `/home/summer/.claude/plans/hazy-kindling-wind.md` (Decisions table).

**deps:**
- `eeg/substrates/README.ai.md` — substrate-agnostic interface (Sprint 1 Part E-1, foundation)
- `eeg/substrates/substrate.hexa` — protocol contract (11 api_* methods)
- `eeg/substrates/registry.yaml` — per-backend `dep_id` / `coupling` / `tier`

Migration target (follow-up PR): `eeg/collect.hexa` and `eeg/eeg_recorder.hexa` switch from inline BoardShim loops to `substrate.api_open_session(spec)` calls. Protocols in this directory are unaffected — they read normalized `(data, ts)` chunks regardless of the underlying substrate.


1. Some entries in the protocols/ directory are **scaffold-only** (no real measurement validation yet — e.g. P300, SSVEP). See `eeg/README.ai.md §Hardware honesty` for the canonical validated-vs-unvalidated list.
2. README content here is hand-maintained; ground truth is the `__init__.hexa` load marker.
