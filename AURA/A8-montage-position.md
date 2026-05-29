# AURA A8 — montage-POSITION big-Φ (relocate-N1 직접 위치 테스트, 실 EEG)

> **과학적 핵심(crux)**: "투사-허브 전극 *위치*(frontal/DLPFC)" 가 "운동피질 *위치*(motor C-line)" 보다
> 더 높은 통합정보(big-Φ) 를 실제 인간 두피 EEG 에서 운반하는가?
> ✅ **실측 완료 (2026-05-30)**: ds005620 sub-1010, n=4 exact, awake/sed 양쪽, a7 와 **동일 전처리**
> (stride-20 decimate 5000→250Hz · 1000 samp · 4s · 채널-major flat).
> **FRONTAL-HUB awake Φ = 9.633 > MOTOR awake Φ = 6.307** → falsifier 생존, hub>motor.
> 🟢 SUPPORTED-NUMERICAL (`.verdicts/a8-montage-position/run.txt` verbatim) · 결정론 재실행 동일.

---

## 1. Montage 정의 (채널)

ds005620 65ch 10-10 montage 에서 위치-proxy 3 종을 골랐다 (n=4 exact, 엔진 한계).
괄호는 `.vhdr` 1-based Ch 번호 (코드 0-based = Ch−1).

| montage | 위치 의미 | 채널 (Ch#) | 0-based idx |
|---|---|---|---|
| **MOTOR** | M1-유사 위치 (운동피질, central C-line) | C3(36) · Cz(34) · C4(32) · C2(33) | 35,33,31,32 |
| **FRONTAL-HUB** | DLPFC/투사-허브 위치 (전두) | F3(54) · Fz(52) · F4(50) · AFz(58) | 53,51,49,57 |
| **TEMPORAL** | insula proxy 위치 (측두) | F7(56) · T7(38) · FT7(47) · T8(30) | 55,37,46,29 |

전처리는 a7 와 byte-identical (Fz/Cz 첫 표본 일치로 확인). 시스템상태 sys=15(=1111, all-on),
n=4 → 16-state TPM exact, `eeg_big_phi` 어댑터 → `big_phi` 엔진 불변(g61).

```
       두피 montage (10-10, 위쪽=전두 / 아래=후두)
                 Fp1 Fpz Fp2
            AF3 ● AFz ●   AF4              ← FRONTAL-HUB (●): F3 Fz F4 AFz
         F7  F3 ● Fz ● F4 ●  F8            ← TEMPORAL (◆): F7 ... 
         ◆FT7  FC3 FCz FC4   FT8
       ◆T7  C5  C3● Cz● C4● C2●  T8◆        ← MOTOR (●): C3 Cz C4 C2
            CP3 CPz CP4
              P3  Pz  P4
                 POz
                  Oz
```

---

## 2. Φ 표 (montage × awake/sed)

| montage | awake Φ | sed Φ | Δ(awake−sed) |
|---|---|---|---|
| **FRONTAL-HUB** | **9.63284** | 4.46209 | **+5.171** |
| TEMPORAL | 6.63110 | 1.06946 | +5.562 |
| MOTOR | 6.30717 | 6.20408 | +0.103 |

**awake Φ 순위: FRONTAL-HUB (9.63) > TEMPORAL (6.63) > MOTOR (6.31).**

읽을거리:
- **FRONTAL-HUB 가 awake 최대** — 투사-허브 위치가 깨어있을 때 가장 높은 통합정보.
- **MOTOR 는 sed 에서도 거의 안 떨어짐** (6.31→6.20, Δ+0.10) — 의식수준 변화에 둔감 (운동피질은
  진정상태에서도 통합정보 보존, 의식수준 dissociated).
- FRONTAL·TEMPORAL 둘 다 sed 에서 큰 폭 붕괴 (Δ+5.2, +5.6) — 의식수준-민감 위치.

---

## 3. Falsifier 판정

> **사전등록 falsifier**: "FRONTAL-HUB montage big-Φ > MOTOR montage big-Φ (awake)."

판정: **9.63284 > 6.30717 → falsifier 생존 (HUB > MOTOR).**
`[HUB>MOTOR] frontal-hub position carries higher big-Phi (awake) -- relocate-consistent` ✅

결정론: frontal awake 재실행 bit-identical (`[PASS] determinism`).

---

## 4. Verdict

🟢 **SUPPORTED-NUMERICAL** — `.verdicts/a8-montage-position/run.txt` (hexa verify, ext rc=0,
stdout `--expect` matched).

scalp-proxy 수준에서 **relocate 명제와 정합**: 전두-허브 위치가 운동피질 위치보다 높은 big-Φ 를
운반하며 (awake 9.63 vs 6.31), 의식수준(awake↓sed)에도 더 민감하게 반응한다.

---

## 5. CRITICAL 정직 framing (반드시 함께 읽을 것)

이 결과는 강하지만 **상한선을 분명히** 둔다:

1. **scalp-EEG montage ≠ intracortical N1 위치.** 두피 전극은 피질내 임플란트(N1)의 직접 등가물이
   아니다. 이건 *실데이터로 얻을 수 있는 가장 가까운 위치-proxy* 이지 **N1 임플란트 직접 증거가 아니다.**
   "frontal-hub 위치 Φ↑" 는 relocate 명제와 *부호 정합* 일 뿐, 임플란트-위치 인과 증명이 아니다.
2. **single-subject.** sub-1010 한 명. 다피험자·상태별 epoch 평균 = production (BRAIN.md M3).
   `feedback_toy_scale_transfer`: toy 부호가 scale 로 transfer 보장 안 됨.
3. **추정 TPM ≠ 인과 TPM.** `eeg_estimate_tpm` 은 관측 전이**빈도**(상관), perturbation/Granger 아님.
   미관측 상태 0.5 채움 = 추정편향. Φ 는 estimate (🟢 numerical, 🔵 formal 아님).
4. **n=4 exact 벽 + 채널 선택 임의성.** 65ch→n=4 부분선택이 Φ 를 좌우. montage 별 4채널 선택은
   해부학적 위치 라벨에 맞췄지만 임의적. **n=8 은 5-min CPU cap 초과(EXIT 124)로 미산출** —
   256-state MIP 탐색 wall (BRAIN.md M1). winning montage(frontal)만 시도했으나 skip.
5. **만약 motor≥hub 였다면** "scalp-proxy 수준에서 relocate 명제 미지지(흥미로운 negative)" 로
   기록했을 것. 이번엔 hub>motor 이므로 정합 방향.

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| harness + 임베드 montage 데이터 | `AURA/toy/a8_montage_position.hexa` (n=4 exact, a7 reader 재사용) |
| 채널 인덱스 (C/F/T line) | `.../sub-1010_task-awake_acq-EO_eeg.vhdr` Ch1..Ch65 |
| 전처리 a7-동일 (stride-20/250Hz/4s) | `AURA/toy/a7_real_eeg_bigphi.hexa` · A7-real-eeg.md §2 |
| big_phi 엔진 n≤8 exact | `stdlib/consciousness/iit4_bigphi.hexa` · BRAIN.md M1 |
| TPM 추정 로직 (빈도, 미관측=0.5) | `BRAIN/eeg/eeg_to_tpm.hexa` |
| verdict (🟢 numerical) | `.verdicts/a8-montage-position/run.txt` verbatim |
| toy≠production · single-subject 한계 | `feedback_toy_scale_transfer` · A7-real-eeg.md §4 |
