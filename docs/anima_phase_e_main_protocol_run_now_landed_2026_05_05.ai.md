<!-- @no-lineage-citation-exempt-file -->

# Anima Phase E main protocol run-now prep landed (2026-05-05)

Status: PREP READY, awaiting fire signal from operator.
Cycle: BG-PHASE-E-MAIN-PROTOCOL-RUN-NOW
Cost: $0 Mac, ~20 min wall when fired.

Sister artifacts (active peer paths, not version-bound citations):
- spec at docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md
- spec landing at docs/anima_phase_e_eeg_live_session_prep_landed_2026_05_04.ai.md
- EC+EO sanity at docs/anima_phase_e_ec_eo_sanity_analysis_landed_2026_05_05.ai.md
- session memory feedback_py_to_hexa_only carve-out for Tk/pylsl bridge

## Section 1 — what this prep delivers

A fireable Phase E P3 run (15-min reading task, 300 sentence-aligned epochs, LSL marker outlet) with single-command launch. All artifacts staged; fire is operator-gated because head-ache plus screen-time plus electrode-cap demand attention.

## Section 2 — artifacts (staged, none fired)

| artifact | path | status |
|---|---|---|
| Sentence corpus, 300, 5-axis x 60 | state/anima_phase_e_eeg_live_2026_05_05/main_protocol_prompts.jsonl | staged 57.6 KB |
| Stimulus presenter (terminal Tk-fallback + LSL outlet) | tool/transient_py/anima_phase_e_stimulus_presenter.py | staged 12.3 KB, selftest PASS |
| Auto-launch orchestrator | state/anima_phase_e_eeg_live_2026_05_05/main_protocol_run.bash | staged 7.2 KB, executable, bash -n PASS |
| Verdict (this BG) | state/phase_e_main_protocol_run_now_2026_05_05/verdict.json | emitted |
| LSL pre-flight | pylsl 1.18.2 in .venv-eeg, outlet+resolve+push selftest PASS | verified |

## Section 3 — fire command (operator, when ready)

```
bash /Users/ghost/core/anima/state/anima_phase_e_eeg_live_2026_05_05/main_protocol_run.bash
```

Optional env overrides:
- EEG_PORT=/dev/cu.usbserial-XXXX (default /dev/cu.usbserial-DP04WGIQ)
- RECAPTURE_BASELINES=1 (re-capture EC+EO 5min each; default skipped because berger_ec_60s + berger_eo_60s already present)
- SKIP_POST_REST=1 (skip 5min post-task rest; default ON)

Total wall: 15min P3 + impedance check (~2min) + optional 5min post-rest = ~17-22 min.

## Section 4 — run flow

1. step0: prompts file presence + n>=300 check
2. step1: impedance recheck via hexa-brain eeg impedance-validate --measure --port $PORT; abort on FAIL with B-track v7 reseat hint + macOS Yuna voice cue
3. step2: optional EC+EO 5min baseline re-capture (skipped by default)
4. step3: parallel: presenter (BG, .venv-eeg python, terminal fullscreen, LSL outlet anima_phase_e_markers) + EEG capture (FG, hexa run anima-eeg/collect.hexa --duration 900 --tag phase_e_main_15min)
5. step4: optional 5min post-task rest
6. step5: completion banner + analysis pipeline next-step pointer

## Section 5 — honest C3 (7 caveats)

1. C1 terminal-UI-not-Tk: .venv-eeg python lacks _tkinter (homebrew minimal build); presenter uses ANSI fullscreen + raw-tty spacebar instead of Tk window. UX (spacebar advance, min-dwell 1.5s, ESC abort) preserved; on-screen text is monospace.
2. C2 LSL marker is fallback sync, not primary: collect.hexa does not consume the LSL outlet; markers exist in main_protocol_stimulus_log.jsonl with ts_ns_monotonic for post-hoc cross-correlation with EEG sample timestamps. Primary sync is shared-Mac monotonic clock.
3. C3 audio sync AUX-17 not implemented: spec section 3 50ms 2kHz tone on AUX channel 17 is NOT generated; F-PHASE-E-2 sync verdict relies on monotonic-clock latency only.
4. C4 no alcohol-attest pre-gate: script does NOT verify user_attest.json before launching; analysis-pipeline section 7 P0 will refuse verdict emission if missing, so post-hoc gate exists but pre-hoc trust gate is on the operator.
5. C5 corpus substitution: anima-axis-conditioned 5-bucket x 60 (not ZuCo SR transcript shuffle as spec C8 suggested); verdict gate is corpus-agnostic so unchanged.
6. C6 125Hz vs 250Hz spec vs 500Hz ZuCo: actual Cyton+Daisy is 125Hz (per berger_ec_60s.npy.meta.json); 250-300ms post-onset epoch contains ~6 samples x 4 channels = 24 samples; spec C1 caveat anticipated 250Hz/48 samples. High-gamma coherence estimation at this window-length is borderline; analyzer must flag.
7. C7 fire is operator-only: this BG did NOT execute main_protocol_run.bash. ready_to_run=true means artifacts staged; the operator must self-decide on physical readiness (head-ache, screen-time tolerance, electrode-cap-on, 5-min stabilize).

## Section 6 — cross-cycle handoff

After fire + completion:

1. Verify outputs exist: phase_e_main_15min.npy (+ meta sidecar), main_protocol_stimulus_log.jsonl (300 sentence_advance events).
2. Run analysis pipeline per spec section 7 (P0 validate, P1 preprocess, P2 epoch, P3 coherence, P4 F-PHASE-E-1, P5 F-PHASE-E-2, P6 verdict).
3. F-PHASE-E-1 + F-PHASE-E-2 PASS + N>=300 yields composite PHASE_E_BINDING_WITNESSED, raising F1_v2 raw 0.408 to 0.558 (YELLOW reach); F2 ceiling unchanged per spec section 9.
4. Apply .roadmap.n_substrate cond.1 + .roadmap.eeg cond.5/cond.7 annotations per spec section 10 (additive-only mutation cycle).

## Section 7 — what this prep does NOT do

- Does NOT fire main_protocol_run.bash (operator-gated).
- Does NOT git commit (per BG charter).
- Does NOT modify .roadmap.* files (post-execution landed cycle).
- Does NOT run the analysis pipeline (post-capture).
- Does NOT generate the AUX-17 audio sync pulse (C3 caveat).

## Section 8 — cost + raw invariants

- Cost: $0 Mac CPU + $0 ubu1 + (when fired) ~17-22 min wall.
- raw-9 (hexa-only): presenter is .py under tool/transient_py/ per raw-37 transient carve-out; launch script is bash orchestrator (transient).
- raw-10 (honesty): 7 honest C3 caveats embedded.
- raw-15 (repo-relative): repo-relative paths.
- raw-37 (transient_py): tool/transient_py/ namespace declared.
- raw-71 (falsifier): F-PHASE-E-1 + F-PHASE-E-2 thresholds NOT relaxed (still spec section 2 frozen).

End of landed.
