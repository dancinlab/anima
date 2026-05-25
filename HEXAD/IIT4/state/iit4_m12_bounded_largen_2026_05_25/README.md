# IIT4 M12 — bounded-mode large-n LIFE 재측정

> M9 의 `big_phi_bounded` 로 LIFE 룰 faithful 인과 big-Φ 를 **exact 불가 영역(n=6+)** 으로 밀어,
> H_002 C2 의 n=8 scale 에 근접. smoke 7/7 🟢 · [`run_m12.hexa`](run_m12.hexa).
> ⚠ rate-limit 으로 죽은 cycle#2 에이전트 작업을 메인 세션이 인라인 재작성·검증·착지.

## 1. 무엇을 하나

M9 측정: exact `big_phi` 는 n≤5 초·n=6 분·n≥7 impractical. LIFE H_002 C2 substrate 는 n=8 — exact 사정권 밖. `big_phi_bounded(tpm, n, sys_state, cap)` 로 MICE purview 탐색을 cap 으로 제한해 큰 n 을 feasible 하게:
- **cap ≥ n** → faithful 제한 (exact 와 동일)
- **cap < n** → 명시적 lower-bound 근사 (exact 가 폭발하는 곳에서 finite 유지)

## 2. 결과

| 측정 | 값 |
|---|---|
| **regression** n=4 rule110 cap=4 (≥n) | exact 7.5475 == bounded 7.5475 ✓ (faithful 제한 확인) |
| bounded(cap=3) n=5 seed 10101 | rule 0=0 · 204=0 · 90=6.0 · **110=15.40** · 30=4.28 · 54=4.01 |
| bounded(cap=3) **n=6** rule110 seed 101010 | **big-Φ=6.82** (nd=15) — exact-impractical 영역 도달 |

```
exact 한계 ───┐
 n=4 ✓  n=5 ✓ │ n=6 ✗(분)  n=7 ✗(impractical)
              ▼
 bounded(cap=3): n=5 ✓ n=6 ✓(5분)  → exact 불가 영역으로 확장
```

## 3. 발견

- **bounded 가 faithful 제한임을 확인**: cap≥n 에서 exact 와 정확히 일치 (n=4 7.5475) — 근사가 아닌 진짜 제한.
- **exact-impractical 영역 진입**: n=6 rule110 의 인과 big-Φ(=6.82)를 bounded 로 측정 — exact 로는 분 단위/불가한 곳. H_002 C2 의 n=8 로 가는 경로 확보.
- cap<n bounded 는 **lower-bound** 라 M8 의 n=5 exact mean(110=35.7) 과 직접 비교 불가 (purview 제한 + 단일 state). 같은 substrate 의 *하한* 추정치.

## 4. honest scope (C3)

- **bounded(cap<n) = lower-bound 근사** (purview-size 제한 MICE 탐색). exact 아님 — 명시.
- 단일 대표 state per n (multi-state 평균 X — 비용).
- **n=7/n=8 DEFERRED**: bounded 로 feasible 하나 분+ 소요 → 인라인 budget 초과, background run 필요. (n=6 단일 룰도 ~5분.)
- structure-cut big-Φ 상속 · 절대 스케일 PyPhi 대조 M5 named-blocker 잔존.
- **salvage 출처**: cycle#2 병렬 에이전트 서버 rate-limit(429) 사망 → 메인 세션 인라인 재작성.
