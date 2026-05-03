# Fp1 chronic high-freq noise — 진단 + 사용자 손 작업 가이드

작성일: 2026-05-03
대상: OpenBCI Cyton + Ultracortex Mark IV + Y-Splitter (mastoid reference) — Fp1 channel only
관련 doc:
- `anima-eeg/docs/cyton_daisy_wiring_diagram_2026_05_03.md`
- `anima-eeg/docs/electrode_adjustment_16ch_concurrent_2026_04_29.md`
- `anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md`

## 0. 발견 (분석 BG aed68edd)

- Fp1 (Cyton N1P, 회색 wire) — REST/Blink/Math 측 모든 phase 76-94 peak count
- REST 측 자연 깜빡 1-2회/30s 예상 vs 실제 76+ peaks → 70배 초과
- broadband chronic noise dominated (단일 spike 아님)
- contrast: Fp2 (Cyton N2P, 보라 wire) — REST 측 0 peaks (clean)
- 동일 frontal montage / 동일 보드 / 동일 reference — 한 channel 측만 noise
- → reference / electrode contact / wire / connector 측 single-source 문제 의심

## 1. 진단 가능성 6 ranked (likelihood × 검증 용이도)

| Rank | 가능성 | likelihood | 검증 용이도 | 비고 |
|------|--------|-----------|------------|------|
| **(a)** | Fp1 cap 전극 측 contact 약함 | **HIGH** | 쉬움 (impedance) | paste 부족 / 머리카락 끼임 / dry gel — 가장 흔한 원인 |
| **(b)** | Fp1 wire 측 보드 N1P 측 헐렁 | HIGH | 쉬움 (재꽂기) | Y-Splitter 측 인접 wire 측 충돌 시 빈번 |
| **(e)** | SRB ear clip / mastoid reference contamination | MED | 보통 (swap test) | reference 측 약하면 frontal channel 측 가장 먼저 영향 — but Fp2 측 깨끗하므로 partial unlikely (단, mastoid 측 단일 측 ipsilateral 영향 시 가능) |
| **(f)** | Eye blink EOG + frontalis EMG 측 직접 hit | MED | 보통 (REST 측 안정 측정) | Fp1 측 hair-line 측 가까움 — but REST 76 peaks 측 blink 빈도 측 너무 높음 → chronic noise 측 다름 |
| **(c)** | Fp1 cap-side wire 측 broken (내부 단선) | LOW-MED | 보통 (swap) | 외관 측 멀쩡 측 내부 conductor 측 fatigue — Bundle spare cable 측 swap 측 verify |
| **(d)** | Cyton N1P pin 자체 측 fault | LOW | 어려움 (swap) | 가능성 낮음 — but (a)(b)(c) 측 모두 배제 후 verify |

## 2. 진단 sequence 4 step

**Step 1 — Impedance check**
- `pixi run impedance-check` (또는 `electrode-helper`)
- Fp1 측 specifically 확인: 다른 ch 측 평균 (예: 5kΩ) vs Fp1 측 (예: 25kΩ) 비교
- threshold: > 20kΩ 또는 다른 ch 측 평균 측 3배 이상 → contact 문제 confirmed

**Step 2 — Visual inspection**
- Cap 측 Fp1 위치 (Fp1 = forehead 좌측, 눈썹 위 ~3cm)
- paste 측 충분히 발렸는지 — 마른 흰 가루 X, 촉촉한 gel ✓
- 머리카락 측 electrode 측 사이 끼었는지 (앞머리 / 잔머리)
- electrode 측 cap hole 측 정확히 안착 확인

**Step 3 — Wire continuity**
- Cyton N1P (회색 wire) 측 보드 측 단단히 꽂기 — 살짝 흔들어 헐렁 X 확인
- Y-Splitter 측 측 Fp1 wire 측 인접 wire 측 충돌/꺾임 X 확인
- cap 측 connector 측 (cap-side) 측 단단히 꽂기

**Step 4 — Swap test (Step 1-3 측 fix 안 될 시)**
- Fp1 wire 측 Cyton N2P 측 swap (Fp2 자리)
  - noise 측 N2P 측 따라가면 → wire / cap electrode 측 문제
  - noise 측 N1P 측 그대로 남으면 → Cyton N1P pin 측 fault
- 반대로 Fp2 wire 측 N1P 측 swap 측 cross-verify

## 3. Fix 가이드 ranked (적용 우선순위)

| 우선순위 | Fix | 대상 가능성 | 적용 시간 |
|---------|-----|-----------|----------|
| **1st** | Ten20 paste 측 Fp1 측 over-fill (2-3배), 머리카락 비키기 | (a) | 30초 |
| **2nd** | wire 측 보드 N1P + Y-Splitter 측 단단히 재꽂기 | (b) | 10초 |
| **3rd** | SRB ear clip 측 contact 강화 (mastoid 측 Gel Electrode 추가) | (e) | 1분 |
| **4th** | Bundle spare cable 측 Fp1 wire 측 swap | (c) | 2분 |
| **5th** | Bundle spare cap electrode 측 N1P 측 connector 측 swap | (d) | 3분 |
| **6th** | Fp1 측 사용 안 하고 Fp2 측만 활용 (paradigm-level workaround) | (f) | code-side, 손 작업 X |

## 4. 즉시 적용 사용자 손 작업 (3-step)

**가장 빠른 fix 우선 — 1회 1 fix 만 적용 (multi-fix 동시 측 attribution 어려움)**

1. **Fp1 측 paste 보충**
   - cap 측 Fp1 hole 측 syringe 측 Ten20 paste 측 추가 (기존 양 측 2-3배)
   - 머리카락 측 electrode 측 사이 측 정리 — 잔머리 측 비키기

2. **60-90s 평형 대기**
   - paste 측 skin 측 stabilize 대기 — 측정 측 너무 빨리 시작 X
   - 그 동안 wire 측 보드 측 단단히 꽂혔는지 시각 확인

3. **Impedance check 측 verify**
   - `pixi run impedance-check` 측 Fp1 측 25kΩ → 5kΩ 도달 verify
   - 도달 시 → Step 2 (blink session 재측정) 진행
   - 도달 X 시 → Section 3 측 2nd fix 적용

## 5. 3 honest C3 caveats (raw#10)

1. **chronic noise 측 root cause 측 single capture 측 진단 측 limit** — 76+ peaks 측 raw signal 측 broadband 측 dominated 시 (a)/(b)/(e) 측 모두 fit 가능. 검증 측 sequential fix + verify 필요.

2. **하나만 적용 후 verify** — paste + wire + reference 측 동시 측 수정 시 어느 fix 측 실제 효과 측 attribution 불가능. 1 fix → impedance check → re-record → 다음 fix 순서 측 엄격 준수.

3. **(f) Eye blink EOG 측 inherent** — Fp1 측 frontal pole 측 EOG 측 본질적으로 high. REST 측 76 peaks 측 너무 많아 chronic noise 측 dominant 측 추정하지만, paste/wire fix 후에도 Fp1 측 Fp2 보다 peak count 측 약간 높음 측 normal (anatomical asymmetry / dominant-eye blink).

## 6. 다음 cycle 권장

**Fp1 fix 후 재측정 protocol**:

1. Section 4 (3-step) 적용 → impedance verify
2. REST 30s 재측정 (eyes-closed, no blink intentional)
3. analyze BG (aed68edd 후속) 측 Fp1 peak count 측 76 → ? 비교
4. Fp1 < 5 peaks/30s 도달 시 → Fix successful → blink/math session 재측정 진행
5. 도달 X 시 → Section 3 측 2nd fix (wire 재꽂기) 적용 후 재측정
6. 5th fix 까지 진행 후에도 fix X 시 → (f) workaround 측 paradigm-level 측 Fp2 측만 활용

**Spare bundle 측 swap test 측 (4th-5th fix)** 측 필요 시 별도 doc 측 land — 본 doc 측 1st-3rd fix 측 hand-work 측 cover.
