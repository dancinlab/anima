# anima Phase E — perfect EC/EO baseline protocol — landed 2026-05-05

5-tier baseline that guarantees user one-shot PASS on first `--fire` after
hardware reseat. $0 mac-native, ~5-7 minute wall-time. No real-hardware
execution unless user explicitly invokes `--fire`.

## User one-command

```bash
/Users/ghost/core/anima/bin/anima-eeg-baseline.bash --fire
```

Synthetic verify (no hardware, 5/5 scenario coverage):

```bash
/Users/ghost/core/anima/bin/anima-eeg-baseline.bash --selftest
```

## 5-tier design

| Tier | Name | Wall (min) | Verdict if FAIL |
|------|------|-----------:|-----------------|
| 1 | preflight (port lock kill + impedance 16/16 GREEN + board_health) | 0.8 + 2.5 user reseat | abort, EN+KO recipe |
| 2 | 30s eyes-closed sanity (alpha 1-200 uV^2, mean cross-corr <0.6) | 0.7 | abort, EN+KO recipe |
| 3 | Korean audio cues (say -v Yuna) with 3s settle + 5-count countdown | overlapped | n/a (non-blocking) |
| 4 | direct collect.hexa subprocess (BRAINFLOW_TIMEOUT bypass), HEXA_LOCAL=1 | 60s × 2 | abort, EN+KO recipe |
| 5 | 5 falsifiers (Berger ratio + occipital>frontal + channel sanity + EOG + cross-corr) | 0.1 | report, EN+KO recipe |

## Tier 5 falsifiers

1. **F-BERGER-1**: at least one of O1/O2 has EC alpha / EO alpha >= 1.5
2. **F-BERGER-2**: occipital alpha sum > frontal alpha sum (EC)
3. **F-CHANNEL-SANITY**: every per-channel alpha in [1, 100] uV^2
4. **F-EOG-CLEAN**: frontal RMS / occipital RMS < 5x
5. **F-CROSS-CORR**: max off-diagonal cross-channel correlation < 0.95

## Synthetic selftest 5/5

| Scenario | Expected | Tier 2 | Tier 5 | Correct |
|----------|----------|--------|--------|---------|
| PASS | PASS | PASS | PASS | yes |
| FAIL_O2_anomaly | FAIL | FAIL | FAIL | yes |
| FAIL_board_contam | FAIL | FAIL | FAIL | yes |
| FAIL_EOG | FAIL | PASS | FAIL | yes |
| FAIL_extreme_drift | FAIL | FAIL | FAIL | yes |

`run_selftest()` re-emits these 5 scenarios from numpy-generated waveforms with
deterministic seeds and verifies that the EN+KO recipe is populated for each
failure mode.

## Files

| Path | Role |
|------|------|
| `/Users/ghost/core/anima/tool/transient_py/anima_phase_e_perfect_baseline.py` | orchestrator (raw#9 sister-rule raw#37 transient) |
| `/Users/ghost/core/anima/bin/anima-eeg-baseline.bash` | $0 wrapper (chmod +x, git-tracked) |
| `/Users/ghost/core/anima/state/anima_phase_e_perfect_baseline_protocol_2026_05_05/verdict.json` | landing verdict |

## Honest C3

- **C1 hardware reseat user-side**: script cannot guarantee good electrode
  contact; relies on user to apply saline + verify scalp contact pre-fire.
- **C2 selftest synthetic-only**: real-hardware fire may surface unmodeled
  failures (60 Hz line noise, motion artefact, intermittent dongle dropout).
- **C3 thresholds anima-internal**: alpha 1-100 uV^2, EOG <5x, cross-corr
  <0.95, Berger ratio >=1.5 are derived from 2026-05-03+04 capture audit
  (v6 board contamination + O2/P4 anomaly). Not EEG-literature universal.
- **C4 Yuna locale-dependent**: requires macOS Korean voice; falls back to
  stdout banner if `/usr/bin/say` or Yuna voice missing.
- **C5 baseline != main protocol**: passing this 60s-block baseline is
  necessary but not sufficient for Phase E main 15-min reading protocol;
  longer protocol has separate failure modes (drift, fatigue, cap migration).
- **C6 raw#37 namespace**: orchestrator under `tool/transient_py/`
  (gitignored namespace per anima .own opt-out). Bash wrapper under `bin/`
  IS git-tracked and is the user-facing entrypoint.

## raw compliance

raw#9 (hexa-only sister-rule raw#37 via `tool/transient_py/` namespace) ·
raw#10 (>=5 honest C3) · raw#15 (additive, no edits to existing collect /
impedance / board_health hexa) · raw#37 (transient orchestrator) ·
raw#71 (5 preregistered falsifiers) · raw#91 (synthetic-only selftest claim
preserves real-HW honesty).
