# AURA A10.1 — 다창 위치효과 통계 (실EEG 축 결정적 마무리) 🔴

> A9.2 교훈("단일창 주장 금지")의 정공 마무리 — FRONTAL vs MOTOR를 **전 300s에 걸친 10창**에서 측정해 paired 통계로 위치효과 유무를 확정.

## 결과 — 위치효과 통계적으로 없음

ds005620 sub-1010 awake, n=4 exact, 10창(전 녹화 스팬), 실 `eeg_big_phi`:

| off | FRONTAL | MOTOR | F−M |
|---|---|---|---|
| 0 | 9.633 | 6.307 | +3.33 |
| 140k | 10.630 | 6.489 | +4.14 |
| 280k | 4.348 | 3.424 | +0.92 |
| 420k | 5.788 | 5.422 | +0.37 |
| 560k | 2.809 | 4.388 | −1.58 |
| 700k | 6.609 | 9.192 | −2.58 |
| 840k | 5.670 | 2.270 | +3.40 |
| 980k | 2.268 | 2.543 | −0.28 |
| 1120k | 2.844 | 2.991 | −0.15 |
| 1260k | 2.927 | 7.947 | −5.02 |
| **평균** | **5.353** | **5.097** | **+0.26** |

```
FRONTAL>MOTOR: █████ 5/10
MOTOR>FRONTAL: █████ 5/10   ← 정확히 5:5
```

| 검정 | 값 | 판정 |
|---|---|---|
| paired diff 평균 | +0.255 (sd 2.88) | ~5%, 노이즈 내 |
| paired t(9) | +0.280 | \|t\|<2.26 → **유의 아님** (.05) |
| sign test | 5/10 positive | **p=1.0** (방향성 없음) |

## 판정: 🔴 relocate-N1, 실 scalp-EEG proxy에서 미지지 (확정)

- **위치효과 없음** — FRONTAL-hub와 MOTOR가 통계적으로 구분 불가(5:5, t=0.28 n.s., p=1.0).
- A9.2의 6창(0–100k clustered, 2/6)보다 **전-스팬 10창(5/5)이 정직한 추정** — 초반 클러스터가 우연히 MOTOR 쪽이었을 뿐, 전체로는 정확히 무효과.
- verdict `/Users/ghost/core/anima/.verdicts/a10-window-stats/test.txt`. honest negative (p7·a_paper_negative_ok).

## AURA 실EEG 축 종결 + 비대칭 재확인

```
구조 모델 (in-silico A6/A7 + connectome A8.4/A9.3)  →  ✅ relocate 일관 지지
실 scalp-EEG proxy (A8.1→A9.2→A10.1, 10창 통계)     →  🔴 위치효과 없음 (확정)
```

→ **핵심 교훈**: "칩 위치만 바꿔 전뇌 통제"는 **이론·구조에선 그럴듯하나, 손에 쥔 실제 인간 scalp-EEG로는 위치효과가 측정되지 않는다.** 이 비대칭이 AURA의 가장 정직한 결론.

## 잔여 (A10.1로 실EEG 단일피험자 축은 닫힘)

- 남은 건 **다피험자**(OpenNeuro download) — single-subject(sub-1010)에서 무효과지만 N=1. 다피험자서도 무효과면 강한 negative, 일부서 효과면 subject-dependent.
- intracortical(N1 실제 깊이)는 scalp-proxy로 영원히 닫을 수 없는 본질 gap — 동물/임상 침습 데이터 필요.
- 이 negative는 a_paper_negative_ok 후보: "scalp-EEG IIT4-Φ 위치효과 부재 — 구조모델↔실측 비대칭".
