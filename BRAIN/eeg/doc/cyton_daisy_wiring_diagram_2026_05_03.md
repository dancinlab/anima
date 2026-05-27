# Cyton + Daisy 16ch wiring diagram (Ultracortex Mark IV + Y-Splitter + Mastoid reference)

작성일: 2026-05-03 (v2: 사용자 실제 layout 반영 + mastoid option)
대상: OpenBCI All-in-One R&D Bundle (Cyton + Daisy + Ultracortex Mark IV + Y-Splitter)
관련 doc:
- `anima-eeg/docs/openbci_bundle_ear_clip_options_2026_05_03.md`
- `anima-eeg/docs/openbci_pragma_practice_2026_05_03.md`
- `anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md`

## 1. Cyton 보드 (사용자 실제 layout, 하단 row only)

```
═══════════════════════════════════════════════════════════════════
                 CYTON 보드 (channels 1-8 + SRB + BIAS)
═══════════════════════════════════════════════════════════════════

  TOP ROW (상단 11핀):  ❌ 사용 안 함 (전부 빈 칸)

  BOTTOM ROW (하단 11핀):
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬──────┬─────┐
  │ N1P │ N2P │ N3P │ N4P │ N5P │ N6P │ N7P │ N8P │ SRB │ BIAS │  -  │
  │  ⓖ │  ⓟ │  ⓑ │  ⓖ │  ⓨ │  ⓞ │  ⓡ │  ⓒ │  ⓦ │  ⓑ  │ 빈  │
  └──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴───┬──┴─────┘
     │     │     │     │     │     │     │     │     │      │
     Fp1   Fp2   C3    C4    P7    P8    O1    O2    │      │
     회색  보라  파랑  초록  노랑  주황  빨강  갈색  │      │
                                                      │      │
                                            (아래 reference 참조)
```

## 2. Daisy 보드 (사용자 실제 layout, 하단 row only)

```
═══════════════════════════════════════════════════════════════════
                  DAISY 보드 (channels 9-16 + SRB share)
═══════════════════════════════════════════════════════════════════

  TOP ROW (상단 11핀):  ❌ 사용 안 함 (전부 빈 칸)

  BOTTOM ROW (하단 11핀):
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │ N1P │ N2P │ N3P │ N4P │ N5P │ N6P │ N7P │ N8P │ SRB │  -  │  -  │
  │  ⓖ │  ⓟ │  ⓑ │  ⓖ │  ⓨ │  ⓞ │  ⓡ │  ⓒ │  ⓦ │ 빈  │ 빈  │
  └──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴──┬──┴─────┴─────┘
     │     │     │     │     │     │     │     │     │
     F7    F8    F3    F4    T7    T8    P3    P4   ⓦ ← Y-Splitter share
     회색  보라  파랑  초록  노랑  주황  빨강  갈색
```

## 3. Reference wiring (Y-Splitter 합치기)

```
═══════════════════════════════════════════════════════════════════
                    REFERENCE WIRING
═══════════════════════════════════════════════════════════════════

  Cyton 하단 9번 (SRB) ──── 흰색 wire ────┐
                                            │
  Daisy 하단 9번 (SRB) ──── 흰색 wire ────┤
                                            │
                                            ▼
                                   [Y-Splitter 합치기]
                                            │
                                            ▼
                                  [ear clip 또는 Gel Electrode]
                                            │
                                            ▼
                                  ⭐ A1 또는 M1 (왼쪽)
                                  (linked SRB reference)


  Cyton 하단 10번 (BIAS) ─── 검정 wire ───→ [ear clip / Gel Electrode] ──→ A2 또는 M2 (오른쪽)
                                                                            (active cancel)
```

## 4. ⭐ Reference 위치 비교 — Mastoid 권장

| 위치 | 안정성 | 학술 표준 | DC drift | Bundle 측 부착 | 추천 |
|------|--------|----------|----------|----------------|------|
| **A1/A2 귓볼** | ⭐⭐ (얇고 움직임) | ⭐⭐ | 큼 (-185mV 등) | ear clip ✅ | 기본 (간단) |
| **M1/M2 mastoid** | ⭐⭐⭐⭐⭐ (단단한 뼈) | ⭐⭐⭐⭐⭐ | **작음** | Gel Electrode ✅ | **⭐ 1순위!** |
| Cz 정수리 | ⭐⭐⭐ | ⭐⭐ (CAR 용) | - | cap 측 N/A | software re-ref |
| 코끝 (Nose) | ⭐⭐⭐⭐ | ⭐⭐⭐ | 작음 | 부착 어려움 | rare |
| 이마 (Fpz) | ⭐⭐⭐ | ⭐ (EEG 오염) | 중간 | Gel Electrode ✅ | 비추천 |

### Mastoid (귀 뒤 뼈) 추천 이유

1. **DC drift 측 거의 0** — 단단한 뼈, 평형 빠름
2. **Motion artifact 측 minimal** — 움직여도 contact 유지
3. **머리카락 영향 X** — paste/Gel 측 직접 skin contact
4. **학술 publication 측 표준** — Berger 1929 + 현대 EEG paper 측 mastoid 일반
5. **Bundle 측 EMG/ECG Gel Electrode 측 부착 쉬움** (snap)

### Mastoid 위치 찾는 방법

```
        귀 ↓
   ┌────────────┐
   │            │
   │   👂      │
   │     /\    │ ← 귀
   │    /  \   │
   │            │
   │     ●     │ ← 약 1-2cm 뒤, 1cm 아래
   │   M1/M2   │   단단한 뼈 (mastoid bone)
   └────────────┘
```

1. 귀 뒤 만져보기
2. 귓불 뒤쪽 → 귀 아래 약간 → 단단한 **뼈** 느낌
3. 머리카락 적은 곳 (시작점 근처)
4. 좌우 mirror — 양쪽 동일 위치

## 5. 색상 범례

```
ⓦ 흰색 (White)   = SRB reference wire (Cyton 9번 + Daisy 9번)
ⓑ 검정 (Black)  = BIAS active cancel wire (Cyton 10번)
ⓖ 회색 (Grey)   = N1P channel (Fp1 / F7)
ⓟ 보라 (Purple) = N2P channel (Fp2 / F8)
ⓑ 파랑 (Blue)   = N3P channel (C3 / F3)
ⓖ 초록 (Green)  = N4P channel (C4 / F4)
ⓨ 노랑 (Yellow) = N5P channel (P7 / T7)
ⓞ 주황 (Orange) = N6P channel (P8 / T8)
ⓡ 빨강 (Red)    = N7P channel (O1 / P3)
ⓒ 갈색 (Brown)  = N8P channel (O2 / P4)
```

## 6. 종합 setup (사람 머리 시야)

```
                       ┌────────────────┐
                       │   Ultracortex  │
                       │   Mark IV cap  │
                       │  (16 channel)  │
                       │                │
                       │   ⓖFp1 ⓟFp2   │ ← Cyton N1P/N2P
                       │   ⓖF7  ⓟF8    │ ← Daisy N1P/N2P
                       │   ⓑF3  ⓖF4    │ ← Daisy N3P/N4P
                       │   ⓑC3  ⓖC4    │ ← Cyton N3P/N4P
                       │   ⓨT7  ⓞT8    │ ← Daisy N5P/N6P
                       │   ⓨP7  ⓞP8    │ ← Cyton N5P/N6P
                       │   ⓡP3  ⓒP4    │ ← Daisy N7P/N8P
                       │   ⓡO1  ⓒO2    │ ← Cyton N7P/N8P
                       │                │
                       └───┐         ┌──┘
                           │         │
                           ▼         ▼
                       (왼쪽 귀 뒤)  (오른쪽 귀 뒤)
                          M1            M2
                          │             │
                          ▼             ▼
                  Gel Electrode    Gel Electrode
                  (SRB linked)     (BIAS)
                          │             │
                          │             │
                          │             └─ Cyton 하단 10번 (BIAS, 검정)
                          │
                  [Y-Splitter]
                          ├── Cyton 하단 9번 (SRB, 흰색)
                          └── Daisy 하단 9번 (SRB, 흰색)
```

## 7. 채널 — 위치 — 색상 — protocol 매핑

| Channel | 핀 위치 | wire 색상 | 10-20 | 우리 protocol 측 anchor |
|---------|---------|----------|-------|------------------------|
| 1 | Cyton 하단 N1P | 회색 (Grey) | Fp1 | **eye blink** ⭐ |
| 2 | Cyton 하단 N2P | 보라 (Purple) | Fp2 | **eye blink** ⭐ |
| 3 | Cyton 하단 N3P | 파랑 (Blue) | C3 | mu rhythm |
| 4 | Cyton 하단 N4P | 초록 (Green) | C4 | mu rhythm |
| 5 | Cyton 하단 N5P | 노랑 (Yellow) | P7 | - |
| 6 | Cyton 하단 N6P | 주황 (Orange) | P8 | - |
| 7 | Cyton 하단 N7P | 빨강 (Red) | **O1** | **Berger 1929** ⭐ |
| 8 | Cyton 하단 N8P | 갈색 (Brown) | **O2** | **Berger 1929** ⭐ |
| 9 | Daisy 하단 N1P | 회색 | F7 | - |
| 10 | Daisy 하단 N2P | 보라 | F8 | - |
| 11 | Daisy 하단 N3P | 파랑 | F3 | - |
| 12 | Daisy 하단 N4P | 초록 | F4 | - |
| 13 | Daisy 하단 N5P | 노랑 | **T7** | **jaw clench EMG** ⭐ |
| 14 | Daisy 하단 N6P | 주황 | **T8** | **jaw clench EMG** ⭐ |
| 15 | Daisy 하단 N7P | 빨강 | P3 | - |
| 16 | Daisy 하단 N8P | 갈색 | P4 | - |
| **Reference (SRB)** | **Cyton 하단 9번 + Daisy 하단 9번** | **흰색 (White) × 2** | **Y-Splitter → A1 또는 M1** | 모든 paradigm 공통 |
| **Active cancel (BIAS)** | **Cyton 하단 10번** | **검정 (Black)** | **A2 또는 M2** | 모든 paradigm 공통 |

## 8. 사용자 손 작업 (mastoid 추천 sequence)

### Step 1: 알코올 wipe
- 양쪽 mastoid (귀 뒤 단단한 뼈) 측 알코올 솜으로 청소
- skin oil / 화장품 / 머리카락 비키기

### Step 2: Gel Electrode + Snap cable 부착
1. **Bundle 측 EMG/ECG Gel Electrode 2장** 측 protective film 떼기
2. **Snap cable 2개** 측 Gel Electrode 측 snap 연결
3. **왼쪽 mastoid (M1)**:
   - Cyton 하단 9번 (SRB, 흰) + Daisy 하단 9번 (SRB, 흰) → Y-Splitter → Snap cable → Gel Electrode → 부착
4. **오른쪽 mastoid (M2)**:
   - Cyton 하단 10번 (BIAS, 검정) → Snap cable → Gel Electrode → 부착

### Step 3: 60-90초 안정 대기
- electrochemical 평형 (DC drift 자연 감소)
- Gel Electrode 측 ear clip 보다 평형 빠름 (~30-60초도 OK)

### Step 4: Wire seating 확인
- Cyton 하단 9번/10번 측 wire 단단히 꽂혔는지
- Daisy 하단 9번 측 wire 단단히 꽂혔는지
- Y-Splitter 측 양쪽 input + output 측 헐렁 X

### Step 5: Impedance verify
```bash
hexa run anima-eeg/impedance_check.hexa --check --port /dev/cu.usbserial-DP04WGIQ
```
→ 16/16 GREEN 목표

### Step 6: 측정 시작
```bash
# 1순위: eye blink (가장 robust)
hexa run anima-eeg/protocols/blink_session_audio.hexa --run \
  --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy

# 그 후: Berger 재시도
hexa run anima-eeg/protocols/berger_session_audio.hexa --run \
  --port /dev/cu.usbserial-DP04WGIQ --board cyton_daisy
```

## 9. 핵심 root cause 진단 (Berger 1929 fail 0/3)

이전 측정 (`berger_ec_60s_2026_05_03.npy`) 측 0/3 falsifier PASS:
- F_BERGER_03: EC α power < EO α power (반대)
- DC drift: P4 -185mV, O2 -182mV

진단 (사용자 wiring 확인 후):
- ✅ Wiring 측 OpenBCI 정통 패턴 (SRB Y-Splitter + BIAS 단일)
- ❌ **Reference contact 약함** = Ear clip 측 귓볼 측 헐렁한 contact + DC drift

### 가능한 root cause (ranked)

| 가능성 | 진단 | Fix |
|--------|------|-----|
| ⭐⭐⭐ **Ear clip 측 귓볼 contact 약함** | DC drift -185mV 측 가장 가능성 큼 | **Mastoid 측 Gel Electrode 교체** |
| ⭐⭐ **Electrochemical 평형 미도달** | 측정 즉시 시작 | 60-90초 대기 |
| ⭐⭐ **Cap fit 측 channel contact 부족** | 일부 channel saturation | cap 다시 fit + paste 보충 |
| ⭐ **Y-Splitter 측 contact resistance** | 분기점 측 작은 impedance | 단단히 꽂기 |


1. **N=1 self-experiment** — single-subject, statistical power 부재
2. **사용자 보드 layout 측 SRB/BIAS 측 하단 row** — OpenBCI Cyton revision 측 다를 수 있음 (사용자 확인됨)
3. **Mastoid 측 anatomical individual variance** — 일부 사용자 측 mastoid 측 평평하거나 hairline 측 가까움
4. **Korean 60Hz grid notch hardcoded** — EU/Japan 50Hz 환경 측 protocol 측 별도 옵션 필요
5. **Y-Splitter 측 contact resistance** — 1M→2F 분기 측 small impedance 추가, 정밀 측정 측 고려

---

## 11. ⭐ Official OpenBCI docs audit (2026-05-03 추가)

**audit 의도**: 사용자 wiring 측 OpenBCI 정통 패턴 인지 vendor docs 측 cross-check.
**source**: `references/Documentation/website/docs/` (local clone) + `docs.openbci.com` live + `references/V3_Hardware_Design_Files/`

### 11.1 Cyton 11핀 layout (V3 hardware) — OpenBCI 공식

OpenBCI Cyton board (V3 = "32bit Board" rebrand, 2015 schematic) 측 11핀 header 측 **bottom row** 측:

| 핀 # | label | function | wire color (kit) |
|------|-------|----------|------------------|
| 1-8  | N1P–N8P | Channel 1-8 positive input | gray, purple, blue, green, yellow, orange, red, brown |
| 9    | **SRB** | SRB2 reference input (default ON) | white |
| 10   | **BIAS** | active common-mode cancel (≈ ground) | black |
| 11   | (unused) | typically 빈 칸 | — |

- `references/Documentation/website/docs/AddOns/Headwear/01-Ultracortex-Mark-IV.md` L351-L362 — `Bottom SRB pin (SRB2)` + `Bottom BIAS pin` 명시
- `references/Documentation/website/docs/GettingStarted/Biosensing-Setups/01-EEG-Setup.md` L55-L60 — "white → SRB2 (bottom SRB pin)" / "black → bottom BIAS pin"
- `references/V3_Hardware_Design_Files/OpenBCI Cyton Designs/OpenBCI 32bit.sch` strings: `IN1P..IN8P`, `SRB1`, `SRB2`, `BIAS_REF`, `BIAS_DRV`, `BIAS_OUT`, `BIAS_INV` (ADS1299 schematic netnames 직접 확인)

**Top row (상단 11핀)**: PIC32 program/SPI/RFduino program pins 등 — biosensing electrode 용도 X. 사용자 측 "상단 row 미사용" 측 100% 정통.

**V3 vs V4**: 사용자 보드 = V3 (Bundle, 2015–현재). V4 측 별도 hardware revision 부재 (Cyton 측 V3 단일, 2023 rebrand "Cyton" — `references/V3_Hardware_Design_Files/OpenBCI Cyton Designs/READ_ME.md` L3 인용: "**32bit Board** rebrand. NO difference between the two").

### 11.2 Daisy SRB share 메커니즘 — Y-Splitter 측 official 패턴

**Daisy 측 자체 ADS1299 chip + 자체 SRB2 pin** — Cyton SRB 측 internal connect X. 즉 Daisy 9-16 channel 측 Daisy-side SRB2 측 reference, Cyton 1-8 channel 측 Cyton-side SRB2 측 reference. Y-Splitter 측 **두 SRB pin 측 외부 ganging** (electrically tie) 하여 single common reference 측 보장.

cite (vendor self):
- `references/Documentation/website/docs/GettingStarted/Boards/011-Daisy_Getting_Started_Guide.md` L43-L51:
  > "The Y-Splitter connects the bottom `SRB` pin of the Daisy Board to the bottom `SRB` pin of the Cyton Board. The single end of the Y-Splitter connects to a reference point i.e. the earlobe or mastoid bone."
- `references/Documentation/website/docs/AddOns/Headwear/01-Ultracortex-Mark-IV.md` L439, L456 — Cyton SRB ⊕ Daisy SRB 측 Y-Splitter 측 ganged → 단일 ear clip reference
- `references/Documentation/website/docs/AddOns/Headwear/Gelfree_Electrode_Cap_Tutorial.md` L36 — 동일 ganging 명시
- live `docs.openbci.com/GettingStarted/Boards/DaisyGS/` (2025-05-09 update) — 동일 텍스트 confirmed

**BIAS 측 단일 wire**: Cyton bottom BIAS pin only. Daisy BIAS pin 측 internal pass-through (Cyton schematic 측 `BIAS_DRV`, `BIAS_OUT` 측 board-to-board SPI header 측 share) — 별도 wire 부착 X. 사용자 wiring 측 정통.

### 11.3 Reference 위치 측 OpenBCI 권장 — earlobe = primary, mastoid = equivalent option

**earlobe (A1/A2)**: Cyton/Daisy getting-started + EEG-Setup 측 1순위 예시 (gold cup ear clip).
- `EEG-Setup.md` L70-L72: "apply this electrode to either one of your earlobes (either A1 or A2 ...)"
- `EEG-Setup.md` L90: BIAS → 반대쪽 earlobe

**mastoid**: Daisy guide + Gelfree cap 측 동등 option 명시.
- `011-Daisy_Getting_Started_Guide.md` L53: "**Usually, the earlobe or mastoid is used** ... low electrical signals"
- 학술 표준 (10-20 system): A1/A2 ear ≡ M1/M2 mastoid (자주 호환 사용)

**verdict**: OpenBCI 측 둘 다 권장. mastoid 측 motion artifact 측 적고 DC drift 측 작은 측 academic literature 통설 — 사용자 doc v2 측 mastoid 측 1순위 권장 측 정통.

### 11.4 사용자 wiring verdict

| 항목 | 사용자 setup | OpenBCI 공식 패턴 | verdict |
|------|-------------|------------------|---------|
| Cyton bottom 1-8 → N1P-N8P | ✅ | ✅ | **정통** |
| Cyton bottom 9 → SRB (white) | ✅ | ✅ | **정통** |
| Cyton bottom 10 → BIAS (black) | ✅ | ✅ | **정통** |
| Daisy bottom 1-8 → N1P-N8P | ✅ | ✅ | **정통** |
| Daisy bottom 9 → SRB (white) | ✅ | ✅ | **정통** |
| Daisy bottom 10 (BIAS) → 미연결 | ✅ | ✅ (internal pass-through) | **정통** |
| Y-Splitter (2 SRB → 1 ear) | ✅ | ✅ | **정통** |
| BIAS 단일 wire → 반대쪽 ear | ✅ | ✅ | **정통** |
| Top row 미사용 | ✅ | ✅ (program/SPI 전용) | **정통** |

**결론**: 사용자 wiring 측 **OpenBCI Daisy Getting Started Guide + Mark IV tutorial 측 100% canonical pattern**. 변경 권장 부분 **없음**. Berger 0/3 PASS 측 wiring 문제 X — root cause 측 reference contact / electrochemical 평형 / cap fit 측 가능성 큼.

### 11.5 DC drift -185mV 측 community 측 troubleshooting

OpenBCI Forum + EEG Hacker blog + EEG-Setup doc 측 표준 가이드:

1. **Bandpass 0.5–45 Hz 측 DC offset 제거** — ADS1299 측 raw measurement 측 mV-range DC offset 측 normal. GUI 측 default filter ON 인지 confirm.
   - cite: `EEG-Setup.md` L94-L100, EEG Hacker `eeghacker.blogspot.com/2014/04/openbci-measuring-electrode-impedance.html`
2. **Impedance 5-15 kΩ 측 target** — Ten20 paste + scalp prep (alcohol wipe + gentle abrasion). 15kΩ 초과 측 paste 보충 + reposition.
3. **60-90초 안정 대기** — vendor docs 측 명시적 시간 X, 그러나 community thread (`forum/discussion/3726`) 측 "wait 1-2 min for impedance to settle" 흔한 권장.
4. **Reference electrode 단단히 부착** — `Troubleshooting/01-MinimizingNoise.md` L20-L22: "Ensure that your electrodes are connected securely (**especially your reference electrode**)!"
5. **Ear clip 측 thin earlobe contact 약함 측 mastoid + Gel snap electrode 교체** — community 측 흔한 fix.

### 11.6 Y-Splitter 측 official 의미

`shop.openbci.com/products/...` 측 product 명: "**Y-Splitter Cable**" — Cyton+Daisy bundle 측 standard accessory.
- 1× female (single end) → ear clip (gold cup) 측 plug
- 2× female (dual end) → Cyton bottom SRB + Daisy bottom SRB 측 plug
- 의도: 두 ADS1299 chip 측 SRB2 측 외부 short → single common reference

cite: `011-Daisy_Getting_Started_Guide.md` L25-L27 (image link) + `Gelfree_Electrode_Cap_Tutorial.md` L36

### 11.7 다음 cycle 권장 (audit 결과 기반)

1. **wiring 측 변경 X** — 정통 setup 유지
2. **mastoid + Gel snap electrode 측 transition** (이미 doc v2 측 권장) — DC drift 측 가장 가능성 큼
3. **GUI bandpass filter 0.5-45Hz + 60Hz notch ON 측 확인** — raw npy 측 unfiltered 측 -185mV 측 expected 측 가능
4. **impedance check (Z command)** — 16/16 < 15kΩ 측 target
5. **60-90s 평형 대기 측 blink session 후 Berger 측 sequential 측정** — blink robust → Berger 측 reference health proxy
6. **reference 위치 측 좌우 swap test** — 한쪽 mastoid 측 contact 약하면 SRB ↔ BIAS swap 시도 (모든 channel 측 polarity flip 측 software 측 -1 곱)

### 11.8 추가 honest C3 caveats (audit 측)

6. **vendor docs 측 일부 outdated** — Mark IV 2022 update 측 최신, 그러나 "32bit Board" 명칭 측 일부 legacy doc 측 잔존. V3 schematic 측 2015-02-16 마지막 update — passive component value 측 silently changed 가능성 부재 검증.
7. **hardware revision drift** — Cyton "Bundle" 측 2023+ 측 lithium battery 측 transition. SRB/BIAS pin 측 layout 측 rebrand 후 변경 X (`READ_ME.md` 명시), 그러나 user-shipped board 측 V3.x minor revision 측 cross-check 측 silkscreen "OpenBCI V3" 측 직접 확인 권장.
8. **한국어 docs 부재** — OpenBCI docs 측 영어 only. community Korean translation 측 부재. 본 doc 측 한국어 quick-ref 가치 큼.

---


**local clone** (`/Users/ghost/core/anima/references/`):
- `Documentation/website/docs/GettingStarted/Boards/011-Daisy_Getting_Started_Guide.md`
- `Documentation/website/docs/GettingStarted/Biosensing-Setups/01-EEG-Setup.md`
- `Documentation/website/docs/AddOns/Headwear/01-Ultracortex-Mark-IV.md`
- `Documentation/website/docs/AddOns/Headwear/04-Electrode_Cap_Tutorial.md`
- `Documentation/website/docs/AddOns/Headwear/Gelfree_Electrode_Cap_Tutorial.md`
- `Documentation/website/docs/AddOns/Headwear/03-Headband_Tutorial.md`
- `Documentation/website/docs/Troubleshooting/01-MinimizingNoise.md`
- `Documentation/website/docs/Software/OpenBCISoftware/02_GUI_Widget_Guide.md` (SRB1/SRB2 channel-setting 정의)
- `Documentation/website/docs/Cyton/02-Cyton.md` (Daisy module specs)
- `V3_Hardware_Design_Files/OpenBCI Cyton Designs/OpenBCI 32bit.sch` (DesignSpark, 2015-02-16)
- `V3_Hardware_Design_Files/OpenBCI Daisy Designs/OpenBCI Daisy.sch` (DesignSpark, 2015-02-16)

**live web** (2026-05-03 fetched, 2025-05-09 last updated):
- `docs.openbci.com/GettingStarted/Boards/DaisyGS/`
- `docs.openbci.com/GettingStarted/Biosensing-Setups/EEGSetup/`
- `docs.openbci.com/AddOns/Headwear/Ultracortex-Mark-IV/`
