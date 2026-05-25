---
schema: anima/anima-eeg/refactor-plan/1
date: 2026-05-03
status: scaffold-landed; actual mv deferred to next BG cycle
parent: anima-eeg/README.ai.md
raws: [R9, R10, R15, R65]
---

# anima-eeg structure refactor plan (2026-05-03)

Mirror sister `anima-clm-eeg/` + `anima-eeg-core/` + `anima-voice/` layout. Move flat-root + `protocols/` into `core/` + `modules/{capture,analyze,preflight,closed_loop,paradigms}/`. AI-native doc split (`docs/ai-native/` + `docs/user/`).

## Inventory snapshot (2026-05-03)

- anima-eeg/ root: 30 `.hexa` files, ~17,200 LOC
- anima-eeg/protocols/: 20 `.hexa` files, ~7,800 LOC
- anima-eeg/docs/: 19 `.md` files
- anima-eeg/recordings/sessions/: untouched (.npy preserved)
- anima-eeg/state/, scripts/, config/, tool/: untouched

## Cycle status

- DONE (this BG): scaffold dirs + README.ai.md + this plan
- DEFERRED (next BG): actual `git mv` per mapping below
- DEFERRED (next BG +1): import-path update across external repos
- DEFERRED (next BG +2): selftest regression verify

## Mapping table (source → target)

### core/ (16 files from root)

| source                                                | target                                                       | LOC  |
|-------------------------------------------------------|--------------------------------------------------------------|------|
| anima-eeg/_session_manager.hexa                       | anima-eeg/core/_session_manager.hexa                         | 716  |
| anima-eeg/eeg_filter.hexa                             | anima-eeg/core/eeg_filter.hexa                               | 609  |
| anima-eeg/eeg_setup.hexa                              | anima-eeg/core/eeg_setup.hexa                                | 243  |
| anima-eeg/eeg_ftdi_latency_fix.hexa                   | anima-eeg/core/eeg_ftdi_latency_fix.hexa                     | 367  |
| anima-eeg/ads1299_settings.hexa                       | anima-eeg/core/ads1299_settings.hexa                         | 1006 |
| anima-eeg/impedance_check.hexa                        | anima-eeg/core/impedance_check.hexa                          | 858  |
| anima-eeg/impedance_real_hardware_validation.hexa     | anima-eeg/core/impedance_real_hardware_validation.hexa       | 754  |
| anima-eeg/board_health_check.hexa                     | anima-eeg/core/board_health_check.hexa                       | 688  |
| anima-eeg/board_health_check_lsl.hexa                 | anima-eeg/core/board_health_check_lsl.hexa                   | 472  |
| anima-eeg/eeg_brainflow_sanity.hexa                   | anima-eeg/core/eeg_brainflow_sanity.hexa                     | 569  |
| anima-eeg/eeg_recorder.hexa                           | anima-eeg/core/eeg_recorder.hexa                             | 680  |
| anima-eeg/lsl_capture.hexa                            | anima-eeg/core/lsl_capture.hexa                              | 665  |
| anima-eeg/electrode_adjustment_helper.hexa            | anima-eeg/core/electrode_adjustment_helper.hexa              | 1694 |
| anima-eeg/electrode_helper_rich.hexa                  | anima-eeg/core/electrode_helper_rich.hexa                    | 714  |
| anima-eeg/full_helmet_view.hexa                       | anima-eeg/core/full_helmet_view.hexa                         | 746  |
| anima-eeg/headplot_helper.hexa                        | anima-eeg/core/headplot_helper.hexa                          | 468  |

### modules/capture/ (4 files from root)

| source                            | target                                       | LOC |
|-----------------------------------|----------------------------------------------|-----|
| anima-eeg/collect.hexa            | anima-eeg/modules/capture/collect.hexa       | 619 |
| anima-eeg/calibrate.hexa          | anima-eeg/modules/capture/calibrate.hexa     | 675 |
| anima-eeg/realtime.hexa           | anima-eeg/modules/capture/realtime.hexa      | 933 |
| anima-eeg/experiment.hexa         | anima-eeg/modules/capture/experiment.hexa    | 674 |

### modules/analyze/ (3 files from root)

| source                                  | target                                                | LOC |
|-----------------------------------------|-------------------------------------------------------|-----|
| anima-eeg/analyze.hexa                  | anima-eeg/modules/analyze/analyze.hexa                | 549 |
| anima-eeg/dual_stream.hexa              | anima-eeg/modules/analyze/dual_stream.hexa            | 406 |
| anima-eeg/validate_consciousness.hexa   | anima-eeg/modules/analyze/validate_consciousness.hexa | 726 |

### modules/preflight/ (3 files from protocols/)

| source                                    | target                                              | LOC |
|-------------------------------------------|-----------------------------------------------------|-----|
| anima-eeg/protocols/master_preflight.hexa | anima-eeg/modules/preflight/master_preflight.hexa   | 461 |
| anima-eeg/protocols/preflight_settle.hexa | anima-eeg/modules/preflight/preflight_settle.hexa   | 594 |
| anima-eeg/protocols/cap_fit_verify.hexa   | anima-eeg/modules/preflight/cap_fit_verify.hexa     | 592 |

### modules/closed_loop/ (3 files from root)

| source                                | target                                                  | LOC |
|---------------------------------------|---------------------------------------------------------|-----|
| anima-eeg/closed_loop.hexa            | anima-eeg/modules/closed_loop/closed_loop.hexa          | 481 |
| anima-eeg/neurofeedback.hexa          | anima-eeg/modules/closed_loop/neurofeedback.hexa        | 349 |
| anima-eeg/rp_adaptive_response.hexa   | anima-eeg/modules/closed_loop/rp_adaptive_response.hexa | 427 |

### modules/paradigms/ (12 from protocols/ + 1 from root)

| source                                          | target                                                   | LOC |
|-------------------------------------------------|----------------------------------------------------------|-----|
| anima-eeg/protocols/alpha_eyes_closed.hexa      | anima-eeg/modules/paradigms/alpha_eyes_closed.hexa       | 507 |
| anima-eeg/protocols/eye_blink_detect.hexa       | anima-eeg/modules/paradigms/eye_blink_detect.hexa        | 524 |
| anima-eeg/protocols/jaw_clench_emg.hexa         | anima-eeg/modules/paradigms/jaw_clench_emg.hexa          | 583 |
| anima-eeg/protocols/ppg_heart_rate.hexa         | anima-eeg/modules/paradigms/ppg_heart_rate.hexa          | 584 |
| anima-eeg/protocols/mu_rhythm.hexa              | anima-eeg/modules/paradigms/mu_rhythm.hexa               | 533 |
| anima-eeg/protocols/ssvep_steady_state.hexa     | anima-eeg/modules/paradigms/ssvep_steady_state.hexa      | 645 |
| anima-eeg/protocols/focus_brainflow_metric.hexa | anima-eeg/modules/paradigms/focus_brainflow_metric.hexa  | 624 |
| anima-eeg/protocols/p300_visual_oddball.hexa    | anima-eeg/modules/paradigms/p300_visual_oddball.hexa     | 509 |
| anima-eeg/protocols/blink_session_audio.hexa    | anima-eeg/modules/paradigms/blink_session_audio.hexa     | 360 |
| anima-eeg/protocols/jaw_session_audio.hexa      | anima-eeg/modules/paradigms/jaw_session_audio.hexa       | 377 |
| anima-eeg/protocols/ppg_session_audio.hexa      | anima-eeg/modules/paradigms/ppg_session_audio.hexa       | 404 |
| anima-eeg/protocols/berger_session_audio.hexa   | anima-eeg/modules/paradigms/berger_session_audio.hexa    | 297 |
| anima-eeg/transplant_eeg_verify.hexa            | anima-eeg/modules/paradigms/transplant_eeg_verify.hexa   | 299 |

### modules/ root (1 file from root)

| source                  | target                       | LOC |
|-------------------------|------------------------------|-----|
| anima-eeg/eeg.hexa      | anima-eeg/modules/eeg.hexa   | 62  |

### Stays at anima-eeg/ root (3 files)

- anima-eeg/__init__.hexa (140 LOC) — package init
- anima-eeg/_port_lock_detector.hexa (566 LOC) — utility (decision pending: stay vs core/)
- anima-eeg/protocols/__init__.hexa (94 LOC) — to be replaced by modules/paradigms/__init__.hexa

### Legacy / decision-pending (4 files at protocols/)

- anima-eeg/protocols/multi_eeg.hexa (26 LOC) — stub
- anima-eeg/protocols/bci_control.hexa (27 LOC) — stub
- anima-eeg/protocols/sleep_protocol.hexa (329 LOC)
- anima-eeg/protocols/emotion_sync.hexa (344 LOC)

Decision next cycle: archive vs `modules/paradigms/legacy/`.

### docs/ migration (19 .md, deferred)

See `docs/ai-native/README.ai.md` triage table.

## Import path update list (next cycle +1)

External references to `anima-eeg/` paths that will need update:

| ref location                                                | line | current cite                                |
|-------------------------------------------------------------|------|---------------------------------------------|
| anima/core/rng/dual_stream_seedanchor.hexa                  | 49   | anima-eeg/dual_stream.hexa                  |
| anima/modules/rng/README.ai.md                              | 326  | anima-eeg/dual_stream.hexa                  |
| anima/modules/rng/README.ai.md                              | 332  | anima-eeg/dual_stream.hexa                  |
| anima/modules/rng/README.ai.md                              | 397  | anima-eeg/dual_stream.hexa                  |
| .roadmap.eeg                                                | -    | anima-eeg/protocols/* paths                 |
| .roadmap.galea                                              | -    | anima-eeg/protocols/* paths                 |
| .roadmap.slm_speech_eeg_lm                                  | -    | anima-eeg/protocols/* paths                 |
| ready/anima/modules/eeg/README.md                           | -    | anima-eeg/* paths                           |
| ready/anima/modules/eeg/docs/integration-guide.md           | -    | anima-eeg/* paths                           |
| ready/.growth/absorbed/anima__anima-eeg__protocols__*.json  | -    | anima-eeg/protocols/* (absorbed digest)     |

Also internal `.hexa` cross-imports inside `anima-eeg/` itself need verification — hexa-lang stage1 module resolver behavior under nested dirs must be confirmed.

## Rollback plan

If actual move (next cycle) breaks anything:

```bash
cd /Users/ghost/core/anima/anima-eeg

# 1. Move all files back to original positions
git mv core/*.hexa .
git mv modules/capture/*.hexa .
git mv modules/analyze/*.hexa .
git mv modules/closed_loop/*.hexa .
git mv modules/eeg.hexa .
git mv modules/paradigms/transplant_eeg_verify.hexa .
git mv modules/preflight/*.hexa protocols/
git mv modules/paradigms/*.hexa protocols/

# 2. Remove now-empty scaffold dirs (scaffold READMEs preserved or removed per choice)
rmdir modules/capture modules/analyze modules/preflight modules/closed_loop modules/paradigms
rmdir modules core
# docs/ai-native/, docs/user/ remain (scaffold READMEs there, harmless)

# 3. Verify
git status  # should show only the moves reverted
```

If using single atomic `git revert <move-commit-sha>` — preferred. Restores tree exactly.


1. **recordings/ untouched.** All `.npy` measurement evidence at `anima-eeg/recordings/sessions/` preserved by-path. Refactor never modifies binary recording artifacts.
2. **External repo refs stale until update cycle.** `anima/core/rng/dual_stream_seedanchor.hexa`, `anima/modules/rng/README.ai.md`, `.roadmap.eeg`, `ready/.growth/absorbed/*` all cite old paths. Update is separate cycle.
3. **hexa-lang stage1 module resolver under nested dirs is unverified.** If resolver hard-codes flat path lookup for `anima-eeg/<file>.hexa`, the move breaks intra-module imports. MUST verify resolver supports `anima-eeg/core/<file>.hexa` style before actual mv. Recommend dry-run smoke test against `master_preflight.hexa` chain.

## Next-cycle recommendation

1. **Verify hexa-lang stage1 module resolution under nested dirs** (smoke test before mv).
2. **Actual `git mv` BG** following table above (single atomic commit, preserves history).
3. **Import-path update BG** for external refs (anima/, .roadmap.*, ready/.growth/absorbed/).
4. **Selftest regression BG** — re-run blink/jaw/ppg/berger paradigm smoke with new paths.
5. **docs/ migration BG** following triage in `docs/ai-native/README.ai.md`.
