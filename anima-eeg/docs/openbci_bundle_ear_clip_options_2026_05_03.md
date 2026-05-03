# OpenBCI All-in-One R&D Bundle — ear clip / reference fix 옵션

작성일: 2026-05-03
용도: Berger 1929 측정 실패 (DC drift -185mV root cause) fix
관련 doc:
- `anima-eeg/docs/cyton_first_real_session_2026_05_03.md`
- `anima-eeg/docs/openbci_pragma_practice_2026_05_03.md`

## Bundle 보유 inventory (사용자 확인됨)

| Item | QTY | 용도 |
|------|-----|------|
| Cyton+Daisy 16-channel + battery + charger | 1 | 본 보드 |
| Ultracortex Mark IV EEG Headset Pro-Assembled 16ch | 1 | 16ch dry headset (본 측정용) |
| EEG Headband Kit | 1 | 추가 headband |
| Gold Cup Electrodes (EEG/EMG/ECG) | 2 | ⭐ reference 용 (A1/A2 귓불) |
| EMG/ECG Snap Electrode Cables | 2 | snap 케이블 |
| EMG/ECG Gel Electrodes pack | 2 | ⭐⭐⭐ 일회용 gel sticker (가장 쉬움) |
| Dry EEG Comb Electrodes pack | 1 | dry 옵션 |
| Pulse Sensor (Heart-Rate Monitor) | 1 | device sanity check |
| Ten20 Paste Jar 8 oz | 1 | gold cup 용 conductive paste |

## Berger fail root cause

직전 측정 (2026-05-03):
- F_BERGER_03: EC α power < EO α power (반대, 0/3 falsifier PASS)
- DC drift: P4 -185mV, O2 -182mV
- 진단: REF/BIAS 측 contact 불량 → reference 측 saturation → 모든 채널 floating noise

해결 = ear clip / reference electrode 정확 부착.

## Fix 옵션 3가지 (완성도 lens ranked)

### ⭐⭐⭐ 옵션 1: EMG/ECG Gel Electrodes (가장 쉬움)

```
1. Gel electrode sticker 2개 꺼내기 (Bundle 안에 있음)
2. 알코올 wipe 로 귓불 (양쪽) skin oil 제거
3. A1 (왼쪽 귓불) + A2 (오른쪽 귓불) 에 각각 하나씩 부착
4. Snap cable 연결:
   - SRB2 (흰색 wire) → A1 (왼쪽)
   - BIAS  (검정 wire) → A2 (오른쪽)
5. 60-90초 대기 (skin-electrode 평형)
6. 측정 시작
```

**장점**:
- 즉시 사용 (paste 안 필요)
- 안정적 contact
- gel 적정 농도 보장 (vendor pre-applied)
- DC drift 최소화

**단점**:
- 일회용 (재사용 X)
- pack 측 stock 소진 시 추가 구매

### ⭐⭐ 옵션 2: Gold Cup + Ten20 paste

```
1. Gold cup 2개 준비
2. Ten20 paste 를 cup 안 그릇 가득 채움 (overflow OK)
3. 귓불 양쪽에 단단히 부착 (paste 가 두피 접촉)
4. SRB2/BIAS wire 연결 (옵션 1 동일)
5. 60-90초 대기
6. 측정
```

**장점**:
- 재사용 가능 (cup + paste)
- paste 양 정밀 조정 가능
- 장시간 측정 안정

**단점**:
- 부착 시간 더 걸림
- paste 마름 (30-60분 후 보충 필요)
- cup-귓불 sealing 어려움 (개인차)

### ⭐ 옵션 3: 그냥 eye blink 가기 (Berger 우회)

```
1. ear clip / reference 측 fix 안 함
2. eye_blink_detect.hexa protocol 사용 (별도 BG land 중)
3. Fp1/Fp2 amplitude 100-300 µV (noise 압도)
4. F_BLINK_01/02/03 falsifier PASS 확보
```

**장점**:
- ear clip / reference 정밀도 영향 적음
- 첫 PASS evidence 빠르게 확보
- 사용자 control (의도적 깜빡임)

**단점**:
- Berger 1929 검증은 미해결
- α-rhythm 검출 안 됨
- 다른 spectral protocol (mu/SSVEP) 도 같은 reference 문제 가능

## 추천 sequence

### Path A: root cause fix 우선 (추천)
1. **옵션 1** (Gel Electrodes) 적용
2. Impedance check 재실행 (16/16 GREEN 목표)
3. Berger 90s × 2 재측정
4. 분석 → F_BERGER_01/02/03 verdict
5. PASS 시 mu_rhythm.hexa / SSVEP / focus 진행

### Path B: momentum 우선
1. **옵션 3** (eye blink) 으로 첫 PASS 확보
2. 그 후 옵션 1 적용 → Berger 재시도
3. spectral protocol 시리즈

⭐ Path A 추천 — Berger 재현 실패 reason 이 hardware 측이면 다른 spectral protocol 도 같은 문제로 fail. fix path 가 더 productive.

## raw#10 honest C3 caveats

1. **개인차**: 귓불 두께 / 머리카락 / 피부 type 측 contact 영향. gel electrode 도 sweaty skin 측 release 빠름.
2. **첫 측정 시 60-90s 대기 강제**: skin-electrode 전기화학 평형 도달까지 multi-mV DC drift 정상.
3. **Pulse Sensor 별도 device sanity**: heart rate (60-80 BPM) 측정으로 board↔software 통신 검증 가능 — Berger 와 무관하지만 첫 PASS evidence 후보.

## Files referenced

- `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_ec_60s_2026_05_03.npy` (실패 evidence)
- `/Users/ghost/core/anima/anima-eeg/recordings/sessions/berger_eo_60s_2026_05_03.npy` (실패 evidence)
- `/Users/ghost/core/anima/anima-eeg/protocols/alpha_eyes_closed.hexa` (Berger protocol)
- `/Users/ghost/core/anima/anima-eeg/protocols/eye_blink_detect.hexa` (옵션 3, BG land 중)
- `/Users/ghost/core/anima/anima-eeg/docs/openbci_pragma_practice_2026_05_03.md` (community tips)
