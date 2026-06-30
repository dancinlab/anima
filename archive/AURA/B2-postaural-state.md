# AURA B2 — 귀뒤 awake/sed 의식수준 검출? 🔴 NULL

> B1(귀뒤가 피질과 동등 big-Φ)에 이어, 귀뒤 montage가 **의식수준 변화(각성 vs 진정)**를 잡는지 검증. = 귀뒤 웨어러블의 임상적 가치(마취/수면 모니터) 검정.

## 결과 — n=4 scalp에선 검출 안 됨 (또 window-fragile)

ds005620 sub-1010, 귀뒤(TP9,TP10,T7,T8), n=4 exact, awake vs sed:

| 표본 | awake 귀뒤 | sed 귀뒤 | Δ | 판정 |
|---|---|---|---|---|
| 초반 5창 | 6.90 | 4.81 | +2.09 (4/5) | ← favorable-window |
| **전체 10창** | **5.378** | **6.226** | **−0.85** | 6/10, t(9)=−0.53 **n.s.** |

→ 초반 5창의 "awake>sed Δ+2.09"는 **또 favorable-window 인공물**. 전체 10창에선 Δ−0.85 (오히려 sed 높음), 유의 아님. verdict `.verdicts/b2-postaural-state/awake_vs_sed.txt`.

## 판정 + 메타 교훈

🔴 **귀뒤 n=4 big-Φ는 awake/sed를 신뢰성 있게 구분 못 함.** A10.1(위치 null) + B2(상태 null) 종합 메타:

```
단일 4s 창 n=4 scalp big-Φ
   ├─ 위치 대조 (FRONTAL vs MOTOR)  → null (A10.1)
   ├─ 상태 대조 (awake vs sed)       → null (B2)
   └─ 공통 원인: EEG 비정상성이 4s 창마다 Φ를 휘저음 → 단일창 주장은 다 cherry
```

- **자기검증으로 잡음**: 5창에서 멈췄으면 "귀뒤가 의식수준 잡는다"(거짓양성) 발표할 뻔. 10창으로 확장하니 null. (A9.2 교훈 재적용)
- A7.3 midline awake>sed(Δ+0.75, 단일창)도 같은 window-fragility 의심 → 그것도 다창 재검 필요(A7.3 retro-qualify).

## 함의 — 귀뒤 웨어러블엔 다른 feature가 필요

- IIT4 big-Φ(n=4, 단일창)는 scalp 의식수준 모니터로 **부적합**(노이즈 지배). 
- 임상 의식수준(마취심도)엔 band-power·entropy·PCI 등 **다창 평균 feature**가 표준 — 단일창 big-Φ가 아님.
- 귀뒤 위치 자체는 유효(B1: 통합정보 피질과 동등)하나, **측정 metric을 바꿔야**(다창 통계 or band feature).

## honest

single-subject(sub-1010) · n=4 exact(n≥6 wall) · scalp-proxy · 단일창 비정상성 지배. B1의 "동등"은 분포 평균 비교라 유효, B2의 "상태검출"은 단일창 metric 한계로 null.
