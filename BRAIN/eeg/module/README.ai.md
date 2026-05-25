---
schema: anima/anima-eeg/modules/ai-native/1
last_updated: 2026-05-03
parent: anima-eeg/README.ai.md
status: scaffold-only
raws: [R9, R10, R65]
---

# anima-eeg/modules

Measurement, analysis, preflight, closed-loop, paradigm modules. Operates on top of `core/`.

## Sub-dirs

- `capture/` — raw acquisition (collect, calibrate, realtime, experiment)
- `analyze/` — post-acquisition (analyze, dual_stream, validate_consciousness)
- `preflight/` — session-start gate (master_preflight, preflight_settle, cap_fit_verify)
- `closed_loop/` — realtime feedback (closed_loop, neurofeedback, rp_adaptive_response)
- `paradigms/` — measurement designs (absorbs current `protocols/`)

## Validated paradigms (real-session evidence 2026-05-03)

- blink_session_audio (360 LOC)
- jaw_session_audio (377 LOC)
- ppg_session_audio (404 LOC)
- berger_session_audio (297 LOC)

## Scaffold caveats

1. Files NOT here yet — scaffold only.
2. `eeg.hexa` (62 LOC) shim entry SCRUBBED v1.3.0 → `eeg/legacy/eeg.hexa` (Phase 4b TODO-stub superseded by `eeg/eeg_setup.hexa` + `bin/hexa-brain`). Migrate any consumers to canonical verbs.
3. transplant_eeg_verify placement under paradigms/ is debatable; may relocate to analyze/.

See `../docs/ai-native/anima_eeg_structure_refactor_plan_2026_05_03.ai.md` for full mapping.
