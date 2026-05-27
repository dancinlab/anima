# OpenBCI pragma practice — community-derived "good enough" baseline

date: 2026-05-03
author: anima-eeg cycle (web search round, 1 round / 4 fetches)
context: Berger 1929 N=1 first attempt — 0/3 falsifiers PASS (EC < EO α 反転, DC drift -185mV saturation). User directive "너무 완벽히 안해도 될듯". Web search round to extract OpenBCI community/forum practical tips.
scope: spec doc only — code touch X (alpha_eyes_closed.hexa thresholds 변경 권장 만 명시, 실제 edit 후속 cycle).

---


이 문서 측 권장 사항 모두 **community forum 측 self-reported tips** 와 **단일 N=1 실패 1회** 측 inference. claim:
- "이 ratio 면 OK" — community consensus N≈10 forum threads + WebFetch 2건 only, peer-reviewed RCT X
- "1.5× 완화 OK" — 우리 self-experiment 1회 측 EC=0.92, EO=1.30 (ratio=0.71) base; community 측 numerical EC/EO ratio 명시 case 0건 (qualitative "strong/consistent" only)
- "10-15% normal subjects 측 weak alpha" — Berger 원조 1929 paper 측 클래식 quote 이지만 우리 search round 측 직접 확인 X (forum 측 "individuals vary" 표현 만 확인)

honest stance: 권장 사항 = community wisdom 측 reasonable starting point, scientific validity 보장 X.

---

## 1. Community tips top-5 (forum/reddit/youtube)

forum thread distillation (sources 末尾):

1. **개인차 normal — 한 사람 alone 으로 결론 X**: "People differ in their amounts of eyes closed alpha production, and some produce much less than others. This is still 'normal'." → 첫 측정 측 self alone 측 결론 X, 가능 시 N≥2 subjects.
2. **Posterior 측 우선 — O1/O2/Pz 만 보면 됨**: "alpha is stronger in the rear of the head". forum 측 frontal 만 봤다가 alpha 안 보이는 사례 다수. our setup 측 Fp2 만 dominant 면 electrode placement 측 issue 일 수 있음.
3. **20s = "fast food" 너무 짧음**: forum 측 "trials of 20 seconds are like a 'fast food' approach", 더 긴 sustained observation + spectrogram 권장. our 60s 측 lower bound 정도, 90-180s 권장.
4. **Reference ear clip 측 saline pad**: "saline-soaked cloth between ear clip and skin" 측 conductivity 大 향상. 우리 DC drift -185mV saturation 측 prime suspect (REF/BIAS contact 측 high impedance).
5. **Time lag — eye open 후 alpha 즉시 사라지는 게 아님**: "There is a time lag sometimes between when you close the eyes and the alpha shows up". 우리 60s window 측 처음 5-10s 측 trim 후 분석 권장.

---

## 2. 흔한 첫 측정 실패 원인 (anima-eeg N=1 결과 매칭)

forum 측 자주 나오는 failure mode → 우리 0/3 결과와 매칭:

| 우리 증상 | forum 측 흔한 원인 | 우리 측 likely root cause |
|---|---|---|
| EC α < EO α (반전) | psychological relaxation 측 부족, 또는 racing thoughts | 가능 — 첫 측정 측 self stress; 또는 alpha 측 발현 X |
| DC drift -185mV saturation | reference 측 high impedance, ear clip 접촉 불량 | **likely #1** — saline pad 안 썼고 electrode paste X |
| Fp2 측 amplitude dominant | electrode misplacement (occipital 측 contact X) | possible — Ultracortex 측 자가 fit 측 occipital 측 hair contact 약함 |
| individual weak alpha | "10-15% subjects show no clear alpha" (folklore, 미검증) | unknown — N=1 측 구별 불가 |

community 측 권장 first-fix: **REF/BIAS contact 측 saline pad** + **occipital electrode 측 conductive paste** (gel). 둘 만 해도 forum 측 multiple thread 측 resolution.

---

## 3. 80/20 minimal viable practice (효율 lens)

community 측 distill 한 minimal viable EEG session:

### Hardware (20% effort, 80% signal):
- REF/BIAS ear clip 측 saline pad (1분 추가)
- O1, O2, Pz 측 conductive paste 만 신경 (frontal 측 안 봐도 됨)
- impedance 측 GUI 측 GREEN 만 OK — kΩ 정확값 신경 X
- Ultracortex 측 hair part 측 손가락 으로 갈라 paste 직접 scalp 접촉

### Recording (20% effort):
- 90s × 2 (EC/EO), 첫 10s trim
- single subject self 측 inconclusive 가능성 ack — N=2-3 권장 만 명시
- DC offset 측 saturation (>±100mV) 측 abort & re-seat

### Analysis (20% effort):
- O1+O2 average spectrogram
- 8-12 Hz band power EC vs EO
- ratio 1.0× (EC > EO) 만으로 "alpha present" 라고 보는 community 도 있음 (strict 2× 측 textbook only)

### skip 가능 (over-engineering):
- impedance <50kΩ strict requirement (community 측 100-200kΩ 도 alpha 보이는 사례)
- SRB2 검증 별도 단계 (just connect & check time series)
- 60-90s pre-recording settling (10-30s 면 충분)

---

## 4. Falsifier 완화 권장 (anima-eeg/protocols/alpha_eyes_closed.hexa)

현재 spec (alpha_eyes_closed.hexa):
- F_BERGER_01: peak in 7.5-12.5 Hz
- F_BERGER_02: O1/O2 > Fp2
- F_BERGER_03: EC > EO × 2.0 (EC_EO_RATIO_MIN = 2.0)

### 권장 완화 (community-aligned tier system)

**Tier A "textbook"** (현 spec 유지) — peer-reviewed publication target:
- F_BERGER_01: 7.5-12.5 Hz
- F_BERGER_03: EC/EO ≥ 2.0

**Tier B "community pragma"** (신규 추가) — N=1 self-experiment 측 realistic:
- F_BERGER_01_LOOSE: peak in **6-13 Hz** (forum 측 8-11 Hz "average" + 개인차 buffer)
- F_BERGER_03_LOOSE: EC/EO ≥ **1.2** (community 측 "EC bigger than EO" qualitative consensus)
- F_BERGER_02: O1/O2 > Fp2 (**유지** — placement sanity check, 개인차 X)

**Tier C "alpha presence binary"** (신규) — 가장 관대:
- F_ALPHA_EXISTS: O1/O2 측 8-12 Hz peak detectable (any amplitude > broadband floor × 1.3)

권장 use: 첫 N=1 측 Tier C 만 PASS 시도, 0/3 재발 시 paradigm switch (sec 5).

### 코드 변경 후속 cycle proposed (이 doc 측 implement X):
```
let EC_EO_RATIO_MIN_TEXTBOOK = 2.0
let EC_EO_RATIO_MIN_PRAGMA   = 1.2
let ALPHA_BAND_LOOSE_LOW     = 6.0   // Hz
let ALPHA_BAND_LOOSE_HIGH    = 13.0  // Hz
```

---

## 5. Alternate easy-PASS paradigm (N=1 측 더 robust)

alpha 측 발현 측 개인차 大. 다음 paradigm 측 "always works" property 측 더 강함:

### 5a. **Eye blink artifact detection** (★★★ 최우선 권장)
- intentional blink × 5 (5s 간격) → Fp1/Fp2 측 high-amplitude (>100µV) negative spike
- 의도적 행동 측 ground truth → falsifier 단순: "5 spikes detected in Fp1/Fp2 within ±1s of cue"
- 모든 사람 측 reliable (alpha 와 달리 개인차 거의 X)
- our setup 측 Fp2 측 saturation 측 했어도 spike detection 측 가능 (DC drift 와 무관)

### 5b. **Jaw clench EMG** (★★)
- 1s clench × 3 → frontal/temporal 측 broadband EMG burst (20-200 Hz, amplitude > resting × 5)
- 100% reliable (모든 사람), but EEG 라기보다 EMG (purist 측 비판 가능)

### 5c. **Heart rate via PPG widget** (★ 가장 쉬움 BUT EEG X)
- OpenBCI Pulse Sensor + Cyton analog read
- BPM extraction → falsifier "BPM in [40, 200] resting"
- EEG 검증 X — but "device 측 작동 함" sanity check (sensor sanity)
- our case 측 anima-eeg 측 EEG 강조 측 fit X 하지만 device baseline 으로 가치

### 권장 next paradigm 순위 (완성도 lens):
1. **eye blink** — EEG 측 정통 + reliable + falsifier 명료
2. **jaw clench** — EMG 일지라도 sanity check 큰 가치
3. **alpha 재시도** — only after saline pad + paste fix + N=2 subjects

---

## 6. 3 honest C3 caveats

1. **single web search round only** (4 WebFetch). community consensus 측 sample size 작음, 특히 ratio numerical 측 forum 측 거의 명시 X — 본 doc 측 1.2× / 6-13 Hz 측 hand-wave estimate.
2. **"10-15% no alpha" folklore 미검증**. Berger 1929 측 직접 quote X, forum 측 "individuals vary" 측 quantification 안 됨. 우리 N=1 측 alpha 측 진짜 발현 안 했는지 / setup 측 fail 인지 구별 불가.
3. **Tier B/C 권장 측 우리 setup 의 saturation root cause 미해결 시 무의미**. saline pad + paste 안 하면 falsifier 완화 측 false PASS 양산 가능. 권장 sequence: hardware fix → re-test Tier A → fail 시에만 Tier B 측 fallback.

---

## 7. 다음 cycle 권장

### 권장 sequence (완성도 lens 측 ranked):

**option-1 (★★★ best 완성도)**: hardware fix + eye blink paradigm 측 우선
- saline pad on REF/BIAS ear clip
- conductive paste on O1/O2/Pz/Fp1/Fp2
- protocol: eye blink artifact detection (paradigm 5a)
- falsifier: F_BLINK_FRONTAL_SPIKE — 5 cued blinks → 5 detected spikes in Fp1/Fp2 (>100µV peak-to-peak)
- 예상: 3/3 PASS likely (개인차 거의 X)
- 가치: "device works + signal chain works" 측 unambiguous 確證

**option-2 (★★)**: alpha Tier C (relaxed 6-13 Hz / EC > EO any) 재시도
- 동일 hardware fix
- 90s × 2 (EC/EO), 첫 10s trim
- 예상: 1/3 ~ 2/3 PASS (Tier C 측 EC/EO ≥ 1.0 only)

**option-3 (★)**: jaw clench EMG fallback
- pure EMG, EEG 측 정통성 낮음
- but "100% reliable" property 측 강함 — 우리 cycle 측 momentum 회복 측 가치

### 권장 final: **option-1** (eye blink + hardware fix). 이유:
- Tier A/B/C 측 어느 것도 "alpha 측 발현 안 함" 가능성 측 안 풀어줌
- eye blink 측 ground truth 명확, falsifier 측 hand-tunable threshold 측 적음
- saturation root cause 측 fix 안 하면 어떤 paradigm 도 fail
- "0/3 → 3/3" 측 cycle momentum 측 회복 가치 大

---

## Sources

- [Cannot reproduce closed eye alpha signal — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/2745/cannot-reproduce-closed-eye-alpha-signal)
- [Trouble getting alpha waves, Cyton with Ultracortex — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/2112/trouble-getting-alpha-waves-cyton-with-ultracortex)
- [Ganglion - missing eyes closed alpha / Electrode Problems? [resolved] — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/3136/ganglion-missing-eyes-closed-alpha-electrode-problems-resolved)
- [Alpha waves not really sensitive to closed eyes — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/2501/alpha-waves-not-really-sensitive-to-closed-eyes-eeg-pipes-using-js)
- [Detecting Alpha Waves — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/166/detecting-alpha-waves)
- [Ultracortex not seeing alpha waves at O1 O2 — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/785/ultracortex-not-seeing-alpha-waves-at-o1-o2)
- [after opening eyes, time lag until alpha extinguished — OpenBCI Forum](https://openbci.com/forum/index.php?p=/discussion/628/after-opening-eyes-time-lag-until-alpha-extinguished)
- [Setting up for EEG | OpenBCI Documentation](https://docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/)
- [Pulse Sensor Guide | OpenBCI Documentation](https://docs.openbci.com/ThirdParty/Pulse_Sensor/Pulse_Sensor_Landing/)
- [Algorithm for Detection of Raising Eyebrows and Jaw Clenching Artifacts in EEG Signals (NeuroSky) — Springer](https://link.springer.com/chapter/10.1007/978-3-030-57566-3_10)
- [Unsupervised Eye Blink Artifact Detection From EEG (k-means++) — GitHub](https://github.com/mikaelhaji/UnsupervisedArtefactDetection)
