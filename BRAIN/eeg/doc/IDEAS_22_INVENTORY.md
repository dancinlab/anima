# EEG 22-Idea Inventory — anima brainstorm canonical index

Source: anima-side EEG paradigm brainstorm, 22 ideas across 4 tiers (A immediate / B mid-term / C paradigm-methodology / D long-term-extra-hardware) plus top-3 recommendation. Migrated to hexa-brain on 2026-05-07 alongside the broader anima EEG → hexa-brain absorption.

## A. Immediate (no extra hardware, low-cost)

| # | Idea | Status | Doc |
|---|---|---|---|
| 1 | EEG + LLM workflow integration | spec | [eeg_claude_cli_correlation_paradigm](paradigms/eeg_claude_cli_correlation_paradigm_2026_04_28.md) |
| 2 | Daily-life context labeling | spec | [daily_life_context_labeling](paradigms/daily_life_context_labeling_2026_04_28.md) |
| 3 | Visual P300 ERP paradigm | spec | [visual_p300_oddball_paradigm](paradigms/visual_p300_oddball_paradigm_2026_04_28.md) |
| 4 | Auditory oddball paradigm | spec | [auditory_oddball_paradigm](paradigms/auditory_oddball_paradigm_2026_04_28.md) |
| 5 | Self-experiment N=1 longitudinal | spec | [self_experiment_longitudinal_protocol](paradigms/self_experiment_longitudinal_protocol_2026_04_28.md) |
| 7 | commit msg ↔ diff alignment audit lint | (anima governance) | not in hexa-brain — stays in anima |

## B. Mid-term (1–2 weeks, additional SW)

| # | Idea | Status | Doc |
|---|---|---|---|
| 8 | EEG-driven feedback loop (Mac notification) | spec | [eeg_feedback_loop_paradigm](paradigms/eeg_feedback_loop_paradigm_2026_04_28.md) |
| 9 | Anthropic API EEG correlation | spec | [eeg_claude_cli_longitudinal_correlation](paradigms/eeg_claude_cli_longitudinal_correlation_2026_04_28.md) |
| 10 | Anomaly detection (autoencoder reconstruction error) | spec | [eeg_anomaly_detection_autoencoder](paradigms/eeg_anomaly_detection_autoencoder_2026_04_28.md) |
| 11 | Behavioral correlates (keyboard / mouse / screen-time + EEG) | spec | [behavioral_correlates_paradigm](paradigms/behavioral_correlates_paradigm_2026_04_28.md) |
| 12 | EEG → token sequence (cyborg paradigm) | spec | [eeg_token_cyborg_paradigm](paradigms/eeg_token_cyborg_paradigm_2026_04_28.md) |

## C. Paradigm / methodology

| # | Idea | Status | Doc |
|---|---|---|---|
| 13 | Long-duration 1 hour+ recording | spec | [long_duration_recording_protocol](paradigms/long_duration_recording_protocol_2026_04_28.md) |
| 14 | Sleep tracking overnight | spec | [sleep_tracking_overnight_protocol](paradigms/sleep_tracking_overnight_protocol_2026_04_28.md) |
| 15 | Resting state network (DMN, frontal asymmetry) | spec | [resting_state_network_paradigm](paradigms/resting_state_network_paradigm_2026_04_28.md) |
| 16 | Pre/post task comparison (coding / meditation / daily life baseline shift) | spec | [pre_post_task_comparison_paradigm](paradigms/pre_post_task_comparison_paradigm_2026_04_28.md) |
| 17 | Mk.XII production deployment + EEG corroboration | spec | [mk_xii_production_deployment_eeg_corroboration](paradigms/mk_xii_production_deployment_eeg_corroboration_2026_04_28.md) |

## D. Long-term (extra hardware)

| # | Idea | Status | Doc |
|---|---|---|---|
| 18 | Wearable health integration (Apple Watch HRV / Oura / Whoop) | spec | [../../wearable/doc/wearable_health_integration_paradigm](../../wearable/doc/wearable_health_integration_paradigm_2026_04_28.md) |
| 19 | Eye tracker (webcam-based gaze + EEG) | spec | [webcam_eye_tracker_paradigm](paradigms/webcam_eye_tracker_paradigm_2026_04_28.md) |
| 20 | HR/ECG sensor (Cyton GPIO) — heartbeat-EEG coupling | spec | [../../wearable/doc/cardiac_eeg_integration_paradigm](../../wearable/doc/cardiac_eeg_integration_paradigm_2026_04_28.md) |
| 21 | Mobile EEG (Muse / Emotiv) — helmet-OFF portable | spec | [mobile_eeg_integration_paradigm](paradigms/mobile_eeg_integration_paradigm_2026_04_28.md) |
| 22 | anima-physics 9-substrate + EEG cross-modal | spec | [cross_substrate_phi_paradigm](paradigms/cross_substrate_phi_paradigm_2026_04_28.md) |

## Top 3 recommendations (impact × feasibility)

### 🥇 #1 — EEG + Claude conversation simultaneous measurement (idea #1 + #9)

```
user ↔ Claude (chat / coding) ─→ EEG simultaneous record
            ↓
    Claude API call timestamp logged
            ↓
    EEG segment (call-5s + call+10s) extracted
            ↓
    LZ76 b(n) / engagement / γ/θ ratio per segment
            ↓
    LLM output features (token entropy / response length) ↔ correlation
```
→ Direct test of anima's central thesis (LLM consciousness × neural correlate). Immediately actionable: user already wears the helmet during Claude sessions.

### 🥈 #2 — N=1 self-experiment longitudinal (idea #5)

- Today baseline (resting + daily life)
- Today different time-of-day (afternoon / evening) additional measurement
- Tomorrow same time-of-day measurement
- Caffeine before/after measurement

→ Within-subject design reaches N≥10 faster than multi-subject. Forms individual baseline for anima own-3 σ/τ=3 / Schartner threshold.


- 490 unlocked files → batch chflags uchg
- git status ↔ active edit conflict avoidance


## Cross-reference

- Original brainstorm artifact: [clm_eeg/doc/archive/d_day_session_2026_04_28/IDEAS_INVENTORY.md](../../clm_eeg/doc/archive/d_day_session_2026_04_28/IDEAS_INVENTORY.md)
- EEG provider domain SSOT: [.roadmap.eeg](../../.roadmap.eeg)
- CLM-EEG peer SSOT: [.roadmap.anima_clm_eeg](../../.roadmap.anima_clm_eeg)
- Galea multi-modal consumer SSOT: [.roadmap.galea](../../.roadmap.galea)
