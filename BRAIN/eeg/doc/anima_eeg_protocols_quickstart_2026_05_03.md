# anima-eeg 4-paradigm × audio cue quickstart

작성일: 2026-05-03
대상: OpenBCI All-in-One R&D Bundle (Cyton+Daisy 16ch + Ultracortex Mark IV + Pulse Sensor + Ten20)

## 1. 4-paradigm × audio cue 풀 매트릭스

| Priority | Paradigm | protocol | audio wrapper | hardware | 측정 시간 |
|----------|----------|----------|---------------|----------|----------|
| ⭐⭐⭐ | **eye blink** | `eye_blink_detect.hexa` (524L) | `blink_session_audio.hexa` (360L) | EEG cap | 90s |
| ⭐⭐ | **jaw clench EMG** | `jaw_clench_emg.hexa` (583L) | `jaw_session_audio.hexa` (377L) | EEG cap | 90s |
| ⭐ | **heart rate (PPG)** | `ppg_heart_rate.hexa` (584L) | `ppg_session_audio.hexa` (404L) | Pulse Sensor | 90s |
| 🔄 | **Berger 1929** | `alpha_eyes_closed.hexa` (505L) | `berger_session_audio.hexa` (240L) | EEG cap (electrode prep fix 후) | 60+60s |

총 신규 land: ~3577 LoC hexa.

## 2. 빠른 사용법

### 2.1 eye blink (1순위 — 가장 쉬운 첫 PASS)

```bash
hexa run anima-eeg/protocols/blink_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

**audio cue (90s)**:
- 0–30s: "휴식. 자연스럽게"
- 30–60s: "강하게 깜빡이세요. 일초당 한번씩 삼십 번"
- 60–90s: "휴식. 다시 자연스럽게"

**falsifier**:
- F_BLINK_01: Fp1/Fp2 peak-to-peak > 100 µV
- F_BLINK_02: blink count ∈ [25, 35]
- F_BLINK_03: Fp1/Fp2 > O1/O2

**output**: `anima-eeg/recordings/sessions/blink_audio_90s_<DATE>.npy`
**분석**: `hexa run anima-eeg/protocols/eye_blink_detect.hexa --run --input <npy>`

### 2.2 jaw clench EMG (device sanity check)

```bash
hexa run anima-eeg/protocols/jaw_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

**audio cue (90s)**:
- 0–30s: "휴식. 턱 이완"
- 30–60s: "어금니 꽉 깨무세요. 일초당 한 번씩 삼십 번"
- 60–90s: "휴식. 턱 이완"

**falsifier**:
- F_JAW_01: T7/T8 CLENCH RMS > 300 µV
- F_JAW_02: CLENCH/REST ratio ≥ 5×
- F_JAW_03: T7/T8 > O1/O2 (temporal-dominant)

**honest C3**: EMG ≠ EEG (temporalis/masseter muscle 측정), purist 비판 사전 명시.

**output**: `anima-eeg/recordings/sessions/jaw_audio_90s_<DATE>.npy`
**분석**: `hexa run anima-eeg/protocols/jaw_clench_emg.hexa --run --input <npy>`

### 2.3 heart rate PPG (Bundle Pulse Sensor 활용)

```bash
hexa run anima-eeg/protocols/ppg_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

**audio cue (90s)**:
- 0–30s: "휴식. 정상 호흡"
- 30–60s: "숨을 참으세요"
- 60–90s: "다시 호흡. 회복"

**falsifier**:
- F_PPG_01: amplitude > 100 raw counts
- F_PPG_02: BPM ∈ [40, 180]
- F_PPG_03: |BPM_hold − BPM_rest1| ≥ 5 (HRV sympathetic response)

**honest C3**: NOT EEG (cardiovascular, sanity check only). ANALOG mode 측 Cyton ch6-8 disable.

**Pulse Sensor connection** (3-wire):
| wire | Cyton pin |
|------|-----------|
| Red (Vcc) | 3.3V |
| Black (GND) | GND |
| Purple (Signal) | D11 (analog input, default) |

Sensor 위치: index fingertip 또는 earlobe (LED side flat against skin).

**output**: `anima-eeg/recordings/sessions/ppg_audio_90s_<DATE>.npy`
**분석**: `hexa run anima-eeg/protocols/ppg_heart_rate.hexa --run --input <npy>`

### 2.4 Berger 1929 재시도 (electrode prep fix 후)

```bash
hexa run anima-eeg/protocols/berger_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

**sequence**:
1. 임피던스 측정 (16/16 GREEN 확인)
2. EC 60s "삼 초 후 눈을 감으세요" → 측정 → "측정 끝"
3. 휴식 10s "잠시 쉬세요"
4. EO 60s "삼 초 후 눈을 뜨세요" → 측정 → "측정 완료"

**falsifier**:
- F_BERGER_01: α peak in 7.5-12.5 Hz at O1/O2
- F_BERGER_02: O1/O2 > Fp2 (occipital-dominant)
- F_BERGER_03: EC α power > EO α power × 2 (alpha blocking)

**prereq fix** (이전 0/3 FAIL — DC drift -185mV):
1. 귓불 alcohol wipe (skin oil 제거)
2. EMG/ECG Gel Electrode (Bundle 안) → A1/A2 부착, snap cable
   - SRB2 (white) → A1 (왼쪽 귓불)
   - BIAS  (black) → A2 (오른쪽 귓불)
3. 60-90s 안정 대기 (electrochemical 평형)
4. impedance check 16/16 GREEN
5. Berger 재측정

## 3. 채널 montage (Cyton+Daisy 16ch, OpenBCI 표준)

| Row | pin | 10-20 위치 | 용도 |
|-----|-----|-----------|------|
| 1 | Cyton N1P (Grey) | Fp1 | 전두엽 (frontal) |
| 2 | Cyton N2P (Purple) | Fp2 | 전두엽 |
| 3 | Cyton N3P (Blue) | C3 | 좌 motor cortex |
| 4 | Cyton N4P (Green) | C4 | 우 motor cortex |
| 5 | Cyton N5P (Yellow) | P7 | 좌 두정-측두 |
| 6 | Cyton N6P (Orange) | P8 | 우 두정-측두 |
| 7 | Cyton N7P (Red) | **O1** | 좌 occipital (Berger anchor) |
| 8 | Cyton N8P (Brown) | **O2** | 우 occipital (Berger anchor) |
| 9 | Daisy N1P (Grey) | F7 | 좌 frontal-temporal |
| 10 | Daisy N2P (Purple) | F8 | 우 frontal-temporal |
| 11 | Daisy N3P (Blue) | F3 | 좌 frontal |
| 12 | Daisy N4P (Green) | F4 | 우 frontal |
| 13 | Daisy N5P (Yellow) | **T7** | 좌 temporal (jaw clench) |
| 14 | Daisy N6P (Orange) | **T8** | 우 temporal (jaw clench) |
| 15 | Daisy N7P (Red) | P3 | 좌 parietal |
| 16 | Daisy N8P (Brown) | P4 | 우 parietal |

**Reference electrodes**:
- SRB2 (white) → A1 (왼쪽 귓불)
- BIAS  (black) → A2 (오른쪽 귓불)

## 4. 추천 진행 순서 (한 session)

```bash
# 1. 임피던스 verify (전체 protocol 공통 prereq)
hexa run anima-eeg/impedance_check.hexa --check --port /dev/cu.usbserial-DP04WGIQ

# 2. ⭐⭐⭐ eye blink — 첫 PASS evidence
hexa run anima-eeg/protocols/blink_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy

# 3. ⭐⭐ jaw clench — device chain 강화
hexa run anima-eeg/protocols/jaw_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy

# 4. ⭐ heart rate (Pulse Sensor 연결 후) — Bundle 자원 활용
hexa run anima-eeg/protocols/ppg_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy

# 5. 🔄 Berger 재시도 (electrode prep fix 후)
hexa run anima-eeg/protocols/berger_session_audio.hexa --run \
    --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

총 약 7분 측정 (sleep / cue 포함하면 10분 정도).


1. **N=1 self-experiment** — 통계 power 부재, 개인차 큼, 외부 generalization 불가.
2. **macOS only** — `say -v Yuna` 한국어 cue 의존 (Linux/Windows 측 변경 필요).
3. **EMG/PPG 측 EEG 아님 명시** — jaw clench / PPG 측 device sanity / artifact 검출 용도, 의식측정 (consciousness) 측 indirect.
4. **electrode-prep responsibility** — Bundle 안 montage 측 사용자 직접 부착, 정확도 영향.
5. **Korean grid 60 Hz notch** — EU/Japan-50Hz 환경 측 protocol 측 `--notch 50` 옵션 추가 필요 (현재 hardcoded).

## 6. 다음 cycle 권장

1. **F1 honest baseline calibration** — focus_brainflow_metric.hexa 측 P9 0.4 mistake 패턴 회피, N≥30 labelled trials
2. **HRV (RMSSD/SDNN)** — PPG 5분 + 6 BPM paced breathing (autonomic modulation)
3. **ECG R-peak detection** — earlobe ref pickup (jaw clench 다음 priority)
4. **collect.hexa / eeg_recorder.hexa 측 _session_manager.hexa 통합** — ~120L 중복 제거
5. **mu_rhythm / SSVEP / focus** — Berger PASS 후 (electrode chain 검증 후)

## 7. v6 audit appendix (2026-05-03) — clean_channels filter + rail saturation

v6 paired-symmetric Berger 측정 직후 channel mapping verify BG audit (id `affd5940d63f830f6`) 측 발견:

### 7.1 discovery

v6 EC measurement 측 cc=1.0000 between rows 1 / 6 / 8 observed → 처음 wiring duplication 의심 → **실제 cause: ADC rail saturation** (±187.5 mV clip). 5/16 channels (rows 1, 5, 6, 8, 16) sit at the negative or positive rail; clipped signals collapse to identical noise/quantization patterns → cc=1.0000 artifact. EO v6 측 동일 5 rows railed → stable hardware/electrode contact issue, not per-recording fluke.

### 7.2 rail saturation table

| row | 10-20 | mean (raw counts) | abs_max | suspected cause |
|-----|-------|-------------------|---------|------------------|
| 1   | Fp1   | -98 545           | 101 449 | electrode contact loss / DC drift (cite `fp1_chronic_noise_diagnose_2026_05_03.md`) |
| 5   | P7    | +119 623          | 123 091 | gel desiccation likely (left parieto-temporal) |
| 6   | P8    | -98 656           | 101 558 | gel desiccation likely (right parieto-temporal) |
| 8   | O2    | -98 722           | 101 627 | mastoid ref imbalance — affects F3 alpha-blocking verdict (Berger right-occipital anchor) |
| 16  | P4    | -96 023           | 98 713  | cable strain / contact (Daisy N8P brown) |

### 7.3 clean_channels canonical (standard for all subsequent analysis)

```
clean_channels = [2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]
# = [Fp2, C3, C4, O1, F7, F8, F3, F4, T7, T8, P3]
# 11 of 16 usable
# O1 only (O2 railed) for occipital alpha
# F3/F4/T7/T8 cleanest Daisy frontocentral
```

§3 mapping table 측 spec 그대로, but 분석 측 입력 채널 측 위 11개로 한정. row 1/5/6/8/16 측 drop or mark-unusable.

### 7.4 mandatory pre-processing (alpha analysis)

before any alpha-band PSD:
1. `clean_channels` filter (drop railed 5)
2. **HPF ≥ 0.5 Hz** (raw means up to ±120 mV swamp 8-13 Hz signal — without HPF, alpha PSD measures DC drift not neural oscillation)
3. 60 Hz notch (Korean grid)
4. Welch nperseg=256, Hann

### 7.5 F3 verdict re-analysis with O1-only fallback (TODO)

F3 (EC α power > EO α power × 2) STILL FAIL post channel-mapping verify — alpha-blocking discriminator unstable. O2 (row 8) rail 측 부분 explanation, but O1 (row 7) clean — O1-only fallback reanalysis 측 pending in `state/berger_v6_clean_reanalyze_2026_05_03/`. 즉시 land 측 deferred (별도 cycle).

### 7.6 analyze.hexa auto-rail-detection follow-up TODO

long-term: `analyze.hexa` 측 자동 rail-detection gate 추가 — 임계값 `|mean| > 50000` or `|max| > 150000` 측 railed channel 측 PSD 입력 측 자동 exclude. v6 cycle 측 manual `clean_channels` literal 측 standard, 다음 cycle 측 자동화 spec.

### 7.7 cross-link

- 전체 audit synthesis: `/Users/ghost/core/anima/docs/eeg_v6_audit_synthesis_2026_05_03.md`
- channel mapping verify (BrainFlow vs spec): `/Users/ghost/core/anima/anima-eeg/docs/cyton_daisy_channel_mapping_official_2026_05_03.md`
- sample-rate root cause (IOSSDATALAT fix): `/Users/ghost/core/anima/anima-eeg/docs/sample_rate_root_cause_consolidated_2026_05_03.md`
- Fp1 chronic noise (row 1 rail explanation): `/Users/ghost/core/anima/anima-eeg/docs/fp1_chronic_noise_diagnose_2026_05_03.md`


본 appendix 측 v6 evidence 측 reflect — F3 alpha-blocking 측 still FAIL 유지 (channel-mapping verify 측 sufficient cause 아님). N=1 self-experiment 한도; tier=functional_analog 까지만 promote 가능.

## Files referenced

- `/Users/ghost/core/anima/anima-eeg/protocols/blink_session_audio.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/eye_blink_detect.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/jaw_session_audio.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/jaw_clench_emg.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/ppg_session_audio.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/ppg_heart_rate.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/berger_session_audio.hexa`
- `/Users/ghost/core/anima/anima-eeg/protocols/alpha_eyes_closed.hexa`
- `/Users/ghost/core/anima/anima-eeg/docs/openbci_bundle_ear_clip_options_2026_05_03.md` (electrode prep fix)
- `/Users/ghost/core/anima/anima-eeg/docs/openbci_pragma_practice_2026_05_03.md` (community tips)
- `/Users/ghost/core/anima/anima-eeg/docs/cyton_first_real_session_2026_05_03.md` (첫 실측 spec)
- `/Users/ghost/core/anima/anima-eeg/docs/cyton_daisy_channel_mapping_official_2026_05_03.md` (mapping verify, §7 source)
- `/Users/ghost/core/anima/docs/eeg_v6_audit_synthesis_2026_05_03.md` (full audit synthesis, §7 cross-link)
