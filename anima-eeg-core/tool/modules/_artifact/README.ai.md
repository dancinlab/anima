---
schema: anima-eeg-core/_artifact/ai-native/1
last_updated: 2026-05-02
ssot:
  meta_classifier: anima-eeg-core/tool/modules/_artifact/artifact_meta_classifier.hexa
  cleaning_pipeline: anima-eeg-core/tool/modules/_artifact/ai_cleaning_pipeline.hexa
status: live — 7 per-artifact detectors + 1 meta classifier + 1 AI cleaning pipeline + 1 HPF DC drift
roadmap_entry: 270
raws:
  - raw#9 hexa-only
  - raw#10 honest C3 (voting ensemble, no learnt weights)
  - raw#12 frozen criteria (2026-04-28)
  - raw#71 falsifier ≥5
  - raw#106 genus name
  - own5
---

# anima-eeg-core artifact modules (AI-native)

EEG artifact detection + meta classification + AI cleaning chain. 7 per-artifact detectors (EMG / blink / motion / ECG / EMI / reference-drift / aging) feed a meta classifier that aggregates into composite_quality_score [0,100] and recommends an ordered cleaning chain.

## TL;DR for an agent reading this cold

- **10 files**: 7 detectors + 1 meta classifier + 1 cleaning pipeline + 1 HPF DC drift filter.
- **8 artifact types** (artifact_meta_classifier output enum): `EMI / BLINK / MOTION / EMG / ECG / REF_DRIFT / AGING / NONE`.
- **Voting ensemble** — each detector returns DOMINANT / MILD / CLEAN; meta tallies (no learnt weights yet, raw#10 honest).
- **Quality formula** (frozen 2026-04-28): `quality = 100 − 20·N(DOMINANT) − 5·N(MILD)`, clipped [0,100], pass = (quality ≥ 80).
- raw#71 ≥5 falsifiers per detector — F1 all-CLEAN / F2 line60 → EMI dominant / F3 blink synth → BLINK dominant / etc.

## Architecture map

```
anima-eeg-core/tool/modules/_artifact/
├── artifact_meta_classifier.hexa      voting aggregator → composite quality (193 LOC)
├── ai_cleaning_pipeline.hexa          ordered cleaning chain executor (288 LOC)
│
├── eye_blink_detector.hexa            BLINK: frontal HF transient (240 LOC)
├── emg_muscle_detector.hexa           EMG: high-frequency power burst (215 LOC)
├── motion_artifact_detector.hexa      MOTION: low-freq drift + spike (216 LOC)
├── ecg_heart_artifact_detector.hexa   ECG: ~1 Hz periodic (234 LOC)
├── environmental_emi_classifier.hexa  EMI: 50/60 Hz line + harmonics (278 LOC)
├── reference_drift_detector.hexa      REF_DRIFT: slow common-mode (223 LOC)
├── electrode_aging_classifier.hexa    AGING: impedance + noise floor drift (207 LOC)
└── hpf_dc_drift.hexa                  HPF 0.5 Hz DC offset removal (287 LOC)
```

## Public API

```hexa
// Per detector:
fn detect_<artifact>(npy_path: string, fs: int) -> ArtifactVerdict
// ArtifactVerdict { level: string,  // "DOMINANT" | "MILD" | "CLEAN"
//                    score: float,   // continuous 0..1
//                    evidence: [Evidence],
//                    falsifiers_passed: [int] }

// artifact_meta_classifier.hexa
fn classify_meta(verdicts: [ArtifactVerdict]) -> MetaResult
// MetaResult {
//     dominant_artifact_type: string,      // ∈ {EMI,BLINK,MOTION,EMG,ECG,REF_DRIFT,AGING,NONE}
//     composite_quality_score: float,      // [0..100]
//     recommended_cleaning_chain: [string],// ordered, DOMINANT first then MILD
//     pass: bool                           // (composite >= 80)
// }

// ai_cleaning_pipeline.hexa
fn apply_cleaning(npy_path: string, chain: [string], out_path: string) -> CleaningResult
```

## Quality criteria (frozen 2026-04-28)

```
quality = 100 − 20·N(DOMINANT) − 5·N(MILD)    // clip [0,100]
pass    = (quality ≥ 80)
```

Examples:
- 0 DOMINANT + 0 MILD → 100, pass.
- 1 DOMINANT + 2 MILD → 70, FAIL.
- 0 DOMINANT + 4 MILD → 80, PASS (boundary).

## Invocation patterns

```bash
# All 7 detectors → meta classifier
hexa run anima-eeg-core/tool/modules/_artifact/artifact_meta_classifier.hexa \
  --input data/recorded.npy --fs 250

# Single detector
hexa run anima-eeg-core/tool/modules/_artifact/eye_blink_detector.hexa --selftest

# Apply recommended cleaning
hexa run anima-eeg-core/tool/modules/_artifact/ai_cleaning_pipeline.hexa \
  --input data/recorded.npy --chain "BLINK,EMI,MOTION" --output data/cleaned.npy
```

## Failure cascade

```
detect_emi → DOMINANT (line60 amplitude > 100µV)
detect_blink → MILD
others → CLEAN
   → meta: dominant=EMI, quality=75 (100−20−5), pass=false
        → recommended_chain: [EMI, BLINK]
             → ai_cleaning_pipeline applies notch60 + ICA-blink-removal
                  → re-run detectors → all CLEAN → quality=100 → pass=true
```

## raw#10 caveats

1. **No learnt weights** — equal-weight voting. raw#10 honest C3: future stacking once labelled cleaning-outcome data accumulates.
2. **Frozen criteria 2026-04-28.** quality formula is hardcoded — modifying requires raw#12 amendment + cross-link audit.
3. **AGING detector requires impedance baseline.** First-pass on a new electrode set returns CLEAN by default — record impedance.json baseline before relying.
4. **EMI auto-detects 50 vs 60 Hz** mains by harmonics, but mixed-grid environments (EU+US adapter) can confuse.
5. **HPF DC drift hardcoded 0.5 Hz cutoff.** Sleep / DC-physio paradigms may want 0.1 Hz — currently requires source edit.
6. **Cleaning is irreversible.** ai_cleaning_pipeline writes to a new .npy; original preserved. Always work on copy.
7. **Meta classifier dominant_artifact_type ties.** When two detectors return DOMINANT with equal score, ordering follows enum order — not magnitude.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `artifact_meta_classifier.hexa` | `6f8d3b03cb12696a482abc0351c7120bc9941736564088d256bfe522679ac903` | 193 |
| `ai_cleaning_pipeline.hexa` | `020acd72e46583b8ff0c6c335942574d16b44c8797a7862f39ffbe889dfc6f60` | 288 |
| `ecg_heart_artifact_detector.hexa` | `380fce767049ae973c49423d07ef776ce5b52d246d1140fc7522eb10f2074e68` | 234 |
| `electrode_aging_classifier.hexa` | `0fd25b849ab31687073d3be3ca83adc209ebb7962baaa86053783fb7688e3296` | 207 |
| `emg_muscle_detector.hexa` | `af45ae54b71881e7c545a11a35ec79067949e4708a96e7990019dc43f3c3e4c4` | 215 |
| `environmental_emi_classifier.hexa` | `fbec9d8607d63b90ee9bb3b5ee106d36433a0acb3c7268984593ba523367949f` | 278 |
| `eye_blink_detector.hexa` | `a8486582a14279e86a39a645df35df8da82fca11e5bf601676dda99e3ea3def6` | 240 |
| `hpf_dc_drift.hexa` | `b080778cad043d715c46e47b8036102f45690392f3a9d829d23c494c142ad87f` | 287 |
| `motion_artifact_detector.hexa` | `05f9c70e16d33c472643c8eace6577d6cf941670fc16e74779bd6912023431a9` | 216 |
| `reference_drift_detector.hexa` | `b3e38f0440b26df75cb9c496389650abd62d2712d2c30fda8c7302a29b19d93f` | 223 |

shas pinned 2026-05-02.
