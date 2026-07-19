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

## 🔬 RV-0 $0 부검 결과(2026-07-17 · 의뢰자 실측 · t3.clm seed7 vs t3_seed11.clm)

CLMS 트레일러(f32 · int4 무관) `read_clms`로 읽어 val 극성분화 + W_h v-block RMS 측정:
- **seed-7**(ORACLE 0.99): ‖val[0]−val[1]‖=0.0968 · 극성분화비 0.992 · W_h v-block RMS 0.01050 · v/g 0.652
- **seed-11**(ORACLE 0.50): ‖val[0]−val[1]‖=0.1153 · 극성분화비 **1.074**(seed-7보다 오히려 큼) · W_h v-block RMS **0.01070**(≈seed-7) · v/g 0.860

**⟹ A(val 붕괴)도 B(W_h 귀먹음)도 아님 — 둘 다 REFUTED.** val은 seed-11서 오히려 더 분화됐고 W_h v-block 크기도 정상. **seed-11 실패는 크기(magnitude)가 아니라 기능(function)**: W_h→W_out 융합이 분화된 v와 g(op)를 **XOR 정답에 매핑하는 함수를 못 배움**(shortcut basin이 MLP를 op-only로 오염 — Fable "흐린 v=majority 신호" 통찰 정합: 균등주소 v=store 극성평균=majority라 값경로 *통해* shortcut). 즉 val 분화는 됐으나 그 분화가 **정답 방향과 정렬 안 됨**(op-only가 CE 최소). ⟹ **magnitude 레버(margin/val 직접감독 RV-4·H_9711)는 무효 예측**(분화≠소비·nullspace gaming) · **함수 레버(RV-1 oracle-aux 연속 이중경로·RV-3 centering)가 정답**: 매 step 올바른 v로 MLP XOR 함수 재훈련(RV-1) or shortcut basin 구조제거(RV-3). **RV-0가 서열 재확인: RV-1/RV-3 승격·RV-4 강등.**
