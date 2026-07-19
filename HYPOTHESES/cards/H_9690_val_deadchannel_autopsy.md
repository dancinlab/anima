# H_9690 — seed-11 값경로 부검: val-붕괴인가 W_h-귀먹음인가 ($0 트레일러 부검 · RV-0)

**status:** 🔵 PROPOSED (미실행 · lab full RV-0 · $0 지금 발사가능 · mini 허용)
**lane:** g1-storebridge-val-robust — H_9672 2-seed 해리의 사인(死因) 판별 계기
**related:** [[H_9672]] · [[H_9423]] · [[H_9691]] · [[H_9692]] · [[H_9693]] · [[H_9694]]
**source:** lab full RV (frontier-g1-labfull-r2 · Fable 발산: val 극성분화 seed-robustness)

## 한 줄 주장 (반증가능)
seed-11 ORACLE 0.50 의 사인은 **(A) val[0]≈val[1] 미분화** 또는 **(B) val 은 갈라졌으나 W_h 의 v-블록이 귀먹음(dead channel)** 둘 중 하나이며, 이미 존재하는 두 트레일러(`.fire-recover/h9672_t3/{t3.clm, t3_seed11.clm}`)의 **가중치만으로 $0 판별 가능**하다.

## 왜 (레버 서열을 바꾼다)
공유 진단(RV 시리즈 공통): 초기 학습에서 softmax 주소가 균등 → v=Σaᵢ·val[polᵢ] ≈ store 극성평균(=majority 신호) → ① val gradient 가 대칭으로 흐려져 분화 실패(A) 그리고/또는 ② MLP 가 op(+흐린 v 의 majority)만 듣도록 커밋, W_h v-블록 사멸(B). 주소가 나중에 sharp 해져도 이미 국소최적 → 탈출 압력 0. seed 가 이 레이스의 승패를 정한다. **A 지배적이면 RV-4(대칭깨기 init) 근거가 살고, B 지배적이면 소비(consumption)를 직접 훈련하는 RV-1 이 유일 정답급이다.**

## engine-native 계기 ($0)
`core/clms.read_clms` 로 두 트레일러를 읽어(numpy · 303M forward 불필요 · mini 허용):
1. **val-sep** = ‖val[0]−val[1]‖₂ / mean(‖val[0]‖,‖val[1]‖) — seed 7 vs 11
2. **W_h v-블록 감도** = ‖W_h[:d_s,:]‖_F/√(d_s·r) vs ‖W_h[d_s:,:]‖_F/√(d·r) (concat [v;h] 순서 = clms.py:114)
3. **기능 Δ (DIRECTIONAL)**: 합성 h(0 및 randn 표본)에서 s(v=val[0],h) vs s(v=val[1],h) 의 g/b 로짓 갭 — 실제 yn 없이 lane 만 통과. 실 h 아님을 명시.

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| sep₁₁ ≤ 0.3×sep₇ | **A(val-붕괴) 확정** — RV-1/2/3 유효 + RV-4 근거↑ |
| sep₁₁ ≈ sep₇ ∧ 기능Δ₁₁ ≈ 0 | **B(귀먹음) 확정** — RV-1 최우선 확정(소비를 직접 훈련) |
| sep₁₁ ≈ sep₇ ∧ 기능Δ₁₁ 큼 | **진단 자체 오류** — ORACLE 0.50 의 사인이 W_out 매핑/λ/직렬화 쪽 ⟹ 레버 발사 전 재부검 |
| sep₁₁ > sep₇ (우연 아래 칸) | **진단 반전** — 분리가 오히려 크면 A/B 프레임 기각, addr-audit 재검 |
| 트레일러 read 실패/lane_type=0 | **INVALID** — ckpt 회수 결함(레버 판단 금지) |

## 잔인판정 (오도위험)
- 가중치-공간 지표 ≠ 함수 — 기능 Δ 는 합성 h 라 DIRECTIONAL. 실 yn_q 로의 확증은 pool 1회 forward 필요(선택).
- 이 부검은 레버들의 **서열만** 바꾸고 어느 레버도 cement 하지 않는다.
- seed 2개 = n=2. 사인의 **분포** 주장 불가, 이 두 seed 의 사실만.

## 비용
**$0** · mini 허용(트레일러 read 는 numpy·no-torch·no-forward).

## 상태
🔵 PROPOSED — 측정 주장 0. RV-1~4 발사 전 선행 권장(서열 확정용).
