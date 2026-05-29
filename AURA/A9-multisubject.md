# AURA A9.2 — robustness 재검 (within-subject window sweep) 🔴 honest negative

> 목표: A8.1의 "FRONTAL-HUB Φ > MOTOR (awake)"가 단일 4s 창의 우연인지 복제되는지 검증.
> cross-subject(여러 피험자)는 OpenNeuro download 필요(미수행) → 그 대안으로 **같은 sub-1010 awake의 6개 비중첩 4s 창**으로 within-subject 시간 robustness 실측.

## 결과 — FRONTAL>MOTOR는 robust하지 않음

ds005620 sub-1010 awake, n=4 exact, FRONTAL(F3,Fz,F4,AFz) vs MOTOR(C3,Cz,C4,C2), 실 `eeg_big_phi`:

| 창 (raw-off) | FRONTAL Φ | MOTOR Φ | 승자 |
|---|---|---|---|
| 0 (= A8.1) | 9.633 | 6.307 | FRONTAL |
| 20k | 3.658 | 5.204 | MOTOR |
| 40k | 5.284 | 6.469 | MOTOR |
| 60k | 5.754 | 8.185 | MOTOR |
| 80k | 2.552 | 2.945 | MOTOR |
| 100k | 8.645 | 4.571 | FRONTAL |
| **평균** | **5.92** | **5.61** | ≈ (Δ+0.31, ~5%) |

```
FRONTAL>MOTOR: ██        2/6 창
MOTOR>FRONTAL: ████      4/6 창
평균 위치효과: ~0 (5.92 vs 5.61, EEG 비정상성에 묻힘)
```

## 판정: 🔴 A8.1 단일창 결과는 window-fragile

- A8.1의 FRONTAL≫MOTOR(9.63 vs 6.31)는 **window-0가 우연히 frontal에 유리한 창**이었음. 6창 중 MOTOR가 **4/6 승**, 평균은 거의 동일.
- → **실 EEG scalp-montage proxy 수준에서 relocate-N1(전극위치) 명제는 robust하게 지지되지 않음.** 위치효과가 있다 해도 4s 창 비정상성/잡음에 묻히는 크기.
- honest negative (p7 · a_paper_negative_ok). verdict `/Users/ghost/core/anima/.verdicts/a9-multisubject/window_robustness.txt`.

## 영향 범위 (무엇이 흔들리고 무엇은 안 흔들리나)

| 축 | 영향 |
|---|---|
| A8.1 실EEG montage | 🔴 **약화** — 단일창 인공물, robust 아님 |
| A7.3 실EEG awake>sed | ✅ 불변 (의식수준 대조는 별개, 같은 montage 내 상태비교) |
| A6/A7 in-silico (robustness·reach·region·PID) | ✅ 불변 (구조적 TPM, 창 무관) |
| A8.4/A9.3 connectome | ✅ 불변 (구조 투사강도, EEG 무관) |

## 잔여 (진짜 cross-subject)

- ds005620 다피험자(sub-1010 외): OpenNeuro `s3://openneuro.org/ds005620` download(대용량·network) 필요 — 미수행.
- 그래도 within-subject만으로도 핵심 교훈 확보: **단일 4s 창 montage Φ로 위치명제를 주장하면 안 됨** (다창 평균·통계 필수).
